"""Tests for ReviewVerdict Pydantic model."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from agentic_devtools.orchestration.schemas.review.verdict import ReviewVerdict


class TestReviewVerdict:
    """Tests for ReviewVerdict schema validation."""

    def test_approve_verdict(self) -> None:
        """Approve verdict constructs correctly."""
        verdict = ReviewVerdict(outcome="approve", summary="Looks good")
        assert verdict.outcome == "approve"
        assert verdict.summary == "Looks good"
        assert verdict.suggestions == []

    def test_request_changes_verdict(self) -> None:
        """Request-changes verdict with summary."""
        verdict = ReviewVerdict(outcome="request-changes", summary="Fix the bug")
        assert verdict.outcome == "request-changes"

    def test_request_changes_with_suggestion(self) -> None:
        """Verdict with valid suggestions list."""
        verdict = ReviewVerdict(
            outcome="request-changes-with-suggestion",
            summary="Add type hint",
            suggestions=[{"line": 1, "content": "Add return type", "replacement_code": "-> str"}],  # type: ignore[list-item]
        )
        assert verdict.outcome == "request-changes-with-suggestion"
        assert len(verdict.suggestions) == 1
        assert verdict.suggestions[0].line == 1

    def test_suggestions_allow_non_string_values(self) -> None:
        """Suggestions accept typed fields like integer line anchors and booleans."""
        verdict = ReviewVerdict(
            outcome="request-changes-with-suggestion",
            summary="Fix line anchor",
            suggestions=[
                {  # type: ignore[list-item]
                    "line": 42,
                    "endLine": 45,
                    "out_of_scope": False,
                    "content": "Add missing type hint",
                }
            ],
        )
        assert verdict.suggestions[0].line == 42
        assert verdict.suggestions[0].endLine == 45
        assert verdict.suggestions[0].out_of_scope is False

    def test_suggestion_missing_line_raises(self) -> None:
        """Suggestions without 'line' and out_of_scope=False raise ValidationError."""
        with pytest.raises(ValidationError, match="line.*required"):
            ReviewVerdict(
                outcome="request-changes-with-suggestion",
                summary="Bad suggestion",
                suggestions=[{"content": "no line field"}],  # type: ignore[list-item]
            )

    def test_out_of_scope_suggestion_without_line_is_valid(self) -> None:
        """out_of_scope=True suggestions without line are valid in a verdict."""
        verdict = ReviewVerdict(
            outcome="request-changes-with-suggestion",
            summary="Architectural note",
            suggestions=[{"out_of_scope": True, "content": "Consider refactoring"}],  # type: ignore[list-item]
        )
        assert verdict.suggestions[0].out_of_scope is True
        assert verdict.suggestions[0].line is None

    def test_invalid_outcome_raises(self) -> None:
        """Invalid outcome value raises ValidationError."""
        with pytest.raises(ValidationError):
            ReviewVerdict(outcome="invalid-outcome", summary="test")  # type: ignore[arg-type]

    def test_defaults(self) -> None:
        """Default summary and suggestions."""
        verdict = ReviewVerdict(outcome="approve")
        assert verdict.summary == ""
        assert verdict.suggestions == []

    def test_json_roundtrip(self) -> None:
        """JSON serialization and deserialization."""
        verdict = ReviewVerdict(
            outcome="request-changes",
            summary="Fix it",
            suggestions=[{"line": 10, "content": "do this"}],  # type: ignore[list-item]
        )
        json_str = verdict.model_dump_json()
        loaded = ReviewVerdict.model_validate_json(json_str)
        assert loaded.outcome == "request-changes"
        assert loaded.suggestions[0].line == 10
        assert loaded.suggestions[0].content == "do this"
