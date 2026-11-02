"""Unit tests for post_issue_comment in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import ANY, patch

from scripts.audit_pr_cleanup import post_issue_comment


def test_post_issue_comment_with_integer() -> None:
    """post_issue_comment writes the Markdown body to a temp file for gh."""
    recorded_body_file: Path | None = None

    def _capture_run_command(
        cmd: list[str],
        dry_run: bool,
        max_retries: int,
        retry_delay: float,
    ) -> None:
        nonlocal recorded_body_file
        assert cmd[:6] == ["gh", "issue", "comment", "3881", "--repo", "swai-factory/agentic-devtools"]
        assert cmd[6] == "--body-file"
        recorded_body_file = Path(cmd[7])
        body = recorded_body_file.read_text(encoding="utf-8")
        assert body.startswith("Issue evaluation comment\n\n<!-- audit-pr-cleanup:issue:3881:")
        assert body.endswith(" -->")
        assert dry_run is False
        assert max_retries == 0
        assert retry_delay == 0.0

    with (
        patch("scripts.audit_pr_cleanup._comment_marker_exists", return_value=False) as mock_marker_exists,
        patch("scripts.audit_pr_cleanup.run_command", side_effect=_capture_run_command) as mock_run,
    ):
        posted = post_issue_comment(
            issue_number=3881,
            comment="Issue evaluation comment",
            dry_run=False,
            max_retries=6,
            retry_delay=0.75,
        )
        assert posted is True
        assert mock_run.call_count == 1
        mock_marker_exists.assert_called_once_with(
            3881,
            marker=ANY,
            dry_run=False,
            max_retries=6,
            retry_delay=0.75,
        )
    assert recorded_body_file is not None
    assert not recorded_body_file.exists()


def test_post_issue_comment_with_hash_string() -> None:
    """post_issue_comment normalizes '#3881' and forwards dry-run mode."""
    recorded_body_file: Path | None = None

    def _capture_run_command(
        cmd: list[str],
        dry_run: bool,
        max_retries: int,
        retry_delay: float,
    ) -> None:
        nonlocal recorded_body_file
        assert cmd[:6] == ["gh", "issue", "comment", "3881", "--repo", "swai-factory/agentic-devtools"]
        assert cmd[6] == "--body-file"
        recorded_body_file = Path(cmd[7])
        body = recorded_body_file.read_text(encoding="utf-8")
        assert body.startswith("Issue comment\n\n<!-- audit-pr-cleanup:issue:3881:")
        assert body.endswith(" -->")
        assert dry_run is True
        assert max_retries == 0
        assert retry_delay == 0.0

    with (
        patch("scripts.audit_pr_cleanup._comment_marker_exists", return_value=False) as mock_marker_exists,
        patch("scripts.audit_pr_cleanup.run_command", side_effect=_capture_run_command) as mock_run,
    ):
        posted = post_issue_comment(
            issue_number="#3881",
            comment="Issue comment",
            dry_run=True,
            max_retries=1,
            retry_delay=2.0,
        )
        assert posted is True
        assert mock_run.call_count == 1
        mock_marker_exists.assert_called_once_with(
            3881,
            marker=ANY,
            dry_run=True,
            max_retries=1,
            retry_delay=2.0,
        )
    assert recorded_body_file is not None
    assert not recorded_body_file.exists()


def test_post_issue_comment_skips_duplicate_marker() -> None:
    """post_issue_comment is a no-op when the same hidden marker already exists."""
    with (
        patch("scripts.audit_pr_cleanup._comment_marker_exists", return_value=True) as mock_marker_exists,
        patch("scripts.audit_pr_cleanup.run_command") as mock_run,
    ):
        posted = post_issue_comment(
            issue_number=3881,
            comment="Already posted",
            dry_run=False,
            max_retries=7,
            retry_delay=0.4,
        )

    assert posted is False
    mock_marker_exists.assert_called_once_with(
        3881,
        marker=ANY,
        dry_run=False,
        max_retries=7,
        retry_delay=0.4,
    )
    mock_run.assert_not_called()


def test_post_issue_comment_trailing_whitespace_normalized() -> None:
    """post_issue_comment generates the same marker for body and body-with-trailing-whitespace."""
    markers: list[str] = []

    def _capture_marker(
        cmd: list[str],
        dry_run: bool,
        max_retries: int,
        retry_delay: float,
    ) -> None:
        body = Path(cmd[7]).read_text(encoding="utf-8")
        markers.append(body.split("\n\n")[-1])

    with patch("scripts.audit_pr_cleanup._comment_marker_exists", return_value=False):
        with patch("scripts.audit_pr_cleanup.run_command", side_effect=_capture_marker):
            post_issue_comment(issue_number=3881, comment="Body", dry_run=False)
        with patch("scripts.audit_pr_cleanup.run_command", side_effect=_capture_marker):
            post_issue_comment(issue_number=3881, comment="Body   \n  ", dry_run=False)

    assert len(markers) == 2
    assert markers[0] == markers[1], "marker should be identical regardless of trailing whitespace"
