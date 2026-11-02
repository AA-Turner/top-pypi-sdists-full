"""Tests for agentic_devtools.cli.git.operations._get_files_changed_for_ref."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git import operations


class TestGetFilesChangedForRef:
    """Tests for _get_files_changed_for_ref."""

    def test_returns_normalized_paths_on_success(self):
        """Normalize slash separators and drop blank NUL-delimited entries."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="src/file1.ts\0src\\file2.ts\0README.md\0",
                stderr="",
            )

            result = operations._get_files_changed_for_ref("main...HEAD")

            assert result == ["src/file1.ts", "src/file2.ts", "README.md"]
            mock_run_git.assert_called_once_with(
                "diff", "--name-only", "-z", "--find-renames", "main...HEAD", check=False
            )

    def test_returns_empty_list_when_diff_fails(self):
        """Return an empty list when git diff fails."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(returncode=128, stdout="", stderr="error")

            result = operations._get_files_changed_for_ref("main...HEAD")

            assert result == []

    def test_non_ascii_paths_are_not_corrupted(self):
        """Non-ASCII paths are returned unquoted when -z is used."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="src/café.py\0docs/résumé.md\0",
                stderr="",
            )

            result = operations._get_files_changed_for_ref("main...HEAD")

            assert result == ["src/café.py", "docs/résumé.md"]

    def test_returns_empty_list_when_stdout_is_empty(self):
        """Return an empty list when git diff produces no output."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(returncode=0, stdout="", stderr="")

            result = operations._get_files_changed_for_ref("main...HEAD")

            assert result == []
