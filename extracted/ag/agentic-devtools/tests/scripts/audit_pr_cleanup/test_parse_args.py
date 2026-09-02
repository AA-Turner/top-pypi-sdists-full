"""Unit tests for parse_args in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

import pytest

from scripts.audit_pr_cleanup import parse_args


def test_parse_args_minimal_required() -> None:
    """parse_args successfully parses minimal required arguments."""
    args = parse_args(["--pr-number", "1234", "--comment", "Evaluation text"])
    assert args.pr_number == 1234
    assert args.comment_file is None
    assert args.comment == "Evaluation text"
    assert args.related_issue is None
    assert args.issue_comment_file is None
    assert args.issue_comment is None
    assert args.delete_branch is False
    assert args.dry_run is False
    assert args.max_retries == 3
    assert args.retry_delay == 1.0


def test_parse_args_all_options() -> None:
    """parse_args successfully parses all CLI options."""
    args = parse_args(
        [
            "--pr-number",
            "5678",
            "--comment-file",
            "pr_comment.md",
            "--related-issue",
            "#999",
            "--issue-comment-file",
            "issue_comment.md",
            "--delete-branch",
            "--dry-run",
            "--max-retries",
            "5",
            "--retry-delay",
            "2.5",
        ]
    )
    assert args.pr_number == 5678
    assert args.comment_file == "pr_comment.md"
    assert args.comment is None
    assert args.related_issue == "#999"
    assert args.issue_comment_file == "issue_comment.md"
    assert args.issue_comment is None
    assert args.delete_branch is True
    assert args.dry_run is True
    assert args.max_retries == 5
    assert args.retry_delay == 2.5


def test_parse_args_missing_pr_number_exits() -> None:
    """parse_args raises SystemExit when required --pr-number is omitted."""
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args_both_comment_sources_rejected() -> None:
    """parse_args raises SystemExit when both --comment-file and --comment are supplied."""
    with pytest.raises(SystemExit):
        parse_args(
            [
                "--pr-number",
                "1234",
                "--comment-file",
                "pr.md",
                "--comment",
                "Direct text",
            ]
        )


def test_parse_args_comment_source_required() -> None:
    """parse_args raises SystemExit when neither --comment-file nor --comment is provided."""
    with pytest.raises(SystemExit):
        parse_args(["--pr-number", "1234"])


def test_parse_args_negative_max_retries_exits() -> None:
    """parse_args raises SystemExit when --max-retries is negative."""
    with pytest.raises(SystemExit):
        parse_args(["--pr-number", "1234", "--comment", "text", "--max-retries", "-1"])


def test_parse_args_negative_retry_delay_exits() -> None:
    """parse_args raises SystemExit when --retry-delay is negative."""
    with pytest.raises(SystemExit):
        parse_args(["--pr-number", "1234", "--comment", "text", "--retry-delay", "-1.0"])


@pytest.mark.parametrize("value", ["nan", "inf"])
def test_parse_args_non_finite_retry_delay_exits(value: str) -> None:
    """parse_args raises SystemExit when --retry-delay is NaN or infinite."""
    with pytest.raises(SystemExit):
        parse_args(["--pr-number", "1234", "--comment", "text", "--retry-delay", value])


def test_parse_args_both_issue_comment_sources_rejected() -> None:
    """parse_args raises SystemExit when both issue comment sources are supplied."""
    with pytest.raises(SystemExit):
        parse_args(
            [
                "--pr-number",
                "1234",
                "--comment",
                "text",
                "--related-issue",
                "456",
                "--issue-comment-file",
                "issue.md",
                "--issue-comment",
                "direct issue text",
            ]
        )


def test_parse_args_issue_comment_requires_related_issue() -> None:
    """parse_args raises SystemExit when issue comment options lack --related-issue."""
    with pytest.raises(SystemExit):
        parse_args(
            [
                "--pr-number",
                "1234",
                "--comment",
                "text",
                "--issue-comment",
                "direct issue text",
            ]
        )


def test_parse_args_empty_issue_comment_still_requires_related_issue() -> None:
    """parse_args treats an explicit empty issue comment as option presence for validation."""
    with pytest.raises(SystemExit):
        parse_args(
            [
                "--pr-number",
                "1234",
                "--comment",
                "text",
                "--issue-comment",
                "",
            ]
        )
