"""Tests for the data node pack: merge, pick, omit, filter, assert."""

from __future__ import annotations

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

from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def _run_single_node(
    node_type: str,
    inputs: dict,
    config: dict | None = None,
) -> dict:
    registry = _registry()
    data: dict = {}
    if config is not None:
        data["config"] = config
    # A single-node definition DECLARES its inputs (W68: a definition that
    # saves is a definition that can start) — the run below still delivers the
    # same values over the broadcast channel, last-writer-wins.
    data["inputs"] = inputs
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": node_type,
                    "position": {"x": 0, "y": 0},
                    "data": data,
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id=f"t-{node_type}", inputs=inputs)
    assert result.status is RunStatus.COMPLETED
    return result.last_outputs["n"]


async def test_merge_combines_with_overlay_winning():
    out = await _run_single_node(
        "data.merge",
        {"base": {"a": 1, "b": 2}, "overlay": {"b": 99, "c": 3}},
    )
    assert out["result"] == {"a": 1, "b": 99, "c": 3}


async def test_merge_empty_inputs():
    out = await _run_single_node("data.merge", {})
    assert out["result"] == {}


async def test_pick_selects_top_level_keys():
    out = await _run_single_node(
        "data.pick",
        {"record": {"a": 1, "b": 2, "c": 3}},
        {"keys": ["a", "c"]},
    )
    assert out["result"] == {"a": 1, "c": 3}


async def test_pick_nested_dotted_path():
    out = await _run_single_node(
        "data.pick",
        {"record": {"user": {"name": "Ada", "age": 30}, "keep": "yes"}},
        {"keys": ["user.name", "keep"]},
    )
    assert out["result"] == {"name": "Ada", "keep": "yes"}


async def test_pick_missing_key_is_dropped():
    out = await _run_single_node(
        "data.pick",
        {"record": {"a": 1}},
        {"keys": ["a", "missing"]},
    )
    assert out["result"] == {"a": 1}


async def test_omit_drops_top_level_keys():
    out = await _run_single_node(
        "data.omit",
        {"record": {"a": 1, "b": 2, "c": 3}},
        {"keys": ["b"]},
    )
    assert out["result"] == {"a": 1, "c": 3}


async def test_filter_keeps_matching_items_on_dicts():
    out = await _run_single_node(
        "data.filter",
        {"items": [{"n": 1}, {"n": 5}, {"n": 10}]},
        {"predicate": "inputs['n'] > 3"},
    )
    assert out["items"] == [{"n": 5}, {"n": 10}]
    assert out["kept"] == 2
    assert out["dropped"] == 1


async def test_filter_keeps_matching_scalars_via_value_binding():
    # Non-dict items get wrapped under inputs['value']
    out = await _run_single_node(
        "data.filter",
        {"items": [1, 2, 3, 4, 5]},
        {"predicate": "inputs['value'] > 2"},
    )
    assert out["items"] == [3, 4, 5]


async def test_filter_empty_list():
    out = await _run_single_node(
        "data.filter",
        {"items": []},
        {"predicate": "inputs['n'] > 0"},
    )
    assert out["items"] == []
    assert out["kept"] == 0
    assert out["dropped"] == 0


async def test_assert_passes_when_predicate_true():
    out = await _run_single_node(
        "data.assert",
        {"count": 5},
        {"predicate": "inputs['count'] > 0"},
    )
    assert out["passed"] is True
    assert out["inputs"] == {"count": 5}


async def test_assert_fails_when_predicate_false():
    # Phase 1 (2026-05-18): per-node failures are now recoverable. The
    # scheduler captures the failure in a NodeOutcome row, parks the run
    # at status=ERRORED with the error in result.error, and returns
    # instead of raising. Recovery happens via the /retry, /skip, and
    # /manual-result endpoints.
    registry = _registry()
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": "data.assert",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "predicate": "inputs['count'] > 0",
                            "message": "Count must be positive",
                        }
                    },
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-assert-fail", inputs={"count": 0})
    assert result.status is RunStatus.ERRORED
    assert "Count must be positive" in (result.error or "")
    # Node Result System: the failure carries a stable machine code.
    assert "assertion_failed" in (result.error or "")


async def test_parse_json_happy_path():
    # Node Result System: the scheduler unwraps Success — downstream sees the
    # bare Value archetype payload.
    out = await _run_single_node(
        "data.parse_json",
        {"text": '{"a": 1, "b": [true, null, "x"]}'},
    )
    assert out["archetype"] == "value"
    assert out["value"] == {"a": 1, "b": [True, None, "x"]}


async def test_parse_json_failure_parks_with_structured_error():
    # A parse failure is a node Failure (route with an ERROR edge or park) —
    # never an ok=false payload flowing downstream as data.
    registry = _registry()
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": "data.parse_json",
                    "position": {"x": 0, "y": 0},
                    # Declared inputs (W68) — the run below delivers the same value.
                    "data": {"inputs": {"text": "not json"}},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-parse-fail", inputs={"text": "not json"})
    assert result.status is RunStatus.ERRORED
    assert "parse_failed" in (result.error or "")


async def test_stringify_json_roundtrip():
    out = await _run_single_node(
        "data.stringify_json",
        {"value": {"a": 1, "b": 2}},
        {"sort_keys": True},
    )
    assert out["text"] == '{"a": 1, "b": 2}'


async def test_stringify_json_writes_real_unicode_unless_ascii_only():
    # 2026-10-27: escaped output ("\\u00dcber") hid É/Ü from a later casefold or search.
    out = await _run_single_node("data.stringify_json", {"value": ["Über", "École"]}, {})
    assert out["text"] == '["Über", "École"]'
    out = await _run_single_node("data.stringify_json", {"value": ["Über"]}, {"ascii_only": True})
    assert out["text"] == '["\\u00dcber"]'


async def test_stringify_json_indent_formats():
    out = await _run_single_node(
        "data.stringify_json",
        {"value": {"a": 1}},
        {"indent": 2},
    )
    assert "\n" in out["text"]
    assert "  " in out["text"]


async def test_stringify_json_non_serializable_rejected_at_model_boundary():
    # Type-contract campaign: ``value`` is ``pydantic.JsonValue``, so a
    # non-JSON python object (a set) is rejected at model construction —
    # one layer EARLIER than the executor's stringify_failed backstop
    # (which remains for anything JsonValue admits but json.dumps rejects).
    # On the real wire this can never fire: scheduler inputs are always
    # JSON (model_dump(mode="json") / checkpoint round-trips).
    import pydantic

    from matrx_graph.nodes.data.json_io import StringifyJsonInput

    with pytest.raises(pydantic.ValidationError):
        StringifyJsonInput(value={1, 2, 3})  # a set is not a JSON value
