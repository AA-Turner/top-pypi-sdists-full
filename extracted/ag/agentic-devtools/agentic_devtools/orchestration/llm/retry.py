"""Retry handler with jittered exponential backoff."""

from __future__ import annotations

import asyncio
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

from agentic_devtools.orchestration.llm.errors import RateLimitExhaustedError, RetryExhaustedError

T = TypeVar("T")

_SYSTEM_RANDOM = secrets.SystemRandom()


def _secure_uniform(lower: float, upper: float) -> float:
    """Return a cryptographically secure jitter sample."""
    return _SYSTEM_RANDOM.uniform(lower, upper)


# HTTP status codes that trigger retry
RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


@dataclass(frozen=True)
class RetryConfig:
    """Configuration for retry behavior."""

    max_attempts: int = 5
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    jitter_factor: float = 0.5
    total_timeout_seconds: float = 120.0

    def __post_init__(self) -> None:
        if self.max_attempts < 0:
            raise ValueError(f"max_attempts must be non-negative, got {self.max_attempts}")
        if self.base_delay_seconds < 0:
            raise ValueError(f"base_delay_seconds must be non-negative, got {self.base_delay_seconds}")
        if self.max_delay_seconds < 0:
            raise ValueError(f"max_delay_seconds must be non-negative, got {self.max_delay_seconds}")
        if self.jitter_factor < 0:
            raise ValueError(f"jitter_factor must be non-negative, got {self.jitter_factor}")
        if self.total_timeout_seconds < 0:
            raise ValueError(f"total_timeout_seconds must be non-negative, got {self.total_timeout_seconds}")


def _compute_delay(config: RetryConfig, attempt: int) -> float:
    """Compute delay with jittered exponential backoff."""
    clamped_exponential = min(config.base_delay_seconds * (2**attempt), config.max_delay_seconds)
    jitter = _secure_uniform(0, config.jitter_factor * clamped_exponential)
    return min(clamped_exponential + jitter, config.max_delay_seconds)


class RetryHandler:
    """Handles retry logic with jittered exponential backoff."""

    def __init__(self, config: RetryConfig | None = None) -> None:
        self._config = config or RetryConfig()

    @property
    def config(self) -> RetryConfig:
        """Return the retry configuration."""
        return self._config

    async def execute(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute a function with retry logic.

        Args:
            func: Async callable to execute.
            *args: Positional arguments for func.
            **kwargs: Keyword arguments for func.

        Returns:
            Result of the function call.

        Raises:
            RetryExhaustedError: When all retries exhausted.
        """
        if "retry_config" in kwargs:
            raise TypeError(
                "RetryHandler.execute() does not accept 'retry_config'; "
                "it always uses the handler's configured RetryConfig"
            )
        return await execute_with_retry(func, *args, retry_config=self._config, **kwargs)


async def execute_with_retry(
    func: Callable[..., Any],
    *args: Any,
    retry_config: RetryConfig | None = None,
    **kwargs: Any,
) -> Any:
    """Execute an async function with retry on transient failures.

    Retries on HTTP 429, 500, 502, 503, 504 status codes.
    Respects Retry-After header when available.

    Args:
        func: Async callable to execute.
        *args: Positional arguments.
        retry_config: Retry configuration. Named ``retry_config`` (not
            ``config``) so that wrapped functions whose own signature
            includes a ``config`` keyword argument are not silently broken.
        **kwargs: Keyword arguments forwarded verbatim to *func*.

    Returns:
        Result of successful function call.

    Raises:
        RetryExhaustedError: When all retry attempts exhausted or timeout exceeded.
    """
    cfg = retry_config or RetryConfig()
    start_time = time.monotonic()
    last_status_code: int | None = None
    total_wait = 0.0

    for attempt in range(cfg.max_attempts):
        # Check total timeout
        elapsed = time.monotonic() - start_time
        if elapsed >= cfg.total_timeout_seconds:
            raise _build_exhausted_error(
                last_status_code=last_status_code,
                message=f"Total timeout ({cfg.total_timeout_seconds}s) exceeded after {attempt} attempts",
                attempts=attempt,
                total_wait_seconds=total_wait,
            )

        try:
            return await func(*args, **kwargs)
        except Exception as e:
            status_code = _extract_status_code(e)
            last_status_code = status_code

            if status_code not in RETRYABLE_STATUS_CODES:
                raise

            # Compute delay
            delay = _compute_delay(cfg, attempt)

            # Check for Retry-After header
            retry_after = _extract_retry_after(e)
            if retry_after is not None:
                delay = max(delay, retry_after)

            # No sleep needed after the final attempt — raise immediately
            if attempt == cfg.max_attempts - 1:
                raise _build_exhausted_error(
                    last_status_code=last_status_code,
                    message=f"All {cfg.max_attempts} retry attempts exhausted",
                    attempts=cfg.max_attempts,
                    total_wait_seconds=total_wait,
                ) from e

            # Don't wait if we'd exceed timeout
            remaining = cfg.total_timeout_seconds - (time.monotonic() - start_time)
            if delay > remaining:
                raise _build_exhausted_error(
                    last_status_code=last_status_code,
                    message=f"Next retry delay ({delay:.1f}s) would exceed timeout",
                    attempts=attempt + 1,
                    total_wait_seconds=total_wait,
                ) from e

            await asyncio.sleep(delay)
            total_wait += delay

    raise _build_exhausted_error(
        last_status_code=last_status_code,
        message=f"All {cfg.max_attempts} retry attempts exhausted",
        attempts=cfg.max_attempts,
        total_wait_seconds=total_wait,
    )


def _extract_status_code(error: Exception) -> int | None:
    """Extract HTTP status code from exception if available."""
    # openai SDK exceptions have status_code attribute
    status_code = getattr(error, "status_code", None)
    if status_code is not None:
        return status_code
    # httpx exceptions
    response = getattr(error, "response", None)
    if response is not None and hasattr(response, "status_code"):
        return response.status_code
    return None


def _extract_retry_after(error: Exception) -> float | None:
    """Extract Retry-After header value from exception if available."""
    if hasattr(error, "response") and hasattr(error.response, "headers"):
        headers = error.response.headers
        retry_after = headers.get("Retry-After") or headers.get("retry-after")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass
    return None


def _build_exhausted_error(
    *,
    last_status_code: int | None,
    message: str,
    attempts: int,
    total_wait_seconds: float,
) -> RetryExhaustedError:
    """Return a specific retry-exhausted error class based on the last status code."""
    if last_status_code == 429:
        return RateLimitExhaustedError(
            message,
            attempts=attempts,
            total_wait_seconds=total_wait_seconds,
            last_status_code=last_status_code,
        )
    return RetryExhaustedError(
        message,
        attempts=attempts,
        total_wait_seconds=total_wait_seconds,
        last_status_code=last_status_code,
    )
