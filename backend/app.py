"""
PHASE 8: Flask Backend API

Endpoints:
  POST /upload_resume   — Upload PDF, parse, and run full analysis
  GET  /score           — Get resume score (after upload)
  GET  /job_matches     — Get matched jobs (after upload)
  GET  /suggestions     — Get improvement suggestions (after upload)
"""

import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from resume_parser import extract_text, extract_text_from_bytes
from nlp_processor import extract_skills, detect_sections
from scoring_engine import score_resume
from job_matcher import match_jobs
from suggestion_engine import generate_suggestions

# ─── App Setup ────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max
ALLOWED_EXTENSIONS = {"pdf"}

# In-memory store for the latest analysis (single-user demo)
analysis_store = {}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── POST /upload_resume ──────────────────────────────────────────

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    """
    Upload a PDF resume and run the full analysis pipeline.
    Returns complete analysis: text, skills, score, jobs, suggestions.
    """
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded. Send a PDF with key 'resume'."}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are accepted."}), 400

    try:
        # ── Phase 3: Resume Parsing ───────────────────────────────
        pdf_bytes = file.read()
        resume_text = extract_text_from_bytes(pdf_bytes)

        if not resume_text.strip():
            return jsonify({
                "error": "Could not extract text from this PDF. "
                         "It may be scanned/image-based. "
                         "Please upload a text-based PDF."
            }), 422

        # ── Phase 4: NLP Processing ───────────────────────────────
        skills_data = extract_skills(resume_text)
        sections = detect_sections(resume_text)

        # ── Phase 5: Scoring ──────────────────────────────────────
        score_data = score_resume(resume_text, skills_data, sections)

        # ── Phase 6: Job Matching ─────────────────────────────────
        job_matches = match_jobs(resume_text, skills_data, top_n=5)

        # ── Phase 7: Suggestions ──────────────────────────────────
        suggestions = generate_suggestions(
            resume_text, skills_data, sections, score_data
        )

        # ── Store results ─────────────────────────────────────────
        result = {
            "filename": secure_filename(file.filename),
            "text_preview": resume_text[:500] + ("..." if len(resume_text) > 500 else ""),
            "word_count": len(resume_text.split()),
            "skills": skills_data,
            "sections_detected": sections,
            "score": score_data,
            "job_matches": job_matches,
            "suggestions": suggestions,
        }

        analysis_store["latest"] = result

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


# ─── GET /score ───────────────────────────────────────────────────

@app.route("/score", methods=["GET"])
def get_score():
    """Return the resume score from the latest analysis."""
    if "latest" not in analysis_store:
        return jsonify({"error": "No resume analyzed yet. Upload one first."}), 404
    return jsonify(analysis_store["latest"]["score"]), 200


# ─── GET /job_matches ─────────────────────────────────────────────

@app.route("/job_matches", methods=["GET"])
def get_job_matches():
    """Return job matches from the latest analysis."""
    if "latest" not in analysis_store:
        return jsonify({"error": "No resume analyzed yet. Upload one first."}), 404
    return jsonify(analysis_store["latest"]["job_matches"]), 200


# ─── GET /suggestions ─────────────────────────────────────────────

@app.route("/suggestions", methods=["GET"])
def get_suggestions():
    """Return improvement suggestions from the latest analysis."""
    if "latest" not in analysis_store:
        return jsonify({"error": "No resume analyzed yet. Upload one first."}), 404
    return jsonify(analysis_store["latest"]["suggestions"]), 200


# ─── Health Check ─────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "app": "AI Resume Analyzer + Job Matcher",
        "endpoints": [
            "POST /upload_resume",
            "GET /score",
            "GET /job_matches",
            "GET /suggestions",
        ],
    })


# ─── Run ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
