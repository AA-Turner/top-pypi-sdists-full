"""Tests for resolve_worktree_path."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.git import worktree_paths


class TestResolveWorktreePath:
    """Tests for resolve_worktree_path."""

    def test_missing_setting_defaults_to_wt_on_posix(self) -> None:
        """An absent config key creates worktrees under a sibling wt folder."""
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            side_effect=lambda *args, **kwargs: kwargs["default"],
        ):
            result = worktree_paths.resolve_worktree_path("/repos/rvn/gh/agentic-devtools", "DFLY-3305")

        assert result.repos_parent == "/repos/rvn/gh"
        assert result.worktree_folder == "wt"
        assert result.configured_parent_dir == "/repos/rvn/gh/wt"
        assert result.worktree_path == "/repos/rvn/gh/wt/DFLY-3305"

    def test_missing_setting_defaults_to_wt_on_windows(self) -> None:
        """Windows-style repository roots keep Windows separators in the resolved path."""
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            side_effect=lambda *args, **kwargs: kwargs["default"],
        ):
            result = worktree_paths.resolve_worktree_path(r"C:\repos\rvn\gh\agentic-devtools", "DFLY-3305")

        assert result.repos_parent == r"C:\repos\rvn\gh"
        assert result.worktree_folder == "wt"
        assert result.configured_parent_dir == r"C:\repos\rvn\gh\wt"
        assert result.worktree_path == r"C:\repos\rvn\gh\wt\DFLY-3305"

    @pytest.mark.parametrize("raw_value", [None, "", "   "])
    def test_null_and_blank_values_opt_out_to_direct_sibling(self, raw_value: str | None) -> None:
        """Null and blank config values preserve the legacy direct-sibling layout."""
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value=raw_value,
        ):
            result = worktree_paths.resolve_worktree_path("/repos/rvn/gh/agentic-devtools", "DFLY-3305")

        assert result.worktree_folder is None
        assert result.configured_parent_dir is None
        assert result.worktree_path == "/repos/rvn/gh/DFLY-3305"

    def test_non_empty_string_is_trimmed_and_used(self) -> None:
        """Surrounding whitespace is trimmed from a valid configured folder name."""
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value="  custom-wt  ",
        ):
            result = worktree_paths.resolve_worktree_path("/repos/rvn/gh/agentic-devtools", "#3305")

        assert result.normalized_issue_key == "3305"
        assert result.worktree_folder == "custom-wt"
        assert result.configured_parent_dir == "/repos/rvn/gh/custom-wt"
        assert result.worktree_path == "/repos/rvn/gh/custom-wt/3305"

    @pytest.mark.parametrize(
        ("raw_value", "message"),
        [
            (False, "booleans are not allowed"),
            (0, "got int"),
            (1.5, "got float"),
            ({}, "got dict"),
            (".", "'.' and '..' are not allowed"),
            ("..", "'.' and '..' are not allowed"),
            ("/wt", "absolute or drive-qualified paths"),
            (r"C:\wt", "absolute or drive-qualified paths"),
            (r"\\server\share", "absolute or drive-qualified paths"),
            ("wt/nested", "path separators are not allowed"),
            (r"wt\nested", "path separators are not allowed"),
            ("wt:", "invalid in Windows folder names"),
            ("con", "reserved Windows device name"),
            ("wt.", "must not end with '.'"),
        ],
    )
    def test_rejects_unsafe_configured_folder_values(self, raw_value: object, message: str) -> None:
        """Unsafe worktree-folder values fail validation before any path is used."""
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value=raw_value,
        ):
            with pytest.raises(ValueError, match=message):
                worktree_paths.resolve_worktree_path("/repos/rvn/gh/agentic-devtools", "DFLY-3305")

    def test_rejects_control_characters_in_folder_name(self) -> None:
        """Control characters are rejected before any path is constructed."""
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value="wt\0bad",
        ):
            with pytest.raises(ValueError, match="control characters"):
                worktree_paths.resolve_worktree_path("/repos/rvn/gh/agentic-devtools", "DFLY-3305")

    def test_rejects_empty_repository_root(self) -> None:
        """A caller must supply a repository root."""
        with pytest.raises(ValueError, match="Repository root is required"):
            worktree_paths.resolve_worktree_path("", "DFLY-3305")

    def test_rejects_folder_name_matching_main_checkout_basename(self, tmp_path) -> None:
        """A worktree_folder equal to the main checkout's basename would nest the worktree inside it."""
        git_root = tmp_path / "acme"
        git_root.mkdir()
        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value="acme",
        ):
            with pytest.raises(ValueError, match="resolves to the main checkout directory"):
                worktree_paths.resolve_worktree_path(str(git_root), "DFLY-3305")

    def test_rejects_configured_folder_symlinked_outside_repository_parent(self, tmp_path) -> None:
        """A configured folder symlink must not redirect worktrees outside the repository parent."""
        git_root = tmp_path / "acme"
        git_root.mkdir()
        outside = tmp_path.parent / f"{tmp_path.name}-outside"
        outside.mkdir()
        (tmp_path / "wt").symlink_to(outside, target_is_directory=True)

        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value="wt",
        ):
            with pytest.raises(ValueError, match="outside the repository parent"):
                worktree_paths.resolve_worktree_path(str(git_root), "DFLY-3305")

    @pytest.mark.parametrize(
        ("target_name", "message"),
        [
            ("acme", "resolves to the main checkout directory"),
            ("parent", "must resolve to a child"),
        ],
    )
    def test_rejects_configured_folder_symlinked_to_forbidden_location(
        self, tmp_path, target_name: str, message: str
    ) -> None:
        """A configured folder symlink must not collapse into the checkout or its parent."""
        git_root = tmp_path / "acme"
        git_root.mkdir()
        target = git_root if target_name == "acme" else tmp_path
        (tmp_path / "wt").symlink_to(target, target_is_directory=True)

        with patch(
            "agentic_devtools.cli.git.worktree_paths.get_effective_project_config_raw_value",
            return_value="wt",
        ):
            with pytest.raises(ValueError, match=message):
                worktree_paths.resolve_worktree_path(str(git_root), "DFLY-3305")
