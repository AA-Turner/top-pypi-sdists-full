"""Tests for _cleanup_pending_auto_start_marker."""

from contextlib import nullcontext
from unittest.mock import patch

from agentic_devtools.cli.workflows.worktree_setup import (
    _AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
    _PENDING_AUTO_START_FILENAME,
    _cleanup_pending_auto_start_marker,
    _get_pending_auto_start_marker_lock_path,
)


class TestCleanupPendingAutoStartMarker:
    """Tests for the _cleanup_pending_auto_start_marker helper."""

    def test_removes_existing_marker_file_for_matching_run(self, tmp_path):
        """Marker file is deleted when the expected run owns it."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text('{"run_id":"run-123"}', encoding="utf-8")

        _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="run-123")

        assert not marker.exists()

    def test_no_error_when_marker_does_not_exist(self, tmp_path):
        """No error is raised when the marker file is absent."""
        _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="run-123")
        # Should not raise

    def test_no_error_when_vscode_dir_does_not_exist(self, tmp_path):
        """No error when .vscode/ directory does not exist."""
        worktree = tmp_path / "no-vscode"
        worktree.mkdir()
        _cleanup_pending_auto_start_marker(str(worktree), expected_run_id="run-123")
        # Should not raise

    def test_handles_removal_error_gracefully(self, tmp_path, capsys):
        """OSError during removal is caught and printed to stderr."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text('{"run_id":"run-123"}', encoding="utf-8")

        with patch("agentic_devtools.cli.workflows.worktree_setup.os.remove", side_effect=OSError("busy")):
            _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="run-123")
        captured = capsys.readouterr()
        assert "failed to remove pending auto-start marker" in captured.err

    def test_preserves_other_vscode_files(self, tmp_path):
        """Other files in .vscode/ are not affected by cleanup."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text('{"run_id":"run-123"}', encoding="utf-8")
        settings = vscode_dir / "settings.json"
        settings.write_text("{}", encoding="utf-8")

        _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="run-123")

        assert not marker.exists()
        assert settings.exists()

    def test_fails_closed_when_expected_run_id_omitted(self, tmp_path):
        """Cleanup preserves the marker when no owning run ID is supplied."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text('{"run_id":"run-123"}', encoding="utf-8")

        _cleanup_pending_auto_start_marker(str(tmp_path))

        assert marker.exists()

    def test_skips_marker_cleanup_when_run_id_mismatches_expected(self, tmp_path):
        """Run-scoped cleanup leaves a newer marker in place when IDs differ."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text('{"run_id":"newer-run"}', encoding="utf-8")

        _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="older-run")

        assert marker.exists()

    def test_run_scoped_cleanup_removes_matching_marker(self, tmp_path):
        """Run-scoped cleanup deletes marker only when run_id matches."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text('{"run_id":"run-123"}', encoding="utf-8")

        _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="run-123")

        assert not marker.exists()

    def test_run_scoped_cleanup_holds_marker_lock_during_compare_and_delete(self, tmp_path):
        """Run-scoped cleanup serializes the marker compare/delete sequence."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text('{"run_id":"run-123"}', encoding="utf-8")

        with patch(
            "agentic_devtools.cli.workflows.worktree_setup.locked_file",
            return_value=nullcontext(),
        ) as mock_lock:
            _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="run-123")

        mock_lock.assert_called_once_with(
            _get_pending_auto_start_marker_lock_path(str(tmp_path)),
            mode="a+",
            exclusive=True,
            timeout=_AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
        )
        assert not marker.exists()

    def test_no_error_when_worktree_path_does_not_exist(self, tmp_path):
        """Missing worktree paths fail closed without creating files."""
        _cleanup_pending_auto_start_marker(str(tmp_path / "missing-worktree"), expected_run_id="run-123")

    def test_run_scoped_cleanup_skips_when_expected_run_id_blank(self, tmp_path):
        """Blank expected run IDs fail closed and do not delete markers."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text('{"run_id":"run-123"}', encoding="utf-8")

        _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="   ")

        assert marker.exists()

    def test_run_scoped_cleanup_skips_invalid_marker_json(self, tmp_path):
        """Invalid marker JSON is treated as non-owned and preserved."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text("{invalid", encoding="utf-8")

        _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="run-123")

        assert marker.exists()

    def test_run_scoped_cleanup_skips_marker_when_json_not_object(self, tmp_path):
        """Non-object marker JSON is treated as non-owned and preserved."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text("[]", encoding="utf-8")

        _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="run-123")

        assert marker.exists()

    def test_run_scoped_cleanup_skips_marker_without_string_run_id(self, tmp_path):
        """Non-string marker run IDs are treated as non-owned and preserved."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        marker = vscode_dir / _PENDING_AUTO_START_FILENAME
        marker.write_text('{"run_id": 123}', encoding="utf-8")

        _cleanup_pending_auto_start_marker(str(tmp_path), expected_run_id="run-123")

        assert marker.exists()
