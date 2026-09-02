"""Best-effort standard-library client for the per-user AI Watch daemon."""

from __future__ import annotations

import ctypes
import os
import socket
import sys
import time
from typing import Any

from runlayer_cli.hook.daemon_protocol import (
    CONNECT_TIMEOUT_SECONDS,
    FRAME_PREFIX_SIZE,
    HEALTH_TIMEOUT_SECONDS,
    REQUEST_ACCEPTED_ACK,
    RESPONSE_TIMEOUT_SECONDS,
    FrameError,
    HealthRequest,
    HealthResponse,
    HookRequest,
    HookResult,
    Overlapped,
    RestartingResponse,
    WINDOWS_RESPONSE_ACK,
    current_windows_user_sid,
    daemon_endpoint,
    decode_frame,
    encode_frame,
    frame_body_length,
    last_windows_error,
    parse_hook_response,
    parse_health_response,
    protocol_version,
    request_environment,
    windows_dll,
    windows_error,
)


class _DaemonRequestAcceptedError(RuntimeError):
    """Raised when replay is unsafe because the daemon accepted the hook."""


class _DaemonClosedBeforeAcceptanceError(OSError):
    """Raised when the daemon dropped the connection before the acceptance frame.

    The signature of an older daemon strict-parsing away the unknown
    ``client_start_ms`` key (also seen when the daemon sheds an over-limit
    connection, hence the ``OSError`` base — callers treating connection
    failures generically keep working). Deadline expiries are deliberately
    excluded: a stalled daemon must fall back inline, not burn another
    response timeout on retry.
    """


def daemon_is_enabled() -> bool:
    """Return whether the managed org-key rollout gate enables daemon IPC."""
    try:
        from runlayer_cli.mdm_config import (  # noqa: PLC0415 - stdlib-only closure
            daemon_gate_open,
            read_managed_config,
        )

        return daemon_gate_open(read_managed_config())
    except Exception:
        return False


def try_daemon_hook(
    stdin_text: str,
    *,
    client_start_ms: int | None = None,
    _gate_checked: bool = False,
) -> HookResult | None:
    """Run one hook through the daemon, returning ``None`` for inline fallback."""
    try:
        if not _gate_checked and not daemon_is_enabled():
            return None
        request: HookRequest = {
            "version": protocol_version(),
            "argv": list(sys.argv),
            "cwd": os.getcwd(),
            "env": request_environment(),
            "stdin": stdin_text,
        }
        if client_start_ms is not None and client_start_ms > 0:
            request["client_start_ms"] = client_start_ms
        try:
            payload = _send_hook_request(request)
        except _DaemonClosedBeforeAcceptanceError:
            if "client_start_ms" not in request:
                raise
            # Older daemons strict-parse the request and reject the unknown
            # client_start_ms key before their version check, closing without
            # a response — which would also suppress the version-skew drain
            # that closed connection exists to trigger. One retry with a
            # legacy frame gives such a daemon a parseable request: the
            # version mismatch then answers "restarting" and begins drain.
            # Pre-acceptance failures are replay-safe by design; a
            # same-version daemon on this path merely serves the hook without
            # startup attribution.
            del request["client_start_ms"]
            payload = _send_hook_request(request)
        response = parse_hook_response(payload)
        if "status" in response:
            return None
        return response
    except _DaemonRequestAcceptedError:
        return {
            "stdout": "",
            "stderr": "AI Watch daemon stopped before returning a hook result.\n",
            "exit_code": 2,
        }
    except Exception:
        return None


def _send_hook_request(request: HookRequest) -> object:
    endpoint = daemon_endpoint()
    if sys.platform == "win32":
        return _send_windows_request(endpoint, request)
    return _send_unix_request(endpoint, request)


def probe_daemon(
    endpoint: str | None = None,
) -> HealthResponse | RestartingResponse | None:
    """Probe one daemon without dispatching a hook or triggering version drain."""
    try:
        request: HealthRequest = {
            "op": "health",
            "version": protocol_version(),
        }
        resolved_endpoint = endpoint or daemon_endpoint()
        if sys.platform == "win32":
            payload = _send_windows_request(
                resolved_endpoint,
                request,
                response_timeout=HEALTH_TIMEOUT_SECONDS,
            )
        else:
            payload = _send_unix_request(
                resolved_endpoint,
                request,
                response_timeout=HEALTH_TIMEOUT_SECONDS,
            )
        return parse_health_response(payload)
    except Exception:
        return None


def _send_unix_request(
    endpoint: str,
    request: HookRequest | HealthRequest,
    *,
    response_timeout: float | None = None,
) -> object:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(CONNECT_TIMEOUT_SECONDS)
        client.connect(endpoint)
        timeout = (
            RESPONSE_TIMEOUT_SECONDS if response_timeout is None else response_timeout
        )
        deadline = time.monotonic() + timeout
        request_frame = encode_frame(request)
        try:
            _send_unix_all(client, request_frame, deadline=deadline)
            first = _receive_unix_frame(client, deadline=deadline)
        except TimeoutError:
            raise
        except Exception as exc:
            raise _DaemonClosedBeforeAcceptanceError() from exc
        if first != {"status": "accepted"}:
            return first
        # A failed send delivered nothing (send() is all-or-nothing per call and
        # raising means not every byte was queued), so the daemon can never read
        # the full ACK and never dispatches: inline replay stays safe.
        _send_unix_all(client, REQUEST_ACCEPTED_ACK, deadline=deadline)
        try:
            response = _receive_unix_frame(client, deadline=deadline)
            return _validate_accepted_response(response)
        except Exception as exc:
            raise _DaemonRequestAcceptedError() from exc


def _receive_unix_frame(client: socket.socket, *, deadline: float) -> object:
    length = frame_body_length(
        _receive_unix_exactly(client, FRAME_PREFIX_SIZE, deadline=deadline)
    )
    return decode_frame(_receive_unix_exactly(client, length, deadline=deadline))


def _validate_accepted_response(response: object) -> object:
    parsed = parse_hook_response(response)
    if "status" in parsed:
        raise FrameError("accepted hook returned a status response")
    return response


def _send_unix_all(
    client: socket.socket,
    data: bytes,
    *,
    deadline: float,
) -> None:
    offset = 0
    while offset < len(data):
        client.settimeout(_remaining_seconds(deadline))
        written = client.send(data[offset:])
        if written <= 0:
            raise OSError("Unix socket write made no progress")
        offset += written


def _receive_unix_exactly(
    client: socket.socket,
    size: int,
    *,
    deadline: float,
) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        client.settimeout(_remaining_seconds(deadline))
        chunk = client.recv(remaining)
        if not chunk:
            raise FrameError("frame ended before declared length")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _remaining_seconds(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("daemon response timed out")
    return remaining


def _send_windows_request(
    endpoint: str,
    request: HookRequest | HealthRequest,
    *,
    response_timeout: float | None = None,
) -> object:
    kernel32 = windows_dll("kernel32")
    _bind_windows_pipe_functions(kernel32)
    handle = _connect_windows_pipe(kernel32, endpoint)
    try:
        return _exchange_windows_request(
            kernel32,
            handle,
            request,
            deadline=time.monotonic()
            + (
                RESPONSE_TIMEOUT_SECONDS
                if response_timeout is None
                else response_timeout
            ),
        )
    finally:
        kernel32.CloseHandle(handle)


def _bind_windows_pipe_functions(kernel32: Any) -> None:
    from ctypes import wintypes  # noqa: PLC0415 - unavailable API off Windows

    kernel32.WaitNamedPipeW.argtypes = (wintypes.LPCWSTR, wintypes.DWORD)
    kernel32.WaitNamedPipeW.restype = wintypes.BOOL
    kernel32.CreateFileW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    kernel32.CreateFileW.restype = wintypes.HANDLE
    kernel32.SetNamedPipeHandleState.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
        wintypes.LPVOID,
    )
    kernel32.SetNamedPipeHandleState.restype = wintypes.BOOL
    kernel32.ReadFile.argtypes = (
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    )
    kernel32.ReadFile.restype = wintypes.BOOL
    kernel32.WriteFile.argtypes = (
        wintypes.HANDLE,
        wintypes.LPCVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    )
    kernel32.WriteFile.restype = wintypes.BOOL
    kernel32.CreateEventW.argtypes = (
        wintypes.LPVOID,
        wintypes.BOOL,
        wintypes.BOOL,
        wintypes.LPCWSTR,
    )
    kernel32.CreateEventW.restype = wintypes.HANDLE
    kernel32.WaitForSingleObject.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
    )
    kernel32.WaitForSingleObject.restype = wintypes.DWORD
    kernel32.GetOverlappedResult.argtypes = (
        wintypes.HANDLE,
        wintypes.LPVOID,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.BOOL,
    )
    kernel32.GetOverlappedResult.restype = wintypes.BOOL
    kernel32.CancelIoEx.argtypes = (wintypes.HANDLE, wintypes.LPVOID)
    kernel32.CancelIoEx.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL


def _connect_windows_pipe(kernel32: Any, endpoint: str) -> object:
    """Open the daemon pipe, prove the owner, and switch it to byte mode."""
    from ctypes import wintypes  # noqa: PLC0415 - unavailable API off Windows

    generic_read = 0x80000000
    generic_write = 0x40000000
    read_control = 0x00020000
    open_existing = 3
    pipe_readmode_byte = 0
    file_flag_overlapped = 0x40000000
    invalid_handle_value = ctypes.c_void_p(-1).value

    if not kernel32.WaitNamedPipeW(endpoint, int(CONNECT_TIMEOUT_SECONDS * 1000)):
        raise windows_error()
    handle = kernel32.CreateFileW(
        endpoint,
        generic_read | generic_write | read_control,
        0,
        None,
        open_existing,
        file_flag_overlapped,
        None,
    )
    if handle == invalid_handle_value:
        raise windows_error()

    try:
        _verify_windows_pipe_owner(handle)
        mode = wintypes.DWORD(pipe_readmode_byte)
        if not kernel32.SetNamedPipeHandleState(
            handle,
            ctypes.byref(mode),
            None,
            None,
        ):
            raise windows_error()
    except BaseException:
        kernel32.CloseHandle(handle)
        raise
    return handle


def _exchange_windows_request(
    kernel32: Any,
    handle: object,
    request: HookRequest | HealthRequest,
    *,
    deadline: float,
) -> object:
    request_frame = encode_frame(request)
    try:
        _write_windows_handle(
            kernel32,
            handle,
            request_frame,
            deadline=deadline,
        )
        response = _read_windows_frame(kernel32, handle, deadline=deadline)
    except TimeoutError:
        raise
    except Exception as exc:
        raise _DaemonClosedBeforeAcceptanceError() from exc
    if response == {"status": "accepted"}:
        response = _await_windows_accepted_response(
            kernel32,
            handle,
            deadline=deadline,
        )
    _ack_windows_response(kernel32, handle, deadline=deadline)
    return response


def _await_windows_accepted_response(
    kernel32: Any,
    handle: object,
    *,
    deadline: float,
) -> object:
    # A raising ACK write means the bytes were not delivered (the overlapped
    # transfer reports a cancelled-but-completed write as success), so the
    # daemon never dispatches: inline replay is safe.
    _write_windows_handle(
        kernel32,
        handle,
        REQUEST_ACCEPTED_ACK,
        deadline=deadline,
    )
    try:
        response = _read_windows_frame(kernel32, handle, deadline=deadline)
        return _validate_accepted_response(response)
    except Exception as exc:
        raise _DaemonRequestAcceptedError() from exc


def _ack_windows_response(
    kernel32: Any,
    handle: object,
    *,
    deadline: float,
) -> None:
    try:
        _write_windows_handle(
            kernel32,
            handle,
            WINDOWS_RESPONSE_ACK,
            deadline=deadline,
        )
    except Exception:
        # The complete validated response is authoritative; an ACK race must
        # not replay the hook inline.
        pass


def _read_windows_frame(
    kernel32: Any,
    handle: object,
    *,
    deadline: float,
) -> object:
    length = frame_body_length(
        _read_windows_exactly(
            kernel32,
            handle,
            FRAME_PREFIX_SIZE,
            deadline=deadline,
        )
    )
    return decode_frame(
        _read_windows_exactly(
            kernel32,
            handle,
            length,
            deadline=deadline,
        )
    )


def _write_windows_handle(
    kernel32: Any,
    handle: object,
    data: bytes,
    *,
    deadline: float,
) -> None:
    offset = 0
    while offset < len(data):
        chunk = data[offset:]
        buffer = ctypes.create_string_buffer(chunk)
        written = _windows_overlapped_transfer(
            kernel32,
            handle,
            buffer,
            len(chunk),
            write=True,
            deadline=deadline,
        )
        if written == 0:
            raise OSError("named pipe write made no progress")
        offset += written


def _read_windows_exactly(
    kernel32: Any,
    handle: object,
    size: int,
    *,
    deadline: float,
) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        buffer = ctypes.create_string_buffer(remaining)
        read = _windows_overlapped_transfer(
            kernel32,
            handle,
            buffer,
            remaining,
            write=False,
            deadline=deadline,
        )
        if read == 0:
            raise FrameError("frame ended before declared length")
        chunks.append(buffer.raw[:read])
        remaining -= read
    return b"".join(chunks)


def _verify_windows_pipe_owner(handle: object) -> None:
    from ctypes import wintypes  # noqa: PLC0415 - unavailable API off Windows

    se_kernel_object = 6
    owner_security_information = 0x00000001
    advapi32 = windows_dll("advapi32")
    kernel32 = windows_dll("kernel32")
    advapi32.GetSecurityInfo.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p),
        wintypes.LPVOID,
        wintypes.LPVOID,
        wintypes.LPVOID,
        ctypes.POINTER(ctypes.c_void_p),
    )
    advapi32.GetSecurityInfo.restype = wintypes.DWORD
    advapi32.ConvertSidToStringSidW.argtypes = (
        ctypes.c_void_p,
        ctypes.POINTER(wintypes.LPWSTR),
    )
    advapi32.ConvertSidToStringSidW.restype = wintypes.BOOL
    kernel32.LocalFree.argtypes = (ctypes.c_void_p,)
    kernel32.LocalFree.restype = ctypes.c_void_p

    owner = ctypes.c_void_p()
    descriptor = ctypes.c_void_p()
    result = advapi32.GetSecurityInfo(
        handle,
        se_kernel_object,
        owner_security_information,
        ctypes.byref(owner),
        None,
        None,
        None,
        ctypes.byref(descriptor),
    )
    if result != 0:
        raise windows_error(int(result))

    owner_text = wintypes.LPWSTR()
    try:
        if not owner.value or not advapi32.ConvertSidToStringSidW(
            owner,
            ctypes.byref(owner_text),
        ):
            raise windows_error()
        if owner_text.value != current_windows_user_sid():
            raise PermissionError("named pipe daemon is owned by another user")
    finally:
        if owner_text:
            kernel32.LocalFree(ctypes.cast(owner_text, ctypes.c_void_p))
        if descriptor.value:
            kernel32.LocalFree(descriptor)


def _windows_overlapped_transfer(
    kernel32: Any,
    handle: object,
    buffer: Any,
    size: int,
    *,
    write: bool,
    deadline: float,
) -> int:
    from ctypes import wintypes  # noqa: PLC0415 - unavailable API off Windows

    error_io_pending = 997
    wait_object_0 = 0
    wait_timeout = 258
    infinite = 0xFFFFFFFF

    event = kernel32.CreateEventW(None, True, False, None)
    if not event:
        raise windows_error()
    overlapped = Overlapped()
    overlapped.hEvent = event
    transferred = wintypes.DWORD()
    operation = kernel32.WriteFile if write else kernel32.ReadFile
    pending = False
    try:
        completed = operation(
            handle,
            buffer,
            size,
            ctypes.byref(transferred),
            ctypes.byref(overlapped),
        )
        if not completed:
            error = last_windows_error()
            if error != error_io_pending:
                raise windows_error(error)
            pending = True
            remaining = deadline - time.monotonic()
            timeout_ms = max(0, int(remaining * 1000))
            wait_result = kernel32.WaitForSingleObject(event, timeout_ms)
            if wait_result != wait_object_0:
                kernel32.CancelIoEx(handle, ctypes.byref(overlapped))
                kernel32.WaitForSingleObject(event, infinite)
                pending = False
                # CancelIoEx cannot revoke an already-completed transfer, and
                # callers classify replay safety by whether bytes were
                # delivered — so report a completed transfer as success.
                if kernel32.GetOverlappedResult(
                    handle,
                    ctypes.byref(overlapped),
                    ctypes.byref(transferred),
                    False,
                ):
                    return int(transferred.value)
                if wait_result == wait_timeout:
                    raise TimeoutError("named pipe daemon response timed out")
                raise windows_error()
            pending = False
            if not kernel32.GetOverlappedResult(
                handle,
                ctypes.byref(overlapped),
                ctypes.byref(transferred),
                False,
            ):
                raise windows_error()
        return int(transferred.value)
    except BaseException:
        if pending:
            kernel32.CancelIoEx(handle, ctypes.byref(overlapped))
            kernel32.WaitForSingleObject(event, infinite)
        raise
    finally:
        kernel32.CloseHandle(event)
