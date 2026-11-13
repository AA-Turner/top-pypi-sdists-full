"""SFT's per-sample loss, entropy and token accuracy, in training updates and `evaluate()` passes (spikes S0, S1,
`sft_trainer.py:1602-1690`): a forward hook keeps the output of the `model(**inputs, fused_lm_head=True)` call
(per-token fields, zero where the label is -100) and, with label smoothing, the plain forward's logits that
`LabelSmoother` reads; the `compute_loss` wrap rebuilds each row's share of the loss it returned. A packed or
padding-free row is split back into its examples (`packing.py`) once its GPU proof is in (`GPU_PROVEN`)."""

from __future__ import annotations

import functools
from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import ContributionSource, Dtype

from ...rows import get_segment_starts, make_sft_key
from ..declarations import EVAL_KEY_PREFIX, GPU_PROVEN, PACKED_SFT, SFT_TENSOR_PARALLEL, SFT_TOKEN_KEYS, make_rollups
from ..hook import LossBatch, LossHook, copy_rows_to_host, get_tensor_dtype, is_scaled_for_accumulation
from .packing import shift_to_targets, to_segments

REBUILT = ("nll", "dft")
#: Packing strategies that keep every example whole in one row.
WHOLE_PACKING = ("bfd",)
WHAT = "a per-sample loss"


class SftLoss(LossHook):
    names = ("SFTTrainer",)
    loss_method = "compute_loss"

    def __init__(self, trainer: Any, recorder: Any) -> None:
        super().__init__(trainer, recorder)
        self._is_inside = False
        self._captured: Any = None
        self._logits: Any = None
        self._handle: Any = None

    def find_unsupported(self) -> list[str]:
        trainer, args = self.trainer, self.trainer.args
        if not self.recorder.should_record_sft:
            return ["SFT without record_sft"]
        is_packed = bool(getattr(args, "packing", False) or getattr(args, "padding_free", False))
        strategy = getattr(args, "packing_strategy", "bfd")
        if getattr(args, "packing", False) and strategy not in WHOLE_PACKING:
            return [f"packed SFT ({strategy})"]
        if is_packed and PACKED_SFT not in GPU_PROVEN:
            return [PACKED_SFT]
        parallel = getattr(getattr(trainer, "accelerator", None), "parallelism_config", None)
        if getattr(parallel, "sp_enabled", False):
            return ["SFT sequence parallel"]
        if getattr(parallel, "cp_enabled", False):
            return ["SFT context parallel"]
        if get_tp_size(trainer) != 1 and SFT_TENSOR_PARALLEL not in GPU_PROVEN:
            return [SFT_TENSOR_PARALLEL]
        is_smoothed = getattr(trainer, "label_smoother", None) is not None
        loss_type = getattr(args, "loss_type", "nll")
        if (loss_type not in REBUILT or getattr(trainer, "compute_loss_func", None) is not None
                or (is_smoothed and (loss_type != "nll" or is_packed))):  # fmt: skip
            return ["SFT loss"]
        return []

    def get_rollups(self, dtype: Dtype, logging_window: int | None, dtypes: Mapping[str, Dtype] | None = None,
                    eval_prefixes: Sequence[str] = (EVAL_KEY_PREFIX,)) -> dict[str, dict]:  # fmt: skip
        return make_rollups(SFT_TOKEN_KEYS, dtype=dtype, dtypes=dtypes, logging_window=logging_window,
                            eval_prefixes=eval_prefixes)  # fmt: skip

    def get_reduction(self) -> str:
        return str(getattr(self.trainer.args, "loss_type", "nll"))

    def get_place(self) -> tuple[int, int] | None:
        accelerator = getattr(self.trainer, "accelerator", None)
        size = get_tp_size(self.trainer)
        rank = int(getattr(accelerator, "tensor_parallel_rank", 0) or 0) if size > 1 else 0
        return get_tensor_parallel_place(int(getattr(accelerator, "process_index", 0) or 0),
                                         int(getattr(accelerator, "num_processes", 1) or 1), rank, size)  # fmt: skip

    def install(self) -> None:
        trainer, guard = self.trainer, self.recorder.guard
        compute = trainer.compute_loss
        is_smoothed = getattr(trainer, "label_smoother", None) is not None

        def handle_forward(_module: Any, _args: Any, kwargs: Any, output: Any) -> None:
            if not self._is_inside:
                return
            if kwargs.get("fused_lm_head"):
                self._captured = output
            elif is_smoothed and getattr(output, "logits", None) is not None:
                self._logits = output.logits.detach()

        @functools.wraps(compute)
        def call_compute(model: Any, inputs: Any, *args: Any, **kwargs: Any) -> Any:
            split = guard.call(WHAT, self._get_split) or SampleSplit.TRAIN
            slot = guard.call(WHAT, self.recorder.open_call, split)
            self._is_inside, self._captured, self._logits = slot is not None, None, None
            try:
                result = compute(model, inputs, *args, **kwargs)
            finally:  # a raising loss never leaves the model's output (and its graph) held here
                captured, logits = self._captured, self._logits
                self._is_inside, self._captured, self._logits = False, None, None
            if slot is not None and captured is not None and (logits is not None or not is_smoothed):
                items = kwargs.get("num_items_in_batch", args[1] if len(args) > 1 else None)
                guard.call(WHAT, self._record, slot, split, inputs, result, captured, logits, items)
            return result

        # DDP's wrapper calls this module, so the hook fires on every process.
        self._handle = trainer.model.register_forward_hook(handle_forward, with_kwargs=True)
        self.recorder.install(trainer, "compute_loss", call_compute)

    def close(self) -> None:
        if self._handle is not None:
            self._handle.remove()
            self._handle = None

    def _get_split(self) -> str:
        return SampleSplit.TRAIN if self.trainer.model.training else SampleSplit.EVAL

    def _record(self, slot: Any, split: str, inputs: Any, result: Any, captured: Any, logits: Any,
                items: Any) -> None:  # fmt: skip
        loss = result[0] if isinstance(result, tuple) else result
        self.recorder.handle_loss(slot, self._rebuild(split, inputs, loss, captured, logits, items))

    def _rebuild(self, split: str, inputs: Any, loss: Any, captured: Any, logits: Any, items: Any) -> LossBatch:
        """`loss = sum(-log_probs) / num_tokens` (DFT's per-token `x exp(log_probs)`; with label smoothing
        `LabelSmoother`'s per token), x processes / TP size with `average_tokens_across_devices`, the MoE aux loss over
        the accumulation steps (`:1655-1672`), then / GA when transformers divides after (a model with
        `accepts_loss_kwargs = False`). An eval pass divides by its own tokens. Every number but the smoothed loss
        reaches the host in one copy."""
        import torch

        trainer, args = self.trainer, self.trainer.args
        log_probs = captured.log_probs.detach()
        per_token = -log_probs
        if getattr(args, "loss_type", "nll") == "dft":
            per_token = per_token * log_probs.exp()
        values = {"entropy": captured.entropy.detach(), "mean_token_accuracy": captured.is_top1.float()}
        if logits is None:
            values["loss"] = per_token
        aux_loss = getattr(captured, "aux_loss", None)
        has_aux = getattr(trainer, "aux_loss_enabled", False) and aux_loss is not None
        scalars = [loss, aux_loss if has_aux else None, items]
        starts = get_segment_starts(inputs)
        if starts is None:
            ids = inputs["input_ids"]
            kept = inputs.get("attention_mask")
            kept = torch.ones_like(ids) if kept is None else kept
            host = copy_rows_to_host(values, captured.label_mask, loss="loss" if logits is None else "entropy",
                                     matrix=torch.cat([ids, kept], dim=1), scalars=scalars)  # fmt: skip
        else:
            total = int(inputs["input_ids"].shape[1])
            placed, label_mask = shift_to_targets({name: value[0] for name, value in values.items()},
                                                  captured.label_mask[0], total)  # fmt: skip
            values, mask, ids, kept = to_segments(placed, label_mask, inputs["input_ids"][0], starts, total)
            host = copy_rows_to_host(values, mask, loss="loss", matrix=torch.cat([ids, kept], dim=1), scalars=scalars)
        rows = host.rows
        if logits is not None:  # the loss rides its own copy: LabelSmoother's shifted [T - 1] positions
            smoothed, mask = get_smoothed(logits, inputs["labels"], trainer.label_smoother.epsilon)
            own = copy_rows_to_host({"loss": smoothed}, mask, loss="loss").rows
            rows = [replace(row, metrics={**row.metrics, **({"loss": found.metrics["loss"]} if "loss" in found.metrics
                                                            else {})}, loss_sum=found.loss_sum)
                    for row, found in zip(rows, own, strict=True)]  # fmt: skip
        width = int(ids.shape[1])
        pairs = [(row, matrix) for row, matrix in zip(rows, host.matrix, strict=True)
                 if starts is None or row.token_count > 0]  # a segment with no trained token is no example's row
        reported, aux, items_number = host.scalars
        is_train = split == SampleSplit.TRAIN
        normalizer = max(items_number if items_number is not None else float(sum(r.token_count for r, _m in pairs)),
                         1.0)  # fmt: skip
        accumulation = float(trainer.current_gradient_accumulation_steps) if is_train else 1.0
        after = 1.0 if not is_train or is_scaled_for_accumulation(trainer, items) else 1.0 / accumulation
        scale = after
        if getattr(args, "average_tokens_across_devices", False) and items is not None:
            scale *= float(int(trainer.accelerator.num_processes) // get_tp_size(trainer))
        built = [replace(row, normalizer=normalizer, scale=scale, contribution=(row.loss_sum or 0.0) / normalizer
                         * scale, contribution_source=ContributionSource.PROBE_REDUCER) for row, _m in pairs]  # fmt: skip
        keys = [make_sft_key([int(token) for token, keep in zip(matrix[:width], matrix[width:], strict=True) if keep],
                             is_eval=not is_train) for _row, matrix in pairs]  # fmt: skip
        terms = {}
        if aux is not None:
            steps = accumulation if items is not None else 1.0
            terms["aux_loss"] = trainer.router_aux_loss_coef * aux / steps * after
        return LossBatch(split=split, keys=keys, rows=built,
                         reported_loss=reported * after if reported is not None else None, batch_terms=terms,
                         normalizer=normalizer, scale=scale,
                         dtype=get_tensor_dtype(logits if logits is not None else captured.log_probs),
                         dtypes={"entropy": get_tensor_dtype(captured.entropy)})  # fmt: skip


def get_smoothed(logits: Any, labels: Any, epsilon: float) -> tuple[Any, Any]:
    """`LabelSmoother`'s per-token loss on the shifted labels, `(1 - eps) x nll + eps x sum(-log p) / V`, one row's
    [T, V] at a time, and its mask."""
    import torch

    shifted = labels[..., 1:]
    mask = shifted != -100
    per_token = torch.zeros(shifted.shape, dtype=torch.float64, device=logits.device)
    with torch.no_grad():
        for index in range(logits.shape[0]):
            negative = -torch.nn.functional.log_softmax(logits[index, :-1, :].contiguous(), dim=-1)
            nll = negative.gather(-1, shifted[index].clamp(min=0).unsqueeze(-1)).squeeze(-1)
            smooth = negative.sum(-1, dtype=torch.float32) / negative.shape[-1]
            per_token[index] = ((1 - epsilon) * nll + epsilon * smooth) * mask[index]
    return per_token, mask


def get_tp_size(trainer: Any) -> int:
    get_size = getattr(trainer, "get_tp_size", None)
    return int(get_size()) if callable(get_size) else 1


def get_tensor_parallel_place(process: int, processes: int, tp_rank: int, tp_size: int) -> tuple[int, int] | None:
    """(data-parallel rank, data-parallel ranks) a process sends as under tensor parallelism (TP innermost in the
    device mesh), or None for TP ranks past 0: they hold the same rows, which would otherwise count `tp_size` times."""
    if tp_size <= 1:
        return process, processes
    if tp_rank != 0:
        return None
    return process // tp_size, max(processes // tp_size, 1)
