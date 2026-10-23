"""Hook events' record-keeping routes, queued for the service to run once (plan D36).

    hooks.queue {id, plugin_root, lane, payload, env, cwd, at}
                a session's dispatcher found no warm host for an event: it ran
                there only what the agent waits on (a decision, context, a
                message) and hands this the routes whose outcome nobody waits
                on (routes.json `"record_keeping": true`: telemetry, the status
                line's refresh, the team note's push). Stored here, then run
                once on the folder's warm host, else as a fresh
                `hooks/dispatch.sh <lane> --record-keeping`, on a thread of
                this queue's, never the service's loop.

The queue is a folder, `paths.hook_queue_dir()` (0700, under the service's
own), one file per event, so a dispatcher with no service to ask writes there
itself (`hooks/dispatch.py` `write_queued`) and the next service to start runs
it:

    <id>.json   waiting: the event as `protocol.need_hook_queue` reads it,
                written whole (a temporary file renamed into place), 0600
    <id>.done   taken: renamed from `<id>.json` the moment before it runs and
                emptied, then kept TOMBSTONE_S, so an id sent twice (the
                dispatcher gave up waiting for the answer and wrote it beside)
                runs once, and a service stopped while it ran never runs it
                again (at most once: a lost telemetry event beats a doubled one)
    <id>.claim  made (O_EXCL) by whichever runs an event whose request went
                unanswered: the store, before it writes `<id>.json`, or the
                dispatcher, before it runs the routes itself (`dispatch.py`
                `claim_event`); the other then leaves it alone, so a store that
                comes late never runs an event its dispatcher already ran
    drained-by  the version of the service that drains it (written at start):
                a dispatcher with no service to ask writes here only when that
                is the CLI version the next service starts as, since an older
                CLI's service never drains it

Bounded: at most MAX_QUEUED waiting (`hooks.queue` refuses past it, and a
dispatcher then runs the routes itself), each at most
`protocol.MAX_HOOK_QUEUE_ITEM` bytes, none run past EXPIRE_S after it happened
(a session end counted hours late is worse than none). Run oldest first, one at
a time (the routes keep per-session state files, written read-modify-write),
each within its lane's budget. The folder is looked at again every RESCAN_S, so
an event a dispatcher wrote while this service was starting runs too.

What a queued event keeps of its environment is `protocol.hook_queue_env`'s
(what a record-keeping route reads, never a credential but Probe's own), and it
lives only in this user's private service folder, which already holds what
every client trusts (runtime.json names the interpreter they start the service
with).

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import contextlib
import json
import os
import stat
import threading
import time
from pathlib import Path

from . import hookhosts, paths
from .protocol import HOOK_LANES, MAX_HOOK_QUEUE_ITEM, RpcError, need_hook_queue

#: Events waiting at once, at most (`hooks/dispatch.py` MAX_QUEUED).
MAX_QUEUED = 128
#: A taken event's mark stays this long: longer than any dispatcher waits
#: before it writes an unanswered event beside the one it sent.
TOMBSTONE_S = 600.0
#: A dispatcher's temporary file (`.<id>.<pid>.tmp`) older than this was left
#: by one that died mid-write.
STALE_TMP_S = 60.0
#: An event that waited longer than this (no service ran to take it) is dropped.
EXPIRE_S = 900.0
#: The runner looks at the folder at least this often, and prunes at most this often.
RESCAN_S = 5.0
PRUNE_EVERY_S = 60.0
#: The dispatcher's option: run only the record-keeping routes (`hooks/dispatch.py`).
RECORD_KEEPING = "--record-keeping"
#: How long one queued event may run, past its lane's own budget.
RUN_SLACK_S = 2.0
WAITING = ".json"
TAKEN = ".done"
CLAIMED = ".claim"


def _read_item(path: Path) -> str | None:
    """A waiting event's text, or None: a regular file (never followed through
    a symlink, never a FIFO), at most MAX_HOOK_QUEUE_ITEM bytes."""
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0))
    except OSError:
        return None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_HOOK_QUEUE_ITEM:
            return None
        chunks, size = [], 0
        while size <= MAX_HOOK_QUEUE_ITEM:
            chunk = os.read(fd, 65536)
            if not chunk:
                return b"".join(chunks).decode("utf-8")
            chunks.append(chunk)
            size += len(chunk)
        return None
    except (OSError, UnicodeDecodeError):
        return None
    finally:
        os.close(fd)


def _empty(path: Path) -> None:
    """Empty a taken event's mark, never through a symlink: one planted in its
    place is removed and a plain empty mark made instead."""
    try:
        fd = os.open(path, os.O_WRONLY | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    except OSError:
        fd = None
    if fd is not None:
        try:
            if stat.S_ISREG(os.fstat(fd).st_mode):
                return
        finally:
            os.close(fd)
    with contextlib.suppress(OSError):
        os.unlink(path)
    with contextlib.suppress(OSError):
        os.close(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600))


def declares_record_keeping(root: str, lane: str) -> bool:
    """Does the folder's routes.json mark a record-keeping route on `lane`? A
    folder from before plan D36 (a checkout moved back) would run every route
    of the lane for `--record-keeping`, its dispatcher not knowing the option:
    such a queued event is dropped instead."""
    text = hookhosts.read_plugin_file(Path(root) / "hooks" / "routes.json")
    if text is None:
        return False
    try:
        wiring = json.loads(text)
        groups = wiring["hooks"][HOOK_LANES[lane]]
    except (ValueError, KeyError, TypeError):
        return False
    if not isinstance(groups, list):
        return False
    for group in groups:
        if not isinstance(group, dict) or group.get("lane") != lane or not isinstance(group.get("hooks"), list):
            continue
        if any(isinstance(hook, dict) and hook.get("record_keeping") is True for hook in group["hooks"]):
            return True
    return False


class HookQueue:
    """The queue and its one runner thread. `store` is called from the
    service's worker threads (`hooks.queue`), `pending` from its loop (what
    holds the service); the lock guards the folder's names, and is never held
    while an event runs."""

    def __init__(self, log, *, folder: Path | None = None, version: str = "", warm=None, changed=None) -> None:
        self.log = log
        self.folder = folder
        self.version = version
        #: Called with a plugin folder whose event ran as a fresh process: its
        #: warm host for the next one (the service's `_warm`, from this thread).
        self.warm = warm
        #: Called when the queue went empty or stopped being empty (what holds
        #: the service), from any thread.
        self.changed = changed
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        #: Events waiting and not yet run, the one running included: what
        #: holds the service. Read without the lock (an int).
        self._pending = 0
        #: Waiting names this service could not take (a folder gone read-only,
        #: a stale NFS handle, a directory in a file's place): logged once, then
        #: left alone, never retried in a loop nor counted as pending.
        self._stuck: set = set()
        self._pruned = 0.0

    # -- lifecycle -------------------------------------------------------------

    def start(self) -> None:
        """Make the folder, say which service drains it, and run what waits."""
        if os.name != "posix":
            return
        try:
            self.folder = paths.private_dir(self.folder or paths.hook_queue_dir())
            stamp = self.folder / paths.HOOK_QUEUE_DRAINER
            tmp = self.folder / f".{paths.HOOK_QUEUE_DRAINER}.{os.getpid()}.tmp"
            with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
                handle.write(self.version)
            os.replace(tmp, stamp)
        except OSError as exc:
            self.log(f"hook queue unavailable: {exc}")
            self.folder = None
            return
        self._pending = len(self._waiting())
        self._thread = threading.Thread(target=self._run, name="hook-queue", daemon=True)
        self._thread.start()
        self._wake.set()

    def close(self) -> None:
        """Stop after the event that runs now (each is bounded by its lane's
        budget); what still waits stays for the next service."""
        self._stop.set()
        self._wake.set()

    def pending(self) -> int:
        """Never takes the lock: the service's loop asks (what holds it), and
        a store may hold the lock across a file write."""
        return self._pending

    def public(self) -> dict:
        return {"pending": self.pending()}

    def _count(self) -> None:
        """Under the lock: `_pending` from the folder; `changed` when it went
        from none to some."""
        before, self._pending = self._pending, len(self._waiting())
        if before == 0 and self._pending and self.changed is not None:
            self.changed()

    # -- hooks.queue ---------------------------------------------------------------

    def store(self, item: dict) -> dict:
        """`hooks.queue`: `{"queued": true, "duplicate": bool}`, or `{"refused": why}`.
        Blocking (a file write): on a worker thread, never the loop."""
        if self.folder is None:
            return {"refused": "the hook queue is unavailable"}
        name = item["id"]
        waiting, taken = self.folder / f"{name}{WAITING}", self.folder / f"{name}{TAKEN}"
        with self._lock:
            if taken.exists():
                return {"queued": True, "duplicate": True}
            if waiting.exists():
                # Its dispatcher stopped waiting for this answer and wrote it
                # itself: that file is the one that runs, now.
                self._count()
                self._wake.set()
                return {"queued": True, "duplicate": True}
            if self._pending >= MAX_QUEUED:
                return {"refused": "the hook queue is full"}
            claim = self.folder / f"{name}{CLAIMED}"
            try:
                os.close(os.open(claim, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600))
            except FileExistsError:
                return {"refused": "its dispatcher ran it itself"}
            except OSError as exc:
                return {"refused": f"the hook queue could not claim it: {exc}"}
            tmp = self.folder / f".{name}.{os.getpid()}.{threading.get_ident()}.tmp"
            try:
                fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
                with open(fd, "w", encoding="utf-8") as handle:
                    json.dump(item, handle)
                os.replace(tmp, waiting)
            except OSError as exc:
                for leftover in (tmp, claim):
                    with contextlib.suppress(OSError):
                        os.unlink(leftover)
                return {"refused": f"the hook queue could not store it: {exc}"}
            self._count()
        self._wake.set()
        return {"queued": True, "duplicate": False}

    # -- the runner ----------------------------------------------------------------

    def _waiting(self) -> list:
        """Waiting events' names, oldest first (by when they were written):
        regular files only. A symlink in a waiting name is removed (the link
        only); anything else that is no file is left, as stuck."""
        found = []
        try:
            with os.scandir(self.folder) as entries:
                for entry in entries:
                    name = entry.name
                    if name.startswith(".") or not name.endswith(WAITING) or name in self._stuck:
                        continue
                    try:
                        if entry.is_symlink():
                            os.unlink(entry.path)
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            self._stuck.add(name)
                            self.log(f"hook queue: {name} is not a file; left alone")
                            continue
                        found.append((entry.stat(follow_symlinks=False).st_mtime_ns, name))
                    except OSError:
                        continue
        except OSError:
            return []
        return [name for _, name in sorted(found)]

    def _run(self) -> None:
        while not self._stop.is_set():
            self._wake.wait(RESCAN_S)
            self._wake.clear()
            if self._stop.is_set():
                return
            try:
                self._drain()
                if time.monotonic() - self._pruned >= PRUNE_EVERY_S:
                    self._pruned = time.monotonic()
                    self._prune()
            except Exception as exc:  # noqa: BLE001 -- the runner never dies of one pass
                self.log(f"hook queue pass failed: {exc!r}")

    def _drain(self) -> None:
        """Run what waits, oldest first, until nothing does. A pass in which
        nothing could be taken ends the drain (what is left is stuck), so a
        name this service cannot move is never retried in a busy loop."""
        while not self._stop.is_set():
            with self._lock:
                names = self._waiting()
                self._pending = len(names)
            if not names:
                if self.changed is not None:
                    self.changed()
                return
            moved = 0
            for name in names:
                if self._stop.is_set():
                    return
                taken, item = self._take(name)
                if not taken:
                    self._stuck.add(name)
                    self.log(f"hook queue: could not take {name}; left alone")
                    continue
                moved += 1
                if item is not None:
                    try:
                        self._run_one(item)
                    except Exception as exc:  # noqa: BLE001 -- one event never stops the rest
                        self.log(f"queued hook event {item['id']} failed: {exc!r}")
                with self._lock:
                    self._pending = max(self._pending - 1, 0)
            if not moved:
                return

    def _take(self, name: str) -> tuple[bool, dict | None]:
        """(taken, the event): the event is taken (`<id>.done`) before it
        runs, so it never runs twice. `(True, None)` for one taken already, too
        old or unreadable (taken all the same: dropped); `(False, None)` when
        it could not be moved at all."""
        waiting = self.folder / name
        taken = self.folder / (name[: -len(WAITING)] + TAKEN)
        with self._lock:
            if taken.exists():
                try:
                    os.unlink(waiting)
                except FileNotFoundError:
                    pass
                except OSError:
                    return False, None
                return True, None
            text = _read_item(waiting)
            try:
                os.replace(waiting, taken)
            except FileNotFoundError:
                return True, None
            except OSError:
                return False, None
            _empty(taken)
        try:
            item = need_hook_queue(json.loads(text)) if text is not None else None
        except (ValueError, TypeError, AttributeError, RpcError):
            item = None
        if item is None or f"{item['id']}{WAITING}" != name:
            self.log(f"dropped an unreadable queued hook event {name}")
            return True, None
        if time.time() - item["at"] > EXPIRE_S:
            self.log(f"queued hook event {item['id']} ({item['lane']}) dropped: waited past {EXPIRE_S:.0f}s")
            return True, None
        return True, item

    def _run_one(self, item: dict) -> None:
        """Its record-keeping routes, once: on the folder's warm host when it
        answers in time, else as a fresh dispatcher (and the host started for
        the next). What they print is nobody's: only a failure is logged."""
        request = {
            "root": item["plugin_root"],
            "lane": item["lane"],
            "payload": item["payload"].encode("utf-8", "surrogateescape"),
            "env": item["env"],
            "cwd": item["cwd"] if os.path.isdir(item["cwd"]) else (item["env"].get("HOME") or "/"),
            "argv": [item["lane"], RECORD_KEEPING],
            "queued": True,
        }
        refused = hookhosts.runnable(request)
        if refused is not None:
            self.log(f"queued hook event {item['id']} dropped: {refused['refused']}")
            return
        if not declares_record_keeping(request["root"], request["lane"]):
            self.log(f"queued hook event {item['id']} dropped: {request['root']} marks no record-keeping route")
            return
        deadline = time.monotonic() + hookhosts.LANE_BUDGET_S[request["lane"]] + hookhosts.HOST_MARGIN_S + RUN_SLACK_S
        answer = hookhosts._via_host(request, None, deadline)
        if answer is None:
            answer = hookhosts._via_process(request, None, deadline)
            if self.warm is not None:
                with contextlib.suppress(Exception):
                    self.warm(request["root"])
        if answer.get("timed_out") or answer.get("exit_code") is None:
            self.log(f"queued hook event {item['id']} ({item['lane']}) did not finish: via {answer.get('via')}")

    def _prune(self) -> None:
        """Marks and claims past TOMBSTONE_S, and temporary files a dispatcher left."""
        now = time.time()
        try:
            with os.scandir(self.folder) as entries:
                for entry in entries:
                    if entry.name.endswith((TAKEN, CLAIMED)):
                        old = TOMBSTONE_S
                    else:
                        old = STALE_TMP_S if entry.name.endswith(".tmp") else None
                    if old is None:
                        continue
                    with contextlib.suppress(OSError):
                        if now - entry.stat(follow_symlinks=False).st_mtime > old:
                            os.unlink(entry.path)
        except OSError:
            return
