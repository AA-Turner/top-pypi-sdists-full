"""Tests for FileReviewOutput Pydantic model."""

import pytest
from pydantic import ValidationError

from agentic_devtools.orchestration.review.state import FileReviewOutput


class TestFileReviewOutput:
    """Tests for FileReviewOutput Pydantic model validation."""

    def test_approve_outcome(self) -> None:
        """Valid approve outcome with empty suggestions."""
        output = FileReviewOutput(outcome="approve", summary="LGTM")
        assert output.outcome == "approve"
        assert output.summary == "LGTM"
        assert output.suggestions == []

    def test_request_changes_with_suggestions(self) -> None:
        """Valid request-changes with suggestions."""
        output = FileReviewOutput(
            outcome="request-changes",
            summary="Issues found",
            suggestions=[
                {  # type: ignore[list-item]
                    "severity": "high",
                    "content": "Missing null check",
                    "line": 42,
                }
            ],
        )
        assert output.outcome == "request-changes"
        assert len(output.suggestions) == 1
        assert output.suggestions[0].severity == "high"

    def test_request_changes_with_suggestion_and_replacement(self) -> None:
        """Valid request-changes-with-suggestion including replacement_code."""
        output = FileReviewOutput(
            outcome="request-changes-with-suggestion",
            summary="Code fix needed",
            suggestions=[
                {  # type: ignore[list-item]
                    "severity": "medium",
                    "content": "Use f-string",
                    "replacement_code": 'f"hello {name}"',
                    "line": 10,
                    "endLine": 12,
                }
            ],
        )
        assert output.suggestions[0].replacement_code == 'f"hello {name}"'
        assert output.suggestions[0].endLine == 12

    def test_invalid_outcome_rejected(self) -> None:
        """Invalid outcome value is rejected."""
        with pytest.raises(ValidationError):
            FileReviewOutput(outcome="invalid", summary="bad")  # type: ignore[arg-type]

    def test_invalid_severity_rejected(self) -> None:
        """Invalid severity value is rejected."""
        with pytest.raises(ValidationError):
            FileReviewOutput(
                outcome="approve",
                summary="ok",
                suggestions=[{"severity": "critical", "content": "bug"}],  # type: ignore[list-item]
            )

    def test_model_dump_roundtrip(self) -> None:
        """model_dump() output can reconstruct the model."""
        original = FileReviewOutput(
            outcome="approve",
            summary="Clean code",
            suggestions=[],
        )
        data = original.model_dump()
        reconstructed = FileReviewOutput(**data)
        assert reconstructed == original

    def test_request_changes_with_suggestion_requires_replacement_code(self) -> None:
        """request-changes-with-suggestion needs a non-empty replacement_code."""
        with pytest.raises(ValidationError):
            FileReviewOutput(
                outcome="request-changes-with-suggestion",
                summary="Code fix needed",
                suggestions=[
                    {  # type: ignore[list-item]
                        "severity": "medium",
                        "content": "Use f-string",
                        "line": 10,
                    }
                ],
            )

    def test_request_changes_with_suggestion_requires_at_least_one_suggestion(self) -> None:
        """request-changes-with-suggestion requires at least one suggestion."""
        with pytest.raises(ValidationError):
            FileReviewOutput(
                outcome="request-changes-with-suggestion",
                summary="Code fix needed",
                suggestions=[],
            )
