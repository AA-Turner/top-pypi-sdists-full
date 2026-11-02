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
