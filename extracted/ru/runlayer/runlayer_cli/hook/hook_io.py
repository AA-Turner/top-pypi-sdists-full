"""Request-scoped IO for in-process hook execution."""

from __future__ import annotations

import os
import sys
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import TextIO


@dataclass(frozen=True)
class HookIO:
    """Overrides for one hook request; unset values use process defaults."""

    stdin_text: str | None = None
    # Set when stdin was already consumed by a failed read: the stream is
    # unrepeatable, so replay the failure rather than a truncated remainder.
    stdin_error: BaseException | None = None
    stdout: TextIO | None = None
    stderr: TextIO | None = None
    env: Mapping[str, str] = field(default_factory=dict)
    cwd: str | None = None
    argv: Sequence[str] | None = None
    daemon_served: bool = False
    daemon_fallback: bool = False
    # Epoch-ms stamp captured at the earliest point of the client entry path
    # (Go shim start, or the thin client's module import). Feeds the flow
    # summary's startup_ms; None means no entry path stamped this request.
    client_start_ms: int | None = None


_hook_io: ContextVar[HookIO | None] = ContextVar("hook_io", default=None)


@contextmanager
def scoped(io: HookIO) -> Iterator[None]:
    """Install request IO for the current context."""
    token = _hook_io.set(io)
    try:
        yield
    finally:
        _hook_io.reset(token)


def has_request_output() -> bool:
    """Return whether both output streams are request-local."""
    io = _hook_io.get()
    return io is not None and io.stdout is not None and io.stderr is not None


def is_daemon_served() -> bool:
    """Return whether the active request arrived through daemon IPC."""
    io = _hook_io.get()
    return io is not None and io.daemon_served


def is_daemon_fallback() -> bool:
    """Return whether a gate-open daemon miss forced inline execution."""
    io = _hook_io.get()
    return io is not None and io.daemon_fallback


def client_start_ms() -> int | None:
    """Return the request's client start stamp (epoch ms), if one was captured."""
    io = _hook_io.get()
    return io.client_start_ms if io is not None else None


def read_stdin() -> str:
    io = _hook_io.get()
    if io is not None:
        if io.stdin_error is not None:
            raise io.stdin_error
        if io.stdin_text is not None:
            return io.stdin_text
    return sys.stdin.read()


def write_stdout(value: str) -> None:
    io = _hook_io.get()
    writer = io.stdout if io is not None and io.stdout is not None else sys.stdout
    writer.write(value)
    writer.flush()


def write_stderr(value: str) -> None:
    io = _hook_io.get()
    writer = io.stderr if io is not None and io.stderr is not None else sys.stderr
    writer.write(value)
    writer.flush()


def getenv(name: str, default: str | None = None) -> str | None:
    io = _hook_io.get()
    if io is not None and name in io.env:
        return io.env[name]
    return os.environ.get(name, default)


def getcwd() -> str:
    io = _hook_io.get()
    if io is not None and io.cwd is not None:
        return io.cwd
    return os.getcwd()


def abspath(path: str) -> str:
    """Absolute form of *path*, anchored at the request cwd; symlinks unresolved.

    Every relative path a hook resolves (``argv[0]``, relocation env vars) belongs
    to the invoking client, not to whatever directory this process happens to sit
    in — ``os.path.abspath`` / ``Path.absolute()`` would silently anchor it there.
    """
    return os.path.abspath(os.path.join(getcwd(), path))


def argv() -> Sequence[str]:
    io = _hook_io.get()
    if io is not None and io.argv is not None:
        return io.argv
    return sys.argv
