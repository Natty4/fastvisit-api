from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.database import Base

class RegisteredDomain(Base):
    __tablename__ = "registered_domains"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    visit_count = relationship("VisitCount", back_populates="domain_rel", uselist=False, cascade="all, delete-orphan")
    visit_logs = relationship("VisitLog", back_populates="domain_rel", cascade="all, delete-orphan")

class VisitCount(Base):
    __tablename__ = "visit_counts"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, ForeignKey("registered_domains.domain", ondelete="CASCADE"), unique=True)
    total_visits = Column(Integer, default=0)

    domain_rel = relationship("RegisteredDomain", back_populates="visit_count")

class VisitLog(Base):
    __tablename__ = "visit_logs"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, ForeignKey("registered_domains.domain", ondelete="CASCADE"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    domain_rel = relationship("RegisteredDomain", back_populates="visit_logs")
