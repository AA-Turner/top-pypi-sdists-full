"""Tests for _normalize_issue_title helper."""

from __future__ import annotations

from agentic_devtools.cli.speckit.hierarchy_detector import _normalize_issue_title


class TestNormalizeIssueTitle:
    """Tests for _normalize_issue_title helper."""

    def test_valid_string_is_returned_unchanged(self) -> None:
        """A non-empty string title is returned as-is."""
        assert _normalize_issue_title("My feature", 42) == "My feature"

    def test_whitespace_only_string_falls_back_to_issue_label(self) -> None:
        """A whitespace-only string is treated as empty and falls back."""
        assert _normalize_issue_title("   ", 7) == "Issue #7"

    def test_empty_string_falls_back_to_issue_label(self) -> None:
        """An empty string falls back to the Issue #N label."""
        assert _normalize_issue_title("", 99) == "Issue #99"

    def test_none_falls_back_to_issue_label(self) -> None:
        """None falls back to the Issue #N label, not the string 'None'."""
        result = _normalize_issue_title(None, 42)
        assert result == "Issue #42"
        assert result != "None"

    def test_non_string_falls_back_to_issue_label(self) -> None:
        """Non-string values (e.g. int) fall back to the Issue #N label."""
        assert _normalize_issue_title(123, 5) == "Issue #5"

    def test_leading_trailing_whitespace_is_stripped(self) -> None:
        """Valid title with surrounding whitespace is stripped."""
        assert _normalize_issue_title("  Fix bug  ", 10) == "Fix bug"
