"""Global weighted score (0-100) per instance type: reliability + cost + performance.

The score unifies every signal into one comparable number so the best-scoring
types are the ones to put in the node group mix. Nothing is hard-excluded by a
reliability signal — they are *weighted*, never gates (only shape / arch /
family are structural filters upstream).

Axes and weights (per ``--goal``; reliability / cost / performance, summing to 1):

* ``balanced`` (default) — 0.65 / 0.20 / 0.15  (reliability-led)
* ``cost``               — 0.40 / 0.45 / 0.15
* ``evictions``          — 0.80 / 0.12 / 0.08

Inside **reliability**, the two **per-type** signals are weighted by how much we
trust them (observed real history > AWS's global predictive rate, which proved
unreliable for our account):

* observed interruption rate — 0.50
* Spot Advisor predictive    — 0.15

The **Spot Placement Score** is deliberately *not* a per-type signal here: AWS
scores a whole diversified *request* (a set of ≥3 instance types) as one
configuration and returns a single pooled score — a one- or two-type request is
always scored low. It is therefore evaluated per **mix** (current vs recommended,
per node group), upstream of this per-type score, and surfaced as a node-group
indicator rather than folded into each type.

Weights are renormalized over the signals actually available for a type. A
never-launched candidate (no observed rate) therefore leans on the predictive
rate alone; when both are present they apply at **0.50 / 0.15** renormalized.
"""

from dataclasses import dataclass

GOAL_WEIGHTS: dict[str, tuple[float, float, float]] = {
    "balanced": (0.65, 0.20, 0.15),
    "cost": (0.40, 0.45, 0.15),
    "evictions": (0.80, 0.12, 0.08),
}

REL_W_OBSERVED = 0.50
REL_W_PREDICTIVE = 0.15

_RATE_MIDPOINT = {0: 2.5, 1: 7.5, 2: 12.5, 3: 17.5, 4: 25.0}


@dataclass
class Signals:
    """The scoring inputs for one instance type (any may be ``None``)."""

    rate_index: int | None  # Spot Advisor bucket 0-4
    observed_rate: float | None  # observed interruptions %, evictions/launches
    price: float | None  # $/h for the relevant capacity (spot or on-demand)
    perf: float | None  # effective compute (vCPU × GHz × IPC)


def reliability(s: Signals) -> float:
    """Reliability sub-score in [0, 1] (1 = most reliable), weighted + renormalized."""
    parts: list[tuple[float, float]] = []
    if s.observed_rate is not None:
        # Steep, aligned on AWS's worst predictive bucket (~25%): an observed
        # rate of 25%+ → 0 reliability (the pool is effectively unusable).
        parts.append((max(0.0, 1.0 - s.observed_rate / 25.0), REL_W_OBSERVED))
    if s.rate_index is not None:
        parts.append((max(0.0, 1.0 - _RATE_MIDPOINT.get(s.rate_index, 25.0) / 25.0), REL_W_PREDICTIVE))
    if not parts:
        return 0.5
    total_w = sum(w for _, w in parts)
    return sum(v * w for v, w in parts) / total_w


def _normalize(values: list[float | None], *, higher_better: bool) -> list[float]:
    """Min-max normalize to [0, 1] within the set. Missing → 0.5 (neutral)."""
    present = [v for v in values if v is not None]
    if not present:
        return [0.5] * len(values)
    lo, hi = min(present), max(present)
    out: list[float] = []
    for v in values:
        if v is None:
            out.append(0.5)
        elif hi == lo:
            out.append(1.0)
        else:
            x = (v - lo) / (hi - lo)
            out.append(x if higher_better else 1.0 - x)
    return out


def global_scores(signals: list[Signals], goal: str) -> list[float]:
    """Return a 0-100 score per type (higher = better to put in the mix).

    Cost and performance are min-max normalized **within the candidate set**, so
    scores rank candidates of the same shape against each other.
    """
    w_rel, w_cost, w_perf = GOAL_WEIGHTS.get(goal, GOAL_WEIGHTS["balanced"])
    cost = _normalize([s.price for s in signals], higher_better=False)
    perf = _normalize([s.perf for s in signals], higher_better=True)
    return [
        round(100.0 * (w_rel * reliability(s) + w_cost * c + w_perf * p), 1)
        for s, c, p in zip(signals, cost, perf, strict=True)
    ]
