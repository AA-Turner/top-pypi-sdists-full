"""An edge kind this engine does not know is REFUSED, never coerced into a data edge.

An older server that silently turned a newer kind (e.g. "teleport") into DATA would run it as
a data edge. Census 2026-11-02: every stored edge kind is absent/data/control/conditional/error.
"""

import pytest
from pydantic import ValidationError

from matrx_graph.types.definition import Definition, EdgeDef
from matrx_graph.types.primitives import EdgeKind


def test_unknown_edge_kind_is_refused_at_load():
    with pytest.raises(ValidationError, match="teleport"):
        EdgeDef(id="e1", source="a", target="b", data={"kind": "teleport"})


def test_unknown_edge_kind_is_refused_inside_a_definition():
    with pytest.raises(ValidationError, match="teleport"):
        Definition.model_validate(
            {
                "nodes": [],
                "edges": [{"id": "e1", "source": "a", "target": "b", "data": {"kind": "teleport"}}],
            }
        )


def test_unknown_edge_kind_set_after_load_raises_on_read():
    edge = EdgeDef(id="e1", source="a", target="b")
    edge.data["kind"] = "teleport"
    with pytest.raises(ValueError, match="teleport"):
        _ = edge.kind


@pytest.mark.parametrize("kind", [k.value for k in EdgeKind])
def test_every_known_kind_still_loads(kind):
    assert EdgeDef(id="e1", source="a", target="b", data={"kind": kind}).kind is EdgeKind(kind)


def test_absent_kind_is_still_data():
    assert EdgeDef(id="e1", source="a", target="b").kind is EdgeKind.DATA
