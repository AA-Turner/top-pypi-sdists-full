"""AnyIO hook daemon with request-scoped dispatch and graceful draining."""

from __future__ import annotations

import io
import os
import socket
import stat
import sys
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any

from runlayer_cli.hook.daemon_client import daemon_is_enabled
from runlayer_cli.hook.daemon_protocol import (
    DAEMON_ENDPOINT_ENV,
    FRAME_PREFIX_SIZE,
    REQUEST_ACCEPTED_ACK,
    WINDOWS_RESPONSE_ACK,
    FrameError,
    HealthResponse,
    HookRequest,
    HookResult,
    UnsupportedDaemonPlatform,
    daemon_endpoint,
    decode_frame,
    encode_frame,
    frame_body_length,
    parse_hook_request,
    parse_health_request,
    protocol_version,
)

_REQUEST_READ_TIMEOUT_SECONDS = 5.0
_RESPONSE_WRITE_TIMEOUT_SECONDS = 5.0
_MAX_CONCURRENT_CONNECTIONS = 32
_MAX_QUEUED_CONNECTIONS = 64
_CONNECTION_QUEUE_TIMEOUT_SECONDS = 5.0
_GATE_CHECK_INTERVAL_SECONDS = 30.0
_SOCKET_PROBE_TIMEOUT_SECONDS = 0.2


class DaemonAlreadyRunning(RuntimeError):
    """Raised when another daemon owns the configured endpoint."""


@dataclass
class _ServerState:
    listener: Any
    draining: bool = False
    accept_scope: Any | None = None

    async def begin_drain(self) -> None:
        if not self.draining:
            self.draining = True
            if self.accept_scope is not None:
                self.accept_scope.cancel()
            await self.listener.aclose()


def run_daemon() -> None:
    """Run the daemon until version skew or the rollout gate requests drain."""
    import anyio  # noqa: PLC0415 - daemon-only dependency
    from runlayer_cli.daemon.runtime import (  # noqa: PLC0415 - daemon-only closure
        DaemonRuntime,
    )

    runtime = DaemonRuntime()
    runtime.install()
    try:
        if not runtime.daemon_is_enabled():
            return
        anyio.run(
            partial(
                serve_daemon,
                gate_check=runtime.daemon_is_enabled,
                before_hook=runtime.before_hook,
                ready=partial(runtime.prewarm_background, force=True),
            )
        )
    except (DaemonAlreadyRunning, UnsupportedDaemonPlatform):
        # Gate flipped on for a platform with no daemon endpoint (Linux is
        # Detect-only): exit as quietly as the gate-off no-op does.
        return
    finally:
        runtime.close()


async def serve_daemon(
    *,
    endpoint: str | None = None,
    gate_check: Callable[[], bool] = daemon_is_enabled,
    gate_check_interval: float = _GATE_CHECK_INTERVAL_SECONDS,
    ready: Callable[[], None] | None = None,
    hook_runner: Callable[[], None] | None = None,
    before_hook: Callable[[], None] | None = None,
) -> None:
    """Serve one endpoint; injectable controls keep integration tests deterministic."""
    import anyio  # noqa: PLC0415 - daemon-only dependency

    resolved_endpoint = endpoint or daemon_endpoint()
    socket_identity: tuple[int, int] | None = None
    unix_lock_fd: int | None = None
    listener: Any | None = None
    if sys.platform == "win32":
        from runlayer_cli.daemon.windows_pipe import (  # noqa: PLC0415
            PipeAlreadyRunning,
            WindowsPipeListener,
        )

        try:
            listener = WindowsPipeListener(resolved_endpoint)
        except PipeAlreadyRunning as exc:
            raise DaemonAlreadyRunning(resolved_endpoint) from exc
    else:
        socket_path = Path(resolved_endpoint)
        _prepare_unix_parent(socket_path)
        try:
            unix_lock_fd = _acquire_unix_lock(socket_path)
        except BlockingIOError as exc:
            raise DaemonAlreadyRunning(resolved_endpoint) from exc
        try:
            _prepare_unix_socket(socket_path)
            listener = await anyio.create_unix_listener(socket_path)
            os.chmod(socket_path, 0o600)
            socket_stat = socket_path.lstat()
            socket_identity = (socket_stat.st_dev, socket_stat.st_ino)
        except BaseException:
            if listener is not None:
                await listener.aclose()
            os.close(unix_lock_fd)
            raise

    assert listener is not None
    state = _ServerState(listener)
    connection_limiter = anyio.CapacityLimiter(_MAX_CONCURRENT_CONNECTIONS)
    admission_limiter = anyio.CapacityLimiter(
        _MAX_CONCURRENT_CONNECTIONS + _MAX_QUEUED_CONNECTIONS
    )

    try:
        if ready is not None:
            ready()
        async with anyio.create_task_group() as connections:
            async with anyio.create_task_group() as watcher:
                watcher.start_soon(
                    _watch_rollout_gate,
                    state,
                    gate_check,
                    gate_check_interval,
                )
                await _accept_connections(
                    state,
                    connections,
                    hook_runner,
                    before_hook,
                    connection_limiter,
                    admission_limiter,
                )
                watcher.cancel_scope.cancel()
    finally:
        await listener.aclose()
        if socket_identity is not None:
            _unlink_owned_socket(Path(resolved_endpoint), socket_identity)
        if unix_lock_fd is not None:
            os.close(unix_lock_fd)


async def _accept_connections(
    state: _ServerState,
    task_group: Any,
    hook_runner: Callable[[], None] | None,
    before_hook: Callable[[], None] | None,
    connection_limiter: Any,
    admission_limiter: Any,
) -> None:
    import anyio  # noqa: PLC0415 - daemon-only dependency

    if sys.platform == "win32":
        from runlayer_cli.daemon.windows_pipe import (  # noqa: PLC0415
            PipeListenerClosed,
        )

        closed_exceptions: tuple[type[BaseException], ...] = (
            anyio.ClosedResourceError,
            PipeListenerClosed,
        )
    else:
        closed_exceptions = (anyio.ClosedResourceError,)

    while not state.draining:
        stream = None
        with anyio.CancelScope() as accept_scope:
            state.accept_scope = accept_scope
            try:
                try:
                    stream = await state.listener.accept()
                except closed_exceptions:
                    if state.draining:
                        return
                    raise
            finally:
                state.accept_scope = None
        if stream is not None:
            borrower = object()
            try:
                admission_limiter.acquire_on_behalf_of_nowait(borrower)
            except anyio.WouldBlock:
                await _close_stream(stream)
                continue
            try:
                task_group.start_soon(
                    _queue_connection,
                    stream,
                    state,
                    hook_runner,
                    before_hook,
                    connection_limiter,
                    admission_limiter,
                    borrower,
                )
            except BaseException:
                try:
                    admission_limiter.release_on_behalf_of(borrower)
                finally:
                    await _close_stream(stream)
                raise


async def _queue_connection(
    stream: Any,
    state: _ServerState,
    hook_runner: Callable[[], None] | None,
    before_hook: Callable[[], None] | None,
    connection_limiter: Any,
    admission_limiter: Any,
    borrower: object,
) -> None:
    import anyio  # noqa: PLC0415 - daemon-only dependency

    acquired = False
    try:
        try:
            with anyio.fail_after(_CONNECTION_QUEUE_TIMEOUT_SECONDS):
                await connection_limiter.acquire_on_behalf_of(borrower)
                acquired = True
        except TimeoutError:
            return
        await _handle_connection(stream, state, hook_runner, before_hook)
    finally:
        try:
            if acquired:
                connection_limiter.release_on_behalf_of(borrower)
        finally:
            try:
                admission_limiter.release_on_behalf_of(borrower)
            finally:
                await _close_stream(stream)


async def _close_stream(stream: Any) -> None:
    import anyio  # noqa: PLC0415 - daemon-only dependency

    with anyio.CancelScope(shield=True):
        await stream.aclose()


async def _handle_connection(
    stream: Any,
    state: _ServerState,
    hook_runner: Callable[[], None] | None,
    before_hook: Callable[[], None] | None,
) -> None:
    import anyio  # noqa: PLC0415 - daemon-only dependency
    from anyio import to_thread  # noqa: PLC0415 - daemon-only dependency

    async with stream:
        try:
            with anyio.fail_after(_REQUEST_READ_TIMEOUT_SECONDS):
                payload = await _receive_frame(stream)
                health_request = parse_health_request(payload)
                request = (
                    None if health_request is not None else parse_hook_request(payload)
                )
        except Exception:
            return

        if health_request is not None:
            if state.draining:
                await _send_response(stream, {"status": "restarting"})
            else:
                health_response: HealthResponse = {
                    "status": "ok",
                    "version": protocol_version(),
                }
                await _send_response(stream, health_response)
            return

        assert request is not None
        if state.draining or request["version"] != protocol_version():
            try:
                await _send_response(stream, {"status": "restarting"})
            except Exception:
                pass
            finally:
                await state.begin_drain()
            return

        try:
            await _accept_request(stream)
            result = await to_thread.run_sync(
                _run_hook_request,
                request,
                hook_runner,
                before_hook,
            )
            await _send_response(stream, result)
        except Exception:
            # Before the accept ACK, closing triggers safe inline fallback.
            # After it, the client returns an error instead of replaying.
            return


async def _accept_request(stream: Any) -> None:
    import anyio  # noqa: PLC0415 - daemon-only dependency

    with anyio.fail_after(_RESPONSE_WRITE_TIMEOUT_SECONDS):
        await stream.send(encode_frame({"status": "accepted"}))
    with anyio.fail_after(_REQUEST_READ_TIMEOUT_SECONDS):
        if sys.platform == "win32":
            await stream.wait_for_client_ack(REQUEST_ACCEPTED_ACK)
        elif await _receive_exactly(stream, len(REQUEST_ACCEPTED_ACK)) != (
            REQUEST_ACCEPTED_ACK
        ):
            raise FrameError("daemon client did not acknowledge accepted request")


async def _send_response(stream: Any, payload: object) -> None:
    import anyio  # noqa: PLC0415 - daemon-only dependency

    with anyio.fail_after(_RESPONSE_WRITE_TIMEOUT_SECONDS):
        await stream.send(encode_frame(payload))
    if sys.platform == "win32" and payload != {"status": "restarting"}:
        # The client sends this ACK as soon as it has read the frame, so the
        # wait is bounded by the client read budget, not by how long the hook
        # itself may run. A client that never ACKs must not keep holding its
        # concurrency slot and delaying drain.
        try:
            with anyio.move_on_after(_REQUEST_READ_TIMEOUT_SECONDS):
                await stream.wait_for_client_ack(WINDOWS_RESPONSE_ACK)
        except Exception:
            pass


async def _receive_frame(stream: Any) -> object:
    length = frame_body_length(await _receive_exactly(stream, FRAME_PREFIX_SIZE))
    return decode_frame(await _receive_exactly(stream, length))


async def _receive_exactly(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = await stream.receive(remaining)
        if not chunk:
            raise FrameError("frame ended before declared length")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _run_hook_request(
    request: HookRequest,
    hook_runner: Callable[[], None] | None,
    before_hook: Callable[[], None] | None = None,
) -> HookResult:
    from runlayer_cli.hook import hook_io  # noqa: PLC0415 - daemon worker closure

    if hook_runner is None:
        from runlayer_cli.hook.dispatch import run_hook  # noqa: PLC0415

        hook_runner = run_hook

    stdout = io.StringIO()
    stderr = io.StringIO()
    exit_code = 0
    if before_hook is not None:
        before_hook()
    with hook_io.scoped(
        hook_io.HookIO(
            stdin_text=request["stdin"],
            stdout=stdout,
            stderr=stderr,
            env=request["env"],
            cwd=request["cwd"],
            argv=request["argv"],
            daemon_served=True,
            client_start_ms=request.get("client_start_ms"),
        )
    ):
        try:
            hook_runner()
        except SystemExit as exc:
            exit_code = _system_exit_code(exc, stderr)
    return {
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "exit_code": exit_code,
    }


def _system_exit_code(exc: SystemExit, stderr: io.StringIO) -> int:
    code = exc.code
    if code is None:
        return 0
    if isinstance(code, int):
        return int(code)
    stderr.write(f"{code}\n")
    return 1


async def _watch_rollout_gate(
    state: _ServerState,
    gate_check: Callable[[], bool],
    interval: float,
) -> None:
    import anyio  # noqa: PLC0415 - daemon-only dependency
    from anyio import to_thread  # noqa: PLC0415 - daemon-only dependency

    while not state.draining:
        await anyio.sleep(interval)
        try:
            enabled = await to_thread.run_sync(gate_check)
        except Exception:
            enabled = False
        if not enabled:
            await state.begin_drain()


def _prepare_unix_parent(path: Path) -> None:
    parent = path.parent
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    parent_stat = parent.stat()
    if parent_stat.st_uid != os.getuid():
        raise PermissionError(f"daemon socket directory is not user-owned: {parent}")
    if os.environ.get(DAEMON_ENDPOINT_ENV):
        if stat.S_IMODE(parent_stat.st_mode) & 0o077:
            raise PermissionError(
                f"daemon socket override directory is not private: {parent}"
            )
    else:
        parent.chmod(0o700)


def _acquire_unix_lock(path: Path) -> int:
    import fcntl  # noqa: PLC0415 - unavailable on Windows

    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    lock_path = Path(f"{path}.lock")
    fd = os.open(lock_path, flags, 0o600)
    try:
        lock_stat = os.fstat(fd)
        if not stat.S_ISREG(lock_stat.st_mode) or lock_stat.st_uid != os.getuid():
            raise PermissionError(f"daemon lock is not user-owned: {lock_path}")
        os.fchmod(fd, 0o600)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BaseException:
        os.close(fd)
        raise
    return fd


def _prepare_unix_socket(path: Path) -> None:
    if not os.path.lexists(path):
        return
    existing = path.lstat()
    if not stat.S_ISSOCK(existing.st_mode) or existing.st_uid != os.getuid():
        raise FileExistsError(f"refusing to replace non-owned daemon socket: {path}")
    if _socket_is_live(path):
        raise DaemonAlreadyRunning(str(path))
    path.unlink()


def _socket_is_live(path: Path) -> bool:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as probe:
        probe.settimeout(_SOCKET_PROBE_TIMEOUT_SECONDS)
        return probe.connect_ex(str(path)) == 0


def _unlink_owned_socket(path: Path, identity: tuple[int, int]) -> None:
    try:
        socket_stat = path.lstat()
    except FileNotFoundError:
        return
    if (
        stat.S_ISSOCK(socket_stat.st_mode)
        and (socket_stat.st_dev, socket_stat.st_ino) == identity
    ):
        path.unlink()
