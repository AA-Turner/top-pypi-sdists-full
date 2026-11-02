"""Tests for raw task inventory results."""

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.ci.models import AgentTaskInventoryAvailability, AgentTaskInventoryLoadResult


@pytest.mark.parametrize(
    ("tasks", "complete", "expected"),
    [
        ((), True, "complete"),
        (({"state": "running"},), False, "partial"),
        ((), False, "unavailable"),
    ],
)
def test_raw_result_normalization(tasks, complete, expected) -> None:
    result = AgentTaskInventoryLoadResult(tasks, complete)
    assert result.tasks == tasks
    assert result.availability is AgentTaskInventoryAvailability(expected)
    assert result.complete is (expected == "complete")


def test_raw_result_is_frozen() -> None:
    with pytest.raises(FrozenInstanceError):
        setattr(AgentTaskInventoryLoadResult(()), "complete", False)


@pytest.mark.parametrize("availability", ["garbage", [], 42])
@pytest.mark.parametrize("tasks", [(), ({"state": "running"},)])
def test_invalid_availability_never_establishes_complete(availability, tasks) -> None:
    result = AgentTaskInventoryLoadResult(tasks, availability=availability)
    assert result.complete is False
    assert result.availability is (
        AgentTaskInventoryAvailability.PARTIAL if tasks else AgentTaskInventoryAvailability.UNAVAILABLE
    )


@pytest.mark.parametrize("availability", ["complete", "partial", "unavailable"])
def test_string_availability_is_canonicalized(availability) -> None:
    result = AgentTaskInventoryLoadResult(({"state": "running"},), availability=availability)
    assert result.availability is AgentTaskInventoryAvailability(availability)
