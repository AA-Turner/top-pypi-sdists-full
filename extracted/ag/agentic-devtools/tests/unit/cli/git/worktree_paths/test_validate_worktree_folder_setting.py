"""Tests for validate_worktree_folder_setting."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.git import worktree_paths


class TestValidateWorktreeFolderSetting:
    """Tests for validate_worktree_folder_setting."""

    def test_rejects_empty_repository_root(self) -> None:
        """A caller must supply a repository root."""
        with pytest.raises(ValueError, match="Repository root is required"):
            worktree_paths.validate_worktree_folder_setting("")

    def test_returns_default_folder_when_unset(self) -> None:
        """An absent config key resolves to the default sibling wt folder."""
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            side_effect=lambda *args, **kwargs: kwargs["default"],
        ):
            assert worktree_paths.validate_worktree_folder_setting("/repos/rvn/gh/agentic-devtools") == "wt"

    def test_returns_none_when_opted_out(self) -> None:
        """A null config value opts out to the legacy direct-sibling layout."""
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value=None,
        ):
            assert worktree_paths.validate_worktree_folder_setting("/repos/rvn/gh/agentic-devtools") is None

    def test_rejects_unsafe_configured_folder_value(self) -> None:
        """Type/shape validation still runs without an issue key."""
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value=False,
        ):
            with pytest.raises(ValueError, match="booleans are not allowed"):
                worktree_paths.validate_worktree_folder_setting("/repos/rvn/gh/agentic-devtools")

    def test_rejects_folder_name_matching_main_checkout_basename(self, tmp_path) -> None:
        """A worktree_folder equal to the main checkout's basename would nest the worktree inside it."""
        git_root = tmp_path / "acme"
        git_root.mkdir()
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value="acme",
        ):
            with pytest.raises(ValueError, match="resolves to the main checkout directory"):
                worktree_paths.validate_worktree_folder_setting(str(git_root))
