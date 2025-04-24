from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.database import get_db
from models.db_models import RegisteredDomain

router = APIRouter()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the landing page"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/dashboard/{key}", response_class=HTMLResponse)
async def dashboard(request: Request, key: str, db: Session = Depends(get_db)):
    """Render the dashboard for a specific API key"""
    origin = str(request.url.scheme) + "://" + request.url.hostname
    # Find domain by API key
    domain = db.query(RegisteredDomain).filter(RegisteredDomain.api_key == key).first()
    if not domain:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request, 
            "domain": domain.domain, 
            "api_key": key,
            "origin": origin,
        }
    )
