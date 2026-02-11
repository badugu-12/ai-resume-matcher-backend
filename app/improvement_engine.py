import re

ACTION_VERBS = [
    "built", "developed", "designed", "implemented", "improved",
    "optimized", "deployed", "analyzed", "automated", "led"
]

WEAK_VERBS = [
    "worked", "responsible", "helped", "assisted", "involved"
]

DEPLOYMENT_KEYWORDS = [
    "deployed", "production", "docker", "aws", "azure", "gcp",
    "cloud", "ci/cd", "pipeline"
]


def generate_resume_feedback(resume_text: str, skills: list):
    feedback = []

    text = resume_text.lower()
    words = text.split()
    word_count = len(words)

    # 1️⃣ Action verbs check
    action_verb_count = sum(1 for v in ACTION_VERBS if v in text)

    if action_verb_count < 5:
        feedback.append({
            "title": "Use stronger action verbs",
            "message": (
                "Your resume uses very few impactful action verbs. "
                "Recruiters prefer bullet points that start with strong action verbs."
            ),
            "example": (
                "Developed a machine learning pipeline that reduced prediction error by 22%"
            )
        })

    # 2️⃣ Quantified impact (numbers, %, metrics)
    if not re.search(r"\d+%|\d+\s?(x|times|hrs|hours|users)", text):
        feedback.append({
            "title": "Add measurable impact",
            "message": (
                "Your resume lacks measurable results. ATS systems and recruiters "
                "strongly favor quantified achievements."
            ),
            "example": (
                "Improved SQL query performance by 35% using indexing and query optimization"
            )
        })

    # 3️⃣ Resume length check
    if word_count < 350:
        feedback.append({
            "title": "Expand resume with relevant details",
            "message": (
                "Your resume is slightly short. Adding more project details, tools used, "
                "and outcomes can improve ATS visibility."
            ),
            "example": (
                "Expanded project descriptions to include tools, challenges, and outcomes"
            )
        })

    # 4️⃣ Resume section completeness
    required_sections = ["experience", "projects", "skills"]
    missing_sections = [
        section for section in required_sections if section not in text
    ]

    if missing_sections:
        feedback.append({
            "title": "Add missing resume sections",
            "message": (
                "Your resume is missing important sections that ATS systems expect."
            ),
            "example": (
                f"Add sections such as: {', '.join(missing_sections).title()}"
            )
        })

    # 5️⃣ Skill grouping suggestion
    if len(skills) > 12:
        feedback.append({
            "title": "Group skills for better readability",
            "message": (
                "Your resume lists many skills but lacks clear grouping. "
                "Grouping skills improves ATS parsing and recruiter scanning."
            ),
            "example": (
                "Languages: Python, Java | Frameworks: FastAPI, React | Databases: MongoDB, MySQL"
            )
        })

    # 6️⃣ Weak verb usage
    weak_verb_count = sum(1 for v in WEAK_VERBS if v in text)

    if weak_verb_count > 2:
        feedback.append({
            "title": "Replace weak verbs with strong action verbs",
            "message": (
                "Your resume uses passive language that reduces impact."
            ),
            "example": (
                "Replaced 'Worked on API development' with "
                "'Designed and implemented REST APIs using FastAPI'"
            )
        })

    # 7️⃣ Skills not used in context
    if skills and action_verb_count < 3:
        feedback.append({
            "title": "Show how you used your skills",
            "message": (
                "Your skills are listed but not clearly linked to achievements. "
                "ATS systems prefer skills shown in context."
            ),
            "example": (
                "Built REST APIs using FastAPI and MongoDB serving 5,000+ users"
            )
        })

    # 8️⃣ Deployment / production experience
    if not any(keyword in text for keyword in DEPLOYMENT_KEYWORDS):
        feedback.append({
            "title": "Highlight deployment or production experience",
            "message": (
                "Your resume lacks evidence of real-world deployment or production usage."
            ),
            "example": (
                "Deployed FastAPI application on AWS using Docker and CI/CD pipelines"
            )
        })

    # 9️⃣ Long sentence readability check
    sentences = re.split(r"[.!?]", resume_text)
    long_sentences = [s for s in sentences if len(s.split()) > 30]

    if len(long_sentences) > 2:
        feedback.append({
            "title": "Improve bullet point readability",
            "message": (
                "Some bullet points are too long. Recruiters prefer concise, scannable bullets."
            ),
            "example": (
                "Kept bullet points under 2 lines using Action → Tool → Impact format"
            )
        })

    # 🔟 Fallback (excellent resume)
    if not feedback:
        feedback.append({
            "title": "Strong ATS-optimized resume",
            "message": (
                "Your resume meets ATS standards. To stand out further, "
                "emphasize leadership, ownership, and business impact."
            ),
            "example": (
                "Led a cross-functional team to deploy an ML system used by 10,000+ users"
            )
        })

    return feedback
