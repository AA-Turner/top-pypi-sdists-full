"""Owner-only Windows named-pipe listener implemented with ctypes."""

from __future__ import annotations

import ctypes
import threading
from dataclasses import dataclass
from typing import Any

from runlayer_cli.hook.daemon_protocol import (
    Overlapped,
    current_windows_user_sid,
    last_windows_error,
    windows_dll,
    windows_error,
)

_PIPE_ACCESS_DUPLEX = 0x00000003
_FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000
_FILE_FLAG_OVERLAPPED = 0x40000000
_PIPE_TYPE_BYTE = 0x00000000
_PIPE_READMODE_BYTE = 0x00000000
_PIPE_WAIT = 0x00000000
_PIPE_REJECT_REMOTE_CLIENTS = 0x00000008
_PIPE_UNLIMITED_INSTANCES = 255
_SDDL_REVISION_1 = 1

_ERROR_INVALID_HANDLE = 6
_ERROR_BROKEN_PIPE = 109
_ERROR_PIPE_BUSY = 231
_ERROR_NO_DATA = 232
_ERROR_PIPE_NOT_CONNECTED = 233
_ERROR_OPERATION_ABORTED = 995
_ERROR_IO_PENDING = 997
_ERROR_PIPE_CONNECTED = 535
_ERROR_PIPE_LISTENING = 536
_WAIT_OBJECT_0 = 0
_WAIT_TIMEOUT = 258
_INFINITE = 0xFFFFFFFF


class PipeListenerClosed(OSError):
    """Raised when a pending named-pipe accept is closed during drain."""


class PipeAlreadyRunning(OSError):
    """Raised when another process owns the first named-pipe instance."""


class _PipeClientDisconnected(OSError):
    """Raised when a client disconnects before accept completes."""


class _SecurityAttributes(ctypes.Structure):
    _fields_ = [
        ("nLength", ctypes.c_ulong),
        ("lpSecurityDescriptor", ctypes.c_void_p),
        ("bInheritHandle", ctypes.c_int),
    ]


@dataclass
class _PendingOperation:
    handle: int
    event: int | None
    overlapped: Overlapped
    transferred: Any
    buffer: Any | None
    pending: bool


class _WindowsAPI:
    def __init__(self) -> None:
        from ctypes import wintypes  # noqa: PLC0415 - unavailable API off Windows

        self.wintypes = wintypes
        self.kernel32 = windows_dll("kernel32")
        self.advapi32 = windows_dll("advapi32")

        self.kernel32.CreateNamedPipeW.argtypes = (
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.POINTER(_SecurityAttributes),
        )
        self.kernel32.CreateNamedPipeW.restype = wintypes.HANDLE
        self.kernel32.ConnectNamedPipe.argtypes = (
            wintypes.HANDLE,
            wintypes.LPVOID,
        )
        self.kernel32.ConnectNamedPipe.restype = wintypes.BOOL
        self.kernel32.SetNamedPipeHandleState.argtypes = (
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
            wintypes.LPVOID,
        )
        self.kernel32.SetNamedPipeHandleState.restype = wintypes.BOOL
        self.kernel32.CancelIoEx.argtypes = (
            wintypes.HANDLE,
            wintypes.LPVOID,
        )
        self.kernel32.CancelIoEx.restype = wintypes.BOOL
        self.kernel32.CreateEventW.argtypes = (
            wintypes.LPVOID,
            wintypes.BOOL,
            wintypes.BOOL,
            wintypes.LPCWSTR,
        )
        self.kernel32.CreateEventW.restype = wintypes.HANDLE
        self.kernel32.WaitForSingleObject.argtypes = (
            wintypes.HANDLE,
            wintypes.DWORD,
        )
        self.kernel32.WaitForSingleObject.restype = wintypes.DWORD
        self.kernel32.GetOverlappedResult.argtypes = (
            wintypes.HANDLE,
            ctypes.POINTER(Overlapped),
            ctypes.POINTER(wintypes.DWORD),
            wintypes.BOOL,
        )
        self.kernel32.GetOverlappedResult.restype = wintypes.BOOL
        self.kernel32.DisconnectNamedPipe.argtypes = (wintypes.HANDLE,)
        self.kernel32.DisconnectNamedPipe.restype = wintypes.BOOL
        self.kernel32.ReadFile.argtypes = (
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        )
        self.kernel32.ReadFile.restype = wintypes.BOOL
        self.kernel32.WriteFile.argtypes = (
            wintypes.HANDLE,
            wintypes.LPCVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        )
        self.kernel32.WriteFile.restype = wintypes.BOOL
        self.kernel32.FlushFileBuffers.argtypes = (wintypes.HANDLE,)
        self.kernel32.FlushFileBuffers.restype = wintypes.BOOL
        self.kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
        self.kernel32.CloseHandle.restype = wintypes.BOOL
        self.kernel32.LocalFree.argtypes = (wintypes.HLOCAL,)
        self.kernel32.LocalFree.restype = wintypes.HLOCAL
        self.advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes = (
            wintypes.LPCWSTR,
            wintypes.DWORD,
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.POINTER(wintypes.DWORD),
        )
        self.advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW.restype = (
            wintypes.BOOL
        )

    def create_pipe(self, name: str, *, first_instance: bool) -> int:
        descriptor = ctypes.c_void_p()
        descriptor_size = self.wintypes.DWORD()
        # Pin owner + protected DACL to this process token's user SID.
        user_sid = current_windows_user_sid()
        sddl = f"O:{user_sid}D:P(A;;GA;;;{user_sid})"
        if not self.advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW(
            sddl,
            _SDDL_REVISION_1,
            ctypes.byref(descriptor),
            ctypes.byref(descriptor_size),
        ):
            raise windows_error()
        attributes = _SecurityAttributes(
            ctypes.sizeof(_SecurityAttributes),
            descriptor,
            False,
        )
        open_mode = _PIPE_ACCESS_DUPLEX | _FILE_FLAG_OVERLAPPED
        if first_instance:
            open_mode |= _FILE_FLAG_FIRST_PIPE_INSTANCE
        try:
            handle = self.kernel32.CreateNamedPipeW(
                name,
                open_mode,
                _PIPE_TYPE_BYTE
                | _PIPE_READMODE_BYTE
                | _PIPE_WAIT
                | _PIPE_REJECT_REMOTE_CLIENTS,
                _PIPE_UNLIMITED_INSTANCES,
                65_536,
                65_536,
                0,
                ctypes.byref(attributes),
            )
            create_error = (
                last_windows_error() if handle == ctypes.c_void_p(-1).value else None
            )
        finally:
            self.kernel32.LocalFree(descriptor)
        if handle == ctypes.c_void_p(-1).value:
            if first_instance and create_error in {5, _ERROR_PIPE_BUSY}:
                raise PipeAlreadyRunning(name)
            raise windows_error(create_error)
        return int(handle)

    def begin_connect(self, handle: int) -> _PendingOperation:
        operation = self._new_operation(handle)
        connected = self.kernel32.ConnectNamedPipe(
            handle,
            ctypes.byref(operation.overlapped),
        )
        if connected:
            operation.pending = False
            return operation

        error = last_windows_error()
        if error == _ERROR_IO_PENDING:
            return operation
        if error == _ERROR_PIPE_CONNECTED:
            operation.pending = False
            return operation
        operation.pending = False
        self._close_operation_event(operation)
        if error == _ERROR_NO_DATA:
            raise _PipeClientDisconnected()
        raise windows_error(error)

    def poll_connect(self, operation: _PendingOperation) -> bool:
        if operation.pending and not self.operation_ready(operation):
            return False
        try:
            self.complete_operation(operation)
        except OSError as exc:
            if getattr(exc, "winerror", None) in {
                _ERROR_BROKEN_PIPE,
                _ERROR_NO_DATA,
                _ERROR_PIPE_NOT_CONNECTED,
            }:
                raise _PipeClientDisconnected() from exc
            raise
        self._set_wait_mode(operation.handle)
        return True

    def begin_read(self, handle: int, max_bytes: int) -> _PendingOperation:
        buffer = ctypes.create_string_buffer(max_bytes)
        operation = self._new_operation(handle, buffer=buffer)
        completed = self.kernel32.ReadFile(
            handle,
            buffer,
            max_bytes,
            ctypes.byref(operation.transferred),
            ctypes.byref(operation.overlapped),
        )
        self._record_io_start(operation, completed)
        return operation

    def begin_write(self, handle: int, item: bytes) -> _PendingOperation:
        buffer = ctypes.create_string_buffer(item)
        operation = self._new_operation(handle, buffer=buffer)
        completed = self.kernel32.WriteFile(
            handle,
            buffer,
            len(item),
            ctypes.byref(operation.transferred),
            ctypes.byref(operation.overlapped),
        )
        self._record_io_start(operation, completed)
        return operation

    def _record_io_start(
        self,
        operation: _PendingOperation,
        completed: bool,
    ) -> None:
        if completed:
            operation.pending = False
            return
        error = last_windows_error()
        if error != _ERROR_IO_PENDING:
            operation.pending = False
            self._close_operation_event(operation)
            raise windows_error(error)

    def operation_ready(self, operation: _PendingOperation) -> bool:
        if not operation.pending:
            return True
        assert operation.event is not None
        result = self.kernel32.WaitForSingleObject(operation.event, 0)
        if result == _WAIT_TIMEOUT:
            return False
        if result != _WAIT_OBJECT_0:
            raise windows_error()
        return True

    def complete_operation(self, operation: _PendingOperation) -> int:
        try:
            if operation.pending:
                completed = self.kernel32.GetOverlappedResult(
                    operation.handle,
                    ctypes.byref(operation.overlapped),
                    ctypes.byref(operation.transferred),
                    False,
                )
                operation.pending = False
                if not completed:
                    raise windows_error()
            return int(operation.transferred.value)
        finally:
            self._close_operation_event(operation)

    def cancel_operation(self, operation: _PendingOperation) -> None:
        try:
            if operation.pending:
                self.kernel32.CancelIoEx(
                    operation.handle,
                    ctypes.byref(operation.overlapped),
                )
                assert operation.event is not None
                self.kernel32.WaitForSingleObject(operation.event, _INFINITE)
                operation.pending = False
        finally:
            self._close_operation_event(operation)

    def _new_operation(
        self,
        handle: int,
        *,
        buffer: Any | None = None,
    ) -> _PendingOperation:
        event = self.kernel32.CreateEventW(None, True, False, None)
        if not event:
            raise windows_error()
        overlapped = Overlapped()
        overlapped.hEvent = event
        return _PendingOperation(
            handle=handle,
            event=int(event),
            overlapped=overlapped,
            transferred=self.wintypes.DWORD(),
            buffer=buffer,
            pending=True,
        )

    def _close_operation_event(self, operation: _PendingOperation) -> None:
        event = operation.event
        operation.event = None
        if event is not None:
            self.kernel32.CloseHandle(event)

    def _set_wait_mode(self, handle: int) -> None:
        mode = self.wintypes.DWORD(_PIPE_READMODE_BYTE | _PIPE_WAIT)
        if not self.kernel32.SetNamedPipeHandleState(
            handle,
            ctypes.byref(mode),
            None,
            None,
        ):
            raise windows_error()

    def close_handle(self, handle: int, *, disconnect: bool = False) -> None:
        self.kernel32.CancelIoEx(handle, None)
        if disconnect:
            self.kernel32.DisconnectNamedPipe(handle)
        self.kernel32.CloseHandle(handle)


class NamedPipeStream:
    """Small AnyIO-compatible byte stream backed by one named-pipe handle."""

    def __init__(self, api: _WindowsAPI, handle: int) -> None:
        self._api = api
        self._handle: int | None = handle
        self._lock = threading.Lock()

    async def receive(self, max_bytes: int = 65_536) -> bytes:
        handle = self._open_handle()
        try:
            operation = self._api.begin_read(handle, max_bytes)
        except OSError as exc:
            if getattr(exc, "winerror", None) in {
                _ERROR_BROKEN_PIPE,
                _ERROR_PIPE_NOT_CONNECTED,
            }:
                return b""
            raise
        try:
            received = await self._await_operation(operation)
        except OSError as exc:
            if getattr(exc, "winerror", None) in {
                _ERROR_BROKEN_PIPE,
                _ERROR_PIPE_NOT_CONNECTED,
            }:
                return b""
            raise
        assert operation.buffer is not None
        return operation.buffer.raw[:received]

    async def send(self, item: bytes) -> None:
        handle = self._open_handle()
        offset = 0
        while offset < len(item):
            operation = self._api.begin_write(handle, item[offset:])
            written = await self._await_operation(operation)
            if written == 0:
                raise OSError("named pipe write made no progress")
            offset += written

    async def wait_for_client_ack(self, expected: bytes) -> None:
        if await self.receive(len(expected)) != expected:
            raise OSError("named pipe client sent an unexpected acknowledgement")

    async def aclose(self) -> None:
        self._close_blocking()

    async def __aenter__(self) -> NamedPipeStream:
        return self

    async def __aexit__(self, *_args: object) -> None:
        await self.aclose()

    async def _await_operation(self, operation: _PendingOperation) -> int:
        import anyio  # noqa: PLC0415 - daemon-only dependency

        try:
            while not self._api.operation_ready(operation):
                await anyio.sleep(0.01)
            return self._api.complete_operation(operation)
        finally:
            if operation.event is not None:
                self._api.cancel_operation(operation)

    def _open_handle(self) -> int:
        with self._lock:
            if self._handle is None:
                raise OSError("named pipe is closed")
            return self._handle

    def _close_blocking(self) -> None:
        with self._lock:
            handle = self._handle
            self._handle = None
        if handle is not None:
            self._api.close_handle(handle, disconnect=True)


class WindowsPipeListener:
    """Cancellable overlapped accept loop for owner-only pipe instances."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._api = _WindowsAPI()
        self._lock = threading.Lock()
        self._closed = False
        self._pending: tuple[int, _PendingOperation] | None = self._create_pending(
            first_instance=True
        )

    async def accept(self) -> NamedPipeStream:
        import anyio  # noqa: PLC0415 - daemon-only dependency

        while True:
            with self._lock:
                if self._closed:
                    raise PipeListenerClosed("named-pipe listener is closed")
                if self._pending is None:
                    self._pending = self._create_pending(first_instance=False)
                handle, operation = self._pending
                try:
                    connected = self._api.poll_connect(operation)
                except _PipeClientDisconnected:
                    self._pending = None
                    self._api.cancel_operation(operation)
                    self._api.close_handle(handle)
                    connected = False
                except OSError as exc:
                    self._pending = None
                    self._api.cancel_operation(operation)
                    self._api.close_handle(handle)
                    if self._closed or getattr(exc, "winerror", None) in {
                        _ERROR_INVALID_HANDLE,
                        _ERROR_OPERATION_ABORTED,
                        _ERROR_PIPE_NOT_CONNECTED,
                    }:
                        raise PipeListenerClosed(
                            "named-pipe listener is closed"
                        ) from exc
                    raise
                if connected:
                    self._pending = None

            if connected:
                return NamedPipeStream(self._api, handle)
            await anyio.sleep(0.01)

    async def aclose(self) -> None:
        with self._lock:
            if self._closed:
                return
            self._closed = True
            pending = self._pending
            self._pending = None
        if pending is not None:
            handle, operation = pending
            self._api.cancel_operation(operation)
            self._api.close_handle(handle)

    def _create_pending(
        self,
        *,
        first_instance: bool,
    ) -> tuple[int, _PendingOperation]:
        handle = self._api.create_pipe(
            self._name,
            first_instance=first_instance,
        )
        try:
            operation = self._api.begin_connect(handle)
        except BaseException:
            self._api.close_handle(handle)
            raise
        return handle, operation
