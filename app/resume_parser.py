import pdfplumber
import re

SKILLS_DB = [
    "python", "java", "sql", "machine learning", "deep learning",
    "data science", "react", "javascript", "html", "css",
    "mongodb", "mysql", "fastapi"
]

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text  # ❗ DO NOT lowercase here

def extract_skills(text):
    text_lower = text.lower()
    skills_found = []
    for skill in SKILLS_DB:
        if skill in text_lower:
            skills_found.append(skill)
    return list(set(skills_found))

def extract_experience(text):
    match = re.search(r"(\d+)\+?\s+years", text.lower())
    return int(match.group(1)) if match else 0

def parse_resume(pdf_path):
    full_text = extract_text_from_pdf(pdf_path)

    return {
        "skills": extract_skills(full_text),
        "experience": extract_experience(full_text),
        "raw_text": full_text  # ✅ REQUIRED FOR ATS SCORE
    }
