"""The verl actor worker's per-sample training metrics (plan rl-trajectory-metrics T3). In each FSDP worker process
`TrainingWorker.train_mini_batch` (one step's share of this rank) and `train_batch` (one optimizer update) are wrapped
on the class, and the loss function the worker holds is wrapped on the instance: each micro-batch's `ppo_loss` call
becomes rows, each update its records, sent as producer `verl-train-<dp rank>` from a background thread. Every wrap
runs verl's own function first and returns its result untouched; Probe's part is guarded. Line refs are
`verl-project/verl@b17218ba58a6`. Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

import functools
import inspect
import json
import logging
import sys
import threading
from dataclasses import dataclass, field
from typing import Any

from probe.sdk.run.samples.points import (
    PointsSender, TrainingGuard, UpdateLog, UpdatePlace, get_optimizer_step, to_float, watch_import,
)

from .loss import CRITIC_PREFIX, ROW_FIELD, ReductionWatch, add_geo_mean_pg, read_geo_mean_fields, summarize_loss_call
from .plan import (
    DISTILLATION_MODES, DISTILLATION_POLICY_MODES, SUPPORTED_LOSS_MODES, build_critic_plan, get_megatron_reason,
)

logger = logging.getLogger(__name__)

#: Where `TrainingWorker` lives (`workers/engine_workers.py:112`) and verl's own loss (`workers/utils/losses.py:56`).
WORKER_MODULE = "verl.workers.engine_workers"
LOSSES_MODULE = "verl.workers.utils.losses"
#: The actor losses `init_model` may set (`engine_workers.py:682-689`), by module: score centering's and
#: distillation's both end in `ppo_loss` (T2c).
ACTOR_LOSSES = {
    LOSSES_MODULE: "ppo_loss",
    "verl.trainer.ppo.score_centering": "score_centering_ppo_loss",
    "verl.trainer.distillation.losses": "distillation_ppo_loss",
}
#: The keyword a loss is called with when the engine runs it as its logits processor (`transformer_impl.py:1342`,
#: `:1440`): top-k distillation and score centering; it returns per-token tensors, not (loss, metrics).
LOGITS_PROCESSOR_ARGUMENT = "student_logits"
#: The non-tensor field the driver puts on a step's batch (`driver.stamp_update_batch`): JSON of `StepFacts`.
STEP_FIELD = "probe_points"
#: Each worker rank writes as its own producer, never declared on the plan (sample capture is unchanged); a critic's
#: ranks as their own (D4), whose first rank sends the critic's own plan.
PRODUCER_PREFIX = "verl-train-"
CRITIC_PRODUCER_PREFIX = "verl-critic-"
#: verl's critic is a training worker built with this model type (`TrainingWorkerConfig`, `ray_trainer.py:825`).
CRITIC_MODEL_TYPE = "value_model"
ACTOR, CRITIC = "actor", "critic"
WRAPPED_MARK = "__probe_verl_training__"
#: The marker a hooked loss function carries, and the function it wraps.
HOOKED_LOSS = "__probe_loss_fn__"
#: What every guarded call says it records.
WHAT = "per-sample training metrics"


@dataclass
class StepFacts:
    """One step's share of this rank: what the driver sent and what this worker found."""

    step: int
    keys: list[str | None]
    updates_in_step: int | None
    reduction: str | None
    rank: int
    ranks: int
    coefficients: dict[str, float]
    role: str = ACTOR
    #: geo_mean: the pg term is rebuilt per row (`loss.add_geo_mean_pg`); the loss config it reads.
    geo_mean_config: Any = None
    next_update: int = 0


@dataclass
class _Current:
    log: UpdateLog
    coefficients: dict[str, float]
    role: str = ACTOR
    geo_mean_config: Any = None


@dataclass
class VerlTraining:
    """This worker process's recording: its sender (joining the run in the background from the first stamped step)
    and each worker's step in progress."""

    guard: TrainingGuard = field(default_factory=lambda: TrainingGuard("verl"))
    sender: PointsSender = field(default_factory=lambda: PointsSender("verl"))
    #: The critic's own producer: verl colocates the actor's and the critic's workers in one process by default.
    critic_sender: PointsSender = field(default_factory=lambda: PointsSender("verl"))
    steps: dict[int, StepFacts] = field(default_factory=dict)
    _local: threading.local = field(default_factory=threading.local)
    _warned: set[str] = field(default_factory=set)
    _has_declared_stop: bool = False
    _has_declared_critic: bool = False

    # -- the wraps -----------------------------------------------------------------------------------------
    def install(self, module: Any) -> bool:
        """Wrap `TrainingWorker.train_mini_batch` and `train_batch` on the class, once, both or neither."""
        cls = getattr(module, "TrainingWorker", None)
        if not isinstance(cls, type) or getattr(cls.__dict__.get("train_batch"), WRAPPED_MARK, False):
            return False
        originals = {name: cls.__dict__.get(name) for name in ("train_mini_batch", "train_batch")}
        missing = sorted(name for name, original in originals.items() if not callable(original))
        if missing:
            raise AttributeError(f"verl's TrainingWorker has no {', '.join(missing)}: nothing is wrapped")
        cls.train_mini_batch = self._wrap_step(originals["train_mini_batch"])
        cls.train_batch = self._wrap_update(originals["train_batch"])
        return True

    def _wrap_step(self, original: Any) -> Any:
        @functools.wraps(original)
        def call_train_mini_batch(worker: Any, *args: Any, **kwargs: Any) -> Any:
            facts = self.guard.call(WHAT, self.open_step, worker, args, kwargs)
            try:
                return original(worker, *args, **kwargs)
            finally:
                if facts is not None:
                    self.steps.pop(id(worker), None)

        setattr(call_train_mini_batch, WRAPPED_MARK, True)
        return call_train_mini_batch

    def _wrap_update(self, original: Any) -> Any:
        @functools.wraps(original)
        def call_train_batch(worker: Any, *args: Any, **kwargs: Any) -> Any:
            current = self.guard.call(WHAT, self.start_update, worker)
            if current is None:
                return original(worker, *args, **kwargs)
            self._local.current = current
            try:
                output = original(worker, *args, **kwargs)
            finally:
                self._local.current = None
            self.guard.call(WHAT, self.finish_update, worker, current.log, output)
            return output

        setattr(call_train_batch, WRAPPED_MARK, True)
        return call_train_batch

    def wrap_loss(self, loss_function: Any) -> Any:
        """The worker's loss function, recording each call made inside an update (an eval or log-prob pass that
        computes a loss outside one records nothing, D6). verl's return value is handed back as it came."""

        signature = _get_signature(loss_function)

        @functools.wraps(loss_function)
        def call_loss(*args: Any, **kwargs: Any) -> Any:
            current = getattr(self._local, "current", None)
            if current is None or is_logits_processor_call(signature, args, kwargs):
                return loss_function(*args, **kwargs)  # a logits-processor call is no micro-batch: never counted
            index = current.log.count_call()  # counted before anything can fail: a lost call reads missing
            watch = ReductionWatch()
            calls = self.guard.call(WHAT, watch.start)
            try:
                output = loss_function(*args, **kwargs)
            finally:
                self.guard.call(WHAT, watch.stop)
            self.guard.call(WHAT, self.record_micro_batch, current, index, calls, loss_function, args, kwargs, output)
            return output

        setattr(call_loss, HOOKED_LOSS, loss_function)
        return call_loss

    # -- a step, an update, a micro-batch ------------------------------------------------------------------
    def open_step(self, worker: Any, args: tuple, kwargs: dict) -> StepFacts | None:
        """The step the driver stamped on this batch, when this worker's path is one the hook supports."""
        data = kwargs.get("data", args[0] if args else None)
        raw = _take_non_tensor(data, STEP_FIELD)
        if raw is None:
            return None
        sent = json.loads(raw)
        role = CRITIC if is_critic(worker) else ACTOR
        reason = get_unsupported_reason(worker)
        if reason is not None:
            self._warn_once(reason, f"Probe records no per-sample training metrics on this verl worker: {reason}.")
            if role == CRITIC:  # a critic's path names only the critic's keys (D4), never the run's `*` stop
                self.guard.call(WHAT, self._send_critic_plan, worker, _get_first_rank(worker), reason)
            elif not self._has_declared_stop:
                self.guard.call(WHAT, self._send_stop_reason, _get_first_rank(worker), reason)
            return None
        place = get_recording_place(worker.engine)
        if place is None:
            return None
        rank, ranks = place
        config = _get_loss_config(worker.loss_fn)
        if role == CRITIC:
            coefficients = {"critic/vf_loss": 0.5}  # `vf_loss = 0.5 * agg_loss(clipped_vf_losses)` (`:2175`)
            self.critic_sender.start(f"{CRITIC_PRODUCER_PREFIX}{rank}")
            self._send_critic_plan(worker, rank, None)
        else:
            coefficients = get_actor_coefficients(worker.loss_fn)
            self.sender.start(f"{PRODUCER_PREFIX}{rank}")  # joins in the background while the step trains
        facts = StepFacts(step=int(sent["step"]), keys=list(sent["keys"]), updates_in_step=sent.get("updates_in_step"),
                          reduction=sent.get("reduction"), rank=rank, ranks=ranks,
                          coefficients=coefficients, role=role,
                          geo_mean_config=config if get_loss_mode(config) == "geo_mean" else None,
                          next_update=int(sent.get("first_update") or 0))  # fmt: skip
        self.steps[id(worker)] = facts
        return facts

    def start_update(self, worker: Any) -> _Current | None:
        facts = self.steps.get(id(worker))
        if facts is None or self.get_sender(facts.role).is_disabled:
            return None
        if not hasattr(worker.loss_fn, HOOKED_LOSS):
            worker.loss_fn = self.wrap_loss(worker.loss_fn)  # on the instance, whenever it was set
        place = UpdatePlace(step=facts.step, update=facts.next_update, rank=facts.rank, ranks=facts.ranks,
                            updates_in_step=facts.updates_in_step, reduction=facts.reduction)  # fmt: skip
        facts.next_update += 1
        return _Current(UpdateLog(place, facts.keys), facts.coefficients, facts.role, facts.geo_mean_config)

    def record_micro_batch(self, current: _Current, index: int, calls: Any, loss_function: Any, args: tuple,
                           kwargs: dict, output: Any) -> None:  # fmt: skip
        """``calls`` None: the watch could not start, so the call stays missing (counted, not captured)."""
        data = inspect.signature(loss_function).bind(*args, **kwargs).arguments.get("data")
        if data is None or ROW_FIELD not in data.keys():
            current.log.broken_reason = "a micro-batch carried no row ids"
            return
        if calls is None:
            return
        loss, metrics = output
        prefix = CRITIC_PREFIX if current.role == CRITIC else "actor/"
        # geo_mean's pg term never passes `agg_loss`: at verl's defaults (no entropy, no KL) nothing does, so the
        # rows are built on the batch's own mask and the rebuilt term is the whole loss.
        fields = read_geo_mean_fields(data) if current.geo_mean_config is not None else None
        captured = summarize_loss_call(calls, rows=data[ROW_FIELD], coefficients=current.coefficients,
                                       metrics=metrics or {}, loss=loss, prefix=prefix,
                                       mask=fields["response_mask"] if fields is not None else None)  # fmt: skip
        if captured is not None and fields is not None:
            model_output = inspect.signature(loss_function).bind(*args, **kwargs).arguments.get("model_output")
            add_geo_mean_pg(captured, current.geo_mean_config, data, model_output, fields)  # raises: stays missing
        if captured is not None:
            current.log.add(index, captured)

    def finish_update(self, worker: Any, log: UpdateLog, output: Any) -> None:
        if log.broken_reason is not None:
            self._warn_once(log.broken_reason, f"Probe sends no per-sample training metrics for a verl update: "
                                               f"{log.broken_reason}.")  # fmt: skip
            return
        if not log.calls:
            return
        metrics = _get_metrics(output)
        optimizer_step = get_optimizer_step(getattr(worker.engine, "optimizer", None))
        role = CRITIC if is_critic(worker) else ACTOR
        rows = log.build_rows(optimizer_step=optimizer_step)
        grad_norm = to_float(metrics.get("grad_norm"))
        records = log.build_records(
            grad_norm=grad_norm, metrics={f"{role}/grad_norm": grad_norm, f"{role}/lr": to_float(metrics.get("lr"))},
            optimizer_step=optimizer_step, reported_loss=to_float(metrics.get("loss")),
        )  # fmt: skip
        if role == CRITIC:  # its updates sit beside the actor's at the same step and ordinals (D4)
            rows = [{**row, "role": CRITIC} for row in rows]
            records = [{**record, "role": CRITIC} for record in records]
        self.get_sender(role).send(log.place.step, log.place.update, rows, records)

    def get_sender(self, role: str) -> PointsSender:
        return self.critic_sender if role == CRITIC else self.sender

    def _warn_once(self, reason: str, message: str) -> None:
        if reason not in self._warned:
            self._warned.add(reason)
            logger.info(message)

    def _send_critic_plan(self, worker: Any, rank: int | None, reason: str | None) -> None:
        """The critic's first rank declares the critic's own keys once (D4): their rollups, or why none is sent."""
        if rank != 0 or self._has_declared_critic:
            return
        self._has_declared_critic = True
        self.critic_sender.start(f"{CRITIC_PRODUCER_PREFIX}{rank}")
        self.critic_sender.send_plan(build_critic_plan(getattr(worker, "engine_config", None), reason))

    def _send_stop_reason(self, rank: int | None, reason: str) -> None:
        """The worker group's first process says once, under `*`, why this run records no per-sample training metrics,
        so every key's read answers "unsupported" with it (no other process joins the run). Never for a critic (its
        value loss says nothing about the policy's); an actor's unproven loss or mode is the run's."""
        if rank != 0 or self._has_declared_stop:
            return
        self._has_declared_stop = True
        self.sender.start(f"{PRODUCER_PREFIX}{rank}")
        self.sender.send_plan({"unsupported": {"*": f"verl: {reason}"}})


def get_unsupported_reason(worker: Any) -> str | None:
    """Why this worker's update path is one the hook does not support (`plan.UNSUPPORTED` says why each is out): an
    actor's loss must be verl's `ppo_loss` (or score centering's or distillation's, `ACTOR_LOSSES`) in a proven mode
    (`plan.LOSS_MODES`, `plan.DISTILLATION_MODES`), a critic's verl's `value_loss`."""
    loss_function = getattr(worker.loss_fn, HOOKED_LOSS, worker.loss_fn)
    wanted = "value_loss" if is_critic(worker) else "ppo_loss"
    expected = getattr(sys.modules.get(LOSSES_MODULE), wanted, None)
    if expected is None:
        return f"verl's losses module ({LOSSES_MODULE}) is not loaded, so its {wanted} cannot be recognised"
    accepted = [expected] if wanted == "value_loss" else [
        found for module, name in ACTOR_LOSSES.items() if (found := getattr(sys.modules.get(module), name, None))]
    if not any(getattr(loss_function, "func", None) is loss for loss in accepted):
        func = getattr(loss_function, "func", loss_function)
        name = getattr(func, "__qualname__", None) or type(func).__name__
        found = ".".join(filter(None, (getattr(func, "__module__", None), name)))
        return f"its loss is {found}, not verl's {wanted}"
    mode = get_loss_mode(_get_loss_config(loss_function))
    if wanted == "ppo_loss" and mode not in SUPPORTED_LOSS_MODES:
        return f"policy loss mode {mode!r}"
    distillation = _get_distillation_settings(loss_function)
    if distillation is not None:
        reason = get_distillation_reason(distillation)
        if reason is not None:
            return reason
    engine_module = type(worker.engine).__module__
    if "megatron" in engine_module:  # only the configurations a GPU proof ran (D18), read off this worker at run time
        reason = get_megatron_reason(getattr(worker, "engine_config", None), getattr(worker, "model_config", None),
                                     CRITIC if wanted == "value_loss" else ACTOR,
                                     read_data_parallel_size(worker.engine))  # fmt: skip
        return None if reason is None else f"the Megatron engine: {reason}"
    if "fsdp" not in engine_module:
        return f"engine {type(worker.engine).__name__} (only the FSDP engine is proven)"
    return get_critic_path_reason(worker) if wanted == "value_loss" else None


def get_distillation_reason(settings: Any) -> str | None:
    """Why this distillation loss sends nothing: a `loss_mode` or a policy-gradient mode no run proved."""
    mode = str(getattr(settings, "loss_mode", "k3"))
    if mode not in DISTILLATION_MODES:
        return f"distillation loss mode {mode!r}"
    policy_mode = str(getattr(settings, "policy_loss_mode", "vanilla"))
    if getattr(settings, "use_policy_gradient", False) and policy_mode not in DISTILLATION_POLICY_MODES:
        return f"distillation policy loss mode {policy_mode!r} (use_policy_gradient)"
    return None


def get_actor_coefficients(loss_function: Any) -> dict[str, float]:
    """How each actor term enters the loss (`losses.py:160-178`); under distillation (`distillation_ppo_loss`,
    `distillation/losses.py:241-259`) its term is x `distillation_loss_coef` with task rewards, else x 1, and the
    policy terms are zeroed without task rewards (computed under `use_policy_gradient`, else not at all)."""
    config = _get_loss_config(loss_function)
    found = {"actor/pg_loss": 1.0, "actor/entropy_loss": -float(getattr(config, "entropy_coeff", 0.0))}
    if getattr(config, "use_kl_loss", False):
        found["actor/kl_loss"] = float(config.kl_loss_coef)
    settings = _get_distillation_settings(loss_function)
    if settings is None:
        return found
    if not settings.use_task_rewards:
        found = dict.fromkeys(found, 0.0) if settings.use_policy_gradient else {}
    found["actor/distillation/loss"] = float(settings.distillation_loss_coef) if settings.use_task_rewards else 1.0
    return found


def is_logits_processor_call(signature: inspect.Signature | None, args: tuple, kwargs: dict) -> bool:
    """A call the engine makes inside the forward with `student_logits` (`LOGITS_PROCESSOR_ARGUMENT`)."""
    if kwargs.get(LOGITS_PROCESSOR_ARGUMENT) is not None:
        return True
    if signature is None or not args:
        return False
    try:
        return signature.bind_partial(*args, **kwargs).arguments.get(LOGITS_PROCESSOR_ARGUMENT) is not None
    except TypeError:  # not a call this loss takes: verl raises it itself
        return False


def get_critic_path_reason(worker: Any) -> str | None:
    """The actor's `use_remove_padding`, Ulysses and LoRA paths are GPU-proven (`gpu/verl/RESULT.md`: their rows
    rebuild every micro-batch and verl's series, training bitwise unchanged); the critic ran only without them."""
    model_config = getattr(worker, "model_config", None)
    if hasattr(model_config, "get") and model_config.get("use_remove_padding", False):
        return "use_remove_padding (sequence packing) on the critic (proven on GPU for the actor only)"
    if int(getattr(worker.engine_config, "ulysses_sequence_parallel_size", 1) or 1) > 1:
        return "Ulysses sequence parallelism on the critic (proven on GPU for the actor only)"
    if hasattr(model_config, "get") and int(model_config.get("lora_rank", 0) or 0) > 0:
        return "LoRA (lora_rank > 0) on the critic (proven on GPU for the actor only)"
    return None


def get_recording_place(engine: Any) -> tuple[int, int] | None:
    """(data-parallel rank, data-parallel size) when this rank records, else None. Under Ulysses the ranks of one
    sequence-parallel group hold shards of the same rows and verl gathers the loss's outputs onto one of them
    (`is_mp_src_rank_with_outputs`, `transformer_impl.py:196-201`): only that rank sends, so each data-parallel rank
    sends once, and `actor/loss` folds over the data-parallel size verl averages it over (`engine_workers.py:230-233`),
    never the world size (`gpu/verl/RESULT.md`: under sp 2 the world size halved it)."""
    if not engine.is_mp_src_rank_with_outputs():
        return None
    return int(engine.get_data_parallel_rank()), int(engine.get_data_parallel_size())


def read_data_parallel_size(engine: Any) -> int | None:
    """The engine's data-parallel size (Megatron: `mpu.get_data_parallel_world_size()`, `transformer_impl.py:737-741`;
    the step gate runs after `initialize`), None when it cannot be read: the gate then refuses (D18 fails closed)."""
    try:
        return int(engine.get_data_parallel_size())
    except Exception:  # noqa: BLE001 -- not initialised, or not an engine verl's base class describes
        return None


def get_loss_mode(config: Any) -> str:
    """The actor's `policy_loss.loss_mode` (verl's default: vanilla)."""
    policy_loss = getattr(config, "policy_loss", None)
    return str(policy_loss.get("loss_mode", "vanilla") if hasattr(policy_loss, "get") else "vanilla")


def _get_loss_config(loss_function: Any) -> Any:
    loss_function = getattr(loss_function, HOOKED_LOSS, loss_function)
    return (getattr(loss_function, "keywords", None) or {}).get("config")


def _get_distillation_settings(loss_function: Any) -> Any:
    """`distillation_config.distillation_loss` of a `distillation_ppo_loss` partial, else None."""
    loss_function = getattr(loss_function, HOOKED_LOSS, loss_function)
    config = (getattr(loss_function, "keywords", None) or {}).get("distillation_config")
    return getattr(config, "distillation_loss", None)


def _get_signature(function: Any) -> inspect.Signature | None:
    try:
        return inspect.signature(function)
    except (TypeError, ValueError):  # a callable with no signature: its calls are taken by keyword only
        return None


def _take_non_tensor(data: Any, name: str) -> Any:
    """A non-tensor field taken off the batch (verl's `tu.pop`), so it never travels on to the engine. A V1 critic's
    worker is handed the `KVBatchMeta` itself (`v1/trainer_base.py:1831`; `tqbridge` turns its `extra_info` into the
    TensorDict's non-tensor fields later): the field is taken off its `extra_info`."""
    extra = getattr(data, "extra_info", None)
    if isinstance(extra, dict) and not callable(getattr(data, "keys", None)):
        return extra.pop(name, None)
    try:
        keys = data.keys()
    except Exception:  # noqa: BLE001 -- not a TensorDict: nothing stamped
        return None
    if name not in keys:
        return None
    value = data.pop(name)
    return getattr(value, "data", value)


def _get_metrics(output: Any) -> dict:
    if output is None:
        return {}
    try:
        metrics = output["metrics"]
    except Exception:  # noqa: BLE001 -- no metrics: nothing to read
        return {}
    metrics = getattr(metrics, "data", metrics)
    return dict(metrics) if hasattr(metrics, "items") else {}


_TRAINING: VerlTraining | None = None


def get_training() -> VerlTraining:
    global _TRAINING
    if _TRAINING is None:
        _TRAINING = VerlTraining()
    return _TRAINING


def install_worker_training() -> None:
    """Ray's setup hook (`tracking.setup_worker`): wrap `TrainingWorker` once its module loads in this worker."""
    watch_import(WORKER_MODULE, get_training().install, framework="verl")


def _get_first_rank(worker: Any) -> int | None:
    """This process's rank in its worker group (torch.distributed: one process is 0, whatever the sequence, tensor or
    pipeline parallelism), else its data-parallel rank; None when neither can be read."""
    try:
        import torch.distributed as dist

        if dist.is_available() and dist.is_initialized():
            return int(dist.get_rank())
    except Exception:  # noqa: BLE001 -- no usable torch.distributed: the engine's own rank instead
        pass
    try:
        return int(worker.engine.get_data_parallel_rank())
    except Exception:  # noqa: BLE001 -- an engine the hook does not know
        return None


def is_critic(worker: Any) -> bool:
    """A verl critic worker (by its role, never by its loss function or the reason's wording)."""
    return getattr(getattr(worker, "config", None), "model_type", None) == CRITIC_MODEL_TYPE
