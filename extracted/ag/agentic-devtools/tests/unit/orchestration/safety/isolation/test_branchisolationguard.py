"""Tests for BranchIsolationGuard — FR-007."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.safety.exceptions import BranchIsolationError
from agentic_devtools.orchestration.safety.isolation import BranchIsolationGuard


class TestBranchIsolationGuard:
    """Tests for branch isolation enforcement."""

    def test_non_git_tool_passes(self) -> None:
        guard = BranchIsolationGuard(["main", "master"])
        # Non-git tools should not trigger branch check
        guard.check("filesystem_read_file")

    @patch("subprocess.run")
    def test_protected_branch_raises(self, mock_run) -> None:
        mock_run.return_value = type("Result", (), {"returncode": 0, "stdout": "main\n"})()
        guard = BranchIsolationGuard(["main", "master"])
        with pytest.raises(BranchIsolationError, match="main"):
            guard.check("git_push")

    @patch("subprocess.run")
    def test_unprotected_branch_passes(self, mock_run) -> None:
        mock_run.return_value = type("Result", (), {"returncode": 0, "stdout": "feature/123\n"})()
        guard = BranchIsolationGuard(["main", "master"])
        guard.check("git_push")

    @patch("subprocess.run")
    def test_glob_pattern_matching(self, mock_run) -> None:
        mock_run.return_value = type("Result", (), {"returncode": 0, "stdout": "release/v1.0\n"})()
        guard = BranchIsolationGuard(["main", "release/*"])
        with pytest.raises(BranchIsolationError, match="release/v1.0"):
            guard.check("git_save_work")

    @patch("subprocess.run")
    def test_detached_head_raises(self, mock_run) -> None:
        mock_run.return_value = type("Result", (), {"returncode": 0, "stdout": "HEAD\n"})()
        guard = BranchIsolationGuard(["main"])
        with pytest.raises(BranchIsolationError, match="detached HEAD"):
            guard.check("git_push")

    @patch("subprocess.run")
    def test_git_error_raises(self, mock_run) -> None:
        mock_run.return_value = type("Result", (), {"returncode": 128, "stdout": "", "stderr": "not a git repo"})()
        guard = BranchIsolationGuard(["main"])
        with pytest.raises(BranchIsolationError):
            guard.check("git_push")

    def test_protected_branches_property(self) -> None:
        guard = BranchIsolationGuard(["main", "develop"])
        assert guard.protected_branches == ["main", "develop"]
