from typing import Dict, List, Optional, Tuple

from acryl_datahub_cloud.periodic_analytics.billing_sync.mtd_keys import (
    base_metric_name,
)
from acryl_datahub_cloud.periodic_analytics.registry import MetronomeAggregation


class BillingValidationError(Exception):
    def __init__(self, reasons: List[str]) -> None:
        self.reasons = reasons
        # TG-6: billing totals must never regress below what was actually
        # billed, or omit a required metric — a failure here blocks the
        # close write and publish stages entirely.
        super().__init__("billing totals failed validation: " + "; ".join(reasons))


def _mtd_covers_metric(mtd: Dict[str, int], metric_name: str) -> bool:
    if metric_name in mtd:
        return True
    # Dimensional MTD keys: metric_name\x1fdim=value...
    prefix = metric_name + "\x1f"
    return any(key.startswith(prefix) for key in mtd)


def _sum_decrease_findings(
    name: str,
    value: int,
    prior: Optional[Dict[str, int]],
    ledger_baseline: Dict[str, int],
    allow_mtd_correction: bool,
) -> Tuple[Optional[str], Optional[str]]:
    """Return (hard_fail_reason, warning) for a SUM metric decrease check."""
    ledger_value = ledger_baseline.get(name)
    if ledger_value is not None and value < ledger_value:
        if allow_mtd_correction:
            return (
                None,
                f"{name}: MTD {value} is below the last billed ledger "
                f"value {ledger_value} — allow_mtd_correction permitted "
                "this regression as a signed adjustment",
            )
        return (
            f"{name} regressed below the billed ledger value: {value} < {ledger_value}",
            None,
        )
    if prior and name in prior and value < prior[name]:
        return (
            None,
            f"{name}: MTD {value} dipped below the prior close snapshot "
            f"{prior[name]}, but is still >= the billed ledger value — "
            "nothing already billed is contradicted",
        )
    return None, None


def validate_mtd(
    mtd: Dict[str, int],
    prior: Optional[Dict[str, int]],
    required_metrics: List[str],
    ledger_baseline: Dict[str, int],
    allow_mtd_correction: bool,
    metric_aggregations: Optional[Dict[str, MetronomeAggregation]] = None,
) -> List[str]:
    """Enforce TG-6 and return non-fatal warnings for the caller to report.

    The hard gate (I1) is the publish ledger — what was actually billed —
    not the computed close snapshot. A regression below the close snapshot
    that never made it into the ledger (e.g. a prior run's publish failed)
    contradicts nothing that was billed, so it's a warning, not a failure.
    A regression below the ledger is only permitted (C2) when
    `allow_mtd_correction` is set, and even then it's still reported as a
    warning so it shows up in operator-facing logs.

    Decrease / dip checks apply only to SUM metrics. MAX/LATEST gauges may
    legitimately fall below a prior high-water; publish logic handles those
    aggregation modes separately.

    Dimensional metronome metrics (MTD keys with embedded dim pairs) count as
    present for ``required_metrics`` when any key for that base name exists,
    or when the metric is listed but has zero traffic (no keys) — callers
    should only put flat-initialized metrics in required_metrics, or pass
    dimensional names that are allowed to be absent when idle.
    """
    aggregations = metric_aggregations or {}
    reasons: List[str] = []
    warnings: List[str] = []
    for name, value in mtd.items():
        if value < 0:
            reasons.append(f"{name}={value} is negative")
    for name in required_metrics:
        if name not in mtd and not _mtd_covers_metric(mtd, name):
            reasons.append(f"required metric {name} missing from MTD")
    for name, value in mtd.items():
        agg = aggregations.get(base_metric_name(name), aggregations.get(name, "sum"))
        if agg != "sum":
            continue
        reason, warning = _sum_decrease_findings(
            name, value, prior, ledger_baseline, allow_mtd_correction
        )
        if reason is not None:
            reasons.append(reason)
        if warning is not None:
            warnings.append(warning)
    if reasons:
        raise BillingValidationError(reasons)
    return warnings
