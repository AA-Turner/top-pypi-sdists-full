"""Tests for setup_git_hooks."""

from __future__ import annotations

import json
import subprocess as _real_subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.setup.git_hooks_policy import (
    HOOKS_DISABLED_MESSAGE,
    PRESERVED_MESSAGE_PREFIX,
    PRESERVED_MESSAGE_SUFFIX,
)
from agentic_devtools.cli.setup.script_generators.required_setup import setup_git_hooks

_MOD = "agentic_devtools.cli.setup.script_generators.required_setup"

_SUCCESS_MESSAGE = "  ✓ core.hooksPath set to '.githooks'"


def _write_project_config(git_root: Path, payload: dict[str, object]) -> None:
    config_path = git_root / ".agdt" / "config" / "project.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(payload), encoding="utf-8")


class TestSetupGitHooks:
    """Tests for setup_git_hooks."""

    def test_returns_none_when_not_in_git_repo(self):
        """Returns None outside a git repository."""
        with patch(
            f"{_MOD}.subprocess.run",
            side_effect=_real_subprocess.CalledProcessError(128, "git"),
        ):
            result = setup_git_hooks()
            assert result is None

    def test_sets_hooks_path(self, tmp_path):
        """Sets core.hooksPath when in a git repo and creates .githooks."""
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),  # rev-parse --git-dir
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),  # show-toplevel
                MagicMock(returncode=1, stdout=""),  # config --get (not set)
                MagicMock(returncode=0),  # config set
            ]
        )
        with patch(f"{_MOD}.subprocess.run", mock_run):
            result = setup_git_hooks()

        assert result == _SUCCESS_MESSAGE
        assert (tmp_path / ".githooks").is_dir()

    def test_preserves_empty_hooks_path(self, tmp_path):
        """An explicitly-configured empty core.hooksPath is preserved (returncode=0, stdout='')."""
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),  # rev-parse --git-dir
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),  # show-toplevel
                MagicMock(returncode=0, stdout=""),  # config --get (empty but set)
            ]
        )
        with patch(f"{_MOD}.subprocess.run", mock_run):
            result = setup_git_hooks()

        assert result is not None
        assert result.startswith(PRESERVED_MESSAGE_PREFIX)
        assert mock_run.call_count == 3
        assert not (tmp_path / ".githooks").exists()

    def test_preserves_foreign_hooks_path(self, tmp_path):
        """A foreign core.hooksPath is preserved: no write, no directory created."""
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),  # rev-parse --git-dir
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),  # show-toplevel
                MagicMock(returncode=0, stdout=".husky/_\n"),  # config --get
            ]
        )
        with patch(f"{_MOD}.subprocess.run", mock_run):
            result = setup_git_hooks()

        assert result is not None
        assert result.startswith(PRESERVED_MESSAGE_PREFIX)
        assert "'.husky/_'" in result
        assert result.endswith(PRESERVED_MESSAGE_SUFFIX)
        assert "Overwriting" not in result
        assert mock_run.call_count == 3
        assert not (tmp_path / ".githooks").exists()

    def test_no_warning_when_already_githooks(self, tmp_path):
        """Re-asserts the value idempotently when already .githooks."""
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),
                MagicMock(returncode=0, stdout=".githooks\n"),
                MagicMock(returncode=0),  # config set (idempotent re-assert)
            ]
        )
        with patch(f"{_MOD}.subprocess.run", mock_run):
            result = setup_git_hooks()

        assert result == _SUCCESS_MESSAGE
        assert mock_run.call_count == 4
        assert (tmp_path / ".githooks").is_dir()

    def test_skips_when_disabled_by_project_config(self, tmp_path):
        """manage_git_hooks=false short-circuits before core.hooksPath is read."""
        _write_project_config(tmp_path, {"manage_git_hooks": False})
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),
            ]
        )
        with patch(f"{_MOD}.subprocess.run", mock_run):
            result = setup_git_hooks()

        assert result == HOOKS_DISABLED_MESSAGE
        assert mock_run.call_count == 2
        assert not (tmp_path / ".githooks").exists()

    def test_returns_none_when_git_not_found(self):
        """Returns None when git binary is not found."""
        with patch(f"{_MOD}.subprocess.run", side_effect=FileNotFoundError("git not found")):
            assert setup_git_hooks() is None

    def test_returns_none_when_config_get_raises_file_not_found(self, tmp_path):
        """Returns None when git config --get raises FileNotFoundError."""
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),  # rev-parse --git-dir
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),  # show-toplevel
                FileNotFoundError("git not found"),  # config --get
            ]
        )
        with patch(f"{_MOD}.subprocess.run", mock_run):
            assert setup_git_hooks() is None

    def test_returns_error_when_config_set_fails(self, tmp_path):
        """Returns error message when git config set raises CalledProcessError."""
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),  # rev-parse --git-dir
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),  # show-toplevel
                MagicMock(returncode=1, stdout=""),  # config --get (not set)
                _real_subprocess.CalledProcessError(1, "git config"),  # config set
            ]
        )
        with patch(f"{_MOD}.subprocess.run", mock_run):
            result = setup_git_hooks()
            assert result is not None
            assert "Failed to set core.hooksPath" in result

    def test_handles_show_toplevel_failure(self):
        """Handles CalledProcessError on git rev-parse --show-toplevel."""
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),  # rev-parse --git-dir
                _real_subprocess.CalledProcessError(1, "git rev-parse"),  # show-toplevel
                MagicMock(returncode=1, stdout=""),  # config --get (not set)
                MagicMock(returncode=0),  # config set
            ]
        )
        with patch(f"{_MOD}.subprocess.run", mock_run):
            result = setup_git_hooks()

        assert result == _SUCCESS_MESSAGE

    def test_preserves_foreign_path_without_a_repo_root(self):
        """An unresolvable root makes the toggle unreadable but still preserves foreign paths."""
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),  # rev-parse --git-dir
                _real_subprocess.CalledProcessError(1, "git rev-parse"),  # show-toplevel
                MagicMock(returncode=0, stdout=".husky/_\n"),  # config --get
            ]
        )
        with patch(f"{_MOD}.subprocess.run", mock_run):
            result = setup_git_hooks()

        assert result is not None
        assert result.startswith(PRESERVED_MESSAGE_PREFIX)
        assert mock_run.call_count == 3

    def test_handles_mkdir_failure(self, tmp_path):
        """A failing .githooks mkdir does not change the success message."""
        mock_run = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout=".git\n"),
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),
                MagicMock(returncode=1, stdout=""),
                MagicMock(returncode=0),
            ]
        )
        with (
            patch(f"{_MOD}.subprocess.run", mock_run),
            patch(f"{_MOD}.Path.mkdir", side_effect=OSError("read-only")),
        ):
            result = setup_git_hooks()

        assert result == _SUCCESS_MESSAGE
