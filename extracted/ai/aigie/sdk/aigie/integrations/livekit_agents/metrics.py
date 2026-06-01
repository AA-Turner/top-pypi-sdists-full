"""
Voice metrics tracking for LiveKit Agents integration.

Provides metrics aggregation for real-time voice applications including
TTFB, latency, audio duration, token usage, and interruption tracking.

LiveKit Agents emits structured metrics via the 'metrics_collected' event:
- LLMMetrics: ttft, duration, completion_tokens, prompt_tokens, tokens_per_second
- STTMetrics: duration, audio_duration, input_tokens, output_tokens
- TTSMetrics: ttfb, duration, audio_duration, characters_count
- EOUMetrics: end_of_utterance_delay, transcription_delay
- InterruptionMetrics: num_interruptions, num_backchannels
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
    Designed to consume LiveKit's native metric types (LLMMetrics, STTMetrics, TTSMetrics).
    """

    # Timing metrics (in milliseconds)
    stt_ttfb_ms: float | None = None
    llm_ttfb_ms: float | None = None
    tts_ttfb_ms: float | None = None
    user_bot_latency_ms: float | None = None
    eou_delay_ms: float | None = None

    # Duration metrics (in milliseconds)
    stt_duration_ms: float | None = None
    llm_duration_ms: float | None = None
    tts_duration_ms: float | None = None
    user_speech_duration_ms: float | None = None
    bot_speech_duration_ms: float | None = None

    # Token metrics
    input_tokens: int = 0
    output_tokens: int = 0
    tokens_per_second: float | None = None

    # TTS metrics
    tts_characters: int = 0

    # Audio metadata
    audio_duration_seconds: float | None = None

    # Timestamps for calculation
    _user_started_speaking: datetime | None = field(
        default=None, init=False, repr=False, compare=False
    )
    _user_stopped_speaking: datetime | None = field(
        default=None, init=False, repr=False, compare=False
    )
    _bot_started_speaking: datetime | None = field(
        default=None, init=False, repr=False, compare=False
    )
    _bot_stopped_speaking: datetime | None = field(
        default=None, init=False, repr=False, compare=False
    )
    _stt_start: datetime | None = field(default=None, init=False, repr=False, compare=False)
    _llm_start: datetime | None = field(default=None, init=False, repr=False, compare=False)
    _tts_start: datetime | None = field(default=None, init=False, repr=False, compare=False)

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
        if self._user_stopped_speaking:
            delta = (self._bot_started_speaking - self._user_stopped_speaking).total_seconds()
            self.user_bot_latency_ms = delta * 1000

    def record_bot_stopped_speaking(self) -> None:
        """Record when bot stopped speaking."""
        self._bot_stopped_speaking = _utc_now()
        if self._bot_started_speaking:
            delta = (self._bot_stopped_speaking - self._bot_started_speaking).total_seconds()
            self.bot_speech_duration_ms = delta * 1000

    def record_llm_metrics(self, metrics: Any) -> None:
        """Record metrics from a LiveKit LLMMetrics event."""
        self.llm_ttfb_ms = getattr(metrics, "ttft", None)
        if self.llm_ttfb_ms is not None:
            self.llm_ttfb_ms *= 1000  # seconds to ms
        duration = getattr(metrics, "duration", None)
        if duration is not None:
            self.llm_duration_ms = duration * 1000
        self.input_tokens = getattr(metrics, "prompt_tokens", 0) or 0
        self.output_tokens = getattr(metrics, "completion_tokens", 0) or 0
        self.tokens_per_second = getattr(metrics, "tokens_per_second", None)

    def record_stt_metrics(self, metrics: Any) -> None:
        """Record metrics from a LiveKit STTMetrics event."""
        duration = getattr(metrics, "duration", None)
        if duration is not None:
            self.stt_duration_ms = duration * 1000
        self.audio_duration_seconds = getattr(metrics, "audio_duration", None)

    def record_tts_metrics(self, metrics: Any) -> None:
        """Record metrics from a LiveKit TTSMetrics event."""
        self.tts_ttfb_ms = getattr(metrics, "ttfb", None)
        if self.tts_ttfb_ms is not None:
            self.tts_ttfb_ms *= 1000
        duration = getattr(metrics, "duration", None)
        if duration is not None:
            self.tts_duration_ms = duration * 1000
        self.tts_characters = getattr(metrics, "characters_count", 0) or 0

    def record_eou_metrics(self, metrics: Any) -> None:
        """Record metrics from a LiveKit EOUMetrics event."""
        delay = getattr(metrics, "end_of_utterance_delay", None)
        if delay is not None:
            self.eou_delay_ms = delay * 1000

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary for serialization."""
        return {
            "stt_ttfb_ms": self.stt_ttfb_ms,
            "llm_ttfb_ms": self.llm_ttfb_ms,
            "tts_ttfb_ms": self.tts_ttfb_ms,
            "user_bot_latency_ms": self.user_bot_latency_ms,
            "eou_delay_ms": self.eou_delay_ms,
            "stt_duration_ms": self.stt_duration_ms,
            "llm_duration_ms": self.llm_duration_ms,
            "tts_duration_ms": self.tts_duration_ms,
            "user_speech_duration_ms": self.user_speech_duration_ms,
            "bot_speech_duration_ms": self.bot_speech_duration_ms,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.input_tokens + self.output_tokens,
            "tokens_per_second": self.tokens_per_second,
            "tts_characters": self.tts_characters,
            "audio_duration_seconds": self.audio_duration_seconds,
        }


@dataclass
class MetricsAggregator:
    """
    Aggregates metrics across a full LiveKit Agents conversation.

    Provides summary statistics for conversation-level analysis.
    """

    turn_count: int = 0
    interruption_count: int = 0
    backchannel_count: int = 0
    total_user_speech_ms: float = 0.0
    total_bot_speech_ms: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tts_characters: int = 0
    total_audio_seconds: float = 0.0

    _stt_ttfb_sum: float = 0.0
    _stt_ttfb_count: int = 0
    _llm_ttfb_sum: float = 0.0
    _llm_ttfb_count: int = 0
    _tts_ttfb_sum: float = 0.0
    _tts_ttfb_count: int = 0
    _user_bot_latency_sum: float = 0.0
    _user_bot_latency_count: int = 0
    _eou_delay_sum: float = 0.0
    _eou_delay_count: int = 0

    turn_metrics: list[VoiceMetrics] = field(default_factory=list)

    def record_turn(self, metrics: VoiceMetrics) -> None:
        """Record metrics from a completed turn."""
        self.turn_count += 1
        self.turn_metrics.append(metrics)

        if metrics.user_speech_duration_ms:
            self.total_user_speech_ms += metrics.user_speech_duration_ms
        if metrics.bot_speech_duration_ms:
            self.total_bot_speech_ms += metrics.bot_speech_duration_ms
        self.total_input_tokens += metrics.input_tokens
        self.total_output_tokens += metrics.output_tokens
        self.total_tts_characters += metrics.tts_characters
        if metrics.audio_duration_seconds:
            self.total_audio_seconds += metrics.audio_duration_seconds

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
        if metrics.eou_delay_ms is not None:
            self._eou_delay_sum += metrics.eou_delay_ms
            self._eou_delay_count += 1

    def record_interruption(self) -> None:
        """Record an interruption event."""
        self.interruption_count += 1

    def record_interruption_metrics(self, metrics: Any) -> None:
        """Record from LiveKit InterruptionMetrics."""
        num = getattr(metrics, "num_interruptions", 0) or 0
        self.interruption_count += num
        bc = getattr(metrics, "num_backchannels", 0) or 0
        self.backchannel_count += bc

    @property
    def avg_stt_ttfb_ms(self) -> float | None:
        if self._stt_ttfb_count == 0:
            return None
        return self._stt_ttfb_sum / self._stt_ttfb_count

    @property
    def avg_llm_ttfb_ms(self) -> float | None:
        if self._llm_ttfb_count == 0:
            return None
        return self._llm_ttfb_sum / self._llm_ttfb_count

    @property
    def avg_tts_ttfb_ms(self) -> float | None:
        if self._tts_ttfb_count == 0:
            return None
        return self._tts_ttfb_sum / self._tts_ttfb_count

    @property
    def avg_user_bot_latency_ms(self) -> float | None:
        if self._user_bot_latency_count == 0:
            return None
        return self._user_bot_latency_sum / self._user_bot_latency_count

    @property
    def avg_eou_delay_ms(self) -> float | None:
        if self._eou_delay_count == 0:
            return None
        return self._eou_delay_sum / self._eou_delay_count

    def to_dict(self) -> dict[str, Any]:
        """Convert aggregated metrics to dictionary for serialization."""
        return {
            "turn_count": self.turn_count,
            "interruption_count": self.interruption_count,
            "backchannel_count": self.backchannel_count,
            "total_user_speech_ms": self.total_user_speech_ms,
            "total_bot_speech_ms": self.total_bot_speech_ms,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_tts_characters": self.total_tts_characters,
            "total_audio_seconds": self.total_audio_seconds,
            "avg_stt_ttfb_ms": self.avg_stt_ttfb_ms,
            "avg_llm_ttfb_ms": self.avg_llm_ttfb_ms,
            "avg_tts_ttfb_ms": self.avg_tts_ttfb_ms,
            "avg_user_bot_latency_ms": self.avg_user_bot_latency_ms,
            "avg_eou_delay_ms": self.avg_eou_delay_ms,
        }
