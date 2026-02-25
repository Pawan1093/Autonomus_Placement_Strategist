# jd_agent.py - Analyzes the Job Description that the student pastes
# Extracts required skills, experience level, and role details

from fastapi import APIRouter
from pydantic import BaseModel
from utils.gemini_client import ask_gemini
import json
import re

router = APIRouter()

# This defines what data we expect from the frontend
class JDRequest(BaseModel):
    job_description: str

@router.post("/analyze")
async def analyze_jd(request: JDRequest):
    """
    Paste a job description and get back:
    - Required skills
    - Nice-to-have skills
    - Experience required
    - Role summary
    """
    
    prompt = f"""
    Analyze this job description and return a JSON response with exactly this structure:
    {{
        "role_title": "job title",
        "company_type": "startup/MNC/product/service",
        "required_skills": ["skill1", "skill2", "skill3"],
        "preferred_skills": ["skill1", "skill2"],
        "experience_required": "0-2 years / fresher etc",
        "key_responsibilities": ["resp1", "resp2", "resp3"],
        "interview_topics": ["topic1", "topic2", "topic3"],
        "difficulty_level": "easy/medium/hard"
    }}
    
    Job Description:
    {request.job_description}
    
    Return ONLY the JSON, no extra text.
    """
    
    ai_response = ask_gemini(prompt)
    
    try:
        clean_response = re.sub(r'```json|```', '', ai_response).strip()
        parsed = json.loads(clean_response)
        return {"success": True, "data": parsed}
    except:
        return {"success": True, "data": ai_response}