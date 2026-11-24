"""A frame that loses members in a write shrinks to the members it still holds (one-graph, Stop/undo
data-loss lane, 2026-11-17): the room a removed step took is not left standing as an empty frame."""

from matrx_graph.placement import (
    GROUP_HEADER_HEIGHT,
    GROUP_PADDING,
    room_of,
    settle_removed_members,
)


def _frame(w: float = 900.0, h: float = 500.0) -> dict:
    return {"id": "f", "type": "info", "data": {"spec_type": "info.frame"}, "position": {"x": 0.0, "y": 0.0}, "width": w, "height": h}


def _step(nid: str, x: float, y: float) -> dict:
    return {"id": nid, "type": "action", "data": {"spec_type": "action.x"}, "parentId": "f", "position": {"x": x, "y": y}}


def test_frame_shrinks_to_remaining_member_and_keeps_its_canvas_place() -> None:
    stored = [_frame(), _step("a", 40.0, 80.0), _step("b", 600.0, 80.0)]
    frame, a = _frame(), _step("a", 40.0, 80.0)
    nodes = [frame, a]  # "b" was removed by this write
    notes = settle_removed_members(nodes, stored)
    assert notes == ["frame 'f' was resized to the items it still holds."]
    ax, ay, aw, ah = room_of(a)
    assert frame["width"] < 900.0
    # canvas place of the member is unchanged
    assert frame["position"]["x"] + a["position"]["x"] == 40.0
    assert frame["position"]["y"] + a["position"]["y"] == 80.0
    assert ax == GROUP_PADDING
    assert ay == GROUP_PADDING + GROUP_HEADER_HEIGHT


def test_untouched_frame_is_left_alone() -> None:
    stored = [_frame(), _step("a", 40.0, 80.0)]
    frame = _frame()
    nodes = [frame, _step("a", 40.0, 80.0)]
    assert settle_removed_members(nodes, stored) == []
    assert frame["width"] == 900.0 and frame["position"] == {"x": 0.0, "y": 0.0}


def test_frame_emptied_is_not_resized_here() -> None:
    stored = [_frame(), _step("a", 40.0, 80.0)]
    frame = _frame()
    assert settle_removed_members([frame], stored) == []
    assert frame["width"] == 900.0
