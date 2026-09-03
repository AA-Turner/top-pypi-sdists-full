"""Tests for MetricEventType."""

from agentic_devtools.cli.ci.reconciliation.metrics import MetricEventType


def test_contains_expected_values() -> None:
    assert MetricEventType.DISCOVERY.value == "discovery"
    assert MetricEventType.DISPATCH_OPPORTUNITY.value == "dispatch_opportunity"
    assert MetricEventType.IDLE_CYCLE.value == "idle_cycle"
    assert MetricEventType.PROBE.value == "probe"
    assert MetricEventType.SAFETY_OUTCOME.value == "safety_outcome"
