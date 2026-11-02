"""Run captured subprocesses with bounded native Windows process-tree ownership."""

from __future__ import annotations

import ctypes
import locale
import math
import os
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from typing import Any

from agentic_devtools.cli.ci.windows_process_cleanup import (
    ProcessCleanupDiagnostic,
    ProcessCleanupError,
    _attempt_process_cleanup,
    _drain_and_reap_process,
)
from agentic_devtools.cli.ci.windows_process_cleanup import _close_process_resources as _close_process_resources_bounded

if sys.platform == "win32":
    _CLEANUP_TIMEOUT = 10.0
    _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
    _JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION = 1
    _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000

    class _IoCounters(ctypes.Structure):
        _fields_ = [
            ("read_operation_count", ctypes.c_ulonglong),
            ("write_operation_count", ctypes.c_ulonglong),
            ("other_operation_count", ctypes.c_ulonglong),
            ("read_transfer_count", ctypes.c_ulonglong),
            ("write_transfer_count", ctypes.c_ulonglong),
            ("other_transfer_count", ctypes.c_ulonglong),
        ]

    class _BasicLimitInformation(ctypes.Structure):
        _fields_ = [
            ("per_process_user_time_limit", ctypes.c_longlong),
            ("per_job_user_time_limit", ctypes.c_longlong),
            ("limit_flags", ctypes.c_ulong),
            ("minimum_working_set_size", ctypes.c_size_t),
            ("maximum_working_set_size", ctypes.c_size_t),
            ("active_process_limit", ctypes.c_ulong),
            ("affinity", ctypes.c_size_t),
            ("priority_class", ctypes.c_ulong),
            ("scheduling_class", ctypes.c_ulong),
        ]

    class _ExtendedLimitInformation(ctypes.Structure):
        _fields_ = [
            ("basic_limit_information", _BasicLimitInformation),
            ("io_info", _IoCounters),
            ("process_memory_limit", ctypes.c_size_t),
            ("job_memory_limit", ctypes.c_size_t),
            ("peak_process_memory_used", ctypes.c_size_t),
            ("peak_job_memory_used", ctypes.c_size_t),
        ]

    class _BasicAccountingInformation(ctypes.Structure):
        _fields_ = [
            ("total_user_time", ctypes.c_longlong),
            ("total_kernel_time", ctypes.c_longlong),
            ("this_period_total_user_time", ctypes.c_longlong),
            ("this_period_total_kernel_time", ctypes.c_longlong),
            ("total_page_fault_count", ctypes.c_ulong),
            ("total_processes", ctypes.c_ulong),
            ("active_processes", ctypes.c_ulong),
            ("total_terminated_processes", ctypes.c_ulong),
        ]

    def _windows_error(stage: str) -> OSError:
        error = getattr(ctypes, "get_last_error")()
        return OSError(error, f"{stage}: {getattr(ctypes, 'WinError')(error)}")

    def _win_dll(name: str) -> Any:
        return getattr(ctypes, "WinDLL")(name, use_last_error=True)

    def _create_job_object() -> int:
        kernel32 = _win_dll("kernel32")
        kernel32.CreateJobObjectW.restype = ctypes.c_void_p
        kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
        kernel32.SetInformationJobObject.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_ulong]
        kernel32.SetInformationJobObject.restype = ctypes.c_int
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel32.CloseHandle.restype = ctypes.c_int
        handle = kernel32.CreateJobObjectW(None, None)
        if not handle:
            raise _windows_error("CreateJobObjectW")
        information = _ExtendedLimitInformation()
        information.basic_limit_information.limit_flags = _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not kernel32.SetInformationJobObject(
            handle,
            _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
            ctypes.byref(information),
            ctypes.sizeof(information),
        ):
            error = _windows_error("SetInformationJobObject")
            if not kernel32.CloseHandle(handle):
                setattr(
                    error,
                    "cleanup_errors",
                    (ProcessCleanupDiagnostic("close", str(_windows_error("CloseHandle"))),),
                )
            raise error
        return int(handle)

    def _assign_process_to_job(job_handle: int, process: subprocess.Popen[str]) -> None:
        kernel32 = _win_dll("kernel32")
        kernel32.AssignProcessToJobObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        kernel32.AssignProcessToJobObject.restype = ctypes.c_int
        if not kernel32.AssignProcessToJobObject(job_handle, int(getattr(process, "_handle"))):
            raise _windows_error("AssignProcessToJobObject")

    def _confirm_process_in_job(job_handle: int, process: subprocess.Popen[str]) -> None:
        kernel32 = _win_dll("kernel32")
        kernel32.IsProcessInJob.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
        kernel32.IsProcessInJob.restype = ctypes.c_int
        in_job = ctypes.c_int()
        if not kernel32.IsProcessInJob(int(getattr(process, "_handle")), job_handle, ctypes.byref(in_job)):
            raise _windows_error("IsProcessInJob")
        if not in_job.value:
            raise OSError("IsProcessInJob confirmed that the process is not owned by its Job Object")

    def _resume_suspended_process(process: subprocess.Popen[str]) -> None:
        ntdll = _win_dll("ntdll")
        ntdll.NtResumeProcess.argtypes = [ctypes.c_void_p]
        ntdll.NtResumeProcess.restype = ctypes.c_long
        status = ntdll.NtResumeProcess(int(getattr(process, "_handle")))
        if status < 0:
            raise OSError(f"NtResumeProcess failed with NTSTATUS 0x{status & 0xFFFFFFFF:08x}")

    def _active_process_count(job_handle: int) -> int:
        kernel32 = _win_dll("kernel32")
        kernel32.QueryInformationJobObject.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.c_ulong,
            ctypes.POINTER(ctypes.c_ulong),
        ]
        kernel32.QueryInformationJobObject.restype = ctypes.c_int
        information = _BasicAccountingInformation()
        if not kernel32.QueryInformationJobObject(
            job_handle,
            _JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION,
            ctypes.byref(information),
            ctypes.sizeof(information),
            None,
        ):
            raise _windows_error("QueryInformationJobObject")
        return int(information.active_processes)

    def _terminate_process_tree(
        job_handle: int,
        process: subprocess.Popen[str] | None,
        assigned: bool = True,
    ) -> None:
        if process is None:
            return
        if assigned and job_handle:
            kernel32 = _win_dll("kernel32")
            kernel32.TerminateJobObject.argtypes = [ctypes.c_void_p, ctypes.c_uint]
            kernel32.TerminateJobObject.restype = ctypes.c_int
            if not kernel32.TerminateJobObject(job_handle, 1):
                raise _windows_error("TerminateJobObject")
            deadline = time.monotonic() + _CLEANUP_TIMEOUT
            while _active_process_count(job_handle):
                if time.monotonic() >= deadline:
                    raise TimeoutError("Job Object processes remained active after termination")
                time.sleep(0.05)
        elif process.poll() is None:
            process.kill()

    def _drain_process(
        process: subprocess.Popen[str],
        timeout: float,
    ) -> tuple[str | None, str | None]:
        return process.communicate(timeout=timeout)

    def _reap_process(process: subprocess.Popen[str], timeout: float) -> None:
        process.wait(timeout=timeout)

    def _close_job_object(job_handle: int) -> None:
        kernel32 = _win_dll("kernel32")
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel32.CloseHandle.restype = ctypes.c_int
        if not kernel32.CloseHandle(job_handle):
            raise _windows_error("CloseHandle")

    def _close_process_resources(
        process: subprocess.Popen[str] | None,
        job_handle: int | None,
    ) -> tuple[str, ...]:
        return _close_process_resources_bounded(process, job_handle, _CLEANUP_TIMEOUT, _close_job_object)

    def _as_text(value: str | bytes | None) -> str | None:
        if isinstance(value, bytes):
            return value.decode(locale.getpreferredencoding(False), errors="replace")
        return value

    def _prefer_output(previous: str | None, latest: str | bytes | None) -> str | None:
        text = _as_text(latest)
        if text is not None and (previous is None or len(text) >= len(previous)):
            return text
        return previous

    def _attach_cleanup_errors(
        primary_error: BaseException,
        errors: list[ProcessCleanupDiagnostic],
        additional_errors: tuple[ProcessCleanupDiagnostic, ...] = (),
    ) -> None:
        setattr(primary_error, "cleanup_errors", (*errors, *additional_errors))

    def _cleanup_process(
        process: subprocess.Popen[str] | None,
        job_handle: int | None,
        *,
        assigned: bool,
        terminate: bool,
    ) -> tuple[list[ProcessCleanupDiagnostic], str | None, str | None, subprocess.TimeoutExpired | None]:
        errors: list[ProcessCleanupDiagnostic] = []
        stdout = stderr = None
        drain_timeout: subprocess.TimeoutExpired | None = None
        cancellation: BaseException | None = None
        if terminate:
            previous_cancellation = cancellation
            _, cancellation, termination_failed = _attempt_process_cleanup(
                "terminate",
                _terminate_process_tree,
                (job_handle or 0, process, assigned),
                errors,
                cancellation,
            )
            if cancellation is not previous_cancellation:
                errors.append(ProcessCleanupDiagnostic("terminate", str(cancellation)))
            if termination_failed:
                previous_cancellation = cancellation
                close_messages, cancellation, _ = _attempt_process_cleanup(
                    "close", _close_process_resources, (None, job_handle), errors, cancellation
                )
                errors.extend(ProcessCleanupDiagnostic("close", message) for message in close_messages or ())
                if cancellation is not previous_cancellation:
                    errors.append(ProcessCleanupDiagnostic("close", str(cancellation)))
                job_handle = None
        stdout, stderr, drain_timeout, cancellation = _drain_and_reap_process(
            process,
            _CLEANUP_TIMEOUT,
            _drain_process,
            _reap_process,
            _as_text,
            _prefer_output,
            errors,
            cancellation,
        )
        previous_cancellation = cancellation
        close_errors, cancellation, _ = _attempt_process_cleanup(
            "close", _close_process_resources, (process, job_handle), errors, cancellation
        )
        errors.extend(ProcessCleanupDiagnostic("close", message) for message in close_errors or ())
        if cancellation is not previous_cancellation:
            errors.append(ProcessCleanupDiagnostic("close", str(cancellation)))
        if cancellation is not None:
            stdout = _prefer_output(stdout, getattr(cancellation, "output", None))
            stderr = _prefer_output(stderr, getattr(cancellation, "stderr", None))
            _attach_cleanup_errors(cancellation, errors, getattr(cancellation, "cleanup_errors", ()))
            setattr(cancellation, "output", stdout)
            setattr(cancellation, "stderr", stderr)
            setattr(cancellation, "_agdt_cleanup_complete", True)
            raise cancellation
        return errors, stdout, stderr, drain_timeout

    def _start_windows_process(
        arguments: Sequence[str],
        *,
        cwd: str | os.PathLike[str] | None,
        env: Mapping[str, str],
    ) -> tuple[subprocess.Popen[str], int]:
        job_handle: int | None = None
        process: subprocess.Popen[str] | None = None
        assigned = False
        stage = "create Job Object"
        try:
            job_handle = _create_job_object()
            stage = "launch suspended process"
            process = subprocess.Popen(
                arguments,
                cwd=cwd,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding=locale.getpreferredencoding(False),
                errors="replace",
                shell=False,
                creationflags=0x00000004,
            )
            stage = "assign process to Job Object"
            _assign_process_to_job(job_handle, process)
            stage = "confirm Job Object ownership"
            _confirm_process_in_job(job_handle, process)
            assigned = True
            stage = "resume owned process"
            _resume_suspended_process(process)
            return process, job_handle
        except BaseException as exc:
            primary_error = OSError(f"Windows process ownership setup failed at {stage}: {exc}")
            try:
                cleanup_errors, _, _, _ = _cleanup_process(
                    process,
                    job_handle,
                    assigned=assigned,
                    terminate=process is not None,
                )
            except BaseException as cleanup_error:
                cleanup_errors = list(getattr(cleanup_error, "cleanup_errors", ()))
                if not cleanup_errors:
                    cleanup_errors.append(ProcessCleanupDiagnostic("cleanup", str(cleanup_error)))
            cleanup_errors.extend(getattr(exc, "cleanup_errors", ()))
            if isinstance(exc, Exception):
                _attach_cleanup_errors(primary_error, cleanup_errors)
                raise primary_error from exc
            _attach_cleanup_errors(exc, cleanup_errors)
            raise

    def _capture_process_result(
        process: subprocess.Popen[str],
        arguments: Sequence[str],
        timeout: float,
    ) -> tuple[str | None, str | None, int | None, BaseException | None]:
        try:
            captured_stdout, captured_stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            return (
                _as_text(exc.output),
                _as_text(exc.stderr),
                process.poll(),
                subprocess.TimeoutExpired(
                    arguments,
                    timeout,
                    output=_as_text(exc.output),
                    stderr=_as_text(exc.stderr),
                ),
            )
        except OSError as exc:
            return (
                _as_text(getattr(exc, "output", None)),
                _as_text(getattr(exc, "stderr", None)),
                process.poll(),
                exc,
            )
        stdout = _as_text(captured_stdout)
        stderr = _as_text(captured_stderr)
        returncode = process.returncode
        if returncode is None:
            returncode = process.wait(timeout=_CLEANUP_TIMEOUT)
        return stdout, stderr, returncode, None

    def _finish_process_result(
        arguments: Sequence[str],
        returncode: int | None,
        stdout: str | None,
        stderr: str | None,
        primary_error: BaseException | None,
        cleanup_errors: list[ProcessCleanupDiagnostic],
        drain_timeout: subprocess.TimeoutExpired | None,
    ) -> subprocess.CompletedProcess[str]:
        if primary_error is None and drain_timeout is not None:
            primary_error = subprocess.TimeoutExpired(arguments, _CLEANUP_TIMEOUT, output=stdout, stderr=stderr)
        if primary_error is not None:
            setattr(primary_error, "output", stdout)
            setattr(primary_error, "stderr", stderr)
        if isinstance(primary_error, subprocess.TimeoutExpired):
            if returncode is not None:
                setattr(primary_error, "returncode", returncode)
        if primary_error is not None:
            _attach_cleanup_errors(primary_error, cleanup_errors)
            raise primary_error
        if returncode is None:
            raise OSError("Process completed without an observed return code")

        completed = subprocess.CompletedProcess(arguments, returncode, stdout, stderr)
        if returncode:
            error = subprocess.CalledProcessError(returncode, arguments, output=stdout, stderr=stderr)
            _attach_cleanup_errors(error, cleanup_errors)
            raise error
        if cleanup_errors:
            raise ProcessCleanupError(completed, tuple(cleanup_errors))
        return completed

    def _run_windows_process(
        arguments: Sequence[str],
        *,
        cwd: str | os.PathLike[str] | None,
        env: Mapping[str, str],
        timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        process, job_handle = _start_windows_process(arguments, cwd=cwd, env=env)
        cleanup_errors: list[ProcessCleanupDiagnostic] = []
        cleanup_done = False
        stdout = stderr = None
        try:
            stdout, stderr, returncode, primary_error = _capture_process_result(process, arguments, timeout)
            needs_termination = primary_error is not None
            if not needs_termination:
                try:
                    needs_termination = _active_process_count(job_handle) > 0
                except Exception as exc:
                    needs_termination = True
                    cleanup_errors.append(ProcessCleanupDiagnostic("terminate", str(exc)))

            later_errors, drained_stdout, drained_stderr, drain_timeout = _cleanup_process(
                process,
                job_handle,
                assigned=True,
                terminate=needs_termination,
            )
            cleanup_done = True
            cleanup_errors.extend(later_errors)
            stdout = _prefer_output(stdout, drained_stdout)
            stderr = _prefer_output(stderr, drained_stderr)
            if returncode is None:
                returncode = process.returncode
            return _finish_process_result(
                arguments,
                returncode,
                stdout,
                stderr,
                primary_error,
                cleanup_errors,
                drain_timeout,
            )
        except BaseException as primary_error:
            if not cleanup_done:
                if not getattr(primary_error, "_agdt_cleanup_complete", False):
                    try:
                        later_errors, drained_stdout, drained_stderr, _ = _cleanup_process(
                            process,
                            job_handle,
                            assigned=True,
                            terminate=True,
                        )
                        cleanup_errors.extend(later_errors)
                        captured_stdout = _prefer_output(
                            _prefer_output(stdout, _as_text(getattr(primary_error, "output", None))),
                            drained_stdout,
                        )
                        captured_stderr = _prefer_output(
                            _prefer_output(stderr, _as_text(getattr(primary_error, "stderr", None))),
                            drained_stderr,
                        )
                        if captured_stdout is not None:
                            setattr(primary_error, "output", captured_stdout)
                        if captured_stderr is not None:
                            setattr(primary_error, "stderr", captured_stderr)
                    except BaseException as cleanup_error:
                        cleanup_errors.extend(
                            getattr(
                                cleanup_error,
                                "cleanup_errors",
                                (ProcessCleanupDiagnostic("cleanup", str(cleanup_error)),),
                            )
                        )
                        stdout = _prefer_output(stdout, getattr(cleanup_error, "output", None))
                        stderr = _prefer_output(stderr, getattr(cleanup_error, "stderr", None))
                setattr(primary_error, "output", _prefer_output(stdout, getattr(primary_error, "output", None)))
                setattr(primary_error, "stderr", _prefer_output(stderr, getattr(primary_error, "stderr", None)))
                _attach_cleanup_errors(primary_error, cleanup_errors, getattr(primary_error, "cleanup_errors", ()))
            raise


def run_bounded_process(
    arguments: Sequence[str],
    *,
    cwd: str | os.PathLike[str] | None,
    env: Mapping[str, str],
    timeout: float,
) -> subprocess.CompletedProcess[str]:
    """Run a captured-text command with bounded execution and cleanup."""
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be a finite positive number")
    if sys.platform == "win32":
        return _run_windows_process(arguments, cwd=cwd, env=env, timeout=timeout)
    return subprocess.run(
        arguments,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        shell=False,
        check=True,
        timeout=timeout,
    )


__all__ = ["ProcessCleanupDiagnostic", "ProcessCleanupError", "run_bounded_process"]
