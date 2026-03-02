"""Context length management for agent conversations."""

from typing import Optional

from ..core.config import get_config
from ..utils.logger import log


def estimate_tokens(text: str) -> int:
    """Estimate token count from text.

    Uses ~4 characters per token as a rough estimate.
    This is conservative for English text and code.

    Args:
        text: Text to estimate tokens for

    Returns:
        Estimated token count
    """
    if not text:
        return 0
    return len(text) // 4


def truncate_tool_output(output: str, max_tokens: Optional[int] = None) -> str:
    """Truncate tool output to stay within token limit.

    Args:
        output: Tool output string (usually JSON)
        max_tokens: Maximum tokens (uses config default if None)

    Returns:
        Truncated output with indicator if truncated
    """
    config = get_config()
    max_tokens = max_tokens or config.agent.tool_max_output_tokens
    max_chars = max_tokens * 4  # Reverse the ~4 chars/token estimate

    if len(output) <= max_chars:
        return output

    # Truncate and add indicator
    truncated = output[: max_chars - 150]  # Leave room for truncation message
    chars_removed = len(output) - len(truncated)
    lines_removed = output[max_chars - 150 :].count("\n")

    truncation_msg = (
        f"\n\n[OUTPUT TRUNCATED: ~{lines_removed} lines omitted, "
        f"{chars_removed} chars removed to fit {max_tokens} token limit]"
    )

    log.warning(
        "Truncated tool output from {} to {} chars (~{} tokens)",
        len(output),
        len(truncated),
        max_tokens,
    )

    return truncated + truncation_msg


def reduce_context_for_retry(
    messages: list[dict],
    keep_recent: int = 4,
) -> list[dict]:
    """Reduce context by removing old messages.

    Keeps the first user message and the most recent messages.

    Args:
        messages: Current messages list
        keep_recent: Number of recent messages to keep

    Returns:
        Reduced messages list
    """
    if len(messages) <= keep_recent + 1:
        return messages  # Can't reduce further

    # Always keep first message (initial user query)
    first_msg = messages[0]

    # Keep the most recent messages
    recent_msgs = messages[-keep_recent:]

    reduced = [first_msg] + recent_msgs

    log.info(
        "Reduced context from {} to {} messages for retry",
        len(messages),
        len(reduced),
    )

    return reduced


def is_context_overflow_error(exc: Exception) -> bool:
    """Check if an exception is a context length overflow error.

    Handles different error formats from various providers:
    - OpenAI: "context_length_exceeded" code
    - Anthropic: "prompt is too long" message
    - Fireworks: Similar to OpenAI format

    Args:
        exc: Exception to check

    Returns:
        True if this is a context overflow error
    """
    error_str = str(exc).lower()

    # Check common error patterns
    overflow_patterns = [
        "context_length_exceeded",
        "context length",
        "maximum context length",
        "prompt is too long",
        "too many tokens",
        "token limit",
        "exceeds the model's maximum",
        "max_tokens",
    ]

    for pattern in overflow_patterns:
        if pattern in error_str:
            return True

    # Check for specific error codes
    if hasattr(exc, "code"):
        if exc.code == "context_length_exceeded":
            return True

    # Check HTTP status (400 often used for this)
    if hasattr(exc, "status_code"):
        if exc.status_code == 400 and any(p in error_str for p in overflow_patterns):
            return True

    return False


def is_transient_network_error(exc: Exception) -> bool:
    """Check if an exception is a transient network error worth retrying.

    Catches timeout and connection errors from httpx (used by OpenAI SDK)
    and standard library network errors.

    Args:
        exc: Exception to check

    Returns:
        True if this is a transient network error
    """
    # Check by exception type name to avoid importing httpx
    exc_type = type(exc).__name__
    transient_types = {
        "ReadTimeout",
        "ConnectTimeout",
        "PoolTimeout",
        "ConnectError",
        "RemoteProtocolError",
        "ReadError",
    }
    if exc_type in transient_types:
        return True

    # Check parent classes (e.g. httpx.TimeoutException)
    for parent in type(exc).__mro__:
        if parent.__name__ in ("TimeoutException", "TransportError"):
            return True

    # Standard library network errors
    if isinstance(exc, (ConnectionError, TimeoutError, OSError)):
        return True

    # Check error message patterns
    error_str = str(exc).lower()
    transient_patterns = [
        "read operation timed out",
        "connection reset",
        "connection refused",
        "temporary failure",
        "name resolution",
        "timed out",
    ]
    for pattern in transient_patterns:
        if pattern in error_str:
            return True

    return False
