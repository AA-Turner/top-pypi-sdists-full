"""Tests for conservative assessment of normalized task lifecycle evidence."""

from datetime import UTC, datetime
from typing import Any

import pytest

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskInventoryAvailability,
    AgentTaskSessionLifecycle,
)
from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    _assess_active_task_lifecycle,
)
from tests.unit.cli.ci.pipeline.session_detector._agent_task_test_support import (
    _expired_lifecycle_provider,
    _lifecycle,
)


def _assess(provider: Any) -> SessionState:
    return _assess_active_task_lifecycle(
        provider,
        7,
        repo="org/repo",
        task_id="task-abc",
        head_branch="copilot/fix",
        head_sha="expected-head",
        raw_task=provider.task,
    )


@pytest.mark.parametrize(
    ("typed_repository", "typed_pr_number", "expected"),
    [
        ("other/repo", 7, SessionOutcome.UNKNOWN),
        ("org/repo", 8, SessionOutcome.UNKNOWN),
        ("org/repo", 7, SessionOutcome.ACTIVE),
    ],
)
def test_raw_clock_union_requires_typed_task_in_requested_scope(
    typed_repository: str,
    typed_pr_number: int,
    expected: SessionOutcome,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = _expired_lifecycle_provider()
    provider.task.pop("pullRequestNumber")
    provider.task["artifacts"] = [{"type": "pull", "data": {"id": 123456}}]
    provider.task["idleAt"] = datetime.now(UTC).isoformat()
    inventory = AgentTaskInventory((_lifecycle(repository=typed_repository, pr_number=typed_pr_number),))
    provider.list_pr_agent_task_lifecycles.return_value = inventory
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.pipeline.session_detector.is_copilot_session_active_via_agent_task",
        lambda *args, **kwargs: False,
    )

    result = _assess(provider)

    assert result.outcome is expected
    assert inventory.tasks[0].idle_at == ""


def test_fresh_raw_only_session_does_not_inherit_completed_parent_state() -> None:
    provider = _expired_lifecycle_provider()
    inventory = AgentTaskInventory(
        (
            _lifecycle(
                state="completed",
                created_at="2020-01-01T00:00:00Z",
                sessions=(AgentTaskSessionLifecycle("typed-session", "running", idle_at="2020-01-02T00:00:00Z"),),
            ),
        ),
        complete=False,
        incomplete_reasons=("task-detail:task-abc",),
    )
    provider.list_pr_agent_task_lifecycles.return_value = inventory
    provider.task["sessions"] = [{"id": "raw-only-session", "idleAt": datetime.now(UTC).isoformat()}]

    result = _assess(provider)

    assert result.outcome is SessionOutcome.UNKNOWN
    assert result.inventory_availability is AgentTaskInventoryAvailability.PARTIAL
    assert inventory.incomplete_reasons == ("task-detail:task-abc",)


def test_incomplete_inventory_does_not_promote_future_raw_clock_to_active() -> None:
    provider = _expired_lifecycle_provider()
    inventory = AgentTaskInventory(
        (_lifecycle(created_at="2020-01-01T00:00:00Z"),),
        complete=False,
        incomplete_reasons=("page-limit",),
        http_status=503,
    )
    provider.list_pr_agent_task_lifecycles.return_value = inventory
    provider.task["idleAt"] = "9999-12-31T23:59:59Z"

    result = _assess(provider)

    assert result.outcome is SessionOutcome.UNKNOWN
    assert result.inventory_availability is AgentTaskInventoryAvailability.PARTIAL
    assert result.http_status == 503
    assert result.failure_source == "agent-task-lifecycle"


@pytest.mark.parametrize("incomplete_reason", ("page-limit", "task-detail:task-abc"))
def test_future_raw_only_session_does_not_hide_recent_typed_parent_activity(incomplete_reason: str) -> None:
    provider = _expired_lifecycle_provider()
    inventory = AgentTaskInventory(
        (_lifecycle(started_at=datetime.now(UTC).isoformat()),),
        complete=False,
        incomplete_reasons=(incomplete_reason,),
    )
    provider.list_pr_agent_task_lifecycles.return_value = inventory
    provider.task["sessions"] = [{"id": "raw-only-session", "idleAt": "9999-12-31T23:59:59Z"}]

    result = _assess(provider)

    assert result.outcome is SessionOutcome.ACTIVE
    assert result.inventory_availability is AgentTaskInventoryAvailability.PARTIAL
    assert result.failure_source == "agent-task-lifecycle"
    assert inventory.incomplete_reasons == (incomplete_reason,)


def test_incomplete_inventory_keeps_independent_typed_blockers_active() -> None:
    provider = _expired_lifecycle_provider()
    inventory = AgentTaskInventory(
        (
            _lifecycle(created_at="2020-01-01T00:00:00Z"),
            _lifecycle(
                task_id="task-other",
                created_at=datetime.now(UTC).isoformat(),
            ),
        ),
        complete=False,
        incomplete_reasons=("page-limit",),
    )
    provider.list_pr_agent_task_lifecycles.return_value = inventory
    provider.task["idleAt"] = "9999-12-31T23:59:59Z"

    result = _assess(provider)

    assert result.outcome is SessionOutcome.ACTIVE
    assert result.task_id is None
