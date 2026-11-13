"""One optimizer update on one rank as the framework ran it, for an RL adapter's loss hook: every loss call the hook
saw (counted before anything is summarized, so a call Probe failed to capture reads as missing, never as complete),
assembled once the update ends into per-sample rows (`run.samples.log_metrics_many`) and the update's own records
(`log_update`). A row's weight is its share of the update's number, which needs the update's call count, so weights
wait for the end. Pure Python (no torch). Why: integrations/verl/DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .....generated.samples.points import ContributionSource, Dtype, LossRole, UpdateLevel

#: Why an update did not move the weights (the frameworks skip a non-finite gradient norm).
NON_FINITE_SKIP = "non_finite_grad_norm"
#: Lower precision first: an update's tolerance follows its least precise term.
_DTYPE_ORDER = (Dtype.BF16, Dtype.FP16, Dtype.FP32)


class Share(Enum):
    """How the framework folds a key's per-call number into the update's: what a row's basis is divided by."""

    TOTAL = "total"  # summed over calls and ranks: the basis is already the row's share
    RANK_MEAN = "rank_mean"  # summed over calls, averaged over ranks: basis / ranks
    CALL_MEAN = "call_mean"  # averaged over (call, rank), padding calls as 0: basis / (calls x ranks)


@dataclass
class RowCapture:
    """One row of one loss call: the sample's own values and how it entered the loss."""

    #: The row's id in the step's batch (an index into `UpdateLog.keys`).
    row: int
    token_count: int
    mask_sha256: str
    loss_sum: float | None
    contribution: float
    contribution_terms: dict[str, float]
    normalizer: float | None
    #: Each key's own value (the row's masked mean); None: no trained token.
    values: dict[str, float | None]
    #: Each key's share of its call's number and how the framework folds it.
    bases: dict[str, tuple[float, Share]]


@dataclass
class MicroBatchCapture:
    rows: list[RowCapture]
    #: The loss the framework returned for the call (what it ran backward on).
    reported_loss: float | None
    dtype: Dtype = Dtype.FP32
    scale: float | None = None
    normalizer: float | None = None
    #: A padding call: no rows, mask all 0, counted in the framework's means.
    is_padding: bool = False
    #: How its rows' contributions were taken; the weakest wins when one term was rebuilt (verl geo_mean's pg term).
    source: ContributionSource = ContributionSource.FRAMEWORK_AUTOGRAD


@dataclass
class UpdatePlace:
    """Where an update sits: its step, ordinal, this rank and what the whole update declares."""

    step: int
    update: int
    rank: int
    ranks: int
    updates_in_step: int | None = None
    reduction: str | None = None
    #: The model the update trains (a critic's value loss beside the actor's); None: the actor (the contract's default).
    role: LossRole | None = None


@dataclass
class UpdateLog:
    """One rank's share of one optimizer update."""

    place: UpdatePlace
    #: Sample key by row id; None for a row with no single sample (data-parallel padding, a merged row).
    keys: Sequence[str | None]
    #: By call ordinal: the calls Probe captured (a missing ordinal is a call it could not).
    micro_batches: dict[int, MicroBatchCapture] = field(default_factory=dict)
    #: Every loss call of the update, captured or not.
    calls: int = 0
    #: Why the update sends nothing (a call carried no row ids: its rows cannot be named).
    broken_reason: str | None = None

    def count_call(self) -> int:
        """The next call's ordinal, counted before the call is summarized."""
        self.calls += 1
        return self.calls - 1

    def add(self, index: int, micro_batch: MicroBatchCapture) -> None:
        self.micro_batches[index] = micro_batch

    def get_key(self, row: int) -> str | None:
        return self.keys[row] if 0 <= row < len(self.keys) else None

    def build_rows(self, *, optimizer_step: int | None) -> list[dict[str, Any]]:
        """Every named row as a `log_metrics_many` row; weights folded the way the framework folds each key."""
        calls = max(self.calls, 1)
        ranks = max(self.place.ranks, 1)
        divisors = {Share.TOTAL: 1, Share.RANK_MEAN: ranks, Share.CALL_MEAN: calls * ranks}
        rows: list[dict[str, Any]] = []
        for index, micro_batch in sorted(self.micro_batches.items()):
            seen: Counter = Counter()
            for capture in micro_batch.rows:
                key = self.get_key(capture.row)
                if key is None:
                    continue  # never sent; the rank record counts only named rows
                occurrence = seen[key]
                seen[key] += 1
                values, weights = {}, {}
                for name, value in capture.values.items():
                    if value is None or not math.isfinite(value):
                        continue  # no trained token: unavailable, never a 0
                    basis, share = capture.bases[name]
                    values[name] = value
                    weights[name] = basis / divisors[share]
                rows.append(_drop_none({
                    "sample_key": key, "step": self.place.step, "update": self.place.update, "metrics": values,
                    "weights": weights, "role": self.place.role, "rank": self.place.rank, "micro_batch": index,
                    "occurrence": occurrence,
                    "token_count": capture.token_count, "mask_sha256": capture.mask_sha256,
                    "loss_sum": capture.loss_sum, "normalizer": capture.normalizer,
                    "scale": micro_batch.scale if micro_batch.scale is not None else 1.0,
                    "contribution": capture.contribution, "contribution_terms": dict(capture.contribution_terms),
                    "contribution_source": micro_batch.source, "optimizer_step": optimizer_step,
                }))  # fmt: skip
        return rows

    def build_records(self, *, grad_norm: float | None, metrics: Mapping[str, float | None],
                      optimizer_step: int | None, reported_loss: float | None) -> list[dict[str, Any]]:  # fmt: skip
        """The update's records, each `log_update`'s keyword arguments: the whole update (rank 0 only), this rank,
        each captured call. ``metrics``: the update's own (lr, gradient norm) under the framework's names."""
        place = self.place
        records: list[dict[str, Any]] = []
        if place.rank == 0:
            applied = None if grad_norm is None else math.isfinite(grad_norm)
            finite = {name: value for name, value in metrics.items() if value is not None and math.isfinite(value)}
            records.append(_drop_none({
                "level": UpdateLevel.UPDATE, "ranks_expected": max(place.ranks, 1),
                "updates_in_step": place.updates_in_step, "reduction": place.reduction,
                "reported_loss": keep_finite(reported_loss), "applied": applied,
                "skipped_reason": NON_FINITE_SKIP if applied is False else None, "optimizer_step": optimizer_step,
                "metrics": finite or None, "dtype": get_lowest_dtype(m.dtype for m in self.micro_batches.values()),
            }))  # fmt: skip
        padding = [index for index, micro_batch in sorted(self.micro_batches.items()) if micro_batch.is_padding]
        if self.calls:
            records.append(_drop_none({
                "level": UpdateLevel.RANK, "rank": place.rank, "micro_batches_expected": self.calls,
                "rows_expected": sum(self._count_named(m) for m in self.micro_batches.values()),
                "padding_micro_batches": padding or None,
            }))  # fmt: skip
        for index, micro_batch in sorted(self.micro_batches.items()):
            records.append(_drop_none({
                "level": UpdateLevel.MICRO_BATCH, "rank": place.rank, "micro_batch": index,
                "reported_loss": keep_finite(micro_batch.reported_loss),
                "scale": micro_batch.scale if micro_batch.scale is not None else 1.0,
                "normalizer": micro_batch.normalizer, "rows": self._count_named(micro_batch),
            }))  # fmt: skip
        if place.role is not None:
            records = [{**record, "role": place.role} for record in records]
        return records

    def _count_named(self, micro_batch: MicroBatchCapture) -> int:
        return sum(1 for capture in micro_batch.rows if self.get_key(capture.row) is not None)


def get_lowest_dtype(dtypes: Iterable[Dtype | str]) -> Dtype | None:
    found = {Dtype(dtype) for dtype in dtypes}
    return next((dtype for dtype in _DTYPE_ORDER if dtype in found), None)


def get_optimizer_step(optimizer: Any) -> int | None:
    """The optimizer's own counter (AdamW `state["step"]`, else a fused optimizer's `param_groups[i]["step"]`, as apex
    FusedAdam keeps it; a Megatron `ChainedOptimizer`'s parts in turn), which a skipped update does not move; None
    without a finite one. Never raises: an optimizer whose `state` is no mapping (Megatron's `ProxyDict`) is skipped."""
    try:
        parts = list(getattr(optimizer, "chained_optimizers", None) or ())
    except Exception:  # noqa: BLE001 -- a property that raises: read the optimizer alone
        parts = []
    for candidate in (optimizer, *parts):
        for holder in _get_step_holders(candidate):
            step = holder.get("step") if hasattr(holder, "get") else None
            if step is not None:
                number = to_float(step)
                return int(number) if number is not None and math.isfinite(number) else None
    return None


def _get_step_holders(optimizer: Any) -> list:
    holders: list = []
    for read in (lambda: getattr(optimizer, "state", {}).values(), lambda: getattr(optimizer, "param_groups", None)):
        try:
            holders += list(read() or ())
        except Exception:  # noqa: BLE001 -- not a mapping or a list: nothing to read here
            continue
    return holders


def to_float(value: Any) -> float | None:
    """A number (a Python one, a one-element tensor or list) as a float, NaN and inf kept; None for anything else.
    A tensor's `.item()` is a device-to-host copy: hand a loss hook's own numbers to `copy_to_host` instead."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (list, tuple)):
        if len(value) != 1:
            return None
        value = value[0]
    item = getattr(value, "item", None)
    try:
        return float(item() if callable(item) else value)
    except (TypeError, ValueError, RuntimeError):
        return None


def keep_finite(value: float | None) -> float | None:
    return value if value is not None and math.isfinite(value) else None


def _drop_none(record: dict[str, Any]) -> dict[str, Any]:
    return {name: value for name, value in record.items() if value is not None}
