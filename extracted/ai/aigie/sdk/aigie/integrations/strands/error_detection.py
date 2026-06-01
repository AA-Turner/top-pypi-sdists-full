"""
Error Detection and Monitoring for Strands Agents.

Provides comprehensive error detection, classification, and monitoring
for tool executions, multi-agent orchestration, and LLM responses.
"""

import logging
import re
from typing import Any

from .error_patterns import ERROR_PATTERNS
from .error_types import DetectedError, ErrorSeverity, ErrorStats, ErrorType

__all__ = [
    "DetectedError",
    "ErrorDetector",
    "ErrorSeverity",
    "ErrorStats",
    "ErrorType",
    "get_error_detector",
    "reset_error_detector",
]

logger = logging.getLogger(__name__)


def _classify_exception_type(exc_type: str, exc_message: str) -> tuple[ErrorType, bool]:
    """Map a Python exception class name + message to (error_type, is_transient)."""
    exc_type_lower = exc_type.lower()
    exc_message_lower = exc_message.lower()
    if "timeout" in exc_type_lower or "timeout" in exc_message_lower:
        return ErrorType.TIMEOUT, True
    if "connection" in exc_type_lower or "network" in exc_message_lower:
        return ErrorType.NETWORK, True
    if "permission" in exc_type_lower or "auth" in exc_type_lower:
        return ErrorType.PERMISSION, False
    if "validation" in exc_type_lower or "value" in exc_type_lower:
        return ErrorType.VALIDATION, False
    return ErrorType.UNKNOWN, False


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
        self.stats: ErrorStats = ErrorStats()
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), error_type, severity, is_transient)
            for pattern, error_type, severity, is_transient in ERROR_PATTERNS
        ]

    def detect_from_text(
        self,
        text: str,
        source: str,
        context: dict[str, Any] | None = None,
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
        # (has explicit error indicators in the first part of the text)
        result_text = str(result) if result else ""
        if result_text:
            # Only scan for errors if the result starts with or contains error indicators
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

    def detect_from_subagent_result(
        self,
        subagent_type: str,
        tool_use_id: str,
        result: Any,
        is_error_flag: bool = False,
        duration_ms: float | None = None,
        tool_count: int = 0,
    ) -> DetectedError | None:
        """
        Detect errors from subagent execution results.

        Args:
            subagent_type: Type of subagent
            tool_use_id: Unique ID for the subagent task
            result: Subagent execution result
            is_error_flag: Whether the subagent reported an error
            duration_ms: Execution duration in milliseconds
            tool_count: Number of tools used by the subagent

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"subagent:{subagent_type}"
        context = {
            "subagent_type": subagent_type,
            "tool_use_id": tool_use_id,
            "duration_ms": duration_ms,
            "tool_count": tool_count,
        }

        result_text = str(result) if result else ""

        # Check for API errors in subagent results
        if is_error_flag or "api error" in result_text.lower():
            error = self.detect_from_text(result_text, source, context)
            if error:
                # Elevate severity for subagent errors
                if error.severity == ErrorSeverity.LOW:
                    error.severity = ErrorSeverity.MEDIUM
                return error

            # Create a generic subagent error
            error = DetectedError(
                error_type=ErrorType.API_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Subagent {subagent_type} failed: {result_text[:200]}",
                source=source,
                is_transient=True,  # Subagent errors are often transient
                raw_error=result_text[:500],
                metadata=context,
            )
            self.stats.record(error)
            return error

        return self.detect_from_text(result_text, source, context)

    def detect_from_llm_response(
        self,
        message: Any,
        model: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from LLM responses.

        Args:
            message: AssistantMessage or similar
            model: Model name

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"llm:{model or 'unknown'}"

        # Check for error attribute. We do pattern matching inline (rather than
        # delegating to detect_from_text) because that helper records an UNKNOWN
        # entry on the substring "error", which would double-count once we fall
        # through to the MODEL_ERROR fallback.
        error_obj = getattr(message, "error", None)
        if error_obj:
            return self._classify_llm_error_obj(str(error_obj), source, model)

        # Check message content for error patterns
        content = getattr(message, "content", None)
        if content:
            if isinstance(content, str):
                return self.detect_from_text(content, source, {"model": model})
            if isinstance(content, list):
                for block in content:
                    if hasattr(block, "text"):
                        error = self.detect_from_text(block.text, source, {"model": model})
                        if error:
                            return error

        return None

    def detect_from_exception(
        self,
        exception: Exception,
        source: str,
        context: dict[str, Any] | None = None,
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

        error_type, is_transient = _classify_exception_type(exc_type, exc_message)
        error = DetectedError(
            error_type=error_type,
            severity=ErrorSeverity.HIGH,
            message=f"{exc_type}: {exc_message[:200]}",
            source=source,
            is_transient=is_transient,
            raw_error=f"{exc_type}: {exc_message}",
            metadata={**(context or {}), "exception_type": exc_type},
        )
        self.stats.record(error)
        return error

    def _classify_llm_error_obj(
        self, error_text: str, source: str, model: str | None
    ) -> DetectedError:
        """Classify a non-empty LLM .error string, recording exactly one stat entry."""
        for pattern, error_type, severity, is_transient in self._compiled_patterns:
            if pattern.search(error_text):
                error = DetectedError(
                    error_type=error_type,
                    severity=severity,
                    message=self._extract_error_message(error_text),
                    source=source,
                    is_transient=is_transient,
                    raw_error=error_text[:500],
                    status_code=self._extract_status_code(error_text),
                    metadata={"model": model},
                )
                self.stats.record(error)
                return error
        error = DetectedError(
            error_type=ErrorType.MODEL_ERROR,
            severity=ErrorSeverity.HIGH,
            message=f"Model error: {error_text[:200]}",
            source=source,
            is_transient=True,
            raw_error=error_text[:500],
            metadata={"model": model},
        )
        self.stats.record(error)
        return error

    def _extract_error_message(self, text: str) -> str:
        """Extract a clean error message from text."""
        # Try to find a specific error message
        patterns = [
            r"error[:\s]+(.+?)(?:\.|$)",
            r"failed[:\s]+(.+?)(?:\.|$)",
            r"exception[:\s]+(.+?)(?:\.|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                msg = match.group(1).strip()
                if len(msg) > 10:  # Sanity check
                    return msg[:200]

        # Return first line or first 200 chars
        first_line = text.split("\n")[0].strip()
        return first_line[:200] if first_line else text[:200]

    def _extract_status_code(self, text: str) -> int | None:
        """Extract HTTP status code from text."""
        # Look for common status code patterns
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

        # Check for inline status codes
        for code in [400, 401, 403, 404, 429, 500, 502, 503, 504]:
            if str(code) in text:
                return code

        return None

    def get_stats(self) -> dict[str, Any]:
        """Get current error statistics."""
        return self.stats.to_dict()

    def get_recent_errors(self, limit: int = 10) -> list[dict[str, Any]]:
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
