"""Tests for WorktreeEntry."""

from agentic_devtools.cli.git.worktree import WorktreeEntry


class TestWorktreeEntry:
    """Tests for WorktreeEntry dataclass."""

    def test_stores_path_and_branch(self):
        """WorktreeEntry stores path and branch values."""
        entry = WorktreeEntry(path="/repo/1900", branch="feature/1900/tests")

        assert entry.path == "/repo/1900"
        assert entry.branch == "feature/1900/tests"

    def test_allows_detached_branch_none(self):
        """Detached worktree entries store branch as None."""
        assert WorktreeEntry(path="/repo/detached", branch=None).branch is None
