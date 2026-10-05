import base64
import json
from pathlib import Path
from ..config import GEMINI_API_KEY, GEMINI_MODEL, USE_AI

class GeminiService:
    def __init__(self):
        self.enabled = bool(GEMINI_API_KEY) and USE_AI
        self.client = None
        if self.enabled:
            from google import genai
            self.client = genai.Client(api_key=GEMINI_API_KEY)

    def recommend(self, planner: str, budget: float, context: dict, image_path: str | None = None):
        if not self.enabled:
            return None, "AI disabled or GEMINI_API_KEY is not configured."
        from google.genai import types
        prompt = self._prompt(planner, budget, context)
        parts = [types.Part.from_text(text=prompt)]
        if image_path:
            raw = Path(image_path).read_bytes()
            mime = self._mime(image_path)
            parts.append(types.Part.from_bytes(data=raw, mime_type=mime))
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=parts,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.4,
                ),
            )
            data = json.loads(response.text)
            return data, None
        except Exception as exc:
            return None, f"Gemini request failed: {exc}"

    def _prompt(self, planner, budget, context):
        return f"""You are PocketSmart AI, a budget-aware recommendation assistant.\nPlanner: {planner}\nBudget: INR {budget:.2f}\nContext: {json.dumps(context, ensure_ascii=False)}\n\nReturn JSON only with this shape:\n{{\n  \"summary\": \"short useful summary\",\n  \"allocation\": {{\"category\": number}},\n  \"recommendations\": [{{\"name\":\"...\",\"category\":\"...\",\"estimated_total\": number,\"platform\":\"Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO/Other\",\"reason\":\"...\"}}],\n  \"warnings\": [\"...\"]\n}}\nRules: keep estimated totals within the budget; do not invent exact live prices or claim live availability; label estimates as estimates; prefer practical options; if an outfit image is provided, describe only observable style/color cues and use them for jewelry coordination."""

    @staticmethod
    def _mime(path):
        suffix = Path(path).suffix.lower()
        return {".jpg":"image/jpeg", ".jpeg":"image/jpeg", ".png":"image/png", ".webp":"image/webp"}.get(suffix, "application/octet-stream")
