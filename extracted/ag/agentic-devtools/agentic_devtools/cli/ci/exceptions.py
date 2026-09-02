"""CI provider exceptions.

Custom exception types for CI platform provider operations.
"""

from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class MalformedEventError(ValueError):
    """Raised when a CI event payload cannot be parsed.

    Attributes:
        event_name: The event type that failed to parse.
        reason: Human-readable description of what was invalid.
    """

    def __init__(self, event_name: str, reason: str) -> None:
        self.event_name = event_name
        self.reason = reason
        super().__init__(f"Malformed {event_name} event: {reason}")


class VariableWriteError(RuntimeError):
    """Raised when a repository variable cannot be written.

    Typically indicates REPO_VARIABLE_WRITER_PAT is missing, expired,
    or lacks the Variables: Read and write permission.
    """


class AgentAssignmentError(RuntimeError):
    """Raised when assignment input validation fails before API dispatch."""


__all__ = [
    "AgentAssignmentError",
    "MalformedEventError",
    "ProviderRateLimitError",
    "VariableWriteError",
]
