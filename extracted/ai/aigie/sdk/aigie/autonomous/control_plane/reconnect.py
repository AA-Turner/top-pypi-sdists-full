"""Exponential backoff with jitter for gRPC reconnect logic (ADR 0001 §3.5).

BackoffPolicy is intentionally stateful: each call to next_delay_seconds()
advances the internal attempt counter.  Call reset() on successful connect.
"""

from __future__ import annotations

import random
from typing import Literal


class BackoffPolicy:
    """Exponential backoff with optional full jitter.

    Parameters
    ----------
    initial_ms:
        Starting delay in milliseconds (before jitter).  Default: 500.
    max_ms:
        Maximum delay in milliseconds (cap before jitter).  Default: 30_000.
    multiplier:
        Exponential growth factor applied each attempt.  Default: 2.0.
    jitter:
        ``"full"`` — uniform random in ``[0, computed_delay]`` (AWS blog convention).
        ``"none"`` — no jitter; deterministic delay (useful for tests).
    """

    def __init__(
        self,
        initial_ms: int = 500,
        max_ms: int = 30_000,
        multiplier: float = 2.0,
        jitter: Literal["full", "none"] = "full",
    ) -> None:
        self._initial_ms = initial_ms
        self._max_ms = max_ms
        self._multiplier = multiplier
        self._jitter = jitter
        self._attempt: int = 0

    def next_delay_seconds(self) -> float:
        """Return next backoff delay in seconds and advance internal state."""
        computed = min(
            self._initial_ms * (self._multiplier**self._attempt),
            self._max_ms,
        )
        self._attempt += 1
        # S311: random.uniform is intentionally non-cryptographic here (backoff jitter).
        delay_ms = random.uniform(0.0, computed) if self._jitter == "full" else computed  # noqa: S311
        return delay_ms / 1000.0

    def reset(self) -> None:
        """Reset attempt counter (call on successful connect)."""
        self._attempt = 0

    @property
    def attempt(self) -> int:
        """Number of delay calls since last reset (read-only, useful for tests)."""
        return self._attempt
