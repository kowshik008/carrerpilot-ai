"""CareerPilot AI - Interview Setup Module
=========================================
Handles user inputs for interview configuration:
- Target job role selection (or custom entry)
- Experience level (Beginner, Intermediate, Advanced)
- Interview type (Technical, HR, Mixed)
- Number of questions (1-10, default 5)
Provides strict validation before generating questions.
"""

from typing import Dict, Any, Tuple, Optional
import streamlit as st
from config import GEMINI_MODEL

POPULAR_ROLES = [
    "Python Developer",
    "AI / Machine Learning Engineer",
    "Data Analyst",
    "Frontend Developer (React / Next.js)",
    "Backend Developer (Node.js / Django)",
    "Full Stack Developer",
    "DevOps / Cloud Engineer",
    "Cybersecurity Analyst",
    "Product Manager",
    "Other (Custom Role)",
]

EXPERIENCE_LEVELS = [
    "Beginner (0-1 years / Fresher)",
    "Intermediate (2-4 years)",
    "Advanced (5+ years / Senior)",
]

INTERVIEW_TYPES = [
    "Technical",
    "HR / Behavioral",
    "Mixed (Technical + Behavioral)",
]


def validate_setup_inputs(
    role: str,
    experience_level: str,
    interview_type: str,
    num_questions: int,
) -> Tuple[bool, Optional[str]]:
    """Validate all user inputs for the interview setup.
    Returns: (is_valid: bool, error_message: Optional[str])
    """
    if not role or not role.strip():
        return False, "Target Job Role cannot be empty. Please specify a role."
    
    if len(role.strip()) < 2:
        return False, "Target Job Role must be at least 2 characters long."

    if not experience_level:
        return False, "Please select an Experience Level."

    if not interview_type:
        return False, "Please select an Interview Type."

    if not isinstance(num_questions, int) or num_questions < 1 or num_questions > 10:
        return False, "Number of questions must be an integer between 1 and 10."

    return True, None


def render_setup_form() -> Optional[Dict[str, Any]]:
    """Render the interview setup UI in Streamlit.
    Returns a dictionary of validated settings when user clicks 'Start Interview',
    or None if the form hasn't been submitted.
    """
    st.markdown(
        f"""
        <div class="cp-card" style="border-left: 4px solid #36A6A0;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin:0 0 6px 0; color:#F3F7F5; font-size:1.35rem;">
                        🎯 Configure Your Mock Interview
                    </h3>
                    <p style="color:#A5B7B3; font-size:0.95rem; margin:0;">
                        Calibrate your session to match your target job profile and industry experience standards.
                    </p>
                </div>
                <span class="cp-badge-teal">{GEMINI_MODEL}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("interview_setup_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            selected_role = st.selectbox(
                "💼 Target Job Role",
                options=POPULAR_ROLES,
                index=0,
                help="Choose from common industry roles or select 'Other' to enter your own.",
            )

            custom_role = ""
            if selected_role == "Other (Custom Role)":
                custom_role = st.text_input(
                    "✏️ Specify Your Target Role",
                    placeholder="e.g. Embedded Firmware Engineer, Data Scientist...",
                )

            experience_level = st.selectbox(
                "📈 Experience Level",
                options=EXPERIENCE_LEVELS,
                index=0,
                help="Determines the depth and difficulty of technical questions.",
            )

        with col2:
            interview_type = st.selectbox(
                "📋 Interview Type",
                options=INTERVIEW_TYPES,
                index=2,  # Default to Mixed for best well-rounded practice
                help="Technical focuses on coding/system concepts; HR on culture and behavioral STAR questions.",
            )

            num_questions = st.slider(
                "🔢 Number of Questions",
                min_value=1,
                max_value=10,
                value=5,
                step=1,
                help="Select between 1 to 10 questions (5 is standard for a quick mock round).",
            )

        # Clean experience level string (e.g., 'Beginner (0-1 years)' -> 'Beginner')
        clean_exp = experience_level.split(" ")[0]

        effective_role = custom_role.strip() if selected_role == "Other (Custom Role)" else selected_role

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🚀 Generate Interview Questions",
            use_container_width=True,
            type="primary",
        )

        if submitted:
            is_valid, err_msg = validate_setup_inputs(
                role=effective_role,
                experience_level=clean_exp,
                interview_type=interview_type,
                num_questions=num_questions,
            )
            if not is_valid:
                st.error(err_msg)
                return None

            return {
                "role": effective_role,
                "experience_level": clean_exp,
                "interview_type": interview_type,
                "num_questions": num_questions,
            }

    return None
