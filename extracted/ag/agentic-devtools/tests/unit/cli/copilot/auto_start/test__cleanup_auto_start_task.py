"""Tests for the _cleanup_auto_start_task helper."""

import json
from contextlib import nullcontext
from unittest.mock import patch

from agentic_devtools.cli.copilot.auto_start import _cleanup_auto_start_task
from agentic_devtools.cli.workflows.worktree_setup import (
    _AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
    _get_auto_start_task_lock_path,
)

_REMOVE = "agentic_devtools.cli.copilot.auto_start.remove_auto_start_task"


def _make_win_error(winerror: int) -> OSError:
    """Create a fresh OSError with a specific Windows winerror code."""
    exc = OSError("file in use")
    exc.winerror = winerror  # type: ignore[attr-defined]
    return exc


class TestCleanupAutoStartTask:
    """Tests for the _cleanup_auto_start_task helper."""

    # ------------------------------------------------------------------
    # File doesn't exist
    # ------------------------------------------------------------------

    def test_noop_when_tasks_json_absent(self, tmp_path):
        """Does nothing when tasks.json doesn't exist (no error)."""
        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=True)
        # No exception raised

    # ------------------------------------------------------------------
    # Tasks remain after removal
    # ------------------------------------------------------------------

    def test_rewrites_file_when_other_tasks_remain(self, tmp_path):
        """Rewrites tasks.json when other tasks remain after removing the target."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        data = {
            "version": "2.0.0",
            "tasks": [
                {"label": "agdt-copilot-auto-start", "type": "shell", "command": "cmd"},
                {"label": "user-task", "type": "shell", "command": "echo hi"},
            ],
        }
        tasks_path.write_text(json.dumps(data), encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["label"] == "user-task"
        assert vscode_dir.exists()

    # ------------------------------------------------------------------
    # No tasks remain, created_new=True
    # ------------------------------------------------------------------

    def test_deletes_file_when_created_new_and_no_tasks_remain(self, tmp_path):
        """Deletes tasks.json when created_new=True and no tasks remain."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        data = {
            "version": "2.0.0",
            "tasks": [{"label": "agdt-copilot-auto-start", "type": "shell", "command": "cmd"}],
        }
        tasks_path.write_text(json.dumps(data), encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=True)

        assert not tasks_path.exists()

    def test_removes_vscode_dir_when_empty_after_file_deletion(self, tmp_path):
        """Removes .vscode/ when it is empty after tasks.json deletion."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        data = {
            "version": "2.0.0",
            "tasks": [{"label": "agdt-copilot-auto-start", "type": "shell", "command": "cmd"}],
        }
        tasks_path.write_text(json.dumps(data), encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=True)

        assert not vscode_dir.exists()

    def test_keeps_vscode_dir_when_not_empty_after_file_deletion(self, tmp_path):
        """Keeps .vscode/ when other files remain after tasks.json deletion."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        data = {
            "version": "2.0.0",
            "tasks": [{"label": "agdt-copilot-auto-start", "type": "shell", "command": "cmd"}],
        }
        tasks_path.write_text(json.dumps(data), encoding="utf-8")
        (vscode_dir / "settings.json").write_text("{}", encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=True)

        assert not tasks_path.exists()
        assert vscode_dir.exists()

    def test_rewrites_with_empty_tasks_when_created_new_and_extra_keys(self, tmp_path):
        """Rewrites with empty tasks (not deletes) when created_new=True but extra keys are present."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        data = {
            "version": "2.0.0",
            "tasks": [{"label": "agdt-copilot-auto-start", "type": "shell", "command": "cmd"}],
            "inputs": [{"id": "myInput", "type": "promptString"}],
        }
        tasks_path.write_text(json.dumps(data), encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=True)

        # File must still exist and preserve the extra key
        assert tasks_path.exists()
        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        assert result["tasks"] == []
        assert result["inputs"] == [{"id": "myInput", "type": "promptString"}]

    # ------------------------------------------------------------------
    # No tasks remain, created_new=False
    # ------------------------------------------------------------------

    def test_rewrites_with_empty_tasks_when_not_created_new_no_extra_keys(self, tmp_path):
        """Rewrites file with empty tasks array when pre-existing and no extra keys."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        data = {
            "version": "2.0.0",
            "tasks": [{"label": "agdt-copilot-auto-start", "type": "shell", "command": "cmd"}],
        }
        tasks_path.write_text(json.dumps(data), encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        assert result["tasks"] == []
        assert tasks_path.exists()

    def test_preserves_extra_keys_when_not_created_new(self, tmp_path):
        """Preserves extra top-level keys (e.g. inputs) when rewriting."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        data = {
            "version": "2.0.0",
            "tasks": [{"label": "agdt-copilot-auto-start", "type": "shell", "command": "cmd"}],
            "inputs": [{"id": "myInput", "type": "promptString"}],
        }
        tasks_path.write_text(json.dumps(data), encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        assert result["tasks"] == []
        assert result["inputs"] == [{"id": "myInput", "type": "promptString"}]

    # ------------------------------------------------------------------
    # Task not present — noop
    # ------------------------------------------------------------------

    def test_noop_when_task_not_present(self, tmp_path):
        """Does nothing when the target task is not in tasks.json."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        data = {
            "version": "2.0.0",
            "tasks": [{"label": "user-task", "type": "shell", "command": "echo hi"}],
        }
        original = json.dumps(data)
        tasks_path.write_text(original, encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        # File content is unchanged
        assert tasks_path.read_text(encoding="utf-8") == original

    # ------------------------------------------------------------------
    # Non-dict items in tasks array preserved
    # ------------------------------------------------------------------

    def test_preserves_non_dict_items_in_tasks(self, tmp_path):
        """Non-dict items in the tasks array are preserved during cleanup."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        data = {
            "version": "2.0.0",
            "tasks": [
                "a string task",
                42,
                {"label": "agdt-copilot-auto-start", "type": "shell", "command": "cmd"},
            ],
        }
        tasks_path.write_text(json.dumps(data), encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        result = json.loads(tasks_path.read_text(encoding="utf-8"))
        assert "a string task" in result["tasks"]
        assert 42 in result["tasks"]
        assert not any(isinstance(t, dict) and t.get("label") == "agdt-copilot-auto-start" for t in result["tasks"])

    # ------------------------------------------------------------------
    # Error handling — silently caught
    # ------------------------------------------------------------------

    def test_silently_ignores_malformed_json(self, tmp_path):
        """Silently ignores malformed JSON in tasks.json."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text("{invalid json", encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        # File is untouched, no exception
        assert tasks_path.read_text(encoding="utf-8") == "{invalid json"

    def test_silently_ignores_os_error_on_read(self, tmp_path):
        """Silently ignores OSError when reading tasks.json."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text("{}", encoding="utf-8")

        with patch("builtins.open", side_effect=OSError("permission denied")):
            _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)
        # No exception raised

    def test_silently_ignores_non_dict_top_level(self, tmp_path):
        """Silently ignores tasks.json with a non-dict top-level value."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text("[1, 2, 3]", encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        assert tasks_path.read_text(encoding="utf-8") == "[1, 2, 3]"

    def test_silently_ignores_non_list_tasks_value(self, tmp_path):
        """Silently ignores tasks.json when tasks value is not a list."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text('{"version": "2.0.0", "tasks": null}', encoding="utf-8")

        _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        # File is unchanged
        assert "null" in tasks_path.read_text(encoding="utf-8")

    def test_silently_ignores_exception_from_remove_auto_start_task(self, tmp_path):
        """Silently ignores any exception raised directly by remove_auto_start_task."""
        with patch(_REMOVE, side_effect=RuntimeError("unexpected failure")):
            # Must not raise despite remove_auto_start_task raising
            _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

    def test_silently_ignores_non_retryable_oserror(self, tmp_path, capsys):
        """Non-retryable OSError from remove_auto_start_task is silently ignored."""
        non_retryable = OSError("permission denied")
        # No winerror attribute set → _is_retryable_win_error returns False
        with patch(_REMOVE, side_effect=non_retryable):
            _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        # No warning emitted (only winerror=32 gets a warning)
        captured = capsys.readouterr()
        assert "transient file lock" not in captured.err

    def test_retries_cleanup_for_retryable_winerrors(self, tmp_path):
        """Retryable cleanup winerrors are retried up to success."""
        with patch(
            _REMOVE,
            side_effect=[_make_win_error(5), _make_win_error(110), _make_win_error(32), None],
        ) as mock_remove:
            with patch("agentic_devtools.cli.copilot.auto_start.time.sleep") as mock_sleep:
                _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        assert mock_remove.call_count == 4
        assert mock_sleep.call_count == 3

    def test_cleanup_sleep_keyboard_interrupt_is_ignored(self, tmp_path):
        """KeyboardInterrupt during cleanup retry backoff is ignored."""
        with patch(_REMOVE, side_effect=[_make_win_error(32)]) as mock_remove:
            with patch("agentic_devtools.cli.copilot.auto_start.time.sleep", side_effect=KeyboardInterrupt):
                _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        assert mock_remove.call_count == 1

    def test_cleanup_noop_when_retry_budget_negative(self, tmp_path):
        """Negative retry budget results in no cleanup attempts."""
        with patch("agentic_devtools.cli.copilot.auto_start._CLEANUP_MAX_RETRIES", -1):
            with patch(_REMOVE) as mock_remove:
                _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        mock_remove.assert_not_called()

    def test_cleanup_single_attempt_when_retry_budget_zero(self, tmp_path):
        """Zero retry budget still performs one cleanup attempt."""
        with patch("agentic_devtools.cli.copilot.auto_start._CLEANUP_MAX_RETRIES", 0):
            with patch(_REMOVE) as mock_remove:
                _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        mock_remove.assert_called_once()

    def test_stops_after_cleanup_retry_budget_exhausted(self, tmp_path):
        """Cleanup stops after configured retry budget for retryable winerrors."""
        with patch(_REMOVE, side_effect=[_make_win_error(5)] * 4) as mock_remove:
            with patch("agentic_devtools.cli.copilot.auto_start.time.sleep") as mock_sleep:
                _cleanup_auto_start_task(str(tmp_path), "agdt-copilot-auto-start", created_new=False)

        assert mock_remove.call_count == 4
        assert mock_sleep.call_count == 3

    def test_run_scoped_cleanup_uses_shared_lock_for_matching_task(self, tmp_path):
        """Run-scoped cleanup holds the shared task lock before deleting the task."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text(
            json.dumps(
                {
                    "version": "2.0.0",
                    "tasks": [
                        {
                            "label": "agdt-copilot-auto-start",
                            "args": ["--run-id", "run-123", "--created-new"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

        with (
            patch("agentic_devtools.cli.copilot.auto_start.locked_file", return_value=nullcontext()) as mock_lock,
            patch(_REMOVE) as mock_remove,
        ):
            _cleanup_auto_start_task(
                str(tmp_path),
                "agdt-copilot-auto-start",
                created_new=False,
                expected_run_id="run-123",
            )

        mock_lock.assert_called_once_with(
            _get_auto_start_task_lock_path(str(tmp_path)),
            mode="a+",
            exclusive=True,
            timeout=_AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
        )
        mock_remove.assert_called_once_with(
            str(tasks_path),
            str(vscode_dir),
            "agdt-copilot-auto-start",
            delete_if_empty=True,
            run_id="run-123",
        )

    def test_run_scoped_cleanup_skips_mismatched_task(self, tmp_path):
        """Run-scoped cleanup preserves a task owned by a different run."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text(
            json.dumps(
                {
                    "version": "2.0.0",
                    "tasks": [{"label": "agdt-copilot-auto-start", "args": ["--run-id", "newer-run"]}],
                }
            ),
            encoding="utf-8",
        )

        with patch(_REMOVE) as mock_remove:
            _cleanup_auto_start_task(
                str(tmp_path),
                "agdt-copilot-auto-start",
                created_new=False,
                expected_run_id="older-run",
            )

        mock_remove.assert_not_called()

    def test_run_scoped_cleanup_skips_blank_expected_run_id(self, tmp_path):
        """Run-scoped cleanup fails closed when the owning run ID is blank."""
        with patch(_REMOVE) as mock_remove:
            _cleanup_auto_start_task(
                str(tmp_path),
                "agdt-copilot-auto-start",
                created_new=False,
                expected_run_id="   ",
            )

        mock_remove.assert_not_called()

    def test_run_scoped_cleanup_skips_non_dict_tasks_file(self, tmp_path):
        """Run-scoped cleanup preserves non-object tasks files."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        (vscode_dir / "tasks.json").write_text("[]", encoding="utf-8")

        with patch(_REMOVE) as mock_remove:
            _cleanup_auto_start_task(
                str(tmp_path),
                "agdt-copilot-auto-start",
                created_new=False,
                expected_run_id="run-123",
            )

        mock_remove.assert_not_called()

    def test_run_scoped_cleanup_skips_non_list_tasks_value(self, tmp_path):
        """Run-scoped cleanup preserves malformed task containers."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        (vscode_dir / "tasks.json").write_text('{"version":"2.0.0","tasks":{}}', encoding="utf-8")

        with patch(_REMOVE) as mock_remove:
            _cleanup_auto_start_task(
                str(tmp_path),
                "agdt-copilot-auto-start",
                created_new=False,
                expected_run_id="run-123",
            )

        mock_remove.assert_not_called()

    def test_run_scoped_cleanup_ignores_non_matching_entries_before_match(self, tmp_path):
        """Run-scoped cleanup scans past unrelated task entries before deleting the match."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text(
            json.dumps(
                {
                    "version": "2.0.0",
                    "tasks": [
                        "not-a-dict",
                        {"label": "other-task", "args": ["--run-id", "run-123"]},
                        {"label": "agdt-copilot-auto-start", "args": ["--run-id", "run-123"]},
                    ],
                }
            ),
            encoding="utf-8",
        )

        with patch(_REMOVE) as mock_remove:
            _cleanup_auto_start_task(
                str(tmp_path),
                "agdt-copilot-auto-start",
                created_new=False,
                expected_run_id="run-123",
            )

        mock_remove.assert_called_once_with(
            str(tasks_path),
            str(vscode_dir),
            "agdt-copilot-auto-start",
            delete_if_empty=False,
            run_id="run-123",
        )

    def test_run_scoped_cleanup_falls_back_to_created_new_when_args_not_list(self, tmp_path):
        """Run-scoped cleanup uses the caller's delete policy when args are malformed."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text(
            json.dumps(
                {
                    "version": "2.0.0",
                    "tasks": [{"label": "agdt-copilot-auto-start", "args": "not-a-list"}],
                }
            ),
            encoding="utf-8",
        )

        with (
            patch(_REMOVE) as mock_remove,
            patch("agentic_devtools.cli.copilot.auto_start.locked_file", return_value=nullcontext()),
            patch(
                "agentic_devtools.cli.workflows.worktree_setup._extract_auto_start_task_run_id",
                return_value="run-123",
            ),
        ):
            _cleanup_auto_start_task(
                str(tmp_path),
                "agdt-copilot-auto-start",
                created_new=True,
                expected_run_id="run-123",
            )

        mock_remove.assert_called_once_with(
            str(tasks_path),
            str(vscode_dir),
            "agdt-copilot-auto-start",
            delete_if_empty=True,
            run_id="run-123",
        )

    def test_run_scoped_cleanup_silently_ignores_malformed_json(self, tmp_path):
        """Run-scoped cleanup returns silently when tasks.json contains invalid JSON."""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        tasks_path = vscode_dir / "tasks.json"
        tasks_path.write_text("{invalid json", encoding="utf-8")

        with patch(_REMOVE) as mock_remove:
            _cleanup_auto_start_task(
                str(tmp_path),
                "agdt-copilot-auto-start",
                created_new=False,
                expected_run_id="run-123",
            )

        mock_remove.assert_not_called()
        # File must be left untouched
        assert tasks_path.read_text(encoding="utf-8") == "{invalid json"
