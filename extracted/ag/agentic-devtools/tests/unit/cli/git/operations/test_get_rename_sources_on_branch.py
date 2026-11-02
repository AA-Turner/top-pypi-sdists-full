"""Tests for agentic_devtools.cli.git.operations.get_rename_sources_on_branch."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git import operations


class TestGetRenameSourcesOnBranch:
    """Tests for get_rename_sources_on_branch."""

    def test_returns_new_to_old_path_mapping_for_rename(self, mock_run_safe):
        """Return {destination: source} for renamed files on the branch."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="R100\tsrc/old.ts\tsrc/new.ts\n", stderr=""),
            ]

            result = operations.get_rename_sources_on_branch()

            assert result == {"src/new.ts": "src/old.ts"}

    def test_returns_empty_dict_when_no_renames(self, mock_run_safe):
        """Return an empty dict when there are no renamed files on the branch."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="A\tsrc/new.ts\nM\tsrc/changed.ts\n", stderr=""),
            ]

            result = operations.get_rename_sources_on_branch()

            assert result == {}

    def test_returns_empty_dict_when_diff_ref_unavailable(self, mock_run_safe):
        """Return an empty dict when no branch diff ref can be resolved."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=128, stdout="", stderr="error"),
                MagicMock(returncode=128, stdout="", stderr="error"),
            ]

            result = operations.get_rename_sources_on_branch()

            assert result == {}

    def test_uses_custom_main_branch(self, mock_run_safe):
        """Pass the custom main branch name through to the diff range."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=1, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="R100\tsrc/old.ts\tsrc/new.ts\n", stderr=""),
            ]

            operations.get_rename_sources_on_branch(main_branch="develop")

            first_call_args = mock_run_git.call_args_list[0][0]
            assert "origin/develop...HEAD" in first_call_args
