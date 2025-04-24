from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List
from datetime import datetime
import re

class DomainBase(BaseModel):
    domain: str
    
    @validator('domain')
    def validate_domain(cls, v):
        # Simple domain validation
        pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid domain format')
        return v

class DomainCreate(DomainBase):
    pass

class DomainResponse(DomainBase):
    api_key: str
    
    class Config:
        orm_mode = True

class VisitLogResponse(BaseModel):
    timestamp: datetime
    
    class Config:
        orm_mode = True

class StatsResponse(BaseModel):
    domain: str
    total_visits: int
    daily_visits: List[VisitLogResponse]
    
    class Config:
        orm_mode = True
