"""Bounded Windows process-token owner lookup for profile scan attribution."""

from __future__ import annotations

import ctypes
from ctypes import wintypes

_PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
_TOKEN_QUERY = 0x0008
_TOKEN_USER = 1


class _SidAndAttributes(ctypes.Structure):
    _fields_ = [("sid", ctypes.c_void_p), ("attributes", wintypes.DWORD)]


class _TokenUser(ctypes.Structure):
    _fields_ = [("user", _SidAndAttributes)]


def windows_process_owner_sid(pid: int) -> str | None:
    """Return a process token's owner SID without invoking WMI."""

    try:
        kernel32 = ctypes.windll.kernel32  # ty: ignore[unresolved-attribute]
        advapi32 = ctypes.windll.advapi32  # ty: ignore[unresolved-attribute]
    except AttributeError:
        return None

    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]
    kernel32.LocalFree.restype = ctypes.c_void_p
    advapi32.OpenProcessToken.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.HANDLE),
    ]
    advapi32.OpenProcessToken.restype = wintypes.BOOL
    advapi32.GetTokenInformation.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    advapi32.GetTokenInformation.restype = wintypes.BOOL
    advapi32.ConvertSidToStringSidW.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(wintypes.LPWSTR),
    ]
    advapi32.ConvertSidToStringSidW.restype = wintypes.BOOL

    process = kernel32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not process:
        return None
    try:
        token = wintypes.HANDLE()
        if not advapi32.OpenProcessToken(process, _TOKEN_QUERY, ctypes.byref(token)):
            return None
        try:
            required = wintypes.DWORD()
            advapi32.GetTokenInformation(
                token,
                _TOKEN_USER,
                None,
                0,
                ctypes.byref(required),
            )
            if required.value < ctypes.sizeof(_TokenUser):
                return None
            token_buffer = ctypes.create_string_buffer(required.value)
            if not advapi32.GetTokenInformation(
                token,
                _TOKEN_USER,
                token_buffer,
                required,
                ctypes.byref(required),
            ):
                return None
            token_user = ctypes.cast(
                token_buffer,
                ctypes.POINTER(_TokenUser),
            ).contents
            sid_text = wintypes.LPWSTR()
            if not advapi32.ConvertSidToStringSidW(
                token_user.user.sid,
                ctypes.byref(sid_text),
            ):
                return None
            try:
                return sid_text.value
            finally:
                kernel32.LocalFree(sid_text)
        finally:
            kernel32.CloseHandle(token)
    finally:
        kernel32.CloseHandle(process)
