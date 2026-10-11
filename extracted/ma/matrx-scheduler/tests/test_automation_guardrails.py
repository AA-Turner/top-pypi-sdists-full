"""AUTOMATION GUARDRAILS in the scheduler (Arman, 2026-10-09).

SUT: ``run_claimed_task`` (fire-time refusal, mid-run stop, run ceiling) and
``repeat_guard.note_failed_run`` (the failure-rate ceiling).

Doubles: the in-memory ``fake_supabase`` ledger and the host's guardrail exts (dict-backed).

Breaks named:
* a refused fire leaves no visible row (a silent skip) or still dispatches the handler;
* a run the host stopped mid-way lands ``failed`` / ``success`` instead of ``stopped`` with its limit;
* the host's max_runtime_seconds is ignored (the run outlives its time limit);
* failures interleaved with successes (no streak) never pause a schedule failing half its runs.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

import matrx_scheduler
from matrx_scheduler import queries, repeat_guard
from matrx_scheduler.models import AgentRunInput, AgentRunResult
from matrx_scheduler.runner import run_claimed_task

ORG = "33333333-3333-4333-8333-333333333333"
USER = "22222222-2222-4222-8222-222222222222"
TASK = "11111111-1111-4111-8111-111111111111"
TRIGGER = "55555555-5555-4555-8555-555555555555"


def _seed(fake_supabase) -> None:
    due = datetime.now(UTC) - timedelta(minutes=5)
    fake_supabase.rows["sch_task"].append(
        {
            "id": TASK, "user_id": USER, "organization_id": ORG, "kind": "agent", "title": "digest",
            "queue": "default", "surfaces": ["any"], "enabled": True, "deleted_at": None,
            "expires_at": None, "next_due_at": due, "last_run_at": None, "metadata": {},
        }
    )
    fake_supabase.rows["sch_agent_task"].append(
        {
            "id": TASK, "agent_id": "agent-1", "mandate_key": None, "prompt": "go", "variables": {},
            "persistent_conversation_id": None, "max_runtime_seconds": 600, "auth_mode": "ask",
            "max_concurrent": 1, "organization_id": ORG,
        }
    )
    fake_supabase.rows["sch_trigger"].append(
        {
            "id": TRIGGER, "task_id": TASK, "user_id": USER, "organization_id": ORG, "type": "interval",
            "config": {"seconds": 3600}, "enabled": True, "deleted_at": None, "next_due_at": due,
            "last_fired_at": None, "metadata": {},
        }
    )


class _Host:
    def __init__(self) -> None:
        self.preflight: dict[str, Any] | None = None
        self.stops: dict[str, dict[str, Any]] = {}
        self.breaches: list[tuple[str, str]] = []
        self.rate: dict[str, Any] | None = None
        self.seen_ceiling: list[int] = []

    async def guardrail_preflight(self, task: Any, run: Any) -> dict[str, Any] | None:
        return self.preflight

    def guardrail_run_stop(self, run_id: str) -> dict[str, Any] | None:
        return self.stops.get(run_id)

    async def guardrail_breach(self, kind: str, task_id: str, run_id: str | None, detail: dict[str, Any]) -> None:
        self.breaches.append((kind, task_id))

    async def failure_rate_limits(self, task_id: str) -> dict[str, Any] | None:
        return self.rate


def _configure(fake_supabase, host: _Host, agent_runner) -> None:
    matrx_scheduler.configure_db(models=fake_supabase.db_models())

    async def sink(_alarm: Any) -> None:
        return None

    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="server",
        agent_runner=agent_runner,
        lease_seconds=30,
        escalation_sink=sink,
        guardrail_preflight=host.guardrail_preflight,
        guardrail_run_stop=host.guardrail_run_stop,
        guardrail_breach=host.guardrail_breach,
        failure_rate_limits=host.failure_rate_limits,
    )


async def _fire_once(fake_supabase) -> None:
    due = await queries.find_due_tasks()
    assert [h.task.id for h in due] == [TASK]
    hydrated = due[0]
    run = await queries.claim_task(hydrated.task, hydrated.trigger, hydrated.agent_task, lease_seconds=30)
    assert run is not None
    await run_claimed_task(hydrated, run)


def _run(fake_supabase) -> dict[str, Any]:
    return fake_supabase.rows["sch_run"][-1]


@pytest.mark.asyncio
async def test_a_refused_fire_is_a_visible_stopped_row_and_never_dispatches(fake_supabase) -> None:
    host = _Host()
    host.preflight = {"refusal": {"kind": "guardrail.missing_limits", "message": "Refused: no max turns", "paused": True}}
    calls = 0

    async def agent_runner(_inp: AgentRunInput) -> AgentRunResult:
        nonlocal calls
        calls += 1
        return AgentRunResult(success=True)

    _configure(fake_supabase, host, agent_runner)
    _seed(fake_supabase)
    await _fire_once(fake_supabase)

    assert calls == 0
    run = _run(fake_supabase)
    assert run["status"] == "stopped"
    assert run["error_message"] == "Refused: no max turns"
    assert run["result_metadata"]["guardrail"]["kind"] == "guardrail.missing_limits"


@pytest.mark.asyncio
async def test_a_mid_run_stop_lands_stopped_with_its_limit_and_keeps_the_output(fake_supabase) -> None:
    host = _Host()

    async def agent_runner(inp: AgentRunInput) -> AgentRunResult:
        host.stops[inp.run_id] = {"kind": "guardrail.max_turns", "limit": 4, "observed": 4, "message": "Stopped: limit — 4 turns"}
        return AgentRunResult(success=False, conversation_id="conv-1", error_message="caller refusal")

    _configure(fake_supabase, host, agent_runner)
    _seed(fake_supabase)
    await _fire_once(fake_supabase)

    run = _run(fake_supabase)
    assert run["status"] == "stopped"
    assert run["result_metadata"]["guardrail"]["kind"] == "guardrail.max_turns"
    assert run["output_ref"] == {"kind": "conversation", "id": "conv-1"}


@pytest.mark.asyncio
async def test_a_handler_raising_from_a_guardrail_stop_lands_stopped(fake_supabase) -> None:
    host = _Host()

    async def agent_runner(inp: AgentRunInput) -> AgentRunResult:
        host.stops[inp.run_id] = {"kind": "guardrail.max_cost_run", "message": "Stopped: limit — $2"}
        raise RuntimeError("GuardrailStopError")

    _configure(fake_supabase, host, agent_runner)
    _seed(fake_supabase)
    await _fire_once(fake_supabase)

    run = _run(fake_supabase)
    assert run["status"] == "stopped"
    assert run["result_metadata"]["guardrail"]["kind"] == "guardrail.max_cost_run"


@pytest.mark.asyncio
async def test_the_hosts_max_runtime_is_the_run_ceiling(fake_supabase) -> None:
    from matrx_scheduler.lease import current_run_lease

    host = _Host()
    host.preflight = {"max_runtime_seconds": 45}
    ceilings: list[int] = []

    async def agent_runner(_inp: AgentRunInput) -> AgentRunResult:
        ceilings.append(current_run_lease().max_runtime_seconds)
        return AgentRunResult(success=True)

    _configure(fake_supabase, host, agent_runner)
    _seed(fake_supabase)
    await _fire_once(fake_supabase)

    assert ceilings == [45]
    assert _run(fake_supabase)["status"] == "success"


def _ledger(fake_supabase, statuses: list[str]) -> None:
    base = datetime.now(UTC) - timedelta(hours=len(statuses))
    for i, status in enumerate(statuses):
        fake_supabase.rows["sch_run"].append(
            {
                "id": f"00000000-0000-4000-8000-{i:012d}", "task_id": TASK, "user_id": USER,
                "organization_id": ORG, "status": status, "due_at": base + timedelta(hours=i),
                "created_at": base + timedelta(hours=i), "error_message": f"boom {i}" if status == "failed" else None,
                "result_metadata": {}, "metadata": {},
            }
        )


@pytest.mark.asyncio
async def test_failures_interleaved_with_successes_pause_at_the_failure_rate(fake_supabase) -> None:
    host = _Host()
    host.rate = {"max_failure_pct": 50, "failure_window_runs": 10, "failure_min_runs": 6}
    _configure(fake_supabase, host, None)
    _seed(fake_supabase)
    # Alternating: never 3 in a row the same way, never 8 in a row — the streak ceilings stay quiet.
    _ledger(fake_supabase, ["failed", "success"] * 4 + ["failed"])
    last = fake_supabase.rows["sch_run"][-1]["id"]

    await repeat_guard.note_failed_run(last, TASK)

    task = fake_supabase.rows["sch_task"][0]
    assert task["enabled"] is False
    assert "failure-rate limit" in task["metadata"]["auto_suspended"]["reason"]
    assert ("guardrail.failure_pct", TASK) in host.breaches


@pytest.mark.asyncio
async def test_a_failure_rate_under_the_limit_never_pauses(fake_supabase) -> None:
    host = _Host()
    host.rate = {"max_failure_pct": 50, "failure_window_runs": 10, "failure_min_runs": 6}
    _configure(fake_supabase, host, None)
    _seed(fake_supabase)
    _ledger(fake_supabase, ["success", "success", "failed", "success", "success", "success", "failed"])

    await repeat_guard.note_failed_run(fake_supabase.rows["sch_run"][-1]["id"], TASK)

    assert fake_supabase.rows["sch_task"][0]["enabled"] is True
    assert host.breaches == []


@pytest.mark.asyncio
async def test_a_stopped_run_is_reported_and_stamps_last_run_at(fake_supabase) -> None:
    host = _Host()

    async def agent_runner(inp: AgentRunInput) -> AgentRunResult:
        host.stops[inp.run_id] = {"kind": "guardrail.max_turns", "message": "Stopped: limit — 4 turns"}
        return AgentRunResult(success=False, conversation_id="conv-1")

    _configure(fake_supabase, host, agent_runner)
    _seed(fake_supabase)
    await _fire_once(fake_supabase)

    assert _run(fake_supabase)["status"] == "stopped"
    assert fake_supabase.rows["sch_task"][0]["last_run_at"] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize("raises", [False, True])
async def test_a_one_shot_stopped_mid_run_is_settled_and_never_fires_again(fake_supabase, raises: bool) -> None:
    host = _Host()

    async def agent_runner(inp: AgentRunInput) -> AgentRunResult:
        host.stops[inp.run_id] = {"kind": "guardrail.max_cost_run", "message": "Stopped: limit — $2"}
        if raises:
            raise RuntimeError("GuardrailStopError")
        return AgentRunResult(success=False, conversation_id="conv-1")

    _configure(fake_supabase, host, agent_runner)
    _seed(fake_supabase)
    trigger = fake_supabase.rows["sch_trigger"][0]
    trigger["type"] = "one-shot"
    trigger["config"] = {"at": trigger["next_due_at"].isoformat()}
    await _fire_once(fake_supabase)

    assert _run(fake_supabase)["status"] == "stopped"
    assert fake_supabase.rows["sch_trigger"][0]["last_fired_at"] is not None
    assert await queries.find_due_tasks() == []


@pytest.mark.asyncio
async def test_the_runner_hands_run_and_task_provenance_to_the_host(fake_supabase) -> None:
    host = _Host()
    seen: list[AgentRunInput] = []

    async def agent_runner(inp: AgentRunInput) -> AgentRunResult:
        seen.append(inp)
        return AgentRunResult(success=True)

    _configure(fake_supabase, host, agent_runner)
    _seed(fake_supabase)
    fake_supabase.rows["sch_task"][0]["metadata"] = {"created_via": "person"}
    fake_supabase.rows["sch_task"][0]["created_by"] = USER
    await _fire_once(fake_supabase)
    assert seen and seen[0].task_metadata == {"created_via": "person"} and seen[0].task_created_by == USER
    assert "claim_protocol" in seen[0].run_metadata


def test_created_via_reads_the_creating_session() -> None:
    from types import SimpleNamespace

    from matrx_scheduler.api.router_scheduler import created_via

    assert created_via(SimpleNamespace(route="/scheduler/tasks", origin_class="human")) == "person"
    assert created_via(SimpleNamespace(route="mcp:schedule", origin_class="human")) == "agent"
    assert created_via(SimpleNamespace(route="/scheduler/tasks", origin_class="api")) == "agent"
