"""Tests for the Windows named-pipe HTTP transport."""

from __future__ import annotations

import ctypes
import threading
import time
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from runlayer_cli.scan.containers import docker_socket as docker_socket_module
from runlayer_cli.scan.containers import (
    windows_named_pipe as windows_named_pipe_module,
)
from runlayer_cli.scan.containers.docker_socket import DockerSocketClient

_INVENTORY_PATH = DockerSocketClient._inventory_path()


class _FakeWindowsPipeAPI:
    def __init__(
        self,
        *,
        read_chunks: list[bytes] | None = None,
        open_error: OSError | None = None,
        write_limit: int | None = None,
    ) -> None:
        self.read_chunks = list(read_chunks or [])
        self.open_error = open_error
        self.write_limit = write_limit
        self.opens: list[tuple[str, float | None]] = []
        self.reads: list[tuple[int, float | None]] = []
        self.writes: list[tuple[bytes, float | None]] = []
        self.closed: list[int] = []

    def open_pipe(self, path: str, *, timeout: float | None) -> int:
        self.opens.append((path, timeout))
        if self.open_error is not None:
            raise self.open_error
        return 42

    def read(
        self,
        handle: int,
        max_bytes: int,
        *,
        timeout: float | None,
    ) -> bytes:
        assert handle == 42
        self.reads.append((max_bytes, timeout))
        if not self.read_chunks:
            return b""
        pending = self.read_chunks[0]
        chunk = pending[:max_bytes]
        if len(chunk) == len(pending):
            self.read_chunks.pop(0)
        else:
            self.read_chunks[0] = pending[len(chunk) :]
        return chunk

    def write(
        self,
        handle: int,
        data: bytes,
        *,
        timeout: float | None,
    ) -> int:
        assert handle == 42
        accepted = data[: self.write_limit]
        self.writes.append((accepted, timeout))
        return len(accepted)

    def close_handle(self, handle: int) -> None:
        self.closed.append(handle)


@pytest.mark.parametrize(
    "open_error",
    [FileNotFoundError(), PermissionError()],
    ids=["unavailable", "access-denied"],
)
def test_windows_named_pipe_available_rejects_unreachable(
    monkeypatch: pytest.MonkeyPatch,
    open_error: OSError,
) -> None:
    api = _FakeWindowsPipeAPI(open_error=open_error)
    monkeypatch.setattr(
        windows_named_pipe_module,
        "_new_windows_named_pipe_api",
        lambda: api,
    )

    assert (
        windows_named_pipe_module._windows_named_pipe_available(
            docker_socket_module.WINDOWS_DOCKER_PIPE
        )
        is False
    )
    assert api.opens == [
        (
            docker_socket_module.WINDOWS_DOCKER_PIPE,
            windows_named_pipe_module._WINDOWS_PIPE_PROBE_TIMEOUT_SECONDS,
        )
    ]
    assert api.closed == []


def test_windows_named_pipe_probe_closes_reachable_handle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    api = _FakeWindowsPipeAPI()
    monkeypatch.setattr(
        windows_named_pipe_module,
        "_new_windows_named_pipe_api",
        lambda: api,
    )

    assert (
        windows_named_pipe_module._windows_named_pipe_available(
            docker_socket_module.WINDOWS_DOCKER_PIPE
        )
        is True
    )
    assert api.closed == [42]


def test_windows_named_pipe_open_limits_server_impersonation() -> None:
    kernel32 = MagicMock()
    kernel32.WaitNamedPipeW.return_value = True
    kernel32.CreateFileW.return_value = 42
    kernel32.SetNamedPipeHandleState.return_value = True
    api = object.__new__(windows_named_pipe_module._CtypesWindowsNamedPipeAPI)
    api._kernel32 = kernel32
    api._wintypes = SimpleNamespace(DWORD=ctypes.c_uint32)

    assert api.open_pipe(docker_socket_module.WINDOWS_DOCKER_PIPE, timeout=1) == 42

    flags = kernel32.CreateFileW.call_args.args[5]
    assert flags == (
        windows_named_pipe_module._FILE_FLAG_OVERLAPPED
        | 0x00100000  # SECURITY_SQOS_PRESENT
        | 0x00010000  # SECURITY_IDENTIFICATION
    )


def test_windows_named_pipe_open_rejects_expired_timeout_without_waiting() -> None:
    kernel32 = MagicMock()
    api = object.__new__(windows_named_pipe_module._CtypesWindowsNamedPipeAPI)
    api._kernel32 = kernel32
    api._wintypes = SimpleNamespace(DWORD=ctypes.c_uint32)

    with pytest.raises(TimeoutError, match="named pipe connection timed out"):
        api.open_pipe(docker_socket_module.WINDOWS_DOCKER_PIPE, timeout=0)

    kernel32.WaitNamedPipeW.assert_not_called()


def test_windows_named_pipe_http_get_and_response_close(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = b'[{"Id":"container-1"}]'
    headers = (
        b"HTTP/1.1 200 OK\r\n"
        + f"Content-Length: {len(body)}\r\n".encode()
        + b"Connection: close\r\n\r\n"
    )
    api = _FakeWindowsPipeAPI(
        read_chunks=[headers, body],
        write_limit=7,
    )
    monkeypatch.setattr(
        windows_named_pipe_module,
        "_new_windows_named_pipe_api",
        lambda: api,
    )
    client = DockerSocketClient(
        docker_socket_module.WINDOWS_DOCKER_PIPE,
        request_timeout=1,
    )

    inventory = client.discover_container_ids(deadline=time.monotonic() + 5)

    assert inventory == {
        "container_ids": ["container-1"],
        "truncated": False,
        "malformed": False,
        "output_empty": False,
    }
    request = b"".join(item for item, _timeout in api.writes)
    assert request.startswith(f"GET {_INVENTORY_PATH} HTTP/1.1\r\n".encode())
    assert b"\r\nHost: localhost\r\n" in request
    assert api.opens[0][0] == docker_socket_module.WINDOWS_DOCKER_PIPE
    assert api.opens[0][1] is not None
    assert 0.9 < api.opens[0][1] <= 1
    # ``Connection: close`` closes the socket before the body is consumed;
    # the makefile reference must keep the handle alive until response close.
    assert api.closed == [42]


def test_windows_named_pipe_response_reads_refresh_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": 0.0}
    body = b"[]"
    headers = b"HTTP/1.1 200 OK\r\n" + f"Content-Length: {len(body)}\r\n\r\n".encode()

    class _TimedWindowsPipeAPI(_FakeWindowsPipeAPI):
        def read(
            self,
            handle: int,
            max_bytes: int,
            *,
            timeout: float | None,
        ) -> bytes:
            chunk = super().read(handle, max_bytes, timeout=timeout)
            clock["now"] += 0.4
            return chunk

    api = _TimedWindowsPipeAPI(read_chunks=[headers, body])
    monkeypatch.setattr(docker_socket_module.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(
        windows_named_pipe_module.time,
        "monotonic",
        lambda: clock["now"],
    )
    monkeypatch.setattr(
        windows_named_pipe_module,
        "_new_windows_named_pipe_api",
        lambda: api,
    )
    client = DockerSocketClient(
        docker_socket_module.WINDOWS_DOCKER_PIPE,
        request_timeout=1,
    )

    inventory = client.discover_container_ids(deadline=100)

    assert inventory == {
        "container_ids": [],
        "truncated": False,
        "malformed": False,
        "output_empty": True,
    }
    assert api.reads[0][1] == pytest.approx(1)
    assert api.reads[1][1] == pytest.approx(0.6)
    assert all(
        size <= windows_named_pipe_module._READ_CHUNK_BYTES for size, _ in api.reads
    )
    assert api.closed == [42]


def test_windows_named_pipe_timeout_refresh_replaces_open_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": 0.0}
    api = _FakeWindowsPipeAPI(read_chunks=[b"x"])
    pipe_socket = windows_named_pipe_module._WindowsNamedPipeSocket(
        api,
        42,
        timeout=1,
        deadline=1,
    )
    monkeypatch.setattr(docker_socket_module.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(
        windows_named_pipe_module.time,
        "monotonic",
        lambda: clock["now"],
    )
    client = DockerSocketClient(
        docker_socket_module.WINDOWS_DOCKER_PIPE,
        request_timeout=5,
    )
    opened = SimpleNamespace(connection=SimpleNamespace(sock=pipe_socket))

    clock["now"] = 2
    client._refresh_timeout(opened, deadline=7)

    assert pipe_socket._handle.read(1) == b"x"
    assert api.reads == [(1, pytest.approx(5))]


@pytest.mark.parametrize("split_body", [False, True], ids=["headers", "body"])
def test_windows_named_pipe_slow_drip_cannot_renew_request_deadline(
    monkeypatch: pytest.MonkeyPatch,
    split_body: bool,
) -> None:
    clock = {"now": 0.0}
    body = b"[]" if not split_body else b"0123456789"
    headers = b"HTTP/1.1 200 OK\r\n" + f"Content-Length: {len(body)}\r\n\r\n".encode()
    chunks = [headers, *[bytes([value]) for value in body]]
    if not split_body:
        chunks = [bytes([value]) for value in headers] + [body]

    class _SlowDripWindowsPipeAPI(_FakeWindowsPipeAPI):
        def read(
            self,
            handle: int,
            max_bytes: int,
            *,
            timeout: float | None,
        ) -> bytes:
            chunk = super().read(handle, max_bytes, timeout=timeout)
            clock["now"] += 0.21
            return chunk

    api = _SlowDripWindowsPipeAPI(read_chunks=chunks)
    monkeypatch.setattr(docker_socket_module.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(
        windows_named_pipe_module.time,
        "monotonic",
        lambda: clock["now"],
    )
    monkeypatch.setattr(
        windows_named_pipe_module,
        "_new_windows_named_pipe_api",
        lambda: api,
    )
    client = DockerSocketClient(
        docker_socket_module.WINDOWS_DOCKER_PIPE,
        request_timeout=1,
    )

    assert client.discover_container_ids(deadline=100) is None
    assert len(api.reads) <= 5
    assert [timeout for _size, timeout in api.reads] == sorted(
        (timeout for _size, timeout in api.reads),
        reverse=True,
    )
    assert api.closed == [42]


def test_windows_named_pipe_stuck_cancel_force_closes_with_bounded_waits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    kernel32 = SimpleNamespace(
        CreateEventW=MagicMock(return_value=99),
        ReadFile=MagicMock(return_value=False),
        WriteFile=MagicMock(return_value=False),
        WaitForSingleObject=MagicMock(
            side_effect=[
                windows_named_pipe_module._WAIT_TIMEOUT,
                windows_named_pipe_module._WAIT_TIMEOUT,
                windows_named_pipe_module._WAIT_OBJECT_0,
            ]
        ),
        CancelIoEx=MagicMock(return_value=True),
        GetOverlappedResult=MagicMock(return_value=False),
        CloseHandle=MagicMock(return_value=True),
    )
    api = object.__new__(windows_named_pipe_module._CtypesWindowsNamedPipeAPI)
    api._kernel32 = kernel32
    api._wintypes = SimpleNamespace(DWORD=ctypes.c_uint32)
    api._closed_handles = set()
    api._close_lock = threading.Lock()
    monkeypatch.setattr(
        windows_named_pipe_module,
        "_last_windows_error",
        lambda: windows_named_pipe_module._ERROR_IO_PENDING,
    )

    with pytest.raises(TimeoutError):
        api._transfer(
            42,
            ctypes.create_string_buffer(8),
            8,
            write=False,
            timeout=0.01,
        )

    waits = [call.args[1] for call in kernel32.WaitForSingleObject.call_args_list]
    assert windows_named_pipe_module._INFINITE not in waits
    assert all(
        wait <= windows_named_pipe_module._WINDOWS_CANCEL_WAIT_MS for wait in waits[1:]
    )
    assert kernel32.CancelIoEx.call_count == 1
    assert [call.args[0] for call in kernel32.CloseHandle.call_args_list].count(42) == 1
    assert [call.args[0] for call in kernel32.CloseHandle.call_args_list].count(99) == 1
    api.close_handle(42)
    assert [call.args[0] for call in kernel32.CloseHandle.call_args_list].count(42) == 1


def test_windows_named_pipe_immediate_overlapped_read_gets_byte_count() -> None:
    def complete(
        _handle: int,
        _overlapped: object,
        transferred: object,
        _wait: bool,
    ) -> bool:
        ctypes.cast(
            transferred,
            ctypes.POINTER(ctypes.c_uint32),
        ).contents.value = 5
        return True

    kernel32 = SimpleNamespace(
        CreateEventW=MagicMock(return_value=99),
        ReadFile=MagicMock(return_value=True),
        WriteFile=MagicMock(return_value=True),
        GetOverlappedResult=MagicMock(side_effect=complete),
        CloseHandle=MagicMock(return_value=True),
    )
    api = object.__new__(windows_named_pipe_module._CtypesWindowsNamedPipeAPI)
    api._kernel32 = kernel32
    api._wintypes = SimpleNamespace(DWORD=ctypes.c_uint32)

    transferred = api._transfer(
        42,
        ctypes.create_string_buffer(8),
        8,
        write=False,
        timeout=1,
    )

    assert transferred == 5
    kernel32.GetOverlappedResult.assert_called_once()
