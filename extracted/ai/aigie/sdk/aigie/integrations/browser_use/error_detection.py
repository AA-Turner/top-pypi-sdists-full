"""
Error Detection and Monitoring for Browser Use Workflows.

Provides comprehensive error detection, classification, and monitoring
for browser actions, navigation, and element interactions.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Classification of error types for browser automation."""

    # Transient errors (may succeed on retry)
    TIMEOUT = "timeout"
    NETWORK = "network"
    RATE_LIMIT = "rate_limit"
    SERVER_ERROR = "server_error"
    PAGE_LOAD = "page_load"

    # Navigation errors
    NAVIGATION_ERROR = "navigation"
    URL_ERROR = "url_error"
    REDIRECT_ERROR = "redirect"
    PAGE_NOT_FOUND = "page_not_found"

    # Element errors
    ELEMENT_NOT_FOUND = "element_not_found"
    ELEMENT_STALE = "element_stale"
    ELEMENT_NOT_INTERACTABLE = "element_not_interactable"
    ELEMENT_HIDDEN = "element_hidden"

    # Interaction errors
    CLICK_ERROR = "click_error"
    TYPE_ERROR = "type_error"
    SCROLL_ERROR = "scroll_error"
    HOVER_ERROR = "hover_error"
    SELECT_ERROR = "select_error"

    # Screenshot/DOM errors
    SCREENSHOT_ERROR = "screenshot"
    DOM_ERROR = "dom_error"

    # JavaScript errors
    JS_ERROR = "js_error"
    JS_TIMEOUT = "js_timeout"

    # Browser errors
    BROWSER_CRASH = "browser_crash"
    CONTEXT_ERROR = "context_error"
    PAGE_CRASH = "page_crash"

    # Authentication/permission
    AUTHENTICATION = "auth"
    PERMISSION = "permission"
    CAPTCHA = "captcha"

    # LLM/Agent errors
    LLM_ERROR = "llm_error"
    AGENT_ERROR = "agent_error"
    TOOL_EXECUTION = "tool_execution"

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
    source: str  # e.g., "action:click", "navigation:goto", "element:selector"
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
            "error_rate": self.total_errors,
        }


# Error pattern matchers for browser automation
ERROR_PATTERNS = [
    # Timeout errors
    (
        r"(?:request|page|navigation|element|action)\s+(?:timed?.?out|timeout)",
        ErrorType.TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"waiting\s+for\s+(?:element|selector|page)\s+timed\s+out",
        ErrorType.TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Navigation errors
    (
        r"navigation\s+(?:failed|error)|failed\s+to\s+navigate",
        ErrorType.NAVIGATION_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (r"net::ERR_|ERR_NAME|ERR_CONNECTION|ERR_CERT", ErrorType.NETWORK, ErrorSeverity.MEDIUM, True),
    (
        r"(?:page|url)\s+not\s+found|404\s+not\s+found",
        ErrorType.PAGE_NOT_FOUND,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"invalid\s+url|malformed\s+url", ErrorType.URL_ERROR, ErrorSeverity.MEDIUM, False),
    (
        r"too\s+many\s+redirects|redirect\s+loop",
        ErrorType.REDIRECT_ERROR,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Element errors
    (
        r"(?:element|selector)\s+not\s+found|no\s+(?:element|node)\s+found",
        ErrorType.ELEMENT_NOT_FOUND,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"stale\s+element|element\s+is\s+stale|detached\s+from\s+dom",
        ErrorType.ELEMENT_STALE,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"element\s+(?:not\s+)?interactable|cannot\s+interact",
        ErrorType.ELEMENT_NOT_INTERACTABLE,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"element\s+(?:is\s+)?hidden|not\s+visible|visibility.*hidden",
        ErrorType.ELEMENT_HIDDEN,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Interaction errors
    (
        r"click\s+(?:failed|error)|failed\s+to\s+click",
        ErrorType.CLICK_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"type\s+(?:failed|error)|failed\s+to\s+type|input\s+error",
        ErrorType.TYPE_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"scroll\s+(?:failed|error)|failed\s+to\s+scroll",
        ErrorType.SCROLL_ERROR,
        ErrorSeverity.LOW,
        True,
    ),
    # JavaScript errors
    (
        r"javascript\s+(?:error|exception)|script\s+error",
        ErrorType.JS_ERROR,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"script\s+timed?\s*out", ErrorType.JS_TIMEOUT, ErrorSeverity.MEDIUM, True),
    # Browser/page errors
    (
        r"browser\s+(?:crashed|disconnected)|target\s+closed",
        ErrorType.BROWSER_CRASH,
        ErrorSeverity.CRITICAL,
        True,
    ),
    (r"page\s+(?:crashed|closed|destroyed)", ErrorType.PAGE_CRASH, ErrorSeverity.HIGH, True),
    (r"context\s+(?:closed|destroyed)", ErrorType.CONTEXT_ERROR, ErrorSeverity.HIGH, True),
    # Screenshot/DOM errors
    (r"screenshot\s+(?:failed|error)", ErrorType.SCREENSHOT_ERROR, ErrorSeverity.LOW, True),
    (r"(?:dom|document)\s+(?:error|not\s+ready)", ErrorType.DOM_ERROR, ErrorSeverity.MEDIUM, True),
    # Authentication/permission
    (r"(?:401|unauthorized|not\s+authorized)", ErrorType.AUTHENTICATION, ErrorSeverity.HIGH, False),
    (r"(?:403|forbidden|access\s+denied)", ErrorType.PERMISSION, ErrorSeverity.HIGH, False),
    (r"captcha|recaptcha|human\s+verification", ErrorType.CAPTCHA, ErrorSeverity.HIGH, False),
    # Rate limiting
    (r"rate.?limit|too\s+many\s+requests|429", ErrorType.RATE_LIMIT, ErrorSeverity.MEDIUM, True),
    # LLM errors
    (r"llm\s+(?:error|failed)|model\s+error", ErrorType.LLM_ERROR, ErrorSeverity.HIGH, True),
    (
        r"agent\s+(?:error|failed)|execution\s+error",
        ErrorType.AGENT_ERROR,
        ErrorSeverity.HIGH,
        False,
    ),
    # Server errors
    (
        r"(?:500|502|503|504)\s*(?:error)?|server\s+error",
        ErrorType.SERVER_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
]


class ErrorDetector:
    """
    Detects and classifies errors from browser automation results.

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
        Detect errors from text content.

        Args:
            text: Text to analyze for errors
            source: Source identifier (e.g., "action:click")
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
                "timeout",
                "not found",
                "could not",
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
                    f"[AIGIE] Browser error detected: {error_type.value} from {source}: {error.message[:100]}"
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
            logger.warning(
                f"[AIGIE] Unknown browser error detected from {source}: {error.message[:100]}"
            )
            return error

        return None

    def detect_from_action_result(
        self,
        action_type: str,
        action_id: str,
        result: Any,
        is_error_flag: bool = False,
        duration_ms: float | None = None,
        selector: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from browser action results.

        Args:
            action_type: Type of action (click, type, navigate, etc.)
            action_id: Unique ID for the action
            result: Action result
            is_error_flag: Whether the action reported an error
            duration_ms: Execution duration in milliseconds
            selector: CSS selector used (if any)

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"action:{action_type}"
        context = {
            "action_type": action_type,
            "action_id": action_id,
            "duration_ms": duration_ms,
            "selector": selector,
        }

        if is_error_flag:
            result_text = str(result) if result else "Unknown error"
            error = self.detect_from_text(result_text, source, context)
            if error:
                return error

            # Map action type to appropriate error
            error_type_map = {
                "click": ErrorType.CLICK_ERROR,
                "type": ErrorType.TYPE_ERROR,
                "scroll": ErrorType.SCROLL_ERROR,
                "hover": ErrorType.HOVER_ERROR,
                "select": ErrorType.SELECT_ERROR,
                "navigate": ErrorType.NAVIGATION_ERROR,
                "goto": ErrorType.NAVIGATION_ERROR,
                "screenshot": ErrorType.SCREENSHOT_ERROR,
            }
            error_type = error_type_map.get(action_type.lower(), ErrorType.TOOL_EXECUTION)

            error = DetectedError(
                error_type=error_type,
                severity=ErrorSeverity.MEDIUM,
                message=f"Action {action_type} failed: {result_text[:200]}",
                source=source,
                is_transient=True,
                raw_error=result_text[:500],
                metadata=context,
            )
            self.stats.record(error)
            return error

        # Check result content for error patterns
        result_text = str(result) if result else ""
        if result_text:
            return self.detect_from_text(result_text, source, context)

        return None

    def detect_from_step_result(
        self,
        step_number: int,
        result: Any,
        is_error_flag: bool = False,
        duration_ms: float | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from agent step results.

        Args:
            step_number: The step number
            result: Step result
            is_error_flag: Whether the step reported an error
            duration_ms: Execution duration in milliseconds

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"step:{step_number}"
        context = {
            "step_number": step_number,
            "duration_ms": duration_ms,
        }

        if is_error_flag:
            result_text = str(result) if result else "Unknown error"
            error = self.detect_from_text(result_text, source, context)
            if error:
                return error

            error = DetectedError(
                error_type=ErrorType.AGENT_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Step {step_number} failed: {result_text[:200]}",
                source=source,
                is_transient=False,
                raw_error=result_text[:500],
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

        # Try to classify the exception
        error = self.detect_from_text(exc_message, source, context)
        if error:
            error.metadata["exception_type"] = exc_type
            return error

        # Default classification based on exception type name
        error_type = ErrorType.UNKNOWN
        severity = ErrorSeverity.HIGH
        is_transient = False

        exc_type_lower = exc_type.lower()
        if "timeout" in exc_type_lower:
            error_type = ErrorType.TIMEOUT
            is_transient = True
        elif "element" in exc_type_lower:
            error_type = ErrorType.ELEMENT_NOT_FOUND
            is_transient = True
        elif "navigation" in exc_type_lower:
            error_type = ErrorType.NAVIGATION_ERROR
            is_transient = True
        elif "browser" in exc_type_lower:
            error_type = ErrorType.BROWSER_CRASH
            severity = ErrorSeverity.CRITICAL
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
