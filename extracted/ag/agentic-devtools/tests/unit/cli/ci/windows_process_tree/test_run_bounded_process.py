import ctypes
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import windows_process_tree
from agentic_devtools.cli.ci.windows_process_tree import (
    ProcessCleanupError,
    run_bounded_process,
)


def _python_command(source: str) -> list[str]:
    return [sys.executable, "-c", source]


def _fake_windows_api(monkeypatch: pytest.MonkeyPatch) -> Mock:
    api = Mock()
    monkeypatch.setattr(windows_process_tree, "_win_dll", lambda _name: api)
    monkeypatch.setattr(windows_process_tree.ctypes, "get_last_error", lambda: 5)
    monkeypatch.setattr(windows_process_tree.ctypes, "WinError", lambda error: OSError(error, "access denied"))
    return api


def _windows_private(name: str) -> Any:
    return getattr(windows_process_tree, name)


def test_helper_import_resolves_from_candidate_head() -> None:
    head_root = Path(os.environ.get("WINDOWS_CI_HEAD_ROOT", Path(__file__).resolve().parents[5])).resolve()

    assert Path(windows_process_tree.__file__).resolve().is_relative_to(head_root)


def test_portable_dispatch_preserves_subprocess_run_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    completed = subprocess.CompletedProcess(["tool", "arg"], 0, "stdout", "stderr")
    run = Mock(return_value=completed)
    monkeypatch.setattr(windows_process_tree.sys, "platform", "linux")
    monkeypatch.setattr(windows_process_tree.subprocess, "run", run)

    result = run_bounded_process(["tool", "arg"], cwd="work", env={"KEY": "value"}, timeout=12.5)

    assert result is completed
    run.assert_called_once_with(
        ["tool", "arg"],
        cwd="work",
        env={"KEY": "value"},
        capture_output=True,
        text=True,
        shell=False,
        check=True,
        timeout=12.5,
    )


def test_portable_dispatch_preserves_timeout_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    error = subprocess.TimeoutExpired(["tool"], 3, output="partial", stderr="diagnostic")
    monkeypatch.setattr(windows_process_tree.sys, "platform", "linux")
    monkeypatch.setattr(
        windows_process_tree.subprocess,
        "run",
        Mock(side_effect=error),
    )

    with pytest.raises(subprocess.TimeoutExpired) as raised:
        run_bounded_process(["tool"], cwd=None, env={}, timeout=3)

    assert raised.value is error
    assert raised.value.cmd == ["tool"]
    assert raised.value.timeout == 3
    assert raised.value.output == "partial"
    assert raised.value.stderr == "diagnostic"


@pytest.mark.parametrize("timeout", (0, -1, float("inf"), float("nan")))
def test_rejects_nonpositive_or_nonfinite_timeout(timeout: float) -> None:
    with pytest.raises(ValueError, match="finite positive"):
        run_bounded_process(["tool"], cwd=None, env={}, timeout=timeout)


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_success_returns_captured_completed_process() -> None:
    completed = run_bounded_process(
        _python_command("print('complete')"),
        cwd=None,
        env=os.environ.copy(),
        timeout=5,
    )

    assert completed.returncode == 0
    assert completed.stdout == "complete\n"
    assert completed.stderr == ""


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_nonzero_exit_preserves_result_and_cleanup_diagnostics(monkeypatch: pytest.MonkeyPatch) -> None:
    close = _windows_private("_close_process_resources")

    def fail_close(process: subprocess.Popen[str] | None, job_handle: int | None) -> tuple[str, ...]:
        close(process, job_handle)
        raise OSError("injected close failure")

    monkeypatch.setattr(windows_process_tree, "_close_process_resources", fail_close)
    command = _python_command("import sys; print('stdout'); print('stderr',file=sys.stderr); sys.exit(9)")

    with pytest.raises(subprocess.CalledProcessError) as raised:
        run_bounded_process(command, cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value.cmd == command
    assert raised.value.returncode == 9
    assert raised.value.output == "stdout\n"
    assert raised.value.stderr == "stderr\n"
    assert tuple(item.stage for item in getattr(raised.value, "cleanup_errors", ())) == ("close",)


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_cleanup_drain_deadline_is_a_timeout_primary_error(monkeypatch: pytest.MonkeyPatch) -> None:
    command = _python_command("import sys; print('captured before cleanup'); sys.exit(9)")
    monkeypatch.setattr(
        windows_process_tree,
        "_drain_process",
        Mock(side_effect=subprocess.TimeoutExpired(command, 10, output=b"later")),
    )

    with pytest.raises(subprocess.TimeoutExpired) as raised:
        run_bounded_process(command, cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value.cmd == command
    assert raised.value.timeout == 10
    assert raised.value.output == "captured before cleanup\n"
    assert getattr(raised.value, "returncode", None) == 9
    assert tuple(item.stage for item in getattr(raised.value, "cleanup_errors", ())) == ("drain",)


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_job_query_failure_after_success_is_process_cleanup_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        windows_process_tree,
        "_active_process_count",
        Mock(side_effect=[OSError("injected job query failure"), 0]),
    )

    with pytest.raises(ProcessCleanupError) as raised:
        run_bounded_process(_python_command("print('completed')"), cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value.completed_process.returncode == 0
    assert raised.value.completed_process.stdout == "completed\n"
    assert tuple(item.stage for item in raised.value.cleanup_errors) == ("terminate",)
    assert "injected job query failure" in raised.value.cleanup_errors[0].message


@pytest.mark.parametrize(
    ("drain_result", "expected_output", "expected_stderr", "expected_stages"),
    [
        (OSError("injected drain failure"), "partial stdout", "partial stderr", ("drain",)),
        (
            ("recovered stdout is longer", "recovered stderr is longer"),
            "recovered stdout is longer",
            "recovered stderr is longer",
            (),
        ),
    ],
)
@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_communication_oserror_preserves_primary_and_best_output(
    monkeypatch: pytest.MonkeyPatch,
    drain_result: object,
    expected_output: str,
    expected_stderr: str,
    expected_stages: tuple[str, ...],
) -> None:
    error = OSError("injected communication failure")
    setattr(error, "output", b"partial stdout")
    setattr(error, "stderr", b"partial stderr")
    monkeypatch.setattr(subprocess.Popen, "communicate", Mock(side_effect=[error, drain_result]))

    with pytest.raises(OSError) as raised:
        run_bounded_process(_python_command("print('not observed')"), cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value is error
    assert getattr(raised.value, "output", None) == expected_output
    assert getattr(raised.value, "stderr", None) == expected_stderr
    assert tuple(item.stage for item in getattr(raised.value, "cleanup_errors", ())) == expected_stages


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_descendant_holds_inherited_pipes_after_root_exit() -> None:
    source = (
        "import subprocess,sys; "
        "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); "
        "print(f'child={child.pid}',flush=True); print('root output',flush=True)"
    )
    started = time.monotonic()

    with pytest.raises(subprocess.TimeoutExpired) as raised:
        run_bounded_process(_python_command(source), cwd=None, env=os.environ.copy(), timeout=5)

    elapsed = time.monotonic() - started
    assert elapsed < 30
    assert raised.value.timeout == 5
    assert getattr(raised.value, "returncode", None) == 0
    assert raised.value.cmd == _python_command(source)
    output = raised.value.output
    if isinstance(output, bytes):
        output = output.decode("utf-8", errors="replace")
    assert "root output" in (output or "")
    child_pid = int((output or "").split("child=", 1)[1].splitlines()[0])
    kernel32 = getattr(ctypes, "WinDLL")("kernel32", use_last_error=True)
    kernel32.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
    kernel32.OpenProcess.restype = ctypes.c_void_p
    kernel32.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel32.WaitForSingleObject.restype = ctypes.c_uint32
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel32.CloseHandle.restype = ctypes.c_int
    kernel32.TerminateProcess.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel32.TerminateProcess.restype = ctypes.c_int
    process_handle = kernel32.OpenProcess(0x00100000, False, child_pid)
    error = getattr(ctypes, "get_last_error")() if not process_handle else 0
    if process_handle:
        try:
            assert kernel32.WaitForSingleObject(process_handle, 5000) == 0
        finally:
            if kernel32.WaitForSingleObject(process_handle, 0) != 0:
                cleanup_handle = kernel32.OpenProcess(0x0001, False, child_pid)
                if cleanup_handle:
                    try:
                        kernel32.TerminateProcess(cleanup_handle, 1)
                    finally:
                        kernel32.CloseHandle(cleanup_handle)
            kernel32.CloseHandle(process_handle)
    else:
        assert error == 87, f"OpenProcess failed with Windows error {error}"


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows process ownership")
def test_ownership_setup_failure_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    marker = tmp_path / "ran"
    command = _python_command(f"from pathlib import Path; Path({str(marker)!r}).write_text('ran')")

    def fail_assignment(*args: object) -> None:
        raise OSError("injected assignment failure")

    drain = _windows_private("_drain_process")
    close = _windows_private("_close_process_resources")

    def fail_drain(process: subprocess.Popen[str], timeout: float) -> tuple[str | None, str | None]:
        drain(process, timeout)
        raise OSError("injected setup drain failure")

    def fail_close(process: subprocess.Popen[str] | None, job_handle: int | None) -> tuple[str, ...]:
        close(process, job_handle)
        raise OSError("injected setup close failure")

    monkeypatch.setattr(windows_process_tree, "_assign_process_to_job", fail_assignment)
    monkeypatch.setattr(windows_process_tree, "_drain_process", fail_drain)
    monkeypatch.setattr(windows_process_tree, "_close_process_resources", fail_close)

    with pytest.raises(OSError, match="ownership setup.*assign") as raised:
        run_bounded_process(command, cwd=None, env=os.environ.copy(), timeout=5)

    assert "injected assignment failure" in str(raised.value)
    assert not marker.exists()
    assert tuple(item.stage for item in getattr(raised.value, "cleanup_errors", ())) == ("drain", "close")


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows process ownership")
def test_ownership_setup_keyboard_interrupt_preserves_cancellation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    marker = tmp_path / "ran"
    command = _python_command(f"from pathlib import Path; Path({str(marker)!r}).write_text('ran')")
    interruption = KeyboardInterrupt("injected setup cancellation")
    terminate = _windows_private("_terminate_process_tree")
    terminate_spy = Mock(wraps=terminate)
    close = _windows_private("_close_process_resources")
    cleanup_calls: list[tuple[subprocess.Popen[str] | None, int | None, tuple[str, ...]]] = []

    def record_close(process: subprocess.Popen[str] | None, job_handle: int | None) -> tuple[str, ...]:
        errors = close(process, job_handle)
        cleanup_calls.append((process, job_handle, errors))
        return errors

    monkeypatch.setattr(windows_process_tree, "_terminate_process_tree", terminate_spy)
    monkeypatch.setattr(windows_process_tree, "_close_process_resources", record_close)
    monkeypatch.setattr(windows_process_tree, "_resume_suspended_process", Mock(side_effect=interruption))

    with pytest.raises(KeyboardInterrupt) as raised:
        run_bounded_process(command, cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value is interruption
    assert not marker.exists()
    terminate_spy.assert_called_once()
    process, job_handle, close_errors = cleanup_calls[0]
    assert process is not None and process.returncode is not None
    assert job_handle is not None
    assert close_errors == ()


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows process ownership")
def test_capture_keyboard_interrupt_terminates_owned_process_tree(monkeypatch: pytest.MonkeyPatch) -> None:
    command = _python_command("import time; time.sleep(30)")
    interruption = KeyboardInterrupt("injected capture cancellation")
    terminate = _windows_private("_terminate_process_tree")
    terminate_spy = Mock(wraps=terminate)
    close = _windows_private("_close_process_resources")

    def fail_close(process: subprocess.Popen[str] | None, job_handle: int | None) -> tuple[str, ...]:
        close(process, job_handle)
        raise OSError("injected close failure")

    monkeypatch.setattr(windows_process_tree, "_terminate_process_tree", terminate_spy)
    monkeypatch.setattr(windows_process_tree, "_close_process_resources", fail_close)
    monkeypatch.setattr(windows_process_tree, "_capture_process_result", Mock(side_effect=interruption))

    with pytest.raises(KeyboardInterrupt) as raised:
        run_bounded_process(command, cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value is interruption
    terminate_spy.assert_called_once()
    assert tuple(item.stage for item in getattr(raised.value, "cleanup_errors", ())) == ("close",)


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows process ownership")
def test_ownership_confirmation_failure_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    marker = tmp_path / "ran"
    command = _python_command(f"from pathlib import Path; Path({str(marker)!r}).write_text('ran')")
    monkeypatch.setattr(
        windows_process_tree,
        "_confirm_process_in_job",
        Mock(side_effect=OSError("injected ownership confirmation failure")),
    )

    with pytest.raises(OSError, match="confirm Job Object ownership"):
        run_bounded_process(command, cwd=None, env=os.environ.copy(), timeout=5)

    assert not marker.exists()


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_drain_close_failure_preserves_partial_output_and_cleanup_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    source = (
        "import subprocess,sys; "
        "subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],"
        "stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); "
        "print('root output',flush=True)"
    )
    drain = _windows_private("_drain_process")
    close = _windows_private("_close_process_resources")

    def fail_drain(process: subprocess.Popen[str], timeout: float) -> tuple[str, str]:
        drain(process, timeout)
        raise OSError("injected drain failure")

    def fail_close(process: subprocess.Popen[str], job_handle: int | None) -> None:
        close(process, job_handle)
        raise OSError("injected close failure")

    monkeypatch.setattr(windows_process_tree, "_drain_process", fail_drain)
    monkeypatch.setattr(windows_process_tree, "_close_process_resources", fail_close)

    with pytest.raises(ProcessCleanupError) as raised:
        run_bounded_process(_python_command(source), cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value.completed_process.returncode == 0
    assert raised.value.completed_process.stdout == "root output\n"
    assert tuple(error.stage for error in getattr(raised.value, "cleanup_errors", ())) == ("drain", "close")
    assert all("injected" in error.message for error in raised.value.cleanup_errors)


@pytest.mark.skipif(sys.platform != "win32", reason="Exercises native Windows API failure paths")
def test_job_creation_failures_report_os_and_cleanup_diagnostics(monkeypatch: pytest.MonkeyPatch) -> None:
    api = _fake_windows_api(monkeypatch)
    api.CreateJobObjectW.return_value = 0
    with pytest.raises(OSError, match="CreateJobObjectW"):
        _windows_private("_create_job_object")()
    api.CreateJobObjectW.return_value = 17
    api.SetInformationJobObject.return_value = 0
    api.CloseHandle.return_value = 0
    with pytest.raises(OSError, match="SetInformationJobObject") as setup_error:
        _windows_private("_create_job_object")()
    cleanup_errors: Any = getattr(setup_error.value, "cleanup_errors", ())
    assert cleanup_errors[0].stage == "close"


@pytest.mark.skipif(sys.platform != "win32", reason="Exercises native Windows API failure paths")
def test_ownership_api_failures_are_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    api = _fake_windows_api(monkeypatch)
    process = Mock()
    process._handle = 23
    api.AssignProcessToJobObject.return_value = 0
    with pytest.raises(OSError, match="AssignProcessToJobObject"):
        _windows_private("_assign_process_to_job")(17, process)
    api.IsProcessInJob.return_value = 0
    with pytest.raises(OSError, match="IsProcessInJob"):
        _windows_private("_confirm_process_in_job")(17, process)
    api.IsProcessInJob.return_value = 1
    with pytest.raises(OSError, match="not owned"):
        _windows_private("_confirm_process_in_job")(17, process)
    api.NtResumeProcess.return_value = -1
    with pytest.raises(OSError, match="NtResumeProcess"):
        _windows_private("_resume_suspended_process")(process)


@pytest.mark.skipif(sys.platform != "win32", reason="Exercises native Windows API failure paths")
def test_job_query_and_termination_failures_are_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    api = _fake_windows_api(monkeypatch)
    process = Mock()
    process._handle = 23
    process.poll.return_value = None
    api.QueryInformationJobObject.return_value = 0
    with pytest.raises(OSError, match="QueryInformationJobObject"):
        _windows_private("_active_process_count")(17)
    api.QueryInformationJobObject.return_value = 1

    def set_active_process_count(*args: Any) -> int:
        information = ctypes.cast(
            args[2],
            ctypes.POINTER(_windows_private("_BasicAccountingInformation")),
        )
        information.contents.active_processes = 4
        return 1

    api.QueryInformationJobObject.side_effect = set_active_process_count
    assert _windows_private("_active_process_count")(17) == 4
    api.TerminateJobObject.return_value = 0
    with pytest.raises(OSError, match="TerminateJobObject"):
        _windows_private("_terminate_process_tree")(17, process)
    api.TerminateJobObject.return_value = 1
    monkeypatch.setattr(windows_process_tree, "_active_process_count", Mock(side_effect=[1, 0]))
    monkeypatch.setattr(windows_process_tree.time, "sleep", Mock())
    _windows_private("_terminate_process_tree")(17, process)
    monkeypatch.setattr(windows_process_tree, "_active_process_count", Mock(return_value=1))
    monkeypatch.setattr(windows_process_tree, "_CLEANUP_TIMEOUT", 0)
    with pytest.raises(TimeoutError, match="remained active"):
        _windows_private("_terminate_process_tree")(17, process)
    assert _windows_private("_terminate_process_tree")(17, None) is None
    process.poll.return_value = None
    _windows_private("_terminate_process_tree")(0, process, assigned=False)
    process.kill.assert_called_once()


@pytest.mark.skipif(sys.platform != "win32", reason="Exercises native Windows cleanup failure paths")
def test_cleanup_stages_retain_every_failure_and_partial_output(monkeypatch: pytest.MonkeyPatch) -> None:
    api = _fake_windows_api(monkeypatch)
    process = Mock()
    api.CloseHandle.return_value = 0
    broken_stream = Mock()
    broken_stream.close.side_effect = OSError("stream close failed")
    fake_process = Mock(stdout=broken_stream, stderr=broken_stream, stdin=broken_stream)
    close_errors = _windows_private("_close_process_resources")(fake_process, 17)
    assert close_errors == (
        "[Errno 5] CloseHandle: [Errno 5] access denied",
        "stream close failed",
        "stream close failed",
        "stream close failed",
    )

    monkeypatch.setattr(
        windows_process_tree,
        "_terminate_process_tree",
        Mock(side_effect=OSError("terminate failed")),
    )
    monkeypatch.setattr(
        windows_process_tree,
        "_drain_process",
        Mock(side_effect=subprocess.TimeoutExpired(["tool"], 10, output=b"partial", stderr=b"diagnostic")),
    )
    monkeypatch.setattr(windows_process_tree, "_reap_process", Mock(side_effect=OSError("reap failed")))
    monkeypatch.setattr(windows_process_tree, "_close_process_resources", Mock(return_value=("close failed",)))
    errors, stdout, stderr, drain_timeout = _windows_private("_cleanup_process")(
        process,
        17,
        assigned=True,
        terminate=True,
    )
    assert tuple(error.stage for error in errors) == ("terminate", "close", "drain", "reap", "close")
    assert (stdout, stderr) == ("partial", "diagnostic")
    assert isinstance(drain_timeout, subprocess.TimeoutExpired)
