"""Composable retry mechanism with context accumulation.

Provides ``with_retry()`` — a wrapper that re-invokes a callable on failure,
accumulating prior failure reasons into a ``RetryContext`` so downstream
reasoning attempts can learn from earlier mistakes.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar

from .exceptions import RetryExhaustedError

T = TypeVar("T")

DEFAULT_MAX_RETRIES = 2
"""Default maximum number of retry attempts (not counting the initial try)."""


@dataclass
class RetryContext:
    """Accumulated metadata across retry attempts.

    Attributes:
        attempt: Current attempt number (0-based).
        max_retries: Maximum retries allowed.
        failure_reasons: List of failure descriptions from prior attempts.
    """

    attempt: int = 0
    max_retries: int = DEFAULT_MAX_RETRIES
    failure_reasons: list[str] = field(default_factory=list)

    @property
    def is_first_attempt(self) -> bool:
        """Return ``True`` if this is the first attempt."""
        return self.attempt == 0

    @property
    def has_retries_remaining(self) -> bool:
        """Return ``True`` if more retry attempts are allowed."""
        return self.attempt < self.max_retries


def with_retry(
    fn: Callable[[RetryContext], T],
    *,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> T:
    """Execute *fn* with retry and context accumulation.

    *fn* receives a ``RetryContext`` on each attempt.  If *fn* raises any
    ``Exception``, the failure reason is appended to the context and the
    next attempt is started.  After *max_retries* failures (plus the
    initial attempt), ``RetryExhaustedError`` is raised.

    Returns the first successful result from *fn*.
    """
    if max_retries < 0:
        raise ValueError(f"max_retries must be >= 0, got {max_retries}")
    ctx = RetryContext(attempt=0, max_retries=max_retries)
    last_error = ""

    for attempt in range(max_retries + 1):
        ctx.attempt = attempt
        try:
            return fn(ctx)
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
            ctx.failure_reasons.append(last_error)

    raise RetryExhaustedError(
        f"All {max_retries + 1} attempts failed",
        attempts=max_retries + 1,
        last_error=last_error,
    )
