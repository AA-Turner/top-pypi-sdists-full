"""GRAPH_OP stream event: payload registry, the CONTRACTS section 3 shapes, extra fields refused."""

from __future__ import annotations

import pytest
from pydantic import TypeAdapter, ValidationError

from matrx_connect.context.events import PAYLOAD_REGISTRY, VALID_EVENT_TYPES, EventType, build_event
from matrx_connect.context.graph_ops import GraphOp, GraphOpEvent

_ACTOR = {"kind": "agent", "id": "agent-1", "label": "Builder", "conversation_id": "c-1"}
_NODE = {
    "id": "n1",
    "type": "agent",
    "position": {"x": 10, "y": 20},
    "parentId": "frame-1",
    "data": {"spec_type": "agent.run", "label": "Summarize"},
}
_EDGE = {"id": "e1", "source": "n1", "target": "n2", "data": {"kind": "relation", "relation": "reports_to"}}


def _event(**over):
    base = {
        "graph": {"kind": "workflow", "id": "wf-1"},
        "op_id": "op-1",
        "seq": 3,
        "batch_id": "b-1",
        "phase": "applied",
        "op": {"op": "add_node", "node": _NODE},
        "actor": _ACTOR,
        "label": "Add step 3 · Summarize",
        "intent_id": "intent-2",
    }
    base.update(over)
    return base


def test_registered_like_every_typed_event():
    assert EventType.GRAPH_OP.value == "graph_op"
    assert "graph_op" in VALID_EVENT_TYPES
    assert PAYLOAD_REGISTRY[EventType.GRAPH_OP] is GraphOpEvent
    event = build_event(EventType.GRAPH_OP, GraphOpEvent.model_validate(_event()))
    assert event.event == "graph_op"


@pytest.mark.parametrize(
    "op",
    [
        {"op": "add_node", "node": _NODE},
        {"op": "remove_node", "node_id": "n1"},
        {"op": "replace_node", "node": _NODE},
        {"op": "update_node_data", "node_id": "n1", "data": {"text": "hi"}},
        {"op": "update_node_type", "node_id": "n1", "type": "llm"},
        {"op": "move_node", "node_id": "n1", "position": {"x": 1, "y": 2}},
        {"op": "set_parent", "node_id": "n1", "parent_id": "frame-1"},
        {"op": "set_parent", "node_id": "n1", "parent_id": None},
        {"op": "add_edge", "edge": _EDGE},
        {"op": "remove_edge", "edge_id": "e1"},
        {"op": "replace_edge", "edge": _EDGE},
        {"op": "set_edge_kind", "edge_id": "e1", "kind": "control"},
        {"op": "set_edge_note", "edge_id": "e1", "note": "after"},
        {"op": "update_edge_data", "edge_id": "e1", "data": {"note": None}},
        {"op": "set_variable", "variable": {"name": "topic"}},
        {"op": "remove_variable", "name": "topic"},
        {"op": "set_result", "node_id": "n1"},
        {"op": "set_entry_nodes", "node_ids": ["n1"]},
    ],
)
def test_every_op_in_the_vocabulary_validates(op):
    parsed = TypeAdapter(GraphOp).validate_python(op)
    assert parsed.op == op["op"]


def test_each_phase_shape():
    GraphOpEvent.model_validate(_event(phase="proposed"))
    GraphOpEvent.model_validate(_event(phase="committed", op=None, base_version=4, version=5))
    GraphOpEvent.model_validate(_event(phase="rejected", op=None, reason="abandoned"))


@pytest.mark.parametrize("kind", ["workflow", "orchestra", "org_chart", "hr_org_chart", "records_org", "topical_map", "map", "agent_graph", "board"])
def test_every_graph_kind(kind):
    GraphOpEvent.model_validate(_event(graph={"kind": kind, "id": "g"}))


def test_unknown_fields_are_refused_everywhere():
    with pytest.raises(ValidationError):
        GraphOpEvent.model_validate(_event(surprise=1))
    with pytest.raises(ValidationError):
        GraphOpEvent.model_validate(_event(actor={**_ACTOR, "extra": 1}))
    with pytest.raises(ValidationError):
        GraphOpEvent.model_validate(_event(graph={"kind": "workflow", "id": "x", "extra": 1}))
    with pytest.raises(ValidationError):
        GraphOpEvent.model_validate(_event(op={"op": "remove_node", "node_id": "n1", "extra": 1}))


def test_bad_values_refused():
    with pytest.raises(ValidationError):
        GraphOpEvent.model_validate(_event(phase="done"))
    with pytest.raises(ValidationError):
        GraphOpEvent.model_validate(_event(op={"op": "teleport_node"}))
    with pytest.raises(ValidationError):
        GraphOpEvent.model_validate(_event(label="x" * 61))
    with pytest.raises(ValidationError):
        GraphOpEvent.model_validate(_event(graph={"kind": "spreadsheet", "id": "x"}))


@pytest.mark.asyncio
async def test_every_emitter_sends_it_and_a_rejoin_replays_it_in_order():
    import json

    from matrx_connect.emitters.console_emitter import ConsoleEmitter
    from matrx_connect.emitters.silent_emitter import SilentEmitter
    from matrx_connect.emitters.stream_emitter import StreamEmitter

    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    for seq, phase in enumerate(("proposed", "applied")):
        await emitter.send_graph_op(GraphOpEvent.model_validate(_event(seq=seq, phase=phase)))
    await emitter.send_graph_op(
        GraphOpEvent.model_validate(_event(seq=2, phase="committed", op=None, version=8))
    )
    await emitter.send_end()
    replay = [json.loads(item) async for item in emitter.generate_replay()]
    ops = [item for item in replay if (item.get("event") or item.get("e")) == "graph_op"]
    assert [o["data"]["phase"] for o in ops] == ["proposed", "applied", "committed"]
    assert ops[-1]["data"]["version"] == 8

    await ConsoleEmitter().send_graph_op(GraphOpEvent.model_validate(_event()))
    await SilentEmitter().send_graph_op(GraphOpEvent.model_validate(_event()))


def test_a_node_whose_type_is_its_spec_type_rides_the_wire_as_stored():
    """Both stored node shapes are real (matrx-graph ``NodeDef.spec_type``: ``data.spec_type`` when
    present, else ``type``). A Studio step keeps its type in ``type`` alone; the wire carries it
    unchanged and never invents a ``data.spec_type`` that would later shadow ``type``."""
    studio = {"id": "a", "type": "output.to_frontend", "position": {"x": 0, "y": 0}, "data": {"label": "Show"}}
    op = TypeAdapter(GraphOp).validate_python({"op": "add_node", "node": studio})
    assert TypeAdapter(GraphOp).dump_python(op, mode="json", exclude_none=False)["node"]["data"] == {"label": "Show"}
    with pytest.raises(ValidationError):
        TypeAdapter(GraphOp).validate_python({"op": "add_node", "node": {**studio, "data": {"spec_type": ""}}})
    with pytest.raises(ValidationError):
        TypeAdapter(GraphOp).validate_python({"op": "add_node", "node": {**studio, "type": ""}})
