"""Tests for _path_cls."""

from pathlib import PurePosixPath, PureWindowsPath

from agentic_devtools.cli.git import worktree_paths


class TestPathCls:
    """Tests for _path_cls."""

    def test_returns_windows_path_class_for_windows_style_text(self) -> None:
        """A Windows-style path text resolves to PureWindowsPath."""
        assert worktree_paths._path_cls(r"C:\repos\acme") is PureWindowsPath

    def test_returns_posix_path_class_for_posix_style_text(self) -> None:
        """A POSIX-style path text resolves to PurePosixPath."""
        assert worktree_paths._path_cls("/repos/acme") is PurePosixPath
