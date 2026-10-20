"""Running `python -m probe.core.run <action>` children for the service (plan R9, A3).

Every action, every status read and the update step run as a child: the
event stream owns its process's stdout (fd 1 is swapped for the run), which a
server answering many requests cannot give one of them, and a child keeps the
service small and lets an update replace the env the service runs from.

    argv    <canonical python> -I -m probe.core.run <action>
    stdin   the request, one JSON object
    stdout  NDJSON events schema v1 (`probe.core.events`), parsed line by line;
            a read (`status`, `version`) writes one object instead
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
from collections.abc import Callable
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


async def run_events(
    action: str,
    request: dict,
    *,
    env_extra: dict | None = None,
    on_event: Callable[[dict], None],
    on_start: Callable[[subprocess.Popen], None] | None = None,
    log_path: Path | None = None,
) -> int:
    """Run one action child, handing each event to `on_event` as it arrives.

    Returns the child's exit status (negative: killed by that signal). Raises
    OSError when it could not start.

    A plain `Popen`, its stdout read through the loop and its exit waited for
    on a thread, not `asyncio.create_subprocess_exec`: from Python 3.13 that
    child's transport KILLS a still-running child when the service exits
    (`BaseSubprocessTransport.close`, run as the service's objects are freed),
    and an action or an update must outlive a service stopped under it --
    SIGKILL in the middle of a config write or a `uv tool upgrade` is what the
    child's own signal handling exists to prevent (`probe.core.events`). The
    next service finds an action in its journal, and an update by its lock.
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
        )
    finally:
        os.close(log_fd)
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
    reader = asyncio.StreamReader(limit=MAX_EVENT_LINE)
    transport, _ = await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), child.stdout)
    try:
        while True:
            try:
                line = await reader.readline()
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
        transport.close()
    return await exited


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
