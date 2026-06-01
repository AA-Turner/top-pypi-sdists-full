"""Tests for the multi-run aggregator (`--runs N` flag)."""

from __future__ import annotations

from evals.aggregate import (
    AggregateMetric,
    aggregate_runs,
    format_aggregate_block,
)
from evals.metrics import MetricResult


def _m(name: str, score: float, denominator: int = 1) -> MetricResult:
    """MetricResult with a single numerator scaled to the desired score.
    `denominator` lets tests exercise the zero-denominator skip path.
    """
    return MetricResult(
        name=name,
        score=score,
        numerator=int(score * denominator) if denominator > 0 else 0,
        denominator=denominator,
        notes="",
    )


def test_aggregate_single_run() -> None:
    """One run -> mean equals the run's score, stddev is 0."""
    runs = [[_m("m1", 0.8), _m("m2", 1.0)]]
    aggs = aggregate_runs(runs)
    by_name = {a.name: a for a in aggs}
    assert by_name["m1"].mean == 0.8
    assert by_name["m1"].stddev == 0.0
    assert by_name["m1"].n_runs == 1
    assert by_name["m2"].mean == 1.0


def test_aggregate_multi_run_mean_and_spread() -> None:
    """Three runs with known scores -> known mean / stddev / min / max."""
    runs = [
        [_m("status_precision", 0.6)],
        [_m("status_precision", 0.8)],
        [_m("status_precision", 1.0)],
    ]
    aggs = aggregate_runs(runs)
    assert len(aggs) == 1
    a = aggs[0]
    assert a.name == "status_precision"
    assert a.n_runs == 3
    assert abs(a.mean - 0.8) < 1e-9
    # Population stddev of [0.6, 0.8, 1.0] around mean 0.8 = sqrt(0.0267) ≈ 0.1633
    assert abs(a.stddev - 0.16329931618554519) < 1e-9
    assert a.min_score == 0.6
    assert a.max_score == 1.0
    assert a.scores == (0.6, 0.8, 1.0)


def test_aggregate_skips_zero_denominator_per_run() -> None:
    """A metric with zero denominator in one run shouldn't contribute,
    but its other-run scores still count."""
    runs = [
        [_m("manifest_quoting", 0.0, denominator=0)],  # no signal
        [_m("manifest_quoting", 1.0, denominator=2)],  # real signal
        [_m("manifest_quoting", 1.0, denominator=2)],  # real signal
    ]
    aggs = aggregate_runs(runs)
    assert len(aggs) == 1
    assert aggs[0].n_runs == 2  # zero-denom run dropped
    assert aggs[0].mean == 1.0


def test_aggregate_omits_metric_with_zero_denominator_in_every_run() -> None:
    """A metric that has zero denominator in EVERY run is omitted entirely
    rather than emitted as a zero-mean entry."""
    runs = [
        [_m("manifest_quoting", 0.0, denominator=0)],
        [_m("manifest_quoting", 0.0, denominator=0)],
    ]
    aggs = aggregate_runs(runs)
    assert aggs == []


def test_aggregate_empty_input() -> None:
    """No runs -> no aggregate."""
    assert aggregate_runs([]) == []


def test_format_aggregate_block_includes_per_metric_summary() -> None:
    """Smoke test on the formatter — should mention each metric name and
    show mean/stddev/min/max."""
    aggs = [
        AggregateMetric(
            name="status_precision",
            n_runs=3,
            mean=0.8,
            stddev=0.163,
            min_score=0.6,
            max_score=1.0,
            scores=(0.6, 0.8, 1.0),
        )
    ]
    out = format_aggregate_block(aggs)
    assert "status_precision" in out
    assert "mean=0.800" in out
    assert "stddev=0.163" in out
    assert "min=0.600" in out
    assert "max=1.000" in out
    assert "n=3" in out


def test_format_aggregate_block_empty_handling() -> None:
    """Empty aggregate -> sentinel string instead of empty output."""
    out = format_aggregate_block([])
    assert "no metrics with signal" in out
