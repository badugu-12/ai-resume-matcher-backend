from app.matcher import match_resume_to_job

resume_skills = ["python", "sql", "machine learning", "mongodb"]
job_skills = ["python", "sql", "machine learning", "fastapi"]

print("Match %:", match_resume_to_job(resume_skills, job_skills))
