import random
import string
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta

from models.database import get_db
from models.db_models import RegisteredDomain, VisitCount, VisitLog
from schemas.domain import DomainCreate, DomainResponse, StatsResponse

router = APIRouter()

def generate_api_key(length=9):
    """Generate a random API key of specified length"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def verify_api_key(domain: str, api_key: str, db: Session):
    """Verify that the API key is valid for the given domain"""
    domain_obj = db.query(RegisteredDomain).filter(RegisteredDomain.domain == domain).first()
    if not domain_obj or domain_obj.api_key != api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return domain_obj

@router.post("/register", response_model=DomainResponse)
def register_domain(domain_data: DomainCreate, db: Session = Depends(get_db)):
    """Register a new domain and generate an API key"""
    # Check if domain already exists
    existing_domain = db.query(RegisteredDomain).filter(RegisteredDomain.domain == domain_data.domain).first()
    if existing_domain:
        raise HTTPException(status_code=400, detail="Domain already registered")
    
    # Generate a unique API key
    api_key = generate_api_key()
    while db.query(RegisteredDomain).filter(RegisteredDomain.api_key == api_key).first():
        api_key = generate_api_key()
    
    # Create new domain record
    new_domain = RegisteredDomain(domain=domain_data.domain, api_key=api_key)
    db.add(new_domain)
    
    # Initialize visit count
    visit_count = VisitCount(domain=domain_data.domain, total_visits=0)
    db.add(visit_count)
    
    db.commit()
    db.refresh(new_domain)
    
    return new_domain

@router.get("/visit/{domain}")
def record_visit(domain: str, key: str = Query(...), db: Session = Depends(get_db)):
    """Record a visit for the specified domain"""
    # Verify API key
    domain_obj = verify_api_key(domain, key, db)
    
    # Increment visit count
    visit_count = db.query(VisitCount).filter(VisitCount.domain == domain).first()
    if not visit_count:
        visit_count = VisitCount(domain=domain, total_visits=1)
        db.add(visit_count)
    else:
        visit_count.total_visits += 1
    
    # Log visit
    visit_log = VisitLog(domain=domain)
    db.add(visit_log)
    
    db.commit()
    
    return {"success": True, "total_visits": visit_count.total_visits}

@router.get("/stats/{domain}", response_model=StatsResponse)
def get_stats(domain: str, key: str = Query(...), db: Session = Depends(get_db)):
    """Get visit statistics for the specified domain"""
    # Verify API key
    domain_obj = verify_api_key(domain, key, db)
    
    # Get visit count
    visit_count = db.query(VisitCount).filter(VisitCount.domain == domain).first()
    if not visit_count:
        raise HTTPException(status_code=404, detail="No visit data found")
    
    # Get daily visits for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_visits = db.query(VisitLog).filter(
        VisitLog.domain == domain,
        VisitLog.timestamp >= thirty_days_ago
    ).order_by(VisitLog.timestamp.desc()).all()
    
    return {
        "domain": domain,
        "total_visits": visit_count.total_visits,
        "daily_visits": daily_visits
    }
