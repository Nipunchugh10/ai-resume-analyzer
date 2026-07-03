# AI Resume Analyzer + Job Matcher

A full-stack AI-powered application that analyzes resumes, extracts skills using NLP, scores them, matches against job descriptions using TF-IDF, and provides actionable improvement suggestions.

## Architecture

```
Resume (PDF)
   |
   v
Text Extraction (PyMuPDF)
   |
   v
NLP Processing (spaCy + keyword matching)
   |
   v
Scoring Engine (rule-based, 5 categories)
   |
   v
Job Matching (TF-IDF + Cosine Similarity)
   |
   v
Suggestion Engine
   |
   v
React Dashboard
```

## Tech Stack

**Backend:** Python, Flask, PyMuPDF, spaCy, scikit-learn  
**Frontend:** React, Axios, CSS  
**NLP:** spaCy (en_core_web_sm), TF-IDF Vectorizer  
**Matching:** Cosine Similarity (sklearn)

---

## Setup Instructions

### Quick Start (Windows PowerShell)

You can run both the backend and frontend with a single command from the project root:

```powershell
.\run.ps1
```

*(Note: If your PowerShell has script execution restrictions, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` or launch with `powershell -ExecutionPolicy Bypass -File .\run.ps1`)*

This script automatically verifies pre-requisites, performs setup (virtual environments, npm installs, and models) if missing, starts both the backend and frontend servers, and safely stops the backend when you exit with `Ctrl+C`.

---

### Manual Setup

### 1. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run server
python app.py
```

Backend runs at **http://localhost:5000**

### 2. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm start
```

Frontend runs at **http://localhost:3000**

---

## API Endpoints

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| POST   | /upload_resume    | Upload PDF and run full analysis   |
| GET    | /score            | Get resume score                   |
| GET    | /job_matches      | Get matched jobs                   |
| GET    | /suggestions      | Get improvement suggestions        |

---

## Project Structure

```
resume-analyzer/
├── backend/
│   ├── app.py                 # Flask API (Phase 8)
│   ├── resume_parser.py       # PDF → Text (Phase 3)
│   ├── nlp_processor.py       # Skill extraction + sections (Phase 4)
│   ├── scoring_engine.py      # Resume scoring (Phase 5)
│   ├── job_matcher.py         # TF-IDF matching (Phase 6)
│   ├── suggestion_engine.py   # Improvement tips (Phase 7)
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js             # Main app (Phase 9)
│   │   ├── App.css            # LinkedIn-inspired theme
│   │   ├── index.js
│   │   └── components/
│   │       ├── ScoreCard.js
│   │       ├── SkillsPanel.js
│   │       ├── JobMatches.js
│   │       ├── Suggestions.js
│   │       └── SectionsDetected.js
│   └── package.json
└── README.md
```

---

## Deployment (Phase 11)

### Backend → Render

1. Push `backend/` to GitHub
2. Create a new Web Service on render.com
3. Set build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. Set start command: `python app.py`

### Frontend → Vercel

1. Push `frontend/` to GitHub
2. Import on vercel.com
3. Set environment variable: `REACT_APP_API_URL=https://your-backend.onrender.com`
4. Deploy

---

## Features

- Resume upload (PDF)
- AI-based skill extraction (100+ skills across 8 categories)
- spaCy NER for entity extraction (organizations, dates)
- Resume score out of 100 with 5-category breakdown
- Job recommendations via TF-IDF + Cosine Similarity (15 jobs)
- Personalized improvement suggestions (critical/important/nice/positive)
- Clean LinkedIn-inspired dashboard UI
- Fully separated backend and frontend
