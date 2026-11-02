"""Streaming file transfer over the public exec WebSocket."""

from __future__ import annotations

import asyncio
import base64
import copy
import errno
from contextlib import asynccontextmanager, contextmanager
import json
import os
import posixpath
import queue
import socket
import ssl
import shutil
import tarfile
import tempfile
import threading
import time
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, BinaryIO
from urllib.parse import quote, urlsplit, urlunsplit

from websockets.asyncio.client import connect as async_connect
from websockets.exceptions import ConnectionClosed, InvalidStatus, WebSocketException
from websockets.sync.client import connect as sync_connect

import runta as _public

from .user_agent import USER_AGENT
from .retry import retry_async, retry_sync
from .async_file_io import _AsyncFileIO, finish_worker
from .byte_budget import _ByteBudget
from .tls_resumption import _TLSResumption

_CHUNK_SIZE = 256 * 1024
_MAX_STDERR_BYTES = 1024 * 1024
_TRANSFER_ATTEMPTS = 16


class _WebSocketTLS:
    """One lazily initialized, immutable TLS configuration per SDK client."""

    def __init__(self) -> None:
        self._context: ssl.SSLContext | None = None
        self._lock = threading.Lock()

    def context(self) -> ssl.SSLContext:
        with self._lock:
            if self._context is None:
                self._context = ssl.create_default_context()
            return self._context


class _AsyncWebSocketTLS:
    """Client-owned, system-CA TLS sessions for asynchronous WebSockets."""

    def __init__(self, bind_loop: Callable[[], Any]) -> None:
        self._bind_loop = bind_loop
        self._resumption: _TLSResumption | None = None

    def prepare(self) -> None:
        self._bind_loop()

    def context(self, hostname: str, port: int) -> ssl.SSLContext:
        self.prepare()
        if self._resumption is None:
            self._resumption = _TLSResumption(ssl.create_default_context)
        return self._resumption.context(hostname, port)

    def close(self) -> None:
        if self._resumption is not None:
            self._resumption.close()


class _TransferInterrupted(_public.ApiError):
    """The transport ended before a transfer exit frame arrived."""


def _retryable_transfer_error(error: Exception) -> bool:
    if isinstance(error, _TransferInterrupted):
        return True
    if isinstance(error, InvalidStatus):
        return error.response.status_code in {408, 429, 502, 503, 504}
    if isinstance(error, ConnectionClosed):
        code = error.rcvd.code if error.rcvd is not None else None
        return code in {None, 1000, 1001, 1005, 1006, 1011, 1012, 1013}
    if isinstance(error, socket.gaierror):
        return error.errno == socket.EAI_AGAIN
    if isinstance(error, OSError):
        return isinstance(error, (ConnectionError, TimeoutError)) or error.errno in {
            errno.ECONNABORTED,
            errno.ECONNREFUSED,
            errno.ECONNRESET,
            errno.ENETDOWN,
            errno.ENETRESET,
            errno.ENETUNREACH,
            errno.EHOSTUNREACH,
            errno.EPIPE,
            errno.ETIMEDOUT,
        }
    return False


_UPLOAD_FILE_SCRIPT = r"""
set -eu
dst=$1
mode=$2
expected_size=$3
parent=$(dirname "$dst")
base=$(basename "$dst")
mkdir -p "$parent"
tmp="$parent/.${base}.runta-upload-$$"
cleanup() { rm -f "$tmp"; }
trap cleanup EXIT HUP INT TERM
cat > "$tmp"
actual_size=$(wc -c < "$tmp")
if [ "$actual_size" -ne "$expected_size" ]; then
  echo "upload size mismatch: expected $expected_size bytes, received $actual_size" >&2
  exit 3
fi
chmod "$mode" "$tmp"
mv -f "$tmp" "$dst"
trap - EXIT HUP INT TERM
"""

_UPLOAD_DIRECTORY_SCRIPT = r"""
set -eu
dst=$1
parent=$(dirname "$dst")
base=$(basename "$dst")
mkdir -p "$parent"
stage="$parent/.${base}.runta-stage-$$"
backup="$parent/.${base}.runta-backup-$$"
cleanup() {
  rm -rf "$stage"
  if [ -e "$backup" ] && [ ! -e "$dst" ]; then mv "$backup" "$dst"; fi
  rm -rf "$backup"
}
trap cleanup EXIT HUP INT TERM
mkdir "$stage"
if [ -d "$dst" ]; then
  cp -a "$dst"/. "$stage"/
elif [ -e "$dst" ]; then
  echo "destination exists and is not a directory: $dst" >&2
  exit 2
fi
status=0
tar xf - -C "$stage" || status=$?
# tar may stop at the archive trailer before stdin reaches EOF. Keep the
# connection alive until close_stdin, and drain any remaining archive padding.
cat > /dev/null
[ "$status" -eq 0 ] || exit "$status"
if [ -e "$dst" ]; then mv "$dst" "$backup"; fi
mv "$stage" "$dst"
rm -rf "$backup"
trap - EXIT HUP INT TERM
"""


# Path bytes arrive as octal escapes, one ASCII line per path. No supplied
# filename is parsed as shell syntax or as a tar option.
_DOWNLOAD_SELECTION_SCRIPT = r"""
set -eu
umask 077
manifest=$(mktemp /tmp/runta-download-paths.XXXXXX)
trap 'rm -f -- "$manifest"' 0
trap 'exit 1' HUP INT TERM
CDPATH= cd -P -- "$1"
printf '.\0' > "$manifest"
while IFS= read -r encoded; do
    # The sentinel preserves trailing newlines through command substitution.
    path=$(printf '%b_' "$encoded")
    path=${path%_}
    rest=$path
    prefix=.
    while [ "${rest#*/}" != "$rest" ]; do
        part=${rest%%/*}
        rest=${rest#*/}
        prefix=$prefix/$part
        if [ -L "$prefix" ]; then
            echo 'selected path traverses a symbolic link' >&2
            exit 2
        fi
    done
    if [ -L "./$path" ]; then continue; fi
    if [ ! -e "./$path" ]; then
        echo 'selected path does not exist' >&2
        exit 2
    fi
    printf './%s\0' "$path" >> "$manifest"
done
unset TAR_OPTIONS
tar cf - --no-recursion --null --verbatim-files-from --files-from "$manifest"
"""


def _normalize_download_paths(paths: Sequence[str] | None) -> tuple[str, ...] | None:
    if paths is None:
        return None
    if isinstance(paths, (str, bytes)) or not isinstance(paths, Sequence):
        raise TypeError("paths must be a sequence of relative path strings")
    result: dict[str, None] = {}
    for path in paths:
        if not isinstance(path, str):
            raise TypeError("paths must contain only strings")
        try:
            _safe_relative_name(path)
            normalized = str(PurePosixPath(path))
            if normalized == ".":
                raise ValueError("paths cannot select the source root")
            normalized.encode("utf-8")
        except (tarfile.FilterError, UnicodeError) as error:
            raise ValueError("paths contains an unsafe relative path") from error
        result[normalized] = None
    return tuple(result)


def _selection_stdin(paths: tuple[str, ...]) -> Iterator[bytes]:
    for path in paths:
        encoded = (
            "".join(f"\\0{byte:03o}" for byte in path.encode("utf-8")) + "\n"
        ).encode("ascii")
        for offset in range(0, len(encoded), _CHUNK_SIZE):
            yield encoded[offset : offset + _CHUNK_SIZE]


def upload_path(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: Path,
    dst: str,
    *,
    timeout: float,
    attempts: int = _TRANSFER_ATTEMPTS,
    _tls: _WebSocketTLS | None = None,
) -> None:
    """Stream a local file or directory into a runtime."""
    if src.is_file():
        target = f"{dst.rstrip('/')}/{src.name}" if dst.endswith("/") else dst
        mode = format(src.stat().st_mode & 0o777, "03o")
        _retry_sync(
            lambda: _sync_upload_file(
                endpoint,
                token,
                runtime_id,
                src,
                target,
                mode,
                src.stat().st_size,
                timeout,
                _tls=_tls,
            ),
            attempts=attempts,
        )
        return
    if src.is_dir():
        _retry_sync(
            lambda: _sync_upload_directory(
                endpoint, token, runtime_id, src, dst, timeout, _tls=_tls
            ),
            attempts=attempts,
        )
        return
    raise FileNotFoundError(src)


async def async_upload_path(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: Path,
    dst: str,
    *,
    timeout: float,
    attempts: int = _TRANSFER_ATTEMPTS,
    _tls: _WebSocketTLS | _AsyncWebSocketTLS | None = None,
) -> None:
    """Asynchronously stream a local file or directory into a runtime."""
    if src.is_file():
        target = f"{dst.rstrip('/')}/{src.name}" if dst.endswith("/") else dst
        mode = format(src.stat().st_mode & 0o777, "03o")
        await _retry_async(
            lambda: _async_upload_file(
                endpoint,
                token,
                runtime_id,
                src,
                target,
                mode,
                src.stat().st_size,
                timeout,
                _tls=_tls,
            ),
            attempts=attempts,
        )
        return
    if src.is_dir():
        await _retry_async(
            lambda: _async_upload_directory(
                endpoint, token, runtime_id, src, dst, timeout, _tls=_tls
            ),
            attempts=attempts,
        )
        return
    raise FileNotFoundError(src)


def download_path(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: str,
    dst: Path,
    *,
    destination_is_directory: bool,
    timeout: float,
    attempts: int = _TRANSFER_ATTEMPTS,
    _tls: _WebSocketTLS | None = None,
) -> None:
    """Stream a runtime file or directory into a local destination."""
    with tempfile.TemporaryDirectory(prefix="runta-download-") as temp:
        archive = Path(temp) / "payload.tar"
        _retry_sync(
            lambda: _sync_download_archive(
                endpoint, token, runtime_id, src, archive, timeout, _tls=_tls
            ),
            attempts=attempts,
        )
        _extract_and_commit(
            archive,
            src,
            dst,
            destination_is_directory=destination_is_directory,
            workspace=Path(temp),
        )


@asynccontextmanager
async def _async_download_workspace(pool: _AsyncFileIO):
    workspace: tempfile.TemporaryDirectory | None = None

    def create() -> None:
        nonlocal workspace
        workspace = tempfile.TemporaryDirectory(prefix="runta-download-")

    try:
        await pool.run(create)
        yield Path(workspace.name)
    finally:
        if workspace is not None:
            # Shield admission too: repeated cancellation must not skip cleanup
            # while other downloads occupy every file-worker slot.
            await finish_worker(asyncio.create_task(pool.run(workspace.cleanup)))


async def async_download_path(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: str,
    dst: Path,
    *,
    destination_is_directory: bool,
    timeout: float,
    attempts: int = _TRANSFER_ATTEMPTS,
    _tls: _WebSocketTLS | _AsyncWebSocketTLS | None = None,
    _file_io: _AsyncFileIO | None = None,
) -> None:
    """Asynchronously stream a runtime path into a local destination."""
    owned_pool = _file_io is None
    pool = _file_io or _AsyncFileIO(None, asyncio.get_running_loop)
    try:
        with pool.lease():
            async with _async_download_workspace(pool) as temp:
                archive = Path(temp) / "payload.tar"
                await _retry_async(
                    lambda: _async_download_archive(
                        endpoint,
                        token,
                        runtime_id,
                        src,
                        archive,
                        timeout,
                        _tls=_tls,
                        _file_io=pool,
                    ),
                    attempts=attempts,
                )
                extraction = asyncio.create_task(
                    asyncio.to_thread(
                        _extract_and_commit,
                        archive,
                        src,
                        dst,
                        destination_is_directory=destination_is_directory,
                        workspace=Path(temp),
                    )
                )
                await finish_worker(extraction)
    finally:
        if owned_pool:
            pool.close()


def download_dir_contents(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: str,
    dst: Path,
    *,
    paths: Sequence[str] | None = None,
    filter: Callable[[tarfile.TarInfo, str], tarfile.TarInfo | None] | None = None,
    timeout: float,
    attempts: int = _TRANSFER_ATTEMPTS,
    _tls: _WebSocketTLS | None = None,
) -> None:
    """Download one seekable archive and merge its directory contents."""
    paths = _normalize_download_paths(paths)
    if paths == ():
        return
    with tempfile.TemporaryDirectory(prefix="runta-download-") as temp:
        archive = Path(temp) / "payload.tar"
        _retry_sync(
            lambda: _sync_download_archive(
                endpoint,
                token,
                runtime_id,
                src,
                archive,
                timeout,
                _tls=_tls,
                directory_contents=True,
                paths=paths,
            ),
            attempts=attempts,
        )
        _extract_dir_contents(archive, dst, filter, paths)


async def async_download_dir_contents(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: str,
    dst: Path,
    *,
    paths: Sequence[str] | None = None,
    filter: Callable[[tarfile.TarInfo, str], tarfile.TarInfo | None] | None = None,
    timeout: float,
    attempts: int = _TRANSFER_ATTEMPTS,
    _tls: _WebSocketTLS | _AsyncWebSocketTLS | None = None,
    _file_io: _AsyncFileIO | None = None,
) -> None:
    """Merge on the client's bounded, cancellation-safe file workers."""
    paths = _normalize_download_paths(paths)
    if paths == ():
        return
    owned_pool = _file_io is None
    pool = _file_io or _AsyncFileIO(None, asyncio.get_running_loop)
    try:
        with pool.lease():
            async with _async_download_workspace(pool) as temp:
                archive = temp / "payload.tar"
                await _retry_async(
                    lambda: _async_download_archive(
                        endpoint,
                        token,
                        runtime_id,
                        src,
                        archive,
                        timeout,
                        _tls=_tls,
                        _file_io=pool,
                        directory_contents=True,
                        paths=paths,
                    ),
                    attempts=attempts,
                )
                await pool.run(_extract_dir_contents, archive, dst, filter, paths)
    finally:
        if owned_pool:
            pool.close()


def execute(
    endpoint: str,
    token: str,
    runtime_id: str,
    command: str,
    args: list[str],
    *,
    env: dict[str, str] | None,
    stdin: bytes | str | None,
    timeout: float | None,
    max_output_bytes: int | None,
    connect_timeout: float,
    idle_timeout: float | None = None,
    _tls: _WebSocketTLS | None = None,
) -> _public.CommandResult:
    """Execute a command over the public streaming WebSocket."""
    started = time.monotonic()
    stdout = bytearray()
    stderr = bytearray()
    stdout_truncated = False
    stderr_truncated = False
    output_limit = max_output_bytes if max_output_bytes is not None else 4 * 1024 * 1024
    deadline = time.monotonic() + timeout if timeout is not None else None

    with _sync_socket(
        endpoint, token, runtime_id, connect_timeout, _tls=_tls
    ) as socket:
        _send_start(socket.send, command, args, env=env)
        if stdin is not None:
            data = stdin if isinstance(stdin, bytes) else stdin.encode()
            for offset in range(0, len(data), _CHUNK_SIZE):
                _send_stdin(socket.send, data[offset : offset + _CHUNK_SIZE])
        _send_close_stdin(socket.send)
        idle_deadline = (
            time.monotonic() + idle_timeout if idle_timeout is not None else None
        )

        while True:
            try:
                deadlines = [
                    value for value in (deadline, idle_deadline) if value is not None
                ]
                if not deadlines:
                    raw = socket.recv()
                else:
                    remaining = min(deadlines) - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError
                    raw = socket.recv(timeout=remaining)
            except TimeoutError:
                _send_signal_best_effort(socket.send, "TERM")
                if idle_deadline is not None and (
                    deadline is None or idle_deadline < deadline
                ):
                    raise _TransferInterrupted("streaming exec stopped making progress")
                exit_code = 124
                message = f"Command timed out after {timeout} seconds.".encode()
                stderr_truncated |= _append_output_capped(stderr, message, output_limit)
                break
            except WebSocketException as exc:
                if _retryable_transfer_error(exc):
                    raise _TransferInterrupted(
                        "streaming exec disconnected before exit"
                    ) from exc
                raise _public.ApiError(
                    f"streaming exec disconnected before exit: {exc}"
                ) from exc
            if raw is None:
                raise _TransferInterrupted("streaming exec disconnected before exit")
            frame = _parse_frame(raw)
            kind = frame.get("type")
            if kind == "stdout":
                stdout_truncated |= _append_output_capped(
                    stdout, _decode_frame_data(frame), output_limit
                )
                if idle_timeout is not None and _decode_frame_data(frame):
                    idle_deadline = time.monotonic() + idle_timeout
            elif kind == "stderr":
                stderr_truncated |= _append_output_capped(
                    stderr, _decode_frame_data(frame), output_limit
                )
                if idle_timeout is not None and _decode_frame_data(frame):
                    idle_deadline = time.monotonic() + idle_timeout
            elif kind == "exit":
                exit_code = int(frame["code"])
                break
            elif kind == "error":
                raise _public.ApiError(
                    str(frame.get("message", "streaming exec failed"))
                )
            elif kind == "heartbeat":
                socket.send('{"type":"heartbeat"}')

    return _public.CommandResult(
        exit_code=exit_code,
        stdout=bytes(stdout),
        stderr=bytes(stderr),
        duration=time.monotonic() - started,
        stdout_truncated=stdout_truncated,
        stderr_truncated=stderr_truncated,
    )


async def async_execute(
    endpoint: str,
    token: str,
    runtime_id: str,
    command: str,
    args: list[str],
    *,
    env: dict[str, str] | None,
    stdin: bytes | str | None,
    timeout: float | None,
    max_output_bytes: int | None,
    connect_timeout: float,
    idle_timeout: float | None = None,
    _tls: _WebSocketTLS | _AsyncWebSocketTLS | None = None,
) -> _public.CommandResult:
    """Execute a command over the public streaming WebSocket."""
    started = time.monotonic()
    stdout = bytearray()
    stderr = bytearray()
    stdout_truncated = False
    stderr_truncated = False
    output_limit = max_output_bytes if max_output_bytes is not None else 4 * 1024 * 1024

    send_budget = _ByteBudget()
    async with _async_socket(
        endpoint, token, runtime_id, connect_timeout, _tls=_tls
    ) as socket:
        await _async_send_start(socket.send, command, args, env=env)
        if stdin is not None:
            data = stdin if isinstance(stdin, bytes) else stdin.encode()
            for offset in range(0, len(data), _CHUNK_SIZE):
                chunk = data[offset : offset + _CHUNK_SIZE]
                await _async_send_stdin(socket.send, chunk)
                await send_budget.processed(len(chunk))
        await _async_send_close_stdin(socket.send)

        async def receive() -> int:
            nonlocal stdout_truncated, stderr_truncated
            receive_budget = _ByteBudget()
            idle_deadline = (
                time.monotonic() + idle_timeout if idle_timeout is not None else None
            )
            while True:
                if idle_deadline is None:
                    raw = await socket.recv()
                else:
                    try:
                        remaining = idle_deadline - time.monotonic()
                        if remaining <= 0:
                            raise asyncio.TimeoutError
                        raw = await asyncio.wait_for(socket.recv(), timeout=remaining)
                    except (TimeoutError, asyncio.TimeoutError) as exc:
                        await _async_send_signal_best_effort(socket.send, "TERM")
                        raise _TransferInterrupted(
                            "streaming exec stopped making progress"
                        ) from exc
                if raw is None:
                    raise _TransferInterrupted(
                        "streaming exec disconnected before exit"
                    )
                frame = _parse_frame(raw)
                kind = frame.get("type")
                if kind == "stdout":
                    data = _decode_frame_data(frame)
                    stdout_truncated |= _append_output_capped(
                        stdout, data, output_limit
                    )
                    if idle_timeout is not None and data:
                        idle_deadline = time.monotonic() + idle_timeout
                    await receive_budget.processed(len(data))
                elif kind == "stderr":
                    data = _decode_frame_data(frame)
                    stderr_truncated |= _append_output_capped(
                        stderr, data, output_limit
                    )
                    if idle_timeout is not None and data:
                        idle_deadline = time.monotonic() + idle_timeout
                    await receive_budget.processed(len(data))
                elif kind == "exit":
                    return int(frame["code"])
                elif kind == "error":
                    raise _public.ApiError(
                        str(frame.get("message", "streaming exec failed"))
                    )
                elif kind == "heartbeat":
                    await socket.send('{"type":"heartbeat"}')

        try:
            if timeout is None:
                exit_code = await receive()
            else:
                exit_code = await asyncio.wait_for(receive(), timeout=timeout)
        except (TimeoutError, asyncio.TimeoutError):
            await _async_send_signal_best_effort(socket.send, "TERM")
            exit_code = 124
            message = f"Command timed out after {timeout} seconds.".encode()
            stderr_truncated |= _append_output_capped(stderr, message, output_limit)
        except asyncio.CancelledError:
            await _async_send_signal_best_effort(socket.send, "TERM")
            raise

    return _public.CommandResult(
        exit_code=exit_code,
        stdout=bytes(stdout),
        stderr=bytes(stderr),
        duration=time.monotonic() - started,
        stdout_truncated=stdout_truncated,
        stderr_truncated=stderr_truncated,
    )


def _sync_upload_file(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: Path,
    dst: str,
    mode: str,
    expected_size: int,
    timeout: float,
    *,
    _tls: _WebSocketTLS | None = None,
) -> None:
    with _sync_socket(endpoint, token, runtime_id, timeout, _tls=_tls) as socket:
        _send_start(
            socket.send,
            "sh",
            ["-c", _UPLOAD_FILE_SCRIPT, "_", dst, mode, str(expected_size)],
        )
        with src.open("rb") as handle:
            for chunk in iter(lambda: handle.read(_CHUNK_SIZE), b""):
                _send_stdin(socket.send, chunk)
        _send_close_stdin(socket.send)
        _receive_completion(socket.recv)


async def _async_upload_file(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: Path,
    dst: str,
    mode: str,
    expected_size: int,
    timeout: float,
    *,
    _tls: _WebSocketTLS | _AsyncWebSocketTLS | None = None,
) -> None:
    send_budget = _ByteBudget()
    async with _async_socket(endpoint, token, runtime_id, timeout, _tls=_tls) as socket:
        await _async_send_start(
            socket.send,
            "sh",
            ["-c", _UPLOAD_FILE_SCRIPT, "_", dst, mode, str(expected_size)],
        )
        with src.open("rb") as handle:
            while chunk := await finish_worker(
                asyncio.create_task(asyncio.to_thread(handle.read, _CHUNK_SIZE))
            ):
                await _async_send_stdin(socket.send, chunk)
                await send_budget.processed(len(chunk))
        await _async_send_close_stdin(socket.send)
        await _async_receive_completion(socket.recv)


def _sync_upload_directory(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: Path,
    dst: str,
    timeout: float,
    *,
    _tls: _WebSocketTLS | None = None,
) -> None:
    with _sync_socket(endpoint, token, runtime_id, timeout, _tls=_tls) as socket:
        _send_start(socket.send, "sh", ["-c", _UPLOAD_DIRECTORY_SCRIPT, "_", dst])
        writer = _SyncSocketWriter(socket.send)
        with tarfile.open(fileobj=writer, mode="w|") as archive:
            archive.add(src, arcname=".", recursive=True)
        _send_close_stdin(socket.send)
        _receive_completion(socket.recv)


async def _async_upload_directory(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: Path,
    dst: str,
    timeout: float,
    *,
    _tls: _WebSocketTLS | _AsyncWebSocketTLS | None = None,
) -> None:
    send_budget = _ByteBudget()
    async with _async_socket(endpoint, token, runtime_id, timeout, _tls=_tls) as socket:
        await _async_send_start(
            socket.send, "sh", ["-c", _UPLOAD_DIRECTORY_SCRIPT, "_", dst]
        )
        chunks: queue.Queue[bytes | BaseException | None] = queue.Queue(maxsize=8)
        stopped = threading.Event()
        available = asyncio.Event()
        loop = asyncio.get_running_loop()

        def notify() -> None:
            loop.call_soon_threadsafe(available.set)

        def produce() -> None:
            try:
                with tarfile.open(
                    fileobj=_QueueWriter(chunks, stopped, notify), mode="w|"
                ) as archive:
                    archive.add(src, arcname=".", recursive=True)
            except BaseException as exc:
                _queue_put(chunks, exc, stopped, notify)
            finally:
                _queue_put(chunks, None, stopped, notify)

        producer = asyncio.create_task(asyncio.to_thread(produce))
        try:
            while True:
                # Never occupy an executor thread waiting for another executor
                # job to produce data. Clearing before checking the queue also
                # avoids losing a notification between the check and the wait.
                available.clear()
                try:
                    item = chunks.get_nowait()
                except queue.Empty:
                    await available.wait()
                    continue
                if item is None:
                    break
                if isinstance(item, BaseException):
                    raise item
                await _async_send_stdin(socket.send, item)
                await send_budget.processed(len(item))
            await finish_worker(producer)
            await _async_send_close_stdin(socket.send)
            await _async_receive_completion(socket.recv)
        finally:
            stopped.set()
            if not producer.done():
                await finish_worker(producer)


def _sync_download_archive(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: str,
    archive: Path,
    timeout: float,
    *,
    _tls: _WebSocketTLS | None = None,
    directory_contents: bool = False,
    paths: tuple[str, ...] | None = None,
) -> None:
    command, args = _download_archive_command(src, directory_contents, paths=paths)
    with _sync_socket(endpoint, token, runtime_id, timeout, _tls=_tls) as socket:
        _send_start(socket.send, command, args)
        if paths is not None:
            for chunk in _selection_stdin(paths):
                _send_stdin(socket.send, chunk)
        _send_close_stdin(socket.send)
        with archive.open("wb") as handle:
            _receive_completion(socket.recv, stdout=handle)


async def _async_download_archive(
    endpoint: str,
    token: str,
    runtime_id: str,
    src: str,
    archive: Path,
    timeout: float,
    *,
    _tls: _WebSocketTLS | _AsyncWebSocketTLS | None = None,
    _file_io: _AsyncFileIO,
    directory_contents: bool = False,
    paths: tuple[str, ...] | None = None,
) -> None:
    command, args = _download_archive_command(src, directory_contents, paths=paths)
    async with _async_socket(endpoint, token, runtime_id, timeout, _tls=_tls) as socket:
        await _async_send_start(socket.send, command, args)
        if paths is not None:
            for chunk in _selection_stdin(paths):
                await _async_send_stdin(socket.send, chunk)
        await _async_send_close_stdin(socket.send)
        writer = _AsyncDownloadWriter(_file_io, archive)
        try:
            await writer.open()
            await _async_receive_completion(socket.recv, stdout=writer)
        finally:
            await writer.close()


def _sync_socket(
    endpoint: str,
    token: str,
    runtime_id: str,
    timeout: float,
    *,
    _tls: _WebSocketTLS | None = None,
):
    url = _stream_url(endpoint, runtime_id)
    options = (
        {"ssl": _tls.context()} if url.startswith("wss:") and _tls is not None else {}
    )
    return sync_connect(
        url,
        additional_headers={"Authorization": f"Bearer {token}"},
        user_agent_header=USER_AGENT,
        open_timeout=timeout,
        close_timeout=timeout,
        max_size=None,
        **options,
    )


def _async_socket(
    endpoint: str,
    token: str,
    runtime_id: str,
    timeout: float,
    *,
    _tls: _WebSocketTLS | _AsyncWebSocketTLS | None = None,
):
    url = _stream_url(endpoint, runtime_id)
    options = {}
    if isinstance(_tls, _AsyncWebSocketTLS):
        _tls.prepare()
        if url.startswith("wss:"):
            parsed = urlsplit(url)
            options["ssl"] = _tls.context(parsed.hostname, parsed.port or 443)
    elif url.startswith("wss:") and _tls is not None:
        options["ssl"] = _tls.context()
    return async_connect(
        url,
        additional_headers={"Authorization": f"Bearer {token}"},
        user_agent_header=USER_AGENT,
        open_timeout=timeout,
        close_timeout=timeout,
        max_size=None,
        **options,
    )


def _stream_url(endpoint: str, runtime_id: str) -> str:
    parsed = urlsplit(endpoint.rstrip("/"))
    scheme = {"http": "ws", "https": "wss"}.get(parsed.scheme)
    if scheme is None:
        raise _public.ConfigError(f"unsupported endpoint scheme: {parsed.scheme}")
    base_path = parsed.path.rstrip("/")
    path = f"{base_path}/v2/runtimes/{quote(runtime_id, safe='')}/exec/stream"
    return urlunsplit((scheme, parsed.netloc, path, "", ""))


def _send_start(
    send: Callable[[str], Any],
    command: str,
    args: list[str],
    *,
    env: dict[str, str] | None = None,
) -> None:
    send(
        json.dumps(
            {
                "type": "start",
                "command": command,
                "args": args,
                "env": env or {},
                "tty": False,
            }
        )
    )


async def _async_send_start(
    send: Callable[[str], Any],
    command: str,
    args: list[str],
    *,
    env: dict[str, str] | None = None,
) -> None:
    await send(
        json.dumps(
            {
                "type": "start",
                "command": command,
                "args": args,
                "env": env or {},
                "tty": False,
            }
        )
    )


def _send_stdin(send: Callable[[str], Any], data: bytes) -> None:
    send(
        json.dumps(
            {"type": "stdin", "data_base64": base64.b64encode(data).decode("ascii")}
        )
    )


async def _async_send_stdin(send: Callable[[str], Any], data: bytes) -> None:
    await send(
        json.dumps(
            {"type": "stdin", "data_base64": base64.b64encode(data).decode("ascii")}
        )
    )


def _send_close_stdin(send: Callable[[str], Any]) -> None:
    send('{"type":"close_stdin"}')


async def _async_send_close_stdin(send: Callable[[str], Any]) -> None:
    await send('{"type":"close_stdin"}')


async def _async_send_signal(send: Callable[[str], Any], signal: str) -> None:
    await send(json.dumps({"type": "signal", "signal": signal}))


async def _async_send_signal_best_effort(
    send: Callable[[str], Any], signal: str
) -> None:
    try:
        await _async_send_signal(send, signal)
    except (OSError, WebSocketException):
        # The command deadline or caller cancellation remains authoritative even
        # if the peer disconnects before it can receive the termination signal.
        pass


def _send_signal_best_effort(send: Callable[[str], Any], signal: str) -> None:
    try:
        send(json.dumps({"type": "signal", "signal": signal}))
    except (OSError, WebSocketException):
        pass


def _receive_completion(
    recv: Callable[[], Any], stdout: BinaryIO | None = None
) -> None:
    stderr = bytearray()
    exit_code: int | None = None
    while True:
        try:
            raw = recv()
        except ConnectionClosed as exc:
            if exit_code is not None:
                break
            if not _retryable_transfer_error(exc):
                raise _public.ApiError(f"streaming transfer closed: {exc}") from exc
            raise _TransferInterrupted(
                f"streaming transfer disconnected: {exc}"
            ) from exc
        if raw is None:
            if exit_code is None:
                raise _TransferInterrupted(
                    "streaming transfer disconnected before exit"
                )
            break
        frame = _parse_frame(raw)
        kind = frame.get("type")
        if kind == "stdout" and stdout is not None:
            stdout.write(_decode_frame_data(frame))
        elif kind == "stderr":
            _append_capped(stderr, _decode_frame_data(frame))
        elif kind == "exit":
            exit_code = int(frame["code"])
        elif kind == "error":
            raise _public.ApiError(
                str(frame.get("message", "streaming transfer failed"))
            )
    _ensure_success(exit_code, stderr)


class _AsyncDownloadWriter:
    def __init__(self, pool: _AsyncFileIO, path: Path) -> None:
        self._pool = pool
        self._path = path
        self._handle: BinaryIO | None = None

    def _open(self) -> None:
        self._handle = self._path.open("wb")

    async def open(self) -> None:
        await self._pool.run(self._open)

    def _write(self, frame: dict[str, Any]) -> int:
        data = _decode_frame_data(frame)
        self._handle.write(data)
        return len(data)

    async def write_frame(self, frame: dict[str, Any]) -> int:
        return await self._pool.run(self._write, frame)

    def _close(self) -> None:
        if self._handle is not None:
            try:
                self._handle.flush()
            finally:
                self._handle.close()

    async def close(self) -> None:
        await finish_worker(asyncio.create_task(self._pool.run(self._close)))


async def _async_receive_completion(
    recv: Callable[[], Any], stdout: _AsyncDownloadWriter | None = None
) -> None:
    budget = _ByteBudget()
    stderr = bytearray()
    exit_code: int | None = None
    while True:
        try:
            raw = await recv()
        except ConnectionClosed as exc:
            if exit_code is not None:
                break
            if not _retryable_transfer_error(exc):
                raise _public.ApiError(f"streaming transfer closed: {exc}") from exc
            raise _TransferInterrupted(
                f"streaming transfer disconnected: {exc}"
            ) from exc
        if raw is None:
            if exit_code is None:
                raise _TransferInterrupted(
                    "streaming transfer disconnected before exit"
                )
            break
        frame = _parse_frame(raw)
        kind = frame.get("type")
        if kind == "stdout" and stdout is not None:
            await budget.processed(await stdout.write_frame(frame))
        elif kind == "stderr":
            data = _decode_frame_data(frame)
            _append_capped(stderr, data)
            await budget.processed(len(data))
        elif kind == "exit":
            exit_code = int(frame["code"])
        elif kind == "error":
            raise _public.ApiError(
                str(frame.get("message", "streaming transfer failed"))
            )
    _ensure_success(exit_code, stderr)


def _parse_frame(raw: str | bytes) -> dict[str, Any]:
    if isinstance(raw, bytes):
        raw = raw.decode()
    try:
        frame = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _public.ApiError("invalid streaming transfer frame") from exc
    if not isinstance(frame, dict):
        raise _public.ApiError("invalid streaming transfer frame")
    return frame


def _decode_frame_data(frame: dict[str, Any]) -> bytes:
    try:
        return base64.b64decode(str(frame["data_base64"]), validate=True)
    except (KeyError, ValueError) as exc:
        raise _public.ApiError("invalid streaming transfer data frame") from exc


def _ensure_success(exit_code: int | None, stderr: bytearray) -> None:
    if exit_code == 0:
        return
    message = stderr.decode(errors="replace").strip() or "streaming transfer failed"
    raise _public.CommandError(message, exit_code=exit_code)


def _append_capped(target: bytearray, data: bytes) -> None:
    remaining = _MAX_STDERR_BYTES - len(target)
    if remaining > 0:
        target.extend(data[:remaining])


def _append_output_capped(target: bytearray, data: bytes, limit: int) -> bool:
    remaining = max(0, limit - len(target))
    target.extend(data[:remaining])
    return len(data) > remaining


def _retry_sync(
    operation: Callable[[], None], *, attempts: int = _TRANSFER_ATTEMPTS
) -> None:
    retry_sync(
        lambda _remaining: operation(),
        name="file transfer",
        attempts=attempts,
        retryable=_retryable_transfer_error,
    )


async def _retry_async(
    operation: Callable[[], Any], *, attempts: int = _TRANSFER_ATTEMPTS
) -> None:
    await retry_async(
        lambda _remaining: operation(),
        name="file transfer",
        attempts=attempts,
        retryable=_retryable_transfer_error,
    )


def _download_archive_command(
    src: str, directory_contents: bool, *, paths: tuple[str, ...] | None = None
) -> tuple[str, list[str]]:
    if directory_contents and paths is not None:
        return "sh", ["-c", _DOWNLOAD_SELECTION_SCRIPT, "_", src]
    if directory_contents:
        # cd follows only the source directory link; tar preserves nested links.
        # Positional arguments preserve arbitrary names without shell interpolation.
        return "sh", [
            "-c",
            'set -eu; CDPATH= cd -P -- "$1"; exec tar cf - .',
            "_",
            src,
        ]
    parent, name = _remote_parent_and_name(src)
    return "tar", ["cf", "-", "-C", parent, name]


def _safe_relative_name(name: str) -> None:
    # Archive names are POSIX paths even on Windows. Reject Windows aliases too,
    # so drive paths, separators and alternate data streams cannot bypass checks.
    if (
        not name
        or "\\" in name
        or ":" in name
        or "\x00" in name
        or PurePosixPath(name).is_absolute()
        or PureWindowsPath(name).drive
        or ".." in PurePosixPath(name).parts
    ):
        raise tarfile.FilterError("download archive contains an unsafe path")


@contextmanager
def _preserve_link_destination(targetpath: str):
    """Keep an existing entry when link creation/fallback produces no output."""
    target = Path(targetpath)
    if not os.path.lexists(target):
        yield
        return
    if target.is_dir():
        raise FileExistsError(
            f"download member conflicts with destination type: {target}"
        )
    # Move the entry, never copy its contents. The backup remains on the same
    # filesystem, and is restored before a skipped/failed link returns to tarfile.
    with tempfile.TemporaryDirectory(prefix=".runta-link-", dir=target.parent) as temp:
        original = Path(temp) / "original"
        os.replace(target, original)
        try:
            yield
        except BaseException:
            if not os.path.lexists(target):
                os.replace(original, target)
            raise
        if not os.path.lexists(target):
            os.replace(original, target)
            # Avoid tarfile applying hard-link attributes to the restored file
            # after a referent was excluded by the filter.
            raise tarfile.ExtractError("link fallback was skipped")


class _DirectoryMergeTarFile(tarfile.TarFile):
    """Replace file entries without writing through existing destination aliases."""

    merge_filter: Callable[[tarfile.TarInfo, str], tarfile.TarInfo | None]
    merge_root: str

    def makelink_with_filter(
        self,
        tarinfo: tarfile.TarInfo,
        targetpath: str,
        filter_function=None,
        extraction_root=None,
    ) -> None:
        if tarinfo.issym():
            # Windows symlink targets need native separators when stored in the
            # reparse point; archive references remain in POSIX form elsewhere.
            tarinfo = tarinfo.replace(
                linkname=os.path.normpath(tarinfo.linkname), deep=False
            )
        # Backports with this method differ: some filter the referent only,
        # while others also check its metadata at the copy destination.
        # Enforce both checks independently of the native implementation.
        filter_function = (
            self.merge_filter if filter_function is None else filter_function
        )
        extraction_root = (
            self.merge_root if extraction_root is None else extraction_root
        )
        actual_name = os.path.relpath(targetpath, extraction_root).replace(os.sep, "/")

        def guarded_filter(member, destination):
            filtered = filter_function(member, destination)
            if filtered is not None:
                _filter_contents_member(
                    filtered.replace(name=actual_name, deep=False),
                    destination,
                )
            return filtered

        with _preserve_link_destination(targetpath):
            super().makelink_with_filter(
                tarinfo,
                targetpath,
                guarded_filter,
                extraction_root,
            )

    def makefile(self, tarinfo: tarfile.TarInfo, targetpath: str) -> None:
        # Do this at the actual write path, after filtering. A filter can also
        # run for a link fallback's referent, whose path must remain untouched.
        target = Path(targetpath)
        if target.is_dir():
            raise FileExistsError(
                f"download member conflicts with destination type: {target}"
            )
        target.unlink(missing_ok=True)
        super().makefile(tarinfo, targetpath)


class _LegacyDirectoryMergeTarFile(_DirectoryMergeTarFile):
    """Supply filtered link fallback when the interpreter does not provide it."""

    def makelink(self, tarinfo: tarfile.TarInfo, targetpath: str) -> None:
        with _preserve_link_destination(targetpath):
            self._make_compat_link(tarinfo, targetpath)

    def _make_compat_link(self, tarinfo: tarfile.TarInfo, targetpath: str) -> None:
        try:
            if tarinfo.issym():
                Path(targetpath).unlink(missing_ok=True)
                os.symlink(os.path.normpath(tarinfo.linkname), targetpath)
                return
            source = os.path.join(self.merge_root, tarinfo.linkname)
            if os.path.exists(source):
                Path(targetpath).unlink(missing_ok=True)
                os.link(source, targetpath)
                return
        except (AttributeError, NotImplementedError, OSError):
            pass

        try:
            referent = self._find_link_target(tarinfo)
        except KeyError:
            if tarinfo.issym():
                # Match tarfile's nonfatal treatment of an unsupported dangling
                # symlink, without suppressing filter or I/O errors.
                raise tarfile.ExtractError(
                    "unable to resolve link inside archive"
                ) from None
            raise tarfile.FilterError(
                "hard link target is missing from the archive"
            ) from None

        # The original archive name is needed for further link lookup. Validate
        # that location through the user filter, then independently validate the
        # filtered metadata at the actual write path without invoking user code.
        filtered = self.merge_filter(referent, self.merge_root)
        if filtered is None:
            return
        actual_name = os.path.relpath(targetpath, self.merge_root).replace(os.sep, "/")
        relocated = _filter_contents_member(
            filtered.replace(name=actual_name, deep=False),
            self.merge_root,
        )
        filtered = relocated.replace(name=filtered.name, deep=False)

        # Recursive aliases can otherwise recurse indefinitely on old tarfile.
        active = getattr(self, "_active_link_fallbacks", set())
        key = (referent.offset, os.path.abspath(targetpath))
        if key in active:
            raise tarfile.FilterError(
                "download archive contains a cyclic link fallback"
            )
        self._active_link_fallbacks = active
        active.add(key)
        try:
            # Reuse the seekable tar's file reader and the existing makefile
            # replacement semantics; no separate link-copy implementation.
            self._extract_member(filtered, targetpath)
        finally:
            active.remove(key)

    def makelink_with_filter(
        self,
        tarinfo: tarfile.TarInfo,
        targetpath: str,
        filter_function=None,
        extraction_root=None,
    ) -> None:
        # Some vendor builds use the newer dispatcher without a usable native
        # implementation. Both dispatchers must enter the same guarded path.
        self.makelink(tarinfo, targetpath)


def _filter_contents_member(
    member: tarfile.TarInfo,
    destination: str,
    *,
    allow_special: bool = False,
) -> tarfile.TarInfo:
    """Mandatory checks, also applied at the physical link-copy destination."""
    _safe_relative_name(member.name)
    if PurePosixPath(member.name) == PurePosixPath("."):
        raise tarfile.FilterError("a filter cannot replace the destination root")
    if member.issym() or member.islnk():
        link = member.linkname.replace(os.sep, "/")
        if (
            PurePosixPath(link).is_absolute()
            or PureWindowsPath(link).drive
            or "\\" in link
            or ":" in link
            or "\x00" in link
        ):
            raise tarfile.FilterError("download archive contains an unsafe link")
        # Match patched data_filter: collapse internal '..' components before
        # checking/creating a link. Otherwise a later archive symlink can change
        # the meaning of a previously accepted dangling link on old Python.
        member = member.replace(linkname=posixpath.normpath(link), deep=False)
    if member.isdev() and allow_special:
        member = copy.copy(member)
        member.type = tarfile.REGTYPE
    elif not (member.isreg() or member.isdir() or member.issym() or member.islnk()):
        # Older data_filter implementations can overlook special files with
        # mode=None. A callback must not be able to bypass this boundary.
        raise tarfile.SpecialFileError(member)
    member = tarfile.data_filter(member, destination)
    if (member.issym() or member.islnk()) and os.sep != "/":
        # Keep archive link references in POSIX form even when a native filter
        # returns Windows separators, so a later fallback can validate them too.
        member = member.replace(
            linkname=member.linkname.replace(os.sep, "/"), deep=False
        )
    target = Path(destination) / member.name
    if not allow_special and target.exists() and target.is_dir() != member.isdir():
        raise FileExistsError(
            f"download member conflicts with destination type: {target}"
        )
    return member


def _validate_selected_members(
    members: list[tarfile.TarInfo], paths: tuple[str, ...]
) -> None:
    selected = set(paths)
    seen = set()
    for index, member in enumerate(members):
        if index == 0:
            continue  # The validated source-directory header is structural.
        if member.name not in selected or member.name in seen or member.issym():
            raise tarfile.FilterError("download archive violates the selected paths")
        seen.add(member.name)
    for member in members:
        if member.islnk() and member.linkname not in seen:
            raise tarfile.FilterError(
                "hard link target is not a selected archive member"
            )


def _extract_dir_contents(
    archive_path: Path,
    dst: Path,
    filter: Callable[[tarfile.TarInfo, str], tarfile.TarInfo | None] | None = None,
    paths: tuple[str, ...] | None = None,
) -> None:
    data_filter = getattr(tarfile, "data_filter", None)
    if data_filter is None:
        raise RuntimeError(
            "directory content downloads require a Python build with tarfile.data_filter"
        )
    if dst.is_symlink():
        raise tarfile.FilterError("download destination must not be a symbolic link")
    archive_type = (
        _DirectoryMergeTarFile
        if callable(getattr(tarfile.TarFile, "makelink_with_filter", None))
        else _LegacyDirectoryMergeTarFile
    )
    with archive_type.open(archive_path, "r:", errorlevel=1) as archive:
        members = archive.getmembers()
        if not members or members[0].name not in {".", "./"} or not members[0].isdir():
            raise _public.ApiError(
                "download archive did not contain a source directory"
            )
        # Rewrite the seekable archive's index as well as extraction members.
        # tarfile uses this index (and the original data offsets) for link fallback.
        for member in members:
            _safe_relative_name(member.name)
            if member.name in {".", "./"}:
                if not member.isdir():
                    raise tarfile.FilterError("invalid source directory member")
                member.name = "."
            elif member.name.startswith("./"):
                member.name = member.name[2:]
                _safe_relative_name(member.name)
            else:
                raise tarfile.FilterError(
                    "download archive member is outside the source directory"
                )
            if member.islnk():
                _safe_relative_name(member.linkname)
                if not member.linkname.startswith("./"):
                    raise tarfile.FilterError(
                        "hard link is outside the source directory"
                    )
                member.linkname = member.linkname[2:]
                _safe_relative_name(member.linkname)

        if paths is not None:
            _validate_selected_members(members, paths)

        dst.mkdir(parents=True, exist_ok=True)

        def safe_filter(
            member: tarfile.TarInfo, destination: str
        ) -> tarfile.TarInfo | None:
            if member.name == ".":
                return None  # Do not apply the source root's metadata to dst.
            # Allow callbacks to skip special files, but validate all paths
            # and link targets before and after user code.
            _filter_contents_member(member, destination, allow_special=True)
            if filter is not None:
                member = filter(copy.copy(member), destination)
                if member is None:
                    return None
            return _filter_contents_member(member, destination)

        archive.merge_filter = safe_filter
        archive.merge_root = os.fspath(dst)

        # errorlevel=1 (the default) propagates security/I/O failures while
        # allowing stdlib's nonfatal unresolved-link fallback to skip a link.
        archive.extractall(dst, filter=safe_filter)


def _remote_parent_and_name(src: str) -> tuple[str, str]:
    normalized = src.rstrip("/") or "/"
    path = Path(normalized)
    name = path.name
    if not name:
        raise ValueError("downloading the runtime root directory is not supported")
    return str(path.parent), name


def _extract_and_commit(
    archive_path: Path,
    src: str,
    dst: Path,
    *,
    destination_is_directory: bool,
    workspace: Path,
) -> None:
    extracted = workspace / "extracted"
    extracted.mkdir()
    with tarfile.open(archive_path, "r|") as archive:
        for member in archive:
            _validate_tar_member(member)
            archive.extract(member, extracted)
    source = extracted / Path(src.rstrip("/")).name
    if not source.exists():
        raise _public.ApiError("download archive did not contain the requested path")
    target = dst / source.name if destination_is_directory else dst
    with _commit_parent(target.parent):
        _commit_download_source(source, target)


@contextmanager
def _commit_parent(parent: Path):
    missing: list[Path] = []
    current = parent
    while not current.exists():
        missing.append(current)
        current = current.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        yield
    except BaseException:
        for path in missing:
            try:
                path.rmdir()
            except OSError:
                pass  # Preserve nonempty directories or paths created by another writer.
        raise


def _commit_download_source(source: Path, target: Path) -> None:
    if source.is_file():
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=target.parent, prefix=f".{target.name}.runta-", delete=False
            ) as handle:
                temporary = Path(handle.name)
                with source.open("rb") as input_handle:
                    shutil.copyfileobj(input_handle, handle, _CHUNK_SIZE)
            shutil.copymode(source, temporary)
            os.replace(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        return
    if not source.is_dir():
        raise _public.ApiError("downloaded path is not a regular file or directory")
    stage = Path(
        tempfile.mkdtemp(dir=target.parent, prefix=f".{target.name}.runta-stage-")
    )
    backup = (
        target.parent / f".{target.name}.runta-backup-{os.getpid()}-{time.time_ns()}"
    )
    try:
        shutil.rmtree(stage)
        shutil.copytree(source, stage, copy_function=shutil.copy2, symlinks=True)
        if target.exists():
            os.replace(target, backup)
        os.replace(stage, target)
        if backup.exists():
            shutil.rmtree(backup)
    except BaseException:
        if backup.exists() and not target.exists():
            os.replace(backup, target)
        raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)
        if backup.exists():
            shutil.rmtree(backup)


def _validate_tar_member(member: tarfile.TarInfo) -> None:
    path = Path(member.name)
    if path.is_absolute() or ".." in path.parts:
        raise _public.ApiError("download archive contains an unsafe path")
    if member.isdev():
        raise _public.ApiError("download archive contains an unsupported special file")
    if member.issym() or member.islnk():
        link = Path(member.linkname)
        if member.issym():
            link = path.parent / link
        if link.is_absolute() or ".." in link.parts:
            raise _public.ApiError("download archive contains an unsafe link")


class _SyncSocketWriter:
    def __init__(self, send: Callable[[str], Any]) -> None:
        self._send = send

    def write(self, data: bytes) -> int:
        if data:
            _send_stdin(self._send, data)
        return len(data)

    def flush(self) -> None:
        return None


class _QueueWriter:
    def __init__(
        self,
        chunks: queue.Queue[bytes | BaseException | None],
        stopped: threading.Event,
        notify: Callable[[], None],
    ) -> None:
        self._chunks = chunks
        self._stopped = stopped
        self._notify = notify

    def write(self, data: bytes) -> int:
        if data and not _queue_put(
            self._chunks, bytes(data), self._stopped, self._notify
        ):
            raise RuntimeError("streaming upload was cancelled")
        return len(data)

    def flush(self) -> None:
        return None


def _queue_put(
    chunks: queue.Queue[bytes | BaseException | None],
    item: bytes | BaseException | None,
    stopped: threading.Event,
    notify: Callable[[], None],
) -> bool:
    while not stopped.is_set():
        try:
            chunks.put(item, timeout=0.1)
            notify()
            return True
        except queue.Full:
            continue
    return False
