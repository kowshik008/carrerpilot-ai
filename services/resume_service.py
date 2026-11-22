"""CareerPilot AI — Resume Service
=================================
Service for ATS resume auditing using centralized GEMINI_MODEL.
"""

from typing import Optional, Tuple
from config import GEMINI_MODEL
from modules.resume_analyzer import ResumeAnalysisResult, analyze_resume_text


def audit_resume(
    resume_text: str,
    target_role: str,
    api_key: Optional[str] = None,
    model: str = GEMINI_MODEL,
) -> Tuple[bool, Optional[ResumeAnalysisResult], Optional[str]]:
    """Audit resume text against target role using Gemini."""
    return analyze_resume_text(
        resume_text=resume_text,
        target_role=target_role,
        api_key=api_key,
    )
