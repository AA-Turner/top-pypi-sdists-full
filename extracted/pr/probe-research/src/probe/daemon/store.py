"""The session's store: scrubbed events, the queue watermark, the logbook.

One SQLite file per session, `<state>/probe/daemon/<sid>.sqlite`. Everything in
it passed the secret scanner first (`probe.tap_core.secrets`, the one detector
capture, the SDK and the daemon share, R4), so `session(op=search)` and
`session(op=open)` can never hand the model a credential the chat log held.

    events     every normalized event, with its turn number and when the daemon
               noticed it (the ~2-minute trigger counts from then)
    events_fts full-text index over event text and commands (`session(op=search)`)
    cursors    per stream: the byte offset read so far (a re-read is idempotent:
               event ids are `<stream>:<offset>:<index>`), and the file's inode
               and a hash of the bytes just before that offset, so a file
               rewritten under the cursor is noticed, never read on (the worker's
               `_read_stream`)
    bites      one row per model call sequence: trigger, what it covered, tokens,
               outcome
    writes     the logbook: every `probe` command the daemon ran or was refused,
               with its operation id (R12) and outcome
    notes      each run's one-line summary, versioned (it was the running note;
               the daemon keeps no memory of its own now)
    facts      session facts (permission mode, harness, working folders)
    files      the folder check's last-seen snapshot (size, mtime, text copy)
    rounds     one row per model response (T10): model, input / cached / output
               tokens, the tools it called, its estimated dollars
    run_alerts the server's run alerts this session's mailbox was handed (its
               ids, and the message that carried each), so each goes out once
    conversations
               conversation mode (T15): the saved message history of the one
               live conversation, resumed on respawn while its fingerprint
               still matches (the session, the job description, the model,
               the Pydantic AI version); ended ones keep their reason (a fresh
               start from disk replaces them)

Deliberately NOT the companion ledger (format 1, read by released CLIs): a
separate file cannot lock an old CLI out. `probe companion log` reads the ledger
of a v1 session and this store's logbook (`writes`) of a v2 one; the device's
token counter is `daemon/device.json` (`worker.add_device_tokens`), not here.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator

from probe.daemon.events import PEER_TOOL, READER_SOURCE, REQUEST_SOURCE, Event, Kind
from probe.tap_core import secrets

FORMAT_VERSION = 1
#: Event text kept per event in the store. A longer output keeps its head and
#: tail; the full text stays in the chat log (or its side file), one
#: `session(op=open)` away, scrubbed when read.
MAX_STORED_CHARS = 200_000

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS events (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE NOT NULL,
    stream TEXT NOT NULL,
    offset INTEGER NOT NULL,
    idx INTEGER NOT NULL,
    kind TEXT NOT NULL,
    turn INTEGER NOT NULL,
    ts TEXT,
    noticed REAL NOT NULL,
    text TEXT NOT NULL DEFAULT '',
    tool TEXT,
    call_id TEXT,
    command TEXT,
    tool_input TEXT,
    is_error INTEGER NOT NULL DEFAULT 0,
    side_file TEXT,
    parent TEXT,
    cwd TEXT,
    chars INTEGER NOT NULL DEFAULT 0,
    bite INTEGER,
    note TEXT,
    source TEXT
);
CREATE INDEX IF NOT EXISTS events_turn ON events (turn, seq);
CREATE INDEX IF NOT EXISTS events_pending ON events (bite, seq);
CREATE INDEX IF NOT EXISTS events_call ON events (call_id);
-- What `totals` (and, from an earlier build, `shown_turn_sizes`) reads without the
-- event text pages; `events_sizes_source` below covers `shown_turn_sizes` now.
-- Both stay: an earlier CLI's worker may still be serving this store.
CREATE INDEX IF NOT EXISTS events_sizes ON events (turn, kind, chars);
CREATE VIRTUAL TABLE IF NOT EXISTS events_fts USING fts5(
    text, command, content='events', content_rowid='seq', tokenize='unicode61'
);
CREATE TRIGGER IF NOT EXISTS events_ai AFTER INSERT ON events BEGIN
    INSERT INTO events_fts (rowid, text, command) VALUES (new.seq, new.text, coalesce(new.command, ''));
END;
CREATE TABLE IF NOT EXISTS cursors (stream TEXT PRIMARY KEY, path TEXT NOT NULL, offset INTEGER NOT NULL,
                                     inode INTEGER, tail_hash TEXT, tail_at INTEGER);
CREATE TABLE IF NOT EXISTS bites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started REAL NOT NULL,
    ended REAL,
    trigger TEXT NOT NULL,
    first_seq INTEGER,
    last_seq INTEGER,
    input_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    cached_tokens INTEGER NOT NULL DEFAULT 0,
    outcome TEXT,
    error TEXT,
    attempts INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS writes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bite INTEGER,
    op_id TEXT NOT NULL,
    at REAL NOT NULL,
    argv TEXT NOT NULL,
    head TEXT NOT NULL,
    status TEXT NOT NULL,
    reason TEXT,
    output TEXT,
    exit_code INTEGER,
    request TEXT
);
CREATE INDEX IF NOT EXISTS writes_bite ON writes (bite);
CREATE TABLE IF NOT EXISTS lookups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bite INTEGER,
    at REAL NOT NULL,
    tool TEXT NOT NULL,
    query TEXT NOT NULL,
    result TEXT
);
CREATE TABLE IF NOT EXISTS notes (version INTEGER PRIMARY KEY AUTOINCREMENT, at REAL NOT NULL, bite INTEGER, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS facts (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, size INTEGER, mtime REAL, text TEXT);
CREATE TABLE IF NOT EXISTS rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bite INTEGER,
    at REAL NOT NULL,
    model TEXT,
    input_tokens INTEGER NOT NULL DEFAULT 0,
    cached_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    tools TEXT,
    usd REAL
);
CREATE INDEX IF NOT EXISTS rounds_bite ON rounds (bite);
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started REAL NOT NULL,
    updated REAL,
    ended REAL,
    end_reason TEXT,
    instructions TEXT NOT NULL,
    messages TEXT,
    runs INTEGER NOT NULL DEFAULT 0,
    compactions INTEGER NOT NULL DEFAULT 0,
    fingerprint TEXT
);
CREATE TABLE IF NOT EXISTS read_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started REAL NOT NULL,
    updated REAL,
    ended REAL,
    end_reason TEXT,
    instructions TEXT NOT NULL,
    messages TEXT,
    runs INTEGER NOT NULL DEFAULT 0,
    compactions INTEGER NOT NULL DEFAULT 0,
    fingerprint TEXT
);
CREATE TABLE IF NOT EXISTS read_asks (
    id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    asked_at REAL NOT NULL,
    wait INTEGER NOT NULL DEFAULT 0,
    taken_at REAL NOT NULL,
    state TEXT NOT NULL DEFAULT 'waiting',
    ended_at REAL,
    reason TEXT
);
CREATE TABLE IF NOT EXISTS read_messages (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    ask TEXT,
    question TEXT,
    text TEXT NOT NULL DEFAULT '',
    reason TEXT,
    origin_turn INTEGER,
    made_at REAL NOT NULL,
    published INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS read_turns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started REAL NOT NULL,
    ended REAL,
    trigger TEXT,
    ask TEXT,
    first_seq INTEGER,
    last_seq INTEGER,
    outcome TEXT,
    error TEXT,
    rounds INTEGER NOT NULL DEFAULT 0,
    input_tokens INTEGER NOT NULL DEFAULT 0,
    cached_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    usd REAL
);
-- The run-alert poller's record (`run_alerts.py`): an alert id here is in the
-- mailbox already. Added in format 1: a store from an earlier build gains it on
-- open, and an earlier CLI never reads it.
CREATE TABLE IF NOT EXISTS run_alerts (
    id INTEGER PRIMARY KEY,
    message_id TEXT NOT NULL,
    seen_at REAL NOT NULL
);
-- The main agent's requests to the writer (`probe ask --writer`): waiting until
-- the run that saw one ends (answered) or it will not run (failed, its event
-- retired). `event_seq`: its event in `events`.
CREATE TABLE IF NOT EXISTS write_requests (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    asked_at REAL NOT NULL,
    wait INTEGER NOT NULL DEFAULT 0,
    taken_at REAL NOT NULL,
    state TEXT NOT NULL DEFAULT 'waiting',
    ended_at REAL,
    reason TEXT,
    event_seq INTEGER,
    bite INTEGER,
    first_bite INTEGER,
    conversation INTEGER
);
-- The bites that worked on each request: the ones that showed its event, and a
-- conversation's later bites while its history holds it. A reply or a failure
-- lists their writes, never an unrelated run's.
CREATE TABLE IF NOT EXISTS write_request_bites (
    request_id TEXT NOT NULL,
    bite INTEGER NOT NULL,
    PRIMARY KEY (request_id, bite)
);
-- What the writer sends the main agent (replies, failures, receipts), published
-- by id after the transaction that saved it: NOT `read_messages`, whose ids the
-- worker reads back as the reader's.
CREATE TABLE IF NOT EXISTS writer_messages (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    ask TEXT,
    text TEXT NOT NULL DEFAULT '',
    reason TEXT,
    bite INTEGER,
    made_at REAL NOT NULL,
    published INTEGER NOT NULL DEFAULT 0
);
"""
#: Ended conversations keep their message history this many deep (the rest only
#: their row): enough to look at what went wrong, never a growing file.
KEEP_ENDED_HISTORIES = 2

#: Kinds a person or the agent produced: what "whole turns" of the chat are made of.
CHAT_KINDS = (Kind.PROMPT, Kind.AGENT_TEXT, Kind.AGENT_REASONING, Kind.TOOL_CALL, Kind.TOOL_OUTPUT,
              Kind.SUBAGENT, Kind.COMPACTION, Kind.META, Kind.TURN_END, Kind.FILE_CHANGE, Kind.RUN_EVENT)


def state_dir() -> Path:
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / "probe" / "daemon"


def store_path(session_id: str) -> Path:
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_") or "session"
    return state_dir() / f"{safe}.sqlite"


#: How a shell write cut short is logged after who approved it (`tools._run_shell_write`).
CUT_SHORT = "the bite was cut short while it ran"
#: How a shell write that raised while it ran is logged after who approved it, with the error's type.
FAILED_WHILE_RUNNING = "failed while it ran"


@dataclass
class JevApproved:
    """`jev_approved`'s answer: the newest `rows`; how many matched in all
    (`total`, which can be more than the rows) and in each session
    (`by_session`, so a session none of whose rows is shown is still named);
    how many session stores could not be read (`unreadable`); and how many of
    its rows a store held in a shape no Jev yes is written in (`damaged`). The
    list is complete only when both of those are 0."""

    rows: list[dict]
    total: int
    unreadable: int
    damaged: int = 0
    by_session: dict[str, int] = field(default_factory=dict)


#: A Jev-approved command's logbook status, as `probe approvals` says it (`_run_shell_write`).
JEV_ENDINGS = {"ran": "ran", "cancelled": "cut short while it ran", "failed": "failed while it ran",
               "running": "still running, or the daemon stopped while it ran"}


def jev_approved(since: float, limit: int, *, session_id: str | None = None) -> JevApproved:
    """Shell commands Jev said yes to and the daemon ran without asking
    (`command_check`), logged at or after `since`, newest first: from every
    session's store on this machine, or `session_id`'s alone. Nobody is asked
    about these, so `probe approvals` lists them beside the questions (R2): the
    researcher sees what ran in their name.

    Only the rows `_run_shell_write` writes on a Jev yes count: a shell head, no
    question behind it, and a reason that is exactly Jev's, checked whole. The
    daemon's model writes the reason of its own `probe` writes (their `why`),
    so a prefix match would let the watched model fill the list and push a real
    one out of it. A command logged `running` started and has not been logged
    since: it still runs, or its worker died while it ran. Read-only; a store
    that cannot be read, or is a newer format, is counted in `unreadable`, and a
    row in another shape in `damaged`, never an error."""
    from probe.daemon.command_check import AUTO_JEV, JEV_REASON

    # Exactly what `_run_shell_write` logs on a Jev yes, each status with its own reason.
    reason_of_jev = {
        "ran": re.compile(JEV_REASON.pattern), "running": re.compile(JEV_REASON.pattern),
        "cancelled": re.compile(JEV_REASON.pattern + "; " + re.escape(CUT_SHORT)),
        "failed": re.compile(JEV_REASON.pattern + "; " + re.escape(FAILED_WHILE_RUNNING) + r" \(\w+\)"),
    }
    paths = [store_path(session_id)] if session_id is not None else sorted(state_dir().glob("*.sqlite"))
    rows: list[dict] = []
    unreadable = damaged = 0
    for path in paths:
        # A row lands in the -wal file first: a store whose files are both older
        # wrote nothing since. The -wal first: a worker closing between the two
        # moves its rows into the main file, whose time is then read after it.
        try:
            touched = [path.with_name(path.name + "-wal").stat().st_mtime]
        except OSError:
            touched = []  # no -wal (closed cleanly): the main file holds every row
        try:
            touched.append(path.stat().st_mtime)
        except FileNotFoundError:
            if session_id is None:
                unreadable += 1  # listed a moment ago; a session with no store has nothing to list
            continue
        except OSError:
            unreadable += 1  # there, and not readable (permissions): never read as "nothing ran"
            continue
        if max(touched) < since:
            continue
        try:
            conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=2.0)
        except (OSError, sqlite3.Error):
            unreadable += 1
            continue
        try:
            row = conn.execute("SELECT value FROM meta WHERE key = 'format_version'").fetchone()
            if row is None or row[0] is None or int(row[0]) > FORMAT_VERSION:
                unreadable += 1
                continue
            # GLOB, not LIKE: it is case-sensitive, as the reason is. Every match is
            # read (a day's are few), so `total` counts exactly what is left out.
            found = conn.execute("SELECT at, argv, reason, exit_code, status FROM writes WHERE at >= ? "
                                 "AND head = 'shell' AND request IS NULL "
                                 "AND status IN ('ran', 'cancelled', 'failed', 'running') "
                                 "AND reason GLOB ?", (since, f"{AUTO_JEV} p=*")).fetchall()
        except (sqlite3.Error, ValueError, TypeError):
            unreadable += 1
            continue
        finally:
            conn.close()
        for at, argv, reason, exit_code, status in found:
            try:
                words = json.loads(argv)
            except (TypeError, ValueError):
                words = None
            jev = reason_of_jev[status].fullmatch(reason) if isinstance(reason, str) else None
            if (jev is None or not isinstance(at, (int, float)) or not isinstance(words, list) or len(words) != 3
                    or words[:2] not in (["sh", "-c"], ["bash", "-c"]) or not isinstance(words[2], str)
                    or not (exit_code is None or isinstance(exit_code, int))):
                damaged += 1  # the shape filter passed it: something wrote it another way
                continue
            rows.append({"session_id": path.stem, "at": float(at), "command": words[2], "lowest": jev.group(1),
                         "ended": status, "exit_code": exit_code})
    rows.sort(key=lambda r: r["at"], reverse=True)
    by_session: dict[str, int] = {}
    for r in rows:
        by_session[r["session_id"]] = by_session.get(r["session_id"], 0) + 1
    return JevApproved(rows=rows[:limit], total=len(rows), unreadable=unreadable, damaged=damaged,
                       by_session=by_session)


# -- the device's daily token counter (every session's worker adds to it) --


def device_path() -> Path:
    return state_dir() / "device.json"


def utc_day(now: float | None = None) -> str:
    """The counter's day: UTC, like the server's `daemon_spend_daily` meter."""
    return time.strftime("%Y-%m-%d", time.gmtime(time.time() if now is None else now))


#: The device counter keeps one total per lane: the writer's under its original
#: key (older CLIs read it), the reader's beside it, so a busy reader can never
#: trip the writer's daily fuse.
LANE_WRITE = "write"
LANE_READ = "read"
_LANE_KEYS = {LANE_WRITE: "tokens", LANE_READ: "read_tokens"}
#: `add_device_tokens` waits at most this long for the device-wide lock: it runs on
#: the event loop two lanes share, so a stalled holder must never freeze both.
DEVICE_LOCK_WAIT_S = 1.0


def _device_today(now: float | None = None) -> dict:
    try:
        data = json.loads(device_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict) or data.get("day") != utc_day(now):
        return {}
    return data


def device_tokens_today(now: float | None = None, lane: str = LANE_WRITE) -> int:
    return int(_device_today(now).get(_LANE_KEYS[lane], 0) or 0)


def add_device_tokens(n: int, lane: str = LANE_WRITE) -> None:
    """Add `n` to today's counter for `lane`, under a device-wide lock
    (`device.lock`) and through a temp file of its own: two sessions' workers
    never lose an update or rename each other's half-written file. The lock is
    waited for at most DEVICE_LOCK_WAIT_S; past that, TimeoutError (the caller
    counts it next time)."""
    from probe._shared import oscompat as fcntl  # fcntl.flock, or msvcrt on Windows

    if n <= 0:
        return
    path = device_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix(".lock").open("a") as lock:
        deadline = time.monotonic() + DEVICE_LOCK_WAIT_S
        while True:
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError("the device token counter is locked by another process")
                time.sleep(0.05)
        today = _device_today()
        counts = {key: int(today.get(key, 0) or 0) for key in _LANE_KEYS.values()}
        counts[_LANE_KEYS[lane]] += n
        fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump({"day": utc_day(), **counts}, handle)
            os.replace(tmp, path)
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise


#: `events.bite` for an event that arrived while the switch read `read only
#: (daemon)`: the reader reads it, no bite ever covers it (-1 is a deferred one).
UNRECORDED_BITE = -2
#: `events.bite` for an event the session held before its first worker started,
#: stamped more than `worker.CATCH_UP_S` before its newest (`cover_before_daemon`):
#: covered -- context the writer sees and `session` reaches, never new.
BEFORE_DAEMON_BITE = -3
#: Fact: a conversation run paused and the next bite carries on (`worker.CARRY_ON`).
CARRY_ON = "carry_on"
#: A bite's outcome when its run finished, and when it paused (`Worker._paused`).
BITE_DONE = "done"
BITE_PAUSED = "paused"
#: A run that stopped unfinished, its events covered as skipped (`Worker._cut_short`).
BITE_SKIPPED = "cut short: skipped"
def _epoch(ts: str | None) -> float | None:
    """An event's ISO stamp (`2026-09-29T05:44:59.989Z`) as epoch seconds, or None."""
    if not ts:
        return None
    from datetime import datetime, timezone

    try:
        at = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (at if at.tzinfo else at.replace(tzinfo=timezone.utc)).timestamp()


#: The writer's view of the events table: every row but those (`recorded=True`).
_RECORDED = f"(bite IS NULL OR bite != {UNRECORDED_BITE})"
#: The session's own history (`cover_before_daemon`): its chat logs and its scripts' run messages.
_HISTORY = "(stream = 'main' OR stream LIKE 'subagent:%' OR stream = 'sdk')"
#: Every row but the history a session's first worker left as context. A helper
#: agent's log is read after the main chat's chunk, so its old events can sit
#: among new ones by seq: a span of new events, and the reader's windows, skip them.
_NOT_BEFORE_DAEMON = f"(bite IS NULL OR bite != {BEFORE_DAEMON_BITE})"

class StoreVersionError(RuntimeError):
    """The store was written by a newer CLI: respawning cannot help."""


def scrub(text: str) -> str:
    if not text:
        return text
    clean, _ = secrets.redact(text)
    return clean


#: A tool call that runs no command is stored with a one-line summary of these
#: arguments as its text (lineage plan L8): what it fetched, read, or searched
#: for, so it renders in the chat and `session(op=search)` finds it. In this
#: order; any other short scalar argument follows them.
SUMMARY_KEYS = ("url", "file_path", "path", "notebook_path", "pattern", "query", "glob", "description",
                "prompt")
#: Arguments that are the content a call carries, not what it points at
#: (`old` / `new`: the daemon writer's own `edit`, and any harness tool
#: spelled the same way).
_CONTENT_KEYS = frozenset({"content", "new_string", "old_string", "edits", "new_source", "body", "text",
                           "todos", "plan", "old", "new"})
SUMMARY_VALUE_CHARS = 200
SUMMARY_CHARS = 600


def call_summary(tool_input: dict) -> str:
    """`url=https://arxiv.org/abs/2401.00001 · prompt=the method section`: one
    line of a tool call's key arguments (strings and numbers, each cut at
    `SUMMARY_VALUE_CHARS`), "" when it has none. Never a command: the working
    folders are read from commands (`folders.py`)."""
    keys = [k for k in SUMMARY_KEYS if k in tool_input]
    keys += [k for k in tool_input if k not in SUMMARY_KEYS and k not in _CONTENT_KEYS]
    parts: list[str] = []
    for key in keys:
        value = tool_input.get(key)
        if isinstance(value, bool) or not isinstance(value, (str, int, float)):
            continue
        text = " ".join(str(value).split())
        if not text:
            continue
        if len(text) > SUMMARY_VALUE_CHARS:
            text = text[:SUMMARY_VALUE_CHARS - 1] + "…"
        parts.append(f"{key}={text}")
    return " · ".join(parts)[:SUMMARY_CHARS]


def _cap(text: str) -> str:
    if len(text) <= MAX_STORED_CHARS:
        return text
    half = MAX_STORED_CHARS // 2
    from probe.daemon import toolset

    how = toolset.pick("session op=open", "probe daemon session open")  # NEW (bite/bash-markers.NEW.md)
    return f"{text[:half]}\n[... {len(text) - MAX_STORED_CHARS:,} characters not stored; {how} reads them ...]\n{text[-half:]}"


@dataclass
class StoredEvent:
    seq: int
    event_id: str
    stream: str
    kind: Kind
    turn: int
    ts: str | None
    noticed: float
    text: str
    tool: str | None
    call_id: str | None
    command: str | None
    is_error: bool
    side_file: str | None
    chars: int
    bite: int | None
    offset: int
    #: A daemon tag shown with the event (`.probe.config` `read`), or None.
    note: str | None = None
    #: The folder the event ran in, when the harness said.
    cwd: str | None = None
    #: `events.READER_SOURCE` for a message the daemon's reader handed the agent.
    source: str | None = None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "StoredEvent":
        return cls(seq=row["seq"], event_id=row["event_id"], stream=row["stream"], kind=Kind(row["kind"]),
                   turn=row["turn"], ts=row["ts"], noticed=row["noticed"], text=row["text"], tool=row["tool"],
                   call_id=row["call_id"], command=row["command"], is_error=bool(row["is_error"]),
                   side_file=row["side_file"], chars=row["chars"], bite=row["bite"], offset=row["offset"],
                   note=row["note"] if "note" in row.keys() else None,
                   cwd=row["cwd"] if "cwd" in row.keys() else None,
                   source=row["source"] if "source" in row.keys() else None)


class Store:
    def __init__(self, path: Path, *, clock=time.time) -> None:
        self.path = path
        self.clock = clock
        #: Told each bite's end as `close_bite` records it (the worker's trace),
        #: and each reader turn's as `close_read_turn` does (the reader's).
        self.on_bite_closed: Callable[[dict], None] | None = None
        self.on_read_turn_closed: Callable[[dict], None] | None = None
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(path), timeout=30, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA busy_timeout=30000")
        self.db.executescript(_SCHEMA)
        self._add_column("conversations", "fingerprint", "TEXT")
        self._add_column("events", "note", "TEXT")
        self._add_column("events", "source", "TEXT")
        # Covers `shown_turn_sizes`, which sizes the reader's messages apart, without
        # reading the event text pages. Made after the column, so a store from an
        # earlier build gets it here.
        self.db.execute("CREATE INDEX IF NOT EXISTS events_sizes_source ON events (turn, kind, source, chars)")
        for column, kind in (("inode", "INTEGER"), ("tail_hash", "TEXT"), ("tail_at", "INTEGER")):
            self._add_column("cursors", column, kind)
        version = self.meta("format_version")
        if version is None:
            self.set_meta("format_version", str(FORMAT_VERSION))
        elif int(version) > FORMAT_VERSION:
            raise StoreVersionError(f"daemon store {path} is format {version}, newer than this CLI: upgrade the CLI")

    def close(self) -> None:
        self.db.close()

    def _add_column(self, table: str, column: str, kind: str) -> None:
        """A column a store written by an earlier build of this format lacks."""
        if column in {r["name"] for r in self.db.execute(f"PRAGMA table_info({table})")}:
            return
        try:
            self.db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {kind}")
        except sqlite3.OperationalError:  # another process added it first
            if column not in {r["name"] for r in self.db.execute(f"PRAGMA table_info({table})")}:
                raise

    @contextmanager
    def tx(self) -> Iterator[sqlite3.Connection]:
        """One transaction. The writer and the reader share this connection on one
        event loop, so no `await` may sit inside a `tx()` block: a statement from
        the other lane would land inside this transaction. Nested, it raises."""
        if self.db.in_transaction:
            raise RuntimeError("a store transaction is already open (no await may sit inside store.tx())")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield self.db
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
        self.db.execute("COMMIT")

    # -- meta / facts --
    def meta(self, key: str) -> str | None:
        row = self.db.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    def set_meta(self, key: str, value: str) -> None:
        self.db.execute("INSERT INTO meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                        (key, value))

    def fact(self, key: str, default=None):
        row = self.db.execute("SELECT value FROM facts WHERE key = ?", (key,)).fetchone()
        return json.loads(row["value"]) if row else default

    def set_fact(self, key: str, value) -> None:
        self.db.execute("INSERT INTO facts (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                        (key, json.dumps(value)))

    # -- cursors --
    def cursor(self, stream: str) -> tuple[str | None, int]:
        row = self.db.execute("SELECT path, offset FROM cursors WHERE stream = ?", (stream,)).fetchone()
        return (row["path"], row["offset"]) if row else (None, 0)

    def set_cursor(self, stream: str, path: str, offset: int, *, inode: int | None = None,
                   tail_hash: str | None = None) -> None:
        """`inode` and `tail_hash` (the file's, and a hash of the bytes just before
        `offset`) are what the next read checks the file against; `tail_at`
        records the offset they hold for. A CLI from before them updates only the
        offset, which leaves `tail_at` behind: the guard then no longer applies."""
        tail_at = offset if tail_hash is not None else None
        self.db.execute("INSERT INTO cursors (stream, path, offset, inode, tail_hash, tail_at) "
                        "VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(stream) DO UPDATE SET path = excluded.path, "
                        "offset = excluded.offset, inode = excluded.inode, tail_hash = excluded.tail_hash, "
                        "tail_at = excluded.tail_at",
                        (stream, path, offset, inode, tail_hash, tail_at))

    def cursor_guard(self, stream: str) -> tuple[int | None, str | None]:
        """The `(inode, tail_hash)` the stream's cursor was saved with, or `(None,
        None)` when there is none for its current offset (a store from before the
        guard, or a cursor an older CLI moved since)."""
        row = self.db.execute("SELECT offset, inode, tail_hash, tail_at FROM cursors WHERE stream = ?",
                              (stream,)).fetchone()
        if row is None or row["tail_hash"] is None or row["tail_at"] != row["offset"]:
            return None, None
        return row["inode"], row["tail_hash"]

    # -- events --
    def current_turn(self) -> int:
        row = self.db.execute("SELECT max(turn) AS t FROM events").fetchone()
        return int(row["t"] or 0)

    def add(self, events: list[Event], *, noticed: float | None = None) -> int:
        """Store events (scrubbed); returns how many were new. A PROMPT on the main
        stream opens a new turn; one already stored (a rewritten log read again
        from 0) does not, so the events after it keep their turn."""
        now = self.clock() if noticed is None else noticed
        turn = self.current_turn()
        added = 0
        for ev in events:
            opens = ev.kind == Kind.PROMPT and ev.stream == "main"
            ev_turn = turn + 1 if opens else turn
            text = _cap(scrub(ev.text))
            command = scrub(ev.command()) or None
            tool_input = None
            chars = len(ev.text or "") + len(command or "")
            if ev.tool_input:
                redacted, _ = secrets.redact_event(ev.tool_input)
                tool_input = json.dumps(redacted if isinstance(redacted, dict) else {}, default=str)[:MAX_STORED_CHARS]
                if ev.kind == Kind.TOOL_CALL and not command and not text and isinstance(redacted, dict):
                    # A WebFetch, a Read, an MCP call: its arguments ARE the event (L8).
                    text = scrub(call_summary(redacted))
                    chars += len(text)
            cur = self.db.execute(
                "INSERT OR IGNORE INTO events (event_id, stream, offset, idx, kind, turn, ts, noticed, text, tool, "
                "call_id, command, tool_input, is_error, side_file, parent, cwd, chars, note, source) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ev.event_id, ev.stream, ev.offset, ev.index, ev.kind.value,
                 max(ev_turn, 1) if ev.kind != Kind.PROMPT else ev_turn,
                 ev.ts, now, text, ev.tool, ev.call_id, command, tool_input, int(ev.is_error), ev.side_file,
                 ev.parent, ev.cwd, chars, getattr(ev, "note", None), getattr(ev, "source", None)),
            )
            added += cur.rowcount
            if opens and cur.rowcount:
                turn = ev_turn
        return added

    def pending(self, *, limit: int | None = None) -> list[StoredEvent]:
        """Events no finished bite has covered yet, in order."""
        sql = "SELECT * FROM events WHERE bite IS NULL ORDER BY seq"
        if limit:
            sql += f" LIMIT {int(limit)}"
        return [StoredEvent.from_row(r) for r in self.db.execute(sql)]

    def queued(self) -> int:
        """How many events no finished bite has covered yet (deferred ones included)."""
        return int(self.db.execute("SELECT count(*) AS n FROM events WHERE bite IS NULL OR bite = -1").fetchone()["n"])

    def pending_count(self, first_seq: int, last_seq: int) -> int:
        """How many events from `first_seq` to `last_seq` no bite has covered yet."""
        return int(self.db.execute("SELECT count(*) AS n FROM events WHERE bite IS NULL AND seq BETWEEN ? AND ?",
                                   (first_seq, last_seq)).fetchone()["n"])

    def mark_covered(self, bite_id: int, last_seq: int) -> None:
        self.db.execute("UPDATE events SET bite = ? WHERE bite IS NULL AND seq <= ?", (bite_id, last_seq))

    def next_seq(self) -> int:
        """The seq the next stored event will get (at least)."""
        row = self.db.execute("SELECT max(seq) AS s FROM events").fetchone()
        return int(row["s"] or 0) + 1

    def leave_unrecorded(self, first_seq: int) -> int:
        """Mark every uncovered event from `first_seq` on as never to be recorded
        (`read only (daemon)`: the reader reads them, no bite ever covers them)."""
        cur = self.db.execute("UPDATE events SET bite = ? WHERE bite IS NULL AND seq >= ?",
                              (UNRECORDED_BITE, first_seq))
        return cur.rowcount

    def leave_unrecorded_before(self, first_seq: int, until: float) -> int:
        """`leave_unrecorded`, but only for events stamped before `until` (epoch
        seconds): the rest of a read-only interval a worker reads only after the
        switch is back on. An event with no readable stamp stays the writer's."""
        rows = self.db.execute("SELECT seq, ts FROM events WHERE bite IS NULL AND seq >= ?", (first_seq,)).fetchall()
        seqs = [r["seq"] for r in rows if (at := _epoch(r["ts"])) is not None and at < until]
        for seq in seqs:
            self.db.execute("UPDATE events SET bite = ? WHERE seq = ?", (UNRECORDED_BITE, seq))
        return len(seqs)

    def newest_stamp(self) -> float | None:
        """The latest readable stamp of the session's own history (`_HISTORY`: its
        chat logs and its scripts' run messages, all on the machine's clock), or None."""
        stamps = [at for (ts,) in self.db.execute(f"SELECT ts FROM events WHERE {_HISTORY}")
                  if (at := _epoch(ts)) is not None]
        return max(stamps) if stamps else None

    def first_uncovered_seq(self) -> int | None:
        row = self.db.execute("SELECT min(seq) AS s FROM events WHERE bite IS NULL").fetchone()
        return int(row["s"]) if row is not None and row["s"] is not None else None

    def cover_before_daemon(self, until: float) -> tuple[int, int, int]:
        """Inside a transaction: every uncovered event stamped before `until` (epoch
        seconds) of the session's own history (`_HISTORY`) becomes BEFORE_DAEMON_BITE.
        Anything else stays new -- a request to the writer (answered however old it
        is), a reader message, a daemon notice, a file change -- and so does an event
        with no readable stamp. `(events marked, first turn, last turn)`."""
        rows = self.db.execute(f"SELECT seq, ts, turn FROM events WHERE bite IS NULL AND {_HISTORY}").fetchall()
        hits = [(int(r["seq"]), int(r["turn"] or 0)) for r in rows
                if (at := _epoch(r["ts"])) is not None and at < until]
        if not hits:
            return 0, 0, 0
        # A helper agent's marker has no stamp of its own: it is history when the
        # agent's first stamped line is.
        markers = self.db.execute("SELECT seq, stream, turn FROM events WHERE bite IS NULL AND kind = ? "
                                  "AND ts IS NULL", (Kind.SUBAGENT.value,)).fetchall()
        if markers:
            first: dict[str, float] = {}  # one pass, never a scan per helper
            for stream, ts in self.db.execute("SELECT stream, ts FROM events WHERE stream LIKE 'subagent:%' "
                                              "AND ts IS NOT NULL"):
                if (at := _epoch(ts)) is not None and at < first.get(stream, float("inf")):
                    first[stream] = at
            hits += [(int(r["seq"]), int(r["turn"] or 0)) for r in markers if first.get(r["stream"], until) < until]
        self.db.executemany("UPDATE events SET bite = ? WHERE seq = ? AND bite IS NULL",
                            [(BEFORE_DAEMON_BITE, seq) for seq, _ in hits])
        turns = [turn for _, turn in hits]
        return len(hits), min(turns), max(turns)

    def leave_unrecorded_in(self, intervals: list[tuple[float, float | None]], *,
                            after_seq: int = 0) -> list[tuple[float, int]]:
        """Mark every uncovered event after `after_seq` stamped inside one of
        `intervals` (`(since, until)` epoch seconds, `until` None while still open)
        as never to be recorded: the researcher had Probe inline then (`/probe
        inline`, the agent's to record). Returns `(since, turn)` for each event marked, `since` naming its
        interval. An event with no readable stamp stays the writer's. One
        transaction, opened only when there is something to mark."""
        rows = self.db.execute("SELECT seq, ts, turn FROM events WHERE bite IS NULL AND seq > ?",
                               (after_seq,)).fetchall()
        hits: list[tuple[int, float, int]] = []
        for row in rows:
            at = _epoch(row["ts"])
            if at is None:
                continue
            since = next((s for s, u in intervals if s <= at and (u is None or at < u)), None)
            if since is not None:
                hits.append((row["seq"], since, int(row["turn"] or 0)))
        if hits:
            with self.tx():
                self.db.executemany("UPDATE events SET bite = ? WHERE seq = ? AND bite IS NULL",
                                    [(UNRECORDED_BITE, seq) for seq, _since, _turn in hits])
        return [(since, turn) for _seq, since, turn in hits]

    def next_offset(self) -> int:
        """A fresh offset for the daemon's own events (notices, folder changes, SDK
        messages): a per-store counter, never the clock -- a clock that jumps back
        would reuse an id, and INSERT OR IGNORE would silently drop the event."""
        value = int(self.meta("synthetic_offset") or 0) + 1
        self.set_meta("synthetic_offset", str(value))
        return value

    def defer(self, first_seq: int, last_seq: int) -> bool:
        """Move a failing range to the back of the queue, when later events wait
        (they go first). False when nothing later waits."""
        later = self.db.execute("SELECT count(*) AS n FROM events WHERE bite IS NULL AND seq > ?",
                                (last_seq,)).fetchone()["n"]
        if not later:
            return False
        with self.tx():
            self.db.execute("UPDATE events SET noticed = ?, bite = -1 WHERE bite IS NULL AND seq BETWEEN ? AND ?",
                            (self.clock(), first_seq, last_seq))
            self.set_fact("deferred_from", first_seq)
        return True

    def requeue_paused(self) -> int:
        """Inside a transaction: the events of the NEWEST run that paused, unless a
        run finished after it, back on the queue (how many). Only that run's: an
        earlier one was carried on by the next, and a fresh start over all of
        them would repeat every write they made (review 10-13). Its first event
        is the requeued bite's first, so a command it repeats keeps its
        Idempotency-Key (`tools._op_id`, seeded by the bite's first event)."""
        for row in self.db.execute("SELECT id, outcome FROM bites ORDER BY id DESC"):
            if row["outcome"] == BITE_DONE:
                return 0
            if row["outcome"] == BITE_PAUSED:
                # A carry-on that paused again with no new events of its own covered
                # none: the work it carried on is the run before it (review 10-13).
                n = self.db.execute("UPDATE events SET bite = NULL WHERE bite = ?", (int(row["id"]),)).rowcount
                if n:
                    return n
        return 0

    def requeue_deferred(self) -> bool:
        """Deferred events come back once nothing else is pending."""
        if not self.fact("deferred_from") or self.pending(limit=1):
            return False
        with self.tx():
            self.db.execute("UPDATE events SET bite = NULL WHERE bite = -1")
            self.set_fact("deferred_from", None)
        return True

    def events_upto(self, after: int, last: int, limit: int) -> list[StoredEvent]:
        """The newest `limit` events after `after` up to `last`, oldest first (seq
        numbers have gaps: an ignored duplicate still uses one up)."""
        rows = self.db.execute(f"SELECT * FROM events WHERE seq > ? AND seq <= ? AND {_NOT_BEFORE_DAEMON} "
                               "ORDER BY seq DESC LIMIT ?", (int(after), int(last), int(limit)))
        return [StoredEvent.from_row(r) for r in rows][::-1]

    def newest_seq(self) -> int:
        """The newest event's seq number (0 with none)."""
        row = self.db.execute("SELECT max(seq) AS s FROM events").fetchone()
        return int(row["s"]) if row is not None and row["s"] is not None else 0

    def events_after(self, seq: int, limit: int) -> list[StoredEvent]:
        """At most `limit` events after `seq`, oldest first: one window, never
        the whole backlog."""
        return [StoredEvent.from_row(r) for r in self.db.execute(
            f"SELECT * FROM events WHERE seq > ? AND {_NOT_BEFORE_DAEMON} ORDER BY seq LIMIT ?",
            (int(seq), int(limit)))]

    def events_between(self, first_seq: int, last_seq: int | None = None, *,
                       recorded: bool = False, new: bool = False) -> list[StoredEvent]:
        """`recorded`: the writer's view -- no event from `read only (daemon)`.
        `new`: a span of new events -- none of the history a first worker left as context."""
        only = (f" AND {_RECORDED}" if recorded else "") + (f" AND {_NOT_BEFORE_DAEMON}" if new else "")
        if last_seq is None:
            rows = self.db.execute(f"SELECT * FROM events WHERE seq >= ?{only} ORDER BY seq", (first_seq,))
        else:
            rows = self.db.execute(f"SELECT * FROM events WHERE seq BETWEEN ? AND ?{only} ORDER BY seq",
                                   (first_seq, last_seq))
        return [StoredEvent.from_row(r) for r in rows]

    def gate_rows(self, after_seq: int, *, limit: int = 2000) -> list[sqlite3.Row]:
        """What the ML gate reads (`gate.py`): every event after `after_seq`,
        recorded or not, with its tool arguments (the code a call wrote)."""
        return self.db.execute(
            "SELECT seq, stream, kind, turn, text, tool, command, tool_input FROM events "
            "WHERE seq > ? ORDER BY seq LIMIT ?", (after_seq, int(limit))).fetchall()

    def digest_rows(self) -> list[sqlite3.Row]:
        """The ML gate's digest (`gate.digest`): the researcher's prompts, the
        messages other agents sent the session (`PEER_TOOL`) and the agent's tool
        calls, oldest first -- never a tool's output."""
        return self.db.execute(
            "SELECT seq, stream, kind, text, tool, command, tool_input FROM events "
            "WHERE kind IN ('prompt', 'tool_call') OR (kind = 'meta' AND tool = ?) ORDER BY seq",
            (PEER_TOOL,)).fetchall()

    def first_seq_of_turn(self, turn: int) -> int | None:
        row = self.db.execute("SELECT min(seq) AS s FROM events WHERE turn = ?", (turn,)).fetchone()
        return int(row["s"]) if row is not None and row["s"] is not None else None

    def shown_turn_sizes(self) -> list[tuple[int, int, int]]:
        """`[(turn, first_seq, characters as the model sees the turn)]`: outputs are a
        one-line tag, long texts are capped, the reader's messages show whole up to
        the text cap (`bite.render`, `bite.shown_chars`). Rows from `read only
        (daemon)` count too: filtering on `bite` would lose the covering index
        (`events_sizes_source`), and they only make the writer's window start later."""
        rows = self.db.execute(
            "SELECT turn, min(seq) AS s, sum(CASE "
            f"WHEN source IN ('{READER_SOURCE}', '{REQUEST_SOURCE}') THEN min(chars, 20000) + 40 "
            "WHEN kind = 'tool_output' THEN 90 "
            "WHEN kind = 'agent_reasoning' THEN min(chars, 2000) + 40 "
            "WHEN kind IN ('meta', 'subagent') THEN min(chars, 300) + 40 "
            "WHEN kind = 'tool_call' THEN min(chars, 4000) + 40 "
            "ELSE min(chars, 20000) + 40 END) AS c FROM events GROUP BY turn ORDER BY turn")
        return [(r["turn"], r["s"], int(r["c"] or 0)) for r in rows]

    def turn_of(self, seq: int) -> int:
        row = self.db.execute("SELECT turn FROM events WHERE seq = ?", (seq,)).fetchone()
        return int(row["turn"]) if row else self.current_turn()

    def totals(self, *, recorded: bool = False) -> dict:
        only = f" WHERE {_RECORDED}" if recorded else ""
        row = self.db.execute(
            "SELECT count(*) AS n, coalesce(sum(chars), 0) AS c, "
            f"sum(CASE WHEN kind = 'prompt' THEN 1 ELSE 0 END) AS prompts, max(turn) AS turns FROM events{only}"
        ).fetchone()
        return {"events": row["n"], "chars": row["c"], "prompts": row["prompts"] or 0, "turns": row["turns"] or 0}

    def counts_before(self, seq: int, *, recorded: bool = False) -> dict:
        only = f" AND {_RECORDED}" if recorded else ""
        row = self.db.execute(
            "SELECT count(*) AS n, coalesce(sum(chars), 0) AS c, "
            "sum(CASE WHEN kind = 'prompt' THEN 1 ELSE 0 END) AS prompts, max(turn) AS last_turn "
            f"FROM events WHERE seq < ?{only}", (seq,)
        ).fetchone()
        return {"events": row["n"], "chars": row["c"], "prompts": row["prompts"] or 0, "last_turn": row["last_turn"] or 0}

    def call_for(self, call_id: str | None, *, recorded: bool = False) -> StoredEvent | None:
        if not call_id:
            return None
        only = f" AND {_RECORDED}" if recorded else ""
        row = self.db.execute(f"SELECT * FROM events WHERE call_id = ? AND kind = 'tool_call'{only} ORDER BY seq LIMIT 1",
                              (call_id,)).fetchone()
        return StoredEvent.from_row(row) if row else None

    def get(self, event_id: str, *, recorded: bool = False) -> StoredEvent | None:
        only = f" AND {_RECORDED}" if recorded else ""
        row = self.db.execute(f"SELECT * FROM events WHERE event_id = ?{only}", (event_id,)).fetchone()
        return StoredEvent.from_row(row) if row else None

    def search(self, query: str, *, kinds: list[str] | None = None, turn_from: int | None = None,
               turn_to: int | None = None, limit: int = 20, recorded: bool = False) -> list[StoredEvent]:
        """Full-text search; `query` is plain words (quoted into an FTS phrase list).
        `recorded`: the writer's view."""
        words = [w for w in query.replace('"', " ").split() if w]
        if not words:
            return []
        match = " ".join(f'"{w}"' for w in words)
        sql = ("SELECT e.* FROM events_fts f JOIN events e ON e.seq = f.rowid WHERE events_fts MATCH ?")
        args: list = [match]
        if kinds:
            sql += f" AND e.kind IN ({','.join('?' * len(kinds))})"
            args += kinds
        if turn_from is not None:
            sql += " AND e.turn >= ?"
            args.append(turn_from)
        if turn_to is not None:
            sql += " AND e.turn <= ?"
            args.append(turn_to)
        if recorded:
            sql += f" AND (e.bite IS NULL OR e.bite != {UNRECORDED_BITE})"
        sql += " ORDER BY e.seq DESC LIMIT ?"
        args.append(limit)
        return [StoredEvent.from_row(r) for r in self.db.execute(sql, args)]

    # -- bites --
    def open_bite(self, trigger: str, first_seq: int | None, last_seq: int | None) -> int:
        cur = self.db.execute("INSERT INTO bites (started, trigger, first_seq, last_seq) VALUES (?, ?, ?, ?)",
                              (self.clock(), trigger, first_seq, last_seq))
        return int(cur.lastrowid)

    def close_bite(self, bite_id: int, *, outcome: str, error: str | None = None, input_tokens: int = 0,
                   output_tokens: int = 0, cached_tokens: int = 0) -> None:
        self.db.execute("UPDATE bites SET ended = ?, outcome = ?, error = ?, input_tokens = ?, output_tokens = ?, "
                        "cached_tokens = ?, attempts = attempts + 1 WHERE id = ?",
                        (self.clock(), outcome, error, input_tokens, output_tokens, cached_tokens, bite_id))
        if self.on_bite_closed is not None:
            self.on_bite_closed({"bite": bite_id, "outcome": outcome, "error": error, "input_tokens": input_tokens,
                                 "output_tokens": output_tokens, "cached_tokens": cached_tokens})

    def recent_bites(self, limit: int = 10) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM bites ORDER BY id DESC LIMIT ?", (limit,)))

    def tokens_today(self) -> int:
        since = self.clock() - 86400
        row = self.db.execute("SELECT coalesce(sum(input_tokens + output_tokens), 0) AS t FROM bites WHERE started >= ?",
                              (since,)).fetchone()
        return int(row["t"])

    # -- logbook --
    def log_write(self, *, bite: int | None, op_id: str, argv: list[str], head: str, status: str,
                  reason: str | None = None, output: str | None = None, exit_code: int | None = None,
                  request: str | None = None) -> int:
        cur = self.db.execute(
            "INSERT INTO writes (bite, op_id, at, argv, head, status, reason, output, exit_code, request) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (bite, op_id, self.clock(), json.dumps([scrub(a) for a in argv]), head, status, reason,
             scrub(output or "")[:20_000] if output is not None else None, exit_code, request),
        )
        return int(cur.lastrowid)

    def update_write(self, row_id: int, *, status: str, reason: str | None, output: str | None = None,
                     exit_code: int | None = None) -> None:
        """A logbook line written before its command ran (`running`), now with how it ended."""
        self.db.execute("UPDATE writes SET status = ?, reason = ?, output = ?, exit_code = ? WHERE id = ?",
                        (status, reason, scrub(output or "")[:20_000] if output is not None else None, exit_code,
                         row_id))

    def recent_writes(self, limit: int = 10) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM writes WHERE status != 'read' ORDER BY id DESC LIMIT ?", (limit,)))

    def open_failures(self, *, bites: int, limit: int) -> list[sqlite3.Row]:
        """Failed, refused or queued writes of the last `bites` bites that no
        later write of the same command and target ran after: what is still NOT
        recorded. A queued write (Probe did not answer; the outbox sends it
        later) stands in for an earlier failure of the same command."""
        row = self.db.execute("SELECT min(started) AS s FROM (SELECT started FROM bites ORDER BY id DESC LIMIT ?)",
                              (bites,)).fetchone()
        rows = self.db.execute("SELECT * FROM writes WHERE at >= ? AND status IN ('failed', 'not_run', 'ran', "
                               "'queued') ORDER BY id", (row["s"] or 0,))
        open_: dict[tuple[str, str], sqlite3.Row] = {}
        for r in rows:
            key = (r["head"], write_target(r["head"], json.loads(r["argv"])))
            if r["status"] == "ran":
                open_.pop(key, None)
            else:
                open_[key] = r
        return sorted(open_.values(), key=lambda r: r["id"], reverse=True)[:limit]

    def filed(self, limit: int = 40, *, skip_heads: tuple[str, ...] = ()) -> list[sqlite3.Row]:
        """The writes that ran, newest first, one per command and target: what the
        record holds so far, in the logbook's own words."""
        seen: set[tuple[str, str]] = set()
        out: list[sqlite3.Row] = []
        # The newest few thousand writes are plenty: this runs before every model request.
        for r in self.db.execute("SELECT * FROM writes WHERE status = 'ran' ORDER BY id DESC LIMIT 5000"):
            if r["head"] in skip_heads:
                continue
            key = (r["head"], write_target(r["head"], json.loads(r["argv"])))
            if key in seen:
                continue
            seen.add(key)
            out.append(r)
            if len(out) >= limit:
                break
        return out

    def writes_count(self) -> int:
        return int(self.db.execute("SELECT count(*) AS n FROM writes WHERE status = 'ran'").fetchone()["n"])

    def log_lookup(self, *, bite: int | None, tool: str, query: str, result: str) -> None:
        self.db.execute("INSERT INTO lookups (bite, at, tool, query, result) VALUES (?, ?, ?, ?, ?)",
                        (bite, self.clock(), tool, scrub(query)[:4000], scrub(result)[:4000]))

    def search_logbook(self, query: str, limit: int = 20, *, writes_only: bool = False) -> list[sqlite3.Row]:
        """The logbook's lines matching `query`, newest first. `writes_only` (the
        reader): the commands only -- the writer's lookups hold what it read,
        files the reader may not open, and a write's output is matched by none."""
        like = f"%{query}%"
        if writes_only:
            return list(self.db.execute(
                "SELECT 'write' AS what, id, at, argv AS body, status, reason FROM writes WHERE argv LIKE ? "
                "AND status != 'read' ORDER BY at DESC LIMIT ?", (like, limit)))
        return list(self.db.execute(
            "SELECT 'write' AS what, id, at, argv AS body, status, reason FROM writes WHERE argv LIKE ? OR output LIKE ? "
            "UNION ALL SELECT 'lookup', id, at, tool || ': ' || query, '', result FROM lookups "
            "WHERE query LIKE ? OR result LIKE ? ORDER BY at DESC LIMIT ?",
            (like, like, like, like, limit)))

    # -- each run's one-line summary --
    def note(self) -> str:
        row = self.db.execute("SELECT body FROM notes ORDER BY version DESC LIMIT 1").fetchone()
        return row["body"] if row else ""

    def set_note(self, body: str, *, bite: int | None) -> None:
        body = scrub(body.strip())
        if body and body != self.note():
            self.db.execute("INSERT INTO notes (at, bite, body) VALUES (?, ?, ?)", (self.clock(), bite, body))

    # -- model rounds (T10) --
    def add_round(self, *, bite: int | None, model: str | None, input_tokens: int, cached_tokens: int,
                  output_tokens: int, tools: list[str], usd: float | None) -> None:
        self.db.execute("INSERT INTO rounds (bite, at, model, input_tokens, cached_tokens, output_tokens, tools, usd) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (bite, self.clock(), model, int(input_tokens), int(cached_tokens), int(output_tokens),
                         json.dumps(tools), usd))

    def usage_summary(self, *, since: float | None = None) -> dict:
        """What the model rounds cost (since `since`): tokens, the cached share of the
        input, the dollars of the rounds a price is known for, and how many were not."""
        where, args = ("WHERE at >= ?", (since,)) if since is not None else ("", ())
        row = self.db.execute(
            "SELECT count(*) AS n, coalesce(sum(input_tokens), 0) AS i, coalesce(sum(cached_tokens), 0) AS c, "
            "coalesce(sum(output_tokens), 0) AS o, coalesce(sum(usd), 0) AS usd, "
            f"sum(CASE WHEN usd IS NULL THEN 1 ELSE 0 END) AS unpriced FROM rounds {where}", args).fetchone()
        models = [r["model"] for r in self.db.execute(
            f"SELECT DISTINCT model FROM rounds {where} ORDER BY model", args) if r["model"]]
        return {"rounds": int(row["n"]), "input_tokens": int(row["i"]), "cached_tokens": int(row["c"]),
                "output_tokens": int(row["o"]), "usd": float(row["usd"] or 0.0),
                "unpriced_rounds": int(row["unpriced"] or 0), "models": models}

    # -- the conversation (T15) --
    def live_conversation(self) -> sqlite3.Row | None:
        return self.db.execute("SELECT * FROM conversations WHERE ended IS NULL ORDER BY id DESC LIMIT 1").fetchone()

    def start_conversation(self, instructions: str, fingerprint: str | None = None) -> int:
        """A fresh conversation (any live one ends first): its instructions are fixed
        for its life, so the cached prefix every later run sends stays the same.
        `fingerprint`: what made it (`Worker._fingerprint`); a resume checks it."""
        live = self.live_conversation()
        if live is not None:
            self.end_conversation(live["id"], "replaced by a fresh start")
        cur = self.db.execute("INSERT INTO conversations (started, instructions, fingerprint) VALUES (?, ?, ?)",
                              (self.clock(), instructions, fingerprint))
        return int(cur.lastrowid)

    def set_conversation_instructions(self, conversation_id: int, instructions: str,
                                      fingerprint: str | None = None) -> None:
        """A conversation whose first run never finished starts again with today's facts."""
        self.db.execute("UPDATE conversations SET instructions = ?, fingerprint = ? WHERE id = ?",
                        (instructions, fingerprint, conversation_id))

    def save_conversation(self, conversation_id: int, messages: str, *, compactions: int = 0) -> None:
        """The history after a run that finished (its compactions counted)."""
        self.db.execute("UPDATE conversations SET messages = ?, updated = ?, runs = runs + 1, "
                        "compactions = compactions + ? WHERE id = ?",
                        (messages, self.clock(), int(compactions), conversation_id))

    def end_conversation(self, conversation_id: int, reason: str) -> None:
        """No run continues it: the next one starts fresh from disk. Only the last
        KEEP_ENDED_HISTORIES ended conversations keep their history."""
        self.db.execute("UPDATE conversations SET ended = ?, end_reason = ? WHERE id = ? AND ended IS NULL",
                        (self.clock(), reason[:500], conversation_id))
        self.db.execute("UPDATE conversations SET messages = NULL WHERE ended IS NOT NULL AND id NOT IN "
                        "(SELECT id FROM conversations WHERE ended IS NOT NULL ORDER BY id DESC LIMIT ?)",
                        (KEEP_ENDED_HISTORIES,))

    # -- the reader (daemon reads): its own tables, never the writer's ----------
    #: The reader's conversation lives in `read_conversations`, NOT a column on
    #: `conversations`: `live_conversation()` above picks any open row, so an older
    #: CLI opening this store would adopt the reader's conversation as the writer's.
    def live_read_conversation(self) -> sqlite3.Row | None:
        return self.db.execute("SELECT * FROM read_conversations WHERE ended IS NULL "
                               "ORDER BY id DESC LIMIT 1").fetchone()

    def start_read_conversation(self, instructions: str, fingerprint: str | None = None) -> int:
        live = self.live_read_conversation()
        if live is not None:
            self.end_read_conversation(live["id"], "replaced by a fresh start")
        cur = self.db.execute("INSERT INTO read_conversations (started, instructions, fingerprint) VALUES (?, ?, ?)",
                              (self.clock(), instructions, fingerprint))
        return int(cur.lastrowid)

    def save_read_conversation(self, conversation_id: int, messages: str, *, compactions: int = 0) -> None:
        self.db.execute("UPDATE read_conversations SET messages = ?, updated = ?, runs = runs + 1, "
                        "compactions = compactions + ? WHERE id = ?",
                        (messages, self.clock(), int(compactions), conversation_id))

    def end_read_conversation(self, conversation_id: int, reason: str) -> None:
        self.db.execute("UPDATE read_conversations SET ended = ?, end_reason = ? WHERE id = ? AND ended IS NULL",
                        (self.clock(), reason[:500], conversation_id))
        self.db.execute("UPDATE read_conversations SET messages = NULL WHERE ended IS NOT NULL AND id NOT IN "
                        "(SELECT id FROM read_conversations WHERE ended IS NOT NULL ORDER BY id DESC LIMIT ?)",
                        (KEEP_ENDED_HISTORIES,))

    def add_read_ask(self, ask_id: str, question: str, asked_at: float, wait: bool) -> bool:
        """Store an ask the mailbox handed over. False: already stored."""
        cur = self.db.execute("INSERT OR IGNORE INTO read_asks (id, question, asked_at, wait, taken_at) "
                              "VALUES (?, ?, ?, ?, ?)", (ask_id, question, asked_at, int(wait), self.clock()))
        return cur.rowcount > 0

    def waiting_read_asks(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM read_asks WHERE state = 'waiting' ORDER BY asked_at, id"))

    def end_read_ask(self, ask_id: str, state: str, reason: str | None = None) -> None:
        self.db.execute("UPDATE read_asks SET state = ?, ended_at = ?, reason = ? WHERE id = ? AND state = 'waiting'",
                        (state, self.clock(), reason, ask_id))

    def add_read_message(self, *, message_id: str, kind: str, text: str = "", ask: str | None = None,
                         question: str | None = None, reason: str | None = None,
                         origin_turn: int | None = None) -> None:
        self.db.execute("INSERT OR IGNORE INTO read_messages (id, kind, ask, question, text, reason, origin_turn, "
                        "made_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (message_id, kind, ask, question, text, reason, origin_turn, self.clock()))

    def read_ask_asked_at(self, ask_id: str) -> float | None:
        row = self.db.execute("SELECT asked_at FROM read_asks WHERE id = ?", (ask_id,)).fetchone()
        return float(row[0]) if row else None

    def read_messages(self, ids: list[str]) -> dict[str, sqlite3.Row]:
        """The reader's own messages with these ids, by id (`rid`: the row's own
        number, stable for the life of the store)."""
        out: dict[str, sqlite3.Row] = {}
        for start in range(0, len(ids), 500):
            chunk = ids[start:start + 500]
            marks = ", ".join("?" for _ in chunk)
            out.update((row["id"], row) for row in self.db.execute(
                f"SELECT rowid AS rid, * FROM read_messages WHERE id IN ({marks})", chunk))
        return out

    def unpublished_read_messages(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM read_messages WHERE published = 0 ORDER BY made_at, id"))

    def sent_read_texts(self, kinds: tuple[str, ...], limit: int) -> list[str]:
        """What the reader has said this session (rows of these `kinds`), newest
        first, at most `limit`."""
        marks = ", ".join("?" for _ in kinds)
        return [row["text"] for row in self.db.execute(
            f"SELECT text FROM read_messages WHERE kind IN ({marks}) AND text != '' "
            "ORDER BY made_at DESC, id DESC LIMIT ?", (*[str(k) for k in kinds], int(limit)))]

    def latest_ts(self, stream: str) -> str | None:
        """The stamp of the newest stored event of `stream` that has one."""
        row = self.db.execute("SELECT ts FROM events WHERE stream = ? AND ts IS NOT NULL ORDER BY seq DESC LIMIT 1",
                              (stream,)).fetchone()
        return row["ts"] if row else None

    def has_events_after(self, seq: int, *, other_than: str | None = None) -> bool:
        """Is anything stored after `seq` (on a stream other than `other_than`)? One
        row, not the backlog."""
        if other_than is None:
            return self.db.execute(f"SELECT 1 FROM events WHERE seq > ? AND {_NOT_BEFORE_DAEMON} LIMIT 1",
                                   (int(seq),)).fetchone() is not None
        return self.db.execute(f"SELECT 1 FROM events WHERE seq > ? AND stream != ? AND {_NOT_BEFORE_DAEMON} LIMIT 1",
                               (int(seq), other_than)).fetchone() is not None

    def has_prompt_after(self, seq: int, *, new: bool = False) -> bool:
        """Did the researcher type a prompt after `seq`? Anywhere in the backlog,
        not only in the first batch a turn shows. `new`: not one from the history
        a first worker left as context."""
        only = f" AND {_NOT_BEFORE_DAEMON}" if new else ""
        return self.db.execute(f"SELECT 1 FROM events WHERE seq > ? AND kind = ?{only} LIMIT 1",
                               (int(seq), Kind.PROMPT.value)).fetchone() is not None

    def mark_read_message_published(self, message_id: str) -> None:
        self.db.execute("UPDATE read_messages SET published = 1 WHERE id = ?", (message_id,))

    # -- run alerts --
    def delivered_run_alerts(self, ids: list[int]) -> set[int]:
        """Which of these server alert ids the mailbox was already handed."""
        out: set[int] = set()
        for start in range(0, len(ids), 500):
            chunk = [int(i) for i in ids[start:start + 500]]
            marks = ", ".join("?" for _ in chunk)
            out.update(int(row["id"]) for row in self.db.execute(
                f"SELECT id FROM run_alerts WHERE id IN ({marks})", chunk))
        return out

    def add_run_alerts(self, ids: list[int], message_id: str) -> None:
        """Record that these alerts went to the mailbox in message `message_id`."""
        now = self.clock()
        self.db.executemany("INSERT OR IGNORE INTO run_alerts (id, message_id, seen_at) VALUES (?, ?, ?)",
                            [(int(i), message_id, now) for i in ids])

    def open_read_turn(self, trigger: str, ask: str | None, first_seq: int | None, last_seq: int | None) -> int:
        cur = self.db.execute("INSERT INTO read_turns (started, trigger, ask, first_seq, last_seq) "
                              "VALUES (?, ?, ?, ?, ?)", (self.clock(), trigger, ask, first_seq, last_seq))
        return int(cur.lastrowid)

    def close_read_turn(self, turn_id: int, *, outcome: str, error: str | None = None, rounds: int = 0,
                        input_tokens: int = 0, cached_tokens: int = 0, output_tokens: int = 0,
                        usd: float | None = None) -> None:
        self.db.execute("UPDATE read_turns SET ended = ?, outcome = ?, error = ?, rounds = ?, input_tokens = ?, "
                        "cached_tokens = ?, output_tokens = ?, usd = ? WHERE id = ?",
                        (self.clock(), outcome, (error or "")[:500] or None, rounds, input_tokens, cached_tokens,
                         output_tokens, usd, turn_id))
        if self.on_read_turn_closed is not None:
            self.on_read_turn_closed({"turn": turn_id, "outcome": str(outcome), "error": error, "rounds": rounds,
                                      "input_tokens": input_tokens, "output_tokens": output_tokens,
                                      "cached_tokens": cached_tokens, "usd": usd})

    def read_summary(self, *, since: float | None = None) -> dict:
        """What the reader did: turns by outcome, tokens and dollars (for `probe doctor`, the benches)."""
        where, args = ("WHERE started >= ?", (since,)) if since is not None else ("", ())
        outcomes = {r["outcome"] or "running": int(r["n"]) for r in self.db.execute(
            f"SELECT outcome, count(*) AS n FROM read_turns {where} GROUP BY outcome", args)}
        row = self.db.execute(f"SELECT count(*) AS n, sum(input_tokens) AS i, sum(cached_tokens) AS c, "
                              f"sum(output_tokens) AS o, sum(usd) AS usd FROM read_turns {where}", args).fetchone()
        messages = {r["kind"]: int(r["n"]) for r in self.db.execute(
            "SELECT kind, count(*) AS n FROM read_messages GROUP BY kind")}
        return {"turns": int(row["n"] or 0), "outcomes": outcomes, "input_tokens": int(row["i"] or 0),
                "cached_tokens": int(row["c"] or 0), "output_tokens": int(row["o"] or 0),
                "usd": float(row["usd"] or 0.0), "messages": messages}

    # -- the main agent's requests to the writer, and what the writer sends back --
    def add_write_request(self, request_id: str, text: str, asked_at: float, wait: bool, event_seq: int | None,
                          *, state: str = "waiting", reason: str | None = None) -> bool:
        """Store a request the mailbox handed over. False: already stored."""
        cur = self.db.execute(
            "INSERT OR IGNORE INTO write_requests (id, text, asked_at, wait, taken_at, state, ended_at, reason, "
            "event_seq) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (request_id, text, asked_at, int(wait), self.clock(), state,
             self.clock() if state != "waiting" else None, reason, event_seq))
        return cur.rowcount > 0

    def has_write_request(self, request_id: str) -> bool:
        return self.db.execute("SELECT 1 FROM write_requests WHERE id = ?", (request_id,)).fetchone() is not None

    def waiting_write_requests(self) -> list[sqlite3.Row]:
        """Waiting requests, oldest first, with where their event stands (`event_bite`)."""
        return list(self.db.execute(
            "SELECT r.*, e.bite AS event_bite FROM write_requests r LEFT JOIN events e ON e.seq = r.event_seq "
            "WHERE r.state = 'waiting' ORDER BY r.asked_at, r.id"))

    def end_write_request(self, request_id: str, state: str, *, reason: str | None = None,
                          bite: int | None = None) -> bool:
        """Inside a transaction: close a waiting request. A failed one's event is
        retired (no bite covers it now, and none ever will: it never runs later)."""
        row = self.db.execute("SELECT event_seq FROM write_requests WHERE id = ? AND state = 'waiting'",
                              (request_id,)).fetchone()
        if row is None:
            return False
        self.db.execute("UPDATE write_requests SET state = ?, ended_at = ?, reason = ?, bite = ? WHERE id = ?",
                        (state, self.clock(), reason, bite, request_id))
        if state == "failed" and row["event_seq"] is not None:
            # Wherever it stood, a paused run's bite included: requeueing that run
            # (`requeue_paused`) must not hand it to a fresh one.
            self.db.execute("UPDATE events SET bite = ? WHERE seq = ?", (UNRECORDED_BITE, int(row["event_seq"])))
        return True

    def mark_requests_seen(self, bite_id: int, first_seq: int | None, last_seq: int | None,
                           conversation: int | None) -> None:
        """Bite `bite_id` starts: the waiting requests it shows (events
        `first_seq`..`last_seq`) were seen by it (`first_bite` keeps the first
        such bite) and belong to `conversation` (None: bites mode); it works on
        them, and on those `conversation`'s history already holds (a run of it
        covered their event), so their writes are listed with them."""
        if first_seq:
            self.db.execute("UPDATE write_requests SET first_bite = coalesce(first_bite, ?), conversation = ? "
                            "WHERE state = 'waiting' AND event_seq BETWEEN ? AND ?",
                            (bite_id, conversation, first_seq, last_seq))
        self.db.execute(
            "INSERT OR IGNORE INTO write_request_bites (request_id, bite) SELECT r.id, ? FROM write_requests r "
            "LEFT JOIN events e ON e.seq = r.event_seq WHERE r.state = 'waiting' AND r.first_bite IS NOT NULL "
            "AND (r.event_seq BETWEEN ? AND ? OR (r.conversation IS NOT NULL AND r.conversation = ? AND e.bite >= 1))",
            (bite_id, first_seq or 0, last_seq or -1, conversation if conversation is not None else -1))

    def bites_of_requests(self, first_bite: int, last_bite: int) -> set[int]:
        """The bites in `first_bite`..`last_bite` that worked on any request: their
        writes are told by that request's reply or failure, never by a receipt."""
        return {int(r["bite"]) for r in self.db.execute(
            "SELECT DISTINCT bite FROM write_request_bites WHERE bite BETWEEN ? AND ?", (first_bite, last_bite))}

    def request_bites(self, request_id: str) -> set[int]:
        return {int(r["bite"]) for r in self.db.execute(
            "SELECT bite FROM write_request_bites WHERE request_id = ?", (request_id,))}

    def writes_of_bites(self, bites: set[int] | list[int]) -> list[sqlite3.Row]:
        """The writes bites `bites` made, oldest first."""
        ids = sorted({int(b) for b in bites})
        if not ids:
            return []
        marks = ", ".join("?" * len(ids))
        return list(self.db.execute(f"SELECT * FROM writes WHERE bite IN ({marks}) ORDER BY id", ids))

    def has_pending_request(self) -> bool:
        """Does a request wait in the queue (anywhere in it)? One row."""
        return self.db.execute("SELECT 1 FROM events WHERE bite IS NULL AND source = ? LIMIT 1",
                               (REQUEST_SOURCE,)).fetchone() is not None

    def run_start(self, bite_id: int) -> int:
        """The first bite of the run that ends at `bite_id` (a paused run spans
        several): the one after the newest earlier bite that ended a run --
        finished, or skipped with requests failed (their failure told its writes,
        so the next receipt does not tell them again; a skipped run with no
        request is told by the next run's receipt)."""
        row = self.db.execute(
            "SELECT max(id) AS b FROM bites WHERE id < ? AND (outcome = ? OR (outcome = ? AND EXISTS "
            "(SELECT 1 FROM writer_messages m WHERE m.bite = bites.id AND m.kind = 'failed')))",
            (bite_id, BITE_DONE, BITE_SKIPPED)).fetchone()
        return int(row["b"] or 0) + 1

    def add_writer_message(self, *, message_id: str, kind: str, text: str = "", ask: str | None = None,
                           reason: str | None = None, bite: int | None = None) -> None:
        self.db.execute("INSERT OR IGNORE INTO writer_messages (id, kind, ask, text, reason, bite, made_at) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (message_id, kind, ask, scrub(text), scrub(reason) if reason else reason, bite,
                         self.clock()))

    def unpublished_writer_messages(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM writer_messages WHERE published = 0 ORDER BY made_at, id"))

    def mark_writer_message_published(self, message_id: str) -> None:
        self.db.execute("UPDATE writer_messages SET published = 1 WHERE id = ?", (message_id,))

    # -- folder check --
    def file_row(self, path: str) -> sqlite3.Row | None:
        return self.db.execute("SELECT * FROM files WHERE path = ?", (path,)).fetchone()

    def file_snapshot(self) -> dict[str, tuple[int, float]]:
        """`{path: (size, mtime)}` of the last folder check."""
        return {r["path"]: (r["size"], r["mtime"] or 0.0) for r in self.db.execute("SELECT path, size, mtime FROM files")}

    def stored_text_bytes(self) -> int:
        """The characters of every last-seen text copy: a running total kept in
        `meta` by `set_file`, so the folder check never sums up to 64 MB on the
        event loop. Summed once, for a store written before the total existed."""
        value = self.meta("files_text_chars")
        if value is None:
            value = str(self.db.execute("SELECT coalesce(sum(length(text)), 0) AS n FROM files").fetchone()["n"])
            self.set_meta("files_text_chars", value)
        return int(value)

    def set_file(self, path: str, size: int, mtime: float, text: str | None) -> None:
        total = self.stored_text_bytes()
        row = self.db.execute("SELECT length(text) AS n FROM files WHERE path = ?", (path,)).fetchone()
        old = int(row["n"] or 0) if row else 0
        self.db.execute("INSERT INTO files (path, size, mtime, text) VALUES (?, ?, ?, ?) ON CONFLICT(path) DO UPDATE "
                        "SET size = excluded.size, mtime = excluded.mtime, text = excluded.text",
                        (path, size, mtime, text))
        self.set_meta("files_text_chars", str(max(0, total - old + len(text or ""))))


def write_target(head: str, argv: list[str]) -> str:
    """What a logged write acted on: a shell write's command, else the first
    positional after the command's words (`probe run tag R ...` -> R), else its
    anchor option (`--run R`). `--group` is a run's sweep group (`run start
    --group`); `--artifact` went with the notes on files."""
    if head == "shell":
        return argv[-1] if argv else ""
    words = argv[1 + len(head.split()):] if argv[:1] == ["probe"] else argv
    for i, word in enumerate(words):
        if not word.startswith("-"):
            if i == 0 or not words[i - 1].startswith("--") or "=" in words[i - 1]:
                return word
    for i, word in enumerate(words[:-1]):
        if word in ("--run", "--project", "--experiment", "--group", "--note"):
            return words[i + 1]
    return ""
