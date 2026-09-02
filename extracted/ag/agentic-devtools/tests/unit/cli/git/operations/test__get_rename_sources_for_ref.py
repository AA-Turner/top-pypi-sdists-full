"""Tests for agentic_devtools.cli.git.operations._get_rename_sources_for_ref."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git import operations


class TestGetRenameSourcesForRef:
    """Tests for _get_rename_sources_for_ref."""

    def test_returns_new_to_old_mapping_for_renamed_file(self):
        """Map destination path to source path for R-status lines."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="R100\x00src/old.ts\x00src/new.ts\x00",
                stderr="",
            )

            result = operations._get_rename_sources_for_ref("main...HEAD")

            assert result == {"src/new.ts": "src/old.ts"}

    def test_preserves_path_characters(self):
        """Path content is preserved verbatim from git name-status output."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="R90\x00src\\old\\file.ts\x00src\\new\\file.ts\x00",
                stderr="",
            )

            result = operations._get_rename_sources_for_ref("main...HEAD")

            assert result == {"src\\new\\file.ts": "src\\old\\file.ts"}

    def test_ignores_non_rename_status_lines(self):
        """A, M, and D status lines are not included in the result."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout=(
                    "A\x00src/added.ts\x00M\x00src/modified.ts\x00D\x00src/deleted.ts\x00"
                    "R100\x00src/old.ts\x00src/new.ts\x00"
                ),
                stderr="",
            )

            result = operations._get_rename_sources_for_ref("main...HEAD")

            assert result == {"src/new.ts": "src/old.ts"}

    def test_skips_rename_lines_without_destination(self):
        """R-status records missing the destination path are skipped."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="R100\x00src/old.ts\x00",
                stderr="",
            )

            result = operations._get_rename_sources_for_ref("main...HEAD")

            assert result == {}

    def test_returns_empty_dict_when_diff_fails(self):
        """Return an empty mapping when git diff returns a non-zero exit code."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(returncode=128, stdout="", stderr="error")

            result = operations._get_rename_sources_for_ref("main...HEAD")

            assert result == {}

    def test_handles_multiple_renames(self):
        """Multiple rename entries all appear in the result."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="R100\x00a/old1.ts\x00a/new1.ts\x00R95\x00b/old2.ts\x00b/new2.ts\x00",
                stderr="",
            )

            result = operations._get_rename_sources_for_ref("main...HEAD")

            assert result == {"a/new1.ts": "a/old1.ts", "b/new2.ts": "b/old2.ts"}

    def test_skips_blank_lines_in_output(self):
        """Blank lines in git diff output are skipped without error."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="R100\x00src/old.ts\x00src/new.ts\x00\x00A\x00src/added.ts\x00",
                stderr="",
            )

            result = operations._get_rename_sources_for_ref("main...HEAD")

            assert result == {"src/new.ts": "src/old.ts"}

    def test_ignores_three_field_non_rename_status_lines(self):
        """Three-field lines not starting with R (e.g. copy status) are ignored."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(
                returncode=0,
                stdout="C100\x00src/source.ts\x00src/copy.ts\x00R100\x00src/old.ts\x00src/new.ts\x00",
                stderr="",
            )

            result = operations._get_rename_sources_for_ref("main...HEAD")

            # Only the R-status entry produces a mapping; C-status is ignored.
            assert result == {"src/new.ts": "src/old.ts"}
