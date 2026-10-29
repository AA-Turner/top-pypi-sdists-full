"""Running `python -m probe.core.run <action>` children for the service (plan R9, A3).

Every action, every status read and the update step run as a child: the
event stream owns its process's stdout (fd 1 is swapped for the run), which a
server answering many requests cannot give one of them, and a child keeps the
service small and lets an update replace the env the service runs from.

    argv    <canonical python> -I -m probe.core.run <action>
    stdin   the request, one JSON object
    stdout  NDJSON events schema v1 (`probe.core.events`), parsed line by line;
            a read (`status`, `version`, `desktop`) writes one object instead
    stderr  the action's log file
    cwd     $HOME
    env     the service's own clean env (it started with one, `client.ENV_ALLOWLIST`)
            plus the request's declared context (`protocol.need_context`) and
            what the service itself sets (the update trigger, the barrier token):
            never the first launcher's tokens or endpoint (plan X2)

The canonical python is the CLI's own interpreter, `runtime.json` (what
`ensure` starts the service with), read again for each child: a CLI that moved
its env since the service started is followed.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import subprocess
import sys
import threading
import time
from collections.abc import Awaitable, Callable
from pathlib import Path

from . import paths

CORE_MODULE = "probe.core.run"
#: An NDJSON line longer than this is dropped (and the next one read).
MAX_EVENT_LINE = 1024 * 1024


def core_python() -> str:
    """The CLI's interpreter (`runtime.json`, else the uv tool env's), else this one."""
    from . import client

    return client.runtime_python() or sys.executable


def core_argv(action: str) -> list[str]:
    return [core_python(), "-I", "-m", CORE_MODULE, action]


#: `probe <args>` (`probe/cli/__main__.py`, in every CLI the service may find
#: in `runtime.json`). The service starts none while its own in-place update
#: replaces those files (`notesync.NoteSync`'s `held`).
CLI_MODULE = "probe.cli"


#: `paths.SERVICE_CHILD_ENV` (its one definition), on every `probe` this
#: service starts itself.
SERVICE_CHILD_ENV = paths.SERVICE_CHILD_ENV


def cli_argv(args: list[str]) -> list[str]:
    """`probe <args>`, run by the CLI's own interpreter. Its environment is to
    carry SERVICE_CHILD_ENV (`cli_env`)."""
    return [core_python(), "-I", "-m", CLI_MODULE, *args]


def cli_env(extra: dict | None = None) -> dict:
    """`child_env` for a `probe` this service starts (`cli_argv`): marked
    SERVICE_CHILD_ENV."""
    return child_env({**(extra or {}), SERVICE_CHILD_ENV: "1"})


def _kill_group(pid: int) -> None:
    """SIGKILL the child's whole process group (it was started as its leader)."""
    import signal

    with contextlib.suppress(ProcessLookupError, PermissionError, OSError):
        os.killpg(pid, signal.SIGKILL)


def spawn_watched(
    argv: list[str],
    *,
    env: dict,
    cwd: str,
    on_exit: Callable[[int], None],
    stdin: bytes = b"",
    log_path: Path | None = None,
    log_fd: int | None = None,
    stdin_by: float | None = None,
) -> subprocess.Popen:
    """Start `argv` in a session of its own and call `on_exit(status)` on the
    loop once it exits (negative: killed by that signal). A plain `Popen`
    waited for on a thread, as `run_events` explains: the child outlives a
    service stopped under it. `stdin` is written to it on a thread of its own,
    then closed, given up at `stdin_by` (time.monotonic()) if the child has not
    taken it all. Its stdout and stderr go to `log_fd` (taken over: closed
    here), else `log_path` (appended), else nowhere. Raises OSError when it
    could not start."""
    loop = asyncio.get_running_loop()
    if log_fd is None:
        log_fd = _open_log(log_path)
    try:
        child = subprocess.Popen(  # noqa: S603 -- an interpreter and a module or script of Probe's own
            argv,
            stdin=subprocess.PIPE if stdin else subprocess.DEVNULL,
            stdout=log_fd,
            stderr=log_fd,
            cwd=cwd,
            env=env,
            close_fds=True,
            start_new_session=True,
        )
    finally:
        os.close(log_fd)

    if stdin:
        # Never on the loop, and never in the way of the wait below: a request
        # bigger than the pipe holds (a status-line batch passes 8 KiB) waits
        # for the child to read it, which a slow child may do late or never,
        # and a descendant that left its group (setsid) keeping stdin outlives
        # the group kill (`run_command`), so the write would wait on it forever.
        assert child.stdin is not None
        fd = os.dup(child.stdin.fileno())
        with contextlib.suppress(OSError, ValueError):
            child.stdin.close()
        child.stdin = None
        threading.Thread(target=_feed, args=(fd, stdin, stdin_by), name=f"probe-stdin-{child.pid}",
                         daemon=True).start()

    def wait() -> None:
        code = child.wait()
        with contextlib.suppress(RuntimeError):  # the loop is closed: the service went first
            loop.call_soon_threadsafe(on_exit, code)

    threading.Thread(target=wait, name=f"probe-child-{child.pid}", daemon=True).start()
    return child


#: How long a non-blocking stdin write waits for room per try.
_FEED_POLL_S = 0.25


def _feed(fd: int, data: bytes, by: float | None) -> None:
    """Write `data` to `fd`, then close it: in pieces as the reader makes room
    (POSIX: non-blocking, so `by` bounds it however the reader behaves), all of
    it before `by` or as much as fits by then. A reader gone ends it (EPIPE)."""
    import select
    import time

    try:
        if os.name == "nt":  # no select on pipes: as before, bounded by the reader
            with contextlib.suppress(OSError):
                os.write(fd, data)
            return
        os.set_blocking(fd, False)
        view = memoryview(data)
        while view:
            left = None if by is None else by - time.monotonic()
            if left is not None and left <= 0:
                return
            try:
                _, ready, _ = select.select([], [fd], [], _FEED_POLL_S if left is None else min(left, _FEED_POLL_S))
            except (OSError, ValueError):
                return
            if not ready:
                continue
            try:
                view = view[os.write(fd, view):]
            except BlockingIOError:
                continue
            except OSError:
                return
    finally:
        with contextlib.suppress(OSError):
            os.close(fd)


async def run_command(
    argv: list[str],
    *,
    env: dict,
    cwd: str,
    timeout: float,
    stdin: bytes = b"",
    log_path: Path | None = None,
    kill_on_cancel: bool = False,
) -> int | None:
    """Run `argv` to its end (`spawn_watched`): its exit status, or None when
    it ran past `timeout` (then its whole process group is killed). Raises
    OSError when it could not start. With `kill_on_cancel`, a cancelled wait
    kills it too (a child that must not outlive this service: a status-line
    refresh reading the service's state after it has gone writes a wrong one)."""
    loop = asyncio.get_running_loop()
    exited: asyncio.Future = loop.create_future()

    def settle(code: int) -> None:
        if not exited.done():
            exited.set_result(code)

    child = spawn_watched(argv, env=env, cwd=cwd, on_exit=settle, stdin=stdin, log_path=log_path,
                          stdin_by=time.monotonic() + timeout)
    try:
        return await asyncio.wait_for(asyncio.shield(exited), timeout)
    except asyncio.TimeoutError:
        if not exited.done():  # still ours: its pid cannot have been reused yet
            _kill_group(child.pid)
        return None
    except asyncio.CancelledError:
        if kill_on_cancel and not exited.done():
            _kill_group(child.pid)
        raise


def child_env(extra: dict | None = None) -> dict:
    """The service's own environment plus `extra` (a request's context)."""
    env = dict(os.environ)
    env.update(extra or {})
    return env


def _open_log(path: Path | None) -> int:
    if path is None:
        return os.open(os.devnull, os.O_WRONLY)
    paths.private_dir(path.parent)
    return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)


#: After the SIGKILL, how long what was stopped is waited for (a process the
#: kernel holds, in D state, outlives even that).
KILL_WAIT_S = 5.0
#: How often a stopping process and its group are looked at.
STOP_POLL_S = 0.1


class Stopped:
    """How `stop` ended."""

    #: Nothing was left to stop: nothing was sent.
    GONE = "gone"
    #: Everything was gone within the grace.
    SIGTERM = "SIGTERM"
    #: Something was still there past the grace (the process or a command of
    #: its group), and the SIGKILL ended it.
    SIGKILL = "SIGKILL"
    #: Still there after the SIGKILL.
    RUNNING = "running"


#: While its group is still its own, the group's members are listed this often,
#: so a command started meanwhile is known before it is needed.
LOOK_EVERY_S = 0.5


async def stop(
    *,
    leader: Callable[[], Awaitable[bool]],
    send: Callable[[int], None],
    group: int | None,
    grace: float,
) -> str:
    """SIGTERM, then SIGKILL past `grace`, a process and (`group`: the pgid it
    leads, POSIX) every member of its group, until none is running; how it
    ended (`Stopped`). `leader()`: is the process still there, and still that
    one (the caller's identity check). Without a group, `send(sig)` signals
    it, only right after `leader()` said yes. Cancelled, it sends nothing more.

    A group's number is its own only while a process of the group is there:
    once all are gone the number can name another group. So the group is
    anchored by the leader, or by a member listed while it was anchored, each
    still that process (pid and kernel start time, `procid.alive`; a zombie is
    gone) and still in the group (one that left it is neither an anchor nor
    signalled: a daemon the run started on purpose); it is listed, and
    signalled with `killpg`, only right after such an anchor answered, never
    otherwise. A member nobody could list in time (one
    started after the last listing, once every anchor is gone) is never
    signalled: the stop then ends `RUNNING`, never claiming the group is gone.
    A command that ignores SIGTERM is killed too. SIGTERM first: the child's
    own handler (`probe.core.events`) ends a run through its `finally` blocks --
    its locks let go, what it records written, `done` last -- and kills the
    command it was running."""
    import signal

    from . import procid

    known: dict[int, str] = {}
    looked = [float("-inf")]

    def still_member(pid: int, start: str) -> bool:
        # Still that process, and still in the group: one that left it (setsid,
        # setpgid) anchors nothing, and is not this stop's to signal.
        if procid.alive(pid, start) is not True:
            return False
        try:
            return os.getpgid(pid) == group
        except OSError:
            return False

    async def anchored() -> bool:
        if await leader():
            return True
        for pid, start in list(known.items()):
            if await asyncio.to_thread(still_member, pid, start):
                return True
        return False

    async def look(*, now: bool = False) -> None:
        if group is None or (not now and time.monotonic() - looked[0] < LOOK_EVERY_S):
            return
        looked[0] = time.monotonic()
        if not await anchored():
            return
        found = await asyncio.to_thread(procid.members, group)
        if await anchored():  # still its own after the listing: these are its members
            known.update(found)

    async def running() -> bool:
        if group is None:
            return await leader()
        if not await anchored():
            return False
        await look()
        return True

    async def signal_all(sig: int) -> None:
        if group is None:
            if await leader():
                with contextlib.suppress(OSError):
                    send(sig)
            return
        await look(now=True)
        if await anchored():
            with contextlib.suppress(OSError):
                os.killpg(group, sig)

    async def gone_within(seconds: float) -> bool:
        deadline = time.monotonic() + seconds
        while await running():
            if time.monotonic() >= deadline:
                return False
            await asyncio.sleep(STOP_POLL_S)
        return True

    async def strays() -> bool:
        return group is not None and bool(await asyncio.to_thread(procid.members, group))

    if not await running():
        return Stopped.GONE
    await signal_all(signal.SIGTERM)
    if await gone_within(grace):
        return Stopped.RUNNING if await strays() else Stopped.SIGTERM
    await signal_all(getattr(signal, "SIGKILL", signal.SIGTERM))  # Windows: TerminateProcess either way
    if await gone_within(KILL_WAIT_S):
        return Stopped.RUNNING if await strays() else Stopped.SIGKILL
    return Stopped.RUNNING


class Overran(Exception):
    """`run_events`' child ran past its `timeout` and was stopped (`stop`):
    `code` is its exit status (negative: the signal; None: not seen to exit),
    `how` the `Stopped` that ended it."""

    def __init__(self, code: int | None, how: str) -> None:
        super().__init__(f"ran past its time limit and was stopped (exit {code}, {how})")
        self.code = code
        self.how = how


async def _stop_overrun(
    child: subprocess.Popen, exited: asyncio.Future, grace: float, start: str | None
) -> Overran:
    """`stop` for `run_events`' own child past its time limit: the leader of
    its group (POSIX), still that process while it is not yet reaped and its
    kernel start time is still `start` (read as it started: `Popen.wait` reaps
    a moment before it sets `returncode`). Windows, where no update runs: the
    child alone."""
    from . import procid

    async def leader() -> bool:
        if child.returncode is not None or exited.done():
            return False
        if start is None:
            # No identity to prove it by: on POSIX nothing is signalled (the
            # stop ends `RUNNING`). Windows signals through the process's own
            # handle, which a reused pid cannot take over.
            return os.name == "nt"
        return await asyncio.to_thread(procid.alive, child.pid, start) is True

    def send(sig: int) -> None:
        child.kill()  # Windows only: POSIX signals its group (`stop`)

    if start is None and os.name != "nt":
        how = Stopped.RUNNING  # nothing sent: nothing proves the pid is still its own
    else:
        how = await stop(leader=leader, send=send, group=None if os.name == "nt" else child.pid, grace=grace)
    code = child.returncode  # set by its waiter as it reaps it, before `exited`
    if code is None:
        try:
            code = await asyncio.wait_for(asyncio.shield(exited), STOP_POLL_S * 10)
        except asyncio.TimeoutError:
            code = None
    return Overran(code, how)


async def run_events(
    action: str,
    request: dict,
    *,
    env_extra: dict | None = None,
    on_event: Callable[[dict], None],
    on_start: Callable[[subprocess.Popen], None] | None = None,
    log_path: Path | None = None,
    timeout: float | None = None,
    grace: float = 30.0,
) -> int:
    """Run one action child, handing each event to `on_event` as it arrives.

    Returns the child's exit status (negative: killed by that signal). Raises
    OSError when it could not start, and `Overran` once a child still running
    at `timeout` (seconds from its start; None: no limit) has been stopped:
    SIGTERM to its process group, then SIGKILL past `grace` to what is left of
    it (`stop`). A child with a timeout leads a process group of its own
    (POSIX), so the stop reaches the commands it started too.

    A plain `Popen`, its stdout read through the loop and its exit waited for
    on a thread, not `asyncio.create_subprocess_exec`: from Python 3.13 that
    child's transport KILLS a still-running child when the service exits
    (`BaseSubprocessTransport.close`, run as the service's objects are freed),
    and an action or an update must outlive a service stopped under it --
    SIGKILL in the middle of a config write or a `uv tool upgrade` is what the
    child's own signal handling exists to prevent (`probe.core.events`). The
    next service finds an action in its journal, and an update by its lock.
    The time limit is this service's alone: cancelled (the service stops),
    this stops reading and leaves the child running, timeout or not.
    """
    loop = asyncio.get_running_loop()
    log_fd = _open_log(log_path)
    try:
        child = subprocess.Popen(  # noqa: S603 -- the CLI's own interpreter, our own module
            core_argv(action),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=log_fd,
            cwd=str(paths.home()),
            env=child_env(env_extra),
            close_fds=True,
            # Windows: its own process group in the service's (hidden) console,
            # so `action.cancel`'s CTRL_BREAK reaches it and nothing else.
            creationflags=0x00000200 if os.name == "nt" else 0,  # CREATE_NEW_PROCESS_GROUP
            # POSIX, with a time limit: the leader of a group of its own, which
            # the stop at the limit signals whole (`_stop_overrun`).
            start_new_session=timeout is not None and os.name != "nt",
        )
    finally:
        os.close(log_fd)
    started = None
    if timeout is not None and os.name != "nt":
        from . import procid

        # Its identity, for the stop at the limit (`_stop_overrun`).
        started = procid.start_time(child.pid)
    exited: asyncio.Future = loop.create_future()

    def wait() -> None:
        code = child.wait()

        def settle() -> None:
            if not exited.done():
                exited.set_result(code)

        with contextlib.suppress(RuntimeError):  # the loop is closed: the service went first
            loop.call_soon_threadsafe(settle)

    threading.Thread(target=wait, name=f"probe-child-{child.pid}", daemon=True).start()
    if on_start is not None:
        on_start(child)
    assert child.stdin is not None and child.stdout is not None
    # One small JSON object (`probe.core.requests` checked it), read whole by
    # the child at its start: it fits the pipe, so this does not block.
    with contextlib.suppress(OSError, ValueError):
        child.stdin.write(json.dumps(request).encode("utf-8"))
    with contextlib.suppress(OSError):
        child.stdin.close()
    if os.name == "nt":
        # Windows: the proactor reads only overlapped pipe HANDLEs, and this is
        # an ordinary one: a thread reads it and hands each line to the loop.
        lines: asyncio.Queue = asyncio.Queue()

        def pump() -> None:
            try:
                for raw in child.stdout:
                    if len(raw) <= MAX_EVENT_LINE:
                        loop.call_soon_threadsafe(lines.put_nowait, raw)
            except (OSError, ValueError):
                pass
            finally:
                with contextlib.suppress(RuntimeError):
                    loop.call_soon_threadsafe(lines.put_nowait, b"")

        threading.Thread(target=pump, name=f"probe-child-out-{child.pid}", daemon=True).start()
        reader = None
        transport = None
    else:
        reader = asyncio.StreamReader(limit=MAX_EVENT_LINE)
        transport, _ = await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), child.stdout)

    async def read() -> int:
        try:
            while True:
                try:
                    line = await (reader.readline() if reader is not None else lines.get())
                except ValueError:  # a line over MAX_EVENT_LINE: dropped, the reader goes on
                    continue
                if not line:
                    break
                try:
                    event = json.loads(line.decode("utf-8"))
                except (UnicodeDecodeError, ValueError):
                    continue
                if isinstance(event, dict) and isinstance(event.get("event"), str):
                    on_event(event)
        finally:
            # Our end of its stdout only: a child we stop reading goes on without
            # its events (`probe.core.events.emit`), never killed.
            if transport is not None:
                transport.close()
        return await exited

    if timeout is None:
        return await read()
    reading = loop.create_task(read())
    try:
        finished, _ = await asyncio.wait({reading}, timeout=timeout)
    except asyncio.CancelledError:
        reading.cancel()  # the reader only: the child goes on (above)
        raise
    if finished:
        return reading.result()
    # The reader goes once the child is stopped: cancelled, not awaited (that
    # would swallow a cancellation of this call), its outcome taken.
    reading.add_done_callback(lambda task: task.cancelled() or task.exception())
    if exited.done() or child.returncode is not None:
        # The child itself ended (its waiter may not have said so yet);
        # something it left behind holds its stdout.
        reading.cancel()
        return exited.result() if exited.done() else child.returncode
    # Still running at its limit. Its events are read while it is stopped: its
    # `done` says how it ended.
    try:
        overran = await _stop_overrun(child, exited, grace, started)
    finally:
        reading.cancel()
    raise overran


async def run_once(
    action: str,
    payload: bytes,
    *,
    env_extra: dict | None = None,
    timeout: float,
    kill: bool,
    max_output: int,
    on_exit: Callable[[], None] | None = None,
    on_start: Callable[[subprocess.Popen], None] | None = None,
) -> tuple[int | None, bytes, bool]:
    """Run one child that reads `payload` and writes one answer (`desktop`):
    `(exit status, its stdout up to max_output, whether there was more)`, or
    `(None, b"", False)` when it is still running at `timeout`. Then it is
    killed only with `kill` (a read); a child that may be writing (a change)
    goes on, its stdout still drained so it never blocks on a full pipe.
    `on_start` is called with the child right after it starts, on the loop;
    `on_exit` is called on the loop once the child has exited, also after
    its caller stopped waiting. Raises OSError when it could not start.

    A plain `Popen` on a daemon thread, as `run_events` and for its reason:
    a child the service stops under must never be killed by the service's
    own exit (asyncio's transport does that from Python 3.13), and a stopping
    service never waits for it either."""
    loop = asyncio.get_running_loop()
    child = subprocess.Popen(  # noqa: S603 -- the CLI's own interpreter, our own module
        core_argv(action),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=str(paths.home()),
        env=child_env(env_extra),
        close_fds=True,
    )
    answered: asyncio.Future = loop.create_future()

    def work() -> None:
        assert child.stdin is not None and child.stdout is not None
        out = bytearray()
        more = False
        # The payload may pass the pipe's buffer: written here, never on the loop.
        with contextlib.suppress(OSError, ValueError):
            child.stdin.write(payload)
        with contextlib.suppress(OSError, ValueError):
            child.stdin.close()
        with contextlib.suppress(OSError, ValueError):
            while True:
                chunk = child.stdout.read(65536)
                if not chunk:
                    break
                room = max_output - len(out)
                if len(chunk) > room:
                    more = True
                out += chunk[: max(room, 0)]
        code = child.wait()

        def settle() -> None:
            if not answered.done():
                answered.set_result((code, bytes(out), more))
            if on_exit is not None:
                on_exit()

        with contextlib.suppress(RuntimeError):  # the loop is closed: the service went first
            loop.call_soon_threadsafe(settle)

    if on_start is not None:
        on_start(child)
    threading.Thread(target=work, name=f"probe-child-{child.pid}", daemon=True).start()
    try:
        return await asyncio.wait_for(asyncio.shield(answered), timeout)
    except asyncio.TimeoutError:
        if kill:
            with contextlib.suppress(OSError):
                child.kill()
        return None, b"", False


async def run_read(
    action: str,
    request: dict,
    *,
    env_extra: dict | None = None,
    timeout: float,
) -> tuple[int | None, object]:
    """Run a read child (`status`, `version`): `(exit status, its one JSON
    value or None)`. A child past `timeout` is killed: `(None, None)`.
    Raises OSError when it could not start."""
    child = await asyncio.create_subprocess_exec(
        *core_argv(action),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
        cwd=str(paths.home()),
        env=child_env(env_extra),
    )
    try:
        out, _ = await asyncio.wait_for(child.communicate(json.dumps(request).encode("utf-8")), timeout)
    except asyncio.TimeoutError:
        with contextlib.suppress(ProcessLookupError):
            child.kill()
        with contextlib.suppress(Exception):
            await child.wait()
        return None, None
    try:
        value = json.loads(out.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        value = None
    return child.returncode, value
