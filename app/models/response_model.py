from pydantic import BaseModel
from typing import List


class GapSkill(BaseModel):
    skill: str
    priority: str


class FeedbackItem(BaseModel):
    skill: str
    suggestion: str
