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
    files      the folder check's last-seen snapshot (size, mtime, text copy; the
               check it last changed at; a growing file's size and text when it
               started growing, `folders.GROWING`)
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
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator
from ...foundation.compose.compose import compose
from probe.daemon.store.conversations import ConversationsMixin
from probe.daemon.store.events import EventsMixin
from probe.daemon.store.files import FolderCheckMixin
from probe.daemon.store.logbook import LogbookMixin
from probe.daemon.store.queue import QueueMixin
from probe.daemon.store.reader import ReaderTablesMixin
from probe.daemon.store.requests import RequestsMixin

FORMAT_VERSION = 1

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


def state_dir() -> Path:
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / "probe" / "daemon"


def store_path(session_id: str) -> Path:
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_") or "session"
    return state_dir() / f"{safe}.sqlite"

class StoreVersionError(RuntimeError):
    """The store was written by a newer CLI: respawning cannot help."""


@compose
class Store(
    EventsMixin,
    QueueMixin,
    LogbookMixin,
    ConversationsMixin,
    ReaderTablesMixin,
    RequestsMixin,
    FolderCheckMixin,
):
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
        for column, kind in (("changed_at", "INTEGER"), ("growing_size", "INTEGER"), ("growing_text", "TEXT")):
            self._add_column("files", column, kind)
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
