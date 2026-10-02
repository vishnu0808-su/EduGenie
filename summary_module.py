from gemini_client import generate_text

SYSTEM = """You are EduGenie's summarization module. Summarize educational text faithfully. Preserve important facts, definitions, relationships, and steps. Use simple language. Do not add facts that are not supported by the input."""


async def summarize_text(text: str) -> str:
    prompt = f"Summarize the following educational passage for quick revision. Start with a one-sentence overview, then give key points.\n\nPASSAGE:\n{text}"
    return generate_text(prompt, system_instruction=SYSTEM, temperature=0.2, max_output_tokens=1000)
