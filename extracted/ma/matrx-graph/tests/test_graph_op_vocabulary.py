"""One graph-op vocabulary: the workflow patch ops and the wire ops cannot drift apart,
and ``set_parent`` applies through the one pure patch function."""

from __future__ import annotations

import pytest
from pydantic import TypeAdapter

from matrx_graph.graph_ops import (
    PATCH_OPS_RETIRING_WITH_THE_MIGRATION,
    GraphOp,
    graph_op_models,
    graph_op_names,
    patch_op_models,
    patch_op_names,
)
from matrx_graph.patch import DefinitionPatch, DefinitionPatchError, apply_patch
from matrx_graph.types.definition import Definition


def _definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {"id": "frame", "type": "info", "position": {"x": 0, "y": 0}, "data": {"spec_type": "info.frame"}},
                {"id": "a", "type": "data.merge", "position": {"x": 10, "y": 10}, "data": {}},
                {"id": "b", "type": "data.merge", "position": {"x": 300, "y": 10}, "data": {}},
            ],
            "edges": [{"id": "e1", "source": "a", "target": "b", "data": {}}],
        }
    )


def _apply(*ops: dict) -> Definition:
    return apply_patch(_definition(), DefinitionPatch.model_validate({"ops": list(ops)}))


def _parent(definition: Definition, node_id: str) -> object:
    node = next(n for n in definition.nodes if n.id == node_id)
    return node.parentId


def test_every_patch_op_is_in_the_wire_vocabulary_except_the_retiring_ones():
    missing = patch_op_names() - graph_op_names() - PATCH_OPS_RETIRING_WITH_THE_MIGRATION
    assert not missing, f"patch ops the wire vocabulary cannot carry: {sorted(missing)}"
    assert PATCH_OPS_RETIRING_WITH_THE_MIGRATION <= patch_op_names()


_NODE = {"id": "a", "type": "data.merge", "position": {"x": 1, "y": 2}, "data": {"spec_type": "data.merge"}}
_EDGE = {"id": "e1", "source": "a", "target": "b", "data": {"kind": "data"}}

# One example per non-retiring patch op. Coverage against the patch union is asserted below,
# so a new patch op without an example here fails the test.
_EXAMPLES: dict[str, dict] = {
    "add_node": {"op": "add_node", "node": _NODE},
    "replace_node": {"op": "replace_node", "node": _NODE},
    "remove_node": {"op": "remove_node", "node_id": "a"},
    "update_node_data": {"op": "update_node_data", "node_id": "a", "data": {"k": 1}},
    "update_node_type": {"op": "update_node_type", "node_id": "a", "type": "llm"},
    "move_node": {"op": "move_node", "node_id": "a", "position": {"x": 1, "y": 2}},
    "set_parent": {"op": "set_parent", "node_id": "a", "parent_id": "frame"},
    "add_edge": {"op": "add_edge", "edge": _EDGE},
    "replace_edge": {"op": "replace_edge", "edge": _EDGE},
    "remove_edge": {"op": "remove_edge", "edge_id": "e1"},
    "set_edge_kind": {"op": "set_edge_kind", "edge_id": "e1", "kind": "control"},
    "set_edge_note": {"op": "set_edge_note", "edge_id": "e1", "note": "x"},
    "update_edge_data": {"op": "update_edge_data", "edge_id": "e1", "data": {"note": "n"}},
    "set_variable": {"op": "set_variable", "variable": {"__kind": "variable_definition", "name": "topic"}},
    "remove_variable": {"op": "remove_variable", "name": "topic"},
    "set_result": {"op": "set_result", "node_id": "a", "output_kind": "text"},
    "set_entry_nodes": {"op": "set_entry_nodes", "node_ids": ["a"]},
    "set_workflow_setting": {"op": "set_workflow_setting", "key": "durability", "value": "boundaries"},
    "describe_workflow": {"op": "describe_workflow", "name": "Read the sources", "description": "Reads each source."},
}


def _twinned() -> list[str]:
    return sorted(patch_op_names() - PATCH_OPS_RETIRING_WITH_THE_MIGRATION)


def test_every_twinned_patch_op_has_an_example():
    assert sorted(_EXAMPLES) == _twinned()


@pytest.mark.parametrize("name", _twinned())
def test_twin_ops_have_the_same_fields_and_requiredness(name):
    patch_cls, wire_cls = patch_op_models()[name], graph_op_models()[name]
    patch_fields = {k: f.is_required() for k, f in patch_cls.model_fields.items() if k != "op"}
    wire_fields = {k: f.is_required() for k, f in wire_cls.model_fields.items() if k != "op"}
    assert patch_fields == wire_fields, f"{name}: patch {patch_fields} != wire {wire_fields}"


@pytest.mark.parametrize("name", _twinned())
def test_twin_ops_dump_equal_on_an_example(name):
    op = _EXAMPLES[name]
    wire = TypeAdapter(GraphOp).validate_python(op)
    patch_op = DefinitionPatch.model_validate({"ops": [op]}).ops[0]
    assert patch_op.model_dump(exclude_none=True) == wire.model_dump(exclude_none=True)


def test_set_parent_puts_a_node_in_a_frame_and_takes_it_out():
    framed = _apply({"op": "set_parent", "node_id": "a", "parent_id": "frame"})
    assert _parent(framed, "a") == "frame"
    assert _parent(framed, "b") is None
    freed = apply_patch(framed, DefinitionPatch.model_validate({"ops": [{"op": "set_parent", "node_id": "a", "parent_id": None}]}))
    assert _parent(freed, "a") is None


@pytest.mark.parametrize(
    "op",
    [
        {"op": "set_parent", "node_id": "ghost", "parent_id": "frame"},
        {"op": "set_parent", "node_id": "a", "parent_id": "ghost"},
        {"op": "set_parent", "node_id": "a", "parent_id": "a"},
    ],
)
def test_set_parent_refuses_missing_nodes_and_self_parenting(op):
    with pytest.raises(DefinitionPatchError):
        _apply(op)
