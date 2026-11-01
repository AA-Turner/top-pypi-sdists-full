"""decide when a bite is due and what triggered it (turn end, age, prompt, request, run event)."""

from __future__ import annotations
from probe.daemon.worker.bite import bite as bite_mod
from probe.shared.harness.events import Kind
from probe.daemon.store.logbook import CARRY_ON
DUE_AFTER_S = 120.0
#: The run triggers the writer's least gap may hold back (`Worker.deferrable`); a
#: researcher's prompt behind other queued events only while
#: `model.writer_prompt_waits` is on.
TRIGGER_TURN_END = "turn end"
TRIGGER_AGE = "age"
TRIGGER_PROMPT = "prompt"
#: A request from the main agent waits (`probe ask --writer`): never held back.
TRIGGER_REQUEST = "request"
#: A request starts a run at once, but at most one per this long (or per the
#: writer's least gap, if longer): an agent asking again and again pays for one
#: run a minute, not one per ask. A request held back waits in the queue like
#: any event and goes with the next run, whatever starts it.
REQUEST_RUN_MIN_GAP_S = 60.0
#: A run start or end (the SDK's message, `Kind.RUN_EVENT`) starts a writer run
#: past the writer's least gap, but at most one run per this long (R34, swarm
#: friction T20): a finished run is filed within it, not up to the gap later
#: (median 3.5 min, p90 7.3 in the 10-28 swarm). Its events lead that run's
#: message (`bite.runs_ahead`).
TRIGGER_RUN = "run event"
RUN_EVENT_MIN_GAP_S = 60.0
QUEUE_LIMIT_CHARS = 200_000


class TriggersMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    # -- deciding when --------------------------------------------------------
    def due(self) -> str | None:
        if self.clock() < self.next_attempt_at:
            return None
        pending = self.store.pending(limit=bite_mod.MAX_EVENTS_PER_BITE + 1)
        if not pending:
            return "carry on" if self._carrying_on() else None
        from probe.daemon.agent.model import model as model_mod

        trigger = self._trigger(pending)
        gap = model_mod.writer_min_gap_s()
        if gap > 0 and self.deferrable(trigger, pending) and self.clock() - self.last_run_at < gap:
            return None  # E: the next run waits for the gap, and takes in more of the session
        return trigger

    def _trigger(self, pending: list) -> str | None:
        # First, wherever it sits in the queue: the agent waits on the answer.
        if self.store.has_pending_request() and self._request_may_start():
            return TRIGGER_REQUEST
        if self.clock() - self.last_run_at >= RUN_EVENT_MIN_GAP_S and self.store.pending_run_events(limit=1):
            return TRIGGER_RUN
        if any(ev.kind == Kind.PROMPT and ev.seq != pending[0].seq for ev in pending):
            return TRIGGER_PROMPT
        if any(ev.kind == Kind.TURN_END for ev in pending):
            return TRIGGER_TURN_END
        if self._over_size(pending):
            return "size"
        if self.clock() - pending[0].noticed >= DUE_AFTER_S:
            return TRIGGER_AGE
        if self.stopping:
            return "session end"
        return "carry on" if self._carrying_on() else None

    def _request_may_start(self) -> bool:
        from probe.daemon.agent.model import model as model_mod

        gap = max(REQUEST_RUN_MIN_GAP_S, model_mod.writer_min_gap_s())
        return self.clock() - self.last_request_run_at >= gap

    @staticmethod
    def _over_size(pending: list) -> bool:
        return sum(ev.chars for ev in pending) > QUEUE_LIMIT_CHARS or len(pending) > bite_mod.MAX_EVENTS_PER_BITE

    def deferrable(self, trigger: str | None, pending: list) -> bool:
        """Whether the writer's least gap (`model.writer_min_gap_s`, daemon cost
        round 4, E) may hold this run back: its only reasons are the agent's
        turn end or the queue's age, and a researcher's prompt while
        `model.writer_prompt_waits` (daemon cost round 7, F1, Richard T1=A:
        machine-sent prompts woke 65% of one team's runs under 5 minutes after
        the last, 83% of them to say nothing new; a record lands up to the gap
        later). A main agent's request, a run start or end (TRIGGER_RUN), a full
        queue, the session ending or a paused conversation run starts it at
        once, whichever label won."""
        from probe.daemon.agent.model import model as model_mod

        prompt_waits = trigger == TRIGGER_PROMPT and model_mod.writer_prompt_waits()
        waits = (TRIGGER_TURN_END, TRIGGER_AGE, TRIGGER_PROMPT) if prompt_waits else (TRIGGER_TURN_END, TRIGGER_AGE)
        return (trigger in waits and not self._over_size(pending)
                and not self.stopping and not self._carrying_on())

    def _carrying_on(self) -> bool:
        """A conversation run was paused (STOP_YIELD): the next bite is due now."""
        return self.mode == Mode.CONVERSATION and bool(self.store.fact(CARRY_ON))
from probe.daemon.worker.loop.mode import Mode  # noqa: E402 -- pieces need each other; the front door loads this one first
