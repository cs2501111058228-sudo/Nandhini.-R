from typing import Any
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1, max_length=128)

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1)
    style: str = Field(default="modern", max_length=80)
    quantities: dict[str, int] = Field(default_factory=dict)
    priorities: list[str] = Field(default_factory=list)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=100_000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="Any", max_length=120)
    preferences: list[str] = Field(default_factory=list)

class RecommendationResponse(BaseModel):
    planner: str
    budget: float
    allocation: dict[str, float]
    summary: str
    recommendations: list[dict[str, Any]]
    source: str
    warnings: list[str] = []

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
