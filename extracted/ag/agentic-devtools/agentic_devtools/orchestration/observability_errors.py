"""Error classification for observability events.

Maps exceptions to one of four categories with a retryable flag:
- ``transient``: Network/rate-limit errors (retryable).
- ``permanent``: Default non-transient fallback when no source context is provided.
- ``llm``: Non-transient errors routed from ``context["source"] == "llm"``.
- ``tool``: Non-transient errors routed from ``context["source"] == "tool"``.
"""

from __future__ import annotations

import errno as _errno
from dataclasses import dataclass
from typing import Any

# Network-related errno values that indicate transient connectivity failures.
# Using errno codes avoids substring matching on the error message, which can
# misclassify unrelated OSErrors (e.g., FileNotFoundError("connection.txt")).
# Built using getattr so the set degrades gracefully on platforms that do not
# expose every constant (e.g., some values are absent on Windows).
_TRANSIENT_ERRNO_NAMES = (
    "ECONNRESET",  # Connection reset by peer
    "ECONNREFUSED",  # Connection refused
    "ECONNABORTED",  # Software caused connection abort
    "ETIMEDOUT",  # Connection timed out
    "ENETUNREACH",  # Network unreachable
    "EHOSTUNREACH",  # Host unreachable
    "EPIPE",  # Broken pipe
)
_TRANSIENT_ERRNOS: frozenset[int] = frozenset(
    getattr(_errno, name) for name in _TRANSIENT_ERRNO_NAMES if hasattr(_errno, name)
)


@dataclass(frozen=True)
class ErrorClassification:
    """Result of classifying an exception.

    Attributes:
        error_class: One of ``"transient"``, ``"permanent"``, ``"llm"``, ``"tool"``.
        retryable: Whether the error is eligible for retry.
        message: Human-readable description of the classification.
    """

    error_class: str
    retryable: bool
    message: str


class ErrorClassifier:
    """Classifies exceptions into observability error categories.

    Context can indicate whether the error occurred during an LLM call
    or tool call, influencing classification routing.
    """

    def classify(self, exception: BaseException, context: dict[str, Any] | None = None) -> ErrorClassification:
        """Classify an exception into an error category.

        Args:
            exception: The exception to classify.
            context: Optional context dict. Recognized keys:
                - ``"source"``: ``"llm"`` or ``"tool"`` to route classification.
                - ``"status_code"``: HTTP status code (int) for HTTP errors.

        Returns:
            An ErrorClassification with category, retryable flag, and message.
        """
        ctx = context or {}
        source = ctx.get("source", "")

        # LLM-specific errors
        if source == "llm":
            return self._classify_llm(exception, ctx)

        # Tool-specific errors
        if source == "tool":
            return self._classify_tool(exception, ctx)

        # Transient network/timeout errors
        if self._is_transient(exception, ctx):
            return ErrorClassification(
                error_class="transient",
                retryable=True,
                message=f"Transient error: {type(exception).__name__}: {exception}",
            )

        # Default: permanent (non-retryable)
        return ErrorClassification(
            error_class="permanent",
            retryable=False,
            message=f"Permanent error: {type(exception).__name__}: {exception}",
        )

    def _is_transient(self, exception: BaseException, ctx: dict[str, Any]) -> bool:
        """Check if an exception represents a transient failure.

        ``OSError`` transience is determined by ``errno`` rather than message
        substring matching, which would misclassify filesystem errors whose
        path or message happens to contain the word "connection".
        """
        # Built-in network/timeout types (ConnectionError, TimeoutError, and
        # their subclasses: ConnectionResetError, ConnectionRefusedError, etc.)
        if isinstance(exception, (ConnectionError, TimeoutError)):
            return True
        # Plain OSError with a known network errno (e.g. ENETUNREACH, EHOSTUNREACH)
        if isinstance(exception, OSError) and exception.errno in _TRANSIENT_ERRNOS:
            return True

        # HTTP status codes indicating transient issues
        status_code = ctx.get("status_code")
        if isinstance(status_code, int):
            if status_code == 429 or status_code >= 500:
                return True

        return False

    def _is_permanent_http_4xx(self, ctx: dict[str, Any]) -> bool:
        """Check for non-transient HTTP 4xx status codes."""
        status_code = ctx.get("status_code")
        return isinstance(status_code, int) and 400 <= status_code < 500 and status_code != 429

    def _classify_llm(self, exception: BaseException, ctx: dict[str, Any]) -> ErrorClassification:
        """Classify an error occurring during an LLM call."""
        # Check for transient errors first (even within LLM context)
        if self._is_transient(exception, ctx):
            return ErrorClassification(
                error_class="transient",
                retryable=True,
                message=f"Transient LLM error: {type(exception).__name__}: {exception}",
            )

        # LLM-specific: validation failure, refusal, malformed output
        return ErrorClassification(
            error_class="llm",
            retryable=not self._is_permanent_http_4xx(ctx),
            message=f"LLM error: {type(exception).__name__}: {exception}",
        )

    def _classify_tool(self, exception: BaseException, ctx: dict[str, Any]) -> ErrorClassification:
        """Classify an error occurring during a tool call."""
        # Check for transient errors first (even within tool context)
        if self._is_transient(exception, ctx):
            return ErrorClassification(
                error_class="transient",
                retryable=True,
                message=f"Transient tool error: {type(exception).__name__}: {exception}",
            )

        # Tool-specific failures
        return ErrorClassification(
            error_class="tool",
            retryable=not self._is_permanent_http_4xx(ctx),
            message=f"Tool error: {type(exception).__name__}: {exception}",
        )
