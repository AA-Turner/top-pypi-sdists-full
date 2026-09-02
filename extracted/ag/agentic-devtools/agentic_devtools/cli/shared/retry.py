"""Shared exponential backoff retry utility.

Defines ``RetryableError``, ``ProviderRateLimitError``, and
``retry_with_backoff`` for use across the package.  Modules outside the
``ci`` package (e.g. ``github/issue_dedup_io``) import from here directly.
The ``agentic_devtools.cli.ci`` package also imports these exception classes
from this module so that both packages share a single canonical definition.
"""

from __future__ import annotations

import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from math import isfinite
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

_SYSTEM_RANDOM = secrets.SystemRandom()


def _secure_uniform(lower: float, upper: float) -> float:
    """Return a cryptographically secure uniform jitter sample."""
    return _SYSTEM_RANDOM.uniform(lower, upper)


# Shared defaults (intentionally different from CI-specific defaults)
DEFAULT_INITIAL_DELAY: float = 1.0
DEFAULT_MAX_DELAY: float = 60.0
DEFAULT_MAX_RETRIES: int = 3
DEFAULT_JITTER_FACTOR: float = 0.1
DEFAULT_RATE_LIMIT_FALLBACK_DELAY: float = 60.0
DEFAULT_RATE_LIMIT_SAFETY_MARGIN: float = 10.0
DEFAULT_RATE_LIMIT_MAX_DELAY: float = 24 * 60 * 60


@dataclass(frozen=True)
class RateLimitDelay:
    """The selected rate-limit source and bounded time at which work may resume."""

    source: str
    delay_seconds: float
    resume_at: float


@dataclass(frozen=True)
class RateLimitMetadata:
    """Sanitized provider timing and identity metadata carried across retries."""

    retry_after_seconds: float | None = None
    reset_timestamp: float | None = None
    remaining: int | None = None
    provider: str = ""
    credential_identity: str = ""
    source: str = ""


def calculate_rate_limit_delay(
    *,
    retry_after_seconds: float | None = None,
    reset_timestamp: float | None = None,
    now: float | None = None,
    fallback_delay: float = DEFAULT_RATE_LIMIT_FALLBACK_DELAY,
    safety_margin: float = DEFAULT_RATE_LIMIT_SAFETY_MARGIN,
    max_delay: float = DEFAULT_RATE_LIMIT_MAX_DELAY,
) -> RateLimitDelay:
    """Calculate a bounded, deterministic provider cooldown.

    ``Retry-After`` takes precedence over an absolute reset timestamp, which
    takes precedence over the fallback. Invalid metadata is ignored.
    """
    current = time.time() if now is None else float(now)
    if not isfinite(current):
        raise ValueError("now must be finite")
    if (
        not all(isfinite(value) for value in (fallback_delay, safety_margin, max_delay))
        or fallback_delay < 0
        or safety_margin < 0
        or max_delay < 0
    ):
        raise ValueError("rate-limit delay configuration must be non-negative")

    delay: float
    source: str
    try:
        retry_after = float(retry_after_seconds) if retry_after_seconds is not None else None
    except (TypeError, ValueError):
        retry_after = None
    try:
        reset = float(reset_timestamp) if reset_timestamp is not None else None
    except (TypeError, ValueError):
        reset = None
    if retry_after is not None and isfinite(retry_after) and retry_after >= 0:
        delay = retry_after + safety_margin
        source = "retry-after"
    elif reset is not None and isfinite(reset) and reset > 0:
        delay = max(0.0, reset - current) + safety_margin
        source = "x-ratelimit-reset"
    else:
        delay = fallback_delay + safety_margin
        source = "fallback"

    delay = max(1.0, min(delay, max_delay if max_delay >= 1.0 else 1.0))
    return RateLimitDelay(source=source, delay_seconds=delay, resume_at=current + delay)


class RetryableError(Exception):
    """Wrapper indicating a retryable failure.

    Attributes:
        retry_after: Seconds to wait before retrying (from Retry-After header).
            None means use exponential backoff.
    """

    def __init__(
        self,
        message: str = "",
        retry_after: float | None = None,
        *,
        reset_timestamp: float | None = None,
        remaining: int | None = None,
        provider: str = "",
        credential_identity: str = "",
        source: str = "",
        is_rate_limit: bool = False,
    ) -> None:
        super().__init__(message)
        self.retry_after = retry_after
        self.reset_timestamp = reset_timestamp
        self.remaining = remaining
        self.provider = provider
        self.credential_identity = credential_identity
        self.source = source
        self.is_rate_limit = is_rate_limit

    @property
    def metadata(self) -> RateLimitMetadata:
        """Return the sanitized metadata associated with this failure."""
        return RateLimitMetadata(
            retry_after_seconds=self.retry_after,
            reset_timestamp=self.reset_timestamp,
            remaining=self.remaining,
            provider=self.provider,
            credential_identity=self.credential_identity,
            source=self.source,
        )


class ProviderRateLimitError(Exception):
    """Raised when a provider rate limit is exhausted after retries.

    Attributes:
        retry_after_seconds: Seconds until the rate limit resets (if known).
    """

    def __init__(
        self,
        retry_after_seconds: float | None = None,
        *,
        reset_timestamp: float | None = None,
        remaining: int | None = None,
        provider: str = "",
        credential_identity: str = "",
        source: str = "",
        is_rate_limit: bool = True,
    ) -> None:
        self.retry_after_seconds = retry_after_seconds
        self.reset_timestamp = reset_timestamp
        self.remaining = remaining
        self.provider = provider
        self.credential_identity = credential_identity
        self.source = source
        self.is_rate_limit = is_rate_limit
        msg = "Provider rate limit exhausted"
        if retry_after_seconds is not None:
            msg += f" (resets in {retry_after_seconds:.0f}s)"
        if provider and credential_identity:
            msg += f" [{provider}:{credential_identity}]"
        super().__init__(msg)

    @property
    def metadata(self) -> RateLimitMetadata:
        """Return the sanitized metadata associated with this failure."""
        return RateLimitMetadata(
            retry_after_seconds=self.retry_after_seconds,
            reset_timestamp=self.reset_timestamp,
            remaining=self.remaining,
            provider=self.provider,
            credential_identity=self.credential_identity,
            source=self.source,
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


def _merge_rate_limit_error_metadata(existing: RetryableError | None, candidate: RetryableError) -> RetryableError:
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


def retry_with_backoff(
    *,
    initial_delay: float = DEFAULT_INITIAL_DELAY,
    max_delay: float = DEFAULT_MAX_DELAY,
    max_retries: int = DEFAULT_MAX_RETRIES,
    jitter_factor: float = DEFAULT_JITTER_FACTOR,
    retryable_exceptions: tuple[type[Exception], ...] = (),
) -> Callable[[F], F]:
    """Decorator that retries a function with exponential backoff on RetryableError.

    Args:
        initial_delay: Initial delay in seconds before first retry.
        max_delay: Maximum delay cap in seconds.
        max_retries: Maximum number of retry attempts.
        jitter_factor: Jitter factor (0.0-1.0) applied to delay.
        retryable_exceptions: Additional exception types to retry on
            (besides ``RetryableError``). These are caught and wrapped
            internally but do not provide ``retry_after``.

    Returns:
        Decorated function that retries on ``RetryableError``.

    Raises:
        ProviderRateLimitError: When rate-limit ``RetryableError`` retries are
            exhausted.
        RetryableError: When a non-rate-limit ``RetryableError`` exhausts its
            retries.
        Exception: When one of ``retryable_exceptions`` exhausts its retries,
            the original exception is re-raised unchanged.
    """
    if not isfinite(initial_delay):
        raise ValueError(f"initial_delay must be finite, got {initial_delay}")
    if not isfinite(max_delay):
        raise ValueError(f"max_delay must be finite, got {max_delay}")
    if not isfinite(jitter_factor):
        raise ValueError(f"jitter_factor must be finite, got {jitter_factor}")
    if initial_delay < 0:
        raise ValueError(f"initial_delay must be >= 0, got {initial_delay}")
    if max_delay < 0:
        raise ValueError(f"max_delay must be >= 0, got {max_delay}")
    if max_retries < 0:
        raise ValueError(f"max_retries must be >= 0, got {max_retries}")
    if jitter_factor < 0 or jitter_factor > 1:
        raise ValueError(f"jitter_factor must be between 0 and 1, got {jitter_factor}")

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            catchable = (RetryableError, *retryable_exceptions)
            rate_limit_metadata: RetryableError | None = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except catchable as exc:  # type: ignore[misc]
                    effective_exc = exc
                    if isinstance(exc, RetryableError) and exc.is_rate_limit:
                        rate_limit_metadata = _merge_rate_limit_error_metadata(rate_limit_metadata, exc)
                        effective_exc = rate_limit_metadata

                    if attempt >= max_retries:
                        if isinstance(effective_exc, RetryableError) and effective_exc.is_rate_limit:
                            raise _provider_rate_limit_error_from_retryable(effective_exc) from exc
                        raise

                    # Honor Retry-After if provided
                    retry_after = getattr(effective_exc, "retry_after", None)
                    reset_delay = None
                    if isinstance(effective_exc, RetryableError) and effective_exc.reset_timestamp is not None:
                        try:
                            reset_delay = float(effective_exc.reset_timestamp) - time.time()
                        except (TypeError, ValueError):
                            pass
                    if retry_after is not None:
                        if (
                            isinstance(effective_exc, RetryableError)
                            and effective_exc.is_rate_limit
                            and retry_after > max_delay
                        ):
                            raise _provider_rate_limit_error_from_retryable(effective_exc) from exc
                        wait_time = retry_after
                    elif (
                        isinstance(effective_exc, RetryableError)
                        and effective_exc.is_rate_limit
                        and reset_delay is not None
                        and isfinite(reset_delay)
                        and reset_delay > 0
                        and reset_delay + DEFAULT_RATE_LIMIT_SAFETY_MARGIN > max_delay
                    ):
                        raise _provider_rate_limit_error_from_retryable(effective_exc) from exc
                    elif (
                        isinstance(effective_exc, RetryableError)
                        and effective_exc.is_rate_limit
                        and reset_delay is not None
                        and isfinite(reset_delay)
                    ):
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
