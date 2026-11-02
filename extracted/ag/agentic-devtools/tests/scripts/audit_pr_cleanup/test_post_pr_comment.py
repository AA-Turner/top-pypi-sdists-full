"""Unit tests for post_pr_comment in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import ANY, patch

from scripts.audit_pr_cleanup import post_pr_comment


def test_post_pr_comment_invokes_run_command() -> None:
    """post_pr_comment writes the Markdown body to a temp file for gh."""
    recorded_body_file: Path | None = None

    def _capture_run_command(
        cmd: list[str],
        dry_run: bool,
        max_retries: int,
        retry_delay: float,
    ) -> None:
        nonlocal recorded_body_file
        assert cmd[:6] == ["gh", "pr", "comment", "123", "--repo", "swai-factory/agentic-devtools"]
        assert cmd[6] == "--body-file"
        recorded_body_file = Path(cmd[7])
        body = recorded_body_file.read_text(encoding="utf-8")
        assert body.startswith("Evaluation comment\n\n<!-- audit-pr-cleanup:pr:123:")
        assert body.endswith(" -->")
        assert dry_run is False
        assert max_retries == 0
        assert retry_delay == 0.0

    with (
        patch("scripts.audit_pr_cleanup._comment_marker_exists", return_value=False) as mock_marker_exists,
        patch("scripts.audit_pr_cleanup.run_command", side_effect=_capture_run_command) as mock_run,
    ):
        posted = post_pr_comment(
            pr_number=123,
            comment="Evaluation comment",
            dry_run=False,
            max_retries=5,
            retry_delay=0.25,
        )
        assert posted is True
        assert mock_run.call_count == 1
        mock_marker_exists.assert_called_once_with(
            123,
            marker=ANY,
            dry_run=False,
            max_retries=5,
            retry_delay=0.25,
        )
    assert recorded_body_file is not None
    assert not recorded_body_file.exists()


def test_post_pr_comment_dry_run() -> None:
    """post_pr_comment passes dry_run through while still using a body file."""
    recorded_body_file: Path | None = None

    def _capture_run_command(
        cmd: list[str],
        dry_run: bool,
        max_retries: int,
        retry_delay: float,
    ) -> None:
        nonlocal recorded_body_file
        assert cmd[:6] == ["gh", "pr", "comment", "456", "--repo", "swai-factory/agentic-devtools"]
        assert cmd[6] == "--body-file"
        recorded_body_file = Path(cmd[7])
        body = recorded_body_file.read_text(encoding="utf-8")
        assert body.startswith("Dry run comment\n\n<!-- audit-pr-cleanup:pr:456:")
        assert body.endswith(" -->")
        assert dry_run is True
        assert max_retries == 0
        assert retry_delay == 0.0

    with (
        patch("scripts.audit_pr_cleanup._comment_marker_exists", return_value=False) as mock_marker_exists,
        patch("scripts.audit_pr_cleanup.run_command", side_effect=_capture_run_command) as mock_run,
    ):
        posted = post_pr_comment(
            pr_number=456,
            comment="Dry run comment",
            dry_run=True,
            max_retries=2,
            retry_delay=1.5,
        )
        assert posted is True
        assert mock_run.call_count == 1
        mock_marker_exists.assert_called_once_with(
            456,
            marker=ANY,
            dry_run=True,
            max_retries=2,
            retry_delay=1.5,
        )
    assert recorded_body_file is not None
    assert not recorded_body_file.exists()


def test_post_pr_comment_skips_duplicate_marker() -> None:
    """post_pr_comment is a no-op when the same hidden marker already exists."""
    with (
        patch("scripts.audit_pr_cleanup._comment_marker_exists", return_value=True) as mock_marker_exists,
        patch("scripts.audit_pr_cleanup.run_command") as mock_run,
    ):
        posted = post_pr_comment(
            pr_number=789,
            comment="Already posted",
            dry_run=False,
            max_retries=4,
            retry_delay=0.5,
        )

    assert posted is False
    mock_marker_exists.assert_called_once_with(
        789,
        marker=ANY,
        dry_run=False,
        max_retries=4,
        retry_delay=0.5,
    )
    mock_run.assert_not_called()


def test_post_pr_comment_trailing_whitespace_normalized() -> None:
    """post_pr_comment generates the same marker for body and body-with-trailing-whitespace."""
    markers: list[str] = []

    def _capture_marker(
        cmd: list[str],
        dry_run: bool,
        max_retries: int,
        retry_delay: float,
    ) -> None:
        body = Path(cmd[7]).read_text(encoding="utf-8")
        # Extract the marker from the last line
        markers.append(body.split("\n\n")[-1])

    with patch("scripts.audit_pr_cleanup._comment_marker_exists", return_value=False):
        with patch("scripts.audit_pr_cleanup.run_command", side_effect=_capture_marker):
            post_pr_comment(pr_number=100, comment="Body", dry_run=False)
        with patch("scripts.audit_pr_cleanup.run_command", side_effect=_capture_marker):
            post_pr_comment(pr_number=100, comment="Body   \n  ", dry_run=False)

    assert len(markers) == 2
    assert markers[0] == markers[1], "marker should be identical regardless of trailing whitespace"
