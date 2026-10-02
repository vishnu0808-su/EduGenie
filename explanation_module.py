from functools import lru_cache

from config import settings
from gemini_client import generate_text


@lru_cache(maxsize=1)
def _local_pipeline():
    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
        device=-1,
    )


def _local_explain(topic: str) -> str:
    generator = _local_pipeline()
    prompt = (
        "Explain the following educational concept to a beginner in simple language. "
        "Give a definition, 3 key points, and one simple example. Keep it concise.\n\n"
        f"Concept: {topic}"
    )
    result = generator(prompt, max_new_tokens=300, do_sample=False)
    return result[0]["generated_text"].strip()


async def explain_concept(topic: str) -> str:
    if settings.explanation_mode in {"local", "auto"}:
        try:
            return _local_explain(topic)
        except Exception:
            if settings.explanation_mode == "local":
                raise RuntimeError(
                    "The local LaMini-Flan-T5 model could not be loaded. Install the local dependencies or use EXPLANATION_MODE=gemini."
                )

    return generate_text(
        f"Explain this concept to a beginner using simple language, a short definition, key points, and one example:\n\n{topic}",
        system_instruction="You are EduGenie. Make complex concepts easy to understand without losing important meaning.",
        temperature=0.3,
        max_output_tokens=800,
    )
