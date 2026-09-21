"""Request-scoped IO for in-process hook execution."""

from __future__ import annotations

import errno
import os
import select
import stat
import sys
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager, suppress
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


def stdout_reader_gone() -> bool:
    """Whether the harness has already left the other end of the process stdout.

    Harnesses treat some events as fire-and-forget (Cursor: sessionStart,
    sessionEnd, afterAgentResponse, ...) and close the hook's stdout before
    a slow hook answers. Knowing that up front lets the flow mark the cohort
    so the rate of departed harnesses can be measured per client and OS. The
    flow still runs in full either way: the event POST is the audit record
    and its value does not depend on who reads the response.

    Zero-timeout ``poll(2)`` on the write end, so O(1) and never blocking.
    A pipe whose read end is closed reports POLLERR on Linux and POLLHUP on
    macOS; a socket whose peer closed, or shut its write side, reports
    POLLHUP. Both flags count as gone: no harness half-closes a child's
    stdout, so the macOS SHUT_WR case is accepted as a departure too. POSIX
    only (Windows anonymous pipes have no poll(2)). Everything that is not
    the harness's channel is False: a request-local writer (daemon request,
    test) is not the process descriptor, a tty or regular file has no reader
    to lose, and any error counts as "still listening".
    """
    io = _hook_io.get()
    gone = False
    if (io is None or io.stdout is None) and sys.platform != "win32":
        with suppress(Exception):
            fd = sys.stdout.fileno()
            mode = os.fstat(fd).st_mode
            if stat.S_ISFIFO(mode) or stat.S_ISSOCK(mode):
                hangup = select.POLLERR | select.POLLHUP
                poller = select.poll()
                poller.register(fd, hangup)
                gone = any(events & hangup for _, events in poller.poll(0))
    return gone


def harness_gone(exc: OSError) -> bool:
    """Whether a stdout write failed because the harness already closed the pipe.

    Clients treat some events as fire-and-forget (Cursor: sessionStart,
    sessionEnd, afterAgentResponse, ...) and stop reading before a slow hook
    answers. POSIX reports the departed reader as EPIPE / ECONNRESET. Windows
    has no SIGPIPE: a pipe whose reader exited fails with ERROR_NO_DATA, which
    CPython maps to EINVAL rather than EPIPE, so that errno counts there only;
    elsewhere EINVAL is a genuine programming error and must keep raising.
    """
    gone = isinstance(exc, BrokenPipeError | ConnectionResetError)
    if not gone and sys.platform == "win32":
        gone = exc.errno == errno.EINVAL
    return gone


def discard_process_stdout() -> None:
    """Point the process stdout descriptor at devnull; no-op for request-local stdout.

    After a write to a pipe whose reader has gone, ``sys.stdout`` still holds
    the unflushed bytes and the interpreter retries the flush at exit. That
    retry fails the same way and prints "Exception ignored ... BrokenPipeError"
    to stderr, which hook clients treat as a hook error. Redirecting the
    descriptor at devnull lets the exit-time flush succeed silently. A
    request-local writer (daemon request, test) has no descriptor the
    interpreter would flush, so nothing is done for it.
    """
    io = _hook_io.get()
    if io is not None and io.stdout is not None:
        return
    try:
        fd = sys.stdout.fileno()
    except (OSError, ValueError):
        # Captured or replaced stream with no descriptor behind it: nothing
        # the interpreter could flush at exit.
        return
    devnull = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull, fd)
    finally:
        os.close(devnull)


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
