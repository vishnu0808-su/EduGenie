# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Q&A
- Concept explanation
- 3-question MCQ quiz generation
- Text summarization
- Beginner-to-advanced learning paths

## Architecture

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    ├── test_quiz.py
    └── test_app.py
```

## VS Code setup

### 1. Open the project

Open the `EduGenie` folder in VS Code.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The default `EXPLANATION_MODE=auto` attempts the documented LaMini-Flan-T5 local explanation model first. To install that local model's dependencies:

```bash
pip install -r requirements-local.txt
```

If you want a lighter installation, set `EXPLANATION_MODE=gemini` in `.env`; then only `requirements.txt` is needed.

### 4. Configure Gemini

Copy `.env.example` to `.env` and put your Gemini API key in `GEMINI_API_KEY`.

Do not commit `.env` or expose the API key in frontend JavaScript.

### 5. Run

```bash
uvicorn main:app --reload
```

Open:

`http://127.0.0.1:8000`

FastAPI API documentation is available at `/docs`.

## API endpoints

- `POST /qa` — `{"question":"What is photosynthesis?"}`
- `POST /explain` — `{"text":"Explain photosynthesis"}`
- `POST /quiz` — `{"text":"Photosynthesis is..."}`
- `POST /summarize` — `{"text":"Long educational passage..."}`
- `POST /learn/recommendations` — `{"text":"SQL"}`
- `GET /health` — service/configuration check

## Testing

Install pytest:

```bash
pip install pytest
```

Run tests:

```bash
pytest -q
```

The tests validate the API shape and quiz validation without making paid/external Gemini calls.

## Notes

The supplied documentation names Gemini 1.5 Pro. The implementation uses the current Google Gen AI Python SDK and reads the model name from `GEMINI_MODEL`, so the model can be changed without editing application code.
