"""A large step result is kind-checked, dumped and ruled on in a worker thread, never on the loop.

Live 2026-11-07: event_loop_stall 52b1cbc57629ba4f froze a workflow worker 7.2 s inside
``check_against_kind`` (strip markers, then jsonschema); 410e60402d73ead7 held the API 2.2 s in
``data.rules`` deciding a long list; 099e931506207bd1 / 7925f60e9d325ec2 held it 1.6-2 s dumping
a step's output. RED before: every spy below saw the loop thread.
"""

from __future__ import annotations

import asyncio
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, field_serializer

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import kinds
from matrx_graph.nodes.data import rules as rules_module
from matrx_graph.nodes.data.rules import RulesConfig, RulesInput, RulesExecutor
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

ITEMS = 3000  # well over values.OFF_LOOP_MIN_NODES once counted with their keys


def _on_loop() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


async def test_a_large_value_is_kind_checked_off_the_loop(monkeypatch) -> None:
    seen: list[bool] = []
    real = kinds.validate_instance_checked

    def spy(schema: dict[str, Any], instance: Any, **kw: Any) -> tuple[list[str], bool]:
        seen.append(_on_loop())
        return real(schema, instance, **kw)

    async def resolved(slug: str):
        return kinds.KindEntry(slug=slug, version=1, json_schema={"type": "object"}), None

    monkeypatch.setattr(kinds, "validate_instance_checked", spy)
    monkeypatch.setattr(kinds, "resolve_kind", resolved)
    check = await kinds.check_against_kind({"rows": [{"n": i} for i in range(ITEMS)]}, "any_kind")
    assert seen == [False]
    assert check.checked and check.errors == []


async def test_a_small_value_is_still_checked_inline_with_the_same_verdict(monkeypatch) -> None:
    seen: list[bool] = []
    real = kinds.validate_instance_checked

    def spy(schema: dict[str, Any], instance: Any, **kw: Any) -> tuple[list[str], bool]:
        seen.append(_on_loop())
        return real(schema, instance, **kw)

    async def resolved(slug: str):
        schema = {"type": "object", "required": ["a"]}
        return kinds.KindEntry(slug=slug, version=1, json_schema=schema), None

    monkeypatch.setattr(kinds, "validate_instance_checked", spy)
    monkeypatch.setattr(kinds, "resolve_kind", resolved)
    check = await kinds.check_against_kind({"b": 1}, "any_kind")
    assert seen == [True]
    assert check.checked and len(check.errors) == 1


async def test_a_long_list_is_ruled_on_off_the_loop_and_every_item_is_decided(monkeypatch) -> None:
    seen: list[bool] = []
    real = rules_module._decide

    def spy(*args: Any, **kw: Any) -> Any:
        seen.append(_on_loop())
        return real(*args, **kw)

    monkeypatch.setattr(rules_module, "_decide", spy)
    config = RulesConfig.model_validate(
        {"items_path": "rows", "rules": [{"when": "inputs['item']['n'] >= 0", "then": {"label": "kept"}}]}
    )
    inputs = RulesInput.model_validate({"rows": [{"n": i} for i in range(ITEMS)]})
    result = await RulesExecutor().execute(object(), inputs, config)
    assert len(seen) == ITEMS and not any(seen)
    assert result.result.counts == {"kept": ITEMS}


DUMPS: list[bool] = []


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Out(BaseModel):
    ledger: Any = None

    @field_serializer("ledger")
    def _record(self, value: Any) -> Any:
        DUMPS.append(_on_loop())
        return value


class _Make:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.big_output",
        category=NodeCategory.DATA,
        display_name="Make",
        description="Emits a large output.",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        return success(_Out(ledger=[{"n": i} for i in range(ITEMS)]))


async def test_a_large_step_output_is_dumped_off_the_loop() -> None:
    DUMPS.clear()
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Make())
    definition = Definition.model_validate(
        {
            "nodes": [{"id": "make", "type": "test.big_output", "position": {"x": 0, "y": 0}, "data": {"config": {}}}],
            "edges": [],
            "entry_nodes": ["make"],
        }
    )
    scheduler = Scheduler(
        compile_graph(definition, registry=registry),
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    await scheduler.run(run_id="00000000-0000-4000-8000-00000000abcd")
    assert DUMPS, "the output was never dumped"
    assert not any(DUMPS), f"{sum(DUMPS)} of {len(DUMPS)} dumps ran on the event loop"
