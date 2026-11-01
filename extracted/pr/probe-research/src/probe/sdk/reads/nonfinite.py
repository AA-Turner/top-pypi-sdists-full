"""NaN, +inf and -inf on the metric read path.

JSON has no NaN/Infinity, so raw point reads (``GET /v1/runs/{id}/metrics``,
``/metrics/export``) send a non-finite value as ``value: null`` plus a
``nonfinite`` marker: ``"nan"``, ``"inf"`` or ``"-inf"``. :func:`to_float` restores
the float (``client.run_metrics(...)`` returns ``float("nan")``, as W&B history
does). A server older than the marker sends bare nulls, which stay None.

:func:`to_wire` is the inverse for strict-JSON writers (MCP tools, CLI JSON): back
to ``None`` plus marker. A finite point drops the empty ``nonfinite: null`` key
(about 5 tokens a point, +5.7%, on the MCP ``metrics`` tool).
"""

from __future__ import annotations

import math
from typing import Any

NONFINITE_KEY = "nonfinite"
_FLOATS = {"nan": math.nan, "inf": math.inf, "-inf": -math.inf}


def to_float(point: dict[str, Any]) -> dict[str, Any]:
    """Rebuild ``point["value"]`` from its ``nonfinite`` marker, in place.

    The marker stays on the point, so :func:`to_wire` can write it back out."""
    if point.get("value") is None and point.get(NONFINITE_KEY) in _FLOATS:
        point["value"] = _FLOATS[point[NONFINITE_KEY]]
    return point


def to_wire(point: dict[str, Any]) -> dict[str, Any]:
    """A strict-JSON copy: a non-finite ``value`` becomes None with the marker; any other
    point only loses an empty ``nonfinite: null`` key."""
    value = point.get("value")
    if not isinstance(value, float) or math.isfinite(value):
        if NONFINITE_KEY in point and point[NONFINITE_KEY] is None:
            return {k: v for k, v in point.items() if k != NONFINITE_KEY}
        return point
    if math.isnan(value):
        marker = "nan"
    else:
        marker = "inf" if value > 0 else "-inf"
    return {**point, "value": None, NONFINITE_KEY: marker}
