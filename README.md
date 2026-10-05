# PocketSmart AI — Complete Starter Project

This project implements the supplied PocketSmart AI documentation as a runnable FastAPI + Jinja2 application with Home, Party, and Jewelry planners, Gemini multimodal integration, authentication, sessions, recommendation history, validation, and fallback recommendations.

## Important source alignment
The supplied document mentions both Flask and FastAPI. The later milestones, route list, UI milestone, and conclusion describe **FastAPI**, so this implementation uses FastAPI. The document also names **Gemini 1.5 Flash Pro**; model availability changes over time, so `GEMINI_MODEL` is configurable and defaults to `gemini-2.5-flash`. The supplied planner/platform names are preserved.

The source describes third-party platform integration but does not provide official API credentials or API contracts. Therefore the implementation uses a small local demo catalog plus outbound platform search links instead of scraping. Replace that catalog with licensed/official APIs for production.

## Included
- FastAPI backend
- Jinja2 HTML/CSS/JavaScript frontend
- Home Interior planner
- Party Budget planner
- Jewelry Budget planner with optional outfit image
- Gemini text + image analysis
- Local fallback recommendation engine
- User registration/login/logout
- Signed session token in an HttpOnly cookie
- `/token`, `/session-info`, `/session-data`
- `/generate-home`, `/generate-party`, `/generate-jewelry`
- `/recommendations-details`, `/history`
- SQLite storage
- Recommendation history
- CORS
- Upload validation
- Automated tests

## VS Code installation
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Windows CMD: `copy .env.example .env`

Open `http://127.0.0.1:8000` and API documentation at `http://127.0.0.1:8000/docs`.

### Gemini setup
Create an API key in Google AI Studio/Google Cloud according to your Google setup, then put it in `.env`:
```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
USE_AI=true
```
If you only want to test the complete UI/backend without an API key:
```env
USE_AI=false
```

## Tests
```bash
pytest -q
```

## Structure
```text
PocketSmart_AI/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── db_models.py
│   │   └── schemas.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── pages.py
│   │   └── planners.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── catalog.py
│   │   ├── gemini_service.py
│   │   └── recommendation_service.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
├── tests/test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```
