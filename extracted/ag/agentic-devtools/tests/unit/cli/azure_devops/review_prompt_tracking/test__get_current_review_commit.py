"""Tests for _get_current_review_commit."""

from agentic_devtools.cli.azure_devops.review_prompt_tracking import _get_current_review_commit


def test_extracts_trimmed_source_commit_from_nested_pr_details() -> None:
    assert _get_current_review_commit({"pullRequest": {"lastMergeSourceCommit": {"commitId": " abc123 "}}}) == "abc123"


def test_returns_none_for_missing_source_commit() -> None:
    assert _get_current_review_commit({"lastMergeSourceCommit": None}) is None
