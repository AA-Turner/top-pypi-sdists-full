"""Tests for _validate_staged_files in retro_spec/commands.py."""

from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.retro_spec.commands import _validate_staged_files

_MOD = "agentic_devtools.cli.speckit.retro_spec.commands"


class TestValidateStagedFiles:
    """Tests for the _validate_staged_files helper."""

    def test_requires_repository_root(self, tmp_path: Path) -> None:
        """Validation fails clearly when the repository root cannot be resolved."""
        with patch(f"{_MOD}._get_git_root", return_value=None):
            with pytest.raises(RuntimeError, match="repository root"):
                _validate_staged_files([tmp_path / "spec.md"])

    def test_reports_git_diff_failure(self, tmp_path: Path) -> None:
        """Git diff --cached failures are surfaced as a RuntimeError."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = SimpleNamespace(returncode=1, stderr="not a git repository", stdout="")
        with (
            patch(f"{_MOD}._get_git_root", return_value=repo_root),
            patch(f"{_MOD}.subprocess.run", return_value=result),
        ):
            with pytest.raises(RuntimeError, match="git diff --cached failed"):
                _validate_staged_files([repo_root / "spec.md"])

    def test_raises_when_unexpected_files_are_staged(self, tmp_path: Path) -> None:
        """Unexpected staged files abort the commit with an informative message."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        expected = repo_root / "specs" / "42" / "spec.md"
        unexpected = "some/other/file.py"
        staged_output = f"specs/42/spec.md\n{unexpected}\n"
        with (
            patch(f"{_MOD}._get_git_root", return_value=repo_root),
            patch(
                f"{_MOD}.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, staged_output, ""),
            ),
        ):
            with pytest.raises(RuntimeError, match="Unexpected files are staged"):
                _validate_staged_files([expected])

    def test_passes_when_only_expected_files_are_staged(self, tmp_path: Path) -> None:
        """No exception when the index contains exactly the generated files."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        spec = repo_root / "specs" / "42" / "spec.md"
        staged_output = "specs/42/spec.md\n"
        with (
            patch(f"{_MOD}._get_git_root", return_value=repo_root),
            patch(
                f"{_MOD}.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, staged_output, ""),
            ),
        ):
            _validate_staged_files([spec])  # Should not raise

    def test_passes_when_index_is_empty(self, tmp_path: Path) -> None:
        """No exception when no files are staged (empty index)."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        spec = repo_root / "specs" / "42" / "spec.md"
        with (
            patch(f"{_MOD}._get_git_root", return_value=repo_root),
            patch(
                f"{_MOD}.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, "", ""),
            ),
        ):
            _validate_staged_files([spec])  # Should not raise — expected file is not staged
