"""Tests for run_worktree_setup_script."""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.workflows.worktree_setup import run_worktree_setup_script


def _make_popen_mock(returncode=0, stderr="", communicate_side_effect=None):
    """Return (popen_cls_mock, proc_mock) configured for bounded stderr + wait()."""
    mock_proc = MagicMock()
    mock_proc.returncode = returncode
    mock_proc.stderr = MagicMock()
    mock_proc.stderr.read.side_effect = [stderr, ""]
    mock_popen = MagicMock()

    if communicate_side_effect is not None:
        # First wait() raises timeout; post-kill wait() succeeds.
        mock_proc.wait.side_effect = [communicate_side_effect, None]
    else:
        mock_proc.wait.return_value = 0

    def _popen(*args, **kwargs):
        return mock_proc

    mock_popen.side_effect = _popen
    return mock_popen, mock_proc


class TestRunWorktreeSetupScript:
    """Tests for run_worktree_setup_script function."""

    def test_no_op_when_script_absent(self, tmp_path):
        """Test that the function does nothing when the setup script is missing."""
        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen") as mock_popen:
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "missing"
        mock_popen.assert_not_called()

    def test_fails_on_permission_error_checking_script_path(self, tmp_path, capsys):
        """PermissionError on lstat must not be silently treated as missing."""
        with patch(
            "agentic_devtools.cli.workflows.worktree_setup.os.lstat",
            side_effect=PermissionError("permission denied"),
        ):
            with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen") as mock_popen:
                result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.category == "validation"
        mock_popen.assert_not_called()
        captured = capsys.readouterr()
        assert "target setup script failure" in captured.err

    def test_fails_when_path_is_directory(self, tmp_path):
        """Test that a directory at the script path is an invalid-path failure."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        # Create a *directory* where the script should be
        (script_dir / "agentic-devtools-worktree-setup.py").mkdir()

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen") as mock_popen:
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.category == "invalid-path"
        mock_popen.assert_not_called()

    def test_fails_when_script_not_readable(self, tmp_path):
        """Test that a non-readable script file returns a validation failure."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        script = script_dir / "agentic-devtools-worktree-setup.py"
        script.write_text("", encoding="utf-8")

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen") as mock_popen:
            with patch("agentic_devtools.cli.workflows.worktree_setup.os.access", return_value=False):
                result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.category == "validation"
        mock_popen.assert_not_called()

    def test_executes_script_when_present(self, tmp_path):
        """Test that the script is executed when it exists."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        script = script_dir / "agentic-devtools-worktree-setup.py"
        script.write_text("print('setup')", encoding="utf-8")

        mock_popen, _ = _make_popen_mock(returncode=0, stderr="")

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "succeeded"
        assert result.exit_code == 0
        mock_popen.assert_called_once()
        args, kwargs = mock_popen.call_args
        assert args == ([sys.executable, str(script.resolve()), str(tmp_path.resolve())],)
        assert kwargs["cwd"] == str(tmp_path.resolve())
        assert kwargs["stdout"] == subprocess.DEVNULL
        assert kwargs["encoding"] == "utf-8"
        assert kwargs["errors"] == "replace"
        assert kwargs["stderr"] == subprocess.PIPE
        if sys.platform == "win32":
            assert "creationflags" in kwargs
        else:
            assert kwargs["start_new_session"] is True

    def test_uses_caller_supplied_timeout(self, tmp_path):
        """Pass the configured timeout to the target setup process."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        script = script_dir / "agentic-devtools-worktree-setup.py"
        script.write_text("print('setup')", encoding="utf-8")

        mock_popen, mock_proc = _make_popen_mock(returncode=0, stderr="")

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path), timeout_seconds=120)

        assert result.status == "succeeded"
        mock_proc.wait.assert_called_once_with(timeout=120)

    def test_executes_script_with_windows_process_group(self, tmp_path):
        """Test that the Windows launch path uses a dedicated process group."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        script = script_dir / "agentic-devtools-worktree-setup.py"
        script.write_text("print('setup')", encoding="utf-8")

        mock_popen, _ = _make_popen_mock(returncode=0, stderr="")

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"),
            patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen),
        ):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "succeeded"
        _, kwargs = mock_popen.call_args
        assert "creationflags" in kwargs
        assert "start_new_session" not in kwargs

    def test_executes_script_with_posix_process_group(self, tmp_path):
        """Test that the POSIX launch path starts a new process session."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        script = script_dir / "agentic-devtools-worktree-setup.py"
        script.write_text("print('setup')", encoding="utf-8")

        mock_popen, _ = _make_popen_mock(returncode=0, stderr="")

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Linux"),
            patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen),
        ):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "succeeded"
        _, kwargs = mock_popen.call_args
        assert kwargs["start_new_session"] is True
        assert "creationflags" not in kwargs

    def test_prints_success_message_on_zero_exit(self, tmp_path, capsys):
        """Test that a success message is printed when the script exits cleanly."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_popen, _ = _make_popen_mock(returncode=0, stderr="")

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "succeeded"
        captured = capsys.readouterr()
        assert "completed successfully" in captured.out

    def test_warns_on_nonzero_exit(self, tmp_path, capsys):
        """Test that a warning is printed when the script exits with a non-zero code."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_popen, _ = _make_popen_mock(returncode=1, stderr="token=super-secret\nAuthorization: ****** failed")

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.exit_code == 1
        captured = capsys.readouterr()
        assert "target setup script failure" in captured.err
        assert "1" in captured.err
        assert "super-secret" not in captured.err
        assert result.error_message == "<redacted> <redacted> failed"

    def test_timeout_is_explicit_failure(self, tmp_path):
        """Test that a target setup timeout returns a bounded failure result."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_popen, _ = _make_popen_mock(communicate_side_effect=subprocess.TimeoutExpired("python", 60))

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen),
            patch("agentic_devtools.cli.workflows.worktree_setup._terminate_worktree_setup_process_tree") as mock_kill,
        ):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.exit_code is None
        assert result.category == "timeout"
        assert "60 seconds" in (result.error_message or "")
        mock_kill.assert_called_once()

    def test_timeout_post_kill_wait_also_times_out(self, tmp_path):
        """Test that a double-timeout (initial + post-kill wait) still returns a timeout failure."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_proc = MagicMock()
        mock_proc.stderr = MagicMock()
        mock_proc.stderr.read.side_effect = ["", ""]
        mock_proc.wait.side_effect = [
            subprocess.TimeoutExpired("python", 60),  # initial wait
            subprocess.TimeoutExpired("python", 5),  # post-kill drain also times out
        ]
        mock_popen = MagicMock(side_effect=lambda *a, **kw: mock_proc)

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen),
            patch("agentic_devtools.cli.workflows.worktree_setup._terminate_worktree_setup_process_tree"),
        ):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.category == "timeout"
        assert "60 seconds" in (result.error_message or "")

    def test_nonzero_without_stderr_uses_fallback_diagnostic(self, tmp_path):
        """Test that a non-zero script without stderr still has an actionable summary."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_popen, _ = _make_popen_mock(returncode=1, stderr="")

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.error_message == "setup script exited without diagnostic output"

    def test_nonzero_with_missing_stderr_pipe_uses_fallback_diagnostic(self, tmp_path):
        """Test fallback diagnostic when the process has no stderr pipe."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stderr = None
        mock_proc.wait.return_value = 0
        mock_popen = MagicMock(side_effect=lambda *a, **kw: mock_proc)

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.error_message == "setup script exited without diagnostic output"

    def test_nonzero_stderr_read_errors_use_fallback_diagnostic(self, tmp_path):
        """Test that stderr read errors are tolerated and produce fallback diagnostics."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.wait.return_value = 0
        mock_proc.stderr = MagicMock()
        mock_proc.stderr.read.side_effect = OSError("read failed")
        mock_popen = MagicMock(side_effect=lambda *a, **kw: mock_proc)

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.error_message == "setup script exited without diagnostic output"

    def test_diagnostic_is_truncated(self, tmp_path):
        """Test that untrusted stderr is sanitized and limited to 4096 characters."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_popen, _ = _make_popen_mock(returncode=1, stderr="x" * 5000)

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert len(result.error_message or "") == 4096

    def test_stderr_capture_discards_chunks_after_limit(self, tmp_path):
        """Test that stderr chunks beyond the cap are discarded before sanitization."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.wait.return_value = 0
        mock_proc.stderr = MagicMock()
        mock_proc.stderr.read.side_effect = ["x" * 5000, "y" * 50, ""]
        mock_proc.stderr.fileno.return_value = -1
        mock_popen = MagicMock(side_effect=lambda *a, **kw: mock_proc)

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert len(result.error_message or "") == 4096

    def test_stderr_capture_expands_for_long_configured_secret(self, tmp_path, monkeypatch):
        """Test that stderr capture grows enough to redact a long configured secret at the boundary."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        long_secret_prefix = "long-boundary-secret-prefix"
        long_secret = long_secret_prefix + ("z" * 900)
        monkeypatch.setenv("GITHUB_TOKEN", long_secret)

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.wait.return_value = 0
        mock_proc.stderr = MagicMock()
        mock_proc.stderr.read.side_effect = ["x" * (4096 - len(long_secret_prefix)) + long_secret, ""]
        mock_popen = MagicMock(side_effect=lambda *a, **kw: mock_proc)

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert long_secret_prefix not in (result.error_message or "")
        assert "[REDACTED]" in (result.error_message or "")

    def test_stderr_capture_thread_timeout_uses_fallback_diagnostic(self, tmp_path):
        """Test that an alive stderr reader thread yields a safe fallback diagnostic."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.wait.return_value = 0
        mock_proc.stderr = MagicMock()
        mock_proc.stderr.read.return_value = ""
        mock_popen = MagicMock(side_effect=lambda *a, **kw: mock_proc)

        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = True

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen),
            patch("agentic_devtools.cli.workflows.worktree_setup.threading.Thread", return_value=mock_thread),
        ):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.error_message == "setup script exited without diagnostic output"

    def test_stderr_capture_preserves_chunks_when_thread_stays_alive(self, tmp_path):
        """Test that already-captured stderr is preserved even if the reader still appears alive."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.wait.return_value = 0
        mock_proc.stderr = MagicMock()
        mock_proc.stderr.read.side_effect = ["provider setup failed", ""]
        mock_popen = MagicMock(side_effect=lambda *a, **kw: mock_proc)

        class _AliveAfterStartThread:
            def __init__(self, target, *args, **kwargs):
                self._target = target

            def start(self):
                self._target()

            def join(self, timeout=None):
                return None

            def is_alive(self):
                return True

        with (
            patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen),
            patch(
                "agentic_devtools.cli.workflows.worktree_setup.threading.Thread",
                side_effect=lambda *args, **kwargs: _AliveAfterStartThread(*args, **kwargs),
            ),
        ):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.error_message == "provider setup failed"

    def test_fails_on_os_error(self, tmp_path, capsys):
        """Test that an OSError during script execution results in a terminal execution failure."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        with patch(
            "agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen",
            side_effect=OSError("permission denied"),
        ):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.category == "execution"
        captured = capsys.readouterr()
        assert "target setup script failure" in captured.err

    def test_fails_on_file_not_found_error(self, tmp_path, capsys):
        """Test that a FileNotFoundError during script execution results in a terminal execution failure."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        (script_dir / "agentic-devtools-worktree-setup.py").write_text("", encoding="utf-8")

        with patch(
            "agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen",
            side_effect=FileNotFoundError("python not found"),
        ):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.category == "execution"
        captured = capsys.readouterr()
        assert "target setup script failure" in captured.err

    def test_prints_script_path_before_running(self, tmp_path, capsys):
        """Test that the script path is printed before execution."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        script = script_dir / "agentic-devtools-worktree-setup.py"
        script.write_text("", encoding="utf-8")

        mock_popen, _ = _make_popen_mock(returncode=0, stderr="")

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen", mock_popen):
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "succeeded"
        captured = capsys.readouterr()
        assert str(script.resolve()) in captured.out

    def test_rejects_symlink_script(self, tmp_path, capsys):
        """Test that a symlinked setup script is refused with a warning."""
        # Create the .agdt dir and a real target file inside the worktree
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        real_file = tmp_path / "real_setup.py"
        real_file.write_text("print('evil')", encoding="utf-8")
        symlink = script_dir / "agentic-devtools-worktree-setup.py"
        try:
            symlink.symlink_to(real_file)
        except OSError:
            pytest.skip("Symlink creation not supported on this platform/configuration")

        with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen") as mock_popen:
            result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.category == "validation"
        mock_popen.assert_not_called()
        captured = capsys.readouterr()
        assert "target setup script failure" in captured.err
        assert "symlink" in captured.err

    def test_rejects_symlink_script_via_mock(self, tmp_path, capsys):
        """Test symlink rejection via mock (works on Windows without symlink privileges).

        Covers lines 1798-1802.
        """
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        script = script_dir / "agentic-devtools-worktree-setup.py"
        script.write_text("", encoding="utf-8")

        with patch.object(type(script), "is_symlink", return_value=True):
            with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen") as mock_popen:
                result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.category == "validation"
        mock_popen.assert_not_called()
        captured = capsys.readouterr()
        assert "target setup script failure" in captured.err
        assert "symlink" in captured.err

    def test_rejects_script_resolving_outside_worktree(self, tmp_path, capsys):
        """Test that a script resolving outside the worktree root is refused."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        script = script_dir / "agentic-devtools-worktree-setup.py"
        script.write_text("", encoding="utf-8")

        outside_path = tmp_path.parent / "evil.py"

        # The implementation calls Path.resolve() twice: first for worktree_root,
        # then for the script path. We use a counter so that only the second call
        # (for the script) returns an outside path; the first call returns normally.
        _real_resolve = Path.resolve
        _calls = [0]

        def _mock_resolve(self):
            _calls[0] += 1
            if _calls[0] == 1:
                return _real_resolve(self)
            return outside_path

        with patch.object(Path, "resolve", _mock_resolve):
            with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen") as mock_popen:
                result = run_worktree_setup_script(str(tmp_path))

        assert result.status == "failed"
        assert result.category == "validation"
        mock_popen.assert_not_called()
        captured = capsys.readouterr()
        assert "target setup script failure" in captured.err
        assert "outside worktree" in captured.err

    def test_fails_on_os_error_during_path_validation(self, tmp_path, capsys):
        """Test that an OSError during path validation results in a terminal validation failure."""
        script_dir = tmp_path / ".agdt"
        script_dir.mkdir()
        script = script_dir / "agentic-devtools-worktree-setup.py"
        script.write_text("", encoding="utf-8")

        with patch.object(type(script), "is_symlink", side_effect=OSError("stat failed")):
            with patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.Popen") as mock_popen:
                run_worktree_setup_script(str(tmp_path))

        mock_popen.assert_not_called()
        captured = capsys.readouterr()
        assert "target setup script failure" in captured.err
        assert "validation" in captured.err

    def test_rejects_negative_timeout(self, tmp_path):
        """Reject a negative timeout before attempting to run the script."""
        with pytest.raises(ValueError, match="timeout_seconds must be non-negative"):
            run_worktree_setup_script(str(tmp_path), timeout_seconds=-1)
