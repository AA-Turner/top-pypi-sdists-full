"""
Error Detection and Monitoring for OpenAI Agents SDK Workflows.

Provides comprehensive error detection, classification, and monitoring
for agent executions, tool calls, handoffs, and guardrails.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Classification of error types for OpenAI Agents SDK."""

    # Transient errors (may succeed on retry)
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    NETWORK = "network"
    SERVER_ERROR = "server_error"

    # Agent errors
    AGENT_ERROR = "agent_error"
    AGENT_NOT_FOUND = "agent_not_found"
    AGENT_CONFIGURATION = "agent_config"
    AGENT_TIMEOUT = "agent_timeout"
    AGENT_LOOP = "agent_loop"

    # Workflow errors
    WORKFLOW_ERROR = "workflow_error"
    WORKFLOW_TIMEOUT = "workflow_timeout"
    WORKFLOW_CONFIGURATION = "workflow_config"

    # Generation errors
    GENERATION_ERROR = "generation_error"
    GENERATION_EMPTY = "generation_empty"
    GENERATION_PARSE = "generation_parse"
    GENERATION_TIMEOUT = "generation_timeout"

    # Tool errors
    TOOL_ERROR = "tool_error"
    TOOL_NOT_FOUND = "tool_not_found"
    TOOL_TIMEOUT = "tool_timeout"
    TOOL_INVALID_INPUT = "tool_invalid_input"
    TOOL_EXECUTION = "tool_execution"

    # Handoff errors
    HANDOFF_ERROR = "handoff_error"
    HANDOFF_REJECTED = "handoff_rejected"
    HANDOFF_LOOP = "handoff_loop"
    HANDOFF_TARGET_NOT_FOUND = "handoff_target_not_found"

    # Guardrail errors
    GUARDRAIL_ERROR = "guardrail_error"
    GUARDRAIL_BLOCKED = "guardrail_blocked"
    INPUT_GUARDRAIL = "input_guardrail"
    OUTPUT_GUARDRAIL = "output_guardrail"

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
    source: str  # e.g., "agent:assistant", "tool:search", "guardrail:input"
    is_transient: bool
    raw_error: str | None = None
    agent_name: str | None = None
    tool_name: str | None = None
    handoff_target: str | None = None
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
            "tool_name": self.tool_name,
            "handoff_target": self.handoff_target,
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
    agent_errors: int = 0
    tool_errors: int = 0
    handoff_errors: int = 0
    guardrail_errors: int = 0
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
            ErrorType.AGENT_ERROR,
            ErrorType.AGENT_NOT_FOUND,
            ErrorType.AGENT_TIMEOUT,
            ErrorType.AGENT_LOOP,
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
            ErrorType.HANDOFF_ERROR,
            ErrorType.HANDOFF_REJECTED,
            ErrorType.HANDOFF_LOOP,
            ErrorType.HANDOFF_TARGET_NOT_FOUND,
        ]:
            self.handoff_errors += 1
        if error.error_type in [
            ErrorType.GUARDRAIL_ERROR,
            ErrorType.GUARDRAIL_BLOCKED,
            ErrorType.INPUT_GUARDRAIL,
            ErrorType.OUTPUT_GUARDRAIL,
        ]:
            self.guardrail_errors += 1

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
            "agent_errors": self.agent_errors,
            "tool_errors": self.tool_errors,
            "handoff_errors": self.handoff_errors,
            "guardrail_errors": self.guardrail_errors,
        }


# Error pattern matchers for OpenAI Agents SDK
ERROR_PATTERNS = [
    # Agent errors
    (r"agent\s+(?:error|failed|exception)", ErrorType.AGENT_ERROR, ErrorSeverity.HIGH, True),
    (r"agent\s+not\s+(?:found|defined)", ErrorType.AGENT_NOT_FOUND, ErrorSeverity.HIGH, False),
    (
        r"agent\s+(?:configuration|config)\s+(?:error|invalid)",
        ErrorType.AGENT_CONFIGURATION,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"agent\s+(?:timed?\s*out|timeout)", ErrorType.AGENT_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (r"agent\s+loop|(?:infinite|endless)\s+loop", ErrorType.AGENT_LOOP, ErrorSeverity.HIGH, False),
    # Workflow errors
    (r"workflow\s+(?:error|failed)", ErrorType.WORKFLOW_ERROR, ErrorSeverity.HIGH, True),
    (
        r"workflow\s+(?:timed?\s*out|timeout)",
        ErrorType.WORKFLOW_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"workflow\s+(?:configuration|config)\s+(?:error|invalid)",
        ErrorType.WORKFLOW_CONFIGURATION,
        ErrorSeverity.HIGH,
        False,
    ),
    # Generation errors
    (r"generation\s+(?:error|failed)", ErrorType.GENERATION_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"(?:empty|no)\s+(?:generation|response)",
        ErrorType.GENERATION_EMPTY,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:parse|parsing)\s+(?:error|failed)|could\s+not\s+parse",
        ErrorType.GENERATION_PARSE,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"generation\s+(?:timed?\s*out|timeout)",
        ErrorType.GENERATION_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
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
    # Handoff errors
    (r"handoff\s+(?:error|failed)", ErrorType.HANDOFF_ERROR, ErrorSeverity.MEDIUM, True),
    (r"handoff\s+(?:rejected|denied)", ErrorType.HANDOFF_REJECTED, ErrorSeverity.MEDIUM, False),
    (r"handoff\s+loop|circular\s+handoff", ErrorType.HANDOFF_LOOP, ErrorSeverity.HIGH, False),
    (
        r"handoff\s+target\s+not\s+found",
        ErrorType.HANDOFF_TARGET_NOT_FOUND,
        ErrorSeverity.HIGH,
        False,
    ),
    # Guardrail errors
    (r"guardrail\s+(?:error|failed)", ErrorType.GUARDRAIL_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"guardrail\s+(?:blocked|triggered)",
        ErrorType.GUARDRAIL_BLOCKED,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"input\s+guardrail|guardrail.*input", ErrorType.INPUT_GUARDRAIL, ErrorSeverity.MEDIUM, False),
    (
        r"output\s+guardrail|guardrail.*output",
        ErrorType.OUTPUT_GUARDRAIL,
        ErrorSeverity.MEDIUM,
        False,
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
    Detects and classifies errors from OpenAI Agents SDK workflows.

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
                    tool_name=context.get("tool_name"),
                    handoff_target=context.get("handoff_target"),
                    metadata=context,
                )
                self.stats.record(error)
                logger.warning(
                    f"[AIGIE] OpenAI Agents error detected: {error_type.value} from {source}"
                )
                return error

        return None

    def detect_from_workflow_result(
        self,
        workflow_name: str,
        success: bool,
        result: Any = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from workflow completion.

        Args:
            workflow_name: Name of the workflow
            success: Whether workflow completed successfully
            result: Workflow result
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"workflow:{workflow_name}"
        context = {"workflow_name": workflow_name}

        if not success and error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic workflow error
            detected = DetectedError(
                error_type=ErrorType.WORKFLOW_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Workflow '{workflow_name}' failed: {error[:200]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_agent_result(
        self,
        agent_name: str,
        success: bool = True,
        output: Any = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from agent execution.

        Args:
            agent_name: Name of the agent
            success: Whether agent completed successfully
            output: Agent output
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"agent:{agent_name}"
        context = {"agent_name": agent_name}

        if not success and error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic agent error
            detected = DetectedError(
                error_type=ErrorType.AGENT_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Agent '{agent_name}' failed: {error[:200]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                agent_name=agent_name,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_generation(
        self,
        model: str,
        response: str | None = None,
        error: str | None = None,
        agent_name: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from LLM generation.

        Args:
            model: Model name
            response: Generation response
            error: Error message if failed
            agent_name: Name of the calling agent

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"generation:{model}"
        context = {
            "model": model,
            "agent_name": agent_name,
        }

        if error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic generation error
            detected = DetectedError(
                error_type=ErrorType.GENERATION_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Generation failed ({model}): {error[:150]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                agent_name=agent_name,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        # Check for empty response
        if response is not None and len(response.strip()) < 5:
            detected = DetectedError(
                error_type=ErrorType.GENERATION_EMPTY,
                severity=ErrorSeverity.MEDIUM,
                message=f"Generation returned empty response ({model})",
                source=source,
                is_transient=True,
                agent_name=agent_name,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_tool_result(
        self,
        tool_name: str,
        success: bool,
        result: Any = None,
        error: str | None = None,
        agent_name: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from tool execution.

        Args:
            tool_name: Name of the tool
            success: Whether tool executed successfully
            result: Tool result
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
            error_text = error or str(result)
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
                tool_name=tool_name,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_handoff(
        self,
        source_agent: str,
        target_agent: str,
        success: bool,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from agent handoff.

        Args:
            source_agent: Agent initiating handoff
            target_agent: Agent receiving handoff
            success: Whether handoff succeeded
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"handoff:{source_agent}->{target_agent}"
        context = {
            "source_agent": source_agent,
            "target_agent": target_agent,
        }

        if not success:
            error_text = error or "Handoff failed"
            detected = self.detect_from_text(error_text, source, context)
            if detected:
                return detected

            # Create generic handoff error
            detected = DetectedError(
                error_type=ErrorType.HANDOFF_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Handoff from '{source_agent}' to '{target_agent}' failed",
                source=source,
                is_transient=True,
                raw_error=error_text[:500] if error_text else None,
                agent_name=source_agent,
                handoff_target=target_agent,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_guardrail(
        self,
        guardrail_name: str,
        guardrail_type: str,
        passed: bool,
        result: Any = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from guardrail checks.

        Args:
            guardrail_name: Name of the guardrail
            guardrail_type: Type (input/output/validation)
            passed: Whether guardrail passed
            result: Guardrail result
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"guardrail:{guardrail_name}"
        context = {
            "guardrail_name": guardrail_name,
            "guardrail_type": guardrail_type,
            "passed": passed,
        }

        if not passed:
            error_text = error or "Guardrail blocked"

            # Determine error type based on guardrail type
            if guardrail_type == "input":
                error_type = ErrorType.INPUT_GUARDRAIL
            elif guardrail_type == "output":
                error_type = ErrorType.OUTPUT_GUARDRAIL
            else:
                error_type = ErrorType.GUARDRAIL_BLOCKED

            detected = DetectedError(
                error_type=error_type,
                severity=ErrorSeverity.MEDIUM,
                message=f"Guardrail '{guardrail_name}' ({guardrail_type}) blocked: {error_text[:150]}",
                source=source,
                is_transient=False,
                raw_error=error_text[:500],
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
            agent_name=context.get("agent_name"),
            tool_name=context.get("tool_name"),
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
        summary += f" (agent: {self.stats.agent_errors}, tool: {self.stats.tool_errors}, handoff: {self.stats.handoff_errors}, guardrail: {self.stats.guardrail_errors})"

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
