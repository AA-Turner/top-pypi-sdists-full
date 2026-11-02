"""Tests for agentic_devtools.cli.git.operations.get_file_change_types_on_branch."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git import operations


class TestGetFileChangeTypesOnBranch:
    """Tests for get_file_change_types_on_branch function."""

    def test_returns_change_types_for_add_modify_delete(self, mock_run_safe):
        """Test returns correct long-form change type for A/M/D git status codes."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="A\tsrc/new.ts\nM\tsrc/changed.ts\nD\tsrc/removed.ts\n", stderr=""),
            ]

            result = operations.get_file_change_types_on_branch()

            assert result == {
                "src/new.ts": "add",
                "src/changed.ts": "edit",
                "src/removed.ts": "delete",
            }

    def test_returns_rename_for_r_status(self, mock_run_safe):
        """Test that R (rename) status produces 'rename' and uses the destination path."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="R100\tsrc/old.ts\tsrc/new.ts\n", stderr=""),
            ]

            result = operations.get_file_change_types_on_branch()

            assert result == {"src/new.ts": "rename"}

    def test_returns_empty_dict_when_no_changes(self, mock_run_safe):
        """Test returns empty dict when branch has no changes."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="", stderr=""),
            ]

            result = operations.get_file_change_types_on_branch()

            assert result == {}

    def test_falls_back_to_main_if_origin_main_not_found(self, mock_run_safe):
        """Test falls back to 'main' if 'origin/main' doesn't exist."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=128, stdout="", stderr="error"),
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="M\tfile.ts\n", stderr=""),
            ]

            result = operations.get_file_change_types_on_branch()

            assert result == {"file.ts": "edit"}

    def test_returns_empty_dict_on_error(self, mock_run_safe):
        """Test returns empty dict when both git invocations fail."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=128, stdout="", stderr="error"),
                MagicMock(returncode=128, stdout="", stderr="error"),
            ]

            result = operations.get_file_change_types_on_branch()

            assert result == {}

    def test_returns_empty_dict_when_name_status_diff_fails(self, mock_run_safe):
        """Test returns empty dict when diff range resolves but name-status lookup fails."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=128, stdout="", stderr="error"),
            ]

            result = operations.get_file_change_types_on_branch()

            assert result == {}

    def test_preserves_backslash_paths(self, mock_run_safe):
        """Keep backslash characters unchanged in parsed file paths."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="M\tsrc\\file.ts\n", stderr=""),
            ]

            result = operations.get_file_change_types_on_branch()

            assert "src\\file.ts" in result

    def test_uses_custom_main_branch(self, mock_run_safe):
        """Test uses custom main branch name in the diff ref."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="M\tfile.ts\n", stderr=""),
            ]

            operations.get_file_change_types_on_branch(main_branch="develop")

            first_call_args = mock_run_git.call_args_list[0][0]
            assert "origin/develop...HEAD" in first_call_args
            assert "--find-renames" in first_call_args

    def test_skips_blank_lines_in_output(self, mock_run_safe):
        """Test that blank lines in git output are skipped without error."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="M\tsrc/file.ts\n\nA\tsrc/new.ts\n", stderr=""),
            ]

            result = operations.get_file_change_types_on_branch()

            assert result == {"src/file.ts": "edit", "src/new.ts": "add"}

    def test_skips_malformed_lines_with_single_column(self, mock_run_safe):
        """Test that lines with fewer than two tab-separated fields are skipped."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="M\tsrc/file.ts\nmalformed-line\n", stderr=""),
            ]

            result = operations.get_file_change_types_on_branch()

            assert result == {"src/file.ts": "edit"}
