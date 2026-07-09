def generate_feedback(gap_analysis):
    """
    Generate improvement suggestions based on missing skills.
    """

    feedback = []

    suggestions = {
        "Python": "Improve Python programming by solving coding problems on LeetCode or HackerRank.",
        "FastAPI": "Build REST APIs using FastAPI and understand request-response handling.",
        "SQL": "Practice SQL queries including JOIN, GROUP BY, and database normalization.",
        "Machine Learning": "Learn supervised and unsupervised machine learning algorithms using scikit-learn.",
        "AI": "Strengthen AI fundamentals including NLP, Computer Vision, and Generative AI.",
        "Docker": "Learn Docker basics, images, containers, and Docker Compose.",
        "AWS": "Complete the AWS Cloud Practitioner certification course.",
        "Git": "Practice Git branching, merging, and GitHub collaboration.",
        "GitHub": "Learn repository management, pull requests, and version control workflows.",
        "MongoDB": "Practice CRUD operations and aggregation in MongoDB.",
        "Firebase": "Learn Authentication, Firestore Database, and Firebase Hosting.",
        "React": "Build React projects using Hooks, Components, and Routing.",
        "JavaScript": "Practice ES6 concepts, DOM manipulation, and asynchronous programming.",
        "HTML": "Improve semantic HTML and responsive layouts.",
        "CSS": "Practice Flexbox, Grid, animations, and responsive design.",
        "Spring Boot": "Learn Spring Boot for building production-grade Java applications.",
        "SpringBoot": "Learn Spring Boot for building production-grade Java applications.",
        "MySQL": "Practice SQL queries, indexing, and database design with MySQL.",
        "C++": "Strengthen C++ programming with object-oriented concepts and STL.",
        "Figma": "Learn Figma for UI/UX design, prototyping, and collaboration."
    }

    for item in gap_analysis:
        skill = item["skill"]

        if skill in suggestions:
            feedback.append({
                "skill": skill,
                "suggestion": suggestions[skill]
            })
        else:
            feedback.append({
                "skill": skill,
                "suggestion": f"Learn and practice {skill} through projects and online courses."
            })

    return feedback