"""Tests for _build_drift_file_list changed-file builder."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.checks.setup_drift_changed_files import _build_drift_file_list

_MOD = "agentic_devtools.cli.checks.setup_drift_changed_files"


class TestBuildDriftFileList:
    """Tests for the _build_drift_file_list function (FR-009)."""

    def test_renamed_path_includes_old_and_new(self, tmp_path: Path) -> None:
        """Renamed path: both old and new paths appear in result."""

        def mock_get_changed(*, pattern: str = "*.py", cwd: str | Path | None = None, **kw: object) -> list[str]:
            return ["agentic_devtools/cli/setup/new_name.py"]

        rename_output = "R100\tagentic_devtools/cli/setup/old_name.py\tagentic_devtools/cli/setup/new_name.py\n"

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 0, stdout=rename_output, stderr="")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert "agentic_devtools/cli/setup/old_name.py" in files
        assert "agentic_devtools/cli/setup/new_name.py" in files
        assert "agentic_devtools/cli/setup/old_name.py" in deleted

    def test_deleted_path_in_result(self, tmp_path: Path) -> None:
        """Deleted path appears in result (FR-009)."""

        def mock_get_changed(**kw: object) -> list[str]:
            return []

        delete_output = "D\tagentic_devtools/cli/setup/removed.py\n"

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 0, stdout=delete_output, stderr="")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert "agentic_devtools/cli/setup/removed.py" in files
        assert "agentic_devtools/cli/setup/removed.py" in deleted

    def test_duplicate_paths_deduplicated(self, tmp_path: Path) -> None:
        """Duplicate paths from primary and supplementary are deduplicated."""

        def mock_get_changed(**kw: object) -> list[str]:
            return ["agentic_devtools/cli/setup/commands.py"]

        # Supplementary also reports the same file as a rename new-path
        rename_output = "R100\told.py\tagentic_devtools/cli/setup/commands.py\n"

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 0, stdout=rename_output, stderr="")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert files.count("agentic_devtools/cli/setup/commands.py") == 1

    def test_fallback_revision_ladder(self, tmp_path: Path) -> None:
        """Fallback revision ladder is exercised when origin/main unavailable."""
        call_count = 0

        def mock_get_changed(**kw: object) -> list[str]:
            return ["some_file.py"]

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            nonlocal call_count
            call_count += 1
            # First strategy fails, second succeeds
            if call_count == 1:
                return subprocess.CompletedProcess(cmd, 128, stdout="", stderr="error")
            return subprocess.CompletedProcess(cmd, 0, stdout="D\tdeleted.py\n", stderr="")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert "deleted.py" in files
        assert call_count >= 2

    def test_empty_git_output(self, tmp_path: Path) -> None:
        """Empty git output returns empty lists."""

        def mock_get_changed(**kw: object) -> list[str]:
            return []

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert files == []
        assert deleted == []

    def test_diff_unavailable_returns_empty_primary(self, tmp_path: Path) -> None:
        """DiffUnavailableError from get_changed_files → empty primary list."""
        from agentic_devtools.cli.checks.changed_files import DiffUnavailableError

        def mock_get_changed(**kw: object) -> list[str]:
            raise DiffUnavailableError("no git")

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 0, stdout="D\tsome_file.py\n", stderr="")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert "some_file.py" in files
        assert "some_file.py" in deleted

    def test_all_strategies_fail_returns_empty(self, tmp_path: Path) -> None:
        """All diff strategies fail → deleted_paths empty, only primary returned."""

        def mock_get_changed(**kw: object) -> list[str]:
            return ["file.py"]

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 128, stdout="", stderr="error")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert files == ["file.py"]
        assert deleted == []

    def test_subprocess_oserror_continues(self, tmp_path: Path) -> None:
        """OSError from subprocess.run → strategy skipped, continues to next."""

        def mock_get_changed(**kw: object) -> list[str]:
            return []

        call_count = 0

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise OSError("git not found")
            return subprocess.CompletedProcess(cmd, 0, stdout="D\tdeleted_file.py\n", stderr="")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert "deleted_file.py" in files
        assert call_count >= 2

    def test_blank_lines_in_git_output_skipped(self, tmp_path: Path) -> None:
        """Blank lines in supplementary git output are skipped."""

        def mock_get_changed(**kw: object) -> list[str]:
            return []

        # Output with blank lines interspersed
        output_with_blanks = "\nD\tfile_a.py\n\n\nD\tfile_b.py\n\n"

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 0, stdout=output_with_blanks, stderr="")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert "file_a.py" in files
        assert "file_b.py" in files

    def test_unrecognised_status_ignored(self, tmp_path: Path) -> None:
        """Lines with statuses other than D/R are silently ignored."""

        def mock_get_changed(**kw: object) -> list[str]:
            return []

        # M (modified) should not be recognised by the DR-only filter
        output = "M\tmodified_file.py\nD\tdeleted_file.py\n"

        def mock_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 0, stdout=output, stderr="")

        with (
            patch(f"{_MOD}.get_changed_files", side_effect=mock_get_changed),
            patch(f"{_MOD}.subprocess.run", side_effect=mock_run),
        ):
            files, deleted = _build_drift_file_list(tmp_path)

        assert "deleted_file.py" in files
        assert "modified_file.py" not in deleted
