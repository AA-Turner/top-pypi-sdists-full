"""
Error Detection and Monitoring for AutoGen/AG2 Multi-Agent Workflows.

Provides comprehensive error detection, classification, and monitoring
for agent conversations, tool executions, and code blocks.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Classification of error types for AutoGen."""

    # Transient errors (may succeed on retry)
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    NETWORK = "network"
    SERVER_ERROR = "server_error"

    # Agent errors
    AGENT_ERROR = "agent_error"
    AGENT_TIMEOUT = "agent_timeout"
    AGENT_LOOP = "agent_loop"
    AGENT_NOT_FOUND = "agent_not_found"
    AGENT_CONFIGURATION = "agent_config"

    # Conversation errors
    CONVERSATION_ERROR = "conversation_error"
    MESSAGE_ERROR = "message_error"
    TURN_LIMIT = "turn_limit"
    TERMINATION_ERROR = "termination_error"

    # Tool/Function errors
    TOOL_ERROR = "tool_error"
    TOOL_NOT_FOUND = "tool_not_found"
    TOOL_TIMEOUT = "tool_timeout"
    TOOL_INVALID_INPUT = "tool_invalid_input"
    TOOL_EXECUTION = "tool_execution"

    # Code execution errors
    CODE_EXECUTION_ERROR = "code_execution"
    CODE_TIMEOUT = "code_timeout"
    CODE_SYNTAX = "code_syntax"
    CODE_RUNTIME = "code_runtime"
    CODE_SECURITY = "code_security"

    # Group chat errors
    GROUP_CHAT_ERROR = "group_chat_error"
    SPEAKER_SELECTION = "speaker_selection"
    GROUP_CHAT_LOOP = "group_chat_loop"

    # LLM errors
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
    source: str  # e.g., "agent:assistant", "tool:search", "code:python"
    is_transient: bool
    raw_error: str | None = None
    agent_name: str | None = None
    turn_number: int | None = None
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
            "agent_name": self.agent_name,
            "turn_number": self.turn_number,
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
    errors_by_agent: Dict[str, int] = field(default_factory=dict)
    transient_errors: int = 0
    permanent_errors: int = 0
    code_execution_errors: int = 0
    tool_errors: int = 0
    agent_errors: int = 0
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

        # By agent
        if error.agent_name:
            self.errors_by_agent[error.agent_name] = (
                self.errors_by_agent.get(error.agent_name, 0) + 1
            )

        # Transient vs permanent
        if error.is_transient:
            self.transient_errors += 1
        else:
            self.permanent_errors += 1

        # Track specific error categories
        if error.error_type in [
            ErrorType.CODE_EXECUTION_ERROR,
            ErrorType.CODE_TIMEOUT,
            ErrorType.CODE_SYNTAX,
            ErrorType.CODE_RUNTIME,
        ]:
            self.code_execution_errors += 1
        if error.error_type in [
            ErrorType.TOOL_ERROR,
            ErrorType.TOOL_NOT_FOUND,
            ErrorType.TOOL_TIMEOUT,
            ErrorType.TOOL_EXECUTION,
        ]:
            self.tool_errors += 1
        if error.error_type in [
            ErrorType.AGENT_ERROR,
            ErrorType.AGENT_TIMEOUT,
            ErrorType.AGENT_LOOP,
        ]:
            self.agent_errors += 1

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
            "errors_by_agent": self.errors_by_agent,
            "transient_errors": self.transient_errors,
            "permanent_errors": self.permanent_errors,
            "code_execution_errors": self.code_execution_errors,
            "tool_errors": self.tool_errors,
            "agent_errors": self.agent_errors,
        }


# Error pattern matchers for AutoGen
ERROR_PATTERNS = [
    # Agent errors
    (r"agent\s+(?:error|failed|exception)", ErrorType.AGENT_ERROR, ErrorSeverity.HIGH, True),
    (r"agent\s+not\s+(?:found|registered)", ErrorType.AGENT_NOT_FOUND, ErrorSeverity.HIGH, False),
    (r"agent\s+(?:timed?\s*out|timeout)", ErrorType.AGENT_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (r"(?:infinite|endless)\s+loop|agent\s+loop", ErrorType.AGENT_LOOP, ErrorSeverity.HIGH, False),
    # Conversation errors
    (r"conversation\s+(?:error|failed)", ErrorType.CONVERSATION_ERROR, ErrorSeverity.HIGH, True),
    (r"message\s+(?:error|failed|invalid)", ErrorType.MESSAGE_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"(?:max|maximum)\s+turns?\s+(?:reached|exceeded)",
        ErrorType.TURN_LIMIT,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"termination\s+(?:error|failed)", ErrorType.TERMINATION_ERROR, ErrorSeverity.MEDIUM, False),
    # Tool/Function errors
    (r"tool\s+(?:error|failed|exception)", ErrorType.TOOL_ERROR, ErrorSeverity.MEDIUM, True),
    (r"(?:function|tool)\s+not\s+found", ErrorType.TOOL_NOT_FOUND, ErrorSeverity.HIGH, False),
    (r"tool\s+(?:timed?\s*out|timeout)", ErrorType.TOOL_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (
        r"invalid\s+(?:tool\s+)?(?:input|argument)",
        ErrorType.TOOL_INVALID_INPUT,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"(?:tool|function)\s+execution\s+(?:error|failed)",
        ErrorType.TOOL_EXECUTION,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Code execution errors
    (
        r"code\s+execution\s+(?:error|failed)",
        ErrorType.CODE_EXECUTION_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (r"code\s+(?:timed?\s*out|timeout)", ErrorType.CODE_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (r"syntax\s*error|invalid\s+syntax", ErrorType.CODE_SYNTAX, ErrorSeverity.MEDIUM, False),
    (r"runtime\s*error|execution\s+error", ErrorType.CODE_RUNTIME, ErrorSeverity.MEDIUM, True),
    (
        r"(?:security|sandbox)\s+(?:violation|error)",
        ErrorType.CODE_SECURITY,
        ErrorSeverity.CRITICAL,
        False,
    ),
    (
        r"exit\s*code\s*[1-9]|non.?zero\s+exit",
        ErrorType.CODE_EXECUTION_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Group chat errors
    (r"group\s*chat\s+(?:error|failed)", ErrorType.GROUP_CHAT_ERROR, ErrorSeverity.HIGH, True),
    (
        r"speaker\s+selection\s+(?:error|failed)",
        ErrorType.SPEAKER_SELECTION,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (r"group\s*chat\s+loop", ErrorType.GROUP_CHAT_LOOP, ErrorSeverity.HIGH, False),
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
    Detects and classifies errors from AutoGen multi-agent workflows.

    Provides:
    - Pattern-based error detection
    - Error classification (type, severity, transient/permanent)
    - Per-agent error tracking
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
            source: Source identifier (e.g., "agent:assistant")
            context: Additional context for the error

        Returns:
            DetectedError if an error is found, None otherwise
        """
        if not text:
            return None

        context = context or {}

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
                    agent_name=context.get("agent_name"),
                    turn_number=context.get("turn_number"),
                    metadata=context,
                )
                self.stats.record(error)
                logger.warning(f"[AIGIE] AutoGen error detected: {error_type.value} from {source}")
                return error

        return None

    def detect_from_conversation_result(
        self,
        success: bool,
        result: Any,
        error_message: str | None = None,
        agent_name: str | None = None,
        termination_reason: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from conversation completion.

        Args:
            success: Whether conversation completed successfully
            result: Conversation result
            error_message: Error message if failed
            agent_name: Name of the failing agent
            termination_reason: Reason for termination

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"conversation:{agent_name}" if agent_name else "conversation"
        context = {
            "agent_name": agent_name,
            "termination_reason": termination_reason,
        }

        if not success and error_message:
            error = self.detect_from_text(error_message, source, context)
            if error:
                return error

            # Create generic conversation error
            error = DetectedError(
                error_type=ErrorType.CONVERSATION_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Conversation failed: {error_message[:200]}",
                source=source,
                is_transient=True,
                raw_error=error_message[:500],
                agent_name=agent_name,
                metadata=context,
            )
            self.stats.record(error)
            return error

        return None

    def detect_from_tool_result(
        self,
        tool_name: str,
        success: bool,
        output: Any,
        error: str | None = None,
        agent_name: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from tool execution results.

        Args:
            tool_name: Name of the tool
            success: Whether tool executed successfully
            output: Tool output
            error: Error message if failed
            agent_name: Name of the calling agent

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"tool:{tool_name}"
        context = {
            "tool_name": tool_name,
            "agent_name": agent_name,
        }

        if not success:
            error_text = error or str(output)
            detected = self.detect_from_text(error_text, source, context)
            if detected:
                return detected

            # Create generic tool error
            detected = DetectedError(
                error_type=ErrorType.TOOL_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Tool '{tool_name}' failed: {error_text[:200]}",
                source=source,
                is_transient=True,
                raw_error=error_text[:500],
                agent_name=agent_name,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_code_execution(
        self,
        exit_code: int,
        output: str | None = None,
        error: str | None = None,
        language: str = "python",
        agent_name: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from code execution.

        Args:
            exit_code: Execution exit code
            output: Standard output
            error: Standard error
            language: Programming language
            agent_name: Name of executing agent

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"code:{language}"
        context = {
            "exit_code": exit_code,
            "language": language,
            "agent_name": agent_name,
        }

        if exit_code != 0:
            error_text = error or output or f"Exit code {exit_code}"
            detected = self.detect_from_text(error_text, source, context)
            if detected:
                detected.metadata["exit_code"] = exit_code
                return detected

            # Create generic code execution error
            detected = DetectedError(
                error_type=ErrorType.CODE_EXECUTION_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Code execution failed with exit code {exit_code}",
                source=source,
                is_transient=True,
                raw_error=error_text[:500] if error_text else None,
                agent_name=agent_name,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_llm_error(
        self,
        error: str,
        model: str | None = None,
        agent_name: str | None = None,
    ) -> DetectedError:
        """
        Detect errors from LLM calls.

        Args:
            error: Error message
            model: Model name
            agent_name: Name of the agent

        Returns:
            DetectedError for the LLM error
        """
        source = f"llm:{model}" if model else "llm"
        context = {
            "model": model,
            "agent_name": agent_name,
        }

        detected = self.detect_from_text(error, source, context)
        if detected:
            return detected

        # Default LLM error
        return DetectedError(
            error_type=ErrorType.MODEL_ERROR,
            severity=ErrorSeverity.HIGH,
            message=f"LLM error: {error[:200]}",
            source=source,
            is_transient=True,
            raw_error=error[:500],
            agent_name=agent_name,
            metadata=context,
        )

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
        context = context or {}

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
        if "timeout" in exc_type_lower:
            error_type = ErrorType.TIMEOUT
            is_transient = True
        elif "connection" in exc_type_lower or "network" in exc_type_lower:
            error_type = ErrorType.NETWORK
            is_transient = True
        elif "permission" in exc_type_lower or "auth" in exc_type_lower:
            error_type = ErrorType.PERMISSION

        error = DetectedError(
            error_type=error_type,
            severity=severity,
            message=f"{exc_type}: {exc_message[:200]}",
            source=source,
            is_transient=is_transient,
            raw_error=f"{exc_type}: {exc_message}",
            agent_name=context.get("agent_name"),
            metadata={**context, "exception_type": exc_type},
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

    def get_errors_by_agent(self) -> Dict[str, int]:
        """Get error counts by agent name."""
        return self.stats.errors_by_agent.copy()

    def get_error_summary(self) -> str:
        """Get a human-readable error summary."""
        if self.stats.total_errors == 0:
            return "No errors detected"

        summary = f"Total errors: {self.stats.total_errors}"
        summary += f" (agent: {self.stats.agent_errors}, tool: {self.stats.tool_errors}, code: {self.stats.code_execution_errors})"

        if self.stats.errors_by_type:
            top_types = sorted(self.stats.errors_by_type.items(), key=lambda x: x[1], reverse=True)[
                :3
            ]
            summary += f"\nTop error types: {', '.join(f'{t}({c})' for t, c in top_types)}"

        if self.stats.errors_by_agent:
            top_agents = sorted(
                self.stats.errors_by_agent.items(), key=lambda x: x[1], reverse=True
            )[:3]
            summary += f"\nTop agents with errors: {', '.join(f'{a}({c})' for a, c in top_agents)}"

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
