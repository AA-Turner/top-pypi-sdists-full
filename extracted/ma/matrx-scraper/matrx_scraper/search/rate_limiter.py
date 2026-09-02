import asyncio
import time


class RateLimiter:
    def __init__(self, min_interval: float = 1.0):
        self.min_interval = min_interval
        self._lock = asyncio.Lock()
        self._last_call_time: float | None = None

    def update_min_interval(self, min_interval: float) -> None:
        # Atomic float assignment — acquire() re-reads self.min_interval under
        # its lock on every call, so a runtime update takes effect immediately
        # without needing to hold the lock here.
        self.min_interval = min_interval

    async def acquire(self):
        async with self._lock:
            current_time = time.time()

            if self._last_call_time is not None:
                time_since_last_call = current_time - self._last_call_time

                if time_since_last_call < self.min_interval:
                    wait_time = self.min_interval - time_since_last_call
                    await asyncio.sleep(wait_time)
                    current_time = time.time()

            self._last_call_time = current_time


# ---------------------------------------------------------------------------
# Adaptive Brave rate-limit policy.
#
# The per-second ceiling DEPENDS ON THE KEY: the PRO AI key allows 50 req/sec,
# the standard AI key and the regular key only 1 req/sec. Rather than hard-code
# one interval, BraveSearchClient reads Brave's own `x-ratelimit-limit` response
# header (format "<per_second>, <per_month>") and tunes a per-key limiter via
# `interval_for_rate()`. The system therefore self-corrects to whatever key is
# actually in use — and to a plan change — without a code edit.
#
# These are CAPS constants (behavior, not environment): changing them is a code
# push, never a silent per-environment difference.
#
#   FLOOR  — the fastest we will ever pace, whatever a header claims. It is a
#            blast-radius cap for an over-reported limit, NOT the working rate;
#            the working rate comes from MARGIN applied to the advertised
#            ceiling.
#   MARGIN — headroom multiplier on the advertised rate (we target 1/MARGIN of
#            the ceiling) so transient bunching can't tip us over.
#
# 🚨 FLOOR was 0.6s until 2026-08-20, which clamped the 50 req/sec PRO key to
# 1.7 req/sec — we were using 3% of the key we pay for, and every fan-out
# (research, coverage sweeps, SEO collection) paid 30x the wall-clock it needed
# to. That value was chosen while a 1 req/sec base key was still in the mix; it
# stopped being a safety margin and became a self-inflicted throttle the moment
# the platform went single-key (Arman's ruling, same day).
#
# Re-measured against the live PRO key before changing it: 15/15 clean at each
# of 1.7, 5, 10, 20 and 33 req/sec, then 40/40 and 60/60 clean at the resulting
# steady-state 41.7 req/sec (1.2 / 50). Zero 429s at any rate tested. The floor
# below therefore no longer binds for a 50 req/sec key — MARGIN sets the rate —
# and still caps us at 50 req/sec if a header ever over-reports.
BRAVE_RATE_LIMIT_FLOOR_SECONDS = 0.02
BRAVE_RATE_LIMIT_SAFETY_FACTOR = 1.2


def interval_for_rate(per_second_limit: float) -> float:
    """Min seconds between requests for a key advertising `per_second_limit`
    req/sec, clamped to the safe FLOOR. e.g. 50/sec -> 0.024s, 1/sec -> 1.2s."""
    if per_second_limit <= 0:
        return BRAVE_RATE_LIMIT_FLOOR_SECONDS
    return max(
        BRAVE_RATE_LIMIT_FLOOR_SECONDS,
        BRAVE_RATE_LIMIT_SAFETY_FACTOR / per_second_limit,
    )


# Shared default limiter (back-compat export). BraveSearchClient owns one
# limiter PER KEY (see brave_client.py); this instance is the one it uses for
# the regular/base key. Seeded conservatively for a 1 req/sec key; the client
# re-tunes it from the first response header.
brave_search_rate_limiter = RateLimiter(min_interval=interval_for_rate(1))
