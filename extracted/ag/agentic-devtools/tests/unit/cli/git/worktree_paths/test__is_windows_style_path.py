"""Tests for _is_windows_style_path."""

import pytest

from agentic_devtools.cli.git import worktree_paths


class TestIsWindowsStylePath:
    """Tests for _is_windows_style_path."""

    @pytest.mark.parametrize(
        "path_text",
        [
            r"C:\repos\acme",
            r"\\server\share\repos",
            r"repos\acme",
        ],
    )
    def test_detects_windows_style_paths(self, path_text: str) -> None:
        """A drive letter, UNC prefix, or backslash marks a path as Windows-style."""
        assert worktree_paths._is_windows_style_path(path_text) is True

    @pytest.mark.parametrize(
        "path_text",
        [
            "/repos/acme",
            "repos/acme",
            "acme",
        ],
    )
    def test_detects_posix_style_paths(self, path_text: str) -> None:
        """A path with no drive, UNC prefix, or backslash is POSIX-style."""
        assert worktree_paths._is_windows_style_path(path_text) is False
