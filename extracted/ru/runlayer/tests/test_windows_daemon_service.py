"""Cross-platform tests for the Windows daemon service policy."""

from __future__ import annotations

import ctypes
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest

from runlayer_cli.daemon import windows_scm, windows_service
from runlayer_cli.hook_install import daemon_lifecycle

_AIWATCH_WXS = Path(__file__).parent.parent / "packaging" / "windows" / "aiwatch.wxs"


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


@dataclass
class FakeProcess:
    exit_code: int | None = None
    terminated: bool = False
    closed: bool = False

    def poll(self) -> int | None:
        return self.exit_code

    def terminate(self) -> None:
        self.terminated = True

    def close(self) -> None:
        self.closed = True


def _supervisor(
    spawn,
    clock: FakeClock,
    *,
    should_stop=lambda: False,
    wait=lambda _delay: None,
    on_spawn_failure=None,
) -> windows_service.SessionSupervisor:
    return windows_service.SessionSupervisor(
        list_sessions=lambda: (),
        spawn=spawn,
        should_stop=should_stop,
        wait=wait,
        clock=clock,
        on_spawn_failure=on_spawn_failure,
    )


def _api_with_wts_sessions(
    records: list[tuple[int, int]],
) -> windows_service._WindowsAPI:
    wintypes = windows_service.wintypes

    class SessionInfo(ctypes.Structure):
        _fields_ = [
            ("SessionId", wintypes.DWORD),
            ("pWinStationName", wintypes.LPWSTR),
            ("State", wintypes.DWORD),
        ]

    session_records = (SessionInfo * len(records))(
        *(SessionInfo(session_id, None, state) for session_id, state in records)
    )

    def enumerate_sessions(
        _server,
        _reserved,
        _version,
        sessions_pointer,
        count_pointer,
    ) -> bool:
        ctypes.cast(
            sessions_pointer,
            ctypes.POINTER(ctypes.POINTER(SessionInfo)),
        )[0] = ctypes.cast(session_records, ctypes.POINTER(SessionInfo))
        ctypes.cast(
            count_pointer,
            ctypes.POINTER(wintypes.DWORD),
        ).contents.value = len(session_records)
        return True

    api = object.__new__(windows_service._WindowsAPI)
    api._ctypes = ctypes
    api._wintypes = wintypes
    api.WTS_SESSION_INFOW = SessionInfo
    api._wtsapi32 = SimpleNamespace(
        WTSEnumerateSessionsW=enumerate_sessions,
        WTSFreeMemory=lambda _memory: None,
    )
    return api


def test_reconcile_starts_one_child_per_active_session() -> None:
    clock = FakeClock()
    spawned: list[tuple[int, FakeProcess]] = []

    def spawn(session_id: int) -> FakeProcess:
        process = FakeProcess()
        spawned.append((session_id, process))
        return process

    supervisor = _supervisor(spawn, clock)

    delay = supervisor.reconcile([2, 1, 2, 0, -1, True])
    supervisor.reconcile([1, 2])

    assert [session_id for session_id, _process in spawned] == [1, 2]
    assert supervisor.child_sessions == frozenset({1, 2})
    assert delay == windows_service.POLL_INTERVAL_SECONDS


def test_logoff_terminates_and_forgets_child() -> None:
    clock = FakeClock()
    process = FakeProcess()
    supervisor = _supervisor(lambda _session_id: process, clock)
    supervisor.reconcile([7])

    supervisor.reconcile([])

    assert process.terminated
    assert process.closed
    assert supervisor.child_sessions == frozenset()


def test_nonzero_exit_relaunches_after_one_minute() -> None:
    clock = FakeClock()
    processes: list[FakeProcess] = []

    def spawn(_session_id: int) -> FakeProcess:
        process = FakeProcess()
        processes.append(process)
        return process

    supervisor = _supervisor(spawn, clock)
    supervisor.reconcile([4])
    processes[0].exit_code = 9
    supervisor.reconcile([4])

    clock.advance(59)
    supervisor.reconcile([4])
    assert len(processes) == 1

    clock.advance(1)
    supervisor.reconcile([4])
    assert len(processes) == 2
    assert processes[0].closed
    assert not processes[0].terminated


def test_clean_gate_off_exit_relaunches_only_hourly() -> None:
    clock = FakeClock()
    processes: list[FakeProcess] = []

    def spawn(_session_id: int) -> FakeProcess:
        process = FakeProcess()
        processes.append(process)
        return process

    supervisor = _supervisor(spawn, clock)
    supervisor.reconcile([11])
    processes[0].exit_code = 0
    supervisor.reconcile([11])

    clock.advance(3599)
    supervisor.reconcile([11])
    assert len(processes) == 1

    clock.advance(1)
    supervisor.reconcile([11])
    assert len(processes) == 2


def test_spawn_failure_uses_failure_retry_without_busy_loop() -> None:
    clock = FakeClock()
    attempts: list[int] = []

    def spawn(session_id: int) -> FakeProcess:
        attempts.append(session_id)
        if len(attempts) == 1:
            raise OSError("token unavailable")
        return FakeProcess()

    supervisor = _supervisor(spawn, clock)

    assert supervisor.reconcile([3]) == windows_service.POLL_INTERVAL_SECONDS
    clock.advance(59)
    supervisor.reconcile([3])
    assert attempts == [3]

    clock.advance(1)
    supervisor.reconcile([3])
    assert attempts == [3, 3]


def test_spawn_failure_reports_once_until_session_recovers() -> None:
    clock = FakeClock()
    failures: list[tuple[int, str]] = []

    def spawn(_session_id: int) -> FakeProcess:
        raise OSError(5, "CreateProcessAsUserW failed")

    supervisor = _supervisor(
        spawn,
        clock,
        on_spawn_failure=lambda session_id, exc: failures.append(
            (session_id, str(exc))
        ),
    )

    supervisor.reconcile([3])
    clock.advance(60)
    supervisor.reconcile([3])
    assert failures == [(3, "[Errno 5] CreateProcessAsUserW failed")]

    supervisor.reconcile([])
    supervisor.reconcile([3])
    assert failures == [
        (3, "[Errno 5] CreateProcessAsUserW failed"),
        (3, "[Errno 5] CreateProcessAsUserW failed"),
    ]


def test_spawn_failure_reports_when_diagnostic_changes() -> None:
    clock = FakeClock()
    attempts = 0
    failures: list[str] = []

    def spawn(_session_id: int) -> FakeProcess:
        nonlocal attempts
        attempts += 1
        operation = (
            "CreateEnvironmentBlock" if attempts == 1 else "CreateProcessAsUserW"
        )
        raise OSError(5, f"{operation} failed")

    supervisor = _supervisor(
        spawn,
        clock,
        on_spawn_failure=lambda _session_id, exc: failures.append(str(exc)),
    )

    supervisor.reconcile([3])
    clock.advance(60)
    supervisor.reconcile([3])
    clock.advance(60)
    supervisor.reconcile([3])

    assert failures == [
        "[Errno 5] CreateEnvironmentBlock failed",
        "[Errno 5] CreateProcessAsUserW failed",
    ]


def test_missing_session_token_retries_only_hourly() -> None:
    clock = FakeClock()
    attempts: list[int] = []
    failures: list[int] = []

    def spawn(session_id: int) -> FakeProcess:
        attempts.append(session_id)
        raise windows_service.SessionTokenUnavailable(1008, "token unavailable")

    supervisor = _supervisor(
        spawn,
        clock,
        on_spawn_failure=lambda session_id, _exc: failures.append(session_id),
    )

    supervisor.reconcile([3])
    clock.advance(60)
    supervisor.reconcile([3])
    assert attempts == [3]

    clock.advance(3540)
    supervisor.reconcile([3])
    assert attempts == [3, 3]
    assert failures == [3]


def test_session_change_clears_token_unavailable_backoff() -> None:
    clock = FakeClock()
    attempts: list[int] = []
    token_available = False

    def spawn(session_id: int) -> FakeProcess:
        attempts.append(session_id)
        if not token_available:
            raise windows_service.SessionTokenUnavailable(1008, "token unavailable")
        return FakeProcess()

    supervisor = _supervisor(spawn, clock)
    supervisor.reconcile([3])
    assert attempts == [3]

    token_available = True
    clock.advance(5)
    supervisor.reconcile([3])
    assert attempts == [3]

    supervisor.note_session_change()
    clock.advance(5)
    supervisor.reconcile([3])
    assert attempts == [3, 3]
    assert supervisor.child_sessions == frozenset({3})


def test_session_change_rearms_breadcrumb_after_token_becomes_available() -> None:
    clock = FakeClock()
    token_available = False
    failures: list[str] = []

    def spawn(_session_id: int) -> FakeProcess:
        if not token_available:
            raise windows_service.SessionTokenUnavailable(1008, "token unavailable")
        raise OSError(5, "CreateProcessAsUserW failed")

    supervisor = _supervisor(
        spawn,
        clock,
        on_spawn_failure=lambda _session_id, exc: failures.append(str(exc)),
    )
    supervisor.reconcile([3])

    token_available = True
    supervisor.note_session_change()
    supervisor.reconcile([3])

    assert failures == [
        "[Errno 1008] token unavailable",
        "[Errno 5] CreateProcessAsUserW failed",
    ]


def test_session_change_keeps_clean_exit_and_failure_backoffs() -> None:
    clock = FakeClock()
    processes: list[FakeProcess] = []
    failing = False

    def spawn(_session_id: int) -> FakeProcess:
        if failing:
            raise OSError("spawn failed")
        process = FakeProcess()
        processes.append(process)
        return process

    supervisor = _supervisor(spawn, clock)
    supervisor.reconcile([11])
    processes[0].exit_code = 0
    supervisor.reconcile([11])

    supervisor.note_session_change()
    clock.advance(5)
    supervisor.reconcile([11])
    assert len(processes) == 1

    failing = True
    clock.advance(3600)
    supervisor.reconcile([11])
    failing = False
    supervisor.note_session_change()
    clock.advance(5)
    supervisor.reconcile([11])
    assert len(processes) == 1


def test_wts_no_token_is_classified_as_session_token_unavailable() -> None:
    class FakeCtypes:
        byref = staticmethod(ctypes.byref)
        get_last_error = staticmethod(lambda: 1008)

    api = object.__new__(windows_service._WindowsAPI)
    api._ctypes = FakeCtypes()
    api._wintypes = windows_service.wintypes
    api._wtsapi32 = SimpleNamespace(WTSQueryUserToken=lambda *_args: False)

    with pytest.raises(windows_service.SessionTokenUnavailable):
        api.spawn_daemon(3)


def test_service_loop_waits_and_terminates_children_on_stop() -> None:
    clock = FakeClock()
    process = FakeProcess()
    stopping = False
    waits: list[float] = []

    def wait(delay: float) -> None:
        nonlocal stopping
        waits.append(delay)
        stopping = True

    supervisor = windows_service.SessionSupervisor(
        list_sessions=lambda: [8],
        spawn=lambda _session_id: process,
        should_stop=lambda: stopping,
        wait=wait,
        clock=clock,
    )

    supervisor.run()

    assert waits == [windows_service.POLL_INTERVAL_SECONDS]
    assert process.terminated
    assert process.closed
    assert supervisor.child_sessions == frozenset()


def test_non_windows_entrypoint_does_not_construct_ctypes_backend(monkeypatch) -> None:
    class UnexpectedBackend:
        def __init__(self, _executable: str) -> None:
            raise AssertionError("Windows APIs loaded off Windows")

    monkeypatch.setattr(windows_service.sys, "platform", "darwin")
    monkeypatch.setattr(windows_service, "_WindowsAPI", UnexpectedBackend)

    assert windows_service.run_service() == 0


def test_windows_entrypoint_reports_dispatch_failure(monkeypatch) -> None:
    reports: list[str] = []

    class FakeAPI:
        def __init__(self, _executable: str) -> None:
            pass

        def report_error(self, message: str) -> None:
            reports.append(message)

    class FailingHost:
        def __init__(self, _api: FakeAPI) -> None:
            pass

        def dispatch(self) -> None:
            raise OSError(1063, "StartServiceCtrlDispatcherW failed")

    monkeypatch.setattr(windows_service.sys, "platform", "win32")
    monkeypatch.setattr(windows_service, "_WindowsAPI", FakeAPI)
    monkeypatch.setattr(windows_service, "_WindowsServiceHost", FailingHost)

    assert windows_service.run_service() == 1
    assert len(reports) == 1
    assert "StartServiceCtrlDispatcherW failed" in reports[0]


def test_non_windows_service_query_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(windows_scm.sys, "platform", "darwin")

    assert windows_scm.query_service_state() is None
    assert windows_scm.query_service_config() is None


def test_windows_service_query_reads_binary_path_and_closes_handles(
    monkeypatch,
) -> None:
    expected = r'"C:\Program Files\Runlayer\AIWatch\aiwatch.exe" daemon-service'
    wintypes = windows_scm.wintypes

    class QueryServiceConfig(ctypes.Structure):
        _fields_ = [
            ("dwServiceType", wintypes.DWORD),
            ("dwStartType", wintypes.DWORD),
            ("dwErrorControl", wintypes.DWORD),
            ("lpBinaryPathName", wintypes.LPWSTR),
            ("lpLoadOrderGroup", wintypes.LPWSTR),
            ("dwTagId", wintypes.DWORD),
            ("lpDependencies", wintypes.LPWSTR),
            ("lpServiceStartName", wintypes.LPWSTR),
            ("lpDisplayName", wintypes.LPWSTR),
        ]

    config = QueryServiceConfig(
        dwStartType=windows_scm.SERVICE_AUTO_START,
        lpBinaryPathName=expected,
    )
    closed: list[int] = []

    class FakeFunction:
        def __init__(self, implementation) -> None:
            self.implementation = implementation
            self.argtypes = None
            self.restype = None

        def __call__(self, *args):
            return self.implementation(*args)

    def query(_service, buffer, _size, needed_pointer):
        needed = ctypes.cast(needed_pointer, ctypes.POINTER(wintypes.DWORD))
        needed.contents.value = ctypes.sizeof(config)
        if buffer is None:
            return False
        ctypes.memmove(buffer, ctypes.byref(config), ctypes.sizeof(config))
        return True

    class FakeAdvapi:
        OpenSCManagerW = FakeFunction(lambda *_args: 11)
        OpenServiceW = FakeFunction(lambda *_args: 22)
        QueryServiceStatusEx = FakeFunction(lambda *_args: False)
        QueryServiceConfigW = FakeFunction(query)
        CloseServiceHandle = FakeFunction(lambda handle: closed.append(handle) or True)

    monkeypatch.setattr(windows_scm.sys, "platform", "win32")
    monkeypatch.setattr(
        windows_scm.ctypes,
        "WinDLL",
        lambda *_args, **_kwargs: FakeAdvapi(),
        raising=False,
    )

    assert windows_scm.query_service_config() == windows_scm.ServiceConfig(
        binary_path=expected,
        start_type=windows_scm.SERVICE_AUTO_START,
    )
    assert closed == [22, 11]


def test_windows_service_query_surfaces_open_access_denied(monkeypatch) -> None:
    closed: list[int] = []

    class FakeFunction:
        def __init__(self, implementation) -> None:
            self.implementation = implementation
            self.argtypes = None
            self.restype = None

        def __call__(self, *args):
            return self.implementation(*args)

    class FakeAdvapi:
        OpenSCManagerW = FakeFunction(lambda *_args: 11)
        OpenServiceW = FakeFunction(lambda *_args: 0)
        QueryServiceStatusEx = FakeFunction(lambda *_args: False)
        QueryServiceConfigW = FakeFunction(lambda *_args: False)
        CloseServiceHandle = FakeFunction(lambda handle: closed.append(handle) or True)

    monkeypatch.setattr(windows_scm.sys, "platform", "win32")
    monkeypatch.setattr(windows_scm.ctypes, "get_last_error", lambda: 5, raising=False)
    monkeypatch.setattr(
        windows_scm.ctypes,
        "WinDLL",
        lambda *_args, **_kwargs: FakeAdvapi(),
        raising=False,
    )

    with pytest.raises(OSError) as exc_info:
        windows_scm.query_service_state()

    assert exc_info.value.errno == 5
    assert "OpenServiceW" in str(exc_info.value)
    assert closed == [11]


@pytest.mark.parametrize(
    ("session_id", "state", "user_sid", "expected"),
    [
        (1, 0, "S-1-5-21-1000", True),
        (2, 4, "S-1-5-21-1000", True),
        (3, 0, "S-1-5-18", False),
        (4, 4, "S-1-5-20", False),
        (0, 0, "S-1-5-21-1000", False),
        (5, 1, "S-1-5-21-1000", False),
    ],
)
def test_supervised_wts_sessions_include_disconnected_users(
    session_id: int,
    state: int,
    user_sid: str,
    expected: bool,
) -> None:
    assert (
        windows_service._is_supervised_session(session_id, state, user_sid) is expected
    )


def test_active_sessions_filter_service_accounts_by_token_sid() -> None:
    api = _api_with_wts_sessions(
        [
            (7, windows_service._WTS_ACTIVE),
            (8, windows_service._WTS_DISCONNECTED),
        ]
    )
    # Local/domain users may legitimately be named SYSTEM; localized service
    # account names are equally unsuitable as an identity boundary.
    api._session_username = lambda session_id: {
        7: "SYSTEM",
        8: "Lokaler Dienst",
    }[session_id]
    api._session_user_sid = lambda session_id: {
        7: "S-1-5-21-1000",
        8: "S-1-5-19",
    }[session_id]

    assert api.active_session_ids() == [7]


def test_disconnected_session_with_no_token_still_reaches_supervisor() -> None:
    api = _api_with_wts_sessions([(9, windows_service._WTS_DISCONNECTED)])

    def no_token(_session_id: int) -> str:
        raise windows_service.SessionTokenUnavailable(1008, "token unavailable")

    api._session_user_sid = no_token

    assert api.active_session_ids() == [9]


def test_active_sessions_isolate_sid_lookup_errors() -> None:
    api = _api_with_wts_sessions(
        [
            (9, windows_service._WTS_ACTIVE),
            (10, windows_service._WTS_ACTIVE),
        ]
    )

    def user_sid(session_id: int) -> str:
        if session_id == 9:
            raise OSError(5, "GetTokenInformation failed")
        return "S-1-5-21-1000"

    api._session_user_sid = user_sid

    assert api.active_session_ids() == [9, 10]


def test_session_user_sid_comes_from_wts_token_and_closes_it() -> None:
    calls: list[tuple[str, int]] = []
    api = object.__new__(windows_service._WindowsAPI)
    api._query_user_token = lambda session_id: calls.append(("query", session_id)) or 41
    api._token_user_sid = lambda token: calls.append(("sid", token)) or "S-1-5-21-1000"
    api._close_handle_quietly = lambda token: calls.append(("close", token))

    assert api._session_user_sid(7) == "S-1-5-21-1000"
    assert calls == [("query", 7), ("sid", 41), ("close", 41)]


def test_token_user_sid_reads_authoritative_token_identity() -> None:
    wintypes = windows_service.wintypes
    sid_bytes = ctypes.create_string_buffer(b"\x01")
    sid_text = ctypes.create_unicode_buffer("S-1-5-21-1000")
    freed: list[str | None] = []

    class FakeAdvapi:
        @staticmethod
        def GetTokenInformation(
            _token,
            _information_class,
            buffer,
            _buffer_size,
            required_pointer,
        ) -> bool:
            required = ctypes.cast(
                required_pointer,
                ctypes.POINTER(wintypes.DWORD),
            )
            required.contents.value = ctypes.sizeof(ctypes.c_void_p)
            if buffer is None:
                return False
            ctypes.cast(
                buffer,
                ctypes.POINTER(ctypes.c_void_p),
            ).contents.value = ctypes.addressof(sid_bytes)
            return True

        @staticmethod
        def ConvertSidToStringSidW(_sid, string_pointer) -> bool:
            ctypes.cast(
                string_pointer,
                ctypes.POINTER(wintypes.LPWSTR),
            )[0] = ctypes.cast(sid_text, wintypes.LPWSTR)
            return True

    class FakeKernel:
        @staticmethod
        def LocalFree(sid_string) -> None:
            freed.append(ctypes.cast(sid_string, wintypes.LPWSTR).value)

    api = object.__new__(windows_service._WindowsAPI)
    api._ctypes = ctypes
    api._wintypes = wintypes
    api._advapi32 = FakeAdvapi()
    api._kernel32 = FakeKernel()

    assert api._token_user_sid(41) == "S-1-5-21-1000"
    assert freed == ["S-1-5-21-1000"]


@pytest.mark.parametrize("service_sid", ["S-1-5-18", "S-1-5-19", "S-1-5-20"])
def test_spawn_rejects_service_account_token_before_process_creation(
    service_sid: str,
) -> None:
    calls: list[tuple[str, int]] = []
    api = object.__new__(windows_service._WindowsAPI)
    api._ctypes = ctypes
    api._wintypes = windows_service.wintypes
    api._query_user_token = lambda session_id: calls.append(("query", session_id)) or 41
    api._token_user_sid = lambda token: calls.append(("sid", token)) or service_sid
    api._close_handle_quietly = lambda token: calls.append(("close", token))
    api._userenv = SimpleNamespace(
        CreateEnvironmentBlock=lambda *_args: pytest.fail(
            "service account token reached process creation"
        )
    )

    with pytest.raises(PermissionError, match=service_sid):
        api.spawn_daemon(7)

    assert calls == [("query", 7), ("sid", 41), ("close", 41)]


def test_spawn_fails_closed_when_actual_token_sid_lookup_fails() -> None:
    closed: list[int] = []
    api = object.__new__(windows_service._WindowsAPI)
    api._ctypes = ctypes
    api._wintypes = windows_service.wintypes
    api._query_user_token = lambda _session_id: 41

    def fail_sid_lookup(_token: int) -> str:
        raise OSError(5, "GetTokenInformation failed")

    api._token_user_sid = fail_sid_lookup
    api._close_handle_quietly = closed.append
    api._userenv = SimpleNamespace(
        CreateEnvironmentBlock=lambda *_args: pytest.fail(
            "unverified token reached process creation"
        )
    )

    with pytest.raises(OSError, match="GetTokenInformation failed"):
        api.spawn_daemon(7)

    assert closed == [41]


def test_windows_process_job_closes_before_parent_process_handle() -> None:
    class FakeProcessAPI:
        def __init__(self) -> None:
            self.calls: list[tuple[str, int]] = []

        def poll_process(self, _handle: int) -> int | None:
            return None

        def terminate_process(self, handle: int) -> None:
            self.calls.append(("terminate", handle))

        def close_handle(self, handle: int) -> None:
            self.calls.append(("close", handle))

    api = FakeProcessAPI()
    process = windows_service._WindowsProcess(api, 11, 22)  # type: ignore[arg-type]

    process.terminate()
    process.close()

    assert api.calls == [("close", 22), ("terminate", 11), ("close", 11)]


def test_windows_process_natural_exit_closes_kill_on_close_job() -> None:
    class FakeProcessAPI:
        def __init__(self) -> None:
            self.closed: list[int] = []

        def poll_process(self, _handle: int) -> int | None:
            return 0

        def terminate_process(self, _handle: int) -> None:
            raise AssertionError("natural process close must not terminate directly")

        def close_handle(self, handle: int) -> None:
            self.closed.append(handle)

    api = FakeProcessAPI()
    process = windows_service._WindowsProcess(api, 31, 32)  # type: ignore[arg-type]

    process.close()

    assert api.closed == [32, 31]


def test_scm_host_reports_full_lifecycle_for_stop_and_shutdown() -> None:
    api_without_windows_dlls = object.__new__(windows_service._WindowsAPI)
    assert api_without_windows_dlls.running_controls() == 0x85

    for control in (
        windows_service._SERVICE_CONTROL_STOP,
        windows_service._SERVICE_CONTROL_SHUTDOWN,
    ):

        class FakeServiceAPI:
            def __init__(self) -> None:
                self.handler = None
                self.statuses: list[dict[str, int]] = []

            def dispatch_service(self, service_name, service_main) -> None:
                assert service_name == windows_service.SERVICE_NAME
                service_main(0, None)

            def register_control_handler(self, service_name, handler):
                assert service_name == windows_service.SERVICE_NAME
                self.handler = handler
                return 42, object()

            def active_session_ids(self) -> list[int]:
                assert self.handler is not None
                self.handler(control, 0, None, None)
                return []

            def spawn_daemon(self, _session_id: int) -> FakeProcess:
                raise AssertionError("stop raced into a new child spawn")

            def running_controls(self) -> int:
                return 0x85

            def set_service_status(self, _handle: int, **status: int) -> None:
                self.statuses.append(status)

        api = FakeServiceAPI()
        host = windows_service._WindowsServiceHost(api)  # type: ignore[arg-type]
        host.dispatch()

        assert host._supervisor is not None
        assert [status["state"] for status in api.statuses] == [
            windows_service._SERVICE_START_PENDING,
            windows_service.SERVICE_RUNNING,
            windows_service._SERVICE_STOP_PENDING,
            windows_service.SERVICE_STOPPED,
        ]
        assert api.statuses[1]["controls"] == 0x85
        assert all(
            status["controls"] == 0
            for index, status in enumerate(api.statuses)
            if index != 1
        )


def test_scm_host_reports_service_main_failure_to_event_log() -> None:
    class FakeServiceAPI:
        def __init__(self) -> None:
            self.errors: list[str] = []

        def dispatch_service(self, _service_name, service_main) -> None:
            service_main(0, None)

        def register_control_handler(self, _service_name, _handler):
            return 42, object()

        def active_session_ids(self) -> list[int]:
            return [7]

        def spawn_daemon(self, _session_id: int) -> FakeProcess:
            raise KeyboardInterrupt("service loop interrupted")

        def running_controls(self) -> int:
            return 0x85

        def set_service_status(self, _handle: int, **_status: int) -> None:
            pass

        def report_error(self, message: str) -> None:
            self.errors.append(message)

    api = FakeServiceAPI()
    windows_service._WindowsServiceHost(api).dispatch()  # type: ignore[arg-type]

    assert len(api.errors) == 1
    assert "service loop interrupted" in api.errors[0]


def test_session_change_wakes_service_without_stopping() -> None:
    class FakeServiceAPI:
        def running_controls(self) -> int:
            return 0x85

        def set_service_status(self, _handle: int, **_status: int) -> None:
            pass

    class RecordingSupervisor:
        def __init__(self) -> None:
            self.notified = 0

        def note_session_change(self) -> None:
            self.notified += 1

    host = windows_service._WindowsServiceHost(FakeServiceAPI())  # type: ignore[arg-type]
    host._status_handle = 42
    host._current_state = windows_service.SERVICE_RUNNING
    supervisor = RecordingSupervisor()
    host._supervisor = supervisor  # type: ignore[assignment]

    result = host._control_handler(
        windows_service._SERVICE_CONTROL_SESSIONCHANGE,
        5,
        None,
        None,
    )

    assert result == 0
    assert host._wake.is_set()
    assert not host._stop.is_set()
    assert supervisor.notified == 1


def test_ctypes_backend_declares_required_service_and_session_apis() -> None:
    source = Path(windows_service.__file__).read_text()

    for api in (
        "StartServiceCtrlDispatcherW",
        "RegisterServiceCtrlHandlerExW",
        "SetServiceStatus",
        "RegisterEventSourceW",
        "ReportEventW",
        "DeregisterEventSource",
        "WTSEnumerateSessionsW",
        "WTSQueryUserToken",
        "GetTokenInformation",
        "ConvertSidToStringSidW",
        "LocalFree",
        "CreateEnvironmentBlock",
        "CreateProcessAsUserW",
        "CreateJobObjectW",
        "SetInformationJobObject",
        "AssignProcessToJobObject",
        "ResumeThread",
    ):
        assert api in source
    assert "_CREATE_SUSPENDED" in source
    assert "_SERVICE_CONTROL_STOP" in source
    assert "_SERVICE_CONTROL_SHUTDOWN" in source
    assert "_SERVICE_CONTROL_SESSIONCHANGE" in source


def test_ctypes_backend_declares_token_sid_api_signatures() -> None:
    class Function:
        argtypes = None
        restype = None

    def dll(*names: str) -> SimpleNamespace:
        return SimpleNamespace(**{name: Function() for name in names})

    class SessionInfo(ctypes.Structure):
        _fields_: list[tuple[str, object]] = []

    api = object.__new__(windows_service._WindowsAPI)
    api._ctypes = ctypes
    api._wintypes = windows_service.wintypes
    api.WTS_SESSION_INFOW = SessionInfo
    api._kernel32 = dll(
        "CloseHandle",
        "LocalFree",
        "WaitForSingleObject",
        "GetExitCodeProcess",
        "TerminateProcess",
        "CreateJobObjectW",
        "SetInformationJobObject",
        "AssignProcessToJobObject",
        "ResumeThread",
    )
    api._advapi32 = dll("GetTokenInformation", "ConvertSidToStringSidW")
    api._userenv = dll("CreateEnvironmentBlock", "DestroyEnvironmentBlock")
    api._wtsapi32 = dll(
        "WTSEnumerateSessionsW",
        "WTSFreeMemory",
        "WTSQueryUserToken",
    )

    api._configure_process_prototypes()

    wintypes = windows_service.wintypes
    assert api._advapi32.GetTokenInformation.argtypes == [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    assert api._advapi32.GetTokenInformation.restype is wintypes.BOOL
    assert api._advapi32.ConvertSidToStringSidW.argtypes == [
        ctypes.c_void_p,
        ctypes.POINTER(wintypes.LPWSTR),
    ]
    assert api._advapi32.ConvertSidToStringSidW.restype is wintypes.BOOL
    assert api._kernel32.LocalFree.argtypes == [wintypes.HLOCAL]
    assert api._kernel32.LocalFree.restype is wintypes.HLOCAL


def test_windows_api_reports_error_to_event_log() -> None:
    calls: list[tuple[str, object]] = []

    class FakeAdvapi:
        @staticmethod
        def RegisterEventSourceW(_server, source):
            calls.append(("register", source))
            return 42

        @staticmethod
        def ReportEventW(
            _handle,
            event_type,
            _category,
            _event_id,
            _sid,
            string_count,
            _data_size,
            strings,
            _raw_data,
        ):
            calls.append(("report", (event_type, string_count, strings[0])))
            return True

        @staticmethod
        def DeregisterEventSource(handle):
            calls.append(("deregister", handle))
            return True

    api = object.__new__(windows_service._WindowsAPI)
    api._ctypes = ctypes
    api._wintypes = windows_service.wintypes
    api._advapi32 = FakeAdvapi()

    api.report_error("daemon spawn failed")

    assert calls == [
        ("register", windows_service.SERVICE_NAME),
        ("report", (1, 1, "daemon spawn failed")),
        ("deregister", 42),
    ]


def test_wix_only_controls_reconcile_managed_daemon_service() -> None:
    root = ET.fromstring(_AIWATCH_WXS.read_text())
    wix_ns = root.tag[root.tag.index("{") : root.tag.index("}") + 1]
    components = {
        component.get("Id"): component for component in root.iter(f"{wix_ns}Component")
    }
    component = components["DaemonService"]

    assert component.find(f"{wix_ns}ServiceInstall") is None

    control = component.find(f"{wix_ns}ServiceControl")
    assert control is not None
    assert control.attrib == {
        "Id": "DaemonServiceControl",
        "Name": windows_scm.SERVICE_NAME,
        "Stop": "both",
        "Remove": "uninstall",
        "Wait": "yes",
    }


def test_reconcile_create_carries_full_windows_service_contract(monkeypatch) -> None:
    executable = r"C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
    states = iter(
        [
            None,
            daemon_lifecycle.SERVICE_STOPPED,
            daemon_lifecycle.SERVICE_RUNNING,
        ]
    )
    commands: list[list[str]] = []
    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Windows")
    monkeypatch.setattr(daemon_lifecycle.sys, "frozen", True, raising=False)
    monkeypatch.setattr(daemon_lifecycle.sys, "executable", executable)
    monkeypatch.setenv("ProgramFiles", r"C:\Program Files")
    monkeypatch.setenv("ProgramW6432", r"C:\Program Files")
    monkeypatch.setattr(daemon_lifecycle, "query_service_state", lambda: next(states))

    def run(command: list[str]) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    expected_binary_path = f'"{executable}" {windows_scm.SERVICE_ARGUMENTS}'
    restart_actions = "/".join(
        f"restart/{windows_scm.SCM_RESTART_DELAY_SECONDS * 1000}"
        for _ in range(windows_scm.SCM_RESTART_COUNT)
    )
    assert result.ok
    assert commands[:4] == [
        [
            "sc.exe",
            "create",
            windows_scm.SERVICE_NAME,
            "binPath=",
            expected_binary_path,
            "start=",
            windows_scm.SERVICE_START_TYPE,
            "obj=",
            windows_scm.SERVICE_ACCOUNT,
            "DisplayName=",
            windows_scm.SERVICE_DISPLAY_NAME,
        ],
        [
            "sc.exe",
            "description",
            windows_scm.SERVICE_NAME,
            windows_scm.SERVICE_DESCRIPTION,
        ],
        [
            "sc.exe",
            "failure",
            windows_scm.SERVICE_NAME,
            "reset=",
            str(windows_scm.SCM_RESET_PERIOD_DAYS * 86_400),
            "actions=",
            restart_actions,
        ],
        ["sc.exe", "failureflag", windows_scm.SERVICE_NAME, "1"],
    ]


def test_wix_service_exe_is_explicit_and_excluded_from_harvest() -> None:
    root = ET.fromstring(_AIWATCH_WXS.read_text())
    wix_ns = root.tag[root.tag.index("{") : root.tag.index("}") + 1]
    component = next(
        component
        for component in root.iter(f"{wix_ns}Component")
        if component.get("Id") == "DaemonService"
    )
    executable = component.find(f"{wix_ns}File")
    assert executable is not None
    assert executable.get("Source") == r"..\..\dist\aiwatch\aiwatch.exe"
    assert executable.get("KeyPath") == "yes"

    files = next(
        group
        for group in root.iter(f"{wix_ns}ComponentGroup")
        if group.get("Id") == "Files"
    ).find(f"{wix_ns}Files")
    assert files is not None
    exclude = files.find(f"{wix_ns}Exclude")
    assert exclude is not None
    assert exclude.get("Files") == executable.get("Source")

    feature = next(root.iter(f"{wix_ns}Feature"))
    refs = {ref.get("Id") for ref in feature.findall(f"{wix_ns}ComponentRef")}
    assert "DaemonService" in refs
