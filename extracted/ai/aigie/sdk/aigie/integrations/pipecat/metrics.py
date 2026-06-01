"""
Voice metrics tracking for Pipecat integration.

Provides metrics aggregation for real-time voice applications including
TTFB, latency, audio duration, and token usage tracking.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    """Get current time in UTC with timezone info."""
    return datetime.now(timezone.utc)


@dataclass
class VoiceMetrics:
    """
    Metrics for a single voice interaction (turn).

    Captures timing, audio, and token metrics for voice-to-voice latency analysis.
    """

    # Timing metrics (in milliseconds)
    stt_ttfb_ms: float | None = None  # Time to first transcription
    llm_ttfb_ms: float | None = None  # Time to first LLM token
    tts_ttfb_ms: float | None = None  # Time to first audio byte
    user_bot_latency_ms: float | None = None  # End-to-end response time

    # Duration metrics (in milliseconds)
    stt_duration_ms: float | None = None
    llm_duration_ms: float | None = None
    tts_duration_ms: float | None = None
    user_speech_duration_ms: float | None = None
    bot_speech_duration_ms: float | None = None

    # Token metrics
    input_tokens: int = 0
    output_tokens: int = 0

    # TTS metrics
    tts_characters: int = 0

    # Audio metadata
    audio_sample_rate: int | None = None
    audio_channels: int | None = None
    audio_format: str | None = None

    # Timestamps for calculation
    _user_started_speaking: datetime | None = None
    _user_stopped_speaking: datetime | None = None
    _bot_started_speaking: datetime | None = None
    _bot_stopped_speaking: datetime | None = None
    _stt_start: datetime | None = None
    _stt_first_result: datetime | None = None
    _stt_end: datetime | None = None
    _llm_start: datetime | None = None
    _llm_first_token: datetime | None = None
    _llm_end: datetime | None = None
    _tts_start: datetime | None = None
    _tts_first_audio: datetime | None = None
    _tts_end: datetime | None = None

    def record_user_started_speaking(self) -> None:
        """Record when user started speaking."""
        self._user_started_speaking = _utc_now()

    def record_user_stopped_speaking(self) -> None:
        """Record when user stopped speaking."""
        self._user_stopped_speaking = _utc_now()
        if self._user_started_speaking:
            delta = (self._user_stopped_speaking - self._user_started_speaking).total_seconds()
            self.user_speech_duration_ms = delta * 1000

    def record_bot_started_speaking(self) -> None:
        """Record when bot started speaking."""
        self._bot_started_speaking = _utc_now()
        # Calculate user-to-bot latency
        if self._user_stopped_speaking:
            delta = (self._bot_started_speaking - self._user_stopped_speaking).total_seconds()
            self.user_bot_latency_ms = delta * 1000

    def record_bot_stopped_speaking(self) -> None:
        """Record when bot stopped speaking."""
        self._bot_stopped_speaking = _utc_now()
        if self._bot_started_speaking:
            delta = (self._bot_stopped_speaking - self._bot_started_speaking).total_seconds()
            self.bot_speech_duration_ms = delta * 1000

    def record_stt_start(self) -> None:
        """Record STT processing start."""
        self._stt_start = _utc_now()

    def record_stt_first_result(self) -> None:
        """Record first STT result (TTFB)."""
        self._stt_first_result = _utc_now()
        if self._stt_start:
            delta = (self._stt_first_result - self._stt_start).total_seconds()
            self.stt_ttfb_ms = delta * 1000

    def record_stt_end(self) -> None:
        """Record STT processing end."""
        self._stt_end = _utc_now()
        if self._stt_start:
            delta = (self._stt_end - self._stt_start).total_seconds()
            self.stt_duration_ms = delta * 1000

    def record_llm_start(self) -> None:
        """Record LLM processing start."""
        self._llm_start = _utc_now()

    def record_llm_first_token(self) -> None:
        """Record first LLM token (TTFB)."""
        self._llm_first_token = _utc_now()
        if self._llm_start:
            delta = (self._llm_first_token - self._llm_start).total_seconds()
            self.llm_ttfb_ms = delta * 1000

    def record_llm_end(self, input_tokens: int = 0, output_tokens: int = 0) -> None:
        """Record LLM processing end with token counts."""
        self._llm_end = _utc_now()
        if self._llm_start:
            delta = (self._llm_end - self._llm_start).total_seconds()
            self.llm_duration_ms = delta * 1000
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens

    def record_tts_start(self) -> None:
        """Record TTS processing start."""
        self._tts_start = _utc_now()

    def record_tts_first_audio(self) -> None:
        """Record first TTS audio byte (TTFB)."""
        self._tts_first_audio = _utc_now()
        if self._tts_start:
            delta = (self._tts_first_audio - self._tts_start).total_seconds()
            self.tts_ttfb_ms = delta * 1000

    def record_tts_end(self, characters: int = 0) -> None:
        """Record TTS processing end with character count."""
        self._tts_end = _utc_now()
        if self._tts_start:
            delta = (self._tts_end - self._tts_start).total_seconds()
            self.tts_duration_ms = delta * 1000
        self.tts_characters = characters

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary for serialization."""
        return {
            # Timing metrics
            "stt_ttfb_ms": self.stt_ttfb_ms,
            "llm_ttfb_ms": self.llm_ttfb_ms,
            "tts_ttfb_ms": self.tts_ttfb_ms,
            "user_bot_latency_ms": self.user_bot_latency_ms,
            # Duration metrics
            "stt_duration_ms": self.stt_duration_ms,
            "llm_duration_ms": self.llm_duration_ms,
            "tts_duration_ms": self.tts_duration_ms,
            "user_speech_duration_ms": self.user_speech_duration_ms,
            "bot_speech_duration_ms": self.bot_speech_duration_ms,
            # Token metrics
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.input_tokens + self.output_tokens,
            # TTS metrics
            "tts_characters": self.tts_characters,
            # Audio metadata
            "audio_sample_rate": self.audio_sample_rate,
            "audio_channels": self.audio_channels,
            "audio_format": self.audio_format,
        }


@dataclass
class MetricsAggregator:
    """
    Aggregates metrics across a full conversation.

    Provides summary statistics for conversation-level analysis.
    """

    turn_count: int = 0
    interruption_count: int = 0
    total_user_speech_ms: float = 0.0
    total_bot_speech_ms: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tts_characters: int = 0

    # TTFB averages (stored as sums for averaging)
    _stt_ttfb_sum: float = 0.0
    _stt_ttfb_count: int = 0
    _llm_ttfb_sum: float = 0.0
    _llm_ttfb_count: int = 0
    _tts_ttfb_sum: float = 0.0
    _tts_ttfb_count: int = 0
    _user_bot_latency_sum: float = 0.0
    _user_bot_latency_count: int = 0

    # Per-turn metrics
    turn_metrics: list[VoiceMetrics] = field(default_factory=list)

    def record_turn(self, metrics: VoiceMetrics) -> None:
        """Record metrics from a completed turn."""
        self.turn_count += 1
        self.turn_metrics.append(metrics)

        # Aggregate duration metrics
        if metrics.user_speech_duration_ms:
            self.total_user_speech_ms += metrics.user_speech_duration_ms
        if metrics.bot_speech_duration_ms:
            self.total_bot_speech_ms += metrics.bot_speech_duration_ms

        # Aggregate token metrics
        self.total_input_tokens += metrics.input_tokens
        self.total_output_tokens += metrics.output_tokens
        self.total_tts_characters += metrics.tts_characters

        # Aggregate TTFB for averages
        if metrics.stt_ttfb_ms is not None:
            self._stt_ttfb_sum += metrics.stt_ttfb_ms
            self._stt_ttfb_count += 1
        if metrics.llm_ttfb_ms is not None:
            self._llm_ttfb_sum += metrics.llm_ttfb_ms
            self._llm_ttfb_count += 1
        if metrics.tts_ttfb_ms is not None:
            self._tts_ttfb_sum += metrics.tts_ttfb_ms
            self._tts_ttfb_count += 1
        if metrics.user_bot_latency_ms is not None:
            self._user_bot_latency_sum += metrics.user_bot_latency_ms
            self._user_bot_latency_count += 1

    def record_interruption(self) -> None:
        """Record an interruption event."""
        self.interruption_count += 1

    @property
    def avg_stt_ttfb_ms(self) -> float | None:
        """Average STT time-to-first-byte."""
        if self._stt_ttfb_count == 0:
            return None
        return self._stt_ttfb_sum / self._stt_ttfb_count

    @property
    def avg_llm_ttfb_ms(self) -> float | None:
        """Average LLM time-to-first-byte."""
        if self._llm_ttfb_count == 0:
            return None
        return self._llm_ttfb_sum / self._llm_ttfb_count

    @property
    def avg_tts_ttfb_ms(self) -> float | None:
        """Average TTS time-to-first-byte."""
        if self._tts_ttfb_count == 0:
            return None
        return self._tts_ttfb_sum / self._tts_ttfb_count

    @property
    def avg_user_bot_latency_ms(self) -> float | None:
        """Average user-to-bot latency."""
        if self._user_bot_latency_count == 0:
            return None
        return self._user_bot_latency_sum / self._user_bot_latency_count

    def to_dict(self) -> dict[str, Any]:
        """Convert aggregated metrics to dictionary for serialization."""
        return {
            "turn_count": self.turn_count,
            "interruption_count": self.interruption_count,
            "total_user_speech_ms": self.total_user_speech_ms,
            "total_bot_speech_ms": self.total_bot_speech_ms,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_tts_characters": self.total_tts_characters,
            # Averages
            "avg_stt_ttfb_ms": self.avg_stt_ttfb_ms,
            "avg_llm_ttfb_ms": self.avg_llm_ttfb_ms,
            "avg_tts_ttfb_ms": self.avg_tts_ttfb_ms,
            "avg_user_bot_latency_ms": self.avg_user_bot_latency_ms,
        }
