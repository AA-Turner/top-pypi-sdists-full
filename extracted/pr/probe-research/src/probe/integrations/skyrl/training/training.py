"""SkyRL's policy worker's per-sample training metrics (plan rl-trajectory-metrics T3). In each policy worker process
(installed by the job's Ray setup hook, `setup.py`) four methods are wrapped on their classes: the batch iterator's
`batch_to_experience` (the driver's row ids into `Experience.info`), `forward_backward` (one rank's share of an
optimizer update), `_forward_backward_micro` (each micro-batch's loss, observed) and `optim_step` (the update ends:
gradient norm, applied, the optimizer's own step). Sent as producer `skyrl-train-<dp rank>` from a background thread.
Every wrap runs SkyRL's own function first and returns its result untouched; Probe's part is guarded. Line refs are
`NovaSky-AI/SkyRL@d87004689e3a`. Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

import functools
import inspect
import logging
import threading
from dataclasses import dataclass, field
from typing import Any

from probe.sdk.run.samples.points import (
    MicroBatchCapture, PointsSender, TrainingGuard, UpdateLog, UpdatePlace, get_optimizer_step, to_float, watch_import,
)

from .loss import ROW_FIELD, SCALE_FIELD, WORKER_MODULE, ReductionWatch, summarize_micro_call
from .plan import MEGATRON_REASON, get_loss_reason, get_unsupported_keys

logger = logging.getLogger(__name__)

PRODUCER_PREFIX = "skyrl-train-"
#: What the driver puts in the batch's metadata (`driver.py`): each row id's sample key, the updates in the step.
KEYS_FIELD = "probe_sample_keys"
UPDATES_FIELD = "probe_updates_in_step"
#: SkyRL's own mark on a token-based iterator's padding micro-batch (`worker_utils.py:358`).
PADDING_FIELD = "is_padding_batch"
#: The driver's mini-batch `(start, end)` pairs, kept on every chunk's metadata (`trainer.py:1032-1041`).
POLICY_BOUNDARIES, CRITIC_BOUNDARIES = "policy_mini_batch_boundaries", "critic_mini_batch_boundaries"
WRAPPED_MARK = "__probe_skyrl_training__"
#: The methods `install` wraps, all or none.
WORKER_METHODS = ("forward_backward", "_forward_backward_micro", "optim_step")
WHAT = "per-sample training metrics"


@dataclass
class _Step:
    step: int
    next_update: int = 0


@dataclass
class _Current:
    log: UpdateLog
    kl_coef: float
    entropy_coef: float
    unsupported: tuple[str, ...] = ()
    #: Every `Experience` the batch iterator built in this update, in order (the Megatron worker's micro-batch
    #: dicts drop `Experience.info`, `megatron.py`); None: not kept.
    experiences: list | None = None


@dataclass
class SkyrlTraining:
    """This worker process's recording: its sender (joining the run in the background from the first update) and each
    worker's update in progress."""

    guard: TrainingGuard = field(default_factory=lambda: TrainingGuard("SkyRL"))
    sender: PointsSender = field(default_factory=lambda: PointsSender("SkyRL"))
    _steps: dict[int, _Step] = field(default_factory=dict)
    _pending: dict[int, UpdateLog] = field(default_factory=dict)
    _pending_outputs: dict[int, Any] = field(default_factory=dict)
    _local: threading.local = field(default_factory=threading.local)
    _warned: set[str] = field(default_factory=set)
    _has_declared_stop: bool = False

    def install(self, module: Any) -> bool:
        """Wrap the policy worker's methods and the iterator's `batch_to_experience`, once, all or none."""
        worker_class = getattr(module, "PolicyWorkerBase", None)
        iterator_class = getattr(module, "BaseBatchIterator", None)
        if not isinstance(worker_class, type) or getattr(worker_class.__dict__.get("forward_backward"), WRAPPED_MARK,
                                                         False):  # fmt: skip
            return False
        originals = {name: worker_class.__dict__.get(name) for name in WORKER_METHODS}
        to_experience = getattr(iterator_class.__dict__.get("batch_to_experience"), "__func__", None) \
            if isinstance(iterator_class, type) else None  # fmt: skip
        missing = sorted(name for name, original in originals.items() if not callable(original))
        if not callable(to_experience):
            missing.append("BaseBatchIterator.batch_to_experience")
        if missing:
            raise AttributeError(f"SkyRL's policy worker has no {', '.join(missing)}: nothing is wrapped")
        iterator_class.batch_to_experience = staticmethod(self._wrap_experience(to_experience))
        worker_class.forward_backward = self._wrap_update(originals["forward_backward"])
        worker_class._forward_backward_micro = self._wrap_micro(originals["_forward_backward_micro"])
        worker_class.optim_step = self._wrap_optim_step(originals["optim_step"])
        return True

    # -- the wraps -----------------------------------------------------------------------------------------
    def _wrap_experience(self, original: Any) -> Any:
        @functools.wraps(original)
        def call_batch_to_experience(*args: Any, **kwargs: Any) -> Any:
            experience = original(*args, **kwargs)
            self.guard.call(WHAT, _copy_row_fields, args, kwargs, experience)
            current = getattr(self._local, "current", None)
            if current is not None and current.experiences is not None:
                current.experiences.append(experience)
            return experience

        return call_batch_to_experience

    def _wrap_update(self, original: Any, *, should_keep_experiences: bool = False) -> Any:
        """``should_keep_experiences``: the update keeps every `Experience` it builds, in order (the Megatron worker)."""

        @functools.wraps(original)
        def call_forward_backward(worker: Any, *args: Any, **kwargs: Any) -> Any:
            current = self.guard.call(WHAT, self.start_update, worker, original, args, kwargs)
            if current is None:
                return original(worker, *args, **kwargs)
            if should_keep_experiences:
                current.experiences = []
            self._local.current = current
            try:
                output = original(worker, *args, **kwargs)
            finally:
                self._local.current = None
            self._pending[id(worker)] = current.log
            self._pending_outputs[id(worker)] = output
            return output

        setattr(call_forward_backward, WRAPPED_MARK, True)
        return call_forward_backward

    def _wrap_micro(self, original: Any) -> Any:
        @functools.wraps(original)
        def call_forward_backward_micro(worker: Any, *args: Any, **kwargs: Any) -> Any:
            current = getattr(self._local, "current", None)
            if current is None:  # outside an update the hook opened (eval, SFT, a Tinker loss): nothing
                return original(worker, *args, **kwargs)
            index = current.log.count_call()  # counted before anything can fail: a lost call reads missing
            watch = ReductionWatch()
            calls = self.guard.call(WHAT, watch.start)
            try:
                status = original(worker, *args, **kwargs)
            finally:
                self.guard.call(WHAT, watch.stop)
            self.guard.call(WHAT, self.record_micro_batch, current, index, original, worker, args, kwargs, status, calls)
            return status

        return call_forward_backward_micro

    def _wrap_optim_step(self, original: Any) -> Any:
        @functools.wraps(original)
        def call_optim_step(worker: Any, *args: Any, **kwargs: Any) -> Any:
            grad_norm = original(worker, *args, **kwargs)
            self.guard.call(WHAT, self.finish_update, worker, grad_norm)
            return grad_norm

        return call_optim_step

    # -- an update -------------------------------------------------------------------------------------------
    def start_update(self, worker: Any, original: Any, args: tuple, kwargs: dict) -> _Current | None:
        arguments = inspect.signature(original).bind(worker, *args, **kwargs).arguments
        metadata = getattr(arguments.get("data"), "metadata", None) or {}
        keys = metadata.get(KEYS_FIELD)
        if keys is None or self.sender.is_disabled or arguments.get("loss_fn") is not None:
            return None  # not a stamped RL step, or a caller's own loss (Tinker API, SFT)
        reason = get_unsupported_reason(worker)
        if reason is not None:
            self._warn_once(reason, f"Probe records no per-sample training metrics on this SkyRL worker: {reason}.")
            if not self._has_declared_stop:
                self.guard.call(WHAT, self._send_stop_reason, _get_first_rank(worker), reason)
            return None
        mesh = worker.mesh_rank
        if not is_recording_rank(mesh):
            return None
        drop_dp_padding_rows(arguments.get("data"), int(mesh.dp), int(mesh.dp_size), POLICY_BOUNDARIES)
        step_number = int(metadata.get("global_step", 0))
        step = self._steps.get(id(worker))
        if step is None or step.step != step_number:
            step = self._steps[id(worker)] = _Step(step_number)
        algorithm = worker.cfg.algorithm
        self.sender.start(f"{PRODUCER_PREFIX}{int(mesh.dp)}")  # joins in the background while the update trains
        place = UpdatePlace(step=step_number, update=step.next_update, rank=int(mesh.dp), ranks=int(mesh.dp_size),
                            updates_in_step=_to_int(metadata.get(UPDATES_FIELD)),
                            reduction=str(algorithm.loss_reduction))  # fmt: skip
        step.next_update += 1
        return _Current(
            UpdateLog(place, list(keys)),
            kl_coef=float(algorithm.kl_loss_coef) if algorithm.use_kl_loss else 0.0,
            entropy_coef=float(algorithm.entropy_loss_coef) if algorithm.use_entropy_loss else 0.0,
            unsupported=get_unsupported_keys(str(algorithm.policy_loss_type)),
        )

    def record_micro_batch(self, current: _Current, index: int, original: Any, worker: Any, args: tuple,
                           kwargs: dict, status: Any, calls: Any) -> None:  # fmt: skip
        """``calls`` None: the watch could not start, so the call stays missing (counted, not captured)."""
        arguments = inspect.signature(original).bind(worker, *args, **kwargs).arguments
        experience = arguments["experience"]
        if (getattr(experience, "metadata", None) or {}).get(PADDING_FIELD):  # no rows, counted in the means
            current.log.add(index, MicroBatchCapture(rows=[], reported_loss=to_float(status.get("final_loss")),
                                                     is_padding=True))  # fmt: skip
            return
        info = getattr(experience, "info", None) or {}
        if ROW_FIELD not in info:
            current.log.broken_reason = "a micro-batch carried no row ids"
            return
        if calls is None:
            return
        captured = summarize_micro_call(
            calls, rows=info[ROW_FIELD], scales=info.get(SCALE_FIELD), status=status,
            micro_weight=float(arguments["microbatch_weight"]), ranks=int(worker.mesh_rank.dp_size),
            kl_coef=current.kl_coef, entropy_coef=current.entropy_coef, unsupported=current.unsupported,
        )  # fmt: skip
        if captured is not None:
            current.log.add(index, captured)

    def finish_update(self, worker: Any, grad_norm: Any) -> None:
        log = self._pending.pop(id(worker), None)
        output = self._pending_outputs.pop(id(worker), None)
        if log is None:
            return
        if log.broken_reason is not None:
            self._warn_once(log.broken_reason, f"Probe sends no per-sample training metrics for a SkyRL update: "
                                               f"{log.broken_reason}.")  # fmt: skip
            return
        if not log.calls:
            return
        metrics = dict(getattr(output, "metrics", None) or {})
        optimizer_step = get_optimizer_step(getattr(worker, "optimizer", None))
        rows = log.build_rows(optimizer_step=optimizer_step)
        norm = to_float(grad_norm)
        records = log.build_records(
            grad_norm=norm, metrics={"policy/grad_norm": norm, "policy/policy_lr": to_float(metrics.get("policy_lr"))},
            optimizer_step=optimizer_step, reported_loss=to_float(metrics.get("final_loss")),
        )  # fmt: skip
        self.sender.send(log.place.step, log.place.update, rows, records)

    def _warn_once(self, reason: str, message: str) -> None:
        if reason not in self._warned:
            self._warned.add(reason)
            logger.info(message)

    def _send_stop_reason(self, rank: int | None, reason: str) -> None:
        """The worker group's first process says once, under `*`, why this run records no per-sample training metrics,
        so every key's read answers "unsupported" with it (no other process joins the run)."""
        if rank != 0 or self._has_declared_stop:
            return
        self._has_declared_stop = True
        self.sender.start(f"{PRODUCER_PREFIX}{rank}")
        self.sender.send_plan({"unsupported": {"*": f"SkyRL: {reason}"}})


def get_unsupported_reason(worker: Any) -> str | None:
    """Why this worker's path sends no rows (`plan.UNSUPPORTED`); None when it is proven. Off-policy correction, score
    centering, step-wise rows, packing and Ulysses sequence parallelism are (rl-trajectory-gaps T2 / T3)."""
    reason = get_loss_reason(str(worker.cfg.algorithm.policy_loss_type))
    if reason is not None:
        return reason
    module = type(worker).__module__
    if "megatron" in module:
        from .megatron import get_megatron_reason

        return get_megatron_reason(worker)
    if "fsdp" not in module:
        return MEGATRON_REASON
    return None


def is_recording_rank(mesh: Any) -> bool:
    """One process per data-parallel rank records (SP 0, TP 0, the last PP stage), else rows repeat: SkyRL gathers
    sequence-parallel outputs back to canonical rows on every SP rank before the loss (`model_wrapper.py:456-466`),
    and every TP rank of a stage holds the same loss, which only the last PP stage computes. SkyRL's own
    `MeshRank.is_collection_dp_rank` (`dispatch.py:35-42`) answers when it has one; the copy below is its rule."""
    own = getattr(mesh, "is_collection_dp_rank", None)
    if callable(own):
        return bool(own())
    sp, tp, pp = int(getattr(mesh, "sp", 0) or 0), int(getattr(mesh, "tp", 0) or 0), int(getattr(mesh, "pp", 0) or 0)
    pp_size = int(getattr(mesh, "pp_size", 1) or 1)
    return sp == 0 and tp == 0 and pp == pp_size - 1


def drop_dp_padding_rows(data: Any, dp: int, dp_size: int, boundaries_key: str) -> None:
    """`MeshDispatch.stage_chunks` pads a mini-batch to a multiple of dp with copies of its row 0, Probe's row id
    included, and only when that mini-batch needs it (`dispatch.py:153-155`, `training_batch.py:701-705`). The padding
    is the mini-batch's tail: global position (dp x rows + local) >= its real size `e - s`, where `(s, e)` is the
    mini-batch in `metadata[boundaries_key]` holding this chunk's first row id (a padding copy holds `s` too). Those
    ids become -1 in a new column of Probe's own (never SkyRL's tensors, never the received one written), so they are
    never named. `metadata["pad_size"]` is not read: `convert_to_training_input` sets it for the whole batch
    (`trainer.py:1073-1074`) and slicing keeps it on a mini-batch that was never padded (`training_batch.py:465`)."""
    import torch

    metadata = getattr(data, "metadata", None) or {}
    if ROW_FIELD not in data or not len(data):
        return
    column = data[ROW_FIELD]
    first = int(column[0])
    size = next((int(e) - int(s) for s, e in metadata.get(boundaries_key) or () if int(s) <= first < int(e)), None)
    rows = len(data)
    if size is None or dp_size * rows <= size:
        return
    positions = dp * rows + torch.arange(rows, device=column.device)
    data[ROW_FIELD] = torch.where(positions >= size, torch.full_like(column, -1), column)


def _copy_row_fields(args: tuple, kwargs: dict, experience: Any) -> None:
    """The driver's columns into `Experience.info`, SkyRL's slot for per-micro-batch extras (it drops unknown
    fields, `worker_utils.py:166`)."""
    batch = kwargs.get("batch", args[0] if args else None)
    for name in (ROW_FIELD, SCALE_FIELD):
        value = batch.get(name) if hasattr(batch, "get") else None
        if value is not None:
            experience.info[name] = value


def _to_int(value: Any) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


_TRAINING: SkyrlTraining | None = None


def get_training() -> SkyrlTraining:
    global _TRAINING
    if _TRAINING is None:
        _TRAINING = SkyrlTraining()
    return _TRAINING


def install_worker_training() -> None:
    """In a Ray worker (the job's setup hook): wrap SkyRL's policy and critic workers once their module loads here."""
    from .critic import get_critic_training

    def install_workers(module: Any) -> bool:
        """Each worker's wraps on their own: a critic SkyRL changed never costs the policy's rows (the first failure is
        raised after both were tried, for `watch_import` to log). A policy worker SkyRL changed costs the critic's rows
        too: only the policy's install wraps `batch_to_experience`, which stamps the rows both read."""
        results, errors = [], []
        for training in (get_training(), get_critic_training()):
            try:
                results.append(training.install(module))
            except AttributeError as exc:
                results.append(False)
                errors.append(exc)
        if errors:
            raise errors[0]
        return results[0]

    watch_import(WORKER_MODULE, install_workers, framework="SkyRL")

    def install_megatron(module: Any) -> bool:
        from .megatron import get_megatron_training

        return get_megatron_training(get_training()).install(module)

    from .megatron import MEGATRON_WORKER_MODULE

    watch_import(MEGATRON_WORKER_MODULE, install_megatron, framework="SkyRL")


def _get_first_rank(worker: Any) -> int | None:
    """This process's rank in its worker group (torch.distributed: one process is 0, whatever the sequence, tensor or
    pipeline parallelism), else its data-parallel rank; None when neither can be read."""
    try:
        import torch.distributed as dist

        if dist.is_available() and dist.is_initialized():
            return int(dist.get_rank())
        return int(worker.mesh_rank.dp)
    except Exception:  # noqa: BLE001 -- a worker the hook does not know
        return None
