import re


def _skill_in_text(skill, text_lower):
    if len(skill) <= 3:
        pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'
        return bool(re.search(pattern, text_lower))
    pattern = re.escape(skill.lower()).replace(r'\ ', r'\s+')
    return bool(re.search(pattern, text_lower))


def extract_jd_skills(text):
    skills_db = [
        "Python",
        "Java",
        "JavaScript",
        "React",
        "Node.js",
        "FastAPI",
        "SQL",
        "MongoDB",
        "Firebase",
        "Git",
        "GitHub",
        "HTML",
        "CSS",
        "Machine Learning",
        "AI",
        "Docker",
        "AWS",
        "Flask",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy",
        "Spring Boot",
        "SpringBoot",
        "MySQL",
        "C++",
        "Figma"
    ]

    found_skills = []
    text_lower = text.lower()

    for skill in skills_db:
        if _skill_in_text(skill, text_lower):
            found_skills.append(skill)

    return found_skills


def extract_experience(text):
    match = re.search(
        r'\d+\s*[-+]\s*\d*\s*Years?|\d+\s*\+\s*Years?|\d+\s+to\s+\d+\s+Years?|\d+\s*Years?',
        text,
        re.IGNORECASE
    )

    if match:
        return match.group()

    return "Not Found"


def _has_edu(variants, normalized, text_lower):
    for v in variants:
        if len(v) <= 3:
            pattern = r'(?<!\w)' + re.escape(v) + r'(?!\w)'
            if '.' in v:
                if re.search(pattern, text_lower):
                    return True
            else:
                if re.search(pattern, normalized):
                    return True
        else:
            if v in normalized or v in text_lower:
                return True
    return False


def extract_qualification(text):
    normalized = text.lower().replace(".", "").replace(",", "")
    text_lower = text.lower()

    def has(variants):
        return _has_edu(variants, normalized, text_lower)

    if has(["phd", "ph.d", "doctor of philosophy", "doctorate"]):
        return "Ph.D"

    if has(["mtech", "m tech", "master of technology"]):
        return "M.Tech"
    if has(["m.e", "m e", "master of engineering"]):
        return "M.E"
    if has(["mba", "master of business administration"]):
        return "MBA"
    if has(["msc", "m sc", "master of science"]):
        return "M.Sc"
    if has(["mca", "master of computer applications"]):
        return "MCA"
    if has(["master", "master's", "masters", "master degree", "post graduate", "postgraduate"]):
        return "Master's Degree"

    if has(["btech", "b tech", "bachelor of technology"]):
        return "B.Tech"
    if has(["b.e", "b e", "bachelor of engineering"]):
        return "B.E"
    if has(["bsc", "b sc", "bachelor of science"]):
        return "B.Sc"
    if has(["bca", "bachelor of computer applications"]):
        return "BCA"
    if has(["bachelor", "bachelor's", "bachelors", "bachelor degree", "graduate", "ug", "undergraduate"]):
        return "Bachelor's Degree"

    if has(["diploma"]):
        return "Diploma"

    return "Not Found"