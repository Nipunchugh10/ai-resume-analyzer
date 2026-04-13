"""
PHASE 3: Resume Parsing
Convert PDF → Text using PyMuPDF
"""

import fitz  # PyMuPDF


def extract_text(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """Extract all text from PDF bytes (for uploaded files)."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()
