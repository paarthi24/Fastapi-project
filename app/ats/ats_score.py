def calculate_ats_score(match_percentage):

    if match_percentage >= 90:
        score = 95

    elif match_percentage >= 80:
        score = 85

    elif match_percentage >= 70:
        score = 75

    elif match_percentage >= 60:
        score = 65

    else:
        score = 50

    return score