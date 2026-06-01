"""
LiveKit Agents integration for Aigie.

This module provides automatic tracing for LiveKit Agents real-time voice
AI applications, capturing conversations, turns, LLM/STT/TTS metrics,
tool executions, agent handoffs, and interruptions.

Usage (Auto-Instrumentation - Recommended):
    import aigie
    from aigie.integrations.livekit_agents import patch_livekit_agents

    # Initialize Aigie
    aigie_client = aigie.Aigie()
    await aigie_client.initialize()

    # Enable auto-instrumentation
    patch_livekit_agents()

    # Now all AgentSessions are automatically traced
    from livekit.agents import AgentSession
    session = AgentSession()  # Automatically traced!

Usage (Manual Handler):
    from livekit.agents import AgentSession
    from aigie.integrations.livekit_agents import LiveKitAgentsHandler

    handler = LiveKitAgentsHandler(trace_name="my-voice-agent")
    session = AgentSession()
    handler.register(session)

Usage (Cost Tracking):
    from aigie.integrations.livekit_agents import get_livekit_agents_cost

    cost = get_livekit_agents_cost(
        model="gpt-4o-mini",
        input_tokens=100,
        output_tokens=50,
        stt_model="deepgram/nova-3",
        audio_duration_seconds=5.0,
    )

Usage (Configuration):
    from aigie.integrations.livekit_agents import LiveKitAgentsConfig

    config = LiveKitAgentsConfig(
        trace_conversations=True,
        trace_turns=True,
        capture_transcriptions=True,
        redact_pii=True,
    )
"""

from typing import TYPE_CHECKING, Any

__all__ = [
    # Handler
    "LiveKitAgentsHandler",
    # Configuration
    "LiveKitAgentsConfig",
    # Auto-instrumentation
    "patch_livekit_agents",
    "unpatch_livekit_agents",
    "is_livekit_agents_patched",
    # Metrics
    "VoiceMetrics",
    "MetricsAggregator",
    # Cost tracking
    "VoiceCostTracker",
    "get_livekit_agents_cost",
    "calculate_turn_cost",
    "calculate_stt_cost",
    "calculate_tts_cost",
    "calculate_llm_cost",
    "get_stt_pricing",
    "get_tts_pricing",
    "get_llm_pricing",
    # Session management
    "LiveKitSessionContext",
    # Error detection
    "VoiceErrorDetector",
    # Drift detection
    "VoiceDriftDetector",
    # Retry
    "LiveKitRetryContext",
    # Fix adapter
    "LiveKitAgentsFixAdapter",
    # Utilities
    "extract_agent_name",
    "extract_model_info",
    "is_livekit_installed",
]


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Handler
    if name == "LiveKitAgentsHandler":
        from .handler import LiveKitAgentsHandler

        return LiveKitAgentsHandler

    # Configuration
    if name == "LiveKitAgentsConfig":
        from .config import LiveKitAgentsConfig

        return LiveKitAgentsConfig

    # Auto-instrumentation
    if name == "patch_livekit_agents":
        from .auto_instrument import patch_livekit_agents

        return patch_livekit_agents

    if name == "unpatch_livekit_agents":
        from .auto_instrument import unpatch_livekit_agents

        return unpatch_livekit_agents

    if name == "is_livekit_agents_patched":
        from .auto_instrument import is_livekit_agents_patched

        return is_livekit_agents_patched

    # Metrics
    if name == "VoiceMetrics":
        from .metrics import VoiceMetrics

        return VoiceMetrics

    if name == "MetricsAggregator":
        from .metrics import MetricsAggregator

        return MetricsAggregator

    # Cost tracking
    if name in (
        "VoiceCostTracker",
        "get_livekit_agents_cost",
        "calculate_turn_cost",
        "calculate_stt_cost",
        "calculate_tts_cost",
        "calculate_llm_cost",
        "get_stt_pricing",
        "get_tts_pricing",
        "get_llm_pricing",
    ):
        from . import cost_tracking

        return getattr(cost_tracking, name)

    # Session management
    if name == "LiveKitSessionContext":
        from .session import LiveKitSessionContext

        return LiveKitSessionContext

    # Error detection
    if name == "VoiceErrorDetector":
        from .error_detection import VoiceErrorDetector

        return VoiceErrorDetector

    # Drift detection
    if name == "VoiceDriftDetector":
        from .drift_detection import VoiceDriftDetector

        return VoiceDriftDetector

    # Retry
    if name == "LiveKitRetryContext":
        from ..._legacy_stubs import LiveKitRetryContext

        return LiveKitRetryContext

    # Fix adapter
    if name == "LiveKitAgentsFixAdapter":
        from .fix_adapter import LiveKitAgentsFixAdapter

        return LiveKitAgentsFixAdapter

    # Utilities
    if name in ("extract_agent_name", "extract_model_info", "is_livekit_installed"):
        from . import utils

        return getattr(utils, name)

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .auto_instrument import (
        is_livekit_agents_patched,
        patch_livekit_agents,
        unpatch_livekit_agents,
    )
    from .config import LiveKitAgentsConfig
    from .cost_tracking import (
        VoiceCostTracker,
        calculate_llm_cost,
        calculate_stt_cost,
        calculate_tts_cost,
        calculate_turn_cost,
        get_livekit_agents_cost,
        get_llm_pricing,
        get_stt_pricing,
        get_tts_pricing,
    )
    from .drift_detection import VoiceDriftDetector
    from .error_detection import VoiceErrorDetector
    from .fix_adapter import LiveKitAgentsFixAdapter
    from .handler import LiveKitAgentsHandler
    from .metrics import MetricsAggregator, VoiceMetrics
    from ..._legacy_stubs import LiveKitRetryContext
    from .session import LiveKitSessionContext
    from .utils import extract_agent_name, extract_model_info, is_livekit_installed
