"""the main agent's requests to the writer: take them, answer or fail each, relay results to the researcher."""

from __future__ import annotations
import time
from probe.shared import mailbox
from probe.shared.mailbox import requests as requests_mod
from probe.shared.harness.events import (
    REQUEST_SOURCE,
    REQUEST_STREAM,
    REQUEST_TOOL,
    Event,
    Kind)
from probe.daemon.store.events import UNRECORDED_BITE
#: Notes for the researcher (`Worker._relay_to_researcher`): the last logbook id
#: looked at (only ever moves forward), and the value last told per scope.
RELAY_SEEN = "relay_seen"
RELAY_TOLD = "relay_told"
#: With no RELAY_SEEN yet (a session's first look, or a daemon from before
#: notes), only writes this recent are told: an upgrade never replays old ones.
RELAY_FIRST_LOOK_S = 15 * 60


class RequestsMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    # -- the main agent's requests (`probe ask --writer`, requests.py) ---------
    def _take_requests(self) -> int:
        """Each request `probe ask --writer` filed: a `write_requests` row and one
        META event on the `request` stream, in one transaction, then its file is
        moved aside. A request already older than WRITE_REQUEST_TIMEOUT_S is
        stored as failed, with no event: it never runs."""
        sid = self.session.session_id
        added = 0
        try:
            pending = mailbox.pending_requests(sid)
        except OSError as exc:  # the mailbox is best effort: the next poll tries again
            log.warning("could not read the main agent's requests: %s", exc)
            pending = []
        for req in pending:
            text = mailbox.request_text(req.text)[:mailbox.REQUEST_MAX_CHARS]
            with self.store.tx():
                if self.store.has_write_request(req.id):
                    pass  # stored by an earlier pass that stopped before moving the file
                elif self.clock() - req.asked_at >= requests_mod.WRITE_REQUEST_TIMEOUT_S:
                    self.store.add_write_request(req.id, text, req.asked_at, req.wait, None, state="failed",
                                                 reason=requests_mod.REASON_TIMEOUT)
                    self._writer_failed(req.id, requests_mod.REASON_TIMEOUT)
                else:
                    ev = Event(kind=Kind.META, stream=REQUEST_STREAM, offset=self.store.next_offset(),
                               text=requests_mod.REQUEST_LINE.format(text=text), ts=_stamp(req.asked_at),
                               tool=REQUEST_TOOL, source=REQUEST_SOURCE)
                    self.store.add([ev])
                    seq = self.store.db.execute("SELECT seq FROM events WHERE event_id = ?",
                                                (ev.event_id,)).fetchone()["seq"]
                    self.store.add_write_request(req.id, text, req.asked_at, req.wait, int(seq))
                    added += 1
            try:
                mailbox.take_request(sid, req.id)
            except OSError as exc:  # stored: the next poll moves it (`has_write_request`)
                log.warning("could not move request %s aside: %s", req.id, exc)
        if added:
            log.info("%s request(s) from the main agent: a run starts now", added)
        self.publish_writer_messages()
        return added

    def _writer_failed(self, request_id: str, reason: str, *, bite: int | None = None) -> None:
        """Inside a transaction: the message that tells the agent a request will not run."""
        self.store.add_writer_message(message_id=mailbox.new_message_id(), kind=mailbox.Kind.FAILED,
                                      ask=request_id, reason=reason, bite=bite)

    def fail_requests(self, reason: str, *, rows: list | None = None, run: range | None = None,
                      bite: int | None = None) -> int:
        """Fail waiting requests (`rows`, default every waiting one): each gets its
        failure message, with what the runs that saw it already wrote ("partly
        done"), and its event is retired in the same transaction, so a request
        reported as failed never runs later. A conversation whose saved history
        holds one (a run of it covered the event: paused, or skipped) ends with
        it: carried on, it would act on a request the agent was told did not run
        (a paused run's other events go back on the queue, `_end_resumed`),
        whatever the mode now. "Partly done": the writes of the bites that
        worked on it (`Store.request_bites`), and of `run`, a run that ended
        unfinished with it (`bite`: the bite that ended it)."""
        rows = self.store.waiting_write_requests() if rows is None else rows
        if not rows:
            return 0
        failed = 0
        with self.store.tx():
            live = self.store.live_conversation()
            if live is not None and any(r["conversation"] == live["id"] and (r["event_bite"] or 0) >= 1
                                        for r in rows):
                self._end_resumed(int(live["id"]), f"a request it was shown failed: {reason}")
            for row in rows:
                bites = self.store.request_bites(row["id"]) | set(run or ())
                done = requests_mod.describe(self.store.writes_of_bites(bites)) if bites else None
                why = requests_mod.failure_reason(reason, done)
                if self.store.end_write_request(row["id"], "failed", reason=why):
                    self._writer_failed(row["id"], why, bite=bite)
                    failed += 1
        if failed:
            log.info("%s request(s) from the main agent failed: %s", failed, reason)
        self.publish_writer_messages()
        return failed

    def _fail_stuck_requests(self) -> None:
        """Fail each waiting request no run will answer:
        - not taken by a run within WRITE_REQUEST_TIMEOUT_S (the lease elsewhere,
          a blocked worker or a failing model leave it queued);
        - its event marked unrecorded (`/probe inline` covered its stamp);
        - shown to a run that will not finish: one that paused in a conversation
          that has ended, or any run in bites mode (a run there answers as it
          ends, so one still waiting was never going to be);
        - shown to the paused run being carried on, which has not finished in
          twice the timeout (each carry-on fails, or the lease is elsewhere):
          REASON_STALLED."""
        now = self.clock()
        live = self.store.live_conversation() if self._carrying_on() else None
        stuck: dict[str, list] = {}
        for row in self.store.waiting_write_requests():
            where, age = row["event_bite"], now - float(row["asked_at"])
            if where is None or where == -1:
                if age >= requests_mod.WRITE_REQUEST_TIMEOUT_S:
                    stuck.setdefault(requests_mod.REASON_TIMEOUT, []).append(row)
            elif where == UNRECORDED_BITE:
                stuck.setdefault(requests_mod.REASON_INLINE, []).append(row)
            elif live is None or row["conversation"] != live["id"]:
                stuck.setdefault(requests_mod.REASON_SKIPPED, []).append(row)
            elif age >= 2 * requests_mod.WRITE_REQUEST_TIMEOUT_S:
                stuck.setdefault(requests_mod.REASON_STALLED, []).append(row)
        for reason, rows in stuck.items():
            self.fail_requests(reason, rows=rows)

    def _answer_run(self, bite_id: int, conversation: int | None, reply: str) -> None:
        """Inside a transaction, as a run finishes (its events covered): ONE reply to
        each request this run saw -- its conversation's, or in bites mode its own
        bite's -- with its `reply` and the writes of this run and of every bite
        that worked on one (an earlier attempt's included; never an unrelated
        run's), or, when it saw none, a receipt for the structural writes the run
        recorded, if any (never a bite that worked on a request: that request
        tells its writes)."""
        asked = [r for r in self.store.waiting_write_requests()
                 if r["first_bite"] is not None and r["event_bite"] is not None and 1 <= r["event_bite"] <= bite_id
                 and (r["conversation"] == conversation if conversation is not None
                      else r["event_bite"] == bite_id)]
        run = set(range(self.store.run_start(bite_id), bite_id + 1))
        if asked:
            bites = run.union(*(self.store.request_bites(r["id"]) for r in asked))
            text = requests_mod.reply_text(reply, requests_mod.describe(self.store.writes_of_bites(bites)))
            for row in asked:
                self.store.end_write_request(row["id"], "answered", bite=bite_id)
                self.store.add_writer_message(message_id=mailbox.new_message_id(), kind=mailbox.Kind.ANSWER,
                                              ask=row["id"], text=text, bite=bite_id)
            return
        if not mailbox.enabled(source=self.session.source):
            return  # nobody delivers a receipt: the agent's hooks read no mailbox
        # A bite that worked on a request is told with that request (its reply or
        # its failure), so a receipt never tells the same write twice; a metric or
        # a pick is told by its own note (`_relay_to_researcher`).
        run -= self.store.bites_of_requests(min(run), bite_id)
        rows = [r for r in self.store.writes_of_bites(run)
                if (note := requests_mod.relay(r)) is None or note.text is None]
        receipt = requests_mod.receipt_text(requests_mod.describe(rows))
        if receipt:
            self.store.add_writer_message(message_id=mailbox.new_message_id(), kind=mailbox.Kind.MESSAGE,
                                          text=receipt, bite=bite_id)

    def _relay_to_researcher(self) -> None:
        """One note for the researcher (`requests.relay`) per headline metric or
        best pick the writer set: each logbook row looked at once, in order,
        whatever run or request it was in. A value a person holds (the write
        changed nothing) and a repeat of the value last told for the same scope
        tell nothing; nor does anything where the agent's hooks read no mailbox."""
        seen = self.store.fact(RELAY_SEEN)
        first_look = not isinstance(seen, int)
        rows = self.store.ran_writes_after(0 if first_look else seen)
        if not rows:
            return
        since = time.time() - RELAY_FIRST_LOOK_S
        told = self.store.fact(RELAY_TOLD)
        told = told if isinstance(told, dict) else {}
        deliver = mailbox.enabled(source=self.session.source)
        with self.store.tx():
            for row in rows:
                note = requests_mod.relay(row)
                if note is None or note.persons or (first_look and float(row["at"]) < since):
                    continue
                if note.text is None:  # a clear: the same value set again is news
                    told.pop(note.scope, None)
                    continue
                if told.get(note.scope) == note.value:
                    continue
                told[note.scope] = note.value
                if deliver:
                    self.store.add_writer_message(message_id=mailbox.new_message_id(), kind=mailbox.Kind.MESSAGE,
                                                  text=note.text, bite=row["bite"])
            self.store.set_fact(RELAY_TOLD, told)
            self.store.set_fact(RELAY_SEEN, int(rows[-1]["id"]))

    def publish_writer_messages(self) -> None:
        """Publish saved writer messages not yet in the mailbox (all of them after a
        crash), the researcher's notes made first. Best effort: one the mailbox
        refuses stays unpublished for the next poll, and never stops the worker."""
        self._relay_to_researcher()
        sid = self.session.session_id
        for row in self.store.unpublished_writer_messages():
            try:
                mailbox.publish(requests_mod.message(row, sid))
            except OSError as exc:
                log.warning("could not hand the main agent the writer's message %s: %s", row["id"], exc)
                return
            with self.store.tx():
                self.store.mark_writer_message_published(row["id"])

    def _fail_skipped_requests(self, bite_id: int) -> None:
        """A run cut short and skipped: the requests it saw fail, with what it did."""
        first = self.store.run_start(bite_id)
        rows = [r for r in self.store.waiting_write_requests()
                if r["first_bite"] is not None and r["event_bite"] is not None
                and first <= r["event_bite"] <= bite_id]
        if rows:
            self.fail_requests(requests_mod.REASON_SKIPPED, rows=rows, run=range(first, bite_id + 1), bite=bite_id)
from probe.daemon.worker.loop.inbox import _stamp  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
