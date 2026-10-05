from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .routes.auth import router as auth_router
from .routes.pages import router as pages_router
from .routes.planners import router as planners_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="PocketSmart AI", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(planners_router)

@app.get("/health")
def health(): return {"status":"ok","service":"PocketSmart AI"}
