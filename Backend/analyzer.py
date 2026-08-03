import re


def analyze_resume(text):

    skills = [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "SQL",
        "Spring Boot",
        "Spring Security",
        "FastAPI",
        "Flask",
        "React",
        "Docker",
        "Kubernetes",
        "Git",
        "Redis",
        "PostgreSQL",
        "MySQL",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch"
    ]

    detected_skills = []

    lower_text = text.lower()

    for skill in skills:

        if skill.lower() in lower_text:
            detected_skills.append(skill)

    projects = len(re.findall(r"PROJECT", text, re.IGNORECASE))

    experience = len(re.findall(r"EXPERIENCE", text, re.IGNORECASE))

    education = len(re.findall(r"EDUCATION", text, re.IGNORECASE))

    certificates = len(
        re.findall(
            r"CERTIFICATION|CERTIFICATIONS|CERTIFICATE",
            text,
            re.IGNORECASE,
        )
    )

    return {
        "Skills": len(detected_skills),
        "Projects": projects,
        "Experience": experience,
        "Education": education,
        "Certificates": certificates,
        "Detected Skills": detected_skills,
    }