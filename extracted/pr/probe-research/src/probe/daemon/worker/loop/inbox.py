"""read the SDK inbox and the reader's claim log into events the writer sees."""

from __future__ import annotations
import json
import math
import os
import sqlite3
from probe.shared import mailbox
from probe.shared.harness.events import (
    READER_SOURCE,
    READER_STREAM,
    Event,
    Kind)


class InboxMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    def _read_inbox(self, until: int | None = None) -> int:
        """Messages capture received on the session's socket (SDK run starts, R3.1),
        at most READ_CHUNK_BYTES per poll. Their events take fresh offsets from the
        store's counter, so an inbox rewritten from empty never reuses an id."""
        path = inbox_path(self.session.session_id)
        _, offset = self.store.cursor("sdk")
        self.stream_behind["sdk"] = False
        try:
            size = path.stat().st_size
        except OSError:
            return 0
        if size < offset:  # rotated or rewritten: all of it is new
            offset = 0
        end = size if until is None else min(size, until)
        self.stream_behind["sdk"] = end - offset > READ_CHUNK_BYTES
        if end <= offset:
            return 0
        with path.open("rb") as handle:
            handle.seek(offset)
            buf = handle.read(min(end - offset, READ_CHUNK_BYTES))
        messages: list[dict] = []
        pos = 0
        while True:
            nl = buf.find(b"\n", pos)
            if nl < 0:
                break
            raw = buf[pos:nl]
            pos = nl + 1
            try:
                msg = json.loads(raw)
            except ValueError:
                continue
            if isinstance(msg, dict):
                messages.append(msg)
        if pos == 0 and len(buf) == READ_CHUNK_BYTES:
            pos = len(buf)
        added = 0
        with self.store.tx():
            for msg in messages:
                try:
                    added += self.store.add([Event(kind=Kind.RUN_EVENT, stream="sdk", offset=self.store.next_offset(),
                                                   text=_describe_sdk(msg), ts=_stamp(msg.get("received_at")))])
                except sqlite3.OperationalError:
                    raise
                except Exception as exc:  # noqa: BLE001
                    log.warning("skipped an SDK message: %s: %s", type(exc).__name__, exc)
            self.store.set_cursor("sdk", str(path), offset + pos)
        return added

    def _start_reader_log(self) -> None:
        """Where this store starts reading the reader's claim log, decided once and
        saved at once, so a later worker on the same store (resume, handover,
        restart) carries on from it. A fresh store reads it all; a store an earlier
        build kept for a session already under way starts after the last whole
        line: its reader messages so far were seen as harness lines."""
        if self.store.cursor(READER_STREAM)[0] is not None:
            return
        path = mailbox.claim_log_path(self.session.session_id)
        start = _whole_lines_end(path) if self.store.totals()["events"] else 0
        with self.store.tx():
            self.store.set_cursor(READER_STREAM, str(path), start)
            self.store.set_fact(READER_LOG_INODE, _inode(path))
            tail = _bytes_before_hash(path, start)
            if tail is not None:
                self.store.set_fact(READER_LOG_TAIL, {"at": start, "hash": tail})

    def _read_reader_log(self, until: int | None = None) -> int:
        """What the daemon's reader handed the main agent: each claim the mailbox
        logged (whichever deliverer took it: a hook, pi's extension, `probe ask
        --wait`), as one event holding the message as the agent read it. A claim
        counts only for a message this daemon recorded (`read_messages`) whose file
        a deliverer really moved into `claimed/`: a file or line anyone could write
        never becomes the reader's. Each event is keyed on its message, so reading
        the log again stores nothing twice. Read from the mailbox, never the
        transcript: the same on every harness, whole however the harness stored it."""
        sid = self.session.session_id
        path = mailbox.claim_log_path(sid)
        _, offset = self.store.cursor(READER_STREAM)
        try:
            handle = path.open("rb")
        except OSError:
            return 0
        with handle:
            stat = os.fstat(handle.fileno())
            known = self.store.fact(READER_LOG_INODE)
            before = b""
            if offset and stat.st_size >= offset:
                handle.seek(max(0, offset - GUARD_BYTES))
                before = handle.read(offset - max(0, offset - GUARD_BYTES))
            guard = self.store.fact(READER_LOG_TAIL)
            guarded = isinstance(guard, dict) and guard.get("at") == offset
            if (stat.st_size < offset or (known is not None and known != stat.st_ino)
                    or (offset and guarded and _tail_hash(before) != guard.get("hash"))):
                offset, before = 0, b""  # a new log (the folder was swept and made again): all of it is new
            elif offset and not guarded:
                # A store from before this guard (or a cursor moved without it):
                # take it now, as the bytes stand, so the next sweep is caught.
                self.store.set_fact(READER_LOG_TAIL, {"at": offset, "hash": _tail_hash(before)})
            end = stat.st_size if until is None else min(stat.st_size, until)
            if end <= offset:
                return 0
            handle.seek(offset)
            buf = handle.read(min(end - offset, READ_CHUNK_BYTES))
        pos = buf.rfind(b"\n") + 1
        lines: list[tuple[int, str | None, object]] = []  # (bytes, message id, claimed at)
        if pos == 0 and len(buf) == READ_CHUNK_BYTES:
            log.warning("skipped %s bytes of the reader's claim log with no line end", len(buf))
            lines.append((len(buf), None, None))
        else:
            for raw in buf[:pos].split(b"\n")[:-1]:
                try:
                    entry = json.loads(raw)
                except ValueError:
                    entry = None
                ok = isinstance(entry, dict) and isinstance(entry.get("id"), str)
                lines.append((len(raw) + 1, entry["id"] if ok else None, entry.get("at") if ok else None))
        moved = mailbox.claimed_ids(sid)
        rows = self.store.read_messages(sorted({i for _, i, _ in lines if i and i in moved}))
        # A claim is logged before the harness writes the lines that carry it (a new
        # prompt, the hook's own context): a claim that will show waits for them
        # (_held), and the claims after it with it, in order. A line that is no
        # claim of ours never holds anything; nothing waits at the shutdown drain.
        claims: list[tuple[str, object]] = []
        used, newest, looked = 0, None, False
        for size, message_id, at in lines:
            if message_id is not None and message_id in rows:
                if until is None:
                    if not looked:
                        newest, looked = self._newest_chat(), True
                    if _held(at, newest, self.clock()):
                        break
                claims.append((message_id, at))
            used += size
        if not used:
            return 0  # all of it waits: nothing to store, the cursor stays
        pos = used
        added = 0
        with self.store.tx():
            events = []
            for message_id, at in claims:
                row = rows.get(message_id)
                if row is None:
                    continue
                try:
                    events.append(Event(kind=Kind.META, stream=READER_STREAM, offset=int(row["rid"]),
                                        text=_reader_message(sid, row).rendered(), ts=_stamp(at),
                                        source=READER_SOURCE))
                except Exception as exc:  # noqa: BLE001 - one bad row never holds back the rest
                    log.warning("skipped a reader message: %s: %s", type(exc).__name__, exc)
            if events:
                added = self.store.add(self.exclusions.keep(events, stream=READER_STREAM))
            self.store.set_cursor(READER_STREAM, str(path), offset + pos)
            self.store.set_fact(READER_LOG_INODE, stat.st_ino)
            self.store.set_fact(READER_LOG_TAIL, {"at": offset + pos,
                                                  "hash": _tail_hash((before + buf[:pos])[-GUARD_BYTES:])})
        return added


#: The claim log's inode when the reader stream's cursor was last saved.
READER_LOG_INODE = "reader_log_inode"
#: ...and `{"at": cursor, "hash": ...}`, the hash of the bytes just before the
#: cursor (`GUARD_BYTES`): a log deleted and made again often gets the SAME
#: inode number back, so the bytes, not the inode alone, tell a new log from the
#: one read so far. A guard saved at another offset (a cursor an older build
#: moved) is no evidence either way and is taken again where the cursor is.
READER_LOG_TAIL = "reader_log_tail"
#: How long a claim waits for the chat line that carries it (`_held`).
CLAIM_HOLD_S = 10.0


def _held(at: object, newest: float | None, now: float) -> bool:
    """Does a claim made at `at` still wait for the chat? Until a chat line at
    least as new is stored (`newest`, the newest chat line's time), so it is
    placed after the prompt or tool result it came with, never a turn early;
    for CLAIM_HOLD_S at most, so a harness that writes nothing more never holds it."""
    if isinstance(at, bool) or not isinstance(at, (int, float)) or not math.isfinite(at):
        return False
    if not 0 <= now - at < CLAIM_HOLD_S:  # a stamp from the future never holds
        return False
    return newest is None or newest < at


def _reader_message(session_id: str, row) -> mailbox.Message:
    """A `read_messages` row as the mailbox message the agent was handed."""
    return mailbox.Message(id=row["id"], session=session_id, kind=row["kind"], text=row["text"] or "",
                           ask=row["ask"], question=row["question"], reason=row["reason"],
                           made_at=row["made_at"], origin_turn=row["origin_turn"])


def _stamp(at: object) -> str | None:
    """An epoch time (the supervisor's `received_at`) as an event's ISO stamp, so
    an SDK message is placed against inline stretches like any transcript line."""
    if isinstance(at, bool) or not isinstance(at, (int, float)):
        return None
    from datetime import datetime, timezone

    try:
        return datetime.fromtimestamp(at, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except (OverflowError, OSError, ValueError):
        return None


def _describe_sdk(msg: dict) -> str:
    """`<event>: <JSON>`, cut at 900 characters; `run_id` first, so a cut never
    takes it (`bite.run_id_of`: the writer's message reads that run first)."""
    kind = msg.get("event") or "run event"
    fields = {k: v for k, v in msg.items() if k in ("description", "tags", "config", "intent", "status",
                                                    "parent_run_id", "relation", "name", "command")}
    if "run_id" in msg:
        fields = {"run_id": msg["run_id"], **fields}
    return f"{kind}: {json.dumps(fields, default=str)[:900]}"
from probe.daemon.worker.files import inbox_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    GUARD_BYTES,
    READ_CHUNK_BYTES,
    _bytes_before_hash,
    _inode,
    _tail_hash,
    _whole_lines_end,
    log,
)
