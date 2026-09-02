"""Tests for agentic_devtools.cli.git.operations._get_file_change_types_for_ref."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git import operations


class TestGetFileChangeTypesForRef:
    """Tests for _get_file_change_types_for_ref."""

    def test_parses_status_codes(self):
        """Map A/M/D statuses to long-form change types."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="A\x00src/new.ts\x00M\x00src/changed.ts\x00D\x00src/removed.ts\x00",
                stderr="",
            )

            result = operations._get_file_change_types_for_ref("main...HEAD")

            assert result == {
                "src/new.ts": "add",
                "src/changed.ts": "edit",
                "src/removed.ts": "delete",
            }

    def test_parses_rename_status_using_destination_path(self):
        """Use the destination path for rename status lines."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="R100\x00src/old.ts\x00src/new.ts\x00",
                stderr="",
            )

            result = operations._get_file_change_types_for_ref("main...HEAD")

            assert result == {"src/new.ts": "rename"}

    def test_skips_malformed_lines(self):
        """Ignore lines that do not provide both status and path fields."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="M\x00src/file.ts\x00malformed-line\x00",
                stderr="",
            )

            result = operations._get_file_change_types_for_ref("main...HEAD")

            assert result == {"src/file.ts": "edit"}
            mock_run_git.assert_called_once_with(
                "diff",
                "--name-status",
                "--find-renames",
                "-z",
                "main...HEAD",
                check=False,
            )

    def test_returns_empty_dict_when_diff_fails(self):
        """Return an empty mapping when git diff fails."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(returncode=128, stdout="", stderr="error")

            result = operations._get_file_change_types_for_ref("main...HEAD")

            assert result == {}
