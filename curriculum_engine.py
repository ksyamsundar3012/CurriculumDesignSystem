from ollama_client import query_granite
import random

def generate_curriculum(skill, level, semesters, weekly_hours, industry_focus):
    prompt = f"""
    Generate a detailed {level} {skill} curriculum for {semesters} semesters with {weekly_hours} weekly hours.
    Focus industry: {industry_focus}.
    Output JSON with semesters, courses, credits, and 5-7 topics for each.
    """

    try:
        result = query_granite(prompt)
        # Basic fallback structure if AI fails
        if not result or "courses" not in str(result):
            curriculum = _fallback_curriculum(skill, level, semesters)
            return {"program_name": f"{skill} {level} Curriculum", "curriculum": curriculum}
        return result
    except Exception:
        curriculum = _fallback_curriculum(skill, level, semesters)
        return {"program_name": f"{skill} {level} Curriculum", "curriculum": curriculum}


def _fallback_curriculum(skill, level, semesters):
    example_topics = [
        "Introduction",
        "Mathematical Foundations",
        "Practical Labs",
        "Project Work",
        "Case Studies"
    ]

    curriculum = []
    for s in range(1, semesters + 1):
        sem_courses = []
        for c in range(3):
            sem_courses.append({
                "name": f"{skill} Course {c+1} - Semester {s}",
                "credits": 4,
                "topics": random.sample(example_topics, 5)
            })
        curriculum.append({"semester": s, "courses": sem_courses})
    return curriculum
