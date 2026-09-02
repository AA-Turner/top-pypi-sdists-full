"""SCM service contract and read-only query surface for the AI Watch service.

Importable on every platform; Win32 calls happen only on win32. The service
host itself lives in :mod:`runlayer_cli.daemon.windows_service`.
"""

from __future__ import annotations

import ctypes
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from ctypes import wintypes
from dataclasses import dataclass
from typing import Any

SERVICE_NAME = "RunlayerAIWatch"
SERVICE_STOPPED = 0x00000001
SERVICE_RUNNING = 0x00000004
SERVICE_AUTO_START = 0x00000002

# Single definition of the SCM service contract. Gate-open reconciliation
# creates and repairs the service with sc.exe; the MSI only retains name-based
# ServiceControl for upgrade/uninstall cleanup.
SERVICE_DISPLAY_NAME = "Runlayer AI Watch"
SERVICE_DESCRIPTION = "Runs the AI Watch hook daemon in interactive user sessions."
SERVICE_ARGUMENTS = "daemon-service"
SERVICE_EXECUTABLE_RELATIVE_PATH = r"Runlayer\AIWatch\aiwatch.exe"
SERVICE_START_TYPE = "auto"
SERVICE_ACCOUNT = "LocalSystem"
SCM_RESTART_DELAY_SECONDS = 60
SCM_RESTART_COUNT = 3
SCM_RESET_PERIOD_DAYS = 1

_SC_MANAGER_CONNECT = 0x0001
_SERVICE_QUERY_STATUS = 0x0004
_SERVICE_QUERY_CONFIG = 0x0001
_SC_STATUS_PROCESS_INFO = 0
_ERROR_SERVICE_DOES_NOT_EXIST = 1060


@dataclass(frozen=True)
class ServiceConfig:
    """SCM configuration fields used by lifecycle drift detection."""

    binary_path: str
    start_type: int = SERVICE_AUTO_START


class _SERVICE_STATUS_PROCESS(ctypes.Structure):
    _fields_ = [
        ("dwServiceType", wintypes.DWORD),
        ("dwCurrentState", wintypes.DWORD),
        ("dwControlsAccepted", wintypes.DWORD),
        ("dwWin32ExitCode", wintypes.DWORD),
        ("dwServiceSpecificExitCode", wintypes.DWORD),
        ("dwCheckPoint", wintypes.DWORD),
        ("dwWaitHint", wintypes.DWORD),
        ("dwProcessId", wintypes.DWORD),
        ("dwServiceFlags", wintypes.DWORD),
    ]


class _QUERY_SERVICE_CONFIGW(ctypes.Structure):
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


def _configured_advapi32() -> Any:
    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)  # ty: ignore[unresolved-attribute]
    advapi32.OpenSCManagerW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        wintypes.DWORD,
    )
    advapi32.OpenSCManagerW.restype = wintypes.HANDLE
    advapi32.OpenServiceW.argtypes = (
        wintypes.HANDLE,
        wintypes.LPCWSTR,
        wintypes.DWORD,
    )
    advapi32.OpenServiceW.restype = wintypes.HANDLE
    advapi32.CloseServiceHandle.argtypes = (wintypes.HANDLE,)
    advapi32.CloseServiceHandle.restype = wintypes.BOOL
    advapi32.QueryServiceStatusEx.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        ctypes.POINTER(ctypes.c_byte),
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    advapi32.QueryServiceStatusEx.restype = wintypes.BOOL
    advapi32.QueryServiceConfigW.argtypes = (
        wintypes.HANDLE,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    advapi32.QueryServiceConfigW.restype = wintypes.BOOL
    return advapi32


def _last_error() -> int:
    get_last_error = getattr(ctypes, "get_last_error", None)
    return int(get_last_error()) if callable(get_last_error) else 0


@contextmanager
def _open_scm_service(
    service_name: str,
    access: int,
) -> Iterator[tuple[Any, Any] | None]:
    """Yield an opened service, ``None`` when absent, or raise on access failure."""
    advapi32 = _configured_advapi32()
    manager = advapi32.OpenSCManagerW(None, None, _SC_MANAGER_CONNECT)
    if not manager:
        error = _last_error()
        raise OSError(error, "OpenSCManagerW failed")
    try:
        service = advapi32.OpenServiceW(manager, service_name, access)
        if not service:
            error = _last_error()
            if error == _ERROR_SERVICE_DOES_NOT_EXIST:
                yield None
            else:
                raise OSError(error, f"OpenServiceW failed for {service_name}")
        else:
            try:
                yield advapi32, service
            finally:
                advapi32.CloseServiceHandle(service)
    finally:
        advapi32.CloseServiceHandle(manager)


def query_service_state(service_name: str = SERVICE_NAME) -> int | None:
    """Return the locale-independent SCM state, or ``None`` when absent."""
    if sys.platform != "win32":
        return None

    with _open_scm_service(service_name, _SERVICE_QUERY_STATUS) as opened:
        if opened is None:
            return None
        advapi32, service = opened
        status = _SERVICE_STATUS_PROCESS()
        needed = wintypes.DWORD()
        status_bytes = ctypes.cast(
            ctypes.byref(status),
            ctypes.POINTER(ctypes.c_byte),
        )
        if not advapi32.QueryServiceStatusEx(
            service,
            _SC_STATUS_PROCESS_INFO,
            status_bytes,
            ctypes.sizeof(status),
            ctypes.byref(needed),
        ):
            return None
        return int(status.dwCurrentState)


def query_service_config(service_name: str = SERVICE_NAME) -> ServiceConfig | None:
    """Return lifecycle-relevant SCM configuration, or ``None`` when unavailable."""
    if sys.platform != "win32":
        return None

    with _open_scm_service(service_name, _SERVICE_QUERY_CONFIG) as opened:
        if opened is None:
            return None
        advapi32, service = opened
        needed = wintypes.DWORD()
        advapi32.QueryServiceConfigW(service, None, 0, ctypes.byref(needed))
        if needed.value == 0:
            return None
        buffer = ctypes.create_string_buffer(needed.value)
        if not advapi32.QueryServiceConfigW(
            service,
            buffer,
            needed.value,
            ctypes.byref(needed),
        ):
            return None
        config = ctypes.cast(
            buffer,
            ctypes.POINTER(_QUERY_SERVICE_CONFIGW),
        ).contents
        return ServiceConfig(
            binary_path=str(config.lpBinaryPathName or ""),
            start_type=int(config.dwStartType),
        )
