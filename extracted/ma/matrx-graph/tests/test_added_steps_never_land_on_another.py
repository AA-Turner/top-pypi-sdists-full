"""An added step never lands on top of another (2026-10-26).

"Study kit — generic" was authored through ``apply-patch`` ``add_node`` ops
whose positions sat 80px apart on 92px-tall cards: the server kept every
position and the Studio found the graph stacked on every open. ``add_node``
now places the step at the nearest free spot — the server twin of the
Studio's ``findFreePosition`` — and leaves a non-overlapping position exactly
where the author put it.
"""

from __future__ import annotations

from matrx_graph import Definition, DefinitionPatch, apply_patch
from matrx_graph.placement import NODE_HEIGHT, NODE_WIDTH, overlapping_pairs


def _base() -> Definition:
    return Definition.model_validate(
        {
            "version": "1",
            "nodes": [{"id": "a", "type": "t", "position": {"x": 0, "y": 0}, "data": {}}],
            "edges": [],
        }
    )


def _add(definition: Definition, node_id: str, x: float, y: float) -> Definition:
    patch = DefinitionPatch.model_validate(
        {"ops": [{"op": "add_node", "node": {"id": node_id, "type": "t", "position": {"x": x, "y": y}, "data": {}}}]}
    )
    return apply_patch(definition, patch)


def _pos(definition: Definition, node_id: str) -> tuple[float, float]:
    node = next(n for n in definition.nodes if n.id == node_id)
    return node.position.x, node.position.y


def test_an_overlapping_add_moves_to_a_free_spot() -> None:
    out = _add(_base(), "b", 0, 80)
    assert overlapping_pairs([n.model_dump() for n in out.nodes]) == []
    assert _pos(out, "b") != (0, 80)


def test_a_free_add_keeps_the_authors_position() -> None:
    out = _add(_base(), "b", NODE_WIDTH + 20, 0)
    assert _pos(out, "b") == (NODE_WIDTH + 20, 0)
    out = _add(_base(), "c", 0, NODE_HEIGHT + 8)
    assert _pos(out, "c") == (0, NODE_HEIGHT + 8)


def test_many_adds_at_one_spot_never_stack() -> None:
    d = _base()
    for i in range(6):
        d = _add(d, f"n{i}", 0, 0)
    assert overlapping_pairs([n.model_dump() for n in d.nodes]) == []
