"""Tests for ``get_repo_root``."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import get_repo_root


class TestGetRepoRoot:
    """get_repo_root resolves via .specify walk, then git, then cwd."""

    def test_returns_specify_parent_when_specify_dir_exists_in_cwd(self, tmp_path: Path) -> None:
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()
        with patch("agentic_devtools.cli.speckit.scaffold_common.Path.cwd", return_value=tmp_path):
            with patch.dict(os.environ, {"SPECIFY_INIT_DIR": ""}, clear=False):
                result = get_repo_root()
        assert result == tmp_path

    def test_returns_ancestor_specify_parent_when_nested(self, tmp_path: Path) -> None:
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()
        nested = tmp_path / "sub" / "deep"
        nested.mkdir(parents=True)
        with patch("agentic_devtools.cli.speckit.scaffold_common.Path.cwd", return_value=nested):
            with patch.dict(os.environ, {"SPECIFY_INIT_DIR": ""}, clear=False):
                result = get_repo_root()
        assert result == tmp_path

    def test_falls_back_to_git_toplevel_when_no_specify_dir(self, tmp_path: Path) -> None:
        completed = MagicMock(returncode=0, stdout="/repo/root\n")
        with patch("subprocess.run", return_value=completed) as mock_run:
            with patch(
                "agentic_devtools.cli.speckit.scaffold_common._find_specify_project_root",
                return_value=None,
            ):
                result = get_repo_root()

        assert result == Path("/repo/root")
        mock_run.assert_called_once_with(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_falls_back_to_cwd_when_git_returns_nonzero(self) -> None:
        completed = MagicMock(returncode=1, stdout="")
        with patch("subprocess.run", return_value=completed):
            with patch(
                "agentic_devtools.cli.speckit.scaffold_common._find_specify_project_root",
                return_value=None,
            ):
                result = get_repo_root()

        assert result == Path.cwd()

    def test_falls_back_to_cwd_when_git_missing(self) -> None:
        with patch("subprocess.run", side_effect=FileNotFoundError("git not found")):
            with patch(
                "agentic_devtools.cli.speckit.scaffold_common._find_specify_project_root",
                return_value=None,
            ):
                result = get_repo_root()

        assert result == Path.cwd()

    def test_falls_back_to_cwd_on_os_error(self) -> None:
        with patch("subprocess.run", side_effect=OSError("boom")):
            with patch(
                "agentic_devtools.cli.speckit.scaffold_common._find_specify_project_root",
                return_value=None,
            ):
                result = get_repo_root()

        assert result == Path.cwd()

    def test_specify_init_dir_env_var_overrides_cwd_search(self, tmp_path: Path) -> None:
        project_root = tmp_path / "project"
        (project_root / ".specify").mkdir(parents=True)
        with patch.dict(os.environ, {"SPECIFY_INIT_DIR": str(project_root)}):
            result = get_repo_root()
        assert result == project_root

    @pytest.mark.usefixtures("tmp_path")
    def test_git_toplevel_preferred_over_outer_repo_when_no_specify_dir(self, tmp_path: Path) -> None:
        nested = tmp_path / "inner"
        nested.mkdir()
        completed = MagicMock(returncode=0, stdout=f"{nested}\n")
        with patch("subprocess.run", return_value=completed):
            with patch(
                "agentic_devtools.cli.speckit.scaffold_common._find_specify_project_root",
                return_value=None,
            ):
                result = get_repo_root()
        assert result == nested
