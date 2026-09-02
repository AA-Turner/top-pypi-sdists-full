"""D-39 — depth-refused member calls are LOUD on the chat path.

Before this, a projected AGENT tool refused by the recursion guardrail was
visible only as an error ToolResult the orchestrator could quietly absorb —
the user got a confident answer silently missing a member's contribution.
Now the executor additionally emits a `member_depth_exhausted` warning event.

Also pins the D-39 projection contract: `AgentToolSpec.max_recursion_depth`
overrides the module constant on the stamped ToolDefinition; None keeps it.
"""
from __future__ import annotations

import inspect
from typing import Any

import pytest

from matrx_ai.tools.agent_projection import (
    PROJECTED_AGENT_MAX_RECURSION_DEPTH,
    resolve_agent_specs,
)
from matrx_ai.tools.executor import warn_member_depth_exhausted
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType
from matrx_ai.tools.specs import AgentToolSpec


class _WarningCapture:
    def __init__(self) -> None:
        self.payloads: list[Any] = []

    async def send_warning(self, payload: Any) -> None:
        self.payloads.append(payload)


class _FakeAppContext:
    def __init__(self, emitter: Any = None) -> None:
        self.emitter = emitter
        self.metadata: dict[str, Any] = {}


def _member_tool(ceiling: int) -> ToolDefinition:
    return ToolDefinition(
        name="custom_tool_1",
        tool_type=ToolType.AGENT,
        prompt_id="agent-abc",
        max_recursion_depth=ceiling,
    )


# ---------------------------------------------------------------------------
# The warning event
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_depth_refusal_emits_member_depth_exhausted_warning(monkeypatch):
    from matrx_ai.context import app_context as app_context_mod

    emitter = _WarningCapture()
    monkeypatch.setattr(
        app_context_mod, "try_get_app_context", lambda: _FakeAppContext(emitter=emitter)
    )

    await warn_member_depth_exhausted(
        ToolContext(call_id="c1", recursion_depth=2), _member_tool(2), "custom_tool_1"
    )

    assert len(emitter.payloads) == 1
    payload = emitter.payloads[0]
    assert payload.code == "member_depth_exhausted"
    # Names the member, the depth, and the ceiling — the D-39 loudness contract.
    assert payload.metadata == {
        "tool_name": "custom_tool_1",
        "agent_id": "agent-abc",
        "depth": 2,
        "ceiling": 2,
    }
    assert "2 levels deep" in (payload.user_message or "")
    assert payload.recoverable is True


@pytest.mark.asyncio
async def test_warning_never_breaks_the_run(monkeypatch):
    """Emitter explosion (or absence) is swallowed loudly — the refusal
    ToolResult is the run's outcome; the warning is strictly additive."""
    from matrx_ai.context import app_context as app_context_mod

    class _Exploding:
        async def send_warning(self, payload: Any) -> None:
            raise RuntimeError("wire down")

    monkeypatch.setattr(
        app_context_mod,
        "try_get_app_context",
        lambda: _FakeAppContext(emitter=_Exploding()),
    )
    await warn_member_depth_exhausted(
        ToolContext(call_id="c1", recursion_depth=2), _member_tool(2), "custom_tool_1"
    )  # must not raise

    monkeypatch.setattr(app_context_mod, "try_get_app_context", lambda: None)
    await warn_member_depth_exhausted(
        ToolContext(call_id="c1", recursion_depth=2), _member_tool(2), "custom_tool_1"
    )  # no context, no emitter — still must not raise


def test_executor_guardrail_branch_wires_the_warning():
    """The dispatch pipeline calls the warning helper on a recursion_depth
    block of an AGENT tool — structural pin so a refactor can't drop it."""
    from matrx_ai.tools.executor import ToolExecutor

    source = inspect.getsource(ToolExecutor)
    assert "warn_member_depth_exhausted" in source
    assert '"recursion_depth"' in source


# ---------------------------------------------------------------------------
# Projection honors the per-spec override (D-39)
# ---------------------------------------------------------------------------


def _fake_agent_row(agent_id: str):
    class _Row:
        name = f"Agent {agent_id}"
        description = "A member agent."
        variable_definitions: list[Any] = []
        output_schema = None

    return _Row()


@pytest.mark.asyncio
async def test_projection_honors_spec_depth_override(monkeypatch):
    from matrx_ai.tools import agent_projection as proj_mod

    async def fake_load(agent_id: str, *, is_version: bool):
        return _fake_agent_row(agent_id)

    monkeypatch.setattr(proj_mod, "_load_agent_row", fake_load)

    ctx = _FakeAppContext()
    _, projections = await resolve_agent_specs(
        [
            AgentToolSpec(agent_id="member-custom", max_recursion_depth=4),
            AgentToolSpec(agent_id="member-default"),
        ],
        ctx,  # type: ignore[arg-type]
    )

    by_agent = {p["prompt_id"]: p for p in projections.values()}
    # The composition-declared budget wins…
    assert by_agent["member-custom"]["max_recursion_depth"] == 4
    # …and an undeclared spec keeps the platform constant.
    assert (
        by_agent["member-default"]["max_recursion_depth"]
        == PROJECTED_AGENT_MAX_RECURSION_DEPTH
    )
