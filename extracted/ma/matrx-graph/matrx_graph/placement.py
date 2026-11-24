"""Step placement on the canvas — never on top of another step.

The server twin of the Studio's ``lib/node-placement.ts`` (same card size,
same square-spiral search): a step a patch ADDS is placed at the nearest spot
where its card overlaps no other step. A position that already overlaps
nothing is the author's and is kept exactly.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

NODE_WIDTH = 240.0
NODE_HEIGHT = 92.0
_STEP = round((NODE_WIDTH + 24) / 3)
_RINGS = 60


def _rect(node: dict[str, Any]) -> tuple[float, float, float, float]:
    pos = node.get("position") or {}
    width = node.get("width") or (node.get("measured") or {}).get("width") or NODE_WIDTH
    height = node.get("height") or (node.get("measured") or {}).get("height") or NODE_HEIGHT
    return float(pos.get("x", 0)), float(pos.get("y", 0)), float(width), float(height)


def _collide(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and a[1] < b[1] + b[3] and a[1] + a[3] > b[1]


def overlapping_pairs(nodes: list[dict[str, Any]]) -> list[tuple[str, str]]:
    """Every pair of steps whose cards overlap (the Studio's ``hasStackedNodes``)."""
    rects = [(str(n.get("id")), _rect(n)) for n in nodes]
    return [
        (a_id, b_id)
        for i, (a_id, a) in enumerate(rects)
        for b_id, b in rects[i + 1 :]
        if _collide(a, b)
    ]


def free_position(node: dict[str, Any], others: list[dict[str, Any]]) -> dict[str, float]:
    """The node's own position when it overlaps nothing, else the nearest free spot."""
    x, y, w, h = _rect(node)
    taken = [_rect(o) for o in others]

    def free(px: float, py: float) -> bool:
        return not any(_collide((px, py, w, h), t) for t in taken)

    if free(x, y):
        return {"x": x, "y": y}
    for ring in range(1, _RINGS + 1):
        for dx in range(-ring, ring + 1):
            for dy in range(-ring, ring + 1):
                if max(abs(dx), abs(dy)) != ring:
                    continue
                px, py = x + dx * _STEP, y + dy * _STEP
                if free(px, py):
                    return {"x": px, "y": py}
    right = max((t[0] + t[2] for t in taken), default=x)
    return {"x": right + 24, "y": y}


def place_added_node(node: dict[str, Any], others: list[dict[str, Any]]) -> dict[str, Any]:
    """Return ``node`` placed where it overlaps no other step — said out loud when moved."""
    placed = free_position(node, others)
    pos = node.get("position") or {}
    if placed["x"] != float(pos.get("x", 0)) or placed["y"] != float(pos.get("y", 0)):
        logger.warning(
            "add_node %r: position (%s, %s) overlaps another step — placed at (%s, %s)",
            node.get("id"), pos.get("x"), pos.get("y"), placed["x"], placed["y"],
        )
        node = {**node, "position": {**pos, **placed}}
    return node


# ── The tool seam: steps, frames and notes an agent adds (STUDIO-SERVER-3, 2026-11-17) ──────────────
#
# ``settle_added_nodes`` is the one rule the Conductor's write door applies to everything an agent
# ADDS, steps, frames and notes alike: a node with no deliberate position, or one that lands on another
# node's room, moves to the nearest free slot (flow direction first); a new frame is sized to its
# members plus padding and never overlaps a sibling frame or a note; a node that was already stored
# (the person's, or an earlier turn's) is never moved. The sizes below are the TS package's
# (``@ai-matrx/graph-canvas`` footprint.ts, groups.ts, node-placement.ts, info-faces); a parity test
# reads those sources and fails when they drift.

#: footprint.ts MAP_LABEL / DEFAULT_CARD / DEFAULT_SHAPE
MAP_LABEL_WIDTH = 220.0
MAP_LABEL_GAP = 10.0
MAP_LABEL_HEIGHT = 64.0
DEFAULT_CARD = (180.0, 92.0)
DEFAULT_SHAPE = (112.0, 112.0)
#: groups.ts
GROUP_PADDING = 28.0
GROUP_HEADER_HEIGHT = 36.0
MIN_GROUP_WIDTH = 220.0
MIN_GROUP_HEIGHT = 140.0
#: node-placement.ts PLACEMENT_GAP
PLACEMENT_GAP = 24.0
#: the size the server gives a note (patch.py NOTE_MIN_*), never under graph-canvas info-faces.tsx's note floor; the card family's (min 200, max 320)
NOTE_MIN = (180.0, 100.0)
CARD_MIN = (200.0, 120.0)

_FRAME_SPEC = "info.frame"
_NOTE_SPEC = "info.note"
_GRID = 40.0
_REACH = 50
_BACKWARD_PENALTY = 3.0

Rect = tuple[float, float, float, float]


def _spec_of(node: dict[str, Any]) -> str:
    data = node.get("data") if isinstance(node.get("data"), dict) else {}
    spec = data.get("spec_type")
    if isinstance(spec, str) and spec:
        return spec
    t = node.get("type")
    return t if isinstance(t, str) else ""


def _is_info(node: dict[str, Any]) -> bool:
    return node.get("type") == "info" or _spec_of(node).startswith("info.")


def _size_of(node: dict[str, Any]) -> tuple[float | None, float | None]:
    data = node.get("data") if isinstance(node.get("data"), dict) else {}
    measured = node.get("measured") if isinstance(node.get("measured"), dict) else {}
    w = node.get("width") or measured.get("width") or data.get("width")
    h = node.get("height") or measured.get("height") or data.get("height")
    return (float(w) if w else None, float(h) if h else None)


def step_footprint(node: dict[str, Any]) -> tuple[float, float, float]:
    """(width, height, offset_x): the room a step needs, its name under it included
    (``stepFootprint`` in footprint.ts, not Map-only). The node's own left edge sits ``offset_x`` in."""
    cw, ch = _size_of(node)
    card_w, card_h = cw or DEFAULT_CARD[0], ch or DEFAULT_CARD[1]
    shape_w, shape_h = DEFAULT_SHAPE
    left = min(0.0, (shape_w - MAP_LABEL_WIDTH) / 2)
    right = max(shape_w, (shape_w + MAP_LABEL_WIDTH) / 2, card_w)
    bottom = max(shape_h + MAP_LABEL_GAP + MAP_LABEL_HEIGHT, card_h)
    return right - left, bottom, -left


def _pos(node: dict[str, Any]) -> tuple[float, float]:
    p = node.get("position")
    if isinstance(p, dict) and isinstance(p.get("x"), (int, float)) and isinstance(p.get("y"), (int, float)):
        return float(p["x"]), float(p["y"])
    return 0.0, 0.0


def room_of(node: dict[str, Any]) -> Rect:
    """The room a node takes, in its own coordinate space (canvas for a top-level node, the frame's
    for a member)."""
    x, y = _pos(node)
    spec = _spec_of(node)
    if spec == _FRAME_SPEC:
        w, h = _size_of(node)
        return x, y, w or MIN_GROUP_WIDTH, h or MIN_GROUP_HEIGHT
    if spec == _NOTE_SPEC:
        w, h = _size_of(node)
        return x, y, w or NOTE_MIN[0], h or NOTE_MIN[1]
    if _is_info(node):
        w, h = _size_of(node)
        return x, y, w or CARD_MIN[0], h or CARD_MIN[1]
    w, h, off = step_footprint(node)
    return x - off, y, w, h


def _inflate(r: Rect, gap: float) -> Rect:
    return r[0] - gap, r[1] - gap, r[2] + 2 * gap, r[3] + 2 * gap


def flow_direction(nodes: list[dict[str, Any]], edges: list[dict[str, Any]] | None) -> str:
    """``"right"`` (the default arrangement) or ``"down"``, read off how the existing connections run."""
    at = {str(n.get("id")): _pos(n) for n in nodes if not _is_info(n) and not n.get("parentId")}
    dx = dy = 0.0
    for e in edges or []:
        a, b = at.get(str(e.get("source"))), at.get(str(e.get("target")))
        if a and b:
            dx += abs(b[0] - a[0])
            dy += abs(b[1] - a[1])
    return "down" if dy > dx else "right"


_OFFSETS: dict[str, list[tuple[float, float]]] = {}


def _offsets(direction: str) -> list[tuple[float, float]]:
    cached = _OFFSETS.get(direction)
    if cached is not None:
        return cached
    out: list[tuple[float, float, float]] = []
    for i in range(-_REACH, _REACH + 1):
        for j in range(-_REACH, _REACH + 1):
            dx, dy = i * _GRID, j * _GRID
            fwd, side = (dx, dy) if direction == "right" else (dy, dx)
            cost = (fwd * fwd * (_BACKWARD_PENALTY if fwd < 0 else 1.0) + side * side) ** 0.5
            out.append((cost, dx, dy))
    out.sort()
    _OFFSETS[direction] = [(dx, dy) for _, dx, dy in out]
    return _OFFSETS[direction]


def _collides(r: Rect, taken: list[Rect]) -> bool:
    return any(_collide(r, t) for t in taken)


def nearest_free_slot(room: Rect, taken: list[Rect], direction: str = "right") -> tuple[float, float]:
    """The shift (dx, dy) that takes ``room`` to the nearest spot clear of every ``taken`` room
    (kept ``PLACEMENT_GAP`` apart), searching forward along the flow before backward. (0, 0) when it
    is already clear."""
    x, y, w, h = room
    padded = [_inflate(t, PLACEMENT_GAP) for t in taken]
    for dx, dy in _offsets(direction):
        if not _collides((x + dx, y + dy, w, h), padded):
            return dx, dy
    if direction == "right":
        return max((t[0] + t[2] for t in taken), default=x) + PLACEMENT_GAP - x, 0.0
    return 0.0, max((t[1] + t[3] for t in taken), default=y) + PLACEMENT_GAP - y


def _shift(node: dict[str, Any], dx: float, dy: float) -> None:
    x, y = _pos(node)
    node["position"] = {**(node.get("position") or {}), "x": x + dx, "y": y + dy}


def _fit_frame(frame: dict[str, Any], members: list[dict[str, Any]]) -> None:
    """Size ``frame`` to its members' rooms plus padding. Members keep their canvas place: the frame's
    origin moves and the members' frame-local positions compensate."""
    rooms = [room_of(m) for m in members]
    min_x = min(r[0] for r in rooms)
    min_y = min(r[1] for r in rooms)
    max_x = max(r[0] + r[2] for r in rooms)
    max_y = max(r[1] + r[3] for r in rooms)
    ox = min_x - GROUP_PADDING
    oy = min_y - GROUP_PADDING - GROUP_HEADER_HEIGHT
    _shift(frame, ox, oy)
    for m in members:
        _shift(m, -ox, -oy)
    width = max(MIN_GROUP_WIDTH, float(int(max_x - min_x + GROUP_PADDING * 2 + 0.999)))
    height = max(MIN_GROUP_HEIGHT, float(int(max_y - min_y + GROUP_PADDING * 2 + GROUP_HEADER_HEIGHT + 0.999)))
    frame["width"], frame["height"] = width, height


def _unplaced(node: dict[str, Any]) -> bool:
    p = node.get("position")
    return not isinstance(p, dict) or p.get("x") is None or p.get("y") is None


def settle_added_nodes(
    nodes: list[dict[str, Any]],
    movable: set[str],
    edges: list[dict[str, Any]] | None = None,
) -> list[str]:
    """Settle every node in ``movable`` (the ids this write adds); never touch another node.
    Mutates ``nodes``; returns one sentence per node moved or frame sized."""
    notes: list[str] = []
    direction = flow_direction(nodes, edges)
    frames = [n for n in nodes if isinstance(n, dict) and _spec_of(n) == _FRAME_SPEC]
    sized: set[str] = set()

    def place(node: dict[str, Any], taken: list[Rect]) -> bool:
        if _unplaced(node):
            node["position"] = {"x": 0.0, "y": 0.0}
        dx, dy = nearest_free_slot(room_of(node), taken, direction)
        if dx or dy:
            _shift(node, dx, dy)
            return True
        return False

    # 1. inside each frame: its new members settle among its stored ones (frame-local space)
    for frame in frames:
        fid = str(frame.get("id"))
        members = [n for n in nodes if isinstance(n, dict) and n.get("parentId") == fid]
        taken = [room_of(m) for m in members if str(m.get("id")) not in movable]
        for m in members:
            mid = str(m.get("id"))
            if mid not in movable:
                continue
            if place(m, taken):
                notes.append(f"'{mid}' overlapped another item in frame '{fid}' — moved to the nearest free spot.")
            taken.append(room_of(m))
        if fid in movable and members and all(str(m.get("id")) in movable for m in members):
            _fit_frame(frame, members)
            sized.add(fid)
            notes.append(f"frame '{fid}' was sized to its members plus padding.")
        elif members and any(str(m.get("id")) in movable for m in members):
            # a stored frame that gained members grows right/down to hold them; its origin never moves
            rooms = [room_of(m) for m in members]
            w, h = _size_of(frame)
            need_w = max(r[0] + r[2] for r in rooms) + GROUP_PADDING
            need_h = max(r[1] + r[3] for r in rooms) + GROUP_PADDING
            if need_w > (w or MIN_GROUP_WIDTH) or need_h > (h or MIN_GROUP_HEIGHT):
                frame["width"] = max(need_w, w or MIN_GROUP_WIDTH)
                frame["height"] = max(need_h, h or MIN_GROUP_HEIGHT)
                notes.append(f"frame '{fid}' grew to hold the items added to it.")

    # 2. the canvas: new top-level frames first (the biggest), then notes and cards, then steps
    def top(n: dict[str, Any]) -> bool:
        return isinstance(n, dict) and not n.get("parentId")

    def rank(n: dict[str, Any]) -> int:
        spec = _spec_of(n)
        return 0 if spec == _FRAME_SPEC else (1 if _is_info(n) else 2)

    fixed = [room_of(n) for n in nodes if top(n) and str(n.get("id")) not in movable]
    for node in sorted((n for n in nodes if top(n) and str(n.get("id")) in movable), key=rank):
        nid = str(node.get("id"))
        if _spec_of(node) == _FRAME_SPEC:
            kids = [k for k in nodes if isinstance(k, dict) and k.get("parentId") == nid]
            if any(str(k.get("id")) not in movable for k in kids):
                fixed.append(room_of(node))  # holds something the person placed: stays put
                continue
        if place(node, fixed):
            notes.append(f"'{nid}' overlapped another item — moved to the nearest free spot.")
        fixed.append(room_of(node))
    return notes


def settle_removed_members(
    nodes: list[dict[str, Any]],
    stored_nodes: list[dict[str, Any]] | None,
) -> list[str]:
    """The other half of ``settle_added_nodes``: a frame that LOST members in this write (a member
    removed, or moved out of it) is re-fitted to the members it still holds plus padding, so a frame
    never keeps the empty room of a step that left. Members keep their canvas place (``_fit_frame``).
    A frame left with no members is not touched here (the empty-frame rule is the writer's).
    Mutates ``nodes``; returns one sentence per frame resized."""
    if not stored_nodes:
        return []
    before: dict[str, set[str]] = {}
    for n in stored_nodes:
        if isinstance(n, dict) and n.get("parentId"):
            before.setdefault(str(n.get("parentId")), set()).add(str(n.get("id")))
    notes: list[str] = []
    for frame in nodes:
        if not isinstance(frame, dict) or _spec_of(frame) != _FRAME_SPEC:
            continue
        fid = str(frame.get("id"))
        members = [n for n in nodes if isinstance(n, dict) and n.get("parentId") == fid]
        now = {str(m.get("id")) for m in members}
        if not (before.get(fid, set()) - now) or not members:
            continue
        _fit_frame(frame, members)
        notes.append(f"frame '{fid}' was resized to the items it still holds.")
    return notes
