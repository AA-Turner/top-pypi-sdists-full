"""Tests for the eval-harness delta-vs-prior reporter."""

from __future__ import annotations

import json
from pathlib import Path

from evals.diff import NOISE_FLOOR, MetricDelta, compute_deltas, format_delta_block


def _write_metrics(path: Path, timestamp: str, metrics: list[dict]) -> Path:
    """Write a metrics.json under <path>/<timestamp>/metrics.json
    matching the shape evals/cli.py emits."""
    run_dir = path / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = run_dir / "metrics.json"
    metrics_path.write_text(
        json.dumps(
            {
                "fixture_id": "test-fixture",
                "ground_truth_revision": 1,
                "timestamp": timestamp,
                "metrics": metrics,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return metrics_path


def test_compute_deltas_first_run_has_no_priors(tmp_path: Path) -> None:
    """First run on a fresh fixture: no prior metrics.json; every
    delta has prior_score=None and delta=None."""
    current = _write_metrics(
        tmp_path,
        "20260508T220000Z",
        [
            {
                "name": "status_precision",
                "score": 0.85,
                "numerator": 17,
                "denominator": 20,
                "notes": "",
            },
            {
                "name": "status_recall",
                "score": 0.90,
                "numerator": 18,
                "denominator": 20,
                "notes": "",
            },
        ],
    )
    deltas = compute_deltas(current, tmp_path)
    assert len(deltas) == 2
    assert all(d.prior_score is None for d in deltas)
    assert all(d.delta is None for d in deltas)


def test_compute_deltas_with_prior_run(tmp_path: Path) -> None:
    """Two runs: deltas compute as `current - prior`."""
    _write_metrics(
        tmp_path,
        "20260508T210000Z",  # prior
        [
            {
                "name": "status_precision",
                "score": 0.85,
                "numerator": 17,
                "denominator": 20,
                "notes": "",
            },
            {
                "name": "status_recall",
                "score": 0.90,
                "numerator": 18,
                "denominator": 20,
                "notes": "",
            },
        ],
    )
    current = _write_metrics(
        tmp_path,
        "20260508T220000Z",  # current
        [
            {
                "name": "status_precision",
                "score": 0.92,
                "numerator": 19,
                "denominator": 20,
                "notes": "",
            },
            {
                "name": "status_recall",
                "score": 0.85,
                "numerator": 17,
                "denominator": 20,
                "notes": "",
            },
        ],
    )
    deltas = {d.name: d for d in compute_deltas(current, tmp_path)}
    # Precision improved.
    assert abs(deltas["status_precision"].delta - 0.07) < 1e-9
    # Recall regressed.
    assert abs(deltas["status_recall"].delta - (-0.05)) < 1e-9


def test_yellow_flag_fires_on_drop_greater_than_noise_floor() -> None:
    """A drop > NOISE_FLOOR (5%) fires the yellow flag. A drop AT
    the threshold does NOT (strictly less-than). Lock the boundary."""
    just_under = MetricDelta(
        name="status_recall", prior_score=0.90, current_score=0.86, delta=-0.04
    )
    at_threshold = MetricDelta(
        name="status_recall", prior_score=0.90, current_score=0.85, delta=-NOISE_FLOOR
    )
    over_threshold = MetricDelta(
        name="status_recall", prior_score=0.90, current_score=0.84, delta=-0.06
    )

    assert not just_under.is_yellow_flag, "4% drop is within noise floor"
    assert not at_threshold.is_yellow_flag, "exactly -5% is the boundary, not over"
    assert over_threshold.is_yellow_flag, "6% drop should yellow-flag"


def test_yellow_flag_does_not_fire_on_improvement() -> None:
    """Improvements never yellow-flag -- even big ones. Catches the
    regression where someone wires the delta as abs() and starts
    flagging good news."""
    big_improvement = MetricDelta(
        name="status_precision", prior_score=0.50, current_score=0.95, delta=0.45
    )
    assert not big_improvement.is_yellow_flag


def test_compute_deltas_handles_new_metric_in_current(tmp_path: Path) -> None:
    """PR gamma adds M5 (poam_scope_discipline). The first post-gamma run
    has M5 in current but not in prior; delta=None for that metric."""
    _write_metrics(
        tmp_path,
        "20260508T210000Z",
        [
            {
                "name": "status_precision",
                "score": 0.85,
                "numerator": 17,
                "denominator": 20,
                "notes": "",
            },
        ],
    )
    current = _write_metrics(
        tmp_path,
        "20260508T220000Z",
        [
            {
                "name": "status_precision",
                "score": 0.85,
                "numerator": 17,
                "denominator": 20,
                "notes": "",
            },
            {
                "name": "poam_scope_discipline",
                "score": 1.0,
                "numerator": 2,
                "denominator": 2,
                "notes": "",
            },
        ],
    )
    deltas = {d.name: d for d in compute_deltas(current, tmp_path)}
    assert deltas["status_precision"].delta == 0.0
    assert deltas["poam_scope_discipline"].prior_score is None
    assert deltas["poam_scope_discipline"].delta is None


def test_format_delta_block_baseline_message(tmp_path: Path) -> None:
    """First run gets a 'this is the baseline' line, not a per-metric
    delta block. Same fixture but with no prior."""
    current = _write_metrics(
        tmp_path,
        "20260508T220000Z",
        [
            {
                "name": "status_precision",
                "score": 0.85,
                "numerator": 17,
                "denominator": 20,
                "notes": "",
            },
        ],
    )
    deltas = compute_deltas(current, tmp_path)
    block = format_delta_block(deltas)
    assert "baseline" in block.lower()


def test_format_delta_block_yellow_flags_regression(tmp_path: Path) -> None:
    """A regression > NOISE_FLOOR shows up with the `!` indicator and
    the regression caveat string."""
    _write_metrics(
        tmp_path,
        "20260508T210000Z",
        [{"name": "status_recall", "score": 0.95, "numerator": 19, "denominator": 20, "notes": ""}],
    )
    current = _write_metrics(
        tmp_path,
        "20260508T220000Z",
        [{"name": "status_recall", "score": 0.80, "numerator": 16, "denominator": 20, "notes": ""}],
    )
    deltas = compute_deltas(current, tmp_path)
    block = format_delta_block(deltas)
    assert "!" in block
    assert "regression" in block.lower()
    assert "status_recall" in block


def test_format_delta_block_quiet_on_unchanged(tmp_path: Path) -> None:
    """A run where nothing changed should not show '!' or 'new
    metric' markers -- just the unchanged scores."""
    metrics = [
        {"name": "status_precision", "score": 0.85, "numerator": 17, "denominator": 20, "notes": ""}
    ]
    _write_metrics(tmp_path, "20260508T210000Z", metrics)
    current = _write_metrics(tmp_path, "20260508T220000Z", metrics)
    deltas = compute_deltas(current, tmp_path)
    block = format_delta_block(deltas)
    assert "!" not in block
    assert "new metric" not in block
