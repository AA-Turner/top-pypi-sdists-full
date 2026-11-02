"""Tests for extract_placeholders() (FR-002)."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import extract_placeholders


class TestExtractPlaceholders:
    """Tests for placeholder name/position extraction."""

    def test_no_placeholders(self) -> None:
        """Content with no placeholders returns an empty list."""
        assert extract_placeholders("plain text") == []

    def test_single_placeholder_position(self) -> None:
        """A single placeholder yields its name with 1-based line/column."""
        result = extract_placeholders("ab {{title}}")
        assert result == [("title", 1, 4)]

    def test_multiple_placeholders_same_line(self) -> None:
        """Multiple placeholders on one line are all returned in order."""
        result = extract_placeholders("{{a}} {{b_c}}")
        assert result == [("a", 1, 1), ("b_c", 1, 7)]

    def test_placeholders_across_lines(self) -> None:
        """Line numbers increment across newlines."""
        result = extract_placeholders("{{a}}\n\n{{b}}")
        assert result == [("a", 1, 1), ("b", 3, 1)]

    def test_malformed_placeholders_ignored(self) -> None:
        """Malformed placeholders are not extracted as valid names."""
        assert extract_placeholders("{{bad name}} {{}}") == []
