import re

# reuse / keep consistent with resume skills
SKILLS_DB = [
    "python", "java", "sql", "machine learning", "deep learning",
    "data science", "react", "javascript", "html", "css",
    "mongodb", "mysql", "fastapi"
]

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_required_skills(text: str):
    text = clean_text(text)
    skills_found = [s for s in SKILLS_DB if s in text]
    return list(set(skills_found))

def parse_job_description(jd_text: str):
    return {
        "required_skills": extract_required_skills(jd_text)
    }
