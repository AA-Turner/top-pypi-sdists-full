"""LLM error normalizer — maps LLM SDK exceptions to ``TransientLLMError``.

Satisfies NFR-004 by providing a context manager that catches common LLM
SDK exceptions (OpenAI, Anthropic), inspects their HTTP status code, and
re-raises transient ones as ``TransientLLMError`` so callers can apply
review-specific retry logic.

Non-transient errors pass through unchanged.
"""

from __future__ import annotations

import contextlib
from collections.abc import Generator

# HTTP status codes considered transient (retryable).
_TRANSIENT_STATUS_CODES: frozenset[int] = frozenset({429, 502, 503})


class TransientLLMError(Exception):
    """Transient LLM error that should be retried.

    Wraps the original LLM SDK exception with a status code so callers can
    catch ``TransientLLMError`` directly and retry only transient failures.
    """

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def _extract_status_code(exc: Exception) -> int | None:
    """Try to extract an HTTP status code from an LLM SDK exception.

    Supports:
    - ``openai.APIStatusError`` (has ``.status_code``)
    - ``anthropic.APIStatusError`` (has ``.status_code``)
    - Generic exceptions with a ``status_code`` attribute.
    """
    code = getattr(exc, "status_code", None)
    if isinstance(code, int):
        return code

    # Some exceptions wrap the response object
    response = getattr(exc, "response", None)
    if response is not None:
        code = getattr(response, "status_code", None)
        if isinstance(code, int):
            return code

    return None


def _is_transient(exc: Exception) -> bool:
    """Return True if the exception represents a transient LLM error."""
    code = _extract_status_code(exc)
    if code is not None and code in _TRANSIENT_STATUS_CODES:
        return True

    # Check class name patterns for known transient error types
    cls_name = type(exc).__name__
    if cls_name in ("RateLimitError", "InternalServerError", "APIConnectionError"):
        return True

    return False


@contextlib.contextmanager
def normalize_llm_error() -> Generator[None, None, None]:
    """Context manager that normalizes LLM SDK exceptions.

    Usage::

        with normalize_llm_error():
            response = llm.invoke(prompt)

    Transient exceptions (429, 502, 503, rate-limit errors) are re-raised
    as ``TransientLLMError``.  Non-transient exceptions pass through
    unchanged.
    """
    try:
        yield
    except TransientLLMError:
        # Already normalized — re-raise as-is.
        raise
    except Exception as exc:
        if _is_transient(exc):
            code = _extract_status_code(exc)
            raise TransientLLMError(
                f"Transient LLM error (HTTP {code}): {exc}",
                status_code=code,
            ) from exc
        raise
