"""Tests for agentic_devtools.orchestration.nodes.commit._has_staged_changes."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.git.core import GitError
from agentic_devtools.orchestration.nodes import commit as commit_mod

_MOD = "agentic_devtools.orchestration.nodes.commit"


def _proc(stdout: str = "", returncode: int = 0, stderr: str = ""):
    return MagicMock(returncode=returncode, stdout=stdout, stderr=stderr)


class TestHasStagedChanges:
    def test_returns_true_for_exit_code_one(self):
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=1)):
            assert commit_mod._has_staged_changes("/wt") is True

    def test_returns_false_for_exit_code_zero(self):
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=0)):
            assert commit_mod._has_staged_changes("/wt") is False

    def test_raises_for_error_exit_code(self):
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=128, stderr="corrupt index")):
            with pytest.raises(GitError):
                commit_mod._has_staged_changes("/wt")
