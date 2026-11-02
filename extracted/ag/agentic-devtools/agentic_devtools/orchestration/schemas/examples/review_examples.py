"""Example factories for review domain models.

Provides factory functions that return new, realistic instances of review models.
"""

from __future__ import annotations

from typing import Any

from ..review.decision import ReviewDecision
from ..review.finding import CodeSuggestion, FileReviewFinding
from ..review.result import FileReviewResult
from ..review.summary import ReviewSummary


def make_code_suggestion(**kwargs: Any) -> CodeSuggestion:
    """Create a realistic CodeSuggestion instance."""
    defaults: dict[str, Any] = {
        "file_path": "src/services/auth_service.py",
        "start_line": 42,
        "end_line": 45,
        "original_code": "if user is None:\n    return None",
        "replacement_code": ("if user is None:\n    raise AuthenticationError('User not found')"),
        "explanation": (
            "Returning None silently hides authentication failures; "
            "raising an explicit error provides better debugging context."
        ),
    }
    defaults.update(kwargs)
    return CodeSuggestion(**defaults)


def make_file_review_finding(**kwargs: Any) -> FileReviewFinding:
    """Create a realistic FileReviewFinding instance."""
    defaults: dict[str, Any] = {
        "severity": "high",
        "diff_side": "new",
        "new_line": 42,
        "confidence": 0.85,
        "description": "Null return value masks authentication failures and makes debugging difficult.",
    }
    defaults.update(kwargs)
    return FileReviewFinding(**defaults)


def make_file_review_result(**kwargs: Any) -> FileReviewResult:
    """Create a realistic FileReviewResult instance."""
    defaults: dict[str, Any] = {
        "file_path": "src/services/auth_service.py",
        "status": "needs-work",
        "summary": "Authentication error handling needs improvement; 2 findings identified.",
        "findings": [make_file_review_finding()],
    }
    defaults.update(kwargs)
    return FileReviewResult(**defaults)


def make_review_decision(**kwargs: Any) -> ReviewDecision:
    """Create a realistic ReviewDecision instance."""
    defaults: dict[str, Any] = {
        "verdict": "request_changes",
        "confidence": 0.85,
        "rationale": "Two high-severity findings in authentication handling require attention before merge.",
        "blocking_findings_count": 2,
    }
    defaults.update(kwargs)
    return ReviewDecision(**defaults)


def make_review_summary(**kwargs: Any) -> ReviewSummary:
    """Create a realistic ReviewSummary instance."""
    defaults: dict[str, Any] = {
        "decision": make_review_decision(),
        "file_results": [make_file_review_result()],
        "total_findings": 3,
        "critical_findings": 0,
        "files_reviewed": 5,
    }
    defaults.update(kwargs)
    return ReviewSummary(**defaults)
