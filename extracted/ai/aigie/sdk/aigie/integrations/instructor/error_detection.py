"""
Error Detection and Monitoring for Instructor Structured Outputs.

Provides comprehensive error detection, classification, and monitoring
for structured output extraction, validation, and retries.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Classification of error types for Instructor."""

    # Transient errors (may succeed on retry)
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    NETWORK = "network"
    SERVER_ERROR = "server_error"

    # Validation errors
    VALIDATION_ERROR = "validation_error"
    TYPE_ERROR = "type_error"
    FIELD_MISSING = "field_missing"
    FIELD_INVALID = "field_invalid"
    CONSTRAINT_VIOLATION = "constraint_violation"
    SCHEMA_ERROR = "schema_error"

    # Parsing errors
    JSON_PARSE_ERROR = "json_parse"
    EXTRACTION_ERROR = "extraction"
    FORMAT_ERROR = "format_error"

    # Model errors
    MODEL_ERROR = "model_error"
    CONTENT_FILTER = "content_filter"
    CONTEXT_LENGTH = "context_length"
    MAX_RETRIES = "max_retries"

    # Authentication
    AUTHENTICATION = "auth"
    PERMISSION = "permission"

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
    source: str  # e.g., "validation:User", "extraction:response"
    is_transient: bool
    raw_error: str | None = None
    validation_errors: List[Dict[str, Any]] | None = None
    retry_count: int = 0
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
            "validation_errors": self.validation_errors,
            "retry_count": self.retry_count,
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
    validation_errors: int = 0
    total_retries: int = 0
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

        # Track validation errors specifically
        if error.error_type == ErrorType.VALIDATION_ERROR:
            self.validation_errors += 1

        # Track retries
        self.total_retries += error.retry_count

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
            "validation_errors": self.validation_errors,
            "total_retries": self.total_retries,
        }


# Error pattern matchers for Instructor
ERROR_PATTERNS = [
    # Validation errors (Pydantic)
    (
        r"validation\s+error|pydantic.*validation",
        ErrorType.VALIDATION_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"field\s+required|missing\s+(?:required\s+)?field",
        ErrorType.FIELD_MISSING,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"value\s+(?:is\s+)?not\s+(?:a\s+)?valid",
        ErrorType.FIELD_INVALID,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"type\s+error|expected\s+(?:type|str|int|float|bool|list|dict)",
        ErrorType.TYPE_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"constraint\s+(?:failed|violated)|assertion\s+error",
        ErrorType.CONSTRAINT_VIOLATION,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # JSON/Parsing errors
    (
        r"json\.?decode\s*error|invalid\s+json|malformed\s+json",
        ErrorType.JSON_PARSE_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:could\s+not|failed\s+to)\s+(?:parse|extract)",
        ErrorType.EXTRACTION_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"unexpected\s+(?:format|token)|format\s+error",
        ErrorType.FORMAT_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Rate limiting
    (r"rate.?limit|too\s+many\s+requests|429", ErrorType.RATE_LIMIT, ErrorSeverity.MEDIUM, True),
    # Timeout
    (
        r"(?:request|connection|operation)\s+(?:timed?.?out|timeout)",
        ErrorType.TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Network
    (
        r"connection\s+(?:refused|reset|failed)|network\s+error",
        ErrorType.NETWORK,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Server errors
    (
        r"(?:500|502|503|504)(?:\s|:|$)|server\s+error",
        ErrorType.SERVER_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Authentication
    (
        r"(?:401|unauthorized)|invalid\s+(?:api.?key|token)",
        ErrorType.AUTHENTICATION,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"(?:403|forbidden)", ErrorType.PERMISSION, ErrorSeverity.HIGH, False),
    # Content filter
    (
        r"content\s+filter|content\s+policy|moderation",
        ErrorType.CONTENT_FILTER,
        ErrorSeverity.HIGH,
        False,
    ),
    # Context length
    (
        r"context.?length|max.?tokens?\s+exceeded|token\s+limit",
        ErrorType.CONTEXT_LENGTH,
        ErrorSeverity.HIGH,
        False,
    ),
    # Max retries
    (
        r"max(?:imum)?\s+retries?\s+(?:exceeded|reached)",
        ErrorType.MAX_RETRIES,
        ErrorSeverity.HIGH,
        False,
    ),
    # Model errors
    (r"model\s+(?:error|unavailable|not\s+found)", ErrorType.MODEL_ERROR, ErrorSeverity.HIGH, True),
]


class ErrorDetector:
    """
    Detects and classifies errors from Instructor structured output operations.

    Provides:
    - Pattern-based error detection
    - Pydantic validation error parsing
    - Error classification (type, severity, transient/permanent)
    - Error statistics and monitoring
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
        Detect errors from text content.

        Args:
            text: Text to analyze for errors
            source: Source identifier (e.g., "validation:User")
            context: Additional context for the error

        Returns:
            DetectedError if an error is found, None otherwise
        """
        if not text:
            return None

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
                    metadata=context or {},
                )
                self.stats.record(error)
                logger.warning(
                    f"[AIGIE] Instructor error detected: {error_type.value} from {source}"
                )
                return error

        return None

    def detect_from_validation_error(
        self,
        validation_error: Any,
        model_name: str,
        retry_count: int = 0,
    ) -> DetectedError:
        """
        Detect errors from a Pydantic validation error.

        Args:
            validation_error: Pydantic ValidationError
            model_name: Name of the Pydantic model
            retry_count: Current retry count

        Returns:
            DetectedError with parsed validation details
        """
        source = f"validation:{model_name}"

        # Parse validation errors
        validation_errors = []
        try:
            if hasattr(validation_error, "errors"):
                errors = validation_error.errors()
                for err in errors:
                    validation_errors.append(
                        {
                            "loc": err.get("loc", []),
                            "msg": err.get("msg", ""),
                            "type": err.get("type", ""),
                        }
                    )
        except Exception:
            pass

        error = DetectedError(
            error_type=ErrorType.VALIDATION_ERROR,
            severity=ErrorSeverity.MEDIUM,
            message=f"Validation failed for {model_name}: {str(validation_error)[:200]}",
            source=source,
            is_transient=True,  # Validation errors can be fixed by retry with better prompting
            raw_error=str(validation_error)[:500],
            validation_errors=validation_errors,
            retry_count=retry_count,
            metadata={
                "model_name": model_name,
                "error_count": len(validation_errors),
            },
        )
        self.stats.record(error)
        logger.warning(
            f"[AIGIE] Validation error for {model_name}: {len(validation_errors)} errors"
        )
        return error

    def detect_from_extraction_result(
        self,
        model_name: str,
        result: Any,
        is_error_flag: bool = False,
        retry_count: int = 0,
    ) -> DetectedError | None:
        """
        Detect errors from extraction results.

        Args:
            model_name: Pydantic model name
            result: Extraction result
            is_error_flag: Whether extraction reported an error
            retry_count: Current retry count

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"extraction:{model_name}"
        context = {
            "model_name": model_name,
            "retry_count": retry_count,
        }

        if is_error_flag:
            result_text = str(result) if result else "Unknown error"
            error = self.detect_from_text(result_text, source, context)
            if error:
                error.retry_count = retry_count
                return error

            # Create generic extraction error
            error = DetectedError(
                error_type=ErrorType.EXTRACTION_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Failed to extract {model_name}: {result_text[:200]}",
                source=source,
                is_transient=True,
                raw_error=result_text[:500],
                retry_count=retry_count,
                metadata=context,
            )
            self.stats.record(error)
            return error

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

        # Check if it's a Pydantic ValidationError
        if "ValidationError" in exc_type:
            model_name = context.get("model_name", "unknown") if context else "unknown"
            return self.detect_from_validation_error(exception, model_name)

        # Try to classify the exception
        error = self.detect_from_text(exc_message, source, context)
        if error:
            error.metadata["exception_type"] = exc_type
            return error

        # Default classification
        error_type = ErrorType.UNKNOWN
        severity = ErrorSeverity.HIGH
        is_transient = False

        exc_type_lower = exc_type.lower()
        if "validation" in exc_type_lower:
            error_type = ErrorType.VALIDATION_ERROR
            is_transient = True
        elif "timeout" in exc_type_lower:
            error_type = ErrorType.TIMEOUT
            is_transient = True
        elif "json" in exc_type_lower:
            error_type = ErrorType.JSON_PARSE_ERROR
            is_transient = True

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
            r"validation\s+error[:\s]+(.+?)(?:\.|$)",
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

    def get_validation_error_rate(self) -> float:
        """Get the rate of validation errors."""
        if self.stats.total_errors == 0:
            return 0.0
        return self.stats.validation_errors / self.stats.total_errors

    def get_error_summary(self) -> str:
        """Get a human-readable error summary."""
        if self.stats.total_errors == 0:
            return "No errors detected"

        summary = f"Total errors: {self.stats.total_errors}"
        summary += (
            f" (validation: {self.stats.validation_errors}, retries: {self.stats.total_retries})"
        )

        if self.stats.errors_by_type:
            top_types = sorted(self.stats.errors_by_type.items(), key=lambda x: x[1], reverse=True)[
                :3
            ]
            summary += f"\nTop error types: {', '.join(f'{t}({c})' for t, c in top_types)}"

        return summary


# Global error detector instance
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
