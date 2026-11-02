import ctypes
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import windows_process_cleanup, windows_process_tree
from agentic_devtools.cli.ci.windows_process_tree import run_bounded_process


def _python_command(source: str) -> list[str]:
    return [sys.executable, "-c", source]


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows process ownership")
def test_worker_base_exception_does_not_skip_resource_cleanup(monkeypatch: pytest.MonkeyPatch) -> None:
    api = Mock()
    api.CloseHandle.return_value = 1
    monkeypatch.setattr(windows_process_tree, "_win_dll", lambda _name: api)
    first, second, third = Mock(), Mock(), Mock()
    first.close.side_effect = KeyboardInterrupt("worker close interruption")
    process_handle = Mock()
    process = Mock(stdout=first, stderr=second, stdin=third)
    process._handle = process_handle

    errors = getattr(windows_process_tree, "_close_process_resources")(process, 17)

    assert errors == ("Stream close failed in worker: worker close interruption",)
    first.close.assert_called_once()
    second.close.assert_called_once()
    third.close.assert_called_once()
    api.CloseHandle.assert_called_once_with(17)
    process_handle.Close.assert_called_once()


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows process ownership")
def test_worker_base_exception_diagnostic_preserves_primary_cancellation(monkeypatch: pytest.MonkeyPatch) -> None:
    primary = KeyboardInterrupt("caller cancellation")
    close_calls: list[object] = []

    def close_stream(stream: object, timeout: float) -> None:
        close_calls.append(stream)
        if len(close_calls) == 1:
            raise RuntimeError("Stream close failed in worker: worker close interruption")

    monkeypatch.setattr(windows_process_tree, "_capture_process_result", Mock(side_effect=primary))
    monkeypatch.setattr(windows_process_cleanup, "_close_stream_bounded", close_stream)

    with pytest.raises(KeyboardInterrupt) as raised:
        run_bounded_process(
            _python_command("import time; time.sleep(30)"),
            cwd=None,
            env=os.environ.copy(),
            timeout=5,
        )

    assert raised.value is primary
    assert len(close_calls) == 3
    cleanup_errors = getattr(primary, "cleanup_errors", ())
    assert tuple(item.stage for item in cleanup_errors) == ("close",)
    assert any("worker close interruption" in item.message for item in cleanup_errors)


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_failed_job_termination_with_inherited_pipe_is_bounded(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    pid_file = tmp_path / "child-pid"
    source = (
        "import subprocess,sys; "
        "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); "
        f"open({str(pid_file)!r},'w').write(str(child.pid)); "
        "print('root output',flush=True)"
    )
    terminate_error = OSError("injected TerminateJobObject failure")
    terminate = Mock(side_effect=terminate_error)
    monkeypatch.setattr(windows_process_tree, "_terminate_process_tree", terminate)
    started = windows_process_tree.time.monotonic()

    with pytest.raises(subprocess.TimeoutExpired) as raised:
        run_bounded_process(_python_command(source), cwd=None, env=os.environ.copy(), timeout=5)

    child_pid = int(pid_file.read_text(encoding="utf-8"))
    kernel32 = getattr(ctypes, "WinDLL")("kernel32", use_last_error=True)
    kernel32.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
    kernel32.OpenProcess.restype = ctypes.c_void_p
    kernel32.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel32.WaitForSingleObject.restype = windows_process_tree.ctypes.c_uint32
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel32.CloseHandle.restype = ctypes.c_int
    kernel32.TerminateProcess.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel32.TerminateProcess.restype = ctypes.c_int
    process_handle = kernel32.OpenProcess(0x00100001, False, child_pid)
    if not process_handle:
        assert getattr(ctypes, "get_last_error")() == 87
    try:
        elapsed = windows_process_tree.time.monotonic() - started
        assert elapsed < 30
        assert raised.value.timeout == 5
        assert getattr(raised.value, "returncode", None) == 0
        output = raised.value.output
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        assert "root output" in (output or "")
        cleanup_errors = getattr(raised.value, "cleanup_errors", ())
        assert any("injected TerminateJobObject failure" in error.message for error in cleanup_errors)
        terminate.assert_called_once()
        if process_handle:
            exit_status = kernel32.WaitForSingleObject(process_handle, 5000)
            assert exit_status == 0, "Job Object closure did not terminate the descendant"
    finally:
        if process_handle and kernel32.WaitForSingleObject(process_handle, 0) != 0:
            kernel32.TerminateProcess(process_handle, 1)
            kernel32.WaitForSingleObject(process_handle, 5000)
        if process_handle:
            kernel32.CloseHandle(process_handle)
