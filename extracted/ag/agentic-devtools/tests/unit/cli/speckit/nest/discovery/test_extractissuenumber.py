"""Tests for extract_issue_number in nest/discovery.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.nest.discovery import extract_issue_number


class TestExtractIssueNumber:
    """Tests for extract_issue_number."""

    def test_returns_number_from_valid_pattern(self) -> None:
        """Returns the leading number from a {number}-{slug} name."""
        assert extract_issue_number("42-my-feature") == 42

    def test_returns_none_for_slug_only_name(self) -> None:
        """Returns None when the name has no leading number."""
        assert extract_issue_number("not-a-spec") is None

    def test_returns_none_for_pure_numeric_name(self) -> None:
        """Returns None for a purely numeric name (nested hierarchy node)."""
        assert extract_issue_number("100") is None

    def test_returns_number_with_multi_digit_prefix(self) -> None:
        """Handles multi-digit issue numbers correctly."""
        assert extract_issue_number("1234-big-epic") == 1234

    def test_returns_none_for_empty_string(self) -> None:
        """Returns None for an empty input string."""
        assert extract_issue_number("") is None
