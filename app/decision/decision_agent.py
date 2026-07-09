def make_decision(match_percentage):
    """
    Make hiring decision based on match percentage.
    """

    if match_percentage >= 80:
        return {
            "decision": "SHORTLISTED",
            "confidence": "95%",
            "reason": "Excellent skill match with the job description."
        }

    elif match_percentage >= 60:
        return {
            "decision": "MAYBE",
            "confidence": "75%",
            "reason": "Good skills, but some important skills are missing."
        }

    elif match_percentage >= 40:
        return {
            "decision": "REJECT",
            "confidence": "60%",
            "reason": "Several required skills are missing."
        }

    else:
        return {
            "decision": "REJECT",
            "confidence": "95%",
            "reason": "Candidate does not meet the minimum skill requirements."
        }
    