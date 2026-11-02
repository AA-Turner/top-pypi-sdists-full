"""Cube router GPS positions from Peplink InControl2, for the console's GPS location row.

`client.py` carries the rules: `ts` is group-local time, only `last_loc` points are GPS
positions, "never reported" differs from "not found", and failure is "unavailable".
It also says how the index is refreshed, since IC2 allows one live token per client.
"""

from __future__ import annotations

from cube_cloud.ic2.client import (
    Ic2Error,
    Ic2Index,
    Position,
    invalidate,
    is_enabled,
    normalize_serial,
    positions,
    stats,
)

__all__ = [
    "Ic2Error",
    "Ic2Index",
    "Position",
    "invalidate",
    "is_enabled",
    "normalize_serial",
    "positions",
    "stats",
]
