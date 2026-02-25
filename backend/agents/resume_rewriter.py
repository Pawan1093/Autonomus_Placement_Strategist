# resume_rewriter.py - The WOW feature
# Takes original resume + job description and rewrites the entire resume
# to be perfectly ATS optimized for that specific job

from fastapi import APIRouter
from pydantic import BaseModel
from utils.gemini_client import ask_gemini
from typing import List
import json
import re

router = APIRouter()

class RewriteRequest(BaseModel):
    resume_text: str
    job_description: str
    role_title: str
    missing_skills: List[str]

@router.post("/rewrite")
async def rewrite_resume(request: RewriteRequest):
    prompt = f"""
    You are an expert resume writer and ATS optimization specialist.
    
    A student needs their resume rewritten to perfectly match this job.
    
    ORIGINAL RESUME:
    {request.resume_text}
    
    TARGET JOB DESCRIPTION:
    {request.job_description}
    
    MISSING SKILLS TO INCORPORATE: {', '.join(request.missing_skills)}
    
    Rewrite the resume to:
    1. Use exact keywords from the job description
    2. Reorder skills to match job requirements
    3. Rewrite experience/project descriptions using job keywords
    4. Add action verbs (Developed, Implemented, Designed, Built, Optimized)
    5. Make it ATS-friendly with proper sections
    
    Return ONLY this JSON:
    {{
        "rewritten_resume": "Full rewritten resume text here with proper formatting using \\n for line breaks",
        "changes_made": ["Change 1", "Change 2", "Change 3"],
        "new_ats_score": 85,
        "keywords_added": ["keyword1", "keyword2"],
        "improvement_summary": "Brief summary of what was improved"
    }}
    """
    
    ai_response = ask_gemini(prompt)
    
    try:
        clean = re.sub(r'```json|```', '', ai_response).strip()
        match = re.search(r'\{.*\}', clean, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            return {"success": True, "data": parsed}
    except:
        pass
    
    return {"success": False, "data": ai_response}