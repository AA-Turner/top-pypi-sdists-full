"""Tests for preflight_check in nest/execution.py."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.nest.execution import preflight_check


class TestPreflightCheck:
    """Tests for the preflight_check function."""

    def test_passes_when_git_state_is_clean(self, tmp_path: Path) -> None:
        """Test that clean staged, unstaged, and untracked checks pass."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),  # diff --cached
            subprocess.CompletedProcess([], 0, "", ""),  # diff
            subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),  # rev-parse
            subprocess.CompletedProcess([], 0, "", ""),  # ls-files specs/
        ]

        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ) as mock_run:
            preflight_check(tmp_path / "specs")

        assert mock_run.call_count == 4

    def test_uses_relative_pathspec_for_git_ls_files(self, tmp_path: Path) -> None:
        """Test that git ls-files receives a repo-relative path, not an absolute path."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),  # diff --cached
            subprocess.CompletedProcess([], 0, "", ""),  # diff
            subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),  # rev-parse
            subprocess.CompletedProcess([], 0, "", ""),  # ls-files
        ]

        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ) as mock_run:
            preflight_check(tmp_path / "specs")

        ls_files_call = mock_run.call_args_list[3]
        path_arg = ls_files_call[0][0][-1]
        assert path_arg == "specs"

    def test_exits_when_index_has_staged_changes(self, tmp_path: Path) -> None:
        """Test that staged changes abort the migration."""
        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", ""),
        ):
            with pytest.raises(SystemExit, match="1"):
                preflight_check(tmp_path / "specs")

    def test_exits_when_git_diff_cached_fails(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that a git diff --cached command failure (e.g. not a git repo) surfaces stderr."""
        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            return_value=subprocess.CompletedProcess([], 128, "", "fatal: not a git repository"),
        ):
            with pytest.raises(SystemExit, match="1"):
                preflight_check(tmp_path / "specs")
        captured = capsys.readouterr()
        assert "git diff --cached failed" in captured.err
        assert "fatal: not a git repository" in captured.err

    def test_exits_when_working_tree_has_unstaged_changes(self, tmp_path: Path) -> None:
        """Test that unstaged changes abort the migration."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 1, "", ""),
        ]

        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            with pytest.raises(SystemExit, match="1"):
                preflight_check(tmp_path / "specs")

    def test_exits_when_git_diff_fails(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that a git diff command failure (e.g. not a git repo) surfaces stderr."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 128, "", "fatal: not a git repository"),
        ]

        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            with pytest.raises(SystemExit, match="1"):
                preflight_check(tmp_path / "specs")
        captured = capsys.readouterr()
        assert "git diff failed" in captured.err
        assert "fatal: not a git repository" in captured.err

    def test_exits_when_git_ls_files_fails(self, tmp_path: Path) -> None:
        """Test that a git ls-files error aborts the migration rather than silently passing."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),
            subprocess.CompletedProcess([], 1, "", "fatal: '/abs/path' is outside repository"),
        ]

        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            with pytest.raises(SystemExit, match="1"):
                preflight_check(tmp_path / "specs")

    def test_exits_when_specs_has_untracked_files(self, tmp_path: Path) -> None:
        """Test that untracked files under specs abort the migration."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),
            subprocess.CompletedProcess([], 0, "specs/new-file.md\n", ""),
        ]

        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            with pytest.raises(SystemExit, match="1"):
                preflight_check(tmp_path / "specs")

    def test_exits_when_git_root_cannot_be_resolved(self, tmp_path: Path) -> None:
        """Test that a rev-parse failure aborts before running git ls-files."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 1, "", "fatal: not a git repository"),
        ]

        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            with pytest.raises(SystemExit, match="1"):
                preflight_check(tmp_path / "specs")

    def test_exits_when_specs_path_is_outside_repo_root(self, tmp_path: Path) -> None:
        """Test that preflight aborts when specs_root is outside the repository."""
        repo_root = tmp_path / "repo"
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, f"{repo_root}\n", ""),
        ]

        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            with pytest.raises(SystemExit, match="1"):
                preflight_check(tmp_path / "outside" / "specs")
