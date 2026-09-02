"""Tests for _terminate_worktree_setup_process_tree."""

import subprocess
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.workflows.worktree_setup import (
    _SETUP_SCRIPT_KILL_WAIT_SECONDS,
    _terminate_worktree_setup_process_tree,
)


class TestTerminateWorktreeSetupProcessTree:
    """Tests for _terminate_worktree_setup_process_tree function."""

    def test_windows_uses_taskkill_and_waits(self):
        """Test that Windows uses taskkill for the full process tree."""
        proc = MagicMock()
        proc.pid = 321

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"),
            patch(
                "agentic_devtools.cli.workflows.worktree_setup.subprocess.run",
                return_value=MagicMock(returncode=0),
            ) as mock_run,
        ):
            _terminate_worktree_setup_process_tree(proc)

        mock_run.assert_called_once_with(
            ["taskkill", "/PID", "321", "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            shell=False,
            timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS,
        )
        proc.kill.assert_not_called()
        proc.wait.assert_called_once_with(timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS)

    def test_windows_falls_back_to_proc_kill_when_taskkill_fails(self):
        """Test that Windows falls back to proc.kill when taskkill cannot be launched."""
        proc = MagicMock()
        proc.pid = 321

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"),
            patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run", side_effect=OSError("missing")),
        ):
            _terminate_worktree_setup_process_tree(proc)

        proc.kill.assert_called_once_with()
        proc.wait.assert_called_once_with(timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS)

    def test_windows_falls_back_to_proc_kill_when_taskkill_times_out(self):
        """Test that Windows falls back to proc.kill when taskkill exceeds the timeout."""
        proc = MagicMock()
        proc.pid = 321

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"),
            patch(
                "agentic_devtools.cli.workflows.worktree_setup.subprocess.run",
                side_effect=subprocess.TimeoutExpired("taskkill", _SETUP_SCRIPT_KILL_WAIT_SECONDS),
            ),
        ):
            _terminate_worktree_setup_process_tree(proc)

        proc.kill.assert_called_once_with()
        proc.wait.assert_called_once_with(timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS)

    def test_windows_falls_back_to_proc_kill_when_taskkill_returns_nonzero(self):
        """Test that Windows falls back to proc.kill when taskkill exits non-zero."""
        proc = MagicMock()
        proc.pid = 321

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"),
            patch(
                "agentic_devtools.cli.workflows.worktree_setup.subprocess.run",
                return_value=MagicMock(returncode=1),
            ),
        ):
            _terminate_worktree_setup_process_tree(proc)

        proc.kill.assert_called_once_with()
        proc.wait.assert_called_once_with(timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS)

    def test_windows_suppresses_proc_kill_errors_during_fallback(self):
        """Test that Windows fallback kill errors are suppressed."""
        proc = MagicMock()
        proc.pid = 321
        proc.kill.side_effect = OSError("already exited")

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"),
            patch(
                "agentic_devtools.cli.workflows.worktree_setup.subprocess.run",
                return_value=MagicMock(returncode=1),
            ),
        ):
            _terminate_worktree_setup_process_tree(proc)

        proc.kill.assert_called_once_with()
        proc.wait.assert_called_once_with(timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS)

    def test_posix_kills_process_group(self):
        """Test that POSIX systems kill the full process group."""
        proc = MagicMock()
        proc.pid = 654

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Linux"),
            patch("agentic_devtools.cli.workflows.worktree_setup.os.killpg", create=True) as mock_killpg,
            patch("agentic_devtools.cli.workflows.worktree_setup.signal.SIGKILL", 9, create=True),
        ):
            _terminate_worktree_setup_process_tree(proc)

        mock_killpg.assert_called_once_with(654, 9)
        proc.kill.assert_not_called()
        proc.wait.assert_called_once_with(timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS)

    def test_posix_falls_back_to_proc_kill_when_killpg_fails(self):
        """Test that POSIX systems fall back to proc.kill when killpg fails."""
        proc = MagicMock()
        proc.pid = 654

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Linux"),
            patch(
                "agentic_devtools.cli.workflows.worktree_setup.os.killpg",
                side_effect=ProcessLookupError("gone"),
                create=True,
            ),
            patch("agentic_devtools.cli.workflows.worktree_setup.signal.SIGKILL", 9, create=True),
        ):
            _terminate_worktree_setup_process_tree(proc)

        proc.kill.assert_called_once_with()
        proc.wait.assert_called_once_with(timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS)

    def test_posix_suppresses_proc_kill_errors_during_fallback(self):
        """Test that POSIX fallback kill errors are suppressed."""
        proc = MagicMock()
        proc.pid = 654
        proc.kill.side_effect = OSError("already exited")

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Linux"),
            patch(
                "agentic_devtools.cli.workflows.worktree_setup.os.killpg",
                side_effect=ProcessLookupError("gone"),
                create=True,
            ),
            patch("agentic_devtools.cli.workflows.worktree_setup.signal.SIGKILL", 9, create=True),
        ):
            _terminate_worktree_setup_process_tree(proc)

        proc.kill.assert_called_once_with()
        proc.wait.assert_called_once_with(timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS)

    def test_wait_timeout_is_suppressed(self):
        """Test that a bounded wait timeout after termination is suppressed."""
        proc = MagicMock()
        proc.pid = 654
        proc.wait.side_effect = subprocess.TimeoutExpired("python", _SETUP_SCRIPT_KILL_WAIT_SECONDS)

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Linux"),
            patch("agentic_devtools.cli.workflows.worktree_setup.os.killpg", create=True),
            patch("agentic_devtools.cli.workflows.worktree_setup.signal.SIGKILL", 9, create=True),
        ):
            _terminate_worktree_setup_process_tree(proc)
