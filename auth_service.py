from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import json
from sqlalchemy.orm import Session
from ..config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from ..models.db_models import User

ALGORITHM = "HS256"
ITERATIONS = 310000

def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def _unb64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))

def hash_password(password: str) -> str:
    salt = hashlib.sha256((SECRET_KEY + str(datetime.now(timezone.utc).timestamp())).encode()).digest()[:16]
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${_b64(salt)}${_b64(digest)}"

def verify_password(password: str, encoded: str) -> bool:
    try:
        scheme, iterations, salt, expected = encoded.split("$", 3)
        if scheme != "pbkdf2_sha256": return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), _unb64(salt), int(iterations))
        return hmac.compare_digest(_b64(digest), expected)
    except Exception:
        return False

def create_access_token(user_id: int) -> str:
    header = _b64(json.dumps({"alg": ALGORITHM, "typ": "JWT"}, separators=(",", ":")).encode())
    exp = int((datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    payload = _b64(json.dumps({"sub": str(user_id), "exp": exp}, separators=(",", ":")).encode())
    signing_input = f"{header}.{payload}".encode()
    signature = _b64(hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest())
    return f"{header}.{payload}.{signature}"

def decode_token(token: str) -> int:
    header, payload, signature = token.split(".", 2)
    expected = _b64(hmac.new(SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(signature, expected): raise ValueError("bad signature")
    data = json.loads(_unb64(payload))
    if int(data["exp"]) < int(datetime.now(timezone.utc).timestamp()): raise ValueError("expired")
    return int(data["sub"])

def authenticate(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user or not verify_password(password, user.password_hash): return None
    return user
