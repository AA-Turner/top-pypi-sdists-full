"""
Error Detection and Monitoring for CrewAI Workflows.

Provides comprehensive error detection, classification, and monitoring
for crew executions, agents, tasks, tools, and delegations.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Classification of error types for CrewAI."""

    # Transient errors (may succeed on retry)
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    NETWORK = "network"
    SERVER_ERROR = "server_error"

    # Crew errors
    CREW_ERROR = "crew_error"
    CREW_CONFIGURATION = "crew_config"
    PROCESS_ERROR = "process_error"

    # Task errors
    TASK_ERROR = "task_error"
    TASK_NOT_FOUND = "task_not_found"
    TASK_TIMEOUT = "task_timeout"
    TASK_DEPENDENCY = "task_dependency"
    TASK_CONTEXT = "task_context"

    # Agent errors
    AGENT_ERROR = "agent_error"
    AGENT_NOT_FOUND = "agent_not_found"
    AGENT_ROLE = "agent_role"
    AGENT_GOAL = "agent_goal"
    AGENT_BACKSTORY = "agent_backstory"
    AGENT_TIMEOUT = "agent_timeout"

    # Step errors (agent execution)
    STEP_ERROR = "step_error"
    STEP_TIMEOUT = "step_timeout"
    MAX_ITERATIONS = "max_iterations"
    PARSING_ERROR = "parsing_error"

    # Tool errors
    TOOL_ERROR = "tool_error"
    TOOL_NOT_FOUND = "tool_not_found"
    TOOL_TIMEOUT = "tool_timeout"
    TOOL_INVALID_INPUT = "tool_invalid_input"
    TOOL_EXECUTION = "tool_execution"

    # Delegation errors
    DELEGATION_ERROR = "delegation_error"
    DELEGATION_LOOP = "delegation_loop"
    DELEGATION_REJECTED = "delegation_rejected"

    # LLM errors
    MODEL_ERROR = "model_error"
    CONTENT_FILTER = "content_filter"
    CONTEXT_LENGTH = "context_length"
    MAX_RETRIES = "max_retries"

    # Memory errors
    MEMORY_ERROR = "memory_error"
    MEMORY_RETRIEVAL = "memory_retrieval"

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
    source: str  # e.g., "task:research", "agent:researcher", "tool:search"
    is_transient: bool
    raw_error: str | None = None
    agent_role: str | None = None
    task_id: str | None = None
    step_number: int | None = None
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
            "agent_role": self.agent_role,
            "task_id": self.task_id,
            "step_number": self.step_number,
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
    errors_by_task: Dict[str, int] = field(default_factory=dict)
    transient_errors: int = 0
    permanent_errors: int = 0
    task_errors: int = 0
    agent_errors: int = 0
    tool_errors: int = 0
    delegation_errors: int = 0
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
        if error.agent_role:
            self.errors_by_agent[error.agent_role] = (
                self.errors_by_agent.get(error.agent_role, 0) + 1
            )

        # By task
        if error.task_id:
            self.errors_by_task[error.task_id] = self.errors_by_task.get(error.task_id, 0) + 1

        # Transient vs permanent
        if error.is_transient:
            self.transient_errors += 1
        else:
            self.permanent_errors += 1

        # Track specific error categories
        if error.error_type in [
            ErrorType.TASK_ERROR,
            ErrorType.TASK_NOT_FOUND,
            ErrorType.TASK_TIMEOUT,
            ErrorType.TASK_DEPENDENCY,
        ]:
            self.task_errors += 1
        if error.error_type in [
            ErrorType.AGENT_ERROR,
            ErrorType.AGENT_NOT_FOUND,
            ErrorType.AGENT_TIMEOUT,
            ErrorType.STEP_ERROR,
        ]:
            self.agent_errors += 1
        if error.error_type in [
            ErrorType.TOOL_ERROR,
            ErrorType.TOOL_NOT_FOUND,
            ErrorType.TOOL_TIMEOUT,
            ErrorType.TOOL_EXECUTION,
        ]:
            self.tool_errors += 1
        if error.error_type in [
            ErrorType.DELEGATION_ERROR,
            ErrorType.DELEGATION_LOOP,
            ErrorType.DELEGATION_REJECTED,
        ]:
            self.delegation_errors += 1

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
            "errors_by_task": self.errors_by_task,
            "transient_errors": self.transient_errors,
            "permanent_errors": self.permanent_errors,
            "task_errors": self.task_errors,
            "agent_errors": self.agent_errors,
            "tool_errors": self.tool_errors,
            "delegation_errors": self.delegation_errors,
        }


# Error pattern matchers for CrewAI
ERROR_PATTERNS = [
    # Crew errors
    (r"crew\s+(?:error|failed|exception)", ErrorType.CREW_ERROR, ErrorSeverity.HIGH, True),
    (
        r"crew\s+(?:configuration|config)\s+(?:error|invalid)",
        ErrorType.CREW_CONFIGURATION,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"process\s+(?:error|failed|type)", ErrorType.PROCESS_ERROR, ErrorSeverity.HIGH, False),
    # Task errors
    (r"task\s+(?:error|failed|exception)", ErrorType.TASK_ERROR, ErrorSeverity.HIGH, True),
    (r"task\s+not\s+(?:found|defined)", ErrorType.TASK_NOT_FOUND, ErrorSeverity.HIGH, False),
    (r"task\s+(?:timed?\s*out|timeout)", ErrorType.TASK_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (
        r"(?:dependency|depends\s+on)\s+(?:error|failed|missing)",
        ErrorType.TASK_DEPENDENCY,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"context\s+(?:error|missing|invalid)", ErrorType.TASK_CONTEXT, ErrorSeverity.MEDIUM, True),
    # Agent errors
    (r"agent\s+(?:error|failed|exception)", ErrorType.AGENT_ERROR, ErrorSeverity.HIGH, True),
    (r"agent\s+not\s+(?:found|defined)", ErrorType.AGENT_NOT_FOUND, ErrorSeverity.HIGH, False),
    (r"agent\s+(?:timed?\s*out|timeout)", ErrorType.AGENT_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (
        r"(?:invalid|missing)\s+(?:role|agent\s+role)",
        ErrorType.AGENT_ROLE,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"(?:invalid|missing)\s+goal", ErrorType.AGENT_GOAL, ErrorSeverity.HIGH, False),
    # Step errors
    (r"step\s+(?:error|failed)", ErrorType.STEP_ERROR, ErrorSeverity.MEDIUM, True),
    (r"step\s+(?:timed?\s*out|timeout)", ErrorType.STEP_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (
        r"max(?:imum)?\s+iterations?\s+(?:reached|exceeded)",
        ErrorType.MAX_ITERATIONS,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"(?:parsing|parse)\s+(?:error|failed)", ErrorType.PARSING_ERROR, ErrorSeverity.MEDIUM, True),
    # Tool errors
    (r"tool\s+(?:error|failed|exception)", ErrorType.TOOL_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"(?:tool|function)\s+not\s+(?:found|available)",
        ErrorType.TOOL_NOT_FOUND,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"tool\s+(?:timed?\s*out|timeout)", ErrorType.TOOL_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (
        r"(?:invalid|bad)\s+(?:tool\s+)?(?:input|argument)",
        ErrorType.TOOL_INVALID_INPUT,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"tool\s+execution\s+(?:error|failed)", ErrorType.TOOL_EXECUTION, ErrorSeverity.MEDIUM, True),
    # Delegation errors
    (r"delegation\s+(?:error|failed)", ErrorType.DELEGATION_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"delegation\s+loop|circular\s+delegation",
        ErrorType.DELEGATION_LOOP,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"delegation\s+(?:rejected|denied)",
        ErrorType.DELEGATION_REJECTED,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Memory errors
    (r"memory\s+(?:error|failed)", ErrorType.MEMORY_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"memory\s+retrieval\s+(?:error|failed)",
        ErrorType.MEMORY_RETRIEVAL,
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
    Detects and classifies errors from CrewAI workflows.

    Provides:
    - Pattern-based error detection
    - Error classification (type, severity, transient/permanent)
    - Per-agent and per-task error tracking
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
            source: Source identifier (e.g., "agent:researcher")
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
                    agent_role=context.get("agent_role"),
                    task_id=context.get("task_id"),
                    step_number=context.get("step_number"),
                    metadata=context,
                )
                self.stats.record(error)
                logger.warning(f"[AIGIE] CrewAI error detected: {error_type.value} from {source}")
                return error

        return None

    def detect_from_crew_result(
        self,
        success: bool,
        result: Any,
        error_message: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from crew execution completion.

        Args:
            success: Whether crew completed successfully
            result: Crew execution result
            error_message: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = "crew"

        if not success and error_message:
            error = self.detect_from_text(error_message, source)
            if error:
                return error

            # Create generic crew error
            error = DetectedError(
                error_type=ErrorType.CREW_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Crew execution failed: {error_message[:200]}",
                source=source,
                is_transient=True,
                raw_error=error_message[:500],
            )
            self.stats.record(error)
            return error

        return None

    def detect_from_task_result(
        self,
        task_id: str,
        task_description: str,
        agent_role: str,
        success: bool = True,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from task execution.

        Args:
            task_id: Task identifier
            task_description: Task description
            agent_role: Role of assigned agent
            success: Whether task completed successfully
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"task:{task_description[:30]}"
        context = {
            "task_id": task_id,
            "agent_role": agent_role,
        }

        if not success and error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic task error
            detected = DetectedError(
                error_type=ErrorType.TASK_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Task '{task_description[:50]}' failed: {error[:150]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                agent_role=agent_role,
                task_id=task_id,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_agent_step(
        self,
        agent_role: str,
        step_number: int,
        success: bool = True,
        thought: str | None = None,
        action: str | None = None,
        observation: str | None = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from agent step execution.

        Args:
            agent_role: Role of the agent
            step_number: Step number within task
            success: Whether step completed successfully
            thought: Agent's reasoning
            action: Action taken
            observation: Result of action
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"agent:{agent_role}:step_{step_number}"
        context = {
            "agent_role": agent_role,
            "step_number": step_number,
            "action": action,
        }

        if not success and error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

        # Check observation for errors
        if observation:
            detected = self.detect_from_text(observation, source, context)
            if detected:
                return detected

        return None

    def detect_from_tool_result(
        self,
        tool_name: str,
        success: bool,
        output: Any,
        error: str | None = None,
        agent_role: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from tool execution.

        Args:
            tool_name: Name of the tool
            success: Whether tool executed successfully
            output: Tool output
            error: Error message if failed
            agent_role: Role of the calling agent

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"tool:{tool_name}"
        context = {
            "tool_name": tool_name,
            "agent_role": agent_role,
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
                agent_role=agent_role,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_delegation(
        self,
        from_agent: str,
        to_agent: str,
        success: bool,
        result: str | None = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from delegation.

        Args:
            from_agent: Role of delegating agent
            to_agent: Role of receiving agent
            success: Whether delegation succeeded
            result: Delegation result
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"delegation:{from_agent}->{to_agent}"
        context = {
            "from_agent": from_agent,
            "to_agent": to_agent,
        }

        if not success:
            error_text = error or "Delegation failed"
            detected = self.detect_from_text(error_text, source, context)
            if detected:
                return detected

            # Create generic delegation error
            detected = DetectedError(
                error_type=ErrorType.DELEGATION_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Delegation from '{from_agent}' to '{to_agent}' failed",
                source=source,
                is_transient=True,
                raw_error=error_text[:500] if error_text else None,
                agent_role=from_agent,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

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
            agent_role=context.get("agent_role"),
            task_id=context.get("task_id"),
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
        """Get error counts by agent role."""
        return self.stats.errors_by_agent.copy()

    def get_errors_by_task(self) -> Dict[str, int]:
        """Get error counts by task."""
        return self.stats.errors_by_task.copy()

    def get_error_summary(self) -> str:
        """Get a human-readable error summary."""
        if self.stats.total_errors == 0:
            return "No errors detected"

        summary = f"Total errors: {self.stats.total_errors}"
        summary += f" (task: {self.stats.task_errors}, agent: {self.stats.agent_errors}, tool: {self.stats.tool_errors}, delegation: {self.stats.delegation_errors})"

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
