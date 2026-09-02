"""Tests for normalize_issue_key."""

import pytest

from agentic_devtools.cli.git.branch_naming import normalize_issue_key


class TestNormalizeIssueKey:
    """Tests for normalize_issue_key."""

    def test_strips_leading_hash_from_github_issue_number(self):
        """A leading hash is removed from numeric GitHub issue keys."""
        assert normalize_issue_key("#1900") == "1900"

    def test_strips_multiple_leading_hashes(self):
        """Multiple leading hashes are stripped before validation."""
        assert normalize_issue_key("##1900") == "1900"

    def test_preserves_jira_key(self):
        """Jira-style issue keys are preserved."""
        assert normalize_issue_key("PROJECT-1234") == "PROJECT-1234"

    @pytest.mark.parametrize("value", ["", "   "])
    def test_rejects_empty_or_whitespace(self, value):
        """Empty and whitespace-only keys are rejected."""
        with pytest.raises(ValueError, match="empty or whitespace-only"):
            normalize_issue_key(value)

    def test_rejects_hash_only_value(self):
        """A key containing only hash characters is rejected after stripping."""
        with pytest.raises(ValueError, match="after stripping"):
            normalize_issue_key("###")

    @pytest.mark.parametrize("value", [None, 1900, object()])
    def test_rejects_non_string_values(self, value):
        """Non-string issue keys are rejected before normalization."""
        with pytest.raises(ValueError, match="must be a string"):
            normalize_issue_key(value)  # type: ignore[arg-type]

    @pytest.mark.parametrize("value", ["feature/1900", "PROJECT..123", "PROJECT 123", "not-valid"])
    def test_rejects_path_or_invalid_separator_values(self, value):
        """Keys containing path separators, dot-dot, whitespace, or invalid separators are rejected."""
        with pytest.raises(ValueError, match="does not normalize"):
            normalize_issue_key(value)
