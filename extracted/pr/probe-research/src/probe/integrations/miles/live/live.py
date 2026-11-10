"""LiveRollouts: this rollout process's running Miles tries as live samples (rl-next W36, W30 spike M1-M5): each try's
start, progress and end through producer `rollout`, and what a cancel, retry or watch does to it. One per process
(`LIVE`). Every call fails open: a Probe error is logged, never Miles'. Why: DESIGN.md beside this file."""

from __future__ import annotations

import asyncio
import itertools
import logging
import threading
from collections import OrderedDict
from collections.abc import Iterable, Mapping
from typing import Any

from probe.integrations.miles.samples.mapping import (
    ERROR_REASONS,
    HOST,
    SCHEDULED_STEP_KEY,
    build_group_key,
    build_task,
    get_status,
    read_reward,
)
from probe.integrations.miles.samples.producers import PROCESS, ROLLOUT

from .engines import EngineAborter, RidStamp
from .rollout import Rollout
from .schedule import RolloutSchedule, wrap_train_input
from .sessions import SessionWatcher, wrap_endpoint_tracer

log = logging.getLogger(__name__)

PASSED, FAILED, ERROR, DROPPED, ABORTED, CANCELED = "passed", "failed", "error", "dropped", "aborted", "canceled"
#: The spike's refusal for Miles agent rollouts (`SPIKE-W30.md`, M5): their model calls leave from the session server.
AGENT_REFUSAL = "cancel and retry need an engine abort Miles' session server does not expose; watch works"
GENERATE_WATCH_REFUSAL = ("a Miles generate rollout sends no turns while it runs; its phase and activity are on its "
                          "live row, and its whole conversation lands with the finished sample")
NOT_STAMPED_REFUSAL = ("this sample's generate function sends its model requests without Miles' `post`, so Probe "
                       "cannot name them to abort them")
ENDED_REFUSAL = "the sample already ended"
NO_REQUEST_REFUSAL = "it has sent no model request Probe can stop yet; ask again in a moment"
FINISHED_FIRST = "it finished before the abort reached the engine: nothing was stopped"
#: How long a cancel or retry waits for the abort to land before it answers.
STOP_WAIT_S = 10.0
#: Tries remembered per sample index, and groups remembered, at once (the oldest forgotten first).
TRIES_REMEMBERED = 100_000
GROUPS_REMEMBERED = 10_000
#: Sibling keys a cancel's answer names (its result is capped at 4 KiB).
MAX_NAMED_SIBLINGS = 32
#: Why a canceled try's siblings end dropped: Miles' filter reason (`common_filters.py:86`), their end's `error_reason`.
DROPPED_BECAUSE = "group_has_aborted"


class LiveRollouts:
    """The running tries, by attempt key; groups (by `Sample.group_index`) for the cancel rule; the writer."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._running: dict[str, Rollout] = {}
        self._tries: OrderedDict[Any, int] = OrderedDict()
        self._eval_calls = itertools.count(1)
        #: group -> {attempt key: its outcome (None while it runs)}.
        self._groups: OrderedDict[Any, dict[str, str | None]] = OrderedDict()
        #: group -> the attempt a cancel asked to stop (decided at its end); group -> the one whose abort dropped it.
        self._cancels: dict[Any, str] = {}
        self._dropped: OrderedDict[Any, str] = OrderedDict()
        #: Siblings that finished while a cancel in their group was undecided: sent once it is.
        self._held: dict[Any, list[tuple[Rollout, str, str | None, str | None]]] = {}
        #: group -> the step its first try began under: every try of the group (a retry too) names that one.
        self._group_steps: OrderedDict[Any, int] = OrderedDict()
        self._writer: Any = None
        self._is_opening = False
        self._is_off = False
        self._kinds: set[str] = set()
        self._declared: frozenset[str] = frozenset()
        self.aborter = EngineAborter()
        self.schedule = RolloutSchedule()
        self.stamp = RidStamp(self.aborter, on_request=self._record_request, on_reply=self._record_reply)
        self.sessions = SessionWatcher(lambda: self._writer)

    def reset(self) -> None:
        """Forget every try, the writer and the wraps' state (tests; a process whose run closed)."""
        from .generate import forget_wrapped

        forget_wrapped()
        self.__init__()

    # -- the writer (producer `rollout`) ----------------------------------------------------------------------------
    def get_writer(self, args: Any) -> Any:
        """The rollout producer's `run.samples`, or None: Probe is off here, or its run is still opening (on a thread
        of its own: the rollout's event loop never waits on Probe)."""
        if self._writer is not None or self._is_off:
            return self._writer
        found = PROCESS.find_samples(ROLLOUT)
        if found is not None:
            self._set_writer(found)
            return found
        with self._lock:
            if self._is_opening:
                return None
            self._is_opening = True
        threading.Thread(target=self._open_writer, args=(args,), name="probe-miles-live-open", daemon=True).start()
        return None

    def _open_writer(self, args: Any) -> None:
        try:
            writer = PROCESS.get_samples(ROLLOUT, args)
        except Exception as exc:  # noqa: BLE001 -- fail open: the rollouts run unrecorded
            log.debug("probe: the Miles rollout producer did not open: %s", exc)
            writer = None
        if writer is None:
            self._is_off = True
        else:
            self._set_writer(writer)

    def _set_writer(self, writer: Any) -> None:
        with self._lock:
            self._writer = writer
        self._send_plan()

    def record_generate(self, *, is_agent: bool, can_abort: bool) -> None:
        """A generate function this process runs: what its samples can be asked (D47: only proven paths)."""
        with self._lock:
            self._kinds.add("agent" if is_agent else "generate" if can_abort else "not_stamped")
        self._send_plan()

    def _send_plan(self) -> None:
        """The producer's plan row: cancel and retry for stamped generate rollouts, watch for agent rollouts; the
        spike's reason for each of the rest (`run.samples.refuse`), so an ask is refused at once in Miles' words."""
        with self._lock:
            writer, kinds = self._writer, frozenset(self._kinds)
            if writer is None or not kinds or kinds == self._declared:
                return
            self._declared = kinds
        if "generate" in kinds:
            writer.on_cancel(self.handle_cancel)
            writer.on_retry(self.handle_retry)
        if "agent" in kinds:
            writer.on_watch(self.handle_watch)
        for kind, why in get_refusals(kinds).items():
            writer.refuse(kind, why)

    # -- a try's life (on the rollout's event loop) -------------------------------------------------------------------
    def start(self, sample: Any, *, is_eval: bool, is_agent: bool, can_abort: bool, can_retry: bool,
              args: Any) -> Rollout | None:  # fmt: skip
        """Name the try and send its start, before its first model request. None when Probe is not recording here.
        An eval pass reuses `Sample.index`, so an eval try's key starts with this process's eval-call number."""
        writer = self.get_writer(args)
        if writer is None:
            return None
        index = getattr(sample, "index", None)
        prefix = f"eval:{next(self._eval_calls)}:{index}:" if is_eval else f"{index}:"
        with self._lock:
            try_number = 1 if is_eval else self._take_try(index)
        rollout = self._make(sample, args, prefix, try_number, is_agent=is_agent, can_abort=can_abort,
                             can_retry=can_retry)  # fmt: skip
        self._send_start(writer, rollout, sample)
        return rollout

    def _take_try(self, index: Any) -> int:
        try_number = self._tries.pop(index, 0) + 1
        self._tries[index] = try_number
        while len(self._tries) > TRIES_REMEMBERED:
            self._tries.popitem(last=False)
        return try_number

    def _make(self, sample: Any, args: Any, prefix: str, try_number: int, *, is_agent: bool, can_abort: bool,
              can_retry: bool, retry_of: str | None = None) -> Rollout:  # fmt: skip
        ip, port = getattr(args, "sglang_router_ip", None), getattr(args, "sglang_router_port", None)
        rollout = Rollout(
            key=f"{prefix}{try_number}", prefix=prefix, index=getattr(sample, "index", None), try_number=try_number,
            group=None if prefix.startswith("eval:") else getattr(sample, "group_index", None), is_agent=is_agent,
            can_abort=can_abort, can_retry=can_retry and callable(getattr(sample, "reset_for_retry", None)),
            router=f"http://{ip}:{port}" if ip and port else None, loop=asyncio.get_running_loop(), retry_of=retry_of,
        )  # fmt: skip
        step = None if rollout.is_eval else self.schedule.get_current(getattr(sample, "trainer_model_id", None))[0]
        with self._lock:
            self._running[rollout.key] = rollout
            if rollout.group is not None:
                self._groups.setdefault(rollout.group, {})[rollout.key] = None
                self._groups.move_to_end(rollout.group)
                while len(self._groups) > GROUPS_REMEMBERED:
                    self._groups.popitem(last=False)
                if step is not None and rollout.group not in self._group_steps:
                    self._group_steps[rollout.group] = step
                    while len(self._group_steps) > GROUPS_REMEMBERED:
                        self._group_steps.popitem(last=False)
                step = self._group_steps.get(rollout.group, step)
            rollout.scheduled_step = step
        return rollout

    def _send_start(self, writer: Any, rollout: Rollout, sample: Any) -> None:
        """The start: task, host, try; a train try also its group, step and the weights its engines serve; the
        engine its requests go to (Miles' router, `single_turn.py:21`)."""
        metadata = getattr(sample, "metadata", None)
        task = build_task(sample, metadata if isinstance(metadata, Mapping) else {})
        fields: dict[str, Any] = {"host": HOST, "try_number": rollout.try_number,
                                  "extras": {"miles": _drop_none({"sample_index": rollout.index,
                                                                  "group_index": rollout.group})}}  # fmt: skip
        if task.get("scenario"):
            fields["scenario"] = task["scenario"]
        if rollout.retry_of:
            fields["retry_of"] = rollout.retry_of
        if rollout.router:
            fields["engine"] = rollout.router
        if not rollout.is_eval:
            version = self.schedule.get_current(getattr(sample, "trainer_model_id", None))[1]
            fields.update(_drop_none({"scheduled_step": rollout.scheduled_step, "weight_version": version}))
            if rollout.scheduled_step is not None and rollout.group is not None:
                fields["group_key"] = build_group_key(rollout.scheduled_step, rollout.group)
        writer.attempt_start(rollout.key, task_key=task["task_key"], **fields)

    def finish_try(self, rollout: Rollout, outputs: list, sample: Any, args: Any) -> Rollout | None:
        """The try's generate function returned. Its samples name the attempt; a retry that aborted it starts the
        next try in the same slot (returned); an aborted or failed try ends now; a finished one waits for its grade."""
        for output in outputs:
            if isinstance(getattr(output, "metadata", None), dict):
                output.metadata["probe_attempt_key"] = rollout.key
                if rollout.scheduled_step is not None:  # the finished sample's group and step (`samples.py`)
                    output.metadata[SCHEDULED_STEP_KEY] = rollout.scheduled_step
        rollout.outputs = list(outputs)
        statuses = [get_status(output) for output in outputs]
        if rollout.stop == "retry" and outputs and all(status == ABORTED for status in statuses) and rollout.can_retry:
            return self._retry(rollout, sample, args)
        if any(status == ABORTED for status in statuses):
            self._end(rollout, ABORTED)
        elif any(status == "failed" for status in statuses):
            self._end(rollout, *_read_failure(outputs))
        else:
            rollout.is_scoring = True
            writer = self._writer
            if writer is not None:
                writer.attempt_progress(rollout.key, phase="scoring", turns=rollout.calls, tokens=rollout.tokens,
                                        activity="scoring")  # fmt: skip
        return None

    def _retry(self, rollout: Rollout, sample: Any, args: Any) -> Rollout | None:
        """Miles' own reset (`types.py:457-482`: the prompt kept, outputs cleared) and the next try, `retry_of` the
        aborted one (which then reads superseded)."""
        writer = self._writer
        if writer is None:
            return None
        sample.reset_for_retry()
        with self._lock:
            try_number = rollout.try_number + 1 if rollout.is_eval else self._take_try(rollout.index)
        new = self._make(sample, args, rollout.prefix, try_number, is_agent=rollout.is_agent,
                         can_abort=rollout.can_abort, can_retry=rollout.can_retry, retry_of=rollout.key)  # fmt: skip
        if isinstance(getattr(sample, "metadata", None), dict):
            sample.metadata["probe_retry_of"] = rollout.key
        self._send_start(writer, new, sample)
        rollout.retried_as = new.key
        self._end(rollout, ABORTED, extras={"retried_as": new.key})
        with self._lock:
            self._groups.get(rollout.group, {}).pop(rollout.key, None)  # replaced: no longer a member of its group
        return new

    def end_raised(self, rollout: Rollout, error: BaseException) -> None:
        """The generate function raised (a task cancel is Miles' own: aborted)."""
        if rollout.is_ended:
            return
        if isinstance(error, asyncio.CancelledError):
            self._end(rollout, ABORTED)
        else:
            self._end(rollout, ERROR, "unknown", f"{type(error).__name__}: {error}"[:1024])

    def end_unscored(self, rollouts: Iterable[Rollout], error: BaseException) -> None:
        """Grading raised after the generate function returned (`generate_and_rm`)."""
        for rollout in rollouts:
            if rollout.is_ended:
                continue
            if isinstance(error, asyncio.CancelledError):
                self._end(rollout, ABORTED)
            else:
                self._end(rollout, ERROR, "reward_fn" if rollout.is_scoring else "unknown",
                          f"{type(error).__name__}: {error}"[:1024])  # fmt: skip

    def end_scored(self, rollouts: Iterable[Rollout], args: Any, *, is_last_chance: bool = False) -> None:
        """Graded tries end passed or failed. With `--group-rm` the grade comes with the whole group: those wait for
        `generate_and_rm_group`, or (``is_last_chance``) the log hook."""
        is_group_graded = bool(getattr(args, "group_rm", False))
        for rollout in rollouts:
            if rollout.is_ended or not rollout.is_scoring:
                continue
            rewards = [read_reward(output, getattr(args, "reward_key", None))[0] for output in rollout.outputs]
            if is_group_graded and not is_last_chance and any(reward is None for reward in rewards):
                continue
            graded = [reward for reward in rewards if reward is not None]
            if not graded:
                self._end(rollout, ERROR, "reward_fn", "Miles graded none of this try's samples")
                continue
            reward_max = getattr(args, "probe_reward_max", None)
            reward_max = float(reward_max) if isinstance(reward_max, (int, float)) and not isinstance(reward_max, bool) else 1.0
            self._end(rollout, PASSED if min(graded) >= reward_max else FAILED)

    def end_named(self, samples: Iterable[Any], args: Any, *, is_last_chance: bool = False) -> None:
        """The tries these finished samples name (`metadata["probe_attempt_key"]`) that still wait for their grade."""
        with self._lock:
            found = {self._running.get(key) for key in map(_get_attempt_key, samples) if key}
        self.end_scored([rollout for rollout in found if rollout is not None], args, is_last_chance=is_last_chance)

    def _end(self, rollout: Rollout, outcome: str, reason: str | None = None, message: str | None = None,
             extras: dict | None = None) -> None:  # fmt: skip
        """Send the try's end, once. A sibling that finished while a cancel in its group is undecided waits; one in a
        group Miles drops (an aborted member, `common_filters.py:83-87`) ends dropped, its reason Miles' own."""
        group = rollout.group
        with self._lock:
            if rollout.is_ended or rollout.outcome is not None:
                return
            if group is not None and outcome in (PASSED, FAILED):
                dropped_by = self._dropped.get(group)
                pending = self._cancels.get(group)
                if dropped_by is not None and dropped_by != rollout.key:
                    outcome, reason = DROPPED, DROPPED_BECAUSE
                    extras = {**(extras or {}), "dropped_because": DROPPED_BECAUSE, "canceled": dropped_by}
                elif pending is not None and pending != rollout.key:
                    self._held.setdefault(group, []).append((rollout, outcome, reason, message))
                    return
            rollout.outcome = outcome
            self._running.pop(rollout.key, None)
            if group is not None and rollout.key in self._groups.get(group, {}):
                self._groups[group][rollout.key] = outcome
            is_deciding = group is not None and self._cancels.get(group) == rollout.key
        writer = self._writer
        if writer is not None:
            fields: dict[str, Any] = {"extras": {"miles": extras}} if extras else {}
            writer.attempt_end(rollout.key, outcome, error_reason=reason, error_message=message, **fields)
        rollout.done.set()
        if is_deciding:
            self._decide_group(group, rollout.key, is_dropped=outcome == ABORTED)

    def _decide_group(self, group: Any, key: str, *, is_dropped: bool) -> None:
        """The canceled try ended: aborted, Miles drops its group (its held siblings end dropped); else nothing was
        stopped and they end as they finished."""
        with self._lock:
            self._cancels.pop(group, None)
            held = self._held.pop(group, [])
            if is_dropped:
                self._dropped[group] = key
                while len(self._dropped) > GROUPS_REMEMBERED:
                    self._dropped.popitem(last=False)
        for sibling, outcome, reason, message in held:
            self._end(sibling, outcome, reason, message)

    # -- progress (the stamped `post`, the session wrap) -------------------------------------------------------------
    def _record_request(self, rollout: Rollout) -> None:
        rollout.calls += 1
        writer = self._writer
        if writer is not None:
            writer.attempt_progress(rollout.key, phase="generating", turns=rollout.calls - 1, tokens=rollout.tokens,
                                    activity=f"model call {rollout.calls}")  # fmt: skip

    def _record_reply(self, rollout: Rollout, output: Any) -> None:
        meta = output.get("meta_info") if isinstance(output, Mapping) else None
        meta = meta if isinstance(meta, Mapping) else {}
        tokens = meta.get("completion_tokens")
        if isinstance(tokens, int) and not isinstance(tokens, bool):
            rollout.tokens += tokens
        finish = meta.get("finish_reason")
        finish = finish.get("type") if isinstance(finish, Mapping) else finish
        writer = self._writer
        if writer is not None:
            writer.attempt_progress(rollout.key, phase="generating", turns=rollout.calls, tokens=rollout.tokens,
                                    activity=f"model replied ({finish or 'done'}, {tokens or 0} tokens)")  # fmt: skip

    def record_session(self, rollout: Rollout, tracer: Any) -> None:
        """An agent rollout's Miles session opened: a watch reads its turns there."""
        rollout.session_url = str(getattr(tracer, "router_url", "") or "") or None
        rollout.session_id = str(getattr(tracer, "session_id", "") or "") or None
        writer = self._writer
        if writer is not None and rollout.session_id:
            writer.attempt_progress(rollout.key, phase="generating", activity=f"agent session {rollout.session_id}")

    # -- commands (on Probe's command thread) -------------------------------------------------------------------------
    def handle_cancel(self, key: str, command: Any) -> dict:
        """Abort the try's requests on every engine (never a task cancel: that takes the whole group, D47). Miles then
        drops its whole group (M2): its siblings end dropped, and the answer says so."""
        from probe.sdk.run.samples.live import CommandRefused

        rollout = self._find_running(key)
        self._check_stoppable(rollout)
        siblings = self._ask_group_drop(rollout)
        rollout.ask_stop("cancel")
        rollout.done.wait(STOP_WAIT_S)
        if rollout.is_ended and rollout.outcome != ABORTED:
            raise CommandRefused(FINISHED_FIRST)  # its end decided the group: it trains
        named = siblings[:MAX_NAMED_SIBLINGS]
        if rollout.group is None:
            note = "canceled" if rollout.is_ended else "asked to stop: it stops at its next model call"
        elif rollout.is_ended:
            note = (f"canceled; Miles drops this sample's whole group from training, so its {len(siblings)} other "
                    f"samples will not train either")  # fmt: skip
        else:
            note = (f"asked to stop: it stops at its next model call, and Miles then drops its whole group from "
                    f"training ({len(siblings)} other samples)")  # fmt: skip
        return {"note": note, "group_dropped": named} if rollout.group is not None else {"note": note}

    def handle_retry(self, key: str, command: Any) -> dict:
        """Abort the try and run Miles' generate again for the same Sample in its group slot (M3): the group trains
        with the new try. Running tries only."""
        from probe.sdk.run.samples.live import CommandRefused

        rollout = self._find_running(key)
        self._check_stoppable(rollout)
        if not rollout.can_retry:
            raise CommandRefused("this Miles build has no `Sample.reset_for_retry`, so a sample cannot run again")
        rollout.ask_stop("retry")
        if rollout.done.wait(STOP_WAIT_S):
            if rollout.retried_as:
                return {"attempt_key": rollout.retried_as}
            raise CommandRefused(FINISHED_FIRST)
        return {"attempt_key": rollout.next_key, "note": f"it stops at its next model call and runs again as "
                                                         f"{rollout.next_key}"}  # fmt: skip

    def handle_watch(self, key: str, command: Any) -> None:
        """An agent rollout's turns from Miles' session server, while watched (M4)."""
        from probe.sdk.run.samples.live import CommandRefused

        rollout = self._find_running(key)
        if not rollout.is_agent:
            raise CommandRefused(GENERATE_WATCH_REFUSAL)
        self.sessions.watch(rollout)

    def _find_running(self, key: str) -> Rollout:
        from probe.sdk.run.samples.live import CommandRefused

        with self._lock:
            rollout = self._running.get(key)
        if rollout is None or rollout.is_ended or rollout.outcome is not None:
            raise CommandRefused(ENDED_REFUSAL)
        return rollout

    @staticmethod
    def _check_stoppable(rollout: Rollout) -> None:
        from probe.sdk.run.samples.live import CommandRefused

        if rollout.is_agent:
            raise CommandRefused(AGENT_REFUSAL)
        if not rollout.can_abort or not rollout.router:
            raise CommandRefused(NOT_STAMPED_REFUSAL)
        if rollout.stop is not None:
            raise CommandRefused(f"a {rollout.stop} of it is already under way")
        if rollout.is_scoring:
            raise CommandRefused("it already finished generating and is being graded")
        if rollout.requests == 0:
            raise CommandRefused(NO_REQUEST_REFUSAL)

    def _ask_group_drop(self, rollout: Rollout) -> list[str]:
        """A train try's group: its cancel is pending until the try ends (`_end` decides it, under the same lock).
        Returns the siblings' keys. A try that ended in the meantime is refused: nothing would decide its group."""
        from probe.sdk.run.samples.live import CommandRefused

        if rollout.group is None:
            return []
        with self._lock:
            if rollout.outcome is not None:
                raise CommandRefused(ENDED_REFUSAL)
            self._cancels[rollout.group] = rollout.key
            return [key for key in self._groups.get(rollout.group, {}) if key != rollout.key]


def get_refusals(kinds: frozenset[str]) -> dict[str, str]:
    """Why the producer refuses each kind it does not declare: cancel and retry for agent rollouts or unstamped
    generate functions, watch for generate rollouts. Empty when it declares all three."""
    refusals: dict[str, str] = {}
    if "generate" not in kinds:
        reasons = [why for kind, why in (("agent", AGENT_REFUSAL), ("not_stamped", NOT_STAMPED_REFUSAL)) if kind in kinds]
        refusals.update(dict.fromkeys(("cancel", "retry"), "; ".join(reasons)))
    if "agent" not in kinds:
        refusals["watch"] = GENERATE_WATCH_REFUSAL
    return {kind: why for kind, why in refusals.items() if why}


def _read_failure(outputs: list) -> tuple[str, str, str]:
    """A FAILED try (`types.py:207-210`): the reason the generate function named, else unknown."""
    for output in outputs:
        metadata = getattr(output, "metadata", None)
        metadata = metadata if isinstance(metadata, Mapping) else {}
        if get_status(output) == "failed":
            named = metadata.get("error_reason")
            reason = named if isinstance(named, str) and named in ERROR_REASONS else "unknown"
            message = metadata.get("error") or metadata.get("exception") or "Miles sample status failed"
            return ERROR, reason, str(message)[:1024]
    return ERROR, "unknown", "Miles sample status failed"


def _get_attempt_key(sample: Any) -> str | None:
    metadata = getattr(sample, "metadata", None)
    key = metadata.get("probe_attempt_key") if isinstance(metadata, Mapping) else None
    return key if isinstance(key, str) and key else None


def _drop_none(values: Mapping[str, Any]) -> dict:
    return {name: value for name, value in values.items() if value is not None}


#: This process's one registry.
LIVE = LiveRollouts()


def install_rid_stamp(module: Any) -> None:
    """`miles.utils.http_utils` as it loads: its `post` stamps a running try's request id (`RidStamp`)."""
    from .generate import is_live_on

    if is_live_on():
        LIVE.stamp.install(module)


def wrap_session_tracer(module: Any) -> None:
    """`miles.rollout.generate_utils.openai_endpoint_utils` as it loads: an agent rollout's session is its try's."""
    from .generate import is_live_on

    if is_live_on():
        wrap_endpoint_tracer(module, LIVE.record_session, LIVE.sessions)


def wrap_rollout_inputs(module: Any) -> None:
    """`miles.rollout.base_types` as it loads: each train input names the step and weights a try starts under."""
    from .generate import is_live_on

    if is_live_on():
        wrap_train_input(module, lambda value: LIVE.schedule.record_input(value))
