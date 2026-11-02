from __future__ import annotations

import random

from matrx_graph.types.primitives import BackoffStrategy, RetryPolicy


def compute_backoff_ms(policy: RetryPolicy, attempt: int) -> int:
    """How long to wait before the next attempt, in milliseconds.

    `attempt` is the attempt number that just failed (1-indexed). The first
    retry uses backoff for attempt=1, the second uses attempt=2, etc.

    Capped at `policy.max_delay_ms`. Jitter is uniform in [0.5x, 1.5x] of the
    base value, then re-capped.
    """
    base = policy.initial_delay_ms
    if base <= 0:
        return 0

    match policy.backoff:
        case BackoffStrategy.NONE:
            return 0
        case BackoffStrategy.FIXED:
            value = base
        case BackoffStrategy.LINEAR:
            value = base * attempt
        case BackoffStrategy.EXPONENTIAL:
            value = base * (2 ** (attempt - 1))
        case BackoffStrategy.EXPONENTIAL_JITTER:
            raw = base * (2 ** (attempt - 1))
            value = int(raw * random.uniform(0.5, 1.5))
        case _:
            value = base

    return min(value, policy.max_delay_ms)


def should_retry(policy: RetryPolicy, attempt: int, error_type: str) -> bool:
    """True if a failed attempt should trigger another attempt.

    A node is retryable if it hasn't exhausted attempts AND the error type
    is either explicitly in `retry_on` or `retry_on` is empty (meaning
    retry-anything semantics).
    """
    if attempt >= policy.max_attempts:
        return False
    if not policy.retry_on:
        return True
    return error_type in policy.retry_on
