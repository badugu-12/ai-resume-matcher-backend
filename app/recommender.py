
def recommend_jobs(resume_skills, jobs, top_n=5):
    results = []

    resume_set = set(resume_skills)

    for job in jobs:
        job_set = set(job["skills"])
        matched = resume_set & job_set
        score = int((len(matched) / len(job_set)) * 100)

        results.append({
            "job_title": job["title"],
            "match_percentage": score,
            "matched_skills": list(matched),
            "missing_skills": list(job_set - resume_set)
        })

    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return results[:top_n]
