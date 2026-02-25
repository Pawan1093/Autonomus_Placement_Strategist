# auth_agent.py - Handles login, signup, and saving user data

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, User, Analysis
from pydantic import BaseModel
from passlib.context import CryptContext
import json

router = APIRouter()

# This handles password hashing - never store plain passwords!
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SaveAnalysisRequest(BaseModel):
    user_id: int
    role_title: str
    ats_score: int
    resume_data: dict
    jd_data: dict
    skill_gap_data: dict

@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password before saving
    hashed = pwd_context.hash(request.password)
    
    user = User(name=request.name, email=request.email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "user": {"id": user.id, "name": user.name, "email": user.email}
    }

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")
    
    # Check password
    if not pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Wrong password")
    
    return {
        "success": True,
        "user": {"id": user.id, "name": user.name, "email": user.email}
    }

@router.post("/save-analysis")
def save_analysis(request: SaveAnalysisRequest, db: Session = Depends(get_db)):
    analysis = Analysis(
        user_id=request.user_id,
        role_title=request.role_title,
        ats_score=request.ats_score,
        resume_data=json.dumps(request.resume_data),
        jd_data=json.dumps(request.jd_data),
        skill_gap_data=json.dumps(request.skill_gap_data),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return {"success": True, "analysis_id": analysis.id}

@router.get("/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    analyses = db.query(Analysis).filter(
        Analysis.user_id == user_id
    ).order_by(Analysis.created_at.desc()).all()
    
    return {
        "success": True,
        "analyses": [
            {
                "id": a.id,
                "role_title": a.role_title,
                "ats_score": a.ats_score,
                "resume_data": json.loads(a.resume_data),
                "jd_data": json.loads(a.jd_data),
                "skill_gap_data": json.loads(a.skill_gap_data),
                "created_at": str(a.created_at)
            }
            for a in analyses
        ]
    }