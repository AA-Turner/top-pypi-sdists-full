"""Core types for matrx-graph workflow definitions, compilation, and execution."""

from matrx_graph.types.channel import ChannelSpec, coerce_to_json
from matrx_graph.types.compiled import CompiledEdge, CompiledGraph, CompiledNode
from matrx_graph.types.context import ChannelView, NodeExecutionContext
from matrx_graph.types.definition import (
    Definition,
    EdgeDef,
    NodeDef,
    Position,
    Viewport,
)
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import (
    EmptyConfig,
    EmptyInput,
    EmptyOutput,
    NodeSpec,
)
from matrx_graph.types.primitives import (
    ActionTier,
    BackoffStrategy,
    EdgeKind,
    NodeCategory,
    Reducer,
    RetryPolicy,
    RunStatus,
)
from matrx_graph.types.canonical_payloads import (
    ARCHETYPES,
    BasePayload,
    BulkItem,
    BulkResult,
    Items,
    OperationResult,
    Page,
    Value,
)
from matrx_graph.types.result import (
    RESERVED_PAYLOAD_FIELDS,
    Failure,
    InterpretedResult,
    NodeError,
    NodeResult,
    Success,
    failure,
    interpret_node_result,
    success,
)
from matrx_graph.types.run import Run
from matrx_graph.types.input_surface import (
    declared_input,
    declared_inputs,
    input_type,
    input_multiple,
    input_picks,
    input_picks_type_into,
    input_options,
    input_option_labels,
    input_accept,
    input_choice_style,
    input_hint,
)
from matrx_graph.types.send import Send
from matrx_graph.types.usl import USLFieldHints, field_extras, model_usl_descriptor
from matrx_graph.types.value_objects import Timing
from matrx_graph.types.variables import var_ref

__all__ = [
    "ARCHETYPES",
    "ActionTier",
    "BackoffStrategy",
    "BasePayload",
    "BulkItem",
    "BulkResult",
    "ChannelSpec",
    "ChannelView",
    "CompiledEdge",
    "CompiledGraph",
    "CompiledNode",
    "Definition",
    "EdgeDef",
    "EdgeKind",
    "EmptyConfig",
    "EmptyInput",
    "EmptyOutput",
    "Failure",
    "HandleDirection",
    "HandleSpec",
    "InterpretedResult",
    "Items",
    "NodeCategory",
    "NodeDef",
    "NodeError",
    "NodeExecutionContext",
    "NodeResult",
    "NodeSpec",
    "OperationResult",
    "Page",
    "Position",
    "RESERVED_PAYLOAD_FIELDS",
    "Reducer",
    "RetryPolicy",
    "Run",
    "RunStatus",
    "Send",
    "Success",
    "Timing",
    "USLFieldHints",
    "Value",
    "declared_input",
    "declared_inputs",
    "input_type",
    "input_multiple",
    "input_picks",
    "input_picks_type_into",
    "input_options",
    "input_option_labels",
    "input_accept",
    "input_choice_style",
    "input_hint",
    "Viewport",
    "coerce_to_json",
    "failure",
    "field_extras",
    "interpret_node_result",
    "model_usl_descriptor",
    "success",
    "var_ref",
]
