"""Tests for best-effort per-command performance telemetry."""

import ctypes
import json
import math
import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest
import structlog

from runlayer_cli import command_metrics
from runlayer_cli.command_metrics import (
    build_command_event,
    run_with_command_metrics,
)


def _fake_rusage(
    *,
    utime: float,
    stime: float,
    maxrss: int,
    inblock: int = 0,
) -> MagicMock:
    rusage = MagicMock()
    rusage.ru_utime = utime
    rusage.ru_stime = stime
    rusage.ru_maxrss = maxrss
    rusage.ru_inblock = inblock
    return rusage


def _usage(
    *,
    cpu_time_ms: float | None = None,
    peak_memory_mb: float | None = None,
    disk_read_ops: float | None = None,
    disk_read_mb: float | None = None,
) -> command_metrics.ResourceUsage:
    return {
        "cpu_time_ms": cpu_time_ms,
        "peak_memory_mb": peak_memory_mb,
        "disk_read_ops": disk_read_ops,
        "disk_read_mb": disk_read_mb,
    }


class TestBuildCommandEvent:
    def test_includes_resource_fields_when_present(self):
        with (
            patch("runlayer_cli.command_metrics.detect_os", return_value="linux"),
            patch("runlayer_cli.command_metrics.detect_os_version", return_value="6"),
            patch(
                "runlayer_cli.command_metrics.detect_source",
                return_value="runlayer-pypi",
            ),
        ):
            event = build_command_event(
                command="scan",
                duration_ms=1234.5678,
                cpu_time_ms=456.789,
                peak_memory_mb=78.9012,
                disk_read_ops=123.0,
                disk_read_mb=45.6789,
                status="ok",
                error_type=None,
            )
        assert event["command"] == "scan"
        assert event["duration_ms"] == 1234.568
        assert event["cpu_time_ms"] == 456.789
        assert event["peak_memory_mb"] == 78.901
        assert event["disk_read_ops"] == 123
        assert event["disk_read_mb"] == 45.679
        assert event["os"] == "linux"
        assert event["os_version"] == "6"
        assert event["source"] == "runlayer-pypi"
        assert event["status"] == "ok"
        assert "error_type" not in event

    def test_omits_optional_fields_when_missing(self):
        with (
            patch("runlayer_cli.command_metrics.detect_os", return_value="darwin"),
            patch("runlayer_cli.command_metrics.detect_os_version", return_value=None),
            patch(
                "runlayer_cli.command_metrics.detect_source",
                return_value="aiwatch-binary",
            ),
        ):
            event = build_command_event(
                command="other",
                duration_ms=10.0,
                cpu_time_ms=None,
                peak_memory_mb=None,
                disk_read_ops=None,
                disk_read_mb=None,
                status="error",
                error_type="ValueError",
            )
        assert "cpu_time_ms" not in event
        assert "peak_memory_mb" not in event
        assert "disk_read_ops" not in event
        assert "disk_read_mb" not in event
        assert "os_version" not in event
        assert event["error_type"] == "ValueError"


class TestCaptureResourceUsage:
    def test_windows_job_assignment_failure_falls_back_to_self_usage(self):
        kernel32 = MagicMock()
        kernel32.CreateJobObjectW.return_value = 123
        kernel32.SetInformationJobObject.return_value = True
        kernel32.GetCurrentProcess.return_value = -1
        kernel32.AssignProcessToJobObject.return_value = False
        kernel32.CloseHandle.return_value = True
        client = MagicMock()
        ran: list[bool] = []

        with (
            patch.object(command_metrics.sys, "platform", "win32"),
            patch.object(
                command_metrics,
                "_windows_kernel32",
                return_value=kernel32,
            ),
            patch.object(
                command_metrics,
                "_capture_windows_process_usage",
                return_value=_usage(
                    cpu_time_ms=12.0,
                    peak_memory_mb=34.0,
                    disk_read_ops=56.0,
                    disk_read_mb=78.0,
                ),
            ),
            patch.object(command_metrics, "_telemetry_disabled", return_value=False),
            patch.object(
                command_metrics,
                "_resolve_report_target",
                return_value=("https://h", "sekret"),
            ),
            patch.object(command_metrics.sys, "argv", ["aiwatch", "scan"]),
            patch("runlayer_cli.api.RunlayerClient", return_value=client),
        ):
            run_with_command_metrics(lambda: ran.append(True))

        [event] = client.track_command_events.call_args.args[0]
        assert ran == [True]
        assert event["cpu_time_ms"] == 12.0
        assert event["peak_memory_mb"] == 34.0
        assert event["disk_read_ops"] == 56
        assert event["disk_read_mb"] == 78.0
        kernel32.AssignProcessToJobObject.assert_called_once()
        kernel32.CloseHandle.assert_called_once()

    def test_windows_job_query_failure_falls_back_per_metric(self):
        with (
            patch.object(
                command_metrics,
                "_capture_windows_job_usage",
                return_value=_usage(cpu_time_ms=123.0, disk_read_ops=456.0),
            ),
            patch.object(
                command_metrics,
                "_capture_windows_process_usage",
                return_value=_usage(
                    cpu_time_ms=12.0,
                    peak_memory_mb=34.0,
                    disk_read_ops=56.0,
                    disk_read_mb=78.0,
                ),
            ),
        ):
            usage = command_metrics._capture_resource_usage_windows(456)

        assert usage == _usage(
            cpu_time_ms=123.0,
            peak_memory_mb=34.0,
            disk_read_ops=456.0,
            disk_read_mb=78.0,
        )

    def test_windows_job_usage_includes_io_counters(self):
        kernel32 = MagicMock()

        def query_information(
            _job_handle,
            information_class,
            buffer,
            _buffer_size,
            _returned,
        ):
            if (
                information_class
                == command_metrics._JOB_OBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION_CLASS
            ):
                accounting_and_io = ctypes.cast(
                    buffer,
                    ctypes.POINTER(
                        command_metrics._JobObjectBasicAndIoAccountingInformation
                    ),
                ).contents
                accounting_and_io.BasicInfo.TotalUserTime = 10_000
                accounting_and_io.BasicInfo.TotalKernelTime = 20_000
                accounting_and_io.IoInfo.ReadOperationCount = 25
                accounting_and_io.IoInfo.ReadTransferCount = 8 * 1024 * 1024
            else:
                assert (
                    information_class
                    == command_metrics._JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS
                )
                limits = ctypes.cast(
                    buffer,
                    ctypes.POINTER(command_metrics._JobObjectExtendedLimitInformation),
                ).contents
                limits.PeakJobMemoryUsed = 4 * 1024 * 1024
            return True

        kernel32.QueryInformationJobObject.side_effect = query_information
        with patch.object(
            command_metrics,
            "_windows_kernel32",
            return_value=kernel32,
        ):
            usage = command_metrics._capture_windows_job_usage(456)

        assert usage == _usage(
            cpu_time_ms=3.0,
            peak_memory_mb=4.0,
            disk_read_ops=25.0,
            disk_read_mb=8.0,
        )

    def test_windows_process_usage_includes_io_counters(self):
        kernel32 = MagicMock()
        kernel32.GetCurrentProcess.return_value = 123

        def get_process_times(
            _process_handle,
            _creation,
            _exit_time,
            kernel_time,
            user_time,
        ):
            kernel = ctypes.cast(
                kernel_time,
                ctypes.POINTER(command_metrics.wintypes.FILETIME),
            ).contents
            user = ctypes.cast(
                user_time,
                ctypes.POINTER(command_metrics.wintypes.FILETIME),
            ).contents
            kernel.dwLowDateTime = 10_000
            user.dwLowDateTime = 20_000
            return True

        def get_process_io_counters(_process_handle, buffer):
            counters = ctypes.cast(
                buffer,
                ctypes.POINTER(command_metrics._IoCounters),
            ).contents
            counters.ReadOperationCount = 15
            counters.ReadTransferCount = 6 * 1024 * 1024
            return True

        kernel32.GetProcessTimes.side_effect = get_process_times
        kernel32.GetProcessIoCounters.side_effect = get_process_io_counters
        psapi = MagicMock()
        psapi.GetProcessMemoryInfo.return_value = False
        with (
            patch.object(
                command_metrics,
                "_windows_kernel32",
                return_value=kernel32,
            ),
            patch.object(
                command_metrics.ctypes,
                "WinDLL",
                return_value=psapi,
                create=True,
            ),
        ):
            usage = command_metrics._capture_windows_process_usage()

        assert usage == _usage(
            cpu_time_ms=3.0,
            disk_read_ops=15.0,
            disk_read_mb=6.0,
        )

    @pytest.mark.skipif(sys.platform != "win32", reason="requires Windows")
    def test_windows_includes_child_process_usage(self):
        probe = """
import json
import subprocess
import sys
from runlayer_cli import command_metrics

job_handle = command_metrics._start_windows_job_accounting()
if job_handle is None:
    raise RuntimeError("failed to start job accounting")

try:
    before = command_metrics._capture_resource_usage_windows(job_handle)
    child = '''
import time

allocation = bytearray(64 * 1024 * 1024)
for offset in range(0, len(allocation), 4096):
    allocation[offset] = 1
deadline = time.process_time() + 0.5
while time.process_time() < deadline:
    sum(value * value for value in range(10_000))
assert allocation
'''
    subprocess.run(
        [sys.executable, "-c", child],
        check=True,
        stdout=subprocess.DEVNULL,
        timeout=10,
    )
    after = command_metrics._capture_resource_usage_windows(job_handle)
    print(json.dumps({"before": before, "after": after}))
finally:
    command_metrics._close_windows_job_accounting(job_handle)
"""
        result = subprocess.run(
            [sys.executable, "-c", probe],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        usage = json.loads(result.stdout.splitlines()[-1])
        before_usage = usage["before"]
        after_usage = usage["after"]

        assert after_usage["cpu_time_ms"] > before_usage["cpu_time_ms"] + 250
        assert after_usage["peak_memory_mb"] > before_usage["peak_memory_mb"] + 32

    @pytest.mark.skipif(sys.platform != "win32", reason="requires Windows")
    def test_windows_returns_finite_positive_usage(self):
        allocation = bytearray(8 * 1024 * 1024)
        cpu_burn = sum(value * value for value in range(100_000))

        usage = command_metrics._capture_resource_usage_windows()

        assert allocation
        assert cpu_burn > 0
        assert usage["cpu_time_ms"] is not None
        assert usage["peak_memory_mb"] is not None
        assert usage["disk_read_ops"] is not None
        assert usage["disk_read_mb"] is not None
        assert math.isfinite(usage["cpu_time_ms"])
        assert math.isfinite(usage["peak_memory_mb"])
        assert math.isfinite(usage["disk_read_ops"])
        assert math.isfinite(usage["disk_read_mb"])
        assert usage["cpu_time_ms"] > 0
        assert usage["peak_memory_mb"] > 0

    def test_posix_linux_normalizes_maxrss_from_kib(self):
        rusage_self = _fake_rusage(
            utime=1.0,
            stime=0.5,
            maxrss=2048,
            inblock=3,
        )  # KiB on Linux
        rusage_children = _fake_rusage(
            utime=0.0,
            stime=0.0,
            maxrss=0,
            inblock=4,
        )
        with (
            patch("sys.platform", "linux"),
            patch("resource.getrusage", side_effect=[rusage_self, rusage_children]),
            patch.object(
                command_metrics,
                "_capture_linux_disk_read_usage",
                return_value={"disk_read_ops": 11.0, "disk_read_mb": 8.0},
            ),
        ):
            usage = command_metrics._capture_resource_usage()
        assert usage == _usage(
            cpu_time_ms=pytest.approx(1500.0),
            peak_memory_mb=pytest.approx(2.0),
            disk_read_ops=11.0,
            disk_read_mb=8.0,
        )

    def test_posix_darwin_normalizes_maxrss_from_bytes(self):
        rusage_self = _fake_rusage(
            utime=0.1,
            stime=0.1,
            maxrss=4 * 1024 * 1024,
            inblock=5,
        )
        rusage_children = _fake_rusage(utime=0.0, stime=0.0, maxrss=0)
        with (
            patch("sys.platform", "darwin"),
            patch("resource.getrusage", side_effect=[rusage_self, rusage_children]),
            patch.object(
                command_metrics,
                "_capture_macos_disk_read_mb",
                return_value=6.0,
            ),
        ):
            usage = command_metrics._capture_resource_usage()
        assert usage == _usage(
            cpu_time_ms=pytest.approx(200.0),
            peak_memory_mb=pytest.approx(4.0),
            disk_read_ops=5.0,
            disk_read_mb=6.0,
        )

    def test_linux_disk_read_usage_comes_from_logical_proc_self_io_counters(self):
        proc_io = "rchar: 8388608\nwchar: 456\nsyscr: 123\nread_bytes: 16777216\n"
        with patch.object(
            command_metrics.Path,
            "read_text",
            return_value=proc_io,
        ):
            usage = command_metrics._capture_linux_disk_read_usage()

        assert usage == {"disk_read_ops": 123.0, "disk_read_mb": 8.0}

    def test_linux_disk_read_capture_fails_dark(self):
        with patch.object(
            command_metrics.Path,
            "read_text",
            side_effect=OSError("procfs unavailable"),
        ):
            assert command_metrics._capture_linux_disk_read_usage() == {
                "disk_read_ops": None,
                "disk_read_mb": None,
            }

    @pytest.mark.parametrize(
        ("proc_io", "expected"),
        [
            (
                "syscr: 123\n",
                {"disk_read_ops": 123.0, "disk_read_mb": None},
            ),
            (
                "rchar: 8388608\n",
                {"disk_read_ops": None, "disk_read_mb": 8.0},
            ),
        ],
    )
    def test_linux_disk_read_capture_fails_dark_per_missing_counter(
        self,
        proc_io: str,
        expected: dict[str, float | None],
    ):
        with patch.object(command_metrics.Path, "read_text", return_value=proc_io):
            assert command_metrics._capture_linux_disk_read_usage() == expected

    def test_macos_disk_read_bytes_come_from_proc_pid_rusage(self):
        libproc = MagicMock()

        def proc_pid_rusage(_pid, _flavor, buffer):
            info = ctypes.cast(
                buffer,
                ctypes.POINTER(command_metrics._RusageInfoV2),
            ).contents
            info.ri_diskio_bytesread = 12 * 1024 * 1024
            return 0

        libproc.proc_pid_rusage.side_effect = proc_pid_rusage
        with (
            patch.object(command_metrics.ctypes, "CDLL", return_value=libproc),
            patch.object(command_metrics.os, "getpid", return_value=123),
        ):
            disk_read_mb = command_metrics._capture_macos_disk_read_mb()

        assert disk_read_mb == 12.0
        assert libproc.proc_pid_rusage.call_args.args[:2] == (
            123,
            command_metrics._RUSAGE_INFO_V2,
        )

    def test_posix_byte_capture_survives_rusage_failure(self):
        with (
            patch("sys.platform", "linux"),
            patch("resource.getrusage", side_effect=OSError("boom")),
            patch.object(
                command_metrics,
                "_capture_linux_disk_read_usage",
                return_value={"disk_read_ops": 4.0, "disk_read_mb": 9.0},
            ),
        ):
            usage = command_metrics._capture_resource_usage()

        assert usage == _usage(disk_read_ops=4.0, disk_read_mb=9.0)

    def test_capture_failure_returns_none_none(self):
        with (
            patch("sys.platform", "linux"),
            patch("resource.getrusage", side_effect=OSError("boom")),
            patch.object(
                command_metrics,
                "_capture_linux_disk_read_usage",
                return_value={"disk_read_ops": None, "disk_read_mb": None},
            ),
        ):
            assert command_metrics._capture_resource_usage() == _usage()

    def test_dispatch_uses_windows_path_on_win32(self):
        with (
            patch("sys.platform", "win32"),
            patch.object(
                command_metrics,
                "_capture_resource_usage_windows",
                return_value=_usage(cpu_time_ms=12.0, peak_memory_mb=34.0),
            ),
        ):
            assert command_metrics._capture_resource_usage() == _usage(
                cpu_time_ms=12.0,
                peak_memory_mb=34.0,
            )


class TestRunWithCommandMetrics:
    def test_windows_closes_job_after_report(self):
        with (
            patch.object(command_metrics.sys, "platform", "win32"),
            patch.object(
                command_metrics,
                "_start_windows_job_accounting",
                return_value=123,
            ),
            patch.object(command_metrics, "_close_windows_job_accounting") as close,
            patch.object(command_metrics, "_telemetry_disabled", return_value=False),
            patch.object(command_metrics, "_report_command") as report,
        ):
            run_with_command_metrics(lambda: None)

        assert report.call_args.kwargs["job_handle"] == 123
        close.assert_called_once_with(123)

    def test_disabled_runs_app_and_skips_report(self):
        ran: list[int] = []
        with (
            patch.object(command_metrics, "_telemetry_disabled", return_value=True),
            patch.object(command_metrics, "_report_command") as report,
        ):
            run_with_command_metrics(lambda: ran.append(1))
        assert ran == [1]
        report.assert_not_called()

    def test_success_reports_ok(self):
        with (
            patch.object(command_metrics, "_telemetry_disabled", return_value=False),
            patch.object(command_metrics, "_report_command") as report,
        ):
            run_with_command_metrics(lambda: None)
        report.assert_called_once()
        assert report.call_args.kwargs["status"] == "ok"
        assert report.call_args.kwargs["error_type"] is None

    def test_systemexit_zero_reports_ok(self):
        def app() -> None:
            raise SystemExit(0)

        with (
            patch.object(command_metrics, "_telemetry_disabled", return_value=False),
            patch.object(command_metrics, "_report_command") as report,
            pytest.raises(SystemExit),
        ):
            run_with_command_metrics(app)
        assert report.call_args.kwargs["status"] == "ok"

    def test_systemexit_nonzero_reports_error(self):
        def app() -> None:
            raise SystemExit(1)

        with (
            patch.object(command_metrics, "_telemetry_disabled", return_value=False),
            patch.object(command_metrics, "_report_command") as report,
            pytest.raises(SystemExit),
        ):
            run_with_command_metrics(app)
        assert report.call_args.kwargs["status"] == "error"
        assert report.call_args.kwargs["error_type"] is None

    def test_unhandled_exception_reports_error_type(self):
        def app() -> None:
            raise ValueError("boom")

        with (
            patch.object(command_metrics, "_telemetry_disabled", return_value=False),
            patch.object(command_metrics, "_report_command") as report,
            pytest.raises(ValueError),
        ):
            run_with_command_metrics(app)
        assert report.call_args.kwargs["status"] == "error"
        assert report.call_args.kwargs["error_type"] == "ValueError"

    def test_command_can_suppress_exit_path_report(self):
        def app() -> None:
            command_metrics.suppress_current_command_metrics()
            raise SystemExit(0)

        with (
            patch.object(command_metrics, "_telemetry_disabled", return_value=False),
            patch.object(command_metrics, "_report_command") as report,
            pytest.raises(SystemExit),
        ):
            run_with_command_metrics(app)

        report.assert_not_called()

    def test_command_metrics_suppression_resets_for_next_invocation(self):
        with (
            patch.object(command_metrics, "_telemetry_disabled", return_value=False),
            patch.object(command_metrics, "_report_command") as report,
        ):
            run_with_command_metrics(command_metrics.suppress_current_command_metrics)
            run_with_command_metrics(lambda: None)

        report.assert_called_once()


class TestReportCommand:
    def test_skips_when_unauthenticated(self):
        with (
            patch.object(
                command_metrics, "_resolve_report_target", return_value=(None, None)
            ),
            patch("runlayer_cli.api.RunlayerClient") as client_cls,
        ):
            command_metrics._report_command(
                duration_ms=5.0, status="ok", error_type=None
            )
        client_cls.assert_not_called()

    def test_posts_event_when_authenticated(self):
        client = MagicMock()
        with (
            patch.object(
                command_metrics,
                "_resolve_report_target",
                return_value=("https://h", "sekret"),
            ),
            patch.object(
                command_metrics,
                "_capture_resource_usage",
                return_value=_usage(
                    cpu_time_ms=11.0,
                    peak_memory_mb=22.0,
                    disk_read_ops=33.0,
                    disk_read_mb=44.0,
                ),
            ),
            patch.object(command_metrics.sys, "argv", ["runlayer", "scan"]),
            patch("runlayer_cli.api.RunlayerClient", return_value=client) as client_cls,
        ):
            command_metrics._report_command(
                duration_ms=5.0, status="ok", error_type=None
            )
        client_cls.assert_called_once_with(hostname="https://h", secret="sekret")
        events = client.track_command_events.call_args.args[0]
        assert len(events) == 1
        assert events[0]["command"] == "scan"
        assert events[0]["cpu_time_ms"] == 11.0
        assert events[0]["peak_memory_mb"] == 22.0
        assert events[0]["disk_read_ops"] == 33
        assert events[0]["disk_read_mb"] == 44.0

    def test_daemon_exit_posts_daemon_command_event(self):
        client = MagicMock()
        with (
            patch.object(
                command_metrics,
                "_resolve_report_target",
                return_value=("https://h", "sekret"),
            ),
            patch.object(
                command_metrics,
                "_capture_resource_usage",
                return_value=_usage(),
            ),
            patch.object(command_metrics.sys, "argv", ["aiwatch", "daemon"]),
            patch("runlayer_cli.api.RunlayerClient", return_value=client),
        ):
            command_metrics._report_command(
                duration_ms=3_600_000.0,
                status="ok",
                error_type=None,
            )

        [event] = client.track_command_events.call_args.args[0]
        assert event["command"] == "daemon"
        assert event["duration_ms"] == 3_600_000.0
        assert event["status"] == "ok"

    def test_never_raises_on_flush_failure(self):
        with (
            patch.object(
                command_metrics,
                "_resolve_report_target",
                return_value=("https://h", "sekret"),
            ),
            patch.object(
                command_metrics,
                "_capture_resource_usage",
                return_value=_usage(),
            ),
            patch(
                "runlayer_cli.api.RunlayerClient",
                side_effect=RuntimeError("network down"),
            ),
        ):
            # Must swallow — telemetry never breaks command exit.
            command_metrics._report_command(
                duration_ms=5.0, status="ok", error_type=None
            )


class TestResolveReportTarget:
    def test_prefers_env(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("RUNLAYER_HOST", "https://env-host/")
        monkeypatch.setenv("RUNLAYER_API_KEY", "env-secret")
        host, secret = command_metrics._resolve_report_target()
        assert host == "https://env-host"
        assert secret == "env-secret"

    def test_falls_back_to_config(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("RUNLAYER_HOST", raising=False)
        monkeypatch.delenv("RUNLAYER_API_KEY", raising=False)
        config = MagicMock()
        config.default_host = "https://config-host"
        config.hosts = {}
        config.get_secret_for_host.return_value = "config-secret"
        with patch("runlayer_cli.config.load_config", return_value=config):
            host, secret = command_metrics._resolve_report_target()
        assert host == "https://config-host"
        assert secret == "config-secret"

    def test_returns_none_when_unresolved(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("RUNLAYER_HOST", raising=False)
        monkeypatch.delenv("RUNLAYER_API_KEY", raising=False)
        config = MagicMock()
        config.default_host = None
        config.hosts = {}
        config.get_secret_for_host.return_value = None
        with patch("runlayer_cli.config.load_config", return_value=config):
            assert command_metrics._resolve_report_target() == (None, None)


class TestMetricsFailureLogging:
    """Reproduction (ENG-4130): the best-effort flush-failure diagnostic must not
    leak on unconfigured-logger paths (``--version`` / ``--help`` / invalid),
    which never call ``setup_logging``. ``run_with_command_metrics`` installs a
    level-filtered stderr logger first, so the ``cli_command_metrics_skipped``
    debug line is silent by default and only surfaces under ``LOG_LEVEL=DEBUG``.
    """

    @pytest.fixture(autouse=True)
    def _fresh_structlog(self, monkeypatch):
        # Reset global structlog config AND swap in a fresh module logger.
        # structlog's lazy proxy permanently caches its bound logger the first
        # time it is used while ``cache_logger_on_first_use`` is True (e.g. left
        # on by a prior test's ``setup_logging``), and ``reset_defaults`` cannot
        # undo that. A fresh proxy + reset reproduces a real CLI process, where
        # ``ensure_base_logging_configured`` (cache=False) runs before any log.
        structlog.reset_defaults()
        monkeypatch.setattr(
            command_metrics, "logger", structlog.get_logger(command_metrics.__name__)
        )
        yield
        structlog.reset_defaults()

    @staticmethod
    def _failing_flush():
        """Patches for a metrics flush that resolves creds then raises on POST."""
        return (
            patch.object(command_metrics, "_telemetry_disabled", return_value=False),
            patch.object(
                command_metrics,
                "_resolve_report_target",
                return_value=("https://h", "sekret"),
            ),
            patch.object(
                command_metrics,
                "_capture_resource_usage",
                return_value=_usage(),
            ),
            patch(
                "runlayer_cli.api.RunlayerClient",
                side_effect=RuntimeError("metrics backend down"),
            ),
        )

    def test_flush_failure_silent_when_logger_unconfigured(self, capsys, monkeypatch):
        monkeypatch.delenv("LOG_LEVEL", raising=False)
        p1, p2, p3, p4 = self._failing_flush()
        with p1, p2, p3, p4:
            run_with_command_metrics(lambda: None)

        captured = capsys.readouterr()
        assert "cli_command_metrics_skipped" not in captured.out
        assert "cli_command_metrics_skipped" not in captured.err

    def test_flush_failure_visible_under_debug(self, capsys, monkeypatch):
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        p1, p2, p3, p4 = self._failing_flush()
        with p1, p2, p3, p4:
            run_with_command_metrics(lambda: None)

        captured = capsys.readouterr()
        # Diagnostic surfaces on stderr, never stdout.
        assert captured.out == ""
        assert "cli_command_metrics_skipped" in captured.err
