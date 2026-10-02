from gemini_client import generate_text

SYSTEM = """You are EduGenie's learning-path planner. Build practical, age-appropriate educational plans. Start from beginner concepts and progress to advanced concepts. Include estimated time, what to learn, a practice activity, and resource types. Do not fabricate specific URLs. If resources are requested, suggest reliable resource names or categories without pretending to have verified links."""


async def get_learning_recommendations(topic: str) -> str:
    prompt = f"Create a personalized learning path for: {topic}\n\nFormat:\n1. Goal\n2. Beginner (topics + suggested time)\n3. Intermediate (topics + suggested time)\n4. Advanced (topics + suggested time)\n5. Weekly practice plan\n6. Resource suggestions\n7. How to check progress"
    return generate_text(prompt, system_instruction=SYSTEM, temperature=0.5, max_output_tokens=1600)
