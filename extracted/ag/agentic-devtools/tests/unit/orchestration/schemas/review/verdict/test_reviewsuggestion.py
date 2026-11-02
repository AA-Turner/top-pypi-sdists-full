"""Tests for ReviewSuggestion Pydantic model."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from agentic_devtools.orchestration.schemas.review.verdict import ReviewSuggestion


class TestReviewSuggestion:
    """Tests for ReviewSuggestion schema validation."""

    def test_valid_with_line(self) -> None:
        """A suggestion with a line number is valid."""
        s = ReviewSuggestion(line=10, content="Add type hint")
        assert s.line == 10
        assert s.content == "Add type hint"
        assert s.out_of_scope is False

    def test_valid_out_of_scope_without_line(self) -> None:
        """out_of_scope=True suggestions do not require a line."""
        s = ReviewSuggestion(out_of_scope=True, content="Architectural concern")
        assert s.line is None
        assert s.out_of_scope is True

    def test_missing_line_raises_when_in_scope(self) -> None:
        """A suggestion without line and out_of_scope=False raises ValidationError."""
        with pytest.raises(ValidationError, match="line.*required"):
            ReviewSuggestion(content="no line given")

    def test_optional_fields_have_defaults(self) -> None:
        """Optional fields have sensible defaults."""
        s = ReviewSuggestion(line=1)
        assert s.endLine is None
        assert s.content == ""
        assert s.replacement_code is None
        assert s.severity is None
        assert s.link_text is None

    def test_all_optional_fields_set(self) -> None:
        """All optional fields can be set."""
        s = ReviewSuggestion(
            line=5,
            endLine=8,
            content="Explanation",
            replacement_code="new_code()",
            out_of_scope=False,
            severity="high",
            link_text="See docs",
        )
        assert s.endLine == 8
        assert s.replacement_code == "new_code()"
        assert s.severity == "high"
        assert s.link_text == "See docs"

    def test_extra_fields_allowed(self) -> None:
        """Extra fields from the LLM (e.g. 'description') are accepted."""
        s = ReviewSuggestion(line=3, description="LLM-provided description")  # type: ignore[call-arg]
        assert s.line == 3

    def test_model_dump_excludes_none(self) -> None:
        """model_dump(exclude_none=True) omits None-valued optional fields."""
        s = ReviewSuggestion(line=7, content="hint")
        d = s.model_dump(exclude_none=True)
        assert d["line"] == 7
        assert "endLine" not in d
        assert "replacement_code" not in d
