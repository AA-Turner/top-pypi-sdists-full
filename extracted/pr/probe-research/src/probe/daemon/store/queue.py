"""the queue watermark: events no bite has covered, deferred or paused ranges, events left unrecorded."""

from __future__ import annotations

from probe.shared.harness.events import Kind
from probe.daemon.store.events import BEFORE_DAEMON_BITE, RUN_SIDE_KINDS, StoredEvent, UNRECORDED_BITE
from probe.daemon.store.logbook import BITE_DONE, BITE_PAUSED
#: How far an event's own stamp may sit before / after the daemon noticed it and
#: still date the work it files (`Store.work_began`): the server's window for
#: a write's event time (`app/sessions/effort.py`, 6 h before, 5 min after).
WORK_STAMP_WINDOW = (6 * 3600.0, 300.0)
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
#: The session's own history (`cover_before_daemon`): its chat logs and its scripts' run messages.
_HISTORY = "(stream = 'main' OR stream LIKE 'subagent:%' OR stream = 'sdk')"


class QueueMixin:
    """Part of Store: its methods run with `self` the Store; compose() folds them into Store."""

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

    def mark_covered(self, bite_id: int, last_seq: int, leads: tuple[int, ...] = ()) -> None:
        """Every uncovered event up to `last_seq`, and the run events past it the
        bite showed first (`bite.runs_ahead`)."""
        self.db.execute("UPDATE events SET bite = ? WHERE bite IS NULL AND seq <= ?", (bite_id, last_seq))
        if leads:
            self.db.executemany("UPDATE events SET bite = ? WHERE bite IS NULL AND seq = ?",
                                [(bite_id, int(seq)) for seq in leads])

    def pending_run_events(self, *, after_seq: int = 0, limit: int = 20) -> list[StoredEvent]:
        """Run starts and ends (`Kind.RUN_EVENT`) no bite has covered, after `after_seq`."""
        return [StoredEvent.from_row(r) for r in self.db.execute(
            "SELECT * FROM events WHERE bite IS NULL AND seq > ? AND kind = ? ORDER BY seq LIMIT ?",
            (int(after_seq), Kind.RUN_EVENT.value, int(limit)))]

    def leave_unrecorded(self, first_seq: int) -> int:
        """Mark every uncovered event from `first_seq` on as never to be recorded
        (`read only (daemon)`: the reader reads them, no bite ever covers them)."""
        current = self.db.execute("UPDATE events SET bite = ? WHERE bite IS NULL AND seq >= ?",
                              (UNRECORDED_BITE, first_seq))
        return current.rowcount

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

    def work_began(self, first_seq: int, last_seq: int) -> float | None:
        """When the work in the pending events `first_seq`..`last_seq` began, in
        epoch seconds: the oldest of their own stamps; None for no such event. A
        bite's `probe` writes are dated by it (`PROBE_EVENT_AT`, swarm friction
        R1): a record carries the session's focus forward from there, never back.

        When the daemon noticed an event stands in for its stamp when the stamp
        says nothing about the work: a folder check's file change (its stamp is
        the file's mtime, which a copy or an unpacked archive keeps), or a stamp
        outside `WORK_STAMP_WINDOW` of the noticing (a skewed or bogus clock)."""
        rows = self.db.execute(
            "SELECT kind, ts, noticed FROM events WHERE seq BETWEEN ? AND ? AND bite IS NULL",
            (first_seq, last_seq)).fetchall()
        times = []
        for row in rows:
            noticed = float(row["noticed"])
            at = None if row["kind"] == Kind.FILE_CHANGE.value else _epoch(row["ts"])
            before, after = WORK_STAMP_WINDOW
            times.append(at if at is not None and noticed - before <= at <= noticed + after else noticed)
        return min(times, default=None)

    def run_side_only(self, first_seq: int, last_seq: int) -> bool:
        """Whether every pending event `first_seq`..`last_seq` is the daemon's
        own observation of a run (`RUN_SIDE_KINDS`), with none of the agent's:
        a bite of only these files what a background job did while its agent
        sat idle, so its `probe` writes go as a run process's (swarm friction
        R41). False for no such event."""
        rows = self.db.execute(
            "SELECT kind FROM events WHERE seq BETWEEN ? AND ? AND bite IS NULL",
            (first_seq, last_seq)).fetchall()
        return bool(rows) and all(row["kind"] in RUN_SIDE_KINDS for row in rows)
