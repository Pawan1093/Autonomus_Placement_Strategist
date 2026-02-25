# roadmap_agent.py - Creates a personalized day-by-day study plan
# Based on missing skills and how many days student has before placement

from fastapi import APIRouter
from pydantic import BaseModel
from utils.gemini_client import ask_gemini
from typing import List
import json
import re

router = APIRouter()

class RoadmapRequest(BaseModel):
    missing_skills: List[str]
    role_title: str
    days_available: int = 30      # How many days until placement
    hours_per_day: int = 3        # How many hours student can study

@router.post("/generate")
async def generate_roadmap(request: RoadmapRequest):
    """
    Generate a personalized week-by-week study roadmap.
    Prioritizes the most important skills first.
    """
    
    prompt = f"""
    Create a study roadmap for a student preparing for: {request.role_title}
    Missing skills to learn: {', '.join(request.missing_skills)}
    Days available: {request.days_available}
    Hours per day: {request.hours_per_day}
    
    Return JSON with exactly this structure:
    {{
        "total_days": 30,
        "overview": "In 30 days, focus on X, Y, Z to be ready",
        "weeks": [
            {{
                "week": 1,
                "focus": "Python Fundamentals",
                "days": [
                    {{
                        "day": 1,
                        "topic": "Python basics - variables, loops, functions",
                        "tasks": ["Watch Python tutorial (2hr)", "Practice 10 problems on HackerRank"],
                        "free_resources": ["youtube.com/watch?v=...", "hackerrank.com/python"]
                    }}
                ]
            }}
        ],
        "daily_checklist": ["Morning: Theory (1hr)", "Evening: Practice (2hr)"],
        "motivation_tip": "You've got this! Small consistent steps lead to big results."
    }}
    
    Use only FREE resources. Return ONLY the JSON, no extra text.
    """
    
    ai_response = ask_gemini(prompt)
    
    try:
        clean_response = re.sub(r'```json|```', '', ai_response).strip()
        parsed = json.loads(clean_response)
        return {"success": True, "data": parsed}
    except:
        return {"success": True, "data": ai_response}