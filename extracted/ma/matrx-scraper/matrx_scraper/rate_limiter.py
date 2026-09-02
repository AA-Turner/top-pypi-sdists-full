"""Per-host politeness — ONE implementation for every lane that fetches.

Two shapes of politeness live here, over ONE shared per-host memory:

* ``acquire(url)`` — token bucket. What the crawler wants: N workers on one
  host must not exceed ``host_rps`` in aggregate, but they may run concurrently
  up to the burst.
* ``slot(url, min_interval=...)`` — serialize + end-gap. What the research
  auto-scraper wants: fetches to the SAME host run one at a time and are
  separated by at least ``min_interval`` measured from the END of the previous
  request, so a slow response never stacks the next one on top of it.

The reason they share a module rather than each lane keeping a private gate:
**a 429 learned on one lane must throttle the other.** ``throttle_host`` records
a per-host backoff FACTOR in a process-wide store (`_SHARED_THROTTLES`), and
every ``HostRateLimiter`` — whatever its own baseline — multiplies its rate by
that factor and divides its interval by it. So the crawler backing iopbm.com off
to half rate also doubles the research scraper's gap on iopbm.com, and vice
versa. A factor is used rather than an absolute rps precisely because the lanes
have different baselines (4 rps vs one request every 2s); the *lesson* is
"this host wants half as much", not "this host wants 2 rps".

Throttles expire after ``THROTTLE_TTL_SECONDS`` without a new 429, so a host
that had one bad minute is not penalised for the life of the process.

Standalone — no sibling matrx imports.
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from urllib.parse import urlparse

from matrx_scraper.utils.url import extract_domain

logger = logging.getLogger(__name__)

# HTTP statuses that mean "the origin is throttling us", not "the page is bad".
RATE_LIMIT_STATUSES = frozenset({429, 503})

# How long a learned backoff survives without a fresh 429. Long enough to shape
# a whole crawl/research run, short enough that one bad minute doesn't pin a
# host at half rate for the life of the process.
THROTTLE_TTL_SECONDS = 900.0


def host_key(url: str) -> str:
    """THE per-host politeness key — one key, so every lane shares one budget.

    Lowercased registrable host with any leading ``www.`` removed, because
    ``www.x.com`` and ``x.com`` are one server and keying on the raw netloc lets
    a burst walk straight through by alternating the prefix. Deeper subdomains
    are deliberately NOT collapsed: ``blog.x.com`` and ``shop.x.com`` are often
    different infrastructure, and on shared hosts (``*.github.io``) they are
    different owners entirely. Returns "" when no host can be resolved — the
    caller then does no pacing rather than lumping every unparseable URL into
    one shared bucket.
    """
    host = (extract_domain(url) or urlparse(url).hostname or "").lower().strip()
    if "/" in host or " " in host:
        # extract_domain falls back to echoing its input when tldextract can't
        # parse it; that is not a host.
        return ""
    if ":" in host:
        host = host.split(":", 1)[0]
    if host.startswith("www."):
        host = host[4:]
    return host


@dataclass
class HostBucket:
    capacity: float  # max tokens (e.g. burst limit)
    refill_per_sec: float  # steady-state RPS
    tokens: float
    updated_at: float


@dataclass
class _HostThrottle:
    """A learned, cross-lane backoff for one host."""

    factor: float  # multiplier on every lane's baseline rate (<= 1.0)
    expires_at: float  # wall clock (time.monotonic)
    reason: str


_SHARED_THROTTLES: dict[str, _HostThrottle] = {}


def _live_factor(key: str) -> float:
    throttle = _SHARED_THROTTLES.get(key)
    if throttle is None:
        return 1.0
    if throttle.expires_at <= time.monotonic():
        _SHARED_THROTTLES.pop(key, None)
        return 1.0
    return throttle.factor


def shared_throttles() -> dict[str, float]:
    """Live per-host backoff factors (expired entries omitted). For ops/tests."""
    return {key: _live_factor(key) for key in list(_SHARED_THROTTLES) if _live_factor(key) < 1.0}


def clear_shared_throttles() -> None:
    """Drop every learned backoff. Tests only — there is no production reset."""
    _SHARED_THROTTLES.clear()


class HostRateLimiter:
    """Token-bucket per host, configurable globally and per-host.

    Defaults are conservative — small burst, low steady RPS — which is what
    we want when crawling our own sites. Override per-host via `set_host`
    when a particular destination tolerates more aggression.
    """

    def __init__(
        self,
        *,
        default_rps: float = 4.0,
        default_burst: float = 8.0,
        max_wait_seconds: float = 30.0,
    ) -> None:
        self.default_rps = default_rps
        self.default_burst = default_burst
        self.max_wait_seconds = max_wait_seconds
        self._buckets: dict[str, HostBucket] = {}
        self._base: dict[str, tuple[float, float]] = {}  # host → (rps, burst) baseline
        # Rates decided by a HostRamp. Separate from `_base` on purpose —
        # see set_ramp_rate() for the two bugs that separation prevents.
        self._ramp_rates: dict[str, tuple[float, float]] = {}
        self._lock = asyncio.Lock()
        # slot() state: one gate per host, plus the earliest next start time.
        self._gates: dict[str, asyncio.Lock] = {}
        self._next_allowed_at: dict[str, float] = {}
        # Stats for observability
        self._stats: dict[str, dict[str, float]] = {}

    # -- configuration ------------------------------------------------------

    def set_host(self, host: str, rps: float, burst: float | None = None) -> None:
        """Override the per-host BASELINE rate. Takes effect on the next acquire()."""
        self._base[host_key(host) or host.lower()] = (
            float(rps),
            float(burst) if burst is not None else float(rps) * 2.0,
        )

    def set_ramp_rate(self, host: str, rps: float, burst: float | None = None) -> None:
        """Set the rate a :class:`~matrx_scraper.host_pacing.HostRamp` decided.

        Kept in a SEPARATE store from the baseline, and this is load-bearing in
        two directions:

        * A ramp rate WINS over the baseline and is **not** scaled by the shared
          throttle factor. The ramp already applied its own back-off for every
          limit signal it saw; multiplying that result by the factor pays for
          one 429 twice and spirals a host to the floor in three hits instead of
          settling just under its limit.
        * The baseline stays untouched, so ``throttle_host`` still computes its
          ``min_rps`` floor against the host's ORIGINAL rate. Writing ramp rates
          into ``_base`` made that floor collapse — once the ramp had backed a
          host down to 0.25 rps, ``min_rps=0.5`` produced a floor factor of 1.0
          and **no cross-lane throttle was recorded at all**, silently cutting
          the research and SEO lanes out of everything the crawler learned.
        """
        key = host_key(host) or host.lower()
        self._ramp_rates[key] = (
            float(rps),
            float(burst) if burst is not None else max(1.0, float(rps) * 2.0),
        )

    def _baseline(self, key: str) -> tuple[float, float]:
        return self._base.get(key, (self.default_rps, self.default_burst))

    def _effective(self, key: str) -> tuple[float, float]:
        """The rate in force for `key` — a ramp decision, else baseline × backoff."""
        ramped = self._ramp_rates.get(key)
        if ramped is not None:
            return ramped
        rps, burst = self._baseline(key)
        factor = _live_factor(key)
        if factor >= 1.0:
            return rps, burst
        return max(rps * factor, 0.001), max(1.0, min(burst, rps * factor * 2.0))

    @property
    def _overrides(self) -> dict[str, tuple[float, float]]:
        """Effective (rps, burst) for every host this limiter knows about.

        Read-only view kept for callers/tests that inspected the old dict; write
        through `set_host` (baseline) or `throttle_host` (learned backoff).
        """
        keys = (
            set(self._base)
            | set(self._ramp_rates)
            | {k for k in _SHARED_THROTTLES if _live_factor(k) < 1.0}
        )
        return {key: self._effective(key) for key in keys}

    # -- learning -----------------------------------------------------------

    def throttle_host(
        self, url: str, *, factor: float = 0.5, min_rps: float = 0.5, reason: str = "rate_limited"
    ) -> tuple[float, float]:
        """Back a host off after IT rate-limited US (HTTP 429/503).

        Multiplies the host's current rate by ``factor`` (floored so the
        effective rate never drops below ``min_rps``) and shrinks burst to
        match, so every worker immediately slows on that host. Adaptive:
        repeated 429s compound the throttle until they stop.

        The backoff is recorded PROCESS-WIDE as a factor, so every other lane —
        including ones with a completely different baseline, like the research
        scraper's one-request-per-2s pacing — slows on this host too. Returns
        the new effective ``(rps, burst)`` for THIS limiter. Idempotent-safe
        under concurrent 429s (two callers throttling to the same value is
        harmless).
        """
        key = host_key(url)
        if not key:
            return self.default_rps, self.default_burst
        base_rps, _ = self._baseline(key)
        floor_factor = min(1.0, min_rps / base_rps) if base_rps > 0 else 1.0
        new_factor = max(_live_factor(key) * factor, floor_factor)
        _SHARED_THROTTLES[key] = _HostThrottle(
            factor=new_factor,
            expires_at=time.monotonic() + THROTTLE_TTL_SECONDS,
            reason=reason,
        )
        return self._effective(key)

    def observe_status(self, url: str, status: int | None, **kwargs: float) -> bool:
        """Record a response status; throttle the host iff it means "slow down".

        One place decides which statuses are the origin throttling us, so every
        lane learns from the same signal. Returns True when a throttle was
        applied.
        """
        if status not in RATE_LIMIT_STATUSES:
            return False
        new_rps, _ = self.throttle_host(url, reason=f"http_{status}", **kwargs)
        logger.warning(
            "host %s returned HTTP %s — throttled to %.2f rps (shared across lanes)",
            host_key(url),
            status,
            new_rps,
        )
        return True

    def stats(self) -> dict[str, dict[str, float]]:
        """Return per-host counters (acquires, total_wait_ms). Cheap to read."""
        return {h: dict(s) for h, s in self._stats.items()}

    # -- pacing -------------------------------------------------------------

    async def acquire(self, url: str) -> float:
        """Wait until a request to *url*'s host is allowed.

        Returns the number of seconds spent waiting (0 when no waiting needed).
        Raises TimeoutError if the wait would exceed `max_wait_seconds`
        — the caller can decide whether to skip or retry.
        """
        host = host_key(url)
        if not host:
            return 0.0

        waited = 0.0
        start = time.monotonic()

        while True:
            now = time.monotonic()
            rps, burst = self._effective(host)
            async with self._lock:
                bucket = self._buckets.get(host)
                if bucket is None:
                    bucket = HostBucket(
                        capacity=burst,
                        refill_per_sec=rps,
                        tokens=burst,
                        updated_at=now,
                    )
                    self._buckets[host] = bucket
                else:
                    # Re-apply the effective rate (baseline or learned backoff)
                    bucket.capacity = burst
                    bucket.refill_per_sec = rps
                    elapsed = now - bucket.updated_at
                    if elapsed > 0:
                        bucket.tokens = min(bucket.capacity, bucket.tokens + elapsed * rps)
                        bucket.updated_at = now

                if bucket.tokens >= 1.0:
                    bucket.tokens -= 1.0
                    s = self._stats.setdefault(host, {"acquires": 0.0, "total_wait_ms": 0.0})
                    s["acquires"] += 1
                    s["total_wait_ms"] += waited * 1000.0
                    return waited

                deficit = 1.0 - bucket.tokens
                wait_for = deficit / max(rps, 0.001)

            if waited + wait_for > self.max_wait_seconds:
                raise TimeoutError(
                    f"rate limit for host {host!r} exceeded max_wait_seconds={self.max_wait_seconds}",
                )
            await asyncio.sleep(min(wait_for, 0.5))
            waited = time.monotonic() - start

    @asynccontextmanager
    async def slot(
        self,
        url: str,
        *,
        min_interval: float,
        jitter: float = 0.0,
        serialize: bool = True,
    ) -> AsyncIterator[None]:
        """Hold one host's slot for the duration of a request.

        Same-host requests serialize (when ``serialize``) and are separated by at
        least ``min_interval`` seconds measured from the END of the previous one,
        plus up to ``jitter`` extra so we never emit a metronome. Different hosts
        stay fully concurrent — throughput on a diverse workload is unchanged;
        only same-host bursts are shaped.

        The interval is DIVIDED by the host's shared backoff factor, so a 429
        seen by any lane widens the gap here too.

        A slot is politeness, never a gate that can fail work: a URL with no
        resolvable host passes straight through, and a token-bucket timeout is
        logged and proceeds rather than raising into the caller's fetch.
        """
        key = host_key(url)
        if not key:
            yield
            return

        gate = self._gates.setdefault(key, asyncio.Lock()) if serialize else None
        if gate is not None:
            await gate.acquire()
        try:
            loop = asyncio.get_running_loop()
            factor = 1.0 if key in self._ramp_rates else _live_factor(key)
            effective_interval = min_interval / factor if factor > 0 else min_interval
            wait_for = self._next_allowed_at.get(key, 0.0) - loop.time()
            if wait_for > 0:
                await asyncio.sleep(wait_for)
            try:
                await self.acquire(url)
            except TimeoutError:
                logger.warning(
                    "host %s token bucket timed out; proceeding (politeness is not a gate)", key
                )
            try:
                yield
            finally:
                self._next_allowed_at[key] = (
                    loop.time()
                    + effective_interval
                    + (random.uniform(0, jitter) if jitter else 0.0)
                )
        finally:
            if gate is not None:
                gate.release()


__all__ = [
    "HostRateLimiter",
    "HostBucket",
    "RATE_LIMIT_STATUSES",
    "THROTTLE_TTL_SECONDS",
    "host_key",
    "shared_throttles",
    "clear_shared_throttles",
]
