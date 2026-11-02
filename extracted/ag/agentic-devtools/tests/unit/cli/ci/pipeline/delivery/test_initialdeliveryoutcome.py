"""Tests for InitialDeliveryOutcome."""

from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryOutcome


def test_initial_delivery_outcome_values() -> None:
    assert [outcome.value for outcome in InitialDeliveryOutcome] == ["DELIVERED", "NO_DELIVERY", "UNKNOWN"]
