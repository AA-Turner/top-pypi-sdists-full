"""Tests for PLACEHOLDER_RE constant."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.template_placeholders import PLACEHOLDER_RE


class TestPlaceholderRe:
    """Tests for the shared placeholder regex."""

    def test_matches_valid_name(self) -> None:
        """Matches a simple identifier placeholder."""
        match = PLACEHOLDER_RE.search("{{title}}")
        assert match is not None
        assert match.group(1) == "title"

    def test_rejects_empty(self) -> None:
        """Does not match empty braces."""
        assert PLACEHOLDER_RE.search("{{}}") is None

    def test_rejects_hyphen(self) -> None:
        """Does not match names with hyphens."""
        assert PLACEHOLDER_RE.search("{{a-b}}") is None
