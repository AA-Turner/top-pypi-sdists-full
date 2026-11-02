"""Tests for _stage_retro_spec in retro_spec/commands.py."""

from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.retro_spec.commands import _stage_retro_spec

_MOD = "agentic_devtools.cli.speckit.retro_spec.commands"


class TestStageRetroSpec:
    """Tests for the _stage_retro_spec helper."""

    def test_requires_repository_root(self, tmp_path: Path) -> None:
        """Staging fails clearly when the repository root cannot be resolved."""
        with patch(f"{_MOD}._get_git_root", return_value=None):
            with pytest.raises(RuntimeError, match="repository root"):
                _stage_retro_spec([tmp_path / "spec.md"])

    def test_rejects_paths_outside_repository(self, tmp_path: Path) -> None:
        """Generated files outside the repository cannot be staged."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with patch(f"{_MOD}._get_git_root", return_value=repo_root):
            with pytest.raises(RuntimeError, match="inside the repository"):
                _stage_retro_spec([tmp_path / "spec.md"])

    def test_reports_git_failure(self, tmp_path: Path) -> None:
        """Git staging failures include the provider error."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = SimpleNamespace(returncode=1, stderr="permission denied")
        with (
            patch(f"{_MOD}._get_git_root", return_value=repo_root),
            patch(f"{_MOD}.subprocess.run", return_value=result) as run,
        ):
            with pytest.raises(RuntimeError, match="permission denied"):
                _stage_retro_spec([repo_root / "spec.md"])

        assert run.call_args.kwargs["shell"] is False

    def test_succeeds(self, tmp_path: Path) -> None:
        """Generated files are staged relative to the repository root."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        spec_file = repo_root / "specs" / "spec.md"
        hierarchy_file = repo_root / "specs" / "100" / "hierarchy.yml"
        with (
            patch(f"{_MOD}._get_git_root", return_value=repo_root),
            patch(
                f"{_MOD}.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, "", ""),
            ) as run,
        ):
            _stage_retro_spec([spec_file, hierarchy_file])

        assert run.call_args.args[0] == ["git", "add", "--", "specs/spec.md", "specs/100/hierarchy.yml"]
