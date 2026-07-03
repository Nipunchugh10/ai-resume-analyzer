"""
PHASE 5: Resume Scoring System — Strict ATS-Style Rubric
Rule-based scoring with weighted features and diminishing returns.

| Feature       | Max Score |
|-------------- |-----------|
| Skills match  |    40     |
| Experience    |    20     |
| Education     |    15     |
| Projects      |    15     |
| Formatting    |    10     |

Designed to produce realistic score distributions:
  - Average resume: 50–65
  - Good resume:    65–80
  - Excellent:      80–90
  - Perfect:        90–100 (very rare)
"""

import re
import math


def _count_job_entries(text: str) -> int:
    """
    Count approximate number of distinct job/internship entries
    by looking for date-range patterns like "Jan 2023 – Present"
    or "2021 - 2023".
    """
    date_range_patterns = [
        # "Jan 2023 – Present", "June 2022 - Dec 2023"
        r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{4}\s*[-–—]\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{4}|present|current|ongoing)',
        # "2021 - 2023", "2022 – Present"
        r'\b\d{4}\s*[-–—]\s*(?:\d{4}|present|current|ongoing)\b',
    ]
    matches = set()
    for pattern in date_range_patterns:
        for m in re.finditer(pattern, text.lower()):
            # Use start position to deduplicate overlapping matches
            matches.add(m.start())
    return len(matches)


def _count_quantified_metrics(text: str) -> int:
    """
    Count quantified achievements: percentages, dollar amounts,
    user/customer counts, time reductions, etc.
    """
    metric_patterns = [
        r'\d+\s*%',                          # 40%, 25 %
        r'\$\s*[\d,]+(?:\.\d+)?[kKmMbB]?',  # $50K, $1.2M
        r'\d+[kKmM]\+?\s*(?:user|customer|client|visitor|download|request)',
        r'(?:reduced|improved|increased|decreased|saved|cut)\s+.*?\d+',
        r'\d+x\s+(?:faster|slower|more|less|improvement)',
    ]
    count = 0
    for pattern in metric_patterns:
        count += len(re.findall(pattern, text.lower()))
    return count


def _count_action_verbs(text: str) -> int:
    """Count unique strong action verbs used in the resume."""
    action_verbs = [
        "developed", "built", "designed", "implemented", "managed",
        "led", "created", "optimized", "reduced", "increased",
        "deployed", "architected", "maintained", "improved",
        "automated", "delivered", "engineered", "launched",
        "scaled", "refactored", "integrated", "migrated",
        "mentored", "coordinated", "analyzed", "researched",
        "streamlined", "established", "spearheaded", "collaborated",
    ]
    text_lower = text.lower()
    return sum(1 for v in action_verbs if v in text_lower)


def _count_projects(text: str) -> int:
    """
    Estimate number of distinct projects described.
    Look for project-like headers, bullet clusters, or tech-stack mentions
    near project-related keywords.
    """
    project_markers = [
        # Project title patterns: "Project Name — Description" or "• Project Name"
        r'(?:^|\n)\s*(?:•|▪|►|>\s|-\s|\d+[\.\)]\s)[A-Z][A-Za-z\s]+(?:\(|–|—|:|\|)',
        # "Tech Stack:" or "Technologies:" followed by tools
        r'(?:tech\s*stack|technologies?\s*used|built\s+with)\s*[:\-]',
        # GitHub/live links often accompany projects
        r'(?:github\.com|live\s*(?:demo|link|url)|deployed\s*(?:on|at|to))',
    ]
    count = 0
    for pattern in project_markers:
        count += len(re.findall(pattern, text, re.IGNORECASE))

    # Fallback: count lines that look like project headings
    # (short lines followed by description paragraphs)
    if count == 0:
        lines = text.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            # A short line (2-8 words) that looks like a title
            words_in_line = stripped.split()
            if 2 <= len(words_in_line) <= 8 and stripped[0:1].isupper():
                # Check if next non-empty line is longer (description)
                for j in range(i + 1, min(i + 3, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and len(next_line.split()) > 8:
                        count += 1
                        break

    return min(count, 6)  # Cap at 6


def _extract_gpa_value(text: str) -> float | None:
    """Try to extract a GPA numeric value."""
    # Match patterns like "GPA: 3.8/4.0", "CGPA: 8.5/10", "GPA - 3.5"
    gpa_match = re.search(
        r'(?:cgpa|gpa|grade\s*point)\s*[:\-–]?\s*(\d+\.?\d*)\s*/?\s*(\d+\.?\d*)?',
        text.lower()
    )
    if gpa_match:
        value = float(gpa_match.group(1))
        scale = float(gpa_match.group(2)) if gpa_match.group(2) else None
        if scale:
            # Normalize to 4.0 scale
            return (value / scale) * 4.0
        elif value <= 4.0:
            return value
        elif value <= 10.0:
            return (value / 10.0) * 4.0
    return None


def score_resume(text: str, skills_data: dict, sections: dict) -> dict:
    """
    Score a resume out of 100 based on detected content.
    Uses strict ATS-style rubric with diminishing returns.
    Returns total score and detailed breakdown.
    """
    breakdown = {}
    total = 0
    text_lower = text.lower()

    # ── 1. Skills Match (max 40) ──────────────────────────────────
    #    Diminishing returns: first skills worth more, later ones less
    num_skills = skills_data["total_skills"]
    skills_by_cat = skills_data.get("skills_by_category", {})

    # Tiered skill point calculation
    skill_points = 0.0
    if num_skills > 0:
        # First 5 skills: 2 pts each
        tier1 = min(num_skills, 5)
        skill_points += tier1 * 2.0
        # Skills 6-10: 1.5 pts each
        tier2 = min(max(num_skills - 5, 0), 5)
        skill_points += tier2 * 1.5
        # Skills 11-15: 1 pt each
        tier3 = min(max(num_skills - 10, 0), 5)
        skill_points += tier3 * 1.0
        # Skills 16+: 0.5 pts each
        tier4 = max(num_skills - 15, 0)
        skill_points += tier4 * 0.5

    skill_points = min(30.0, skill_points)  # Cap base at 30

    # Category diversity bonus: +2 per category with ≥2 skills, max +10
    diverse_categories = sum(
        1 for cat_skills in skills_by_cat.values()
        if len(cat_skills) >= 2
    )
    category_bonus = min(10, diverse_categories * 2)

    skill_score = min(40, int(skill_points + category_bonus))

    breakdown["skills_match"] = {
        "score": skill_score,
        "max": 40,
        "detail": f"{num_skills} skills found across {len(skills_by_cat)} categories"
                  + (f" ({diverse_categories} with depth)" if diverse_categories > 0 else ""),
    }
    total += skill_score

    # ── 2. Experience (max 20) ────────────────────────────────────
    #    Requires actual depth, not just section existence
    exp_score = 0

    if sections.get("experience"):
        exp_score = 4  # Base: section header detected

        # Count job/internship entries via date ranges
        job_count = _count_job_entries(text)
        exp_score += min(6, job_count * 3)  # +3 per entry, max +6

        # Quantified metrics
        metric_count = _count_quantified_metrics(text)
        exp_score += min(4, metric_count * 2)  # +2 per metric, max +4

        # Action verbs diversity
        verb_count = _count_action_verbs(text)
        exp_score += min(3, verb_count)  # +1 per verb, max +3

        # Duration/timeline presence
        has_timeline = bool(re.search(
            r'\b\d{4}\b.*\b(?:\d{4}|present|current)\b', text_lower
        ))
        if has_timeline:
            exp_score += 3

    exp_score = min(20, exp_score)
    # Build detail message
    if exp_score == 0:
        exp_detail = "No experience section detected"
    elif exp_score <= 7:
        exp_detail = "Experience section found but lacks depth"
    elif exp_score <= 13:
        exp_detail = "Experience section with some detail"
    elif exp_score <= 17:
        exp_detail = "Strong experience with metrics and action verbs"
    else:
        exp_detail = "Excellent experience — detailed, quantified, well-structured"

    breakdown["experience"] = {
        "score": exp_score,
        "max": 20,
        "detail": exp_detail,
    }
    total += exp_score

    # ── 3. Education (max 15) ─────────────────────────────────────
    #    Multi-factor: header + degree + institution + year + GPA + coursework
    edu_score = 0

    if sections.get("education"):
        edu_score = 3  # Base: section heading detected

        # Degree mentioned
        has_degree = bool(re.search(
            r'\b(?:b\.?\s*tech|m\.?\s*tech|b\.?\s*sc|m\.?\s*sc|b\.?\s*e|m\.?\s*e|'
            r'bachelor|master|phd|doctorate|diploma|associate|b\.?\s*a|m\.?\s*a|'
            r'b\.?\s*com|m\.?\s*com|mba|bba)\b',
            text_lower
        ))
        if has_degree:
            edu_score += 3

        # Institution name (look for "University", "Institute", "College")
        has_institution = bool(re.search(
            r'\b(?:university|institute|college|school|academy)\b', text_lower
        ))
        if has_institution:
            edu_score += 2

        # Graduation year
        has_grad_year = bool(re.search(
            r'\b(?:20[0-3]\d|19[89]\d)\b', text
        ))
        if has_grad_year:
            edu_score += 2

        # GPA/CGPA mentioned
        has_gpa = bool(re.search(
            r'(?:cgpa|gpa|percentage)\s*[:\-–]?\s*\d', text_lower
        ))
        if has_gpa:
            edu_score += 2

            # GPA quality bonus/penalty
            gpa_normalized = _extract_gpa_value(text)
            if gpa_normalized is not None:
                if gpa_normalized >= 3.5:   # ~8.75/10
                    edu_score += 1
                elif gpa_normalized < 2.4:  # ~6.0/10
                    edu_score -= 1

        # Relevant coursework
        has_coursework = bool(re.search(
            r'\b(?:coursework|relevant\s*courses|courses?\s*taken)\b', text_lower
        ))
        if has_coursework:
            edu_score += 2

    edu_score = max(0, min(15, edu_score))

    if edu_score == 0:
        edu_detail = "No education section detected"
    elif edu_score <= 5:
        edu_detail = "Education mentioned but missing details"
    elif edu_score <= 9:
        edu_detail = "Education section with basic information"
    elif edu_score <= 12:
        edu_detail = "Good education section with degree and GPA"
    else:
        edu_detail = "Comprehensive education section"

    breakdown["education"] = {
        "score": edu_score,
        "max": 15,
        "detail": edu_detail,
    }
    total += edu_score

    # ── 4. Projects (max 15) ──────────────────────────────────────
    #    Count and evaluate project quality
    proj_score = 0

    if sections.get("projects"):
        proj_score = 2  # Base: section heading detected

        # Count actual projects
        project_count = _count_projects(text)
        proj_score += min(9, project_count * 3)  # +3 per project, max +9

        # Tech stack mentioned in project context
        has_project_tech = bool(re.search(
            r'(?:tech\s*(?:stack|nolog)|built\s*(?:with|using)|'
            r'tools?\s*used|stack\s*[:\-])',
            text_lower
        ))
        if has_project_tech:
            proj_score += 2

        # Outcomes/results described in projects
        has_outcomes = bool(re.search(
            r'(?:result|outcome|impact|achieved|deployed|launched|'
            r'served\s+\d|users?\s+\d|\d+\s*%)',
            text_lower
        ))
        if has_outcomes:
            proj_score += 2

    proj_score = min(15, proj_score)

    if proj_score == 0:
        proj_detail = "No projects section detected"
    elif proj_score <= 4:
        proj_detail = "Projects section found but minimal detail"
    elif proj_score <= 8:
        proj_detail = "Some projects described"
    elif proj_score <= 12:
        proj_detail = "Good projects with tech details"
    else:
        proj_detail = "Strong projects section with outcomes"

    breakdown["projects"] = {
        "score": proj_score,
        "max": 15,
        "detail": proj_detail,
    }
    total += proj_score

    # ── 5. Formatting & Professionalism (max 10) ─────────────────
    words = len(text.split())
    fmt_score = 0

    # Word count — penalize both too short AND too long
    if words < 150:
        fmt_score = 0
    elif words < 300:
        fmt_score = 1
    elif words < 450:
        fmt_score = 2
    elif words < 600:
        fmt_score = 3
    elif words <= 800:
        fmt_score = 4  # Ideal range
    else:
        fmt_score = 3  # Slightly too long

    # Contact info
    has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text))
    has_phone = bool(re.search(r'[\+]?[\d\s\-\(\)]{10,}', text))
    if has_email:
        fmt_score += 2
    if has_phone:
        fmt_score += 1

    # Professional links
    has_linkedin = bool(re.search(r'linkedin', text_lower))
    has_github = bool(re.search(r'github', text_lower))
    has_portfolio = bool(re.search(r'(?:portfolio|personal\s*(?:site|website))', text_lower))
    if has_linkedin or has_github or has_portfolio:
        fmt_score += 1

    # Professional summary/objective
    has_summary = bool(re.search(
        r'\b(?:summary|objective|about\s*me|profile|professional\s*summary)\b',
        text_lower
    ))
    # Also detect summary-like opening paragraphs (first ~200 chars)
    first_chunk = text[:200].lower()
    has_summary_style = bool(re.search(
        r'(?:seeking|passionate|experienced|proficient|dedicated|motivated|'
        r'results.driven|detail.oriented)',
        first_chunk
    ))
    if has_summary or has_summary_style:
        fmt_score += 1

    fmt_score = min(10, fmt_score)

    breakdown["formatting"] = {
        "score": fmt_score,
        "max": 10,
        "detail": f"{words} words"
                  + (", email found" if has_email else ", no email")
                  + (", phone found" if has_phone else ", no phone")
                  + (", has links" if (has_linkedin or has_github) else ""),
    }
    total += fmt_score

    # ── Final ─────────────────────────────────────────────────────
    total = min(100, total)

    # Grade assignment — stricter thresholds
    if total >= 90:
        grade = "A+"
        verdict = "Outstanding resume — top-tier candidate"
    elif total >= 85:
        grade = "A"
        verdict = "Excellent resume"
    elif total >= 78:
        grade = "B+"
        verdict = "Very good resume"
    elif total >= 70:
        grade = "B"
        verdict = "Good resume with room for improvement"
    elif total >= 63:
        grade = "B-"
        verdict = "Decent resume — several areas to improve"
    elif total >= 55:
        grade = "C+"
        verdict = "Average resume — needs noticeable improvements"
    elif total >= 45:
        grade = "C"
        verdict = "Below average — significant gaps present"
    elif total >= 30:
        grade = "D"
        verdict = "Weak resume — major sections missing or underdeveloped"
    else:
        grade = "F"
        verdict = "Resume needs a complete overhaul"

    return {
        "total": total,
        "grade": grade,
        "verdict": verdict,
        "breakdown": breakdown,
    }
