"""Workflow graph analysis — public API.

    Source -> [builder] -> list[TreeNode] -> [flattener] -> flat dicts -> [emitter] -> AtlasWireFormat

See _graph_builder, _graph_flattener, _graph_emitter for internals.
"""

from __future__ import annotations

from mistralai.workflows.core._graph_builder import (
    _activity_connectors_from_ast,
    _collect_connector_bindings,
    _connector_call_names,
    _depends_import_names,
)
from mistralai.workflows.core._graph_emitter import (
    build_graph_dynamically,
    build_graph_statically,
)
from mistralai.workflows.core._graph_flattener import GraphValidationError
from mistralai.workflows.core._graph_types import _CONNECTORS_META_KEY, _MISTRALAI_PLUGIN_KEY

__all__ = [
    "GraphValidationError",
    "_CONNECTORS_META_KEY",
    "_MISTRALAI_PLUGIN_KEY",
    "_activity_connectors_from_ast",
    "_collect_connector_bindings",
    "_connector_call_names",
    "_depends_import_names",
    "build_graph_dynamically",
    "build_graph_statically",
]
