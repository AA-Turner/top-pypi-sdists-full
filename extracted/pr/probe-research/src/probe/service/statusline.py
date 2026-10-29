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

A marker's capture reading (`not capturing session transcript: ...`) is taken
from this service (its registration and its recorder of the session), and a
hook asks only on its own events: a session's start, a prompt, a tool call,
at most every INTERVAL_S. The reading taken at a session's start or at a
`/probe` switch lands a moment before this service registers the session or
its recorder takes it, and an idle session asks again only at its next prompt,
so its status line said "not started" or "not recording" while it was
recorded (2026-10-27). So a session that asked is FOLLOWED: every FOLLOW_S
this service compares what that reading is taken from (`readings`) with what
it was when the session's last child started, and a change refreshes it again
with that session's last request (its folder, interpreter and context), then
once more SETTLE_S later: the child also reads what this service does not
see (the `.hosted` marker, the session's switch file), which can land after
the change. A child that fails is retried at most MAX_FOLLOW_RETRIES times
for one change, its folder checked again before each (a plugin update removes
the old one: then the session is no longer followed).

Never followed or refreshed from here:
    a session Probe is off for   (`OFF`) its hooks refresh none, and a child
                                 reads the server for it (no API call for a
                                 session the person switched off)
    a request naming an endpoint (`PROBE_BASE_URL`) it was checked against
                                 the CLI config only when it asked: the
                                 config's token may follow another context
                                 by now; its hooks refresh it as before
    a session that ended         its registration, once seen, gone
Followed sessions are bounded (MAX_FOLLOWED, the oldest asked dropped); one
this service never knew is dropped FOLLOW_GRACE_S after it last asked. A new
folder past MAX_GROUPS takes the place of the idle one whose followed sessions
asked longest ago (they are no longer followed; their hooks still ask), else
it is refused and its hook fetches itself. Following
stops first at shutdown (`close`, before the recorders pause), and a child
still running is killed: one reading this service after it has gone wrote
"not started" (review of #3554).

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
from .protocol import BASE_URL_ENV

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
#: How often a followed session's capture is compared (module doc).
FOLLOW_S = 1.0
#: Sessions followed at once; past it the one that asked longest ago is dropped.
MAX_FOLLOWED = 256
#: A followed session this service never knew is dropped this long after it last asked.
FOLLOW_GRACE_S = 60.0
#: After a change's refresh, one more this long later (module doc).
SETTLE_S = 10.0
#: Children that may fail for one change of a followed session.
MAX_FOLLOW_RETRIES = 3
#: What `readings` says of a session Probe is off for: never refreshed from here.
OFF = "off"
#: A reading no session has: a failed child's session compares changed.
_UNSEEN = object()


@dataclass
class _Group:
    root: str
    python: str
    env: dict
    key: str = ""
    #: sid -> agent id (or None): the sessions to refresh at the next child.
    pending: dict = field(default_factory=dict)
    running: asyncio.Task | None = None
    timer: asyncio.TimerHandle | None = None
    last_start: float = float("-inf")  # monotonic


@dataclass
class _Followed:
    #: The group (`StatuslineRefresher.key`) and agent of the session's last request.
    key: str
    agent: str | None
    #: Its reading when its last child started (None: unknown here, or none started yet).
    seen: object = None
    asked_at: float = 0.0  # monotonic
    #: When the one more refresh after a change is due (module doc), else None.
    settle_at: float | None = None
    #: Children that failed for its reading `failed_on` (module doc: bounded).
    failures: int = 0
    failed_on: object = None
    #: This service has had it registered, or held it off: from then on, gone is ended.
    known: bool = False
    #: Seen off and not registered since: a recorder alone is not ended then.
    from_off: bool = False


class StatuslineRefresher:
    def __init__(
        self,
        *,
        log: Callable[[str], None],
        changed: Callable[[], None] = lambda: None,
        readings: Callable[[], dict] = dict,
    ) -> None:
        self.log = log
        self._changed = changed
        #: sid -> what its capture reading is taken from here, for every session
        #: this service knows, `OFF` for one Probe is off for (module doc); runs
        #: on the loop.
        self._readings = readings
        self.groups: dict[str, _Group] = {}
        #: sid -> its last request, in the order they last asked (module doc).
        self.followed: dict[str, _Followed] = {}
        self._follow_timer: asyncio.TimerHandle | None = None
        #: Refreshes a change of capture asked for, not a hook (`service.status`).
        self.followups = 0
        self._look_failing = False
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
                self._forget_followed_idle()
            if len(self.groups) >= MAX_GROUPS:
                return {"scheduled": False, "reason": "busy: too many plugin folders"}
            group = self.groups[key] = _Group(root, python, dict(env), key)
        if sid not in group.pending:
            if sum(len(g.pending) for g in self.groups.values()) >= MAX_PENDING:
                return {"scheduled": False, "reason": "busy: too many sessions waiting"}
        group.pending[sid] = agent
        if group.env.get(BASE_URL_ENV):
            self.followed.pop(sid, None)  # module doc: its hooks refresh it
        else:
            self._follow(sid, key, agent)
        return {"scheduled": True, "due_in": round(self._schedule(group), 3)}

    def _forget_idle(self) -> None:
        needed = {followed.key for followed in self.followed.values()}
        for key, group in list(self.groups.items()):
            if group.running is None and group.timer is None and not group.pending and key not in needed:
                del self.groups[key]

    def _forget_followed_idle(self) -> None:
        """Make room for a new folder: forget the idle one whose followed
        sessions asked longest ago, and stop following them (their hooks still
        ask on their events)."""
        idle = {key for key, group in self.groups.items()
                if group.running is None and group.timer is None and not group.pending}
        last: dict = {}
        for followed in self.followed.values():
            if followed.key in idle:
                last[followed.key] = max(last.get(followed.key, 0.0), followed.asked_at)
        if not last:
            return
        oldest = min(last, key=last.__getitem__)
        del self.groups[oldest]
        for sid, followed in list(self.followed.items()):
            if followed.key == oldest:
                del self.followed[sid]

    # -- following (module doc) ----------------------------------------------

    def _follow(self, sid: str, key: str, agent: str | None) -> None:
        previous = self.followed.pop(sid, None)
        if previous is not None and previous.key == key:
            previous.agent, previous.asked_at = agent, time.monotonic()
            self.followed[sid] = previous
        else:
            self.followed[sid] = _Followed(key, agent, None, time.monotonic())
        while len(self.followed) > MAX_FOLLOWED:
            self.followed.pop(next(iter(self.followed)))
        if self._follow_timer is None:
            loop = asyncio.get_running_loop()
            self._follow_timer = loop.call_later(FOLLOW_S, self._look)

    def _look(self) -> None:
        """Refresh each followed session whose capture moved since its last
        child started (and once more SETTLE_S after); drop those that ended
        or that this service never knew (module doc)."""
        self._follow_timer = None
        if self._closed or not self.followed:
            return
        readings = self._read()
        if readings is not None:
            now = time.monotonic()
            for sid, followed in list(self.followed.items()):
                group = self.groups.get(followed.key)
                reading = readings.get(sid)
                if reading == OFF or _registered(reading):
                    followed.known, followed.from_off = True, reading == OFF
                # Back on from off, a recorder can show before its registration
                # does: only gone altogether is ended then.
                ended = (followed.known and reading != OFF and not _registered(reading)
                         and (reading is None or not followed.from_off))
                if group is None or ended or (reading is None and now - followed.asked_at >= FOLLOW_GRACE_S):
                    del self.followed[sid]
                    continue
                if reading == OFF:
                    followed.seen, followed.settle_at = OFF, None
                    continue
                if followed.failures and reading != followed.failed_on:
                    followed.failures = 0  # a new change gets its own tries
                settling = followed.settle_at is not None and now >= followed.settle_at
                if (reading == followed.seen and not settling) or sid in group.pending:
                    continue
                if sum(len(g.pending) for g in self.groups.values()) >= MAX_PENDING:
                    break
                followed.settle_at = None if reading == followed.seen else now + SETTLE_S
                group.pending[sid] = followed.agent
                self.followups += 1
                self._schedule(group)
        if self.followed and not self._closed:
            self._follow_timer = asyncio.get_running_loop().call_later(FOLLOW_S, self._look)

    def _read(self) -> dict | None:
        """`readings`, or None when it fails (said once until it reads again)."""
        try:
            readings = self._readings()
        except Exception as exc:  # noqa: BLE001 -- the hooks still ask on their events
            if not self._look_failing:
                self.log(f"statusline: reading the sessions failed: {type(exc).__name__}")
            self._look_failing = True
            return None
        self._look_failing = False
        return readings if isinstance(readings, dict) else None

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
        batch = self._seen(group, batch)
        if not batch:
            if group.pending and not self._closed:
                self._schedule(group)
            self._changed()
            return
        group.last_start = time.monotonic()
        group.running = asyncio.ensure_future(self._run(group, batch))
        self._changed()

    def _seen(self, group: _Group, batch: dict) -> dict:
        """The batch a starting child refreshes: without the sessions Probe is
        off for now. Notes what each followed session of it reads now (its child
        reads no earlier, so a later change is one it may have missed); only
        for a session that last asked in this group's context, whose marker
        this child writes."""
        readings = self._read()
        if readings is None:
            # Unknown now: one last seen off stays out.
            return {sid: agent for sid, agent in batch.items()
                    if getattr(self.followed.get(sid), "seen", None) != OFF}
        kept = {}
        for sid, agent in batch.items():
            reading = readings.get(sid)
            followed = self.followed.get(sid)
            if followed is not None and followed.key == group.key:
                followed.seen = reading
            if reading != OFF:
                kept[sid] = agent
        return kept

    async def _run(self, group: _Group, batch: dict) -> None:
        request = {"sessions": [{"sid": sid, "agent": agent} for sid, agent in batch.items()]}
        code: int | None = None
        error = await asyncio.to_thread(self.check, group.root)
        if error is not None:
            # Gone or changed since it was asked (a plugin update): nothing
            # runs from it, and its sessions are no longer followed.
            for sid, followed in list(self.followed.items()):
                if followed.key == group.key:
                    del self.followed[sid]
        else:
            self.children += 1
            try:
                code = await children.run_command(
                    [group.python, "-I", self.script(group.root), "fetch-all"],
                    env=children.child_env(group.env),
                    cwd=str(paths.home()),
                    timeout=TIMEOUT_S,
                    stdin=json.dumps(request).encode("utf-8"),
                    kill_on_cancel=True,
                )
            except OSError as exc:
                error = f"could not start: {exc}"
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 -- one bad child never stops the refreshes
                error = f"failed: {exc!r}"
            if code is None and error is None:
                error = f"timed out after {TIMEOUT_S:g} s"
        self.last = {"at": time.time(), "sessions": len(batch), "exit_code": code, "error": error}
        failed = error is not None or code != 0
        if failed:
            self.log(f"statusline: refresh of {len(batch)} session(s) in {group.root}: {error or f'exit {code}'}")
        for sid in batch:
            followed = self.followed.get(sid)
            if followed is None or followed.key != group.key:
                continue
            if not failed:
                followed.failures = 0
                continue
            followed.failures += 1
            if followed.seen is not _UNSEEN:
                followed.failed_on = followed.seen
            followed.settle_at = None
            # Below the cap it compares changed (the next look tries again); at
            # it, as the reading it failed on (the next change tries again).
            followed.seen = _UNSEEN if followed.failures < MAX_FOLLOW_RETRIES else followed.failed_on
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
            "followed": len(self.followed),
            "followups": self.followups,
            "last": dict(self.last) if self.last else None,
        }

    def close(self) -> None:
        self._closed = True
        if self._follow_timer is not None:
            self._follow_timer.cancel()
            self._follow_timer = None
        for group in self.groups.values():
            if group.timer is not None:
                group.timer.cancel()
                group.timer = None
            if group.running is not None:
                with contextlib.suppress(Exception):
                    group.running.cancel()


def _registered(reading: object) -> bool:
    """Does a reading say this service has the session registered?"""
    return isinstance(reading, tuple) and bool(reading) and reading[0] is not None
