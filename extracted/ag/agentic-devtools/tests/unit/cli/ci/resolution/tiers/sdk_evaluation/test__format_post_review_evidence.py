"""Tests for _format_post_review_evidence."""

from agentic_devtools.cli.ci.resolution.github_adapter import GitHubThreadComment
from agentic_devtools.cli.ci.resolution.tiers.sdk_evaluation import _format_post_review_evidence


def test_formats_comments_in_order() -> None:
    comments = (
        GitHubThreadComment(body="first", created_at="2026-01-01", author_login="alice"),
        GitHubThreadComment(body="second", created_at="2026-01-02", author_login=None),
    )

    assert _format_post_review_evidence(comments) == ("[2026-01-01] @alice\nfirst\n---\n[2026-01-02] @unknown\nsecond")


def test_caps_total_evidence_characters() -> None:
    comment = GitHubThreadComment(body="x" * 20, created_at="2026-01-01", author_login="alice")

    assert _format_post_review_evidence((comment,), max_chars=10) == "[2026-01-0"


def test_caps_evidence_by_retaining_newest_comments_in_order() -> None:
    comments = (
        GitHubThreadComment(body="old", created_at="2026-01-01", author_login="alice"),
        GitHubThreadComment(body="newer", created_at="2026-01-02", author_login="bob"),
        GitHubThreadComment(body="newest", created_at="2026-01-03", author_login="carol"),
    )
    newest_evidence = _format_post_review_evidence(comments[1:], max_chars=68)

    assert _format_post_review_evidence(comments, max_chars=68) == newest_evidence
    assert newest_evidence == ("[2026-01-02] @bob\nnewer\n---\n[2026-01-03] @carol\nnewest")


def test_zero_budget_returns_empty_evidence() -> None:
    comment = GitHubThreadComment(body="evidence", created_at="2026-01-01", author_login="alice")

    assert _format_post_review_evidence((comment,), max_chars=0) == ""
