"""
PHASE 5: Resume Scoring System
Rule-based scoring with weighted features.

| Feature      | Max Score |
|------------- |-----------|
| Skills match |    40     |
| Experience   |    20     |
| Education    |    15     |
| Projects     |    15     |
| Formatting   |    10     |
"""

import re


def score_resume(text: str, skills_data: dict, sections: dict) -> dict:
    """
    Score a resume out of 100 based on detected content.
    Returns total score and detailed breakdown.
    """
    breakdown = {}
    total = 0

    # ── 1. Skills Match (max 40) ──────────────────────────────────
    num_skills = skills_data["total_skills"]
    skill_score = min(40, num_skills * 3)

    # Bonus for diversity across categories
    num_categories = len(skills_data["skills_by_category"])
    if num_categories >= 4:
        skill_score = min(40, skill_score + 5)

    breakdown["skills_match"] = {
        "score": skill_score,
        "max": 40,
        "detail": f"{num_skills} skills found across {num_categories} categories",
    }
    total += skill_score

    # ── 2. Experience (max 20) ────────────────────────────────────
    exp_score = 0
    if sections.get("experience"):
        exp_score = 12
        # Bonus: look for quantifiable achievements
        if re.search(r'\d+\s*(%|percent|years?|months?)', text.lower()):
            exp_score += 4
        # Bonus: action verbs
        action_verbs = [
            "developed", "built", "designed", "implemented", "managed",
            "led", "created", "optimized", "reduced", "increased",
            "deployed", "architected", "maintained", "improved",
        ]
        verb_count = sum(1 for v in action_verbs if v in text.lower())
        if verb_count >= 3:
            exp_score += 4

    exp_score = min(20, exp_score)
    breakdown["experience"] = {
        "score": exp_score,
        "max": 20,
        "detail": "Experience section found with details" if exp_score > 12
                  else "Experience section found" if exp_score > 0
                  else "No experience section detected",
    }
    total += exp_score

    # ── 3. Education (max 15) ─────────────────────────────────────
    edu_score = 0
    if sections.get("education"):
        edu_score = 10
        # Bonus for GPA mention
        if re.search(r'(cgpa|gpa|percentage)\s*[:\-]?\s*\d', text.lower()):
            edu_score += 5

    edu_score = min(15, edu_score)
    breakdown["education"] = {
        "score": edu_score,
        "max": 15,
        "detail": "Education section with GPA found" if edu_score > 10
                  else "Education section found" if edu_score > 0
                  else "No education section detected",
    }
    total += edu_score

    # ── 4. Projects (max 15) ──────────────────────────────────────
    proj_score = 0
    if sections.get("projects"):
        proj_score = 10
        # Count approximate number of projects (heuristic)
        proj_markers = len(re.findall(
            r'(?:project\s*[:\-]|•\s*\w|─\s*\w|\d+\.\s*\w)',
            text.lower()
        ))
        if proj_markers >= 2:
            proj_score += 5

    proj_score = min(15, proj_score)
    breakdown["projects"] = {
        "score": proj_score,
        "max": 15,
        "detail": "Multiple projects detected" if proj_score > 10
                  else "Projects section found" if proj_score > 0
                  else "No projects section detected",
    }
    total += proj_score

    # ── 5. Formatting & Length (max 10) ───────────────────────────
    words = len(text.split())
    fmt_score = 0

    if words >= 400:
        fmt_score = 6
    elif words >= 200:
        fmt_score = 4
    elif words >= 100:
        fmt_score = 2
    else:
        fmt_score = 1

    # Bonus for contact info
    has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text))
    has_phone = bool(re.search(r'[\+]?[\d\s\-\(\)]{10,}', text))
    if has_email:
        fmt_score += 2
    if has_phone:
        fmt_score += 2

    fmt_score = min(10, fmt_score)
    breakdown["formatting"] = {
        "score": fmt_score,
        "max": 10,
        "detail": f"{words} words, {'email found' if has_email else 'no email'}, "
                  f"{'phone found' if has_phone else 'no phone'}",
    }
    total += fmt_score

    # ── Final ─────────────────────────────────────────────────────
    total = min(100, total)

    # Grade assignment
    if total >= 85:
        grade = "A"
        verdict = "Excellent resume"
    elif total >= 70:
        grade = "B"
        verdict = "Good resume with room for improvement"
    elif total >= 50:
        grade = "C"
        verdict = "Average resume — needs significant improvements"
    elif total >= 30:
        grade = "D"
        verdict = "Below average — major sections missing"
    else:
        grade = "F"
        verdict = "Resume needs a complete overhaul"

    return {
        "total": total,
        "grade": grade,
        "verdict": verdict,
        "breakdown": breakdown,
    }
