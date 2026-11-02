"""AN EDGE SELECTS A FIELD — dotted/indexed source paths, end to end.

The defect (live 2026-09-12, run ``cdde033d``): the Conductor believed an edge
mapping could only carry a top-level key or the whole upstream output, so it
built an extra step to pull a field out — and a merge step downstream was
handed four WHOLE agent results (their ``messages`` histories, the documents
inside them, usage, metadata) and blew a 1,000,000-token context window.

What is locked here:

1. a dotted source path resolves AT RUN TIME through the real scheduler, and
   delivers ONLY the selected field;
2. bracket/index syntax (``items[0].x``) resolves the same way — ONE resolver
   (``matrx_graph.paths``) behind edges, display steps and ``text.json_path``;
3. a path the upstream's declared output schema provably cannot produce is
   rejected AT VALIDATE TIME, naming the segment and what the step does emit;
4. an open/dynamic upstream output still passes through unchecked, exactly as
   before — an unprovable path is not a finding.
"""

from __future__ import annotations

from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition
from pydantic import BaseModel, ConfigDict, Field

from tests._fixtures import FakeEmitter, make_app_context


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Structured(BaseModel):
    """The nested half of an AI-shaped result."""

    model_config = ConfigDict(extra="forbid")

    entries: list[str] = Field(default_factory=list)


class _AiLike(BaseModel):
    """A closed, AI-shaped output: a big raw half and the field you want."""

    model_config = ConfigDict(extra="forbid")

    final_text: str = ""
    messages: list[dict[str, Any]] = Field(default_factory=list)
    structured_output: _Structured = Field(default_factory=_Structured)


class _AiLikeNode:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.ai_like",
        category=NodeCategory.DATA,
        display_name="ai-like",
        description="emits an AI-shaped closed output",
        input_schema=_In,
        output_schema=_AiLike,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg
    ) -> NodeResult[_AiLike]:
        return success(
            _AiLike(
                final_text="the whole ledger, at length",
                messages=[{"role": "user", "content": "a very long document" * 100}],
                structured_output=_Structured(entries=["one", "two"]),
            )
        )


class _SpyOut(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: bool = True


class _Spy:
    """Records exactly what the edge delivered."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.sel_spy",
        category=NodeCategory.DATA,
        display_name="spy",
        description="records delivered inputs",
        input_schema=_In,
        output_schema=_SpyOut,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.seen: list[dict[str, Any]] = []

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg
    ) -> NodeResult[_SpyOut]:
        self.seen.append(inputs.model_dump())
        return success(_SpyOut())


def _registry(*executors: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for ex in executors:
        reg.register(ex, overwrite=True)
    return reg


def _defn(mapping: dict[str, str]) -> dict:
    return {
        "version": "1",
        "nodes": [
            {"id": "a", "type": "test.ai_like", "position": {"x": 0, "y": 0}, "data": {}},
            {"id": "b", "type": "test.sel_spy", "position": {"x": 200, "y": 0}, "data": {}},
        ],
        "edges": [{"id": "e1", "source": "a", "target": "b", "data": {"mappings": mapping}}],
    }


async def _run(definition: dict, registry: NodeRegistry, run_id: str):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    return await scheduler.run(run_id=run_id)


# ---------------------------------------------------------------------------
# 1 + 2. Run time
# ---------------------------------------------------------------------------


async def test_dotted_source_path_delivers_only_the_selected_field():
    spy = _Spy()
    registry = _registry(_AiLikeNode(), spy)
    result = await _run(_defn({"entries": "structured_output.entries"}), registry, "sel-dotted")

    assert result.status is RunStatus.COMPLETED
    assert spy.seen == [{"entries": ["one", "two"]}]
    # The whole result — messages and all — never reached the next step.
    assert "messages" not in spy.seen[0]


async def test_indexed_source_path_resolves_through_the_one_resolver():
    spy = _Spy()
    registry = _registry(_AiLikeNode(), spy)
    result = await _run(_defn({"first": "structured_output.entries[0]"}), registry, "sel-indexed")

    assert result.status is RunStatus.COMPLETED
    assert spy.seen == [{"first": "one"}]


async def test_dotted_path_that_misses_at_run_time_arrives_absent():
    spy = _Spy()
    registry = _registry(_AiLikeNode(), spy)
    # `structured_output` is declared (so validation lets it through) but this
    # leaf is not there at run time (the list is shorter): data, not wiring.
    # The input arrives ABSENT and the target's own input check decides (this
    # spy requires nothing, so it runs without `x`). A path the declared output
    # can never have is refused at save (tests below) — 2026-10-27 contract,
    # tests/test_a_missing_mapping_path_arrives_absent.py.
    result = await _run(_defn({"x": "structured_output.entries[9]"}), registry, "sel-miss")

    assert result.status is RunStatus.COMPLETED, result.error
    assert len(spy.seen) == 1 and "x" not in spy.seen[0]


# ---------------------------------------------------------------------------
# 3 + 4. Validate time
# ---------------------------------------------------------------------------


def test_unknown_source_path_on_closed_schema_is_rejected():
    registry = _registry(_AiLikeNode(), _Spy())
    result = validate_definition(
        Definition.model_validate(_defn({"entries": "structured_output.items"})), registry=registry
    )

    assert not result.valid
    issue = next(i for i in result.issues if i.edge_id == "e1")
    assert issue.severity == "error"
    assert "structured_output.items" in issue.message
    assert "segment 'items'" in issue.message  # names WHICH segment
    assert "entries" in issue.message  # and what the step does emit


def test_unknown_top_level_source_key_is_rejected():
    registry = _registry(_AiLikeNode(), _Spy())
    result = validate_definition(
        Definition.model_validate(_defn({"entries": "nonexistent"})), registry=registry
    )
    assert not result.valid
    assert any("segment 'nonexistent'" in i.message for i in result.issues)


def test_valid_nested_path_passes_validation():
    registry = _registry(_AiLikeNode(), _Spy())
    result = validate_definition(
        Definition.model_validate(_defn({"entries": "structured_output.entries"})),
        registry=registry,
    )
    assert result.valid, [i.message for i in result.issues]


def test_open_upstream_output_still_passes_any_path_through():
    """data.transform's output is dynamic — the schema cannot rule anything
    out, so an unprovable path stays legal exactly as it was."""
    registry = _registry(_Spy())
    defn = {
        "version": "1",
        "nodes": [
            {
                "id": "a",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"expression": "{'v': 1}"}},
            },
            {"id": "b", "type": "test.sel_spy", "position": {"x": 200, "y": 0}, "data": {}},
        ],
        "edges": [
            {
                "id": "e1",
                "source": "a",
                "target": "b",
                "data": {"mappings": {"x": "anything.at.all"}},
            }
        ],
    }
    result = validate_definition(Definition.model_validate(defn), registry=registry)
    assert result.valid, [i.message for i in result.issues]
