"""
Google ADK integration for Aigie.

This module provides automatic tracing for Google ADK (Agent Development Kit),
capturing agent invocations, tool calls, LLM calls, and events.

Usage (Auto-Instrumentation - Recommended):
    from aigie.integrations.google_adk import patch_google_adk
    patch_google_adk()  # Patches Runner to auto-inject AigiePlugin

    from google.adk import Runner, LlmAgent
    runner = Runner(agent=agent, session_service=...)  # Automatically traced!

Usage (Plugin-based - Manual):
    from google.adk import Runner, LlmAgent
    from aigie.integrations.google_adk import AigiePlugin

    plugin = AigiePlugin(trace_name="my-agent")
    runner = Runner(agent=agent, session_service=..., plugins=[plugin])

Usage (Handler - Low-level):
    from aigie.integrations.google_adk import GoogleADKHandler

    handler = GoogleADKHandler(trace_name="my-agent")
    # Use handler methods in custom callbacks

Usage (Session Management):
    from aigie.integrations.google_adk import google_adk_session

    with google_adk_session("My Agent", user_id="user-123") as session:
        result = await runner.run_async(user_id=..., session_id=...)
        print(f"Total tokens: {session.total_tokens}")

Usage (Error Detection):
    from aigie.integrations.google_adk import get_error_detector

    detector = get_error_detector()
    print(detector.get_stats())

Usage (Drift Detection):
    from aigie.integrations.google_adk import get_drift_detector

    detector = get_drift_detector()
    print(detector.get_drift_report())
"""

from typing import TYPE_CHECKING, Any

__all__ = [
    # Handler
    "GoogleADKHandler",
    # Plugin
    "AigiePlugin",
    # Configuration
    "GoogleADKConfig",
    # Auto-instrumentation
    "patch_google_adk",
    "unpatch_google_adk",
    "is_google_adk_patched",
    # Cost tracking
    "calculate_google_adk_cost",
    "get_model_pricing",
    "GEMINI_MODEL_PRICING",
    # Session management
    "GoogleADKSessionContext",
    "google_adk_session",
    "get_session_context",
    "set_session_context",
    "get_or_create_session_context",
    "clear_session_context",
    # Retry utilities
    "RetryContext",
    "RetryExhaustedError",
    "TimeoutExceededError",
    "GoogleADKExecutionError",
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
    "is_google_adk_available",
    "get_google_adk_version",
    "safe_str",
    "truncate_text",
    "mask_sensitive_content",
    "mask_sensitive_data",
    "mask_dict_keys",
    "extract_tool_name",
    "extract_agent_info",
    "extract_response_tokens",
    "format_duration_ms",
    "normalize_model_name",
    "is_gemini_model",
    "get_gemini_model_tier",
    "extract_event_type",
    "parse_function_call",
    "is_streaming_response",
    "SENSITIVE_PATTERNS",
]


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Handler
    if name == "GoogleADKHandler":
        from .handler import GoogleADKHandler

        return GoogleADKHandler

    # Plugin
    if name == "AigiePlugin":
        from .plugin import AigiePlugin

        return AigiePlugin

    # Configuration
    if name == "GoogleADKConfig":
        from .config import GoogleADKConfig

        return GoogleADKConfig

    # Auto-instrumentation
    if name == "patch_google_adk":
        from .auto_instrument import patch_google_adk

        return patch_google_adk

    if name == "unpatch_google_adk":
        from .auto_instrument import unpatch_google_adk

        return unpatch_google_adk

    if name == "is_google_adk_patched":
        from .auto_instrument import is_google_adk_patched

        return is_google_adk_patched

    # Cost tracking
    if name == "calculate_google_adk_cost":
        from .cost_tracking import calculate_google_adk_cost

        return calculate_google_adk_cost

    if name == "get_model_pricing":
        from .cost_tracking import get_model_pricing

        return get_model_pricing

    if name == "GEMINI_MODEL_PRICING":
        from .cost_tracking import GEMINI_MODEL_PRICING

        return GEMINI_MODEL_PRICING

    # Session management
    if name == "GoogleADKSessionContext":
        from .session import GoogleADKSessionContext

        return GoogleADKSessionContext

    if name == "google_adk_session":
        from .session import google_adk_session

        return google_adk_session

    if name == "get_session_context":
        from .session import get_session_context

        return get_session_context

    if name == "set_session_context":
        from .session import set_session_context

        return set_session_context

    if name == "get_or_create_session_context":
        from .session import get_or_create_session_context

        return get_or_create_session_context

    if name == "clear_session_context":
        from .session import clear_session_context

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

    if name == "GoogleADKExecutionError":
        from ..._legacy_stubs import GoogleADKExecutionError

        return GoogleADKExecutionError

    if name == "retry_decorator":
        from ..._legacy_stubs import retry_decorator

        return retry_decorator

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
    if name == "is_google_adk_available":
        from .utils import is_google_adk_available

        return is_google_adk_available

    if name == "get_google_adk_version":
        from .utils import get_google_adk_version

        return get_google_adk_version

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

    if name == "extract_agent_info":
        from .utils import extract_agent_info

        return extract_agent_info

    if name == "extract_response_tokens":
        from .utils import extract_response_tokens

        return extract_response_tokens

    if name == "format_duration_ms":
        from .utils import format_duration_ms

        return format_duration_ms

    if name == "normalize_model_name":
        from .utils import normalize_model_name

        return normalize_model_name

    if name == "is_gemini_model":
        from .utils import is_gemini_model

        return is_gemini_model

    if name == "get_gemini_model_tier":
        from .utils import get_gemini_model_tier

        return get_gemini_model_tier

    if name == "extract_event_type":
        from .utils import extract_event_type

        return extract_event_type

    if name == "parse_function_call":
        from .utils import parse_function_call

        return parse_function_call

    if name == "is_streaming_response":
        from .utils import is_streaming_response

        return is_streaming_response

    if name == "SENSITIVE_PATTERNS":
        from .utils import SENSITIVE_PATTERNS

        return SENSITIVE_PATTERNS

    if name == "with_timeout":
        from ..._legacy_stubs import with_timeout

        return with_timeout

    if name == "with_retry":
        from ..._legacy_stubs import with_retry

        return with_retry

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .auto_instrument import (
        is_google_adk_patched,
        patch_google_adk,
        unpatch_google_adk,
    )
    from .config import GoogleADKConfig
    from .cost_tracking import (
        GEMINI_MODEL_PRICING,
        calculate_google_adk_cost,
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
    from .handler import GoogleADKHandler
    from .plugin import AigiePlugin
    from ..._legacy_stubs import (
        GoogleADKExecutionError,
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        retry_decorator,
        with_retry,
        with_timeout,
    )
    from .session import (
        GoogleADKSessionContext,
        clear_session_context,
        get_or_create_session_context,
        get_session_context,
        google_adk_session,
        set_session_context,
    )
    from .utils import (
        SENSITIVE_PATTERNS,
        extract_agent_info,
        extract_event_type,
        extract_response_tokens,
        extract_tool_name,
        format_duration_ms,
        get_gemini_model_tier,
        get_google_adk_version,
        is_gemini_model,
        is_google_adk_available,
        is_streaming_response,
        mask_dict_keys,
        mask_sensitive_content,
        mask_sensitive_data,
        normalize_model_name,
        parse_function_call,
        safe_str,
        truncate_text,
    )
