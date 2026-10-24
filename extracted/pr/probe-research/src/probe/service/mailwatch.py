"""The machine's view of what waits for the coding agents (plan Q2).

The Probe daemon's messages, the agents' asks and the held questions are plain
files (`probe.daemon.mailbox`, `probe.daemon.approvals`), and every party that
waited for one polled them on its own: an idle Claude Code session's Stop
waiter, one Python process per session, looked every 2 s for up to seven days.
Now a waiting party subscribes here and sleeps on its socket, and this service
looks at the files once for the machine and says when to look again:

    events.subscribe {topics: [mailbox.changed, approvals.changed],
                      sessions?: [sid], state_dir?: <state>/probe}
        answered once the sessions' files are baselined, so a change after the
        answer is an event: a subscriber that reads the files after the answer
        misses nothing in between. No `sessions`: every live registered one.
    every WATCH_S (IDLE_WATCH_S once nothing changed for FAST_FOR_S), on this
    module's one thread, while anyone watches:
        reads/messages/<sid>/              the names in it    -> messages
        reads/claimed/<sid>/               the folder's stamp -> claimed
        reads/asks/<sid>/ (+ .taken/)      names (+ stamp)    -> asks
        reads/requests/<sid>/ (+ .taken/)  names (+ stamp)    -> requests
        reads/turns/<sid>, <sid>.waiter    the files' stamps  -> turn, waiter
        reads/status/<sid>.json            its stamp          -> status
          => mailbox.changed {sid, parts}
        approvals/requests/*.json, approvals/answers/*.json   (only while
        someone subscribes to approvals.changed)
          => approvals.changed {sid, ids}   (the session a request names)

THE FILES STAY THE SOURCE OF TRUTH. An event only says "look again": the
subscriber reads the files with its own rules, as it did when it polled. A
change missed here costs latency, never a message, and a service that dies
loses nothing: its subscribers go back to their own poll (`reads_hook.py`).

THE PACE. An ask is answered within a few minutes of being filed, and the
waiter it replaces looked every 0.5 s while one was open and every 2 s for a
run alert or a request to the writer: so a look every WATCH_S for FAST_FOR_S
after any change (a new ask is one) or a new subscription, and every
IDLE_WATCH_S otherwise. Never slower than the poll it replaces.

NAMES, not an mtime, where a missed change would cost a wake (messages, asks,
requests): an mtime only a second fine (HFS+, some network homes) hides a
second change within that second. A folder that only fills up (claimed) and a
file rewritten in place (a turn's token) are stamped: inode, mtime, size.

Nothing runs while nobody watches: no timer, no thread. Files are opened
without blocking (a FIFO planted where a request file goes is skipped), one
session's error never costs another's events, and the looks run on a daemon
thread: a look stuck on a hung network home holds no other part of the service
and never the process's exit. No next look starts until it ends, and a
subscription whose baseline is not done in BASELINE_WAIT_S is refused (the
subscriber polls on its own).

Stdlib only.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import json
import os
import queue
import stat
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field

from . import paths
from .protocol import MailboxPart, Topic

#: Watched folders are looked at this often for FAST_FOR_S after a change or a
#: new subscription...
WATCH_S = 0.25
#: ...and this often otherwise: the waiter it replaces polled a run alert every
#: 2 s, so one idle session costs no more wakes than before, and more cost fewer.
IDLE_WATCH_S = 2.0
#: An ask's answer comes within the waiter's 150 s window (`reads_hook.WAKE_MAX_S`).
FAST_FOR_S = 180.0
#: What `events.subscribe` waits for its sessions' baseline, at most.
BASELINE_WAIT_S = 3.0
#: Sessions watched at once, at most (past it a subscription is refused).
MAX_TARGETS = 512
#: A folder holding more names than this is stamped instead (these hold a few).
MAX_NAMES = 512
#: A request file larger than this is not read for its session.
MAX_REQUEST_BYTES = 256 * 1024


def safe(session_id: str) -> str:
    """`probe.daemon.mailbox._safe`: a session id as its folder name."""
    return "".join(c for c in session_id if c.isalnum() or c in "-_") or "session"


def default_state() -> str:
    """The state folder of a session that named none: the default one."""
    return str(paths.state_dir())


def read_regular(path: str, limit: int) -> bytes | None:
    """A regular file's bytes, at most `limit`, opened without blocking and
    without following a symlink: None for anything else (a FIFO, a device, a
    folder, a file too large, one that cannot be read)."""
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOCTTY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        return None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > limit:
            return None
        chunks: list = []
        size = 0
        while size <= limit:  # to the end: a network file system may read short
            chunk = os.read(fd, limit + 1 - size)
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
    except OSError:
        return None
    finally:
        os.close(fd)
    data = b"".join(chunks)
    return data if len(data) <= limit else None


def read_json(path: str, limit: int) -> object:
    """`read_regular`'s JSON, or None for anything that is not (a nesting deep
    enough to overflow the parser included)."""
    raw = read_regular(path, limit)
    if raw is None:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, RecursionError):
        return None


class DaemonLane:
    """Calls run in order on one daemon thread. A `ThreadPoolExecutor`'s threads
    are joined when the interpreter exits, so one call stuck in a syscall (a
    hung network home) would keep the service from ever exiting, and its lock
    with it; this thread is not waited for."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._queue: queue.SimpleQueue = queue.SimpleQueue()
        self._thread: threading.Thread | None = None
        self._closed = False
        #: When the step running now started (monotonic), or None between steps.
        self._started: float | None = None

    def running_for(self) -> float:
        """How long the step running now has run (0.0 when none runs)."""
        started = self._started
        return 0.0 if started is None else max(0.0, time.monotonic() - started)

    def submit(self, fn: Callable, *args) -> concurrent.futures.Future:
        if self._closed:
            raise RuntimeError(f"{self.name} is closed")
        future: concurrent.futures.Future = concurrent.futures.Future()
        self._queue.put((future, fn, args))
        if self._thread is None:
            self._thread = threading.Thread(target=self._run, name=self.name, daemon=True)
            self._thread.start()
        return future

    def _run(self) -> None:
        while True:
            item = self._queue.get()
            if item is None:
                return
            future, fn, args = item
            if not future.set_running_or_notify_cancel():
                continue
            self._started = time.monotonic()
            try:
                future.set_result(fn(*args))
            except BaseException as exc:  # noqa: BLE001 -- handed to whoever waits
                future.set_exception(exc)
            finally:
                self._started = None

    def close(self) -> None:
        self._closed = True
        self._queue.put(None)


@dataclass(frozen=True)
class Target:
    """One watched session: its id and its state folder (`<state>/probe`)."""

    sid: str
    state: str


def _stamp(path: str) -> tuple | None:
    try:
        st = os.stat(path)
    except FileNotFoundError:
        return None
    except OSError:
        return ("unreadable",)
    return (st.st_ino, st.st_mtime_ns, st.st_size)


def _names(path: str) -> tuple | None:
    names: list = []
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                names.append(entry.name)
                if len(names) > MAX_NAMES:
                    return ("many", _stamp(path))
    except FileNotFoundError:
        return None
    except OSError:
        return ("unreadable",)
    return tuple(sorted(names))


def mailbox_signature(target: Target) -> dict:
    """What a change of `target`'s mailbox changes, part by part."""
    reads = os.path.join(target.state, "reads")
    name = safe(target.sid)
    join = os.path.join
    return {
        MailboxPart.MESSAGES: _names(join(reads, "messages", name)),
        MailboxPart.CLAIMED: _stamp(join(reads, "claimed", name)),
        MailboxPart.ASKS: (_names(join(reads, "asks", name)), _stamp(join(reads, "asks", name, ".taken"))),
        MailboxPart.REQUESTS: (
            _names(join(reads, "requests", name)),
            _stamp(join(reads, "requests", name, ".taken")),
        ),
        MailboxPart.TURN: _stamp(join(reads, "turns", name)),
        MailboxPart.WAITER: _stamp(join(reads, "turns", name + ".waiter")),
        MailboxPart.STATUS: _stamp(join(reads, "status", name + ".json")),
    }


@dataclass
class Board:
    """One state folder's approvals board, as last seen."""

    #: request file name -> (inode, mtime, size, its session id or None)
    requests: dict = field(default_factory=dict)
    answers: frozenset = frozenset()


def _request_session(path: str) -> str | None:
    """The session a held question belongs to (`probe.daemon.approvals.Request`)."""
    data = read_json(path, MAX_REQUEST_BYTES)
    sid = data.get("session_id") if isinstance(data, dict) else None
    return sid if isinstance(sid, str) and sid else None


def board_scan(state: str, old: Board | None) -> tuple[Board, dict]:
    """`state`'s board now, and `{sid: {request ids}}` changed since `old` (none
    when `old` is None: a baseline)."""
    root = os.path.join(state, "approvals")
    requests: dict = {}
    changed: dict = {}

    def note(sid: str | None, rid: str) -> None:
        if old is not None and sid:
            changed.setdefault(sid, set()).add(rid)

    try:
        with os.scandir(os.path.join(root, "requests")) as entries:
            for entry in entries:
                if not entry.name.endswith(".json") or entry.name.startswith("."):
                    continue
                try:
                    st = entry.stat(follow_symlinks=False)
                except OSError:
                    continue
                key = (st.st_ino, st.st_mtime_ns, st.st_size)
                before = old.requests.get(entry.name) if old is not None else None
                if before is not None and before[:3] == key:
                    requests[entry.name] = before
                    continue
                sid = _request_session(entry.path)
                requests[entry.name] = (*key, sid)
                note(sid, entry.name[: -len(".json")])
                if len(requests) >= MAX_NAMES:
                    break
    except OSError:
        pass
    if old is not None:
        for name, before in old.requests.items():
            if name not in requests:
                note(before[3], name[: -len(".json")])
    answers: set = set()
    try:
        with os.scandir(os.path.join(root, "answers")) as entries:
            for entry in entries:
                if entry.name.endswith(".json") and not entry.name.startswith("."):
                    answers.add(entry.name)
                if len(answers) >= MAX_NAMES:
                    break
    except OSError:
        pass
    if old is not None:
        for name in answers ^ old.answers:
            row = requests.get(name) or old.requests.get(name)
            note(row[3] if row else None, name[: -len(".json")])
    return Board(requests, frozenset(answers)), changed


class MailWatch:
    """Looks at the watched sessions' mailboxes and boards for the service.

    `targets()` is who is watched now and `boards()` whether anyone wants the
    approvals board (both asked on the loop); `emit(topic, payload)` is the
    service's event fan-out. Its state is touched only on its one thread, so a
    look and a baseline never race."""

    def __init__(
        self,
        *,
        loop_getter: Callable[[], asyncio.AbstractEventLoop | None],
        emit: Callable[[str, dict], None],
        targets: Callable[[], set],
        log: Callable[[str], None],
        boards: Callable[[], bool] = lambda: True,
        watch_s: float = WATCH_S,
        idle_watch_s: float = IDLE_WATCH_S,
    ) -> None:
        self._loop_getter = loop_getter
        self._emit = emit
        self._targets = targets
        self._boards_wanted = boards
        self._log = log
        self.watch_s = watch_s
        self.idle_watch_s = idle_watch_s
        self._mail: dict = {}
        self._boards: dict = {}
        self._lane = DaemonLane("mailwatch")
        self._handle: asyncio.TimerHandle | None = None
        self._inflight = 0
        #: When the oldest look still running was asked for (monotonic).
        self._inflight_since = 0.0
        self._closed = False
        #: Look every `watch_s` until then (monotonic), `idle_watch_s` after.
        self._fast_until = 0.0

    # -- the thread ------------------------------------------------------------

    def scan(self, targets: set, boards: bool = True) -> list:
        """One look: `[(topic, payload)]` for what changed since the last. A
        session seen for the first time is only baselined. Runs on the thread;
        one session's or one board's failure costs only its own events."""
        out: list = []
        for target in sorted(targets, key=lambda t: (t.state, t.sid)):
            try:
                now = mailbox_signature(target)
            except Exception as exc:  # noqa: BLE001 -- the others' events still go out
                self._log(f"mailbox watch: {target.sid} could not be looked at: {exc!r}")
                continue
            before = self._mail.get(target)
            self._mail[target] = now
            if before is None:
                continue
            parts = sorted(part for part, value in now.items() if before.get(part) != value)
            if parts:
                out.append((Topic.MAILBOX_CHANGED, {"sid": target.sid, "parts": parts}))
        for gone in set(self._mail) - targets:
            del self._mail[gone]
        states = {t.state for t in targets} if boards else set()
        for state in sorted(states):
            try:
                board, changed = board_scan(state, self._boards.get(state))
            except Exception as exc:  # noqa: BLE001 -- the mailboxes' events still go out
                self._log(f"mailbox watch: the approvals board under {state} could not be read: {exc!r}")
                continue
            self._boards[state] = board
            for sid in sorted(changed):
                out.append((Topic.APPROVALS_CHANGED, {"sid": sid, "ids": sorted(changed[sid])}))
        for gone in set(self._boards) - states:
            del self._boards[gone]
        return out

    # -- the loop --------------------------------------------------------------

    def _submit(self, loop: asyncio.AbstractEventLoop, targets: set) -> asyncio.Future | None:
        try:
            future = asyncio.wrap_future(self._lane.submit(self.scan, targets, self._boards_wanted()), loop=loop)
        except RuntimeError:
            return None  # closed: the service is stopping
        if not self._inflight:
            self._inflight_since = time.monotonic()
        self._inflight += 1
        future.add_done_callback(self._scanned)
        return future

    def _scanned(self, future: asyncio.Future) -> None:
        self._inflight -= 1
        if future.cancelled():
            return
        exc = future.exception()
        if exc is not None:
            self._log(f"mailbox watch: a look failed: {exc!r}")
            return
        events = future.result()
        if events:
            self._go_fast()
        for topic, payload in events:
            self._emit(topic, payload)

    def count(self) -> int:
        """How many sessions are watched now."""
        return len(self._targets())

    async def baseline(self) -> bool:
        """Baseline every watched session not seen yet (a new subscription's)
        and look at the others: True once done, False past BASELINE_WAIT_S (a
        hung folder: the caller refuses the subscription)."""
        loop = asyncio.get_running_loop()
        if self._closed:
            return False
        if self._inflight and time.monotonic() - self._inflight_since > BASELINE_WAIT_S:
            return False  # a look is stuck (a hung folder): never queue more behind it
        self._go_fast()
        future = self._submit(loop, self._targets())
        if future is None:
            return False
        done, _ = await asyncio.wait({future}, timeout=BASELINE_WAIT_S)
        self.changed()
        return bool(done) and not future.cancelled() and future.exception() is None

    def _pace(self) -> float:
        return self.watch_s if time.monotonic() < self._fast_until else self.idle_watch_s

    def _go_fast(self) -> None:
        """Look every `watch_s` for FAST_FOR_S from now, starting with the next
        look: one already set at the idle pace is brought forward."""
        self._fast_until = time.monotonic() + FAST_FOR_S
        loop = self._loop_getter()
        handle = self._handle
        if loop is not None and handle is not None and handle.when() > loop.time() + self.watch_s:
            handle.cancel()
            self._handle = loop.call_later(self.watch_s, self._tick)

    def changed(self) -> None:
        """Who watches may have changed: start looking when someone does."""
        if self._closed or self._handle is not None:
            return
        loop = self._loop_getter()
        if loop is None or not self._targets():
            return
        self._handle = loop.call_later(self._pace(), self._tick)

    def _tick(self) -> None:
        self._handle = None
        loop = self._loop_getter()
        if self._closed or loop is None:
            return
        targets = self._targets()
        if not targets:
            if not self._inflight:
                self._mail.clear()  # the thread is idle: nothing else touches these now
                self._boards.clear()
            return
        if not self._inflight:
            self._submit(loop, targets)
        self._handle = loop.call_later(self._pace(), self._tick)

    def close(self) -> None:
        self._closed = True
        if self._handle is not None:
            self._handle.cancel()
            self._handle = None
        self._lane.close()


__all__ = [
    "BASELINE_WAIT_S", "Board", "DaemonLane", "MailWatch", "Target", "WATCH_S", "board_scan", "mailbox_signature",
    "read_json", "read_regular",
]
