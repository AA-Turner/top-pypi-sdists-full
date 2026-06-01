"""
Agno integration for Aigie.

This module provides automatic tracing for Agno agents, capturing
agent invocations, tool calls, and multi-agent team orchestrations.

Usage (Auto-Instrumentation - Recommended):
    from aigie.integrations.agno import patch_agno
    patch_agno()  # Patches Agent.__init__ and Team.__init__ to auto-register handler

    from agno.agent import Agent
    agent = Agent(model=..., tools=[...])  # Automatically traced!
    result = agent.run("What is the capital of France?")

Usage (Manual Handler):
    from agno.agent import Agent
    from aigie.integrations.agno import AgnoHandler

    handler = AgnoHandler(trace_name="my-agent")
    agent = Agent(model=..., tools=[...])
    handler.register(agent)
    result = agent.run("What is the capital of France?")

Usage (Session Management):
    from aigie.integrations.agno import agno_session

    with agno_session("My Agent Session", trace_id="custom-id") as session:
        agent.run("First question")
        agent.run("Follow-up")  # Shares same session context
        print(f"Total tokens: {session.total_tokens}")

Usage (Error Detection):
    from aigie.integrations.agno import get_error_detector

    detector = get_error_detector()
    # Errors are automatically tracked
    print(detector.get_stats())

Usage (Drift Detection):
    from aigie.integrations.agno import get_drift_detector

    detector = get_drift_detector()
    detector.capture_system_prompt("You are a helpful assistant...")
    print(detector.get_drift_report())
"""

from typing import TYPE_CHECKING, Any

__all__ = [
    # Handler
    "AgnoHandler",
    # Configuration
    "AgnoConfig",
    # Auto-instrumentation
    "patch_agno",
    "unpatch_agno",
    "is_agno_patched",
    # Cost tracking
    "calculate_agno_cost",
    "get_model_pricing",
    "AGNO_MODEL_PRICING",
    # Session management
    "AgnoSessionContext",
    "agno_session",
    "get_session_context",
    "set_session_context",
    "reset_session_context",
    "get_or_create_session_context",
    "clear_session_context",
    # Retry utilities
    "RetryContext",
    "RetryExhaustedError",
    "TimeoutExceededError",
    "AgnoExecutionError",
    "retry_decorator",
    "with_timeout",
    "with_retry",
    # Error detection
    "ErrorDetector",
    "ErrorType",
    "ErrorSeverity",
    "DetectedError",
    "ErrorStats",
    "get_error_detector",
    "reset_error_detector",
    # Drift detection
    "DriftDetector",
    "DriftType",
    "DriftSeverity",
    "DetectedDrift",
    "AgentPlan",
    "ExecutionTrace",
    "get_drift_detector",
    "reset_drift_detector",
    # Utilities
    "is_agno_available",
    "get_agno_version",
    "safe_str",
    "truncate_text",
    "mask_sensitive_content",
    "mask_sensitive_data",
    "mask_dict_keys",
    "extract_tool_name",
    "extract_tool_description",
    "extract_agent_info",
    "extract_response_tokens",
    "extract_model_from_response",
    "format_duration_ms",
    "normalize_model_name",
    "get_provider_from_model",
    "parse_tool_result",
    "is_streaming_response",
    "SENSITIVE_PATTERNS",
]


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Handler
    if name == "AgnoHandler":
        from .handler import AgnoHandler

        return AgnoHandler

    # Configuration
    if name == "AgnoConfig":
        from .config import AgnoConfig

        return AgnoConfig

    # Auto-instrumentation
    if name == "patch_agno":
        from .auto_instrument import patch_agno

        return patch_agno

    if name == "unpatch_agno":
        from .auto_instrument import unpatch_agno

        return unpatch_agno

    if name == "is_agno_patched":
        from .auto_instrument import is_agno_patched

        return is_agno_patched

    # Cost tracking
    if name == "calculate_agno_cost":
        from .cost_tracking import calculate_agno_cost

        return calculate_agno_cost

    if name == "get_model_pricing":
        from .cost_tracking import get_model_pricing

        return get_model_pricing

    if name == "AGNO_MODEL_PRICING":
        from .cost_tracking import AGNO_MODEL_PRICING

        return AGNO_MODEL_PRICING

    # Session management
    if name == "AgnoSessionContext":
        from .session_context import AgnoSessionContext

        return AgnoSessionContext

    if name == "agno_session":
        from .session_context import agno_session

        return agno_session

    if name == "get_session_context":
        from .session_context import get_session_context

        return get_session_context

    if name == "set_session_context":
        from .session_context import set_session_context

        return set_session_context

    if name == "reset_session_context":
        from .session_context import reset_session_context

        return reset_session_context

    if name == "get_or_create_session_context":
        from .session_context import get_or_create_session_context

        return get_or_create_session_context

    if name == "clear_session_context":
        from .session_context import clear_session_context

        return clear_session_context

    # Retry utilities
    if name == "RetryContext":
        from ..._legacy_stubs import RetryContext

        return RetryContext

    if name == "RetryExhaustedError":
        from ..._legacy_stubs import RetryExhaustedError

        return RetryExhaustedError

    if name == "TimeoutExceededError":
        from ..._legacy_stubs import TimeoutExceededError

        return TimeoutExceededError

    if name == "AgnoExecutionError":
        from ..._legacy_stubs import AgnoExecutionError

        return AgnoExecutionError

    if name == "retry_decorator":
        from ..._legacy_stubs import retry_decorator

        return retry_decorator

    if name == "with_timeout":
        from ..._legacy_stubs import with_timeout

        return with_timeout

    if name == "with_retry":
        from ..._legacy_stubs import with_retry

        return with_retry

    # Error detection
    if name == "ErrorDetector":
        from .error_detection import ErrorDetector

        return ErrorDetector

    if name == "ErrorType":
        from .error_detection import ErrorType

        return ErrorType

    if name == "ErrorSeverity":
        from .error_detection import ErrorSeverity

        return ErrorSeverity

    if name == "DetectedError":
        from .error_detection import DetectedError

        return DetectedError

    if name == "ErrorStats":
        from .error_detection import ErrorStats

        return ErrorStats

    if name == "get_error_detector":
        from .error_detection import get_error_detector

        return get_error_detector

    if name == "reset_error_detector":
        from .error_detection import reset_error_detector

        return reset_error_detector

    # Drift detection
    if name == "DriftDetector":
        from .drift_detection import DriftDetector

        return DriftDetector

    if name == "DriftType":
        from .drift_detection import DriftType

        return DriftType

    if name == "DriftSeverity":
        from .drift_detection import DriftSeverity

        return DriftSeverity

    if name == "DetectedDrift":
        from .drift_detection import DetectedDrift

        return DetectedDrift

    if name == "AgentPlan":
        from .drift_detection import AgentPlan

        return AgentPlan

    if name == "ExecutionTrace":
        from .drift_detection import ExecutionTrace

        return ExecutionTrace

    if name == "get_drift_detector":
        from .drift_detection import get_drift_detector

        return get_drift_detector

    if name == "reset_drift_detector":
        from .drift_detection import reset_drift_detector

        return reset_drift_detector

    # Utilities
    if name == "is_agno_available":
        from .utils import is_agno_available

        return is_agno_available

    if name == "get_agno_version":
        from .utils import get_agno_version

        return get_agno_version

    if name == "safe_str":
        from .utils import safe_str

        return safe_str

    if name == "truncate_text":
        from .utils import truncate_text

        return truncate_text

    if name == "mask_sensitive_content":
        from .utils import mask_sensitive_content

        return mask_sensitive_content

    if name == "mask_sensitive_data":
        from .utils import mask_sensitive_data

        return mask_sensitive_data

    if name == "mask_dict_keys":
        from .utils import mask_dict_keys

        return mask_dict_keys

    if name == "extract_tool_name":
        from .utils import extract_tool_name

        return extract_tool_name

    if name == "extract_tool_description":
        from .utils import extract_tool_description

        return extract_tool_description

    if name == "extract_agent_info":
        from .utils import extract_agent_info

        return extract_agent_info

    if name == "extract_response_tokens":
        from .utils import extract_response_tokens

        return extract_response_tokens

    if name == "extract_model_from_response":
        from .utils import extract_model_from_response

        return extract_model_from_response

    if name == "format_duration_ms":
        from .utils import format_duration_ms

        return format_duration_ms

    if name == "normalize_model_name":
        from .utils import normalize_model_name

        return normalize_model_name

    if name == "get_provider_from_model":
        from .utils import get_provider_from_model

        return get_provider_from_model

    if name == "parse_tool_result":
        from .utils import parse_tool_result

        return parse_tool_result

    if name == "is_streaming_response":
        from .utils import is_streaming_response

        return is_streaming_response

    if name == "SENSITIVE_PATTERNS":
        from .utils import SENSITIVE_PATTERNS

        return SENSITIVE_PATTERNS

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .auto_instrument import (
        is_agno_patched,
        patch_agno,
        unpatch_agno,
    )
    from .config import AgnoConfig
    from .cost_tracking import (
        AGNO_MODEL_PRICING,
        calculate_agno_cost,
        get_model_pricing,
    )
    from .drift_detection import (
        AgentPlan,
        DetectedDrift,
        DriftDetector,
        DriftSeverity,
        DriftType,
        ExecutionTrace,
        get_drift_detector,
        reset_drift_detector,
    )
    from .error_detection import (
        DetectedError,
        ErrorDetector,
        ErrorSeverity,
        ErrorStats,
        ErrorType,
        get_error_detector,
        reset_error_detector,
    )
    from .handler import AgnoHandler
    from ..._legacy_stubs import (
        AgnoExecutionError,
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        retry_decorator,
        with_retry,
        with_timeout,
    )
    from .session_context import (
        AgnoSessionContext,
        agno_session,
        clear_session_context,
        get_or_create_session_context,
        get_session_context,
        reset_session_context,
        set_session_context,
    )
    from .utils import (
        SENSITIVE_PATTERNS,
        extract_agent_info,
        extract_model_from_response,
        extract_response_tokens,
        extract_tool_description,
        extract_tool_name,
        format_duration_ms,
        get_agno_version,
        get_provider_from_model,
        is_agno_available,
        is_streaming_response,
        mask_dict_keys,
        mask_sensitive_content,
        mask_sensitive_data,
        normalize_model_name,
        parse_tool_result,
        safe_str,
        truncate_text,
    )
