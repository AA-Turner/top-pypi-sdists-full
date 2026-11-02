"""the main agent's requests to the writer and what the writer sends back."""

from __future__ import annotations
import sqlite3

from probe.shared.harness.events import REQUEST_SOURCE
from probe.daemon.store.events import UNRECORDED_BITE, scrub
from probe.daemon.store.logbook import BITE_DONE, BITE_SKIPPED


class RequestsMixin:
    """Part of Store: its methods run with `self` the Store; compose() folds them into Store."""

    # -- the main agent's requests to the writer, and what the writer sends back --
    def add_write_request(self, request_id: str, text: str, asked_at: float, wait: bool, event_seq: int | None,
                          *, state: str = "waiting", reason: str | None = None) -> bool:
        """Store a request the mailbox handed over. False: already stored."""
        current = self.db.execute(
            "INSERT OR IGNORE INTO write_requests (id, text, asked_at, wait, taken_at, state, ended_at, reason, "
            "event_seq) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (request_id, text, asked_at, int(wait), self.clock(), state,
             self.clock() if state != "waiting" else None, reason, event_seq))
        return current.rowcount > 0

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

    def ran_writes_after(self, row_id: int) -> list[sqlite3.Row]:
        """The writes that ran with a logbook id past `row_id`, oldest first."""
        return list(self.db.execute("SELECT * FROM writes WHERE id > ? AND status = 'ran' ORDER BY id", (row_id,)))

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
