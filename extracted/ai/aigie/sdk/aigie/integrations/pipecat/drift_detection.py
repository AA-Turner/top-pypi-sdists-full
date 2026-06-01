"""
Drift Detection for Pipecat Voice Pipelines.

Tracks expected conversation flow vs actual execution to detect behavioral drifts.
Useful for monitoring voice pipeline reliability and detecting deviations.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class VoiceDriftType(Enum):
    """Types of behavioral drift in voice pipelines."""

    # Turn flow drifts
    MISSING_RESPONSE = "missing_response"  # Bot didn't respond to user
    EXTRA_RESPONSE = "extra_response"  # Bot responded unexpectedly
    TURN_TIMEOUT = "turn_timeout"  # Turn took too long

    # Service drifts
    STT_MISSING = "stt_missing"  # No transcription received
    STT_EMPTY = "stt_empty"  # Empty transcription
    LLM_MISSING = "llm_missing"  # No LLM response
    LLM_TRUNCATED = "llm_truncated"  # LLM response cut short
    TTS_MISSING = "tts_missing"  # No audio generated
    TTS_FAILED = "tts_failed"  # TTS failed to generate

    # Interruption drifts
    EXCESSIVE_INTERRUPTIONS = "excessive_interruptions"  # Too many interruptions
    BOT_INTERRUPTED = "bot_interrupted"  # Bot was interrupted frequently

    # Latency drifts
    HIGH_STT_LATENCY = "high_stt_latency"  # STT TTFB too high
    HIGH_LLM_LATENCY = "high_llm_latency"  # LLM TTFB too high
    HIGH_TTS_LATENCY = "high_tts_latency"  # TTS TTFB too high
    HIGH_E2E_LATENCY = "high_e2e_latency"  # End-to-end latency too high

    # Quality drifts
    POOR_AUDIO_QUALITY = "poor_audio_quality"  # Low confidence transcription
    SHORT_RESPONSE = "short_response"  # Response too brief
    LONG_RESPONSE = "long_response"  # Response too long

    # Error drifts
    SERVICE_ERROR = "service_error"  # Service returned error
    PIPELINE_ERROR = "pipeline_error"  # Pipeline processing error


class DriftSeverity(Enum):
    """Severity of detected drift."""

    INFO = "info"  # Expected variation, informational
    WARNING = "warning"  # Notable deviation, worth monitoring
    ALERT = "alert"  # Significant drift, may need intervention


@dataclass
class DetectedDrift:
    """Represents a detected drift with full context."""

    drift_type: VoiceDriftType
    severity: DriftSeverity
    description: str
    expected: str | None = None
    actual: str | None = None
    turn_number: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "drift_type": self.drift_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "expected": self.expected,
            "actual": self.actual,
            "turn_number": self.turn_number,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class VoicePipelineExpectations:
    """Defines expected behavior for a voice pipeline."""

    # Turn expectations
    max_turn_duration_ms: float = 15000  # 15 seconds max per turn
    min_response_length: int = 10  # Min bot response chars
    max_response_length: int = 2000  # Max bot response chars

    # Latency thresholds (ms)
    max_stt_ttfb_ms: float = 500  # Max STT time to first result
    max_llm_ttfb_ms: float = 1000  # Max LLM time to first token
    max_tts_ttfb_ms: float = 500  # Max TTS time to first audio
    max_e2e_latency_ms: float = 3000  # Max end-to-end user-to-bot

    # Interruption thresholds
    max_interruptions_per_conversation: int = 5
    max_interruptions_per_turn: int = 2

    # Quality thresholds
    min_transcription_confidence: float = 0.7

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "max_turn_duration_ms": self.max_turn_duration_ms,
            "min_response_length": self.min_response_length,
            "max_response_length": self.max_response_length,
            "max_stt_ttfb_ms": self.max_stt_ttfb_ms,
            "max_llm_ttfb_ms": self.max_llm_ttfb_ms,
            "max_tts_ttfb_ms": self.max_tts_ttfb_ms,
            "max_e2e_latency_ms": self.max_e2e_latency_ms,
            "max_interruptions_per_conversation": self.max_interruptions_per_conversation,
            "max_interruptions_per_turn": self.max_interruptions_per_turn,
            "min_transcription_confidence": self.min_transcription_confidence,
        }


@dataclass
class TurnExecution:
    """Tracks actual execution of a single turn."""

    turn_number: int
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None

    # Service events
    stt_received: bool = False
    stt_text: str | None = None
    stt_confidence: float | None = None
    stt_ttfb_ms: float | None = None

    llm_received: bool = False
    llm_text: str | None = None
    llm_ttfb_ms: float | None = None
    llm_input_tokens: int = 0
    llm_output_tokens: int = 0

    tts_received: bool = False
    tts_ttfb_ms: float | None = None

    # Interruptions in this turn
    interruption_count: int = 0
    was_interrupted: bool = False

    # User-to-bot latency
    e2e_latency_ms: float | None = None

    # Errors
    errors: List[str] = field(default_factory=list)

    @property
    def duration_ms(self) -> float | None:
        """Get turn duration in ms."""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "turn_number": self.turn_number,
            "duration_ms": self.duration_ms,
            "stt_received": self.stt_received,
            "stt_text_length": len(self.stt_text) if self.stt_text else 0,
            "stt_ttfb_ms": self.stt_ttfb_ms,
            "llm_received": self.llm_received,
            "llm_text_length": len(self.llm_text) if self.llm_text else 0,
            "llm_ttfb_ms": self.llm_ttfb_ms,
            "tts_received": self.tts_received,
            "tts_ttfb_ms": self.tts_ttfb_ms,
            "e2e_latency_ms": self.e2e_latency_ms,
            "interruption_count": self.interruption_count,
            "was_interrupted": self.was_interrupted,
            "error_count": len(self.errors),
        }


class VoiceDriftDetector:
    """
    Detects drift in voice pipeline execution.

    Captures:
    - Expected pipeline behavior (latency thresholds, turn expectations)
    - Actual execution path (STT, LLM, TTS events, timing)
    - Compares and reports deviations
    """

    def __init__(self, expectations: VoicePipelineExpectations | None = None):
        self.expectations = expectations or VoicePipelineExpectations()
        self.turns: List[TurnExecution] = []
        self.current_turn: TurnExecution | None = None
        self.detected_drifts: List[DetectedDrift] = []

        # Conversation-level tracking
        self.total_interruptions: int = 0
        self.conversation_start: datetime | None = None
        self.conversation_end: datetime | None = None

    def start_conversation(self) -> None:
        """Mark conversation start."""
        self.conversation_start = datetime.now()
        self.turns = []
        self.detected_drifts = []
        self.total_interruptions = 0

    def start_turn(self, turn_number: int) -> TurnExecution:
        """Start tracking a new turn."""
        # Complete previous turn if exists
        if self.current_turn:
            self._complete_turn()

        self.current_turn = TurnExecution(turn_number=turn_number)
        return self.current_turn

    def record_stt(
        self,
        text: str,
        ttfb_ms: float | None = None,
        confidence: float | None = None,
    ) -> DetectedDrift | None:
        """Record STT result and check for drift."""
        if not self.current_turn:
            return None

        self.current_turn.stt_received = True
        self.current_turn.stt_text = text
        self.current_turn.stt_ttfb_ms = ttfb_ms
        self.current_turn.stt_confidence = confidence

        # Check for empty transcription
        if not text or not text.strip():
            drift = DetectedDrift(
                drift_type=VoiceDriftType.STT_EMPTY,
                severity=DriftSeverity.WARNING,
                description="Empty transcription received",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check TTFB
        if ttfb_ms and ttfb_ms > self.expectations.max_stt_ttfb_ms:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.HIGH_STT_LATENCY,
                severity=DriftSeverity.WARNING,
                description=f"STT TTFB ({ttfb_ms:.0f}ms) exceeds threshold",
                expected=f"<{self.expectations.max_stt_ttfb_ms}ms",
                actual=f"{ttfb_ms:.0f}ms",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check confidence
        if confidence and confidence < self.expectations.min_transcription_confidence:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.POOR_AUDIO_QUALITY,
                severity=DriftSeverity.INFO,
                description=f"Low transcription confidence ({confidence:.2f})",
                expected=f">{self.expectations.min_transcription_confidence}",
                actual=f"{confidence:.2f}",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_llm(
        self,
        text: str,
        ttfb_ms: float | None = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> DetectedDrift | None:
        """Record LLM result and check for drift."""
        if not self.current_turn:
            return None

        self.current_turn.llm_received = True
        self.current_turn.llm_text = text
        self.current_turn.llm_ttfb_ms = ttfb_ms
        self.current_turn.llm_input_tokens = input_tokens
        self.current_turn.llm_output_tokens = output_tokens

        # Check TTFB
        if ttfb_ms and ttfb_ms > self.expectations.max_llm_ttfb_ms:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.HIGH_LLM_LATENCY,
                severity=DriftSeverity.WARNING,
                description=f"LLM TTFB ({ttfb_ms:.0f}ms) exceeds threshold",
                expected=f"<{self.expectations.max_llm_ttfb_ms}ms",
                actual=f"{ttfb_ms:.0f}ms",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check response length
        text_len = len(text) if text else 0
        if text_len < self.expectations.min_response_length:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.SHORT_RESPONSE,
                severity=DriftSeverity.INFO,
                description=f"LLM response too short ({text_len} chars)",
                expected=f">{self.expectations.min_response_length} chars",
                actual=f"{text_len} chars",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            return drift

        if text_len > self.expectations.max_response_length:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.LONG_RESPONSE,
                severity=DriftSeverity.INFO,
                description=f"LLM response too long ({text_len} chars)",
                expected=f"<{self.expectations.max_response_length} chars",
                actual=f"{text_len} chars",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_tts(self, ttfb_ms: float | None = None) -> DetectedDrift | None:
        """Record TTS result and check for drift."""
        if not self.current_turn:
            return None

        self.current_turn.tts_received = True
        self.current_turn.tts_ttfb_ms = ttfb_ms

        # Check TTFB
        if ttfb_ms and ttfb_ms > self.expectations.max_tts_ttfb_ms:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.HIGH_TTS_LATENCY,
                severity=DriftSeverity.WARNING,
                description=f"TTS TTFB ({ttfb_ms:.0f}ms) exceeds threshold",
                expected=f"<{self.expectations.max_tts_ttfb_ms}ms",
                actual=f"{ttfb_ms:.0f}ms",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_e2e_latency(self, latency_ms: float) -> DetectedDrift | None:
        """Record end-to-end latency and check for drift."""
        if not self.current_turn:
            return None

        self.current_turn.e2e_latency_ms = latency_ms

        if latency_ms > self.expectations.max_e2e_latency_ms:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.HIGH_E2E_LATENCY,
                severity=DriftSeverity.ALERT,
                description=f"E2E latency ({latency_ms:.0f}ms) exceeds threshold",
                expected=f"<{self.expectations.max_e2e_latency_ms}ms",
                actual=f"{latency_ms:.0f}ms",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_interruption(self) -> DetectedDrift | None:
        """Record an interruption and check for drift."""
        self.total_interruptions += 1

        if self.current_turn:
            self.current_turn.interruption_count += 1
            self.current_turn.was_interrupted = True

            # Check per-turn interruption threshold
            if self.current_turn.interruption_count > self.expectations.max_interruptions_per_turn:
                drift = DetectedDrift(
                    drift_type=VoiceDriftType.BOT_INTERRUPTED,
                    severity=DriftSeverity.WARNING,
                    description=f"Turn interrupted {self.current_turn.interruption_count} times",
                    expected=f"<{self.expectations.max_interruptions_per_turn} interruptions",
                    actual=f"{self.current_turn.interruption_count} interruptions",
                    turn_number=self.current_turn.turn_number,
                )
                self.detected_drifts.append(drift)
                return drift

        # Check conversation-level interruption threshold
        if self.total_interruptions > self.expectations.max_interruptions_per_conversation:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.EXCESSIVE_INTERRUPTIONS,
                severity=DriftSeverity.ALERT,
                description=f"Conversation has {self.total_interruptions} interruptions",
                expected=f"<{self.expectations.max_interruptions_per_conversation} interruptions",
                actual=f"{self.total_interruptions} interruptions",
                turn_number=self.current_turn.turn_number if self.current_turn else 0,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_error(self, error: str, service: str = "pipeline") -> DetectedDrift:
        """Record an error."""
        drift_type = (
            VoiceDriftType.SERVICE_ERROR if service != "pipeline" else VoiceDriftType.PIPELINE_ERROR
        )

        if self.current_turn:
            self.current_turn.errors.append(error)

        drift = DetectedDrift(
            drift_type=drift_type,
            severity=DriftSeverity.ALERT,
            description=f"{service.upper()} error: {error[:100]}",
            turn_number=self.current_turn.turn_number if self.current_turn else 0,
            metadata={"service": service, "error": error},
        )
        self.detected_drifts.append(drift)
        return drift

    def end_turn(self) -> List[DetectedDrift]:
        """End the current turn and perform final checks."""
        if not self.current_turn:
            return []

        drifts = self._complete_turn()
        return drifts

    def _complete_turn(self) -> List[DetectedDrift]:
        """Complete the current turn with final analysis."""
        if not self.current_turn:
            return []

        self.current_turn.end_time = datetime.now()
        drifts: List[DetectedDrift] = []

        # Check for missing services
        if not self.current_turn.stt_received:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.STT_MISSING,
                severity=DriftSeverity.WARNING,
                description="No STT transcription received for turn",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            drifts.append(drift)

        if not self.current_turn.llm_received:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.LLM_MISSING,
                severity=DriftSeverity.WARNING,
                description="No LLM response received for turn",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            drifts.append(drift)

        if not self.current_turn.tts_received and self.current_turn.llm_received:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.TTS_MISSING,
                severity=DriftSeverity.WARNING,
                description="No TTS audio generated for turn",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            drifts.append(drift)

        # Check turn duration
        duration = self.current_turn.duration_ms
        if duration and duration > self.expectations.max_turn_duration_ms:
            drift = DetectedDrift(
                drift_type=VoiceDriftType.TURN_TIMEOUT,
                severity=DriftSeverity.WARNING,
                description=f"Turn duration ({duration:.0f}ms) exceeds threshold",
                expected=f"<{self.expectations.max_turn_duration_ms}ms",
                actual=f"{duration:.0f}ms",
                turn_number=self.current_turn.turn_number,
            )
            self.detected_drifts.append(drift)
            drifts.append(drift)

        # Save turn and reset
        self.turns.append(self.current_turn)
        self.current_turn = None

        return drifts

    def end_conversation(self) -> List[DetectedDrift]:
        """End conversation and perform final analysis."""
        self.conversation_end = datetime.now()

        # Complete any pending turn
        drifts = []
        if self.current_turn:
            drifts = self._complete_turn()

        return drifts

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of drift detection results."""
        return {
            "expectations": self.expectations.to_dict(),
            "turns": [t.to_dict() for t in self.turns],
            "drifts": [d.to_dict() for d in self.detected_drifts],
            "drift_count": len(self.detected_drifts),
            "turn_count": len(self.turns),
            "total_interruptions": self.total_interruptions,
            "has_warnings": any(
                d.severity in [DriftSeverity.WARNING, DriftSeverity.ALERT]
                for d in self.detected_drifts
            ),
            "has_alerts": any(d.severity == DriftSeverity.ALERT for d in self.detected_drifts),
        }

    def get_drift_report(self) -> str:
        """Get a human-readable drift report."""
        if not self.detected_drifts:
            return "No drifts detected - voice pipeline executed as expected"

        report = f"Detected {len(self.detected_drifts)} drift(s):\n"
        for i, drift in enumerate(self.detected_drifts, 1):
            report += f"\n{i}. [{drift.severity.value.upper()}] {drift.drift_type.value}"
            if drift.turn_number:
                report += f" (Turn {drift.turn_number})"
            report += f"\n   {drift.description}\n"
            if drift.expected:
                report += f"   Expected: {drift.expected}\n"
            if drift.actual:
                report += f"   Actual: {drift.actual}\n"

        return report

    def get_drift_counts_by_type(self) -> Dict[str, int]:
        """Get counts of each drift type."""
        counts: Dict[str, int] = {}
        for drift in self.detected_drifts:
            key = drift.drift_type.value
            counts[key] = counts.get(key, 0) + 1
        return counts

    def get_drift_counts_by_severity(self) -> Dict[str, int]:
        """Get counts by severity."""
        counts: Dict[str, int] = {}
        for drift in self.detected_drifts:
            key = drift.severity.value
            counts[key] = counts.get(key, 0) + 1
        return counts


# Global drift detector instance
_global_drift_detector: VoiceDriftDetector | None = None


def get_voice_drift_detector(
    expectations: VoicePipelineExpectations | None = None,
) -> VoiceDriftDetector:
    """
    Get or create the global voice drift detector instance.

    This provides a singleton pattern for drift detection, allowing
    drift to be tracked across multiple voice sessions without
    explicit passing of the detector instance.

    Args:
        expectations: Optional expectations configuration. Only used
            when creating a new detector instance.

    Returns:
        The global VoiceDriftDetector instance.
    """
    global _global_drift_detector
    if _global_drift_detector is None:
        _global_drift_detector = VoiceDriftDetector(expectations=expectations)
    return _global_drift_detector


def reset_voice_drift_detector() -> None:
    """
    Reset the global voice drift detector.

    This clears all detected drifts and resets the detector state.
    Useful for testing or when starting a completely new monitoring session.
    """
    global _global_drift_detector
    _global_drift_detector = None
