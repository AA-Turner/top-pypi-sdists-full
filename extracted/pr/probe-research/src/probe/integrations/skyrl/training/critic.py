"""SkyRL's critic value loss per sample (rl-trajectory-gaps D4). The critic worker (`CriticWorkerBase`,
`worker.py:1608`) is wrapped as the policy worker is: `forward_backward` opens one rank's share of a critic update,
`_forward_backward_micro` is observed (`ppo_utils.ppo_critic_loss` reduces each row with `masked_mean(..., dim=-1)`,
then the plain mean over rows, x 0.5; `values_mean` and `values_clipfrac` are token means), `optim_step` closes it.
Sent as producer `skyrl-train-critic-<dp>`, role critic, with a plan naming only the critic's own `critic/*` keys
(never a `*` stop, never the actor's producer). Line refs are `NovaSky-AI/SkyRL@d87004689e3a`."""

from __future__ import annotations

import functools
import inspect
import logging
import threading
from dataclasses import dataclass, field
from typing import Any

from probe.generated.samples.points import Dtype, Grouping, LossRole, Reducer, hash_mask
from probe.sdk.run.samples.points import (
    MicroBatchCapture, PointsSender, RowCapture, Share, TrainingGuard, UpdateLog, UpdatePlace, copy_to_host,
    get_optimizer_step, to_float,
)

from .loss import ROW_FIELD, ReductionWatch, get_own_mask, get_row_shares
from .plan import CRITIC_PATHS_REASON, MEGATRON_REASON
from .training import (
    CRITIC_BOUNDARIES, KEYS_FIELD, PADDING_FIELD, WORKER_METHODS, WRAPPED_MARK, drop_dp_padding_rows, is_recording_rank,
)

logger = logging.getLogger(__name__)

CRITIC_PRODUCER_PREFIX = "skyrl-train-critic-"
#: SkyRL's driver logs the critic worker's metrics as `critic/<key>` (`trainer.py:1681-1683`).
LOSS, VALUES_MEAN, CLIPFRAC = "critic/critic_loss", "critic/values_mean", "critic/values_clipfrac"
WHAT = "per-sample critic metrics"
UPDATE_MEAN = [{"by": Grouping.UPDATE, "reducer": Reducer.SUM}, {"by": Grouping.STEP, "reducer": Reducer.MEAN}]


def build_critic_plan() -> dict[str, Any]:
    """Only the critic's own keys (D4): the actor's plan is never replaced, no `*`."""
    rollups = {key: {"role": LossRole.CRITIC, "levels": UPDATE_MEAN, "dtype": Dtype.BF16}
               for key in (LOSS, VALUES_MEAN, CLIPFRAC)}  # fmt: skip
    return {"sends_loss_bookkeeping": True, "rollups": rollups, "unsupported": {}}


@dataclass
class _Open:
    log: UpdateLog
    micro_weights: list = field(default_factory=list)


@dataclass
class SkyrlCriticTraining:
    """This worker process's critic recording: its own sender and each critic worker's update in progress."""

    guard: TrainingGuard = field(default_factory=lambda: TrainingGuard("SkyRL critic"))
    sender: PointsSender = field(default_factory=lambda: PointsSender("SkyRL"))
    _local: threading.local = field(default_factory=threading.local)
    #: By worker: (step, the next update's ordinal).
    _next_update: dict = field(default_factory=dict)
    _pending: dict = field(default_factory=dict)
    _warned: set = field(default_factory=set)
    _has_declared: bool = False

    def install(self, module: Any) -> bool:
        """Wrap the critic worker's methods once, all or none (as the policy worker's, `SkyrlTraining.install`)."""
        worker_class = getattr(module, "CriticWorkerBase", None)
        if not isinstance(worker_class, type) or getattr(worker_class.__dict__.get("forward_backward"), WRAPPED_MARK,
                                                         False):  # fmt: skip
            return False
        originals = {name: worker_class.__dict__.get(name) for name in WORKER_METHODS}
        missing = sorted(name for name, original in originals.items() if not callable(original))
        if missing:
            raise AttributeError(f"SkyRL's critic worker has no {', '.join(missing)}: nothing is wrapped")
        forward_backward, micro, optim_step = (originals[name] for name in WORKER_METHODS)

        @functools.wraps(forward_backward)
        def call_forward_backward(worker: Any, data: Any, *args: Any, **kwargs: Any) -> Any:
            opened = self.guard.call(WHAT, self.start_update, worker, data)
            self._local.current = opened
            try:
                output = forward_backward(worker, data, *args, **kwargs)
            finally:
                self._local.current = None
            if opened is not None:
                self._pending[id(worker)] = (opened, output)
            return output

        @functools.wraps(micro)
        def call_micro(worker: Any, *args: Any, **kwargs: Any) -> Any:
            opened = getattr(self._local, "current", None)
            if opened is None:
                return micro(worker, *args, **kwargs)
            index = opened.log.count_call()
            watch = ReductionWatch()
            calls = self.guard.call(WHAT, watch.start)
            try:
                status = micro(worker, *args, **kwargs)
            finally:
                self.guard.call(WHAT, watch.stop)
            self.guard.call(WHAT, self.record_micro_batch, opened, index, micro, worker, args, kwargs, status, calls)
            return status

        @functools.wraps(optim_step)
        def call_optim_step(worker: Any, *args: Any, **kwargs: Any) -> Any:
            grad_norm = optim_step(worker, *args, **kwargs)
            self.guard.call(WHAT, self.finish_update, worker, grad_norm)
            return grad_norm

        setattr(call_forward_backward, WRAPPED_MARK, True)
        worker_class.forward_backward = call_forward_backward
        worker_class._forward_backward_micro = call_micro
        worker_class.optim_step = call_optim_step
        return True

    def start_update(self, worker: Any, data: Any) -> _Open | None:
        metadata = getattr(data, "metadata", None) or {}
        keys = metadata.get(KEYS_FIELD)
        if keys is None or ROW_FIELD not in data or self.sender.is_disabled:
            return None
        reason = get_critic_unsupported_reason(worker)
        if reason is not None:
            if reason not in self._warned:
                self._warned.add(reason)
                logger.info("Probe records no per-sample critic metrics on this SkyRL worker: %s.", reason)
            return None
        mesh = worker.mesh_rank
        if not is_recording_rank(mesh):
            return None
        drop_dp_padding_rows(data, int(mesh.dp), int(mesh.dp_size), CRITIC_BOUNDARIES)
        step = int(metadata.get("global_step", 0))
        last_step, ordinal = self._next_update.get(id(worker), (step, 0))
        ordinal = ordinal if last_step == step else 0
        self._next_update[id(worker)] = (step, ordinal + 1)
        boundaries = metadata.get(CRITIC_BOUNDARIES) or []
        updates = int(worker.cfg.update_epochs_per_batch) * len(boundaries) if boundaries else None
        self.sender.start(f"{CRITIC_PRODUCER_PREFIX}{int(mesh.dp)}")
        if not self._has_declared and int(mesh.dp) == 0:
            self._has_declared = True
            self.sender.send_plan(build_critic_plan())
        place = UpdatePlace(step=step, update=ordinal, rank=int(mesh.dp), ranks=int(mesh.dp_size),
                            updates_in_step=updates, reduction="critic_row_mean", role=LossRole.CRITIC)  # fmt: skip
        return _Open(UpdateLog(place, list(keys)))

    def record_micro_batch(self, opened: _Open, index: int, original: Any, worker: Any, args: tuple, kwargs: dict,
                           status: Any, calls: Any) -> None:  # fmt: skip
        import torch

        bound = inspect.signature(original).bind(worker, *args, **kwargs)
        bound.apply_defaults()
        experience, weight = bound.arguments["experience"], bound.arguments.get("microbatch_weight")
        if (getattr(experience, "metadata", None) or {}).get(PADDING_FIELD):
            opened.log.add(index, MicroBatchCapture(rows=[], reported_loss=to_float(status.get("critic_loss")),
                                                    is_padding=True))  # fmt: skip
            return
        info = getattr(experience, "info", None) or {}
        if calls is None or calls.failures or ROW_FIELD not in info:
            return
        loss_call = next((c for c in calls.means if c.where == "ppo_utils" and c.dim == -1), None)
        values_call = next((c for c in calls.means if c.where == "worker" and c.dim is None), None)
        clip_call = next((c for c in calls.means if c.where == "ppo_utils" and c.dim is None), None)
        if loss_call is None:
            return
        scale = 1.0 if weight is None else float(weight)
        mask = get_own_mask(loss_call, loss_call.values)
        rows_in = mask.shape[0]
        shares = get_row_shares(lambda x: 0.5 * loss_call.reduce(x, loss_call.mask, -1).mean() * scale,
                                 loss_call.values)  # fmt: skip
        columns = [info[ROW_FIELD], mask.sum(-1), (loss_call.values.to(torch.float64) * mask).sum(-1), shares]
        named = [(key, call) for key, call in ((VALUES_MEAN, values_call), (CLIPFRAC, clip_call)) if call is not None]
        for _, call in named:
            own = get_own_mask(call, mask)
            columns += [(call.values.to(torch.float64) * own).sum(-1), own.sum(-1)]
        host = copy_to_host(columns, mask > 0, [status.get("critic_loss")])
        totals = {key: sum(r[4 + 2 * j + 1] for r in host.rows) for j, (key, _) in enumerate(named)}
        captured = []
        for stats, flags in zip(host.rows, host.flags, strict=True):
            row_id, count, loss_sum, contribution = stats[:4]
            values = {LOSS: 0.5 * loss_sum / count if count else None}
            bases = {LOSS: (scale / rows_in, Share.CALL_MEAN)}
            for j, (key, _) in enumerate(named):
                own_sum, own_count = stats[4 + 2 * j], stats[5 + 2 * j]
                values[key] = own_sum / own_count if own_count else None
                bases[key] = (own_count / totals[key] if totals[key] else 0.0, Share.CALL_MEAN)
            captured.append(RowCapture(row=int(row_id), token_count=int(round(count)), mask_sha256=hash_mask(flags),
                                       loss_sum=0.5 * loss_sum, normalizer=float(count * rows_in) / scale,
                                       contribution=contribution, contribution_terms={LOSS: contribution},
                                       values=values, bases=bases))  # fmt: skip
        dtype = Dtype.BF16 if loss_call.values.dtype == torch.bfloat16 else Dtype.FP32
        opened.log.add(index, MicroBatchCapture(rows=captured, reported_loss=host.scalars[0], dtype=dtype))

    def finish_update(self, worker: Any, grad_norm: Any) -> None:
        opened, output = self._pending.pop(id(worker), (None, None))
        if opened is None or not opened.log.calls or len(opened.log.micro_batches) != opened.log.calls:
            return
        optimizer_step = get_optimizer_step(getattr(worker, "optimizer", None))
        rows = opened.log.build_rows(optimizer_step=optimizer_step)
        norm = to_float(grad_norm)
        records = opened.log.build_records(grad_norm=norm, metrics={"critic/grad_norm": norm},
                                           optimizer_step=optimizer_step,
                                           reported_loss=to_float((getattr(output, "metrics", None) or {})
                                                                  .get("critic_loss")))  # fmt: skip
        self.sender.send(opened.log.place.step, opened.log.place.update, rows, records)


def get_critic_unsupported_reason(worker: Any) -> str | None:
    """Why this critic worker sends no rows: Megatron (no `_forward_backward_micro`), or packing / sequence parallel
    (proven for the policy only)."""
    if "fsdp" not in type(worker).__module__:
        return MEGATRON_REASON
    mesh = worker.mesh_rank
    if getattr(worker.cfg, "remove_microbatch_padding", False) or int(mesh.world_size) != int(mesh.dp_size):
        return CRITIC_PATHS_REASON
    return None


_CRITIC: SkyrlCriticTraining | None = None


def get_critic_training() -> SkyrlCriticTraining:
    global _CRITIC
    if _CRITIC is None:
        _CRITIC = SkyrlCriticTraining()
    return _CRITIC
