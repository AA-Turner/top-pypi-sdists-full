"""Deterministic keyword-market demand math (v1) — implemented ONCE.

``seo.keyword_market.monthly_searches`` is a merged rolling history
(``[{"year": 2026, "month": 6, "search_volume": 5400}, ...]``). The DB owns the
merge (``seo.fn_merge_monthly``); this module owns the derived stats the volume
writer recomputes AFTER every merge, over the FULL merged history — never over
just the fresh provider months. Tune the rules here and only here.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict

TRAJECTORY_EXPLODING_GROWTH = Decimal("2.0")
TRAJECTORY_GROWING_GROWTH = Decimal("0.3")
TRAJECTORY_DECLINING_GROWTH = Decimal("-0.3")
TRAJECTORY_SEASONAL_INDEX = Decimal("2.0")
TRAJECTORY_SEASONAL_MIN_MONTHS = 24
TRAJECTORY_MIN_MONTHS = 6


class MarketStats(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data_months: int
    growth_rate: Decimal | None
    seasonality_index: Decimal | None
    demand_trajectory: str


def _normalized_months(monthly: list[dict[str, Any]]) -> list[tuple[int, int, int]]:
    """Distinct (year, month, volume) sorted most-recent-first. Later entries
    win on a (year, month) collision — matching ``seo.fn_merge_monthly``."""
    by_month: dict[tuple[int, int], int] = {}
    for item in monthly:
        if not isinstance(item, dict):
            continue
        year, month = item.get("year"), item.get("month")
        if year is None or month is None:
            continue
        by_month[(int(year), int(month))] = int(item.get("search_volume") or 0)
    return sorted(
        ((year, month, volume) for (year, month), volume in by_month.items()),
        key=lambda entry: (entry[0], entry[1]),
        reverse=True,
    )


def merge_monthly(old: list[dict[str, Any]], new: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Python mirror of ``seo.fn_merge_monthly`` for the in-memory repository:
    UNION by (year, month), new wins on collision, old months retained,
    sorted descending."""
    return [
        {"year": year, "month": month, "search_volume": volume}
        for year, month, volume in _normalized_months([*old, *new])
    ]


def compute_market_stats(monthly: list[dict[str, Any]]) -> MarketStats:
    months = _normalized_months(monthly)
    data_months = len(months)
    volumes = [Decimal(volume) for _, _, volume in months]

    growth_rate: Decimal | None = None
    if data_months >= 4:
        recent = sum(volumes[:3]) / Decimal(min(3, data_months))
        prior_window = volumes[3:12]
        if prior_window:
            prior = sum(prior_window) / Decimal(len(prior_window))
            if prior != 0:
                growth_rate = recent / prior - Decimal(1)

    seasonality_index: Decimal | None = None
    last_12 = volumes[:12]
    if last_12:
        average = sum(last_12) / Decimal(len(last_12))
        if average != 0:
            seasonality_index = max(last_12) / average

    if data_months < TRAJECTORY_MIN_MONTHS:
        trajectory = "insufficient_data"
    elif growth_rate is not None and growth_rate >= TRAJECTORY_EXPLODING_GROWTH:
        trajectory = "exploding"
    elif growth_rate is not None and growth_rate >= TRAJECTORY_GROWING_GROWTH:
        trajectory = "growing"
    elif growth_rate is not None and growth_rate <= TRAJECTORY_DECLINING_GROWTH:
        trajectory = "declining"
    elif (
        data_months >= TRAJECTORY_SEASONAL_MIN_MONTHS
        and seasonality_index is not None
        and seasonality_index >= TRAJECTORY_SEASONAL_INDEX
        and growth_rate is not None
        and TRAJECTORY_DECLINING_GROWTH < growth_rate < TRAJECTORY_GROWING_GROWTH
    ):
        trajectory = "seasonal"
    else:
        trajectory = "stable"

    return MarketStats(
        data_months=data_months,
        growth_rate=growth_rate,
        seasonality_index=seasonality_index,
        demand_trajectory=trajectory,
    )


__all__ = ["MarketStats", "compute_market_stats", "merge_monthly"]
