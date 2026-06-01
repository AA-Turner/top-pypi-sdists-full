"""Typed error model used by the Strands ErrorDetector."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


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
    source: str  # e.g., "tool:WebSearch", "subagent:researcher", "llm"
    is_transient: bool
    raw_error: str | None = None
    status_code: int | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
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
    errors_by_type: dict[str, int] = field(default_factory=dict)
    errors_by_source: dict[str, int] = field(default_factory=dict)
    errors_by_severity: dict[str, int] = field(default_factory=dict)
    transient_errors: int = 0
    permanent_errors: int = 0
    recent_errors: list[DetectedError] = field(default_factory=list)

    def record(self, error: DetectedError) -> None:
        """Record an error in statistics."""
        self.total_errors += 1
        type_key = error.error_type.value
        self.errors_by_type[type_key] = self.errors_by_type.get(type_key, 0) + 1
        self.errors_by_source[error.source] = self.errors_by_source.get(error.source, 0) + 1
        sev_key = error.severity.value
        self.errors_by_severity[sev_key] = self.errors_by_severity.get(sev_key, 0) + 1
        if error.is_transient:
            self.transient_errors += 1
        else:
            self.permanent_errors += 1
        # Keep last 100 errors
        self.recent_errors.append(error)
        if len(self.recent_errors) > 100:
            self.recent_errors = self.recent_errors[-100:]

    def to_dict(self) -> dict[str, Any]:
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
