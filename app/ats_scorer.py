
import re

ACTION_VERBS = [
    "built", "designed", "developed", "implemented", "optimized",
    "improved", "created", "analyzed", "led", "managed", "deployed"
]

REQUIRED_SECTIONS = [
    "experience", "education", "skills", "projects"
]


def calculate_ats_score(resume_text: str, skills: list[str]):
    text = resume_text.lower()
    words = re.findall(r"\b\w+\b", text)
    word_count = len(words)

    breakdown = {}

    # --------------------
    # 1. Formatting Quality (20)
    # --------------------
    formatting_score = 20 if word_count > 300 else int((word_count / 300) * 20)
    breakdown["formatting"] = min(formatting_score, 20)

    # --------------------
    # 2. Skill Density (30)
    # --------------------
    skill_mentions = sum(text.count(skill.lower()) for skill in skills)
    skills_per_100_words = (skill_mentions / word_count) * 100 if word_count else 0

    if skills_per_100_words >= 5:
        breakdown["skill_density"] = 30
    else:
        breakdown["skill_density"] = int((skills_per_100_words / 5) * 30)

    # --------------------
    # 3. Action Verbs (20)
    # --------------------
    action_count = sum(text.count(v) for v in ACTION_VERBS)

    if action_count >= 10:
        breakdown["action_verbs"] = 20
    else:
        breakdown["action_verbs"] = int((action_count / 10) * 20)

    # --------------------
    # 4. Resume Length (15)
    # Ideal: 450–800 words
    # --------------------
    if 450 <= word_count <= 800:
        breakdown["length"] = 15
    elif 300 <= word_count < 450:
        breakdown["length"] = 10
    else:
        breakdown["length"] = 5

    # --------------------
    # 5. Section Coverage (15)
    # --------------------
    found_sections = sum(1 for sec in REQUIRED_SECTIONS if sec in text)
    breakdown["sections"] = int((found_sections / len(REQUIRED_SECTIONS)) * 15)

    total_score = sum(breakdown.values())

    return {
        "score": total_score,
        "breakdown": breakdown
    }
