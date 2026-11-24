"""Live walk 2026-11-17: when the Conductor added to an existing workflow, new frames overlapped each other and the
note, and a new step landed on an existing step. One rule at the tool's write seam settles steps, frames and notes
the write ADDS; anything already stored is the person's and never moves."""

from matrx_graph import placement as P
from matrx_graph.placement import room_of, settle_added_nodes



def step(i, x, y, **extra):
    return {"id": i, "type": "workflow", "position": {"x": x, "y": y}, "data": {"spec_type": "web.search"}, **extra}


def frame(i, x, y, w=None, h=None, parent=None):
    n = {"id": i, "type": "info", "position": {"x": x, "y": y}, "data": {"spec_type": "info.frame", "title": i}}
    if w:
        n["width"], n["height"] = w, h
    return n


def note(i, x, y):
    return {"id": i, "type": "info", "position": {"x": x, "y": y}, "data": {"spec_type": "info.note", "text": "t"}}


def overlaps(a, b):
    ra, rb = room_of(a), room_of(b)
    return P._collide(ra, rb)


def test_a_step_added_on_an_occupied_spot_moves_and_the_stored_step_does_not():
    nodes = [step("old", 400, 300), step("new", 410, 310)]
    settle_added_nodes(nodes, {"new"})
    assert nodes[0]["position"] == {"x": 400, "y": 300}
    assert not overlaps(nodes[0], nodes[1])
    # the flow runs right: it moves forward, not back behind its neighbour
    assert nodes[1]["position"]["x"] > 400


def test_a_flow_down_graph_moves_the_new_step_down():
    nodes = [step("a", 0, 0), step("b", 0, 400), step("new", 5, 5)]
    edges = [{"source": "a", "target": "b"}]
    settle_added_nodes(nodes, {"new"}, edges)
    assert not overlaps(nodes[0], nodes[2])
    assert nodes[2]["position"]["y"] > 0


def test_a_step_with_a_free_deliberate_position_keeps_it():
    nodes = [step("old", 0, 0), step("new", 900, 700)]
    assert settle_added_nodes(nodes, {"new"}) == []
    assert nodes[1]["position"] == {"x": 900, "y": 700}


def test_steps_added_with_no_position_do_not_stack_on_each_other():
    nodes = [step("s1", 0, 0), step("s2", 0, 0), step("s3", 0, 0)]
    settle_added_nodes(nodes, {"s1", "s2", "s3"})
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            assert not overlaps(a, b)


def test_a_second_frame_never_overlaps_the_first_and_is_sized_to_its_members():
    nodes = [
        frame("f1", 0, 0, 400, 300),
        step("m1", 40, 70, parentId="f1"),
        frame("f2", 10, 10),
        step("m2", 20, 60, parentId="f2"),
        step("m3", 20, 400, parentId="f2"),
    ]
    settle_added_nodes(nodes, {"f2", "m2", "m3"})
    f1, f2 = nodes[0], nodes[2]
    assert f1["position"] == {"x": 0, "y": 0} and f1["width"] == 400
    assert not overlaps(f1, f2)
    members = [room_of(n) for n in nodes if n.get("parentId") == "f2"]
    assert f2["width"] >= max(r[0] + r[2] for r in members) + P.GROUP_PADDING - 1
    assert f2["height"] >= max(r[1] + r[3] for r in members) + P.GROUP_PADDING - 1
    assert min(r[0] for r in members) >= P.GROUP_PADDING - 0.01


def test_a_frame_holding_a_persons_step_stays_where_it_is():
    nodes = [step("blocker", 0, 0), frame("f", 5, 5, 300, 200), step("mine", 20, 60, parentId="f")]
    settle_added_nodes(nodes, {"f"})
    assert nodes[1]["position"] == {"x": 5, "y": 5}


def test_a_note_added_near_a_frame_moves_clear_of_it_and_a_stored_note_stays():
    nodes = [frame("f", 0, 0, 500, 400), note("kept", 100, 100), note("new", 120, 120)]
    settle_added_nodes(nodes, {"new"})
    assert nodes[2]["position"] != {"x": 120, "y": 120}
    assert not overlaps(nodes[0], nodes[2])
    assert nodes[1]["position"] == {"x": 100, "y": 100}


def test_a_new_member_of_a_stored_frame_lands_clear_of_its_siblings_and_grows_the_frame():
    nodes = [frame("f", 0, 0, 300, 250), step("a", 40, 70, parentId="f"), step("b", 45, 75, parentId="f")]
    settle_added_nodes(nodes, {"b"})
    assert nodes[0]["position"] == {"x": 0, "y": 0}
    assert not overlaps(nodes[1], nodes[2])
    assert nodes[0]["width"] >= room_of(nodes[2])[0] + room_of(nodes[2])[2]
