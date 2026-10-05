from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.db_models import User
from ..models.schemas import LoginRequest, RegisterRequest, TokenResponse
from ..services.auth_service import authenticate, create_access_token, hash_password
from ..config import SESSION_COOKIE_NAME

router = APIRouter()

def _set_cookie(resp, token):
    resp.set_cookie(SESSION_COOKIE_NAME, token, httponly=True, samesite="lax", secure=False, max_age=60*120)
    return resp

@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        return JSONResponse({"detail":"Enter a valid email address"}, status_code=422)
    if db.query(User).filter(User.email == email).first():
        return JSONResponse({"detail":"Email already registered"}, status_code=409)
    user = User(name=payload.name.strip(), email=email, password_hash=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    return _set_cookie(JSONResponse({"message":"Registered", "user":{"id":user.id,"name":user.name,"email":user.email}}), create_access_token(user.id))

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate(db, payload.email.strip().lower(), payload.password)
    if not user:
        return JSONResponse({"detail":"Invalid email or password"}, status_code=401)
    return _set_cookie(JSONResponse({"message":"Logged in", "user":{"id":user.id,"name":user.name,"email":user.email}}), create_access_token(user.id))

@router.post("/token", response_model=TokenResponse)
def token(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate(db, payload.email.strip().lower(), payload.password)
    if not user:
        return JSONResponse({"detail":"Invalid email or password"}, status_code=401)
    return {"access_token": create_access_token(user.id), "token_type":"bearer"}

@router.get("/logout")
def logout():
    resp = RedirectResponse("/login", status_code=303)
    resp.delete_cookie(SESSION_COOKIE_NAME)
    return resp
