"""how a run ends early: interrupted between rounds, paused to yield, cut short by limits, its range deferred."""

from __future__ import annotations
import sqlite3
import uuid
from probe.foundation.compat.compat import StrEnum
from probe.daemon.worker.bite import bite as bite_mod
from probe.daemon.host import lease
from probe.daemon.agent import tools
from probe.daemon.worker import alerts
from probe.daemon.agent.model import model as model_mod
from probe.daemon.store.logbook import (
    BITE_PAUSED,
    BITE_SKIPPED,
    CARRY_ON)
from probe.daemon.store.device import LANE_WRITE
BACKOFF_CAP_S = 30 * 60
#: A bite cut short by its limits is retried over half as many new events; this
#: many in a row from the same first event and those events are skipped (a notice
#: and a logbook line say so), never retried forever.
CUT_SHORTS_BEFORE_SKIP = 2


class CutShort(StrEnum):
    """What cut a bite short (`Worker._cut_short`)."""

    LIMITS = "limits"  # its per-bite caps (bites mode)
    LOOP = "loop"  # the loop detector
    NO_ANSWER = "no answer"  # the model thought until its token limit (`agent.answered_nothing`)
    TOO_LARGE = "too large"  # the model route refused the prompt as over its ceiling (`PROMPT_TOO_LARGE`)


#: Why a run stopped between two model rounds (`Worker._between_rounds`).
STOP_LOOP = "loop"
STOP_LEASE = "lease"
STOP_DEADLINE = "session end"
STOP_YIELD = "yield"
#: Why a run stopped when the CLI was reinstalled under it (`install_replaced`).
REINSTALLED = "the probe CLI was reinstalled under this worker"
STOP_REINSTALLED = "reinstalled"


class Interrupted(Exception):
    """A run stopped between two model rounds: `kind` (a STOP_*) and why.
    `messages`: a paused run's history, the tool results of its last round
    included (STOP_YIELD)."""

    def __init__(self, kind: str, why: str, messages: list | None = None) -> None:
        super().__init__(f"{kind}: {why}")
        self.kind = kind
        self.why = why
        self.messages = messages


class RunEndMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    # -- how a run ends early ------------------------------------------------
    def _interrupted(self, bite_id: int, built: bite_mod.Bite, stop: "Interrupted", usage=None, *,
                     deps: tools.Deps | None = None, conversation: int | None = None,
                     compactions: int = 0) -> bool:
        """A run stopped between two model rounds (`_between_rounds`). Its events
        are not covered, except a range the loop detector stopped twice and a
        conversation run paused to let new events in (`_paused`)."""
        in_tok, out_tok, cached = _tokens(usage)
        spent = {"input_tokens": in_tok, "output_tokens": out_tok, "cached_tokens": cached}
        if stop.kind != STOP_YIELD:  # a pause is logged by `_paused`: it is not a problem
            log.warning("bite %s stopped between model rounds (%s): %s", bite_id, stop.kind, stop.why)
        if stop.kind == STOP_REINSTALLED:
            # Not a failure: its events stay queued, and the next poll leaves for the new install.
            self.store.close_bite(bite_id, outcome="stopped: reinstalled", error=stop.why, **spent)
            return False
        if _key_refused(deps):
            self.store.close_bite(bite_id, outcome="key refused", **spent)
            return self._refused_key("a `probe` command", probe=True)
        if stop.kind == STOP_YIELD and conversation is not None and stop.messages:
            return self._paused(bite_id, built, stop, spent, conversation, compactions)
        if stop.kind == STOP_LOOP:
            if conversation is not None:
                self.store.end_conversation(conversation, f"the loop detector stopped a run: {stop.why}")
            return self._cut_short(bite_id, built, f"loop: {stop.why}", spent, cause=CutShort.LOOP)
        if stop.kind == STOP_DEADLINE:
            self.store.close_bite(bite_id, outcome="stopped: session end", error=stop.why, **spent)
            return False
        return self._lease_lost(bite_id, spent)

    def _paused(self, bite_id: int, built: bite_mod.Bite, stop: "Interrupted", spent: dict, conversation: int,
                compactions: int) -> bool:
        """A conversation run paused after ROUNDS_BEFORE_YIELD rounds: not a failure.
        Its history -- the tool results of its last round included, so a write that
        ran is never run again -- is saved, the events it was shown are covered, and
        the next bite (due at once, CARRY_ON) continues the same conversation with
        whatever arrived meanwhile."""
        log.info("bite %s: paused after %s model rounds; the next bite carries on", bite_id, ROUNDS_BEFORE_YIELD)
        with self.store.tx():
            self.store.save_conversation(conversation, _dump_messages(stop.messages), compactions=compactions)
            # The list it was sent is in the saved history now; its own writes are there
            # as tool calls until the run that finishes it completes.
            self._settle_writes_list(built, lean=model_mod.writer_history() == model_mod.WriterHistory.LEAN,
                                     paused=True)
            self.store.mark_covered(bite_id, built.last_seq, built.leads)
            self.store.close_bite(bite_id, outcome=BITE_PAUSED, error=stop.why, **spent)
            self.store.set_fact(CARRY_ON, True)
            if self.store.fact("cut_short"):
                self.store.set_fact("cut_short", None)
        self.failures = 0
        self.gateway_failures = 0
        self.next_attempt_at = 0.0
        self._renew()
        return True

    def _lease_lost(self, bite_id: int, spent: dict) -> bool:
        log.warning("bite %s ended without the lease; its events stay queued", bite_id)
        self.store.close_bite(bite_id, outcome="lease lost", **spent)
        self.failures += 1
        self.next_attempt_at = self.clock() + min(BACKOFF_CAP_S, 30 * (2 ** (self.failures - 1)))
        return False

    def _cut_short(self, bite_id: int, built: bite_mod.Bite, text: str, spent: dict, *,
                   cause: CutShort = CutShort.LIMITS, exc: BaseException | None = None) -> bool:
        """A bite its limits (CutShort.LIMITS, bites mode), the loop detector
        (CutShort.LOOP), a model that answered nothing before its token limit
        (CutShort.NO_ANSWER) or the route's prompt ceiling (CutShort.TOO_LARGE) cut short. Its events are NOT covered: the next bite takes half
        as many new events from the same first one (`bite.cover`'s `shrink`).
        CUT_SHORTS_BEFORE_SKIP in a row from the same first event: that range is
        covered as skipped -- a notice for the model, a logbook line in "Not
        recorded yet" and `probe companion log`, a device error line -- never a
        loop that spends a bite on it forever. A carry-on bite (`first_seq` 0, its
        events covered when its run paused) has nothing to shrink: what the run had
        left is dropped at once, said the same way. `exc` keeps the alert's dedupe
        key apart from the other causes'."""
        from probe.daemon import agent as agent_mod

        if not built.first_seq:
            why = {
                CutShort.LIMITS: "it hit its limits",
                CutShort.LOOP: "it went round in circles (the loop detector stopped it)",
                CutShort.NO_ANSWER: agent_mod.ANSWERED_NOTHING,
                CutShort.TOO_LARGE: "its prompt was over the model route's ceiling",
            }[cause]
            with self.store.tx():
                self.store.close_bite(bite_id, outcome=BITE_SKIPPED, error=text, **spent)
                self.store.set_fact("cut_short", None)
                self.store.set_fact(CARRY_ON, None)
                self.store.log_write(bite=bite_id, op_id=uuid.uuid4().hex, argv=["continued run"], head="skipped",
                                     status="not_run", reason=why)
                self.store.add([_notice_event(self.store, (
                    f"The continued run stopped before it finished and what it had left was not recorded: {why}."))])
            self._fail_skipped_requests(bite_id)
            _device_error(f"session {self.session.session_id}: a continued run stopped unfinished: {why}")
            alerts.report(alerts.Kind.EVENTS_SKIPPED, session_id=self.session.session_id, lane=LANE_WRITE, exc=exc,
                          text=f"a continued run stopped unfinished: {why}")
            return True
        cut = self.store.fact("cut_short") or {}
        times = int(cut.get("times") or 0) + 1 if cut.get("first_seq") == built.first_seq else 1
        if times < CUT_SHORTS_BEFORE_SKIP:
            took = self.store.pending_count(built.first_seq, built.last_seq)
            with self.store.tx():
                self.store.close_bite(bite_id, outcome="cut short", error=text, **spent)
                self.store.set_fact("cut_short", {"first_seq": built.first_seq, "times": times,
                                                  "max_events": max(1, took // 2)})
            return False
        what = f"events #{built.first_seq}-#{built.last_seq}"
        why = {
            CutShort.LIMITS: (f"skipped as too costly: {times} bites in a row hit their limits (model requests, "
                              "tool calls or tokens) on them"),
            CutShort.LOOP: (f"skipped: {times} bites in a row went round in circles on them (the loop detector "
                            "stopped them)"),
            CutShort.NO_ANSWER: f"skipped: {times} bites in a row on them, {agent_mod.ANSWERED_NOTHING}",
            CutShort.TOO_LARGE: f"skipped: {times} bites in a row on them were over the model route's ceiling",
        }[cause]
        skipped = self.store.pending_count(built.first_seq, built.last_seq)
        with self.store.tx():
            # Not the run events it showed first: they were not the trouble, and lead the next bite.
            self.store.mark_covered(bite_id, built.last_seq)
            self.store.close_bite(bite_id, outcome=BITE_SKIPPED, error=text, **spent)
            self.store.set_fact("cut_short", None)
            self.store.log_write(bite=bite_id, op_id=uuid.uuid4().hex, argv=[what], head="skipped",
                                 status="not_run", reason=why)
            self.store.add([_notice_event(self.store, (
                f"{what} (turn {self.store.turn_of(built.first_seq)}) were not recorded: {why}."))])
        self._fail_skipped_requests(bite_id)
        _device_error(f"session {self.session.session_id}: {what} were {why}")
        how = {
            CutShort.LIMITS: f"{times} bites in a row hit their limits",
            CutShort.LOOP: f"the loop detector stopped {times} bites in a row",
            CutShort.NO_ANSWER: f"the model answered nothing {times} bites in a row (token limit)",
            CutShort.TOO_LARGE: f"{times} bites in a row were over the model route's ceiling",
        }[cause]
        alerts.report(alerts.Kind.EVENTS_SKIPPED, session_id=self.session.session_id, lane=LANE_WRITE, exc=exc,
                      text=f"{skipped} events skipped: {how}", count=skipped)
        return True

    def _defer(self, built: bite_mod.Bite) -> None:
        """Move a failing range to the back of the queue: later events go first."""
        if self.store.defer(built.first_seq, built.last_seq):
            self.failures = 0

    def requeue_deferred(self) -> None:
        """When nothing else is pending, deferred events come back."""
        self.store.requeue_deferred()

    async def _between_rounds(self, deps: tools.Deps, state) -> Interrupted | None:
        """Between two model rounds of a run: what a poll does, so no run starves
        the loop (A1). New lines go into the queue (the next bite shows them),
        answers are settled, and the run is stopped -- `Interrupted` -- for the
        loop detector, a lost lease or a moved switch, or the session-end
        deadline (SIGTERM, or capture gone: FINISH_CAP_S from then)."""
        if state.detector.tripped is not None:
            return Interrupted(STOP_LOOP, state.detector.tripped)
        if self.replay is None and install_replaced():
            # Its next read of its own files would be the new version's, or fail: the
            # run stops with its events queued, and the next poll leaves for the new install.
            return Interrupted(STOP_REINSTALLED, REINSTALLED)
        if not self.stopping and self._parent_gone():
            log.info("capture is gone: finishing what is queued")
            self.begin_stopping()
        try:
            self._take_input()
        except sqlite3.Error as exc:
            log.warning("reading between model rounds failed: %s: %s", type(exc).__name__, exc)
        if self.finish_by is not None and self.clock() >= self.finish_by:
            return Interrupted(STOP_DEADLINE, "the session ended and its finish budget is spent")
        if self._went_inline():
            # Before the answers: nothing is settled once the agent records.
            return Interrupted(STOP_LEASE, INLINE_STOP)
        await self.settle_answers()
        if _key_refused(deps) or deps.stopped:
            return Interrupted(STOP_LEASE, deps.stopped or "Probe refused the daemon's key")
        if not self._lease_ours():
            return Interrupted(STOP_LEASE, lease.may_write(self.session.session_id) or "the lease is gone")
        return None
from probe.daemon.worker.bite.run import ROUNDS_BEFORE_YIELD  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.env import _tokens  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.error_log import _device_error  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.install import install_replaced  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.failures import _key_refused  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.held import _notice_event  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.modes.conversation import _dump_messages  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.stretches import INLINE_STOP  # noqa: E402 -- pieces need each other; the front door loads this one first
