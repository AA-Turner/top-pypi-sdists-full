"""NaN, +inf and -inf on the metric read path.

JSON has no NaN or Infinity, so a server's raw point reads (``GET
/v1/runs/{id}/metrics`` and ``/metrics/export``) send a stored non-finite value
as ``value: null`` beside a ``nonfinite`` marker: ``"nan"``, ``"inf"`` or
``"-inf"``. :func:`to_float` puts the float back for Python callers, so
``client.run_metrics(...)`` returns ``float("nan")`` where the run logged one,
as ``wandb.Api().run(...).history()`` does. A server older than the marker sends
bare nulls, which stay None: there is nothing to rebuild them from.

:func:`to_wire` is the inverse, for writers that must emit strict JSON (the MCP
tools, the CLI's JSON output): a non-finite value goes back to ``None`` beside
its marker, which is the shape the server sent. A finite point drops the
``nonfinite: null`` key: it says nothing, and on the MCP ``metrics`` tool it
cost about 5 tokens a point (+5.7%).
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
    """A copy safe for strict JSON: a non-finite ``value`` becomes None and the
    marker names it. Any other point loses an empty ``nonfinite: null`` key and
    is otherwise unchanged."""
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
