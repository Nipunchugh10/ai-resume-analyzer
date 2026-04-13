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

SECTION_PATTERNS = {
    "education": [
        r'\beducation\b', r'\bacademic\b', r'\buniversity\b',
        r'\bcollege\b', r'\bdegree\b', r'\bbachelor\b', r'\bmaster\b',
        r'\bphd\b', r'\bb\.?tech\b', r'\bm\.?tech\b', r'\bcgpa\b',
        r'\bgpa\b', r'\bb\.?sc\b', r'\bm\.?sc\b', r'\bb\.?e\b',
        r'\bm\.?e\b', r'\bdiploma\b',
    ],
    "experience": [
        r'\bexperience\b', r'\bwork\s*history\b', r'\bemployment\b',
        r'\binternship\b', r'\bworked\s*at\b', r'\brole\b',
        r'\bposition\b', r'\bjob\b', r'\bcompany\b', r'\bemployer\b',
        r'\bintern\b',
    ],
    "projects": [
        r'\bproject\b', r'\bportfolio\b', r'\bbuilt\b',
        r'\bdeveloped\b', r'\bimplemented\b', r'\bcreated\b',
        r'\bdesigned\b', r'\bapplication\b',
    ],
    "skills": [
        r'\bskill\b', r'\btechnical\b', r'\bproficien\b',
        r'\btechnolog\b', r'\btool\b', r'\bframework\b',
        r'\blanguage\b', r'\bstack\b',
    ],
    "certifications": [
        r'\bcertif\b', r'\bcredential\b', r'\blicensed\b',
        r'\bcourse\b', r'\btraining\b', r'\budemy\b',
        r'\bcoursera\b', r'\bedx\b', r'\bgoogle\s*cloud\b',
        r'\baws\s*certified\b',
    ],
    "achievements": [
        r'\bachieve\b', r'\baward\b', r'\bhonor\b',
        r'\brecognition\b', r'\baccomplish\b', r'\bwon\b',
        r'\bprize\b', r'\brank\b', r'\bhackathon\b',
    ],
}


def detect_sections(text: str) -> dict:
    """Detect which sections are present in the resume."""
    text_lower = text.lower()
    sections = {}

    for section, patterns in SECTION_PATTERNS.items():
        found = False
        for pattern in patterns:
            if re.search(pattern, text_lower):
                found = True
                break
        sections[section] = found

    return sections
