"""Tests for the text.* node pack: regex extract/replace, json_path, custom_extract."""

from __future__ import annotations

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


# ---------------------------------------------------------------------------
# regex_extract
# ---------------------------------------------------------------------------


async def test_regex_extract_no_groups_returns_full_matches():
    out = await _run_single_node(
        "text.regex_extract",
        {"text": "a 1 and b 22 and c 333"},
        {"pattern": r"\d+"},
    )
    assert out["matches"] == ["1", "22", "333"]
    assert out["count"] == 3
    assert out["first"] == "1"


async def test_regex_extract_named_groups_returns_dicts():
    out = await _run_single_node(
        "text.regex_extract",
        {"text": "Ada is 36 and Linus is 54"},
        {"pattern": r"(?P<name>\w+) is (?P<age>\d+)"},
    )
    assert out["count"] == 2
    assert out["matches"][0] == {"name": "Ada", "age": "36"}
    assert out["matches"][1] == {"name": "Linus", "age": "54"}


async def test_regex_extract_positional_groups_returns_lists():
    out = await _run_single_node(
        "text.regex_extract",
        {"text": "x=1;y=2;z=3"},
        {"pattern": r"(\w+)=(\d+)"},
    )
    assert out["matches"] == [["x", "1"], ["y", "2"], ["z", "3"]]


async def test_regex_extract_first_only_short_circuits():
    out = await _run_single_node(
        "text.regex_extract",
        {"text": "aaa bbb ccc ddd"},
        {"pattern": r"\w+", "first_only": True},
    )
    assert out["matches"] == ["aaa"]
    assert out["first"] == "aaa"


async def test_regex_extract_invalid_pattern_lands_in_errored_state():
    # Phase 1 (2026-05-18): per-node failures are recoverable. An invalid
    # regex no longer terminates the run with ExecutionError — it parks
    # the run at status=ERRORED and the user can retry with a fixed
    # pattern or skip the node.
    registry = _registry()
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": "text.regex_extract",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"pattern": "[invalid"},
                        # Declared inputs (W68) — the run below delivers the same value.
                        "inputs": {"text": "hi"},
                    },
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-regex-invalid", inputs={"text": "hi"})
    assert result.status is RunStatus.ERRORED
    assert "invalid regex" in (result.error or "").lower()


# ---------------------------------------------------------------------------
# regex_replace
# ---------------------------------------------------------------------------


async def test_regex_replace_literal():
    out = await _run_single_node(
        "text.regex_replace",
        {"text": "hello world"},
        {"pattern": "world", "replacement": "graph"},
    )
    assert out["text"] == "hello graph"
    assert out["replacements"] == 1


async def test_regex_replace_with_backreference():
    out = await _run_single_node(
        "text.regex_replace",
        {"text": "John Smith"},
        {"pattern": r"(\w+) (\w+)", "replacement": r"\2 \1"},
    )
    assert out["text"] == "Smith John"
    assert out["replacements"] == 1


async def test_regex_replace_count_caps_replacements():
    out = await _run_single_node(
        "text.regex_replace",
        {"text": "aaaa"},
        {"pattern": "a", "replacement": "b", "count": 2},
    )
    assert out["text"] == "bbaa"
    assert out["replacements"] == 2


# ---------------------------------------------------------------------------
# json_path
# ---------------------------------------------------------------------------


async def test_json_path_basic_dotted():
    out = await _run_single_node(
        "text.json_path",
        {"value": {"user": {"name": "Ada", "age": 36}}},
        {"path": "user.name"},
    )
    assert out["found"] is True
    assert out["value"] == "Ada"


async def test_json_path_indexed():
    out = await _run_single_node(
        "text.json_path",
        {"value": {"items": [{"id": 1}, {"id": 2}, {"id": 3}]}},
        {"path": "items[1].id"},
    )
    assert out["value"] == 2


async def test_json_path_negative_index():
    out = await _run_single_node(
        "text.json_path",
        {"value": {"items": [10, 20, 30]}},
        {"path": "items[-1]"},
    )
    assert out["value"] == 30


async def test_json_path_miss_returns_default():
    out = await _run_single_node(
        "text.json_path",
        {"value": {"a": 1}},
        {"path": "b.c.d", "default": "fallback"},
    )
    assert out["found"] is False
    assert out["value"] == "fallback"


async def test_json_path_escaped_dot_in_key():
    out = await _run_single_node(
        "text.json_path",
        {"value": {"foo.bar": 42, "foo": {"bar": "nested"}}},
        {"path": r"foo\.bar"},
    )
    assert out["value"] == 42


# ---------------------------------------------------------------------------
# custom_extract — happy path
# ---------------------------------------------------------------------------


async def test_custom_extract_simple_loop():
    script = (
        "out = []\n"
        "for item in inputs['items']:\n"
        "    if item['score'] > 0.5:\n"
        "        out.append(item['name'])\n"
        "__result__ = out\n"
    )
    out = await _run_single_node(
        "text.custom_extract",
        {
            "items": [
                {"name": "a", "score": 0.9},
                {"name": "b", "score": 0.3},
                {"name": "c", "score": 0.7},
            ]
        },
        {"script": script},
    )
    assert out["result"] == ["a", "c"]


async def test_custom_extract_uses_safe_builtins():
    script = "__result__ = sum(inputs['nums']) + len(inputs['nums'])\n"
    out = await _run_single_node(
        "text.custom_extract",
        {"nums": [1, 2, 3, 4]},
        {"script": script},
    )
    assert out["result"] == 14


async def test_custom_extract_regex_via_re_prefix():
    script = "__result__ = re_findall(r'\\d+', inputs['text'])\n"
    out = await _run_single_node(
        "text.custom_extract",
        {"text": "x=1, y=22, z=333"},
        {"script": script},
    )
    assert out["result"] == ["1", "22", "333"]


async def test_custom_extract_json_loads_and_dumps():
    script = (
        "parsed = json_loads(inputs['raw'])\n"
        "__result__ = json_dumps({'sum': parsed['a'] + parsed['b']})\n"
    )
    out = await _run_single_node(
        "text.custom_extract",
        {"raw": '{"a": 3, "b": 4}'},
        {"script": script},
    )
    assert out["result"] == '{"sum": 7}'


# ---------------------------------------------------------------------------
# custom_extract — sandbox enforcement
# ---------------------------------------------------------------------------


# D1 (audit 2026-07-08): a genuine custom_extract failure FAILS the node — it
# does NOT complete carrying ok=false (the silent-success shape). The run parks
# ERRORED, recoverable, with the failure named. These probe the executor
# directly (the node's real failure posture) so they assert on the raised
# ExecutionError rather than a COMPLETED run's output.


async def _run_expect_error(node_type: str, inputs: dict, config: dict) -> str:
    """Run one node expecting it to FAIL; return the run's error string."""
    registry = _registry()
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": node_type,
                    "position": {"x": 0, "y": 0},
                    "data": {"config": config},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id=f"t-fail-{node_type}", inputs=inputs)
    assert result.status is not RunStatus.COMPLETED, f"expected node failure, got {result.status}"
    return result.error or ""


async def test_custom_extract_rejects_import():
    err = await _run_expect_error(
        "text.custom_extract", {}, {"script": "import os\n__result__ = 1"}
    )
    assert "Import" in err or "disallowed" in err


async def test_custom_extract_rejects_attribute_access():
    err = await _run_expect_error(
        "text.custom_extract", {}, {"script": "__result__ = (1).__class__"}
    )
    assert "Attribute" in err or "attribute" in err


async def test_custom_extract_rejects_function_def():
    err = await _run_expect_error(
        "text.custom_extract", {}, {"script": "def f():\n    pass\n__result__ = 1"}
    )
    assert err  # node failed with a message


async def test_custom_extract_rejects_missing_result():
    err = await _run_expect_error("text.custom_extract", {}, {"script": "x = 1 + 2"})
    assert "__result__" in err


async def test_custom_extract_rejects_non_json_result():
    # ``set`` results aren't JSON-serializable and should FAIL the node.
    err = await _run_expect_error("text.custom_extract", {}, {"script": "__result__ = {1, 2, 3}"})
    assert "serializable" in err


async def test_custom_extract_nameerror_fails_node():
    err = await _run_expect_error(
        "text.custom_extract", {}, {"script": "__result__ = undefined_thing"}
    )
    assert "NameError" in err


async def test_custom_extract_runtime_error_fails_node():
    # D1's canonical case: a poison step (division by zero) must FAIL the node,
    # not complete with ok=false — otherwise downstream misses result.* and the
    # run dies as a mis-attributed edge-routing error.
    err = await _run_expect_error("text.custom_extract", {}, {"script": "__result__ = 1 // 0"})
    assert "ZeroDivisionError" in err
