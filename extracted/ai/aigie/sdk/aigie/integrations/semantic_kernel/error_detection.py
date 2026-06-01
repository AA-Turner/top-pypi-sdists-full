"""
Error Detection and Monitoring for Semantic Kernel.

Provides comprehensive error detection, classification, and monitoring
for Semantic Kernel function invocations, planners, and plugin executions.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Classification of error types for Semantic Kernel."""

    # Function/Plugin errors
    FUNCTION_NOT_FOUND = "function_not_found"
    PLUGIN_NOT_FOUND = "plugin_not_found"
    FUNCTION_INVOCATION_ERROR = "function_invocation_error"
    FUNCTION_RESULT_ERROR = "function_result_error"
    ARGUMENT_ERROR = "argument_error"

    # Planner errors
    PLANNER_ERROR = "planner_error"
    PLAN_CREATION_ERROR = "plan_creation_error"
    PLAN_EXECUTION_ERROR = "plan_execution_error"
    GOAL_NOT_ACHIEVABLE = "goal_not_achievable"
    NO_AVAILABLE_FUNCTIONS = "no_available_functions"

    # Prompt errors
    PROMPT_RENDER_ERROR = "prompt_render_error"
    TEMPLATE_ERROR = "template_error"
    VARIABLE_NOT_FOUND = "variable_not_found"

    # Connector errors
    CONNECTOR_ERROR = "connector_error"
    MODEL_NOT_AVAILABLE = "model_not_available"
    AZURE_ERROR = "azure_error"
    OPENAI_ERROR = "openai_error"

    # Transient errors (may succeed on retry)
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    NETWORK = "network"
    SERVER_ERROR = "server_error"

    # Content errors
    CONTENT_FILTER = "content_filter"
    CONTEXT_LENGTH = "context_length"
    TOKEN_LIMIT = "token_limit"

    # Memory/kernel errors
    MEMORY_ERROR = "memory_error"
    KERNEL_ERROR = "kernel_error"
    SERVICE_NOT_FOUND = "service_not_found"

    # Validation errors
    VALIDATION_ERROR = "validation_error"
    TYPE_ERROR = "type_error"
    SERIALIZATION_ERROR = "serialization_error"

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
    source: str  # e.g., "function:MyPlugin.Search", "planner:Sequential"
    is_transient: bool
    raw_error: str | None = None
    function_name: str | None = None
    plugin_name: str | None = None
    planner_type: str | None = None
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
            "function_name": self.function_name,
            "plugin_name": self.plugin_name,
            "planner_type": self.planner_type,
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
    errors_by_plugin: Dict[str, int] = field(default_factory=dict)
    transient_errors: int = 0
    permanent_errors: int = 0
    planner_errors: int = 0
    function_errors: int = 0
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

        # By plugin
        if error.plugin_name:
            self.errors_by_plugin[error.plugin_name] = (
                self.errors_by_plugin.get(error.plugin_name, 0) + 1
            )

        # Transient vs permanent
        if error.is_transient:
            self.transient_errors += 1
        else:
            self.permanent_errors += 1

        # Track planner vs function errors
        if error.planner_type or "planner" in error.source.lower():
            self.planner_errors += 1
        if error.function_name or "function" in error.source.lower():
            self.function_errors += 1

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
            "errors_by_plugin": self.errors_by_plugin,
            "transient_errors": self.transient_errors,
            "permanent_errors": self.permanent_errors,
            "planner_errors": self.planner_errors,
            "function_errors": self.function_errors,
        }


# Error pattern matchers for Semantic Kernel
ERROR_PATTERNS = [
    # Function/Plugin errors
    (
        r"function\s+(?:not\s+)?found|unknown\s+function",
        ErrorType.FUNCTION_NOT_FOUND,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"plugin\s+(?:not\s+)?found|unknown\s+plugin",
        ErrorType.PLUGIN_NOT_FOUND,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"function\s+invocation\s+(?:failed|error)",
        ErrorType.FUNCTION_INVOCATION_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"function\s+result\s+(?:invalid|error)",
        ErrorType.FUNCTION_RESULT_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:invalid|missing)\s+argument|argument\s+(?:error|required)",
        ErrorType.ARGUMENT_ERROR,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Planner errors
    (
        r"planner\s+(?:failed|error)|planning\s+(?:failed|error)",
        ErrorType.PLANNER_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"(?:could\s+not|failed\s+to)\s+create\s+plan",
        ErrorType.PLAN_CREATION_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"plan\s+execution\s+(?:failed|error)",
        ErrorType.PLAN_EXECUTION_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"goal\s+(?:not\s+achievable|cannot\s+be\s+achieved)",
        ErrorType.GOAL_NOT_ACHIEVABLE,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"no\s+(?:available|suitable)\s+functions",
        ErrorType.NO_AVAILABLE_FUNCTIONS,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Prompt errors
    (
        r"prompt\s+render\s+(?:failed|error)|(?:failed\s+to\s+)?render\s+prompt",
        ErrorType.PROMPT_RENDER_ERROR,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"template\s+(?:error|invalid|not\s+found)",
        ErrorType.TEMPLATE_ERROR,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"variable\s+(?:not\s+found|missing|undefined)",
        ErrorType.VARIABLE_NOT_FOUND,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Connector errors
    (
        r"connector\s+(?:error|failed)|connection\s+(?:error|failed)",
        ErrorType.CONNECTOR_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"model\s+(?:not\s+available|unavailable|not\s+found)",
        ErrorType.MODEL_NOT_AVAILABLE,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"azure\s+(?:error|openai\s+error)|azureopenai",
        ErrorType.AZURE_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (r"openai\s+(?:error|api\s+error)", ErrorType.OPENAI_ERROR, ErrorSeverity.HIGH, True),
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
        r"(?:500|502|503|504)(?:\s|:|$)|server\s+error|internal\s+server",
        ErrorType.SERVER_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Content filter
    (
        r"content\s+filter|content\s+policy|moderation|safety\s+filter",
        ErrorType.CONTENT_FILTER,
        ErrorSeverity.HIGH,
        False,
    ),
    # Context/Token length
    (
        r"context.?length|max.?tokens?\s+exceeded|token\s+limit",
        ErrorType.CONTEXT_LENGTH,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"(?:input|prompt)\s+(?:too\s+)?long|truncat",
        ErrorType.TOKEN_LIMIT,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Memory errors
    (r"memory\s+(?:error|not\s+found|failed)", ErrorType.MEMORY_ERROR, ErrorSeverity.MEDIUM, True),
    # Kernel errors
    (r"kernel\s+(?:error|not\s+initialized)", ErrorType.KERNEL_ERROR, ErrorSeverity.HIGH, False),
    (
        r"service\s+(?:not\s+found|not\s+registered|unavailable)",
        ErrorType.SERVICE_NOT_FOUND,
        ErrorSeverity.HIGH,
        False,
    ),
    # Validation errors
    (
        r"validation\s+(?:failed|error)|invalid\s+(?:input|output)",
        ErrorType.VALIDATION_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"type\s+error|expected\s+(?:type|str|int|float|bool|list|dict)",
        ErrorType.TYPE_ERROR,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"serialization\s+(?:failed|error)|(?:cannot|failed\s+to)\s+serialize",
        ErrorType.SERIALIZATION_ERROR,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Authentication
    (
        r"(?:401|unauthorized)|invalid\s+(?:api.?key|token)",
        ErrorType.AUTHENTICATION,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"(?:403|forbidden)|access\s+denied", ErrorType.PERMISSION, ErrorSeverity.HIGH, False),
]


class ErrorDetector:
    """
    Detects and classifies errors from Semantic Kernel operations.

    Provides:
    - Pattern-based error detection
    - Error classification (type, severity, transient/permanent)
    - Error statistics and monitoring
    - Plugin and function error tracking
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
            source: Source identifier (e.g., "function:MyPlugin.Search")
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
                    function_name=context.get("function_name") if context else None,
                    plugin_name=context.get("plugin_name") if context else None,
                    planner_type=context.get("planner_type") if context else None,
                    metadata=context or {},
                )
                self.stats.record(error)
                logger.warning(
                    f"[AIGIE] Semantic Kernel error detected: {error_type.value} from {source}"
                )
                return error

        return None

    def detect_from_function_result(
        self,
        function_name: str,
        plugin_name: str | None,
        result: Any,
        error_message: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from a function invocation result.

        Args:
            function_name: Name of the function
            plugin_name: Name of the plugin
            result: Function result
            error_message: Error message if function failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        full_name = f"{plugin_name}.{function_name}" if plugin_name else function_name
        source = f"function:{full_name}"
        context = {
            "function_name": function_name,
            "plugin_name": plugin_name,
        }

        if error_message:
            error = self.detect_from_text(error_message, source, context)
            if error:
                return error

            # Create generic function error
            error = DetectedError(
                error_type=ErrorType.FUNCTION_INVOCATION_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Function {full_name} failed: {error_message[:200]}",
                source=source,
                is_transient=True,
                raw_error=error_message[:500],
                function_name=function_name,
                plugin_name=plugin_name,
                metadata=context,
            )
            self.stats.record(error)
            return error

        return None

    def detect_from_planner_result(
        self,
        planner_type: str,
        goal: str,
        plan: Any = None,
        error_message: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from a planner execution.

        Args:
            planner_type: Type of planner (Sequential, Action, Handlebars)
            goal: The planning goal
            plan: The generated plan (if any)
            error_message: Error message if planning failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"planner:{planner_type}"
        context = {
            "planner_type": planner_type,
            "goal": goal[:200],
        }

        if error_message:
            error = self.detect_from_text(error_message, source, context)
            if error:
                error.planner_type = planner_type
                return error

            # Create generic planner error
            error = DetectedError(
                error_type=ErrorType.PLANNER_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Planner {planner_type} failed: {error_message[:200]}",
                source=source,
                is_transient=True,
                raw_error=error_message[:500],
                planner_type=planner_type,
                metadata=context,
            )
            self.stats.record(error)
            return error

        # Check if plan is empty or indicates failure
        if plan is None:
            error = DetectedError(
                error_type=ErrorType.PLAN_CREATION_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Planner {planner_type} returned no plan for goal: {goal[:100]}",
                source=source,
                is_transient=True,
                planner_type=planner_type,
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

        # Default classification based on exception type
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
        elif "service" in exc_type_lower:
            error_type = ErrorType.SERVICE_NOT_FOUND
            is_transient = True
        elif "kernel" in exc_type_lower:
            error_type = ErrorType.KERNEL_ERROR
        elif "planner" in exc_type_lower or "plan" in exc_type_lower:
            error_type = ErrorType.PLANNER_ERROR
            is_transient = True
        elif "function" in exc_type_lower:
            error_type = ErrorType.FUNCTION_INVOCATION_ERROR
            is_transient = True

        error = DetectedError(
            error_type=error_type,
            severity=severity,
            message=f"{exc_type}: {exc_message[:200]}",
            source=source,
            is_transient=is_transient,
            raw_error=f"{exc_type}: {exc_message}",
            function_name=context.get("function_name") if context else None,
            plugin_name=context.get("plugin_name") if context else None,
            planner_type=context.get("planner_type") if context else None,
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

    def get_stats(self) -> Dict[str, Any]:
        """Get current error statistics."""
        return self.stats.to_dict()

    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent errors as dictionaries."""
        return [e.to_dict() for e in self.stats.recent_errors[-limit:]]

    def get_plugin_error_rate(self, plugin_name: str) -> float:
        """Get the error rate for a specific plugin."""
        if self.stats.total_errors == 0:
            return 0.0
        plugin_errors = self.stats.errors_by_plugin.get(plugin_name, 0)
        return plugin_errors / self.stats.total_errors

    def get_error_summary(self) -> str:
        """Get a human-readable error summary."""
        if self.stats.total_errors == 0:
            return "No errors detected"

        summary = f"Total errors: {self.stats.total_errors}"
        summary += (
            f" (planner: {self.stats.planner_errors}, function: {self.stats.function_errors})"
        )

        if self.stats.errors_by_type:
            top_types = sorted(self.stats.errors_by_type.items(), key=lambda x: x[1], reverse=True)[
                :3
            ]
            summary += f"\nTop error types: {', '.join(f'{t}({c})' for t, c in top_types)}"

        if self.stats.errors_by_plugin:
            top_plugins = sorted(
                self.stats.errors_by_plugin.items(), key=lambda x: x[1], reverse=True
            )[:3]
            summary += f"\nTop plugin errors: {', '.join(f'{p}({c})' for p, c in top_plugins)}"

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
