from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import settings
from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie", version="1.0.0", description="Google Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=settings.max_input_chars)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=settings.max_input_chars)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
  return templates.TemplateResponse(
    request=request,
    name="index.html"
)


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", "gemini_configured": settings.gemini_configured}


@app.post("/qa")
async def qa(payload: QuestionRequest):
    try:
        return {"result": await answer_question(payload.question)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain")
async def explain(payload: TextRequest):
    try:
        return {"result": await explain_concept(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz")
async def quiz(payload: TextRequest):
    try:
        return {"result": await generate_quiz(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        return {"result": await summarize_text(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):
    try:
        return {"result": await get_learning_recommendations(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
