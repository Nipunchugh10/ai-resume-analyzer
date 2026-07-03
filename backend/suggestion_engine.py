"""
PHASE 7: Suggestion Engine
Generate actionable improvement tips based on resume analysis.
Aligned with the strict ATS-style scoring rubric.
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
    skills_by_cat = skills_data.get("skills_by_category", {})
    total_score = score_data.get("total", 0)
    breakdown = score_data.get("breakdown", {})
    words = len(text.split())
    text_lower = text.lower()

    # ── Critical Issues ───────────────────────────────────────────

    if len(all_skills) < 5:
        suggestions.append({
            "type": "critical",
            "category": "Skills",
            "text": "Very few technical skills detected (only "
                    f"{len(all_skills)}). Add a dedicated 'Technical Skills' "
                    "section listing your languages, frameworks, tools, and "
                    "platforms explicitly. Most competitive resumes list "
                    "15–25 relevant skills.",
        })

    if not sections.get("experience"):
        suggestions.append({
            "type": "critical",
            "category": "Experience",
            "text": "No work experience section detected. Include "
                    "internships, freelance projects, part-time roles, or "
                    "open-source contributions — any hands-on work counts. "
                    "Use a clear heading like 'EXPERIENCE' or "
                    "'WORK EXPERIENCE'.",
        })

    if not sections.get("education"):
        suggestions.append({
            "type": "critical",
            "category": "Education",
            "text": "Education section is missing or not recognized. Add "
                    "your degree, institution, graduation year, and GPA/CGPA "
                    "under a clear 'EDUCATION' heading.",
        })

    if words < 150:
        suggestions.append({
            "type": "critical",
            "category": "Content",
            "text": "Your resume is extremely short "
                    f"({words} words). A competitive resume typically has "
                    "450–700 words with detailed descriptions of your "
                    "responsibilities, projects, and achievements.",
        })

    # ── Scoring-based Suggestions ─────────────────────────────────

    # Skills depth
    skills_score = breakdown.get("skills_match", {}).get("score", 0)
    skills_max = breakdown.get("skills_match", {}).get("max", 40)
    if 5 <= len(all_skills) < 12:
        suggestions.append({
            "type": "important",
            "category": "Skills",
            "text": f"You have {len(all_skills)} skills listed "
                    f"(scoring {skills_score}/{skills_max}). "
                    "Expand to 15+ relevant skills. Include specific tools "
                    "and frameworks, not just general categories.",
        })

    # Category diversity
    diverse_cats = sum(1 for v in skills_by_cat.values() if len(v) >= 2)
    if diverse_cats < 3 and len(all_skills) >= 5:
        suggestions.append({
            "type": "important",
            "category": "Skills Diversity",
            "text": f"Skills are concentrated in only {diverse_cats} "
                    "categories with depth. Diversify across areas like "
                    "Programming, Databases, Cloud/DevOps, and Tools to show "
                    "a well-rounded technical profile.",
        })

    # Experience depth
    exp_score = breakdown.get("experience", {}).get("score", 0)
    if sections.get("experience") and exp_score <= 10:
        if not re.search(r'\d+\s*(%|percent)', text_lower):
            suggestions.append({
                "type": "important",
                "category": "Impact Metrics",
                "text": "Your experience section lacks quantified achievements. "
                        "Add numbers: 'Reduced load time by 40%', 'Served 10K+ "
                        "users', 'Improved model accuracy from 78% to 93%'. "
                        "ATS systems and recruiters value measurable impact.",
            })

        action_verbs = [
            "developed", "built", "designed", "implemented", "managed",
            "led", "created", "optimized", "reduced", "increased",
            "deployed", "architected", "automated", "delivered",
        ]
        verb_count = sum(1 for v in action_verbs if v in text_lower)
        if verb_count < 3:
            suggestions.append({
                "type": "important",
                "category": "Action Language",
                "text": "Use stronger action verbs to describe your work: "
                        "'Developed', 'Architected', 'Optimized', 'Deployed', "
                        "'Automated', 'Spearheaded' — these make your "
                        "contributions stand out to ATS and recruiters.",
            })

    # Experience entries
    if sections.get("experience") and exp_score <= 7:
        suggestions.append({
            "type": "important",
            "category": "Experience Detail",
            "text": "Your experience section needs more structure. Include "
                    "date ranges (e.g., 'Jan 2023 – Present'), role titles, "
                    "company names, and 2–4 bullet points per role describing "
                    "your specific contributions.",
        })

    # Education quality
    edu_score = breakdown.get("education", {}).get("score", 0)
    if sections.get("education") and edu_score <= 8:
        missing_items = []
        if not re.search(r'\b(?:b\.?\s*tech|bachelor|master|phd|diploma|mba)\b', text_lower):
            missing_items.append("degree type")
        if not re.search(r'\b(?:university|institute|college)\b', text_lower):
            missing_items.append("institution name")
        if not re.search(r'\b20[0-3]\d\b', text):
            missing_items.append("graduation year")
        if not re.search(r'(?:cgpa|gpa)\s*[:\-]?\s*\d', text_lower):
            missing_items.append("GPA/CGPA")

        if missing_items:
            suggestions.append({
                "type": "important",
                "category": "Education",
                "text": "Your education section is missing: "
                        + ", ".join(missing_items) + ". "
                        "Include all of these for a complete education entry.",
            })

    # Projects
    if not sections.get("projects"):
        suggestions.append({
            "type": "important",
            "category": "Projects",
            "text": "No projects section found. Add 2–3 significant projects "
                    "with: project name, tech stack used, your specific role, "
                    "and a measurable outcome or result. Use a clear "
                    "'PROJECTS' heading.",
        })
    else:
        proj_score = breakdown.get("projects", {}).get("score", 0)
        if proj_score <= 6:
            suggestions.append({
                "type": "important",
                "category": "Projects",
                "text": "Your projects section needs more depth. For each "
                        "project, include the tech stack, your specific "
                        "contribution, and a tangible result or outcome "
                        "(e.g., 'Deployed on AWS, serving 500+ daily users').",
            })

    # Content length
    if 150 <= words < 400:
        suggestions.append({
            "type": "important",
            "category": "Content Length",
            "text": f"Resume is short ({words} words). Expand to 450–700 "
                    "words by adding details to your experience, projects, "
                    "and skills sections. Explain what you did, how you "
                    "did it, and what the result was.",
        })
    elif words > 900:
        suggestions.append({
            "type": "important",
            "category": "Content Length",
            "text": f"Resume is quite long ({words} words). Consider "
                    "trimming to 500–800 words. Focus on the most relevant "
                    "and recent experiences. ATS systems and recruiters "
                    "prefer concise, impactful content.",
        })

    # Contact info
    has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text))
    has_phone = bool(re.search(r'[\+]?[\d\s\-\(\)]{10,}', text))
    has_linkedin = bool(re.search(r'linkedin', text_lower))
    has_github = bool(re.search(r'github', text_lower))

    if not has_email or not has_phone:
        suggestions.append({
            "type": "important",
            "category": "Contact Info",
            "text": "Make sure your resume includes both email and phone "
                    "number at the top. Recruiters need to reach you easily.",
        })

    if not has_linkedin and not has_github:
        suggestions.append({
            "type": "important",
            "category": "Professional Links",
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

    # Professional summary check
    has_summary = bool(re.search(
        r'\b(?:summary|objective|about\s*me|profile)\b', text_lower
    ))
    first_chunk = text[:200].lower()
    has_summary_style = bool(re.search(
        r'(?:seeking|passionate|experienced|proficient|dedicated|motivated)',
        first_chunk
    ))
    if not has_summary and not has_summary_style:
        suggestions.append({
            "type": "nice",
            "category": "Summary",
            "text": "Add a 2–3 line professional summary at the top of your "
                    "resume. Highlight your key strengths, years of "
                    "experience, and career goals concisely.",
        })

    # Relevant coursework
    if not re.search(r'\b(?:coursework|relevant\s*courses)\b', text_lower):
        suggestions.append({
            "type": "nice",
            "category": "Education",
            "text": "Consider listing relevant coursework under your "
                    "education — especially if you're a recent graduate. "
                    "This helps ATS match you with role requirements.",
        })

    # ── Positive Feedback ─────────────────────────────────────────

    if total_score >= 85:
        suggestions.append({
            "type": "positive",
            "category": "Overall",
            "text": "Excellent resume! Strong across all major categories. "
                    "Focus on tailoring it for specific job applications "
                    "to maximize your match rate.",
        })
    elif total_score >= 65:
        suggestions.append({
            "type": "positive",
            "category": "Overall",
            "text": "Good foundation. Address the suggestions above to push "
                    "your resume from good to great — small improvements "
                    "can make a big difference.",
        })
    elif total_score >= 45:
        suggestions.append({
            "type": "positive",
            "category": "Overall",
            "text": "You have a starting base to work with. Addressing the "
                    "critical and important suggestions above will "
                    "significantly boost your score and competitiveness.",
        })

    if len(all_skills) >= 15:
        suggestions.append({
            "type": "positive",
            "category": "Skills",
            "text": f"Strong technical profile with {len(all_skills)} skills "
                    f"detected across {len(skills_by_cat)} categories. "
                    "Well diversified!",
        })
    elif len(all_skills) >= 10:
        suggestions.append({
            "type": "positive",
            "category": "Skills",
            "text": f"Good skill set with {len(all_skills)} skills detected. "
                    "Consider adding a few more in areas you have experience.",
        })

    exp_score = breakdown.get("experience", {}).get("score", 0)
    if exp_score >= 16:
        suggestions.append({
            "type": "positive",
            "category": "Experience",
            "text": "Your experience section is well-detailed with metrics "
                    "and action verbs. This is exactly what ATS systems and "
                    "recruiters look for.",
        })

    return suggestions
