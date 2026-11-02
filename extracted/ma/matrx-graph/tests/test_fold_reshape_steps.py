"""Reshape-only steps fold into their connections, and the receiving step gets the same thing.

Every case runs the definition before and after the fold on the real Scheduler and compares what
the receiving step answered; the kept cases name why the step stayed.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.fold import fold_reshape_steps

from tests._fixtures import FakeEmitter, make_app_context

PAGES = {"pages": [{"url": "a", "title": "A", "x": 1}, {"url": "b", "x": 2}, {"url": "c", "title": "C"}]}


def _node(nid: str, typ: str, config: dict[str, Any], **data: Any) -> dict[str, Any]:
    return {"id": nid, "type": typ, "position": {"x": 0, "y": 0}, "data": {"config": config, **data}}


def _edge(eid: str, s: str, t: str, mappings: dict[str, str] | None, kind: str = "data") -> dict[str, Any]:
    data: dict[str, Any] = {"kind": kind}
    if mappings is not None:
        data["mappings"] = mappings
    return {"id": eid, "source": s, "target": t, "data": data}


def _chain(*middle: dict[str, Any], out_map: dict[str, str]) -> dict[str, Any]:
    ids = ["src", *[m["id"] for m in middle], "use"]
    edges = [_edge("e0", "src", ids[1], {"items": "pages"})]
    for i in range(1, len(ids) - 2):
        edges.append(_edge(f"e{i}", ids[i], ids[i + 1], {"items": "values" if middle[i - 1]["type"] == "data.map_template" else "items"}))
    edges.append(_edge("e_last", ids[-2], "use", out_map))
    return {
        "nodes": [_node("src", "data.transform", {"expression": repr(PAGES)}), *middle,
                  _node("use", "data.transform", {"expression": "inputs"})],
        "edges": edges,
    }


async def _use(defn: dict[str, Any]) -> Any:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(defn), registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry).run(run_id="f")
    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs["use"]


async def test_a_pick_template_and_a_fixed_limit_fold_and_the_receiver_gets_the_same() -> None:
    template = {"link": "$item.url", "title": {"$optional": "$item.title", "default": ""}, "n": "$index", "kind": "page"}
    defn = _chain(
        _node("shape", "data.map_template", {"template": template}),
        _node("top", "data.limit", {"count": 2, "offset": 1}),
        out_map={"rows": "items", "first": "items[0].link"},
    )
    folded, folds, kept = fold_reshape_steps(defn)
    assert [f.step_id for f in folds] == ["shape", "top"], kept
    assert [n["id"] for n in folded["nodes"]] == ["src", "use"]
    assert folded["edges"][-1]["data"]["mappings"]["rows"] == 'pages.{link: url, title: title ?? "", n: #, kind: "page"}[1:3]'
    assert await _use(folded) == await _use(defn)


async def test_a_step_that_is_more_than_a_reshape_stays_and_says_why() -> None:
    defn = _chain(
        _node("shape", "data.map_template", {"template": {"u": "$item.url", "t": "$in.topic"}}),
        out_map={"rows": "values"},
    )
    folded, folds, kept = fold_reshape_steps(defn)
    assert folds == []
    assert kept[0].step_id == "shape" and "$in" in kept[0].reason
    assert folded == defn


async def test_a_step_read_for_its_count_stays() -> None:
    defn = _chain(_node("top", "data.limit", {"count": 2}), out_map={"n": "kept"})
    _, folds, kept = fold_reshape_steps(defn)
    assert folds == [] and "kept" in kept[0].reason


async def test_a_step_with_its_own_review_mark_stays() -> None:
    defn = _chain(_node("top", "data.limit", {"count": 2}, review={"label": "cut"}), out_map={"rows": "items"})
    _, folds, kept = fold_reshape_steps(defn)
    assert folds == [] and "review" in kept[0].reason


async def test_a_for_each_around_real_work_becomes_run_once_per_item_and_the_receiver_gets_the_same() -> None:
    """For each -> step -> Gather is one card with data.for_each; the engine writes the trio back out."""
    defn = {
        "nodes": [
            _node("src", "data.transform", {"expression": "{'pages': [{'u': 'a'}, {'u': 'b'}], 'topic': 'bread'}"}),
            _node("each", "control.map", {"target_node_id": "work",
                                          "payload_template": {"page": "$item", "topic": "$in.topic"}}),
            # a non-formula step (a text template): real work for the purpose of the fold
            _node("work", "data.transform", {"expression": "{'got': inputs['page']['u'] + ':' + inputs['topic']}"},
                  review={"label": "keep-as-step"}),
            _node("all", "control.gather", {}),
            _node("use", "data.transform", {"expression": "inputs"}),
        ],
        "edges": [
            _edge("e1", "src", "each", {"items": "pages", "topic": "topic"}),
            _edge("e2", "work", "all", None),
            _edge("e3", "all", "use", {"v": "values", "n": "count"}),
        ],
    }
    folded, folds, kept = fold_reshape_steps(defn)
    assert [f.step_id for f in folds] == ["each"], kept
    assert [n["id"] for n in folded["nodes"]] == ["src", "work", "use"]
    work = next(n for n in folded["nodes"] if n["id"] == "work")
    assert work["data"]["for_each"] == {"payload_template": {"page": "$item", "topic": "$in.topic"}}
    assert await _use(folded) == await _use(defn) == {"v": [{"got": "a:bread"}, {"got": "b:bread"}], "n": 2}


async def test_a_formula_read_only_by_another_formula_is_written_into_it() -> None:
    defn = {
        "nodes": [
            _node("src", "data.transform", {"expression": "{'pages': [1, 2, 3], 'n': 2}"}),
            _node("pick", "data.transform", {"expression": "{'top': inputs['pages'][:inputs['n']], 'unused': 1 / 1}"}),
            _node("say", "data.transform", {"expression": "{'count': len(inputs['top']), 'n': inputs['n'] * 10, 'has': 'top' in inputs}"}),
        ],
        "edges": [
            _edge("e1", "src", "pick", {"pages": "pages", "n": "n"}),
            _edge("e2", "pick", "say", {"top": "top"}),
            _edge("e3", "src", "say", {"n": "n"}),
        ],
    }
    folded, folds, kept = fold_reshape_steps(defn)
    assert [f.step_id for f in folds] == ["pick"], kept
    assert [n["id"] for n in folded["nodes"]] == ["src", "say"]
    assert await _use_named(folded, "say") == await _use_named(defn, "say") == {"count": 2, "n": 20, "has": True}


async def _use_named(defn: dict[str, Any], node: str) -> Any:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(defn), registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry).run(run_id="m")
    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs[node]


# --- Independent review 2026-10-28: each case where a fold would change what a step receives stays put.

def _template_chain(template: dict[str, Any], incoming: str = "pages", **edge_extra: Any) -> dict[str, Any]:
    defn = _chain(_node("shape", "data.map_template", {"template": template}), out_map={"rows": "values"})
    defn["edges"][0]["data"]["mappings"] = {"items": incoming}
    defn["edges"][0]["data"].update(edge_extra)
    return defn


def test_a_path_that_reads_like_a_fixed_value_is_not_folded() -> None:
    for template in ({"first": "$item.0"}, {"t": "$item.true"}, {"n": "$item.null"}):
        _, folds, kept = fold_reshape_steps(_template_chain(template))
        assert folds == [] and kept[0].step_id == "shape", template


def test_a_name_or_path_with_other_characters_is_not_folded() -> None:
    for template in ({"café": "$item.url"}, {"u": "$item.café"}, {'a"b': "$item.url"}, {"u": "$item.a,b"}):
        _, folds, _ = fold_reshape_steps(_template_chain(template))
        assert folds == [], template


def test_a_step_fed_by_an_either_or_is_not_folded() -> None:
    _, folds, _ = fold_reshape_steps(_template_chain({"u": "$item.url"}, incoming="pages ?? alt"))
    assert folds == []
    _, folds, _ = fold_reshape_steps(_template_chain({"u": "$item.url"}, incoming="trim(pages)"))
    assert folds == []


def test_a_connection_with_a_review_mark_keeps_its_step() -> None:
    _, folds, kept = fold_reshape_steps(_template_chain({"u": "$item.url"}, review={"label": "check"}))
    assert folds == [] and "own settings" in kept[0].reason


def test_a_failure_connection_out_of_the_gather_keeps_the_for_each() -> None:
    defn = {
        "nodes": [
            _node("src", "data.transform", {"expression": "{'pages': [1, 2]}"}),
            _node("each", "control.map", {"target_node_id": "work", "payload_template": {"p": "$item"}}),
            _node("work", "data.transform", {"expression": "{'got': inputs['p']}"}, review={"label": "x"}),
            _node("all", "control.gather", {}),
            _node("handler", "data.transform", {"expression": "inputs"}),
        ],
        "edges": [_edge("e1", "src", "each", {"items": "pages"}), _edge("e2", "work", "all", None),
                  _edge("e3", "all", "handler", None, kind="error")],
    }
    _, folds, _ = fold_reshape_steps(defn)
    assert folds == []


def test_a_list_formula_fold_keeps_a_run_cap() -> None:
    defn = {
        "nodes": [
            _node("src", "data.transform", {"expression": "{'pages': [1, 2, 3]}"}),
            _node("each", "control.map", {"target_node_id": "work", "max_dispatches": 1, "payload_template": {"p": "$item"}}),
            _node("work", "data.transform", {"expression": "{'got': inputs['p']}"}),
            _node("all", "control.gather", {}),
            _node("use", "data.transform", {"expression": "inputs"}),
        ],
        "edges": [_edge("e1", "src", "each", {"items": "pages"}), _edge("e2", "work", "all", None),
                  _edge("e3", "all", "use", {"v": "values"})],
    }
    folded, folds, _ = fold_reshape_steps(defn)
    assert all(f.step_id != "each" or f.source == "data.for_each" for f in folds)
    work = next((n for n in folded["nodes"] if n["id"] == "work"), None)
    assert work is not None and (work["data"].get("for_each") or {}).get("max_dispatches", 1) == 1


async def test_a_template_and_a_filter_read_by_a_formula_are_written_into_it() -> None:
    """Multi-input chains (Vision Interview): a template with $in look-ups and a filter against another
    list, each read only by a Transform, become part of that Transform — same answer."""
    defn = {
        "nodes": [
            _node("src", "data.transform", {"expression": "{'rows': [{'id': 'a', 'n': 1}, {'id': 'b', 'n': 5}, {'id': 'c'}], "
                                                          "'names': {'a': 'Ann', 'b': 'Bo', 'c': 'Cy'}, 'seen': ['b']}"}),
            _node("shape", "data.map_template", {"template": {"id": "$item.id", "who": "$in.names.{$item.id}",
                                                              "n": {"$optional": "$item.n", "default": 0}, "at": "$index"},
                                                 "require_path": "id"}),
            _node("fresh", "data.filter", {"predicate": "inputs['id'] not in inputs['$in']['seen'] and 'n' in inputs"}),
            _node("say", "data.transform", {"expression": "{'rows': inputs['rows'], 'n': inputs['n_rows'], 'fresh': inputs['fresh'], 'left': inputs['left']}"}),
        ],
        "edges": [
            _edge("e1", "src", "shape", {"items": "rows", "names": "names"}),
            _edge("e2", "shape", "say", {"rows": "values", "n_rows": "count"}),
            _edge("e3", "src", "fresh", {"items": "rows", "seen": "seen"}),
            _edge("e4", "fresh", "say", {"fresh": "items", "left": "dropped"}),
        ],
    }
    folded, folds, kept = fold_reshape_steps(defn)
    assert sorted(f.step_id for f in folds) == ["fresh", "shape"], kept
    assert [n["id"] for n in folded["nodes"]] == ["src", "say"]
    want = {"rows": [{"id": "a", "who": "Ann", "n": 1, "at": 0}, {"id": "b", "who": "Bo", "n": 5, "at": 1},
                     {"id": "c", "who": "Cy", "n": 0, "at": 2}], "n": 3, "fresh": [{"id": "a", "n": 1}], "left": 2}
    assert await _use_named(folded, "say") == await _use_named(defn, "say") == want


async def test_a_transform_names_its_parts_and_each_reads_the_ones_before() -> None:
    defn = {
        "nodes": [
            _node("src", "data.transform", {"expression": "{'rows': [{'id': 'a', 'n': 1}, {'id': 'b', 'n': 5}]}"}),
            _node("use", "data.transform", {
                "define": {"big": "[r for r in inputs['rows'] if r['n'] > 2]", "ids": "[r['id'] for r in inputs['big']]"},
                "expression": "{'ids': inputs['ids'], 'count': len(inputs['big'])}"}),
        ],
        "edges": [_edge("e1", "src", "use", {"rows": "rows"})],
    }
    assert await _use(defn) == {"ids": ["b"], "count": 1}
    from matrx_graph.validation import validate_definition

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    defn["nodes"][1]["data"]["config"]["define"]["bad"] = "__import__('os')"
    issues = [i for i in validate_definition(defn, registry).issues if i.severity == "error"]
    assert any("Part 'bad'" in i.message for i in issues), [i.message for i in issues]


def _trio_with_items_from(gather_config: dict[str, Any], beside_map: dict[str, str] | None) -> dict[str, Any]:
    edges = [
        _edge("e1", "src", "each", {"items": "pages", "topic": "topic"}),
        _edge("e2", "work", "all", None),
        _edge("e3", "all", "use", {"pairs": "pairs", "holes": "holes", "v": "values"}),
    ]
    if beside_map is not None:
        edges.append(_edge("e4", "src", "all", beside_map))
    return {
        "nodes": [
            _node("src", "data.transform", {"expression": "{'pages': [{'u': 'a'}, {'u': 'b'}, {'u': 'c'}], 'topic': 'bread'}"}),
            _node("each", "control.map", {"target_node_id": "work",
                                          "payload_template": {"page": "$item", "topic": "$in.topic"}}),
            _node("work", "data.transform",
                  {"expression": "{'got': inputs['page']['u'] + ':' + inputs['topic'], "
                                 "'n': 1 // (0 if inputs['page']['u'] == 'b' else 1)}"},
                  review={"label": "keep-as-step"}, on_item_failure="hole"),
            _node("all", "control.gather", gather_config),
            _node("use", "data.transform", {"expression": "inputs"}),
        ],
        "edges": edges,
    }


async def test_a_gather_that_names_its_items_folds_into_run_once_per_item_with_pairs() -> None:
    """Gap 9: For each -> step -> Gather(items_from) is one card with data.for_each.pairs, and the
    receiver gets the same pairs and the same holes — each naming its item."""
    defn = _trio_with_items_from({"items_from": "sent"}, {"sent": "pages"})
    folded, folds, kept = fold_reshape_steps(defn)
    assert [f.step_id for f in folds] == ["each"], kept
    assert [n["id"] for n in folded["nodes"]] == ["src", "work", "use"]
    work = next(n for n in folded["nodes"] if n["id"] == "work")
    assert work["data"]["for_each"] == {"payload_template": {"page": "$item", "topic": "$in.topic"}, "pairs": True}
    before, after = await _use(defn), await _use(folded)
    assert after == before
    assert [(p["item"], p["value"]["got"]) for p in after["pairs"]] == [({"u": "a"}, "a:bread"), ({"u": "c"}, "c:bread")]
    assert [(h["item_index"], h["item"]) for h in after["holes"]] == [(1, {"u": "b"})]


def test_a_gather_naming_a_different_list_keeps_its_for_each() -> None:
    defn = _trio_with_items_from({"items_from": "sent"}, {"sent": "topic"})
    _, folds, kept = fold_reshape_steps(defn)
    assert folds == []
    assert any("not the one the For Each fans out" in k.reason for k in kept), kept
