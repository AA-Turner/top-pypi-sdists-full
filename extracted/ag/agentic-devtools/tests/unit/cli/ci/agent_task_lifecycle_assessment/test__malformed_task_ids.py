"""Tests for identifying tasks with incomplete lifecycle evidence."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.agent_task_lifecycle_assessment import _malformed_task_ids
from agentic_devtools.cli.ci.models import AgentTaskInventory
from tests.unit.cli.ci.pipeline.session_detector._agent_task_test_support import _task

NOW = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)
MAX_AGE = timedelta(minutes=75)


def test_empty_inventory_has_no_malformed_task_ids() -> None:
    assert _malformed_task_ids(AgentTaskInventory(()), now=NOW, max_age=MAX_AGE) == frozenset()


def test_task_scoped_reasons_are_returned_and_other_reasons_are_ignored() -> None:
    inventory = AgentTaskInventory(
        (_task(),),
        complete=False,
        incomplete_reasons=(
            "task-detail:task-1",
            "malformed-session:task-2",
            "missing-session-id:task-3",
            "malformed-page-1",
            "missing-task-id",
        ),
    )

    assert _malformed_task_ids(inventory, now=NOW, max_age=MAX_AGE) == frozenset({"task-1", "task-2", "task-3"})


@pytest.mark.parametrize(
    ("started_at", "expected"),
    [
        ((NOW - timedelta(minutes=5)).isoformat(), frozenset()),
        ((NOW - timedelta(minutes=76)).isoformat(), frozenset({"task-1"})),
        ((NOW + timedelta(minutes=5)).isoformat(), frozenset({"task-1"})),
        ("invalid", frozenset({"task-1"})),
    ],
)
def test_task_detail_is_not_malformed_when_parent_activity_is_current(
    started_at: str, expected: frozenset[str]
) -> None:
    task = replace(_task(), started_at=started_at)
    inventory = AgentTaskInventory((task,), complete=False, incomplete_reasons=("task-detail:task-1",))

    assert _malformed_task_ids(inventory, now=NOW, max_age=MAX_AGE) == expected
