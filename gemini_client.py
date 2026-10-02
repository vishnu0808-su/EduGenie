from functools import lru_cache

from config import settings


@lru_cache(maxsize=1)
def get_client():
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError(
            "google-genai is not installed. Run: pip install -r requirements.txt"
        ) from exc
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to your .env file and restart the server."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def _types():
    try:
        from google.genai import types
        return types
    except ImportError as exc:
        raise RuntimeError(
            "google-genai is not installed. Run: pip install -r requirements.txt"
        ) from exc


def generate_text(prompt: str, *, system_instruction: str | None = None, temperature: float = 0.4, max_output_tokens: int = 1200) -> str:
    client = get_client()
    types = _types()
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


def generate_json(prompt: str, *, schema: dict, system_instruction: str | None = None) -> str:
    client = get_client()
    types = _types()
    config = types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=1800,
        response_mime_type="application/json",
        response_schema=schema,
        system_instruction=system_instruction,
    )
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty JSON response.")
    return text
