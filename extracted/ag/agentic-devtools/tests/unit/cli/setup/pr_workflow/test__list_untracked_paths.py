"""Tests for _list_untracked_paths."""

from subprocess import CompletedProcess
from unittest.mock import patch

from agentic_devtools.cli.setup.pr_workflow import _list_untracked_paths


def _ok(stdout: str = "") -> CompletedProcess:
    return CompletedProcess(args=[], returncode=0, stdout=stdout, stderr="")


def _fail(stderr: str = "") -> CompletedProcess:
    return CompletedProcess(args=[], returncode=1, stdout="", stderr=stderr)


class TestListUntrackedPaths:
    """Tests for _list_untracked_paths."""

    def test_returns_untracked_paths_set(self) -> None:
        """Splits NUL-delimited git output into a de-duplicated set."""
        with patch(
            "agentic_devtools.cli.setup.pr_workflow.run_git",
            return_value=_ok("a.txt\0dir/b.txt\0a.txt\0"),
        ):
            assert _list_untracked_paths() == {"a.txt", "dir/b.txt"}

    def test_returns_none_on_git_failure(self) -> None:
        """Returns None when git ls-files fails."""
        with patch("agentic_devtools.cli.setup.pr_workflow.run_git", return_value=_fail("failed")):
            assert _list_untracked_paths() is None
