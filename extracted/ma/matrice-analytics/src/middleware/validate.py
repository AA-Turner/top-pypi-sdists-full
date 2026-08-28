"""Input validation utilities.

For FastAPI, use Pydantic models directly (built-in).
These utilities are for non-FastAPI code or additional validation.
"""
from __future__ import annotations

import html
import re


def sanitize_string(value: str) -> str:
    """HTML-escape a string to prevent XSS."""
    return html.escape(value)


def validate_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_required_fields(data: dict, required: list[str]) -> tuple[bool, list[str]]:
    """Check that all required fields are present and non-empty."""
    missing = [f for f in required if not data.get(f)]
    return len(missing) == 0, missing
