"""Deterministic v1 demand-trajectory rules — pinned so tuning is deliberate."""

from decimal import Decimal

from matrx_seo.market_math import compute_market_stats, merge_monthly


def _months(volumes: list[int], start_year: int = 2026, start_month: int = 6) -> list[dict]:
    """volumes[0] = most recent month, walking backwards."""
    out = []
    year, month = start_year, start_month
    for volume in volumes:
        out.append({"year": year, "month": month, "search_volume": volume})
        month -= 1
        if month == 0:
            year, month = year - 1, 12
    return out


def test_merge_unions_by_month_new_wins_and_retains_old():
    old = _months([10, 20, 30])  # 2026-06, 05, 04
    new = [
        {"year": 2026, "month": 7, "search_volume": 99},
        {"year": 2026, "month": 6, "search_volume": 11},
    ]
    merged = merge_monthly(old, new)
    assert [(m["year"], m["month"], m["search_volume"]) for m in merged] == [
        (2026, 7, 99),
        (2026, 6, 11),
        (2026, 5, 20),
        (2026, 4, 30),
    ]
    # Idempotent: merging the same data again changes nothing.
    assert merge_monthly(merged, new) == merged


def test_insufficient_data_under_six_months():
    stats = compute_market_stats(_months([100] * 5))
    assert stats.data_months == 5
    assert stats.demand_trajectory == "insufficient_data"


def test_stable_flat_history():
    stats = compute_market_stats(_months([100] * 12))
    assert stats.growth_rate == Decimal(0)
    assert stats.seasonality_index == Decimal(1)
    assert stats.demand_trajectory == "stable"


def test_growing_and_exploding_and_declining():
    growing = compute_market_stats(_months([140] * 3 + [100] * 9))
    assert growing.demand_trajectory == "growing"
    exploding = compute_market_stats(_months([300] * 3 + [100] * 9))
    assert exploding.demand_trajectory == "exploding"
    declining = compute_market_stats(_months([60] * 3 + [100] * 9))
    assert declining.demand_trajectory == "declining"


def test_seasonal_requires_24_months_and_flat_growth():
    # One yearly spike (December), otherwise flat — 24 months of history.
    spiky_24 = []
    year, month = 2026, 6
    for _ in range(24):
        spiky_24.append(
            {
                "year": year,
                "month": month,
                "search_volume": 300 if month == 12 else 100,
            }
        )
        month -= 1
        if month == 0:
            year, month = year - 1, 12
    stats = compute_market_stats(spiky_24)
    assert stats.data_months == 24
    assert stats.seasonality_index >= Decimal(2)
    assert stats.demand_trajectory == "seasonal"
    # Same spike with only 12 months reads as stable, not seasonal.
    stats_12 = compute_market_stats(spiky_24[:12])
    assert stats_12.demand_trajectory == "stable"


def test_growth_rate_null_when_no_prior_window():
    stats = compute_market_stats(_months([100, 100, 100]))
    assert stats.growth_rate is None
    assert stats.demand_trajectory == "insufficient_data"
