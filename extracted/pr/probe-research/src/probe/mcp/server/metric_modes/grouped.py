"""`metrics` mode=grouped: aggregated by coordinate (metrics_grouped)."""

from __future__ import annotations
from typing import Any
from ...tools.tools import ResearchReadService


def _metric_route_grouped(s: ResearchReadService, a: dict[str, Any]) -> dict:
    return s.metrics_grouped(
        a["run_id"],
        a["key"],
        kind=a.get("kind"),
        agg=a.get("agg"),
        by=a.get("by"),
        where=a.get("where"),
        step_bucket=a.get("step_bucket"),
        step_from=a.get("step_from"),
        step_to=a.get("step_to"),
        max_rows=a.get("max_rows"),
    )
