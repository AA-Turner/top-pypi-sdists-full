"""Tests for server manager service."""

from __future__ import annotations

import json
import signal
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from anteroom.services.server_manager import (
    _CREATE_NEW_PROCESS_GROUP,
    _CREATE_NO_WINDOW,
    _MAX_LOG_BYTES,
    ServerManager,
    ServerStatus,
    _terminate_unix,
    _terminate_windows,
)

_MODULE = "anteroom.services.server_manager"


class TestServerStatus:
    def test_frozen_dataclass(self) -> None:
        status = ServerStatus(pid=123, port=8080, alive=True, responding=True, start_time=1.0, log_path=Path("/tmp"))
        assert status.pid == 123
        assert status.port == 8080
        assert status.alive is True
        assert status.responding is True
        with pytest.raises(AttributeError):
            status.pid = 456  # type: ignore[misc]


class TestServerManagerInit:
    def test_default_paths(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path, host="127.0.0.1", port=8080)
        assert mgr.pid_path == tmp_path / "anteroom-web-8080.pid"
        assert mgr.log_path == tmp_path / "anteroom-web.log"
        assert mgr.host == "127.0.0.1"
        assert mgr.port == 8080

    def test_custom_port_in_pid_filename(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path, port=9090)
        assert mgr.pid_path == tmp_path / "anteroom-web-9090.pid"

    def test_defaults(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        assert mgr.host == "127.0.0.1"
        assert mgr.port == 8080


class TestPidFileOperations:
    def test_write_and_read_pid(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(12345)
        assert mgr.read_pid() == 12345

    def test_write_pid_creates_data_dir(self, tmp_path: Path) -> None:
        nested = tmp_path / "sub" / "dir"
        mgr = ServerManager(data_dir=nested)
        mgr.write_pid(100)
        assert nested.exists()
        assert mgr.read_pid() == 100

    def test_read_pid_missing_file(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        assert mgr.read_pid() is None

    def test_read_pid_empty_file(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text("")
        assert mgr.read_pid() is None

    def test_read_pid_invalid_json(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text("not json")
        assert mgr.read_pid() is None

    def test_read_pid_missing_pid_key(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text(json.dumps({"port": 8080}))
        assert mgr.read_pid() is None

    def test_read_pid_negative_pid(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text(json.dumps({"pid": -1}))
        assert mgr.read_pid() is None

    def test_read_pid_zero_pid(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text(json.dumps({"pid": 0}))
        assert mgr.read_pid() is None

    def test_read_pid_string_pid(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text(json.dumps({"pid": "not_a_number"}))
        assert mgr.read_pid() is None

    def test_read_pid_info_returns_full_dict(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        info = mgr.read_pid_info()
        assert info is not None
        assert info["pid"] == 999
        assert info["port"] == 8080
        assert info["host"] == "127.0.0.1"
        assert "start_time" in info

    def test_read_pid_info_not_a_dict(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text(json.dumps([1, 2, 3]))
        assert mgr.read_pid_info() is None

    def test_clear_pid(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(100)
        assert mgr.pid_path.exists()
        mgr.clear_pid()
        assert not mgr.pid_path.exists()

    def test_clear_pid_missing_file(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.clear_pid()  # should not raise

    def test_read_pid_info_os_error(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text(json.dumps({"pid": 123}))
        with patch.object(Path, "read_text", side_effect=OSError("disk error")):
            assert mgr.read_pid_info() is None


class TestIsProcessAlive:
    @pytest.mark.skipif(sys.platform == "win32", reason="Unix signal test")
    def test_alive_process(self) -> None:
        with patch(f"{_MODULE}.os.kill") as mock_kill:
            mock_kill.return_value = None
            assert ServerManager.is_process_alive(12345) is True
            mock_kill.assert_called_once_with(12345, 0)

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix signal test")
    def test_dead_process(self) -> None:
        with patch(f"{_MODULE}.os.kill", side_effect=ProcessLookupError):
            assert ServerManager.is_process_alive(12345) is False

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix signal test")
    def test_permission_error_means_alive(self) -> None:
        with patch(f"{_MODULE}.os.kill", side_effect=PermissionError):
            assert ServerManager.is_process_alive(12345) is True

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix signal test")
    def test_os_error_means_dead(self) -> None:
        with patch(f"{_MODULE}.os.kill", side_effect=OSError("other")):
            assert ServerManager.is_process_alive(12345) is False

    def test_negative_pid(self) -> None:
        assert ServerManager.is_process_alive(-1) is False

    def test_zero_pid(self) -> None:
        assert ServerManager.is_process_alive(0) is False


class TestIsProcessAliveWindows:
    @patch(f"{_MODULE}.IS_WINDOWS", True)
    def test_alive_via_kernel32(self) -> None:
        mock_kernel32 = MagicMock()
        mock_kernel32.OpenProcess.return_value = 42
        mock_kernel32.CloseHandle.return_value = True
        mock_ctypes = MagicMock()
        mock_ctypes.windll.kernel32 = mock_kernel32
        with patch.dict("sys.modules", {"ctypes": mock_ctypes}):
            from anteroom.services.server_manager import _is_process_alive_windows

            assert _is_process_alive_windows(123) is True

    @patch(f"{_MODULE}.IS_WINDOWS", True)
    def test_dead_via_kernel32(self) -> None:
        mock_kernel32 = MagicMock()
        mock_kernel32.OpenProcess.return_value = 0
        mock_ctypes = MagicMock()
        mock_ctypes.windll.kernel32 = mock_kernel32
        with patch.dict("sys.modules", {"ctypes": mock_ctypes}):
            from anteroom.services.server_manager import _is_process_alive_windows

            assert _is_process_alive_windows(123) is False

    @patch(f"{_MODULE}.IS_WINDOWS", True)
    def test_os_error_returns_false(self) -> None:
        mock_kernel32 = MagicMock()
        mock_kernel32.OpenProcess.side_effect = OSError("access denied")
        mock_ctypes = MagicMock()
        mock_ctypes.windll.kernel32 = mock_kernel32
        with patch.dict("sys.modules", {"ctypes": mock_ctypes}):
            from anteroom.services.server_manager import _is_process_alive_windows

            assert _is_process_alive_windows(123) is False


class TestIsPortResponding:
    def test_port_open(self) -> None:
        with patch(f"{_MODULE}.socket.create_connection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock()
            mock_conn.return_value.__exit__ = MagicMock(return_value=False)
            assert ServerManager.is_port_responding("127.0.0.1", 8080) is True

    def test_port_closed(self) -> None:
        with patch(f"{_MODULE}.socket.create_connection", side_effect=OSError):
            assert ServerManager.is_port_responding("127.0.0.1", 8080) is False

    def test_custom_timeout(self) -> None:
        with patch(f"{_MODULE}.socket.create_connection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock()
            mock_conn.return_value.__exit__ = MagicMock(return_value=False)
            ServerManager.is_port_responding("127.0.0.1", 8080, timeout=5.0)
            mock_conn.assert_called_once_with(("127.0.0.1", 8080), timeout=5.0)


class TestGetStatus:
    def test_no_pid_file_not_responding(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        with patch.object(ServerManager, "is_port_responding", return_value=False):
            status = mgr.get_status()
        assert status.pid is None
        assert status.alive is False
        assert status.responding is False

    def test_alive_and_responding(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch.object(ServerManager, "is_port_responding", return_value=True),
        ):
            status = mgr.get_status()
        assert status.pid == 999
        assert status.alive is True
        assert status.responding is True
        assert status.start_time is not None

    def test_alive_but_not_responding(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch.object(ServerManager, "is_port_responding", return_value=False),
        ):
            status = mgr.get_status()
        assert status.alive is True
        assert status.responding is False

    def test_dead_process_stale_pid(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch.object(ServerManager, "is_port_responding", return_value=False),
        ):
            status = mgr.get_status()
        assert status.pid == 999
        assert status.alive is False
        assert status.responding is False

    def test_no_pid_but_port_responding(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        with patch.object(ServerManager, "is_port_responding", return_value=True):
            status = mgr.get_status()
        assert status.pid is None
        assert status.alive is False
        assert status.responding is True

    def test_invalid_start_time_ignored(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text(json.dumps({"pid": 999, "port": 8080, "start_time": "not_a_number"}))
        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch.object(ServerManager, "is_port_responding", return_value=True),
        ):
            status = mgr.get_status()
        assert status.start_time is None
        assert status.alive is True

    def test_negative_start_time_ignored(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text(json.dumps({"pid": 999, "port": 8080, "start_time": -100}))
        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch.object(ServerManager, "is_port_responding", return_value=True),
        ):
            status = mgr.get_status()
        assert status.start_time is None

    def test_invalid_pid_type_in_info(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.pid_path.write_text(json.dumps({"pid": "not_int", "port": 8080}))
        with patch.object(ServerManager, "is_port_responding", return_value=False):
            status = mgr.get_status()
        assert status.pid is None
        assert status.alive is False


class TestStartBackground:
    def test_launches_subprocess(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mock_proc = MagicMock()
        mock_proc.pid = 42
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc) as mock_popen,
        ):
            pid = mgr.start_background()
        assert pid == 42
        assert mgr.read_pid() == 42
        call_args = mock_popen.call_args
        cmd = call_args[0][0]
        assert cmd[0] == sys.executable
        assert "-m" in cmd
        assert "anteroom" in cmd
        assert "--_bg-worker" in cmd
        assert "--port" in cmd
        assert "8080" in cmd

    def test_raises_if_already_running(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        with patch.object(ServerManager, "is_process_alive", return_value=True):
            with pytest.raises(RuntimeError, match="already running"):
                mgr.start_background()

    def test_clears_stale_pid_and_starts(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        mock_proc = MagicMock()
        mock_proc.pid = 42

        alive_calls = [False]  # stale PID check returns False

        with (
            patch.object(ServerManager, "is_process_alive", side_effect=alive_calls),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc),
        ):
            pid = mgr.start_background()
        assert pid == 42

    def test_debug_flag_passed(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mock_proc = MagicMock()
        mock_proc.pid = 42
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc) as mock_popen,
        ):
            mgr.start_background(debug=True)
        cmd = mock_popen.call_args[0][0]
        assert "--debug" in cmd

    def test_extra_args_passed(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mock_proc = MagicMock()
        mock_proc.pid = 42
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc) as mock_popen,
        ):
            mgr.start_background(extra_args=["--tls"])
        cmd = mock_popen.call_args[0][0]
        assert "--tls" in cmd

    @patch(f"{_MODULE}.IS_WINDOWS", True)
    def test_windows_creation_flags(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mock_proc = MagicMock()
        mock_proc.pid = 42
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc) as mock_popen,
        ):
            mgr.start_background()
        kwargs = mock_popen.call_args[1]
        assert "creationflags" in kwargs
        assert kwargs["creationflags"] == _CREATE_NEW_PROCESS_GROUP | _CREATE_NO_WINDOW

    @patch(f"{_MODULE}.IS_WINDOWS", False)
    def test_unix_start_new_session(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mock_proc = MagicMock()
        mock_proc.pid = 42
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc) as mock_popen,
        ):
            mgr.start_background()
        kwargs = mock_popen.call_args[1]
        assert kwargs.get("start_new_session") is True

    def test_popen_failure_closes_log_file(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mock_log = MagicMock()
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", side_effect=OSError("exec failed")),
            patch("builtins.open", return_value=mock_log),
        ):
            with pytest.raises(OSError, match="exec failed"):
                mgr.start_background()
        mock_log.close.assert_called_once()

    def test_log_file_closed_on_success(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mock_log = MagicMock()
        mock_proc = MagicMock()
        mock_proc.pid = 42
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc),
            patch("builtins.open", return_value=mock_log),
        ):
            mgr.start_background()
        mock_log.close.assert_called_once()

    def test_write_pid_failure_kills_orphan(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mock_proc = MagicMock()
        mock_proc.pid = 42
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc),
            patch.object(ServerManager, "write_pid", side_effect=OSError("disk full")),
        ):
            with pytest.raises(OSError, match="disk full"):
                mgr.start_background()
        mock_proc.kill.assert_called_once()


class TestStop:
    def test_no_pid_file(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        assert mgr.stop() is False

    def test_stale_pid_cleans_up(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        with patch.object(ServerManager, "is_process_alive", return_value=False):
            assert mgr.stop() is False
        assert not mgr.pid_path.exists()

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix signal test")
    def test_sends_sigterm_unix(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch(f"{_MODULE}._terminate_unix", return_value=True) as mock_term,
        ):
            assert mgr.stop() is True
        mock_term.assert_called_once_with(999, 10.0)
        assert not mgr.pid_path.exists()

    @patch(f"{_MODULE}.IS_WINDOWS", True)
    def test_calls_terminate_windows(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch(f"{_MODULE}._terminate_windows", return_value=True) as mock_term,
        ):
            assert mgr.stop() is True
        mock_term.assert_called_once_with(999, 10.0)

    def test_custom_timeout(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        term_fn = f"{_MODULE}._terminate_unix" if sys.platform != "win32" else f"{_MODULE}._terminate_windows"
        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch(term_fn, return_value=True) as mock_term,
        ):
            mgr.stop(timeout=5.0)
        mock_term.assert_called_once_with(999, 5.0)


class TestTerminateUnix:
    @pytest.mark.skipif(sys.platform == "win32", reason="Unix signal test")
    def test_sigterm_and_process_exits(self) -> None:
        kill_calls = []

        def fake_kill(pid: int, sig: int) -> None:
            kill_calls.append((pid, sig))
            if sig == 0 and len(kill_calls) > 1:
                raise ProcessLookupError

        with (
            patch(f"{_MODULE}.os.kill", side_effect=fake_kill),
            patch(f"{_MODULE}.time.sleep"),
        ):
            result = _terminate_unix(999, timeout=10.0)
        assert result is True
        assert kill_calls[0] == (999, signal.SIGTERM)

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix signal test")
    def test_process_already_dead(self) -> None:
        with patch(f"{_MODULE}.os.kill", side_effect=ProcessLookupError):
            result = _terminate_unix(999, timeout=10.0)
        assert result is False

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix signal test")
    def test_permission_denied(self) -> None:
        with patch(f"{_MODULE}.os.kill", side_effect=PermissionError):
            result = _terminate_unix(999, timeout=10.0)
        assert result is False

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix signal test")
    def test_sigkill_after_timeout(self) -> None:
        kill_calls = []

        def fake_kill(pid: int, sig: int) -> None:
            kill_calls.append((pid, sig))
            if sig == signal.SIGKILL:
                return

        with (
            patch(f"{_MODULE}.os.kill", side_effect=fake_kill),
            patch(f"{_MODULE}.time.sleep"),
            patch(f"{_MODULE}.time.monotonic", side_effect=[0.0, 100.0]),
        ):
            result = _terminate_unix(999, timeout=1.0)
        assert result is True
        sigs_sent = [s for _, s in kill_calls]
        assert signal.SIGTERM in sigs_sent
        assert signal.SIGKILL in sigs_sent


class TestTerminateWindows:
    def test_successful_termination(self) -> None:
        mock_kernel32 = MagicMock()
        mock_kernel32.OpenProcess.return_value = 42
        mock_kernel32.TerminateProcess.return_value = True
        mock_kernel32.CloseHandle.return_value = True
        mock_ctypes = MagicMock()
        mock_ctypes.windll.kernel32 = mock_kernel32
        with patch.dict("sys.modules", {"ctypes": mock_ctypes}):
            result = _terminate_windows(999, timeout=10.0)
        assert result is True

    def test_open_process_fails(self) -> None:
        mock_kernel32 = MagicMock()
        mock_kernel32.OpenProcess.return_value = 0
        mock_ctypes = MagicMock()
        mock_ctypes.windll.kernel32 = mock_kernel32
        with patch.dict("sys.modules", {"ctypes": mock_ctypes}):
            result = _terminate_windows(999, timeout=10.0)
        assert result is False


class TestProgressFile:
    def test_progress_path_naming(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path, port=9090)
        assert mgr.progress_path == tmp_path / "anteroom-web-9090.progress"

    def test_clear_progress_removes_file(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.progress_path.write_text("data")
        mgr.clear_progress()
        assert not mgr.progress_path.exists()

    def test_clear_progress_missing_file(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.clear_progress()  # should not raise

    def test_start_background_clears_stale_progress(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.progress_path.write_text("stale data")
        mock_proc = MagicMock()
        mock_proc.pid = 42
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc),
        ):
            mgr.start_background()
        assert not mgr.progress_path.exists()

    def test_stop_clears_progress(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.write_pid(999)
        mgr.progress_path.write_text("progress data")
        term_fn = f"{_MODULE}._terminate_unix" if sys.platform != "win32" else f"{_MODULE}._terminate_windows"
        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch(term_fn, return_value=True),
        ):
            mgr.stop()
        assert not mgr.progress_path.exists()


class TestLogRotation:
    def test_truncates_large_log(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.log_path.write_text("x" * (_MAX_LOG_BYTES + 1))
        mgr._rotate_log()
        assert mgr.log_path.stat().st_size == 0

    def test_keeps_small_log(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        content = "some log content"
        mgr.log_path.write_text(content)
        mgr._rotate_log()
        assert mgr.log_path.read_text() == content

    def test_no_log_file(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr._rotate_log()  # should not raise

    def test_os_error_on_stat(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        mgr.log_path.write_text("data")
        with patch.object(Path, "stat", side_effect=OSError("permission denied")):
            mgr._rotate_log()  # should not raise


class TestServiceScopedFiles:
    def test_default_service_is_web(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path, port=8080)
        assert mgr.service_name == "web"
        assert mgr.pid_path == tmp_path / "anteroom-web-8080.pid"
        assert mgr.progress_path == tmp_path / "anteroom-web-8080.progress"
        assert mgr.log_path == tmp_path / "anteroom-web.log"

    def test_docs_service_produces_docs_paths(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path, port=8400, service_name="docs")
        assert mgr.pid_path == tmp_path / "anteroom-docs-8400.pid"
        assert mgr.progress_path == tmp_path / "anteroom-docs-8400.progress"
        assert mgr.log_path == tmp_path / "anteroom-docs.log"

    def test_disjoint_paths_across_services(self, tmp_path: Path) -> None:
        web = ServerManager(data_dir=tmp_path, port=8080, service_name="web")
        docs = ServerManager(data_dir=tmp_path, port=8400, service_name="docs")
        assert web.pid_path != docs.pid_path
        assert web.log_path != docs.log_path
        assert web.progress_path != docs.progress_path

    def test_start_background_uses_configured_bg_worker_flag(self, tmp_path: Path) -> None:
        mgr = ServerManager(
            data_dir=tmp_path,
            port=8400,
            service_name="docs",
            bg_worker_flag="--_bg-worker-docs",
        )
        mock_proc = MagicMock()
        mock_proc.pid = 99
        with (
            patch.object(ServerManager, "is_process_alive", return_value=False),
            patch(f"{_MODULE}.subprocess.Popen", return_value=mock_proc) as mock_popen,
        ):
            mgr.start_background()
        cmd = mock_popen.call_args[0][0]
        assert "--_bg-worker-docs" in cmd
        assert "--_bg-worker" not in [c for c in cmd if c == "--_bg-worker"]

    def test_default_bg_worker_flag(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path)
        assert mgr.bg_worker_flag == "--_bg-worker"

    def test_disjoint_pid_reads_across_services(self, tmp_path: Path) -> None:
        web = ServerManager(data_dir=tmp_path, port=8080, service_name="web")
        docs = ServerManager(data_dir=tmp_path, port=8080, service_name="docs")
        docs.write_pid(222)
        # The web manager should not see the docs PID.
        assert web.read_pid() is None
        assert docs.read_pid() == 222


class TestLegacyPidFallback:
    def test_legacy_pid_path_fallback_on_read(self, tmp_path: Path) -> None:
        """A legacy `anteroom-{port}.pid` (pre-service-name) must still be honoured."""
        legacy = tmp_path / "anteroom-8080.pid"
        legacy.write_text(json.dumps({"pid": 42, "port": 8080, "start_time": 1.0}))
        mgr = ServerManager(data_dir=tmp_path, port=8080)
        assert mgr.read_pid() == 42

    def test_new_start_writes_prefixed_filename(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path, port=8080)
        mgr.write_pid(123)
        assert (tmp_path / "anteroom-web-8080.pid").exists()
        assert not (tmp_path / "anteroom-8080.pid").exists()


class TestDiscoverPidPorts:
    def test_empty_data_dir_returns_empty_list(self, tmp_path: Path) -> None:
        assert ServerManager.discover_pid_ports(tmp_path, "docs") == []

    def test_returns_sorted_ports(self, tmp_path: Path) -> None:
        (tmp_path / "anteroom-docs-9400.pid").write_text("{}")
        (tmp_path / "anteroom-docs-8400.pid").write_text("{}")
        assert ServerManager.discover_pid_ports(tmp_path, "docs") == [8400, 9400]

    def test_non_integer_segment_skipped(self, tmp_path: Path) -> None:
        (tmp_path / "anteroom-docs-foo.pid").write_text("{}")
        (tmp_path / "anteroom-docs-8400.pid").write_text("{}")
        assert ServerManager.discover_pid_ports(tmp_path, "docs") == [8400]

    def test_service_name_filter(self, tmp_path: Path) -> None:
        (tmp_path / "anteroom-web-8080.pid").write_text("{}")
        (tmp_path / "anteroom-docs-8400.pid").write_text("{}")
        assert ServerManager.discover_pid_ports(tmp_path, "docs") == [8400]
        assert ServerManager.discover_pid_ports(tmp_path, "web") == [8080]


class TestGetStatusHostFromPidInfo:
    def test_get_status_uses_host_from_pid_info_when_present(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path, host="127.0.0.1", port=8400, service_name="docs")
        mgr.pid_path.write_text(json.dumps({"pid": 12345, "host": "192.0.2.1", "port": 8400, "start_time": 1.0}))
        captured: list[tuple[str, int]] = []

        def fake_probe(host: str, port: int, timeout: float = 1.0) -> bool:
            captured.append((host, port))
            return True

        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch.object(ServerManager, "is_port_responding", staticmethod(fake_probe)),
        ):
            mgr.get_status()
        assert captured, "is_port_responding was not invoked"
        assert captured[0][0] == "192.0.2.1"
        assert captured[0][1] == 8400

    def test_get_status_falls_back_to_self_host_when_pid_missing_host_field(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path, host="10.0.0.5", port=8400, service_name="docs")
        mgr.pid_path.write_text(json.dumps({"pid": 12345, "port": 8400, "start_time": 1.0}))
        captured: list[tuple[str, int]] = []

        def fake_probe(host: str, port: int, timeout: float = 1.0) -> bool:
            captured.append((host, port))
            return True

        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch.object(ServerManager, "is_port_responding", staticmethod(fake_probe)),
        ):
            mgr.get_status()
        assert captured[0][0] == "10.0.0.5"

    def test_get_status_port_matches_pid_info_when_discovered(self, tmp_path: Path) -> None:
        mgr = ServerManager(data_dir=tmp_path, host="127.0.0.1", port=8400, service_name="docs")
        # The PID file records a *different* port than the instance attribute —
        # that happens when lifecycle commands construct a manager and then
        # read from an existing PID file.
        mgr.pid_path.write_text(json.dumps({"pid": 12345, "host": "127.0.0.1", "port": 9400, "start_time": 1.0}))
        with (
            patch.object(ServerManager, "is_process_alive", return_value=True),
            patch.object(ServerManager, "is_port_responding", staticmethod(lambda h, p, timeout=1.0: True)),
        ):
            status = mgr.get_status()
        assert status.port == 9400
