"""
How a metric's value is shown: `success` is the share of episodes whose @seq.step said they succeeded, a "rate" from
0 to 1 shown as a percentage; any other metric is the benchmark's own number, which declares no unit, shown as it is
.
"""
from __future__ import annotations



UNITS = {"success": "rate"}


def shown(value: float, unit: str | None) -> str:
    """One value: "70.0%" for a rate, "0.412 m" for a unit of its own, "0.412" for none."""
    if unit == "rate":
        return f"{float(value) * 100:.1f}%"
    return f"{float(value):.3f}" + (f" {unit}" if unit else "")
