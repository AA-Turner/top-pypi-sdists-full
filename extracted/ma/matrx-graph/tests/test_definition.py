from __future__ import annotations

import pytest
from matrx_graph import ChannelSpec, Definition, EdgeDef, EdgeKind, NodeDef, Position


def _reactflow_sample() -> dict:
    return {
        "version": "1",
        "nodes": [
            {
                "id": "a",
                "type": "control.branch",
                "position": {"x": 0, "y": 0},
                "data": {"label": "Start", "config": {"predicate": "x > 0"}},
            },
            {
                "id": "b",
                "type": "data.transform",
                "position": {"x": 200, "y": 0},
                "data": {"config": {"expression": "x * 2"}},
            },
        ],
        "edges": [
            {
                "id": "e1",
                "source": "a",
                "sourceHandle": "true",
                "target": "b",
                "type": "smoothstep",
                "data": {"kind": "conditional", "condition": "x > 0"},
            }
        ],
        "viewport": {"x": 10, "y": 20, "zoom": 1.5},
    }


def test_definition_parses_reactflow_json():
    d = Definition.model_validate(_reactflow_sample())
    assert d.version == "1"
    assert len(d.nodes) == 2
    assert d.nodes[0].config == {"predicate": "x > 0"}
    assert d.nodes[0].label == "Start"
    assert d.edges[0].kind is EdgeKind.CONDITIONAL
    assert d.edges[0].condition == "x > 0"
    assert d.viewport.zoom == 1.5


def test_definition_edge_kind_defaults_to_data():
    edge = EdgeDef(id="e1", source="a", target="b")
    assert edge.kind is EdgeKind.DATA


def test_definition_roundtrips_unknown_data_keys():
    # ReactFlow tools add fields we don't know about (e.g. 'measured', 'dragging').
    # Definition must accept and preserve them so it's lossless.
    raw = _reactflow_sample()
    raw["nodes"][0]["data"]["selected"] = True
    raw["nodes"][0]["measured"] = {"width": 150, "height": 40}
    raw["nodes"][0]["dragging"] = False
    d = Definition.model_validate(raw)
    dumped = d.model_dump(mode="json")
    assert dumped["nodes"][0]["data"]["selected"] is True
    assert dumped["nodes"][0]["measured"] == {"width": 150, "height": 40}


def test_definition_rejects_duplicate_node_ids():
    with pytest.raises(Exception):
        Definition.model_validate(
            {
                "nodes": [
                    {"id": "x", "type": "t", "position": {"x": 0, "y": 0}},
                    {"id": "x", "type": "t", "position": {"x": 1, "y": 1}},
                ],
                "edges": [],
            }
        )


def test_definition_rejects_duplicate_edge_ids():
    with pytest.raises(Exception):
        Definition.model_validate(
            {
                "nodes": [
                    {"id": "a", "type": "t", "position": {"x": 0, "y": 0}},
                    {"id": "b", "type": "t", "position": {"x": 1, "y": 1}},
                ],
                "edges": [
                    {"id": "e", "source": "a", "target": "b"},
                    {"id": "e", "source": "a", "target": "b"},
                ],
            }
        )


def test_definition_rejects_duplicate_channel_names():
    with pytest.raises(Exception):
        Definition.model_validate(
            {
                "nodes": [],
                "edges": [],
                "channels": [
                    {"name": "state"},
                    {"name": "state"},
                ],
            }
        )


def test_definition_empty_is_valid():
    d = Definition()
    assert d.nodes == []
    assert d.edges == []
    assert d.channels == []


def test_definition_with_explicit_channels():
    d = Definition(
        channels=[
            ChannelSpec(name="messages", reducer="append", default=[]),
            ChannelSpec(name="counter", reducer="sum", default=0),
        ]
    )
    assert len(d.channels) == 2
    assert d.channels[0].reducer == "append"


def test_node_def_position_required():
    with pytest.raises(Exception):
        NodeDef(id="a", type="t")  # type: ignore[call-arg]
    NodeDef(id="a", type="t", position=Position(x=0, y=0))


def test_edge_def_conditional_without_condition_has_none():
    edge = EdgeDef(
        id="e",
        source="a",
        target="b",
        data={"kind": "conditional"},
    )
    assert edge.kind is EdgeKind.CONDITIONAL
    assert edge.condition is None


# ---------------------------------------------------------------------------
# THE VERSION IS TEXT, AND "1" IS ALSO 1 (W68, 2026-09-12)
# ---------------------------------------------------------------------------
# The Emergency Conductor posted the same definition seven times with
# ``"version": 1`` (a JSON number) and got back only ``Input should be '1'``.
# It read that as a platform bug and stopped. The integer means exactly the
# same thing, so it is accepted; anything else says what the value must be.


def test_version_accepts_the_integer_one():
    assert Definition.model_validate({"version": 1}).version == "1"
    assert Definition.model_validate({"version": 1.0}).version == "1"
    assert Definition.model_validate({"version": "1"}).version == "1"
    assert Definition().version == "1"


def test_version_anything_else_says_what_it_must_be():
    for bad in (2, "2", "v1", True):
        with pytest.raises(Exception) as excinfo:
            Definition.model_validate({"version": bad})
        assert 'version must be the text "1"' in str(excinfo.value)


def test_validate_definition_accepts_the_integer_version():
    from matrx_graph.validation import validate_definition

    result = validate_definition({"version": 1, "nodes": [], "edges": []})
    assert result.valid, [i.message for i in result.issues]
