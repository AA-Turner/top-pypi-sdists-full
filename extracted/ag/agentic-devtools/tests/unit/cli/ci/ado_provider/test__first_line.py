"""Tests for the ado_provider._first_line snippet helper."""

from __future__ import annotations

from agentic_devtools.cli.ci.ado_provider import _first_line


class TestFirstLine:
    """Tests for the snippet extraction helper."""

    def test_strips_marker_and_returns_first_body_line(self) -> None:
        content = "<!-- agdt-review:v1 type:file-summary -->\nFirst body line\nSecond line"
        assert _first_line(content) == "First body line"

    def test_empty_content_returns_placeholder(self) -> None:
        assert _first_line("") == "(empty)"

    def test_whitespace_only_returns_placeholder(self) -> None:
        assert _first_line("   \n  \n\t") == "(empty)"

    def test_skips_leading_blank_lines(self) -> None:
        assert _first_line("\n\n   \nReal text") == "Real text"

    def test_truncates_long_line_to_80_chars(self) -> None:
        long_line = "x" * 200
        result = _first_line(long_line)
        assert result == "x" * 80
        assert len(result) == 80
