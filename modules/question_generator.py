"""CareerPilot AI - Question Generator Module
===========================================
Generates tailored, high-caliber interview questions using Google Gemini.
Ensures strict JSON output matching the Pydantic schema:
- Role-specific questions
- Difficulty calibrated to experience level
- Category split (Technical, HR, or Mixed)
- Avoids repetition and trivial questions
"""

from typing import List, Tuple, Optional
from pydantic import BaseModel, Field
from utils.gemini_helper import generate_structured_response


class InterviewQuestion(BaseModel):
    """Schema for an individual interview question."""
    id: int = Field(description="1-based index of the question.")
    question: str = Field(description="The interview question text.")
    category: str = Field(description="Question category: 'Technical' or 'HR / Behavioral'.")
    difficulty: str = Field(description="Difficulty level: 'Beginner', 'Intermediate', or 'Advanced'.")
    expected_competency: str = Field(description="Core concept, skill, or behavioral trait being evaluated.")


class QuestionSet(BaseModel):
    """Schema for the full set of generated interview questions."""
    role: str = Field(description="Target job role.")
    experience_level: str = Field(description="Candidate's experience level.")
    interview_type: str = Field(description="Selected interview type.")
    questions: List[InterviewQuestion] = Field(description="List of generated questions.")


def generate_interview_questions(
    role: str,
    experience_level: str,
    interview_type: str,
    num_questions: int = 5,
    api_key: Optional[str] = None,
) -> Tuple[bool, Optional[List[InterviewQuestion]], Optional[str]]:
    """Call Gemini to generate a verified list of InterviewQuestions.

    Returns:
        (success: bool, questions: Optional[List[InterviewQuestion]], error_message: Optional[str])
    """
    system_instruction = (
        "You are an expert technical recruiter and senior hiring manager conducting realistic job interviews. "
        "Your task is to generate realistic, professional, and insightful interview questions tailored to the candidate's "
        "target role, experience level, and interview type. "
        "Rules: "
        "1. Every question must be distinct and non-repetitive. "
        "2. If interview_type is 'Technical', all questions must assess technical expertise, system design, or problem-solving. "
        "3. If interview_type is 'HR / Behavioral', focus on teamwork, conflict resolution, situational handling, and ethics. "
        "4. If interview_type is 'Mixed', balance technical questions and behavioral/situational questions appropriately. "
        "5. Calibrate the complexity precisely: 'Beginner' tests fundamentals and core syntax/concepts; "
        "'Intermediate' tests real-world application, optimization, and edge cases; "
        "'Advanced' tests architecture, trade-offs, scalability, and deep mastery. "
        "6. Return ONLY valid JSON adhering strictly to the requested schema."
    )

    prompt = f"""
    Please generate exactly {num_questions} interview questions for the following candidate profile:
    
    - Target Role: {role}
    - Candidate Experience Level: {experience_level}
    - Interview Type: {interview_type}
    - Required Question Count: {num_questions}

    Ensure each question is clear, realistic, and evaluates practical competencies required in top-tier company interviews.
    """

    success, result_obj, err_msg = generate_structured_response(
        prompt=prompt,
        response_schema=QuestionSet,
        system_instruction=system_instruction,
        api_key=api_key,
        temperature=0.7,
    )

    if not success or result_obj is None:
        return False, None, err_msg

    try:
        # Cast / access questions list
        questions = result_obj.questions  # type: ignore
        if not questions or len(questions) == 0:
            return False, None, "AI generated an empty set of questions. Please retry."
        
        # Guarantee sequential IDs 1..N
        for idx, q in enumerate(questions, start=1):
            q.id = idx

        return True, questions, None
    except Exception as e:
        return False, None, f"Failed to parse generated questions: {str(e)}"
