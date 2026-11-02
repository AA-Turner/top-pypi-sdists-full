"""Extraction planner — a run of steps becomes its own Workflow, losslessly.

The promises under test are the ones a user can SEE break: the child runs the
same steps in the same order, the parent still delivers the same fields to
whatever came after, and anything that cannot be reproduced faithfully is
refused by name instead of quietly approximated.
"""

from __future__ import annotations

import pytest

from matrx_graph.extract import (
    SUBGRAPH_CALL_SPEC_TYPE,
    ExtractionRejected,
    plan_extraction,
)
from matrx_graph.patch import apply_patch
from matrx_graph.types.definition import Definition


def _node(nid: str, spec: str = "data.transform", x: float = 0.0, **data):
    return {
        "id": nid,
        "type": "data",
        "position": {"x": x, "y": 0.0},
        "data": {"spec_type": spec, **data},
    }


def _edge(src: str, tgt: str, mappings=None, **data):
    edge = {"id": f"e_{src}__{tgt}", "source": src, "target": tgt, "data": {"kind": "data", **data}}
    if mappings is not None:
        edge["data"]["mappings"] = mappings
    return edge


def _linear_parent() -> Definition:
    """ask → shape → [store_prompt → store → store_parse] → report

    Modeled on the real pending assist (acceptance-dry_run_zero_side_effects):
    the run's last step fans out to two downstream consumers.
    """
    return Definition.model_validate(
        {
            "nodes": [
                _node("ask", x=0),
                _node("shape", x=100),
                _node("store_prompt", "text.custom_extract", x=200),
                _node("store", "ai.chat.manual", x=300),
                _node("store_parse", "text.custom_extract", x=400),
                _node("report", x=500),
                _node("describe", x=600),
            ],
            "edges": [
                _edge("ask", "shape", {"topic": "topic"}),
                _edge("shape", "store_prompt", {"row": "result.row"}),
                _edge("store_prompt", "store", {"user_input": "result.user_input"}),
                _edge("store", "store_parse", {"final_text": "final_text"}),
                _edge("store_parse", "report", {"row_id": "result.row_id"}),
                _edge("store_parse", "describe", {"row": "$FULL_PAYLOAD"}),
            ],
            "variables": [
                {"name": "table_name", "default": "cities"},
                {"name": "unused_elsewhere", "default": 1},
            ],
        }
    )


RUN = ["store_prompt", "store", "store_parse"]


def test_child_holds_the_run_in_order_with_only_its_internal_connections():
    parent = _linear_parent()
    plan = plan_extraction(parent, node_ids=RUN)

    assert plan.node_ids == RUN
    assert plan.entry_node_id == "store_prompt"
    assert plan.terminal_node_id == "store_parse"
    assert [n.id for n in plan.child.nodes] == RUN
    assert sorted(e.id for e in plan.child.edges) == [
        "e_store__store_parse",
        "e_store_prompt__store",
    ]
    # The child starts where the run started — explicitly, not by inference.
    assert plan.child.entry_nodes == ["store_prompt"]
    # Positions are translated to the origin so the new workflow opens framed.
    assert min(n.position.x for n in plan.child.nodes) == 0.0


def test_selection_order_does_not_matter():
    parent = _linear_parent()
    plan = plan_extraction(parent, node_ids=["store_parse", "store_prompt", "store"])
    assert plan.node_ids == RUN


def test_only_the_variables_the_run_actually_references_are_copied():
    parent = _linear_parent()
    parent.nodes[3].data["config"] = {"table": {"$var": "table_name"}}
    plan = plan_extraction(parent, node_ids=RUN)
    assert plan.variables_copied == ["table_name"]


def test_parent_keeps_its_shape_and_every_field_link_still_resolves():
    parent = _linear_parent()
    plan = plan_extraction(parent, node_ids=RUN)
    patched = apply_patch(parent, plan.parent_patch("child-def-id", label="Update Database"))

    ids = [n.id for n in patched.nodes]
    assert "store" not in ids and plan.call_node_id in ids
    call = next(n for n in patched.nodes if n.id == plan.call_node_id)
    assert call.spec_type == SUBGRAPH_CALL_SPEC_TYPE
    assert call.config == {"definition_id": "child-def-id"}

    by_id = {e.id: e for e in patched.edges}
    # Inbound: reattached untouched — the links already name the first step's
    # own input args, which is exactly what subgraph.call seeds the child with.
    inbound = by_id["e_shape__store_prompt"]
    assert inbound.target == plan.call_node_id
    assert inbound.mappings == {"row": "result.row"}
    # Outbound: re-addressed at the child run's output for the last step.
    assert by_id["e_store_parse__report"].source == plan.call_node_id
    assert by_id["e_store_parse__report"].mappings == {
        "row_id": "last_outputs.store_parse.result.row_id"
    }
    # $FULL_PAYLOAD means "that step's whole result", which is the bare prefix.
    assert by_id["e_store_parse__describe"].mappings == {"row": "last_outputs.store_parse"}
    # No handle survives: subgraph.call emits on none, and a handle it never
    # emits on would prune the edge and silently kill everything downstream.
    assert by_id["e_store_parse__report"].sourceHandle is None


def test_a_reattached_edge_keeps_its_own_id():
    parent = _linear_parent()
    plan = plan_extraction(parent, node_ids=RUN)
    patched = apply_patch(parent, plan.parent_patch("child", label="X"))
    assert {"e_shape__store_prompt", "e_store_parse__report"} <= {e.id for e in patched.edges}


def test_error_edges_are_left_alone():
    parent = _linear_parent()
    parent.edges.append(
        Definition.model_validate(
            {
                "nodes": [],
                "edges": [_edge("store_parse", "report", {"why": "message"}, kind="error")],
            }
        )
        .edges[0]
        .model_copy(update={"id": "e_err"})
    )
    plan = plan_extraction(parent, node_ids=RUN)
    patched = apply_patch(parent, plan.parent_patch("child", label="X"))
    err = next(e for e in patched.edges if e.id == "e_err")
    # code/message/details address the FAILURE dump, which subgraph.call raises
    # in its own right when the child run dies — no re-addressing to do.
    assert err.mappings == {"why": "message"}


def test_call_node_id_does_not_collide():
    parent = _linear_parent()
    parent.nodes.append(
        Definition.model_validate({"nodes": [_node("sub_workflow", x=999)], "edges": []}).nodes[0]
    )
    plan = plan_extraction(parent, node_ids=RUN)
    assert plan.call_node_id == "sub_workflow_2"


# ── refusals: every one names the thing the user has to change ─────────────


def _issues(parent: Definition, node_ids: list[str]) -> list[str]:
    with pytest.raises(ExtractionRejected) as exc:
        plan_extraction(parent, node_ids=node_ids)
    return exc.value.issues


def test_refuses_a_selection_that_is_not_one_connected_run():
    parent = _linear_parent()
    issues = _issues(parent, ["store_prompt", "report"])
    assert any("not one connected run" in i for i in issues)


def test_refuses_when_something_feeds_the_middle_of_the_run():
    parent = _linear_parent()
    parent.edges.append(
        Definition.model_validate(
            {"nodes": [], "edges": [_edge("ask", "store", {"a": "b"})]}
        ).edges[0]
    )
    issues = _issues(parent, RUN)
    assert any("MIDDLE" in i and "e_ask__store" in i for i in issues)


def test_refuses_when_the_middle_of_the_run_sends_output_away():
    parent = _linear_parent()
    parent.edges.append(
        Definition.model_validate(
            {"nodes": [], "edges": [_edge("store", "report", {"a": "b"})]}
        ).edges[0]
    )
    issues = _issues(parent, RUN)
    assert any("MIDDLE" in i and "e_store__report" in i for i in issues)


def test_refuses_an_outbound_connection_with_no_field_links():
    parent = _linear_parent()
    parent.edges = [e for e in parent.edges if e.id != "e_store_parse__report"]
    parent.edges.append(
        Definition.model_validate({"nodes": [], "edges": [_edge("store_parse", "report")]}).edges[0]
    )
    issues = _issues(parent, RUN)
    assert any("field links" in i for i in issues)


def test_refuses_a_branch_output_it_cannot_reproduce():
    parent = _linear_parent()
    edge = next(e for e in parent.edges if e.id == "e_store_parse__report")
    edge.sourceHandle = "yes"
    issues = _issues(parent, RUN)
    assert any("branch" in i for i in issues)


def test_refuses_a_conditional_that_reads_the_last_steps_own_result():
    parent = _linear_parent()
    edge = next(e for e in parent.edges if e.id == "e_store_parse__report")
    edge.data["kind"] = "conditional"
    edge.data["condition"] = "result.row_id"
    issues = _issues(parent, RUN)
    assert any("condition" in i for i in issues)


def test_refuses_a_run_of_one_step():
    assert any("at least 2" in i for i in _issues(_linear_parent(), ["store"]))


def test_refuses_steps_that_are_no_longer_there():
    issues = _issues(_linear_parent(), ["store_prompt", "ghost_step"])
    assert any("ghost_step" in i and "changed since" in i for i in issues)


def test_refuses_when_the_workflow_pins_a_start_inside_the_run():
    parent = _linear_parent()
    parent.entry_nodes = ["store_prompt"]
    assert any("pinned start" in i for i in _issues(parent, RUN))


def test_refuses_a_terminal_step_whose_id_cannot_be_addressed():
    parent = Definition.model_validate(
        {
            "nodes": [_node("a"), _node("b.c"), _node("z")],
            "edges": [_edge("a", "b.c", {"x": "x"}), _edge("b.c", "z", {"y": "y"})],
        }
    )
    assert any("contains a dot" in i for i in _issues(parent, ["a", "b.c"]))


def test_a_second_workflow_rewired_onto_a_SHARED_child_addresses_the_childs_steps():
    """The bug this pins: when two workflows point at ONE sub-workflow, only
    the first one's plan built it. The second must address the CHILD's step
    ids — its own are not in there, and a field link naming them would compile
    fine and then never resolve at run time."""
    parent = Definition.model_validate(
        {
            "nodes": [_node("a"), _node("b"), _node("c"), _node("z")],
            "edges": [
                _edge("a", "b", {"x": "x"}),
                _edge("b", "c", {"y": "y"}),
                _edge("c", "z", {"out": "result.value"}),
            ],
        }
    )
    plan = plan_extraction(parent, node_ids=["b", "c"])
    patch = plan.parent_patch("shared-child", label="Shared", child_terminal_node_id="store_parse")
    patched = apply_patch(parent, patch)
    edge = next(e for e in patched.edges if e.id == "e_c__z")
    assert edge.mappings == {"out": "last_outputs.store_parse.result.value"}
