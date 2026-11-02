"""Tests for create_metric_event()."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum, StrEnum
from typing import cast

import pytest

from agentic_devtools.cli.ci.reconciliation.metrics import MetricEventType, create_metric_event
from agentic_devtools.cli.ci.reconciliation.models import MetricEvent


class _EventAttribute(StrEnum):
    READY = "ready"


class _NumericEnum(Enum):
    COUNT = 3


def test_metric_event_immutable() -> None:
    event = create_metric_event(MetricEventType.DISCOVERY, "owner/repo")
    assert isinstance(event, MetricEvent)
    with pytest.raises((AttributeError, TypeError)):
        event.repo = "other"  # type: ignore[misc]


def test_attributes_immutable() -> None:
    event = create_metric_event(MetricEventType.DISCOVERY, "owner/repo", {"pages": 2})
    with pytest.raises(TypeError):
        event.attributes["pages"] = 99  # type: ignore[index]


def test_attributes_are_copied_before_freezing() -> None:
    attributes = {"pages": 2}
    event = create_metric_event(MetricEventType.DISCOVERY, "owner/repo", attributes)
    attributes["pages"] = 99
    assert event.attributes["pages"] == 2


def test_sanitizes_nested_mutable_values() -> None:
    nested_pages = [1, 2]
    tags = {"beta", "alpha"}
    event = create_metric_event(
        MetricEventType.DISCOVERY,
        "owner/repo",
        {"nested": {"pages": nested_pages}, "tags": tags},
    )
    nested_pages.append(3)
    tags.add("gamma")
    nested = cast(dict[str, tuple[int, ...]], event.attributes["nested"])
    assert nested["pages"] == (1, 2)
    assert event.attributes["tags"] == ("alpha", "beta")


def test_redacts_unsupported_objects() -> None:
    event = create_metric_event(MetricEventType.DISCOVERY, "owner/repo", {"client": object()})
    assert event.attributes["client"] == "<redacted:object>"


def test_serializes_datetime_attribute() -> None:
    event = create_metric_event(
        MetricEventType.DISCOVERY,
        "owner/repo",
        {"when": datetime(2024, 1, 2, 3, 4, 5, tzinfo=UTC)},
    )
    assert event.attributes["when"] == "2024-01-02T03:04:05+00:00"


def test_rejects_naive_datetime_attribute() -> None:
    with pytest.raises(TypeError, match="timezone-aware"):
        create_metric_event(MetricEventType.DISCOVERY, "owner/repo", {"when": datetime(2024, 1, 2, 3, 4, 5)})


def test_serializes_enum_attribute() -> None:
    text_event = create_metric_event(MetricEventType.DISCOVERY, "owner/repo", {"state": _EventAttribute.READY})
    numeric_event = create_metric_event(MetricEventType.DISCOVERY, "owner/repo", {"count": _NumericEnum.COUNT})
    assert text_event.attributes["state"] == "ready"
    assert numeric_event.attributes["count"] == 3


def test_sets_expected_fields() -> None:
    event = create_metric_event(MetricEventType.DISPATCH_OPPORTUNITY, "owner/repo", {"pages": 2})
    assert event.event_type == MetricEventType.DISPATCH_OPPORTUNITY.value
    assert event.repo == "owner/repo"
    assert event.attributes["pages"] == 2


def test_records_timezone_aware_timestamp() -> None:
    assert create_metric_event(MetricEventType.DISCOVERY, "owner/repo").recorded_at.tzinfo is not None


def test_unknown_attribution_and_watermark_events_are_sanitized() -> None:
    unknown = create_metric_event(
        MetricEventType.UNKNOWN_ATTRIBUTION,
        "owner/repo",
        {"pr_number": 42, "outcome": "unknown", "reason": "incomplete"},
    )
    advanced = create_metric_event(
        MetricEventType.WATERMARK_ADVANCED,
        "owner/repo",
        {"pr_number": 42, "outcome": "advanced"},
    )
    failure = create_metric_event(
        MetricEventType.PROVIDER_ATTRIBUTION_FAILURE,
        "owner/repo",
        {"outcome": "failed", "reason": "provider_error"},
    )

    assert unknown.repo == "owner/repo"
    assert dict(unknown.attributes) == {
        "outcome": "unknown",
        "pr_number": 42,
        "reason": "incomplete",
    }
    assert advanced.repo == "owner/repo"
    assert dict(advanced.attributes) == {"outcome": "advanced", "pr_number": 42}
    assert dict(failure.attributes) == {"outcome": "failed", "reason": "provider_error"}


@pytest.mark.parametrize(
    ("event_type", "attributes"),
    [
        (
            MetricEventType.UNKNOWN_ATTRIBUTION,
            {"outcome": "unknown", "token": "secret"},
        ),
        (
            MetricEventType.UNKNOWN_ATTRIBUTION,
            {"outcome": "unknown", "raw_payload": {"provider": "private"}},
        ),
        (
            MetricEventType.UNKNOWN_ATTRIBUTION,
            {"outcome": "unexpected"},
        ),
        (
            MetricEventType.UNKNOWN_ATTRIBUTION,
            {"outcome": "unknown", "reason": "exception text"},
        ),
        (
            MetricEventType.UNKNOWN_ATTRIBUTION,
            {"outcome": "unknown", "pr_number": 0},
        ),
        (
            MetricEventType.UNKNOWN_ATTRIBUTION,
            {"outcome": "unknown", "pr_number": True},
        ),
        (
            MetricEventType.WATERMARK_ADVANCED,
            {"outcome": "advanced", "unexpected": "value"},
        ),
        (
            MetricEventType.WATERMARK_ADVANCED,
            {"outcome": "advanced", "reason": "not applicable"},
        ),
        (
            MetricEventType.PROVIDER_ATTRIBUTION_FAILURE,
            {"outcome": "failed", "reason": "provider_error", "token": "secret"},
        ),
        (
            MetricEventType.PROVIDER_ATTRIBUTION_FAILURE,
            {
                "outcome": "failed",
                "reason": "provider_error",
                "raw_payload": {"provider": "private"},
            },
        ),
    ],
)
def test_attribution_events_reject_unexpected_and_sensitive_attributes(
    event_type: MetricEventType,
    attributes: dict[str, object],
) -> None:
    with pytest.raises(ValueError):
        create_metric_event(event_type, "owner/repo", attributes)
