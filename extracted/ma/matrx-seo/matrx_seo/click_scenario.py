"""Click-share scenarios — what a search position is worth in clicks, on a stated curve.

Pure: no I/O, no model. ``traffic_scenario(volume, current_pos, target_pos)``
multiplies a search volume by the expected click-through rate at each position
and returns the clicks now, at the target, and the difference.

Honesty rules (OpenSEO seo-audit skill, "size the benefit honestly"):

* Search volume is not visits. Every figure is **hypothetical, from an average
  click curve** — :data:`SCENARIO_LABEL` rides every result.
* Missing volume or position is said, never invented: an unknown volume gives
  no clicks at all; an unknown current position gives the target's clicks as
  *total potential* clicks, never *additional* ones.

The curve is :data:`matrx_scraper.click_curve.GSC_EXPECTED_CTR_CURVE` — the
platform's one declaration — and the default of the ``seo.click_curve`` knob,
which an organization overrides with its own JSON array; the host reads the knob
and passes the curve in.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

import math

from matrx_scraper.click_curve import (
    GSC_EXPECTED_CTR_CURVE,
    expected_ctr_for_position,
    validate_click_curve,
)

#: The label every scenario carries, verbatim.
SCENARIO_LABEL = "hypothetical, from an average click curve"

#: Said wherever a scenario's target is no better than where the keyword already ranks.
ALREADY_AT_TARGET = "already at or above the target position, so there is no gain to size"

#: The knob holding the curve (feature ``seo``).
CLICK_CURVE_KNOB = "click_curve"


def parse_click_curve(raw: Any) -> tuple[float, ...]:
    """A knob value as a curve, or ValueError naming ``seo.click_curve`` and the
    reason (the rules: :func:`matrx_scraper.click_curve.click_curve_problem`)."""
    return validate_click_curve(raw)


def _rank(position: float) -> int:
    return max(1, math.floor(position + 0.5))


def _clicks(volume: float, position: float, curve: Sequence[float]) -> float:
    return round(volume * expected_ctr_for_position(position, curve), 1)


@dataclass(frozen=True, slots=True)
class TrafficScenario:
    volume: float | None
    current_position: float | None
    target_position: float | None
    ctr_now: float | None
    ctr_at_target: float | None
    clicks_now: float | None
    clicks_at_target: float | None
    delta: float | None
    missing: tuple[str, ...] = ()
    notes: tuple[str, ...] = field(default=())
    label: str = SCENARIO_LABEL
    already_at_target: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "volume": self.volume,
            "current_position": self.current_position,
            "target_position": self.target_position,
            "ctr_now": self.ctr_now,
            "ctr_at_target": self.ctr_at_target,
            "clicks_now": self.clicks_now,
            "clicks_at_target": self.clicks_at_target,
            "delta": self.delta,
            "missing": list(self.missing),
            "notes": list(self.notes),
            "already_at_target": self.already_at_target,
        }

    def compact(self) -> dict[str, Any]:
        """The per-row form for list reads (the label rides once, in the read's notice).
        A row already at or above its target carries the note that says so."""
        row: dict[str, Any] = {
            "now": self.clicks_now,
            "at_target": self.clicks_at_target,
            "gain": self.delta,
            "target_position": self.target_position,
        }
        if self.already_at_target:
            row["note"] = ALREADY_AT_TARGET
        return row


def traffic_scenario(
    volume: float | None,
    current_pos: float | None,
    target_pos: float | None,
    curve: Sequence[float] = GSC_EXPECTED_CTR_CURVE,
) -> TrafficScenario:
    """Expected clicks now, at ``target_pos``, and the delta — on ``curve``.

    ``volume`` is searches (or impressions) over whatever period it covers; the
    clicks are over the same period. Positions are rounded half-up to a rank."""
    if volume is not None and volume < 0:
        raise ValueError("volume cannot be negative")
    for name, pos in (("current position", current_pos), ("target position", target_pos)):
        if pos is not None and pos <= 0:
            raise ValueError(f"{name} must be 1 or more (1 = the top result)")
    missing: list[str] = []
    notes: list[str] = []
    if volume is None:
        missing.append("volume")
        notes.append("Search volume is unknown, so no clicks are estimated.")
    if target_pos is None:
        missing.append("target_position")
        notes.append("No target position was given, so there is no scenario to size.")
    if current_pos is None:
        missing.append("current_position")
        notes.append(
            "The current position is unknown (not ranking, or never checked): clicks_at_target "
            "is total potential clicks, not additional clicks."
        )
    ctr_now = expected_ctr_for_position(current_pos, curve) if current_pos is not None else None
    ctr_target = expected_ctr_for_position(target_pos, curve) if target_pos is not None else None
    now = _clicks(volume, current_pos, curve) if volume is not None and current_pos is not None else None
    at_target = _clicks(volume, target_pos, curve) if volume is not None and target_pos is not None else None
    above = (
        current_pos is not None
        and target_pos is not None
        and _rank(current_pos) <= _rank(target_pos)
    )
    if above:
        # Never a negative "gain": the target is no better than where it ranks now.
        delta = None
        notes.append(ALREADY_AT_TARGET[0].upper() + ALREADY_AT_TARGET[1:] + ".")
    else:
        delta = round(at_target - now, 1) if now is not None and at_target is not None else None
    return TrafficScenario(
        volume=volume,
        current_position=current_pos,
        target_position=target_pos,
        ctr_now=ctr_now,
        ctr_at_target=ctr_target,
        clicks_now=now,
        clicks_at_target=at_target,
        delta=delta,
        missing=tuple(missing),
        notes=tuple(notes),
        already_at_target=above,
    )


__all__ = [
    "ALREADY_AT_TARGET",
    "CLICK_CURVE_KNOB",
    "SCENARIO_LABEL",
    "TrafficScenario",
    "parse_click_curve",
    "traffic_scenario",
]
