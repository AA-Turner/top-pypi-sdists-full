"""`metrics` mode=points: raw points, paged by id (metrics_export)."""

from __future__ import annotations
from typing import Any
from ...tools.tools import ResearchReadService


def _metric_route_points(s: ResearchReadService, a: dict[str, Any]) -> dict:
    return s.metrics_export(
        a["run_id"],
        key=a.get("key"),
        kind=a.get("kind"),
        step_from=a.get("step_from"),
        step_to=a.get("step_to"),
        after_id=a.get("after_id"),
        limit=a.get("limit"),
    )
