import re
from sentence_transformers import util
from Backend.embeddings import model


# ---------------- Common Technical Skills ---------------- #

COMMON_SKILLS = [
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
    "HTML", "CSS", "React", "Angular", "Vue",
    "Spring Boot", "Spring", "Node.js", "Express",
    "Flask", "FastAPI", "Django",

    "MySQL", "PostgreSQL", "MongoDB", "Redis",

    "Docker", "Kubernetes", "Git", "GitHub",
    "CI/CD", "Jenkins",

    "AWS", "Azure", "GCP",

    "REST API", "RESTful APIs",
    "Microservices",

    "TensorFlow", "PyTorch", "Scikit-learn",
    "Pandas", "NumPy",

    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Computer Vision",

    "Linux",

    "Kafka",

    "FAISS",

    "LangChain",

    "SQL"
]


# ---------------- Extract Skills ---------------- #

def extract_skills(text):

    found = []

    text = text.lower()

    for skill in COMMON_SKILLS:

        if skill.lower() in text:
            found.append(skill)

    return sorted(list(set(found)))


# ---------------- Match Resume ---------------- #

def calculate_match(resume_text, job_description):

    # Semantic Similarity

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    jd_embedding = model.encode(
        job_description,
        convert_to_tensor=True
    )

    semantic_score = util.cos_sim(
        resume_embedding,
        jd_embedding
    ).item()

    semantic_score = semantic_score * 100


    # Skill Matching

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    matched = [
        skill for skill in jd_skills
        if skill in resume_skills
    ]

    missing = [
        skill for skill in jd_skills
        if skill not in resume_skills
    ]

    if len(jd_skills):

        skill_score = (
            len(matched) /
            len(jd_skills)
        ) * 100

    else:

        skill_score = 100


    # Final Score

    final_score = (
        semantic_score * 0.6 +
        skill_score * 0.4
    )

    return {

        "score": round(final_score, 2),

        "matched": matched,

        "missing": missing,

        "semantic": round(semantic_score, 2),

        "skill_score": round(skill_score, 2)
    }