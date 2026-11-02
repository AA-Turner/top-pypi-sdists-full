"""Tests for get_effective_project_config_raw_value()."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.config.project_config import get_effective_project_config_raw_value


class TestGetEffectiveProjectConfigRawValue:
    """Tests for get_effective_project_config_raw_value function."""

    def test_returns_raw_boolean_without_stringifying(self) -> None:
        """Boolean config values remain booleans for typed validation."""
        with patch(
            "agentic_devtools.cli.config.project_config.load_effective_project_config",
            return_value={"worktree_folder": False},
        ):
            assert get_effective_project_config_raw_value("worktree_folder") is False

    def test_returns_raw_null_without_replacing_it(self) -> None:
        """Explicit JSON null remains None."""
        with patch(
            "agentic_devtools.cli.config.project_config.load_effective_project_config",
            return_value={"worktree_folder": None},
        ):
            assert get_effective_project_config_raw_value("worktree_folder") is None

    def test_returns_default_for_missing_key(self) -> None:
        """Callers can distinguish an absent key from an explicit null."""
        missing = object()
        with patch(
            "agentic_devtools.cli.config.project_config.load_effective_project_config",
            return_value={},
        ):
            assert get_effective_project_config_raw_value("worktree_folder", default=missing) is missing

    def test_forwards_git_root_to_effective_config_loader(self) -> None:
        """The typed accessor uses the caller-supplied repository root."""
        git_root = Path("/repo/root")
        with patch(
            "agentic_devtools.cli.config.project_config.load_effective_project_config",
            return_value={},
        ) as mock_load:
            get_effective_project_config_raw_value("worktree_folder", git_root=git_root)

        mock_load.assert_called_once_with(git_root=git_root)
