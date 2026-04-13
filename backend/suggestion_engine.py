"""
PHASE 7: Suggestion Engine
Generate actionable improvement tips based on resume analysis.
"""

import re


def generate_suggestions(
    text: str,
    skills_data: dict,
    sections: dict,
    score_data: dict,
) -> list:
    """
    Generate personalized improvement suggestions.
    Each suggestion has: type (critical/important/nice/positive), text, category.
    """
    suggestions = []
    all_skills = skills_data.get("all_skills", [])
    all_skills_lower = [s.lower() for s in all_skills]
    total_score = score_data.get("total", 0)
    words = len(text.split())

    # ── Critical Issues ───────────────────────────────────────────

    if len(all_skills) < 3:
        suggestions.append({
            "type": "critical",
            "category": "Skills",
            "text": "Very few technical skills detected. Add a dedicated "
                    "'Technical Skills' section listing your languages, "
                    "frameworks, tools, and platforms explicitly.",
        })

    if not sections.get("experience"):
        suggestions.append({
            "type": "critical",
            "category": "Experience",
            "text": "No work experience section detected. Include "
                    "internships, freelance projects, part-time roles, or "
                    "open-source contributions — any hands-on work counts.",
        })

    if not sections.get("education"):
        suggestions.append({
            "type": "critical",
            "category": "Education",
            "text": "Education section is missing or not recognized. Add "
                    "your degree, institution, graduation year, and GPA/CGPA.",
        })

    if words < 100:
        suggestions.append({
            "type": "critical",
            "category": "Content",
            "text": "Your resume is extremely short. A competitive resume "
                    "typically has 400–700 words with detailed descriptions "
                    "of your responsibilities and achievements.",
        })

    # ── Important Improvements ────────────────────────────────────

    if not sections.get("projects"):
        suggestions.append({
            "type": "important",
            "category": "Projects",
            "text": "No projects section found. Add 2–3 significant projects "
                    "with: project name, tech stack used, your specific role, "
                    "and a measurable outcome or result.",
        })

    if not re.search(r'\d+\s*(%|percent)', text.lower()):
        suggestions.append({
            "type": "important",
            "category": "Impact",
            "text": "Add quantifiable metrics to your achievements. "
                    "Use numbers: 'Reduced load time by 40%', 'Served 10K+ "
                    "users', 'Improved model accuracy from 78% to 93%'.",
        })

    action_verbs = [
        "developed", "built", "designed", "implemented", "managed",
        "led", "created", "optimized", "reduced", "increased",
        "deployed", "architected", "automated", "delivered",
    ]
    verb_count = sum(1 for v in action_verbs if v in text.lower())
    if verb_count < 3:
        suggestions.append({
            "type": "important",
            "category": "Language",
            "text": "Use strong action verbs to describe your work: "
                    "'Developed', 'Architected', 'Optimized', 'Deployed', "
                    "'Automated' — these make your contributions stand out.",
        })

    if 100 <= words < 300:
        suggestions.append({
            "type": "important",
            "category": "Content",
            "text": "Resume is on the shorter side. Expand your experience "
                    "and project descriptions with specific details about "
                    "what you built, which technologies you used, and the "
                    "results you achieved.",
        })

    has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text))
    has_phone = bool(re.search(r'[\+]?[\d\s\-\(\)]{10,}', text))
    has_linkedin = bool(re.search(r'linkedin', text.lower()))
    has_github = bool(re.search(r'github', text.lower()))

    if not has_email or not has_phone:
        suggestions.append({
            "type": "important",
            "category": "Contact",
            "text": "Make sure your resume includes both email and phone "
                    "number at the top. Recruiters need to reach you easily.",
        })

    if not has_linkedin and not has_github:
        suggestions.append({
            "type": "important",
            "category": "Links",
            "text": "Add links to your LinkedIn profile and GitHub account. "
                    "These let recruiters see your professional presence and "
                    "code contributions.",
        })

    # ── Nice-to-Have Suggestions ──────────────────────────────────

    if not sections.get("certifications"):
        suggestions.append({
            "type": "nice",
            "category": "Certifications",
            "text": "Consider adding relevant certifications: AWS Certified, "
                    "Google Cloud Professional, Coursera/Udemy specializations "
                    "— they validate your skills formally.",
        })

    if not sections.get("achievements"):
        suggestions.append({
            "type": "nice",
            "category": "Achievements",
            "text": "An achievements section can set you apart. Include "
                    "hackathon wins, academic ranks, competition placements, "
                    "or any recognitions you have received.",
        })

    skills_by_cat = skills_data.get("skills_by_category", {})

    if "Cloud / DevOps" not in skills_by_cat:
        suggestions.append({
            "type": "nice",
            "category": "Skills Gap",
            "text": "Cloud and DevOps skills (Docker, AWS, CI/CD, Git) are "
                    "increasingly expected across roles. Add them if you "
                    "have any experience.",
        })

    if "Databases" not in skills_by_cat:
        suggestions.append({
            "type": "nice",
            "category": "Skills Gap",
            "text": "No database skills detected. Most roles require some "
                    "SQL or NoSQL knowledge — mention any database experience.",
        })

    # ── Positive Feedback ─────────────────────────────────────────

    if total_score >= 80:
        suggestions.append({
            "type": "positive",
            "category": "Overall",
            "text": "Excellent resume! Strong across all major categories. "
                    "Focus on tailoring it for specific job applications "
                    "to maximize your match rate.",
        })
    elif total_score >= 60:
        suggestions.append({
            "type": "positive",
            "category": "Overall",
            "text": "Good foundation. Address the suggestions above to push "
                    "your resume from good to great — small improvements "
                    "can make a big difference.",
        })

    if len(all_skills) >= 10:
        suggestions.append({
            "type": "positive",
            "category": "Skills",
            "text": f"Strong technical profile with {len(all_skills)} skills "
                    f"detected across {len(skills_by_cat)} categories.",
        })

    return suggestions
