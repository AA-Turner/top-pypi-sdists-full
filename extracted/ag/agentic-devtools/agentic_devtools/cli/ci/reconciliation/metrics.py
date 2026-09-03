"""Reconciliation metrics and efficiency calculations."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum, StrEnum
from types import MappingProxyType
from uuid import uuid4

from agentic_devtools.cli.ci.reconciliation.models import MetricEvent

_REQUIRED_BASELINE_WINDOWS = 7
_MIN_DISPATCH_OPPORTUNITIES = 20
_COMPARABLE_WINDOW = timedelta(hours=24)


class MetricEventType(StrEnum):
    """Types of metric events emitted by the reconciliation engine."""

    DISCOVERY = "discovery"
    DISPATCH_OPPORTUNITY = "dispatch_opportunity"
    UNCHANGED_DISPATCH = "unchanged_dispatch"
    IDLE_CYCLE = "idle_cycle"
    PROBE = "probe"
    SAFETY_OUTCOME = "safety_outcome"
    PROVIDER_FAILURE = "provider_failure"
    CLAIM_ACQUIRED = "claim_acquired"
    LEASE_ACQUIRED = "lease_acquired"
    STALE_WRITE_REJECTED = "stale_write_rejected"


def create_metric_event(
    event_type: MetricEventType,
    repo: str,
    attributes: Mapping[str, object] | None = None,
) -> MetricEvent:
    """Create a metric event with a UTC timestamp."""
    return MetricEvent(
        event_id=str(uuid4()),
        event_type=event_type.value,
        repo=repo,
        recorded_at=datetime.now(UTC),
        attributes=_sanitize_mapping(attributes or {}),
    )


def _sanitize_mapping(attributes: Mapping[str, object]) -> MappingProxyType[str, object]:
    return MappingProxyType(
        {
            str(key): _sanitize_attribute_value(value)
            for key, value in sorted(attributes.items(), key=lambda item: str(item[0]))
        }
    )


def _sanitize_attribute_value(value: object) -> object:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise TypeError("Metric attribute datetimes must be timezone-aware")
        return value.isoformat()
    if isinstance(value, Enum):
        return _sanitize_attribute_value(value.value)
    if isinstance(value, Mapping):
        return _sanitize_mapping(value)
    if isinstance(value, (list, tuple)):
        return tuple(_sanitize_attribute_value(item) for item in value)
    if isinstance(value, (set, frozenset)):
        sanitized = (_sanitize_attribute_value(item) for item in value)
        return tuple(sorted(sanitized, key=repr))
    return f"<redacted:{type(value).__name__}>"


def efficiency_window_from_metric_events(
    events: Iterable[MetricEvent],
    *,
    window_id: str,
    start_at: datetime,
    end_at: datetime,
) -> EfficiencyWindow:
    """Aggregate persisted metric events that fall within a half-open time window."""
    if start_at.tzinfo is None:
        raise ValueError("start_at must be timezone-aware")
    if end_at.tzinfo is None:
        raise ValueError("end_at must be timezone-aware")
    if end_at <= start_at:
        raise ValueError("end_at must be after start_at")

    counts = {
        MetricEventType.DISPATCH_OPPORTUNITY: 0,
        MetricEventType.UNCHANGED_DISPATCH: 0,
        MetricEventType.DISCOVERY: 0,
        MetricEventType.IDLE_CYCLE: 0,
    }
    for event in events:
        if event.recorded_at.tzinfo is None:
            raise ValueError("metric event recorded_at must be timezone-aware")
        if start_at <= event.recorded_at < end_at and event.event_type in counts:
            counts[MetricEventType(event.event_type)] += 1
    return EfficiencyWindow(
        window_id=window_id,
        start_at=start_at,
        end_at=end_at,
        dispatch_opportunities=counts[MetricEventType.DISPATCH_OPPORTUNITY],
        unchanged_dispatches=counts[MetricEventType.UNCHANGED_DISPATCH],
        discovery_calls=counts[MetricEventType.DISCOVERY],
        idle_cycles=counts[MetricEventType.IDLE_CYCLE],
    )


@dataclass
class EfficiencyWindow:
    """A time window for efficiency calculations."""

    window_id: str
    start_at: datetime
    end_at: datetime
    dispatch_opportunities: int = 0
    unchanged_dispatches: int = 0
    discovery_calls: int = 0
    idle_cycles: int = 0

    def __post_init__(self) -> None:
        if self.start_at.tzinfo is None:
            raise ValueError("start_at must be timezone-aware")
        if self.end_at.tzinfo is None:
            raise ValueError("end_at must be timezone-aware")


def calculate_efficiency(
    baseline_windows: list[EfficiencyWindow],
    post_window: EfficiencyWindow,
) -> dict[str, object]:
    """Calculate unchanged, discovery, and idle-cycle deltas over comparable 24-hour windows.

    Returns a mapping that always includes ``"evaluable"``.  When fewer than
    seven qualifying baseline windows from the seven immediately preceding
    24-hour windows (each with at least 20 dispatch opportunities) exist, or
    when the post window is not a qualifying 24-hour window, ``"evaluable"``
    is ``False`` and no rate or reduction keys are present, matching the
    SC-004/SC-005 contract.
    """

    if _window_duration(post_window) != _COMPARABLE_WINDOW:
        return {"evaluable": False}
    if post_window.dispatch_opportunities < _MIN_DISPATCH_OPPORTUNITIES:
        return {"evaluable": False}
    qualifying = _select_immediately_preceding_baselines(
        baseline_windows=baseline_windows,
        post_window=post_window,
    )
    if len(qualifying) < _REQUIRED_BASELINE_WINDOWS:
        return {"evaluable": False}

    def _unchanged_rate(window: EfficiencyWindow) -> float:
        return window.unchanged_dispatches / window.dispatch_opportunities

    def _discovery_rate(window: EfficiencyWindow) -> float:
        return window.discovery_calls / window.dispatch_opportunities

    post_unchanged_rate = _unchanged_rate(post_window)
    post_discovery_rate = _discovery_rate(post_window)
    post_idle_cycles = post_window.idle_cycles

    baseline_mean_unchanged = sum(_unchanged_rate(w) for w in qualifying) / len(qualifying)
    baseline_mean_discovery = sum(_discovery_rate(w) for w in qualifying) / len(qualifying)
    baseline_mean_idle_cycles = sum(window.idle_cycles for window in qualifying) / len(qualifying)

    def _reduction_pct(baseline: float, post: float) -> float:
        if baseline == 0.0:
            return 0.0
        return (baseline - post) / baseline * 100.0

    return {
        "evaluable": True,
        "baseline_mean_unchanged_rate": baseline_mean_unchanged,
        "post_unchanged_rate": post_unchanged_rate,
        "unchanged_reduction_pct": _reduction_pct(
            baseline_mean_unchanged,
            post_unchanged_rate,
        ),
        "baseline_mean_discovery_rate": baseline_mean_discovery,
        "post_discovery_rate": post_discovery_rate,
        "discovery_reduction_pct": _reduction_pct(
            baseline_mean_discovery,
            post_discovery_rate,
        ),
        "baseline_mean_idle_cycles": baseline_mean_idle_cycles,
        "post_idle_cycles": post_idle_cycles,
        "idle_cycle_delta": post_idle_cycles - baseline_mean_idle_cycles,
    }


def _window_duration(window: EfficiencyWindow) -> timedelta:
    """Return the wall-clock duration covered by *window*."""
    return window.end_at - window.start_at


def _select_immediately_preceding_baselines(
    baseline_windows: list[EfficiencyWindow],
    post_window: EfficiencyWindow,
) -> list[EfficiencyWindow]:
    """Return the seven qualifying 24-hour windows immediately preceding *post_window*."""
    candidates = {
        (window.start_at, window.end_at): window
        for window in baseline_windows
        if window.dispatch_opportunities >= _MIN_DISPATCH_OPPORTUNITIES
        and _window_duration(window) == _COMPARABLE_WINDOW
        and window.end_at <= post_window.start_at
    }
    selected: list[EfficiencyWindow] = []
    expected_end = post_window.start_at
    for _ in range(_REQUIRED_BASELINE_WINDOWS):
        expected_start = expected_end - _COMPARABLE_WINDOW
        window = candidates.get((expected_start, expected_end))
        if window is None:
            return []
        selected.append(window)
        expected_end = expected_start
    selected.reverse()
    return selected
