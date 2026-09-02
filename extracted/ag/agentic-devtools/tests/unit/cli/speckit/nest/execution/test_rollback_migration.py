"""Tests for rollback_migration in nest/execution.py."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import call, patch

import pytest

from agentic_devtools.cli.speckit.nest.execution import rollback_migration


class TestRollbackMigration:
    """Tests for the rollback_migration function."""

    def test_resets_head_and_cleans_specs_directory(self, tmp_path: Path) -> None:
        """Test that rollback performs reset and clean using a repo-relative pathspec."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),
            subprocess.CompletedProcess([], 0, "", ""),
        ]
        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ) as mock_run:
            result = rollback_migration("abc123", tmp_path / "specs")

        assert result is True
        assert mock_run.call_args_list == [
            call(["git", "reset", "--hard", "abc123"], capture_output=True, text=True, shell=False),
            call(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, shell=False),
            call(["git", "clean", "-fd", "--", "specs"], capture_output=True, text=True, shell=False),
        ]

    def test_uses_relative_pathspec_for_git_clean(self, tmp_path: Path) -> None:
        """Test that rollback passes a repo-relative path, not an absolute path, to git clean."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),
            subprocess.CompletedProcess([], 0, "", ""),
        ]
        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ) as mock_run:
            rollback_migration("abc123", tmp_path / "specs")

        clean_call = mock_run.call_args_list[2]
        path_arg = clean_call[0][0][-1]
        assert path_arg == "specs"

    def test_warns_when_git_reset_fails(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that a failing git reset prints a warning but continues to run git clean."""
        results = [
            subprocess.CompletedProcess([], 1, "", "fatal: bad revision"),
            subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),
            subprocess.CompletedProcess([], 0, "", ""),
        ]
        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            result = rollback_migration("abc123", tmp_path / "specs")

        captured = capsys.readouterr()
        assert result is False
        assert "Warning" in captured.err
        assert "git reset" in captured.err

    def test_warns_when_git_clean_fails(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that a failing git clean prints a warning without masking the reset result."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),
            subprocess.CompletedProcess([], 1, "", "error: pathspec is outside repository"),
        ]
        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            result = rollback_migration("abc123", tmp_path / "specs")

        captured = capsys.readouterr()
        assert result is False
        assert "Warning" in captured.err
        assert "git clean" in captured.err

    def test_warns_when_repo_root_resolution_fails(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that rollback warns and returns False when repo root lookup fails."""
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 1, "", "fatal: not a git repository"),
        ]
        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            result = rollback_migration("abc123", tmp_path / "specs")

        captured = capsys.readouterr()
        assert result is False
        assert "Warning" in captured.err
        assert "could not compute specs path for git clean during rollback" in captured.err

    def test_warns_when_specs_path_is_outside_repo_root(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that rollback warns and returns False when specs_root is outside the repo."""
        repo_root = tmp_path / "repo"
        results = [
            subprocess.CompletedProcess([], 0, "", ""),
            subprocess.CompletedProcess([], 0, f"{repo_root}\n", ""),
        ]
        with patch(
            "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
            side_effect=results,
        ):
            result = rollback_migration("abc123", tmp_path / "outside" / "specs")

        captured = capsys.readouterr()
        assert result is False
        assert "Warning" in captured.err
        assert "outside the repository root" in captured.err
