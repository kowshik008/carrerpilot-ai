"""CareerPilot AI — Roadmap Service
==================================
Service for career roadmap generation using centralized GEMINI_MODEL.
"""

from typing import Optional, Tuple
from config import GEMINI_MODEL
from modules.career_roadmap import CareerRoadmapPlan, generate_ai_roadmap


def create_roadmap(
    role: str,
    experience_level: str,
    timeline: str,
    api_key: Optional[str] = None,
    model: str = GEMINI_MODEL,
) -> Tuple[bool, Optional[CareerRoadmapPlan], Optional[str]]:
    """Generate career roadmap using Gemini."""
    return generate_ai_roadmap(
        role=role,
        experience_level=experience_level,
        timeline=timeline,
        api_key=api_key,
    )
