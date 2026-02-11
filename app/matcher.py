from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_to_job(resume_skills, job_skills):
    # join skills as text
    resume_text = " ".join(resume_skills)
    job_text = " ".join(job_skills)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)
