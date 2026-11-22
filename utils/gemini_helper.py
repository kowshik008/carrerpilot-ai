"""CareerPilot AI - Gemini API Helper Module
===========================================
This module provides a unified interface for interacting with Google's Gemini models
using the official modern `google-genai` SDK.

Key Responsibilities:
1. Securely fetch and validate the Gemini API Key from environment or session.
2. Initialize and cache `google.genai.Client` connections.
3. Generate structured JSON conforming to Pydantic schemas (for questions & evaluations).
4. Perform native multimodal audio transcription from recorded speech.
5. Provide robust error handling for API quotas, timeouts, and network issues.
"""

import os
from typing import Optional, Tuple, Type
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel

# Load local environment variables from .env if present
load_dotenv()

from config import GEMINI_MODEL, FALLBACK_MODELS

# Centralized default Gemini model imported from config.py
DEFAULT_MODEL = GEMINI_MODEL


def get_api_key(override_key: Optional[str] = None) -> Optional[str]:
    """Retrieve the Gemini API key with priority:
    1. Explicit override passed by user/session (even if empty, respects override)
    2. Streamlit secrets (.streamlit/secrets.toml or st.secrets)
    3. Environment variable GEMINI_API_KEY from .env
    """
    if override_key is not None:
        return override_key.strip() if override_key.strip() else None

    # 1. Check Streamlit native secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"].strip()
    except Exception:
        pass

    # 2. Check .streamlit/secrets.toml file directly
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        secrets_path = os.path.join(base_dir, ".streamlit", "secrets.toml")
        if os.path.exists(secrets_path):
            with open(secrets_path, "r", encoding="utf-8") as f:
                for line in f:
                    line_s = line.strip()
                    if line_s.startswith("GEMINI_API_KEY"):
                        parts = line_s.split("=", 1)
                        if len(parts) == 2:
                            val = parts[1].strip().strip('"').strip("'")
                            if val:
                                return val
    except Exception:
        pass

    # 3. Check environment variable from .env
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    return None


def get_gemini_client(api_key: Optional[str] = None) -> genai.Client:
    """Initialize and return a google.genai.Client instance.
    Raises ValueError if no API key is available.
    """
    key = get_api_key(api_key)
    if not key:
        raise ValueError(
            "Gemini API Key is missing. Please provide it in a .env file or enter it in the sidebar."
        )
    return genai.Client(api_key=key)


def test_api_connection(api_key: Optional[str] = None, model: str = DEFAULT_MODEL) -> Tuple[bool, str]:
    """Test the validity of the API key with a lightweight prompt across available models.
    Returns: (success: bool, message: str)
    """
    key = get_api_key(api_key)
    if not key:
        return False, "Gemini API Key is missing. Please provide it in a .env file or enter it in the sidebar."

    models_to_try = [model] + [m for m in FALLBACK_MODELS if m != model]
    last_err = ""
    for candidate_model in models_to_try:
        try:
            client = get_gemini_client(api_key)
            response = client.models.generate_content(
                model=candidate_model,
                contents="Say 'OK' in one word.",
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=10,
                ),
            )
            if response and response.text:
                return True, f"Connected successfully to {candidate_model}!"
        except APIError as e:
            last_err = e.message if hasattr(e, "message") else str(e)
            continue
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            last_err = str(e)
            continue
    return False, f"Connection failed: {last_err}"


def generate_structured_response(
    prompt: str,
    response_schema: Type[BaseModel],
    system_instruction: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.5,
) -> Tuple[bool, Optional[BaseModel], Optional[str]]:
    """Generate structured output adhering strictly to a Pydantic schema using Gemini.
    Attempts candidate models if capacity spikes or deprecation is encountered.
    """
    models_to_try = [model] + [m for m in FALLBACK_MODELS if m != model]
    last_err = "No models available."

    for candidate_model in models_to_try:
        try:
            client = get_gemini_client(api_key)
            
            config = types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
                response_schema=response_schema,
                system_instruction=system_instruction,
            )

            response = client.models.generate_content(
                model=candidate_model,
                contents=prompt,
                config=config,
            )

            if not response or not response.text:
                continue

            if hasattr(response, "parsed") and response.parsed is not None:
                return True, response.parsed, None

            parsed_obj = response_schema.model_validate_json(response.text)
            return True, parsed_obj, None

        except APIError as e:
            err_msg = str(e)
            last_err = err_msg
            if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg or "high demand" in err_msg.lower() or "not available" in err_msg.lower():
                continue
            return False, None, f"Gemini API Error: {err_msg}"
        except ValueError as e:
            return False, None, str(e)
        except Exception as e:
            last_err = str(e)
            continue

    return False, None, f"AI generation failed across models: {last_err}"


def transcribe_audio_bytes(
    audio_bytes: bytes,
    mime_type: str = "audio/wav",
    api_key: Optional[str] = None,
    model: str = DEFAULT_MODEL,
) -> Tuple[bool, Optional[str], Optional[str]]:
    """Transcribe spoken audio into text using Gemini's native multimodal capabilities.

    Args:
        audio_bytes: Raw binary bytes of the recorded audio file.
        mime_type: MIME type of the audio (e.g. 'audio/wav', 'audio/mp3', 'audio/webm').
        api_key: Optional explicit API key.
        model: Multimodal Gemini model identifier.

    Returns:
        (success: bool, transcription: Optional[str], error_message: Optional[str])
    """
    if not audio_bytes or len(audio_bytes) < 100:
        return False, None, "Audio recording is empty or too short. Please speak clearly into your mic."

    try:
        client = get_gemini_client(api_key)

        audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type=mime_type,
        )

        prompt = (
            "You are a high-accuracy speech transcription engine. "
            "Please transcribe the following spoken audio interview answer word-for-word into plain English. "
            "Do NOT add any introductory remarks, explanations, quotes, or timestamps. "
            "Output ONLY the exact transcribed spoken words."
        )

        response = client.models.generate_content(
            model=model,
            contents=[audio_part, prompt],
            config=types.GenerateContentConfig(
                temperature=0.1,
            ),
        )

        if not response or not response.text:
            return False, None, "Transcription resulted in empty text. Please try speaking louder or closer to the mic."

        transcription = response.text.strip()
        return True, transcription, None

    except APIError as e:
        return False, None, f"Gemini API Error during transcription: {str(e)}"
    except ValueError as e:
        return False, None, str(e)
    except Exception as e:
        return False, None, f"Failed to transcribe audio: {str(e)}"
