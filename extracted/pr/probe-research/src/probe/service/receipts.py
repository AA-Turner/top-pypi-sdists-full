"""Each registered session's delivery receipts (plan D29): what the server has
taken of its transcript, and what still waits to go.

    the journal   `~/.probe/transcripts-v2/<namespace>/state.sqlite3`, the
                  recorder's own record (`tap_core/session_journal.py`; one
                  namespace per account and agent, `$PROBE_TRANSCRIPT_STATE_DIR`
                  moves the folder), one row per session: the server's receipt
                  cursor (`source_line_end`, `source_byte_end`), when the last
                  receipt landed (`received_at`, written by taps from 0.10.6),
                  and a staged batch still waiting for its receipt (`pending`)
    the file      the transcript itself: its bytes past the receipt cursor wait
                  to go (`pending_bytes`); the complete lines among them are
                  counted once and then only as the file grows (`pending_lines`)

NOT `<capture plugin dir>/state.db`: that is the protocol-1 outbox, which the
recorder stopped writing when capture moved to the journal (2026-09-08,
#1415), so its `last_successful_post_at` and outbox count stopped moving.

`session.list` answers each session's `receipts` and `harnesses`, the same per
agent and account. Only the journal of the destination the session records to
now counts (`read`: what the service's own recorder published, else Linux's
/proc/locks), and each receipt names that journal's account (`scope`,
`journal_scope`): None when either cannot be told. Read-only and bounded: one
read-only SQLite connection per journal, SCAN_BYTES of transcript at most per
session per pass, on a thread (never the service's loop), at most once per
TTL_S; a caller that cannot wait gets the last answer.

Stdlib only; `sqlite3` is imported on the first read (the start path; plan S1).
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import json
import os
import stat
import threading
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from . import paths

#: Where the journal lives unless `$PROBE_TRANSCRIPT_STATE_DIR` names another
#: folder (`session_journal.state_root`).
STATE_DIR_ENV = "PROBE_TRANSCRIPT_STATE_DIR"
JOURNAL_DIR = (".probe", "transcripts-v2")
JOURNAL_NAME = "state.sqlite3"
#: Beside each journal: the destination its folder's name hashes
#: (`session_journal.DESTINATION_NAME`; tests/test_service_receipts.py holds
#: the two equal).
DESTINATION_NAME = "destination.json"
#: Linux's list of the locks processes hold (`_linux_flocks`).
PROC_LOCKS = Path("/proc/locks")
#: Journals read per folder, at most (one per account and agent).
MAX_JOURNALS = 64
#: Folders read, at most (the default and what recorded sessions name).
MAX_ROOTS = 8
#: How long a reader waits for a journal another process is writing.
BUSY_S = 0.25
#: Transcript bytes counted per session per pass: a backlog larger than this is
#: counted over the next passes (`pending_lines` is None until it is).
SCAN_BYTES = 8 * 1024 * 1024
#: An answer is reused this long.
TTL_S = 5.0
_CHUNK = 1024 * 1024
#: The sessions tables, protocol 3's first (a row there wins, as in the journal).
_TABLES = ("fragment_sessions", "sessions")


def _no_network_text(text: object) -> bool:
    # On the slow checks' thread, never the start path (plan S1).
    from probe._shared import offline

    return offline.no_network_text(text)


def _count(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def _time(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        return None
    return float(value)


def journal_roots(envs: Iterable[dict] = ()) -> list[Path]:
    """The journal folders to read: the default under `$HOME` (fixed, as every
    service path), and the `$PROBE_TRANSCRIPT_STATE_DIR` each of `envs` (the
    environments the service's recorders run with) names."""
    roots = [paths.home().joinpath(*JOURNAL_DIR)]
    for env in envs:
        named = env.get(STATE_DIR_ENV) if isinstance(env, dict) else None
        if isinstance(named, str) and named.strip():
            root = Path(named).expanduser()
            if root.is_absolute() and root not in roots:
                roots.append(root)
    return roots[:MAX_ROOTS]


def _journals(roots: list[Path]) -> list[Path]:
    found = []
    for root in roots:
        try:
            names = sorted(entry.name for entry in os.scandir(root) if entry.is_dir(follow_symlinks=False))
        except OSError:
            continue
        for name in names[:MAX_JOURNALS]:
            db = root / name / JOURNAL_NAME
            if db.is_file():
                found.append(db)
    return found


def _rows(db: Path, wanted: set) -> dict:
    """`{sid: (state, staged)}` of `wanted` in one journal, read-only."""
    import sqlite3

    found: dict = {}
    try:
        conn = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True, timeout=BUSY_S)
    except (sqlite3.Error, ValueError):
        return found
    try:
        for sid in wanted:
            for table in _TABLES:
                try:
                    row = conn.execute(f"SELECT state FROM {table} WHERE session_id=?", (sid,)).fetchone()
                except sqlite3.Error:
                    continue  # a journal from before protocol 3 has no fragment_sessions
                if row is None:
                    continue
                try:
                    state = json.loads(row[0])
                except (TypeError, ValueError):
                    break
                if not isinstance(state, dict):
                    break
                try:
                    staged = conn.execute("SELECT 1 FROM pending WHERE session_id=?", (sid,)).fetchone() is not None
                except sqlite3.Error:
                    staged = False
                found[sid] = (state, staged)
                break
    finally:
        conn.close()
    return found


@dataclass
class _Lines:
    """Newlines counted in one transcript from a receipt cursor on."""

    path: str
    inode: int
    base_byte: int
    base_line: int
    counted_to: int
    lines: int = 0

    def pending(self, size: int, line_end: int, budget: int) -> int | None:
        """Complete lines past the receipt cursor `line_end`, counting at most
        `budget` more bytes of the file (`size` long now); None while the count
        has not reached its end. A line still being written is not one yet."""
        # Without blocking, and only a regular file: a FIFO put where the
        # transcript was would hang the read for good.
        flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOCTTY", 0) | getattr(os, "O_BINARY", 0)
        fd = os.open(self.path, flags)
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise OSError(f"{self.path} is not a regular file")
            handle = os.fdopen(fd, "rb")
        except BaseException:
            os.close(fd)
            raise
        with handle:
            handle.seek(self.counted_to)
            while self.counted_to < size and budget > 0:
                chunk = handle.read(min(_CHUNK, budget, size - self.counted_to))
                if not chunk:
                    break
                self.lines += chunk.count(b"\n")
                self.counted_to += len(chunk)
                budget -= len(chunk)
        if self.counted_to < size:
            return None
        waiting = self.base_line + self.lines - line_end
        return waiting if waiting >= 0 else None

    def fits(self, path: str, inode: int, size: int, byte_end: int) -> bool:
        """Does this count still hold: the same file, not cut shorter, and the
        receipt cursor neither behind its start (a rewrite) nor past what it
        counted (a receipt that jumped ahead)? Else a new count starts."""
        return (
            path == self.path and inode == self.inode and size >= self.counted_to
            and self.base_byte <= byte_end <= self.counted_to
        )


def receipt(
    state: dict, staged: bool, counts: dict, sid: str, budget: int = SCAN_BYTES, scope: dict | None = None
) -> dict | None:
    """One session's receipts from its journal row (and its transcript), and
    `scope`: whose they are (`journal_scope`)."""
    line_end, byte_end = _count(state.get("source_line_end")), _count(state.get("source_byte_end"))
    if line_end is None or byte_end is None:
        return None
    pending_bytes = pending_lines = None
    path = state.get("path")
    if isinstance(path, str) and os.path.isabs(path):
        try:
            info = os.stat(path)
            if not stat.S_ISREG(info.st_mode):
                # A row naming a FIFO or a device would hang or fill the read.
                raise OSError(f"{path} is not a regular file")
            pending_bytes = max(0, info.st_size - byte_end)
            count = counts.get(sid)
            if count is None or not count.fits(path, info.st_ino, info.st_size, byte_end):
                count = _Lines(path, info.st_ino, byte_end, line_end, byte_end)
                counts[sid] = count
            pending_lines = count.pending(info.st_size, line_end, budget)
        except OSError:
            counts.pop(sid, None)
    return {
        "last_line": line_end,
        "received_bytes": byte_end,
        "received_at": _time(state.get("received_at")),
        "pending_bytes": pending_bytes,
        "pending_lines": pending_lines,
        "pending_batch": bool(staged),
        "finalized": state.get("finalized") is True,
        "retrying": bool(state.get("error")),
        # Its last upload had no network at all (`probe._shared.offline`): the
        # machine is offline, not the server stalled.
        "offline": _no_network_text(state.get("error")),
        "scope": dict(scope) if scope is not None else None,
    }


def backend_of(url: object) -> str | None:
    """A base URL's host, with `:port` when it names one, lower case: the
    `backend` of a receipt's scope (and what the desktop app compares with its
    signed-in account's). None when it is no URL."""
    if not isinstance(url, str) or not url:
        return None
    from urllib.parse import urlsplit

    try:
        parts = urlsplit(url.strip())
        host, port = parts.hostname, parts.port
    except ValueError:
        return None
    if not host:
        return None
    return f"{host}:{port}" if port else host


def journal_scope(folder: Path) -> dict | None:
    """`{"backend", "customer"}` of the account a journal folder records to,
    from its destination record (`session_journal.DESTINATION_NAME`, written by
    taps from 0.10.6), and only when that record hashes to the folder's own
    name, as the journal names it: a record copied or edited into another
    folder names no account. None when it cannot be told."""
    try:
        record = json.loads((folder / DESTINATION_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict):
        return None
    base_url, customer, source = record.get("base_url"), record.get("customer_id"), record.get("source")
    if not all(isinstance(v, str) and v for v in (base_url, customer, source)):
        return None
    if hashlib.sha256(json.dumps([base_url, customer, source]).encode()).hexdigest() != folder.name:
        return None
    backend = backend_of(base_url)
    return {"backend": backend, "customer": customer} if backend else None


def owner_lock(folder: Path, sid: str) -> Path:
    """The live recorder's claim on a session in one journal
    (`session_journal.Journal._try_owner`): held (flock, exclusive) for as long
    as a recorder records the session into that journal's destination."""
    return folder / (hashlib.sha256(sid.encode()).hexdigest() + ".owner.lock")


def _linux_flocks() -> set | None:
    """`{(major, minor, inode)}` of every file a process holds an exclusive
    flock on (Linux `/proc/locks`, the device parts in hex), or None where
    there is no such list. Read, never taken: nothing a recorder does is ever
    in its way. Elsewhere (macOS) no lock is probed at all: only what the
    service's own recorders publish says where a session records."""
    try:
        text = PROC_LOCKS.read_text(encoding="ascii", errors="replace")
    except OSError:
        return None
    held = set()
    for line in text.splitlines():
        # `1: FLOCK  ADVISORY  WRITE 4242 fd:01:123456 0 EOF`; a waiter has `->` second.
        parts = line.split()
        if len(parts) < 6 or parts[1] != "FLOCK" or parts[3] != "WRITE":
            continue
        device = parts[5].split(":")
        try:
            held.add((int(device[0], 16), int(device[1], 16), int(device[2])))
        except (IndexError, ValueError):
            continue
    return held


def _held(path: Path, linux: set) -> bool:
    """Does a process hold this claim now (Linux: the same device AND inode)?"""
    try:
        info = os.stat(path)
    except OSError:
        return False
    return (os.major(info.st_dev), os.minor(info.st_dev), info.st_ino) in linux


def read(sids: Iterable[str], roots: list[Path], counts: dict, claims: dict | None = None) -> dict:
    """`{sid: receipts}` for each of `sids` whose live recorder's journal, and
    whose account, are known. Blocking: a thread's.

    A session can have rows in several journals (an account switch, staging
    and production, a re-import elsewhere), and the newest receipt among them
    can be another account's: after a switch the old account's full receipt
    would hide the new one's refused uploads. So only the journal of the
    destination the session is recorded to now counts:

        claims    `{sid: journal folder}` the service's own recorders published
                  (`RecorderHost.claims`): that journal, no lock looked at
        Linux     else the journal whose claim (`owner_lock`) a process holds,
                  read from /proc/locks (none, or two: unknown)
        elsewhere else unknown: no lock is ever probed, since a probe can make
                  a recorder that is claiming at that instant give up

    and only a journal whose account can be told (`journal_scope`): each
    receipt carries it, so a reader overlays only its own account's."""
    wanted = {sid for sid in sids if isinstance(sid, str) and sid}
    rows: dict = {}
    for sid, folder in (claims or {}).items():
        if sid not in wanted or not isinstance(folder, str) or not os.path.isabs(folder):
            continue
        db = Path(folder) / JOURNAL_NAME
        found = _rows(db, {sid}) if db.is_file() else {}
        if sid in found:
            rows[sid] = (db.parent, found[sid])
    rest = wanted - set(claims or {})
    linux = _linux_flocks() if rest else None
    if linux is not None:
        candidates: dict = {}
        for db in _journals(roots):
            for sid, row in _rows(db, rest).items():
                candidates.setdefault(sid, []).append((db.parent, row))
        for sid, found in candidates.items():
            live = [(folder, row) for folder, row in found if _held(owner_lock(folder, sid), linux)]
            if len(live) == 1:
                rows[sid] = live[0]
    out = {}
    for sid, (folder, (state, staged)) in rows.items():
        scope = journal_scope(folder)
        if scope is None:
            continue
        try:
            out[sid] = receipt(state, staged, counts, sid, scope=scope)
        except Exception:  # noqa: BLE001 -- one unreadable row costs that session's receipts
            counts.pop(sid, None)
            out[sid] = None
    return out


def _scope_key(scope: object) -> tuple:
    if not isinstance(scope, dict):
        return ("", "")
    return (str(scope.get("backend") or ""), str(scope.get("customer") or ""))


def by_harness(sessions: list[dict], *, scoped: bool = True) -> list[dict]:
    """`session.list`'s `harnesses`: per agent (`harness`, in order) and, with
    `scoped`, per account its receipts came from (`scope`; None for sessions
    with none): how many sessions (`alive` of them), the latest receipt, and
    what waits (sums over the sessions where it is known; None where it is
    known for none). Unscoped (the CLI's delivery op, after keeping only its
    account's receipts): one row per agent."""
    out: dict = {}
    for session in sessions:
        harness = session.get("harness")
        if not isinstance(harness, str):
            continue
        found = session.get("receipts")
        scope = found.get("scope") if scoped and isinstance(found, dict) else None
        key = (harness, isinstance(scope, dict), _scope_key(scope))
        row = out.get(key)
        if row is None:
            row = out[key] = {"harness": harness, "sessions": 0, "alive": 0, "received_at": None,
                              "pending_bytes": None, "pending_lines": None, "pending_batches": 0}
            if scoped:
                row["scope"] = dict(scope) if isinstance(scope, dict) else None
        row["sessions"] += 1
        row["alive"] += 1 if session.get("alive") is True else 0
        if not isinstance(found, dict):
            continue
        at = found.get("received_at")
        if at is not None and (row["received_at"] is None or at > row["received_at"]):
            row["received_at"] = at
        for name in ("pending_bytes", "pending_lines"):
            if found.get(name) is not None:
                row[name] = (row[name] or 0) + found[name]
        row["pending_batches"] += 1 if found.get("pending_batch") else 0
    return [out[key] for key in sorted(out)]


class ReceiptCache:
    """One read at a time, on a thread; answers reused for `ttl` seconds."""

    def __init__(self, *, ttl: float = TTL_S) -> None:
        self.ttl = ttl
        #: sid -> (monotonic time read, receipts or None)
        self._answers: dict = {}
        #: sid -> its transcript's line count (`_Lines`), touched by the thread only.
        self._counts: dict = {}
        self._flight: asyncio.Future | None = None
        #: Reads run so far (the tests read it).
        self.reads = 0

    async def get(self, sids: list[str], roots: list[Path], *, wait: float, claims: dict | None = None) -> dict:
        """`{sid: receipts or None}`: fresh ones, read now when any is stale,
        within `wait` seconds; past that, the last answer each had."""
        now = time.monotonic()
        stale = [sid for sid in sids if now - self._answers.get(sid, (-self.ttl - 1, None))[0] > self.ttl]
        if stale:
            if self._flight is None or self._flight.done():
                self._flight = asyncio.ensure_future(self._read(list(sids), roots, dict(claims or {})))
            done, _ = await asyncio.wait({self._flight}, timeout=max(wait, 0.0))
            if not done:
                self._flight.add_done_callback(_settled)
        return {sid: self._answers.get(sid, (0.0, None))[1] for sid in sids}

    async def _read(self, sids: list[str], roots: list[Path], claims: dict | None = None) -> None:
        """On a daemon thread of its own: a stopping service never waits for a
        read stalled on a transcript (a hung network mount)."""
        self.reads += 1
        loop = asyncio.get_running_loop()
        counts = {sid: self._counts[sid] for sid in sids if sid in self._counts}
        result: asyncio.Future = loop.create_future()

        def work() -> None:
            try:
                found = read(sids, roots, counts, claims)
            except Exception:  # noqa: BLE001 -- the last answers stand, never a failed listing
                found = None

            def settle() -> None:
                if not result.done():
                    result.set_result(found)

            with contextlib.suppress(RuntimeError):  # the loop is closed: the service went first
                loop.call_soon_threadsafe(settle)

        threading.Thread(target=work, name="probe-receipts", daemon=True).start()
        found = await result
        if found is None:
            return  # the answers read last stand, and stay stale: the next call reads again
        self._counts = counts
        stamp = time.monotonic()
        self._answers = {sid: (stamp, found.get(sid)) for sid in sids}


def _settled(future: asyncio.Future) -> None:
    if not future.cancelled():
        future.exception()
