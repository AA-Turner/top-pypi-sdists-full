"""A loss hook's per-token tensors as per-row values: any named per-token values, the loss mask and token weights in;
each row's weighted mean of every name, its weight, trained tokens, mask digest and, for the loss, its contribution to
the micro-batch's objective. One device-to-host copy per micro-batch (everything stacked, then one `.tolist()`).

The contribution comes from the framework's own reduction when it is given as a callable (the gradient of that
reduction with respect to the detached per-token loss, times the loss: exact for any reduction linear in the loss,
`framework_autograd`), else from an explicit normalizer (`probe_reducer`). Plain nested lists work without torch."""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from .....generated.samples.points import ContributionSource, hash_mask


@dataclass(frozen=True)
class RowSummary:
    """One row (a sample occurrence) of a micro-batch."""

    #: Each name's weighted mean over the row's masked tokens; a row with no weight has none.
    metrics: dict[str, float] = field(default_factory=dict)
    #: What every value averages over: the row's sum of mask x token weight (1 a row when not token-weighted).
    weight: float = 0.0
    token_count: int = 0
    mask_sha256: str = ""
    #: The masked per-token loss sum, before any normalizer (with ``loss``).
    loss_sum: float | None = None
    contribution: float | None = None
    contribution_source: ContributionSource | None = None
    normalizer: float | None = None
    scale: float | None = None

    def to_row(self, sample_key: str, *, step: int, update: int | None = None, **place: Any) -> dict[str, Any]:
        """A `run.samples.log_metrics_many` row: ``place`` is the row's `rank`, `micro_batch`, `occurrence`, ...
        (bookkeeping only inside an update)."""
        row: dict[str, Any] = {"sample_key": sample_key, "step": step, "update": update, "metrics": dict(self.metrics),
                               "weights": self.weight, **place}  # fmt: skip
        if update is not None:
            row.update(token_count=self.token_count, mask_sha256=self.mask_sha256, loss_sum=self.loss_sum,
                       contribution=self.contribution,
                       contribution_source=self.contribution_source, normalizer=self.normalizer, scale=self.scale)  # fmt: skip
        return row


def _is_torch(value: Any) -> bool:
    return type(value).__module__.split(".")[0] == "torch"


def _get_normalizers(normalizer: float | Sequence[float] | None, rows: int) -> list[float | None]:
    if normalizer is None or isinstance(normalizer, (int, float)):
        return [normalizer] * rows
    found = [float(value) for value in normalizer]
    if len(found) != rows:
        raise ValueError(f"normalizer names {len(found)} rows, the batch has {rows}")
    return found


def summarize_rows(
    values: Mapping[str, Any], mask: Any, *, weights: Any = None, loss: str | None = None,
    reduction: Callable[[Any, Any], Any] | None = None, normalizer: float | Sequence[float] | None = None,
    scale: float | None = None, is_token_weighted: bool = True,
) -> list[RowSummary]:  # fmt: skip
    """Per row of ``mask`` ([rows, tokens]): every ``values`` name ([rows, tokens], any name) as its weighted mean.
    ``weights``: per-token weights (default 1) inside the mask. ``loss``: which name is the per-token loss; with
    ``reduction(loss, mask) -> scalar`` (the framework's own) each row's contribution is taken by autograd, else with
    ``normalizer`` (one, or one a row) as sum(loss x mask) / normalizer. ``scale`` multiplies a contribution after
    the reduction (gradient accumulation, data-parallel averaging). ``is_token_weighted`` false: every row weighs 1
    (a sequence-mean framework)."""
    if loss is not None and loss not in values:
        raise KeyError(f"loss {loss!r} is not among the values {sorted(values)}")
    if _is_torch(mask):
        table, masks = _summarize_torch(values, mask, weights, loss, reduction, normalizer, scale)
    else:
        if reduction is not None:
            raise TypeError("a framework reduction needs torch tensors (autograd); give a normalizer for lists")
        table, masks = _summarize_lists(values, mask, weights, loss, normalizer, scale)
    names = list(values)
    source = None
    if loss is not None and (reduction is not None or normalizer is not None):
        source = ContributionSource.FRAMEWORK_AUTOGRAD if reduction is not None else ContributionSource.PROBE_REDUCER
    normalizers = _get_normalizers(normalizer, len(table))
    rows = []
    for index, (stats, flags) in enumerate(zip(table, masks, strict=True)):
        weight, tokens, sums, tail = stats[0], stats[1], stats[2:2 + len(names)], stats[2 + len(names):]
        loss_sum, contribution = (tail[0], tail[1:]) if loss is not None else (None, [])
        metrics = {name: total / weight for name, total in zip(names, sums, strict=True)
                   if weight > 0 and math.isfinite(total / weight)}  # fmt: skip
        rows.append(RowSummary(
            metrics=metrics, weight=weight if is_token_weighted else (1.0 if weight > 0 else 0.0),
            token_count=int(round(tokens)), mask_sha256=hash_mask(flags), loss_sum=loss_sum,
            contribution=contribution[0] if contribution and source is not None else None,
            contribution_source=source, normalizer=normalizers[index] if source is ContributionSource.PROBE_REDUCER else None,
            scale=scale if source is not None else None,
        ))  # fmt: skip
    return rows


def _summarize_torch(values, mask, weights, loss, reduction, normalizer, scale) -> tuple[list[list[float]], list[list[float]]]:
    import torch

    flags = mask.detach().to(torch.float64)
    token_weights = flags if weights is None else weights.detach().to(torch.float64) * flags
    columns = [token_weights.sum(-1), flags.sum(-1)]
    columns += [(values[name].detach().to(torch.float64) * token_weights).sum(-1) for name in values]
    if loss is not None:
        columns.append((values[loss].detach().to(torch.float64) * flags).sum(-1))
    if loss is not None and reduction is not None:
        per_token = values[loss].detach().clone().requires_grad_(True)
        with torch.enable_grad():
            objective = reduction(per_token, mask)
            (gradient,) = torch.autograd.grad(objective, per_token)
        columns.append((gradient.to(torch.float64) * per_token.detach().to(torch.float64)).sum(-1) * (scale or 1.0))
    elif loss is not None and normalizer is not None:
        divisor = torch.as_tensor(normalizer, dtype=torch.float64, device=flags.device)
        columns.append((values[loss].detach().to(torch.float64) * flags).sum(-1) / divisor * (scale or 1.0))
    # One copy to the host for the whole micro-batch: the stats and the masks (for their digests) together.
    joined = torch.cat([torch.stack(columns, dim=1), flags], dim=1).cpu().tolist()
    width = len(columns)
    return [row[:width] for row in joined], [row[width:] for row in joined]


def _summarize_lists(values, mask, weights, loss, normalizer, scale) -> tuple[list[list[float]], list[list[float]]]:
    flags = [[1.0 if flag else 0.0 for flag in row] for row in mask]
    normalizers = _get_normalizers(normalizer, len(flags))
    table = []
    for index, row in enumerate(flags):
        token_weights = row if weights is None else [float(w) * f for w, f in zip(weights[index], row, strict=True)]
        stats = [sum(token_weights), sum(row)]
        stats += [sum(float(v) * w for v, w in zip(values[name][index], token_weights, strict=True)) for name in values]
        if loss is not None:
            total = sum(float(v) * f for v, f in zip(values[loss][index], row, strict=True))
            stats.append(total)
            if normalizer is not None:
                stats.append(total / normalizers[index] * (scale or 1.0))
        table.append(stats)
    return table, flags
