def compare_skills(resume_skills, jd_skills):
    """
    Compare Resume Skills with JD Skills
    Returns:
    - matched_skills
    - missing_skills
    - match_percentage
    """

    resume_set = {skill.lower(): skill for skill in resume_skills}

    matched_skills = []
    missing_skills = []

    for skill in jd_skills:

        if skill.lower() in resume_set:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(jd_skills) == 0:
        match_percentage = 0
    else:
        match_percentage = (
            len(matched_skills) / len(jd_skills)
        ) * 100

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(match_percentage, 2)
    }