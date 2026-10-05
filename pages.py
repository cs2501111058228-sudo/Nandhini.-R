from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models.db_models import User, RecommendationHistory

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def index(request: Request): return templates.TemplateResponse("index.html", {"request":request})

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request): return templates.TemplateResponse("login.html", {"request":request})

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request): return templates.TemplateResponse("register.html", {"request":request})

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recent = db.query(RecommendationHistory).filter_by(user_id=user.id).order_by(RecommendationHistory.created_at.desc()).limit(5).all()
    return templates.TemplateResponse("dashboard.html", {"request":request,"user":user,"recent":recent})

@router.get("/history-page", response_class=HTMLResponse)
def history_page(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(RecommendationHistory).filter_by(user_id=user.id).order_by(RecommendationHistory.created_at.desc()).all()
    return templates.TemplateResponse("history.html", {"request":request,"user":user,"rows":rows})

@router.get("/planner/{planner}", response_class=HTMLResponse)
def planner_page(request: Request, planner: str):
    if planner not in {"home","party","jewelry"}: return HTMLResponse("Planner not found", status_code=404)
    return templates.TemplateResponse("planner.html", {"request":request,"planner":planner})
