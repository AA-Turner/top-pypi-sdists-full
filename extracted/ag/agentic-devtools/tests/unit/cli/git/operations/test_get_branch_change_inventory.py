"""Tests for agentic_devtools.cli.git.operations.get_branch_change_inventory."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git import operations


class TestGetBranchChangeInventory:
    """Tests for get_branch_change_inventory."""

    def test_parses_changed_files_types_and_rename_sources_from_single_diff(self):
        """Return files, change types, and rename sources from one name-status diff."""
        with patch.object(operations, "resolve_branch_diff_ref", return_value="main...HEAD"):
            with patch.object(operations, "run_git") as mock_run_git:
                mock_run_git.return_value = MagicMock(
                    returncode=0,
                    stdout=("A\tsrc/new.ts\nM\tsrc/edit.ts\nR100\tsrc/old.ts\tsrc/new-name.ts\n"),
                    stderr="",
                )

                files, change_types, rename_sources, diff_ref, inventory_loaded = (
                    operations.get_branch_change_inventory()
                )

                assert files == ["src/new.ts", "src/edit.ts", "src/new-name.ts"]
                assert change_types == {
                    "src/new.ts": "add",
                    "src/edit.ts": "edit",
                    "src/new-name.ts": "rename",
                }
                assert rename_sources == {"src/new-name.ts": "src/old.ts"}
                assert diff_ref == "main...HEAD"
                assert inventory_loaded is True
                mock_run_git.assert_called_once_with(
                    "diff",
                    "--name-status",
                    "--find-renames",
                    "-z",
                    "main...HEAD",
                    check=False,
                )

    def test_returns_empty_when_diff_ref_unavailable(self):
        """Return empty inventory when no valid branch diff ref can be resolved."""
        with patch.object(operations, "resolve_branch_diff_ref", return_value=None):
            with patch.object(operations, "run_git") as mock_run_git:
                files, change_types, rename_sources, diff_ref, inventory_loaded = (
                    operations.get_branch_change_inventory()
                )

                assert files == []
                assert change_types == {}
                assert rename_sources == {}
                assert diff_ref is None
                assert inventory_loaded is False
                mock_run_git.assert_not_called()

    def test_deduplicates_changed_files_when_status_lists_same_path_multiple_times(self):
        """Keep changed-file order unique while retaining the latest change type."""
        with patch.object(operations, "resolve_branch_diff_ref", return_value="main...HEAD"):
            with patch.object(operations, "run_git") as mock_run_git:
                mock_run_git.return_value = MagicMock(
                    returncode=0,
                    stdout="M\tsrc/file.ts\nD\tsrc/file.ts\n",
                    stderr="",
                )

                files, change_types, rename_sources, diff_ref, inventory_loaded = (
                    operations.get_branch_change_inventory()
                )

                assert files == ["src/file.ts"]
                assert change_types == {"src/file.ts": "delete"}
                assert rename_sources == {}
                assert diff_ref == "main...HEAD"
                assert inventory_loaded is True

    def test_returns_empty_inventory_when_name_status_diff_fails(self):
        """Return empty inventory with the resolved diff ref when git diff fails."""
        with patch.object(operations, "resolve_branch_diff_ref", return_value="origin/main...HEAD"):
            with patch.object(operations, "run_git") as mock_run_git:
                mock_run_git.return_value = MagicMock(returncode=128, stdout="", stderr="error")

                files, change_types, rename_sources, diff_ref, inventory_loaded = (
                    operations.get_branch_change_inventory()
                )

                assert files == []
                assert change_types == {}
                assert rename_sources == {}
                assert diff_ref == "origin/main...HEAD"
                assert inventory_loaded is False
