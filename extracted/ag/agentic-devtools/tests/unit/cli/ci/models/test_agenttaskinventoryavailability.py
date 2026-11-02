"""Tests for task inventory availability values."""

from agentic_devtools.cli.ci.models import AgentTaskInventoryAvailability


def test_availability_values() -> None:
    assert {item.value for item in AgentTaskInventoryAvailability} == {"complete", "partial", "unavailable"}
