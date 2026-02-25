from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import create_tables

load_dotenv()

app = FastAPI(title="Placement Strategist API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
create_tables()

from agents import resume_agent, jd_agent, skill_gap, interview_agent, roadmap_agent, resume_rewriter, auth_agent, company_agent

app.include_router(company_agent.router, prefix="/api/company", tags=["Company"])
app.include_router(resume_agent.router, prefix="/api/resume", tags=["Resume"])
app.include_router(jd_agent.router, prefix="/api/jd", tags=["JD"])
app.include_router(skill_gap.router, prefix="/api/skillgap", tags=["Skill Gap"])
app.include_router(interview_agent.router, prefix="/api/interview", tags=["Interview"])
app.include_router(roadmap_agent.router, prefix="/api/roadmap", tags=["Roadmap"])
app.include_router(resume_rewriter.router, prefix="/api/rewriter", tags=["Rewriter"])
app.include_router(auth_agent.router, prefix="/api/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Placement Strategist API is running!"}