"""CareerPilot AI — Career Roadmap Module
=======================================
Generates a structured career progression timeline with:
- Attractive visual milestone indicators in teal
- Interactive task completion checkboxes with live progress tracking
- Phase-by-phase learning goals, essential skills & curated resources
- Powered by Google Gemini structured response
"""

from typing import List, Optional
import streamlit as st
from pydantic import BaseModel, Field
from utils.gemini_helper import generate_structured_response


class RoadmapTask(BaseModel):
    """A specific actionable task within a milestone phase."""
    task_id: str = Field(description="Unique string identifier like 'p1_t1'.")
    title: str = Field(description="Actionable title of the task.")
    description: str = Field(description="What to build, learn, or execute.")
    recommended_resource: str = Field(description="Course, doc, or project suggestion.")


class RoadmapPhase(BaseModel):
    """A milestone stage in the career progression path."""
    phase_number: int = Field(description="Phase index 1 to 4.")
    phase_name: str = Field(description="Title: e.g. 'Phase 1: Foundations & Systems'.")
    estimated_duration: str = Field(description="e.g. 'Weeks 1-4' or 'Month 1-2'.")
    core_competencies: List[str] = Field(description="Key skills mastered in this phase.")
    tasks: List[RoadmapTask] = Field(description="Actionable tasks to complete.")


class CareerRoadmapPlan(BaseModel):
    """Container schema for the entire generated roadmap."""
    role: str = Field(description="Target industry role.")
    experience_level: str = Field(description="Current level.")
    target_timeline: str = Field(description="Target timeline (e.g. 3 Months, 6 Months).")
    summary: str = Field(description="High-level strategy for landing the role.")
    phases: List[RoadmapPhase] = Field(description="Chronological phases.")


def generate_ai_roadmap(
    role: str,
    experience_level: str,
    timeline: str,
    api_key: Optional[str] = None,
) -> tuple[bool, Optional[CareerRoadmapPlan], Optional[str]]:
    """Synthesize a personalized step-by-step career path using Gemini."""
    system_instruction = (
        "You are an elite career architect and principal engineering mentor. "
        "Create an actionable, high-yield, 4-phase career roadmap to guide a student or job seeker "
        "to land their target position within their specified timeline. "
        "Make tasks hands-on: building real projects, solving algorithms, reading open-source code, and mock interviewing."
    )

    prompt = f"""
    Generate an actionable 4-phase career roadmap for:
    - Target Role: {role}
    - Current Experience Level: {experience_level}
    - Target Timeline: {timeline}

    Include exactly 4 progressive phases:
    1. Phase 1: Core Foundations & Technical Prerequisites
    2. Phase 2: Applied Projects & Modern Tooling
    3. Phase 3: Advanced Architectures, Optimization & Production Readiness
    4. Phase 4: Interview Mastery, Portfolio Polish & Offer Negotiation

    For each phase, provide 3 concrete tasks with recommended resources.
    Return strictly structured JSON matching the schema.
    """

    success, result_obj, err = generate_structured_response(
        prompt=prompt,
        response_schema=CareerRoadmapPlan,
        system_instruction=system_instruction,
        api_key=api_key,
        temperature=0.4,
    )

    if not success or result_obj is None:
        return False, None, err

    return True, result_obj, None  # type: ignore


def render_career_roadmap():
    """Render the Career Roadmap UI."""
    st.markdown(
        """
        <div class="cp-card" style="border-left: 4px solid #36A6A0; margin-bottom: 24px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0 0 6px 0; color:#F3F7F5; font-size:1.6rem; font-weight:700;">
                        🗺️ Personalized Career Roadmap
                    </h2>
                    <p style="color:#A5B7B3; font-size:0.95rem; margin:0;">
                        Structured milestone timeline designed to take you from your current level to offer-ready.
                    </p>
                </div>
                <span class="cp-badge-teal">Milestone Timeline</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Configuration Row
    col1, col2, col3 = st.columns(3)
    with col1:
        target_role = st.selectbox(
            "💼 Target Role",
            options=[
                "AI / Machine Learning Engineer",
                "Python Developer",
                "Data Analyst",
                "Full Stack Developer",
                "Cloud / DevOps Engineer",
            ],
            key="roadmap_role_select",
        )
    with col2:
        experience_level = st.selectbox(
            "📈 Current Level",
            options=["Beginner / College Student", "Intermediate (1-3 yrs)", "Career Switcher"],
            key="roadmap_level_select",
        )
    with col3:
        timeline = st.selectbox(
            "⏱️ Target Timeline",
            options=["3 Months (Intensive)", "6 Months (Standard)", "12 Months (Comprehensive)"],
            key="roadmap_timeline_select",
        )

    if st.button("🚀 Generate Step-by-Step Roadmap", type="primary", use_container_width=True):
        api_key = st.session_state.get("api_key")
        if not api_key:
            st.error("Please configure your Gemini API Key in the left sidebar first.")
            return

        with st.spinner(f"🤖 Designing customized career roadmap for {target_role}..."):
            success, roadmap, err = generate_ai_roadmap(
                role=target_role,
                experience_level=experience_level,
                timeline=timeline,
                api_key=api_key,
            )

            if success and roadmap:
                st.session_state.career_roadmap = roadmap
                st.session_state.roadmap_checked_tasks = set()
                st.success("Roadmap generated successfully!")
            else:
                st.error(f"Generation failed: {err}")

    # Render Roadmap if in session
    if st.session_state.get("career_roadmap"):
        render_roadmap_view(st.session_state.career_roadmap)


def render_roadmap_view(roadmap: CareerRoadmapPlan):
    """Render the timeline, milestones, tasks and live progress bar."""
    if "roadmap_checked_tasks" not in st.session_state:
        st.session_state.roadmap_checked_tasks = set()

    total_tasks = sum(len(p.tasks) for p in roadmap.phases)
    completed_tasks = len(st.session_state.roadmap_checked_tasks)
    progress_pct = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

    st.markdown("<hr style='border-color:#304747; margin:24px 0;'>", unsafe_allow_html=True)

    # Progress Overview Header
    st.markdown(
        f"""
        <div class="cp-card" style="margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <h3 style="margin:0; color:#F3F7F5; font-size:1.25rem;">
                    🎯 Progress: <span style="color:#36A6A0;">{progress_pct}% Completed</span> ({completed_tasks}/{total_tasks} Tasks)
                </h3>
                <span class="cp-badge-success">{roadmap.target_timeline}</span>
            </div>
            <p style="color:#A5B7B3; font-size:0.92rem; margin:0 0 12px 0;">{roadmap.summary}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(progress_pct / 100.0)
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Render Phases Chronologically
    for phase in roadmap.phases:
        with st.expander(f"📍 {phase.phase_name} • ({phase.estimated_duration})", expanded=True):
            st.markdown(
                f"""
                <div style="margin-bottom:12px;">
                    <strong style="color:#A9C9BD; font-size:0.88rem;">Key Competencies to Master:</strong><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
            competency_pills = " ".join([f"<span class='cp-badge-teal' style='margin:3px;'>{c}</span>" for c in phase.core_competencies])
            st.markdown(competency_pills, unsafe_allow_html=True)
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # Render Tasks with Checkboxes
            for t in phase.tasks:
                task_key = f"task_check_{t.task_id}"
                is_checked = t.task_id in st.session_state.roadmap_checked_tasks
                
                col_chk, col_content = st.columns([0.08, 0.92])
                with col_chk:
                    checked = st.checkbox("", value=is_checked, key=task_key)
                    if checked and t.task_id not in st.session_state.roadmap_checked_tasks:
                        st.session_state.roadmap_checked_tasks.add(t.task_id)
                        st.rerun()
                    elif not checked and t.task_id in st.session_state.roadmap_checked_tasks:
                        st.session_state.roadmap_checked_tasks.remove(t.task_id)
                        st.rerun()

                with col_content:
                    st.markdown(
                        f"""
                        <div style="background:#172728; border:1px solid #304747; border-radius:10px; padding:12px 14px; margin-bottom:8px;">
                            <div style="font-weight:600; color:{'#55A987' if is_checked else '#F3F7F5'}; font-size:0.95rem;">
                                {'✅' if is_checked else '📌'} {t.title}
                            </div>
                            <p style="color:#A5B7B3; font-size:0.85rem; margin:4px 0 6px 0;">{t.description}</p>
                            <span style="font-size:0.78rem; color:#36A6A0;">📚 Recommended: <em>{t.recommended_resource}</em></span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
