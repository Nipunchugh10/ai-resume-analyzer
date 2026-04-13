"""
PHASE 6: Job Matching Engine
Approach 1: TF-IDF + Cosine Similarity
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ─── Sample Job Descriptions Dataset ────────────────────────────────

JOB_DATABASE = [
    {
        "id": 1,
        "title": "Machine Learning Engineer",
        "company": "TechCorp AI",
        "location": "Bangalore, India",
        "skills_required": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "NLP", "Docker", "AWS"],
        "description": "Design, build, and deploy production machine learning models. Work with large-scale datasets, train deep learning models using TensorFlow and PyTorch, and implement NLP pipelines. Strong Python skills and experience with cloud deployment required.",
    },
    {
        "id": 2,
        "title": "Full Stack Developer",
        "company": "WebScale Inc",
        "location": "Remote",
        "skills_required": ["JavaScript", "React", "Node.js", "TypeScript", "MongoDB", "REST API", "Git", "Docker"],
        "description": "Build and maintain full stack web applications using React frontend and Node.js backend. Design RESTful APIs, work with MongoDB databases, and deploy using Docker. TypeScript proficiency preferred.",
    },
    {
        "id": 3,
        "title": "Data Scientist",
        "company": "DataDriven Analytics",
        "location": "Hyderabad, India",
        "skills_required": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "Scikit-learn", "Tableau", "A/B Testing"],
        "description": "Analyze large datasets to extract actionable insights. Build predictive models using scikit-learn, perform statistical analysis, create dashboards in Tableau, and run A/B tests to drive data-informed decisions.",
    },
    {
        "id": 4,
        "title": "Backend Engineer",
        "company": "CloudFirst Systems",
        "location": "Pune, India",
        "skills_required": ["Python", "Django", "Flask", "PostgreSQL", "Redis", "Docker", "Kubernetes", "REST API"],
        "description": "Design and implement scalable backend services using Python with Django and Flask frameworks. Manage PostgreSQL databases, implement caching with Redis, containerize with Docker, and orchestrate with Kubernetes.",
    },
    {
        "id": 5,
        "title": "Frontend Developer",
        "company": "PixelPerfect UI",
        "location": "Mumbai, India",
        "skills_required": ["JavaScript", "React", "TypeScript", "CSS", "HTML", "Tailwind", "Next.js", "Git"],
        "description": "Create responsive, performant user interfaces using React and TypeScript. Style with Tailwind CSS, build server-rendered pages with Next.js, and ensure cross-browser compatibility with pixel-perfect designs.",
    },
    {
        "id": 6,
        "title": "DevOps Engineer",
        "company": "InfraScale",
        "location": "Noida, India",
        "skills_required": ["Docker", "Kubernetes", "AWS", "CI/CD", "Terraform", "Linux", "Python", "Jenkins"],
        "description": "Build and manage CI/CD pipelines, automate infrastructure provisioning with Terraform, deploy on AWS using Docker and Kubernetes, and maintain Linux-based production environments.",
    },
    {
        "id": 7,
        "title": "AI Research Intern",
        "company": "DeepTech Labs",
        "location": "Bangalore, India",
        "skills_required": ["Python", "PyTorch", "Deep Learning", "NLP", "Transformers", "Research", "Mathematics"],
        "description": "Conduct cutting-edge AI research in natural language processing and deep learning. Implement transformer architectures in PyTorch, write research papers, and contribute to open-source AI projects.",
    },
    {
        "id": 8,
        "title": "Data Engineer",
        "company": "BigData Solutions",
        "location": "Gurgaon, India",
        "skills_required": ["Python", "SQL", "Spark", "Airflow", "Kafka", "AWS", "ETL", "Hadoop"],
        "description": "Design and build robust data pipelines using Apache Spark and Airflow. Process streaming data with Kafka, manage ETL workflows, and optimize data warehousing on AWS infrastructure.",
    },
    {
        "id": 9,
        "title": "Mobile App Developer",
        "company": "AppNova",
        "location": "Chennai, India",
        "skills_required": ["Kotlin", "Swift", "React Native", "Flutter", "REST API", "Firebase", "Git"],
        "description": "Develop cross-platform mobile applications using React Native or Flutter. Build native features in Kotlin and Swift, integrate REST APIs, and manage backend with Firebase.",
    },
    {
        "id": 10,
        "title": "Cloud Solutions Architect",
        "company": "SkyCompute",
        "location": "Remote",
        "skills_required": ["AWS", "Azure", "GCP", "Terraform", "Kubernetes", "Docker", "Microservices", "Serverless"],
        "description": "Design enterprise cloud architectures across AWS, Azure, and GCP. Implement infrastructure as code with Terraform, design microservices patterns, and optimize serverless deployments.",
    },
    {
        "id": 11,
        "title": "NLP Engineer",
        "company": "LangTech AI",
        "location": "Bangalore, India",
        "skills_required": ["Python", "NLP", "Transformers", "BERT", "PyTorch", "Hugging Face", "Deep Learning", "LLM"],
        "description": "Build and fine-tune large language models using Hugging Face Transformers. Develop NLP solutions including text classification, named entity recognition, and question answering systems using BERT and GPT architectures.",
    },
    {
        "id": 12,
        "title": "Cybersecurity Analyst",
        "company": "SecureNet",
        "location": "Delhi, India",
        "skills_required": ["Linux", "Python", "Networking", "Penetration Testing", "OWASP", "Cryptography"],
        "description": "Monitor and protect systems from security threats. Perform penetration testing, implement security protocols, analyze vulnerabilities using OWASP guidelines, and develop security automation scripts in Python.",
    },
    {
        "id": 13,
        "title": "Computer Vision Engineer",
        "company": "VisionAI Corp",
        "location": "Hyderabad, India",
        "skills_required": ["Python", "OpenCV", "Computer Vision", "Deep Learning", "CNN", "TensorFlow", "YOLO"],
        "description": "Develop computer vision solutions for object detection, image segmentation, and video analysis. Implement CNN architectures, use YOLO for real-time detection, and deploy models with TensorFlow Serving.",
    },
    {
        "id": 14,
        "title": "Software Development Engineer",
        "company": "CodeCraft Technologies",
        "location": "Pune, India",
        "skills_required": ["Java", "Spring Boot", "SQL", "Git", "Docker", "Agile", "REST API", "Testing"],
        "description": "Build enterprise software solutions using Java and Spring Boot. Design and implement RESTful microservices, write unit and integration tests, follow Agile methodologies, and deploy with Docker.",
    },
    {
        "id": 15,
        "title": "Business Intelligence Analyst",
        "company": "InsightPro",
        "location": "Mumbai, India",
        "skills_required": ["SQL", "Tableau", "Power BI", "Excel", "Python", "Statistics", "Data Visualization"],
        "description": "Create business intelligence dashboards and reports using Tableau and Power BI. Write complex SQL queries for data extraction, perform statistical analysis, and present data-driven recommendations to stakeholders.",
    },
]


def match_jobs(resume_text: str, skills_data: dict, top_n: int = 5) -> list:
    """
    Match resume against job descriptions using TF-IDF + Cosine Similarity.
    Returns top N matching jobs with similarity scores.
    """
    # Build combined text for each job (description + skills)
    job_texts = []
    for job in JOB_DATABASE:
        combined = job["description"] + " " + " ".join(job["skills_required"])
        job_texts.append(combined)

    # Documents: [resume, job1, job2, ...]
    documents = [resume_text] + job_texts

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2),
    )
    vectors = vectorizer.fit_transform(documents)

    # Cosine Similarity: resume (index 0) vs all jobs (index 1+)
    similarity = cosine_similarity(vectors[0:1], vectors[1:])
    similarity_scores = similarity[0]

    # Build results
    results = []
    all_user_skills = [s.lower() for s in skills_data.get("all_skills", [])]

    for i, job in enumerate(JOB_DATABASE):
        job_skills_lower = [s.lower() for s in job["skills_required"]]
        matched_skills = [s for s in job["skills_required"]
                          if s.lower() in all_user_skills]
        missing_skills = [s for s in job["skills_required"]
                          if s.lower() not in all_user_skills]

        results.append({
            "id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "similarity": round(float(similarity_scores[i]) * 100, 1),
            "skills_required": job["skills_required"],
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_percent": round(
                len(matched_skills) / len(job["skills_required"]) * 100
            ) if job["skills_required"] else 0,
            "description": job["description"],
        })

    # Sort by similarity (descending)
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results[:top_n]
