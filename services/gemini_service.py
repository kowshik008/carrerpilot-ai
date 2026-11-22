"""CareerPilot AI — Gemini Core Service
=======================================
Direct integration with Google Gemini SDK using centralized model configuration.
"""

from typing import Optional, Tuple, Type
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel
from config import GEMINI_MODEL, FALLBACK_MODELS
from utils.gemini_helper import get_api_key, get_gemini_client


def test_gemini_connection(api_key: Optional[str] = None, model: str = GEMINI_MODEL) -> Tuple[bool, str]:
    """Test actual connectivity to Gemini using the configured model.
    Shows the REAL API status and never displays a fake success.
    """
    key = get_api_key(api_key)
    if not key:
        return False, "Gemini API Key is missing. Please configure it in .streamlit/secrets.toml or sidebar."

    try:
        client = get_gemini_client(key)
        response = client.models.generate_content(
            model=model,
            contents="Say 'OK' in one word.",
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=10,
            ),
        )
        if response and response.text:
            return True, f"Connected successfully to {model}!"
        return False, f"Received empty response from {model}."
    except APIError as e:
        err_msg = e.message if hasattr(e, "message") else str(e)
        return False, f"Gemini API Error ({model}): {err_msg}"
    except Exception as e:
        return False, f"Connection to {model} failed: {str(e)}"


def call_gemini_structured(
    prompt: str,
    response_schema: Type[BaseModel],
    system_instruction: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = GEMINI_MODEL,
    temperature: float = 0.5,
) -> Tuple[bool, Optional[BaseModel], Optional[str]]:
    """Invoke Gemini model for structured JSON schema generation using GEMINI_MODEL.
    Attempts primary GEMINI_MODEL first; handles capacity spikes gracefully.
    """
    key = get_api_key(api_key)
    if not key:
        return False, None, "API Key is missing. Please check .streamlit/secrets.toml."

    models_to_try = [model] + [m for m in FALLBACK_MODELS if m != model]
    last_err = f"Failed to call {model}"

    for candidate_model in models_to_try:
        try:
            client = get_gemini_client(key)
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
            if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg or "503" in err_msg or "high demand" in err_msg.lower():
                continue  # Try next available model in fallback sequence
            return False, None, f"Gemini API Error ({candidate_model}): {err_msg}"
        except Exception as e:
            last_err = str(e)
            continue

    return False, None, f"AI generation failed: {last_err}"
