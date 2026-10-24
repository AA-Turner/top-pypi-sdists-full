"""`statusline.refresh`: the status line's server read, once per machine on the service's schedule (plan Q4).

A session's status line renders from a marker file (`<state>/probe/sessions/
<sid>.json`) that the plugin's `hooks/statusline_refresh.py` keeps warm: its
hook used to hand every due refresh (a session's start, then at most every
INTERVAL_S per session) to a detached copy of itself, which made four API
reads and wrote that session's marker. Where a service answers, the hook asks
it instead and returns:

    one child per plugin folder   `<python> -I <root>/hooks/statusline_refresh.py
                                  fetch-all`, the request on stdin: the
                                  sessions that asked since the last one, each
                                  marker written by the plugin's own code, as
                                  the detached fetch wrote it
    on the service's schedule     at most one child in flight per folder, the
                                  next one INTERVAL_S after the last one
                                  started (GATHER_S after a quiet spell); a
                                  request meanwhile joins it
    the caller's context          its config, state and network variables
                                  (`protocol.CONTEXT_ENV`): the marker lands
                                  where the renderer reads it, read with the
                                  credential the CLI config holds
    bounded                       MAX_BATCH sessions per child, MAX_GROUPS
                                  folders, MAX_PENDING sessions waiting, a
                                  child past TIMEOUT_S killed

The folder is checked as `hooks.host` checks it (a Probe plugin folder of this
user's, `hookhosts.probe_plugin`) and the script must be there; the
interpreter is the caller's when it is a 3.9 or newer, as for a hook host.
A caller in a sandbox is refused (its child would run outside it). The
renderer is unchanged: it reads the marker file, never the service.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field

from . import children, paths

#: hooks/statusline_refresh.py REFRESH_SECONDS: a session's refresh at most this often.
INTERVAL_S = 5.0
#: A folder's first child after a quiet spell waits this long, so the
#: sessions asking together (a burst of hooks) share it.
GATHER_S = 0.25
#: A child past this is killed (each session is four reads of at most 10 s each).
TIMEOUT_S = 60.0
#: Sessions one child refreshes; the rest wait for the next.
MAX_BATCH = 32
#: Plugin folders (and contexts) refreshed at once; past it a request is refused.
MAX_GROUPS = 8
#: Sessions waiting across every folder; past it a request is refused.
MAX_PENDING = 256
#: A folder's check is trusted this long (a plugin update replaces the folder).
CHECK_TTL_S = 60.0
SCRIPT = ("hooks", "statusline_refresh.py")


@dataclass
class _Group:
    root: str
    python: str
    env: dict
    #: sid -> agent id (or None): the sessions to refresh at the next child.
    pending: dict = field(default_factory=dict)
    running: asyncio.Task | None = None
    timer: asyncio.TimerHandle | None = None
    last_start: float = float("-inf")  # monotonic


class StatuslineRefresher:
    def __init__(self, *, log: Callable[[str], None], changed: Callable[[], None] = lambda: None) -> None:
        self.log = log
        self._changed = changed
        self.groups: dict[str, _Group] = {}
        #: plugin folder -> (monotonic, verdict) from `check` (worker threads: the lock)
        self._checked: dict[str, tuple[float, str | None]] = {}
        self._check_lock = threading.Lock()
        self._closed = False
        #: Children run so far, and the last one's outcome (`service.status`).
        self.children = 0
        self.last: dict | None = None

    @staticmethod
    def key(root: str, python: str, env: dict) -> str:
        return json.dumps([root, python, sorted(env.items())])

    def script(self, root: str) -> str:
        return "/".join((root.rstrip("/"), *SCRIPT))

    # -- checks (blocking: a worker thread) ----------------------------------

    def check(self, root: str) -> str | None:
        """None when `root` (a real path) is a Probe plugin folder of this
        user's with the refresh script, else why not. Reads files: never on
        the loop."""
        import os
        from pathlib import Path

        from .hookhosts import probe_plugin, read_plugin_file

        now = time.monotonic()
        with self._check_lock:
            cached = self._checked.get(root)
        if cached is not None and now - cached[0] < CHECK_TTL_S:
            return cached[1]
        verdict = None
        folder = Path(root)
        if os.name != "posix":
            verdict = "POSIX only"
        elif not probe_plugin(folder):
            verdict = "not a Probe plugin folder"
        elif read_plugin_file(folder.joinpath(*SCRIPT)) is None:
            verdict = "the plugin folder has no status-line refresh"
        with self._check_lock:
            self._checked[root] = (now, verdict)
            while len(self._checked) > 4 * MAX_GROUPS:
                self._checked.pop(next(iter(self._checked)))
        return verdict

    # -- requests (the loop) --------------------------------------------------

    def request(self, root: str, python: str, env: dict, sid: str, agent: str | None) -> dict:
        """Refresh `sid`'s marker at the folder's next child: `{scheduled:
        true, due_in}` (seconds until that child starts), or `{scheduled:
        false, reason}` (the hook then runs its own detached fetch)."""
        if self._closed:
            return {"scheduled": False, "reason": "the service is stopping"}
        key = self.key(root, python, env)
        group = self.groups.get(key)
        if group is None:
            if len(self.groups) >= MAX_GROUPS:
                self._forget_idle()
            if len(self.groups) >= MAX_GROUPS:
                return {"scheduled": False, "reason": "busy: too many plugin folders"}
            group = self.groups[key] = _Group(root, python, dict(env))
        if sid not in group.pending:
            if sum(len(g.pending) for g in self.groups.values()) >= MAX_PENDING:
                return {"scheduled": False, "reason": "busy: too many sessions waiting"}
        group.pending[sid] = agent
        return {"scheduled": True, "due_in": round(self._schedule(group), 3)}

    def _forget_idle(self) -> None:
        for key, group in list(self.groups.items()):
            if group.running is None and group.timer is None and not group.pending:
                del self.groups[key]

    def _schedule(self, group: _Group) -> float:
        """Seconds until `group`'s next child starts (a timer set when none is)."""
        if group.running is not None:
            # It schedules the next one when it ends.
            return max(0.0, group.last_start + INTERVAL_S - time.monotonic())
        delay = max(GATHER_S, group.last_start + INTERVAL_S - time.monotonic())
        if group.timer is None:
            loop = asyncio.get_running_loop()
            group.timer = loop.call_later(delay, self._start, group)
            self._changed()
        return delay

    def _start(self, group: _Group) -> None:
        group.timer = None
        if self._closed or group.running is not None or not group.pending:
            return
        batch = dict(list(group.pending.items())[:MAX_BATCH])
        for sid in batch:
            del group.pending[sid]
        group.last_start = time.monotonic()
        group.running = asyncio.ensure_future(self._run(group, batch))
        self._changed()

    async def _run(self, group: _Group, batch: dict) -> None:
        request = {"sessions": [{"sid": sid, "agent": agent} for sid, agent in batch.items()]}
        self.children += 1
        code: int | None
        error = None
        try:
            code = await children.run_command(
                [group.python, "-I", self.script(group.root), "fetch-all"],
                env=children.child_env(group.env),
                cwd=str(paths.home()),
                timeout=TIMEOUT_S,
                stdin=json.dumps(request).encode("utf-8"),
            )
        except OSError as exc:
            code, error = None, f"could not start: {exc}"
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 -- one bad child never stops the refreshes
            code, error = None, f"failed: {exc!r}"
        if code is None and error is None:
            error = f"timed out after {TIMEOUT_S:g} s"
        self.last = {"at": time.time(), "sessions": len(batch), "exit_code": code, "error": error}
        if error is not None or code != 0:
            self.log(f"statusline: refresh of {len(batch)} session(s) in {group.root}: {error or f'exit {code}'}")
        group.running = None
        if group.pending and not self._closed:
            self._schedule(group)
        self._changed()

    # -- state ----------------------------------------------------------------

    def in_flight(self) -> bool:
        return any(g.running is not None or g.timer is not None for g in self.groups.values())

    def public(self) -> dict:
        return {
            "folders": len(self.groups),
            "waiting": sum(len(g.pending) for g in self.groups.values()),
            "running": sum(1 for g in self.groups.values() if g.running is not None),
            "children": self.children,
            "last": dict(self.last) if self.last else None,
        }

    def close(self) -> None:
        self._closed = True
        for group in self.groups.values():
            if group.timer is not None:
                group.timer.cancel()
                group.timer = None
            if group.running is not None:
                with contextlib.suppress(Exception):
                    group.running.cancel()
