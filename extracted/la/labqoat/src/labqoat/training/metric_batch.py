"""Finite step-aligned training metrics."""

import math
import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class MetricBatch:
    """One immutable batch of uniquely named finite scalar metrics."""

    step: int
    metrics: tuple[tuple[str, float], ...]

    def __post_init__(self) -> None:
        """Validate steps, stable names, and finite values."""
        if self.step < 0:
            raise ValueError("Metric step cannot be negative")
        names = tuple(name for name, _ in self.metrics)
        invalid = [name for name in names if re.fullmatch(r"[a-z][a-z0-9_.-]*(?:/[a-z0-9_.-]+)*", name) is None]
        if invalid:
            raise ValueError(
                f"Metric names must be lowercase letters, digits, _ . - and / between parts, starting with a letter; "
                f"got {', '.join(map(repr, invalid[:5]))}"
            )
        if len(names) != len(set(names)):
            raise ValueError("Metric names must be unique")
        if any(not math.isfinite(value) for _, value in self.metrics):
            raise ValueError(
                f"Metric values must be finite; got {', '.join(f'{n}={v}' for n, v in self.metrics if not math.isfinite(v))}"
            )
