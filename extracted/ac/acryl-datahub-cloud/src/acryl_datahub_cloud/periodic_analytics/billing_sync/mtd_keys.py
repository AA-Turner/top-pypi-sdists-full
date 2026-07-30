"""MTD / publish ledger keys for metronome_dimensions breakout.

Flat metrics use the metric name as the key. Dimensional metrics append
``\\x1f``-separated ``dim=value`` pairs so the existing Dict[str, int] MTD and
ledger stay string-keyed while BillingUsageRequest.eventType stays the base
metric name and dimensions land in properties.
"""

from typing import Dict, Iterable, Tuple

_DIM_SEP = "\x1f"


def format_mtd_key(metric_name: str, dimensions: Dict[str, str]) -> str:
    if not dimensions:
        return metric_name
    parts = [f"{k}={dimensions[k]}" for k in sorted(dimensions)]
    return metric_name + _DIM_SEP + _DIM_SEP.join(parts)


def parse_mtd_key(mtd_key: str) -> Tuple[str, Dict[str, str]]:
    if _DIM_SEP not in mtd_key:
        return mtd_key, {}
    metric_name, rest = mtd_key.split(_DIM_SEP, 1)
    dims: Dict[str, str] = {}
    for part in rest.split(_DIM_SEP):
        if "=" not in part:
            raise ValueError(f"invalid dimensional MTD key segment: {part!r}")
        key, value = part.split("=", 1)
        dims[key] = value
    return metric_name, dims


def base_metric_name(mtd_key: str) -> str:
    return parse_mtd_key(mtd_key)[0]


def is_flat_mtd_key(mtd_key: str) -> bool:
    return _DIM_SEP not in mtd_key


def mtd_has_dimensional_keys(mtd_keys: Iterable[str], metric_name: str) -> bool:
    """True when any key is a dimensional breakout of ``metric_name``."""
    prefix = metric_name + _DIM_SEP
    return any(key.startswith(prefix) for key in mtd_keys)
