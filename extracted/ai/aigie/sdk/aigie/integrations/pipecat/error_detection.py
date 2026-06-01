"""
Error Detection and Monitoring for Pipecat integration.

Provides voice-specific error detection and classification for
STT, TTS, LLM, and audio processing errors.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class VoiceErrorType(Enum):
    """Classification of voice-specific error types."""

    # Audio errors
    AUDIO_DECODE = "audio_decode"
    AUDIO_ENCODE = "audio_encode"
    AUDIO_FORMAT = "audio_format"
    AUDIO_QUALITY = "audio_quality"
    NO_AUDIO = "no_audio"

    # STT errors
    STT_TIMEOUT = "stt_timeout"
    STT_NO_SPEECH = "stt_no_speech"
    STT_UNINTELLIGIBLE = "stt_unintelligible"
    STT_SERVICE_ERROR = "stt_service_error"

    # LLM errors
    LLM_TIMEOUT = "llm_timeout"
    LLM_CONTEXT_LENGTH = "llm_context_length"
    LLM_RATE_LIMIT = "llm_rate_limit"
    LLM_SERVICE_ERROR = "llm_service_error"
    LLM_CONTENT_FILTER = "llm_content_filter"

    # TTS errors
    TTS_TIMEOUT = "tts_timeout"
    TTS_INVALID_TEXT = "tts_invalid_text"
    TTS_VOICE_NOT_FOUND = "tts_voice_not_found"
    TTS_SERVICE_ERROR = "tts_service_error"

    # Pipeline errors
    PIPELINE_TIMEOUT = "pipeline_timeout"
    PIPELINE_OVERFLOW = "pipeline_overflow"
    FRAME_DROP = "frame_drop"

    # Network errors
    NETWORK_ERROR = "network_error"
    CONNECTION_LOST = "connection_lost"

    # Unknown
    UNKNOWN = "unknown"


class ErrorSeverity(Enum):
    """Severity levels for errors."""

    LOW = "low"  # Minor issues, no action needed
    MEDIUM = "medium"  # May affect quality, worth investigating
    HIGH = "high"  # Significant impact, needs attention
    CRITICAL = "critical"  # Execution failed, immediate action needed


@dataclass
class DetectedVoiceError:
    """Represents a detected voice error with full context."""

    error_type: VoiceErrorType
    severity: ErrorSeverity
    message: str
    source: str  # e.g., "stt", "tts", "llm", "pipeline"
    is_transient: bool
    raw_error: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "error_type": self.error_type.value,
            "severity": self.severity.value,
            "message": self.message,
            "source": self.source,
            "is_transient": self.is_transient,
            "raw_error": self.raw_error,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class VoiceErrorStats:
    """Statistics for voice error monitoring."""

    total_errors: int = 0
    errors_by_type: Dict[str, int] = field(default_factory=dict)
    errors_by_source: Dict[str, int] = field(default_factory=dict)
    errors_by_severity: Dict[str, int] = field(default_factory=dict)
    transient_errors: int = 0
    permanent_errors: int = 0
    recent_errors: List[DetectedVoiceError] = field(default_factory=list)

    def record(self, error: DetectedVoiceError) -> None:
        """Record an error in statistics."""
        self.total_errors += 1

        # By type
        type_key = error.error_type.value
        self.errors_by_type[type_key] = self.errors_by_type.get(type_key, 0) + 1

        # By source
        self.errors_by_source[error.source] = self.errors_by_source.get(error.source, 0) + 1

        # By severity
        sev_key = error.severity.value
        self.errors_by_severity[sev_key] = self.errors_by_severity.get(sev_key, 0) + 1

        # Transient vs permanent
        if error.is_transient:
            self.transient_errors += 1
        else:
            self.permanent_errors += 1

        # Keep last 100 errors
        self.recent_errors.append(error)
        if len(self.recent_errors) > 100:
            self.recent_errors = self.recent_errors[-100:]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "total_errors": self.total_errors,
            "errors_by_type": self.errors_by_type,
            "errors_by_source": self.errors_by_source,
            "errors_by_severity": self.errors_by_severity,
            "transient_errors": self.transient_errors,
            "permanent_errors": self.permanent_errors,
        }


# Voice-specific error patterns
VOICE_ERROR_PATTERNS = [
    # STT errors
    (
        r"no\s+speech\s+detected|speech\s+not\s+detected",
        VoiceErrorType.STT_NO_SPEECH,
        ErrorSeverity.LOW,
        False,
    ),
    (
        r"could\s+not\s+understand|unintelligible|unclear\s+audio",
        VoiceErrorType.STT_UNINTELLIGIBLE,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"stt\s+(?:timeout|timed?\s*out)", VoiceErrorType.STT_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (
        r"speech\s+recognition\s+(?:error|failed)",
        VoiceErrorType.STT_SERVICE_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    # TTS errors
    (r"tts\s+(?:timeout|timed?\s*out)", VoiceErrorType.TTS_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (
        r"voice\s+not\s+found|invalid\s+voice",
        VoiceErrorType.TTS_VOICE_NOT_FOUND,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"text\s+(?:too\s+long|invalid)|invalid\s+(?:ssml|text)",
        VoiceErrorType.TTS_INVALID_TEXT,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"speech\s+synthesis\s+(?:error|failed)|tts\s+(?:error|failed)",
        VoiceErrorType.TTS_SERVICE_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    # LLM errors
    (
        r"llm\s+(?:timeout|timed?\s*out)|model\s+timeout",
        VoiceErrorType.LLM_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"context\s+(?:length|window)\s+exceeded|too\s+many\s+tokens",
        VoiceErrorType.LLM_CONTEXT_LENGTH,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"rate\s+limit|too\s+many\s+requests|429",
        VoiceErrorType.LLM_RATE_LIMIT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"content\s+(?:filter|blocked)|safety\s+(?:filter|violation)",
        VoiceErrorType.LLM_CONTENT_FILTER,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"llm\s+(?:error|failed)|model\s+(?:error|failed)",
        VoiceErrorType.LLM_SERVICE_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    # Audio errors
    (
        r"audio\s+decode\s+(?:error|failed)|invalid\s+audio\s+data",
        VoiceErrorType.AUDIO_DECODE,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"audio\s+encode\s+(?:error|failed)", VoiceErrorType.AUDIO_ENCODE, ErrorSeverity.HIGH, False),
    (
        r"unsupported\s+(?:audio\s+)?format|invalid\s+(?:audio\s+)?format",
        VoiceErrorType.AUDIO_FORMAT,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"low\s+audio\s+quality|poor\s+audio|audio\s+quality",
        VoiceErrorType.AUDIO_QUALITY,
        ErrorSeverity.LOW,
        False,
    ),
    (
        r"no\s+audio|missing\s+audio|empty\s+audio",
        VoiceErrorType.NO_AUDIO,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Pipeline errors
    (
        r"pipeline\s+(?:timeout|timed?\s*out)",
        VoiceErrorType.PIPELINE_TIMEOUT,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"(?:buffer|queue)\s+overflow|pipeline\s+overflow",
        VoiceErrorType.PIPELINE_OVERFLOW,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (r"frame\s+(?:drop|dropped|loss)", VoiceErrorType.FRAME_DROP, ErrorSeverity.LOW, True),
    # Network errors
    (
        r"connection\s+(?:lost|closed|reset)|disconnected",
        VoiceErrorType.CONNECTION_LOST,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"network\s+(?:error|failure)|socket\s+error",
        VoiceErrorType.NETWORK_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
]


class VoiceErrorDetector:
    """
    Detects and classifies voice-specific errors.

    Provides:
    - Pattern-based error detection for voice applications
    - Error classification (type, severity, transient/permanent)
    - Error statistics and monitoring
    """

    def __init__(self):
        self.stats = VoiceErrorStats()
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), error_type, severity, is_transient)
            for pattern, error_type, severity, is_transient in VOICE_ERROR_PATTERNS
        ]

    def detect_from_text(
        self,
        text: str,
        source: str,
        context: Dict[str, Any] | None = None,
    ) -> DetectedVoiceError | None:
        """
        Detect errors from text content.

        Args:
            text: Text to analyze for errors
            source: Source identifier (e.g., "stt", "tts", "llm")
            context: Additional context for the error

        Returns:
            DetectedVoiceError if an error is found, None otherwise
        """
        if not text:
            return None

        text_lower = text.lower()

        # Check for explicit error indicators
        is_error_indicator = any(
            indicator in text_lower
            for indicator in ["error", "failed", "failure", "exception", "timeout"]
        )

        # Try to match error patterns
        for pattern, error_type, severity, is_transient in self._compiled_patterns:
            if pattern.search(text):
                error = DetectedVoiceError(
                    error_type=error_type,
                    severity=severity,
                    message=self._extract_error_message(text),
                    source=source,
                    is_transient=is_transient,
                    raw_error=text[:500] if len(text) > 500 else text,
                    metadata=context or {},
                )
                self.stats.record(error)
                logger.warning(f"[AIGIE] Voice error detected: {error_type.value} from {source}")
                return error

        # If we see error indicators but no specific pattern, classify as unknown
        if is_error_indicator:
            error = DetectedVoiceError(
                error_type=VoiceErrorType.UNKNOWN,
                severity=ErrorSeverity.MEDIUM,
                message=self._extract_error_message(text),
                source=source,
                is_transient=False,
                raw_error=text[:500] if len(text) > 500 else text,
                metadata=context or {},
            )
            self.stats.record(error)
            return error

        return None

    def detect_from_exception(
        self,
        exception: Exception,
        source: str,
        context: Dict[str, Any] | None = None,
    ) -> DetectedVoiceError:
        """
        Create DetectedVoiceError from a Python exception.

        Args:
            exception: The exception that occurred
            source: Source identifier
            context: Additional context

        Returns:
            DetectedVoiceError for the exception
        """
        exc_type = type(exception).__name__
        exc_message = str(exception)

        # Try to classify the exception
        error = self.detect_from_text(exc_message, source, context)
        if error:
            error.metadata["exception_type"] = exc_type
            return error

        # Default classification based on exception type
        error_type = VoiceErrorType.UNKNOWN
        severity = ErrorSeverity.HIGH
        is_transient = False

        if "timeout" in exc_type.lower() or "timeout" in exc_message.lower():
            error_type = VoiceErrorType.PIPELINE_TIMEOUT
            is_transient = True
        elif "connection" in exc_type.lower() or "network" in exc_message.lower():
            error_type = VoiceErrorType.NETWORK_ERROR
            is_transient = True

        error = DetectedVoiceError(
            error_type=error_type,
            severity=severity,
            message=f"{exc_type}: {exc_message[:200]}",
            source=source,
            is_transient=is_transient,
            raw_error=f"{exc_type}: {exc_message}",
            metadata={**(context or {}), "exception_type": exc_type},
        )
        self.stats.record(error)
        return error

    def _extract_error_message(self, text: str) -> str:
        """Extract a clean error message from text."""
        patterns = [
            r"error[:\s]+(.+?)(?:\.|$)",
            r"failed[:\s]+(.+?)(?:\.|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                msg = match.group(1).strip()
                if len(msg) > 10:
                    return msg[:200]

        # Return first line or first 200 chars
        first_line = text.split("\n")[0].strip()
        return first_line[:200] if first_line else text[:200]

    def get_stats(self) -> Dict[str, Any]:
        """Get current error statistics."""
        return self.stats.to_dict()

    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent errors as dictionaries."""
        return [e.to_dict() for e in self.stats.recent_errors[-limit:]]


# Global error detector instance
_global_detector: VoiceErrorDetector | None = None


def get_voice_error_detector() -> VoiceErrorDetector:
    """Get or create the global voice error detector instance."""
    global _global_detector
    if _global_detector is None:
        _global_detector = VoiceErrorDetector()
    return _global_detector


def reset_voice_error_detector() -> None:
    """Reset the global voice error detector (for testing)."""
    global _global_detector
    _global_detector = None
