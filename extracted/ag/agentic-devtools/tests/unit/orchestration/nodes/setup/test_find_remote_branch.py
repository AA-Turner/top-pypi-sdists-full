"""Tests for agentic_devtools.orchestration.nodes.setup._find_remote_branch."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.git.core import GitError
from agentic_devtools.orchestration.nodes import setup as setup_mod

_MOD = "agentic_devtools.orchestration.nodes.setup"


def _proc(stdout: str = "", returncode: int = 0):
    return MagicMock(returncode=returncode, stdout=stdout, stderr="")


class TestFindRemoteBranch:
    def test_matches_segment(self):
        stdout = "sha1\trefs/heads/main\nsha2\trefs/heads/feature/42/impl\n"
        with patch(f"{_MOD}.run_git_safe", return_value=_proc(stdout=stdout)):
            assert setup_mod._find_remote_branch("/r", "42") == "feature/42/impl"

    def test_returns_none_when_no_match(self):
        stdout = "sha1\trefs/heads/main\n"
        with patch(f"{_MOD}.run_git_safe", return_value=_proc(stdout=stdout)):
            assert setup_mod._find_remote_branch("/r", "42") is None

    def test_ignores_malformed_and_non_heads_lines(self):
        stdout = "garbage\nsha\trefs/tags/v1\nsha2\trefs/heads/feature/42/x\n"
        with patch(f"{_MOD}.run_git_safe", return_value=_proc(stdout=stdout)):
            assert setup_mod._find_remote_branch("/r", "42") == "feature/42/x"

    def test_git_error_propagates(self):
        with patch(f"{_MOD}.run_git_safe", side_effect=GitError(1, "x", ["ls-remote"])):
            with pytest.raises(GitError):
                setup_mod._find_remote_branch("/r", "42")
