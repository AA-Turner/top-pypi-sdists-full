"""read each chat log from its cursor into the store: rewrites noticed, long lines skipped, history caught up."""

from __future__ import annotations
import hashlib
import json
import logging
import os
import sqlite3
from pathlib import Path
from probe.shared import mailbox
from probe.daemon.worker import alerts
from probe.shared.harness.events import (
    MAIN_STREAM,
    READER_STREAM,
    Event)
from probe.daemon.store.device import LANE_WRITE
from probe.daemon.store.queue import _epoch

log = logging.getLogger("probe.daemon")
READ_CHUNK_BYTES = 4 * 1024 * 1024
MAX_LINE_BYTES = 8 * 1024 * 1024
#: A chat log's bytes just before its cursor that are hashed with the cursor: a
#: file rewritten under the cursor shows there (`Worker._read_stream`).
GUARD_BYTES = 4 * 1024
#: Store fact (`<this>:<stream>`): the stream was rewritten under its cursor and
#: is read no more -- why, and where it stopped.
STREAM_STOPPED = "stream_stopped"
#: A rewrite seen by one poll, at this cursor; the next poll confirms or clears it.
STREAM_SUSPECT = "stream_suspect"
#: A session's first worker found history already there (switched on late, or an
#: old session resumed after the daemon became the default): only the events
#: stamped within this long of the newest are new to it; older ones are context
#: (`Store.cover_before_daemon`), and the reader starts at the current turn. Round 6
#: (2026-10-14): 13 sessions 1-38 days old were replayed whole, one of 29 days in
#: 1,980 model calls. `PROBE_DAEMON_CATCH_UP_S` overrides it.
CATCH_UP_S = 2 * 3600.0
ENV_CATCH_UP_S = "PROBE_DAEMON_CATCH_UP_S"
#: Store fact: the store was new when this session's first worker started, and the
#: history it found is still being read (`Worker._catch_up` decides once it is).
CATCH_UP_PENDING = "catch_up_pending"


def catch_up_s() -> float:
    raw = (os.environ.get(ENV_CATCH_UP_S) or "").strip()
    try:
        return max(0.0, float(raw)) if raw else CATCH_UP_S
    except ValueError:
        return CATCH_UP_S


class ReadingMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    # -- reading ------------------------------------------------------------
    def read_new(self, until: dict[str, int] | None = None) -> int:
        """One chunk of each stream. `until`: read no stream past these offsets,
        and no stream not named in it (the shutdown drain's snapshot)."""
        added = 0
        files = self.adapter.session_files(self.session.transcript)
        if until is None:
            # A helper log that is gone is never read again: never "behind" either.
            live = {"main", "sdk", *(f"subagent:{p.stem}" for p in files.subagents)}
            for stream in [s for s in self.stream_behind if s not in live]:
                del self.stream_behind[stream]
        if until is None or "main" in until:
            added += self._read_stream("main", files.main, None if until is None else until["main"])
        for path in files.subagents:
            stream = f"subagent:{path.stem}"
            if until is not None and stream not in until:
                continue
            if self.store.cursor(stream)[0] is None:
                marker = self.adapter.subagent_event(path)
                if marker is not None:
                    added += self.store.add([marker])
            added += self._read_stream(stream, path, None if until is None else until[stream])
        if until is None or "sdk" in until:
            added += self._read_inbox(None if until is None else until["sdk"])
        # Not while a chat backlog is still being read a chunk a poll: a claim is
        # placed by when it is read, so it must not come before those lines.
        if (until is None or READER_STREAM in until) and not self.stream_behind.get("main"):
            added += self._read_reader_log(None if until is None else until[READER_STREAM])
        if until is None:  # not at the shutdown drain: a request filed now waits for the next worker
            added += self._take_requests()
        self._mark_inline()
        self._catch_up()
        return added

    def catching_up(self) -> bool:
        """Is the history this session held before its first worker still being
        read? No bite and no reader turn until it is (`_catch_up`)."""
        return self._catch_up_pending

    def _catch_up(self) -> None:
        """Once every stream's history is read, a session's first worker judges it
        once: events stamped more than `catch_up_s()` before the newest are
        context, never new (the writer's window and `session` still show them);
        the reader starts at the current turn. A session the worker starts with
        holds no such events: nothing changes."""
        if not self._catch_up_pending or any(self.stream_behind.values()):
            return
        newest = self.store.newest_stamp()
        marked, first, last = 0, 0, 0
        with self.store.tx():
            if newest is not None:
                marked, first, last = self.store.cover_before_daemon(newest - catch_up_s())
            if marked:
                # The reader starts at the current turn -- or, when that turn began before
                # the cut (one long autonomous turn), at the first event still new.
                start = max(self.store.first_seq_of_turn(self.store.current_turn()) or 0,
                            self.store.first_uncovered_seq() or 0)
                if start - 1 > int(self.store.fact("read_cursor") or 0):
                    self.store.set_fact("read_cursor", start - 1)
            self.store.set_fact(CATCH_UP_PENDING, None)
        self._catch_up_pending = False
        if not marked:
            return
        # No notice to the writer: a bite already shows what is above its divider as
        # context. A notice naming the skipped turns told it the current turn was not
        # to be recorded when that turn began before the cut (round-6 bench: one of two
        # late-start runs then wrote nothing at all).
        log.info("first start on a session with history: %s events (turns %s-%s) older than %.3g h before the "
                 "newest are context, not recorded", marked, first, last, catch_up_s() / 3600)
        self.trace.write({"type": "catch_up", "events": marked, "turns": [first, last], "window_s": catch_up_s()})

    def _end_offsets(self) -> dict[str, int]:
        """Where each stream ends now: what a stopping worker still takes on."""
        files = self.adapter.session_files(self.session.transcript)
        paths = [("main", files.main), *((f"subagent:{p.stem}", p) for p in files.subagents),
                 ("sdk", inbox_path(self.session.session_id)),
                 (READER_STREAM, mailbox.claim_log_path(self.session.session_id))]
        ends: dict[str, int] = {}
        for stream, path in paths:
            try:
                ends[stream] = path.stat().st_size
            except OSError:
                continue
        return ends

    def drain(self, ends: dict[str, int]) -> int:
        """Read every stream up to `ends` (its snapshot when shutdown began), chunk
        after chunk, while the finish budget lasts -- not the one chunk a poll
        reads. Stops when no stream moves (the rest is a line still being written)."""
        added = 0
        while True:
            before = {s: self.store.cursor(s)[1] for s in ends}
            added += self.read_new(until=ends)
            if {s: self.store.cursor(s)[1] for s in ends} == before:
                return added
            if self.finish_by is not None and self.clock() >= self.finish_by:
                return added

    def _read_stream(self, stream: str, path: Path, until: int | None = None) -> int:
        """The next chunk of one chat log, from its cursor. The file must still be
        the one read so far: the same inode, no shorter than the cursor, the same
        GUARD_BYTES just before it (as saved with the cursor). A file rewritten
        under the cursor stops the stream for good (`_stop_stream`) -- never read
        again from 0, where event ids (`<stream>:<offset>:<index>`) would pass old
        events off as new, nor on from the cursor, inside bytes it never read."""
        # Set again below when there is more than a chunk to read: a stream that stopped,
        # vanished or shrank is never "behind" (the first worker's catch-up waits on it).
        self.stream_behind[stream] = False
        if self.store.fact(f"{STREAM_STOPPED}:{stream}") is not None:
            return 0
        _, offset = self.store.cursor(stream)
        try:
            handle = path.open("rb")
        except OSError:
            return 0
        with handle:
            info = os.fstat(handle.fileno())
            inode, size = info.st_ino, info.st_size
            _known_inode, known_tail = self.store.cursor_guard(stream)
            if size < offset:
                return self._suspect(stream, offset, f"it is shorter than the {offset:,} bytes already read")
            end = size if until is None else min(size, until)
            self.stream_behind[stream] = end - offset > READ_CHUNK_BYTES
            start = max(0, offset - GUARD_BYTES)
            handle.seek(start)
            before = handle.read(offset - start)
            # The bytes decide, never the inode alone: a copy, an atomic-rename
            # writer or a network mount gives the same bytes a new inode.
            if offset and known_tail is not None and _tail_hash(before) != known_tail:
                return self._suspect(stream, offset, f"the bytes before byte {offset:,} changed")
            self._clear_suspect(stream)
            if end <= offset:
                return 0
            if self.store.fact(f"skipping_line:{stream}") == offset:
                return self._skip_line(stream, path, handle, offset, end, notice=False, inode=inode)
            buffer = handle.read(min(READ_CHUNK_BYTES, end - offset))
            if b"\n" not in buffer and len(buffer) == READ_CHUNK_BYTES:
                # One line longer than a chunk: read on for its end, up to MAX_LINE_BYTES.
                more = min(MAX_LINE_BYTES + 1, end - offset) - len(buffer)
                if more > 0:
                    buffer += handle.read(more)
                if b"\n" not in buffer and len(buffer) > MAX_LINE_BYTES:
                    return self._skip_line(stream, path, handle, offset, end, notice=True, inode=inode)
        lines: list[tuple[int, list[Event]]] = []
        pos = 0
        while True:
            nl = buffer.find(b"\n", pos)
            if nl < 0:
                break
            line = buffer[pos:nl]
            pos = nl + 1
            if not line.strip() or len(line) > MAX_LINE_BYTES:
                continue
            end = offset + pos
            try:
                target = json.loads(line)
            except ValueError:
                continue
            if not isinstance(target, dict):
                continue
            try:
                lines.append((end, self._parse(target, stream, end)))
            except Exception as exc:  # noqa: BLE001 -- one line the adapter cannot read is skipped, never a crash loop
                log.warning("skipped the line ending at %s:%s: %s: %s", stream, end, type(exc).__name__, exc)
        tail = _tail_hash((before + buffer[:pos])[-GUARD_BYTES:])
        return self._store_lines(stream, str(path), offset + pos, lines, inode=inode, tail_hash=tail)

    def _suspect(self, stream: str, offset: int, why: str) -> int:
        """A rewrite seen once is only suspected: a writer caught between
        truncating and writing the same bytes back looks like one. The stream
        stops when the next poll, at the same cursor, still sees it."""
        key = f"{STREAM_SUSPECT}:{stream}"
        if self.store.fact(key) == offset:
            return self._stop_stream(stream, offset, why)
        self.store.set_fact(key, offset)
        return 0

    def _clear_suspect(self, stream: str) -> None:
        key = f"{STREAM_SUSPECT}:{stream}"
        if self.store.fact(key) is not None:
            self.store.set_fact(key, None)

    def _stop_stream(self, stream: str, offset: int, why: str) -> int:
        """The chat log was rewritten under the cursor (Kimi Code rewrites its wire
        when it migrates an older one on resume): what it holds now cannot be told
        apart from what was read. Stop reading it, once and loudly -- a notice for
        the model, a device error line, the log -- and never start it over."""
        sid = self.session.session_id
        log.error("the chat log %s was rewritten under the cursor (%s): stopped reading it at byte %s",
                  stream, why, offset)
        with self.store.tx():
            self.store.set_fact(f"{STREAM_STOPPED}:{stream}", {"offset": offset, "why": why, "at": self.clock()})
            added = self.store.add([_notice_event(
                self.store, f"the chat log ({stream}) was rewritten in place - {why} - so the daemon stopped reading "
                            f"it at byte {offset:,}: nothing after that is in the session store")])
        _device_error(f"session {sid}: its chat log ({stream}) was rewritten in place ({why}); the daemon stopped "
                      f"reading it at byte {offset:,} instead of reading it again")
        alerts.report(alerts.Kind.CHAT_LOG_REWRITTEN, session_id=sid, lane=LANE_WRITE,
                      text=f"chat log ({stream}) rewritten in place: {why}")
        return added

    def _skip_line(self, stream: str, path: Path, handle, offset: int, end: int, *, notice: bool,
                   inode: int | None = None) -> int:
        """A line over MAX_LINE_BYTES starts at `offset`: move the cursor past its
        newline (or to `end`, remembering that the next read continues the skip),
        with a notice the first time. Never a crash, never the whole chunk after it."""
        pos = offset
        handle.seek(offset)
        is_found = False
        while pos < end:
            chunk = handle.read(min(READ_CHUNK_BYTES, end - pos))
            if not chunk:
                break
            nl = chunk.find(b"\n")
            if nl >= 0:
                pos += nl + 1
                is_found = True
                break
            pos += len(chunk)
        handle.seek(max(0, pos - GUARD_BYTES))
        tail = _tail_hash(handle.read(pos - max(0, pos - GUARD_BYTES)))
        added = 0
        with self.store.tx():
            if notice:
                log.warning("skipped a line over %s bytes at %s:%s", MAX_LINE_BYTES, stream, offset)
                cap = (f"{MAX_LINE_BYTES // (1024 * 1024)} MB" if MAX_LINE_BYTES >= 1024 * 1024
                       else f"{MAX_LINE_BYTES:,} bytes")
                added = self.store.add([_notice_event(
                    self.store, f"a transcript line over {cap} was skipped ({stream}, byte {offset:,}) - it isn't "
                                "in the session store")])
            self.store.set_fact(f"skipping_line:{stream}", None if is_found else pos)
            self.store.set_cursor(stream, str(path), pos, inode=inode, tail_hash=tail)
        return added

    def _parse(self, obj: dict, stream: str, end: int) -> list[Event]:
        if stream == MAIN_STREAM:
            # Every chat line read counts, stored or not (the hook's own copy of a
            # reader message is not stored): the reader stream waits for it.
            seen = _epoch(self.adapter.line_ts(obj))
            if seen is not None and (self.chat_seen_at is None or seen > self.chat_seen_at):
                self.chat_seen_at = seen
        mode = self.adapter.permission_mode(obj)
        if mode:
            self.store.set_fact("permission_mode", mode)
        events = list(self.adapter.parse_line(obj, stream=stream, offset=end))
        for index, ev in enumerate(events):
            ev.index = index
        # `.probe.config`: what it excludes never enters the store, so no bite,
        # reader or tool can see it. After the ids, so a kept event's id is the
        # same whatever was dropped beside it.
        line_cwd = obj.get("cwd") if isinstance(obj.get("cwd"), str) else None
        return self.exclusions.keep(events, stream=stream, line_cwd=line_cwd)

    def _store_lines(self, stream: str, path: str, cursor: int, lines: list[tuple[int, list[Event]]], *,
                     inode: int | None = None, tail_hash: str | None = None) -> int:
        """Each line's events, and the cursor past them (with the file's inode and
        the hash of the bytes before it), in one transaction. A line
        that cannot be stored is logged and skipped; only a store that cannot be
        written at all (locked, full, I/O) rolls back, to be read again."""
        added = 0
        with self.store.tx():
            for end, events in lines:
                if not events:
                    continue
                try:
                    added += self.store.add(events)
                except sqlite3.OperationalError:
                    raise
                except Exception as exc:  # noqa: BLE001
                    log.warning("skipped the line ending at %s:%s: not storable: %s: %s", stream, end,
                                type(exc).__name__, exc)
            self.store.set_cursor(stream, path, cursor, inode=inode, tail_hash=tail_hash)
        return added

    def _newest_chat(self) -> float | None:
        """The newest main chat line's time: stored, or read and not stored (the
        hook's own copy of a reader message), whichever is newer."""
        stamps = (_epoch(self.store.latest_ts(MAIN_STREAM)), self.chat_seen_at)
        return max((t for t in stamps if t is not None), default=None)

    def agent_active_at(self) -> float | None:
        """When the agent was last active in this session on this machine (epoch
        seconds): its transcript's newest chat line (`_newest_chat`), or None
        before any. The session-message poll tells Probe (G7), which moves a
        message not yet shown to the machine whose agent was active last."""
        return self._newest_chat()


def _tail_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _bytes_before_hash(path: Path, offset: int) -> str | None:
    """`_tail_hash` of the `GUARD_BYTES` before `offset` in `path`, or None."""
    try:
        with path.open("rb") as handle:
            handle.seek(max(0, offset - GUARD_BYTES))
            return _tail_hash(handle.read(offset - max(0, offset - GUARD_BYTES)))
    except OSError:
        return None


def _inode(path: Path) -> int | None:
    try:
        return path.stat().st_ino
    except OSError:
        return None


def _whole_lines_end(path: Path) -> int:
    """The offset just past the file's last whole line (0 when there is none)."""
    try:
        with path.open("rb") as handle:
            size = handle.seek(0, os.SEEK_END)
            at = size
            while at > 0:
                step = min(at, 64 * 1024)
                handle.seek(at - step)
                nl = handle.read(step).rfind(b"\n")
                if nl >= 0:
                    return at - step + nl + 1
                at -= step
    except OSError:
        pass
    return 0
from probe.daemon.worker.error_log import _device_error  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.files import inbox_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.held import _notice_event  # noqa: E402 -- pieces need each other; the front door loads this one first
