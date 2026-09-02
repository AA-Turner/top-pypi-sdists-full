"""Tests for _helpers.normalize_github_issue_number."""

from __future__ import annotations

from agentic_devtools.orchestration.nodes._helpers import normalize_github_issue_number


class TestNormalizeGithubIssueNumber:
    def test_accepts_plain_numeric(self):
        assert normalize_github_issue_number("42") == "42"

    def test_accepts_hash_prefixed_numeric(self):
        assert normalize_github_issue_number("#42") == "42"

    def test_rejects_empty(self):
        assert normalize_github_issue_number("") == ""

    def test_rejects_non_numeric(self):
        assert normalize_github_issue_number("abc") == ""

    def test_rejects_option_like(self):
        assert normalize_github_issue_number("--help") == ""

    def test_rejects_zero(self):
        assert normalize_github_issue_number("0") == ""

    def test_rejects_all_zeros(self):
        assert normalize_github_issue_number("000") == ""

    def test_accepts_very_large_positive_number(self):
        large = "9" * 5000
        assert normalize_github_issue_number(large) == large
