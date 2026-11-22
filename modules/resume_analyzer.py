"""CareerPilot AI — Resume Analyzer Module
========================================
AI-powered Resume Analyzer adhering strictly to the Dark Teal Palette:
- Dark file upload dropzone with teal accents
- Direct text paste option
- Real-time Gemini evaluation:
  * ATS Match Score (0-100)
  * Structural Clarity Score (0-100)
  * Impact & Metrics Score (0-100)
  * Color-coded strengths & growth opportunities
  * Missing technical keywords
  * AI-enhanced summary snippet
"""

from typing import List, Optional
import streamlit as st
from pydantic import BaseModel, Field
from utils.gemini_helper import generate_structured_response


class ResumeAnalysisResult(BaseModel):
    """Structured ATS & resume evaluation schema."""
    target_role: str = Field(description="Role against which the resume was audited.")
    ats_score: int = Field(ge=0, le=100, description="Overall ATS compatibility score out of 100.")
    structural_clarity_score: int = Field(ge=0, le=100, description="Formatting, organization, and visual hierarchy.")
    impact_metrics_score: int = Field(ge=0, le=100, description="Usage of quantifiable achievements and data points.")
    key_strengths: List[str] = Field(description="Strong bullet points, experiences, or credentials.")
    critical_missing_keywords: List[str] = Field(description="High-demand industry keywords not found in the resume.")
    actionable_improvements: List[str] = Field(description="Concrete suggestions to improve ATS ranking.")
    enhanced_summary: str = Field(description="A rewritten high-impact executive summary for this candidate.")


def analyze_resume_text(
    resume_text: str,
    target_role: str,
    api_key: Optional[str] = None,
) -> tuple[bool, Optional[ResumeAnalysisResult], Optional[str]]:
    """Evaluate candidate resume against a target role using Gemini."""
    if not resume_text or len(resume_text.strip()) < 50:
        return False, None, "Resume content is too short. Please paste or upload a substantive resume."

    system_instruction = (
        "You are an elite Applicant Tracking System (ATS) auditor and senior technical talent recruiter. "
        "Analyze the candidate's resume objectively against the target job role. "
        "Score realistically (0-100): "
        "- 85-100: Exceptional alignment, strong metrics, clear keywords. "
        "- 70-84: Solid background, but needs more quantifiable results or missing secondary skills. "
        "- Below 70: Major gaps in required tools, weak impact verbs, or poor ATS formatting. "
        "Provide actionable, specific recommendations and an optimized executive summary."
    )

    prompt = f"""
    Please audit the following candidate resume for the target role: "{target_role}".

    RESUME CONTENT:
    \"\"\"{resume_text.strip()}\"\"\"

    Analyze keyword density, role relevancy, quantifiable business impact, and formatting clarity.
    Return strictly structured JSON matching the requested schema.
    """

    success, result_obj, err = generate_structured_response(
        prompt=prompt,
        response_schema=ResumeAnalysisResult,
        system_instruction=system_instruction,
        api_key=api_key,
        temperature=0.3,
    )

    if not success or result_obj is None:
        return False, None, err

    return True, result_obj, None  # type: ignore


def render_resume_analyzer():
    """Render the Resume Analyzer UI."""
    st.markdown(
        """
        <div class="cp-card" style="border-left: 4px solid #36A6A0; margin-bottom: 24px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0 0 6px 0; color:#F3F7F5; font-size:1.6rem; font-weight:700;">
                        📄 Smart Resume Analyzer
                    </h2>
                    <p style="color:#A5B7B3; font-size:0.95rem; margin:0;">
                        Optimize your resume for modern Applicant Tracking Systems (ATS) and hiring manager standards.
                    </p>
                </div>
                <span class="cp-badge-teal">ATS Audit Engine</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        target_role = st.text_input(
            "🎯 Target Job Role for Evaluation",
            value="AI Engineer / Python Developer",
            placeholder="e.g. Full Stack Developer, Data Scientist...",
            help="The analyzer compares your resume against real-world job expectations for this role.",
        )

        st.markdown("**Option A: Upload Resume File**")
        uploaded_file = st.file_uploader(
            "Upload resume (.txt, .md, .pdf)",
            type=["txt", "md", "pdf"],
            key="resume_uploader",
        )

    with col2:
        st.markdown("**Option B: Or Paste Resume Text Directly**")
        pasted_text = st.text_area(
            "Paste resume content here:",
            height=210,
            placeholder="Paste your education, skills, projects, and work experience here...",
            key="pasted_resume_text",
        )

    resume_content = ""
    if uploaded_file is not None:
        try:
            # Handle text/md or extractable streams
            if uploaded_file.name.endswith(".pdf"):
                # Pass plain bytes or attempt decode
                content_bytes = uploaded_file.read()
                # Try simple utf-8 decode or fallback to representation
                try:
                    resume_content = content_bytes.decode("utf-8", errors="ignore")
                except Exception:
                    resume_content = str(content_bytes)
            else:
                resume_content = uploaded_file.read().decode("utf-8", errors="replace")
            st.info(f"Loaded `{uploaded_file.name}` ({len(resume_content)} characters).")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

    if not resume_content and pasted_text.strip():
        resume_content = pasted_text.strip()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Analyze Resume with Gemini", type="primary", use_container_width=True):
        api_key = st.session_state.get("api_key")
        if not api_key:
            st.error("Please configure your Gemini API Key in the left sidebar first.")
            return

        if not resume_content:
            st.warning("Please upload a resume file or paste your resume text to analyze.")
            return

        with st.spinner("🤖 Auditing resume against industry ATS standards..."):
            success, analysis, err = analyze_resume_text(
                resume_text=resume_content,
                target_role=target_role,
                api_key=api_key,
            )

            if success and analysis:
                st.session_state.last_resume_analysis = analysis
                st.success("Resume audit complete!")
            else:
                st.error(f"Analysis failed: {err}")

    # Render results if available in session
    if st.session_state.get("last_resume_analysis"):
        analysis: ResumeAnalysisResult = st.session_state.last_resume_analysis
        st.markdown("<hr style='border-color:#304747; margin:28px 0;'>", unsafe_allow_html=True)
        render_resume_results(analysis)


def render_resume_results(analysis: ResumeAnalysisResult):
    """Render the visual scorecards and feedback for the analyzed resume."""
    ats = analysis.ats_score
    badge_cls = "cp-badge-success" if ats >= 80 else ("cp-badge-warning" if ats >= 65 else "cp-badge-error")
    badge_color = "#55A987" if ats >= 80 else ("#E4B35E" if ats >= 65 else "#D77B69")

    st.markdown(
        f"""
        <div class="cp-card" style="border-top: 4px solid {badge_color}; text-align:center; padding: 24px;">
            <div style="font-size:0.8rem; color:#A5B7B3; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">
                ATS Match Report for {analysis.target_role}
            </div>
            <h1 style="color:#F3F7F5; font-size: 2.4rem; font-weight:800; margin: 8px 0;">
                Overall Score: <span style="color:{badge_color};">{ats} / 100</span>
            </h1>
            <span class="{badge_cls}" style="font-size:0.9rem; padding: 6px 16px;">
                {'Target Ready' if ats >= 80 else ('Needs Keyword Optimization' if ats >= 65 else 'Major Gaps Detected')}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sc1, sc2 = st.columns(2)
    with sc1:
        st.metric("📐 Structural & Formatting Clarity", f"{analysis.structural_clarity_score}/100")
    with sc2:
        st.metric("📈 Impact & Metric Quantification", f"{analysis.impact_metrics_score}/100")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    c_str, c_rec = st.columns(2)

    with c_str:
        st.markdown(
            """
            <div style="background: rgba(85, 169, 135, 0.08); border: 1px solid rgba(85, 169, 135, 0.3); border-left: 4px solid #55A987;
                        border-radius: 12px; padding: 18px; min-height: 220px;">
                <h4 style="color:#55A987; margin-top:0; font-size:1.1rem;">💪 Key Resume Strengths</h4>
            """,
            unsafe_allow_html=True,
        )
        for s in analysis.key_strengths:
            st.markdown(f"✅ {s}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_rec:
        st.markdown(
            """
            <div style="background: rgba(215, 123, 105, 0.08); border: 1px solid rgba(215, 123, 105, 0.3); border-left: 4px solid #D77B69;
                        border-radius: 12px; padding: 18px; min-height: 220px;">
                <h4 style="color:#D77B69; margin-top:0; font-size:1.1rem;">⚠️ Actionable Improvements</h4>
            """,
            unsafe_allow_html=True,
        )
        for imp in analysis.actionable_improvements:
            st.markdown(f"🔍 {imp}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Missing Keywords Badge List
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="cp-card">
            <h4 style="margin:0 0 10px 0; color:#36A6A0; font-size:1.1rem;">
                🔑 High-Demand Keywords to Add
            </h4>
            <p style="color:#A5B7B3; font-size:0.88rem; margin:0 0 12px 0;">
                Recruiting algorithms specifically filter candidates on these terms. Incorporate them into relevant project descriptions:
            </p>
        """,
        unsafe_allow_html=True,
    )
    keyword_html = " ".join([f"<span class='cp-badge-teal' style='margin: 4px;'>{kw}</span>" for kw in analysis.critical_missing_keywords])
    st.markdown(keyword_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Enhanced Summary Expander
    with st.expander("✨ AI-Optimized Executive Summary for Your Profile", expanded=True):
        st.markdown(
            f"""
            <div style="background:#172728; border:1px solid #36A6A0; border-radius:10px; padding:18px; color:#F3F7F5; font-size:0.95rem; line-height:1.6;">
                {analysis.enhanced_summary}
            </div>
            """,
            unsafe_allow_html=True,
        )
