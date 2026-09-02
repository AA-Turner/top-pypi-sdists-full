"""Regression tests for cross-agent recursion-depth threading (2026-07-01).

Pins the dead-guard defect: the orchestrator built every ToolContext with
``recursion_depth=0`` and nothing bumped depth across the ``run_agent``
boundary, so the ``ToolType.AGENT`` ``max_recursion_depth`` guardrail could
never fire — A→B→C→… nested unbounded.

Post-review hardening (2026-07-02): the depth travels via a TASK-LOCAL context
rebinding (``set_app_context(with_overrides(...))``), NEVER an in-place bump on
the shared metadata dict — concurrent sibling tool calls in one batch share
that dict (asyncio.gather), so a shared bump/restore raced siblings into false
nesting and could permanently inflate the parent's depth.
"""
from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.guardrails import GuardrailEngine
from matrx_ai.tools.models import (
    AGENT_DEPTH_METADATA_KEY,
    ToolContext,
    ToolDefinition,
    ToolType,
    read_agent_depth,
)


class _FakeAppContext:
    def __init__(self, metadata: dict[str, Any] | None = None):
        self.metadata = metadata if metadata is not None else {}

    def with_overrides(self, **kwargs):
        clone = _FakeAppContext(metadata=dict(self.metadata))
        for k, v in kwargs.items():
            setattr(clone, k, v)
        return clone


def test_read_agent_depth_handles_missing_and_garbage():
    assert read_agent_depth(None) == 0
    assert read_agent_depth({}) == 0
    assert read_agent_depth({AGENT_DEPTH_METADATA_KEY: 2}) == 2
    assert read_agent_depth({AGENT_DEPTH_METADATA_KEY: "3"}) == 3
    assert read_agent_depth({AGENT_DEPTH_METADATA_KEY: "junk"}) == 0
    assert read_agent_depth({AGENT_DEPTH_METADATA_KEY: None}) == 0


def _projected_agent_tool() -> ToolDefinition:
    return ToolDefinition(
        name="custom_tool_1",
        tool_type=ToolType.AGENT,
        prompt_id="abc-123",
        max_recursion_depth=2,
    )


def test_guardrail_blocks_agent_tool_at_max_depth():
    guard = GuardrailEngine()
    tool_def = _projected_agent_tool()

    allowed = guard._check_recursion_depth(
        ToolContext(call_id="c", recursion_depth=1), tool_def
    )
    assert allowed.blocked is False

    blocked = guard._check_recursion_depth(
        ToolContext(call_id="c", recursion_depth=2), tool_def
    )
    assert blocked.blocked is True
    assert blocked.error_type == "recursion_depth"


def _patch_agent_stack(monkeypatch, app_ctx, on_run):
    """Patch context access + Agent load + run_agent around execute_agent_tool."""
    from matrx_ai.tools import agent_tool as agent_tool_mod

    bindings: list[Any] = []

    def fake_set_app_context(ctx):
        bindings.append(ctx)

    def fake_try_get():
        # The "active" context is the most recent binding, like the ContextVar.
        return bindings[-1] if bindings else app_ctx

    monkeypatch.setattr(agent_tool_mod, "try_get_app_context", fake_try_get)
    monkeypatch.setattr(agent_tool_mod, "set_app_context", fake_set_app_context)

    async def fake_from_agent(agent_id, is_version=False, variables=None, **kw):
        return object()

    import matrx_ai.agents.definition as definition_mod
    import matrx_ai.agents.executor as executor_mod

    monkeypatch.setattr(
        definition_mod.Agent, "from_agent", classmethod(
            lambda cls, agent_id, is_version=False, variables=None, **kw: fake_from_agent(
                agent_id, is_version=is_version, variables=variables, **kw
            )
        ),
    )
    monkeypatch.setattr(executor_mod, "run_agent", on_run)
    return bindings


@pytest.mark.asyncio
async def test_child_sees_bumped_depth_without_shared_mutation(monkeypatch):
    from matrx_ai.tools import agent_tool as agent_tool_mod

    app_ctx = _FakeAppContext(metadata={AGENT_DEPTH_METADATA_KEY: 1})
    seen: dict[str, int] = {}

    async def fake_run_agent(agent, *, label, source_feature, user_input, suppress_stream=False, **_kw):
        # What run_agent's fork would copy: the ACTIVE binding's metadata.
        active = agent_tool_mod.try_get_app_context()
        seen["depth"] = read_agent_depth(active.metadata)
        from matrx_ai.agents.executor import AgentRunResult

        return AgentRunResult(success=True, output="ok")

    bindings = _patch_agent_stack(monkeypatch, app_ctx, fake_run_agent)

    # _execute_agent hands the tool a ToolContext already bumped to parent+1.
    result = await agent_tool_mod.execute_agent_tool(
        _projected_agent_tool(), {"input": "task"}, ToolContext(call_id="c1", recursion_depth=2)
    )

    assert result.success is True
    # The child fork saw the bumped depth from the ToolContext…
    assert seen["depth"] == 2
    # …the SHARED parent dict was never mutated (the race-fix invariant)…
    assert app_ctx.metadata[AGENT_DEPTH_METADATA_KEY] == 1
    # …and the task binding was restored to the original context afterwards.
    assert bindings[-1] is app_ctx


@pytest.mark.asyncio
async def test_binding_restored_even_when_run_agent_raises(monkeypatch):
    from matrx_ai.tools import agent_tool as agent_tool_mod

    app_ctx = _FakeAppContext()

    async def exploding_run_agent(agent, **kwargs):
        raise RuntimeError("boom")

    bindings = _patch_agent_stack(monkeypatch, app_ctx, exploding_run_agent)

    result = await agent_tool_mod.execute_agent_tool(
        _projected_agent_tool(), {"input": "task"}, ToolContext(call_id="c1", recursion_depth=1)
    )

    assert result.success is False
    assert AGENT_DEPTH_METADATA_KEY not in app_ctx.metadata  # never mutated
    assert bindings[-1] is app_ctx  # restored


@pytest.mark.asyncio
async def test_concurrent_siblings_do_not_race_depth(monkeypatch):
    """Two sibling agent-tool calls with the same parent context must each see
    depth parent+1 — never each other's bump — and leave the parent untouched.
    (With task-local rebinding this holds even under interleaved awaits.)"""
    import asyncio

    from matrx_ai.tools import agent_tool as agent_tool_mod

    app_ctx = _FakeAppContext(metadata={AGENT_DEPTH_METADATA_KEY: 0})
    depths_seen: list[int] = []
    release = asyncio.Event()

    async def slow_run_agent(agent, *, label, source_feature, user_input, suppress_stream=False, **_kw):
        active = agent_tool_mod.try_get_app_context()
        depths_seen.append(read_agent_depth(active.metadata))
        await release.wait()
        from matrx_ai.agents.executor import AgentRunResult

        return AgentRunResult(success=True, output="ok")

    _patch_agent_stack(monkeypatch, app_ctx, slow_run_agent)

    async def one_call():
        # Each sibling runs in its own task (as execute_batch does), so each
        # task's binding stack is independent in production; the fake here
        # shares the binding list, but the parent dict must stay untouched
        # regardless — that is the invariant that kills the race.
        return await agent_tool_mod.execute_agent_tool(
            _projected_agent_tool(), {"input": "t"}, ToolContext(call_id="c", recursion_depth=1)
        )

    t1 = asyncio.create_task(one_call())
    t2 = asyncio.create_task(one_call())
    await asyncio.sleep(0.01)
    release.set()
    r1, r2 = await asyncio.gather(t1, t2)

    assert r1.success and r2.success
    # Both siblings saw THEIR OWN ToolContext depth (parent 0 → child 1) —
    # never each other's bump (the old shared-dict race made one sibling see 2).
    assert depths_seen == [1, 1]
    # The invariant that kills the race: the shared dict was NEVER written.
    assert app_ctx.metadata[AGENT_DEPTH_METADATA_KEY] == 0
