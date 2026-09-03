"""Tests for efficiency_window_from_metric_events()."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import MappingProxyType

import pytest

from agentic_devtools.cli.ci.reconciliation.metrics import (
    MetricEventType,
    efficiency_window_from_metric_events,
)
from agentic_devtools.cli.ci.reconciliation.models import MetricEvent


def _event(event_type: str, recorded_at: datetime) -> MetricEvent:
    return MetricEvent(
        event_id=f"{event_type}-{recorded_at.isoformat()}",
        event_type=event_type,
        repo="owner/repo",
        recorded_at=recorded_at,
        attributes=MappingProxyType({}),
    )


def test_aggregates_persisted_events_inside_the_window() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    end = start + timedelta(hours=24)
    events = [
        _event(MetricEventType.DISPATCH_OPPORTUNITY.value, start),
        _event(MetricEventType.UNCHANGED_DISPATCH.value, start + timedelta(hours=1)),
        _event(MetricEventType.DISCOVERY.value, start + timedelta(hours=2)),
        _event(MetricEventType.IDLE_CYCLE.value, start + timedelta(hours=3)),
        _event("unknown", start + timedelta(hours=4)),
        _event(MetricEventType.DISCOVERY.value, end),
    ]

    window = efficiency_window_from_metric_events(
        events,
        window_id="window-1",
        start_at=start,
        end_at=end,
    )

    assert window.window_id == "window-1"
    assert window.dispatch_opportunities == 1
    assert window.unchanged_dispatches == 1
    assert window.discovery_calls == 1
    assert window.idle_cycles == 1


def test_accepts_a_generator_of_events() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    end = start + timedelta(hours=24)

    window = efficiency_window_from_metric_events(
        (_event(MetricEventType.IDLE_CYCLE.value, start) for _ in range(1)),
        window_id="window-1",
        start_at=start,
        end_at=end,
    )

    assert window.idle_cycles == 1


def test_rejects_a_naive_event_timestamp() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    end = start + timedelta(hours=24)

    with pytest.raises(ValueError, match="recorded_at"):
        efficiency_window_from_metric_events(
            [_event(MetricEventType.IDLE_CYCLE.value, datetime(2026, 1, 1))],
            window_id="window-1",
            start_at=start,
            end_at=end,
        )


@pytest.mark.parametrize(
    ("start_at", "end_at", "match"),
    [
        (datetime(2026, 1, 1), datetime(2026, 1, 2, tzinfo=UTC), "start_at"),
        (datetime(2026, 1, 1, tzinfo=UTC), datetime(2026, 1, 2), "end_at"),
        (datetime(2026, 1, 2, tzinfo=UTC), datetime(2026, 1, 1, tzinfo=UTC), "after"),
    ],
)
def test_rejects_invalid_window_bounds(
    start_at: datetime,
    end_at: datetime,
    match: str,
) -> None:
    with pytest.raises(ValueError, match=match):
        efficiency_window_from_metric_events(
            [],
            window_id="window-1",
            start_at=start_at,
            end_at=end_at,
        )
