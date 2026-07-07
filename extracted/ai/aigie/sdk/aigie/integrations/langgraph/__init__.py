"""Aigie LangGraph Integration.

LangGraph tracing + autonomous interventions, exposed via a single
`FrameworkAdapter` registered for `framework="langgraph"`. Auto-installed
when `aigie.init()` runs — no per-user setup required.

Usage::

    import aigie
    aigie.init(...)

    from langgraph.graph import StateGraph
    graph = StateGraph(MyState)
    # ... add nodes and edges
    app = graph.compile()
    result = await app.ainvoke({"input": "..."})  # automatically traced
"""

from typing import TYPE_CHECKING, Any

__all__ = [
    # Configuration
    "LangGraphConfig",
    # Utilities
    "is_langgraph_available",
    "get_langgraph_version",
    "safe_str",
    "extract_node_name",
    "extract_edge_name",
    "extract_graph_structure",
    "extract_state_info",
    "format_state_for_trace",
    "get_execution_path",
    "mask_sensitive_state",
    "calculate_state_diff",
    # Retry/Timeout utilities (legacy stubs)
    "RetryExhaustedError",
    "TimeoutExceededError",
    "GraphExecutionError",
    "with_timeout",
    "with_retry",
    "with_timeout_and_retry",
    "retry_decorator",
    "RetryContext",
    "GraphRetryContext",
]


def __getattr__(name: str) -> Any:  # noqa: C901, PLR0911, PLR0912
    """Lazy imports for performance."""

    if name == "LangGraphConfig":
        from aigie.integrations.langgraph.config import LangGraphConfig

        return LangGraphConfig

    # Utilities
    if name == "is_langgraph_available":
        from aigie.integrations.langgraph.utils import is_langgraph_available

        return is_langgraph_available
    if name == "get_langgraph_version":
        from aigie.integrations.langgraph.utils import get_langgraph_version

        return get_langgraph_version
    if name == "safe_str":
        from aigie.integrations.langgraph.utils import safe_str

        return safe_str
    if name == "extract_node_name":
        from aigie.integrations.langgraph.utils import extract_node_name

        return extract_node_name
    if name == "extract_edge_name":
        from aigie.integrations.langgraph.utils import extract_edge_name

        return extract_edge_name
    if name == "extract_graph_structure":
        from aigie.integrations.langgraph.utils import extract_graph_structure

        return extract_graph_structure
    if name == "extract_state_info":
        from aigie.integrations.langgraph.utils import extract_state_info

        return extract_state_info
    if name == "format_state_for_trace":
        from aigie.integrations.langgraph.utils import format_state_for_trace

        return format_state_for_trace
    if name == "get_execution_path":
        from aigie.integrations.langgraph.utils import get_execution_path

        return get_execution_path
    if name == "mask_sensitive_state":
        from aigie.integrations.langgraph.utils import mask_sensitive_state

        return mask_sensitive_state
    if name == "calculate_state_diff":
        from aigie.integrations.langgraph.utils import calculate_state_diff

        return calculate_state_diff

    # Retry/Timeout utilities (legacy stubs)
    if name == "RetryExhaustedError":
        from aigie._legacy_stubs import RetryExhaustedError

        return RetryExhaustedError
    if name == "TimeoutExceededError":
        from aigie._legacy_stubs import TimeoutExceededError

        return TimeoutExceededError
    if name == "GraphExecutionError":
        from aigie._legacy_stubs import GraphExecutionError

        return GraphExecutionError
    if name == "with_timeout":
        from aigie._legacy_stubs import with_timeout

        return with_timeout
    if name == "with_retry":
        from aigie._legacy_stubs import with_retry

        return with_retry
    if name == "with_timeout_and_retry":
        from aigie._legacy_stubs import with_timeout_and_retry

        return with_timeout_and_retry
    if name == "retry_decorator":
        from aigie._legacy_stubs import retry_decorator

        return retry_decorator
    if name == "RetryContext":
        from aigie._legacy_stubs import RetryContext

        return RetryContext
    if name == "GraphRetryContext":
        from aigie._legacy_stubs import GraphRetryContext

        return GraphRetryContext

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from aigie._legacy_stubs import (
        GraphExecutionError,
        GraphRetryContext,
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        retry_decorator,
        with_retry,
        with_timeout,
        with_timeout_and_retry,
    )
    from aigie.integrations.langgraph.config import LangGraphConfig
    from aigie.integrations.langgraph.utils import (
        calculate_state_diff,
        extract_edge_name,
        extract_graph_structure,
        extract_node_name,
        extract_state_info,
        format_state_for_trace,
        get_execution_path,
        get_langgraph_version,
        is_langgraph_available,
        mask_sensitive_state,
        safe_str,
    )


# Eager: register the LangGraph FrameworkAdapter (tracing + autonomous).
# Must happen before `aigie.init()` looks up the framework in the registry —
# this is the one import this module cannot defer.
from aigie.integrations.langgraph.adapter import LangGraphAdapter  # noqa: F401, E402
