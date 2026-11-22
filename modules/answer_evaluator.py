"""CareerPilot AI - Answer Evaluator Module
=========================================
Evaluates user interview answers against the generated question using Google Gemini.
Features:
- Rejects empty or low-effort answers before consuming API quota.
- Analyzes:
  1. Relevance
  2. Technical Correctness
  3. Clarity & Structure
  4. Completeness
  5. Communication Quality
- Produces structured JSON parsed into Pydantic models:
  - Numerical scores (0-10)
  - Strengths list
  - Weaknesses list
  - Missing key concepts
  - Actionable improvement suggestions
  - High-scoring improved sample answer
"""

from typing import List, Tuple, Optional
import streamlit as st
from pydantic import BaseModel, Field
from utils.gemini_helper import generate_structured_response


class EvaluationResult(BaseModel):
    """Structured rubric-based evaluation schema."""
    question_id: int = Field(description="ID of the question evaluated.")
    score: float = Field(ge=0.0, le=10.0, description="Overall score out of 10.0.")
    relevance_score: float = Field(ge=0.0, le=10.0, description="Relevance to the question (0-10).")
    technical_correctness_score: float = Field(ge=0.0, le=10.0, description="Accuracy of concepts & facts (0-10).")
    clarity_score: float = Field(ge=0.0, le=10.0, description="Communication clarity and structure (0-10).")
    completeness_score: float = Field(ge=0.0, le=10.0, description="Depth and coverage of key elements (0-10).")
    strengths: List[str] = Field(description="List of positive aspects identified in the candidate's answer.")
    weaknesses: List[str] = Field(description="List of weak areas or inaccuracies.")
    missing_points: List[str] = Field(description="Key concepts or industry best practices that were omitted.")
    suggestions: List[str] = Field(description="Concrete advice to level up this answer.")
    improved_sample_answer: str = Field(description="An exemplary, high-scoring model answer for comparison.")
    verdict: str = Field(description="Summary tag: e.g. 'Outstanding', 'Strong Answer', 'Competent', 'Needs Polish', 'Incomplete'.")


def validate_user_answer(answer: Optional[str]) -> Tuple[bool, Optional[str]]:
    """Verify that the user's answer is non-empty and substantive.
    Returns: (is_valid: bool, error_message: Optional[str])
    """
    if not answer or not answer.strip():
        return False, "Answer cannot be empty. Please type or speak your response before submitting."

    cleaned = answer.strip()
    if len(cleaned.split()) < 3 or len(cleaned) < 10:
        return False, "Your answer is too brief to evaluate realistically. Please elaborate on your reasoning."

    return True, None


def evaluate_answer(
    question_id: int,
    question_text: str,
    user_answer: str,
    role: str,
    experience_level: str,
    interview_type: str,
    expected_competency: str = "",
    api_key: Optional[str] = None,
) -> Tuple[bool, Optional[EvaluationResult], Optional[str]]:
    """Evaluate a candidate's answer using Gemini structured response.

    Returns:
        (success: bool, evaluation: Optional[EvaluationResult], error_message: Optional[str])
    """
    # 1. Pre-validation
    is_valid, validation_err = validate_user_answer(user_answer)
    if not is_valid:
        return False, None, validation_err

    # 2. System Instruction
    system_instruction = (
        "You are a rigorous, constructive senior technical interviewer and hiring manager at a premier technology company. "
        "Your role is to critically evaluate a candidate's interview answer with high professional standards while providing "
        "encouraging, actionable feedback. "
        "Scoring Guidelines (0.0 to 10.0): "
        "- 9.0-10.0: Exceptional, covers nuances, edge cases, trade-offs, or uses structured STAR technique. "
        "- 7.0-8.9: Solid, accurate, and relevant with only minor gaps. "
        "- 5.0-6.9: Partially correct or superficial; lacks depth or precision. "
        "- Below 5.0: Inaccurate, misleading, or largely irrelevant. "
        "Always provide a concrete, articulate improved sample answer that demonstrates how an ideal candidate would reply."
    )

    prompt = f"""
    Evaluate the following interview answer:

    CANDIDATE CONTEXT:
    - Target Role: {role}
    - Experience Level: {experience_level}
    - Interview Category: {interview_type}

    INTERVIEW QUESTION #{question_id}:
    "{question_text}"
    Target Competency: {expected_competency}

    CANDIDATE'S SUBMITTED ANSWER:
    \"\"\"{user_answer.strip()}\"\"\"

    Please evaluate:
    1. Relevance to the question.
    2. Technical correctness and factual accuracy.
    3. Clarity, tone, and conciseness.
    4. Completeness and depth according to the '{experience_level}' expectations.
    5. Specific strengths, weaknesses, and omitted concepts.
    6. An improved sample answer illustrating ideal structure and terminology.

    Return the evaluation adhering strictly to the requested schema. Set question_id to {question_id}.
    """

    success, result_obj, err_msg = generate_structured_response(
        prompt=prompt,
        response_schema=EvaluationResult,
        system_instruction=system_instruction,
        api_key=api_key,
        temperature=0.3,  # Lower temperature for consistent, objective scoring
    )

    if not success or result_obj is None:
        return False, None, err_msg

    try:
        eval_result = result_obj  # type: ignore
        eval_result.question_id = question_id
        # Clamp score between 0.0 and 10.0 just in case
        eval_result.score = max(0.0, min(10.0, round(float(eval_result.score), 1)))
        return True, eval_result, None
    except Exception as e:
        return False, None, f"Failed to parse evaluation output: {str(e)}"


def render_evaluation_feedback(eval_result: EvaluationResult):
    """Render a modern visual scorecard for a single evaluated answer."""
    score = eval_result.score
    
    # Determine color badge based on score
    if score >= 8.0:
        badge_color = "#55A987"  # Success green
        badge_bg = "rgba(85, 169, 135, 0.15)"
        badge_text = "EXCELLENT"
    elif score >= 6.0:
        badge_color = "#36A6A0"  # Accent teal
        badge_bg = "rgba(54, 166, 160, 0.15)"
        badge_text = "COMPETENT"
    else:
        badge_color = "#D77B69"  # Error / Coral
        badge_bg = "rgba(215, 123, 105, 0.15)"
        badge_text = "NEEDS REFINEMENT"

    st.markdown(
        f"""
        <div class="cp-card" style="margin-top: 18px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                <div>
                    <span style="font-size:0.8rem; color:#A5B7B3; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Question Scorecard</span>
                    <h3 style="margin:4px 0 0 0; color:#F3F7F5; font-size:1.45rem;">
                        Score: <span style="color:{badge_color}; font-weight:800;">{score} / 10.0</span>
                    </h3>
                </div>
                <div style="background:{badge_bg}; border:1px solid {badge_color}; 
                            color:{badge_color}; padding:6px 14px; border-radius:20px; font-weight:700; font-size:0.85rem;">
                    {badge_text} • {eval_result.verdict}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sub-metric cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🎯 Relevance", f"{eval_result.relevance_score:.1f}/10")
    with c2:
        st.metric("⚙️ Technical", f"{eval_result.technical_correctness_score:.1f}/10")
    with c3:
        st.metric("💬 Clarity", f"{eval_result.clarity_score:.1f}/10")
    with c4:
        st.metric("📊 Completeness", f"{eval_result.completeness_score:.1f}/10")

    # Strengths and Weaknesses Columns
    col_str, col_weak = st.columns(2)
    with col_str:
        st.markdown(
            """
            <div style="background:rgba(85, 169, 135, 0.08); border:1px solid rgba(85, 169, 135, 0.3); border-left:4px solid #55A987; 
                        padding:14px 16px; border-radius:10px; margin: 12px 0;">
                <h4 style="margin:0 0 8px 0; color:#55A987; font-size:1.05rem;">💪 Key Strengths</h4>
            """,
            unsafe_allow_html=True,
        )
        for s in eval_result.strengths:
            st.markdown(f"- {s}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_weak:
        st.markdown(
            """
            <div style="background:rgba(215, 123, 105, 0.08); border:1px solid rgba(215, 123, 105, 0.3); border-left:4px solid #D77B69; 
                        padding:14px 16px; border-radius:10px; margin: 12px 0;">
                <h4 style="margin:0 0 8px 0; color:#D77B69; font-size:1.05rem;">⚠️ Areas for Growth</h4>
            """,
            unsafe_allow_html=True,
        )
        for w in eval_result.weaknesses:
            st.markdown(f"- {w}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Missing Points and Suggestions
    if eval_result.missing_points:
        with st.expander("🔍 Crucial Points You Missed (Click to view)", expanded=False):
            for mp in eval_result.missing_points:
                st.markdown(f"- **{mp}**")

    if eval_result.suggestions:
        with st.expander("💡 Actionable Recommendations (Click to view)", expanded=False):
            for sug in eval_result.suggestions:
                st.markdown(f"- {sug}")

    # Improved Sample Answer
    with st.expander("✨ AI-Crafted High-Scoring Model Answer", expanded=True):
        st.markdown(
            f"""
            <div style="background: #172728; border: 1px solid #36A6A0; 
                        border-radius: 10px; padding: 18px; color: #F3F7F5; line-height: 1.6; font-size: 0.95rem;">
                {eval_result.improved_sample_answer}
            </div>
            """,
            unsafe_allow_html=True,
        )
