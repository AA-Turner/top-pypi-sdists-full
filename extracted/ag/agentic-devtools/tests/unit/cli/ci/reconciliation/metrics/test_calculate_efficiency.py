"""Tests for calculate_efficiency()."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import cast

from agentic_devtools.cli.ci.reconciliation.metrics import EfficiencyWindow, calculate_efficiency


def _make_window(
    *,
    start_at: datetime,
    dispatch_opportunities: int = 20,
    unchanged_dispatches: int = 10,
    discovery_calls: int = 12,
    idle_cycles: int = 4,
) -> EfficiencyWindow:
    return EfficiencyWindow(
        window_id=start_at.isoformat(),
        start_at=start_at,
        end_at=start_at + timedelta(hours=24),
        dispatch_opportunities=dispatch_opportunities,
        unchanged_dispatches=unchanged_dispatches,
        discovery_calls=discovery_calls,
        idle_cycles=idle_cycles,
    )


def test_calculates_reductions_from_seven_immediately_preceding_windows() -> None:
    baseline = [_make_window(start_at=datetime(2024, 1, day, tzinfo=UTC)) for day in range(1, 8)]
    post = _make_window(
        start_at=datetime(2024, 1, 8, tzinfo=UTC),
        unchanged_dispatches=2,
        discovery_calls=2,
    )
    result = calculate_efficiency(baseline, post)
    assert result["evaluable"] is True
    assert result["baseline_mean_unchanged_rate"] == 0.5
    assert result["post_unchanged_rate"] == 0.1
    assert cast(float, result["unchanged_reduction_pct"]) > 0
    assert cast(float, result["baseline_mean_discovery_rate"]) > cast(float, result["post_discovery_rate"])
    assert result["baseline_mean_idle_cycles"] == 4
    assert result["post_idle_cycles"] == 4
    assert result["idle_cycle_delta"] == 0


def test_ignores_older_qualifying_windows_beyond_the_immediately_preceding_seven() -> None:
    baseline = [_make_window(start_at=datetime(2023, 12, 31, tzinfo=UTC), unchanged_dispatches=20, discovery_calls=20)]
    baseline.extend(_make_window(start_at=datetime(2024, 1, day, tzinfo=UTC)) for day in range(1, 8))
    post = _make_window(
        start_at=datetime(2024, 1, 8, tzinfo=UTC),
        unchanged_dispatches=2,
        discovery_calls=2,
    )
    result = calculate_efficiency(baseline, post)
    assert result["evaluable"] is True
    assert result["baseline_mean_unchanged_rate"] == 0.5


def test_returns_not_evaluable_when_fewer_than_seven_immediately_preceding_windows_qualify() -> None:
    baseline = [_make_window(start_at=datetime(2024, 1, day, tzinfo=UTC)) for day in range(1, 7)]
    baseline.append(_make_window(start_at=datetime(2024, 1, 7, tzinfo=UTC), dispatch_opportunities=19))
    post = _make_window(start_at=datetime(2024, 1, 8, tzinfo=UTC))
    assert calculate_efficiency(baseline, post) == {"evaluable": False}


def test_returns_not_evaluable_for_overlapping_or_future_baselines() -> None:
    baseline = [_make_window(start_at=datetime(2024, 1, day, tzinfo=UTC)) for day in range(1, 6)]
    baseline.append(_make_window(start_at=datetime(2024, 1, 6, 12, tzinfo=UTC)))
    baseline.append(_make_window(start_at=datetime(2024, 1, 7, 12, tzinfo=UTC)))
    post = _make_window(start_at=datetime(2024, 1, 8, tzinfo=UTC))
    assert calculate_efficiency(baseline, post) == {"evaluable": False}


def test_returns_not_evaluable_for_non_24_hour_post_window() -> None:
    baseline = [_make_window(start_at=datetime(2024, 1, day, tzinfo=UTC)) for day in range(1, 8)]
    post = EfficiencyWindow(
        window_id="post",
        start_at=datetime(2024, 1, 8, tzinfo=UTC),
        end_at=datetime(2024, 1, 8, 12, tzinfo=UTC),
        dispatch_opportunities=20,
    )
    assert calculate_efficiency(baseline, post) == {"evaluable": False}


def test_returns_not_evaluable_for_non_24_hour_baseline_window() -> None:
    baseline = [_make_window(start_at=datetime(2024, 1, day, tzinfo=UTC)) for day in range(1, 7)]
    baseline.append(
        EfficiencyWindow(
            window_id="bad",
            start_at=datetime(2024, 1, 7, tzinfo=UTC),
            end_at=datetime(2024, 1, 7, 12, tzinfo=UTC),
            dispatch_opportunities=20,
        )
    )
    post = _make_window(start_at=datetime(2024, 1, 8, tzinfo=UTC))
    assert calculate_efficiency(baseline, post) == {"evaluable": False}


def test_returns_not_evaluable_for_zero_post_dispatch_opportunities() -> None:
    baseline = [_make_window(start_at=datetime(2024, 1, day, tzinfo=UTC)) for day in range(1, 8)]
    post = _make_window(start_at=datetime(2024, 1, 8, tzinfo=UTC), dispatch_opportunities=0)
    result = calculate_efficiency(baseline, post)
    assert result["evaluable"] is False
    assert "post_unchanged_rate" not in result


def test_zero_baseline_rate_produces_zero_percent_reduction() -> None:
    baseline = [
        _make_window(
            start_at=datetime(2024, 1, day, tzinfo=UTC),
            unchanged_dispatches=0,
            discovery_calls=0,
        )
        for day in range(1, 8)
    ]
    post = _make_window(
        start_at=datetime(2024, 1, 8, tzinfo=UTC),
        unchanged_dispatches=0,
        discovery_calls=0,
    )
    result = calculate_efficiency(baseline, post)
    assert result["evaluable"] is True
    assert result["unchanged_reduction_pct"] == 0.0
    assert result["discovery_reduction_pct"] == 0.0


def test_reports_idle_cycle_delta() -> None:
    baseline = [
        _make_window(
            start_at=datetime(2024, 1, day, tzinfo=UTC),
            idle_cycles=8,
        )
        for day in range(1, 8)
    ]
    post = _make_window(
        start_at=datetime(2024, 1, 8, tzinfo=UTC),
        idle_cycles=10,
    )

    result = calculate_efficiency(baseline, post)

    assert result["evaluable"] is True
    assert result["baseline_mean_idle_cycles"] == 8
    assert result["post_idle_cycles"] == 10
    assert result["idle_cycle_delta"] == 2
