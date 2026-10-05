import json
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..config import ALLOWED_IMAGE_TYPES, MAX_UPLOAD_MB
from ..database import get_db
from ..dependencies import get_current_user
from ..models.db_models import User, RecommendationHistory
from ..models.schemas import HomeRequest, PartyRequest
from ..services.recommendation_service import generate

router = APIRouter()
UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/generate-home")
def generate_home(payload: HomeRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    context = payload.model_dump()
    return generate("home", payload.budget, context, db, user.id)

@router.post("/generate-party")
def generate_party(payload: PartyRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    context = payload.model_dump()
    return generate("party", payload.budget, context, db, user.id)

@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...), occasion: str = Form(...), style: str = Form("modern"), preferences: str = Form(""), outfit: UploadFile | None = File(None),
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    if budget <= 0 or budget > 10_000_000: raise HTTPException(422, "Budget must be between 1 and 10,000,000")
    context = {"budget":budget,"occasion":occasion,"style":style,"preferences":preferences}
    image_path = None
    if outfit and outfit.filename:
        if outfit.content_type not in ALLOWED_IMAGE_TYPES: raise HTTPException(400, "Upload a JPG, PNG, or WEBP image")
        data = await outfit.read()
        if len(data) > MAX_UPLOAD_MB * 1024 * 1024: raise HTTPException(413, "Image is too large")
        suffix = Path(outfit.filename).suffix.lower()
        path = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
        path.write_bytes(data); image_path = str(path)
    return generate("jewelry", budget, context, db, user.id, image_path)

@router.get("/recommendations-details")
def recommendations_details(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(RecommendationHistory).filter_by(id=id, user_id=user.id).first()
    if not row: raise HTTPException(404, "Recommendation not found")
    return json.loads(row.result_json)

@router.get("/session-info")
def session_info(user: User = Depends(get_current_user)):
    return {"logged_in": True, "user_id": user.id, "name": user.name, "email": user.email}

@router.get("/session-data")
def session_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    count = db.query(RecommendationHistory).filter_by(user_id=user.id).count()
    return {"user_id":user.id,"recommendation_count":count}

@router.get("/history")
def history_api(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(RecommendationHistory).filter_by(user_id=user.id).order_by(RecommendationHistory.created_at.desc()).all()
    return [{"id":r.id,"planner":r.planner,"budget":r.budget,"created_at":r.created_at.isoformat()} for r in rows]
