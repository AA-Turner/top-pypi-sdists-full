"""Autonomous execution model for LangGraph nodes.

Provides the foundational contracts, types, and utilities that define how
LangGraph nodes reason (via ``ReasoningProvider``), act (via ``ToolRegistry``),
and iterate on failure (via ``with_retry``).

All public symbols are re-exported here for single-import convenience::

    from agentic_devtools.orchestration.execution import (
        ExecutionContext,
        ExecutionState,
        NodeUpdateAlias,
        ReasoningProvider,
        ReasoningResponse,
        ToolRegistry,
        TraceEmitter,
        TraceEvent,
    )

This package's own modules import nothing from ``langchain``, ``openai``, or
``anthropic``.  Note that Python will still execute
``agentic_devtools.orchestration.__init__`` (which may import LangGraph) before
loading this sub-package; the isolation guarantee applies to the modules under
``execution/``, not to parent-package initialisation.
"""

from .adr_validation import validate_adr_014
from .context import ExecutionContext
from .exceptions import (
    ReasoningTimeoutError,
    RetryExhaustedError,
    ToolInvocationError,
)
from .poc_node import create_analysis_node
from .protocols import (
    ReasoningProvider,
    ToolRegistry,
    TraceEmitter,
    assert_import_isolation,
)
from .retry import RetryContext, with_retry
from .state import ExecutionState, NodeUpdateAlias
from .tracing import LoggingTraceEmitter, TraceEvent, make_trace_event, redact_sensitive_keys
from .types import JSONValue, ReasoningResponse, TokenUsage

__all__ = [
    "ExecutionContext",
    "ExecutionState",
    "JSONValue",
    "LoggingTraceEmitter",
    "NodeUpdateAlias",
    "ReasoningProvider",
    "ReasoningResponse",
    "ReasoningTimeoutError",
    "RetryContext",
    "RetryExhaustedError",
    "TokenUsage",
    "ToolInvocationError",
    "ToolRegistry",
    "TraceEmitter",
    "TraceEvent",
    "assert_import_isolation",
    "create_analysis_node",
    "make_trace_event",
    "redact_sensitive_keys",
    "validate_adr_014",
    "with_retry",
]
