"""User-facing configuration for the Pipecat integration."""

from __future__ import annotations

import os
from dataclasses import dataclass, replace
from typing import Any

from aigie.tracing.config_base import FrameworkConfigBase


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {raw!r}") from exc


@dataclass
class PipecatConfig(FrameworkConfigBase):
    """Configuration for Pipecat voice-pipeline tracing behavior.

    Inherits ``zero_retention: bool`` from FrameworkConfigBase.

    ``capture_transcripts`` is deliberately separate from ``capture_inputs``: a
    voice transcript is the most sensitive payload this SDK touches, so an
    operator can keep spans while dropping recorded speech.

    Attributes:
        trace_conversations: Whether to trace conversations
        trace_turns: Whether to trace turns
        trace_llm_calls: Whether to trace LLM calls
        trace_tools: Whether to trace tool invocations
        trace_stt: Whether to trace speech-to-text
        trace_tts: Whether to trace text-to-speech
        capture_transcripts: Whether to capture voice transcripts
        capture_inputs: Whether to capture input data
        capture_outputs: Whether to capture output data
        max_content_length: Maximum content length to capture
    """

    trace_conversations: bool = True
    trace_turns: bool = True
    trace_llm_calls: bool = True
    trace_tools: bool = True
    trace_stt: bool = True
    trace_tts: bool = True
    capture_transcripts: bool = True
    capture_inputs: bool = True
    capture_outputs: bool = True
    max_content_length: int = 10000

    def __post_init__(self) -> None:
        if self.max_content_length < 0:
            raise ValueError("max_content_length must be >= 0")

    @classmethod
    def from_env(cls) -> PipecatConfig:
        """Create configuration from ``AIGIE_PIPECAT_*`` environment variables.

        Environment variables:
            AIGIE_PIPECAT_TRACE_CONVERSATIONS: Trace conversations (default: true)
            AIGIE_PIPECAT_TRACE_TURNS: Trace turns (default: true)
            AIGIE_PIPECAT_TRACE_LLM_CALLS: Trace LLM calls (default: true)
            AIGIE_PIPECAT_TRACE_TOOLS: Trace tool invocations (default: true)
            AIGIE_PIPECAT_TRACE_STT: Trace speech-to-text (default: true)
            AIGIE_PIPECAT_TRACE_TTS: Trace text-to-speech (default: true)
            AIGIE_PIPECAT_CAPTURE_TRANSCRIPTS: Capture voice transcripts (default: true)
            AIGIE_PIPECAT_CAPTURE_INPUTS: Capture input data (default: true)
            AIGIE_PIPECAT_CAPTURE_OUTPUTS: Capture output data (default: true)
            AIGIE_PIPECAT_MAX_CONTENT_LENGTH: Max content length (default: 10000)
            AIGIE_PIPECAT_MASK_SENSITIVE_DATA: Mask sensitive data (default: false).
                Reserved — no masking primitive exists in the SDK yet, so this
                flag is currently a no-op.
            AIGIE_PIPECAT_ZERO_RETENTION: Suppress persistence (default: false)
        """
        return cls(
            trace_conversations=_env_bool("AIGIE_PIPECAT_TRACE_CONVERSATIONS", True),
            trace_turns=_env_bool("AIGIE_PIPECAT_TRACE_TURNS", True),
            trace_llm_calls=_env_bool("AIGIE_PIPECAT_TRACE_LLM_CALLS", True),
            trace_tools=_env_bool("AIGIE_PIPECAT_TRACE_TOOLS", True),
            trace_stt=_env_bool("AIGIE_PIPECAT_TRACE_STT", True),
            trace_tts=_env_bool("AIGIE_PIPECAT_TRACE_TTS", True),
            capture_transcripts=_env_bool("AIGIE_PIPECAT_CAPTURE_TRANSCRIPTS", True),
            capture_inputs=_env_bool("AIGIE_PIPECAT_CAPTURE_INPUTS", True),
            capture_outputs=_env_bool("AIGIE_PIPECAT_CAPTURE_OUTPUTS", True),
            max_content_length=_env_int("AIGIE_PIPECAT_MAX_CONTENT_LENGTH", 10000),
            zero_retention=_env_bool("AIGIE_PIPECAT_ZERO_RETENTION", False),
        )

    def merge(self, **overrides: Any) -> PipecatConfig:
        """Create a new config with overridden values."""
        return replace(self, **overrides)
