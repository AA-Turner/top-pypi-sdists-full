"""The interface every TRL loss hook implements: wrap the trainer's loss on this instance, and hand each loss call's
per-row values to the training recorder as one `LossBatch`; and `copy_rows_to_host`, a call's per-token tensors as
per-row values in one device-to-host copy. The registry that picks a hook is `hooks/`."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from probe.generated.samples.points import Dtype, Reducer, hash_mask
from probe.sdk.run.samples.points import RowSummary, copy_to_host, get_lowest_dtype

from .declarations import EVAL_KEY_PREFIX, EXTREME_KEYS


@dataclass
class LossBatch:
    """One loss call (a micro-batch): its rows' sample keys and summaries, what the loss returned, and the reduction
    that explains it. Names are TRL's train names; the recorder prefixes eval ones."""

    split: str
    keys: list[str]
    #: `RowSummary` per row, in batch order: values, token weights and the loss bookkeeping.
    rows: list[Any]
    #: The loss TRL ran backward on for this call (eval: the loss it returned).
    reported_loss: float | None
    #: Per key, a weight per row when it is not the row's trained tokens (a loss's share of the reduction).
    weights: dict[str, list[float]] = field(default_factory=dict)
    #: Loss terms no row owns (an MoE router's auxiliary loss).
    batch_terms: dict[str, float] = field(default_factory=dict)
    #: The micro-batch's own normalizer and scale, when one serves every row.
    normalizer: float | None = None
    scale: float | None = None
    #: The precision of the tensors the loss was computed from (the shard check's and the loss keys' tolerance).
    dtype: Dtype = Dtype.FP32
    #: Keys computed from other tensors (`entropy` from the entropies): their own precision, each key's tolerance.
    dtypes: dict[str, Dtype] = field(default_factory=dict)


class LossHook:
    """One trainer kind's loss capture. ``unsupported`` is what this run's settings put out of reach (keys of
    `declarations.UNSUPPORTED`, or of the hook's own `get_reasons`); a hook with any installs nothing."""

    #: The TRL class names it hooks, matched along the trainer's class chain.
    names: tuple[str, ...] = ()
    #: The method it rebuilds: a subclass that defines its own is not rebuilt (`hooks.pick_hook`).
    loss_method = ""
    #: Keys whose series takes each call's min or max over rows (each row sends its own value with that `agg`).
    extremes: Mapping[str, Reducer] = EXTREME_KEYS

    def __init__(self, trainer: Any, recorder: Any) -> None:
        self.trainer = trainer
        self.recorder = recorder

    def find_unsupported(self) -> list[str]:
        """What this run's settings ask for that the hook does not rebuild: nothing is sent."""
        return []

    def find_unsent(self) -> list[str]:
        """What the hook leaves out while it sends the rest (declared unsupported beside its rollups)."""
        return []

    def get_reasons(self) -> dict[str, str]:
        """Why, for what this hook names that `declarations.UNSUPPORTED` does not (a loss type it does not rebuild)."""
        return {}

    def get_rollups(self, dtype: Dtype, logging_window: int | None, dtypes: Mapping[str, Dtype] | None = None,
                    eval_prefixes: Sequence[str] = (EVAL_KEY_PREFIX,)) -> dict[str, dict]:  # fmt: skip
        """How TRL computes its own series of each key this run sends (`declarations.make_rollups`): each at
        ``dtype``, the loss's precision, or its own in ``dtypes``; eval keys once per `evaluate()` prefix seen."""
        return {}

    def get_reduction(self) -> str:
        """TRL's own reduction setting, as a label (`loss_type`)."""
        return str(getattr(self.trainer, "loss_type", None) or getattr(self.trainer.args, "loss_type", "") or "loss")

    def get_dtype(self) -> Dtype:
        """The precision declared before the first loss call shows the real one (`bf16` / `fp16` mixed precision)."""
        args = self.trainer.args
        if getattr(args, "bf16", False):
            return Dtype.BF16
        return Dtype.FP16 if getattr(args, "fp16", False) else Dtype.FP32

    def get_place(self) -> tuple[int, int] | None:
        """(rank, ranks) this process sends as: the data-parallel ones; None when another process sends its rows."""
        accelerator = getattr(self.trainer, "accelerator", None)
        return (int(getattr(accelerator, "process_index", 0) or 0),
                int(getattr(accelerator, "num_processes", 1) or 1))  # fmt: skip

    def install(self) -> None:
        """Wrap the instance's loss path (`recorder.install`); each loss call goes to `recorder.handle_loss`."""

    def close(self) -> None:
        """Take off what `install` put on outside the instance dict (a forward hook)."""


def is_scaled_for_accumulation(trainer: Any, items: Any) -> bool:
    """transformers' own rule (`trainer.py:2083-2091`): whether the loss compute_loss returns is already divided over
    the accumulation steps; when not, transformers divides it after, before backward."""
    flag = getattr(trainer, "loss_is_scaled_for_ga", None)
    if flag is not None:
        return bool(flag)
    return bool(getattr(trainer, "model_accepts_loss_kwargs", False) and items is not None) or getattr(
        trainer, "compute_loss_func", None) is not None


@dataclass(frozen=True)
class HostRows:
    rows: list[RowSummary]
    #: Per row, each extra column's value, in the order given.
    extras: list[list[float]]
    #: Per row, the extra matrix's values (SFT's token ids), when one was given.
    matrix: list[list[float]]
    scalars: list[float | None]


def copy_rows_to_host(values: Mapping[str, Any], mask: Any, *, loss: str, extras: Sequence[Any] = (),
                      matrix: Any = None, scalars: Sequence[Any] = ()) -> HostRows:  # fmt: skip
    """Per row of ``mask`` ([rows, tokens]): every ``values`` name as its masked token mean, its trained tokens, mask
    digest and ``loss``'s masked sum; ``extras`` ([rows] each), ``matrix`` ([rows, n]) and ``scalars`` ride the same
    single copy (`copy_to_host`)."""
    import torch

    flags = (mask > 0).to(torch.float64)
    names = list(values)
    columns = [flags.sum(-1), *((values[name].detach().to(torch.float64) * flags).sum(-1) for name in names), *extras]
    joined = flags if matrix is None else torch.cat([flags, matrix.detach().to(flags.device, torch.float64)], dim=1)
    host = copy_to_host(columns, joined, scalars)
    width, start = int(flags.shape[1]), 1 + len(names)
    rows = []
    for stats, row_flags in zip(host.rows, host.flags, strict=True):
        tokens, sums = stats[0], stats[1:start]
        metrics = {name: total / tokens for name, total in zip(names, sums, strict=True)
                   if tokens > 0 and math.isfinite(total / tokens)}  # fmt: skip
        rows.append(RowSummary(metrics=metrics, weight=tokens, token_count=int(round(tokens)),
                               mask_sha256=hash_mask(row_flags[:width]), loss_sum=sums[names.index(loss)]))  # fmt: skip
    return HostRows(rows=rows, extras=[stats[start:] for stats in host.rows],
                    matrix=[row[width:] for row in host.flags], scalars=host.scalars)  # fmt: skip


def get_tensor_dtype(*tensors: Any) -> Dtype:
    """The least precise of the tensors' dtypes (bf16, fp16, else fp32)."""
    names = {str(getattr(tensor, "dtype", "")) for tensor in tensors if tensor is not None}
    found = [Dtype.BF16 for name in names if name == "torch.bfloat16"] + [Dtype.FP16 for name in names
                                                                           if name == "torch.float16"]  # fmt: skip
    return get_lowest_dtype(found) or Dtype.FP32
