"""Durable guest tasks, observed through replaceable exec WebSockets."""

from __future__ import annotations

import asyncio
import logging
import math
import shlex
import socket
import ssl
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from websockets.exceptions import ConnectionClosed, InvalidStatus

import runta as _public

from .helpers import command_parts
from .byte_budget import _ByteBudget
from .retry import _delay, retry_async, retry_sync
from .streaming_transfer import (
    _async_send_close_stdin,
    _async_send_start,
    _async_send_stdin,
    _async_socket,
    _decode_frame_data,
    _parse_frame,
    _retryable_transfer_error,
    _send_close_stdin,
    _send_start,
    _send_stdin,
    _sync_socket,
)

_LOG = logging.getLogger(__name__)
_ROOT = "/tmp/runta-sdk-exec"
_PREFIX = "RUNTA_EXEC_V1"
_RESULT_PREFIX = b"RUNTA_EXEC_RESULT_V2"
_IDLE_TIMEOUT = 30.0
_OUTPUT_LIMIT = 4 * 1024 * 1024
_TERMINAL = {"completed", "timed_out", "cancelled"}
_SCRIPT = Path(__file__).with_name("execution.sh").read_text()
# Open the inode before sizing it, then stream exactly that prefix. Appending or
# unlinking a collector file after open cannot invalidate this snapshot.
_SNAPSHOT_SCRIPT = """(
    size=$(stat -Lc %s /proc/self/fd/3) || exit 125
    [ "$size" -le "$2" ] || size=$2
    head -c "$size" <&3
) 3< "$1"
rc=$?
[ "$rc" -eq 0 ] && exit 0
[ -e "$1" ] || exit 44
exit "$rc"
"""


def _snapshot_bytes(result: _public.CommandResult) -> bytes:
    if result.exit_code == 44:
        raise _public.ApiError("Execution output file disappeared", status_code=404)
    if result.exit_code != 0:
        raise _public.ApiError(result.stderr_text or "Execution output snapshot failed")
    return result.stdout


class ExecutionError(_public.ApiError):
    """Execution could not be observed; its guest task may still be running."""

    execution_id: str
    """Task UUID retained for diagnostics after observation failure."""

    def __init__(self, message: str, execution_id: str, **kwargs: Any) -> None:
        self.execution_id = execution_id
        super().__init__(f"{message} (execution_id={execution_id})", **kwargs)


@dataclass(frozen=True)
class ExecutionState:
    """Snapshot of a guest execution, including final result metadata."""

    status: str
    """starting, running, completed, timed_out, cancelled, lost, or unknown."""
    exit_code: int | None = None
    """Command exit code, available after completion."""
    stdout_truncated: bool = False
    """Whether stdout exceeded its capture limit."""
    stderr_truncated: bool = False
    """Whether stderr exceeded its capture limit."""
    duration: float = 0.0
    """Execution duration in seconds, available after completion."""


def _parse_state(line: bytes) -> ExecutionState:
    try:
        fields = line.decode("ascii").split()
        if fields[:1] != [_PREFIX]:
            raise ValueError("wrong protocol version")
        status = fields[1]
        if status in _TERMINAL:
            if (
                len(fields) != 6
                or fields[3] not in {"0", "1"}
                or fields[4] not in {"0", "1"}
            ):
                raise ValueError("invalid result")
            duration = float(fields[5])
            if not math.isfinite(duration) or duration < 0:
                raise ValueError("invalid duration")
            return ExecutionState(
                status, int(fields[2]), fields[3] == "1", fields[4] == "1", duration
            )
        if status not in {"starting", "running", "lost", "unknown"} or len(fields) != 2:
            raise ValueError("invalid state")
        return ExecutionState(status)
    except (UnicodeError, ValueError, IndexError) as exc:
        raise _public.ApiError("Invalid execution observation message") from exc


class _Observation:
    """Parse status lines followed by a length-delimited binary result."""

    def __init__(self, limit: int = _OUTPUT_LIMIT) -> None:
        self.buffer = bytearray()
        self.limit = limit
        self.state: ExecutionState | None = None
        self.lengths: tuple[int, int] | None = None
        self.output: tuple[bytes, bytes] | None = None

    def feed(self, data: bytes) -> list[ExecutionState]:
        states = []
        self.buffer.extend(data)
        while self.lengths is None:
            if b"\n" not in self.buffer:
                if len(self.buffer) > 8192:
                    raise _public.ApiError("Execution observation message is too large")
                return states
            line, _, rest = self.buffer.partition(b"\n")
            self.buffer[:] = rest
            if len(line) > 8192:
                raise _public.ApiError("Execution observation message is too large")
            if line.startswith(_RESULT_PREFIX + b" "):
                fields = line.split()
                try:
                    if len(fields) != 8:
                        raise ValueError("invalid result header")
                    state = _parse_state(b" ".join([_PREFIX.encode(), *fields[1:6]]))
                    if state.status not in _TERMINAL:
                        raise ValueError("nonterminal result")
                    if any(not value.isdigit() for value in fields[6:]):
                        raise ValueError("invalid output length")
                    lengths = (int(fields[6]), int(fields[7]))
                    if any(length > self.limit for length in lengths):
                        raise ValueError("output exceeds capture limit")
                except ValueError as exc:
                    raise _public.ApiError("Invalid execution result header") from exc
                self.state, self.lengths = state, lengths
            else:
                states.append(_parse_state(bytes(line)))
        out_size, err_size = self.lengths
        if len(self.buffer) > out_size + err_size:
            raise _public.ApiError("Execution result exceeds declared lengths")
        if len(self.buffer) == out_size + err_size:
            self.output = (bytes(self.buffer[:out_size]), bytes(self.buffer[out_size:]))
            self.buffer.clear()
            assert self.state is not None
            states.append(self.state)
        return states


def _write_script(path: str, content: str) -> str:
    return f"printf '%s\\n' {shlex.quote(content)} > {shlex.quote(path)}\n"


def _bootstrap(
    directory: str,
    command: str,
    args: list[str],
    *,
    env: dict[str, str] | None,
    timeout: float | None,
    limit: int,
    stdin_size: int = 0,
) -> str:
    argv = ["env", "--", *(f"{k}={v}" for k, v in (env or {}).items()), command, *args]
    command_script = "exec " + shlex.join(argv) + "\n"
    q = shlex.quote(directory)
    return (
        "set -eu\numask 077\n"
        "for tool in setsid timeout head stdbuf cat wc mkfifo mv rm sleep awk stat id env mkdir; do\n"
        ' command -v "$tool" >/dev/null || { printf \'Missing execution dependency: %s\\n\' "$tool" >&2; exit 127; }\n'
        "done\n"
        "test -x /bin/kill && test -r /proc/uptime && test -r /proc/sys/kernel/random/boot_id || "
        "{ printf 'Execution requires Linux /proc and /bin/kill\\n' >&2; exit 127; }\n"
        "timeout --version >/dev/null 2>&1 || { printf 'Execution requires GNU timeout\\n' >&2; exit 127; }\n"
        "sleep --version >/dev/null 2>&1 || { printf 'Execution requires GNU sleep\\n' >&2; exit 127; }\n"
        "stdbuf --version >/dev/null 2>&1 || { printf 'Execution requires GNU stdbuf\\n' >&2; exit 127; }\n"
        f"test ! -L {_ROOT} || exit 126\n"
        f"mkdir -m 700 {_ROOT} 2>/dev/null || test -d {_ROOT}\n"
        f'test "$(stat -c %u {_ROOT})" = "$(id -u)" && '
        f'test "$(stat -c %a {_ROOT})" = 700 || '
        "{ printf 'Unsafe SDK execution directory\\n' >&2; exit 126; }\n"
        f"mkdir -m 700 {q}\n"
        + _write_script(f"{directory}/control.sh", _SCRIPT)
        + _write_script(f"{directory}/command.sh", command_script)
        + f'sh {q}/control.sh bootstrap_identity {q} "$$"\n'
        + f"cat > {q}/stdin.tmp\n"
        + f"received=$(wc -c < {q}/stdin.tmp)\n"
        + f'if [ "$received" -ne {stdin_size} ]; then\n'
        + f"  printf '%s %s\\n' {stdin_size} \"$received\" > {q}/stdin.incomplete.tmp\n"
        # The reader has exited: release partial data before publishing failure.
        + f"  rm -f {q}/stdin.tmp\n"
        + f"  mv {q}/stdin.incomplete.tmp {q}/stdin.incomplete\n"
        + f"  printf 'Incomplete execution stdin: expected {stdin_size} bytes, received %s\\n' \"$received\" >&2\n"
        + "  exit 125\nfi\n"
        + f"mv {q}/stdin.tmp {q}/stdin\n"
        + f"printf '%s\\n' {stdin_size} > {q}/stdin.complete.tmp\n"
        + f"mv {q}/stdin.complete.tmp {q}/stdin.complete\n"
        + f"printf '%s\\n' {limit} > {q}/limit\n"
        + f"setsid sh {q}/control.sh supervise {q} {limit} {timeout if timeout is not None else 'none'} "
        "< /dev/null > /dev/null 2>&1 &\n" + f"exec sh {q}/control.sh watch {q}\n"
    )


def _retryable_observation(exc: Exception) -> bool:
    if isinstance(exc, ssl.SSLError):
        return False
    if isinstance(exc, socket.gaierror) and exc.errno in {
        socket.EAI_NONAME,
        socket.EAI_FAIL,
    }:
        return False
    if isinstance(exc, InvalidStatus):
        return exc.response.status_code in {408, 429, 502, 503, 504}
    return isinstance(
        exc,
        (
            ConnectionClosed,
            TimeoutError,
            asyncio.TimeoutError,
            ConnectionError,
            OSError,
        ),
    )


class _ExecutionBase:
    id: str
    """Task UUID for recovering this execution."""

    def __init__(self, runtime: Any, execution_id: str) -> None:
        self.id = str(uuid.UUID(execution_id))
        self._runtime = runtime
        self._http = runtime._client._http
        self._directory = f"{_ROOT}/{self.id}"
        self._launch: str | None = None
        self._stdin = b""
        self._limit = _OUTPUT_LIMIT
        self._inline_output: tuple[bytes, bytes] | None = None
        self._route_deadline = time.monotonic() + 60

    @classmethod
    def _new(
        cls,
        runtime: Any,
        command: str | list[str],
        *,
        timeout: float | None,
        env: dict[str, str] | None,
        stdin: bytes | str | None,
        cwd: str | None,
        max_output_bytes: int | None,
    ) -> Any:
        if timeout is not None and (not math.isfinite(timeout) or timeout <= 0):
            raise ValueError("timeout must be a finite positive number")
        limit = _OUTPUT_LIMIT if max_output_bytes is None else max_output_bytes
        if type(limit) is not int or not 0 <= limit < 2**63 - 1:
            raise ValueError(
                "max_output_bytes must be a nonnegative integer smaller than 2**63-1"
            )
        exe, args = command_parts(command, cwd=cwd)
        if env and any(
            not k or "=" in k or "\0" in k or "\0" in v for k, v in env.items()
        ):
            raise ValueError("Invalid execution environment variable")
        task = cls(runtime, str(uuid.uuid4()))
        task._limit = limit
        task._stdin = stdin.encode() if isinstance(stdin, str) else stdin or b""
        task._launch = _bootstrap(
            task._directory,
            exe,
            args,
            env=env,
            timeout=timeout,
            limit=limit,
            stdin_size=len(task._stdin),
        )
        return task

    def _control(self, mode: str) -> str:
        q = shlex.quote(self._directory)
        return (
            f"if test -f {q}/control.sh && test ! -L {q}; then "
            f"exec sh {q}/control.sh {mode} {q}; "
            f"else printf '{_PREFIX} unknown\\n'; exit 1; fi"
        )

    def _accept(
        self, state: ExecutionState, healthy: Callable[[], None]
    ) -> ExecutionState | None:
        if state.status in {"unknown", "lost"}:
            raise ExecutionError(
                f"Execution is {state.status}; command will not be resubmitted", self.id
            )
        if state.status != "starting":
            healthy()
        return state if state.status in _TERMINAL else None

    def _error(self, exc: Exception) -> ExecutionError:
        if isinstance(exc, ExecutionError):
            return exc
        return ExecutionError(
            str(exc),
            self.id,
            status_code=getattr(exc, "status_code", None),
            code=getattr(exc, "code", None),
        )


class Execution(_ExecutionBase):
    """Recover a synchronous execution using its ID and owning runtime."""

    def _short(self, mode: str) -> _public.CommandResult:
        result = self._http.execute(
            self._runtime.id, "sh", ["-c", self._control(mode)], timeout=30
        )
        if result.exit_code != 0 and mode != "status":
            raise ExecutionError(
                result.stderr_text or f"Execution {mode} failed", self.id
            )
        return result

    def status(self) -> ExecutionState:
        """Query state without waiting for task completion."""
        try:
            return _parse_state(self._short("status").stdout.strip())
        except _public.ApiError as exc:
            raise self._error(exc) from exc

    def output(self) -> tuple[bytes, bytes]:
        """Read buffered stdout and stderr; ongoing tasks expose capped snapshots."""
        state = self.status()
        return self._output(state)

    def _output(self, state: ExecutionState) -> tuple[bytes, bytes]:
        def read(path: str) -> bytes:
            try:
                return self._http.read_file(self._runtime.id, path)
            except _public.ApiError as exc:
                if exc.status_code != 422 or "file is too large" not in str(exc):
                    raise
                cap = limit
                if cap is None:
                    cap = int(
                        self._http.read_file(
                            self._runtime.id, f"{self._directory}/limit"
                        )
                    )
                return retry_sync(
                    lambda _: _snapshot_bytes(
                        self._http.execute(
                            self._runtime.id,
                            "sh",
                            ["-c", _SNAPSHOT_SCRIPT, "sh", path, str(cap)],
                            timeout=None,
                            idle_timeout=_IDLE_TIMEOUT,
                            max_output_bytes=cap,
                        )
                    ),
                    name="execution snapshot",
                    attempts=self._http.retry_max_attempts,
                    retryable=_retryable_transfer_error,
                )

        limit = None
        if state.status not in _TERMINAL:
            limit = int(
                self._http.read_file(self._runtime.id, f"{self._directory}/limit")
            )
        values = []
        for stream in ("stdout", "stderr"):
            path = f"{self._directory}/{stream}" + (
                "" if state.status in _TERMINAL else ".raw"
            )
            try:
                data = read(path)
            except _public.ApiError as exc:
                if exc.status_code == 404 and state.status not in _TERMINAL:
                    state = self.status()
                    try:
                        # A collector can finalize its stream before the whole
                        # task publishes its terminal status.
                        data = read(f"{self._directory}/{stream}")
                    except _public.ApiError as final_exc:
                        if (
                            final_exc.status_code == 404
                            and state.status not in _TERMINAL
                        ):
                            data = b""
                        else:
                            raise self._error(final_exc) from final_exc
                else:
                    raise self._error(exc) from exc
            # During capture the final byte is a truncation sentinel.
            if limit is not None:
                data = data[:limit]
            values.append(data)
        return values[0], values[1]

    def cancel(self) -> None:
        """Request cancellation; the supervisor applies TERM then KILL."""
        self._short("cancel")

    def cleanup(self) -> None:
        """Remove a completed task's files; unfinished tasks cannot be removed."""
        self._short("cleanup")

    def _observe(self, healthy: Callable[[], None]) -> ExecutionState:
        observation = _Observation(self._limit)
        self._inline_output = None
        errors = bytearray()
        with _sync_socket(
            self._http.endpoint,
            self._http.token,
            self._runtime.id,
            self._http.timeout,
            _tls=getattr(self._http, "_websocket_tls", None),
        ) as socket:
            body = self._launch or self._control("watch")
            stdin = self._stdin
            # Once sending begins the launch outcome is uncertain. All later
            # connections observe the ID and can never launch again.
            self._launch = None
            self._stdin = b""
            _send_start(socket.send, "sh", ["-c", body])
            for offset in range(0, len(stdin), 64 * 1024):
                _send_stdin(socket.send, stdin[offset : offset + 64 * 1024])
            _send_close_stdin(socket.send)
            deadline = time.monotonic() + _IDLE_TIMEOUT
            while True:
                frame = _parse_frame(
                    socket.recv(timeout=max(0, deadline - time.monotonic()))
                )
                kind = frame.get("type")
                if kind == "heartbeat":
                    socket.send('{"type":"heartbeat"}')
                    deadline = time.monotonic() + _IDLE_TIMEOUT
                elif kind == "stdout":
                    data = _decode_frame_data(frame)
                    states = observation.feed(data)
                    if data:
                        deadline = time.monotonic() + _IDLE_TIMEOUT
                    for state in states:
                        result = self._accept(state, healthy)
                        if result is not None:
                            self._inline_output = observation.output
                            return result
                elif kind == "stderr":
                    errors.extend(_decode_frame_data(frame)[: 4096 - len(errors)])
                elif kind == "exit":
                    if frame.get("code") == 0 and not errors:
                        raise ConnectionError("Observer exited without a result")
                    raise _public.ApiError(
                        errors.decode(errors="replace")
                        or "Observer exited without a result"
                    )
                elif kind == "error":
                    raise _public.ApiError(
                        str(frame.get("message", "Execution observation failed"))
                    )

    def wait(self) -> _public.CommandResult:
        """Observe the existing task, reconnecting without executing it again."""
        failures = 0
        observed_result = False

        def healthy() -> None:
            nonlocal failures
            failures = 0

        try:
            while True:
                try:
                    state = self._observe(healthy)
                    observed_result = True
                    stdout, stderr = (
                        self._inline_output
                        if self._inline_output is not None
                        else self._output(state)
                    )
                    result = _public.CommandResult(
                        state.exit_code,
                        stdout,
                        stderr,
                        state.duration,
                        state.stdout_truncated,
                        state.stderr_truncated,
                    )
                    try:
                        self.cleanup()
                    except Exception:
                        _LOG.debug(
                            "Could not clean execution %s", self.id, exc_info=True
                        )
                    return result
                except Exception as exc:
                    failures += 1
                    route_miss = (
                        isinstance(exc, InvalidStatus)
                        and exc.response.status_code == 404
                        and time.monotonic() < self._route_deadline
                        and self._runtime._exec_route_miss_can_retry()
                    )
                    if (
                        not (_retryable_observation(exc) or route_miss)
                        or failures >= self._http.retry_max_attempts
                    ):
                        error = self._error(exc)
                        if not observed_result:
                            try:
                                cleanup = self._short("cleanup_incomplete")
                                detail = cleanup.stdout_text.strip()
                                if detail.startswith("Incomplete execution stdin:"):
                                    error = ExecutionError(detail, self.id)
                            except Exception:
                                _LOG.debug(
                                    "Could not clean incomplete input for execution %s",
                                    self.id,
                                    exc_info=True,
                                )
                        if error is exc:
                            raise
                        raise error from exc
                    time.sleep(_delay(failures - 1, None))
        except (KeyboardInterrupt, SystemExit):
            try:
                self.cancel()
            except Exception:
                _LOG.debug("Could not cancel execution %s", self.id, exc_info=True)
            raise


class AsyncExecution(_ExecutionBase):
    """Recover an asynchronous execution using its ID and owning runtime."""

    async def _short(self, mode: str) -> _public.CommandResult:
        result = await self._http.execute(
            self._runtime.id, "sh", ["-c", self._control(mode)], timeout=30
        )
        if result.exit_code != 0 and mode != "status":
            raise ExecutionError(
                result.stderr_text or f"Execution {mode} failed", self.id
            )
        return result

    async def status(self) -> ExecutionState:
        """Query state without waiting for task completion."""
        try:
            return _parse_state((await self._short("status")).stdout.strip())
        except _public.ApiError as exc:
            raise self._error(exc) from exc

    async def output(self) -> tuple[bytes, bytes]:
        """Read buffered stdout and stderr."""
        return await self._output(await self.status())

    async def _output(self, state: ExecutionState) -> tuple[bytes, bytes]:
        async def read(path: str) -> bytes:
            try:
                return await self._http.read_file(self._runtime.id, path)
            except _public.ApiError as exc:
                if exc.status_code != 422 or "file is too large" not in str(exc):
                    raise
                cap = limit
                if cap is None:
                    cap = int(
                        await self._http.read_file(
                            self._runtime.id, f"{self._directory}/limit"
                        )
                    )

                async def snapshot(_: float | None) -> bytes:
                    return _snapshot_bytes(
                        await self._http.execute(
                            self._runtime.id,
                            "sh",
                            ["-c", _SNAPSHOT_SCRIPT, "sh", path, str(cap)],
                            timeout=None,
                            idle_timeout=_IDLE_TIMEOUT,
                            max_output_bytes=cap,
                        )
                    )

                return await retry_async(
                    snapshot,
                    name="execution snapshot",
                    attempts=self._http.retry_max_attempts,
                    retryable=_retryable_transfer_error,
                )

        limit = None
        if state.status not in _TERMINAL:
            limit = int(
                await self._http.read_file(self._runtime.id, f"{self._directory}/limit")
            )
        values = []
        for stream in ("stdout", "stderr"):
            path = f"{self._directory}/{stream}" + (
                "" if state.status in _TERMINAL else ".raw"
            )
            try:
                data = await read(path)
            except _public.ApiError as exc:
                if exc.status_code == 404 and state.status not in _TERMINAL:
                    state = await self.status()
                    try:
                        data = await read(f"{self._directory}/{stream}")
                    except _public.ApiError as final_exc:
                        if (
                            final_exc.status_code == 404
                            and state.status not in _TERMINAL
                        ):
                            data = b""
                        else:
                            raise self._error(final_exc) from final_exc
                else:
                    raise self._error(exc) from exc
            if limit is not None:
                data = data[:limit]
            values.append(data)
        return values[0], values[1]

    async def cancel(self) -> None:
        """Request cancellation; the supervisor applies TERM then KILL."""
        await self._short("cancel")

    async def cleanup(self) -> None:
        """Remove a completed task's files."""
        await self._short("cleanup")

    async def _observe(self, healthy: Callable[[], None]) -> ExecutionState:
        send_budget = _ByteBudget()
        receive_budget = _ByteBudget()
        observation = _Observation(self._limit)
        self._inline_output = None
        errors = bytearray()
        async with _async_socket(
            self._http.endpoint,
            self._http.token,
            self._runtime.id,
            self._http.timeout,
            _tls=getattr(self._http, "_websocket_tls", None),
        ) as socket:
            body = self._launch or self._control("watch")
            stdin = self._stdin
            self._launch = None
            self._stdin = b""
            await _async_send_start(socket.send, "sh", ["-c", body])
            for offset in range(0, len(stdin), 64 * 1024):
                chunk = stdin[offset : offset + 64 * 1024]
                await _async_send_stdin(socket.send, chunk)
                await send_budget.processed(len(chunk))
            await _async_send_close_stdin(socket.send)
            deadline = time.monotonic() + _IDLE_TIMEOUT
            while True:
                raw = await asyncio.wait_for(
                    socket.recv(), timeout=max(0, deadline - time.monotonic())
                )
                frame = _parse_frame(raw)
                kind = frame.get("type")
                if kind == "heartbeat":
                    await socket.send('{"type":"heartbeat"}')
                    deadline = time.monotonic() + _IDLE_TIMEOUT
                elif kind == "stdout":
                    data = _decode_frame_data(frame)
                    states = observation.feed(data)
                    if data:
                        deadline = time.monotonic() + _IDLE_TIMEOUT
                    await receive_budget.processed(len(data))
                    for state in states:
                        result = self._accept(state, healthy)
                        if result is not None:
                            self._inline_output = observation.output
                            return result
                elif kind == "stderr":
                    data = _decode_frame_data(frame)
                    errors.extend(data[: 4096 - len(errors)])
                    await receive_budget.processed(len(data))
                elif kind == "exit":
                    if frame.get("code") == 0 and not errors:
                        raise ConnectionError("Observer exited without a result")
                    raise _public.ApiError(
                        errors.decode(errors="replace")
                        or "Observer exited without a result"
                    )
                elif kind == "error":
                    raise _public.ApiError(
                        str(frame.get("message", "Execution observation failed"))
                    )

    async def wait(self) -> _public.CommandResult:
        """Observe the task, reconnecting without executing it again."""
        failures = 0
        observed_result = False

        def healthy() -> None:
            nonlocal failures
            failures = 0

        try:
            while True:
                try:
                    state = await self._observe(healthy)
                    observed_result = True
                    stdout, stderr = (
                        self._inline_output
                        if self._inline_output is not None
                        else await self._output(state)
                    )
                    result = _public.CommandResult(
                        state.exit_code,
                        stdout,
                        stderr,
                        state.duration,
                        state.stdout_truncated,
                        state.stderr_truncated,
                    )
                    try:
                        await self.cleanup()
                    except Exception:
                        _LOG.debug(
                            "Could not clean execution %s", self.id, exc_info=True
                        )
                    return result
                except Exception as exc:
                    failures += 1
                    route_miss = (
                        isinstance(exc, InvalidStatus)
                        and exc.response.status_code == 404
                        and time.monotonic() < self._route_deadline
                        and await self._runtime._exec_route_miss_can_retry()
                    )
                    if (
                        not (_retryable_observation(exc) or route_miss)
                        or failures >= self._http.retry_max_attempts
                    ):
                        error = self._error(exc)
                        if not observed_result:
                            try:
                                cleanup = await self._short("cleanup_incomplete")
                                detail = cleanup.stdout_text.strip()
                                if detail.startswith("Incomplete execution stdin:"):
                                    error = ExecutionError(detail, self.id)
                            except Exception:
                                _LOG.debug(
                                    "Could not clean incomplete input for execution %s",
                                    self.id,
                                    exc_info=True,
                                )
                        if error is exc:
                            raise
                        raise error from exc
                    await asyncio.sleep(_delay(failures - 1, None))
        except asyncio.CancelledError:
            try:
                await self.cancel()
            except Exception:
                _LOG.debug("Could not cancel execution %s", self.id, exc_info=True)
            raise
