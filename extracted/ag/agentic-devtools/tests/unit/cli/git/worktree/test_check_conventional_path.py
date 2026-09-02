"""Tests for check_conventional_path."""

from agentic_devtools.cli.git.worktree import check_conventional_path


class TestCheckConventionalPath:
    """Tests for check_conventional_path."""

    def test_returns_existing_parent_issue_directory(self, tmp_path):
        """The conventional ../{normalized_key} path is returned when it exists."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        expected = tmp_path / "1900"
        expected.mkdir()

        assert check_conventional_path(str(repo_root), "#1900") == expected

    def test_returns_none_when_conventional_path_is_missing(self, tmp_path):
        """Missing conventional paths return None."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()

        assert check_conventional_path(str(repo_root), "PROJECT-1234") is None
