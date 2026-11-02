"""Tests for check_conventional_path."""

from agentic_devtools.cli.git.worktree import check_conventional_path
from agentic_devtools.cli.git.worktree_paths import WorktreePathResolution


class TestCheckConventionalPath:
    """Tests for check_conventional_path."""

    def test_returns_existing_configured_worktree_directory(self, monkeypatch, tmp_path):
        """The conventional fallback uses the shared configured worktree path."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        expected = tmp_path / "wt" / "1900"
        expected.mkdir(parents=True)
        monkeypatch.setattr(
            "agentic_devtools.cli.git.worktree.resolve_worktree_path",
            lambda repo_root, issue_key: WorktreePathResolution(
                repos_parent=str(tmp_path),
                worktree_path=str(expected),
                normalized_issue_key="1900",
                worktree_folder="wt",
                configured_parent_dir=str(tmp_path / "wt"),
            ),
        )

        assert check_conventional_path(str(repo_root), "#1900") == expected

    def test_returns_existing_legacy_direct_sibling_directory(self, monkeypatch, tmp_path):
        """Explicit direct-sibling opt-out still resolves through the shared contract."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        expected = tmp_path / "PROJECT-1234"
        expected.mkdir()
        monkeypatch.setattr(
            "agentic_devtools.cli.git.worktree.resolve_worktree_path",
            lambda repo_root, issue_key: WorktreePathResolution(
                repos_parent=str(tmp_path),
                worktree_path=str(expected),
                normalized_issue_key="PROJECT-1234",
                worktree_folder=None,
                configured_parent_dir=None,
            ),
        )

        assert check_conventional_path(str(repo_root), "PROJECT-1234") == expected

    def test_returns_none_when_conventional_path_is_missing(self, monkeypatch, tmp_path):
        """Missing conventional paths return None."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        missing = tmp_path / "wt" / "PROJECT-1234"
        monkeypatch.setattr(
            "agentic_devtools.cli.git.worktree.resolve_worktree_path",
            lambda repo_root, issue_key: WorktreePathResolution(
                repos_parent=str(tmp_path),
                worktree_path=str(missing),
                normalized_issue_key="PROJECT-1234",
                worktree_folder="wt",
                configured_parent_dir=str(tmp_path / "wt"),
            ),
        )

        assert check_conventional_path(str(repo_root), "PROJECT-1234") is None
