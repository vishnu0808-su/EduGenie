import json
import re
from typing import Any

from gemini_client import generate_json

QUIZ_SCHEMA = {
    "type": "array",
    "minItems": 3,
    "maxItems": 3,
    "items": {
        "type": "object",
        "properties": {
            "question": {"type": "string"},
            "options": {"type": "array", "minItems": 4, "maxItems": 4, "items": {"type": "string"}},
            "correct_answer": {"type": "string"},
            "explanation": {"type": "string"},
        },
        "required": ["question", "options", "correct_answer", "explanation"],
    },
}

SYSTEM = """You are EduGenie's quiz generator. Create exactly three educational multiple-choice questions from the supplied topic or passage. Each question must have exactly four options and exactly one correct answer. The correct_answer must exactly match one option. Include a short explanation. Only use information supported by the input."""


def clean_json_block(raw: str) -> str:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def validate_quiz(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Quiz must contain exactly 3 questions.")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Invalid quiz question format.")
        if not isinstance(item.get("question"), str):
            raise ValueError("Each quiz question needs question text.")
        options = item.get("options")
        if not isinstance(options, list) or len(options) != 4 or not all(isinstance(x, str) for x in options):
            raise ValueError("Each quiz question must have exactly 4 options.")
        if item.get("correct_answer") not in options:
            raise ValueError("correct_answer must match one of the options.")
        if not isinstance(item.get("explanation"), str):
            raise ValueError("Each question needs an explanation.")
    return data


async def generate_quiz(text: str) -> list[dict[str, Any]]:
    prompt = f"Generate the quiz from this topic or passage:\n\n{text}"

    try:
        raw = generate_json(
            prompt,
            schema=QUIZ_SCHEMA,
            system_instruction=SYSTEM,
        )
    except Exception as exc:
        raise RuntimeError(
            "Gemini is temporarily unavailable. Please try again after a few minutes."
        ) from exc

    try:
        data = json.loads(clean_json_block(raw))
    except json.JSONDecodeError as exc:
        raise ValueError("Gemini returned invalid quiz JSON.") from exc

    return validate_quiz(data)