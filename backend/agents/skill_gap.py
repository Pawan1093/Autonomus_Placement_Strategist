from fastapi import APIRouter
from pydantic import BaseModel
from utils.gemini_client import ask_gemini
from typing import List
import json
import re

router = APIRouter()

class SkillGapRequest(BaseModel):
    resume_skills: List[str]
    required_skills: List[str]
    preferred_skills: List[str]
    role_title: str

@router.post("/analyze")
async def analyze_skill_gap(request: SkillGapRequest):
    prompt = f"""
    Student skills: {', '.join(request.resume_skills)}
    Job required skills: {', '.join(request.required_skills)}
    Job preferred skills: {', '.join(request.preferred_skills)}
    Role: {request.role_title}

    Return ONLY this JSON, no markdown:
    {{
        "ats_score": 65,
        "matched_skills": ["Python"],
        "missing_critical_skills": ["React", "Node.js"],
        "missing_preferred_skills": ["Docker"],
        "learning_priority": [
            {{"skill": "React", "priority": "high", "estimated_days": 14, "free_resource": "react.dev"}}
        ],
        "overall_readiness": "partially ready",
        "readiness_message": "You are 65% ready. Focus on React and Node.js first."
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

    # Default fallback
    matched = list(set(request.resume_skills) & set(request.required_skills))
    missing = list(set(request.required_skills) - set(request.resume_skills))
    score = int((len(matched) / max(len(request.required_skills), 1)) * 100)

    return {
        "success": True,
        "data": {
            "ats_score": score,
            "matched_skills": matched,
            "missing_critical_skills": missing,
            "missing_preferred_skills": request.preferred_skills,
            "learning_priority": [],
            "overall_readiness": "partially ready",
            "readiness_message": f"You matched {score}% of required skills!"
        }
    }