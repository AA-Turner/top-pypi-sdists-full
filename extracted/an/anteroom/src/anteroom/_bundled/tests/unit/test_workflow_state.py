"""Tests for workflow_state helpers (#1236)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from anteroom.services.workflow_state import (
    git_common_dir,
    issue_state_dir,
    read_issue_state,
)


class TestGitCommonDir:
    def test_returns_absolute_path(self, tmp_path: Path) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = str(tmp_path / ".git")
        with patch("anteroom.services.workflow_state.subprocess.run", return_value=mock_result) as mock_run:
            result = git_common_dir(tmp_path)
        assert result == tmp_path / ".git"
        mock_run.assert_called_once()

    def test_resolves_relative_path(self, tmp_path: Path) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ".git"
        with patch("anteroom.services.workflow_state.subprocess.run", return_value=mock_result):
            result = git_common_dir(tmp_path)
        assert result == (tmp_path / ".git").resolve()

    def test_raises_on_failure(self, tmp_path: Path) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "not a git repo"
        with patch("anteroom.services.workflow_state.subprocess.run", return_value=mock_result):
            with pytest.raises(ValueError, match="git rev-parse failed"):
                git_common_dir(tmp_path)

    def test_raises_when_git_not_found(self, tmp_path: Path) -> None:
        with patch("anteroom.services.workflow_state.subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(ValueError, match="git is not available"):
                git_common_dir(tmp_path)


class TestIssueStateDir:
    def test_returns_expected_path(self, tmp_path: Path) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = str(tmp_path / ".git")
        with patch("anteroom.services.workflow_state.subprocess.run", return_value=mock_result):
            result = issue_state_dir(tmp_path, 42)
        assert result == tmp_path / ".git" / "anteroom-workflows" / "issue-42"


class TestReadIssueState:
    def test_returns_none_when_missing(self, tmp_path: Path) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = str(tmp_path / ".git")
        with patch("anteroom.services.workflow_state.subprocess.run", return_value=mock_result):
            result = read_issue_state(tmp_path, 99)
        assert result is None

    def test_reads_valid_state(self, tmp_path: Path) -> None:
        git_dir = tmp_path / ".git"
        state_dir = git_dir / "anteroom-workflows" / "issue-42"
        state_dir.mkdir(parents=True)
        state = {"worktree_path": "/tmp/wt", "branch": "issue-42-fix"}
        (state_dir / "state.json").write_text(json.dumps(state))

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = str(git_dir)
        with patch("anteroom.services.workflow_state.subprocess.run", return_value=mock_result):
            result = read_issue_state(tmp_path, 42)
        assert result == state

    def test_returns_none_on_invalid_json(self, tmp_path: Path) -> None:
        git_dir = tmp_path / ".git"
        state_dir = git_dir / "anteroom-workflows" / "issue-42"
        state_dir.mkdir(parents=True)
        (state_dir / "state.json").write_text("not json{{{")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = str(git_dir)
        with patch("anteroom.services.workflow_state.subprocess.run", return_value=mock_result):
            result = read_issue_state(tmp_path, 42)
        assert result is None
