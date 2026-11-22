"""CareerPilot AI - Voice Processing Helper Module
=================================================
Manages microphone audio input recorded via Streamlit and orchestrates
transcription using Google Gemini's native multimodal audio capabilities.

Features:
- Validates recorded audio buffer (checks size, type, non-emptiness).
- Dispatches binary audio payload to `gemini_helper.transcribe_audio_bytes`.
- Returns user-friendly status, transcribed text, or actionable error instructions.
- Provides a clean Streamlit UI widget for recording and live preview/editing.
"""

from typing import Tuple, Optional
import streamlit as st
from utils.gemini_helper import transcribe_audio_bytes


def process_audio_recording(
    audio_file,
    api_key: Optional[str] = None,
) -> Tuple[bool, Optional[str], Optional[str]]:
    """Process an audio file uploaded or recorded via st.audio_input.

    Args:
        audio_file: The Streamlit UploadedFile or buffer from st.audio_input.
        api_key: Optional Gemini API key.

    Returns:
        (success: bool, transcription: Optional[str], error_message: Optional[str])
    """
    if audio_file is None:
        return False, None, "No audio detected. Please record a voice note."

    try:
        # Read the raw binary content
        audio_bytes = audio_file.read()
        
        # Reset buffer pointer in case it's re-read later
        if hasattr(audio_file, "seek"):
            audio_file.seek(0)

        if not audio_bytes or len(audio_bytes) < 200:
            return False, None, "Audio recording is empty or silent. Please check your microphone and speak clearly."

        # Detect MIME type (default to audio/wav)
        mime_type = getattr(audio_file, "type", "audio/wav") or "audio/wav"

        # Dispatch to Gemini multimodal audio transcription
        success, transcription, err = transcribe_audio_bytes(
            audio_bytes=audio_bytes,
            mime_type=mime_type,
            api_key=api_key,
        )

        return success, transcription, err

    except Exception as e:
        return False, None, f"An error occurred while processing your voice recording: {str(e)}"
