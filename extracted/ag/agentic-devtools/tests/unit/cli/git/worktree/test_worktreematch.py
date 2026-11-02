"""Tests for WorktreeMatch."""

from agentic_devtools.cli.git.worktree import WorktreeMatch


class TestWorktreeMatch:
    """Tests for WorktreeMatch dataclass."""

    def test_stores_matching_path_and_branch(self):
        """WorktreeMatch stores the matched worktree path and branch."""
        match = WorktreeMatch(path="/repo/1900", branch="feature/1900/tests")

        assert match.path == "/repo/1900"
        assert match.branch == "feature/1900/tests"
