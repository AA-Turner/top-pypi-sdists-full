"""control.map payload_template — per-item payload shaping at dispatch time.

When MapConfig.payload_template is set, each dispatched payload is a deep
substitution of the template against the item: '$item' → the whole item,
'$item.<dot.path>' → that path into the item (digit segments index lists),
everything else literal, recursing into nested dicts/lists. A missing path
fails the node loudly (parks, recoverable). Template shaping must live in
the map executor itself: send-invocation distinctness dies at the first
edge hop, so a downstream transform can never shape per-item payloads.

Verifies:
    1. Classic payload_key behavior unchanged when template is None.
    2. '$item', '$item.path', nested templates, literals, include_index.
    3. Missing path → ExecutionError → run parks ERRORED.
    4. max_dispatches cap unaffected by templating.
"""

from __future__ import annotations

from typing import Any, ClassVar

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._template import substitute_template as _substitute_template
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

_received: list[dict[str, Any]] = []


class _SinkInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _SinkOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ok: bool = True


class _SinkConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _SinkExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.payload_sink",
        category=NodeCategory.DATA,
        display_name="Payload sink",
        description="Records every payload it is invoked with.",
        input_schema=_SinkInput,
        output_schema=_SinkOutput,
        config_schema=_SinkConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        inputs: _SinkInput,
        _config: _SinkConfig,
    ) -> NodeResult[_SinkOutput]:
        _received.append(inputs.model_dump())
        return success(_SinkOutput())


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_SinkExecutor(), overwrite=True)
    return reg


def _definition(map_config: dict[str, Any], items: list[Any]) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "fanout",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "sink", **map_config},
                        "input": {"items": items},
                    },
                },
                {
                    "id": "sink",
                    "type": "test.payload_sink",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [],
            "entry_nodes": ["fanout"],
        }
    )


async def _run(definition: Definition, run_id: str) -> Any:
    _received.clear()
    registry = _registry()
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    return await scheduler.run(run_id=run_id)


async def test_no_template_keeps_payload_key_shape():
    result = await _run(_definition({"payload_key": "value"}, ["a", "b"]), "tmpl-none")
    assert result.status is RunStatus.COMPLETED
    assert sorted(p["value"] for p in _received) == ["a", "b"]


async def test_template_substitutes_item_paths_and_literals():
    cards = [
        {"question": "Q1", "answer": "A1", "meta": {"tags": ["x", "y"]}},
        {"question": "Q2", "answer": "A2", "meta": {"tags": ["z"]}},
    ]
    template = {
        "user_input": "$item.question",
        "variables": {
            "front": "$item.question",
            "back": "$item.answer",
            "first_tag": "$item.meta.tags.0",
            "topic": "General Chemistry",
            "whole_card": "$item",
        },
        "count": 25,
    }
    result = await _run(_definition({"payload_template": template}, cards), "tmpl-paths")
    assert result.status is RunStatus.COMPLETED
    assert len(_received) == 2
    by_input = {p["user_input"]: p for p in _received}
    assert by_input["Q1"]["variables"] == {
        "front": "Q1",
        "back": "A1",
        "first_tag": "x",
        "topic": "General Chemistry",
        "whole_card": cards[0],
    }
    assert by_input["Q2"]["variables"]["first_tag"] == "z"
    assert all(p["count"] == 25 for p in _received)


async def test_template_with_include_index():
    result = await _run(
        _definition(
            {"payload_template": {"v": "$item"}, "include_index": True},
            ["a", "b", "c"],
        ),
        "tmpl-idx",
    )
    assert result.status is RunStatus.COMPLETED
    assert sorted((p["v"], p["index"]) for p in _received) == [
        ("a", 0),
        ("b", 1),
        ("c", 2),
    ]


async def test_missing_path_parks_run():
    result = await _run(
        _definition(
            {"payload_template": {"q": "$item.question"}},
            [{"question": "Q1"}, {"answer": "no question here"}],
        ),
        "tmpl-miss",
    )
    assert result.status is RunStatus.ERRORED


async def test_cap_still_enforced_with_template():
    result = await _run(
        _definition(
            {"payload_template": {"v": "$item"}, "max_dispatches": 2},
            ["a", "b", "c"],
        ),
        "tmpl-cap",
    )
    assert result.status is RunStatus.ERRORED


def test_substitute_template_unit():
    item = {"a": {"b": [10, 20]}}
    assert _substitute_template("$item", item, index=0) == item
    assert _substitute_template("$item.a.b.1", item, index=0) == 20
    assert _substitute_template("plain", item, index=0) == "plain"
    assert _substitute_template({"x": ["$item.a.b.0", False, None]}, item, index=0) == {
        "x": [10, False, None]
    }
    with pytest.raises(ExecutionError, match=r"\$item\.a\.c"):
        _substitute_template("$item.a.c", item, index=3)


def test_substitute_template_indirect_segment():
    """'{sibling}' resolves against the same root and becomes the segment.

    The shape this exists for: an LLM emits a list plus a sibling index into
    it ('choices' + 'correct_index'). No static dot-path can reach the chosen
    element, and the sandbox behind data.transform has no comprehensions, so
    without this the value is unreachable by any generic node.
    """
    mcq = {
        "question": "Where does photosynthesis happen?",
        "choices": ["Mitochondria", "Chloroplast", "Nucleus"],
        "correct_index": 1,
    }
    assert _substitute_template("$item.choices.{correct_index}", mcq, index=0) == "Chloroplast"
    assert _substitute_template(
        {"answer": "$item.choices.{correct_index}", "q": "$item.question"}, mcq, index=0
    ) == {"answer": "Chloroplast", "q": mcq["question"]}

    # A dict keyed by an indirect segment resolves the same way.
    keyed = {"pick": "b", "values": {"a": 1, "b": 2}}
    assert _substitute_template("$item.values.{pick}", keyed, index=0) == 2

    # Missing indirection target parks, naming the segment that failed.
    with pytest.raises(ExecutionError, match="correct_index"):
        _substitute_template("$item.choices.{correct_index}", {"choices": ["a"]}, index=0)
    # Out-of-range resolved index parks too.
    with pytest.raises(ExecutionError, match=r"\$item\.choices"):
        _substitute_template(
            "$item.choices.{correct_index}", {"choices": ["a"], "correct_index": 5}, index=0
        )
    # A literal brace-free path is untouched.
    assert _substitute_template("$item.choices.0", mcq, index=0) == "Mitochondria"


def test_substitute_template_index_ref():
    """'$index' is the element's 0-based position.

    The plumbing was already there (every per-element caller passes index=,
    for error messages); until now nothing could read it.
    """
    assert _substitute_template("$index", {"a": 1}, index=0) == 0
    assert _substitute_template("$index", {"a": 1}, index=7) == 7
    assert _substitute_template({"n": "$index", "v": "$item.a"}, {"a": 1}, index=3) == {
        "n": 3,
        "v": 1,
    }
    # No position available -> raise, never invent 0. work_seed's key_template
    # shapes one item at a time and legitimately has no index.
    with pytest.raises(ExecutionError, match=r"\$index"):
        _substitute_template("$index", {"a": 1})


def test_substitute_template_cycle_ref():
    """{'$cycle': [...]} round-robins a literal pool across the fan-out.

    Written for per-item Mandate rotation: one Mandate for every render in a
    fan-out means every render bursts at the same provider (the 2026-07-24
    Together collapse). The pool lives in the template, not the data, so no
    dot-path can reach it.
    """
    pool = ["a", "b", "c"]
    got = [_substitute_template({"$cycle": pool}, None, index=i) for i in range(7)]
    assert got == ["a", "b", "c", "a", "b", "c", "a"]

    # Nested inside a larger template, beside ordinary refs.
    assert _substitute_template({"desc": "$item", "who": {"$cycle": pool}}, "prompt", index=4) == {
        "desc": "prompt",
        "who": "b",
    }

    # Pool entries are themselves substituted.
    assert _substitute_template({"$cycle": ["$item.x", "fixed"]}, {"x": 9}, index=0) == 9
    assert _substitute_template({"$cycle": ["$item.x", "fixed"]}, {"x": 9}, index=1) == "fixed"

    # A single-key '$cycle' dict is the ref; anything else is a plain dict.
    assert _substitute_template({"$cycle": pool, "other": 1}, None, index=0) == {
        "$cycle": pool,
        "other": 1,
    }

    with pytest.raises(ExecutionError, match=r"\$cycle"):
        _substitute_template({"$cycle": []}, None, index=0)
    with pytest.raises(ExecutionError, match=r"\$cycle"):
        _substitute_template({"$cycle": "nope"}, None, index=0)
    with pytest.raises(ExecutionError, match=r"\$cycle"):
        _substitute_template({"$cycle": pool}, None)
