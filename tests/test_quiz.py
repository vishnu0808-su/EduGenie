import pytest

from quiz_module import clean_json_block, validate_quiz


def test_clean_json_block():
    assert clean_json_block("```json\n[]\n```") == "[]"


def test_validate_quiz_accepts_three_questions():
    quiz = [
        {"question": f"Q{i}", "options": ["A", "B", "C", "D"], "correct_answer": "A", "explanation": "Because."}
        for i in range(3)
    ]
    assert len(validate_quiz(quiz)) == 3


def test_validate_quiz_rejects_wrong_count():
    with pytest.raises(ValueError):
        validate_quiz([])
