from pydantic import BaseModel, Field
from typing import Literal, Optional


GuardCategory = Literal[
    "safe",
    "profanity",
    "insult",
    "harassment",
    "hate",
    "sexual",
    "violence",
    "illegal",
    "self_harm",
    "other_policy_violation",
]


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class GuardDecision(BaseModel):
    allowed: bool = Field(description="Можно ли пропустить текст")
    category: GuardCategory
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
    answer_to_user: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    model: str
    blocked: bool = False
    guard_category: Optional[str] = None
    guard_reason: Optional[str] = None