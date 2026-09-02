"""Unit tests for run_command in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, run_command


def test_run_command_dry_run() -> None:
    """run_command in dry_run mode should return synthetic CompletedProcess without running subprocess."""
    with patch("subprocess.run") as mock_run:
        result = run_command(["gh", "pr", "close", "123"], dry_run=True)
        assert result.returncode == 0
        assert "[DRY-RUN]" in result.stdout
        mock_run.assert_not_called()


def test_run_command_success() -> None:
    """run_command executes successfully and returns CompletedProcess."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "version"],
        returncode=0,
        stdout="gh version 2.40.0",
        stderr="",
    )
    with patch("subprocess.run", return_value=mock_res) as mock_run:
        result = run_command(["gh", "version"], dry_run=False)
        assert result.returncode == 0
        assert "gh version" in result.stdout
        mock_run.assert_called_once_with(
            ["gh", "version"],
            capture_output=True,
            text=True,
            shell=False,
            check=False,
        )


def test_run_command_permanent_failure_raises_error() -> None:
    """run_command raises AuditCleanupError on permanent failure without retrying."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "close", "999"],
        returncode=1,
        stdout="",
        stderr="GraphQL: Could not resolve to a PullRequest with the number of 999 (NOT_FOUND)",
    )
    with patch("subprocess.run", return_value=mock_res) as mock_run:
        with pytest.raises(AuditCleanupError, match=r"(?s)Command failed.*NOT_FOUND"):
            run_command(["gh", "pr", "close", "999"], dry_run=False, max_retries=3)
        assert mock_run.call_count == 1


def test_run_command_retries_transient_failure_then_succeeds() -> None:
    """run_command retries on transient errors and returns if subsequent attempt succeeds."""
    mock_fail = subprocess.CompletedProcess(
        args=["gh", "pr", "comment", "123"],
        returncode=1,
        stdout="",
        stderr="HTTP 503 Service Unavailable",
    )
    mock_success = subprocess.CompletedProcess(
        args=["gh", "pr", "comment", "123"],
        returncode=0,
        stdout="https://github.com/org/repo/pull/123#issuecomment-1",
        stderr="",
    )
    with (
        patch("subprocess.run", side_effect=[mock_fail, mock_success]) as mock_run,
        patch("time.sleep") as mock_sleep,
    ):
        result = run_command(
            ["gh", "pr", "comment", "123"],
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )
        assert result.returncode == 0
        assert mock_run.call_count == 2
        mock_sleep.assert_called_once_with(0.1)


def test_run_command_retries_exhausted_raises_error() -> None:
    """run_command raises AuditCleanupError when transient retries are exhausted."""
    mock_fail = subprocess.CompletedProcess(
        args=["gh", "pr", "comment", "123"],
        returncode=1,
        stdout="",
        stderr="HTTP 429 Too Many Requests",
    )
    with (
        patch("subprocess.run", return_value=mock_fail) as mock_run,
        patch("time.sleep"),
    ):
        with pytest.raises(AuditCleanupError, match=r"(?s)Command failed.*429"):
            run_command(["gh", "pr", "comment", "123"], dry_run=False, max_retries=1)
        assert mock_run.call_count == 2


def test_run_command_handles_subprocess_error_retry_and_exhaustion() -> None:
    """run_command handles SubprocessError with retry and raises on exhaustion."""
    with (
        patch(
            "subprocess.run",
            side_effect=[subprocess.SubprocessError("timeout"), subprocess.SubprocessError("timeout")],
        ) as mock_run,
        patch("time.sleep") as mock_sleep,
    ):
        with pytest.raises(AuditCleanupError, match=r"(?s)Process execution error.*timeout"):
            run_command(["gh", "api", "status"], dry_run=False, max_retries=1, retry_delay=0.1)
        assert mock_run.call_count == 2
        mock_sleep.assert_called_once_with(0.1)


def test_run_command_handles_subprocess_error_retry_then_success() -> None:
    """run_command handles SubprocessError on first attempt and succeeds on retry."""
    mock_success = subprocess.CompletedProcess(
        args=["gh", "api", "status"],
        returncode=0,
        stdout="OK",
        stderr="",
    )
    with (
        patch(
            "subprocess.run",
            side_effect=[subprocess.SubprocessError("connection reset"), mock_success],
        ) as mock_run,
        patch("time.sleep") as mock_sleep,
    ):
        result = run_command(["gh", "api", "status"], dry_run=False, max_retries=1, retry_delay=0.2)
        assert result.returncode == 0
        assert result.stdout == "OK"
        assert mock_run.call_count == 2
        mock_sleep.assert_called_once_with(0.2)


def test_run_command_handles_subprocess_error_retry_without_delay() -> None:
    """run_command retries a subprocess error without sleeping when delay is zero."""
    mock_success = subprocess.CompletedProcess(
        args=["gh", "api", "status"],
        returncode=0,
        stdout="OK",
        stderr="",
    )
    with patch("subprocess.run", side_effect=[subprocess.SubprocessError("timeout"), mock_success]) as mock_run:
        result = run_command(["gh", "api", "status"], dry_run=False, max_retries=1)
        assert result.returncode == 0
        assert mock_run.call_count == 2


def test_run_command_negative_max_retries_raises_value_error() -> None:
    """run_command rejects a negative retry budget before attempting execution."""
    with pytest.raises(ValueError, match="max_retries cannot be negative"):
        run_command(["gh", "version"], max_retries=-1)


def test_run_command_negative_retry_delay_raises_value_error() -> None:
    """run_command rejects a negative retry delay before attempting execution."""
    with pytest.raises(ValueError, match="retry_delay must be finite and non-negative"):
        run_command(["gh", "version"], retry_delay=-0.1)


@pytest.mark.parametrize("value", [float("nan"), float("inf")])
def test_run_command_non_finite_retry_delay_raises_value_error(value: float) -> None:
    """run_command rejects NaN and infinite retry delays before attempting execution."""
    with pytest.raises(ValueError, match="retry_delay must be finite and non-negative"):
        run_command(["gh", "version"], retry_delay=value)


def test_run_command_os_error_wrapped_as_audit_cleanup_error() -> None:
    """run_command wraps an OSError (e.g. gh not found) as AuditCleanupError without retrying."""
    with patch("subprocess.run", side_effect=FileNotFoundError("No such file or directory: 'gh'")) as mock_run:
        with pytest.raises(AuditCleanupError, match="Command launch error"):
            run_command(["gh", "version"], dry_run=False, max_retries=3)
        assert mock_run.call_count == 1
