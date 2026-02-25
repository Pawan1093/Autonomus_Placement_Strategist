# interview_agent.py - Generates interview questions and evaluates answers
# This is the mock interview feature - the heart of the project

from fastapi import APIRouter
from pydantic import BaseModel
from utils.gemini_client import ask_gemini
from typing import List
import json
import re

router = APIRouter()

class InterviewRequest(BaseModel):
    role_title: str
    skills: List[str]
    difficulty: str = "medium"    # easy, medium, hard
    num_questions: int = 5

class EvaluateRequest(BaseModel):
    question: str
    user_answer: str
    role_title: str

@router.post("/generate-questions")
async def generate_questions(request: InterviewRequest):
    """
    Generate mock interview questions based on the role and skills.
    Mix of technical, behavioral, and situational questions.
    """
    
    prompt = f"""
    Generate {request.num_questions} interview questions for a {request.role_title} role.
    Focus on these skills: {', '.join(request.skills)}
    Difficulty level: {request.difficulty}
    
    Return JSON with exactly this structure:
    {{
        "questions": [
            {{
                "id": 1,
                "question": "Explain the difference between REST and GraphQL?",
                "type": "technical",
                "skill_tested": "API Design",
                "hint": "Think about data fetching differences",
                "ideal_answer_points": ["point1", "point2", "point3"]
            }}
        ]
    }}
    
    Mix question types: technical (60%), behavioral (20%), situational (20%)
    Return ONLY the JSON, no extra text.
    """
    
    ai_response = ask_gemini(prompt)
    
    try:
        clean_response = re.sub(r'```json|```', '', ai_response).strip()
        parsed = json.loads(clean_response)
        return {"success": True, "data": parsed}
    except:
        return {"success": True, "data": ai_response}

@router.post("/evaluate-answer")
async def evaluate_answer(request: EvaluateRequest):
    """
    Student submits their answer and Gemini evaluates it.
    Returns score, feedback, and model answer.
    """
    
    prompt = f"""
    Role: {request.role_title}
    Interview Question: {request.question}
    Student's Answer: {request.user_answer}
    
    Evaluate the answer and return JSON with exactly this structure:
    {{
        "score": 7,
        "score_out_of": 10,
        "verdict": "Good / Needs Improvement / Excellent / Poor",
        "what_was_good": "Student correctly mentioned X and Y",
        "what_was_missing": "Should have also mentioned Z",
        "model_answer": "A complete ideal answer for this question",
        "tip": "One specific tip to improve this type of answer"
    }}
    
    Be encouraging but honest. Return ONLY the JSON, no extra text.
    """
    
    ai_response = ask_gemini(prompt)
    
    try:
        clean_response = re.sub(r'```json|```', '', ai_response).strip()
        parsed = json.loads(clean_response)
        return {"success": True, "data": parsed}
    except:
        return {"success": True, "data": ai_response}