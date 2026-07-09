import fitz
import re


def extract_pdf_text(file_path):
    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)

    if match:
        return match.group()

    return "Not Found"


def extract_name(file_path):
    pdf = fitz.open(file_path)
    page = pdf[0]

    blocks = page.get_text("dict")["blocks"]

    candidates = []

    ignore_words = [
        "software developer",
        "developer",
        "engineer",
        "profile",
        "education",
        "skills",
        "projects",
        "experience",
        "internship",
        "certification",
        "resume",
        "curriculum vitae",
        "cv"
    ]

    for block in blocks:
        if "lines" not in block:
            continue

        for line in block["lines"]:
            text = ""
            max_size = 0

            for span in line["spans"]:
                text += span["text"] + " "
                if span["size"] > max_size:
                    max_size = span["size"]

            text = text.strip()

            if not text:
                continue

            lower = text.lower()

            if "@" in text:
                continue

            if any(word in lower for word in ignore_words):
                continue

            if sum(c.isdigit() for c in text) > 0:
                continue

            if len(text.split()) > 5:
                continue

            candidates.append((max_size, text))

    pdf.close()

    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1].upper()

    # Fallback: use first meaningful line from raw text
    pdf = fitz.open(file_path)
    raw_lines = pdf[0].get_text().strip().split("\n")
    pdf.close()

    for line in raw_lines[:5]:
        line = line.strip()
        if not line:
            continue
        if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line):
            continue
        lower = line.lower()
        if any(word in lower for word in ignore_words):
            continue
        if len(line.split()) > 5:
            continue
        return line.upper()

    return "Name Not Found"


def _skill_in_text(skill, text_lower):
    if len(skill) <= 3:
        pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'
        return bool(re.search(pattern, text_lower))
    pattern = re.escape(skill.lower()).replace(r'\ ', r'\s+')
    return bool(re.search(pattern, text_lower))


def extract_skills(text):
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


def extract_education(text):
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