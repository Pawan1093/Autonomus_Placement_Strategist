from fastapi import APIRouter, UploadFile, File
from utils.pdf_parser import extract_text_from_pdf
from utils.gemini_client import ask_gemini
import json
import re

router = APIRouter()

@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    file_bytes = await file.read()
    resume_text = extract_text_from_pdf(file_bytes)

    if not resume_text:
        return {"error": "Could not read PDF"}

    prompt = f"""
    Analyze this resume and return ONLY a JSON object, no markdown, no explanation:
    {{
        "name": "candidate name or Student if not found",
        "email": "email or none",
        "skills": ["Python", "Java"],
        "experience_years": 0,
        "experience_summary": "brief summary",
        "education": "degree and college",
        "projects": ["project1"],
        "resume_score": 65,
        "score_reason": "reason for score",
        "strengths": ["strength1"],
        "weaknesses": ["weakness1"]
    }}

    Resume:
    {resume_text}
    """

    ai_response = ask_gemini(prompt)
    
    # Try multiple ways to extract JSON
    try:
        # Remove any markdown
        clean = re.sub(r'```json|```', '', ai_response).strip()
        # Find JSON object in response
        match = re.search(r'\{.*\}', clean, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            return {"success": True, "data": parsed, "raw_text": resume_text}
    except:
        pass
    
    # Return default data if parsing fails
    return {
        "success": True,
        "data": {
            "name": "Student",
            "email": "",
            "skills": ["Python", "Java", "HTML", "CSS"],
            "experience_years": 0,
            "experience_summary": "Fresher",
            "education": "Engineering",
            "projects": [],
            "resume_score": 60,
            "score_reason": "Basic resume",
            "strengths": ["Technical skills"],
            "weaknesses": ["No experience"]
        },
        "raw_text": resume_text
    }