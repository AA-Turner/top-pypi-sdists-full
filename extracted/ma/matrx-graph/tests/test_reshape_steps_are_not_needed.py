"""The four engine capabilities that remove reshape-only steps (generic-only engine wave 2).

Each was a step a converter added only to move data around (Smart Add unit 2 had 8, unit 7 had 7):

* a connection picks a field from EACH item of a list (``values[*].url``, ``values[*].socials[*]``);
* several connections append into ONE list input (``data.arg_merge: {key: append}``);
* ``data.rules`` writes the deciding row's ``fields`` onto each item and splits the list by label;
* ``control.gather`` carries the dispatched item beside each value and hole (``items_from``).

All driven through the real Scheduler; each test fails when its capability is removed.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import Definition, MemoryCheckpointer, RunStatus, Scheduler, compile_graph
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.result import NodeResult, failure, success
from tests._fixtures import FakeEmitter
from tests.test_once_per_key import ORG_A, WF, _Cfg, _ctx, _In, _Out, _registry, _Step


def _node(node_id: str, node_type: str, *, config: dict[str, Any] | None = None,
          inputs: dict[str, Any] | None = None, **data: Any) -> dict[str, Any]:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0},
            "data": {"config": config or {}, "input": inputs or {}, **data}}


def _echo(node_id: str, **inputs: Any) -> dict[str, Any]:
    """A step that answers with exactly what it received."""
    return _node(node_id, "data.transform", config={"expression": "inputs"}, inputs=inputs)


def _edge(edge_id: str, source: str, target: str, mappings: dict[str, str] | None = None) -> dict[str, Any]:
    data: dict[str, Any] = {"kind": "data"}
    if mappings is not None:
        data["mappings"] = mappings
    return {"id": edge_id, "source": source, "target": target, "data": data}


async def _run(definition: dict[str, Any], *steps: _Step) -> dict[str, Any]:
    registry = _registry(*steps)
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), _ctx(FakeEmitter(), ORG_A),
                          registry=registry, definition_id=WF)
    result = await scheduler.run(run_id="run-1", max_steps=30)
    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs or {}


PROFILES = [
    {"handle": "a", "external_url": "https://a.example", "socials": ["x/a", "ig/a"]},
    {"handle": "b", "external_url": None, "socials": ["x/b"]},
    {"handle": "c", "socials": []},
]


async def test_a_connection_picks_a_field_from_each_item():
    out = await _run({
        "entry_nodes": ["src"],
        "nodes": [_echo("src", values=PROFILES), _echo("sink")],
        "edges": [_edge("e", "src", "sink", {"ext": "values[*].external_url",
                                             "socials": "values.*.socials[*]",
                                             "per_item": "values[*].socials"})],
    })
    sink = out["sink"]
    assert sink["ext"] == ["https://a.example"], "an item without the field (or null) is left out"
    assert sink["socials"] == ["x/a", "ig/a", "x/b"], "a second * flattens"
    assert sink["per_item"] == [["x/a", "ig/a"], ["x/b"], []]


async def test_two_connections_append_into_one_list_input():
    out = await _run({
        "entry_nodes": ["left", "right"],
        "nodes": [_echo("left", found=["a", "b"]), _echo("right", found=["c"]),
                  _node("sink", "data.transform", config={"expression": "inputs"},
                        arg_merge={"all_found": "append"})],
        "edges": [_edge("e1", "left", "sink", {"all_found": "found"}),
                  _edge("e2", "right", "sink", {"all_found": "found"})],
    })
    assert sorted(out["sink"]["all_found"]) == ["a", "b", "c"]


RULES = [
    {"when": "inputs['item']['kind'] == 'bio'", "then": {"label": "read", "fields": {"tier": "bio"}}},
    {"when": "inputs['item']['kind'] == 'social'", "then": {"label": "look", "fields": {"probability": "high"}}},
]


async def test_rules_write_the_deciding_rows_fields_onto_each_item_and_split_by_label():
    items = [{"kind": "bio", "probability": "low"}, {"kind": "social", "probability": "low"},
             {"kind": "other", "probability": "medium"}]
    out = await _run({
        "entry_nodes": ["src"],
        "nodes": [_echo("src", candidates=items),
                  _node("rules", "data.rules", config={"rules": RULES, "items_path": "candidates",
                                                       "write_fields": True, "split_by_label": True})],
        "edges": [_edge("e", "src", "rules")],
    })
    rules = out["rules"]
    assert rules["updated_items"] == [
        {"kind": "bio", "probability": "low", "tier": "bio"},
        {"kind": "social", "probability": "high"},
        {"kind": "other", "probability": "medium"},
    ], "a field no row set keeps the item's own value; an undecided item is unchanged"
    assert rules["by_label"] == {
        "read": [{"kind": "bio", "probability": "low", "tier": "bio"}],
        "look": [{"kind": "social", "probability": "high"}],
    }


class _Lookup(_Step):
    """A per-item lookup that fails the item ``"gone"`` (a hole)."""

    def __init__(self) -> None:
        super().__init__("test.lookup")

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        account = inputs.model_dump(mode="json").get("value") or {}
        if account.get("handle") == "gone":
            return failure(code="NotFound", message="no such account")
        return success(_Out(followers=len(account.get("handle", ""))))


async def test_gather_carries_each_dispatched_item_beside_its_value_and_hole():
    accounts = [{"handle": "abc"}, {"handle": "gone"}, {"handle": "de"}]
    out = await _run({
        "entry_nodes": ["src"],
        "nodes": [_echo("src", accounts=accounts),
                  _node("fan", "control.map", config={"target_node_id": "look", "payload_key": "value"}),
                  _node("look", "test.lookup", on_item_failure="hole"),
                  _node("gather", "control.gather", config={"items_from": "asked"})],
        "edges": [_edge("e_sf", "src", "fan", {"items": "accounts"}),
                  _edge("e_lg", "look", "gather"),
                  _edge("e_sg", "src", "gather", {"asked": "accounts"})],
    }, _Lookup())
    gather = out["gather"]
    assert [(p["item"]["handle"], p["value"]["followers"]) for p in gather["pairs"]] == [("abc", 3), ("de", 2)]
    assert [(h["item_index"], h["item"]) for h in gather["holes"]] == [(1, {"handle": "gone"})]


async def test_gather_with_items_from_closes_an_empty_for_each():
    out = await _run({
        "entry_nodes": ["src"],
        "nodes": [_echo("src", accounts=[]),
                  _node("fan", "control.map", config={"target_node_id": "look", "payload_key": "value"}),
                  _node("look", "test.lookup", on_item_failure="hole"),
                  _node("gather", "control.gather", config={"items_from": "asked"})],
        "edges": [_edge("e_sf", "src", "fan", {"items": "accounts"}),
                  _edge("e_lg", "look", "gather"),
                  _edge("e_sg", "src", "gather", {"asked": "accounts"})],
    }, _Lookup())
    assert out["gather"]["count"] == 0 and out["gather"]["pairs"] == [] and out["gather"]["expected"] == 0


async def test_rules_write_the_decision_itself_under_the_items_own_names():
    items = [{"key": "a", "choice": "unsure", "reason": "job said so", "probability": 0.5},
             {"key": "b", "choice": "unsure", "reason": "job said so", "probability": 0.5}]
    rules = [{"when": "inputs['item']['key'] == 'a'",
              "then": {"label": "match", "reason": "links back", "score": 0.92, "fields": {"decided_by": "rules"}}}]
    out = await _run({
        "entry_nodes": ["src"],
        "nodes": [_echo("src", items=items),
                  _node("r", "data.rules", config={
                      "rules": rules, "items_path": "items", "write_fields": True,
                      "decision_keys": {"label": "choice", "reason": "reason", "score": "probability"}})],
        "edges": [_edge("e", "src", "r")],
    })
    assert out["r"]["updated_items"] == [
        {"key": "a", "choice": "match", "reason": "links back", "probability": 0.92, "decided_by": "rules"},
        {"key": "b", "choice": "unsure", "reason": "job said so", "probability": 0.5},
    ]
