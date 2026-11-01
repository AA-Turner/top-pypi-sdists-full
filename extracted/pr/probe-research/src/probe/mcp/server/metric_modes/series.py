"""`metrics` mode=series: smoothed, budgeted curves across runs."""

from __future__ import annotations
from typing import Any
from ...tools.tools import ResearchReadService

#: Delivery state the series route reads beside the caller's arguments: which
#: series the page starts at (the native cursor) and the budget it fits to.
#: Underscored because they are never caller arguments and must not collide
#: with one -- `_metric_args_for_mode` has already validated those.
_SERIES_OFFSET = "_series_offset"
_SERIES_BUDGET = "_series_budget"


def _metric_route_series(s: ResearchReadService, a: dict[str, Any]) -> dict:
    return s.metrics_series(
        a["run_ids"],
        a["keys"],
        step_from=a.get("step_from"),
        step_to=a.get("step_to"),
        smoothing=a.get("smoothing"),
        max_points=a.get("max_points"),
        offset=a.get(_SERIES_OFFSET, 0),
        token_budget=a.get(_SERIES_BUDGET, 2000),
    )
