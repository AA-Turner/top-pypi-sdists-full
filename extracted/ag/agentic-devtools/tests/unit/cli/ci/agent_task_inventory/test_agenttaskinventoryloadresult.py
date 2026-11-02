"""Tests for the generic frozen inventory result shared by lifecycle models."""

import pytest

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskInventoryAvailability,
    AgentTaskInventoryLoadResult,
)


def test_unavailable_evidence_is_not_promoted_by_existing_rows() -> None:
    result = AgentTaskInventory((), availability=AgentTaskInventoryAvailability.UNAVAILABLE)
    assert result.complete is False
    assert result.availability is AgentTaskInventoryAvailability.UNAVAILABLE


@pytest.mark.parametrize("availability", ["garbage", [], 42])
@pytest.mark.parametrize("tasks", [(), ({"state": "running"},)])
def test_invalid_explicit_availability_is_conservative(availability, tasks) -> None:
    result = AgentTaskInventoryLoadResult(tasks, availability=availability)
    assert not result.complete
    assert result.availability == ("partial" if tasks else "unavailable")


def test_partial_without_rows_is_unavailable() -> None:
    result = AgentTaskInventoryLoadResult((), availability=AgentTaskInventoryAvailability.PARTIAL)
    assert result.availability is AgentTaskInventoryAvailability.UNAVAILABLE
    assert result.complete is False
