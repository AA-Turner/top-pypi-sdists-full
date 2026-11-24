"""The graph-operation vocabulary as seen from the workflow engine.

ONE vocabulary: the wire models (``GraphOp``, ``GraphOpEvent`` and the generic
ops over the shared node/edge shape) are defined once, in
``matrx_connect.context.graph_ops`` (this package depends on matrx-connect, so
the event payload cannot live here). The workflow ops' APPLY semantics are the
``matrx_graph.patch`` classes. This module re-exports the vocabulary and names
the one relationship between the two halves so a test can hold it:

* every ``DefinitionPatch`` op is in the ``GraphOp`` union, EXCEPT the retiring
  annotation/group ops (``PATCH_OPS_RETIRING_WITH_THE_MIGRATION``), which the
  one-graph migration deletes (notes and frames become ``info.*`` nodes).
"""

from __future__ import annotations

from typing import Annotated, Union, get_args, get_origin
import types

from matrx_connect.context.graph_ops import (
    GraphEdge,
    GraphNode,
    GraphOp,
    GraphOpActor,
    GraphOpEvent,
    GraphRef,
)
from pydantic import BaseModel

__all__ = [
    "GraphEdge",
    "GraphNode",
    "GraphOp",
    "GraphOpActor",
    "GraphOpEvent",
    "GraphRef",
    "PATCH_OPS_RETIRING_WITH_THE_MIGRATION",
    "graph_op_models",
    "graph_op_names",
    "patch_op_models",
    "patch_op_names",
]

PATCH_OPS_RETIRING_WITH_THE_MIGRATION: frozenset[str] = frozenset(
    {"add_annotation", "update_annotation", "remove_annotation", "group_nodes", "ungroup"}
)


def _members(tp: object) -> list[type[BaseModel]]:
    """Flatten an Annotated/Union type into its model classes, whatever the wrapping."""
    origin = get_origin(tp)
    if origin is Annotated:
        return _members(get_args(tp)[0])
    if origin is Union or origin is types.UnionType:
        return [m for arg in get_args(tp) for m in _members(arg)]
    return [tp]  # type: ignore[list-item]


def _op_name(model: type[BaseModel]) -> str:
    return get_args(model.model_fields["op"].annotation)[0]


def graph_op_models() -> dict[str, type[BaseModel]]:
    """Every wire op class, by ``op`` name."""
    return {_op_name(m): m for m in _members(GraphOp)}


def patch_op_models() -> dict[str, type[BaseModel]]:
    """Every ``DefinitionPatch`` op class, by ``op`` name."""
    from matrx_graph.patch import PatchOp

    return {_op_name(m): m for m in _members(PatchOp)}


def graph_op_names() -> frozenset[str]:
    """Every ``op`` name the wire vocabulary carries."""
    return frozenset(graph_op_models())


def patch_op_names() -> frozenset[str]:
    """Every ``op`` name ``DefinitionPatch`` accepts."""
    return frozenset(patch_op_models())
