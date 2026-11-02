"""Tests for the collection staples (dedupe/sort/limit/batch/aggregate),
the tabular parsers (parse_csv/parse_yaml), and math.evaluate."""

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

from matrx_graph.errors import CompilationError
from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def _run(node_type: str, inputs: dict, config: dict | None = None):
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
                {"id": "n", "type": node_type, "position": {"x": 0, "y": 0}, "data": data}
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    return await scheduler.run(run_id=f"t-{node_type.replace('.', '-')}", inputs=inputs)


async def _out(node_type: str, inputs: dict, config: dict | None = None) -> dict:
    result = await _run(node_type, inputs, config)
    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs["n"]


# ---------------------------------------------------------------------------
# data.dedupe
# ---------------------------------------------------------------------------


async def test_dedupe_by_key_path_keeps_first():
    items = [
        {"url": "https://a.com", "rank": 1},
        {"url": "https://b.com", "rank": 2},
        {"url": "https://a.com", "rank": 3},
    ]
    out = await _out("data.dedupe", {"items": items}, {"key": "url"})
    assert out["kept"] == 2 and out["dropped"] == 1
    assert [i["rank"] for i in out["items"]] == [1, 2]


async def test_dedupe_keep_last_wins():
    items = [{"k": "x", "v": 1}, {"k": "x", "v": 2}]
    out = await _out("data.dedupe", {"items": items}, {"key": "k", "keep": "last"})
    assert out["items"] == [{"k": "x", "v": 2}]


async def test_dedupe_whole_item_identity_and_missing_key_holes():
    out = await _out("data.dedupe", {"items": [1, 2, 1, "1"]})
    assert out["items"] == [1, 2, "1"]
    # A hole (key path absent) falls back to whole-item identity: identical
    # hole items collapse, distinct hole items both survive.
    items = [{"a": 1}, {"b": 2}, {"b": 2}, {"c": 3}]
    out = await _out("data.dedupe", {"items": items}, {"key": "a"})
    assert out["kept"] == 3 and out["dropped"] == 1


# ---------------------------------------------------------------------------
# data.sort
# ---------------------------------------------------------------------------


async def test_sort_by_key_desc_with_nested_path():
    items = [
        {"m": {"score": 0.2}, "id": "low"},
        {"m": {"score": 0.9}, "id": "high"},
        {"m": {"score": 0.5}, "id": "mid"},
    ]
    out = await _out("data.sort", {"items": items}, {"key": "m.score", "order": "desc"})
    assert [i["id"] for i in out["items"]] == ["high", "mid", "low"]
    assert out["count"] == 3


async def test_sort_missing_keys_land_where_declared():
    items = [{"s": 2}, {"other": True}, {"s": 1}]
    out = await _out("data.sort", {"items": items}, {"key": "s"})
    assert out["items"][-1] == {"other": True}
    out = await _out("data.sort", {"items": items}, {"key": "s", "missing": "first"})
    assert out["items"][0] == {"other": True}


async def test_sort_mixed_types_never_crashes():
    out = await _out("data.sort", {"items": [3, "b", 1, "a", True]})
    assert out["items"][:3] == [True, 1, 3]  # numbers (bool ranks as number)
    assert out["items"][3:] == ["a", "b"]


# ---------------------------------------------------------------------------
# data.limit
# ---------------------------------------------------------------------------


async def test_limit_head_offset_and_tail():
    items = list(range(10))
    out = await _out("data.limit", {"items": items}, {"count": 3})
    assert out["items"] == [0, 1, 2] and out["dropped"] == 7
    out = await _out("data.limit", {"items": items}, {"count": 3, "offset": 4})
    assert out["items"] == [4, 5, 6]
    out = await _out("data.limit", {"items": items}, {"count": 2, "from_end": True})
    assert out["items"] == [8, 9]
    out = await _out("data.limit", {"items": items}, {"count": 0})
    assert out["items"] == [] and out["dropped"] == 10


# ---------------------------------------------------------------------------
# data.batch
# ---------------------------------------------------------------------------


async def test_batch_chunks_in_order_with_short_tail():
    out = await _out("data.batch", {"items": [1, 2, 3, 4, 5]}, {"size": 2})
    assert out["batches"] == [[1, 2], [3, 4], [5]]
    assert out["count"] == 3 and out["total_items"] == 5 and out["size"] == 2


async def test_batch_empty_list():
    out = await _out("data.batch", {"items": []}, {"size": 10})
    assert out["batches"] == [] and out["count"] == 0


# ---------------------------------------------------------------------------
# data.aggregate
# ---------------------------------------------------------------------------


async def test_aggregate_sum_avg_min_max_over_key_path():
    items = [{"v": 2}, {"v": 4}, {"v": 6}]
    assert (await _out("data.aggregate", {"items": items}, {"operation": "sum", "value_key": "v"}))[
        "result"
    ] == 12
    assert (await _out("data.aggregate", {"items": items}, {"operation": "avg", "value_key": "v"}))[
        "result"
    ] == 4
    assert (await _out("data.aggregate", {"items": items}, {"operation": "min", "value_key": "v"}))[
        "result"
    ] == 2
    assert (await _out("data.aggregate", {"items": items}, {"operation": "max", "value_key": "v"}))[
        "result"
    ] == 6


async def test_aggregate_count_and_skipped_non_numeric():
    items = [{"v": 1}, {"v": "not a number"}, {"other": True}]
    out = await _out("data.aggregate", {"items": items}, {"operation": "count"})
    assert out["result"] == 3 and out["skipped"] == 0
    out = await _out(
        "data.aggregate", {"items": items}, {"operation": "sum", "value_key": "v"}
    )
    assert out["result"] == 1 and out["skipped"] == 2 and out["count"] == 1


async def test_aggregate_group_by():
    items = [
        {"cat": "a", "v": 1},
        {"cat": "b", "v": 10},
        {"cat": "a", "v": 3},
    ]
    out = await _out(
        "data.aggregate",
        {"items": items},
        {"operation": "sum", "value_key": "v", "group_by": "cat"},
    )
    assert out["result"] is None
    groups = {g["key"]: g for g in out["groups"]}
    assert groups["a"]["result"] == 4 and groups["a"]["count"] == 2
    assert groups["b"]["result"] == 10 and groups["b"]["count"] == 1


async def test_aggregate_bare_number_items():
    out = await _out("data.aggregate", {"items": [1, 2, 3]}, {"operation": "avg"})
    assert out["result"] == 2


# ---------------------------------------------------------------------------
# math.evaluate
# ---------------------------------------------------------------------------


async def test_math_evaluate_arithmetic_over_inputs():
    out = await _out(
        "math.evaluate",
        {"subtotal": 100, "tax_rate": 0.2},
        {"expression": "inputs['subtotal'] * (1 + inputs['tax_rate'])"},
    )
    assert out["value"] == 120.0


async def test_math_evaluate_helpers_allowed():
    out = await _out(
        "math.evaluate",
        {"score": 7, "total": 9},
        {"expression": "round(inputs['score'] / inputs['total'] * 100, 1)"},
    )
    assert out["value"] == 77.8


async def test_math_evaluate_non_numeric_result_is_failure():
    result = await _run("math.evaluate", {"a": 1}, {"expression": "'text'"})
    assert result.status is RunStatus.ERRORED


async def test_math_evaluate_rejects_disallowed_syntax():
    # 2026-09-11: the authoring validator now refuses what the runtime sandbox
    # refuses, so the illegal expression never reaches execution.
    with pytest.raises(CompilationError, match="Pow"):
        await _run("math.evaluate", {"a": 2}, {"expression": "inputs['a'] ** 10"})


# ---------------------------------------------------------------------------
# data.parse_csv / data.parse_yaml
# ---------------------------------------------------------------------------


async def test_parse_csv_with_header():
    text = "name, city\nAda, London\nAlan , Manchester\n"
    out = await _out("data.parse_csv", {"text": text})
    assert out["columns"] == ["name", "city"]
    assert out["rows"] == [
        {"name": "Ada", "city": "London"},
        {"name": "Alan", "city": "Manchester"},
    ]
    assert out["count"] == 2


async def test_parse_csv_without_header_and_ragged_rows():
    out = await _out(
        "data.parse_csv",
        {"text": "a;b;c\n1;2\n"},
        {"delimiter": ";", "has_header": False},
    )
    assert out["rows"] == [["a", "b", "c"], ["1", "2"]]
    # Ragged data row under a header pads with None.
    out = await _out("data.parse_csv", {"text": "x,y\n1\n"})
    assert out["rows"] == [{"x": "1", "y": None}]


async def test_parse_yaml_object_and_failure():
    out = await _out("data.parse_yaml", {"text": "name: Ada\ntags:\n  - a\n  - b\n"})
    assert out["value"] == {"name": "Ada", "tags": ["a", "b"]}
    result = await _run("data.parse_yaml", {"text": "a: [unclosed"})
    assert result.status is RunStatus.ERRORED
