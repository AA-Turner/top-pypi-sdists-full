"""`run.samples`: one producer's RL samples on a run (log, score, seal, commit, plan, weights, in-flight
attempts, compute phases), journaled to the outbox and sent as `/samples/batch`. Never raises."""

from __future__ import annotations

import os
import re
import threading
from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ...routes import WriteOp, path_for
from .attempts import AttemptBeats
from .barrier import wait_for_last_seals
from .bundles import TEXT_ARTIFACT_KIND, Bundle, Bundles, SealedBundle, get_artifact_kind
from .phases import SPANS_MAX, Phase, build_phase_spans
from .prepare import PartPreparer, PendingBlob, PreparedPart
from ....generated.samples import MAX_ACTIVITY_CHARS, AttemptKind, AttemptOutcome, AttemptProgress, PartRole
from ....generated.samples.capture import MAX_REFUSAL_CHARS
from .wire import (
    MAX_LOG_TAIL_BYTES,
    PLAN_FIELD,
    PLAN_FIELDS,
    BatchList,
    cut_tail,
    measure_bytes,
    to_wire_item,
    to_wire_plan,
)

if TYPE_CHECKING:
    from ....generated.records import CommandKind
    from ..run import Run
    from .live import CommandHandler, LiveSamples
    from .live.proxy import RolloutProxy

#: Items and bytes per journaled op; the drain merges ops up to the same caps (`coalesce.py`).
OP_MAX_ITEMS = 1_000
OP_MAX_BYTES = 4 * 1024 * 1024
#: Parts held for one step's bundles before the step's bundles close early (memory bound).
WAITING_MAX = 5_000
_SAFE_NAME = re.compile(r"[^A-Za-z0-9_.-]+")
#: A start's own facts (`AttemptStart`); the rest of a start's fields ride the part (host, engine, sandbox_id, ...).
START_FIELDS = ("started_at", "group_key", "scheduled_step", "weight_version", "try_number", "retry_of", "command_id")
#: How a canceled attempt's framework may say it ended; the claimed cancel makes each of these `canceled`.
_CANCEL_ENDINGS = frozenset({AttemptOutcome.ERROR, AttemptOutcome.ABORTED, AttemptOutcome.DROPPED,
                             AttemptOutcome.CANCELED})
#: `PROBE_LIVE_PROXY` values that turn the rollout proxy off: `live_url` then hands out the upstream URL.
_PROXY_OFF = frozenset({"0", "false", "off", "no"})


def _get_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RunSamples:
    """One producer's view of a run's samples. Every method fails open: a Probe error warns once
    per method, is counted on ``failures``, and never reaches the trainer."""

    def __init__(self, run: Run, producer: str, *, root: RunSamples | None = None) -> None:
        self._run = run
        self.producer = producer
        self.failures = 0
        self._warned: set[str] = set()
        self._lock = threading.RLock()
        folder = Path(_get_spool_folder(run)) / "sample-bundles" / str(run.id) / _SAFE_NAME.sub("_", producer)
        self._bundles = Bundles(folder, upload=self._upload_bundle)
        self._preparer = PartPreparer(self._bundles, scrub=_scrub_text, upload_text=self._upload_text)
        self._beats = AttemptBeats(send_held=self._send_held_beat)
        #: The view whose live side (held samples, handlers, the command listener) this one shares.
        self._root = root or self
        self._live: LiveSamples | None = None
        #: The rollout proxy this view's run shares (`live_url`), made on first use; broken: it could not start.
        self._proxy: RolloutProxy | None = None
        self._is_proxy_broken = False
        self._final_keys: dict[int, set[str]] = {}
        self._waiting: dict[int | None, list[dict]] = {}
        #: Bundles a step closed before its seal (too many parts held): the seal declares them too.
        self._early_bundles: dict[int | None, list[SealedBundle]] = {}
        #: What each step's seals declared so far: a re-seal repeats it plus what came since.
        self._sealed: dict[int, dict[str, Any]] = {}
        self._views: dict[str, RunSamples] = {}
        #: Why this producer refuses each kind it cannot do (`refuse`), sent whole each time (`PlanIn.refusals`).
        self._refusals: dict[str, str] = {}

    def as_producer(self, producer: str) -> RunSamples:
        """The same run's samples written as another producer (a trainer beside a rollout)."""
        if producer == self.producer:
            return self
        with self._lock:
            view = self._views.get(producer)
            if view is None:
                view = self._views[producer] = RunSamples(self._run, producer, root=self._root)
            return view

    # -- samples ---------------------------------------------------------------------------------
    def log(
        self, samples: Iterable[Any], *, role: str = PartRole.GENERATOR, step: int | None = None
    ) -> int:
        """Journal parts (dicts or `SamplePartIn`-shaped models), ``role`` unless a part names its
        own. ``step`` is the step they count toward in its seal (default: each part's consumed,
        else scheduled step). Returns how many were taken. Never raises."""
        return self._guard("log", self._log_parts, samples, role, step) or 0

    def score(
        self,
        key: str,
        *,
        scorer: Mapping[str, Any],
        reward: float | None = None,
        reward_parts: Mapping[str, float] | None = None,
    ) -> None:
        """Append a grade to an attempt (a regrade, a judge): one `scorer` part."""
        part = {"key": key, "role": PartRole.SCORER, "scored_by": [dict(scorer)]}
        if reward is not None:
            part["reward"] = reward
        if reward_parts:
            part["reward_parts"] = dict(reward_parts)
        self._guard("score", self._log_parts, [part], PartRole.SCORER, None)

    def attempt_start(self, key: str, *, task_key: str, step: int | None = None, **fields: Any) -> None:
        """A sample began: its `start` part, sent at once. ``fields``: its start facts (`started_at`, `group_key`,
        `scheduled_step`, `weight_version`, `try_number`, `retry_of`, `command_id`) and the part's own (`host`,
        `worker`, `engine`, `sandbox_id`, `scenario`, ...). A retry names `retry_of`; its try and the retry
        command are filled in. Its row reads running until its end."""
        self._guard("attempt_start", lambda: self._log_parts([self._make_start(key, task_key, step, fields)],
                                                             PartRole.ATTEMPT, None))

    def attempt_start_many(self, starts: Iterable[Mapping[str, Any]], *, step: int | None = None) -> int:
        """Several samples began at once (a generation batch): each mapping holds `key`, `task_key` and that sample's
        `attempt_start` fields; their `start` parts go in one write. Returns how many went. Never raises."""

        def send() -> int:
            parts = []
            for start in starts:
                fields = dict(start)
                try:
                    parts.append(self._make_start(str(fields.pop("key")), fields.pop("task_key"), step, fields))
                except Exception as exc:  # noqa: BLE001 -- one bad start never costs the rest
                    self._record_failure("attempt_start", exc)
            return self._log_parts(parts, PartRole.ATTEMPT, None)

        return self._guard("attempt_start", send) or 0

    def attempt_progress(
        self,
        key: str,
        *,
        phase: str | None = None,
        turns: int | None = None,
        tokens: int | None = None,
        activity: str | None = None,
        **fields: Any,
    ) -> None:
        """How the sample is going: its whole snapshot (`phase`, `turns`, `tokens`, `activity`, a line like
        `tool bash: pytest -x`) as a `progress` part. Its first progress and each new phase go at once; the rest at
        most one per sample per 30 s. A changed value is progress and moves `last_progress_at`; the same values
        again only say it is alive."""

        def send() -> None:
            changes = {"phase": phase, "turns": turns, "tokens": tokens, "activity": _cut_activity(activity)}
            # Checked before the snapshot takes it: a bad value kept there would fail every later beat.
            checked = AttemptProgress.model_validate({name: value for name, value in changes.items() if value is not None})
            is_news = self._beats.update_progress(key, checked.model_dump(mode="json", exclude_none=True), _get_now())
            self._send_beat(key, fields, is_news=is_news)

        self._guard("attempt_progress", send)

    def heartbeat(self, key: str, **fields: Any) -> None:
        """The sample is still running (last command, last error): a `progress` part with its whole snapshot, at
        most one per sample per 30 s; a held beat goes when the window opens. A new `last_command_at` is
        progress."""

        def send() -> None:
            if fields.get("last_command_at"):
                checked = AttemptProgress(last_progress_at=fields["last_command_at"])
                self._beats.update_progress(key, checked.model_dump(mode="json", exclude_none=True), _get_now())
            self._send_beat(key, fields)

        self._guard("heartbeat", send)

    def attempt_end(
        self,
        key: str,
        outcome: str,
        *,
        error_reason: str | None = None,
        error_message: str | None = None,
        log_text: str | None = None,
        ended_at: datetime | str | None = None,
        **fields: Any,
    ) -> None:
        """The sample ended (`passed`, `failed`, `error`, `dropped`, `aborted`, `canceled`): its `end` part, sent
        at once and never held for the step's bundles, so it stops reading running now. ``log_text`` rides as its
        last 4 KiB; the full log goes with the finished sample. After a claimed cancel, an error, abort or drop
        reads `canceled`."""
        ending = {"error_reason": error_reason, "error_message": error_message, "log_text": log_text,
                  "ended_at": ended_at, **fields}
        self._guard("attempt_end", lambda: self._send_ends([(key, outcome, ending)]))

    def attempt_end_many(self, ends: Iterable[Mapping[str, Any]]) -> int:
        """Several samples ended at once: each mapping holds `key`, `outcome` and that sample's `attempt_end` fields;
        their `end` parts go in one write. Returns how many went. Never raises."""

        def send() -> int:
            items = []
            for end in ends:
                fields = dict(end)
                items.append((str(fields.pop("key")), fields.pop("outcome"), fields))
            return self._send_ends(items)

        return self._guard("attempt_end", send) or 0

    # -- commands and watched turns (rl-next W34) -------------------------------------------------
    def on_cancel(self, handler: CommandHandler) -> None:
        """This producer can stop a running sample: ``handler(attempt_key, command)`` does it by the framework's
        safe path, on Probe's command thread. Return to answer `done`; raise `CommandRefused("why")` (or anything)
        to refuse. Its end then reads `canceled` (`attempt_end`)."""
        self._register("on_cancel", "cancel", handler)

    def on_retry(self, handler: CommandHandler) -> None:
        """This producer can run a sample again in its slot: ``handler(attempt_key, command)`` starts the new
        attempt (`attempt_start(new_key, retry_of=attempt_key, ...)`) and returns its key."""
        self._register("on_retry", "retry", handler)

    def on_watch(self, handler: CommandHandler | None = None) -> None:
        """This producer sends a watched sample's turns (`log_turns`). ``handler(attempt_key, command)``, if given,
        runs when a watch starts: send the conversation so far there."""
        self._register("on_watch", "watch", handler)

    def refuse(self, kind: str, why: str) -> None:
        """This producer cannot do ``kind`` (`cancel`, `retry`, `watch`): an ask for it is refused at once with
        ``why``, the framework's own words (rl-next W36: Harbor's "no safe way to stop one trial ..."), instead of
        the generic "not supported". A kind the producer registers (`on_cancel`, ...) still goes to it."""

        def send() -> None:
            from ....generated.records import CommandKind

            with self._lock:
                self._refusals[CommandKind(kind).value] = " ".join(str(why).split())[:MAX_REFUSAL_CHARS]
                refusals = dict(self._refusals)
            self._write_op({}, plan=to_wire_plan({"refusals": refusals}))

        self._guard("refuse", send)

    def is_watched(self, key: str) -> bool:
        """Does someone watch this sample now? Its turns are sent only then. Never raises."""
        live = self._root._live
        return bool(live is not None and self._guard("is_watched", live.turns.is_watched, key))

    def log_turns(self, key: str, turns: Iterable[Mapping[str, Any]]) -> int:
        """A watched sample's turns as they happen (each `role`, `content`, and `tool_name`, `tokens`, `at`,
        `weight_version` when known), scrubbed, cut to 64 KiB each and 1 MiB a call (oldest first). Nothing is
        sent while nobody watches it. Returns how many were taken."""

        def send() -> int:
            live = self._root._live
            items = live.turns.make_items(key, list(turns)) if live is not None else []
            self._send({BatchList.LIVE_TURNS: items})
            return len(items)

        return self._guard("log_turns", send) or 0

    def live_url(self, key: str, *, upstream: str, can_cancel: bool = False) -> str:
        """The model URL to give one sample's agent (rl-next W35): Probe's local rollout proxy forwards its calls to
        ``upstream`` (the API root it would call, `http://router:30000/v1`) byte for byte and records the sample's
        progress and, while watched, its turns. ``can_cancel``: `probe samples cancel` may stop it (its calls then
        answer `403 probe_canceled`); off by default. Call after `attempt_start`. Returns ``upstream`` itself when
        the proxy is off (`PROBE_LIVE_PROXY=0`), cannot start, or fails its health check. Never raises."""

        def open_route() -> str:
            if not str(upstream).startswith(("http://", "https://")):
                raise ValueError(f"upstream must be an http(s) URL, not {upstream!r}")
            proxy = self._get_proxy()
            if proxy is None:
                return upstream
            proxy.register_handlers(self, can_cancel=can_cancel)
            return proxy.open_route(self, key, upstream)

        return self._guard("live_url", open_route) or upstream

    # -- step control ----------------------------------------------------------------------------
    def seal(self, step: int, *, sent: int | None = None, dropped: Mapping[str, int] | None = None) -> None:
        """This producer is done with ``step``: the final samples it sent (counted here unless
        given), drops it only counted (by reason), and the step's bundles, closed and uploaded."""
        self._guard("seal", self._send_seal, step, sent, dropped)

    def commit(self, step: int, *, consumed_at: datetime | str | None = None) -> None:
        """The optimizer step ``step`` succeeded: its consumed samples read `trained`."""
        at = consumed_at.isoformat() if isinstance(consumed_at, datetime) else (consumed_at or _get_now())
        self._guard("commit", self._send, {BatchList.COMMITS: [{"step": step, "consumed_at": at}]})

    def plan(self, **fields: Any) -> None:
        """A change to what the run expects (`PlanIn`): `expected_steps`, `producers`, `reward_max`,
        `max_staleness`, and the owner's terminal manifest `final_step` + `is_closed` (`closed`
        works too). Only the fields given change."""
        if "closed" in fields:
            fields.setdefault("is_closed", fields.pop("closed"))
        unknown = sorted(set(fields) - set(PLAN_FIELDS))
        plan = {name: value for name, value in fields.items() if value is not None and name in PLAN_FIELDS}
        if "producers" in plan:
            plan["producers"] = list(plan["producers"])

        def send() -> None:
            if unknown:
                raise ValueError(f"plan() takes {', '.join(PLAN_FIELDS)}; not {', '.join(unknown)}")
            if plan:
                self._write_op({}, plan=to_wire_plan(plan))

        self._guard("plan", send)

    def log_groups(self, groups: Iterable[Mapping[str, Any]]) -> None:
        """Group facts (`GroupIn`): a group's expected size, its steps, and a whole-group drop
        (`drop_reason`, DAPO). Reward mean and variance are read from the members."""
        self._guard("log_groups", self._send, {BatchList.GROUPS: [dict(group) for group in groups]})

    def weights(
        self,
        version: int,
        *,
        after_step: int,
        checkpoint: str | Mapping[str, Any] | None = None,
        policy_id: str | None = None,
        pushed_at: datetime | str | None = None,
    ) -> None:
        """A weight version went live after ``after_step``; ``checkpoint`` is its saved artifact id,
        or `{uri, sha256}`, when one was saved."""
        row: dict[str, Any] = {"version": version, "after_step": after_step}
        if policy_id is not None:
            row["policy_id"] = policy_id
        if isinstance(checkpoint, str):
            row["checkpoint"] = {"kind": "checkpoint", "artifact_id": checkpoint}
        elif checkpoint is not None:
            row["checkpoint"] = {"kind": "checkpoint", **dict(checkpoint)}
        at = pushed_at.isoformat() if isinstance(pushed_at, datetime) else pushed_at
        row["pushed_at"] = at or _get_now()
        self._guard("weights", self._send, {BatchList.WEIGHTS: [row]})

    def record_phases(self, step: int, phases: Iterable[Phase | Mapping[str, Any]]) -> None:
        """What each rank did during ``step`` (rollout, train, weight sync, eval), as `phase` spans
        in ONE spans POST."""
        self._guard("record_phases", self._send_phases, step, list(phases))

    def wait_for_producers(self, *, timeout: float | None = None) -> bool:
        """The owner's close barrier: wait (default `PROBE_SAMPLES_CLOSE_WAIT`, 120 s) until capture
        shows every declared producer's last seal received. True when it did."""
        result = self._guard("wait_for_producers", self._wait_for_seals, timeout)
        return bool(result)

    def close(self) -> None:
        """Journal what this process still holds: parts waiting on bundles, and the bundles
        themselves; stop the command listener. `Run.finish` calls it before its drain."""
        self._guard("close", self._close_all)

    def _check_commands_seq(self, seq: Any) -> None:
        """The writer beat's command counter, for the listener's backstop. Never raises."""
        live = self._root._live
        if live is not None:
            self._guard("commands", live.check_commands_seq, seq)

    # -- inside ----------------------------------------------------------------------------------
    def _guard(self, what: str, call, *args):
        try:
            return call(*args)
        except Exception as exc:  # noqa: BLE001 -- fail open: a Probe error never stops training
            self._record_failure(what, exc)
            return None

    def _get_live(self) -> LiveSamples:
        """The live side this view shares with its run's other producers, made on first use."""
        root = self._root
        with root._lock:
            if root._live is None:
                from .live import LiveSamples

                root._live = LiveSamples(self._run, _scrub_text)
            return root._live

    def _register(self, what: str, kind: str, handler: CommandHandler | None) -> None:
        """A handler for ``kind``; the producer's plan row then says what it can be asked."""
        from ....generated.records import CommandKind

        def register() -> None:
            kinds = self._get_live().register(self.producer, CommandKind(kind), handler)
            self._write_op({}, plan=to_wire_plan({"capabilities": [str(known) for known in kinds]}))

        self._guard(what, register)

    def _wrap_handler(self, kind: CommandKind, make: Callable[[CommandHandler | None], CommandHandler]) -> None:
        """Register ``make(previous)``: a handler wrapping the one this producer registered before (the proxy's).
        A handle with no writer lease declares nothing, quietly: no command could reach it."""
        if getattr(self._run, "_lease", None) is None:
            return
        previous = self._get_live().get_handler(self.producer, kind)
        self._register(f"on_{kind.value}", kind.value, make(previous))

    def _get_proxy(self) -> RolloutProxy | None:
        """The run's rollout proxy, started on first use; None when it is off or could not start."""
        if os.environ.get("PROBE_LIVE_PROXY", "").strip().lower() in _PROXY_OFF:
            return None
        root = self._root
        with root._lock:
            if root._proxy is None and not root._is_proxy_broken:
                from .live.proxy import LOCALHOST, RolloutProxy

                proxy = RolloutProxy(host=os.environ.get("PROBE_LIVE_PROXY_HOST") or LOCALHOST)
                root._is_proxy_broken = True  # until it listens: a start that raises is not tried again
                proxy.start()
                root._proxy, root._is_proxy_broken = proxy, False
            return root._proxy

    def _make_start(self, key: str, task_key: str, step: int | None, fields: dict) -> dict:
        """One `start` part; the attempt is held from here (its commands, its beats' task)."""
        start = {name: fields.pop(name) for name in START_FIELDS if fields.get(name) is not None}
        start.setdefault("started_at", _get_now())
        start = self._get_live().record_start(key, self.producer, start)
        part = {"key": key, "role": PartRole.ATTEMPT, "attempt_kind": AttemptKind.START, "task_key": task_key,
                "heartbeat_at": _get_now(), "start": start, **fields}
        if step is not None:
            part["seal_step"] = step
        self._beats.record_start(key, {name: part[name] for name in ("task_key", "scenario")
                                       if part.get(name) is not None})
        return part

    def _send_ends(self, items: list[tuple[str, str, dict]]) -> int:
        """`end` parts in one write: each (key, outcome, its `attempt_end` fields). One bad end never costs the rest."""
        parts = []
        for key, outcome, fields in items:
            try:
                parts.append(self._make_end(key, outcome, dict(fields)))
            except Exception as exc:  # noqa: BLE001 -- one bad end never costs the rest
                self._record_failure("attempt_end", exc)
        taken = self._log_parts(parts, PartRole.ATTEMPT, None)
        if self._root._proxy is not None:
            for part in parts:
                self._root._proxy.end_route(part["key"])
        return taken

    def _make_end(self, key: str, outcome: str, fields: dict) -> dict:
        """One `end` part: a claimed cancel turns an error, abort or drop into `canceled`."""
        error_reason, error_message = fields.pop("error_reason", None), fields.pop("error_message", None)
        log_text, ended_at = fields.pop("log_text", None), fields.pop("ended_at", None)
        end: dict[str, Any] = {"outcome": AttemptOutcome(outcome), "ended_at": _to_iso(ended_at) or _get_now()}
        canceled_by = self._get_live().record_end(key)
        part: dict[str, Any] = {"key": key, "role": PartRole.ATTEMPT, "attempt_kind": AttemptKind.END,
                                "heartbeat_at": _get_now(), **fields}
        reason = error_reason
        if canceled_by is not None and end["outcome"] in _CANCEL_ENDINGS:
            end.update(outcome=AttemptOutcome.CANCELED, command_id=canceled_by)
            reason = "canceled"
        if reason is not None:
            part["error_reason"] = reason
        if error_message is not None:
            part["error_message"] = error_message
        if log_text:
            part.setdefault("log_tail", cut_tail(log_text, MAX_LOG_TAIL_BYTES)[0])
        part["end"] = end
        part = self._beats.fill_task(part, PartRole.ATTEMPT)
        self._beats.forget(key)
        return part

    def _send_beat(self, key: str, fields: dict, *, is_news: bool = False) -> None:
        beat = self._beats.take_beat(key, dict(fields), is_news=is_news)
        if beat is not None:
            self._send_held_beat(key, beat)

    def _send_held_beat(self, key: str, fields: dict) -> None:
        """A `progress` part: the attempt's whole snapshot, and the part fields given since the last one."""
        part = {**fields, "key": key, "role": PartRole.ATTEMPT, "attempt_kind": AttemptKind.PROGRESS,
                "heartbeat_at": _get_now()}
        snapshot = self._beats.get_snapshot(key)
        if snapshot:
            part["progress"] = snapshot
        self._log_parts([part], PartRole.ATTEMPT, None)

    def _record_failure(self, what: str, exc: Exception) -> None:
        """Count one failure; warn on the first of each call."""
        self.failures += 1
        if what not in self._warned:
            self._warned.add(what)
            effect = ("its samples cannot be asked to do it" if what.startswith("on_")
                      else "an ask it cannot do is refused with the generic reason" if what == "refuse"
                      else "its samples call the model server directly" if what == "live_url"
                      else "`probe samples live` misses those samples" if what.startswith("attempt_")
                      else "the run's capture will answer 'no'")  # fmt: skip
            _diagnostics.warn(
                f"probe: run.samples.{what} could not record ({type(exc).__name__}: {exc}); "
                f"training continues, and {effect}. Later failures of this call are counted, not shown."
            )

    def _log_parts(self, samples: Iterable[Any], role: str, step: int | None) -> int:
        tasks: list[dict] = []
        ready: list[dict] = []
        blobs: list[PendingBlob] = []
        taken = 0
        with self._lock:
            for sample in samples:
                prepared = self._prepare_one(sample, role, step)
                if prepared is None:
                    continue
                taken += 1
                blobs.extend(prepared.blobs)
                if prepared.task is not None:
                    tasks.append(prepared.task)
                if prepared.is_waiting_for_bundles:
                    self._waiting.setdefault(prepared.part.get("seal_step"), []).append(prepared.part)
                else:
                    ready.append(prepared.part)
            crowded = [step for step, parts in self._waiting.items() if len(parts) >= WAITING_MAX]
        # Spilled texts are stored outside the lock (rl-scale C9): a slow upload never holds another producer thread
        # or a Harbor hook's live write. A text that could not be stored leaves its part's row without it.
        for exc in self._preparer.store_blobs(blobs):
            self._record_failure("log", exc)
        self._send({BatchList.TASKS: tasks, BatchList.SAMPLES: ready})
        for crowded_step in crowded:
            self._release_waiting(crowded_step)
        return taken

    def _prepare_one(self, sample: Any, role: str, step: int | None) -> PreparedPart | None:
        try:
            prepared = self._preparer.prepare(self._beats.fill_task(sample, role), role=role, seal_step=step)
        except Exception as exc:  # noqa: BLE001 -- one bad sample never costs the rest
            self._record_failure("log", exc)
            return None
        return prepared

    def _send_seal(self, step: int, sent: int | None, dropped: Mapping[str, int] | None) -> None:
        """One seal per (step, producer) on the server: sealing a step again (an eval pass at a
        train step) declares the totals so far, never only what came since."""
        with self._lock:
            sealed = self._early_bundles.pop(step, []) + self._bundles.close_step(step)
            parts = self._drop_unsealed_refs(self._waiting.pop(step, []))
        checked = self._check_items({BatchList.SAMPLES: parts})
        with self._lock:
            totals = self._sealed.setdefault(step, {"sent": 0, "dropped": {}, "bundles": []})
            totals["sent"] += len(self._final_keys.pop(step, ()))
            if sent is not None:
                totals["sent"] = int(sent)
            for reason, count in (dropped or {}).items():
                if count:
                    totals["dropped"][str(reason)] = totals["dropped"].get(str(reason), 0) + int(count)
            totals["bundles"].extend(bundle.to_wire() for bundle in sealed)
            seal = {"step": step, "sent": totals["sent"], "dropped": dict(totals["dropped"]),
                    "bundles": list(totals["bundles"])}
        self._write_items(checked + self._check_items({BatchList.SEALS: [seal]}))

    def _release_waiting(self, step: int | None) -> None:
        """Close a step's bundles early (too many parts held, or the run closing) and journal the
        parts that waited on them; the step's seal later declares what is still open then."""
        with self._lock:
            closed = self._bundles.close_step(step)
            self._early_bundles.setdefault(step, []).extend(closed)
            parts = self._drop_unsealed_refs(self._waiting.pop(step, []))
        self._send({BatchList.SAMPLES: parts})

    def _close_all(self) -> None:
        if self._root is self and self._proxy is not None:
            self._proxy.stop(should_fail_live=False)  # first: what it saw last is journaled below
        for view in list(self._views.values()):
            view.close()
        self._beats.stop()
        if self._root is self and self._live is not None:
            self._live.close()
        steps = set(self._waiting) | set(self._bundles.get_open_steps())
        for step in sorted(steps, key=lambda value: (value is None, value or 0)):
            self._release_waiting(step)

    @staticmethod
    def _drop_unsealed_refs(parts: list[dict]) -> list[dict]:
        """A bundle that could not be read back has no sha256: its refs are dropped, not sent."""
        for part in parts:
            for name in ("log", "tokens", "trainer_tokens"):
                ref = part.get(name)
                if isinstance(ref, dict) and not ref.get("sha256"):
                    part.pop(name)
        return parts

    def _send(self, lists: Mapping[str, list]) -> None:
        self._write_items(self._check_items(lists))

    def _check_items(self, lists: Mapping[str, list]) -> list[tuple[str, dict]]:
        """Each item checked against its contract model, in order; one that fails is dropped alone
        and counted. A final part is counted toward its seal here, when it is sent."""
        checked: list[tuple[str, dict]] = []
        for name, values in lists.items():
            for item in values or ():
                try:
                    wire, model = to_wire_item(BatchList(name), item)
                except Exception as exc:  # noqa: BLE001 -- one bad item never costs the rest
                    self._record_failure(f"log {name}" if name != BatchList.SAMPLES else "log", exc)
                    continue
                if name == BatchList.SAMPLES:
                    self._count_part_sent(model)
                checked.append((str(name), wire))
        return checked

    def _count_part_sent(self, part) -> None:
        """A final part counts toward its seal step; a finished attempt's held beat is dropped."""
        if not part.is_final:
            return
        with self._lock:
            if part.seal_step is not None:
                self._final_keys.setdefault(part.seal_step, set()).add(part.key)
        if part.role is PartRole.GENERATOR:
            self._beats.forget(part.key)

    def _write_items(self, items: list[tuple[str, dict]]) -> None:
        """Journal ``items`` as ops of at most `OP_MAX_ITEMS` items and `OP_MAX_BYTES`."""
        if not items:
            return
        body: dict[str, list] = {}
        count = size = 0
        for name, item in items:
            weight = measure_bytes(item)
            if count and (count + 1 > OP_MAX_ITEMS or size + weight > OP_MAX_BYTES):
                self._write_op(body)
                body, count, size = {}, 0, 0
            body.setdefault(name, []).append(item)
            count += 1
            size += weight
        self._write_op(body)

    def _write_op(self, lists: dict[str, list], *, plan: dict | None = None) -> None:
        run = self._run
        body = run._stamp_writer({"producer": self.producer, **lists})
        # Required by the batch, and never a fence there: an epoch this handle does not know is 1.
        body["write_epoch"] = run.write_epoch or 1
        if plan is not None:
            body[PLAN_FIELD] = plan
        run._progress.bump()
        run._client.write("POST", path_for(WriteOp.SAMPLES, run.id), body, strict=False)

    def _send_phases(self, step: int, phases: list) -> None:
        from ..metrics.spans import _span_id_for

        run = self._run
        spans = build_phase_spans(
            step, phases, epoch=run.write_epoch or 1, make_id=lambda key: _span_id_for(run.id, "phase", key)
        )
        for start in range(0, len(spans), SPANS_MAX):
            body = run._stamp_writer({"spans": spans[start:start + SPANS_MAX]})
            run._client.write("POST", path_for(WriteOp.SPANS, run.id), body, strict=False, blocking=False)

    def _wait_for_seals(self, timeout: float | None) -> bool:
        client = self._run._client
        return wait_for_last_seals(lambda: client.get_sample_capture(self._run.id), timeout=timeout)

    def _upload_bundle(self, bundle: Bundle) -> None:
        kind = get_artifact_kind(bundle.kind)
        name = f"{kind}-{_SAFE_NAME.sub('_', self.producer)}-step{bundle.step}-p{bundle.part}.gz"
        meta = {"sample_bundle": {"producer": self.producer, "step": bundle.step, "members": bundle.members}}
        self._guard(
            "upload_bundle",
            lambda: self._run.log_artifact(
                name,
                path=str(bundle.path),
                kind=kind,
                content_type="application/gzip",
                step_index=bundle.step,
                meta=meta,
                strict=False,
            ),
        )

    def _upload_text(self, path: Path, sha256: str, size: int) -> None:
        self._run.log_artifact(
            f"sample-text-{sha256[:16]}.txt",
            path=str(path),
            kind=TEXT_ARTIFACT_KIND,
            content_type="text/plain",
            meta={"sample_blob": {"sha256": sha256, "size_bytes": size}},
            strict=False,
        )


def _to_iso(value: datetime | str | None) -> str | None:
    return value.isoformat() if isinstance(value, datetime) else value


def _cut_activity(activity: str | None) -> str | None:
    """The activity line, scrubbed, at most 512 characters (keeping its start: the tool and its command)."""
    if not activity:
        return None
    return _scrub_text(" ".join(str(activity).split()))[:MAX_ACTIVITY_CHARS]


def _scrub_text(text: str) -> str:
    from ...redaction import scrub_string

    return scrub_string(text)


def _get_spool_folder(run: Run) -> str:
    journal = getattr(run._client, "journal", None)
    folder = getattr(journal, "dir", None)
    if folder:
        return str(folder)
    import tempfile

    return tempfile.gettempdir()
