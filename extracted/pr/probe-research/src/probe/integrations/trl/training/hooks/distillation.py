"""DistillationTrainer's per-sample divergence and entropy (`distillation_trainer.py:104-216`, `:1853-1984`; spike S1,
plan D3). The per-token values never leave `_chunked_divergence_loss`, so ONE module-level tap replaces the module's
`ChunkedDivergenceFunction` name with a class whose `apply` calls the real one and, only while a context variable
holds a sink, keeps detached copies of its two outputs. Only a tracked instance's `_compute_loss` wrap sets the
variable: any other instance in the process runs the real function and nothing is kept. Rows are keyed like GRPO's
(the generation output is shuffled and split the same way, `:1838-1845`)."""

from __future__ import annotations

import contextvars
import functools
from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import ContributionSource, Dtype

from ..declarations import EVAL_KEY_PREFIX, make_rollups
from ..hook import LossBatch, LossHook, copy_rows_to_host, get_tensor_dtype
from .generations import ROW, GenerationStamps

WHAT = "a per-sample loss"
#: Where the tap keeps a tracked call's per-token outputs; None (every other call): it keeps nothing.
SINK: contextvars.ContextVar[list | None] = contextvars.ContextVar("probe_trl_distillation_sink", default=None)
TAP_FLAG = "is_probe_tap"


def install_tap(module: Any) -> None:
    """Once per process: the module's `ChunkedDivergenceFunction` -> a tap with the same `apply` (D3)."""
    import torch

    real = module.ChunkedDivergenceFunction
    if getattr(real, TAP_FLAG, False):
        return

    class ChunkedDivergenceTap:
        is_probe_tap = True
        _probe_real = real

        @staticmethod
        def apply(*args: Any) -> Any:
            result = real.apply(*args)
            sink = SINK.get()
            # Only tensors are kept: an output of another shape leaves the sink empty and the call records nothing.
            if sink is not None and isinstance(result, tuple) and all(isinstance(v, torch.Tensor) for v in result):
                sink.append(tuple(value.detach() for value in result))
            return result

    module.ChunkedDivergenceFunction = ChunkedDivergenceTap


class DistillationLoss(LossHook):
    names = ("DistillationTrainer",)
    loss_method = "_compute_loss"

    def __init__(self, trainer: Any, recorder: Any) -> None:
        super().__init__(trainer, recorder)
        self.stamps = GenerationStamps(recorder)

    def get_reduction(self) -> str:
        return "jsd"

    def get_rollups(self, dtype: Dtype, logging_window: int | None, dtypes: Mapping[str, Dtype] | None = None,
                    eval_prefixes: Sequence[str] = (EVAL_KEY_PREFIX,)) -> dict[str, dict]:  # fmt: skip
        return make_rollups(("entropy",), dtype=dtype, dtypes=dtypes, logging_window=logging_window,
                            eval_prefixes=eval_prefixes)  # fmt: skip

    def install(self) -> None:
        from trl.trainer import distillation_trainer

        install_tap(distillation_trainer)
        trainer, guard = self.trainer, self.recorder.guard
        score = trainer._generate_and_score_completions
        compute = trainer._compute_loss

        @functools.wraps(score)
        def call_score(*args: Any, **kwargs: Any) -> Any:
            output = score(*args, **kwargs)
            guard.call("a per-sample generation", self.stamps.stamp, output, self._get_split())
            return output

        @functools.wraps(compute)
        def call_compute(unwrapped: Any, inputs: Any, *args: Any, **kwargs: Any) -> Any:
            split = guard.call(WHAT, self._get_split) or SampleSplit.TRAIN
            slot = guard.call(WHAT, self.recorder.open_call, split)
            sink: list = []
            token = SINK.set(sink if slot is not None else None)
            try:
                result = compute(unwrapped, inputs, *args, **kwargs)
            finally:
                SINK.reset(token)
            items = args[0] if args else kwargs.get("num_items_in_batch")
            if slot is not None and len(sink) == 1 and ROW in inputs:
                guard.call(WHAT, self._record, slot, split, inputs, result, sink[0], items)
            return result

        self.recorder.install(trainer, "_generate_and_score_completions", call_score)
        self.recorder.install(trainer, "_compute_loss", call_compute)

    def _get_split(self) -> str:
        return SampleSplit.TRAIN if self.trainer.model.training else SampleSplit.EVAL

    def _record(self, slot: Any, split: str, inputs: Any, result: Any, kept: Any, items: Any) -> None:
        self.recorder.handle_loss(slot, self._rebuild(split, inputs, result, kept, items))

    def _rebuild(self, split: str, inputs: Any, result: Any, kept: Any, items: Any) -> LossBatch:
        """The tap's flat per-token divergence and entropy back to [rows, completion tokens] (every position on
        CPU; valid positions only where Triton compacts them, `:182-188`), then `loss = sum / num_items_in_batch`
        (train, already GA-scaled: `loss_is_scaled_for_ga = True`) or `/ local valid tokens` (eval)."""
        import torch

        divergence, entropy = kept
        mask = inputs["completion_mask"]
        mask = mask * inputs["tool_mask"] if "tool_mask" in inputs else mask
        if divergence.numel() != mask.numel():  # compacted: valid positions only
            valid = mask.reshape(-1) != 0
            full_divergence = torch.zeros(mask.numel(), dtype=divergence.dtype, device=divergence.device)
            full_entropy = torch.zeros_like(full_divergence)
            full_divergence[valid], full_entropy[valid] = divergence, entropy
            divergence, entropy = full_divergence, full_entropy
        divergence, entropy = divergence.reshape(mask.shape), entropy.reshape(mask.shape)
        host = copy_rows_to_host({"loss": divergence, "entropy": entropy}, mask, loss="loss",
                                 extras=self.stamps.get_columns(inputs), scalars=[result[0], items])  # fmt: skip
        reported, items_number = host.scalars
        normalizer = items_number if items_number is not None else float(max(sum(r.token_count for r in host.rows), 1))
        rows = [replace(row, normalizer=normalizer, scale=1.0, contribution=(row.loss_sum or 0.0) / normalizer,
                        contribution_source=ContributionSource.PROBE_REDUCER) for row in host.rows]  # fmt: skip
        keys = self.stamps.take_keys([(extra[0], extra[1]) for extra in host.extras], split)
        return LossBatch(split=split, keys=keys, rows=rows, reported_loss=reported, normalizer=normalizer, scale=1.0,
                         dtype=get_tensor_dtype(divergence), dtypes={"entropy": get_tensor_dtype(entropy)})
