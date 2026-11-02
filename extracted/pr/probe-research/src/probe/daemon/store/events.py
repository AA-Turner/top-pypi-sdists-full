"""scrubbed events: store them (idempotent per stream cursor), read windows and turns, full-text search."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass

from probe.shared.harness.events import PEER_TOOL, READER_SOURCE, REQUEST_SOURCE, Event, Kind
from probe.tap_core import secrets
#: Event text kept per event in the store. A longer output keeps its head and
#: tail; the full text stays in the chat log (or its side file), one
#: `session(op=open)` away, scrubbed when read.
MAX_STORED_CHARS = 200_000

#: Kinds a person or the agent produced: what "whole turns" of the chat are made of.
#: The daemon's own observations of a run's process, not the agent's work: a
#: run start or end the SDK announced, a file the folder check found
#: (`Store.run_side_only`, swarm friction R41).
RUN_SIDE_KINDS = frozenset({Kind.RUN_EVENT.value, Kind.FILE_CHANGE.value})
CHAT_KINDS = (Kind.PROMPT, Kind.AGENT_TEXT, Kind.AGENT_REASONING, Kind.TOOL_CALL, Kind.TOOL_OUTPUT,
              Kind.SUBAGENT, Kind.COMPACTION, Kind.META, Kind.TURN_END, Kind.FILE_CHANGE, Kind.RUN_EVENT)


#: `events.bite` for an event that arrived while the switch read `read only
#: (daemon)`: the reader reads it, no bite ever covers it (-1 is a deferred one).
UNRECORDED_BITE = -2
#: `events.bite` for an event the session held before its first worker started,
#: stamped more than `worker.CATCH_UP_S` before its newest (`cover_before_daemon`):
#: covered -- context the writer sees and `session` reaches, never new.
BEFORE_DAEMON_BITE = -3


#: The writer's view of the events table: every row but those (`recorded=True`).
_RECORDED = f"(bite IS NULL OR bite != {UNRECORDED_BITE})"
#: Every row but the history a session's first worker left as context. A helper
#: agent's log is read after the main chat's chunk, so its old events can sit
#: among new ones by seq: a span of new events, and the reader's windows, skip them.
_NOT_BEFORE_DAEMON = f"(bite IS NULL OR bite != {BEFORE_DAEMON_BITE})"


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
    from probe.daemon.agent import toolset

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


class EventsMixin:
    """Part of Store: its methods run with `self` the Store; compose() folds them into Store."""

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
            current = self.db.execute(
                "INSERT OR IGNORE INTO events (event_id, stream, offset, idx, kind, turn, ts, noticed, text, tool, "
                "call_id, command, tool_input, is_error, side_file, parent, cwd, chars, note, source) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ev.event_id, ev.stream, ev.offset, ev.index, ev.kind.value,
                 max(ev_turn, 1) if ev.kind != Kind.PROMPT else ev_turn,
                 ev.ts, now, text, ev.tool, ev.call_id, command, tool_input, int(ev.is_error), ev.side_file,
                 ev.parent, ev.cwd, chars, getattr(ev, "note", None), getattr(ev, "source", None)),
            )
            added += current.rowcount
            if opens and current.rowcount:
                turn = ev_turn
        return added

    def next_seq(self) -> int:
        """The seq the next stored event will get (at least)."""
        row = self.db.execute("SELECT max(seq) AS s FROM events").fetchone()
        return int(row["s"] or 0) + 1

    def next_offset(self) -> int:
        """A fresh offset for the daemon's own events (notices, folder changes, SDK
        messages): a per-store counter, never the clock -- a clock that jumps back
        would reuse an id, and INSERT OR IGNORE would silently drop the event."""
        value = int(self.meta("synthetic_offset") or 0) + 1
        self.set_meta("synthetic_offset", str(value))
        return value

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
                       recorded: bool = False, new: bool = False, uncovered: bool = False,
                       kind: Kind | None = None) -> list[StoredEvent]:
        """`recorded`: the writer's view -- no event from `read only (daemon)`.
        `new`: a span of new events -- none of the history a first worker left as context.
        `uncovered`: none a finished bite covered already (a run event an earlier
        bite showed first, `bite.runs_ahead`). `kind`: only events of that kind."""
        only = ((f" AND {_RECORDED}" if recorded else "") + (f" AND {_NOT_BEFORE_DAEMON}" if new else "")
                + (" AND (bite IS NULL OR bite < 0)" if uncovered else "") + (" AND kind = ?" if kind else ""))
        tail = (kind.value,) if kind else ()
        if last_seq is None:
            rows = self.db.execute(f"SELECT * FROM events WHERE seq >= ?{only} ORDER BY seq", (first_seq, *tail))
        else:
            rows = self.db.execute(f"SELECT * FROM events WHERE seq BETWEEN ? AND ?{only} ORDER BY seq",
                                   (first_seq, last_seq, *tail))
        return [StoredEvent.from_row(r) for r in rows]

    def first_seq_of_turn(self, turn: int) -> int | None:
        row = self.db.execute("SELECT min(seq) AS s FROM events WHERE turn = ?", (turn,)).fetchone()
        return int(row["s"]) if row is not None and row["s"] is not None else None

    def shown_turn_sizes(self) -> list[tuple[int, int, int]]:
        """`[(turn, first_seq, characters as the model sees the turn)]`: outputs are a
        one-line tag, a file change one line, long texts are capped, the reader's
        messages show whole up to the text cap (`bite.render`, `bite.shown_chars`). Rows from `read only
        (daemon)` count too: filtering on `bite` would lose the covering index
        (`events_sizes_source`), and they only make the writer's window start later."""
        rows = self.db.execute(
            "SELECT turn, min(seq) AS s, sum(CASE "
            f"WHEN source IN ('{READER_SOURCE}', '{REQUEST_SOURCE}') THEN min(chars, 20000) + 40 "
            "WHEN kind = 'tool_output' THEN 90 "
            "WHEN kind = 'agent_reasoning' THEN min(chars, 2000) + 40 "
            "WHEN kind IN ('meta', 'subagent') THEN min(chars, 300) + 40 "
            "WHEN kind = 'tool_call' THEN min(chars, 4000) + 40 "
            # One line (`bite._file_line`): its first line is not a column, so flat.
            "WHEN kind = 'file_change' THEN 200 "
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

    def has_peer_message_after(self, seq: int, *, new: bool = False) -> bool:
        """Did another agent message this session (`events.PEER_TOOL`) after `seq`?
        `new` as `has_prompt_after`."""
        only = f" AND {_NOT_BEFORE_DAEMON}" if new else ""
        return self.db.execute(f"SELECT 1 FROM events WHERE seq > ? AND kind = ? AND tool = ?{only} LIMIT 1",
                               (int(seq), Kind.META.value, PEER_TOOL)).fetchone() is not None
