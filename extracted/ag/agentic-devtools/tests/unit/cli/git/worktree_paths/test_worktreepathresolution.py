"""Tests for WorktreePathResolution."""

from agentic_devtools.cli.git import worktree_paths


class TestWorktreePathResolution:
    """Tests for WorktreePathResolution."""

    def test_is_frozen(self) -> None:
        """The dataclass is immutable once constructed."""
        resolution = worktree_paths.WorktreePathResolution(
            repos_parent="/repos",
            worktree_path="/repos/wt/DFLY-3305",
            normalized_issue_key="DFLY-3305",
            worktree_folder="wt",
            configured_parent_dir="/repos/wt",
        )

        try:
            resolution.worktree_path = "/other"  # type: ignore[misc]
        except AttributeError:
            pass
        else:
            raise AssertionError("WorktreePathResolution must be immutable")

    def test_stores_all_fields(self) -> None:
        """All resolved fields are exposed unchanged."""
        resolution = worktree_paths.WorktreePathResolution(
            repos_parent="/repos",
            worktree_path="/repos/DFLY-3305",
            normalized_issue_key="DFLY-3305",
            worktree_folder=None,
            configured_parent_dir=None,
        )

        assert resolution.repos_parent == "/repos"
        assert resolution.worktree_path == "/repos/DFLY-3305"
        assert resolution.normalized_issue_key == "DFLY-3305"
        assert resolution.worktree_folder is None
        assert resolution.configured_parent_dir is None
