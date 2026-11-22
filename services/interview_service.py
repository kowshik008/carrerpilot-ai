"""CareerPilot AI — Interview Service
====================================
Handles question generation and answer evaluation using centralized GEMINI_MODEL.
"""

from typing import List, Tuple, Optional
from pydantic import BaseModel
from config import GEMINI_MODEL
from modules.question_generator import InterviewQuestion, QuestionSet, generate_interview_questions
from modules.answer_evaluator import EvaluationResult, evaluate_answer


def generate_questions_for_role(
    role: str,
    experience_level: str,
    interview_type: str,
    num_questions: int = 5,
    api_key: Optional[str] = None,
    model: str = GEMINI_MODEL,
) -> Tuple[bool, Optional[List[InterviewQuestion]], Optional[str]]:
    """Generate interview questions calibrated to role and experience level."""
    return generate_interview_questions(
        role=role,
        experience_level=experience_level,
        interview_type=interview_type,
        num_questions=num_questions,
        api_key=api_key,
    )


def evaluate_candidate_answer(
    question_id: int,
    question_text: str,
    user_answer: str,
    role: str,
    experience_level: str,
    interview_type: str,
    expected_competency: str = "",
    api_key: Optional[str] = None,
    model: str = GEMINI_MODEL,
) -> Tuple[bool, Optional[EvaluationResult], Optional[str]]:
    """Evaluate candidate answer using rubric scoring."""
    return evaluate_answer(
        question_id=question_id,
        question_text=question_text,
        user_answer=user_answer,
        role=role,
        experience_level=experience_level,
        interview_type=interview_type,
        expected_competency=expected_competency,
        api_key=api_key,
    )
