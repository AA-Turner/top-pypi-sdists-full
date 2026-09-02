"""Tests for _spawn_delayed_autostart_verification."""

from __future__ import annotations

import os
import threading
from unittest.mock import MagicMock, call, patch

_MODULE = "agentic_devtools.cli.workflows.worktree_setup"


class TestSpawnDelayedAutostartVerification:
    """Unit tests for _spawn_delayed_autostart_verification."""

    def _import_fn(self):
        from agentic_devtools.cli.workflows.worktree_setup import (
            _spawn_delayed_autostart_verification,
        )

        return _spawn_delayed_autostart_verification

    def _join_verification_thread(self, timeout: float = 5.0) -> None:
        deadline = threading.Event()
        wait_s = 0.01
        elapsed = 0.0
        while elapsed < timeout:
            for thread in threading.enumerate():
                if thread.name == "autostart-verification":
                    thread.join(timeout=max(0.0, timeout - elapsed))
                    return
            deadline.wait(wait_s)
            elapsed += wait_s

    @patch(f"{_MODULE}._in_test_environment", return_value=True)
    def test_noop_in_test_environment(self, mock_test_env):
        """Verify function is a no-op when _in_test_environment returns True."""
        fn = self._import_fn()

        # Should return immediately without spawning a thread
        fn(
            worktree_path="/tmp/fake",
            start_prompt="test prompt",
            workflow_name="test-workflow",
        )

        # No thread should be running with our name
        threads = [t for t in threading.enumerate() if t.name == "autostart-verification"]
        assert threads == []

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=True)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_returns_early_when_run_triggered(self, mock_triggered, mock_resolve, mock_test_env, tmp_path):
        """Verify thread exits without starting fallback when auto-start task ran."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        pending_marker = tmp_path / ".vscode" / "pending-auto-start.json"
        pending_marker.parent.mkdir(parents=True)
        pending_marker.write_text('{"run_id":"run-123"}', encoding="utf-8")
        mock_resolve.return_value = (state_file, "")

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
        )

        self._join_verification_thread()

        # _is_run_triggered was called and returned True — no fallback
        mock_triggered.assert_called()

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch(f"{_MODULE}._open_log_in_vscode")
    @patch(f"{_MODULE}.is_vscode_available", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    def test_skips_fallback_when_no_state_file(
        self,
        mock_resolve,
        mock_copilot,
        mock_vscode,
        mock_open_log,
        mock_test_env,
        tmp_path,
        capsys,
    ):
        """Missing state file fails closed and does not launch fallback."""
        fn = self._import_fn()
        mock_resolve.return_value = (None, "")
        mock_copilot.return_value = None

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
        )

        self._join_verification_thread()

        mock_copilot.assert_not_called()
        assert "Skipping fallback startup to avoid an unclaimed duplicate session" in capsys.readouterr().err

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch(f"{_MODULE}._open_log_in_vscode")
    @patch(f"{_MODULE}.is_vscode_available", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_starts_fallback_after_timeout(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_vscode,
        mock_open_log,
        mock_test_env,
        tmp_path,
    ):
        """Verify fallback session starts when polling times out."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        pending_marker = tmp_path / ".vscode" / "pending-auto-start.json"
        pending_marker.parent.mkdir(parents=True)
        pending_marker.write_text('{"run_id":"run-456"}', encoding="utf-8")
        mock_resolve.return_value = (state_file, "")
        mock_copilot.return_value = None

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
        )

        self._join_verification_thread()

        mock_copilot.assert_called_once()

    @patch(f"{_MODULE}._cleanup_pending_auto_start_marker")
    @patch(f"{_MODULE}._cleanup_stale_auto_start_task_for_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_cleans_pending_auto_start_after_fallback(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_record,
        mock_cleanup_task,
        mock_cleanup_marker,
        tmp_path,
    ):
        """Fallback startup removes the orphaned folder-open task and marker."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")
        mock_process = MagicMock()
        mock_process.wait.return_value = 0
        mock_copilot.return_value = MagicMock(log_file=None, process=mock_process)

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-fallback",
        )

        self._join_verification_thread()

        mock_copilot.assert_called_once()
        mock_record.assert_has_calls(
            [
                call(state_file, "run-fallback", "running"),
                call(state_file, "run-fallback", "completed", 0),
            ]
        )
        mock_cleanup_task.assert_called_once_with(str(tmp_path), expected_run_id="run-fallback")
        mock_cleanup_marker.assert_called_once_with(str(tmp_path), expected_run_id="run-fallback")

    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch("agentic_devtools.cli.copilot.auto_start._unmark_run_triggered")
    @patch(f"{_MODULE}._cleanup_pending_auto_start_marker")
    @patch(f"{_MODULE}._cleanup_stale_auto_start_task_for_worktree")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session", return_value=None)
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_releases_claim_when_fallback_does_not_launch_child(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_cleanup_task,
        mock_cleanup_marker,
        mock_unmark,
        mock_record,
        tmp_path,
        capsys,
    ):
        """A fallback with no child process releases its claim and preserves retry artifacts."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-no-child",
        )

        self._join_verification_thread()

        mock_copilot.assert_called_once()
        mock_unmark.assert_called_once_with(state_file, "run-no-child")
        mock_record.assert_has_calls(
            [
                call(state_file, "run-no-child", "running"),
                call(state_file, "run-no-child", "failed", 1),
            ]
        )
        mock_cleanup_task.assert_not_called()
        mock_cleanup_marker.assert_not_called()
        assert "did not launch a child process" in capsys.readouterr().err

    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch("agentic_devtools.cli.copilot.auto_start._unmark_run_triggered")
    @patch(f"{_MODULE}._cleanup_pending_auto_start_marker")
    @patch(f"{_MODULE}._cleanup_stale_auto_start_task_for_worktree")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_preserves_claim_when_fallback_observes_existing_live_session(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_cleanup_task,
        mock_cleanup_marker,
        mock_unmark,
        mock_record,
        tmp_path,
        capsys,
    ):
        """Existing live session records a terminal skipped outcome; triggered-run claim is kept."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")
        mock_copilot.return_value = MagicMock(pid=4321, process=None, log_file=None)

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-existing",
        )

        self._join_verification_thread()

        mock_unmark.assert_not_called()
        assert mock_record.call_count == 2
        mock_record.assert_any_call(state_file, "run-existing", "running")
        mock_record.assert_any_call(state_file, "run-existing", "skipped")
        mock_cleanup_task.assert_not_called()
        mock_cleanup_marker.assert_not_called()
        assert "existing live Copilot session (pid=4321)" in capsys.readouterr().err

    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch("agentic_devtools.cli.copilot.auto_start._unmark_run_triggered")
    @patch(f"{_MODULE}._cleanup_pending_auto_start_marker")
    @patch(f"{_MODULE}._cleanup_stale_auto_start_task_for_worktree")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_releases_claim_when_fallback_result_has_no_child_and_no_live_pid(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_cleanup_task,
        mock_cleanup_marker,
        mock_unmark,
        mock_record,
        tmp_path,
        capsys,
    ):
        """No-child fallback results without a live PID are treated as failures."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")
        mock_copilot.return_value = MagicMock(pid=None, process=None, log_file=None)

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-no-live-pid",
        )

        self._join_verification_thread()

        mock_unmark.assert_called_once_with(state_file, "run-no-live-pid")
        mock_record.assert_has_calls(
            [
                call(state_file, "run-no-live-pid", "running"),
                call(state_file, "run-no-live-pid", "failed", 1),
            ]
        )
        mock_cleanup_task.assert_not_called()
        mock_cleanup_marker.assert_not_called()
        assert "did not launch a child process" in capsys.readouterr().err

    @patch("agentic_devtools.cli.copilot.auto_start._mark_run_triggered", return_value=False)
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_skips_fallback_when_auto_start_claims_run_during_timeout(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_mark_triggered,
        tmp_path,
    ):
        """A late auto-start claim wins the race and prevents duplicate fallback startup."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-race",
        )

        self._join_verification_thread()

        mock_mark_triggered.assert_called_once_with(state_file, "run-race")
        mock_copilot.assert_not_called()

    @patch("agentic_devtools.cli.copilot.auto_start._mark_run_triggered", side_effect=RuntimeError("claim failed"))
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_skips_fallback_when_run_claim_fails(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_mark_triggered,
        tmp_path,
        capsys,
    ):
        """A failed run claim does not launch an unprotected fallback session."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-claim-error",
        )

        self._join_verification_thread()

        mock_mark_triggered.assert_called_once_with(state_file, "run-claim-error")
        mock_copilot.assert_not_called()
        assert "could not claim auto-start run" in capsys.readouterr().err

    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch("agentic_devtools.cli.copilot.auto_start._unmark_run_triggered")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session", side_effect=RuntimeError("fallback failed"))
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_unmarks_run_when_claimed_fallback_fails(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_unmark,
        mock_record,
        tmp_path,
    ):
        """A fallback startup failure releases its atomic run claim."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-fallback-error",
        )

        self._join_verification_thread()

        mock_unmark.assert_called_once_with(state_file, "run-fallback-error")
        mock_record.assert_has_calls(
            [
                call(state_file, "run-fallback-error", "running"),
                call(state_file, "run-fallback-error", "failed", 1),
            ]
        )

    @patch("agentic_devtools.cli.copilot.auto_start._unmark_run_triggered", side_effect=RuntimeError("release failed"))
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session", side_effect=RuntimeError("fallback failed"))
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_suppresses_run_cleanup_error_after_fallback_fails(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_unmark,
        tmp_path,
        capsys,
    ):
        """A cleanup failure after fallback startup failure is swallowed and logged once."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-cleanup-error",
        )

        self._join_verification_thread()

        mock_unmark.assert_called_once_with(state_file, "run-cleanup-error")
        assert "delayed fallback Copilot session failed" in capsys.readouterr().err

    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch(f"{_MODULE}._cleanup_pending_auto_start_marker")
    @patch(f"{_MODULE}._cleanup_stale_auto_start_task_for_worktree")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_records_fallback_terminal_failure_after_process_exit(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_cleanup_task,
        mock_cleanup_marker,
        mock_record,
        tmp_path,
    ):
        """Fallback outcome stays running until the detached Copilot process exits."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")
        mock_process = MagicMock()
        mock_process.wait.return_value = 7
        mock_result = MagicMock(log_file=None, process=mock_process)
        mock_copilot.return_value = mock_result

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-process-exit",
        )

        self._join_verification_thread()

        mock_process.wait.assert_called_once_with()
        mock_record.assert_has_calls(
            [
                call(state_file, "run-process-exit", "running"),
                call(state_file, "run-process-exit", "failed", 7),
            ]
        )

    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch("agentic_devtools.cli.copilot.auto_start._unmark_run_triggered")
    @patch(f"{_MODULE}._cleanup_pending_auto_start_marker")
    @patch(f"{_MODULE}._cleanup_stale_auto_start_task_for_worktree")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_retains_claim_when_monitoring_child_raises(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_cleanup_task,
        mock_cleanup_marker,
        mock_unmark,
        mock_record,
        tmp_path,
        capsys,
    ):
        """A post-launch monitoring error retains ownership to prevent duplicate startup."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")
        mock_process = MagicMock()
        mock_process.wait.side_effect = RuntimeError("wait failed")
        mock_copilot.return_value = MagicMock(log_file=None, process=mock_process)

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-monitoring-error",
        )

        self._join_verification_thread()

        mock_unmark.assert_not_called()
        mock_cleanup_task.assert_called_once_with(str(tmp_path), expected_run_id="run-monitoring-error")
        mock_cleanup_marker.assert_called_once_with(str(tmp_path), expected_run_id="run-monitoring-error")
        mock_record.assert_called_once_with(state_file, "run-monitoring-error", "running")
        assert "wait failed" in capsys.readouterr().err

    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch(f"{_MODULE}._open_log_in_vscode", side_effect=RuntimeError("open log failed"))
    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}._cleanup_pending_auto_start_marker")
    @patch(f"{_MODULE}._cleanup_stale_auto_start_task_for_worktree")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_records_terminal_outcome_when_log_open_fails_after_launch(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_cleanup_task,
        mock_cleanup_marker,
        mock_vscode,
        mock_open_log,
        mock_record,
        tmp_path,
        capsys,
    ):
        """Post-launch monitor errors still finalize run outcome after process exit."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")
        mock_process = MagicMock()
        mock_process.wait.return_value = 9
        mock_copilot.return_value = MagicMock(log_file="/tmp/copilot.log", process=mock_process)

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-open-log-error",
        )

        self._join_verification_thread()

        mock_process.wait.assert_called_once_with()
        mock_record.assert_has_calls(
            [
                call(state_file, "run-open-log-error", "running"),
                call(state_file, "run-open-log-error", "failed", 9),
            ]
        )
        assert "open log failed" in capsys.readouterr().err

    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch("agentic_devtools.cli.copilot.auto_start._unmark_run_triggered")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_skips_unmark_when_session_raises_child_alive_error(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        mock_unmark,
        mock_record,
        tmp_path,
        capsys,
    ):
        """CopilotChildAliveError from start_copilot_session preserves the run claim.

        When the session abort cannot confirm child process exit the fallback
        must NOT unmark the triggered run or record "failed" — the child may
        still be alive and holds the session mutex.  Recording "failed" would
        allow a late folder-open task to re-trigger a duplicate session.
        """
        from agentic_devtools.cli.copilot.session import CopilotChildAliveError

        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")
        child_alive_exc = CopilotChildAliveError("log open failed")
        child_alive_exc.__cause__ = OSError("log open failed")
        mock_copilot.side_effect = child_alive_exc

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-child-alive",
        )

        self._join_verification_thread()

        mock_unmark.assert_not_called()
        # Only the initial "running" record call is expected; no "failed" call.
        mock_record.assert_called_once_with(state_file, "run-child-alive", "running")
        assert "log open failed" in capsys.readouterr().err

    @patch("agentic_devtools.cli.copilot.auto_start._record_run_outcome")
    @patch("agentic_devtools.cli.copilot.auto_start._unmark_run_triggered")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_unmarks_run_when_session_module_import_fails(
        self,
        mock_triggered,
        mock_resolve,
        mock_test_env,
        mock_unmark,
        mock_record,
        tmp_path,
        capsys,
    ):
        """Import failure of copilot.session falls back to normal unmark behaviour.

        When the copilot.session module cannot be imported the inner
        CopilotChildAliveError import also fails, so is_child_alive_error
        stays False and the run is unmarked and recorded as "failed" as normal.
        """
        import sys

        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")

        with patch.dict(sys.modules, {"agentic_devtools.cli.copilot.session": None}):
            fn(
                worktree_path=str(tmp_path),
                start_prompt="test prompt",
                workflow_name="test-workflow",
                run_id="run-import-fail",
            )
            self._join_verification_thread()

        mock_unmark.assert_called_once_with(state_file, "run-import-fail")
        mock_record.assert_any_call(state_file, "run-import-fail", "failed", 1)

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch(f"{_MODULE}._open_log_in_vscode")
    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_opens_log_before_waiting_for_fallback_process_exit(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_vscode,
        mock_open_log,
        mock_test_env,
        tmp_path,
    ):
        """Fallback opens its log for live monitoring before waiting for process exit."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")
        events: list[str] = []
        mock_process = MagicMock()

        def _wait_for_exit() -> int:
            events.append("wait")
            return 0

        mock_process.wait.side_effect = _wait_for_exit
        session_result = MagicMock(log_file="/tmp/copilot.log", process=mock_process)
        mock_copilot.return_value = session_result

        def _capture_open(*_args, **_kwargs) -> None:
            events.append("open")

        mock_open_log.side_effect = _capture_open

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-ordering",
        )

        self._join_verification_thread()

        assert events == ["open", "wait"]

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_pins_state_dir_for_fallback_session(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        tmp_path,
    ):
        """Fallback session temporarily pins AGENTIC_DEVTOOLS_STATE_DIR to target state dir."""
        fn = self._import_fn()
        state_dir = tmp_path / ".agdt-state"
        state_dir.mkdir()
        state_file = state_dir / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")

        pending_marker = tmp_path / ".vscode" / "pending-auto-start.json"
        pending_marker.parent.mkdir(parents=True)
        pending_marker.write_text('{"run_id":"run-456"}', encoding="utf-8")

        original_state_dir = "/tmp/original-state-dir"
        with patch.dict(os.environ, {"AGENTIC_DEVTOOLS_STATE_DIR": original_state_dir}, clear=False):
            observed: dict[str, str | None] = {}

            def _capture_state_dir(**kwargs):
                observed["during_call"] = os.environ.get("AGENTIC_DEVTOOLS_STATE_DIR")
                return None

            mock_copilot.side_effect = _capture_state_dir

            fn(
                worktree_path=str(tmp_path),
                start_prompt="test prompt",
                workflow_name="test-workflow",
            )

            self._join_verification_thread()

            assert observed["during_call"] == str(state_dir)
            assert os.environ.get("AGENTIC_DEVTOOLS_STATE_DIR") == original_state_dir

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch(f"{_MODULE}._open_log_in_vscode")
    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_opens_log_when_vscode_available(
        self,
        _mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_vscode,
        mock_open_log,
        mock_test_env,
        tmp_path,
    ):
        """Verify _open_log_in_vscode is called when session has a log file."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "")

        session_result = MagicMock()
        session_result.process = MagicMock()
        session_result.process.wait.return_value = 0
        session_result.log_file = "/tmp/copilot.log"
        mock_copilot.return_value = session_result

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="run-open-log",
        )

        self._join_verification_thread()

        mock_open_log.assert_called_once_with("/tmp/copilot.log", str(tmp_path))

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    def test_handles_exception_in_fallback(
        self,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        tmp_path,
        capsys,
    ):
        """Missing claim context skips fallback startup and preserves retry artifacts."""
        fn = self._import_fn()
        mock_resolve.return_value = (None, "")
        mock_copilot.side_effect = RuntimeError("boom")

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
        )

        self._join_verification_thread()

        captured = capsys.readouterr()
        mock_copilot.assert_not_called()
        assert "Skipping fallback startup to avoid an unclaimed duplicate session" in captured.err

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    def test_skips_fallback_when_pending_marker_is_invalid_json(
        self,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        tmp_path,
        capsys,
    ):
        """Invalid marker run_id fails closed instead of launching unclaimed fallback."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        pending_marker = tmp_path / ".vscode" / "pending-auto-start.json"
        pending_marker.parent.mkdir(parents=True)
        pending_marker.write_text("{", encoding="utf-8")
        mock_resolve.return_value = (state_file, "")
        mock_copilot.return_value = None

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
        )

        self._join_verification_thread()

        mock_copilot.assert_not_called()
        assert "Skipping fallback startup to avoid an unclaimed duplicate session" in capsys.readouterr().err

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    def test_skips_fallback_when_pending_marker_run_id_not_string(
        self,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        tmp_path,
        capsys,
    ):
        """Non-string marker run_id fails closed instead of launching unclaimed fallback."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        pending_marker = tmp_path / ".vscode" / "pending-auto-start.json"
        pending_marker.parent.mkdir(parents=True)
        pending_marker.write_text('{"run_id":123}', encoding="utf-8")
        mock_resolve.return_value = (state_file, "")
        mock_copilot.return_value = None

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
        )

        self._join_verification_thread()

        mock_copilot.assert_not_called()
        assert "Skipping fallback startup to avoid an unclaimed duplicate session" in capsys.readouterr().err

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    def test_skips_fallback_when_pending_marker_is_not_object(
        self,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        tmp_path,
        capsys,
    ):
        """Non-object marker JSON fails closed without launching unclaimed fallback."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        pending_marker = tmp_path / ".vscode" / "pending-auto-start.json"
        pending_marker.parent.mkdir(parents=True)
        pending_marker.write_text('["run-789"]', encoding="utf-8")
        mock_resolve.return_value = (state_file, "")
        mock_copilot.return_value = None

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
        )

        self._join_verification_thread()

        mock_copilot.assert_not_called()
        assert "Skipping fallback startup to avoid an unclaimed duplicate session" in capsys.readouterr().err

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch(f"{_MODULE}._open_log_in_vscode")
    @patch(f"{_MODULE}.is_vscode_available", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    def test_skips_fallback_when_no_state_file_but_has_run_id(
        self,
        mock_resolve,
        mock_copilot,
        mock_vscode,
        mock_open_log,
        mock_test_env,
        tmp_path,
        capsys,
    ):
        """Missing state file fails closed even when a run ID is present."""
        fn = self._import_fn()
        # state_file_path is None, but state_run_id has a value
        mock_resolve.return_value = (None, "run-123")
        mock_copilot.return_value = None

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
        )

        self._join_verification_thread()

        mock_copilot.assert_not_called()
        assert "Skipping fallback startup to avoid an unclaimed duplicate session" in capsys.readouterr().err

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered")
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.05)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_prefers_injected_run_id_over_state(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_test_env,
        tmp_path,
    ):
        """The injected run_id is polled for, not the (possibly-mutated) state run_id (#2161).

        Regression for the duplicate-session bug: a nested setup command overwrites
        agdt_run_id after the VS Code task was injected with a different run ID. The
        verification must poll for the *injected* run ID (which the task marks as
        triggered), not the stale state value — otherwise it spuriously starts a
        duplicate fallback session.
        """
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        # State holds a DIFFERENT (mutated) run id than what was injected.
        mock_resolve.return_value = (state_file, "state-B")

        # The auto-start task marked only the INJECTED run id as triggered.
        def _only_injected_triggered(_state_path, run_id):
            return run_id == "injected-A"

        mock_triggered.side_effect = _only_injected_triggered

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="injected-A",
        )

        self._join_verification_thread()

        # Verification polled for the injected run id and found it triggered —
        # so NO duplicate fallback session was started.
        mock_copilot.assert_not_called()
        polled_run_ids = {call.args[1] for call in mock_triggered.call_args_list}
        assert "injected-A" in polled_run_ids
        assert "state-B" not in polled_run_ids

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch(f"{_MODULE}._open_log_in_vscode")
    @patch(f"{_MODULE}.is_vscode_available", return_value=False)
    @patch("agentic_devtools.cli.copilot.session.start_copilot_session")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch("agentic_devtools.cli.copilot.auto_start._is_run_triggered", return_value=False)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_DELAY_S", 0.01)
    @patch(f"{_MODULE}._AUTOSTART_VERIFICATION_POLL_S", 0.005)
    def test_injected_run_id_not_triggered_falls_back(
        self,
        mock_triggered,
        mock_resolve,
        mock_copilot,
        mock_vscode,
        mock_open_log,
        mock_test_env,
        tmp_path,
    ):
        """When the injected run_id is never triggered, the fallback still starts."""
        fn = self._import_fn()
        state_file = tmp_path / "state.json"
        state_file.write_text("{}")
        mock_resolve.return_value = (state_file, "state-B")
        mock_copilot.return_value = None

        fn(
            worktree_path=str(tmp_path),
            start_prompt="test prompt",
            workflow_name="test-workflow",
            run_id="injected-A",
        )

        self._join_verification_thread()

        # Polled for the injected run id; never triggered -> fallback started.
        polled_run_ids = {call.args[1] for call in mock_triggered.call_args_list}
        assert polled_run_ids == {"injected-A"}
        mock_copilot.assert_called_once()
