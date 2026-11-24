"""A child that a limit or a stop ended is reported as THAT to its parent, whatever ``success`` says.

Failure register 2026-11-15, entry 8: ``agent_call`` failed any child with ``success=False`` before it reached
the bounded marker, so a cancelled child showed as "failed". A run whose ``stop_cause`` is cancelled / time /
cost / rounds comes back as a bounded result naming it; a run that really failed (no stop cause) still fails.

SUT: ``agent_call``. The double replaces only what it CALLS: the agent loader, the access check and
``run_agent`` (returning the ``AgentRunResult`` the loop would build).
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
_AGENT_ID = "3b1f6c1e-7d0a-4f0e-9a51-2f4c8f0d9e21"


async def _value(v: Any) -> Any:
    return v


async def _call(monkeypatch, run_result: Any) -> Any:
    import matrx_ai._ext as ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.db.agx_manager import AgxDefinition
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)
    monkeypatch.setattr(
        AgxDefinition,
        "load_by_id_or_none",
        classmethod(
            lambda _cls, _id: _value(
                SimpleNamespace(id=_AGENT_ID, created_by=_USER_ID, is_active=True, is_archived=False)
            )
        ),
    )

    class _ChildAgent:
        name = "Senior desk"
        output_schema = None
        async def run_first_turn_pass(self):  # the real pass: present on every Agent
            return self

    monkeypatch.setattr(Agent, "from_agent", classmethod(lambda _cls, *a, **k: _value(_ChildAgent())))

    async def fake_run_agent(_agent: Any, **kwargs: Any) -> Any:
        return run_result

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    token = set_app_context(
        AppContext(emitter=None, user_id=_USER_ID, organization_id="0a900000-0000-4000-8000-00000000a7a7")
    )
    try:
        return await agent_call({"agent_id": _AGENT_ID}, ToolContext(call_id="call-1"))
    finally:
        clear_app_context(token)


def _run(**kw: Any) -> Any:
    from matrx_ai.agents.executor import AgentRunResult

    return AgentRunResult(**{"success": False, "error": "stopped", "error_kind": "execution", **kw})


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["cancelled", "time", "cost", "rounds"])
async def test_a_limit_stop_is_reported_as_that_even_when_success_is_false(monkeypatch, kind: str) -> None:
    from matrx_ai.orchestrator.stop_cause import RunStopCause

    stop = RunStopCause(kind=kind, detail="the person stopped it")
    result = await _call(monkeypatch, _run(output="half of the answer", stop_cause=stop, metadata={"status": "cancelled"}))

    assert result.success is True, "a stop at a limit is a bounded result, not a failure"
    bounded = result.output["bounded"]
    assert bounded["stop_cause"]["kind"] == kind
    assert "failed" not in bounded["detail"].lower()


@pytest.mark.asyncio
async def test_a_run_that_really_failed_still_fails(monkeypatch) -> None:
    result = await _call(monkeypatch, _run(error="the provider refused", metadata={"status": "failed"}))
    assert result.success is False
    assert "the provider refused" in result.error.message


@pytest.mark.asyncio
async def test_a_dollar_cap_stop_at_the_round_ceiling_is_cost_not_rounds(monkeypatch) -> None:
    """The mislabel the old inference made: a spend stop that ended AT the round ceiling read as rounds.

    The run carries ``status=max_iterations_exceeded`` AND the budget wrap-up, and the loop's own stop cause
    says cost. The marker the parent reads must say cost, with the numbers."""
    from matrx_ai.orchestrator.stop_cause import cost_cause

    result = await _call(
        monkeypatch,
        _run(
            success=True,
            output="half of the answer",
            stop_cause=cost_cause(allowed=0.5, used=0.52, detail="cap"),
            metadata={"status": "max_iterations_exceeded", "max_iterations": 12, "budget_wrap_up": True},
        ),
    )
    bounded = result.output["bounded"]
    assert bounded["stopped_by"] == "cost", bounded
    assert "round" not in bounded["detail"].lower()
    assert bounded["stop_cause"]["allowed"] == 0.5 and bounded["stop_cause"]["used"] == 0.52
