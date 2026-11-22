"""CareerPilot AI — Intelligent Career & Mock Interview Platform
==============================================================
Tagline: Navigate Your Future.
Palette:
  Main Background:      #101C1D
  Secondary Background: #172728
  Card Background:      #203536
  Primary Teal:         #155E63
  Accent Teal:          #36A6A0
  Soft Mint:            #A9C9BD
  Primary Text:         #F3F7F5
  Secondary Text:       #A5B7B3
  Borders:              #304747
  Success:              #55A987
  Warning:              #E4B35E
  Error:                #D77B69
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

# Streamlit Page Configuration - Must be the first Streamlit command
st.set_page_config(
    page_title="CareerPilot AI — Navigate Your Future",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Internal Module Imports
from config import GEMINI_MODEL
from utils.gemini_helper import get_api_key, test_api_connection
from utils.voice_helper import process_audio_recording
from modules.dashboard import render_dashboard
from modules.resume_analyzer import render_resume_analyzer
from modules.career_roadmap import render_career_roadmap
from modules.progress_history import render_progress_history
from modules.settings_view import render_settings
from modules.interview_setup import render_setup_form
from modules.question_generator import generate_interview_questions
from modules.answer_evaluator import evaluate_answer, render_evaluation_feedback
from modules.results_dashboard import render_results_dashboard


# ==============================================================================
# CENTRALIZED THEME LOADER
# ==============================================================================
def load_centralized_theme():
    """Load the external CSS stylesheet from styles/theme.css."""
    css_path = os.path.join(os.path.dirname(__file__), "styles", "theme.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
def initialize_session_state():
    defaults = {
        "current_page": "Dashboard",
        "api_key": get_api_key() or "",
        "interview_started": False,
        "interview_completed": False,
        "setup_config": None,
        "questions": [],
        "current_question_index": 0,
        "user_answers": {},  # {question_id: answer_text}
        "evaluations": [],   # List of EvaluationResult
        "transcribed_text": "",  # Temporary storage for active voice transcription
        "last_resume_analysis": None,
        "career_roadmap": None,
        "roadmap_checked_tasks": set(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def navigate_to(page_name: str):
    """Callback to switch pages programmatically from buttons."""
    st.session_state.current_page = page_name
    st.rerun()


# ==============================================================================
# SIDEBAR NAVIGATION & CONTROLS
# ==============================================================================
def render_sidebar():
    with st.sidebar:
        # Brand Logo and Tagline
        st.markdown(
            """
            <div style="padding: 12px 0 20px 0; text-align: left;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="background: linear-gradient(135deg, #155E63, #36A6A0); 
                                width:40px; height:40px; border-radius:12px; 
                                display:flex; align-items:center; justify-content:center; 
                                font-size:20px; box-shadow: 0 4px 12px rgba(54, 166, 160, 0.25);">
                        🎯
                    </div>
                    <div>
                        <div style="font-size:1.35rem; font-weight:800; color:#F3F7F5; letter-spacing:-0.5px; line-height:1.2;">
                            CareerPilot <span style="color:#36A6A0;">AI</span>
                        </div>
                        <div style="color:#A9C9BD; font-size:0.75rem; font-weight:600; letter-spacing:0.5px; text-transform:uppercase;">
                            Navigate Your Future.
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='border-color:#304747; margin:12px 0 20px 0;'>", unsafe_allow_html=True)

        # Main Navigation Menu (Radio buttons styled via theme.css)
        pages = [
            "Dashboard",
            "Resume Analyzer",
            "Mock Interviewer",
            "Career Roadmap",
            "Progress & History",
            "Settings",
        ]

        # Sync radio index with current_page state
        default_idx = pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0

        selected_page = st.radio(
            "Navigation",
            options=pages,
            index=default_idx,
            label_visibility="collapsed",
            format_func=lambda x: {
                "Dashboard": "🏠   Dashboard",
                "Resume Analyzer": "📄   Resume Analyzer",
                "Mock Interviewer": "🎯   Mock Interviewer",
                "Career Roadmap": "🗺️   Career Roadmap",
                "Progress & History": "📊   Progress & History",
                "Settings": "⚙️   Settings",
            }.get(x, x),
        )

        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()

        st.markdown("<hr style='border-color:#304747; margin:24px 0 18px 0;'>", unsafe_allow_html=True)

        # Quick API Key Status in Sidebar
        api_configured = bool(st.session_state.get("api_key"))
        if api_configured:
            st.markdown(
                f"""
                <div style="background:rgba(85, 169, 135, 0.1); border:1px solid #55A987; border-radius:10px; padding:10px 14px; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
                    <span style="color:#55A987; font-size:14px;">●</span>
                    <span style="color:#F3F7F5; font-size:0.82rem; font-weight:600;">{GEMINI_MODEL} Connected</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="background:rgba(228, 179, 94, 0.1); border:1px solid #E4B35E; border-radius:10px; padding:10px 14px; margin-bottom:14px;">
                    <div style="color:#E4B35E; font-size:0.82rem; font-weight:600;">⚠️ API Key Missing</div>
                    <div style="color:#A5B7B3; font-size:0.75rem; margin-top:2px;">Go to Settings to connect.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Active Session Metadata if inside Mock Interview
        if st.session_state.interview_started and st.session_state.setup_config:
            cfg = st.session_state.setup_config
            st.markdown(
                f"""
                <div class="cp-card" style="padding:14px; margin-bottom:16px;">
                    <div style="font-size:0.75rem; color:#A5B7B3; text-transform:uppercase; font-weight:600;">Active Mock Interview</div>
                    <div style="color:#36A6A0; font-weight:700; font-size:0.95rem; margin:2px 0;">{cfg.get('role')}</div>
                    <div style="color:#A5B7B3; font-size:0.8rem;">Q{st.session_state.current_question_index + 1} of {len(st.session_state.questions)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🛑 Reset Session", use_container_width=True):
                for k in ["interview_started", "interview_completed", "setup_config", "questions", "current_question_index", "user_answers", "evaluations", "transcribed_text"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()

        # Sidebar Footer
        st.markdown(
            """
            <div style="font-size:0.75rem; color:#A5B7B3; margin-top:28px; text-align:center; line-height:1.5;">
                <strong>CareerPilot AI</strong> • v2.0<br>
                <span style="color:#36A6A0;">Navigate Your Future.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# MAIN APPLICATION ROUTER
# ==============================================================================
def main():
    load_centralized_theme()
    initialize_session_state()
    render_sidebar()

    current_page = st.session_state.current_page

    # Header Branding Banner
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:12px;">
                <div>
                    <h1 style="margin:0; font-size:2.2rem; color:#F3F7F5; font-weight:800;">
                        CareerPilot <span style="color:#36A6A0;">AI</span>
                    </h1>
                    <p style="color:#A5B7B3; font-size:0.98rem; margin-top:4px; margin-bottom:0;">
                        Navigate Your Future. Empowering students and professionals with intelligent career tools.
                    </p>
                </div>
                <div style="background:#203536; border:1px solid #304747; padding:6px 16px; border-radius:20px; color:#A9C9BD; font-size:0.85rem; font-weight:600;">
                    AI Engine: <strong style="color:#36A6A0;">{GEMINI_MODEL}</strong>
                </div>
            </div>
            <hr style="border-color: #304747; margin: 16px 0 24px 0;">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ROUTING
    if current_page == "Dashboard":
        render_dashboard(on_navigate=navigate_to)

    elif current_page == "Resume Analyzer":
        render_resume_analyzer()

    elif current_page == "Mock Interviewer":
        render_mock_interviewer_page()

    elif current_page == "Career Roadmap":
        render_career_roadmap()

    elif current_page == "Progress & History":
        render_progress_history()

    elif current_page == "Settings":
        render_settings()


# ==============================================================================
# MOCK INTERVIEWER WORKFLOW (PRESERVED FULL FUNCTIONALITY)
# ==============================================================================
def render_mock_interviewer_page():
    """Manages the full lifecycle of the AI Mock Interviewer."""
    # State 1: Interview Setup Form
    if not st.session_state.interview_started:
        setup_data = render_setup_form()
        if setup_data:
            if not st.session_state.api_key:
                st.error("Please enter a valid Gemini API Key in the Settings page or sidebar before generating questions.")
                return

            with st.spinner(f"🤖 Senior Interviewer is generating {setup_data['num_questions']} questions for {setup_data['role']}..."):
                success, questions, err = generate_interview_questions(
                    role=setup_data["role"],
                    experience_level=setup_data["experience_level"],
                    interview_type=setup_data["interview_type"],
                    num_questions=setup_data["num_questions"],
                    api_key=st.session_state.api_key,
                )

                if success and questions:
                    st.session_state.setup_config = setup_data
                    st.session_state.questions = questions
                    st.session_state.current_question_index = 0
                    st.session_state.evaluations = []
                    st.session_state.user_answers = {}
                    st.session_state.interview_started = True
                    st.session_state.interview_completed = False
                    st.rerun()
                else:
                    st.error(f"Failed to generate questions: {err}")

    # State 2: Interview Completed (Results Dashboard)
    elif st.session_state.interview_completed:
        render_results_dashboard(
            session_config=st.session_state.setup_config,
            questions=st.session_state.questions,
            evaluations=st.session_state.evaluations,
            user_answers=st.session_state.user_answers,
        )

    # State 3: Active Question Workspace
    else:
        render_active_interview_workspace()


def render_active_interview_workspace():
    idx = st.session_state.current_question_index
    questions = st.session_state.questions
    total_q = len(questions)
    current_q = questions[idx]

    # Progress Indicator
    progress_val = (idx) / total_q
    st.progress(progress_val)
    st.markdown(
        f"<div style='display:flex; justify-content:space-between; font-size:0.85rem; color:#A5B7B3; margin-bottom:14px;'>"
        f"<span>Question <strong style='color:#F3F7F5;'>{idx + 1}</strong> of <strong style='color:#F3F7F5;'>{total_q}</strong></span>"
        f"<span>Category: <strong style='color:#36A6A0;'>{current_q.category}</strong> | Difficulty: <strong style='color:#55A987;'>{current_q.difficulty}</strong></span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Question Display Card
    st.markdown(
        f"""
        <div class="cp-card" style="border-left: 4px solid #36A6A0; margin-bottom: 22px;">
            <div style="font-size:0.8rem; color:#A5B7B3; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; font-weight:600;">
                Interviewer Question #{current_q.id}
            </div>
            <h2 style="margin: 0; color:#F3F7F5; font-size:1.35rem; line-height: 1.5; font-weight:700;">
                {current_q.question}
            </h2>
            <div style="margin-top:10px; font-size:0.85rem; color:#A5B7B3;">
                🎯 Evaluates: <em style="color:#A9C9BD;">{current_q.expected_competency}</em>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Check if this question has already been evaluated in this session
    has_evaluation = len(st.session_state.evaluations) > idx
    current_evaluation = st.session_state.evaluations[idx] if has_evaluation else None

    # If already evaluated, display results and navigation button
    if has_evaluation and current_evaluation:
        render_evaluation_feedback(current_evaluation)

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        col_nav1, col_nav2 = st.columns([3, 1])
        with col_nav2:
            if idx + 1 < total_q:
                if st.button("Next Question ➡️", use_container_width=True, type="primary"):
                    st.session_state.current_question_index += 1
                    st.session_state.transcribed_text = ""
                    st.rerun()
            else:
                if st.button("🏁 View Final Results", use_container_width=True, type="primary"):
                    st.session_state.interview_completed = True
                    st.rerun()
        return

    # If NOT evaluated yet, show Answer Submission Tabs (Text & Voice)
    tab_text, tab_voice = st.tabs(["⌨️ Text Answer", "🎙️ Voice Answer"])

    with tab_text:
        text_answer = st.text_area(
            "Type your response below:",
            height=160,
            placeholder="Structure your answer clearly. Explain your thought process, approach, and practical examples...",
            key=f"text_input_{idx}",
        )

        if st.button("📤 Submit Text Answer", type="primary", key=f"submit_text_{idx}"):
            submit_and_evaluate(current_q, text_answer)

    with tab_voice:
        st.markdown(
            """
            <div style="background:#203536; border:1px dashed #36A6A0; 
                        border-radius:10px; padding:14px; margin-bottom:14px; font-size:0.9rem; color:#A5B7B3;">
                🎙️ <strong>Speak Your Answer:</strong> Click the microphone below to record. 
                Your audio is transcribed using Gemini's native multimodal speech engine, allowing you to review and polish your answer before submitting.
            </div>
            """,
            unsafe_allow_html=True,
        )

        audio_buffer = st.audio_input("Record your answer", key=f"audio_input_{idx}")

        if audio_buffer is not None:
            c_trans1, c_trans2 = st.columns([1, 3])
            with c_trans1:
                if st.button("🔄 Transcribe Audio", key=f"btn_transcribe_{idx}"):
                    if not st.session_state.api_key:
                        st.error("API Key required for transcription.")
                    else:
                        with st.spinner("🤖 Transcribing audio with Gemini..."):
                            success, transcript, err = process_audio_recording(
                                audio_buffer,
                                api_key=st.session_state.api_key,
                            )
                            if success and transcript:
                                st.session_state.transcribed_text = transcript
                                st.success("Audio transcribed successfully!")
                            else:
                                st.error(f"Transcription failed: {err}")

        # Editable transcription box
        voice_final_answer = st.text_area(
            "Review & Edit Transcribed Text (or make corrections before submitting):",
            value=st.session_state.transcribed_text,
            height=130,
            key=f"voice_edit_{idx}",
            help="Review the transcription for any misheard technical terms or acronyms.",
        )

        if st.button("📤 Submit Voice Answer", type="primary", key=f"submit_voice_{idx}"):
            submit_and_evaluate(current_q, voice_final_answer)


def submit_and_evaluate(question, user_answer_text: str):
    """Orchestrates validation, evaluation, and state update for an answered question."""
    if not st.session_state.api_key:
        st.error("Please configure your Gemini API Key in the Settings page or sidebar before submitting.")
        return

    with st.spinner("🧠 Senior AI Interviewer is evaluating your response..."):
        cfg = st.session_state.setup_config or {}
        success, eval_result, err = evaluate_answer(
            question_id=question.id,
            question_text=question.question,
            user_answer=user_answer_text,
            role=cfg.get("role", "Developer"),
            experience_level=cfg.get("experience_level", "Intermediate"),
            interview_type=cfg.get("interview_type", "Technical"),
            expected_competency=question.expected_competency,
            api_key=st.session_state.api_key,
        )

        if success and eval_result:
            st.session_state.user_answers[question.id] = user_answer_text
            st.session_state.evaluations.append(eval_result)
            st.session_state.transcribed_text = ""
            st.rerun()
        else:
            st.error(f"Evaluation error: {err}")


# ==============================================================================
# APPLICATION ENTRYPOINT
# ==============================================================================
if __name__ == "__main__":
    main()
