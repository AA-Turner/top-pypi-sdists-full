"""Tests for AgentTaskInventory."""

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskInventoryAvailability,
    AgentTaskLifecycle,
    FailureCategory,
)


def test_agent_task_inventory_defaults_to_complete() -> None:
    """Treats a supplied bounded inventory as complete unless marked otherwise."""
    task = AgentTaskLifecycle("task-1", "owner/repo", 42, "branch", "idle", "")

    assert AgentTaskInventory((task,)).complete is True
    assert AgentTaskInventory((task,), complete=False).complete is False


@pytest.mark.parametrize(
    ("complete", "has_tasks", "availability", "expected"),
    [
        (True, False, None, "complete"),
        (False, True, None, "partial"),
        (False, False, None, "unavailable"),
        (False, True, "complete", "partial"),
        (True, True, "partial", "partial"),
        (True, False, "partial", "unavailable"),
        (True, True, "unavailable", "unavailable"),
    ],
)
def test_normalizes_conservatively(complete, has_tasks, availability, expected) -> None:
    task = AgentTaskLifecycle("task-1", "owner/repo", 42, "branch", "idle", "")
    result = AgentTaskInventory(
        (task,) if has_tasks else (),
        complete,
        (),
        AgentTaskInventoryAvailability(availability) if availability else None,
    )
    assert result.availability == expected
    assert result.complete is (expected == "complete")


@pytest.mark.parametrize(
    "metadata",
    [
        {"incomplete_reasons": ("missing page",)},
        {"failure_category": FailureCategory.HTTP_NOT_FOUND},
        {"http_status": 404},
    ],
)
def test_failure_metadata_prevents_complete(metadata) -> None:
    result = AgentTaskInventory((), **metadata)
    assert result.availability is AgentTaskInventoryAvailability.UNAVAILABLE
    assert result.complete is False


def test_inventory_is_frozen() -> None:
    with pytest.raises(FrozenInstanceError):
        setattr(AgentTaskInventory(()), "complete", False)
