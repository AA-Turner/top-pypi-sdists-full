"""Tests for resolve_worktree_path_from_parent."""

import pytest

from agentic_devtools.cli.git import worktree_paths


class TestResolveWorktreePathFromParent:
    """Tests for resolve_worktree_path_from_parent."""

    def test_resolve_from_parent_uses_supplied_git_root_for_config(self, tmp_path) -> None:
        """The parent-based resolver reads project config from the supplied main repo root."""
        git_root = tmp_path / "agentic-devtools"
        git_root.mkdir()
        config_dir = git_root / ".agdt" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "project.json").write_text('{"worktree_folder": "team-wt"}\n', encoding="utf-8")

        result = worktree_paths.resolve_worktree_path_from_parent(tmp_path, "DFLY-3305", git_root=git_root)

        assert result.repos_parent == str(tmp_path)
        assert result.configured_parent_dir == str(tmp_path / "team-wt")
        assert result.worktree_path == str(tmp_path / "team-wt" / "DFLY-3305")

    def test_rejects_empty_parent_directory(self) -> None:
        """A caller must supply a repository parent directory."""
        with pytest.raises(ValueError, match="Repository parent directory is required"):
            worktree_paths.resolve_worktree_path_from_parent("", "DFLY-3305")

    def test_skips_nesting_check_when_git_root_not_supplied(self, tmp_path) -> None:
        """Without a git_root, the nesting-collision check cannot run and is skipped."""
        with pytest.MonkeyPatch().context() as monkeypatch:
            monkeypatch.setattr(
                worktree_paths,
                "get_effective_project_config_raw_value",
                lambda *args, **kwargs: "acme",
            )
            result = worktree_paths.resolve_worktree_path_from_parent(tmp_path, "DFLY-3305")

        assert result.configured_parent_dir == str(tmp_path / "acme")

    def test_rejects_folder_name_matching_git_root_case_insensitively_on_windows(self) -> None:
        """A Windows-style worktree_folder colliding with git_root only by case is still rejected."""
        with pytest.MonkeyPatch().context() as monkeypatch:
            monkeypatch.setattr(
                worktree_paths,
                "get_effective_project_config_raw_value",
                lambda *args, **kwargs: "ACME",
            )
            with pytest.raises(ValueError, match="resolves to the main checkout directory"):
                worktree_paths.resolve_worktree_path_from_parent(
                    r"C:\repos",
                    "DFLY-3305",
                    git_root=r"C:\repos\acme",  # type: ignore[arg-type]
                )
