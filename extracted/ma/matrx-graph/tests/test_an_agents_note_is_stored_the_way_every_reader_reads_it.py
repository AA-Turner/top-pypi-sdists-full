"""The Conductor writes a note step-shaped (type "info.note", text under data.config); the canvas face,
the minimap and the engine read the stored shape (type "info", spec_type, flat fields). Live 2026-11-15:
the note drew as a blank grey rectangle because the two spellings were never reconciled."""

from matrx_graph.information import canonical_information_node, place_information_nodes

CONDUCTOR_NOTE = {
    "id": "note_overview",
    "type": "info.note",
    "position": {"x": 0, "y": -300},
    "data": {"label": "About this workflow", "config": {"text": "## Summary", "color": "yellow"}},
}


def test_the_step_shaped_note_is_stored_as_an_info_node_with_flat_fields():
    out = canonical_information_node(CONDUCTOR_NOTE)
    assert out["type"] == "info"
    assert out["data"]["spec_type"] == "info.note"
    assert out["data"]["text"] == "## Summary"
    assert out["data"]["color"] == "yellow"
    assert "config" not in out["data"]
    assert canonical_information_node(out) == out


def test_a_flat_value_wins_over_a_config_value_and_a_step_is_untouched():
    node = {"id": "n", "type": "info", "data": {"spec_type": "info.note", "text": "flat", "config": {"text": "old"}}}
    assert canonical_information_node(node)["data"]["text"] == "flat"
    step = {"id": "s", "type": "web.search", "data": {"config": {}}}
    assert canonical_information_node(step) is step


def test_a_note_far_from_the_steps_is_brought_above_them():
    nodes = [
        {"id": "a", "type": "io.user_input", "position": {"x": 400, "y": 500}, "data": {}},
        {"id": "b", "type": "ai.agent.start", "position": {"x": 900, "y": 500}, "data": {}},
        canonical_information_node({**CONDUCTOR_NOTE, "position": {"x": -3000, "y": -2000}}),
    ]
    assert place_information_nodes(nodes) == ["note_overview"]
    assert nodes[2]["position"] == {"x": 400, "y": 240}


def test_a_note_already_beside_the_steps_keeps_its_place():
    nodes = [
        {"id": "a", "type": "io.user_input", "position": {"x": 0, "y": 0}, "data": {}},
        canonical_information_node(CONDUCTOR_NOTE),
    ]
    assert place_information_nodes(nodes) == []
    assert nodes[1]["position"] == {"x": 0, "y": -300}
