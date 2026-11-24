"""Guard (2026-11-10): a step handed an input name its input model refuses is found before publish.

A step whose input model forbids extra keys refuses, at run time, every name it does not declare. Research
triage 7f6f480b v11 gave its ``log.record`` step the fixed input ``category`` (a SETTING of that step, not
an input): every triage run errored there and the keyword read stopped after two pages. Nothing said so
until a paid pair was compared. ``unaccepted_input_issues`` names the step and the field for the three
places a step is handed names (fixed inputs, connection field links, a For each's per-item payload), and
aidream's publish refuses on it.

Red when the check stops seeing one of the three places, or starts refusing what a run accepts (an open
step, a name the step declares, a link the 'Only when' gate filters).
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.validation import unaccepted_input_issues


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _node(node_id: str, spec_type: str, *, config: dict | None = None, **data: object) -> dict:
    return {
        "id": node_id,
        "type": spec_type,
        "position": {"x": 0, "y": 0},
        "data": {"config": config or {}, **data},
    }


def _start() -> dict:
    return _node(
        "ask",
        "io.user_input",
        config={"fields": [{"key": "rows", "type": "text", "label": "Rows"}]},
    )


def _edge(eid: str, source: str, target: str, mappings: dict | None) -> dict:
    data: dict = {"kind": "data"}
    if mappings is not None:
        data["mappings"] = mappings
    return {"id": eid, "source": source, "target": target, "data": data}


def _issues(nodes: list[dict], edges: list[dict]) -> list[tuple[str, str | None, str]]:
    found = unaccepted_input_issues({"nodes": nodes, "edges": edges}, _registry())
    return [(i.path, i.node_id, i.message) for i in found]


def test_a_fixed_input_the_step_does_not_take_is_named():
    warn = _node(
        "warn", "log.record", inputs={"label": "x", "severity": "warning", "category": "fallback"}
    )
    found = _issues([_start(), warn], [_edge("e1", "ask", "warn", {"message": "rows"})])
    assert [(p, n) for p, n, _ in found] == [("nodes[warn].data.inputs.category", "warn")]
    assert "Step 'warn' (log.record)" in found[0][2] and "'category'" in found[0][2]


def test_a_connection_field_link_the_step_does_not_take_is_named():
    warn = _node("warn", "log.record", inputs={"label": "x"})
    found = _issues(
        [_start(), warn], [_edge("e1", "ask", "warn", {"message": "rows", "category": "rows"})]
    )
    assert [(p, n) for p, n, _ in found] == [("edges[e1].data.mappings.category", "warn")]
    assert "connection 'e1' from 'ask'" in found[0][2]


def test_a_for_each_item_name_the_step_does_not_take_is_named():
    each = _node(
        "each",
        "control.map",
        config={"target_node_id": "warn", "payload_template": {"categry": "$item"}},
    )
    warn = _node("warn", "log.record", inputs={"label": "x"})
    found = _issues([_start(), each, warn], [_edge("e1", "ask", "each", {"items": "rows"})])
    assert [(p, n) for p, n, _ in found] == [
        ("nodes[each].data.config.payload_template.categry", "warn")
    ]


def test_a_run_once_per_item_step_takes_items_and_its_item_name():
    warn = _node("warn", "log.record", inputs={"label": "x"}, for_each={"as": "message"})
    assert _issues([_start(), warn], [_edge("e1", "ask", "warn", {"items": "rows"})]) == []
    bad = _node("warn", "log.record", inputs={"label": "x"}, for_each={"as": "note"})
    found = _issues([_start(), bad], [_edge("e1", "ask", "warn", {"items": "rows"})])
    assert [n for _, n, _ in found] == ["warn"] and "'note'" in found[0][2]


def test_what_a_run_accepts_is_never_refused():
    # Declared names (fixed and linked), an open step (data.transform takes any name), a marker, and a link into
    # a step with an 'Only when' (its gate hands the step only the names it takes).
    warn = _node("warn", "log.record", inputs={"label": "x", "severity": "warning", "__kind": "k"})
    open_step = _node(
        "t", "data.transform", config={"expression": "inputs"}, inputs={"anything": 1}
    )
    gated = _node("g", "log.record", inputs={"label": "y"}, when="True")
    edges = [
        _edge("e1", "ask", "warn", {"message": "rows"}),
        _edge("e2", "ask", "t", {"whatever": "rows"}),
        _edge("e3", "ask", "g", {"message": "rows", "only_for_the_condition": "rows"}),
    ]
    assert _issues([_start(), warn, open_step, gated], edges) == []


def test_the_input_a_run_in_another_organization_setting_reads_is_accepted():
    # Knowledge buckets 6b86c945 v41: a For each hands its step each item's organization_id, which the step's
    # 'Run in another organization' setting reads and removes before the step's inputs are checked
    # (in_organization.consume_setting_input). A run accepts it; so must publish. A name the setting does
    # not read is still refused.
    each = _node(
        "each",
        "control.map",
        config={
            "target_node_id": "warn",
            "payload_template": {"message": "$item.m", "organization_id": "$item.org"},
        },
    )
    warn = _node(
        "warn", "log.record", inputs={"label": "x"}, in_organization={"input": "organization_id.id"}
    )
    edges = [_edge("e1", "ask", "each", {"items": "rows"})]
    assert _issues([_start(), each, warn], edges) == []
    bare = _node("warn", "log.record", inputs={"label": "x"})
    found = _issues([_start(), each, bare], edges)
    assert [p for p, _, _ in found] == ["nodes[each].data.config.payload_template.organization_id"]
