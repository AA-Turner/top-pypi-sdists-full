"""Tests for check_syntax() (FR-001, E001)."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import check_syntax


class TestCheckSyntax:
    """Tests for E001 malformed-placeholder detection."""

    def test_valid_placeholder_no_diagnostics(self) -> None:
        """A well-formed placeholder produces no diagnostics."""
        assert check_syntax("Line {{title}} end") == []

    def test_unclosed_placeholder(self) -> None:
        """An unclosed '{{' is reported as E001."""
        diags = check_syntax("start {{title")
        assert len(diags) == 1
        assert diags[0].code == "E001"
        assert diags[0].level == "error"
        assert diags[0].line == 1
        assert diags[0].column == 7
        assert "Unclosed" in diags[0].message

    def test_stray_closing_delimiter(self) -> None:
        """A stray '}}' with no opening is reported as E001."""
        diags = check_syntax("oops }} here")
        assert len(diags) == 1
        assert diags[0].code == "E001"
        assert diags[0].column == 6
        assert "Stray" in diags[0].message

    def test_empty_placeholder(self) -> None:
        """An empty '{{}}' is reported as E001."""
        diags = check_syntax("{{}}")
        assert len(diags) == 1
        assert diags[0].code == "E001"
        assert "{{}}" in diags[0].message

    def test_placeholder_with_space(self) -> None:
        """A placeholder with an invalid space is reported as E001."""
        diags = check_syntax("{{foo bar}}")
        assert len(diags) == 1
        assert diags[0].code == "E001"

    def test_placeholder_starting_with_digit(self) -> None:
        """A placeholder starting with a digit is reported as E001."""
        diags = check_syntax("{{123abc}}")
        assert len(diags) == 1
        assert diags[0].code == "E001"

    def test_multiple_lines_line_numbers(self) -> None:
        """Line numbers are 1-based and reported per line."""
        diags = check_syntax("ok {{title}}\nbad {{oops\nfine")
        assert len(diags) == 1
        assert diags[0].line == 2

    def test_plain_text_no_diagnostics(self) -> None:
        """Plain text with no braces produces no diagnostics."""
        assert check_syntax("just some text") == []

    def test_valid_then_stray_close(self) -> None:
        """A valid placeholder followed by a stray close reports only the stray."""
        diags = check_syntax("{{title}} }}")
        assert len(diags) == 1
        assert diags[0].column == 11
