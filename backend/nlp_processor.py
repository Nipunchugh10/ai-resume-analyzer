"""
PHASE 4: NLP Processing (CORE AI PART)
- Skill Extraction (keyword matching + spaCy NER)
- Section Detection (regex + keywords)
"""

import re
import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")


# ─── Skills Database ────────────────────────────────────────────────

SKILLS_DB = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C", "C#",
        "Go", "Rust", "Kotlin", "Swift", "R", "Scala", "PHP", "Ruby",
        "Perl", "MATLAB", "Dart", "Lua", "Haskell", "Shell", "Bash",
    ],
    "Machine Learning / AI": [
        "Machine Learning", "Deep Learning", "NLP",
        "Natural Language Processing", "Computer Vision",
        "Reinforcement Learning", "TensorFlow", "PyTorch", "Scikit-learn",
        "Keras", "OpenCV", "BERT", "GPT", "Transformers", "LLM",
        "Neural Networks", "GANs", "YOLO", "Hugging Face", "CUDA",
        "ONNX", "MLflow", "Feature Engineering", "XGBoost", "LightGBM",
        "Random Forest", "SVM", "CNN", "RNN", "LSTM", "Attention",
    ],
    "Data Science": [
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly",
        "Statistics", "A/B Testing", "Data Visualization", "Tableau",
        "Power BI", "Excel", "Data Modeling", "ETL", "Data Cleaning",
        "Regression", "Classification", "Clustering", "EDA",
        "Hypothesis Testing",
    ],
    "Web Development": [
        "React", "Angular", "Vue", "Node.js", "Express", "Django",
        "Flask", "FastAPI", "Spring Boot", "HTML", "CSS", "Tailwind",
        "Bootstrap", "REST API", "GraphQL", "WebSocket", "Next.js",
        "Svelte", "jQuery", "SASS", "Webpack", "Vite",
    ],
    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis",
        "Elasticsearch", "Cassandra", "DynamoDB", "Neo4j", "SQLite",
        "Oracle", "Firebase", "Supabase", "MariaDB",
    ],
    "Cloud / DevOps": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD",
        "Terraform", "Ansible", "Jenkins", "Git", "GitHub Actions",
        "Linux", "Nginx", "Serverless", "Microservices", "Monitoring",
        "Prometheus", "Grafana", "Heroku", "Vercel", "Netlify",
    ],
    "Big Data": [
        "Spark", "Hadoop", "Kafka", "Airflow", "Hive", "Flink",
        "Presto", "Databricks", "Snowflake", "BigQuery", "Redshift",
    ],
    "Soft Skills": [
        "Agile", "Scrum", "Leadership", "Communication", "Teamwork",
        "Problem Solving", "Critical Thinking", "Project Management",
        "Mentoring", "Research", "Testing", "Jira",
    ],
}

ALL_SKILLS = []
for category_skills in SKILLS_DB.values():
    ALL_SKILLS.extend(category_skills)


# ─── 1. Skill Extraction ───────────────────────────────────────────

def extract_skills_keyword(text: str) -> dict:
    """
    Option A (Beginner): Keyword matching against skills database.
    Returns dict of {category: [matched_skills]}.
    """
    found = {}
    text_lower = text.lower()

    for category, skills in SKILLS_DB.items():
        matched = []
        for skill in skills:
            skill_lower = skill.lower()
            # Use word boundary matching for short skills to avoid false positives
            if len(skill) <= 2:
                pattern = rf'\b{re.escape(skill)}\b'
                if re.search(pattern, text):
                    matched.append(skill)
            elif skill_lower in text_lower:
                matched.append(skill)
        if matched:
            found[category] = matched

    return found


def extract_entities_spacy(text: str) -> list:
    """
    Option B (Advanced): Use spaCy NER to extract named entities.
    Returns list of (entity_text, entity_label) tuples.
    """
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
        })
    return entities


def extract_skills(text: str) -> dict:
    """
    Combined skill extraction: keyword matching + spaCy entities.
    """
    # Primary: keyword matching (reliable)
    skills_by_category = extract_skills_keyword(text)

    # Secondary: spaCy NER for additional context
    entities = extract_entities_spacy(text)

    # Extract organization names (potential companies worked at)
    organizations = [e["text"] for e in entities if e["label"] == "ORG"]
    # Extract person names
    persons = [e["text"] for e in entities if e["label"] == "PERSON"]
    # Extract dates
    dates = [e["text"] for e in entities if e["label"] == "DATE"]

    all_skills = []
    for cat_skills in skills_by_category.values():
        all_skills.extend(cat_skills)

    return {
        "skills_by_category": skills_by_category,
        "all_skills": all_skills,
        "total_skills": len(all_skills),
        "entities": {
            "organizations": list(set(organizations))[:10],
            "persons": list(set(persons))[:5],
            "dates": list(set(dates))[:10],
        },
    }


# ─── 2. Section Detection ──────────────────────────────────────────

# --- Heading-level keywords: only match when they appear as a ---
# --- section heading (start of line, standalone, or ALL-CAPS)  ---

SECTION_HEADING_KEYWORDS = {
    "education": [
        "education", "academic background", "academic qualifications",
        "educational qualifications", "academic details",
    ],
    "experience": [
        "experience", "work experience", "professional experience",
        "work history", "employment history", "employment",
        "internship experience", "internships",
    ],
    "projects": [
        "projects", "personal projects", "academic projects",
        "key projects", "selected projects", "project work",
    ],
    "skills": [
        "skills", "technical skills", "core competencies",
        "technologies", "tools & technologies", "tools and technologies",
        "tech stack", "proficiencies", "competencies",
    ],
    "certifications": [
        "certifications", "certificates", "courses",
        "training", "professional development", "credentials",
        "courses & certifications", "licenses & certifications",
    ],
    "achievements": [
        "achievements", "awards", "honors", "accomplishments",
        "awards & achievements", "recognitions",
    ],
}

# --- Body-level evidence: secondary signals found in body text ---
# --- These alone do NOT confirm a section, but support it      ---

SECTION_BODY_EVIDENCE = {
    "education": [
        r'\bb\.?\s*tech\b', r'\bm\.?\s*tech\b', r'\bb\.?\s*sc\b',
        r'\bm\.?\s*sc\b', r'\bb\.?\s*e\b', r'\bm\.?\s*e\b',
        r'\bbachelor\b', r'\bmaster\b', r'\bphd\b', r'\bdiploma\b',
        r'\buniversity\b', r'\bcollege\b', r'\binstitute\b',
        r'\bcgpa\b', r'\bgpa\b',
    ],
    "experience": [
        r'\binternship\b', r'\bintern\b',
        r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*\d{4}\b',
        r'\b\d{4}\s*[-–]\s*(?:\d{4}|present|current)\b',
    ],
    "projects": [
        r'\bgithub\.com/\S+\b', r'\bdeployed\s+(?:on|to|at)\b',
        r'\btech\s*stack\s*:', r'\bbuilt\s+(?:a|an|the|using)\b',
    ],
    "skills": [],
    "certifications": [
        r'\budemy\b', r'\bcoursera\b', r'\bedx\b',
        r'\bgoogle\s*cloud\b', r'\baws\s*certified\b',
        r'\bcertified\b',
    ],
    "achievements": [
        r'\bhackathon\b', r'\bwon\b', r'\brank\b', r'\bprize\b',
        r'\b1st\s*place\b', r'\b2nd\s*place\b', r'\b3rd\s*place\b',
        r'\btop\s*\d+%?\b',
    ],
}


def _is_heading_line(line: str, keyword: str) -> bool:
    """
    Check if a line looks like a section heading containing the keyword.
    Heading criteria:
      - Line is short (≤ 80 chars after stripping)
      - Keyword appears at or near the start of the line
      - Line may be ALL-CAPS, Title Case, or preceded by markers (─, =, *, #)
    """
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return False

    stripped_lower = stripped.lower()
    keyword_lower = keyword.lower()

    # Must actually contain the keyword
    if keyword_lower not in stripped_lower:
        return False

    # Good heading signals
    is_short = len(stripped.split()) <= 8
    is_upper = stripped.isupper()
    is_title = stripped.istitle()
    starts_with_keyword = stripped_lower.startswith(keyword_lower)
    has_marker = bool(re.match(r'^[\s─═•\-\*#=|►▶→]+', stripped))

    # Keyword at start of a short line is strong evidence
    if starts_with_keyword and is_short:
        return True
    # ALL CAPS short line with the keyword
    if is_upper and is_short:
        return True
    # Title case short line
    if is_title and is_short:
        return True
    # Line starts with a marker followed by the keyword
    if has_marker:
        after_marker = re.sub(r'^[\s─═•\-\*#=|►▶→]+', '', stripped).strip().lower()
        if after_marker.startswith(keyword_lower):
            return True

    return False


def detect_sections(text: str) -> dict:
    """
    Detect which sections are present in the resume using
    heading-level detection (primary) + body evidence (secondary).

    A section is marked as detected only if:
      - A heading-like line contains the section keyword, OR
      - Multiple (≥ 2) body-level evidence patterns match
    """
    lines = text.split('\n')
    text_lower = text.lower()
    sections = {}

    for section, heading_keywords in SECTION_HEADING_KEYWORDS.items():
        found_heading = False

        # Primary: check for heading-like lines
        for line in lines:
            for keyword in heading_keywords:
                if _is_heading_line(line, keyword):
                    found_heading = True
                    break
            if found_heading:
                break

        if found_heading:
            sections[section] = True
            continue

        # Secondary: count body-level evidence matches
        body_patterns = SECTION_BODY_EVIDENCE.get(section, [])
        evidence_count = sum(
            1 for p in body_patterns if re.search(p, text_lower)
        )
        # Require at least 2 independent evidence signals
        sections[section] = evidence_count >= 2

    return sections
