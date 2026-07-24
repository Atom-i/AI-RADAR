from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class Paper(BaseModel):
    title: str
    authors: str
    source: str
    keyword: str

class Repository(BaseModel):
    name: str
    owner: str
    url: str
    description: Optional[str]
    stars: int
    language: Optional[str]
    updated_at: str
    source: str

class NewsItem(BaseModel):
    title: str
    link: str
    published: str
    source: str
    keywords: List[str]

class Trend(BaseModel):
    trend: str
    count: int

class RadarData(BaseModel):
    timestamp: datetime
    papers: List[Paper]
    repositories: List[Repository]
    news: List[NewsItem]
    trends: List[Trend]