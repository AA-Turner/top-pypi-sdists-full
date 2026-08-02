"""Data model for the ops KPI snapshot.

Metric keys follow the contract in the ``stats-kpi-ops`` skill
(``references/kpi-definitions.md``) — the sheet, the snapshot history and
the future cockpit all consume these same keys.
"""

import dataclasses
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Metric:
    """One collected KPI value, or the reason it could not be collected."""

    key: str
    value: float | int | None
    unit: str
    error: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class KpiSnapshot:
    """All metrics collected over a single time window."""

    since: str  # YYYY-MM-DD, inclusive
    until: str  # YYYY-MM-DD, exclusive
    metrics: dict[str, Metric] = field(default_factory=dict)

    def add(self, metric: Metric) -> None:
        self.metrics[metric.key] = metric

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
