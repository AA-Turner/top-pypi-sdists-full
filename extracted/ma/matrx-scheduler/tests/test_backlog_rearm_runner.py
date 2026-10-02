"""Forcing tests for the claimed-run integration of atomic backlog rearming."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from matrx_scheduler.backlog import BacklogRearmOutcome
from matrx_scheduler.models import (
    AgentRunResult,
    BacklogRearmResult,
    HydratedTask,
    SchAgentTask,
    SchRun,
    SchTask,
)
from matrx_scheduler import runner


ACTOR_ID = "11111111-1111-4111-8111-111111111111"
ORG_ID = "22222222-2222-4222-8222-222222222222"
TASK_ID = "33333333-3333-4333-8333-333333333333"
RUN_ID = "44444444-4444-4444-8444-444444444444"


def _claimed_rows() -> tuple[HydratedTask, SchRun, SchTask]:
    task = SchTask(
        id=TASK_ID,
        user_id=ACTOR_ID,
        organization_id=ORG_ID,
        kind="tool",
        title="Harbor Dental mailbox recovery",
        queue="recoveries",
    )
    carrier = SchAgentTask(
        id=TASK_ID,
        prompt="",
        variables={"tool_name": "outreach_reply_recovery", "args": {}},
    )
    run = SchRun(
        id=RUN_ID,
        task_id=TASK_ID,
        user_id=ACTOR_ID,
        organization_id=ORG_ID,
        status="claimed",
        claim_token="claim-token-7",
        claim_expires_at=datetime.now(UTC) + timedelta(minutes=5),
        due_at=datetime.now(UTC),
        queue="recoveries",
    )
    return HydratedTask(task=task, agent_task=carrier), run, task


@pytest.mark.asyncio
async def test_typed_backlog_result_uses_atomic_commit_without_post_commit_reporting(
    monkeypatch,
) -> None:
    """Removing the typed branch double-finalizes instead of atomically handing off."""
    hydrated, run, task = _claimed_rows()
    rearm_at = datetime.now(UTC) + timedelta(seconds=45)
    result = BacklogRearmResult(
        recovery_key="v1:harbor-dental-reply-recovery",
        rearm_at=rearm_at,
        result_summary="Applied 18 replies and queued the remaining mailbox page",
        metadata={"cursor": "page-8"},
        units_done=18,
    )
    events: list[tuple[str, object]] = []

    async def mark_running(_run_id: str, _claim_token: str) -> bool:
        return True

    async def dispatch(*_args, **_kwargs):
        return result

    async def rearm(request):
        events.append(("commit", request))
        return BacklogRearmOutcome(
            status="rearmed",
            predecessor_run_id=RUN_ID,
            successor_run_id="55555555-5555-4555-8555-555555555555",
        )

    async def report(*_args, **_kwargs) -> None:
        raise AssertionError("backlog reporting must be part of the atomic persistence primitive")

    async def normal_finalize(*_args, **_kwargs):
        raise AssertionError("typed backlog result must not use ordinary finalization")

    monkeypatch.setattr(runner.queries, "mark_run_running", mark_running)
    monkeypatch.setattr(runner, "_dispatch_under_lease", dispatch)
    monkeypatch.setattr(runner, "finalize_and_rearm_backlog", rearm)
    monkeypatch.setattr(runner.queries, "report_finalized_run", report)
    monkeypatch.setattr(runner.queries, "finalize_run", normal_finalize)

    await runner._run_claimed_task_inner(
        hydrated,
        run,
        task,
        hydrated.agent_task,
        None,
        "claim-token-7",
        SimpleNamespace(units_done=21),
    )

    assert [name for name, _ in events] == ["commit"]
    request = events[0][1]
    assert request.task_id == TASK_ID
    assert request.user_id == ACTOR_ID
    assert request.organization_id == ORG_ID
    assert request.predecessor_run_id == RUN_ID
    assert request.claim_token == "claim-token-7"
    assert request.recovery_key == "v1:harbor-dental-reply-recovery"
    assert request.due_at == rearm_at
    assert request.result_metadata == {
        "cursor": "page-8",
        "units_done": 21,
        "stopped_early": None,
    }


@pytest.mark.asyncio
async def test_refused_backlog_handoff_reports_operationally_but_not_as_terminal(
    monkeypatch,
) -> None:
    """Lost authority must write and report no fabricated terminal verdict."""
    hydrated, run, task = _claimed_rows()
    result = BacklogRearmResult(
        recovery_key="v1:harbor-dental-reply-recovery",
        rearm_at=datetime.now(UTC) + timedelta(seconds=45),
        units_done=7,
    )
    reports: list[str] = []
    failures: list[dict[str, object]] = []

    async def mark_running(_run_id: str, _claim_token: str) -> bool:
        return True

    async def dispatch(*_args, **_kwargs):
        return result

    async def rearm(_request):
        return BacklogRearmOutcome(
            status="authority_lost",
            predecessor_run_id=RUN_ID,
            reason="predecessor authority is no longer active",
        )

    async def report(*_args, **_kwargs) -> None:
        reports.append("terminal")

    async def operational(_exc, *, operation: str, context: dict[str, object]) -> None:
        failures.append({"operation": operation, **context})

    monkeypatch.setattr(runner.queries, "mark_run_running", mark_running)
    monkeypatch.setattr(runner, "_dispatch_under_lease", dispatch)
    monkeypatch.setattr(runner, "finalize_and_rearm_backlog", rearm)
    monkeypatch.setattr(runner.queries, "report_finalized_run", report)
    monkeypatch.setattr(runner, "report_operational_failure", operational)

    await runner._run_claimed_task_inner(
        hydrated,
        run,
        task,
        hydrated.agent_task,
        None,
        "claim-token-7",
        SimpleNamespace(units_done=7),
    )

    assert reports == []
    assert failures == [
        {
            "operation": "finalize_and_rearm_backlog",
            "run_id": RUN_ID,
            "task_id": TASK_ID,
            "status": "authority_lost",
        }
    ]


@pytest.mark.asyncio
async def test_normal_tool_result_keeps_the_existing_finalize_path(monkeypatch) -> None:
    """The opt-in type must not change completion for ordinary tool handlers."""
    hydrated, run, task = _claimed_rows()
    finalized: list[dict[str, object]] = []

    async def mark_running(_run_id: str, _claim_token: str) -> bool:
        return True

    async def dispatch(*_args, **_kwargs):
        return AgentRunResult(success=True, result_summary="Mailbox health check complete")

    async def finalize(run_id: str, claim_token: str, **patch: object) -> bool:
        finalized.append({"run_id": run_id, "claim_token": claim_token, **patch})
        return True

    monkeypatch.setattr(runner.queries, "mark_run_running", mark_running)
    monkeypatch.setattr(runner, "_dispatch_under_lease", dispatch)
    monkeypatch.setattr(runner.queries, "finalize_run", finalize)

    await runner._run_claimed_task_inner(
        hydrated,
        run,
        task,
        hydrated.agent_task,
        None,
        "claim-token-7",
        SimpleNamespace(units_done=0),
    )

    assert finalized[0]["status"] == "success"
    assert finalized[0]["result_summary"] == "Mailbox health check complete"
