from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class UserConfig(BaseModel):
    id: UUID
    subreddits: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


class UserConfigUpdate(BaseModel):
    subreddits: Optional[List[str]] = None
    keywords: Optional[List[str]] = None


class Match(BaseModel):
    id: str
    reddit_id: str
    type: str
    subreddit: str
    title: str
    content: Optional[str] = None
    url: Optional[str] = None
    upvotes: Optional[int] = None
    num_comments: Optional[int] = None
    ratio: Optional[float] = None
    intent_score: Optional[float] = None
    matched_keywords: List[str] = Field(default_factory=list)
    sentiment: Optional[str] = None
    user_ids: List[UUID] = Field(default_factory=list)
    timestamp: datetime


class Metadata(BaseModel):
    id: int
    job_name: str
    synced: datetime


class User(BaseModel):
    id: str
    email: str
    name: Optional[str]


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime 