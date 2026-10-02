from gemini_client import generate_text

SYSTEM = """You are EduGenie, a friendly educational assistant. Answer academic questions accurately and concisely. Explain unfamiliar terms in simple language. If a question is ambiguous, state the assumption you made. Do not invent citations or sources."""


async def answer_question(question: str) -> str:
    prompt = f"Answer this student's question clearly. Prefer short paragraphs and bullets when useful.\n\nQuestion: {question}"
    return generate_text(prompt, system_instruction=SYSTEM, temperature=0.3, max_output_tokens=900)
