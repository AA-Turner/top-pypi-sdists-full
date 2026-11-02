"""Tests for _get_status_snapshot."""

from subprocess import CompletedProcess
from unittest.mock import patch

from agentic_devtools.cli.setup.pr_workflow import _get_status_snapshot


def _ok(stdout: str = "") -> CompletedProcess:
    return CompletedProcess(args=[], returncode=0, stdout=stdout, stderr="")


def _fail(stderr: str = "") -> CompletedProcess:
    return CompletedProcess(args=[], returncode=1, stdout="", stderr=stderr)


class TestGetStatusSnapshot:
    """Tests for _get_status_snapshot."""

    def test_returns_porcelain_snapshot_on_success(self) -> None:
        """Returns the raw porcelain snapshot string when git succeeds."""
        with patch("agentic_devtools.cli.setup.pr_workflow.run_git", return_value=_ok(" M a.py\0?? b.txt\0")):
            assert _get_status_snapshot() == " M a.py\0?? b.txt\0"

    def test_returns_none_on_git_failure(self) -> None:
        """Returns None when git status probe fails."""
        with patch("agentic_devtools.cli.setup.pr_workflow.run_git", return_value=_fail("failed")):
            assert _get_status_snapshot() is None
