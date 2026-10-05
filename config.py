import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

APP_NAME = os.getenv("APP_NAME", "PocketSmart AI")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pocketsmart.db")
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "pocketsmart_session")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))
USE_AI = os.getenv("USE_AI", "true").lower() == "true"
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
