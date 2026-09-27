"""A workflow agent step runs under its ORGANIZATION'S iteration limit, and says so when it stops.

Use case: a bookkeeping firm sets "Workflows › Agent step iteration limit" to 3 so a
month-end reconciliation workflow can never let an agent grind through a hundred tool
rounds on one invoice. Its reconciliation step (an "Agent with Tools" and a "Run Agent"
step, neither with a limit of its own) must run with 3 — not the 100 that used to be
frozen in the node input — and when the agent hits 3 the run's failure must name that
setting, so the person reading the run knows exactly which knob stopped it.

The provider and the host agent runner are the only stand-ins (the same seams
``test_node_handlers_execute`` uses); the node, the limit resolution and the failure
path are the real code. RED before 2026-09-26: the node sent ``max_iterations=100``
whatever the organization said, and the failure read only "Stopped after 100 iterations".
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph.actions.decorator import resolve_action_executor
from matrx_graph.types.node_spec import EmptyConfig
from matrx_graph.types.result import Failure, Success

from matrx_ai.graph_nodes import iteration_limit
from matrx_ai.graph_nodes.tests.test_node_handlers_execute import (
    NODE_FIXTURES,
    _FakeCompleted,
    _patch_agent_host,
)

FIRM_ORG = "b00k7eep-0000-4000-8000-000000000003"


def _stopped_at(limit: int) -> _FakeCompleted:
    """What the orchestrator hands back when the loop reaches its cap."""
    return _FakeCompleted(
        iterations=limit,
        metadata={
            "status": "max_iterations_exceeded",
            "error_type": "max_iterations_exceeded",
            "error": (
                f"Stopped after {limit} iterations to avoid a runaway loop. "
                "Reply with 'continue' or new guidance to resume."
            ),
        },
    )


@pytest.fixture
def firm_limit_is_three(monkeypatch: pytest.MonkeyPatch) -> list[str | None]:
    asked: list[str | None] = []

    async def _resolver(organization_id: str | None) -> int:
        asked.append(organization_id)
        return 3 if organization_id == FIRM_ORG else 100

    monkeypatch.setattr(iteration_limit, "_RESOLVER", _resolver)
    return asked


def _patch_provider_recording(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    from matrx_ai.orchestrator import executor as executor_module

    seen: dict[str, Any] = {}

    async def _fake(*_a: Any, max_iterations: int, **_k: Any) -> Any:
        seen["max_iterations"] = max_iterations
        return _stopped_at(max_iterations)

    monkeypatch.setattr(executor_module, "execute_ai_request", _fake)
    return seen


@pytest.mark.asyncio
async def test_tool_calling_step_runs_under_the_orgs_limit_and_names_it(
    monkeypatch: pytest.MonkeyPatch, firm_limit_is_three: list[str | None]
) -> None:
    inputs, ctx = NODE_FIXTURES["ai.agent.tool_calling"](monkeypatch)
    ctx.app = ctx.app.with_overrides(organization_id=FIRM_ORG)
    seen = _patch_provider_recording(monkeypatch)

    result = await resolve_action_executor("ai.agent.tool_calling").execute(
        ctx, inputs, EmptyConfig()
    )

    assert firm_limit_is_three == [FIRM_ORG], "the organization's setting was not consulted"
    assert seen["max_iterations"] == 3, f"ran with {seen['max_iterations']}, not the org's 3"
    assert isinstance(result, Failure)
    message = result.error.message
    assert "Agent step iteration limit" in message
    assert "workflow.run_limits/agent_max_iterations = 3" in message
    assert "Stopped after 3 iterations" in message, "the orchestrator's own sentence was lost"
    assert result.error.details["iteration_limit_setting"]["value"] == 3


@pytest.mark.asyncio
async def test_run_agent_step_sends_the_orgs_limit_to_the_host(
    monkeypatch: pytest.MonkeyPatch, firm_limit_is_three: list[str | None]
) -> None:
    inputs, ctx = NODE_FIXTURES["ai.agent.start"](monkeypatch)
    ctx.app = ctx.app.with_overrides(organization_id=FIRM_ORG)
    sent = _patch_agent_host(monkeypatch, completed=_stopped_at(3))

    result = await resolve_action_executor("ai.agent.start").execute(ctx, inputs, EmptyConfig())

    assert sent["request"].max_iterations == 3
    assert isinstance(result, Failure)
    assert "Agent step iteration limit" in result.error.message


@pytest.mark.asyncio
async def test_a_limit_the_author_set_on_the_step_wins_and_is_not_blamed_on_the_setting(
    monkeypatch: pytest.MonkeyPatch, firm_limit_is_three: list[str | None]
) -> None:
    inputs, ctx = NODE_FIXTURES["ai.agent.tool_calling"](monkeypatch)
    ctx.app = ctx.app.with_overrides(organization_id=FIRM_ORG)
    inputs.max_iterations = 7
    seen = _patch_provider_recording(monkeypatch)

    result = await resolve_action_executor("ai.agent.tool_calling").execute(
        ctx, inputs, EmptyConfig()
    )

    assert seen["max_iterations"] == 7
    assert firm_limit_is_three == [], "an authored limit must not read the setting"
    assert isinstance(result, Failure)
    assert "Agent step iteration limit" not in result.error.message


@pytest.mark.asyncio
async def test_a_step_that_finishes_is_untouched(
    monkeypatch: pytest.MonkeyPatch, firm_limit_is_three: list[str | None]
) -> None:
    inputs, ctx = NODE_FIXTURES["ai.agent.tool_calling"](monkeypatch)
    ctx.app = ctx.app.with_overrides(organization_id=FIRM_ORG)

    result = await resolve_action_executor("ai.agent.tool_calling").execute(
        ctx, inputs, EmptyConfig()
    )

    assert isinstance(result, Success)


@pytest.mark.asyncio
async def test_an_unreadable_setting_falls_back_loudly_never_fails_the_step(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def _broken(_org: str | None) -> int:
        raise RuntimeError("knob row missing")

    monkeypatch.setattr(iteration_limit, "_RESOLVER", _broken)
    assert await iteration_limit.organization_agent_max_iterations(FIRM_ORG) == 100
