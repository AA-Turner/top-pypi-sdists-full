"""SkyRL's Megatron policy worker's per-sample training metrics (rl-trajectory-gaps T12, D19). `MegatronPolicyWorkerBase`
overrides `forward_backward` and `optim_step` and never calls `_forward_backward_micro`, the FSDP worker's micro-batch
door (`training.py`): it builds its own micro-batch dicts from the batch iterator's `Experience`s, one dict per
`Experience`, in order, without `Experience.info` (Probe's row ids with it, `megatron_worker.py:1462-1497`), and runs
them through `MegatronModelWrapper.forward_backward_mini_batch`, whose `loss_func` calls the policy loss inside
Megatron's pipeline schedule (`megatron_model_wrapper.py:760`, `:970`).

Here, on the classes, once: `forward_backward` opens one rank's share of an update as the FSDP worker's does (same
`SkyrlTraining.start_update` / `finish_update`) and keeps each `Experience` the iterator builds; `forward_backward_mini_batch`
puts each micro-batch's row ids and scales into its own dict (padded rows -1) for the call, and the schedule
`get_forward_backward_func` returns while it runs wraps `forward_step`, so each `loss_func` it hands Megatron is observed
keyed by the `data` it was bound to (the device copy of that dict, every key kept, `megatron_model_wrapper.py:158`,
`:1410`); `optim_step` closes the update. Only TP 0 of the last pipeline stage, context-parallel rank 0, records
(`training.is_recording_rank`): there the loss is the whole micro-batch's (log-probs and entropy are reduced over the
vocabulary shards before it). No collective is added (D15). Line refs are `NovaSky-AI/SkyRL@d87004689e3a`."""

from __future__ import annotations

import functools
import sys
import threading
from typing import Any

from probe.sdk.run.samples.points import MicroBatchCapture, to_float

from .loss import ROW_FIELD, SCALE_FIELD, ReductionWatch, summarize_micro_call
from .plan import MEGATRON_PROVEN, MEGATRON_PROVEN_DATA_PARALLEL, MEGATRON_REASONS
from .training import WHAT, WORKER_METHODS, WRAPPED_MARK, SkyrlTraining, _Current

MEGATRON_WORKER_MODULE = "skyrl.backends.skyrl_train.workers.megatron.megatron_worker"
MEGATRON_WRAPPER_MODULE = "skyrl.backends.skyrl_train.workers.megatron.megatron_model_wrapper"
#: SkyRL's own keys on a micro-batch dict (`megatron_worker.py:1479-1505`).
PADDING_KEY, SUB_SEQUENCES_KEY, REAL_MICRO_BATCHES_KEY = "is_padding_batch", "sub_seq_lengths", "num_real_microbatches"


class SkyrlMegatronTraining:
    """The Megatron worker's wraps, recording through the policy's `SkyrlTraining` (one sender, one producer per
    data-parallel rank, `skyrl-train-<dp>`)."""

    def __init__(self, training: SkyrlTraining) -> None:
        self.training = training
        #: The update a `forward_backward_mini_batch` call is filling, for the schedule it asks for (per thread).
        self._local = threading.local()

    def install(self, module: Any) -> bool:
        """Wrap `MegatronPolicyWorkerBase.forward_backward` / `optim_step`, `MegatronModelWrapper.
        forward_backward_mini_batch` and the wrapper module's `get_forward_backward_func`, once, all or none."""
        worker_class = getattr(module, "MegatronPolicyWorkerBase", None)
        wrapper_module = sys.modules.get(MEGATRON_WRAPPER_MODULE)
        wrapper_class = getattr(wrapper_module, "MegatronModelWrapper", None)
        if not isinstance(worker_class, type) or getattr(worker_class.__dict__.get("forward_backward"), WRAPPED_MARK,
                                                         False):  # fmt: skip
            return False
        originals = {name: worker_class.__dict__.get(name) for name in WORKER_METHODS if name != "_forward_backward_micro"}
        mini_batch = wrapper_class.__dict__.get("forward_backward_mini_batch") if isinstance(wrapper_class, type) \
            else None  # fmt: skip
        get_schedule = getattr(wrapper_module, "get_forward_backward_func", None)
        missing = sorted(f"MegatronPolicyWorkerBase.{name}" for name, original in originals.items()
                         if not callable(original))  # fmt: skip
        missing += [] if callable(mini_batch) else ["MegatronModelWrapper.forward_backward_mini_batch"]
        missing += [] if callable(get_schedule) else ["megatron_model_wrapper.get_forward_backward_func"]
        if missing:
            raise AttributeError(f"SkyRL's Megatron worker has no {', '.join(missing)}: nothing is wrapped")
        training = self.training
        worker_class.forward_backward = training._wrap_update(originals["forward_backward"], should_keep_experiences=True)
        worker_class.optim_step = training._wrap_optim_step(originals["optim_step"])
        wrapper_class.forward_backward_mini_batch = self._wrap_mini_batch(mini_batch)
        wrapper_module.get_forward_backward_func = self._wrap_get_schedule(get_schedule)
        return True

    # -- the wraps -----------------------------------------------------------------------------------------------
    def _wrap_mini_batch(self, original: Any) -> Any:
        @functools.wraps(original)
        def call_forward_backward_mini_batch(model: Any, micro_batches: Any, *args: Any, **kwargs: Any) -> Any:
            current = getattr(self.training._local, "current", None)
            if current is None or current.experiences is None or kwargs.get("forward_only"):
                return original(model, micro_batches, *args, **kwargs)  # outside an update the hook opened
            stamped = self.training.guard.call(WHAT, stamp_micro_batches, current, micro_batches)
            self._local.current = current if stamped else None
            try:
                return original(model, micro_batches, *args, **kwargs)
            finally:
                self._local.current = None
                # Every exit, a partial stamp's keys too.
                self.training.guard.call(WHAT, clear_micro_batches, micro_batches)

        return call_forward_backward_mini_batch

    def _wrap_get_schedule(self, original: Any) -> Any:
        @functools.wraps(original)
        def get_forward_backward_func(*args: Any, **kwargs: Any) -> Any:
            schedule = original(*args, **kwargs)
            current = getattr(self._local, "current", None)
            return schedule if current is None else self._wrap_schedule(schedule, current)

        return get_forward_backward_func

    def _wrap_schedule(self, schedule: Any, current: _Current) -> Any:
        @functools.wraps(schedule)
        def call_schedule(*args: Any, **kwargs: Any) -> Any:
            forward_step = kwargs.get("forward_step_func")
            if callable(forward_step):
                kwargs["forward_step_func"] = self._wrap_forward_step(forward_step, current)
            return schedule(*args, **kwargs)

        return call_schedule

    def _wrap_forward_step(self, forward_step: Any, current: _Current) -> Any:
        @functools.wraps(forward_step)  # Megatron reads its signature (`checkpoint_activations_microbatch`)
        def call_forward_step(*args: Any, **kwargs: Any) -> Any:
            output, loss_func = forward_step(*args, **kwargs)
            return output, self._wrap_loss(loss_func, current)

        return call_forward_step

    def _wrap_loss(self, loss_func: Any, current: _Current) -> Any:
        data = getattr(loss_func, "keywords", {}).get("data")
        if not isinstance(data, dict) or ROW_FIELD not in data:
            return loss_func

        def call_loss_func(*args: Any, **kwargs: Any) -> Any:
            guard = self.training.guard
            index = current.log.count_call()  # counted before anything can fail: a lost call reads missing
            watch = ReductionWatch(MEGATRON_WRAPPER_MODULE)
            calls = guard.call(WHAT, watch.start)
            try:
                result = loss_func(*args, **kwargs)
            finally:
                guard.call(WHAT, watch.stop)
            guard.call(WHAT, record_loss_call, current, index, data, result, calls)
            return result

        return call_loss_func


def stamp_micro_batches(current: _Current, micro_batches: list) -> bool:
    """Each micro-batch dict gets its `Experience`'s row ids and scales (dict i was built from Experience i,
    `megatron_worker.py:1462-1497`); rows SkyRL padded to the largest micro-batch (`_pad_microbatch_to_size`) are -1,
    never named. False (nothing stamped, the update reads broken): the counts disagree."""
    import torch

    experiences = current.experiences or []
    if len(experiences) != len(micro_batches):
        current.log.broken_reason = (f"the Megatron worker built {len(micro_batches)} micro-batches from "
                                     f"{len(experiences)} experiences")  # fmt: skip
        return False
    for micro_batch, experience in zip(micro_batches, experiences, strict=True):
        info = getattr(experience, "info", None) or {}
        rows = info.get(ROW_FIELD)
        if rows is None:
            current.log.broken_reason = "a micro-batch carried no row ids"
            return False
        size = int(micro_batch["sequences"].shape[0])
        rows = rows.to(torch.long)
        padding = size - int(rows.shape[0])
        if padding < 0:
            current.log.broken_reason = "a Megatron micro-batch is smaller than its experience"
            return False
        micro_batch[ROW_FIELD] = torch.cat([rows, rows.new_full((padding,), -1)])
        scales = info.get(SCALE_FIELD)
        if scales is not None:
            micro_batch[SCALE_FIELD] = torch.cat([scales, scales.new_zeros((padding,))])
    return True


def clear_micro_batches(micro_batches: list) -> None:
    """Probe's row ids and scales off each micro-batch dict, whatever `stamp_micro_batches` got to."""
    for micro_batch in micro_batches:
        micro_batch.pop(ROW_FIELD, None)
        micro_batch.pop(SCALE_FIELD, None)


def record_loss_call(current: _Current, index: int, data: dict, result: Any, calls: Any) -> None:
    """One `loss_func` call: ``data`` is the micro-batch it was bound to, ``result`` `(loss, metrics)` or
    `(loss, tokens, metrics)` (`megatron_model_wrapper.py:808-812`). Megatron scales each micro-batch's KL and entropy
    by 1 / (real micro-batches x data-parallel ranks) on top of the pre-scaled policy loss (`:792-806`): the FSDP
    worker's `microbatch_weight / ranks`."""
    metrics = result[-1] if isinstance(result, tuple) and result and isinstance(result[-1], dict) else {}
    if data.get(PADDING_KEY):  # a token-batching padding micro-batch: no rows, counted
        current.log.add(index, MicroBatchCapture(rows=[], reported_loss=to_float(metrics.get("final_loss")),
                                                 is_padding=True))  # fmt: skip
        return
    if data.get(SUB_SEQUENCES_KEY) is not None:
        current.log.broken_reason = "a Megatron micro-batch packs several sequences in a row"
        return
    if calls is None:
        return
    real = int(data.get(REAL_MICRO_BATCHES_KEY) or data.get("num_microbatches") or 1)
    captured = summarize_micro_call(
        calls, rows=data[ROW_FIELD], scales=data.get(SCALE_FIELD), status=metrics, micro_weight=1.0 / max(real, 1),
        ranks=current.log.place.ranks, kl_coef=current.kl_coef, entropy_coef=current.entropy_coef,
        unsupported=current.unsupported,
    )  # fmt: skip
    if captured is not None:
        current.log.add(index, captured)


def get_megatron_reason(worker: Any) -> str | None:
    """Why this Megatron worker's configuration sends no rows (`plan.MEGATRON_REASONS`); None inside the proven
    boundary (`plan.MEGATRON_PROVEN`), read from the worker's own config and model as it trains."""
    trainer_config = worker.cfg
    megatron = trainer_config.policy.megatron_config
    tp, pp = int(megatron.tensor_model_parallel_size), int(megatron.pipeline_model_parallel_size)
    model = getattr(worker, "model", None)
    model_config = _get_model_config(worker)
    checks = (
        ("context_parallel", int(megatron.context_parallel_size) != 1),
        ("expert_parallel", int(megatron.expert_model_parallel_size) != 1),
        ("virtual_pipeline", len(getattr(worker, "actor_module", None) or [None]) != 1),
        ("packing", bool(trainer_config.remove_microbatch_padding)),
        ("token_batching", int(trainer_config.max_tokens_per_microbatch) > 0),
        ("fused_lm_head", bool(getattr(model, "_fused_lm_head", trainer_config.fused_lm_head_logprob))),
        ("sample_support", bool(trainer_config.algorithm.enable_sample_support_replay)),
        ("mtp", bool(getattr(model_config, "mtp_num_layers", None))),
        ("vlm", bool(getattr(worker, "is_vlm", False))),
        ("router_replay", bool(getattr(megatron, "moe_enable_routing_replay", False))),
    )  # fmt: skip
    for name, is_set in checks:
        if is_set:
            return MEGATRON_REASONS[name]
    dp = int(worker.mesh_rank.dp_size)
    # Every proven (TP, PP) ran at data parallel 1 and 2 (T12: DP 2 at TP 1 / PP 1; T15: TP 2 / PP 2 x DP 2), no more.
    if (tp, pp) not in MEGATRON_PROVEN or dp > MEGATRON_PROVEN_DATA_PARALLEL:
        return MEGATRON_REASONS["parallel"].format(tp=tp, pp=pp, dp=dp)
    return None


def _get_model_config(worker: Any) -> Any:
    """Megatron's own config of the worker's first model chunk (MTP lives there), else None."""
    if not getattr(worker, "actor_module", None):
        return None
    from megatron.core.utils import get_model_config

    return get_model_config(worker.actor_module[0])


_MEGATRON: SkyrlMegatronTraining | None = None


def get_megatron_training(training: SkyrlTraining) -> SkyrlMegatronTraining:
    global _MEGATRON
    if _MEGATRON is None:
        _MEGATRON = SkyrlMegatronTraining(training)
    return _MEGATRON
