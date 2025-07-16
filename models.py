from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

class NewsArticleRequest(BaseModel):
    url: HttpUrl
    
class NewsTopicRequest(BaseModel):
    topic: str
    limit: Optional[int] = 5

class NewsArticle(BaseModel):
    title: str
    url: str
    content: str
    author: Optional[str] = None
    publish_date: Optional[datetime] = None
    source: Optional[str] = None

class Summary(BaseModel):
    original_title: str
    summary: str
    key_points: List[str]
    sentiment: str
    
class FactCheck(BaseModel):
    claim: str
    verification_status: str  # "verified", "false", "partially_true", "unverified"
    evidence: List[str]
    confidence_score: float
    sources: List[str]

class NewsAnalysis(BaseModel):
    article: NewsArticle
    summary: Summary
    fact_checks: List[FactCheck]
    credibility_score: float
    overall_assessment: str
    processing_time: float

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int