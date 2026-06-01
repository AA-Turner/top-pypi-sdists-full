"""Multi-run aggregation for the eval harness.

Single-run metrics are noisy on small denominators — a one-call swing
on a 4-denominator metric is a 0.25 swing. Per the noise-floor study
in the project's DECISIONS log, per-metric noise floors run M1 ~0.20,
M2 ~0.10, M3 ~0.20, M4 ~0.05, M5 ~0.05 on Haiku 4.5 against the
Phase 1 fixtures.

`--runs N` on `python -m evals run` executes N independent pipeline
runs against the same fixture and aggregates the per-metric scores
into mean / stddev / min / max. Use it when evaluating a prompt
change: a 3- or 5-run aggregate before-and-after the change has
honest signal, where a single run/run comparison usually doesn't.

Aggregation discipline:
- Skip metrics with denominator == 0 (no signal in that run).
- Empty-input -> empty-output (no aggregate emitted).
- stddev computed with population formula (not sample) since these
  are full enumerations of the runs we did, not samples from a
  larger population.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from evals.metrics import MetricResult


@dataclass(frozen=True)
class AggregateMetric:
    """Per-metric aggregate across N independent runs."""

    name: str
    n_runs: int
    mean: float
    stddev: float
    min_score: float
    max_score: float
    scores: tuple[float, ...]


def aggregate_runs(runs: Iterable[Iterable[MetricResult]]) -> list[AggregateMetric]:
    """Aggregate per-metric scores across N runs.

    Each run contributes its scores by name. Metrics with zero denominator
    in a given run are skipped for that run (they had no signal to
    contribute), but other runs' scores for the same metric still count.
    A metric that has zero denominator in EVERY run is omitted from the
    aggregate entirely.
    """
    by_name: dict[str, list[float]] = {}
    for run in runs:
        for m in run:
            if m.denominator <= 0:
                continue
            by_name.setdefault(m.name, []).append(m.score)

    out: list[AggregateMetric] = []
    for name, scores in by_name.items():
        n = len(scores)
        mean = sum(scores) / n
        # Population variance (we have the full set of runs, not a sample).
        var = sum((s - mean) ** 2 for s in scores) / n
        out.append(
            AggregateMetric(
                name=name,
                n_runs=n,
                mean=mean,
                stddev=var**0.5,
                min_score=min(scores),
                max_score=max(scores),
                scores=tuple(scores),
            )
        )
    return out


def format_aggregate_block(aggs: list[AggregateMetric]) -> str:
    """Format the aggregate as a multi-line text block for the run summary."""
    if not aggs:
        return "(no metrics with signal across the runs)"
    lines = []
    for a in aggs:
        scores_str = ", ".join(f"{s:.3f}" for s in a.scores)
        lines.append(
            f"  {a.name:24s} mean={a.mean:.3f}  stddev={a.stddev:.3f}  "
            f"min={a.min_score:.3f}  max={a.max_score:.3f}  (n={a.n_runs})  "
            f"[{scores_str}]"
        )
    return "\n".join(lines)
