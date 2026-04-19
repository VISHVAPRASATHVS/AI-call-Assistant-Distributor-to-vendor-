from pydantic import BaseModel
from typing import List, Dict

class SeedBrief(BaseModel):
    distributor_name: str
    challenges: List[str]

class TranscriptRequest(BaseModel):
    transcript: str

class InsightsResponse(BaseModel):
    problems: List[str]
    solutions: List[str]
    action_items: List[Dict[str, str]]
    sentiment_tags: List[Dict[str, str]]

class TranscriptResponse(BaseModel):
    transcript: List[str]
