"""Exponential backoff retry utility for CI provider operations.

Implements retry with jitter for transient failures. Supports an optional
``retry_after`` value on ``RetryableError`` when callers supply it;
otherwise falls back to exponential backoff. Exhausted rate-limit retries raise
``ProviderRateLimitError``; exhausted non-rate-limit retries re-raise the
original ``RetryableError``.

This module imports ``RetryableError`` and ``ProviderRateLimitError`` from
``agentic_devtools.cli.shared.retry`` (the canonical location) and
provides a CI-specific ``retry_with_backoff`` decorator with its own
defaults (``max_retries=5``, ``jitter_factor=0.5``).
"""

from __future__ import annotations

import secrets
import time
from collections.abc import Callable
from functools import wraps
from math import isfinite
from typing import Any, TypeVar

from agentic_devtools.cli.shared.retry import (
    ProviderRateLimitError,
    RetryableError,
)

F = TypeVar("F", bound=Callable[..., Any])

_SYSTEM_RANDOM = secrets.SystemRandom()


def _validate_non_negative_finite(name: str, value: float) -> None:
    """Reject negative or non-finite timing values at decorator construction time."""
    if not isfinite(value):
        raise ValueError(f"{name} must be finite, got {value}")
    if value < 0:
        raise ValueError(f"{name} must be >= 0, got {value}")


def _secure_uniform(lower: float, upper: float) -> float:
    """Return a cryptographically secure uniform jitter sample."""
    return _SYSTEM_RANDOM.uniform(lower, upper)


def _as_non_negative_finite_float(value: Any) -> float | None:
    """Return ``value`` as a non-negative finite float, else ``None``."""
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not isfinite(numeric) or numeric < 0:
        return None
    return numeric


def _as_non_negative_int(value: Any) -> int | None:
    """Return ``value`` as a non-negative int, else ``None``."""
    try:
        numeric = int(value)
    except (TypeError, ValueError):
        return None
    if numeric < 0:
        return None
    return numeric


def _merge_rate_limit_error_metadata(
    existing: RetryableError | None,
    candidate: RetryableError,
) -> RetryableError:
    """Keep the most conservative rate-limit metadata observed across retries."""
    if existing is None:
        return candidate

    existing_retry_after = _as_non_negative_finite_float(existing.retry_after)
    candidate_retry_after = _as_non_negative_finite_float(candidate.retry_after)
    retry_after = max((v for v in (existing_retry_after, candidate_retry_after) if v is not None), default=None)

    existing_reset = _as_non_negative_finite_float(existing.reset_timestamp)
    candidate_reset = _as_non_negative_finite_float(candidate.reset_timestamp)
    reset_timestamp = max((v for v in (existing_reset, candidate_reset) if v is not None), default=None)

    existing_remaining = _as_non_negative_int(existing.remaining)
    candidate_remaining = _as_non_negative_int(candidate.remaining)
    remaining = min((v for v in (existing_remaining, candidate_remaining) if v is not None), default=None)

    return RetryableError(
        str(candidate),
        retry_after=retry_after,
        reset_timestamp=reset_timestamp,
        remaining=remaining,
        provider=existing.provider or candidate.provider,
        credential_identity=existing.credential_identity or candidate.credential_identity,
        source=existing.source or candidate.source,
        is_rate_limit=True,
    )


def _provider_rate_limit_error_from_retryable(exc: RetryableError) -> ProviderRateLimitError:
    """Re-raise retryable rate-limit metadata as the terminal provider error."""
    return ProviderRateLimitError(
        retry_after_seconds=exc.retry_after,
        reset_timestamp=exc.reset_timestamp,
        remaining=exc.remaining,
        provider=exc.provider,
        credential_identity=exc.credential_identity,
        source=exc.source,
        is_rate_limit=exc.is_rate_limit,
    )


# Defaults matching plan §4.1
DEFAULT_INITIAL_DELAY: float = 1.0
DEFAULT_MAX_DELAY: float = 60.0
DEFAULT_MAX_RETRIES: int = 5
DEFAULT_JITTER_FACTOR: float = 0.5
DEFAULT_RATE_LIMIT_SAFETY_MARGIN: float = 10.0

# Re-export so existing imports continue to work
__all__ = [
    "DEFAULT_INITIAL_DELAY",
    "DEFAULT_JITTER_FACTOR",
    "DEFAULT_MAX_DELAY",
    "DEFAULT_MAX_RETRIES",
    "RetryableError",
    "retry_with_backoff",
]


def retry_with_backoff(
    *,
    initial_delay: float = DEFAULT_INITIAL_DELAY,
    max_delay: float = DEFAULT_MAX_DELAY,
    max_retries: int = DEFAULT_MAX_RETRIES,
    jitter_factor: float = DEFAULT_JITTER_FACTOR,
) -> Callable[[F], F]:
    """Decorator that retries a function with exponential backoff on RetryableError.

    Args:
        initial_delay: Initial delay in seconds before first retry.
        max_delay: Maximum delay cap in seconds.
        max_retries: Maximum number of retry attempts.
        jitter_factor: Jitter factor (0.0-1.0) applied to delay.

    Returns:
        Decorated function that retries on ``RetryableError``.

    Raises:
        ProviderRateLimitError: When rate-limit retries are exhausted.
        RetryableError: When non-rate-limit retries are exhausted.
    """
    _validate_non_negative_finite("initial_delay", initial_delay)
    _validate_non_negative_finite("max_delay", max_delay)
    if max_retries < 0:
        raise ValueError(f"max_retries must be >= 0, got {max_retries}")
    if not isfinite(jitter_factor):
        raise ValueError(f"jitter_factor must be finite, got {jitter_factor}")
    if jitter_factor < 0 or jitter_factor > 1:
        raise ValueError(f"jitter_factor must be between 0 and 1, got {jitter_factor}")

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            rate_limit_metadata: RetryableError | None = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except RetryableError as exc:
                    effective_exc = exc
                    if exc.is_rate_limit:
                        rate_limit_metadata = _merge_rate_limit_error_metadata(rate_limit_metadata, exc)
                        effective_exc = rate_limit_metadata

                    reset_delay: float | None = None
                    if effective_exc.reset_timestamp is not None:
                        try:
                            candidate = float(effective_exc.reset_timestamp) - time.time()
                        except (TypeError, ValueError):
                            pass
                        else:
                            if isfinite(candidate):
                                reset_delay = candidate
                    if effective_exc.is_rate_limit and (
                        (effective_exc.retry_after is not None and effective_exc.retry_after > max_delay)
                        or (
                            effective_exc.retry_after is None
                            and reset_delay is not None
                            and isfinite(reset_delay)
                            and reset_delay > 0
                            and reset_delay + DEFAULT_RATE_LIMIT_SAFETY_MARGIN > max_delay
                        )
                    ):
                        raise _provider_rate_limit_error_from_retryable(effective_exc) from exc
                    if attempt >= max_retries:
                        if not effective_exc.is_rate_limit:
                            raise
                        raise _provider_rate_limit_error_from_retryable(effective_exc) from exc

                    # Honor Retry-After if provided
                    if effective_exc.retry_after is not None:
                        wait_time = effective_exc.retry_after
                    elif effective_exc.is_rate_limit and reset_delay is not None and isfinite(reset_delay):
                        wait_time = min(max(0.0, reset_delay) + DEFAULT_RATE_LIMIT_SAFETY_MARGIN, max_delay)
                    else:
                        # Exponential backoff with jitter
                        jitter = _secure_uniform(0, jitter_factor * delay)
                        wait_time = min(delay + jitter, max_delay)
                        delay = min(delay * 2, max_delay)

                    time.sleep(wait_time)

            # Unreachable: loop always returns or raises
            raise AssertionError("Unreachable")  # pragma: no cover

        return wrapper  # type: ignore[return-value]

    return decorator
