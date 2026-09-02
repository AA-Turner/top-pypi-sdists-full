"""Best-effort per-command performance telemetry for the CLI / AI Watch.

Wraps the typer ``app()`` in each entrypoint (``main.py:cli`` and
``aiwatch.py:main``), times the invocation, captures CPU + peak-memory usage,
disk reads, and POSTs one event to the backend relay
(``POST /api/v1/telemetry/cli-command-events``). The backend validates it and
records customer-tagged ``runlayer.cli.command.*`` OTel metrics — clients ship
no telemetry SDK.

Design constraints (mirrors ``telemetry.py`` / ``metrics.py``):
- Import-safe inside the ``aiwatch`` PyInstaller bundle: only stdlib +
  structlog at top level; ``httpx`` and ``config`` are deferred into functions.
- Never slows or breaks a command: resource capture, credential resolution and
  the flush all swallow their own errors. Resource metrics are optional — a
  command still reports ``duration_ms`` when resource capture is unavailable.
- Skips silently when telemetry is disabled or no credential resolves
  (unauthenticated invocations such as ``--version`` / pre-login are not
  reported).
- Native self-update commands suppress the exit-path report before replacing
  their running PyInstaller bundle, preventing late imports from mutated files.
"""

from __future__ import annotations

import ctypes
import os
import sys
import time
from collections.abc import Callable
from ctypes import wintypes
from pathlib import Path
from typing import Any, TypedDict

import structlog

from runlayer_cli import __version__
from runlayer_cli.command_contract import (
    detect_os,
    detect_os_version,
    detect_source,
    sanitize_command,
)
from runlayer_cli.logging import ensure_base_logging_configured
from runlayer_cli.telemetry import _telemetry_disabled

logger = structlog.get_logger(__name__)
_suppress_current_report = False
_JOB_OBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION_CLASS = 8
_JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS = 9
_JOB_OBJECT_LIMIT_BREAKAWAY_OK = 0x00000800
_RUSAGE_INFO_V2 = 2
_BYTES_PER_MB = 1024.0 * 1024.0


class ResourceUsage(TypedDict):
    cpu_time_ms: float | None
    peak_memory_mb: float | None
    disk_read_ops: float | None
    disk_read_mb: float | None


def _empty_resource_usage() -> ResourceUsage:
    return {
        "cpu_time_ms": None,
        "peak_memory_mb": None,
        "disk_read_ops": None,
        "disk_read_mb": None,
    }


class _JobObjectBasicAccountingInformation(ctypes.Structure):
    _fields_ = (
        ("TotalUserTime", ctypes.c_int64),
        ("TotalKernelTime", ctypes.c_int64),
        ("ThisPeriodTotalUserTime", ctypes.c_int64),
        ("ThisPeriodTotalKernelTime", ctypes.c_int64),
        ("TotalPageFaultCount", wintypes.DWORD),
        ("TotalProcesses", wintypes.DWORD),
        ("ActiveProcesses", wintypes.DWORD),
        ("TotalTerminatedProcesses", wintypes.DWORD),
    )


class _JobObjectBasicLimitInformation(ctypes.Structure):
    _fields_ = (
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    )


class _IoCounters(ctypes.Structure):
    _fields_ = (
        ("ReadOperationCount", ctypes.c_uint64),
        ("WriteOperationCount", ctypes.c_uint64),
        ("OtherOperationCount", ctypes.c_uint64),
        ("ReadTransferCount", ctypes.c_uint64),
        ("WriteTransferCount", ctypes.c_uint64),
        ("OtherTransferCount", ctypes.c_uint64),
    )


class _JobObjectBasicAndIoAccountingInformation(ctypes.Structure):
    _fields_ = (
        ("BasicInfo", _JobObjectBasicAccountingInformation),
        ("IoInfo", _IoCounters),
    )


class _RusageInfoV2(ctypes.Structure):
    _fields_ = (
        ("ri_uuid", ctypes.c_uint8 * 16),
        ("ri_user_time", ctypes.c_uint64),
        ("ri_system_time", ctypes.c_uint64),
        ("ri_pkg_idle_wkups", ctypes.c_uint64),
        ("ri_interrupt_wkups", ctypes.c_uint64),
        ("ri_pageins", ctypes.c_uint64),
        ("ri_wired_size", ctypes.c_uint64),
        ("ri_resident_size", ctypes.c_uint64),
        ("ri_phys_footprint", ctypes.c_uint64),
        ("ri_proc_start_abstime", ctypes.c_uint64),
        ("ri_proc_exit_abstime", ctypes.c_uint64),
        ("ri_child_user_time", ctypes.c_uint64),
        ("ri_child_system_time", ctypes.c_uint64),
        ("ri_child_pkg_idle_wkups", ctypes.c_uint64),
        ("ri_child_interrupt_wkups", ctypes.c_uint64),
        ("ri_child_pageins", ctypes.c_uint64),
        ("ri_child_elapsed_abstime", ctypes.c_uint64),
        ("ri_diskio_bytesread", ctypes.c_uint64),
        ("ri_diskio_byteswritten", ctypes.c_uint64),
    )


class _JobObjectExtendedLimitInformation(ctypes.Structure):
    _fields_ = (
        ("BasicLimitInformation", _JobObjectBasicLimitInformation),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    )


def suppress_current_command_metrics() -> None:
    """Skip the exit-path report for a command that may replace this bundle."""
    global _suppress_current_report
    _suppress_current_report = True


def run_with_command_metrics(app_callable: Callable[[], Any]) -> None:
    """Run ``app_callable`` (the typer app), then flush a command-perf event.

    Records wall time and terminal status. ``SystemExit`` with a non-zero code
    is ``error``; any other unhandled exception is ``error`` with its class name
    as ``error_type``. The flush runs in ``finally`` (before the exit propagates)
    unless the command suppresses it before replacing the running bundle.
    """
    global _suppress_current_report
    _suppress_current_report = False

    # Universal non-hook wrapper: guarantee a level-filtered stderr logger so the
    # best-effort failure diagnostic below never leaks on unconfigured-logger
    # paths (``--version`` / ``--help`` / invalid). No-op once ``setup_logging``
    # has run (``run`` / ``scan`` / ...).
    ensure_base_logging_configured()

    if _telemetry_disabled():
        app_callable()
        return

    started = time.monotonic()
    job_handle = _start_windows_job_accounting() if sys.platform == "win32" else None
    status = "ok"
    error_type: str | None = None
    try:
        app_callable()
    except SystemExit as exc:
        if exc.code not in (None, 0):
            status = "error"
        raise
    except BaseException as exc:
        status = "error"
        error_type = type(exc).__name__
        raise
    finally:
        duration_ms = (time.monotonic() - started) * 1000.0
        try:
            if not _suppress_current_report:
                _report_command(
                    duration_ms=duration_ms,
                    status=status,
                    error_type=error_type,
                    job_handle=job_handle,
                )
        finally:
            _suppress_current_report = False
            handle = job_handle
            job_handle = None
            if handle is not None:
                _close_windows_job_accounting(handle)


def build_command_event(
    *,
    command: str,
    duration_ms: float,
    cpu_time_ms: float | None,
    peak_memory_mb: float | None,
    disk_read_ops: float | None,
    disk_read_mb: float | None,
    status: str,
    error_type: str | None,
) -> dict[str, Any]:
    """Build the wire event for one command invocation.

    Optional resource fields are omitted (not sent as ``null``) when capture was
    unavailable, so the backend simply skips those tags.
    """
    event: dict[str, Any] = {
        "command": command,
        "duration_ms": round(max(duration_ms, 0.0), 3),
        "os": detect_os(),
        "source": detect_source(),
        "cli_version": __version__,
        "status": status,
    }
    os_version = detect_os_version()
    if os_version is not None:
        event["os_version"] = os_version
    if cpu_time_ms is not None:
        event["cpu_time_ms"] = round(max(cpu_time_ms, 0.0), 3)
    if peak_memory_mb is not None:
        event["peak_memory_mb"] = round(max(peak_memory_mb, 0.0), 3)
    if disk_read_ops is not None:
        event["disk_read_ops"] = int(max(disk_read_ops, 0.0))
    if disk_read_mb is not None:
        event["disk_read_mb"] = round(max(disk_read_mb, 0.0), 3)
    if error_type is not None:
        event["error_type"] = error_type
    return event


def _report_command(
    *,
    duration_ms: float,
    status: str,
    error_type: str | None,
    job_handle: int | None = None,
) -> None:
    """Assemble and POST the command event. Best-effort; swallows all errors."""
    try:
        host, secret = _resolve_report_target()
        if not host or not secret:
            return  # unauthenticated / offline invocations are not reported
        usage = _capture_resource_usage(job_handle)
        event = build_command_event(
            command=sanitize_command(sys.argv),
            duration_ms=duration_ms,
            cpu_time_ms=usage["cpu_time_ms"],
            peak_memory_mb=usage["peak_memory_mb"],
            disk_read_ops=usage["disk_read_ops"],
            disk_read_mb=usage["disk_read_mb"],
            status=status,
            error_type=error_type,
        )
        # Deferred: RunlayerClient pulls the heavier api closure; by post-command
        # flush time it is already imported for authenticated invocations.
        from runlayer_cli.api import RunlayerClient  # noqa: PLC0415

        RunlayerClient(hostname=host, secret=secret).track_command_events([event])
    except Exception as exc:
        logger.debug("cli_command_metrics_skipped", error=str(exc))


def _resolve_report_target() -> tuple[str | None, str | None]:
    """Resolve ``(host, secret)`` for the flush without prompting or printing.

    Priority mirrors ``config.resolve_credentials`` (env → config default →
    single host) but stays non-interactive and side-effect-free: this runs on
    the exit path of every command, so it must never raise, prompt, or emit
    output. Returns ``(None, None)`` when either is missing.
    """
    host = os.environ.get("RUNLAYER_HOST") or None
    secret = os.environ.get("RUNLAYER_API_KEY") or None
    if host and secret:
        return _normalize_host(host), secret

    try:
        # Deferred: config pulls keyring/MDM readers; keep them off the fast
        # import path and out of the aiwatch bundle's top-level closure.
        from runlayer_cli.config import load_config, normalize_url  # noqa: PLC0415

        config = load_config()
        if host is None:
            host = config.default_host
            if host is None and len(config.hosts) == 1:
                host = next(iter(config.hosts.values())).get("url")
        if host and secret is None:
            secret = config.get_secret_for_host(normalize_url(host))
    except Exception:
        return None, None

    if not host or not secret:
        return None, None
    return _normalize_host(host), secret


def _normalize_host(host: str) -> str:
    return host.rstrip("/")


def _capture_resource_usage(
    job_handle: int | None = None,
) -> ResourceUsage:
    """Return resource usage for this process, best-effort.

    CPU time is total user+system across the process and its children. Peak
    memory and disk-read operation count cover the process tree where the
    platform supports it. Disk-read bytes cover self on POSIX and the process
    tree on Windows. Any field may be ``None`` when its platform syscall is
    unavailable; the command still reports its wall time.
    """
    if sys.platform == "win32":
        return _capture_resource_usage_windows(job_handle)
    return _capture_resource_usage_posix()


def _capture_resource_usage_posix() -> ResourceUsage:
    usage = _empty_resource_usage()
    try:
        import resource  # noqa: PLC0415 - POSIX-only stdlib

        rusage_self = resource.getrusage(resource.RUSAGE_SELF)
        rusage_children = resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu_seconds = (
            rusage_self.ru_utime
            + rusage_self.ru_stime
            + rusage_children.ru_utime
            + rusage_children.ru_stime
        )
        usage["cpu_time_ms"] = cpu_seconds * 1000.0
        # ru_maxrss units differ by platform: macOS reports bytes, Linux KiB.
        max_rss = max(rusage_self.ru_maxrss, rusage_children.ru_maxrss)
        if sys.platform == "darwin":
            usage["peak_memory_mb"] = max_rss / _BYTES_PER_MB
        else:
            usage["peak_memory_mb"] = max_rss / 1024.0
        usage["disk_read_ops"] = float(
            rusage_self.ru_inblock + rusage_children.ru_inblock
        )
    except Exception:
        pass

    if sys.platform == "linux":
        usage["disk_read_mb"] = _capture_linux_disk_read_mb()
    elif sys.platform == "darwin":
        usage["disk_read_mb"] = _capture_macos_disk_read_mb()
    return usage


def _capture_linux_disk_read_mb() -> float | None:
    """Read Linux's self-process storage bytes counter from procfs."""
    try:
        for line in Path("/proc/self/io").read_text(encoding="ascii").splitlines():
            key, separator, raw_value = line.partition(":")
            if key == "read_bytes" and separator:
                read_bytes = int(raw_value.strip())
                if read_bytes < 0:
                    return None
                return read_bytes / _BYTES_PER_MB
    except (OSError, ValueError):
        return None
    return None


def _capture_macos_disk_read_mb() -> float | None:
    """Read macOS's self-process storage bytes counter through libproc."""
    try:
        libproc = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
        proc_pid_rusage = libproc.proc_pid_rusage
        proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
        proc_pid_rusage.restype = ctypes.c_int
        info = _RusageInfoV2()
        if (
            proc_pid_rusage(
                os.getpid(),
                _RUSAGE_INFO_V2,
                ctypes.byref(info),
            )
            != 0
        ):
            return None
        return info.ri_diskio_bytesread / _BYTES_PER_MB
    except Exception:
        return None


def _windows_kernel32() -> Any:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # ty: ignore[unresolved-attribute]
    kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.AssignProcessToJobObject.argtypes = [
        wintypes.HANDLE,
        wintypes.HANDLE,
    ]
    kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    kernel32.GetCurrentProcess.argtypes = []
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.GetProcessTimes.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
    ]
    kernel32.GetProcessTimes.restype = wintypes.BOOL
    kernel32.GetProcessIoCounters.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_IoCounters),
    ]
    kernel32.GetProcessIoCounters.restype = wintypes.BOOL
    return kernel32


def _windows_last_error() -> int:
    return ctypes.get_last_error()  # ty: ignore[unresolved-attribute]


def _windows_handle_value(handle: Any) -> int:
    value = getattr(handle, "value", handle)
    if not isinstance(value, int):
        raise OSError("Win32 returned an invalid handle")
    return value


def _start_windows_job_accounting() -> int | None:
    """Assign this invocation to an unnamed job; fail dark on native errors."""
    job_handle: int | None = None
    assigned = False
    try:
        kernel32 = _windows_kernel32()
        job = kernel32.CreateJobObjectW(None, None)
        if not job:
            logger.debug(
                "cli_command_metrics_windows_create_job_object_failed",
                last_error=_windows_last_error(),
            )
            return None
        job_handle = _windows_handle_value(job)
        limits = _JobObjectExtendedLimitInformation()
        # Preserve explicit breakaway behavior: metrics must not make child
        # creation fail for commands that intentionally leave the process tree.
        limits.BasicLimitInformation.LimitFlags = _JOB_OBJECT_LIMIT_BREAKAWAY_OK
        if not kernel32.SetInformationJobObject(
            wintypes.HANDLE(job_handle),
            _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            logger.debug(
                "cli_command_metrics_windows_set_job_breakaway_failed",
                last_error=_windows_last_error(),
            )
            return None
        process_handle = kernel32.GetCurrentProcess()
        if not process_handle:
            logger.debug(
                "cli_command_metrics_windows_get_current_process_failed",
                last_error=_windows_last_error(),
            )
            return None
        if not kernel32.AssignProcessToJobObject(
            wintypes.HANDLE(job_handle),
            process_handle,
        ):
            logger.debug(
                "cli_command_metrics_windows_assign_process_to_job_failed",
                last_error=_windows_last_error(),
            )
            return None
        assigned = True
        return job_handle
    except Exception as exc:
        logger.debug(
            "cli_command_metrics_windows_job_setup_failed",
            error=str(exc),
        )
        return None
    finally:
        if job_handle is not None and not assigned:
            _close_windows_job_accounting(job_handle)


def _close_windows_job_accounting(job_handle: int) -> None:
    try:
        kernel32 = _windows_kernel32()
        if not kernel32.CloseHandle(wintypes.HANDLE(job_handle)):
            logger.debug(
                "cli_command_metrics_windows_close_job_failed",
                last_error=_windows_last_error(),
            )
    except Exception as exc:
        logger.debug(
            "cli_command_metrics_windows_close_job_failed",
            error=str(exc),
        )


def _capture_resource_usage_windows(
    job_handle: int | None = None,
) -> ResourceUsage:
    usage = _empty_resource_usage()
    if job_handle is not None:
        usage = _capture_windows_job_usage(job_handle)
    if any(value is None for value in usage.values()):
        self_usage = _capture_windows_process_usage()
        if usage["cpu_time_ms"] is None:
            usage["cpu_time_ms"] = self_usage["cpu_time_ms"]
        if usage["peak_memory_mb"] is None:
            usage["peak_memory_mb"] = self_usage["peak_memory_mb"]
        if usage["disk_read_ops"] is None:
            usage["disk_read_ops"] = self_usage["disk_read_ops"]
        if usage["disk_read_mb"] is None:
            usage["disk_read_mb"] = self_usage["disk_read_mb"]
    return usage


def _capture_windows_job_usage(
    job_handle: int,
) -> ResourceUsage:
    usage = _empty_resource_usage()
    try:
        kernel32 = _windows_kernel32()
    except Exception as exc:
        logger.debug(
            "cli_command_metrics_windows_job_resource_capture_failed",
            error=str(exc),
        )
        return usage

    accounting_and_io = _JobObjectBasicAndIoAccountingInformation()
    returned = wintypes.DWORD(0)
    try:
        if kernel32.QueryInformationJobObject(
            wintypes.HANDLE(job_handle),
            _JOB_OBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION_CLASS,
            ctypes.byref(accounting_and_io),
            ctypes.sizeof(accounting_and_io),
            ctypes.byref(returned),
        ):
            usage["cpu_time_ms"] = (
                accounting_and_io.BasicInfo.TotalUserTime
                + accounting_and_io.BasicInfo.TotalKernelTime
            ) / 10_000.0
            usage["disk_read_ops"] = float(accounting_and_io.IoInfo.ReadOperationCount)
            usage["disk_read_mb"] = (
                accounting_and_io.IoInfo.ReadTransferCount / _BYTES_PER_MB
            )
        else:
            logger.debug(
                "cli_command_metrics_windows_query_job_accounting_failed",
                last_error=_windows_last_error(),
            )
    except Exception as exc:
        logger.debug(
            "cli_command_metrics_windows_query_job_accounting_failed",
            error=str(exc),
        )

    limits = _JobObjectExtendedLimitInformation()
    returned = wintypes.DWORD(0)
    try:
        if kernel32.QueryInformationJobObject(
            wintypes.HANDLE(job_handle),
            _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
            ctypes.byref(returned),
        ):
            usage["peak_memory_mb"] = limits.PeakJobMemoryUsed / _BYTES_PER_MB
        else:
            logger.debug(
                "cli_command_metrics_windows_query_job_limits_failed",
                last_error=_windows_last_error(),
            )
    except Exception as exc:
        logger.debug(
            "cli_command_metrics_windows_query_job_limits_failed",
            error=str(exc),
        )
    return usage


def _capture_windows_process_usage() -> ResourceUsage:
    usage = _empty_resource_usage()
    try:
        kernel32 = _windows_kernel32()
        process_handle = kernel32.GetCurrentProcess()
        if not process_handle:
            logger.debug(
                "cli_command_metrics_windows_get_current_process_failed",
                last_error=_windows_last_error(),
            )
            return usage
    except Exception as exc:
        logger.debug(
            "cli_command_metrics_windows_get_current_process_failed",
            error=str(exc),
        )
        return usage

    creation = wintypes.FILETIME()
    exit_time = wintypes.FILETIME()
    kernel_time = wintypes.FILETIME()
    user_time = wintypes.FILETIME()
    try:
        if kernel32.GetProcessTimes(
            process_handle,
            ctypes.byref(creation),
            ctypes.byref(exit_time),
            ctypes.byref(kernel_time),
            ctypes.byref(user_time),
        ):
            # FILETIME kernel/user times are in 100ns ticks -> milliseconds.
            kernel_ticks = (
                kernel_time.dwHighDateTime << 32
            ) | kernel_time.dwLowDateTime
            user_ticks = (user_time.dwHighDateTime << 32) | user_time.dwLowDateTime
            usage["cpu_time_ms"] = (kernel_ticks + user_ticks) / 10_000.0
        else:
            logger.debug(
                "cli_command_metrics_windows_get_process_times_failed",
                last_error=_windows_last_error(),
            )
    except Exception as exc:
        logger.debug(
            "cli_command_metrics_windows_get_process_times_failed",
            error=str(exc),
        )

    try:

        class _ProcessMemoryCounters(ctypes.Structure):
            _fields_ = (
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            )

        counters = _ProcessMemoryCounters()
        counters.cb = ctypes.sizeof(_ProcessMemoryCounters)
        psapi = ctypes.WinDLL("psapi", use_last_error=True)  # ty: ignore[unresolved-attribute]
        psapi.GetProcessMemoryInfo.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(_ProcessMemoryCounters),
            wintypes.DWORD,
        ]
        psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
        if psapi.GetProcessMemoryInfo(
            process_handle, ctypes.byref(counters), counters.cb
        ):
            usage["peak_memory_mb"] = counters.PeakWorkingSetSize / _BYTES_PER_MB
        else:
            logger.debug(
                "cli_command_metrics_windows_get_process_memory_info_failed",
                last_error=_windows_last_error(),
            )
    except Exception as exc:
        logger.debug(
            "cli_command_metrics_windows_get_process_memory_info_failed",
            error=str(exc),
        )

    io_counters = _IoCounters()
    try:
        if kernel32.GetProcessIoCounters(
            process_handle,
            ctypes.byref(io_counters),
        ):
            usage["disk_read_ops"] = float(io_counters.ReadOperationCount)
            usage["disk_read_mb"] = io_counters.ReadTransferCount / _BYTES_PER_MB
        else:
            logger.debug(
                "cli_command_metrics_windows_get_process_io_counters_failed",
                last_error=_windows_last_error(),
            )
    except Exception as exc:
        logger.debug(
            "cli_command_metrics_windows_get_process_io_counters_failed",
            error=str(exc),
        )
    return usage
