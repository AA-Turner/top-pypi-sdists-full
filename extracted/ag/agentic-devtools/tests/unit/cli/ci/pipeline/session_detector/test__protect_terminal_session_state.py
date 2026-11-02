from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskInventoryAvailability,
    AgentTaskLifecycle,
    FailureCategory,
)
from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    _protect_terminal_session_state,
)


def test_protective_activity_does_not_reuse_terminal_task_id() -> None:
    provider = MagicMock()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(())
    with patch(
        "agentic_devtools.cli.ci.pipeline.session_detector.is_copilot_session_active_via_agent_task", return_value=True
    ):
        result = _protect_terminal_session_state(
            SessionState(SessionOutcome.FINISHED, task_id="old"),
            provider,
            7,
            repo="org/repo",
            head_branch="",
            pr_id=None,
            head_sha="",
        )
    assert result.outcome is SessionOutcome.ACTIVE
    assert result.task_id is None


def test_lifecycle_failure_preserves_source_status_and_terminal_correlation() -> None:
    provider = MagicMock()
    error = RuntimeError("provider unavailable")
    error.__dict__["status_code"] = 404
    provider.list_pr_agent_task_lifecycles.side_effect = error
    result = _protect_terminal_session_state(
        SessionState(SessionOutcome.FAILED, task_id="old", failure_event_id=42),
        provider,
        7,
        repo="org/repo",
        head_branch="",
        pr_id=None,
        head_sha="",
    )
    assert result.outcome is SessionOutcome.UNKNOWN
    assert result.task_id == "old"
    assert result.failure_event_id == 42
    assert result.http_status == 404
    assert result.failure_category is FailureCategory.HTTP_NOT_FOUND
    assert result.failure_source == "agent-task-lifecycle"
    provider.list_pr_agent_task_lifecycles.assert_called_once()


def test_verified_active_preserves_partial_lifecycle_diagnostics() -> None:
    provider = MagicMock()
    task = AgentTaskLifecycle(
        task_id="running",
        repository="org/repo",
        pr_number=7,
        head_branch="feature",
        state="in_progress",
        created_at=datetime.now(UTC).isoformat(),
    )
    inventory = AgentTaskInventory(
        (task,),
        complete=False,
        failure_category=FailureCategory.PROVIDER_UNAVAILABLE,
        http_status=500,
    )
    provider.list_pr_agent_task_lifecycles.return_value = inventory

    with patch(
        "agentic_devtools.cli.ci.pipeline.session_detector.is_copilot_session_active_via_agent_task",
        return_value=True,
    ):
        result = _protect_terminal_session_state(
            SessionState(SessionOutcome.FINISHED, task_id="terminal"),
            provider,
            7,
            repo="org/repo",
            head_branch="feature",
            pr_id=None,
            head_sha="",
        )

    assert result.outcome is SessionOutcome.ACTIVE
    assert result.task_id is None
    assert result.inventory_availability is AgentTaskInventoryAvailability.PARTIAL
    assert result.failure_category is FailureCategory.PROVIDER_UNAVAILABLE
    assert result.http_status == 500
    assert result.failure_source == "agent-task-lifecycle"


def test_nonterminal_state_is_not_reassessed() -> None:
    state = SessionState(SessionOutcome.UNKNOWN)
    provider = MagicMock()
    assert (
        _protect_terminal_session_state(
            state,
            provider,
            7,
            repo="org/repo",
            head_branch="",
            pr_id=None,
            head_sha="",
        )
        is state
    )
    provider.list_pr_agent_task_lifecycles.assert_not_called()
