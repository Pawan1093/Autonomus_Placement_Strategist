from fastapi import APIRouter
from pydantic import BaseModel
from utils.gemini_client import ask_gemini
import json
import re

router = APIRouter()

class CompanyPrepRequest(BaseModel):
    company: str
    role: str
    skills: list

@router.post("/prep")
async def get_company_prep(request: CompanyPrepRequest):
    prompt = f"""
    You are an expert on {request.company}'s hiring process.
    Role: {request.role}
    Student skills: {', '.join(request.skills)}
    
    Return ONLY this JSON:
    {{
        "company": "{request.company}",
        "overview": "Brief company overview and culture",
        "hiring_process": [
            {{"round": 1, "name": "Online Test", "description": "What happens in this round", "duration": "1 hour", "tips": "How to prepare"}}
        ],
        "interview_questions": [
            {{"question": "Tell me about yourself", "type": "HR", "tip": "Keep it under 2 minutes"}}
        ],
        "salary_range": "3-6 LPA for freshers",
        "preparation_tips": ["Tip 1", "Tip 2", "Tip 3"],
        "must_know_topics": ["Topic 1", "Topic 2"],
        "company_values": ["Value 1", "Value 2"],
        "difficulty": "easy/medium/hard",
        "success_rate": "65%"
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