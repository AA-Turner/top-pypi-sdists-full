"""
Resume Parser

Extract structured information from PDF resumes using NLP and pattern matching
"""

__version__ = "0.1.0"
__author__ = "Rahul Bagai"

from .resume_parser import (
    ensure_spacy_model,
    extract_text_from_pdf,
    clean_text,
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_role,
    extract_name,
    extract_location,
    extract_summary,
    is_job_header_line,
    extract_achievements,
    extract_awards_and_honors,
    parse_resume,
)

__all__ = [
    "ensure_spacy_model",
    "extract_text_from_pdf",
    "clean_text",
    "extract_email",
    "extract_phone",
    "extract_linkedin",
    "extract_role",
    "extract_name",
    "extract_location",
    "extract_summary",
    "is_job_header_line",
    "extract_achievements",
    "extract_awards_and_honors",
    "parse_resume",
]
