import os
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from models.database import engine, Base
from models.db_models import RegisteredDomain, VisitCount, VisitLog
from routes import api, html
from middleware.bot_detection import BotDetectionMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Visit Tracker API",
    description="Track visits to your website with a simple API",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This will be dynamically updated based on registered domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add bot detection middleware
app.add_middleware(BotDetectionMiddleware)

# Include routers
app.include_router(api.router, prefix="/api", tags=["api"])
app.include_router(html.router, tags=["html"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
