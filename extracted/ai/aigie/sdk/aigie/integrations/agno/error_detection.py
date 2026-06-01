"""
Error Detection and Monitoring for Agno Agents.

Provides comprehensive error detection, classification, and monitoring
for tool executions, multi-agent orchestration, and LLM responses.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Classification of error types."""

    # Transient errors (may succeed on retry)
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    NETWORK = "network"
    CONCURRENCY = "concurrency"
    SERVER_ERROR = "server_error"
    QUOTA_EXCEEDED = "quota_exceeded"

    # Permanent errors (will not succeed on retry)
    VALIDATION = "validation"
    AUTHENTICATION = "auth"
    PERMISSION = "permission"
    NOT_FOUND = "not_found"
    INVALID_INPUT = "invalid_input"
    INVALID_API_KEY = "invalid_api_key"

    # Tool-specific errors
    TOOL_EXECUTION = "tool_execution"
    TOOL_NOT_FOUND = "tool_not_found"
    TOOL_TIMEOUT = "tool_timeout"

    # Model/API errors
    MODEL_ERROR = "model_error"
    API_ERROR = "api_error"
    CONTEXT_LENGTH = "context_length"
    SAFETY_FILTER = "safety_filter"
    CONTENT_BLOCKED = "content_blocked"

    # Agent errors
    AGENT_ERROR = "agent_error"
    AGENT_LOOP = "agent_loop"

    # Unknown
    UNKNOWN = "unknown"


class ErrorSeverity(Enum):
    """Severity levels for errors."""

    LOW = "low"  # Minor issues, no action needed
    MEDIUM = "medium"  # May affect results, worth investigating
    HIGH = "high"  # Significant impact, needs attention
    CRITICAL = "critical"  # Execution failed, immediate action needed


@dataclass
class DetectedError:
    """Represents a detected error with full context."""

    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    source: str  # e.g., "tool:WebSearch", "agent:researcher", "llm"
    is_transient: bool
    raw_error: str | None = None
    status_code: int | None = None
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
            "status_code": self.status_code,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class ErrorStats:
    """Statistics for error monitoring."""

    total_errors: int = 0
    errors_by_type: Dict[str, int] = field(default_factory=dict)
    errors_by_source: Dict[str, int] = field(default_factory=dict)
    errors_by_severity: Dict[str, int] = field(default_factory=dict)
    transient_errors: int = 0
    permanent_errors: int = 0
    recent_errors: List[DetectedError] = field(default_factory=list)

    def record(self, error: DetectedError) -> None:
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
            "error_rate": self.total_errors,  # Can be divided by total operations
        }


# Error pattern matchers
# These patterns are designed to be specific enough to avoid false positives.
# Each pattern should match error messages, not normal content.
ERROR_PATTERNS = [
    # Rate limiting - specific error messages
    (
        r"rate.?limit(?:ed|ing)?|http.?429|too many requests|quota exceeded|throttl(?:ed|ing)",
        ErrorType.RATE_LIMIT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:server|api|service)\s+(?:is\s+)?(?:overloaded|busy)|capacity\s+exceeded",
        ErrorType.RATE_LIMIT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Timeout - specific error messages
    (
        r"(?:request|connection|operation)\s+(?:timed?.?out|timeout)",
        ErrorType.TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"deadline\s+exceeded|read.?timeout|write.?timeout|connect.?timeout",
        ErrorType.TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Network - specific error indicators
    (
        r"connection\s+(?:refused|reset|failed|error)|socket\s+error",
        ErrorType.NETWORK,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:network|dns)\s+(?:error|failure|unreachable)",
        ErrorType.NETWORK,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"ssl.?(?:error|handshake|certificate)|tls.?(?:error|handshake)",
        ErrorType.NETWORK,
        ErrorSeverity.HIGH,
        True,
    ),
    # Concurrency - specific tool error
    (
        r"tool.?use.?concurrency|concurrent.?(?:request|limit)|parallel.?limit",
        ErrorType.CONCURRENCY,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Server errors - HTTP status codes with context
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?(?:500|502|503|504)(?:\s|:|$)",
        ErrorType.SERVER_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"internal\s+server\s+error|server\s+error|service\s+unavailable",
        ErrorType.SERVER_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Authentication - specific error messages
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?401(?:\s|:|$)|unauthorized",
        ErrorType.AUTHENTICATION,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"(?:invalid|expired|missing)\s+(?:api.?key|token|credentials)",
        ErrorType.AUTHENTICATION,
        ErrorSeverity.HIGH,
        False,
    ),
    # Permission - specific error messages
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?403(?:\s|:|$)|forbidden",
        ErrorType.PERMISSION,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"permission\s+denied|access\s+denied|not\s+(?:allowed|authorized)",
        ErrorType.PERMISSION,
        ErrorSeverity.HIGH,
        False,
    ),
    # Not found - specific error messages
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?404(?:\s|:|$)",
        ErrorType.NOT_FOUND,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"(?:resource|file|path)\s+not\s+found|does\s+not\s+exist|no\s+such\s+file",
        ErrorType.NOT_FOUND,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Validation - specific error messages
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?400(?:\s|:|$)|bad\s+request",
        ErrorType.VALIDATION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"(?:invalid|malformed)\s+(?:request|input|parameter|argument)",
        ErrorType.VALIDATION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"missing\s+required\s+(?:field|parameter)|required\s+field\s+missing",
        ErrorType.VALIDATION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Context length - specific model errors
    (
        r"context.?length\s+exceeded|max.?tokens?\s+exceeded|token\s+limit",
        ErrorType.CONTEXT_LENGTH,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"(?:input|prompt|message)\s+too\s+long", ErrorType.CONTEXT_LENGTH, ErrorSeverity.HIGH, False),
    # Model errors - specific model-related errors
    (
        r"model\s+(?:error|failed|unavailable|not\s+found)",
        ErrorType.MODEL_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    # Quota exceeded
    (r"resource.?exhausted|resourceexhausted", ErrorType.QUOTA_EXCEEDED, ErrorSeverity.HIGH, True),
    (r"quota.*exceeded|exceeded.*quota", ErrorType.QUOTA_EXCEEDED, ErrorSeverity.HIGH, False),
    # Safety / Content filtering
    (
        r"safety.?(?:filter|block|rating)|content.?blocked",
        ErrorType.SAFETY_FILTER,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"harmful.?content|blocked.?(?:due|by).?safety",
        ErrorType.SAFETY_FILTER,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"finish.?reason.*safety|safety.*finish.?reason",
        ErrorType.SAFETY_FILTER,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"blocked_reason|candidatesblockedreason",
        ErrorType.CONTENT_BLOCKED,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Agent errors
    (r"agent\s+(?:error|failed|exception)", ErrorType.AGENT_ERROR, ErrorSeverity.HIGH, False),
    (
        r"(?:infinite|endless)\s+loop|loop\s+detected",
        ErrorType.AGENT_LOOP,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"max.?(?:iterations?|turns?|steps?)\s+(?:reached|exceeded)",
        ErrorType.AGENT_LOOP,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Tool errors - specific tool execution errors
    (
        r"tool\s+(?:execution|call)\s+(?:error|failed)",
        ErrorType.TOOL_EXECUTION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"command\s+(?:execution\s+)?failed|execution\s+error",
        ErrorType.TOOL_EXECUTION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"(?:unknown|unsupported|invalid)\s+tool",
        ErrorType.TOOL_NOT_FOUND,
        ErrorSeverity.HIGH,
        False,
    ),
    # Python exceptions - common runtime errors
    (
        r"name\s+['\"]?\w+['\"]?\s+is\s+not\s+defined",
        ErrorType.TOOL_EXECUTION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"(?:NameError|TypeError|ValueError|KeyError|IndexError|AttributeError):\s*",
        ErrorType.TOOL_EXECUTION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"SyntaxError:\s*", ErrorType.VALIDATION, ErrorSeverity.MEDIUM, False),
    (r"ImportError|ModuleNotFoundError", ErrorType.TOOL_EXECUTION, ErrorSeverity.MEDIUM, False),
    (r"\[EXIT\s*CODE\]:\s*[1-9]\d*", ErrorType.TOOL_EXECUTION, ErrorSeverity.MEDIUM, False),
    # API errors - generic API failure patterns
    (r"api\s+(?:error|failure|unavailable)", ErrorType.API_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"api\s+call\s+failed|api\s+request\s+failed",
        ErrorType.API_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"failed\s+to\s+(?:fetch|get|retrieve|connect)",
        ErrorType.NETWORK,
        ErrorSeverity.MEDIUM,
        True,
    ),
]


class ErrorDetector:
    """
    Detects and classifies errors from tool results, messages, and API responses.

    Provides:
    - Pattern-based error detection
    - Error classification (type, severity, transient/permanent)
    - Error statistics and monitoring
    - Rich error metadata for debugging
    """

    def __init__(self):
        self.stats = ErrorStats()
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), error_type, severity, is_transient)
            for pattern, error_type, severity, is_transient in ERROR_PATTERNS
        ]

    def detect_from_text(
        self,
        text: str,
        source: str,
        context: Dict[str, Any] | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from text content (tool results, error messages, etc.).

        Args:
            text: Text to analyze for errors
            source: Source identifier (e.g., "tool:WebSearch")
            context: Additional context for the error

        Returns:
            DetectedError if an error is found, None otherwise
        """
        if not text:
            return None

        text_lower = text.lower()

        # Check for explicit error indicators
        is_error_indicator = any(
            indicator in text_lower
            for indicator in [
                "error",
                "failed",
                "failure",
                "exception",
                "traceback",
                "api error",
                "request failed",
            ]
        )

        # Try to match error patterns
        for pattern, error_type, severity, is_transient in self._compiled_patterns:
            if pattern.search(text):
                error = DetectedError(
                    error_type=error_type,
                    severity=severity,
                    message=self._extract_error_message(text),
                    source=source,
                    is_transient=is_transient,
                    raw_error=text[:500] if len(text) > 500 else text,
                    status_code=self._extract_status_code(text),
                    metadata=context or {},
                )
                self.stats.record(error)
                logger.warning(
                    f"[AIGIE] Error detected: {error_type.value} from {source}: {error.message[:100]}"
                )
                return error

        # If we see error indicators but no specific pattern, classify as unknown
        if is_error_indicator:
            error = DetectedError(
                error_type=ErrorType.UNKNOWN,
                severity=ErrorSeverity.MEDIUM,
                message=self._extract_error_message(text),
                source=source,
                is_transient=False,
                raw_error=text[:500] if len(text) > 500 else text,
                metadata=context or {},
            )
            self.stats.record(error)
            logger.debug(f"[AIGIE] Potential error detected from {source}: {error.message[:100]}")
            return error

        return None

    def detect_from_tool_result(
        self,
        tool_name: str,
        tool_use_id: str,
        result: Any,
        is_error_flag: bool = False,
        duration_ms: float | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from tool execution results.

        Args:
            tool_name: Name of the tool
            tool_use_id: Unique ID for the tool use
            result: Tool execution result
            is_error_flag: Whether the tool reported an error
            duration_ms: Execution duration in milliseconds

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"tool:{tool_name}"
        context = {
            "tool_name": tool_name,
            "tool_use_id": tool_use_id,
            "duration_ms": duration_ms,
        }

        # If explicitly marked as error
        if is_error_flag:
            result_text = str(result) if result else "Unknown error"
            error = self.detect_from_text(result_text, source, context)
            if error:
                return error

            # Create a generic tool error
            error = DetectedError(
                error_type=ErrorType.TOOL_EXECUTION,
                severity=ErrorSeverity.MEDIUM,
                message=f"Tool {tool_name} failed: {result_text[:200]}",
                source=source,
                is_transient=False,
                raw_error=result_text[:500],
                metadata=context,
            )
            self.stats.record(error)
            return error

        # Only check result content for error patterns if it looks like an error
        result_text = str(result) if result else ""
        if result_text:
            text_lower = result_text[:200].lower()
            if any(
                indicator in text_lower
                for indicator in [
                    "error",
                    "failed",
                    "exception",
                    "traceback",
                    "fatal",
                    "status: 4",
                    "status: 5",
                    "http 4",
                    "http 5",
                ]
            ):
                return self.detect_from_text(result_text, source, context)

        return None

    def detect_from_exception(
        self,
        exception: Exception,
        source: str,
        context: Dict[str, Any] | None = None,
    ) -> DetectedError:
        """
        Create DetectedError from a Python exception.

        Args:
            exception: The exception that occurred
            source: Source identifier
            context: Additional context

        Returns:
            DetectedError for the exception
        """
        exc_type = type(exception).__name__
        exc_message = str(exception)

        # Try to classify the exception
        error = self.detect_from_text(exc_message, source, context)
        if error:
            error.metadata["exception_type"] = exc_type
            return error

        # Default classification based on exception type
        error_type = ErrorType.UNKNOWN
        severity = ErrorSeverity.HIGH
        is_transient = False

        if "timeout" in exc_type.lower() or "timeout" in exc_message.lower():
            error_type = ErrorType.TIMEOUT
            is_transient = True
        elif "connection" in exc_type.lower() or "network" in exc_message.lower():
            error_type = ErrorType.NETWORK
            is_transient = True
        elif "permission" in exc_type.lower() or "auth" in exc_type.lower():
            error_type = ErrorType.PERMISSION
        elif "validation" in exc_type.lower() or "value" in exc_type.lower():
            error_type = ErrorType.VALIDATION

        error = DetectedError(
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
            r"exception[:\s]+(.+?)(?:\.|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                msg = match.group(1).strip()
                if len(msg) > 10:
                    return msg[:200]

        first_line = text.split("\n")[0].strip()
        return first_line[:200] if first_line else text[:200]

    def _extract_status_code(self, text: str) -> int | None:
        """Extract HTTP status code from text."""
        patterns = [
            r"status[:\s]*(\d{3})",
            r"(\d{3})\s+(?:error|ok|created|accepted)",
            r"http[:\s]*(\d{3})",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    pass

        for code in [400, 401, 403, 404, 429, 500, 502, 503, 504]:
            if str(code) in text:
                return code

        return None

    def get_stats(self) -> Dict[str, Any]:
        """Get current error statistics."""
        return self.stats.to_dict()

    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent errors as dictionaries."""
        return [e.to_dict() for e in self.stats.recent_errors[-limit:]]

    def has_critical_errors(self) -> bool:
        """Check if there are any critical errors."""
        return self.stats.errors_by_severity.get("critical", 0) > 0

    def get_error_summary(self) -> str:
        """Get a human-readable error summary."""
        if self.stats.total_errors == 0:
            return "No errors detected"

        summary = f"Total errors: {self.stats.total_errors}"
        summary += (
            f" (transient: {self.stats.transient_errors}, permanent: {self.stats.permanent_errors})"
        )

        if self.stats.errors_by_type:
            top_types = sorted(self.stats.errors_by_type.items(), key=lambda x: x[1], reverse=True)[
                :3
            ]
            summary += f"\nTop error types: {', '.join(f'{t}({c})' for t, c in top_types)}"

        return summary


# Global error detector instance for easy access
_global_detector: ErrorDetector | None = None


def get_error_detector() -> ErrorDetector:
    """Get or create the global error detector instance."""
    global _global_detector
    if _global_detector is None:
        _global_detector = ErrorDetector()
    return _global_detector


def reset_error_detector() -> None:
    """Reset the global error detector (for testing)."""
    global _global_detector
    _global_detector = None
