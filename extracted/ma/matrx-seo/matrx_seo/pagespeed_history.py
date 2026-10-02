from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class PagePerformanceHistoryPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    strategy: Literal["mobile", "desktop"]
    observed_at: datetime
    fetched_at: datetime
    performance_score: Decimal | None = None
    accessibility_score: Decimal | None = None
    best_practices_score: Decimal | None = None
    seo_score: Decimal | None = None
    lighthouse: dict[str, Any] = Field(default_factory=dict)
    crux: dict[str, Any] = Field(default_factory=dict)
    diagnostics: dict[str, Any] = Field(default_factory=dict)


class PagePerformanceFieldHistoryPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    observed_at: datetime
    fetched_at: datetime
    crux: dict[str, Any] = Field(default_factory=dict)


class PagePerformanceRegression(BaseModel):
    model_config = ConfigDict(extra="forbid")

    strategy: Literal["mobile", "desktop"] | None
    previous_observed_at: datetime
    current_observed_at: datetime
    metric: str
    data_kind: Literal["lab", "field"]
    previous_value: Decimal
    current_value: Decimal
    delta: Decimal


def detect_page_performance_regressions(
    history: list[PagePerformanceHistoryPoint],
    *,
    score_drop: Decimal = Decimal("0.10"),
    lab_lcp_increase_ms: Decimal = Decimal("500"),
    field_lcp_increase_ms: Decimal = Decimal("500"),
    include_field: bool = True,
) -> list[PagePerformanceRegression]:
    thresholds = (score_drop, lab_lcp_increase_ms, field_lcp_increase_ms)
    if any(value < 0 for value in thresholds):
        raise ValueError("regression thresholds cannot be negative")
    ordered = sorted(history, key=lambda item: item.observed_at)
    regressions: list[PagePerformanceRegression] = []
    for previous, current in zip(ordered, ordered[1:], strict=False):
        if previous.strategy != current.strategy:
            continue
        _append_score_regression(regressions, previous, current, score_drop)
        _append_increase_regression(
            regressions,
            previous,
            current,
            metric="lcp_ms",
            data_kind="lab",
            previous_value=_nested_decimal(
                previous.lighthouse, "metrics", "lcp_ms", "numeric_value"
            ),
            current_value=_nested_decimal(current.lighthouse, "metrics", "lcp_ms", "numeric_value"),
            threshold=lab_lcp_increase_ms,
        )
        if include_field:
            _append_increase_regression(
                regressions,
                previous,
                current,
                metric="largest_contentful_paint_p75_ms",
                data_kind="field",
                previous_value=_field_lcp(previous.crux),
                current_value=_field_lcp(current.crux),
                threshold=field_lcp_increase_ms,
                strategy_independent=True,
            )
    return regressions


def detect_field_performance_regressions(
    history: list[PagePerformanceFieldHistoryPoint],
    *,
    field_lcp_increase_ms: Decimal = Decimal("500"),
) -> list[PagePerformanceRegression]:
    if field_lcp_increase_ms < 0:
        raise ValueError("regression thresholds cannot be negative")
    ordered = sorted(history, key=lambda item: item.observed_at)
    regressions: list[PagePerformanceRegression] = []
    for previous, current in zip(ordered, ordered[1:], strict=False):
        _append_increase_regression(
            regressions,
            previous,
            current,
            metric="largest_contentful_paint_p75_ms",
            data_kind="field",
            previous_value=_field_lcp(previous.crux),
            current_value=_field_lcp(current.crux),
            threshold=field_lcp_increase_ms,
            strategy_independent=True,
        )
    return regressions


def _append_score_regression(
    output: list[PagePerformanceRegression],
    previous: PagePerformanceHistoryPoint,
    current: PagePerformanceHistoryPoint,
    threshold: Decimal,
) -> None:
    if previous.performance_score is None or current.performance_score is None:
        return
    drop = previous.performance_score - current.performance_score
    if drop < threshold:
        return
    output.append(
        PagePerformanceRegression(
            strategy=current.strategy,
            previous_observed_at=previous.observed_at,
            current_observed_at=current.observed_at,
            metric="performance_score",
            data_kind="lab",
            previous_value=previous.performance_score,
            current_value=current.performance_score,
            delta=current.performance_score - previous.performance_score,
        )
    )


def _append_increase_regression(
    output: list[PagePerformanceRegression],
    previous: PagePerformanceHistoryPoint | PagePerformanceFieldHistoryPoint,
    current: PagePerformanceHistoryPoint | PagePerformanceFieldHistoryPoint,
    *,
    metric: str,
    data_kind: Literal["lab", "field"],
    previous_value: Decimal | None,
    current_value: Decimal | None,
    threshold: Decimal,
    strategy_independent: bool = False,
) -> None:
    if previous_value is None or current_value is None:
        return
    increase = current_value - previous_value
    if increase < threshold:
        return
    output.append(
        PagePerformanceRegression(
            strategy=None if strategy_independent else getattr(current, "strategy", None),
            previous_observed_at=previous.observed_at,
            current_observed_at=current.observed_at,
            metric=metric,
            data_kind=data_kind,
            previous_value=previous_value,
            current_value=current_value,
            delta=increase,
        )
    )


def _nested_decimal(value: dict[str, Any], *path: str) -> Decimal | None:
    current: Any = value
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    if current is None:
        return None
    return Decimal(str(current))


def _field_lcp(crux: dict[str, Any]) -> Decimal | None:
    for name in ("LARGEST_CONTENTFUL_PAINT_MS", "largest_contentful_paint"):
        value = _nested_decimal(crux, "page", "metrics", name, "percentile")
        if value is not None:
            return value
    return None


__all__ = [
    "PagePerformanceFieldHistoryPoint",
    "PagePerformanceHistoryPoint",
    "PagePerformanceRegression",
    "detect_field_performance_regressions",
    "detect_page_performance_regressions",
]
