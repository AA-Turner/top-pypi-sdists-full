"""Unit tests for _run_comment_command in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, _run_comment_command


def test__run_comment_command_writes_body_file_and_removes_it_on_success() -> None:
    """_run_comment_command forwards args, always uses max_retries=0, and removes temp file."""
    recorded_body_file: Path | None = None

    def _capture_run_command(
        cmd: list[str],
        dry_run: bool,
        max_retries: int,
        retry_delay: float,
    ) -> None:
        nonlocal recorded_body_file
        assert cmd[:3] == ["gh", "pr", "comment"]
        assert cmd[3:] and cmd[3] == "--body-file"
        recorded_body_file = Path(cmd[4])
        assert recorded_body_file.read_text(encoding="utf-8") == "Comment body"
        assert dry_run is True
        assert max_retries == 0
        assert retry_delay == 0.0

    with patch("scripts.audit_pr_cleanup.run_command", side_effect=_capture_run_command) as mock_run:
        _run_comment_command(
            ["gh", "pr", "comment"],
            comment="Comment body",
            dry_run=True,
        )
        assert mock_run.call_count == 1
    assert recorded_body_file is not None
    assert not recorded_body_file.exists()


def test__run_comment_command_removes_body_file_when_run_command_raises() -> None:
    """_run_comment_command always removes the temp body file in exception paths."""
    recorded_body_file: Path | None = None

    def _raise_after_capturing(
        cmd: list[str],
        dry_run: bool,
        max_retries: int,
        retry_delay: float,
    ) -> None:
        nonlocal recorded_body_file
        assert cmd[:3] == ["gh", "issue", "comment"]
        assert cmd[3:] and cmd[3] == "--body-file"
        recorded_body_file = Path(cmd[4])
        assert recorded_body_file.exists()
        assert dry_run is False
        assert max_retries == 0
        assert retry_delay == 0.0
        raise AuditCleanupError("simulated gh failure")

    with patch("scripts.audit_pr_cleanup.run_command", side_effect=_raise_after_capturing):
        with pytest.raises(AuditCleanupError, match="simulated gh failure"):
            _run_comment_command(["gh", "issue", "comment"], comment="Issue comment")

    assert recorded_body_file is not None
    assert not recorded_body_file.exists()
