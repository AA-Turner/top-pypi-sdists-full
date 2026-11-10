"""`probe.integrations.art.track(model)`: ART's metrics, trajectories, weight versions and checkpoints on one Probe
run, with no W&B (RL plan §6.2). It wraps the instance's methods only, never a class. DESIGN.md. Line refs are
`OpenPipe/ART@414acc5`."""

from __future__ import annotations

import asyncio
import functools
import math
import os
import socket
import weakref
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit

from probe.sdk import errors

from .. import _rl_owner
from .._live import refuse_commands
from . import checkpoints as _checkpoints
from .live import COMMAND_REFUSAL, ArtLive, TaskKeySpec
from .trajectories import ScenarioSpec, TrajectoryMapper

#: The producer an ART process writes samples as: rollouts and training share one process.
PRODUCER = "art"
#: ART prefixes a metric with its split unless its first part is one of these (`model.py:125-137`, `:641-653`).
METRIC_SECTIONS = frozenset({"reward", "loss", "offpolicy", "pipeline", "throughput", "costs", "time", "data"})
METRIC_SPLITS = frozenset({"train", "val", "test"})
#: Added to ART's own metrics at each train log: the PipelineTrainer queue's depth (console-only in ART).
QUEUE_DEPTH_KEY = "pipeline/queue_depth"
#: ART opens a W&B run whenever this is set, even with `report_metrics=[]` (`local/backend.py:324`).
WANDB_KEY_ENV = "WANDB_API_KEY"

_TRACKERS: dict[int, tuple[weakref.ref, ArtTracker]] = {}


def get_rewind_step(checkpoint_step: int) -> int:
    """A relaunch at ART checkpoint ``k`` trains step k+1 next (`local/backend.py:885`), so the run
    continues from R = k+1: `Rewind(step=k+1)`."""
    return checkpoint_step + 1


def track(
    model: Any,
    backend: Any = None,
    trainer: Any = None,
    scenario: ScenarioSpec = None,
    *,
    reward_max: float | None = None,
    **init_kwargs: Any,
) -> ArtTracker:
    """Record ``model``'s training on Probe. ``backend`` (else the one ``model.register`` gets) and a
    ``PipelineTrainer`` are wrapped too. ``scenario`` names the trajectory metadata keys that pose a task
    (or is a callable ``(trajectory, group) -> dict``). ``reward_max`` is the full reward (default 1.0).
    Other keywords go to `probe.init()` (``project=``, ``experiment=``, ``tags=``); a run the script
    already opened is used as it is. Refuses to start while `WANDB_API_KEY` is set."""
    from probe.sdk.settings.settings import Mode, resolve_mode

    if resolve_mode(None) is Mode.DISABLED:
        return ArtTracker(model, is_enabled=False)
    if os.environ.get(WANDB_KEY_ENV):
        raise errors.ValidationError(
            f"probe.integrations.art.track(): {WANDB_KEY_ENV} is set, and ART opens a W&B run whenever it is "
            "(even with report_metrics=[]). Unset it to record this run on Probe."
        )
    found = _TRACKERS.get(id(model))
    tracker = found[1] if found is not None and found[0]() is model else None
    if tracker is None or tracker.is_finished:
        tracker = ArtTracker(model, scenario=scenario, reward_max=reward_max, init_kwargs=init_kwargs)
        _TRACKERS[id(model)] = (weakref.ref(model), tracker)
    for target in (backend, getattr(trainer, "backend", None), getattr(model, "_backend", None)):
        if target is not None:
            tracker.guard.call("backend", tracker.watch_backend, target)
    if trainer is not None:
        tracker.guard.call("PipelineTrainer", tracker.watch_trainer, trainer)
    return tracker


@dataclass
class _Seen:
    """The key an ART object got when a hook first saw it, and which of its parts went out."""

    key: str
    group_key: str
    has_generator: bool = False
    has_trainer: bool = False


class _SeenObjects:
    """Keys by object identity, kept while the object lives: one attempt keeps one key whether the train
    call or the log call meets it first."""

    def __init__(self) -> None:
        self._entries: dict[int, tuple[weakref.ref, _Seen]] = {}

    def get(self, target: Any) -> _Seen | None:
        entry = self._entries.get(id(target))
        return entry[1] if entry is not None and entry[0]() is target else None

    def add(self, target: Any, key: str, group_key: str) -> _Seen:
        seen = _Seen(key, group_key)
        oid = id(target)

        def forget(ref: weakref.ref, oid: int = oid) -> None:
            entry = self._entries.get(oid)
            if entry is not None and entry[0] is ref:
                del self._entries[oid]

        try:
            self._entries[oid] = (weakref.ref(target, forget), seen)
        except TypeError:
            pass  # cannot be weakly kept: it gets a key per call, never a stale one
        return seen


class ArtTracker:
    """One ART model's Probe run. Every hook fails open (`HookGuard`): ART's own call always runs, with the
    caller's arguments, and its result or error is the caller's."""

    def __init__(
        self,
        model: Any,
        *,
        scenario: ScenarioSpec = None,
        reward_max: float | None = None,
        init_kwargs: Mapping[str, Any] | None = None,
        is_enabled: bool = True,
    ) -> None:
        self._model = model
        self._scenario = scenario
        self._reward_max = reward_max
        self._init_kwargs = dict(init_kwargs or {})
        self.guard = _rl_owner.HookGuard("ART")
        self.run: Any = None
        self._samples: Any = None
        self._mapper: TrajectoryMapper | None = None
        self._is_owner = False
        self._is_open_failed = False
        self._open_lock: asyncio.Lock | None = None
        self._step: int | None = None
        self._floor = 0
        self._seen = _SeenObjects()
        self._ordinals: Counter = Counter()
        self._sealed: set[int] = set()
        self._pending_drops: dict[int, Counter] = defaultdict(Counter)
        self._max_staleness: int | None = None
        self._set_names: dict[str, str] = {}
        self._installed: list[tuple[Any, str, Any]] = []
        self._backends: set[int] = set()
        self._trainers: set[int] = set()
        self.queue_depth: Any = None
        #: Decorated rollouts as live samples (`live.py`, `record_rollout`).
        self.live = ArtLive(self)
        self.is_finished = not is_enabled
        if is_enabled:
            self.guard.call("the model", self._wrap_model)

    # -- public ------------------------------------------------------------------------------------------
    def watch_backend(self, backend: Any) -> None:
        """Wrap ``backend.train`` (this model's calls only): consumption, the commit, the weight version."""
        if self.is_finished or id(backend) in self._backends or not callable(getattr(backend, "train", None)):
            return
        self._backends.add(id(backend))
        original = getattr(backend, "train")

        @functools.wraps(original)
        async def call_train(model: Any, trajectory_groups: Iterable[Any], *args: Any, **kwargs: Any) -> Any:
            if model is not self._model or self.is_finished:
                return await original(model, trajectory_groups, *args, **kwargs)
            groups = list(trajectory_groups)
            started = datetime.now(timezone.utc)
            planned = await self.guard.call_async("backend.train", self._record_consumption, groups)
            result = await original(model, groups, *args, **kwargs)
            await self.guard.call_async("backend.train", self._record_trained_step, result, planned, started)
            return result

        self.install(backend, "train", call_train)

    def watch_trainer(self, trainer: Any) -> None:
        """Wrap a `PipelineTrainer`'s stale and zero-variance drops, checkpoint rows and queue depth."""
        if self.is_finished or id(trainer) in self._trainers:
            return
        from .pipeline import PipelineHooks

        self._trainers.add(id(trainer))
        self.watch_backend(trainer.backend)
        PipelineHooks(self, trainer)
        limit = getattr(trainer, "max_steps_off_policy", None)
        if isinstance(limit, int):
            self._max_staleness = limit
            if self._samples is not None:
                self.guard.call("plan", self._samples.plan, max_staleness=limit)

    def record_rollout(self, function: Callable[..., Any] | None = None, *, task_key: TaskKeySpec) -> Any:
        """Decorate an async rollout (`async def rollout(model, scenario) -> art.Trajectory`): each call is a live
        sample in `probe samples live` (running, slow, hung, failing) from its start to its return, and its trajectory
        names it (`metadata["probe_attempt_key"]`). ``task_key`` is the task's key, or a callable reading it from the
        rollout's arguments (`lambda model, scenario: scenario.id`); use the one its trajectory's `task_id` holds."""
        if function is None:
            return functools.partial(self.record_rollout, task_key=task_key)
        return self.live.wrap_rollout(function, task_key)

    def send_progress(self, **snapshot: Any) -> None:
        """Inside a decorated rollout: how it is going (`phase`, `turns`, `tokens`, `activity`). A change is progress;
        a rollout with none for 10 minutes reads hung. Never raises."""
        self.guard.call("a live sample", self.live.send_progress, snapshot)

    def get_where(self) -> dict:
        """Where this model's rollouts run (host, inference engine), once the run is open."""
        return dict(self._mapper.where) if self._mapper is not None else {}

    def get_cached_step(self) -> int | None:
        """The model's step as the hooks last saw it (the weights its rollouts sample from)."""
        return self._step

    def finish(self, status: str | None = None) -> None:
        """Close the record: the terminal manifest, the producers' barrier, then the run itself when this
        tracker opened it. ART's methods are unwrapped. Never raises."""
        if self.is_finished:
            return
        self.is_finished = True
        try:
            self._close(should_finish=self._is_owner, status=status)
        finally:
            self._unwrap()
            found = _TRACKERS.get(id(self._model))
            if found is not None and found[1] is self:
                del _TRACKERS[id(self._model)]

    def close_at_exit(self) -> None:
        """At exit: the manifest and barrier only; `probe.init()`'s exit hooks give the run its status."""
        if not self.is_finished:
            self.is_finished = True
            self._close(should_finish=False, status=None)

    def install(self, target: Any, name: str, wrapper: Any) -> None:
        """``wrapper`` as ``target.name`` on this instance alone (a pydantic model's `__setattr__` refuses
        an unknown name, so the instance dict is written directly)."""
        object.__setattr__(target, name, wrapper)
        self._installed.append((target, name, wrapper))

    def add_drops(self, step: int, reason: str, count: int) -> None:
        """Drops that exist only as counts, declared in ``step``'s next seal."""
        if count > 0:
            self._pending_drops[step][reason] += count

    def log_metrics(self, metrics: Mapping[str, float], step: int) -> None:
        if self.run is not None:
            self.run.log(dict(metrics), step=step)

    # -- the model's methods -------------------------------------------------------------------------------
    def _wrap_model(self) -> None:
        model = self._model
        log_metrics = model._log_metrics
        log = model.log

        @functools.wraps(log_metrics)
        def call_log_metrics(metrics: dict, split: str, step: int) -> Any:
            result = log_metrics(metrics, split, step)
            if not self.is_finished and self.run is not None:
                self.guard.call("metrics", self._send_metrics, metrics, split, step)
            return result

        @functools.wraps(log)
        async def call_log(
            trajectories: Any = None, split: str = "val", *, metrics: Any = None, step: int | None = None
        ) -> Any:
            if trajectories is not None:
                trajectories = self._normalize(trajectories)
            if not self.is_finished:
                resolved = await self.guard.call_async("model.log", self._record_log, trajectories, split, step)
                if step is None and isinstance(resolved, int):
                    step = resolved  # what ART computes itself (`model.py:866`)
            return await log(trajectories, split, metrics=metrics, step=step)

        self.install(model, "_log_metrics", call_log_metrics)
        self.install(model, "log", call_log)
        register = getattr(model, "register", None)
        if callable(register):

            @functools.wraps(register)
            async def call_register(backend: Any, *args: Any, **kwargs: Any) -> Any:
                result = await register(backend, *args, **kwargs)
                self.guard.call("register", self.watch_backend, backend)
                return result

            self.install(model, "register", call_register)
        train_sft = getattr(model, "train_sft", None)
        if callable(train_sft):

            @functools.wraps(train_sft)
            async def call_train_sft(trajectories: Iterable[Any], *args: Any, **kwargs: Any) -> Any:
                items = list(trajectories)
                if not self.is_finished:
                    await self.guard.call_async("train_sft", self.ensure_run)
                result = await train_sft(items, *args, **kwargs)
                if not self.is_finished:
                    await self.guard.call_async("train_sft", self._record_sft, items)
                return result

            self.install(model, "train_sft", call_train_sft)

    def _unwrap(self) -> None:
        for target, name, wrapper in reversed(self._installed):
            try:
                if target.__dict__.get(name) is wrapper:  # another tracker's wrap on top stays (ours passes through)
                    del target.__dict__[name]
            except Exception:  # noqa: BLE001 -- an object that will not give it back keeps the wrap
                pass
        self._installed.clear()

    def _normalize(self, trajectories: Any) -> Any:
        """ART's own normalizing into groups (`model.py:819-836`), done once so both sides see the same
        group objects; anything it refuses goes to ART unchanged, to raise there."""
        items = list(trajectories)
        normalize = getattr(self._model, "_normalize_trajectory_groups", None)
        try:
            return normalize(items) if callable(normalize) else items
        except Exception:  # noqa: BLE001 -- ART raises its own error on the same input
            return items

    # -- the run -------------------------------------------------------------------------------------------
    async def ensure_run(self) -> None:
        if self.run is not None or self._is_open_failed or self.is_finished:
            return
        if self._open_lock is None:
            self._open_lock = asyncio.Lock()
        async with self._open_lock:
            if self.run is not None or self._is_open_failed:
                return
            try:
                step = await self._get_model_step()
            except Exception:  # noqa: BLE001 -- an unregistered model has no step yet: a fresh start
                step = 0
            self.guard.call("run open", self._open, step)
            self._is_open_failed = self.run is None

    def _open(self, step: int) -> None:
        model = self._model
        rewind = get_rewind_step(step) if step > 0 else None
        run, owns = _rl_owner.open_run(
            name=getattr(model, "name", None),
            external_id=f"art:{getattr(model, 'project', '')}/{getattr(model, 'name', '')}",
            rewind_step=rewind,
            config=self._get_config(),
            init_kwargs=self._init_kwargs,
        )
        self.run, self._is_owner, self._step, self._floor = run, owns, step, rewind or 0
        self._samples = run.samples.as_producer(PRODUCER)
        self._mapper = TrajectoryMapper(
            scenario=self._scenario,
            base_model=getattr(model, "base_model", None),
            run_id=str(run.id),
            host=socket.gethostname(),
            engine=_get_engine(model),
        )
        self.live.open(self._samples, self._reward_max)
        plan: dict[str, Any] = {"producers": [PRODUCER]}
        if self._reward_max is not None:
            plan["reward_max"] = self._reward_max
        if self._max_staleness is not None:
            plan["max_staleness"] = self._max_staleness
        self._samples.plan(**plan)
        refuse_commands(self._samples, COMMAND_REFUSAL)
        self.guard.call("base model", self._record_base_model, run)
        _rl_owner.close_at_exit(self)

    def _get_config(self) -> dict:
        """The model's own fields, minus its inference key and its unserializable `config`
        (`safe_model_dump`, `model.py:1144-1151`)."""
        dump = getattr(self._model, "safe_model_dump", None)
        try:
            config = dict(dump(mode="json")) if callable(dump) else {}
        except Exception:  # noqa: BLE001 -- a config Probe cannot read never costs the run
            config = {}
        config.pop("inference_api_key", None)
        config.pop("config", None)
        user_config = getattr(self._model, "config", None)
        to_dict = getattr(user_config, "model_dump", None)
        if callable(to_dict):
            try:
                config["config"] = to_dict(mode="json")
            except Exception:  # noqa: BLE001 -- ART itself leaves out a config it cannot dump
                pass
        from probe.sdk.redaction import default_scrub

        return {"art": default_scrub(config)}  # a user's config can hold a judge's API key

    def _record_base_model(self, run: Any) -> None:
        """ART's ``base_model`` as the Hub model this run starts from (role ``init``), for the lineage of
        `probe checkpoint best`. Off with read capture."""
        from probe.sdk.capture import lineage as inputs

        from .._hub import get_hub_model

        hub_ref = get_hub_model(getattr(self._model, "base_model", None))
        if hub_ref is None or not inputs.enabled(self._init_kwargs.get("capture_reads")):
            return
        run.use_dataset(hub_ref.to_source(), role="init")  # by its uri: a run token may record it

    async def _get_model_step(self) -> int:
        model = self._model
        return int(await model.get_step()) if getattr(model, "trainable", False) else 0

    def _close(self, *, should_finish: bool, status: str | None) -> None:
        if self.run is None:
            return
        for step in sorted(self._pending_drops):
            self.guard.call("seal", self._send_seal, step)
        final = max(self._sealed) if self._sealed else None
        self.guard.call(
            "finish", _rl_owner.close_run, self.run, self._samples,
            final_step=final, should_finish=should_finish, status=status,
        )

    # -- hooks ---------------------------------------------------------------------------------------------
    async def _record_log(self, groups: Any, split: str, step: int | None) -> int | None:
        await self.ensure_run()
        if step is None:
            step = await self._get_model_step()
        if self._samples is None or groups is None or not isinstance(groups, list):
            return step
        parts, rows = self._map_groups(groups, split=split, step=step, version=step, consumed=None)
        self._send(parts, rows, step)
        return step

    async def _record_consumption(self, groups: list) -> int | None:
        """Before ART trains: the batch as consumed by the step it will make, `pre + 1` (ART advances one
        step per train call, `local/backend.py:885`; PipelineTrainer counts on it, `pipeline_trainer/trainer.py:514`).
        A crash mid-update leaves them consumed, never committed."""
        await self.ensure_run()
        if self._samples is None:
            return None
        pre = self._step if self._step is not None else await self._get_model_step()
        step = pre + 1
        parts, rows = self._map_groups(groups, split="train", step=step, version=pre, consumed=(step, pre))
        self._send(parts, rows, step, should_seal=False)
        return step

    async def _record_trained_step(self, result: Any, planned: int | None, started: datetime) -> None:
        if self._samples is None:
            return
        step = int(result.step)
        if planned is not None and step != planned:
            self.guard.record_failure("train step", ValueError(f"ART trained step {step}, not {planned}"))
        self._step = step
        self._samples.commit(step, consumed_at=started)
        await self._record_weights(
            step, getattr(result, "checkpoint_path", None), getattr(result, "artifact_name", None)
        )
        self._send_seal(step)

    async def _record_sft(self, items: list) -> None:
        """SFT examples, trained by the step `train_sft` just saved (`unsloth/service.py:850-862`)."""
        if self._samples is None:
            return
        pre = self._step if self._step is not None else 0
        step = await self._get_model_step()
        ordinal = self._take_ordinal("sft", step)
        parts: list[dict] = []
        for index, trajectory in enumerate(items):
            seen = self._seen.get(trajectory) or self._seen.add(trajectory, f"sft:{step}:{ordinal}:{index}", "")
            if not seen.has_generator:
                part = self.guard.call("an SFT example", self._mapper.map_sft, trajectory, key=seen.key)
                if part is None:
                    continue
                parts.append(part)
                seen.has_generator = True
            if not seen.has_trainer:
                parts.append({"key": seen.key, "role": "trainer", "consumed_step": step, "consumed_version": pre})
                seen.has_trainer = True
        self._samples.log(parts, step=step)
        self._step = step
        self._samples.commit(step)
        output_dir = getattr(self._model, "_get_output_dir", None)
        path = os.path.join(output_dir(), "checkpoints", f"{step:04d}") if callable(output_dir) else None
        await self._record_weights(step, path if path and os.path.isdir(path) else None, None)
        self._send_seal(step)

    # -- inside --------------------------------------------------------------------------------------------
    def _map_groups(
        self, groups: list, *, split: str, step: int, version: int | None, consumed: tuple[int, int] | None
    ) -> tuple[list[dict], list[dict]]:
        """Parts for the attempts of ``groups`` this tracker has not sent yet, and their group rows. With
        ``consumed`` = (step, version), every trajectory also gets a trainer part."""
        mapper = self._mapper
        ordinal = self._take_ordinal(split, step)
        parts: list[dict] = []
        consumptions: list[dict] = []
        rows: list[dict] = []
        for index, group in enumerate(groups):
            group_key = f"{split}:{step}:{ordinal}:{index}"
            fresh: list[dict] = []
            members = list(getattr(group, "trajectories", None) or [])
            for position, trajectory in enumerate(members):
                seen = self._seen.get(trajectory) or self._seen.add(trajectory, f"{group_key}:{position}", group_key)
                if not seen.has_generator:
                    part = self.guard.call(
                        "a trajectory", mapper.map_trajectory, trajectory, group,
                        key=seen.key, group_key=seen.group_key, split=split, version=version,
                    )
                    if part is None:
                        continue  # counted and warned; the rest of the batch still goes
                    fresh.append(part)
                    seen.has_generator = True
                if consumed is not None and not seen.has_trainer:
                    consumptions.append({"key": seen.key, "role": "trainer", "consumed_step": consumed[0],
                                         "consumed_version": consumed[1]})
                    seen.has_trainer = True
            for position, exception in enumerate(getattr(group, "exceptions", None) or []):
                seen = self._seen.get(exception) or self._seen.add(exception, f"{group_key}:x{position}", group_key)
                if not seen.has_generator:
                    part = self.guard.call(
                        "a group exception", mapper.map_exception, exception, group,
                        key=seen.key, group_key=seen.group_key, split=split, version=version,
                    )
                    if part is not None:
                        fresh.append(part)
                        seen.has_generator = True
            if fresh:
                rows.append(_make_group_row(fresh, group, group_key, split))
                parts.extend(fresh)
        return parts + consumptions, rows

    def _send(self, parts: list[dict], rows: list[dict], step: int, *, should_seal: bool = True) -> None:
        if parts:
            self._samples.log(parts, step=step)
        if rows:
            self._samples.log_groups(rows)
        if should_seal:
            self._send_seal(step)

    def _send_seal(self, step: int) -> None:
        """Seal ``step`` with its totals so far, first sealing any step this producer skipped since its
        last (it had nothing there), so capture's 0..N finds a seal for every step."""
        start = max(self._sealed) + 1 if self._sealed else self._floor
        for gap in range(start, step):
            if gap not in self._sealed:
                self._samples.seal(gap)
                self._sealed.add(gap)
        drops = self._pending_drops.pop(step, None)
        self._samples.seal(step, dropped=dict(drops) if drops else None)
        self._sealed.add(step)

    async def _record_weights(self, step: int, path: str | None, artifact_name: str | None) -> None:
        """The weight version ``step`` made, naming its checkpoint. Hashing and staging run in a thread so
        a PipelineTrainer's rollouts keep going while a big checkpoint is read."""
        checkpoint = None
        if path:
            checkpoint = await self.guard.call_async(
                "checkpoint", asyncio.to_thread, _checkpoints.record_checkpoint, self.run, path,
                name=str(getattr(self._model, "name", "") or "checkpoint"), step=step,
                warn=lambda _key, message: self.guard.record_failure("checkpoint", RuntimeError(message)),
                taken=self._set_names,
            )
        elif artifact_name:
            checkpoint = _checkpoints.make_artifact_ref(artifact_name, step)
        self._samples.weights(step, after_step=step, checkpoint=checkpoint)

    def _send_metrics(self, metrics: Mapping[str, Any], split: str, step: int) -> None:
        """ART's metric row under ART's own names (`model.py:641-653`), at its `training_step`."""
        row: dict[str, float] = {}
        for key, value in metrics.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                continue
            first = key.split("/", 1)[0]
            keep = split in METRIC_SPLITS and "/" in key and (first in METRIC_SECTIONS or first in METRIC_SPLITS)
            row[key if keep else f"{split}/{key}"] = float(value)
        depth = self.queue_depth() if split == "train" and callable(self.queue_depth) else None
        if isinstance(depth, int):
            row[QUEUE_DEPTH_KEY] = float(depth)
        if row:
            self.run.log(row, step=step)

    def _take_ordinal(self, split: str, step: int) -> int:
        ordinal = self._ordinals[(split, step)]
        self._ordinals[(split, step)] += 1
        return ordinal


def _make_group_row(parts: list[dict], group: Any, group_key: str, split: str) -> dict:
    first = parts[0]
    row: dict[str, Any] = {
        "group_key": group_key,
        "size": len(getattr(group, "trajectories", None) or []) + len(getattr(group, "exceptions", None) or []),
        "task_key": first["task_key"],
        "scenario": first.get("scenario") or {},
    }
    if first.get("scheduled_step") is not None:
        row["scheduled_step"] = first["scheduled_step"]
    if split == "discarded":
        row["drop_reason"] = "zero_variance"
    return row


def _get_engine(model: Any) -> str | None:
    """The inference server the model samples from, as `scheme://host:port` (no path, user or query)."""
    url = getattr(model, "inference_base_url", None)
    if not isinstance(url, str) or not url:
        return None
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.hostname}{f':{parts.port}' if parts.port else ''}" if parts.hostname else None
