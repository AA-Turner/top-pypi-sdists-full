"""Tests for _PLACEHOLDER_RE regex in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _PLACEHOLDER_RE


class TestPlaceholderRe:
    """Tests for the _PLACEHOLDER_RE compiled regex (FR-001)."""

    def test_matches_simple_placeholder(self) -> None:
        """Matches a simple {{name}} placeholder."""
        m = _PLACEHOLDER_RE.search("{{title}}")
        assert m is not None
        assert m.group(1) == "title"

    def test_matches_underscore_placeholder(self) -> None:
        """Matches placeholder with underscores."""
        m = _PLACEHOLDER_RE.search("{{issue_id}}")
        assert m is not None
        assert m.group(1) == "issue_id"

    def test_matches_alphanumeric_placeholder(self) -> None:
        """Matches placeholder with digits."""
        m = _PLACEHOLDER_RE.search("{{field2}}")
        assert m is not None
        assert m.group(1) == "field2"

    def test_does_not_match_numeric_start(self) -> None:
        """Does not match placeholder starting with digit."""
        m = _PLACEHOLDER_RE.search("{{2field}}")
        assert m is None

    def test_does_not_match_hyphen(self) -> None:
        """Does not match placeholder with hyphens."""
        m = _PLACEHOLDER_RE.search("{{my-field}}")
        assert m is None

    def test_does_not_match_spaces(self) -> None:
        """Does not match placeholder with spaces."""
        m = _PLACEHOLDER_RE.search("{{my field}}")
        assert m is None

    def test_findall_multiple(self) -> None:
        """Finds all placeholders in a string."""
        results = _PLACEHOLDER_RE.findall("{{a}} and {{b_c}}")
        assert results == ["a", "b_c"]

    def test_empty_braces_not_matched(self) -> None:
        """Empty braces {{}} do not match."""
        m = _PLACEHOLDER_RE.search("{{}}")
        assert m is None
