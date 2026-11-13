"""Per-sample metrics as `POST /v1/runs/{id}/samples/points` takes them (twin: app/runs/samples/points): one call's
metrics flattened and kept like `run.log`'s (nested dicts to `/` keys, numbers only), each with its weight, checked
against the contract (`SampleMetricsIn`, `UpdateIn`) before anything is journaled. No fixed list of names."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from .....generated.samples.points import LOSS_FIELDS, SampleMetricsIn, UpdateIn
from ...metrics.values import _as_metric_value, _flatten

#: Where a sample sat in the update, beside the loss bookkeeping (`SampleMetricsIn`).
PLACE_FIELDS = ("eval_pass", "role", "rank", "micro_batch", "occurrence", "fragment", "fragments_expected")
ROW_FIELDS = frozenset((*PLACE_FIELDS, *LOSS_FIELDS))
#: Optional bookkeeping numbers (a row's or an update record's): NaN or infinite (a skipped update's loss) is sent as
#: unknown, never refused with the whole record (the contract takes only finite numbers).
_OPTIONAL_NUMBERS = frozenset({"loss_sum", "normalizer", "scale", "contribution", "reported_loss"})
#: Optional bookkeeping maps, flattened like `run.log` with each non-finite entry left out.
_OPTIONAL_MAPS = frozenset({"contribution_terms", "metrics", "batch_terms", "denominators"})


def _flatten_map(values: Mapping[str, Any], known: set[str]) -> dict[str, Any]:
    """Nested mappings to `/` keys, as `run.log` does (a mapping kept whole is dropped here: not a number)."""
    if any(isinstance(value, Mapping) for value in values.values()):
        values = _flatten(values, known=known)[0]
    return {str(key): value for key, value in values.items()}


def to_numbers(metrics: Mapping[str, Any], known: set[str]) -> tuple[dict[str, float], list[str]]:
    """The finite numbers of one call by flat key, and the keys left out (not a number, NaN or infinite: a weighted
    sum cannot carry them)."""
    kept: dict[str, float] = {}
    left: list[str] = []
    for key, value in _flatten_map(metrics, known).items():
        number = _as_metric_value(value)
        if number is None or not math.isfinite(number):
            left.append(key)
        else:
            kept[key] = number
    return kept, left


def keep_finite(fields: Mapping[str, Any], known: set[str]) -> tuple[dict[str, Any], list[str]]:
    """`fields` with each optional bookkeeping number that is NaN or infinite dropped (unknown) and each map's
    non-finite entries left out, and the names dropped (`name` or `name/key`)."""
    kept: dict[str, Any] = {}
    dropped: list[str] = []
    for name, value in fields.items():
        if name in _OPTIONAL_MAPS and isinstance(value, Mapping):
            kept[name], left = to_numbers(value, known)
            dropped += [f"{name}/{key}" for key in left]
            continue
        number = _as_metric_value(value) if name in _OPTIONAL_NUMBERS and value is not None else None
        if number is not None and not math.isfinite(number):
            dropped.append(name)
            continue
        kept[name] = value
    return kept, dropped


def _pick_per_key(given: Any, keys: list[str], known: set[str]) -> dict[str, Any]:
    """One value for every key, or a mapping (nested like the metrics) naming some of them."""
    if given is None:
        return {}
    if isinstance(given, Mapping):
        flat = _flatten_map(given, known)
        return {key: flat[key] for key in keys if key in flat}
    return dict.fromkeys(keys, given)


def build_point_row(
    sample_key: str, metrics: Mapping[str, Any], *, step: int, update: int | None, split: str | None,
    weights: Any, agg: Any, fields: Mapping[str, Any], known: set[str],
) -> tuple[dict, list[str]]:  # fmt: skip
    """One `SampleMetricsIn` as sent (only the fields set), and the keys and bookkeeping left out (not finite).
    ``weights`` and ``agg``: one for every key, or a mapping by key. ``fields``: the row's place and loss bookkeeping.
    Raises on a bad row."""
    stray = sorted(set(fields) - ROW_FIELDS)
    if stray:
        raise TypeError(f"log_metrics() takes {', '.join(sorted(ROW_FIELDS))}; not {', '.join(stray)}")
    numbers, left = to_numbers(metrics, known)
    fields, dropped = keep_finite(fields, known)
    left += dropped
    keys = list(numbers)
    per_weight = _pick_per_key(weights, keys, known)
    values: dict[str, Any] = {}
    for key, number in numbers.items():
        weight = per_weight.get(key)
        values[key] = number if weight is None else {"value": number, "weight": float(weight)}
    row: dict[str, Any] = {"key": str(sample_key), "step": step, "metrics": values}
    if update is not None:
        row["update"] = update
    if split is not None:
        row["split"] = str(split)
    declared = _pick_per_key(agg, keys, known)
    if declared:
        row["agg"] = {key: str(value) for key, value in declared.items()}
    row.update({name: value for name, value in fields.items() if value is not None})
    model = SampleMetricsIn.model_validate(row)
    return model.model_dump(mode="json", exclude_unset=True), left


def build_update_row(step: int, update: int | None, level: str, fields: Mapping[str, Any],
                     known: set[str]) -> tuple[dict, list[str]]:  # fmt: skip
    """One `UpdateIn` as sent (an eval pass: no update, `split="eval"`, `eval_pass`), its `metrics`, `batch_terms`
    and `denominators` flattened like `run.log`'s, and the bookkeeping left out (not finite: a skipped update's NaN
    loss is unknown, the record still goes). Raises on a bad row."""
    row: dict[str, Any] = {"step": step, "level": str(level)}
    if update is not None:
        row["update"] = update
    kept, dropped = keep_finite({name: value for name, value in fields.items() if value is not None}, known)
    row.update(kept)
    return UpdateIn.model_validate(row).model_dump(mode="json", exclude_unset=True), dropped
