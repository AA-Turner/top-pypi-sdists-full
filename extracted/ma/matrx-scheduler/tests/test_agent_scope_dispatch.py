from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

import matrx_scheduler
from matrx_scheduler.models import (
    AgentRunInput,
    AgentRunResult,
    HydratedTask,
    SchAgentTask,
    SchRun,
    SchTask,
)
from matrx_scheduler.runner import _run_agent_kind


@pytest.mark.asyncio
async def test_agent_dispatch_preserves_task_organization() -> None:
    captured: list[AgentRunInput] = []

    async def agent_runner(run_input: AgentRunInput) -> AgentRunResult:
        captured.append(run_input)
        return AgentRunResult(success=True)

    matrx_scheduler.configure(
        supabase_client=object(),
        surface="test",
        agent_runner=agent_runner,
    )
    organization_id = "00000000-0000-4000-8000-0000000fffa1"
    task = SchTask(
        id="11111111-1111-4111-8111-111111111111",
        user_id="22222222-2222-4222-8222-222222222222",
        organization_id=organization_id,
        kind="agent",
        title="Scoped schedule",
    )
    agent_task = SchAgentTask(
        id=task.id,
        agent_id="33333333-3333-4333-8333-333333333333",
        prompt="Summarize the week.",
    )
    run = SchRun(
        id="44444444-4444-4444-8444-444444444444",
        task_id=task.id,
        user_id=task.user_id,
        organization_id=task.organization_id,
        status="running",
        due_at=datetime.now(UTC),
    )

    result = await _run_agent_kind(
        HydratedTask(task=task, agent_task=agent_task),
        run,
        "claim-token",
    )

    assert result is not None and result.success is True
    assert len(captured) == 1
    assert captured[0].organization_id == organization_id


def test_agent_dispatch_contract_rejects_blank_selection() -> None:
    with pytest.raises(ValidationError, match="agent_id or mandate_key is required"):
        AgentRunInput(
            task_id="11111111-1111-4111-8111-111111111111",
            run_id="44444444-4444-4444-8444-444444444444",
            user_id="22222222-2222-4222-8222-222222222222",
            organization_id="00000000-0000-4000-8000-0000000fffa1",
            agent_id="  ",
            prompt="Summarize the week.",
            variables={},
            persistent_conversation_id=None,
            max_runtime_seconds=600,
        )


@pytest.mark.asyncio
async def test_invalid_legacy_agent_schedule_is_paused_before_host_dispatch(
    monkeypatch,
) -> None:
    called = False
    disabled: list[str] = []
    finalized: list[dict[str, object]] = []

    async def agent_runner(_run_input: AgentRunInput) -> AgentRunResult:
        nonlocal called
        called = True
        return AgentRunResult(success=True)

    async def suspend_schedule_now(task_id: str, run_id: str, **_kw: object) -> None:
        # The pause is a RECORDED suspension + escalation, never a bare
        # enabled=false (the "learn" one-shot, 2026-09-16) — and it lands
        # BEFORE the terminal write, so the schedule cannot re-dispatch.
        assert finalized == [], "the pause must land before the run is finalized"
        disabled.append(task_id)

    async def finalize_run(
        run_id: str,
        claim_token: str,
        **patch: object,
    ) -> bool:
        finalized.append({"run_id": run_id, "claim_token": claim_token, **patch})
        return True

    matrx_scheduler.configure(
        supabase_client=object(),
        surface="test",
        agent_runner=agent_runner,
    )
    monkeypatch.setattr("matrx_scheduler.runner.suspend_schedule_now", suspend_schedule_now)
    monkeypatch.setattr("matrx_scheduler.runner.queries.finalize_run", finalize_run)

    task = SchTask(
        id="11111111-1111-4111-8111-111111111111",
        user_id="22222222-2222-4222-8222-222222222222",
        organization_id="00000000-0000-4000-8000-0000000fffa1",
        kind="agent",
        title="Legacy invalid schedule",
    )
    agent_task = SchAgentTask(id=task.id, agent_id=None, prompt="Summarize the week.")
    run = SchRun(
        id="44444444-4444-4444-8444-444444444444",
        task_id=task.id,
        user_id=task.user_id,
        organization_id=task.organization_id,
        status="running",
        due_at=datetime.now(UTC),
    )

    result = await _run_agent_kind(
        HydratedTask(task=task, agent_task=agent_task),
        run,
        "claim-token",
    )

    assert result is None
    assert called is False
    assert disabled == [task.id]
    assert finalized == [
        {
            "run_id": run.id,
            "claim_token": "claim-token",
            "status": "failed",
            "error_message": (
                f"kind='agent' task {task.id} has neither agent_id nor mandate_key; "
                "schedule was paused. Choose an agent or Mandate before enabling it again."
            ),
        }
    ]


@pytest.mark.asyncio
async def test_agent_dispatch_accepts_mandate_without_agent_id() -> None:
    captured: list[AgentRunInput] = []

    async def agent_runner(run_input: AgentRunInput) -> AgentRunResult:
        captured.append(run_input)
        return AgentRunResult(success=True)

    matrx_scheduler.configure(
        supabase_client=object(),
        surface="test",
        agent_runner=agent_runner,
    )
    task = SchTask(
        id="11111111-1111-4111-8111-111111111111",
        user_id="22222222-2222-4222-8222-222222222222",
        organization_id="00000000-0000-4000-8000-0000000fffa1",
        kind="agent",
        title="Mandated schedule",
    )
    agent_task = SchAgentTask(
        id=task.id,
        mandate_key="observability.tool_trace_triage",
        prompt="",
    )
    run = SchRun(
        id="44444444-4444-4444-8444-444444444444",
        task_id=task.id,
        user_id=task.user_id,
        organization_id=task.organization_id,
        status="running",
        due_at=datetime.now(UTC),
    )

    result = await _run_agent_kind(
        HydratedTask(task=task, agent_task=agent_task), run, "claim-token"
    )

    assert result is not None and result.success is True
    assert captured[0].agent_id is None
    assert captured[0].mandate_key == "observability.tool_trace_triage"
