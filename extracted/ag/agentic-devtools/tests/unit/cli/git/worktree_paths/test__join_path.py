"""Tests for _join_path."""

from agentic_devtools.cli.git import worktree_paths


class TestJoinPath:
    """Tests for _join_path."""

    def test_joins_posix_segments(self) -> None:
        """POSIX-style base paths join with forward slashes."""
        assert worktree_paths._join_path("/repos/acme", "wt", "DFLY-3305") == "/repos/acme/wt/DFLY-3305"

    def test_joins_windows_segments(self) -> None:
        """Windows-style base paths join with backslashes."""
        assert worktree_paths._join_path(r"C:\repos\acme", "wt", "DFLY-3305") == r"C:\repos\acme\wt\DFLY-3305"

    def test_joins_no_extra_parts(self) -> None:
        """With no extra parts, the base path is returned unchanged."""
        assert worktree_paths._join_path("/repos/acme") == "/repos/acme"
