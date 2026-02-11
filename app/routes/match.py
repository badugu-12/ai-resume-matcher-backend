from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.security import OAuth2PasswordBearer
import shutil
from datetime import datetime
from app.database import matches_collection
from app.resume_parser import parse_resume
from app.job_parser import parse_job_description
from app.matcher import match_resume_to_job
from app.ats_scorer import calculate_ats_score
from app.improvement_engine import generate_resume_feedback
from app.auth import verify_token
from app.recommender import recommend_jobs
from app.jobs_db import JOBS

router = APIRouter(prefix="", tags=["Match"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

@router.post("/match")
async def match_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    file_path = f"temp_{resume.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    resume_data = parse_resume(file_path)
    job_data = parse_job_description(job_description)

    score = match_resume_to_job(
        resume_data["skills"],
        job_data["required_skills"]
    )

    ats = calculate_ats_score(
        resume_text=resume_data["raw_text"],
        skills=resume_data["skills"]
    )

    feedback = generate_resume_feedback(
        resume_text=resume_data["raw_text"],
        skills=resume_data["skills"]
    )

    resume_skills_set = set(resume_data["skills"])
    job_skills_set = set(job_data["required_skills"])

    matched_skills = list(resume_skills_set & job_skills_set)
    missing_skills = list(job_skills_set - resume_skills_set)

    job_recommendations = recommend_jobs(resume_data["skills"], JOBS)

    match_document = {
        "user_id": current_user,
        "match_percentage": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ats_score": ats,
        "resume_feedback": feedback,
        "job_recommendations": job_recommendations,
        "created_at": datetime.utcnow()
    }

    matches_collection.insert_one(match_document)

    return {
        "match_percentage": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ats_score": ats,
        "resume_feedback": feedback,
        "job_recommendations": job_recommendations
    }
