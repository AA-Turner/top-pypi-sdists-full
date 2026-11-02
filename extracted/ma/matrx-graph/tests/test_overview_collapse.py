"""The plain-words overview: collapse rules + the structure hash (legible-diagrams L6a)."""

from __future__ import annotations

from matrx_graph import Definition
from matrx_graph.overview import collapse_definition, collapse_definition_detailed, definition_collapse_hash, definition_structure_hash


def _node(nid: str, spec: str, label: str | None = None, x: float = 0.0, y: float = 0.0) -> dict:
    data: dict = {"spec_type": spec}
    if label:
        data["label"] = label
    return {"id": nid, "type": spec, "position": {"x": x, "y": y}, "data": data}


def _edge(a: str, b: str, kind: str = "data") -> dict:
    return {"id": f"{a}__{b}", "source": a, "target": b, "data": {"kind": kind}}


def _fan_out() -> Definition:
    tools = [f"t{i}" for i in range(7)]
    return Definition.model_validate(
        {
            "nodes": [_node("in", "io.user_input", "Your notes"), _node("prep", "data.transform", "Prepare")]
            + [_node(t, "ai.agent.produce", f"Tool {i}") for i, t in enumerate(tools)]
            + [_node("join", "control.gather", "Join"), _node("save", "data.record.save_many", "Save it"),
               _node("fix", "ai.mandate.start", "Explain the failure")],
            "edges": [_edge("in", "prep")] + [_edge("prep", t) for t in tools] + [_edge(t, "join") for t in tools]
            + [_edge("join", "save"), _edge("t0", "fix", "error"), _edge("t1", "fix", "error")],
        }
    )


def test_parallel_siblings_fold_into_one_counted_node_keeping_real_ids() -> None:
    result = collapse_definition_detailed(_fan_out())
    folded = [n for n in result.spec["nodes"] if n["label"].startswith("7 ")]
    assert len(folded) == 1, result.spec["nodes"]
    assert sorted(result.node_map[folded[0]["id"]]) == [f"t{i}" for i in range(7)]


def test_pass_through_nodes_drop_and_neighbours_reconnect() -> None:
    result = collapse_definition_detailed(_fan_out())
    assert {"prep", "join"} <= set(result.hidden)
    labels = {n["label"] for n in result.spec["nodes"]}
    assert "Prepare" not in labels and "Join" not in labels
    ids = {n["id"] for n in result.spec["nodes"]}
    assert all(e["from"] in ids and e["to"] in ids for e in result.spec["edges"])
    assert any(e["to"] == "save" for e in result.spec["edges"])  # fold -> save survived the dropped join


def test_error_edges_fold_into_one_note_per_target_and_are_not_drawn() -> None:
    spec = collapse_definition(_fan_out())
    cards = [c for c in spec["cards"] if c["title"] == "If a step fails"]
    assert len(cards) == 1 and cards[0]["items"] == ["Handled by: Explain the failure"]
    assert "fix" not in {n["id"] for n in spec["nodes"]}  # reachable only through failure edges


def test_one_lane_per_family_and_one_lane_when_only_one_family() -> None:
    spec = collapse_definition(_fan_out())
    assert [lane["id"] for lane in spec["lanes"]] == ["inputs", "ai", "saved"]
    solo = Definition.model_validate({"nodes": [_node("a", "tool.call", "Look up")], "edges": []})
    assert len(collapse_definition(solo)["lanes"]) == 1


def test_columns_follow_depth_and_stay_inside_the_v2_ranks() -> None:
    chain = [_node(f"n{i}", "tool.call", f"Step {i}") for i in range(10)]
    defn = Definition.model_validate({"nodes": chain, "edges": [_edge(f"n{i}", f"n{i+1}") for i in range(9)]})
    spec = collapse_definition(defn)
    assert all(0 <= n["col"] <= 5 for n in spec["nodes"])
    assert len(spec["nodes"]) <= 12


def test_the_hash_ignores_positions_and_labels_but_not_structure() -> None:
    base = _fan_out()
    moved = Definition.model_validate(
        {**base.model_dump(mode="json"), "nodes": [{**n.model_dump(mode="json"), "position": {"x": 999.0, "y": -5.0}} for n in base.nodes]}
    )
    renamed = Definition.model_validate(base.model_dump(mode="json"))
    renamed.nodes[2].data["label"] = "Something else"
    assert definition_structure_hash(base) == definition_structure_hash(moved) == definition_structure_hash(renamed)

    more = base.model_dump(mode="json")
    more["edges"].append(_edge("in", "save"))
    assert definition_structure_hash(Definition.model_validate(more)) != definition_structure_hash(base)

    retyped = base.model_dump(mode="json")
    retyped["nodes"][2]["data"]["spec_type"] = "tool.call"
    assert definition_structure_hash(Definition.model_validate(retyped)) != definition_structure_hash(base)

    kind = base.model_dump(mode="json")
    kind["edges"][0]["data"]["kind"] = "control"
    assert definition_structure_hash(Definition.model_validate(kind)) != definition_structure_hash(base)


def test_collapse_hash_covers_what_the_collapse_reads_and_ignores_positions() -> None:
    base = _fan_out()
    h = definition_collapse_hash(base, title="T")

    moved = Definition.model_validate(
        {**base.model_dump(mode="json"), "nodes": [{**n.model_dump(mode="json"), "position": {"x": 7.0, "y": 9.0}} for n in base.nodes]}
    )
    assert definition_collapse_hash(moved, title="T") == h  # moving a node: no change

    renamed = Definition.model_validate(base.model_dump(mode="json"))
    renamed.nodes[2].data["label"] = "Something else"
    assert definition_collapse_hash(renamed, title="T") != h  # renaming: changes (structure hash does not)
    assert definition_structure_hash(renamed) == definition_structure_hash(base)

    assert definition_collapse_hash(base, title="Other") != h  # the title is in the picture
    solo = Definition.model_validate({"nodes": [_node("a", "tool.call", "Look up")], "edges": []})
    assert definition_collapse_hash(solo, categories={"tool.call": "llm"}) != definition_collapse_hash(solo)  # lane source
    assert definition_collapse_hash(base, title="T", categories={"ai.agent.produce": "tool"}) == h  # same lane: no change

    more = base.model_dump(mode="json")
    more["edges"].append(_edge("in", "save"))
    assert definition_collapse_hash(Definition.model_validate(more), title="T") != h

    assert collapse_definition_detailed(base, title="T").collapse_hash == h


def _long_pipeline(stages: int = 10, per_stage: int = 4) -> Definition:
    """A long build: each stage is a gate, a few tool steps and one AI step, joined in one line, with a
    final decision that loops back to the start — the shape of the 107-step agent build (2026-10-25)."""
    nodes = [_node("start", "io.user_input", "Read the request")]
    edges = []
    prev = "start"
    for s in range(stages):
        gate = f"g{s}"
        nodes.append(_node(gate, "agent.gate.check", f"Gate {s}"))
        edges.append(_edge(prev, gate))
        last = gate
        for t in range(per_stage):
            nid = f"s{s}_t{t}"
            nodes.append(_node(nid, "agent.tool.lookup", f"Look up part {s}.{t}"))
            edges.append(_edge(last, nid))
            last = nid
        ai = f"s{s}_ai"
        nodes.append(_node(ai, "ai.agent.produce", f"Write part {s}"))
        edges.append(_edge(last, ai))
        prev = ai
    nodes.append(_node("decide", "agent.proof.decide", "Decide"))
    edges += [_edge(prev, "decide"), _edge("decide", "g0")]
    return Definition.model_validate({"nodes": nodes, "edges": edges})


def test_a_long_workflow_is_told_as_named_stages_wrapped_into_rows() -> None:
    spec = collapse_definition(_long_pipeline())
    nodes = spec["nodes"]
    assert 6 < len(nodes) <= 12, [n["label"] for n in nodes]
    # Rows of at most six columns, read left to right then down.
    assert {n["lane"] for n in nodes} == {"part_1", "part_2"}
    assert all(0 <= n["col"] <= 5 for n in nodes)
    # Each stage is named by its AI step, never by its gate.
    assert not any(n["label"].lower().startswith("gate") for n in nodes)
    assert sum(n["label"].startswith("Write part") for n in nodes) >= 6
    # One chain, stage to stage, and the loop back is said once.
    assert len(spec["edges"]) == len(nodes) - 1
    assert sum(1 for n in nodes if n.get("tag") == "repeats") == 1


def test_a_short_workflow_keeps_its_steps() -> None:
    spec = collapse_definition(_long_pipeline(stages=2, per_stage=1))
    assert not any(n["lane"].startswith("part_") for n in spec["nodes"])


def test_folded_labels_never_say_steps_steps_or_a_double_ellipsis() -> None:
    nodes = [_node("in", "io.user_input", "Ask")]
    edges = []
    for i in range(14):
        nodes.append(_node(f"t{i}", "agent.tool.lookup", f"Check the instructions number {i}"))
        edges.append(_edge("in", f"t{i}"))
    spec = collapse_definition(Definition.model_validate({"nodes": nodes, "edges": edges}))
    for n in spec["nodes"]:
        assert "steps steps" not in n["label"] and "……" not in n.get("sublabel", ""), n


def test_a_very_long_chain_does_not_overflow_the_stack() -> None:
    nodes = [_node(f"n{i}", "ai.agent.produce" if i % 5 == 0 else "agent.tool.lookup", f"Step {i}") for i in range(1500)]
    edges = [_edge(f"n{i}", f"n{i + 1}") for i in range(1499)]
    spec = collapse_definition(Definition.model_validate({"nodes": nodes, "edges": edges}))
    assert 6 < len(spec["nodes"]) <= 12

