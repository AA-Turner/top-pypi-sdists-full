"""Windows SCM host for one per-session AI Watch hook daemon.

The service process runs as LocalSystem, but every ``aiwatch.exe daemon`` child
runs with its interactive session user's token. Platform-neutral supervision is
kept in :class:`SessionSupervisor`; Win32 calls are loaded only when the Windows
service entrypoint runs, so this module remains importable on every platform.
The SCM service contract and read-only query surface live in
:mod:`runlayer_cli.daemon.windows_scm`.
"""

from __future__ import annotations

import ctypes
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Iterable
from ctypes import wintypes
from dataclasses import dataclass
from typing import Any, Protocol

from runlayer_cli.daemon.windows_scm import (
    SERVICE_NAME,
    SERVICE_RUNNING,
    SERVICE_STOPPED,
)

FAILURE_RETRY_SECONDS = 60.0
CLEAN_EXIT_RETRY_SECONDS = 3600.0
POLL_INTERVAL_SECONDS = 5.0

_SERVICE_START_PENDING = 0x00000002
_SERVICE_STOP_PENDING = 0x00000003
_SERVICE_CONTROL_STOP = 0x00000001
_SERVICE_CONTROL_SHUTDOWN = 0x00000005
_SERVICE_CONTROL_SESSIONCHANGE = 0x0000000E
_ERROR_SERVICE_SPECIFIC_ERROR = 1066
_ERROR_NO_TOKEN = 1008
_TOKEN_USER = 1
_WTS_ACTIVE = 0
_WTS_DISCONNECTED = 4
_WTS_SERVICE_ACCOUNT_SIDS = frozenset({"S-1-5-18", "S-1-5-19", "S-1-5-20"})


class SessionTokenUnavailable(OSError):
    """A WTS session exists but has no queryable user token."""


def _has_supervised_session_state(session_id: int, state: int) -> bool:
    return session_id > 0 and state in {_WTS_ACTIVE, _WTS_DISCONNECTED}


def _is_service_account_sid(user_sid: str) -> bool:
    return user_sid in _WTS_SERVICE_ACCOUNT_SIDS


def _is_supervised_session(session_id: int, state: int, user_sid: str) -> bool:
    """Keep daemons for connected and disconnected interactive user sessions."""
    return _has_supervised_session_state(
        session_id, state
    ) and not _is_service_account_sid(user_sid)


class ChildProcess(Protocol):
    """Minimal process handle used by the pure supervisor policy."""

    def poll(self) -> int | None: ...

    def terminate(self) -> None: ...

    def close(self) -> None: ...


@dataclass
class _Child:
    process: ChildProcess


class SessionSupervisor:
    """Maintain exactly one daemon child per supervised interactive session."""

    def __init__(
        self,
        *,
        list_sessions: Callable[[], Iterable[int]],
        spawn: Callable[[int], ChildProcess],
        should_stop: Callable[[], bool],
        wait: Callable[[float], object],
        on_spawn_failure: Callable[[int, BaseException], None] | None = None,
        clock: Callable[[], float] = time.monotonic,
        poll_interval: float = POLL_INTERVAL_SECONDS,
        failure_retry: float = FAILURE_RETRY_SECONDS,
        clean_exit_retry: float = CLEAN_EXIT_RETRY_SECONDS,
    ) -> None:
        self._list_sessions = list_sessions
        self._spawn = spawn
        self._should_stop = should_stop
        self._wait = wait
        self._on_spawn_failure = on_spawn_failure
        self._clock = clock
        self._poll_interval = poll_interval
        self._failure_retry = failure_retry
        self._clean_exit_retry = clean_exit_retry
        self._children: dict[int, _Child] = {}
        self._retry_at: dict[int, float] = {}
        self._token_unavailable: set[int] = set()
        self._reported_spawn_failures: dict[
            int,
            tuple[type[BaseException], object, str],
        ] = {}
        self._session_change = threading.Event()

    @property
    def child_sessions(self) -> frozenset[int]:
        """Session ids currently owning a supervised process handle."""
        return frozenset(self._children)

    def note_session_change(self) -> None:
        """Ask the next tick to re-probe token-unavailable sessions.

        Safe to call from the SCM control-handler thread: a logon can make a
        previously unqueryable session token available, so the hourly backoff
        set for ``SessionTokenUnavailable`` must not outlive the session event.
        """
        self._session_change.set()

    def reconcile(self, active_sessions: Iterable[int]) -> float:
        """Apply one policy tick and return the next non-busy wait duration."""
        if self._session_change.is_set():
            self._session_change.clear()
            for session_id in self._token_unavailable:
                self._retry_at.pop(session_id, None)
                self._reported_spawn_failures.pop(session_id, None)
            self._token_unavailable.clear()

        now = self._clock()
        active = {
            session_id
            for session_id in active_sessions
            if isinstance(session_id, int)
            and not isinstance(session_id, bool)
            and session_id > 0
        }

        for session_id in tuple(self._children):
            if session_id not in active:
                self._terminate_child(session_id)
        for session_id in tuple(self._retry_at):
            if session_id not in active:
                self._retry_at.pop(session_id, None)
                self._token_unavailable.discard(session_id)
                self._reported_spawn_failures.pop(session_id, None)

        for session_id, child in tuple(self._children.items()):
            try:
                exit_code = child.process.poll()
            except Exception:
                exit_code = 1
            if exit_code is None:
                continue
            self._close_child(session_id)
            retry = self._clean_exit_retry if exit_code == 0 else self._failure_retry
            self._retry_at[session_id] = now + retry

        for session_id in sorted(active):
            if self._should_stop():
                break
            if session_id in self._children:
                continue
            if now < self._retry_at.get(session_id, 0.0):
                continue
            try:
                process = self._spawn(session_id)
            except SessionTokenUnavailable as exc:
                self._retry_at[session_id] = now + self._clean_exit_retry
                self._token_unavailable.add(session_id)
                self._report_spawn_failure_once(session_id, exc)
            except Exception as exc:
                self._retry_at[session_id] = now + self._failure_retry
                self._token_unavailable.discard(session_id)
                self._report_spawn_failure_once(session_id, exc)
            else:
                self._children[session_id] = _Child(process)
                self._retry_at.pop(session_id, None)
                self._token_unavailable.discard(session_id)
                self._reported_spawn_failures.pop(session_id, None)

        delay = self._poll_interval
        pending = [
            retry_at - now
            for session_id, retry_at in self._retry_at.items()
            if session_id in active and session_id not in self._children
        ]
        if pending:
            delay = min(delay, max(0.1, min(pending)))
        return max(0.1, delay)

    def run(self) -> None:
        """Reconcile until service stop, then terminate every child."""
        try:
            while not self._should_stop():
                try:
                    active_sessions = tuple(self._list_sessions())
                except Exception:
                    delay = self._poll_interval
                else:
                    if self._should_stop():
                        break
                    delay = self.reconcile(active_sessions)
                if not self._should_stop():
                    self._wait(delay)
        finally:
            self.stop_all()

    def stop_all(self) -> None:
        """Terminate and close all child process handles."""
        for session_id in tuple(self._children):
            self._terminate_child(session_id)
        self._retry_at.clear()
        self._token_unavailable.clear()
        self._reported_spawn_failures.clear()

    def _report_spawn_failure_once(
        self,
        session_id: int,
        exc: BaseException,
    ) -> None:
        fingerprint = (type(exc), getattr(exc, "errno", None), str(exc))
        if self._reported_spawn_failures.get(session_id) == fingerprint:
            return
        self._reported_spawn_failures[session_id] = fingerprint
        if self._on_spawn_failure is not None:
            try:
                self._on_spawn_failure(session_id, exc)
            except Exception:
                pass

    def _close_child(self, session_id: int) -> None:
        child = self._children.pop(session_id, None)
        if child is None:
            return
        try:
            child.process.close()
        except Exception:
            pass

    def _terminate_child(self, session_id: int) -> None:
        child = self._children.pop(session_id, None)
        if child is None:
            return
        try:
            child.process.terminate()
        except Exception:
            pass
        finally:
            try:
                child.process.close()
            except Exception:
                pass


class _WindowsProcess:
    def __init__(self, api: _WindowsAPI, handle: int, job_handle: int) -> None:
        self._api = api
        self._handle = handle
        self._job_handle: int | None = job_handle
        self._closed = False

    def poll(self) -> int | None:
        return self._api.poll_process(self._handle)

    def terminate(self) -> None:
        try:
            self._close_job()
        finally:
            self._api.terminate_process(self._handle)

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            try:
                self._close_job()
            finally:
                self._api.close_handle(self._handle)

    def _close_job(self) -> None:
        job_handle = self._job_handle
        if job_handle is not None:
            self._job_handle = None
            self._api.close_handle(job_handle)


class _WindowsAPI:
    """Narrow ctypes backend for SCM, WTS, and user-token process creation."""

    _ctypes: Any
    _wintypes: Any
    _advapi32: Any
    _kernel32: Any
    _userenv: Any
    _wtsapi32: Any
    executable: str
    WTS_SESSION_INFOW: Any
    STARTUPINFOW: Any
    PROCESS_INFORMATION: Any
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION: Any
    SERVICE_STATUS: Any
    SERVICE_MAIN_CALLBACK: Any
    HANDLER_EX_CALLBACK: Any
    SERVICE_TABLE_ENTRYW: Any

    _CREATE_SUSPENDED = 0x00000004
    _CREATE_UNICODE_ENVIRONMENT = 0x00000400
    _CREATE_NO_WINDOW = 0x08000000
    _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS = 9
    _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    _RESUME_THREAD_FAILED = 0xFFFFFFFF
    _WAIT_OBJECT_0 = 0x00000000
    _WAIT_TIMEOUT = 0x00000102
    _SERVICE_WIN32_OWN_PROCESS = 0x00000010
    _SERVICE_ACCEPT_STOP = 0x00000001
    _SERVICE_ACCEPT_SHUTDOWN = 0x00000004
    _SERVICE_ACCEPT_SESSIONCHANGE = 0x00000080
    _EVENTLOG_ERROR_TYPE = 0x0001
    _SERVICE_EVENT_ID = 1

    def __init__(self, executable: str | None = None) -> None:
        if sys.platform != "win32":
            raise OSError("Windows service APIs are unavailable on this platform")

        self._ctypes = ctypes
        self._wintypes = wintypes
        self.executable = executable or sys.executable
        self._advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
        self._configure_event_log_prototypes()
        try:
            self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            self._userenv = ctypes.WinDLL("userenv", use_last_error=True)
            self._wtsapi32 = ctypes.WinDLL("wtsapi32", use_last_error=True)
            self._configure_types()
            self._configure_prototypes()
        except OSError as exc:
            self.report_error(
                f"AI Watch service initialization failed: {type(exc).__name__}: {exc}"
            )
            raise

    def _configure_types(self) -> None:
        ctypes = self._ctypes
        wintypes = self._wintypes

        class WTS_SESSION_INFOW(ctypes.Structure):
            _fields_ = [
                ("SessionId", wintypes.DWORD),
                ("pWinStationName", wintypes.LPWSTR),
                ("State", wintypes.DWORD),
            ]

        class STARTUPINFOW(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("lpReserved", wintypes.LPWSTR),
                ("lpDesktop", wintypes.LPWSTR),
                ("lpTitle", wintypes.LPWSTR),
                ("dwX", wintypes.DWORD),
                ("dwY", wintypes.DWORD),
                ("dwXSize", wintypes.DWORD),
                ("dwYSize", wintypes.DWORD),
                ("dwXCountChars", wintypes.DWORD),
                ("dwYCountChars", wintypes.DWORD),
                ("dwFillAttribute", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("wShowWindow", wintypes.WORD),
                ("cbReserved2", wintypes.WORD),
                ("lpReserved2", ctypes.POINTER(ctypes.c_byte)),
                ("hStdInput", wintypes.HANDLE),
                ("hStdOutput", wintypes.HANDLE),
                ("hStdError", wintypes.HANDLE),
            ]

        class PROCESS_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("hProcess", wintypes.HANDLE),
                ("hThread", wintypes.HANDLE),
                ("dwProcessId", wintypes.DWORD),
                ("dwThreadId", wintypes.DWORD),
            ]

        class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_int64),
                ("PerJobUserTimeLimit", ctypes.c_int64),
                ("LimitFlags", wintypes.DWORD),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", wintypes.DWORD),
                ("SchedulingClass", wintypes.DWORD),
            ]

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [
                ("ReadOperationCount", ctypes.c_uint64),
                ("WriteOperationCount", ctypes.c_uint64),
                ("OtherOperationCount", ctypes.c_uint64),
                ("ReadTransferCount", ctypes.c_uint64),
                ("WriteTransferCount", ctypes.c_uint64),
                ("OtherTransferCount", ctypes.c_uint64),
            ]

        class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
                ("IoInfo", IO_COUNTERS),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        class SERVICE_STATUS(ctypes.Structure):
            _fields_ = [
                ("dwServiceType", wintypes.DWORD),
                ("dwCurrentState", wintypes.DWORD),
                ("dwControlsAccepted", wintypes.DWORD),
                ("dwWin32ExitCode", wintypes.DWORD),
                ("dwServiceSpecificExitCode", wintypes.DWORD),
                ("dwCheckPoint", wintypes.DWORD),
                ("dwWaitHint", wintypes.DWORD),
            ]

        service_main = ctypes.WINFUNCTYPE(
            None,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.LPWSTR),
        )
        handler_ex = ctypes.WINFUNCTYPE(
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.c_void_p,
            ctypes.c_void_p,
        )

        class SERVICE_TABLE_ENTRYW(ctypes.Structure):
            _fields_ = [
                ("lpServiceName", wintypes.LPWSTR),
                ("lpServiceProc", service_main),
            ]

        self.WTS_SESSION_INFOW = WTS_SESSION_INFOW
        self.STARTUPINFOW = STARTUPINFOW
        self.PROCESS_INFORMATION = PROCESS_INFORMATION
        self.JOBOBJECT_EXTENDED_LIMIT_INFORMATION = JOBOBJECT_EXTENDED_LIMIT_INFORMATION
        self.SERVICE_STATUS = SERVICE_STATUS
        self.SERVICE_MAIN_CALLBACK = service_main
        self.HANDLER_EX_CALLBACK = handler_ex
        self.SERVICE_TABLE_ENTRYW = SERVICE_TABLE_ENTRYW

    def _configure_prototypes(self) -> None:
        ctypes = self._ctypes
        wintypes = self._wintypes

        self._advapi32.StartServiceCtrlDispatcherW.argtypes = [
            ctypes.POINTER(self.SERVICE_TABLE_ENTRYW)
        ]
        self._advapi32.StartServiceCtrlDispatcherW.restype = wintypes.BOOL
        self._advapi32.RegisterServiceCtrlHandlerExW.argtypes = [
            wintypes.LPCWSTR,
            self.HANDLER_EX_CALLBACK,
            ctypes.c_void_p,
        ]
        self._advapi32.RegisterServiceCtrlHandlerExW.restype = wintypes.HANDLE
        self._advapi32.SetServiceStatus.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(self.SERVICE_STATUS),
        ]
        self._advapi32.SetServiceStatus.restype = wintypes.BOOL
        self._advapi32.CreateProcessAsUserW.argtypes = [
            wintypes.HANDLE,
            wintypes.LPCWSTR,
            wintypes.LPWSTR,
            ctypes.c_void_p,
            ctypes.c_void_p,
            wintypes.BOOL,
            wintypes.DWORD,
            ctypes.c_void_p,
            wintypes.LPCWSTR,
            ctypes.POINTER(self.STARTUPINFOW),
            ctypes.POINTER(self.PROCESS_INFORMATION),
        ]
        self._advapi32.CreateProcessAsUserW.restype = wintypes.BOOL
        self._configure_process_prototypes()

    def _configure_event_log_prototypes(self) -> None:
        ctypes = self._ctypes
        wintypes = self._wintypes
        self._advapi32.RegisterEventSourceW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
        ]
        self._advapi32.RegisterEventSourceW.restype = wintypes.HANDLE
        self._advapi32.ReportEventW.argtypes = [
            wintypes.HANDLE,
            wintypes.WORD,
            wintypes.WORD,
            wintypes.DWORD,
            ctypes.c_void_p,
            wintypes.WORD,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.LPCWSTR),
            ctypes.c_void_p,
        ]
        self._advapi32.ReportEventW.restype = wintypes.BOOL
        self._advapi32.DeregisterEventSource.argtypes = [wintypes.HANDLE]
        self._advapi32.DeregisterEventSource.restype = wintypes.BOOL

    def _configure_process_prototypes(self) -> None:
        ctypes = self._ctypes
        wintypes = self._wintypes
        self._kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        self._kernel32.CloseHandle.restype = wintypes.BOOL
        self._kernel32.LocalFree.argtypes = [wintypes.HLOCAL]
        self._kernel32.LocalFree.restype = wintypes.HLOCAL
        self._kernel32.WaitForSingleObject.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
        ]
        self._kernel32.WaitForSingleObject.restype = wintypes.DWORD
        self._kernel32.GetExitCodeProcess.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.DWORD),
        ]
        self._kernel32.GetExitCodeProcess.restype = wintypes.BOOL
        self._kernel32.TerminateProcess.argtypes = [
            wintypes.HANDLE,
            wintypes.UINT,
        ]
        self._kernel32.TerminateProcess.restype = wintypes.BOOL
        self._kernel32.CreateJobObjectW.argtypes = [
            ctypes.c_void_p,
            wintypes.LPCWSTR,
        ]
        self._kernel32.CreateJobObjectW.restype = wintypes.HANDLE
        self._kernel32.SetInformationJobObject.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        self._kernel32.SetInformationJobObject.restype = wintypes.BOOL
        self._kernel32.AssignProcessToJobObject.argtypes = [
            wintypes.HANDLE,
            wintypes.HANDLE,
        ]
        self._kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
        self._kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
        self._kernel32.ResumeThread.restype = wintypes.DWORD

        self._advapi32.GetTokenInformation.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
        ]
        self._advapi32.GetTokenInformation.restype = wintypes.BOOL
        self._advapi32.ConvertSidToStringSidW.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(wintypes.LPWSTR),
        ]
        self._advapi32.ConvertSidToStringSidW.restype = wintypes.BOOL

        self._userenv.CreateEnvironmentBlock.argtypes = [
            ctypes.POINTER(ctypes.c_void_p),
            wintypes.HANDLE,
            wintypes.BOOL,
        ]
        self._userenv.CreateEnvironmentBlock.restype = wintypes.BOOL
        self._userenv.DestroyEnvironmentBlock.argtypes = [ctypes.c_void_p]
        self._userenv.DestroyEnvironmentBlock.restype = wintypes.BOOL

        session_pointer = ctypes.POINTER(self.WTS_SESSION_INFOW)
        self._wtsapi32.WTSEnumerateSessionsW.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.POINTER(session_pointer),
            ctypes.POINTER(wintypes.DWORD),
        ]
        self._wtsapi32.WTSEnumerateSessionsW.restype = wintypes.BOOL
        self._wtsapi32.WTSFreeMemory.argtypes = [ctypes.c_void_p]
        self._wtsapi32.WTSFreeMemory.restype = None
        self._wtsapi32.WTSQueryUserToken.argtypes = [
            wintypes.ULONG,
            ctypes.POINTER(wintypes.HANDLE),
        ]
        self._wtsapi32.WTSQueryUserToken.restype = wintypes.BOOL

    def active_session_ids(self) -> list[int]:
        """Enumerate connected/disconnected user sessions via WTS."""
        ctypes = self._ctypes
        wintypes = self._wintypes
        sessions = ctypes.POINTER(self.WTS_SESSION_INFOW)()
        count = wintypes.DWORD(0)
        if not self._wtsapi32.WTSEnumerateSessionsW(
            wintypes.HANDLE(0),
            0,
            1,
            ctypes.byref(sessions),
            ctypes.byref(count),
        ):
            self._raise_last_error("WTSEnumerateSessionsW")
        try:
            supervised: set[int] = set()
            for index in range(count.value):
                session_id = int(sessions[index].SessionId)
                state = int(sessions[index].State)
                if not _has_supervised_session_state(session_id, state):
                    continue
                try:
                    user_sid = self._session_user_sid(session_id)
                except OSError:
                    supervised.add(session_id)
                    continue
                if _is_supervised_session(
                    session_id,
                    state,
                    user_sid,
                ):
                    supervised.add(session_id)
            return sorted(supervised)
        finally:
            if sessions:
                self._wtsapi32.WTSFreeMemory(sessions)

    def _query_user_token(self, session_id: int) -> int:
        token = self._wintypes.HANDLE()
        if not self._wtsapi32.WTSQueryUserToken(
            session_id,
            self._ctypes.byref(token),
        ):
            error = self._ctypes.get_last_error()
            if error == _ERROR_NO_TOKEN:
                raise SessionTokenUnavailable(
                    error,
                    f"WTSQueryUserToken unavailable for session {session_id}",
                )
            raise OSError(error, "WTSQueryUserToken failed")
        return self._handle_value(token)

    def _session_user_sid(self, session_id: int) -> str:
        token = self._query_user_token(session_id)
        try:
            return self._token_user_sid(token)
        finally:
            self._close_handle_quietly(token)

    def _token_user_sid(self, token: int) -> str:
        ctypes = self._ctypes
        wintypes = self._wintypes
        required = wintypes.DWORD(0)
        self._advapi32.GetTokenInformation(
            wintypes.HANDLE(token),
            _TOKEN_USER,
            None,
            0,
            ctypes.byref(required),
        )
        if required.value == 0:
            self._raise_last_error("GetTokenInformation")

        buffer = ctypes.create_string_buffer(required.value)
        if not self._advapi32.GetTokenInformation(
            wintypes.HANDLE(token),
            _TOKEN_USER,
            buffer,
            required,
            ctypes.byref(required),
        ):
            self._raise_last_error("GetTokenInformation")

        sid_pointer = ctypes.cast(
            buffer,
            ctypes.POINTER(ctypes.c_void_p),
        ).contents.value
        if not sid_pointer:
            raise OSError("GetTokenInformation returned a null user SID")

        sid_string = wintypes.LPWSTR()
        if not self._advapi32.ConvertSidToStringSidW(
            ctypes.c_void_p(sid_pointer),
            ctypes.byref(sid_string),
        ):
            self._raise_last_error("ConvertSidToStringSidW")
        try:
            if not sid_string.value:
                raise OSError("ConvertSidToStringSidW returned an empty SID")
            return sid_string.value
        finally:
            self._kernel32.LocalFree(ctypes.cast(sid_string, ctypes.c_void_p))

    def spawn_daemon(self, session_id: int) -> ChildProcess:
        """Create ``aiwatch.exe daemon`` as the session's user."""
        ctypes = self._ctypes
        wintypes = self._wintypes
        token_handle = self._query_user_token(session_id)
        token = wintypes.HANDLE(token_handle)

        try:
            user_sid = self._token_user_sid(token_handle)
            if _is_service_account_sid(user_sid):
                raise PermissionError(
                    f"refusing to launch daemon with service account token {user_sid}"
                )
            environment = ctypes.c_void_p()
            if not self._userenv.CreateEnvironmentBlock(
                ctypes.byref(environment),
                token,
                False,
            ):
                self._raise_last_error("CreateEnvironmentBlock")
            try:
                startup = self.STARTUPINFOW()
                startup.cb = ctypes.sizeof(self.STARTUPINFOW)
                startup.lpDesktop = "winsta0\\default"
                process_info = self.PROCESS_INFORMATION()
                command_line = subprocess.list2cmdline([self.executable, "daemon"])
                command_buffer = ctypes.create_unicode_buffer(command_line)
                job_handle: int | None = self._create_kill_on_close_job()
                process_handle: int | None = None
                thread_handle: int | None = None
                try:
                    # Suspend until job assignment so a fast daemon cannot spawn
                    # a detached worker outside the service-owned process tree.
                    if not self._advapi32.CreateProcessAsUserW(
                        token,
                        self.executable,
                        command_buffer,
                        None,
                        None,
                        False,
                        self._CREATE_NO_WINDOW
                        | self._CREATE_SUSPENDED
                        | self._CREATE_UNICODE_ENVIRONMENT,
                        environment,
                        None,
                        ctypes.byref(startup),
                        ctypes.byref(process_info),
                    ):
                        self._raise_last_error("CreateProcessAsUserW")
                    process_handle = self._handle_value(process_info.hProcess)
                    thread_handle = self._handle_value(process_info.hThread)
                    if not self._kernel32.AssignProcessToJobObject(
                        wintypes.HANDLE(job_handle),
                        wintypes.HANDLE(process_handle),
                    ):
                        self._raise_last_error("AssignProcessToJobObject")
                    if (
                        self._kernel32.ResumeThread(wintypes.HANDLE(thread_handle))
                        == self._RESUME_THREAD_FAILED
                    ):
                        self._raise_last_error("ResumeThread")
                    process = _WindowsProcess(self, process_handle, job_handle)
                    process_handle = None
                    job_handle = None
                    return process
                finally:
                    if thread_handle is not None:
                        self._close_handle_quietly(thread_handle)
                    if process_handle is not None:
                        self._kernel32.TerminateProcess(
                            wintypes.HANDLE(process_handle),
                            1,
                        )
                        self._close_handle_quietly(process_handle)
                    if job_handle is not None:
                        self._close_handle_quietly(job_handle)
            finally:
                self._userenv.DestroyEnvironmentBlock(environment)
        finally:
            self._close_handle_quietly(token_handle)

    def poll_process(self, handle: int) -> int | None:
        wintypes = self._wintypes
        result = self._kernel32.WaitForSingleObject(wintypes.HANDLE(handle), 0)
        if result == self._WAIT_TIMEOUT:
            return None
        if result != self._WAIT_OBJECT_0:
            self._raise_last_error("WaitForSingleObject")
        exit_code = wintypes.DWORD(0)
        if not self._kernel32.GetExitCodeProcess(
            wintypes.HANDLE(handle),
            self._ctypes.byref(exit_code),
        ):
            self._raise_last_error("GetExitCodeProcess")
        return int(exit_code.value)

    def terminate_process(self, handle: int) -> None:
        wintypes = self._wintypes
        if self.poll_process(handle) is not None:
            return
        if not self._kernel32.TerminateProcess(wintypes.HANDLE(handle), 1):
            if self.poll_process(handle) is None:
                self._raise_last_error("TerminateProcess")
            return
        result = self._kernel32.WaitForSingleObject(
            wintypes.HANDLE(handle),
            10_000,
        )
        if result == self._WAIT_TIMEOUT:
            raise TimeoutError("terminated daemon child did not exit")
        if result != self._WAIT_OBJECT_0:
            self._raise_last_error("WaitForSingleObject")

    def close_handle(self, handle: int) -> None:
        if not self._kernel32.CloseHandle(self._wintypes.HANDLE(handle)):
            self._raise_last_error("CloseHandle")

    def _create_kill_on_close_job(self) -> int:
        ctypes = self._ctypes
        job = self._kernel32.CreateJobObjectW(None, None)
        if not job:
            self._raise_last_error("CreateJobObjectW")
        job_handle = self._handle_value(job)
        limits = self.JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        limits.BasicLimitInformation.LimitFlags = (
            self._JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        )
        if not self._kernel32.SetInformationJobObject(
            self._wintypes.HANDLE(job_handle),
            self._JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            self._close_handle_quietly(job_handle)
            self._raise_last_error("SetInformationJobObject")
        return job_handle

    def _close_handle_quietly(self, handle: int) -> None:
        self._kernel32.CloseHandle(self._wintypes.HANDLE(handle))

    def dispatch_service(
        self,
        service_name: str,
        service_main: Callable[..., None],
    ) -> None:
        callback = self.SERVICE_MAIN_CALLBACK(service_main)
        table = (self.SERVICE_TABLE_ENTRYW * 2)()
        table[0].lpServiceName = service_name
        table[0].lpServiceProc = callback
        if not self._advapi32.StartServiceCtrlDispatcherW(table):
            self._raise_last_error("StartServiceCtrlDispatcherW")

    def register_control_handler(
        self,
        service_name: str,
        handler: Callable[..., int],
    ) -> tuple[int, Any]:
        callback = self.HANDLER_EX_CALLBACK(handler)
        handle = self._advapi32.RegisterServiceCtrlHandlerExW(
            service_name,
            callback,
            None,
        )
        if not handle:
            self._raise_last_error("RegisterServiceCtrlHandlerExW")
        return self._handle_value(handle), callback

    def set_service_status(
        self,
        handle: int,
        *,
        state: int,
        controls: int,
        win32_exit_code: int,
        service_exit_code: int,
        checkpoint: int,
        wait_hint: int,
    ) -> None:
        status = self.SERVICE_STATUS(
            self._SERVICE_WIN32_OWN_PROCESS,
            state,
            controls,
            win32_exit_code,
            service_exit_code,
            checkpoint,
            wait_hint,
        )
        if not self._advapi32.SetServiceStatus(
            self._wintypes.HANDLE(handle),
            self._ctypes.byref(status),
        ):
            self._raise_last_error("SetServiceStatus")

    def running_controls(self) -> int:
        return (
            self._SERVICE_ACCEPT_STOP
            | self._SERVICE_ACCEPT_SHUTDOWN
            | self._SERVICE_ACCEPT_SESSIONCHANGE
        )

    def report_error(self, message: str) -> None:
        """Best-effort Windows Application event for service diagnosis."""
        source = None
        try:
            source = self._advapi32.RegisterEventSourceW(None, SERVICE_NAME)
            if not source:
                return
            strings = (self._wintypes.LPCWSTR * 1)(message[:30_000])
            self._advapi32.ReportEventW(
                source,
                self._EVENTLOG_ERROR_TYPE,
                0,
                self._SERVICE_EVENT_ID,
                None,
                1,
                0,
                strings,
                None,
            )
        except Exception:
            pass
        finally:
            if source:
                try:
                    self._advapi32.DeregisterEventSource(source)
                except Exception:
                    pass

    def _raise_last_error(self, operation: str) -> None:
        error = self._ctypes.get_last_error()
        raise OSError(error, f"{operation} failed")

    @staticmethod
    def _handle_value(handle: object) -> int:
        value: Any = getattr(handle, "value", handle)
        if value is None:
            raise OSError("Win32 returned a null handle")
        if not isinstance(value, int):
            raise OSError("Win32 returned an invalid handle")
        return value


class _WindowsServiceHost:
    def __init__(self, api: _WindowsAPI) -> None:
        self._api = api
        self._stop = threading.Event()
        self._wake = threading.Event()
        self._status_lock = threading.Lock()
        self._status_handle: int | None = None
        # Anchor the ctypes trampoline so SCM control callbacks remain valid.
        self._handler_callback: Any | None = None
        self._supervisor: SessionSupervisor | None = None
        self._current_state = SERVICE_STOPPED
        self._checkpoint = 0

    def dispatch(self) -> None:
        self._api.dispatch_service(SERVICE_NAME, self._service_main)

    def _service_main(self, _argc: int, _argv: object) -> None:
        failed = False
        try:
            (
                self._status_handle,
                self._handler_callback,
            ) = self._api.register_control_handler(
                SERVICE_NAME,
                self._control_handler,
            )
            self._report_status(_SERVICE_START_PENDING, wait_hint=15_000)
            supervisor = SessionSupervisor(
                list_sessions=self._api.active_session_ids,
                spawn=self._api.spawn_daemon,
                should_stop=self._stop.is_set,
                wait=self._wait,
                on_spawn_failure=self._report_spawn_failure,
            )
            self._supervisor = supervisor
            self._report_status(SERVICE_RUNNING)
            supervisor.run()
        except BaseException as exc:
            failed = True
            self._api.report_error(
                f"AI Watch service main failed: {type(exc).__name__}: {exc}"
            )
            self._stop.set()
            self._wake.set()
        finally:
            if self._status_handle is not None:
                try:
                    if failed:
                        self._report_status(
                            SERVICE_STOPPED,
                            win32_exit_code=_ERROR_SERVICE_SPECIFIC_ERROR,
                            service_exit_code=1,
                        )
                    else:
                        if self._current_state != _SERVICE_STOP_PENDING:
                            self._report_status(
                                _SERVICE_STOP_PENDING,
                                wait_hint=30_000,
                            )
                        self._report_status(SERVICE_STOPPED)
                except Exception:
                    pass

    def _control_handler(
        self,
        control: int,
        _event_type: int,
        _event_data: object,
        _context: object,
    ) -> int:
        try:
            if control in (_SERVICE_CONTROL_STOP, _SERVICE_CONTROL_SHUTDOWN):
                self._stop.set()
                self._wake.set()
                if self._current_state not in (
                    _SERVICE_STOP_PENDING,
                    SERVICE_STOPPED,
                ):
                    self._report_status(
                        _SERVICE_STOP_PENDING,
                        wait_hint=30_000,
                    )
            elif control == _SERVICE_CONTROL_SESSIONCHANGE:
                supervisor = self._supervisor
                if supervisor is not None:
                    supervisor.note_session_change()
                self._wake.set()
        except Exception:
            pass
        return 0

    def _wait(self, timeout: float) -> None:
        self._wake.wait(timeout)
        self._wake.clear()

    def _report_spawn_failure(
        self,
        session_id: int,
        exc: BaseException,
    ) -> None:
        self._api.report_error(
            "AI Watch daemon spawn failed for "
            f"session {session_id}: {type(exc).__name__}: {exc}"
        )

    def _report_status(
        self,
        state: int,
        *,
        win32_exit_code: int = 0,
        service_exit_code: int = 0,
        wait_hint: int = 0,
    ) -> None:
        if self._status_handle is None:
            return
        with self._status_lock:
            pending = state in (_SERVICE_START_PENDING, _SERVICE_STOP_PENDING)
            self._checkpoint = self._checkpoint + 1 if pending else 0
            controls = self._api.running_controls() if state == SERVICE_RUNNING else 0
            self._api.set_service_status(
                self._status_handle,
                state=state,
                controls=controls,
                win32_exit_code=win32_exit_code,
                service_exit_code=service_exit_code,
                checkpoint=self._checkpoint,
                wait_hint=wait_hint,
            )
            self._current_state = state


def run_service() -> int:
    """Run under SCM on Windows; quietly no-op on unsupported platforms."""
    if sys.platform != "win32":
        return 0
    api: _WindowsAPI | None = None
    try:
        api = _WindowsAPI(sys.executable)
        _WindowsServiceHost(api).dispatch()
    except OSError as exc:
        if api is not None:
            api.report_error(f"AI Watch service failed: {type(exc).__name__}: {exc}")
        return 1
    return 0
