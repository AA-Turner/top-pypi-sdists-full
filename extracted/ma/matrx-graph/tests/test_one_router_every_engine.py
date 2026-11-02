"""ONE router: every door calls ``run_action``; it sends the call to the Action's engine.

Arman, 2026-10-29: an Action is a name, a typed input, an ENGINE and a typed output;
"the key is to know how to send the task to the right engine". These tests run the
real router with real registries — they fail if a door bypasses it, if an Action on an
unregistered engine runs at all, or if a gated Action runs through a tool/mcp door
without the apply gate saying yes.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from pydantic import BaseModel

from matrx_graph.actions import (
    ActionFailed,
    ActionRegistry,
    ActionStarted,
    configure_action_ledger,
    last_run_replayed,
    configure_apply_gate,
    declare_action,
    declare_engine_action,
    register_engine,
    run_action,
)
from matrx_graph.actions import engines as engines_mod
from matrx_graph.executor.registry import NodeRegistry


class In(BaseModel):
    text: str


class Out(BaseModel):
    echoed: str


@pytest.fixture
def regs():
    return NodeRegistry(), ActionRegistry()


def _code_action(regs, *, writes: bool = False):
    nodes, actions = regs

    @declare_action(
        name="test.echo",
        description="echo",
        input_schema=In,
        output_schema=Out,
        doors={"step", "tool", "mcp"},
        node_registry=nodes,
        action_registry=actions,
        writes_or_spends=writes,
    )
    async def echo(app: Any, item: In) -> Out:
        return Out(echoed=item.text)

    return actions.get("test.echo")


def test_code_engine_runs_the_work_function(regs):
    spec = _code_action(regs)
    assert spec.engine == "code"
    out = asyncio.run(run_action("test.echo", {"text": "hi"}, app=None, registry=regs[1]))
    assert out == Out(echoed="hi")


def test_an_action_on_an_unregistered_engine_refuses_naming_it(regs, monkeypatch):
    monkeypatch.setattr(engines_mod, "_ENGINES", {"code": engines_mod._ENGINES["code"]})
    nodes, actions = regs
    spec = declare_engine_action(
        name="test.later", description="x", input_schema=In, output_schema=Out,
        engine="workflow", doors={"step"}, node_registry=nodes, action_registry=actions,
    )
    with pytest.raises(ActionFailed, match="workflow") as caught:
        asyncio.run(run_action(spec, {"text": "a"}, app=None))
    assert caught.value.code == "engine_not_registered"
    assert caught.value.suggested_action


def test_a_step_only_spec_refuses_as_action_not_runnable_never_a_type_error(regs):
    nodes, actions = regs
    spec = _code_action(regs)
    object.__setattr__(spec, "work", None)  # a step-only register_node has no plain work function
    with pytest.raises(ActionFailed) as caught:
        asyncio.run(run_action(spec, {"text": "a"}, app=None, door="tool"))
    assert caught.value.code == "action_not_runnable"
    assert caught.value.suggested_action


def test_a_ledger_replay_is_flagged_never_silent(regs, monkeypatch):
    monkeypatch.setattr(engines_mod, "_LEDGER", [])
    spec = _code_action(regs, writes=True)
    first: dict[str, Any] = {}

    async def ledger(spec, app, data, *, door, idempotency_key, run):
        if idempotency_key in first:
            return first[idempotency_key]  # a repeat: the first output, run never called
        first[idempotency_key] = await run()
        return first[idempotency_key]

    configure_action_ledger(ledger)
    async def scenario() -> list[bool]:
        seen = []
        for key in ("k1", "k1", None):
            await run_action(spec, {"text": "a"}, app=None, idempotency_key=key, door="step")
            seen.append(last_run_replayed())
        return seen

    try:
        # first run, repeat of the same key, then no key (no ledger → runs, never flagged)
        assert asyncio.run(scenario()) == [False, True, False]
    finally:
        configure_action_ledger(None)


RID = "6f1c2d3e-4b5a-4c6d-8e9f-0a1b2c3d4e5f"


def test_a_host_engine_runs_and_may_hand_back_a_started_handle(regs, monkeypatch):
    monkeypatch.setattr(engines_mod, "_ENGINES", dict(engines_mod._ENGINES))
    seen: list[str] = []

    async def wf_engine(spec, app, data, *, idempotency_key=None):
        seen.append(data.text)
        return ActionStarted(action=spec.name, request_id=RID)

    register_engine("workflow", wf_engine, overwrite=True)  # the host may have registered its own
    nodes, actions = regs
    spec = declare_engine_action(
        name="test.long", description="x", input_schema=In, output_schema=Out,
        engine="workflow", doors={"step"}, node_registry=nodes, action_registry=actions,
    )
    out = asyncio.run(run_action(spec, {"text": "go"}, app=None))
    assert isinstance(out, ActionStarted) and str(out.request_id) == RID and seen == ["go"]
    assert out.follow == f"/runtime/operations/{RID}" and out.rejoin == f"/runtime/operations/{RID}/rejoin"
    with pytest.raises(ValueError):
        ActionStarted(action="x", request_id=RID, follow="/somewhere/else")
    with pytest.raises(ValueError):
        ActionStarted(action="x", request_id="r-1")


def test_an_engine_returning_the_wrong_type_is_a_loud_defect(regs, monkeypatch):
    monkeypatch.setattr(engines_mod, "_ENGINES", dict(engines_mod._ENGINES))

    async def bad(spec, app, data, *, idempotency_key=None):
        return In(text="not the output")

    register_engine("outside", bad)
    nodes, actions = regs
    spec = declare_engine_action(
        name="test.bad", description="x", input_schema=In, output_schema=Out,
        engine="outside", doors={"step"}, node_registry=nodes, action_registry=actions,
    )
    with pytest.raises(TypeError, match="declared output"):
        asyncio.run(run_action(spec, {"text": "x"}, app=None))


def test_a_code_action_cannot_be_declared_without_its_work_function(regs):
    nodes, actions = regs
    with pytest.raises(ValueError, match="declare_action"):
        declare_engine_action(
            name="test.nowork", description="x", input_schema=In, output_schema=Out,
            engine="code", doors={"step"}, node_registry=nodes, action_registry=actions,
        )


def test_a_gated_action_never_runs_through_tool_or_mcp_without_the_gate(regs, monkeypatch):
    monkeypatch.setattr(engines_mod, "_GATE", [])
    spec = _code_action(regs, writes=True)
    assert spec.gated
    for door in ("tool", "mcp"):
        with pytest.raises(ActionFailed) as exc:
            asyncio.run(run_action(spec, {"text": "x"}, app=None, door=door))
        assert exc.value.code == "apply_off"
    # The directive door's dispatcher already resolved the policy; a step runs in the
    # person's own workflow — neither asks again.
    for door in ("directive", "step"):
        assert asyncio.run(run_action(spec, {"text": "x"}, app=None, door=door)) == Out(echoed="x")


def test_the_gate_decides_for_tool_and_mcp(regs, monkeypatch):
    monkeypatch.setattr(engines_mod, "_GATE", [])
    spec = _code_action(regs, writes=True)
    asked: list[tuple[str, str | None]] = []

    async def gate(spec, app, data, *, door, authority):
        asked.append((door, authority))
        if authority == "agent":
            raise ActionFailed("needs_approval", "ask the person")

    configure_apply_gate(gate)
    with pytest.raises(ActionFailed, match="ask the person"):
        asyncio.run(run_action(spec, {"text": "x"}, app=None, door="tool"))
    assert asyncio.run(run_action(spec, {"text": "x"}, app=None, door="mcp")) == Out(echoed="x")
    assert asyncio.run(run_action(spec, {"text": "x"}, app=None, door="step")) == Out(echoed="x")
    assert asyncio.run(run_action(spec, {"text": "x"}, app=None, door="api")) == Out(echoed="x")
    # The caller names its own authority over its door's.
    with pytest.raises(ActionFailed):
        asyncio.run(run_action(spec, {"text": "x"}, app=None, door="api", authority="agent"))
    # The directive door's dispatcher already resolved it: never asked twice.
    assert asyncio.run(run_action(spec, {"text": "x"}, app=None, door="directive")) == Out(echoed="x")
    assert asked == [
        ("tool", "agent"), ("mcp", "person"), ("step", "workflow"), ("api", "person"), ("api", "agent"),
    ]


def test_a_lazy_source_resolves_a_generated_action_by_name(regs, monkeypatch):
    """Generated Actions (workflows, agents) are rows, not code: a source resolves them
    by name at call time — through the SAME run_action — and an unknown one is not found."""
    from matrx_graph.types.primitives import ActionTier, NodeCategory
    from matrx_graph.actions.spec import ActionSpec, build_action_node_spec
    from matrx_graph.errors import NodeRegistryError

    _nodes, actions = regs
    seen: list[str] = []
    generated = ActionSpec(
        name="lazy.thing", description="generated", input_schema=In, output_schema=Out,
        node_spec=build_action_node_spec(
            name="lazy.thing", description="", category=NodeCategory.CUSTOM,
            determinism=ActionTier.NON_DETERMINISTIC, input_schema=In, output_schema=Out,
            icon=None, tags=(), version="1.0.0",
        ),
        engine="outside", doors=frozenset({"api", "mcp"}),
    )

    async def source(name, app):
        seen.append(name)
        return generated if name == "lazy.thing" else None

    async def outside(spec, app, data, *, idempotency_key=None):
        return Out(echoed=f"{spec.name}:{data.text}")

    monkeypatch.setitem(engines_mod._ENGINES, "outside", outside)
    actions.add_source("lazy", source)
    assert asyncio.run(run_action("lazy.thing", {"text": "x"}, app=None, door="api", registry=actions)) == Out(echoed="lazy.thing:x")
    with pytest.raises(NodeRegistryError):
        asyncio.run(run_action("lazy.missing", {"text": "x"}, app=None, door="api", registry=actions))
    assert seen == ["lazy.thing", "lazy.missing"]
    assert generated.door_names()["api"] == "/actions/lazy.thing/run"
    assert generated.to_descriptor()["apply_rule"] == "auto"



def test_an_ungated_action_never_asks(regs, monkeypatch):
    monkeypatch.setattr(engines_mod, "_GATE", [])
    spec = _code_action(regs, writes=False)
    assert asyncio.run(run_action(spec, {"text": "x"}, app=None, door="tool")) == Out(echoed="x")
