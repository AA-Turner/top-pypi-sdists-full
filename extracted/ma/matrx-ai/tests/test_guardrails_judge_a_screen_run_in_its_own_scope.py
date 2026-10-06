"""A run with no conversation (a screen calling a tool) is judged in its own
guardrail scope, which its owner clears; per-minute limits count per person
across runs. Before this, every conversation-less call landed in ONE shared,
never-cleared bucket keyed by ``None``: one person's calls tripped another's
duplicate guard and the bucket grew forever. Drives the real GuardrailEngine."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.tools.guardrails import GuardrailEngine
from matrx_ai.tools.models import ToolContext, ToolDefinition


@pytest.fixture(autouse=True)
def _no_conversation(monkeypatch):
    import matrx_ai.context.app_context as app_context

    ambient = SimpleNamespace(user_id="user-1", conversation_id=None, request_id="req-1")
    monkeypatch.setattr(app_context, "get_app_context", lambda: ambient)
    return ambient


def _ctx(scope: str | None, rate: str | None = None, call: str = "c") -> ToolContext:
    return ToolContext(call_id=call, tool_name="t", guardrail_scope=scope, rate_scope=rate)


ARGS = {"action": "overview", "domain": "example.com"}


@pytest.mark.asyncio
async def test_two_screen_runs_never_share_duplicate_history() -> None:
    engine = GuardrailEngine()
    tool = ToolDefinition(name="t")
    for _ in range(2):
        engine.record_call("t", ARGS, _ctx("screen:user-1:run-a"))

    # A third identical call in run A is a loop; the same call in run B is not.
    assert (await engine.check("t", ARGS, _ctx("screen:user-1:run-a"), tool)).blocked
    assert not (await engine.check("t", ARGS, _ctx("screen:user-2:run-b"), tool)).blocked


@pytest.mark.asyncio
async def test_a_cleared_run_scope_leaves_nothing_behind() -> None:
    engine = GuardrailEngine()
    engine.record_call("t", ARGS, _ctx("screen:user-1:run-a"))
    engine.clear_conversation("screen:user-1:run-a")
    assert dict(engine._history) == {}


@pytest.mark.asyncio
async def test_a_call_with_no_scope_and_no_conversation_is_never_pooled() -> None:
    engine = GuardrailEngine()
    tool = ToolDefinition(name="t")
    for n in range(4):
        engine.record_call("t", ARGS, _ctx(None, call=f"c{n}"))
    assert dict(engine._history) == {}
    assert not (await engine.check("t", ARGS, _ctx(None, call="c9"), tool)).blocked


@pytest.mark.asyncio
async def test_a_per_minute_limit_counts_the_person_across_runs() -> None:
    engine = GuardrailEngine()
    tool = ToolDefinition(name="t", max_calls_per_minute=2)
    for run in ("run-a", "run-b"):
        engine.record_call("t", {"n": run}, _ctx(f"screen:user-1:{run}", "screen-user:user-1"))
        engine.clear_conversation(f"screen:user-1:{run}")

    third = await engine.check("t", {"n": "c"}, _ctx("screen:user-1:run-c", "screen-user:user-1"), tool)
    other_person = await engine.check(
        "t", {"n": "c"}, _ctx("screen:user-2:run-d", "screen-user:user-2"), tool
    )
    assert third.blocked and third.error_type == "rate_limit"
    assert not other_person.blocked
