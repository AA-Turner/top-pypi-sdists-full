"""Unit tests for normalize_issue_number in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

import pytest

from scripts.audit_pr_cleanup import normalize_issue_number


def test_normalize_issue_number_from_int() -> None:
    """normalize_issue_number returns positive integer directly."""
    assert normalize_issue_number(3881) == 3881


def test_normalize_issue_number_from_hash_string() -> None:
    """normalize_issue_number parses '#3881' to 3881."""
    assert normalize_issue_number("#3881") == 3881


def test_normalize_issue_number_from_plain_string() -> None:
    """normalize_issue_number parses '3881' to 3881."""
    assert normalize_issue_number("3881") == 3881


def test_normalize_issue_number_from_url() -> None:
    """normalize_issue_number parses a current-repository GitHub issue URL."""
    assert normalize_issue_number("https://github.com/swai-factory/agentic-devtools/issues/3881") == 3881


def test_normalize_issue_number_invalid_int_raises() -> None:
    """normalize_issue_number raises ValueError for non-positive integer."""
    with pytest.raises(ValueError, match="must be positive"):
        normalize_issue_number(0)
    with pytest.raises(ValueError, match="must be positive"):
        normalize_issue_number(-5)


def test_normalize_issue_number_url_zero_raises() -> None:
    """normalize_issue_number raises ValueError for a URL with issue number 0."""
    with pytest.raises(ValueError, match="must be positive"):
        normalize_issue_number("https://github.com/swai-factory/agentic-devtools/issues/0")


def test_normalize_issue_number_invalid_string_raises() -> None:
    """normalize_issue_number raises ValueError for strings without digits or zero/negative."""
    with pytest.raises(ValueError, match="Could not parse issue number"):
        normalize_issue_number("invalid-issue")
    with pytest.raises(ValueError, match="Could not parse issue number"):
        normalize_issue_number("abc3881")
    with pytest.raises(ValueError, match="must be positive"):
        normalize_issue_number("#0")


def test_normalize_issue_number_cross_repository_url_raises() -> None:
    """normalize_issue_number rejects GitHub issue URLs outside the current repository."""
    with pytest.raises(ValueError, match="Unsupported issue URL repository"):
        normalize_issue_number("https://github.com/other/repo/issues/3881")


def test_normalize_issue_number_non_github_url_raises() -> None:
    """normalize_issue_number rejects non-GitHub issue URLs."""
    with pytest.raises(ValueError, match="Unsupported issue URL host"):
        normalize_issue_number("https://example.com/swai-factory/agentic-devtools/issues/3881")


def test_normalize_issue_number_issue_comment_url_path_raises() -> None:
    """normalize_issue_number rejects GitHub issue URLs with extra path segments."""
    with pytest.raises(ValueError, match="Unsupported issue URL path"):
        normalize_issue_number("https://github.com/swai-factory/agentic-devtools/issues/3881/comments/123")


def test_normalize_issue_number_trailing_slash_url_raises() -> None:
    """normalize_issue_number rejects current-repository issue URLs with a trailing slash."""
    with pytest.raises(ValueError, match="Unsupported issue URL path"):
        normalize_issue_number("https://github.com/swai-factory/agentic-devtools/issues/3881/")


def test_normalize_issue_number_rejects_bool_true() -> None:
    """normalize_issue_number raises ValueError for True (bool is int subclass)."""
    with pytest.raises(ValueError, match="must be an integer"):
        normalize_issue_number(True)


def test_normalize_issue_number_rejects_bool_false() -> None:
    """normalize_issue_number raises ValueError for False (bool is int subclass)."""
    with pytest.raises(ValueError, match="must be an integer"):
        normalize_issue_number(False)
