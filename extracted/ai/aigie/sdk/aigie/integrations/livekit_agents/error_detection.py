"""
Error Detection and Monitoring for LiveKit Agents integration.

Provides voice-specific error detection and classification for
STT, TTS, LLM, VAD, and connection errors in LiveKit Agents.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class VoiceErrorType(Enum):
    """Classification of voice-specific error types for LiveKit Agents."""

    # STT errors
    STT_TIMEOUT = "stt_timeout"
    STT_NO_SPEECH = "stt_no_speech"
    STT_UNINTELLIGIBLE = "stt_unintelligible"
    STT_SERVICE_ERROR = "stt_service_error"
    TRANSCRIPTION_FAILURE = "transcription_failure"

    # LLM errors
    LLM_TIMEOUT = "llm_timeout"
    LLM_CONTEXT_LENGTH = "llm_context_length"
    LLM_RATE_LIMIT = "llm_rate_limit"
    LLM_SERVICE_ERROR = "llm_service_error"
    LLM_CONTENT_FILTER = "llm_content_filter"
    MODEL_OVERLOADED = "model_overloaded"

    # TTS errors
    TTS_TIMEOUT = "tts_timeout"
    TTS_INVALID_TEXT = "tts_invalid_text"
    TTS_VOICE_NOT_FOUND = "tts_voice_not_found"
    TTS_SERVICE_ERROR = "tts_service_error"
    SYNTHESIS_FAILURE = "synthesis_failure"

    # VAD errors
    VAD_ERROR = "vad_error"
    VAD_TIMEOUT = "vad_timeout"

    # Tool execution errors
    TOOL_ERROR = "tool_error"
    TOOL_TIMEOUT = "tool_timeout"
    TOOL_NOT_FOUND = "tool_not_found"

    # Connection errors
    CONNECTION_LOST = "connection_lost"
    CONNECTION_TIMEOUT = "connection_timeout"
    ROOM_CONNECTION_ERROR = "room_connection_error"
    PARTICIPANT_DISCONNECTED = "participant_disconnected"

    # Network errors
    NETWORK_ERROR = "network_error"
    WEBSOCKET_ERROR = "websocket_error"

    # Unknown
    UNKNOWN = "unknown"


class ErrorSeverity(Enum):
    """Severity levels for errors."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DetectedVoiceError:
    """Represents a detected voice error with full context."""

    error_type: VoiceErrorType
    severity: ErrorSeverity
    message: str
    source: str  # e.g., "stt", "tts", "llm", "vad", "tool", "connection"
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


# LiveKit Agents typed error class names for direct matching
LIVEKIT_ERROR_CLASS_MAP: Dict[str, tuple[VoiceErrorType, ErrorSeverity, str, bool]] = {
    "LLMError": (VoiceErrorType.LLM_SERVICE_ERROR, ErrorSeverity.HIGH, "llm", True),
    "STTError": (VoiceErrorType.STT_SERVICE_ERROR, ErrorSeverity.HIGH, "stt", True),
    "TTSError": (VoiceErrorType.TTS_SERVICE_ERROR, ErrorSeverity.HIGH, "tts", True),
    "VADError": (VoiceErrorType.VAD_ERROR, ErrorSeverity.HIGH, "vad", True),
    "AssistantError": (VoiceErrorType.UNKNOWN, ErrorSeverity.HIGH, "agent", True),
    "AgentError": (VoiceErrorType.UNKNOWN, ErrorSeverity.HIGH, "agent", True),
}


# Voice-specific error patterns (regex, error_type, severity, is_transient)
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
    (
        r"stt\s+(?:timeout|timed?\s*out)|transcription\s+timeout",
        VoiceErrorType.STT_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"speech\s+recognition\s+(?:error|failed)|transcription\s+(?:error|failed)",
        VoiceErrorType.TRANSCRIPTION_FAILURE,
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
        VoiceErrorType.SYNTHESIS_FAILURE,
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
        r"model\s+(?:overloaded|capacity)|server\s+overloaded|503",
        VoiceErrorType.MODEL_OVERLOADED,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"llm\s+(?:error|failed)|model\s+(?:error|failed)",
        VoiceErrorType.LLM_SERVICE_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    # VAD errors
    (
        r"vad\s+(?:error|failed)|voice\s+activity\s+detection\s+(?:error|failed)",
        VoiceErrorType.VAD_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (r"vad\s+(?:timeout|timed?\s*out)", VoiceErrorType.VAD_TIMEOUT, ErrorSeverity.MEDIUM, True),
    # Tool execution errors
    (
        r"tool\s+(?:execution\s+)?(?:error|failed)|function\s+call\s+(?:error|failed)",
        VoiceErrorType.TOOL_ERROR,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"tool\s+(?:timeout|timed?\s*out)|function\s+call\s+timeout",
        VoiceErrorType.TOOL_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"tool\s+not\s+found|function\s+not\s+found|unknown\s+(?:tool|function)",
        VoiceErrorType.TOOL_NOT_FOUND,
        ErrorSeverity.HIGH,
        False,
    ),
    # Connection errors
    (
        r"connection\s+(?:lost|closed|reset)|disconnected",
        VoiceErrorType.CONNECTION_LOST,
        ErrorSeverity.CRITICAL,
        True,
    ),
    (
        r"connection\s+(?:timeout|timed?\s*out)",
        VoiceErrorType.CONNECTION_TIMEOUT,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"room\s+(?:connection\s+)?(?:error|failed)|could\s+not\s+connect\s+to\s+room",
        VoiceErrorType.ROOM_CONNECTION_ERROR,
        ErrorSeverity.CRITICAL,
        True,
    ),
    (
        r"participant\s+(?:disconnected|left)|peer\s+disconnected",
        VoiceErrorType.PARTICIPANT_DISCONNECTED,
        ErrorSeverity.HIGH,
        False,
    ),
    # Network errors
    (
        r"network\s+(?:error|failure)|socket\s+error",
        VoiceErrorType.NETWORK_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"websocket\s+(?:error|closed|failed)",
        VoiceErrorType.WEBSOCKET_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
]


class VoiceErrorDetector:
    """
    Detects and classifies voice-specific errors for LiveKit Agents.

    Provides:
    - Typed error detection for LiveKit Agents exceptions (LLMError, STTError, etc.)
    - Pattern-based error detection for voice applications
    - Error classification (type, severity, transient/permanent)
    - Error statistics and monitoring
    - Error frequency tracking
    """

    def __init__(self) -> None:
        self.stats = VoiceErrorStats()
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), error_type, severity, is_transient)
            for pattern, error_type, severity, is_transient in VOICE_ERROR_PATTERNS
        ]
        self._error_frequency: Dict[str, List[datetime]] = {}

    def detect_error(
        self,
        error: Exception,
        context: Dict[str, Any] | None = None,
    ) -> DetectedVoiceError | None:
        """
        Detect and classify an error from a LiveKit Agents pipeline.

        First checks for typed LiveKit errors (LLMError, STTError, etc.),
        then falls back to pattern-based detection.

        Args:
            error: The exception that occurred.
            context: Additional context (e.g., room_id, participant_id).

        Returns:
            DetectedVoiceError if classified, None if not an error of interest.
        """
        if error is None:
            return None

        exc_type_name = type(error).__name__
        exc_message = str(error)

        # Check for typed LiveKit Agents errors
        if exc_type_name in LIVEKIT_ERROR_CLASS_MAP:
            error_type, severity, source, is_transient = LIVEKIT_ERROR_CLASS_MAP[exc_type_name]

            # Refine classification based on message content
            refined = self._refine_from_message(exc_message, error_type, severity, is_transient)
            if refined:
                error_type, severity, is_transient = refined

            detected = DetectedVoiceError(
                error_type=error_type,
                severity=severity,
                message=f"{exc_type_name}: {exc_message[:200]}",
                source=source,
                is_transient=is_transient,
                raw_error=f"{exc_type_name}: {exc_message}",
                metadata={**(context or {}), "exception_type": exc_type_name},
            )
            self._record_and_track(detected)
            logger.warning(
                f"[AIGIE] LiveKit voice error detected: {error_type.value} from {source}"
            )
            return detected

        # Fall back to pattern-based detection from exception
        return self.detect_from_exception(error, context=context)

    def detect_from_text(
        self,
        text: str,
        source: str,
        context: Dict[str, Any] | None = None,
    ) -> DetectedVoiceError | None:
        """
        Detect errors from text content (e.g., log messages).

        Args:
            text: Text to analyze for errors.
            source: Source identifier (e.g., "stt", "tts", "llm").
            context: Additional context for the error.

        Returns:
            DetectedVoiceError if an error is found, None otherwise.
        """
        if not text:
            return None

        text_lower = text.lower()

        is_error_indicator = any(
            indicator in text_lower
            for indicator in ["error", "failed", "failure", "exception", "timeout"]
        )

        for pattern, error_type, severity, is_transient in self._compiled_patterns:
            if pattern.search(text):
                detected = DetectedVoiceError(
                    error_type=error_type,
                    severity=severity,
                    message=self._extract_error_message(text),
                    source=source,
                    is_transient=is_transient,
                    raw_error=text[:500] if len(text) > 500 else text,
                    metadata=context or {},
                )
                self._record_and_track(detected)
                logger.warning(f"[AIGIE] Voice error detected: {error_type.value} from {source}")
                return detected

        if is_error_indicator:
            detected = DetectedVoiceError(
                error_type=VoiceErrorType.UNKNOWN,
                severity=ErrorSeverity.MEDIUM,
                message=self._extract_error_message(text),
                source=source,
                is_transient=False,
                raw_error=text[:500] if len(text) > 500 else text,
                metadata=context or {},
            )
            self._record_and_track(detected)
            return detected

        return None

    def detect_from_exception(
        self,
        exception: Exception,
        source: str | None = None,
        context: Dict[str, Any] | None = None,
    ) -> DetectedVoiceError:
        """
        Create DetectedVoiceError from a Python exception.

        Args:
            exception: The exception that occurred.
            source: Source identifier. If None, inferred from exception type.
            context: Additional context.

        Returns:
            DetectedVoiceError for the exception.
        """
        exc_type = type(exception).__name__
        exc_message = str(exception)
        inferred_source = source or self._infer_source(exc_type, exc_message)

        # Try to classify via text patterns
        text_error = self.detect_from_text(exc_message, inferred_source, context)
        if text_error:
            text_error.metadata["exception_type"] = exc_type
            return text_error

        # Default classification based on exception type
        error_type = VoiceErrorType.UNKNOWN
        severity = ErrorSeverity.HIGH
        is_transient = False

        if "timeout" in exc_type.lower() or "timeout" in exc_message.lower():
            error_type = VoiceErrorType.CONNECTION_TIMEOUT
            is_transient = True
        elif "connection" in exc_type.lower() or "network" in exc_message.lower():
            error_type = VoiceErrorType.NETWORK_ERROR
            is_transient = True
        elif "websocket" in exc_type.lower() or "websocket" in exc_message.lower():
            error_type = VoiceErrorType.WEBSOCKET_ERROR
            is_transient = True

        detected = DetectedVoiceError(
            error_type=error_type,
            severity=severity,
            message=f"{exc_type}: {exc_message[:200]}",
            source=inferred_source,
            is_transient=is_transient,
            raw_error=f"{exc_type}: {exc_message}",
            metadata={**(context or {}), "exception_type": exc_type},
        )
        self._record_and_track(detected)
        return detected

    def get_error_frequency(self, error_type: str, window_seconds: int = 60) -> int:
        """
        Get the frequency of a specific error type within a time window.

        Args:
            error_type: The error type value string.
            window_seconds: Time window in seconds to check.

        Returns:
            Number of occurrences within the window.
        """
        if error_type not in self._error_frequency:
            return 0

        now = datetime.now()
        timestamps = self._error_frequency[error_type]
        cutoff = now.timestamp() - window_seconds
        recent = [ts for ts in timestamps if ts.timestamp() >= cutoff]
        self._error_frequency[error_type] = recent
        return len(recent)

    def is_error_recurring(
        self,
        error_type: str,
        threshold: int = 3,
        window_seconds: int = 60,
    ) -> bool:
        """
        Check if an error type is recurring above a threshold.

        Args:
            error_type: The error type value string.
            threshold: Minimum occurrences to consider recurring.
            window_seconds: Time window in seconds.

        Returns:
            True if the error is recurring above the threshold.
        """
        return self.get_error_frequency(error_type, window_seconds) >= threshold

    def _refine_from_message(
        self,
        message: str,
        default_type: VoiceErrorType,
        default_severity: ErrorSeverity,
        default_transient: bool,
    ) -> tuple[VoiceErrorType, ErrorSeverity, bool] | None:
        """Refine error classification based on message content."""
        msg_lower = message.lower()

        if "timeout" in msg_lower:
            if default_type == VoiceErrorType.LLM_SERVICE_ERROR:
                return VoiceErrorType.LLM_TIMEOUT, ErrorSeverity.MEDIUM, True
            if default_type == VoiceErrorType.STT_SERVICE_ERROR:
                return VoiceErrorType.STT_TIMEOUT, ErrorSeverity.MEDIUM, True
            if default_type == VoiceErrorType.TTS_SERVICE_ERROR:
                return VoiceErrorType.TTS_TIMEOUT, ErrorSeverity.MEDIUM, True

        if "rate limit" in msg_lower or "429" in message:
            return VoiceErrorType.LLM_RATE_LIMIT, ErrorSeverity.MEDIUM, True

        if "overloaded" in msg_lower or "503" in message:
            return VoiceErrorType.MODEL_OVERLOADED, ErrorSeverity.HIGH, True

        if "context" in msg_lower and ("length" in msg_lower or "window" in msg_lower):
            return VoiceErrorType.LLM_CONTEXT_LENGTH, ErrorSeverity.HIGH, False

        return None

    def _infer_source(self, exc_type: str, exc_message: str) -> str:
        """Infer error source from exception type and message."""
        combined = f"{exc_type} {exc_message}".lower()
        if any(kw in combined for kw in ["stt", "transcri", "speech recognition"]):
            return "stt"
        if any(kw in combined for kw in ["tts", "synthes", "speech generation"]):
            return "tts"
        if any(kw in combined for kw in ["llm", "model", "completion", "chat"]):
            return "llm"
        if any(kw in combined for kw in ["vad", "voice activity"]):
            return "vad"
        if any(kw in combined for kw in ["tool", "function call"]):
            return "tool"
        if any(kw in combined for kw in ["connect", "room", "websocket", "network"]):
            return "connection"
        return "agent"

    def _record_and_track(self, error: DetectedVoiceError) -> None:
        """Record error in stats and track frequency."""
        self.stats.record(error)
        type_key = error.error_type.value
        if type_key not in self._error_frequency:
            self._error_frequency[type_key] = []
        self._error_frequency[type_key].append(error.timestamp)

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
