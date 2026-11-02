"""Tests for agentic_devtools.orchestration.nodes.commit._has_pending_changes."""

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.nodes import commit as commit_mod

_MOD = "agentic_devtools.orchestration.nodes.commit"


def _proc(stdout: str = "", returncode: int = 0, stderr: str = ""):
    return MagicMock(returncode=returncode, stdout=stdout, stderr=stderr)


class TestHasPendingChanges:
    def test_returns_true_when_status_has_output(self):
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout=" M file\n")):
            assert commit_mod._has_pending_changes("/wt") is True

    def test_returns_false_when_status_is_empty(self):
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout="")):
            assert commit_mod._has_pending_changes("/wt") is False
