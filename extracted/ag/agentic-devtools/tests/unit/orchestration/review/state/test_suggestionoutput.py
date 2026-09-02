"""Tests for SuggestionOutput Pydantic model."""

import pytest
from pydantic import ValidationError

from agentic_devtools.orchestration.review.state import SuggestionOutput


class TestSuggestionOutput:
    """Tests for SuggestionOutput Pydantic model validation."""

    def test_minimal_suggestion(self) -> None:
        """Minimal valid suggestion with required fields only."""
        s = SuggestionOutput(severity="high", content="Fix this bug", line=7)
        assert s.severity == "high"
        assert s.content == "Fix this bug"
        assert s.replacement_code is None
        assert s.line == 7
        assert s.endLine is None
        assert s.out_of_scope is False

    def test_full_suggestion(self) -> None:
        """Suggestion with all optional fields."""
        s = SuggestionOutput(
            severity="medium",
            content="Refactor this",
            replacement_code="new_code()",
            line=10,
            endLine=15,
            out_of_scope=True,
        )
        assert s.replacement_code == "new_code()"
        assert s.line == 10
        assert s.endLine == 15
        assert s.out_of_scope is True

    def test_invalid_severity(self) -> None:
        """Invalid severity value is rejected."""
        with pytest.raises(ValidationError):
            SuggestionOutput(severity="critical", content="bad", line=1)  # type: ignore[arg-type]

    def test_low_severity(self) -> None:
        """Low severity is valid."""
        s = SuggestionOutput(severity="low", content="Nice to have", line=1)
        assert s.severity == "low"

    def test_out_of_scope_suggestion_requires_line(self) -> None:
        """Out-of-scope suggestions still require a line anchor (for ADO thread posting)."""
        s = SuggestionOutput(severity="low", content="Architectural concern", out_of_scope=True, line=42)
        assert s.line == 42
        assert s.out_of_scope is True

    def test_out_of_scope_suggestion_without_line_is_rejected(self) -> None:
        """Out-of-scope suggestions without a line anchor are invalid."""
        with pytest.raises(ValidationError):
            SuggestionOutput(severity="low", content="Architectural concern", out_of_scope=True)  # type: ignore[call-arg]

    def test_line_required_for_all_suggestions(self) -> None:
        """All suggestions must include a line anchor."""
        with pytest.raises(ValidationError):
            SuggestionOutput(severity="high", content="Fix this bug")  # type: ignore[call-arg]

    def test_endline_requires_line(self) -> None:
        """endLine is invalid without line (which is always required)."""
        with pytest.raises(ValidationError):
            SuggestionOutput(severity="medium", content="Refactor", endLine=3)  # type: ignore[call-arg]

    def test_endline_must_not_precede_line(self) -> None:
        """endLine must be greater than or equal to line."""
        with pytest.raises(ValidationError):
            SuggestionOutput(severity="medium", content="Refactor", line=5, endLine=4)

    def test_line_must_be_positive(self) -> None:
        """line must be a positive 1-based anchor."""
        with pytest.raises(ValidationError):
            SuggestionOutput(severity="medium", content="Refactor", line=0)

    def test_endline_must_be_positive(self) -> None:
        """endLine must be a positive 1-based anchor."""
        with pytest.raises(ValidationError):
            SuggestionOutput(severity="medium", content="Refactor", line=2, endLine=0)
