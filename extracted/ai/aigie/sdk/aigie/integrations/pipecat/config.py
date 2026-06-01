"""
Configuration for Pipecat integration.
"""

import os
from dataclasses import dataclass


@dataclass
class PipecatConfig:
    """
    Configuration for Pipecat integration.

    Attributes:
        enabled: Whether tracing is enabled
        trace_conversations: Whether to trace full conversations (StartFrame → EndFrame)
        trace_turns: Whether to trace individual turns (User speaks → Bot responds)
        trace_services: Whether to trace service calls (STT, LLM, TTS)
        trace_stt: Whether to trace STT (speech-to-text) calls
        trace_tts: Whether to trace TTS (text-to-speech) calls
        trace_llm: Whether to trace LLM calls
        capture_transcriptions: Whether to capture user transcriptions
        capture_bot_responses: Whether to capture bot text responses
        capture_audio_metadata: Whether to capture audio frame metadata (duration, format)
        capture_ttfb: Whether to capture time-to-first-byte metrics
        capture_latency: Whether to capture latency metrics
        capture_token_usage: Whether to capture LLM token usage
        capture_interruptions: Whether to capture user interruptions
        redact_pii: Whether to redact PII from transcriptions
        max_transcription_length: Maximum length of captured transcriptions
    """

    enabled: bool = True

    # Tracing granularity
    trace_conversations: bool = True
    trace_turns: bool = True
    trace_services: bool = True
    trace_stt: bool = True
    trace_tts: bool = True
    trace_llm: bool = True

    # Data capture
    capture_transcriptions: bool = True
    capture_bot_responses: bool = True
    capture_audio_metadata: bool = True
    capture_ttfb: bool = True
    capture_latency: bool = True
    capture_token_usage: bool = True
    capture_interruptions: bool = True

    # Privacy
    redact_pii: bool = False
    max_transcription_length: int = 2000

    # Model info (optional - can be set for LLM tracking)
    llm_model: str = ""
    stt_model: str = ""
    tts_model: str = ""

    def __post_init__(self):
        """Validate configuration."""
        if self.max_transcription_length < 100:
            raise ValueError("max_transcription_length must be at least 100")

    @classmethod
    def from_env(cls) -> "PipecatConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            AIGIE_PIPECAT_ENABLED: Enable/disable tracing (default: true)
            AIGIE_PIPECAT_TRACE_CONVERSATIONS: Trace conversations (default: true)
            AIGIE_PIPECAT_TRACE_TURNS: Trace turns (default: true)
            AIGIE_PIPECAT_TRACE_SERVICES: Trace services (default: true)
            AIGIE_PIPECAT_TRACE_STT: Trace STT calls (default: true)
            AIGIE_PIPECAT_TRACE_TTS: Trace TTS calls (default: true)
            AIGIE_PIPECAT_TRACE_LLM: Trace LLM calls (default: true)
            AIGIE_PIPECAT_CAPTURE_TRANSCRIPTIONS: Capture transcriptions (default: true)
            AIGIE_PIPECAT_CAPTURE_BOT_RESPONSES: Capture bot responses (default: true)
            AIGIE_PIPECAT_CAPTURE_AUDIO_METADATA: Capture audio metadata (default: true)
            AIGIE_PIPECAT_CAPTURE_TTFB: Capture TTFB metrics (default: true)
            AIGIE_PIPECAT_CAPTURE_LATENCY: Capture latency metrics (default: true)
            AIGIE_PIPECAT_CAPTURE_TOKEN_USAGE: Capture token usage (default: true)
            AIGIE_PIPECAT_CAPTURE_INTERRUPTIONS: Capture interruptions (default: true)
            AIGIE_PIPECAT_REDACT_PII: Redact PII (default: false)
            AIGIE_PIPECAT_MAX_TRANSCRIPTION_LENGTH: Max transcription length (default: 2000)
        """
        return cls(
            enabled=os.getenv("AIGIE_PIPECAT_ENABLED", "true").lower() == "true",
            trace_conversations=os.getenv("AIGIE_PIPECAT_TRACE_CONVERSATIONS", "true").lower()
            == "true",
            trace_turns=os.getenv("AIGIE_PIPECAT_TRACE_TURNS", "true").lower() == "true",
            trace_services=os.getenv("AIGIE_PIPECAT_TRACE_SERVICES", "true").lower() == "true",
            trace_stt=os.getenv("AIGIE_PIPECAT_TRACE_STT", "true").lower() == "true",
            trace_tts=os.getenv("AIGIE_PIPECAT_TRACE_TTS", "true").lower() == "true",
            trace_llm=os.getenv("AIGIE_PIPECAT_TRACE_LLM", "true").lower() == "true",
            capture_transcriptions=os.getenv("AIGIE_PIPECAT_CAPTURE_TRANSCRIPTIONS", "true").lower()
            == "true",
            capture_bot_responses=os.getenv("AIGIE_PIPECAT_CAPTURE_BOT_RESPONSES", "true").lower()
            == "true",
            capture_audio_metadata=os.getenv("AIGIE_PIPECAT_CAPTURE_AUDIO_METADATA", "true").lower()
            == "true",
            capture_ttfb=os.getenv("AIGIE_PIPECAT_CAPTURE_TTFB", "true").lower() == "true",
            capture_latency=os.getenv("AIGIE_PIPECAT_CAPTURE_LATENCY", "true").lower() == "true",
            capture_token_usage=os.getenv("AIGIE_PIPECAT_CAPTURE_TOKEN_USAGE", "true").lower()
            == "true",
            capture_interruptions=os.getenv("AIGIE_PIPECAT_CAPTURE_INTERRUPTIONS", "true").lower()
            == "true",
            redact_pii=os.getenv("AIGIE_PIPECAT_REDACT_PII", "false").lower() == "true",
            max_transcription_length=int(
                os.getenv("AIGIE_PIPECAT_MAX_TRANSCRIPTION_LENGTH", "2000")
            ),
            llm_model=os.getenv("AIGIE_PIPECAT_LLM_MODEL", ""),
            stt_model=os.getenv("AIGIE_PIPECAT_STT_MODEL", ""),
            tts_model=os.getenv("AIGIE_PIPECAT_TTS_MODEL", ""),
        )

    def merge(self, **overrides) -> "PipecatConfig":
        """
        Create a new config with overridden values.

        Args:
            **overrides: Values to override

        Returns:
            New PipecatConfig with overrides applied
        """
        return PipecatConfig(
            enabled=overrides.get("enabled", self.enabled),
            trace_conversations=overrides.get("trace_conversations", self.trace_conversations),
            trace_turns=overrides.get("trace_turns", self.trace_turns),
            trace_services=overrides.get("trace_services", self.trace_services),
            trace_stt=overrides.get("trace_stt", self.trace_stt),
            trace_tts=overrides.get("trace_tts", self.trace_tts),
            trace_llm=overrides.get("trace_llm", self.trace_llm),
            capture_transcriptions=overrides.get(
                "capture_transcriptions", self.capture_transcriptions
            ),
            capture_bot_responses=overrides.get(
                "capture_bot_responses", self.capture_bot_responses
            ),
            capture_audio_metadata=overrides.get(
                "capture_audio_metadata", self.capture_audio_metadata
            ),
            capture_ttfb=overrides.get("capture_ttfb", self.capture_ttfb),
            capture_latency=overrides.get("capture_latency", self.capture_latency),
            capture_token_usage=overrides.get("capture_token_usage", self.capture_token_usage),
            capture_interruptions=overrides.get(
                "capture_interruptions", self.capture_interruptions
            ),
            redact_pii=overrides.get("redact_pii", self.redact_pii),
            max_transcription_length=overrides.get(
                "max_transcription_length", self.max_transcription_length
            ),
            llm_model=overrides.get("llm_model", self.llm_model),
            stt_model=overrides.get("stt_model", self.stt_model),
            tts_model=overrides.get("tts_model", self.tts_model),
        )
