"""Unit tests for main in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupResult, main


def test_main_success_flow(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """main parses arguments, executes cleanup, prints results, and returns 0."""
    comment_file = tmp_path / "pr_eval.md"
    comment_file.write_text("## Valid PR Evaluation\n", encoding="utf-8")

    mock_result = AuditCleanupResult(
        pr_number=123,
        pr_commented=True,
        pr_closed=True,
        branch_deleted=True,
        issue_commented=True,
        issue_closed=True,
        success=True,
    )

    with patch("scripts.audit_pr_cleanup.cleanup_audit_pr", return_value=mock_result) as mock_cleanup:
        exit_code = main(
            [
                "--pr-number",
                "123",
                "--comment-file",
                str(comment_file),
                "--related-issue",
                "456",
                "--delete-branch",
            ]
        )

        assert exit_code == 0
        mock_cleanup.assert_called_once_with(
            pr_number=123,
            comment="## Valid PR Evaluation",
            related_issue="456",
            issue_comment="## Valid PR Evaluation",
            delete_branch=True,
            dry_run=False,
            max_retries=3,
            retry_delay=1.0,
        )

        out, _ = capsys.readouterr()
        assert "Successfully processed cleanup for PR #123." in out
        assert "PR #123 comment posted." in out
        assert "PR #123 closed." in out
        assert "PR #123 branch deleted." in out
        assert "Issue #456 comment posted." in out
        assert "Issue #456 closed." in out


def test_main_dry_run_with_custom_issue_comment_file(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """main supports separate issue comment files and dry-run output prefix."""
    pr_file = tmp_path / "pr.md"
    pr_file.write_text("PR Evaluation", encoding="utf-8")
    issue_file = tmp_path / "issue.md"
    issue_file.write_text("Issue Evaluation", encoding="utf-8")

    mock_result = AuditCleanupResult(
        pr_number=789,
        pr_commented=True,
        pr_closed=True,
        branch_deleted=False,
        issue_commented=True,
        issue_closed=True,
        success=True,
    )

    with patch("scripts.audit_pr_cleanup.cleanup_audit_pr", return_value=mock_result):
        exit_code = main(
            [
                "--pr-number",
                "789",
                "--comment-file",
                str(pr_file),
                "--related-issue",
                "#888",
                "--issue-comment-file",
                str(issue_file),
                "--dry-run",
            ]
        )

        assert exit_code == 0
        out, _ = capsys.readouterr()
        assert "[DRY-RUN] Successfully processed cleanup for PR #789." in out
        assert "Issue #888 comment posted." in out
        assert "Issue #888 closed." in out
        assert "Issue ##888" not in out


def test_main_with_direct_comment_strings(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """main supports direct comment strings for both PR and issue."""
    mock_result = AuditCleanupResult(
        pr_number=555,
        pr_commented=True,
        pr_closed=True,
        branch_deleted=False,
        issue_commented=True,
        issue_closed=False,
        success=True,
    )

    with patch("scripts.audit_pr_cleanup.cleanup_audit_pr", return_value=mock_result) as mock_cleanup:
        exit_code = main(
            [
                "--pr-number",
                "555",
                "--comment",
                "Direct PR comment",
                "--related-issue",
                "666",
                "--issue-comment",
                "Direct issue comment",
            ]
        )

        assert exit_code == 0
        mock_cleanup.assert_called_once_with(
            pr_number=555,
            comment="Direct PR comment",
            related_issue="666",
            issue_comment="Direct issue comment",
            delete_branch=False,
            dry_run=False,
            max_retries=3,
            retry_delay=1.0,
        )


def test_main_handles_exception_and_returns_1(capsys: pytest.CaptureFixture[str]) -> None:
    """main catches exceptions, prints to stderr, and returns exit code 1."""
    with patch("scripts.audit_pr_cleanup.parse_args", side_effect=ValueError("Invalid config")):
        exit_code = main(["--invalid"])
        assert exit_code == 1
        _, err = capsys.readouterr()
        assert "Error during audit cleanup: Invalid config" in err


def test_main_explicit_empty_issue_comment_is_rejected(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """main rejects an explicit empty issue comment instead of falling back to the PR comment."""
    with patch("scripts.audit_pr_cleanup.cleanup_audit_pr") as mock_cleanup:
        exit_code = main(
            [
                "--pr-number",
                "321",
                "--comment",
                "Evaluation",
                "--related-issue",
                "654",
                "--issue-comment",
                "",
            ]
        )

    assert exit_code == 1
    mock_cleanup.assert_not_called()
    _, err = capsys.readouterr()
    assert "Error during audit cleanup: Comment string cannot be empty." in err


def test_main_success_without_related_issue(capsys: pytest.CaptureFixture[str]) -> None:
    """main succeeds without an issue and does not print unset result statuses."""
    mock_result = AuditCleanupResult(pr_number=321)

    with patch("scripts.audit_pr_cleanup.cleanup_audit_pr", return_value=mock_result):
        exit_code = main(["--pr-number", "321", "--comment", "Evaluation"])

    assert exit_code == 0
    out, _ = capsys.readouterr()
    assert out == "Successfully processed cleanup for PR #321.\n"


def test_main_returns_1_when_success_is_false(capsys: pytest.CaptureFixture[str]) -> None:
    """main returns 1 and prints an error when result.success is False."""
    mock_result = AuditCleanupResult(
        pr_number=123,
        pr_closed=False,
        success=False,
        error_message="PR #123 is still open after close attempt",
    )

    with patch("scripts.audit_pr_cleanup.cleanup_audit_pr", return_value=mock_result):
        exit_code = main(["--pr-number", "123", "--comment", "Evaluation"])

    assert exit_code == 1
    _, err = capsys.readouterr()
    assert "postcondition check failed" in err
    assert "still open" in err


def test_main_url_issue_display_is_normalized(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """main normalizes a URL-form --related-issue to a plain number in output."""
    comment_file = tmp_path / "pr_eval.md"
    comment_file.write_text("## Evaluation", encoding="utf-8")

    mock_result = AuditCleanupResult(
        pr_number=99,
        pr_commented=True,
        pr_closed=True,
        issue_commented=True,
        issue_closed=True,
        success=True,
    )

    with patch("scripts.audit_pr_cleanup.cleanup_audit_pr", return_value=mock_result):
        exit_code = main(
            [
                "--pr-number",
                "99",
                "--comment-file",
                str(comment_file),
                "--related-issue",
                "https://github.com/swai-factory/agentic-devtools/issues/3881",
            ]
        )

    assert exit_code == 0
    out, _ = capsys.readouterr()
    assert "Issue #3881 comment posted." in out
    assert "Issue #3881 closed." in out
    assert "Issue #https" not in out
