"""Deadline-aware HTTP transport over Windows named pipes."""

from __future__ import annotations

import ctypes
import http.client
import io
import math
import socket
import sys
import threading
import time
from typing import TYPE_CHECKING, IO, Any, Callable, Protocol, cast

if TYPE_CHECKING:
    from ctypes import wintypes
elif sys.platform == "win32":
    from ctypes import wintypes
else:
    wintypes = None

_READ_CHUNK_BYTES = 64 * 1024
_WINDOWS_PIPE_PROBE_TIMEOUT_SECONDS = 0.2

_GENERIC_READ = 0x80000000
_GENERIC_WRITE = 0x40000000
_OPEN_EXISTING = 3
_FILE_FLAG_OVERLAPPED = 0x40000000
# WinBase.h security-quality-of-service values. Identification lets the pipe
# server identify the caller for authorization but cannot impersonate its token.
_SECURITY_IDENTIFICATION = 0x00010000
_SECURITY_SQOS_PRESENT = 0x00100000
_PIPE_READMODE_BYTE = 0x00000000
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

_ERROR_BROKEN_PIPE = 109
_ERROR_SEM_TIMEOUT = 121
_ERROR_PIPE_BUSY = 231
_ERROR_NO_DATA = 232
_ERROR_PIPE_NOT_CONNECTED = 233
_ERROR_IO_PENDING = 997
_WAIT_OBJECT_0 = 0
_WAIT_TIMEOUT = 258
_WAIT_FAILED = 0xFFFFFFFF
_INFINITE = 0xFFFFFFFF
_MAX_FINITE_WAIT_MS = 0xFFFFFFFE
_WINDOWS_CANCEL_WAIT_MS = 50

__all__ = [
    "_WindowsNamedPipeHTTPConnection",
    "_windows_named_pipe_available",
]


class _Overlapped(ctypes.Structure):
    """Portable definition of Win32 ``OVERLAPPED``."""

    _fields_ = [
        ("Internal", ctypes.c_size_t),
        ("InternalHigh", ctypes.c_size_t),
        ("Offset", ctypes.c_uint32),
        ("OffsetHigh", ctypes.c_uint32),
        ("hEvent", ctypes.c_void_p),
    ]


class _WindowsNamedPipeAPI(Protocol):
    """Small synchronous named-pipe API seam used by the HTTP adapter."""

    def open_pipe(self, path: str, *, timeout: float | None) -> int: ...

    def read(self, handle: int, max_bytes: int, *, timeout: float | None) -> bytes: ...

    def write(self, handle: int, data: bytes, *, timeout: float | None) -> int: ...

    def close_handle(self, handle: int) -> None: ...


def _last_windows_error() -> int:
    return int(
        ctypes.get_last_error()  # ty: ignore[unresolved-attribute]
    )


def _windows_error(code: int | None = None) -> OSError:
    return ctypes.WinError(  # ty: ignore[unresolved-attribute]
        _last_windows_error() if code is None else code
    )


def _timeout_milliseconds(timeout: float | None) -> int:
    if timeout is None:
        return _INFINITE
    if timeout <= 0:
        return 0
    return min(max(1, math.ceil(timeout * 1000)), _MAX_FINITE_WAIT_MS)


class _CtypesWindowsNamedPipeAPI:
    """Win32 named-pipe client with deadline-aware overlapped I/O."""

    def __init__(self) -> None:
        if wintypes is None:
            raise OSError("Windows named pipes are unavailable")
        self._wintypes = wintypes
        self._kernel32 = ctypes.WinDLL(  # ty: ignore[unresolved-attribute]
            "kernel32",
            use_last_error=True,
        )
        self._closed_handles: set[int] = set()
        self._close_lock = threading.Lock()
        self._kernel32.WaitNamedPipeW.argtypes = (
            wintypes.LPCWSTR,
            wintypes.DWORD,
        )
        self._kernel32.WaitNamedPipeW.restype = wintypes.BOOL
        self._kernel32.CreateFileW.argtypes = (
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        )
        self._kernel32.CreateFileW.restype = wintypes.HANDLE
        self._kernel32.SetNamedPipeHandleState.argtypes = (
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
            wintypes.LPVOID,
        )
        self._kernel32.SetNamedPipeHandleState.restype = wintypes.BOOL
        self._kernel32.ReadFile.argtypes = (
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(_Overlapped),
        )
        self._kernel32.ReadFile.restype = wintypes.BOOL
        self._kernel32.WriteFile.argtypes = (
            wintypes.HANDLE,
            wintypes.LPCVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(_Overlapped),
        )
        self._kernel32.WriteFile.restype = wintypes.BOOL
        self._kernel32.CreateEventW.argtypes = (
            wintypes.LPVOID,
            wintypes.BOOL,
            wintypes.BOOL,
            wintypes.LPCWSTR,
        )
        self._kernel32.CreateEventW.restype = wintypes.HANDLE
        self._kernel32.WaitForSingleObject.argtypes = (
            wintypes.HANDLE,
            wintypes.DWORD,
        )
        self._kernel32.WaitForSingleObject.restype = wintypes.DWORD
        self._kernel32.GetOverlappedResult.argtypes = (
            wintypes.HANDLE,
            ctypes.POINTER(_Overlapped),
            ctypes.POINTER(wintypes.DWORD),
            wintypes.BOOL,
        )
        self._kernel32.GetOverlappedResult.restype = wintypes.BOOL
        self._kernel32.CancelIoEx.argtypes = (
            wintypes.HANDLE,
            ctypes.POINTER(_Overlapped),
        )
        self._kernel32.CancelIoEx.restype = wintypes.BOOL
        self._kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
        self._kernel32.CloseHandle.restype = wintypes.BOOL

    def open_pipe(self, path: str, *, timeout: float | None) -> int:
        """Open one pipe instance without exceeding ``timeout``."""
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            remaining = (
                None if deadline is None else max(0.0, deadline - time.monotonic())
            )
            if remaining is not None and remaining <= 0:
                raise TimeoutError("named pipe connection timed out")
            if not self._kernel32.WaitNamedPipeW(
                path,
                _timeout_milliseconds(remaining),
            ):
                error = _last_windows_error()
                if error == _ERROR_SEM_TIMEOUT:
                    raise TimeoutError("named pipe connection timed out")
                raise _windows_error(error)

            handle = self._kernel32.CreateFileW(
                path,
                _GENERIC_READ | _GENERIC_WRITE,
                0,
                None,
                _OPEN_EXISTING,
                (
                    _FILE_FLAG_OVERLAPPED
                    | _SECURITY_SQOS_PRESENT
                    | _SECURITY_IDENTIFICATION
                ),
                None,
            )
            if handle != _INVALID_HANDLE_VALUE:
                break

            error = _last_windows_error()
            if error != _ERROR_PIPE_BUSY:
                raise _windows_error(error)
            if deadline is not None and time.monotonic() >= deadline:
                raise TimeoutError("named pipe connection timed out")

        mode = self._wintypes.DWORD(_PIPE_READMODE_BYTE)
        if not self._kernel32.SetNamedPipeHandleState(
            handle,
            ctypes.byref(mode),
            None,
            None,
        ):
            error = _last_windows_error()
            self.close_handle(int(handle))
            raise _windows_error(error)
        return int(handle)

    def read(self, handle: int, max_bytes: int, *, timeout: float | None) -> bytes:
        if max_bytes <= 0:
            return b""
        buffer = ctypes.create_string_buffer(max_bytes)
        try:
            transferred = self._transfer(
                handle,
                buffer,
                max_bytes,
                write=False,
                timeout=timeout,
            )
        except OSError as exc:
            if getattr(exc, "winerror", None) in {
                _ERROR_BROKEN_PIPE,
                _ERROR_NO_DATA,
                _ERROR_PIPE_NOT_CONNECTED,
            }:
                return b""
            raise
        if transferred > max_bytes:
            raise OSError("named pipe read exceeded requested size")
        return buffer.raw[:transferred]

    def write(self, handle: int, data: bytes, *, timeout: float | None) -> int:
        if not data:
            return 0
        buffer = ctypes.create_string_buffer(data)
        return self._transfer(
            handle,
            buffer,
            len(data),
            write=True,
            timeout=timeout,
        )

    def close_handle(self, handle: int) -> None:
        should_close = False
        with self._close_lock:
            if handle not in self._closed_handles:
                self._closed_handles.add(handle)
                should_close = True
        if should_close:
            self._kernel32.CloseHandle(handle)

    def _retain_pending_transfer(
        self,
        *,
        event: int,
        overlapped: _Overlapped,
        buffer: Any,
    ) -> None:
        """Keep I/O storage alive until forced-close completion signals."""

        kernel32 = self._kernel32

        def drain() -> None:
            _keepalive = (overlapped, buffer)
            while True:
                result = kernel32.WaitForSingleObject(
                    event,
                    _WINDOWS_CANCEL_WAIT_MS,
                )
                if result == _WAIT_OBJECT_0:
                    kernel32.CloseHandle(event)
                    return
                time.sleep(_WINDOWS_CANCEL_WAIT_MS / 1000)

        threading.Thread(
            target=drain,
            name="docker-pipe-cancel-drain",
            daemon=True,
        ).start()

    def _cancel_pending_transfer(
        self,
        *,
        handle: int,
        event: int,
        overlapped: _Overlapped,
        buffer: Any,
    ) -> bool:
        """Cancel pending I/O; return whether the caller still owns the event."""

        self._kernel32.CancelIoEx(handle, ctypes.byref(overlapped))
        settled = self._kernel32.WaitForSingleObject(
            event,
            _WINDOWS_CANCEL_WAIT_MS,
        )
        if settled == _WAIT_OBJECT_0:
            return True

        self.close_handle(handle)
        settled = self._kernel32.WaitForSingleObject(
            event,
            _WINDOWS_CANCEL_WAIT_MS,
        )
        if settled == _WAIT_OBJECT_0:
            return True

        self._retain_pending_transfer(
            event=event,
            overlapped=overlapped,
            buffer=buffer,
        )
        return False

    def _transfer(
        self,
        handle: int,
        buffer: Any,
        size: int,
        *,
        write: bool,
        timeout: float | None,
    ) -> int:
        event = self._kernel32.CreateEventW(None, True, False, None)
        if not event:
            raise _windows_error()
        overlapped = _Overlapped()
        overlapped.hEvent = event
        transferred = self._wintypes.DWORD()
        operation = self._kernel32.WriteFile if write else self._kernel32.ReadFile
        pending = False
        event_owned = True
        try:
            completed = operation(
                handle,
                buffer,
                size,
                ctypes.byref(transferred),
                ctypes.byref(overlapped),
            )
            if not completed:
                error = _last_windows_error()
                if error != _ERROR_IO_PENDING:
                    raise _windows_error(error)
                pending = True
                wait_result = self._kernel32.WaitForSingleObject(
                    event,
                    _timeout_milliseconds(timeout),
                )
                if wait_result != _WAIT_OBJECT_0:
                    wait_error = (
                        _last_windows_error() if wait_result == _WAIT_FAILED else None
                    )
                    event_owned = self._cancel_pending_transfer(
                        handle=handle,
                        event=event,
                        overlapped=overlapped,
                        buffer=buffer,
                    )
                    pending = False
                    if wait_result == _WAIT_TIMEOUT:
                        raise TimeoutError("named pipe I/O timed out")
                    if wait_result == _WAIT_FAILED:
                        raise _windows_error(wait_error)
                    raise OSError("unexpected named pipe wait result")

                pending = False
            if not self._kernel32.GetOverlappedResult(
                handle,
                ctypes.byref(overlapped),
                ctypes.byref(transferred),
                False,
            ):
                raise _windows_error()
            return int(transferred.value)
        except BaseException:
            if pending:
                event_owned = self._cancel_pending_transfer(
                    handle=handle,
                    event=event,
                    overlapped=overlapped,
                    buffer=buffer,
                )
            raise
        finally:
            if event_owned:
                self._kernel32.CloseHandle(event)


def _new_windows_named_pipe_api() -> _WindowsNamedPipeAPI:
    return _CtypesWindowsNamedPipeAPI()


class _WindowsNamedPipeHandle:
    """Reference-counted handle shared by a socket facade and its file."""

    def __init__(
        self,
        api: _WindowsNamedPipeAPI,
        handle: int,
        *,
        timeout: float | None,
        deadline: float | None,
    ) -> None:
        self._api = api
        self._handle: int | None = handle
        self._timeout = timeout
        self._deadline = deadline
        self._references = 1
        self._lock = threading.Lock()

    def acquire(self) -> None:
        with self._lock:
            if self._handle is None:
                raise OSError("named pipe is closed")
            self._references += 1

    def release(self) -> None:
        handle: int | None = None
        with self._lock:
            if self._references <= 0:
                return
            self._references -= 1
            if self._references == 0:
                handle = self._handle
                self._handle = None
        if handle is not None:
            self._api.close_handle(handle)

    def settimeout(self, timeout: float | None) -> None:
        with self._lock:
            if self._handle is None:
                raise OSError("named pipe is closed")
            self._timeout = timeout

    def set_deadline(self, deadline: float | None) -> None:
        with self._lock:
            if self._handle is None:
                raise OSError("named pipe is closed")
            self._deadline = deadline

    def gettimeout(self) -> float | None:
        with self._lock:
            return self._timeout

    def _operation_timeout(self) -> float | None:
        with self._lock:
            if self._handle is None:
                raise OSError("named pipe is closed")
            timeout = self._timeout
            deadline = self._deadline
        if deadline is None:
            return timeout
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("named pipe request deadline exceeded")
        return remaining if timeout is None else min(timeout, remaining)

    def read(self, max_bytes: int) -> bytes:
        with self._lock:
            handle = self._handle
        if handle is None:
            raise OSError("named pipe is closed")
        return self._api.read(
            handle,
            max_bytes,
            timeout=self._operation_timeout(),
        )

    def write(self, data: bytes) -> int:
        with self._lock:
            handle = self._handle
        if handle is None:
            raise OSError("named pipe is closed")
        return self._api.write(
            handle,
            data,
            timeout=self._operation_timeout(),
        )


class _WindowsNamedPipeRawReader(io.RawIOBase):
    """Bounded raw reader used by ``http.client.HTTPResponse``."""

    def __init__(self, handle: _WindowsNamedPipeHandle) -> None:
        super().__init__()
        self._handle = handle
        self._handle.acquire()

    def readable(self) -> bool:
        return True

    def readinto(self, buffer: Any) -> int:
        if self.closed:
            raise ValueError("I/O operation on closed named pipe")
        view = memoryview(buffer).cast("B")
        if not view:
            return 0
        chunk = self._handle.read(min(len(view), _READ_CHUNK_BYTES))
        if len(chunk) > len(view):
            raise OSError("named pipe read exceeded destination size")
        view[: len(chunk)] = chunk
        return len(chunk)

    def close(self) -> None:
        if not self.closed:
            try:
                self._handle.release()
            finally:
                super().close()


class _WindowsNamedPipeSocket:
    """Socket/file subset required by ``http.client``."""

    def __init__(
        self,
        api: _WindowsNamedPipeAPI,
        handle: int,
        *,
        timeout: float | None,
        deadline: float | None,
    ) -> None:
        self._handle = _WindowsNamedPipeHandle(
            api,
            handle,
            timeout=timeout,
            deadline=deadline,
        )
        self._closed = False

    @classmethod
    def connect(
        cls,
        path: str,
        *,
        timeout: float | None,
        deadline: float | None,
        api: _WindowsNamedPipeAPI,
    ) -> _WindowsNamedPipeSocket:
        open_timeout = timeout
        if deadline is not None:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("named pipe request deadline exceeded")
            open_timeout = remaining if timeout is None else min(timeout, remaining)
        handle = api.open_pipe(path, timeout=open_timeout)
        return cls(api, handle, timeout=timeout, deadline=deadline)

    def sendall(self, data: Any, flags: int = 0) -> None:
        if flags:
            raise ValueError("named pipe transport does not support send flags")
        payload = bytes(data)
        offset = 0
        while offset < len(payload):
            chunk = payload[offset : offset + _READ_CHUNK_BYTES]
            written = self._handle.write(chunk)
            if written <= 0 or written > len(chunk):
                raise OSError("named pipe write made invalid progress")
            offset += written

    def makefile(
        self,
        mode: str = "rb",
        buffering: int | None = None,
        *,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> IO[bytes]:
        if mode != "rb" or any(
            option is not None for option in (encoding, errors, newline)
        ):
            raise ValueError("named pipe HTTP transport supports binary reads only")
        reader = _WindowsNamedPipeRawReader(self._handle)
        if buffering == 0:
            return cast(IO[bytes], reader)
        buffer_size = io.DEFAULT_BUFFER_SIZE if buffering in {None, -1} else buffering
        if buffer_size is None or buffer_size <= 0:
            reader.close()
            raise ValueError("invalid named pipe buffer size")
        try:
            return cast(IO[bytes], io.BufferedReader(reader, buffer_size))
        except BaseException:
            reader.close()
            raise

    def settimeout(self, timeout: float | None) -> None:
        if timeout is not None:
            timeout = float(timeout)
            if timeout < 0 or not math.isfinite(timeout):
                raise ValueError("invalid named pipe timeout")
        self._handle.settimeout(timeout)

    def set_deadline(self, deadline: float | None) -> None:
        self._handle.set_deadline(deadline)

    def gettimeout(self) -> float | None:
        return self._handle.gettimeout()

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self._handle.release()


class _WindowsNamedPipeHTTPConnection(http.client.HTTPConnection):
    """HTTP connection whose transport is a Windows named pipe."""

    def __init__(
        self,
        pipe_path: str,
        *,
        timeout: float,
        deadline: float,
        api_factory: Callable[[], _WindowsNamedPipeAPI] | None = None,
    ) -> None:
        super().__init__("localhost", timeout=timeout)
        self._pipe_path = pipe_path
        self._deadline = deadline
        self._api_factory = api_factory or _new_windows_named_pipe_api

    def connect(self) -> None:
        timeout = None if self.timeout is None else float(self.timeout)
        pipe_socket = _WindowsNamedPipeSocket.connect(
            self._pipe_path,
            timeout=timeout,
            deadline=self._deadline,
            api=self._api_factory(),
        )
        self.sock = cast(socket.socket, pipe_socket)


def _windows_named_pipe_available(path: str) -> bool:
    """Probe a pipe with a short, bounded open and guaranteed cleanup."""
    try:
        api = _new_windows_named_pipe_api()
        handle = api.open_pipe(
            path,
            timeout=_WINDOWS_PIPE_PROBE_TIMEOUT_SECONDS,
        )
    except (AttributeError, OSError, ValueError):
        return False
    try:
        return True
    finally:
        api.close_handle(handle)
