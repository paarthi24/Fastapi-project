def analyze_gaps(missing_skills):
    """
    Analyze missing skills and assign priority.
    """

    result = []

    high_priority = [
        "Python",
        "FastAPI",
        "SQL",
        "Machine Learning",
        "AI",
        "Docker",
        "AWS"
    ]

    medium_priority = [
        "Git",
        "GitHub",
        "MongoDB",
        "Firebase",
        "HTML",
        "CSS",
        "React",
        "JavaScript",
        "Spring Boot",
        "SpringBoot",
        "MySQL",
        "C++",
        "Figma"
    ]

    for skill in missing_skills:

        if skill in high_priority:
            priority = "HIGH"

        elif skill in medium_priority:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        result.append({
            "skill": skill,
            "priority": priority
        })

    return result