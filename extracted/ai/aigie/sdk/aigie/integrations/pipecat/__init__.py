"""
Pipecat integration for Aigie.

This module provides automatic tracing for Pipecat real-time voice and
multimodal AI pipelines, capturing conversations, turns, STT/TTS/LLM calls,
and interruptions.

Usage (Auto-Instrumentation - Recommended):
    import aigie
    from aigie.integrations.pipecat import patch_pipecat

    # Initialize Aigie
    aigie_client = aigie.Aigie()
    await aigie_client.initialize()

    # Enable auto-instrumentation
    patch_pipecat()

    # Now all pipeline tasks are automatically traced
    from pipecat.pipeline.task import PipelineTask
    task = PipelineTask(pipeline)  # Automatically traced!

Usage (Manual Observer):
    from pipecat.pipeline.task import PipelineTask
    from aigie.integrations.pipecat import AigieObserver

    observer = AigieObserver(trace_name="my-voice-app")
    task = PipelineTask(pipeline, observers=[observer])

Usage (Session Management):
    from aigie.integrations.pipecat import voice_session

    with voice_session("Customer Call", user_id="user-123") as session:
        task = PipelineTask(pipeline, observers=[observer])
        await task.run()
        print(f"Turns: {session.total_turns}")

Usage (Cost Tracking):
    from aigie.integrations.pipecat import VoiceCostTracker

    tracker = VoiceCostTracker()
    tracker.add_turn(stt_model="deepgram", llm_model="gpt-4o", ...)
    print(tracker.get_summary())

Usage (Drift Detection):
    from aigie.integrations.pipecat import VoiceDriftDetector

    detector = VoiceDriftDetector()
    detector.start_conversation()
    # ... record events ...
    print(detector.get_drift_report())

Usage (Configuration):
    from aigie.integrations.pipecat import PipecatConfig

    config = PipecatConfig(
        trace_conversations=True,
        trace_turns=True,
        capture_transcriptions=True,
        redact_pii=True,
    )
"""

from typing import TYPE_CHECKING, Any

__all__ = [
    # Handler
    "AigieObserver",
    # Configuration
    "PipecatConfig",
    # Auto-instrumentation
    "patch_pipecat",
    "unpatch_pipecat",
    "is_pipecat_patched",
    # Metrics
    "VoiceMetrics",
    "MetricsAggregator",
    # Cost tracking
    "VoiceCostTracker",
    "calculate_turn_cost",
    "calculate_stt_cost",
    "calculate_tts_cost",
    "calculate_llm_cost",
    "get_stt_pricing",
    "get_tts_pricing",
    "get_llm_pricing",
    # Session management
    "VoiceSessionContext",
    "VoiceSessionManager",
    "voice_session",
    "get_session_context",
    "set_session_context",
    "get_or_create_session_context",
    "clear_session_context",
    # Retry utilities
    "RetryContext",
    "RetryExhaustedError",
    "TimeoutExceededError",
    "PipelineExecutionError",
    "VoiceServiceError",
    "VoiceServiceRetry",
    "retry_decorator",
    "with_timeout",
    "with_retry",
    "with_timeout_and_retry",
    # Error detection
    "VoiceErrorDetector",
    "VoiceErrorType",
    "ErrorSeverity",
    "DetectedVoiceError",
    "VoiceErrorStats",
    "get_voice_error_detector",
    "reset_voice_error_detector",
    # Drift detection
    "VoiceDriftDetector",
    "VoiceDriftType",
    "DriftSeverity",
    "DetectedDrift",
    "VoicePipelineExpectations",
    "TurnExecution",
    "get_voice_drift_detector",
    "reset_voice_drift_detector",
    # Utilities
    "is_pipecat_available",
    "get_pipecat_version",
    "safe_str",
    "truncate_text",
    "mask_sensitive_transcription",
    "mask_sensitive_data",
    "mask_dict_keys",
    "extract_frame_type",
    "extract_text_from_frame",
    "extract_audio_metadata",
    "serialize_frame",
    "extract_model_from_service",
    "format_duration_ms",
    "calculate_audio_duration_ms",
    "normalize_model_name",
    "get_frame_category",
    "VOICE_SENSITIVE_PATTERNS",
]


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Handler
    if name == "AigieObserver":
        from .handler import AigieObserver

        return AigieObserver

    # Configuration
    if name == "PipecatConfig":
        from .config import PipecatConfig

        return PipecatConfig

    # Auto-instrumentation
    if name == "patch_pipecat":
        from .auto_instrument import patch_pipecat

        return patch_pipecat

    if name == "unpatch_pipecat":
        from .auto_instrument import unpatch_pipecat

        return unpatch_pipecat

    if name == "is_pipecat_patched":
        from .auto_instrument import is_pipecat_patched

        return is_pipecat_patched

    # Metrics
    if name == "VoiceMetrics":
        from .metrics import VoiceMetrics

        return VoiceMetrics

    if name == "MetricsAggregator":
        from .metrics import MetricsAggregator

        return MetricsAggregator

    # Cost tracking
    if name == "VoiceCostTracker":
        from .cost_tracking import VoiceCostTracker

        return VoiceCostTracker

    if name == "calculate_turn_cost":
        from .cost_tracking import calculate_turn_cost

        return calculate_turn_cost

    if name == "calculate_stt_cost":
        from .cost_tracking import calculate_stt_cost

        return calculate_stt_cost

    if name == "calculate_tts_cost":
        from .cost_tracking import calculate_tts_cost

        return calculate_tts_cost

    if name == "calculate_llm_cost":
        from .cost_tracking import calculate_llm_cost

        return calculate_llm_cost

    if name == "get_stt_pricing":
        from .cost_tracking import get_stt_pricing

        return get_stt_pricing

    if name == "get_tts_pricing":
        from .cost_tracking import get_tts_pricing

        return get_tts_pricing

    if name == "get_llm_pricing":
        from .cost_tracking import get_llm_pricing

        return get_llm_pricing

    # Session management
    if name == "VoiceSessionContext":
        from .session import VoiceSessionContext

        return VoiceSessionContext

    if name == "VoiceSessionManager":
        from .session import VoiceSessionManager

        return VoiceSessionManager

    if name == "voice_session":
        from .session import voice_session

        return voice_session

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

    if name == "PipelineExecutionError":
        from ..._legacy_stubs import PipelineExecutionError

        return PipelineExecutionError

    if name == "VoiceServiceError":
        from ..._legacy_stubs import VoiceServiceError

        return VoiceServiceError

    if name == "VoiceServiceRetry":
        from ..._legacy_stubs import VoiceServiceRetry

        return VoiceServiceRetry

    if name == "retry_decorator":
        from ..._legacy_stubs import retry_decorator

        return retry_decorator

    if name == "with_timeout":
        from ..._legacy_stubs import with_timeout

        return with_timeout

    if name == "with_retry":
        from ..._legacy_stubs import with_retry

        return with_retry

    if name == "with_timeout_and_retry":
        from ..._legacy_stubs import with_timeout_and_retry

        return with_timeout_and_retry

    # Error detection
    if name == "VoiceErrorDetector":
        from .error_detection import VoiceErrorDetector

        return VoiceErrorDetector

    if name == "VoiceErrorType":
        from .error_detection import VoiceErrorType

        return VoiceErrorType

    if name == "ErrorSeverity":
        from .error_detection import ErrorSeverity

        return ErrorSeverity

    if name == "DetectedVoiceError":
        from .error_detection import DetectedVoiceError

        return DetectedVoiceError

    if name == "VoiceErrorStats":
        from .error_detection import VoiceErrorStats

        return VoiceErrorStats

    if name == "get_voice_error_detector":
        from .error_detection import get_voice_error_detector

        return get_voice_error_detector

    if name == "reset_voice_error_detector":
        from .error_detection import reset_voice_error_detector

        return reset_voice_error_detector

    # Drift detection
    if name == "VoiceDriftDetector":
        from .drift_detection import VoiceDriftDetector

        return VoiceDriftDetector

    if name == "VoiceDriftType":
        from .drift_detection import VoiceDriftType

        return VoiceDriftType

    if name == "DriftSeverity":
        from .drift_detection import DriftSeverity

        return DriftSeverity

    if name == "DetectedDrift":
        from .drift_detection import DetectedDrift

        return DetectedDrift

    if name == "VoicePipelineExpectations":
        from .drift_detection import VoicePipelineExpectations

        return VoicePipelineExpectations

    if name == "TurnExecution":
        from .drift_detection import TurnExecution

        return TurnExecution

    if name == "get_voice_drift_detector":
        from .drift_detection import get_voice_drift_detector

        return get_voice_drift_detector

    if name == "reset_voice_drift_detector":
        from .drift_detection import reset_voice_drift_detector

        return reset_voice_drift_detector

    # Utilities
    if name == "is_pipecat_available":
        from .utils import is_pipecat_available

        return is_pipecat_available

    if name == "get_pipecat_version":
        from .utils import get_pipecat_version

        return get_pipecat_version

    if name == "safe_str":
        from .utils import safe_str

        return safe_str

    if name == "truncate_text":
        from .utils import truncate_text

        return truncate_text

    if name == "mask_sensitive_transcription":
        from .utils import mask_sensitive_transcription

        return mask_sensitive_transcription

    if name == "mask_sensitive_data":
        from .utils import mask_sensitive_data

        return mask_sensitive_data

    if name == "mask_dict_keys":
        from .utils import mask_dict_keys

        return mask_dict_keys

    if name == "extract_frame_type":
        from .utils import extract_frame_type

        return extract_frame_type

    if name == "extract_text_from_frame":
        from .utils import extract_text_from_frame

        return extract_text_from_frame

    if name == "extract_audio_metadata":
        from .utils import extract_audio_metadata

        return extract_audio_metadata

    if name == "serialize_frame":
        from .utils import serialize_frame

        return serialize_frame

    if name == "extract_model_from_service":
        from .utils import extract_model_from_service

        return extract_model_from_service

    if name == "format_duration_ms":
        from .utils import format_duration_ms

        return format_duration_ms

    if name == "calculate_audio_duration_ms":
        from .utils import calculate_audio_duration_ms

        return calculate_audio_duration_ms

    if name == "normalize_model_name":
        from .utils import normalize_model_name

        return normalize_model_name

    if name == "get_frame_category":
        from .utils import get_frame_category

        return get_frame_category

    if name == "VOICE_SENSITIVE_PATTERNS":
        from .utils import VOICE_SENSITIVE_PATTERNS

        return VOICE_SENSITIVE_PATTERNS

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .auto_instrument import (
        is_pipecat_patched,
        patch_pipecat,
        unpatch_pipecat,
    )
    from .config import PipecatConfig
    from .cost_tracking import (
        VoiceCostTracker,
        calculate_llm_cost,
        calculate_stt_cost,
        calculate_tts_cost,
        calculate_turn_cost,
        get_llm_pricing,
        get_stt_pricing,
        get_tts_pricing,
    )
    from .drift_detection import (
        DetectedDrift,
        DriftSeverity,
        TurnExecution,
        VoiceDriftDetector,
        VoiceDriftType,
        VoicePipelineExpectations,
        get_voice_drift_detector,
        reset_voice_drift_detector,
    )
    from .error_detection import (
        DetectedVoiceError,
        ErrorSeverity,
        VoiceErrorDetector,
        VoiceErrorStats,
        VoiceErrorType,
        get_voice_error_detector,
        reset_voice_error_detector,
    )
    from .handler import AigieObserver
    from .metrics import MetricsAggregator, VoiceMetrics
    from ..._legacy_stubs import (
        PipelineExecutionError,
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        VoiceServiceError,
        VoiceServiceRetry,
        retry_decorator,
        with_retry,
        with_timeout,
        with_timeout_and_retry,
    )
    from .session import (
        VoiceSessionContext,
        VoiceSessionManager,
        clear_session_context,
        get_or_create_session_context,
        get_session_context,
        set_session_context,
        voice_session,
    )
    from .utils import (
        VOICE_SENSITIVE_PATTERNS,
        calculate_audio_duration_ms,
        extract_audio_metadata,
        extract_frame_type,
        extract_model_from_service,
        extract_text_from_frame,
        format_duration_ms,
        get_frame_category,
        get_pipecat_version,
        is_pipecat_available,
        mask_dict_keys,
        mask_sensitive_data,
        mask_sensitive_transcription,
        normalize_model_name,
        safe_str,
        serialize_frame,
        truncate_text,
    )
