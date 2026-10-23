"""THE average click curve — the platform's one declaration of expected organic
CTR by search position.

It lives in matrx-scraper because matrx-seo depends on matrx-scraper and never
the reverse: the GSC CTR check here reads it, and matrx_seo's click scenarios
(``matrx_seo.click_scenario``) import it. The ``seo.click_curve`` knob's
default is exactly :data:`GSC_EXPECTED_CTR_CURVE`; an organization that supplies
its own curve passes it as ``curve``. Pure — no I/O.
"""

from __future__ import annotations

import math
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Any

#: THE average click curve — expected organic CTR by average position, ONE
#: declaration for the platform (see the module docstring for why it
#: lives here).
#: Entry ``i`` is position ``i + 1``; the LAST entry applies to every deeper
#: position. Positions 11–20 (page two) share one flat value and anything deeper
#: another, because below page one the curve is noise, not signal. It is also the
#: default of the ``seo.click_curve`` knob, where an organization supplies its own.
GSC_EXPECTED_CTR_CURVE: tuple[float, ...] = (
    0.28,
    0.15,
    0.11,
    0.08,
    0.06,
    0.05,
    0.04,
    0.032,
    0.028,
    0.025,
    *(0.015,) * 10,
    0.008,
)


def expected_ctr_for_position(
    position: float, curve: Sequence[float] = GSC_EXPECTED_CTR_CURVE
) -> float:
    """The CTR a page at this average position would normally earn on ``curve``.

    The position is rounded half-up to a whole rank (2.5 → 3, 1.4 → 1) and
    clamped to 1; a rank past the curve's end reads its last entry."""
    if not curve:
        raise ValueError("a click curve needs at least one value")
    rank = max(1, math.floor(position + 0.5))
    return float(curve[min(rank, len(curve)) - 1])


#: A curve covers at least page one and at most this many positions.
CURVE_MIN_LENGTH = 10
CURVE_MAX_LENGTH = 100


def click_curve_problem(raw: Any) -> str | None:
    """Why ``raw`` is not a usable click curve, in one sentence — or None when it is.

    The rules (enforced at READ time only — validation offers, never blocks, so a
    bad stored value is read as the platform curve with a notice): a JSON array of
    CURVE_MIN_LENGTH–CURVE_MAX_LENGTH numbers, each greater than 0 and at most 1
    (a 0 would make every expected-click ratio a division by zero), never
    rising from one position to the next."""
    if not isinstance(raw, (list, tuple)):
        return "it must be a list of click-through rates, position 1 first"
    if not CURVE_MIN_LENGTH <= len(raw) <= CURVE_MAX_LENGTH:
        return (
            f"it has {len(raw)} values; it needs {CURVE_MIN_LENGTH} to {CURVE_MAX_LENGTH} "
            "(position 1 first; the last value covers every deeper position)"
        )
    previous: float | None = None
    for index, value in enumerate(raw, start=1):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return f"value {index} is not a number ({value!r})"
        if not 0 < float(value) <= 1:
            return f"value {index} is {value}; each rate must be greater than 0 and at most 1"
        if previous is not None and float(value) > previous:
            return f"value {index} ({value}) is higher than value {index - 1} ({previous}); a lower position never earns more clicks"
        previous = float(value)
    return None


def validate_click_curve(raw: Any) -> tuple[float, ...]:
    """``raw`` as a curve, or ValueError naming the knob and the reason."""
    problem = click_curve_problem(raw)
    if problem is not None:
        raise ValueError(f"seo.click_curve is not a usable click curve: {problem}.")
    return tuple(float(v) for v in raw)


@dataclass(frozen=True, slots=True)
class ResolvedClickCurve:
    curve: tuple[float, ...]
    #: Set when the organization's curve was unusable and the platform curve was
    #: used instead — say it wherever the curve's numbers are shown.
    notice: str | None = None


def curve_or_platform(raw: Any) -> ResolvedClickCurve:
    """Read time: a bad stored curve never crashes a read — the platform curve
    answers, with a visible notice naming the reason."""
    problem = click_curve_problem(raw)
    if problem is None:
        return ResolvedClickCurve(tuple(float(v) for v in raw))
    return ResolvedClickCurve(
        GSC_EXPECTED_CTR_CURVE,
        f"This organization's click curve (seo.click_curve) is unusable — {problem} — so the "
        "platform's average curve was used.",
    )


#: The host's per-organization curve: ``(organization_id, site_id) -> the stored
#: seo.click_curve value``. The host (aidream) installs its knob ladder, so ONE
#: organization's curve applies everywhere the platform reads a click curve.
#: Standalone, there is no knob system and the package's own declaration answers.
ClickCurveResolver = Callable[[str, str | None], Awaitable[Any]]

_resolver: ClickCurveResolver | None = None


def set_click_curve_resolver(resolver: ClickCurveResolver | None) -> None:
    """Install (or clear, with None) the host's click-curve resolver."""
    global _resolver
    _resolver = resolver


async def resolve_click_curve(organization_id: str, site_id: str | None = None) -> ResolvedClickCurve:
    """The curve THIS organization (and site) uses. An unusable stored value falls
    back to the platform curve WITH a notice; a resolver that cannot read at all
    raises, for the caller to report as itself."""
    if _resolver is None:
        return ResolvedClickCurve(GSC_EXPECTED_CTR_CURVE)
    return curve_or_platform(await _resolver(organization_id, site_id))


__all__ = [
    "CURVE_MAX_LENGTH",
    "CURVE_MIN_LENGTH",
    "GSC_EXPECTED_CTR_CURVE",
    "ClickCurveResolver",
    "ResolvedClickCurve",
    "click_curve_problem",
    "curve_or_platform",
    "expected_ctr_for_position",
    "resolve_click_curve",
    "set_click_curve_resolver",
    "validate_click_curve",
]
