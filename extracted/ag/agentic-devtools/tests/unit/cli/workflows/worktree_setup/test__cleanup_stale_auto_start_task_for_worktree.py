"""Tests for _cleanup_stale_auto_start_task_for_worktree."""

import json
from contextlib import nullcontext
from unittest.mock import patch

import agentic_devtools.cli.workflows.worktree_setup as _ws_module
from agentic_devtools.cli.workflows.worktree_setup import (
    _AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
    _AUTO_START_TASK_LABEL,
    _cleanup_stale_auto_start_task_for_worktree,
    _get_auto_start_task_lock_path,
)


class TestCleanupStaleAutoStartTaskForWorktree:
    """Tests for the _cleanup_stale_auto_start_task_for_worktree helper."""

    def test_removes_stale_task_from_tasks_json(self, tmp_path):
        """Should remove the auto-start task when tasks.json exists."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_data = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": _AUTO_START_TASK_LABEL,
                    "type": "shell",
                    "command": "echo stale",
                    "runOptions": {"runOn": "folderOpen"},
                },
                {
                    "label": "other-task",
                    "type": "shell",
                    "command": "echo keep",
                },
            ],
        }
        tasks_path.write_text(json.dumps(tasks_data), encoding="utf-8")

        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path))

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        labels = [t["label"] for t in result["tasks"]]
        assert _AUTO_START_TASK_LABEL not in labels
        assert "other-task" in labels

    def test_no_op_when_tasks_json_missing(self, tmp_path):
        """Should not raise when .vscode/tasks.json does not exist."""
        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path))

    def test_no_op_when_vscode_dir_missing(self, tmp_path):
        """Should not raise when .vscode directory does not exist."""
        nonexistent = str(tmp_path / "nonexistent_worktree")
        _cleanup_stale_auto_start_task_for_worktree(nonexistent)

    def test_no_op_when_no_matching_task(self, tmp_path):
        """Should leave tasks.json unchanged when no auto-start task present."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_data = {
            "version": "2.0.0",
            "tasks": [
                {"label": "build", "type": "shell", "command": "make"},
            ],
        }
        tasks_path.write_text(json.dumps(tasks_data), encoding="utf-8")

        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path))

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["label"] == "build"

    def test_silently_handles_invalid_json(self, tmp_path):
        """Should not raise when tasks.json contains invalid JSON."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text("not valid json {{{", encoding="utf-8")

        # Should not raise
        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path))

    def test_silently_handles_unexpected_exception(self, tmp_path):
        """Should not raise when an unexpected error occurs (e.g. OS error on isfile)."""
        with patch.object(_ws_module.os.path, "isfile", side_effect=OSError("boom")):
            # Should not raise despite the OSError
            _cleanup_stale_auto_start_task_for_worktree(str(tmp_path))

    def test_delegates_to_remove_stale_auto_start_task(self, tmp_path):
        """Should call _remove_stale_auto_start_task with correct paths."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_data = {"version": "2.0.0", "tasks": []}
        tasks_path.write_text(json.dumps(tasks_data), encoding="utf-8")

        with patch("agentic_devtools.cli.workflows.worktree_setup._remove_stale_auto_start_task") as mock_remove:
            _cleanup_stale_auto_start_task_for_worktree(str(tmp_path))

        mock_remove.assert_called_once_with(
            str(tasks_path),
            str(vscode_dir),
            _AUTO_START_TASK_LABEL,
            expected_run_id=None,
        )

    def test_run_scoped_cleanup_skips_task_with_mismatched_run_id(self, tmp_path):
        """Run-scoped cleanup does not remove a task for a different run."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_data = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": _AUTO_START_TASK_LABEL,
                    "type": "process",
                    "command": "agdt-copilot-auto-start",
                    "args": ["--run-id", "newer-run"],
                }
            ],
        }
        tasks_path.write_text(json.dumps(tasks_data), encoding="utf-8")

        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path), expected_run_id="older-run")

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        labels = [t["label"] for t in result["tasks"]]
        assert _AUTO_START_TASK_LABEL in labels

    def test_run_scoped_cleanup_removes_task_with_matching_run_id(self, tmp_path):
        """Run-scoped cleanup removes the task when run_id matches."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_data = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": _AUTO_START_TASK_LABEL,
                    "type": "process",
                    "command": "agdt-copilot-auto-start",
                    "args": ["--run-id", "run-123"],
                }
            ],
        }
        tasks_path.write_text(json.dumps(tasks_data), encoding="utf-8")

        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path), expected_run_id="run-123")

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        labels = [t["label"] for t in result["tasks"]]
        assert _AUTO_START_TASK_LABEL not in labels

    def test_run_scoped_cleanup_holds_task_lock_during_compare_and_delete(self, tmp_path):
        """Run-scoped cleanup serializes the compare/delete sequence with the task lock."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_data = {
            "version": "2.0.0",
            "tasks": [{"label": _AUTO_START_TASK_LABEL, "args": ["--run-id", "run-123"]}],
        }
        tasks_path.write_text(json.dumps(tasks_data), encoding="utf-8")

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.locked_file", return_value=nullcontext()) as mock_lock,
            patch("agentic_devtools.cli.workflows.worktree_setup._remove_stale_auto_start_task") as mock_remove,
        ):
            _cleanup_stale_auto_start_task_for_worktree(str(tmp_path), expected_run_id="run-123")

        mock_lock.assert_called_once_with(
            _get_auto_start_task_lock_path(str(tmp_path)),
            mode="a+",
            exclusive=True,
            timeout=_AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
        )
        mock_remove.assert_called_once_with(
            str(tasks_path),
            str(vscode_dir),
            _AUTO_START_TASK_LABEL,
            expected_run_id="run-123",
        )

    def test_run_scoped_cleanup_skips_when_expected_run_id_blank(self, tmp_path):
        """Blank expected run IDs fail closed and skip cleanup."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_data = {
            "version": "2.0.0",
            "tasks": [{"label": _AUTO_START_TASK_LABEL, "args": ["--run-id", "run-123"]}],
        }
        tasks_path.write_text(json.dumps(tasks_data), encoding="utf-8")

        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path), expected_run_id="   ")

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        labels = [t["label"] for t in result["tasks"]]
        assert _AUTO_START_TASK_LABEL in labels

    def test_run_scoped_cleanup_skips_when_tasks_file_not_object(self, tmp_path):
        """Run-scoped cleanup skips non-object tasks files to avoid unsafe deletes."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text("[]", encoding="utf-8")

        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path), expected_run_id="run-123")

        assert tasks_path.exists()

    def test_run_scoped_cleanup_skips_when_tasks_field_not_list(self, tmp_path):
        """Run-scoped cleanup skips malformed task containers."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text(json.dumps({"version": "2.0.0", "tasks": {}}), encoding="utf-8")

        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path), expected_run_id="run-123")

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        assert isinstance(result["tasks"], dict)

    def test_run_scoped_cleanup_skips_when_no_auto_start_task_label(self, tmp_path):
        """Run-scoped cleanup skips files without the auto-start task label."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_data = {
            "version": "2.0.0",
            "tasks": [{"label": "build", "args": ["--run-id", "run-123"]}],
        }
        tasks_path.write_text(json.dumps(tasks_data), encoding="utf-8")

        _cleanup_stale_auto_start_task_for_worktree(str(tmp_path), expected_run_id="run-123")

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        assert result["tasks"][0]["label"] == "build"
