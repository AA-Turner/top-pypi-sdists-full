"""Execution-model exception hierarchy.

All exceptions are stdlib-only and carry structured context for
observability and retry decisions.
"""


class ReasoningTimeoutError(TimeoutError):
    """Raised when an LLM invocation exceeds its configured timeout."""

    def __init__(self, message: str = "LLM reasoning timed out", *, timeout_seconds: float | None = None) -> None:
        self.timeout_seconds = timeout_seconds
        super().__init__(message)


class ToolInvocationError(RuntimeError):
    """Raised when a tool invocation fails."""

    def __init__(self, message: str, *, tool_name: str = "", cause: BaseException | None = None) -> None:
        self.tool_name = tool_name
        self.cause = cause
        super().__init__(message)


class RetryExhaustedError(RuntimeError):
    """Raised when all retry attempts have been exhausted."""

    def __init__(
        self,
        message: str = "All retry attempts exhausted",
        *,
        attempts: int = 0,
        last_error: str = "",
    ) -> None:
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(message)
