from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import shutil
import os
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


# ✅ FIXED TOKEN VALIDATION
def get_current_user(token: str = Depends(oauth2_scheme)):
    email = verify_token(token)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return email


@router.post("/match")
async def match_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: str = Depends(get_current_user)
):
    try:
        # 🔹 Save uploaded file temporarily
        file_path = f"temp_{resume.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        # 🔹 Parse resume & job
        resume_data = parse_resume(file_path)
        job_data = parse_job_description(job_description)

        # 🔹 Match score
        score = match_resume_to_job(
            resume_data["skills"],
            job_data["required_skills"]
        )

        # 🔹 ATS score
        ats = calculate_ats_score(
            resume_text=resume_data["raw_text"],
            skills=resume_data["skills"]
        )

        # 🔹 Feedback
        feedback = generate_resume_feedback(
            resume_text=resume_data["raw_text"],
            skills=resume_data["skills"]
        )

        # 🔹 Skill comparison
        resume_skills_set = set(resume_data["skills"])
        job_skills_set = set(job_data["required_skills"])

        matched_skills = list(resume_skills_set & job_skills_set)
        missing_skills = list(job_skills_set - resume_skills_set)

        # 🔹 Job recommendations
        job_recommendations = recommend_jobs(resume_data["skills"], JOBS)

        # 🔹 Save to MongoDB
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

        # 🔹 Delete temp file
        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "match_percentage": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "ats_score": ats,
            "resume_feedback": feedback,
            "job_recommendations": job_recommendations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Match failed: {str(e)}"
        )
