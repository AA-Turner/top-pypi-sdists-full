"""Retry utility with exponential backoff for transient HTTP errors.

Provides a decorator and callable wrapper that retries operations on
transient failures (HTTP 429, 502, 503) with exponential backoff.

Configuration:
  - Initial delay: 1 second
  - Max retries: 3
  - Max total retry wait: 15 seconds
"""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

T = TypeVar("T")

# Transient HTTP status codes that should trigger a retry
TRANSIENT_STATUS_CODES = frozenset({429, 502, 503})

# Alternation of transient status codes, built from ``TRANSIENT_STATUS_CODES``
# so that constant is the single source of truth and cannot drift from the
# matcher below (adding a code to the constant automatically updates detection).
_TRANSIENT_CODE_ALTERNATION = "|".join(str(code) for code in sorted(TRANSIENT_STATUS_CODES))

# Matches an ``HTTP <code>`` token (case-insensitive) where ``<code>`` is a
# transient status code bounded by word boundaries. Word boundaries avoid false
# positives from adjacent-digit strings such as ``"HTTP 50200"``.
_TRANSIENT_HTTP_RE = re.compile(rf"\bhttp ({_TRANSIENT_CODE_ALTERNATION})\b", re.IGNORECASE)

# Bare status-code forms seen in provider stderr, matched only when followed by
# the corresponding transient reason phrase after whitespace or punctuation
# separators (for example ``"503 service unavailable"`` or
# ``"429 - too many requests"``). This keeps strings like
# ``"processed 429 rows"`` from being misclassified. Numeric-only bare codes
# like ``"503"`` intentionally do not match because, without a reason phrase or
# an ``HTTP`` prefix, they are too ambiguous to safely classify as transient.
_TRANSIENT_BARE_STATUS_RE = {
    429: re.compile(r"\b429\b(?=(?:\s|[:;,.()/-])+too many requests\b)", re.IGNORECASE),
    502: re.compile(r"\b502\b(?=(?:\s|[:;,.()/-])+bad gateway\b)", re.IGNORECASE),
    503: re.compile(r"\b503\b(?=(?:\s|[:;,.()/-])+service unavailable\b)", re.IGNORECASE),
}


def detect_transient_status_code(text: str) -> int | None:
    """Return the transient HTTP status code embedded in *text*, or ``None``.

    Searches for either an ``HTTP <code>`` token or a known bare transient
    provider error such as ``"503 service unavailable"`` or
    ``"429 - too many requests"``. Returns the matched code as an ``int`` when
    present, otherwise ``None``. Shared by :func:`is_transient_error` and
    provider-level transient detection so both paths use the exact same precise
    matcher.
    """
    match = _TRANSIENT_HTTP_RE.search(text)
    if match is not None:
        return int(match.group(1))
    for status_code, pattern in _TRANSIENT_BARE_STATUS_RE.items():
        if pattern.search(text):
            return status_code
    return None


# Default retry configuration
DEFAULT_INITIAL_DELAY = 1.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_MAX_TOTAL_WAIT = 15.0


class TransientError(Exception):
    """Raised to signal a transient error that should be retried.

    Attributes:
        status_code: HTTP status code that triggered the error.
    """

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.status_code = status_code
        super().__init__(message)


def is_transient_error(exc: Exception) -> bool:
    """Check if an exception represents a transient error worth retrying.

    Returns ``True`` for :class:`TransientError` instances, or for
    ``RuntimeError`` messages that mention transient status codes either as
    ``http <code>`` tokens or as known bare transient provider errors such as
    ``"503 service unavailable"``. Precise matching prevents false positives
    from adjacent-digit strings such as ``"HTTP 50200"`` or unrelated numbers
    such as ``"processed 429 rows"``.
    """
    if isinstance(exc, TransientError):
        return True
    # Only check RuntimeError for HTTP status indicators to avoid false
    # positives from unrelated exceptions (e.g. ValueError("503"))
    if not isinstance(exc, RuntimeError):
        return False
    return detect_transient_status_code(str(exc)) is not None


def retry_on_transient(
    func: Callable[..., T] | None = None,
    *,
    max_retries: int = DEFAULT_MAX_RETRIES,
    initial_delay: float = DEFAULT_INITIAL_DELAY,
    max_total_wait: float = DEFAULT_MAX_TOTAL_WAIT,
) -> Any:
    """Retry a function on transient errors with exponential backoff.

    Can be used as a decorator (with or without arguments) or called directly.

    Args:
        func: The function to wrap (when used as bare decorator).
        max_retries: Maximum number of retry attempts.
        initial_delay: Initial delay between retries in seconds.
        max_total_wait: Maximum total time spent waiting (not including
            execution time).

    Returns:
        Decorated function or decorator.
    """
    if max_retries < 0:
        raise ValueError("max_retries must be >= 0")
    if initial_delay < 0:
        raise ValueError("initial_delay must be >= 0")
    if max_total_wait < 0:
        raise ValueError("max_total_wait must be >= 0")

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            total_waited = 0.0
            delay = initial_delay

            for attempt in range(max_retries + 1):  # pragma: no branch
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    if not is_transient_error(exc):
                        raise
                    if attempt == max_retries or total_waited + delay > max_total_wait:
                        raise  # Re-raise with original traceback intact
                    time.sleep(delay)
                    total_waited += delay
                    delay *= 2  # Exponential backoff

            # Unreachable: max_retries >= 0 ensures the loop executes at least once
            # and always ends via return or raise inside the loop body.
            raise AssertionError("unreachable")  # pragma: no cover

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator
