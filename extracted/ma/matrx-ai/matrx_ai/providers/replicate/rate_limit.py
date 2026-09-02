"""Client-side rate limiting for outbound Replicate prediction creates.

Replicate documents a ceiling of 600 prediction-creates / minute (other
endpoints 3000/min). We bound ourselves *below* that so fan-out + retries can
never pin the account on HTTP 429 — the same failure mode Fastino hit before
its token bucket (see ``providers/fastino/client.py``).

``replicate.async_run`` = create prediction + poll. Only the create counts
against the 600/min budget, so every image/video ``_call_provider`` acquires
one token before going out (including executor retries).
"""

from __future__ import annotations

import asyncio
import time

from matrx_utils import vcprint

# Provider ceiling: 600 prediction creates / minute
# (https://replicate.com/docs/topics/predictions/rate-limits).
#
# Burst bound: BURST + PER_MINUTE ≤ CEILING.
# 560 + 20 = 580 worst-case/min — 20 under the documented limit for clock skew
# and Replicate's own window accounting. Burst stays small so a fan-out can't
# front-load the whole window.
REPLICATE_RATE_LIMIT_PER_MINUTE: float = 560.0
REPLICATE_RATE_LIMIT_BURST: float = 20.0


class _AsyncTokenBucket:
    """Process-wide monotonic-clock token bucket for outbound Replicate creates."""

    def __init__(self, rate_per_sec: float, capacity: float) -> None:
        self._rate = max(rate_per_sec, 0.0001)
        self._capacity = max(capacity, 1.0)
        self._tokens = self._capacity
        self._updated = time.monotonic()
        self._lock: asyncio.Lock | None = None
        self._warned = False

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._updated
        if elapsed > 0:
            self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
            self._updated = now

    async def acquire(self) -> None:
        if self._lock is None:
            self._lock = asyncio.Lock()
        async with self._lock:
            while True:
                self._refill()
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
                deficit = 1.0 - self._tokens
                wait_s = deficit / self._rate
                if not self._warned:
                    self._warned = True
                    vcprint(
                        f"⏳ Replicate rate limiter ACTIVE — throttling prediction "
                        f"creates to {self._rate * 60:.0f}/min (under the 600/min "
                        f"provider ceiling). Queued ~{wait_s:.1f}s.",
                        color="yellow",
                        verbose=True,
                    )
                await asyncio.sleep(wait_s)


_RATE_LIMITER = _AsyncTokenBucket(
    rate_per_sec=REPLICATE_RATE_LIMIT_PER_MINUTE / 60.0,
    capacity=REPLICATE_RATE_LIMIT_BURST,
)


async def acquire_replicate_slot() -> None:
    """Block until the shared budget grants one prediction-create token."""
    await _RATE_LIMITER.acquire()
