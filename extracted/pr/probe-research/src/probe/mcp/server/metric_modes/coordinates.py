"""`metrics` mode=coordinates: a run's coordinate axes."""

from __future__ import annotations
from typing import Any
from ...tools.tools import ResearchReadService


def _metric_route_coordinates(s: ResearchReadService, a: dict[str, Any]) -> dict:
    return s.run_coordinates(a["run_id"])
