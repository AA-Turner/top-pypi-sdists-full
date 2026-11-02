"""Tests for detect_parent_cli._normalize_title()."""

from __future__ import annotations

from agentic_devtools.cli.speckit.detect_parent_cli import _normalize_title


class TestNormalizeTitle:
    """Tests for title normalization logic."""

    def test_removes_hash_from_issue_title(self):
        """'Issue #200' becomes 'Issue 200' when issue_number matches."""
        assert _normalize_title("Issue #200", 200) == "Issue 200"

    def test_preserves_normal_title(self):
        """A regular title is unchanged."""
        assert _normalize_title("Add webhook support", 42) == "Add webhook support"

    def test_preserves_hash_in_non_issue_pattern(self):
        """'Issue #NNN' pattern only matches exact format."""
        assert _normalize_title("Fix issue #123 regression", 123) == "Fix issue #123 regression"

    def test_preserves_multidigit_issue(self):
        """Works with large issue numbers."""
        assert _normalize_title("Issue #12345", 12345) == "Issue 12345"

    def test_empty_title(self):
        """Empty string stays empty."""
        assert _normalize_title("", 1) == ""

    def test_does_not_normalize_different_issue_number(self):
        """Does not strip '#' when the issue number does not match the current issue."""
        # title is a user-provided title for issue 123, but current issue is 456
        assert _normalize_title("Issue #123", 456) == "Issue #123"

    def test_does_not_normalize_partial_match(self):
        """Does not normalize when the title has extra content beyond the pattern."""
        assert _normalize_title("Issue #200 follow-up", 200) == "Issue #200 follow-up"
