from sqlalchemy.orm import Session
from ..models.db_models import RecommendationHistory
from .catalog import fallback_recommendations
from .gemini_service import GeminiService
import json

gemini = GeminiService()

HOME_ALLOCATION = {"furniture": 0.45, "lighting": 0.20, "decor": 0.20, "appliances": 0.15}
PARTY_ALLOCATION = {"catering": 0.50, "decoration": 0.20, "venue": 0.20, "entertainment": 0.10}
JEWELRY_ALLOCATION = {"necklace": 0.45, "earrings": 0.30, "bracelet": 0.15, "reserve": 0.10}

def allocation(planner, budget):
    weights = {"home": HOME_ALLOCATION, "party": PARTY_ALLOCATION, "jewelry": JEWELRY_ALLOCATION}[planner]
    return {k: round(budget*v, 2) for k,v in weights.items()}

def generate(planner, budget, context, db: Session, user_id: int, image_path=None):
    ai_data, warning = gemini.recommend(planner, budget, context, image_path)
    if ai_data:
        result = {
            "planner": planner,
            "budget": budget,
            "allocation": ai_data.get("allocation") or allocation(planner, budget),
            "summary": ai_data.get("summary", "Recommendations generated from your preferences."),
            "recommendations": ai_data.get("recommendations", []),
            "source": "gemini",
            "warnings": ai_data.get("warnings", []),
        }
    else:
        result = {
            "planner": planner,
            "budget": budget,
            "allocation": allocation(planner, budget),
            "summary": "Demo recommendations generated from the built-in catalog and budget rules.",
            "recommendations": fallback_recommendations(planner, budget, context),
            "source": "fallback",
            "warnings": [warning] if warning else [],
        }
    history = RecommendationHistory(user_id=user_id, planner=planner, budget=budget, query_json=json.dumps(context), result_json=json.dumps(result))
    db.add(history); db.commit()
    return result
