"""
No-op stubs for symbols whose backing modules were removed with the
autonomous-mode subsystem (error_detection, drift_detection, retry).

These stubs let the remaining observability / handler code continue to
import the old symbols and call the old methods without doing anything.
Production callers should migrate off these eventually, but for now the
stubs keep the SDK importable.
"""

import enum
import re
from dataclasses import dataclass, field
from typing import Any

_API_ERROR_RE = re.compile(r"\bAPI[\s_-]?Error\b", re.IGNORECASE)


class _NoOpStats:
    total_errors: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"total_errors": 0}


class _NoOpPlan:
    expected_tools: set[str] = set()
    model: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {}


class _NoOpExecution:
    retry_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {}


def _extract_message_text(message: Any) -> str:
    """Best-effort text extraction from a Claude Agent SDK AssistantMessage."""
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            text = getattr(block, "text", None)
            if isinstance(text, str):
                parts.append(text)
        return "\n".join(parts)
    if content is not None:
        return str(content)
    return ""


def _api_error_in(text: str) -> bool:
    return bool(text) and bool(_API_ERROR_RE.search(text))


def _make_detected_error(message: str, source: str) -> "DetectedError":
    return DetectedError(
        message=message,
        error_type=ErrorType.API_ERROR,
        severity=ErrorSeverity.ERROR,
        source=source,
    )


class ErrorDetector:
    """Minimal text-pattern error detector.

    Autonomous remediation was deleted; the detector retains just enough
    behavior to mark spans and traces as failed when a Claude response carries
    a content-level API error (e.g. ``"API Error: 400 ..."``).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.stats = _NoOpStats()

    def detect_from_exception(self, *args: Any, **kwargs: Any) -> None:
        return None

    def detect_from_llm_response(
        self, message: Any = None, model_name: str | None = None, *args: Any, **kwargs: Any
    ) -> "DetectedError | None":
        text = _extract_message_text(message)
        if _api_error_in(text):
            source = f"llm:{model_name}" if model_name else "llm"
            return _make_detected_error(text, source)
        return None

    def detect_from_tool_result(
        self,
        tool_name: str | None = None,
        tool_use_id: str | None = None,
        result: Any = None,
        is_error_flag: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> "DetectedError | None":
        text = str(result) if result is not None else ""
        if is_error_flag or _api_error_in(text):
            return _make_detected_error(text or "tool error", f"tool:{tool_name or 'unknown'}")
        return None

    def detect_from_chain_result(self, *args: Any, **kwargs: Any) -> None:
        return None

    def detect_from_retriever_result(self, *args: Any, **kwargs: Any) -> None:
        return None

    def detect_from_graph_result(self, *args: Any, **kwargs: Any) -> None:
        return None

    def detect_from_node_result(self, *args: Any, **kwargs: Any) -> None:
        return None

    def detect_from_subagent_result(
        self,
        subagent_type: str | None = None,
        tool_use_id: str | None = None,
        result: Any = None,
        is_error_flag: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> "DetectedError | None":
        text = str(result) if result is not None else ""
        if is_error_flag or _api_error_in(text):
            return _make_detected_error(
                text or "subagent error", f"subagent:{subagent_type or 'unknown'}"
            )
        return None

    def detect_from_text(
        self, text: str = "", source: str = "text", *args: Any, **kwargs: Any
    ) -> "DetectedError | None":
        if _api_error_in(text):
            return _make_detected_error(text, source)
        return None


class DriftDetector:
    """No-op drift detector (autonomous mode removed)."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.plan = _NoOpPlan()
        self.execution = _NoOpExecution()
        self._plan_captured = False

    def capture_system_prompt(self, *args: Any, **kwargs: Any) -> None:
        return None

    def capture_initial_prompt(self, *args: Any, **kwargs: Any) -> None:
        return None

    def capture_initial_input(self, *args: Any, **kwargs: Any) -> None:
        return None

    def capture_planning_chain_output(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_chain_execution(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_llm_response(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_tool_use(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_agent_execution(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_subagent_spawn(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_subagent_end(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_stt(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_llm(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_error(self, *args: Any, **kwargs: Any) -> None:
        return None

    def record_interruption(self, *args: Any, **kwargs: Any) -> None:
        return None

    def start_conversation(self, *args: Any, **kwargs: Any) -> None:
        return None

    def start_turn(self, *args: Any, **kwargs: Any) -> None:
        return None

    def finalize(self, *args: Any, **kwargs: Any) -> list:
        return []

    def get_summary(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {}

    def get_plan_metadata(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {}


VoiceErrorDetector = ErrorDetector
VoiceDriftDetector = DriftDetector


class ErrorType(enum.Enum):
    UNKNOWN = "unknown"
    API_ERROR = "api_error"


class ErrorSeverity(enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class DetectedError:
    """Detected error record (text-pattern detection only)."""

    message: str = ""
    error_type: ErrorType = ErrorType.UNKNOWN
    severity: ErrorSeverity = ErrorSeverity.ERROR
    source: str = ""
    is_transient: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "error_type": self.error_type.value
            if isinstance(self.error_type, ErrorType)
            else self.error_type,
            "severity": self.severity.value
            if isinstance(self.severity, ErrorSeverity)
            else self.severity,
            "source": self.source,
            "metadata": self.metadata,
        }


@dataclass
class DetectedDrift:
    message: str = ""
    drift_type: str = ""
    severity: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "drift_type": self.drift_type,
            "severity": self.severity,
        }


class DriftType:
    UNKNOWN = "unknown"


class DriftSeverity:
    INFO = "info"
    WARNING = "warning"


class ErrorStats(_NoOpStats):
    pass


class AgentPlan(_NoOpPlan):
    pass


class ExecutionTrace(_NoOpExecution):
    pass


_singleton_error_detector: ErrorDetector | None = None
_singleton_drift_detector: DriftDetector | None = None


def get_error_detector() -> ErrorDetector:
    global _singleton_error_detector
    if _singleton_error_detector is None:
        _singleton_error_detector = ErrorDetector()
    return _singleton_error_detector


def reset_error_detector() -> None:
    global _singleton_error_detector
    _singleton_error_detector = None


def get_drift_detector() -> DriftDetector:
    global _singleton_drift_detector
    if _singleton_drift_detector is None:
        _singleton_drift_detector = DriftDetector()
    return _singleton_drift_detector


def reset_drift_detector() -> None:
    global _singleton_drift_detector
    _singleton_drift_detector = None


# Voice variants (no-op aliases)
get_voice_error_detector = get_error_detector
reset_voice_error_detector = reset_error_detector
get_voice_drift_detector = get_drift_detector
reset_voice_drift_detector = reset_drift_detector


# Retry / timeout exceptions (autonomous retry removed; raised by nothing now)
class RetryExhaustedError(Exception):
    def __init__(
        self, *args: Any, attempts: int = 0, last_error: Exception | None = None, **kwargs: Any
    ) -> None:
        super().__init__(*args)
        self.attempts = attempts
        self.last_error = last_error


class TimeoutExceededError(Exception):
    def __init__(self, *args: Any, timeout: float = 0.0, **kwargs: Any) -> None:
        super().__init__(*args)
        self.timeout = timeout


class AgentExecutionError(Exception):
    pass


# Aliases used by various framework integrations
AgnoExecutionError = AgentExecutionError
DSPyExecutionError = AgentExecutionError
ConversationError = AgentExecutionError
QueryError = AgentExecutionError
CrewExecutionError = AgentExecutionError
GoogleADKExecutionError = AgentExecutionError
GraphExecutionError = AgentExecutionError


@dataclass
class RetryContext:
    attempt: int = 0
    max_attempts: int = 0
    last_error: Exception | None = None


ConversationRetryContext = RetryContext
QueryRetryContext = RetryContext
LiveKitRetryContext = RetryContext
OptimizationRetryContext = RetryContext
ProgramRetryContext = RetryContext
WorkflowRetryContext = RetryContext
CrewRetryContext = RetryContext
GraphRetryContext = RetryContext
GraphPlan = _NoOpPlan
WorkflowPlan = _NoOpPlan

# Pipecat voice variants
PipelineExecutionError = AgentExecutionError
VoiceServiceError = AgentExecutionError
VoiceServiceRetry = RetryContext
VoiceErrorType = ErrorType
DetectedVoiceError = DetectedError
VoiceErrorStats = ErrorStats
VoiceDriftType = DriftType
VoicePipelineExpectations = _NoOpPlan
TurnExecution = _NoOpExecution


def retry_decorator(*dargs: Any, **dkwargs: Any):
    """No-op decorator (autonomous retry removed)."""

    def _wrap(fn):
        return fn

    if len(dargs) == 1 and callable(dargs[0]) and not dkwargs:
        return dargs[0]
    return _wrap


with_retry = retry_decorator
with_timeout = retry_decorator


async def with_timeout_and_retry(fn: Any, *args: Any, **kwargs: Any) -> Any:
    """No-op timeout+retry — just invokes the callable (autonomous retry removed)."""
    # Strip retry/timeout kwargs that the real impl consumed
    for k in (
        "timeout",
        "max_retries",
        "retry_delay",
        "retry_on",
        "operation_name",
        "max_attempts",
        "backoff_factor",
    ):
        kwargs.pop(k, None)
    import inspect

    result = fn(*args, **kwargs) if callable(fn) else fn
    if inspect.isawaitable(result):
        return await result
    return result
