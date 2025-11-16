# backend/db.py
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_interview.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SessionLog(Base):
    __tablename__ = "session_logs"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, index=True)
    transcript = Column(Text, default="")
    proctoring_flags = Column(JSON, default=[])
    scores = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")