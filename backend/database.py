# database.py - Sets up our SQLite database
# SQLite is a free database that saves as a single file - perfect for us!

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# This creates a file called placement.db in your backend folder
engine = create_engine("sqlite:///placement.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User table - stores login info
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    analyses = relationship("Analysis", back_populates="user")

# Analysis table - stores each resume analysis
class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_title = Column(String)
    ats_score = Column(Integer)
    resume_data = Column(Text)    # JSON string
    jd_data = Column(Text)        # JSON string
    skill_gap_data = Column(Text) # JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="analyses")

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()