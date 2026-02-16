from pydantic import BaseModel

class MarketAnalysis(BaseModel):
    probability: float  # Estimation (0.0 - 1.0)
    reasoning: str
    confidence: float   # LLM's confidence about his choice