"""CareerPilot AI — Dashboard Module
==================================
The central command center for student career readiness:
- Warm, human-centered welcome message
- Student profile snapshot
- High-level career progress metrics
- 3 AI Feature quick-launch cards
- Recent mock interview & resume activity
- Curated career tips & actionable strategies
"""

import streamlit as st


def render_dashboard(on_navigate):
    """Render the main CareerPilot AI dashboard.
    
    Args:
        on_navigate: Callback function taking a page name to switch navigation state.
    """
    # Welcome & Student Profile Header Card
    st.markdown(
        """
        <div class="cp-card" style="border-left: 4px solid #36A6A0; margin-bottom: 24px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
                <div>
                    <div style="display:inline-block; margin-bottom:8px;">
                        <span class="cp-badge-teal">Student Career Portal</span>
                    </div>
                    <h2 style="margin:0 0 6px 0; color:#F3F7F5; font-size:1.85rem; font-weight:800;">
                        Welcome back, Candidate! 👋
                    </h2>
                    <p style="color:#A5B7B3; font-size:1.0rem; margin:0; line-height:1.5;">
                        Your intelligent AI-powered copilot for mock interviews, resume optimization, and career roadmaps.
                    </p>
                </div>
                <div style="background:#172728; border:1px solid #304747; border-radius:12px; padding:12px 18px; text-align:right;">
                    <div style="font-size:0.75rem; color:#A5B7B3; text-transform:uppercase; letter-spacing:1px; font-weight:600;">
                        Target Career Track
                    </div>
                    <div style="color:#36A6A0; font-size:1.05rem; font-weight:700;">
                        AI & Software Engineering
                    </div>
                    <div style="font-size:0.8rem; color:#55A987; margin-top:2px;">
                        ● Readiness: 84% (Strong)
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top KPI Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="🎯 Mock Rounds Completed",
            value=len(st.session_state.get("evaluations", [])),
            delta="Active Session",
        )
    with m2:
        evals = st.session_state.get("evaluations", [])
        avg = round(sum(e.score for e in evals) / len(evals), 1) if evals else 0.0
        st.metric(
            label="⭐ Avg Interview Score",
            value=f"{avg} / 10" if evals else "—",
            delta="+0.8 this week" if evals else "Start practice",
        )
    with m3:
        st.metric(
            label="📄 Resumes Audited",
            value="1 File" if st.session_state.get("last_resume_analysis") else "0",
            delta="ATS Ready",
        )
    with m4:
        st.metric(
            label="🗺️ Roadmap Milestones",
            value="2 of 4 Active",
            delta="50% Complete",
        )

    st.markdown("<hr style='border-color:#304747; margin:28px 0;'>", unsafe_allow_html=True)

    # Three AI Feature Cards
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <h3 style="margin:0 0 4px 0; color:#F3F7F5; font-size:1.35rem;">
                🚀 AI-Powered Career Modules
            </h3>
            <p style="color:#A5B7B3; font-size:0.95rem; margin:0;">
                Select a tool to accelerate your interview preparation and job readiness.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_feat1, c_feat2, c_feat3 = st.columns(3)

    with c_feat1:
        st.markdown(
            """
            <div class="cp-card" style="height: 250px; display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span style="font-size:2rem;">🎯</span>
                        <span class="cp-badge-teal">Core Module</span>
                    </div>
                    <h4 style="margin:0 0 8px 0; color:#F3F7F5; font-size:1.15rem;">AI Mock Interviewer</h4>
                    <p style="color:#A5B7B3; font-size:0.88rem; line-height:1.5; margin:0;">
                        Dynamic question generation, dual text/voice answering, and rubric-based evaluations with improved model answers.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Launch Mock Interview ↗", key="dash_btn_interview", use_container_width=True, type="primary"):
            on_navigate("Mock Interviewer")

    with c_feat2:
        st.markdown(
            """
            <div class="cp-card" style="height: 250px; display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span style="font-size:2rem;">📄</span>
                        <span class="cp-badge-success">ATS Audit</span>
                    </div>
                    <h4 style="margin:0 0 8px 0; color:#F3F7F5; font-size:1.15rem;">Resume Analyzer</h4>
                    <p style="color:#A5B7B3; font-size:0.88rem; line-height:1.5; margin:0;">
                        Upload or paste your resume to get instant ATS match scoring, identify missing technical keywords, and polish bullet points.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Scan Resume ↗", key="dash_btn_resume", use_container_width=True):
            on_navigate("Resume Analyzer")

    with c_feat3:
        st.markdown(
            """
            <div class="cp-card" style="height: 250px; display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span style="font-size:2rem;">🗺️</span>
                        <span class="cp-badge-teal">Timeline</span>
                    </div>
                    <h4 style="margin:0 0 8px 0; color:#F3F7F5; font-size:1.15rem;">Career Roadmap</h4>
                    <p style="color:#A5B7B3; font-size:0.88rem; line-height:1.5; margin:0;">
                        Personalized step-by-step career path with interactive checkboxes, core concepts to learn, and recommended learning resources.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Roadmap ↗", key="dash_btn_roadmap", use_container_width=True):
            on_navigate("Career Roadmap")

    st.markdown("<hr style='border-color:#304747; margin:28px 0;'>", unsafe_allow_html=True)

    # Activity & Career Tips 2-Column Split
    col_act, col_tips = st.columns([1, 1])

    with col_act:
        st.markdown(
            """
            <div class="cp-card" style="min-height:280px;">
                <h4 style="margin:0 0 14px 0; color:#F3F7F5; font-size:1.15rem;">
                    ⏱️ Recent Practice Activity
                </h4>
            """,
            unsafe_allow_html=True,
        )
        if st.session_state.get("evaluations"):
            evals = st.session_state.evaluations
            for i, ev in enumerate(reversed(evals[-3:]), start=1):
                badge_cls = "cp-badge-success" if ev.score >= 8.0 else ("cp-badge-teal" if ev.score >= 6.0 else "cp-badge-error")
                st.markdown(
                    f"""
                    <div style="background:#172728; border:1px solid #304747; border-radius:10px; padding:12px 14px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-weight:600; color:#F3F7F5; font-size:0.92rem;">Question #{ev.question_id} Answered</div>
                            <div style="color:#A5B7B3; font-size:0.8rem; margin-top:2px;">Verdict: {ev.verdict}</div>
                        </div>
                        <span class="{badge_cls}">{ev.score:.1f} / 10</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """
                <div style="background:#172728; border:1px dashed #304747; border-radius:10px; padding:24px; text-align:center;">
                    <p style="color:#A5B7B3; font-size:0.92rem; margin:0 0 12px 0;">
                        No interview sessions completed yet. Take your first simulated mock round!
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_tips:
        st.markdown(
            """
            <div class="cp-card" style="min-height:280px;">
                <h4 style="margin:0 0 14px 0; color:#36A6A0; font-size:1.15rem;">
                    💡 Pro Career & Interview Tips
                </h4>
                <div style="background:#172728; border-left:3px solid #36A6A0; border-radius:6px; padding:10px 14px; margin-bottom:10px;">
                    <strong style="color:#F3F7F5; font-size:0.88rem;">1. The STAR Technique</strong>
                    <p style="color:#A5B7B3; font-size:0.82rem; margin:4px 0 0 0;">
                        Structure behavioral answers into Situation, Task, Action, and quantifiable Result for maximum impact.
                    </p>
                </div>
                <div style="background:#172728; border-left:3px solid #55A987; border-radius:6px; padding:10px 14px; margin-bottom:10px;">
                    <strong style="color:#F3F7F5; font-size:0.88rem;">2. Technical Trade-offs</strong>
                    <p style="color:#A5B7B3; font-size:0.82rem; margin:4px 0 0 0;">
                        Senior interviewers evaluate your reasoning. Always discuss time/space complexity and alternatives.
                    </p>
                </div>
                <div style="background:#172728; border-left:3px solid #E4B35E; border-radius:6px; padding:10px 14px;">
                    <strong style="color:#F3F7F5; font-size:0.88rem;">3. ATS Keyword Density</strong>
                    <p style="color:#A5B7B3; font-size:0.82rem; margin:4px 0 0 0;">
                        Align your resume bullet points with exact phrasing found in the target job description.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
