"""
Configuration for LiveKit Agents integration.
"""

import dataclasses
import os
from dataclasses import dataclass


@dataclass
class LiveKitAgentsConfig:
    """
    Configuration for LiveKit Agents integration.

    Attributes:
        enabled: Whether tracing is enabled
        trace_conversations: Whether to trace full session traces
        trace_turns: Whether to trace user-to-agent turn cycles
        trace_services: Whether to trace service calls (STT, LLM, TTS spans)
        trace_stt: Whether to trace STT (speech-to-text) calls
        trace_tts: Whether to trace TTS (text-to-speech) calls
        trace_llm: Whether to trace LLM calls
        trace_tools: Whether to trace function tool calls
        trace_handoffs: Whether to trace agent-to-agent transitions
        capture_transcriptions: Whether to capture user transcriptions
        capture_bot_responses: Whether to capture bot text responses
        capture_audio_metadata: Whether to capture audio frame metadata (duration, format)
        capture_ttfb: Whether to capture time-to-first-byte metrics
        capture_latency: Whether to capture latency metrics
        capture_token_usage: Whether to capture LLM token usage
        capture_interruptions: Whether to capture user interruptions
        capture_tool_calls: Whether to capture tool call details
        redact_pii: Whether to redact PII from transcriptions
        max_transcription_length: Maximum length of captured transcriptions
        max_content_length: Maximum length of captured content
        llm_model: LLM model identifier (optional)
        stt_model: STT model identifier (optional)
        tts_model: TTS model identifier (optional)
        enable_realtime_remediation: Whether to enable realtime remediation
        remediation_mode: Remediation mode (recommendation or correction)
        remediation_query_timeout: Timeout for remediation queries in seconds
    """

    enabled: bool = True

    # Tracing granularity
    trace_conversations: bool = True
    trace_turns: bool = True
    trace_services: bool = True
    trace_stt: bool = True
    trace_tts: bool = True
    trace_llm: bool = True
    trace_tools: bool = True
    trace_handoffs: bool = True

    # Data capture
    capture_transcriptions: bool = True
    capture_bot_responses: bool = True
    capture_audio_metadata: bool = True
    capture_ttfb: bool = True
    capture_latency: bool = True
    capture_token_usage: bool = True
    capture_interruptions: bool = True
    capture_tool_calls: bool = True

    # Privacy
    redact_pii: bool = False
    max_transcription_length: int = 2000
    max_content_length: int = 2000

    # Model info (optional - can be set for tracking)
    llm_model: str = ""
    stt_model: str = ""
    tts_model: str = ""

    # Cost tracking
    use_cost_tracking: bool = True

    # Remediation
    enable_realtime_remediation: bool = False
    remediation_mode: str = "recommendation"
    remediation_query_timeout: float = 2.0

    def __post_init__(self):
        """Validate configuration."""
        if self.max_transcription_length < 100:
            raise ValueError("max_transcription_length must be at least 100")
        if self.max_content_length < 100:
            raise ValueError("max_content_length must be at least 100")
        if self.remediation_mode not in ("recommendation", "correction"):
            raise ValueError(
                f"remediation_mode must be 'recommendation' or 'correction', "
                f"got '{self.remediation_mode}'"
            )
        if self.remediation_query_timeout <= 0:
            raise ValueError("remediation_query_timeout must be positive")

    @classmethod
    def from_env(cls) -> "LiveKitAgentsConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            AIGIE_LIVEKIT_ENABLED: Enable/disable tracing (default: true)
            AIGIE_LIVEKIT_TRACE_CONVERSATIONS: Trace conversations (default: true)
            AIGIE_LIVEKIT_TRACE_TURNS: Trace turns (default: true)
            AIGIE_LIVEKIT_TRACE_SERVICES: Trace services (default: true)
            AIGIE_LIVEKIT_TRACE_STT: Trace STT calls (default: true)
            AIGIE_LIVEKIT_TRACE_TTS: Trace TTS calls (default: true)
            AIGIE_LIVEKIT_TRACE_LLM: Trace LLM calls (default: true)
            AIGIE_LIVEKIT_TRACE_TOOLS: Trace tool calls (default: true)
            AIGIE_LIVEKIT_TRACE_HANDOFFS: Trace handoffs (default: true)
            AIGIE_LIVEKIT_CAPTURE_TRANSCRIPTIONS: Capture transcriptions (default: true)
            AIGIE_LIVEKIT_CAPTURE_BOT_RESPONSES: Capture bot responses (default: true)
            AIGIE_LIVEKIT_CAPTURE_AUDIO_METADATA: Capture audio metadata (default: true)
            AIGIE_LIVEKIT_CAPTURE_TTFB: Capture TTFB metrics (default: true)
            AIGIE_LIVEKIT_CAPTURE_LATENCY: Capture latency metrics (default: true)
            AIGIE_LIVEKIT_CAPTURE_TOKEN_USAGE: Capture token usage (default: true)
            AIGIE_LIVEKIT_CAPTURE_INTERRUPTIONS: Capture interruptions (default: true)
            AIGIE_LIVEKIT_CAPTURE_TOOL_CALLS: Capture tool calls (default: true)
            AIGIE_LIVEKIT_REDACT_PII: Redact PII (default: false)
            AIGIE_LIVEKIT_MAX_TRANSCRIPTION_LENGTH: Max transcription length (default: 2000)
            AIGIE_LIVEKIT_MAX_CONTENT_LENGTH: Max content length (default: 2000)
            AIGIE_LIVEKIT_LLM_MODEL: LLM model identifier (default: "")
            AIGIE_LIVEKIT_STT_MODEL: STT model identifier (default: "")
            AIGIE_LIVEKIT_TTS_MODEL: TTS model identifier (default: "")
            AIGIE_LIVEKIT_ENABLE_REALTIME_REMEDIATION: Enable remediation (default: false)
            AIGIE_LIVEKIT_REMEDIATION_MODE: Remediation mode (default: recommendation)
            AIGIE_LIVEKIT_REMEDIATION_QUERY_TIMEOUT: Query timeout (default: 2.0)
        """
        return cls(
            enabled=os.getenv("AIGIE_LIVEKIT_ENABLED", "true").lower() == "true",
            trace_conversations=os.getenv("AIGIE_LIVEKIT_TRACE_CONVERSATIONS", "true").lower()
            == "true",
            trace_turns=os.getenv("AIGIE_LIVEKIT_TRACE_TURNS", "true").lower() == "true",
            trace_services=os.getenv("AIGIE_LIVEKIT_TRACE_SERVICES", "true").lower() == "true",
            trace_stt=os.getenv("AIGIE_LIVEKIT_TRACE_STT", "true").lower() == "true",
            trace_tts=os.getenv("AIGIE_LIVEKIT_TRACE_TTS", "true").lower() == "true",
            trace_llm=os.getenv("AIGIE_LIVEKIT_TRACE_LLM", "true").lower() == "true",
            trace_tools=os.getenv("AIGIE_LIVEKIT_TRACE_TOOLS", "true").lower() == "true",
            trace_handoffs=os.getenv("AIGIE_LIVEKIT_TRACE_HANDOFFS", "true").lower() == "true",
            capture_transcriptions=os.getenv("AIGIE_LIVEKIT_CAPTURE_TRANSCRIPTIONS", "true").lower()
            == "true",
            capture_bot_responses=os.getenv("AIGIE_LIVEKIT_CAPTURE_BOT_RESPONSES", "true").lower()
            == "true",
            capture_audio_metadata=os.getenv("AIGIE_LIVEKIT_CAPTURE_AUDIO_METADATA", "true").lower()
            == "true",
            capture_ttfb=os.getenv("AIGIE_LIVEKIT_CAPTURE_TTFB", "true").lower() == "true",
            capture_latency=os.getenv("AIGIE_LIVEKIT_CAPTURE_LATENCY", "true").lower() == "true",
            capture_token_usage=os.getenv("AIGIE_LIVEKIT_CAPTURE_TOKEN_USAGE", "true").lower()
            == "true",
            capture_interruptions=os.getenv("AIGIE_LIVEKIT_CAPTURE_INTERRUPTIONS", "true").lower()
            == "true",
            capture_tool_calls=os.getenv("AIGIE_LIVEKIT_CAPTURE_TOOL_CALLS", "true").lower()
            == "true",
            redact_pii=os.getenv("AIGIE_LIVEKIT_REDACT_PII", "false").lower() == "true",
            max_transcription_length=int(
                os.getenv("AIGIE_LIVEKIT_MAX_TRANSCRIPTION_LENGTH", "2000")
            ),
            max_content_length=int(os.getenv("AIGIE_LIVEKIT_MAX_CONTENT_LENGTH", "2000")),
            llm_model=os.getenv("AIGIE_LIVEKIT_LLM_MODEL", ""),
            stt_model=os.getenv("AIGIE_LIVEKIT_STT_MODEL", ""),
            tts_model=os.getenv("AIGIE_LIVEKIT_TTS_MODEL", ""),
            use_cost_tracking=os.getenv("AIGIE_LIVEKIT_USE_COST_TRACKING", "true").lower()
            == "true",
            enable_realtime_remediation=os.getenv(
                "AIGIE_LIVEKIT_ENABLE_REALTIME_REMEDIATION", "false"
            ).lower()
            == "true",
            remediation_mode=os.getenv("AIGIE_LIVEKIT_REMEDIATION_MODE", "recommendation"),
            remediation_query_timeout=float(
                os.getenv("AIGIE_LIVEKIT_REMEDIATION_QUERY_TIMEOUT", "2.0")
            ),
        )

    def merge(self, **overrides) -> "LiveKitAgentsConfig":
        """Create a new config with overridden values."""
        return dataclasses.replace(self, **overrides)
