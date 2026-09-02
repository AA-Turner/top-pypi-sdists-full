"""Tests for find_issue_worktree."""

from agentic_devtools.cli.git.worktree import WorktreeEntry, find_issue_worktree


class TestFindIssueWorktree:
    """Tests for find_issue_worktree."""

    def test_finds_exact_slash_segment_case_insensitively(self):
        """A branch segment matching the normalized key returns a WorktreeMatch."""
        entries = [WorktreeEntry(path="/repo/one", branch="feature/project-1234/tests")]

        match = find_issue_worktree("PROJECT-1234", entries)

        assert match is not None
        assert match.path == "/repo/one"
        assert match.branch == "feature/project-1234/tests"

    def test_does_not_match_substring_segment(self):
        """Issue keys must match a complete branch segment, not a substring."""
        entries = [WorktreeEntry(path="/repo/one", branch="feature/PROJECT-12345/tests")]

        assert find_issue_worktree("PROJECT-1234", entries) is None

    def test_skips_detached_worktrees(self):
        """Detached entries are ignored even when their path contains the key."""
        entries = [WorktreeEntry(path="/repo/PROJECT-1234", branch=None)]

        assert find_issue_worktree("PROJECT-1234", entries) is None

    def test_matches_branch_with_no_slash(self):
        """Branch names with no slash are treated as one segment."""
        entries = [WorktreeEntry(path="/repo/plain", branch="1900")]

        match = find_issue_worktree("#1900", entries)

        assert match is not None
        assert match.branch == "1900"

    def test_ignores_empty_branch_segments(self):
        """Empty slash-delimited segments do not match but later exact segments can."""
        entries = [WorktreeEntry(path="/repo/plain", branch="feature//1900")]

        assert find_issue_worktree("1900", entries) is not None

    def test_excludes_primary_checkout_when_repo_root_provided(self, tmp_path):
        """The primary checkout is excluded when its path equals repo_root."""
        repo_root = str(tmp_path / "main")
        entries = [
            WorktreeEntry(path=repo_root, branch="feature/1900/impl"),
            WorktreeEntry(path="/sibling/1900", branch="feature/1900/impl"),
        ]

        match = find_issue_worktree("#1900", entries, repo_root=repo_root)

        assert match is not None
        assert match.path == "/sibling/1900"

    def test_returns_none_when_only_primary_checkout_matches(self, tmp_path):
        """Returns None when only the primary checkout entry matches the issue key."""
        repo_root = str(tmp_path / "main")
        entries = [WorktreeEntry(path=repo_root, branch="feature/1900/impl")]

        assert find_issue_worktree("#1900", entries, repo_root=repo_root) is None
