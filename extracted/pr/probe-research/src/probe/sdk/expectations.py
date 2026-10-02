"""Declared metric ranges, client side: the shapes `expect()` accepts.

``probe.expect({"val/acc": (0.5, 1.0), "train/loss": (None, 20)})`` tells the
server where a metric should stay; the server's `out_of_range` detector emails
the run's creator the first time a value crosses. It is an ADD-ON: a script
that never calls it behaves exactly as before, and a call can never break the
script -- a malformed entry is dropped with a warning, and delivery is
fail-open like ``log()``.

Accepted per key:

* ``(lo, hi)`` or ``[lo, hi]`` -- either end ``None`` for "no limit that side";
* ``{"min": lo, "max": hi}`` -- either key may be absent;
* ``None`` -- remove the range this run declared for that key.

The server's rules (app/findings/expectations.py) are mirrored here so a bad
entry is reported at the call site, where the traceback still points at it.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

#: Mirrors the server (`MAX_EXPECTATION_KEY_CHARS`, `MAX_EXPECTATIONS_PER_RUN`).
MAX_KEY_CHARS = 256
MAX_PER_CALL = 100


def _bound(value: Any) -> tuple[bool, float | None]:
    """(ok, value) for one end of a range."""
    if value is None:
        return True, None
    if isinstance(value, bool | str | bytes):
        return False, None  # True is 1 to Python and "0.5" parses; neither is a bound
    if not isinstance(value, int | float):
        try:  # numpy scalars and the like
            value = float(value)
        except (TypeError, ValueError):
            return False, None
    value = float(value)
    return (math.isfinite(value), value if math.isfinite(value) else None)


def _one(spec: Any) -> tuple[dict[str, float | None] | None, str | None]:
    """(wire entry, problem). A None spec is a removal and has no problem."""
    if isinstance(spec, Mapping):
        unknown = set(spec) - {"min", "max"}
        if unknown:
            return None, f"unknown field(s) {sorted(unknown)}; use 'min' and 'max'"
        lo_raw, hi_raw = spec.get("min"), spec.get("max")
    elif isinstance(spec, tuple | list) and len(spec) == 2:
        lo_raw, hi_raw = spec
    else:
        return None, "expected (min, max), {'min': .., 'max': ..} or None"
    ok_lo, lo = _bound(lo_raw)
    ok_hi, hi = _bound(hi_raw)
    if not (ok_lo and ok_hi):
        return None, "bounds must be finite numbers or None"
    if lo is None and hi is None:
        return None, "a range needs a min, a max, or both"
    if lo is not None and hi is not None and lo > hi:
        return None, f"min {lo} is above max {hi}"
    return {"min": lo, "max": hi}, None


def normalize(ranges: Any) -> tuple[dict[str, dict[str, float | None] | None], list[str]]:
    """(the wire map for ``metric_expectations``, one problem string per
    dropped entry). Never raises."""
    if not isinstance(ranges, Mapping):
        return {}, [f"expect() takes a dict of metric ranges, got {type(ranges).__name__}"]
    wire: dict[str, dict[str, float | None] | None] = {}
    problems: list[str] = []
    for key, spec in ranges.items():
        if not isinstance(key, str) or not key or len(key) > MAX_KEY_CHARS:
            problems.append(f"{key!r}: a metric key must be a 1-{MAX_KEY_CHARS} character string")
            continue
        if spec is None:
            wire[key] = None
            continue
        entry, problem = _one(spec)
        if problem is not None:
            problems.append(f"{key!r}: {problem}")
            continue
        wire[key] = entry
    if len(wire) > MAX_PER_CALL:
        problems.append(f"at most {MAX_PER_CALL} ranges per call; the rest were dropped")
        wire = dict(list(wire.items())[:MAX_PER_CALL])
    return wire, problems
