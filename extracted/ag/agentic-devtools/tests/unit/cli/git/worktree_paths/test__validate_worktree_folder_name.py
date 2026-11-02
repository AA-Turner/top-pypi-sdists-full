"""Tests for _validate_worktree_folder_name."""

import pytest

from agentic_devtools.cli.git import worktree_paths


class TestValidateWorktreeFolderName:
    """Tests for _validate_worktree_folder_name."""

    def test_returns_the_value_unchanged_when_valid(self) -> None:
        """A safe relative folder name is returned as-is."""
        assert worktree_paths._validate_worktree_folder_name("custom-wt") == "custom-wt"

    @pytest.mark.parametrize(
        ("value", "message"),
        [
            (".", "'.' and '..' are not allowed"),
            ("..", "'.' and '..' are not allowed"),
            ("/wt", "absolute or drive-qualified paths"),
            (r"C:\wt", "absolute or drive-qualified paths"),
            (r"\\server\share", "absolute or drive-qualified paths"),
            ("wt/nested", "path separators are not allowed"),
            (r"wt\nested", "path separators are not allowed"),
            ("wt\0bad", "control characters"),
            ("wt:", "invalid in Windows folder names"),
            ("wt.", "must not end with '.'"),
            ("con", "reserved Windows device name"),
            ("CON", "reserved Windows device name"),
            ("con.txt", "reserved Windows device name"),
            ("conin$", "reserved Windows device name"),
            ("CONOUT$.log", "reserved Windows device name"),
            ("COM¹.txt", "reserved Windows device name"),
            ("COM¹", "reserved Windows device name"),
            ("COM²", "reserved Windows device name"),
            ("COM³", "reserved Windows device name"),
            ("LPT².log", "reserved Windows device name"),
            ("LPT¹", "reserved Windows device name"),
            ("LPT²", "reserved Windows device name"),
            ("LPT³", "reserved Windows device name"),
        ],
    )
    def test_rejects_unsafe_values(self, value: str, message: str) -> None:
        """Each unsafe folder-name shape is rejected with a specific message."""
        with pytest.raises(ValueError, match=message):
            worktree_paths._validate_worktree_folder_name(value)
