"""CareerPilot AI — Centralized Platform Configuration
=====================================================
Centralized model configuration and platform-wide constants.
"""

import os

# Centralized Google Gemini Model Configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Fallback sequence in case of temporary regional capacity spikes
FALLBACK_MODELS = [
    GEMINI_MODEL,
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-flash-latest",
]
