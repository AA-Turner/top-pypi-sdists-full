"""Basic per-session rate limiting for the browser app proxy (spec §5 Phase 2a
security floor).

In-process sliding window, keyed by an opaque per-session identifier
(``request.state.session_key``, set by the auth middleware from a hash of the
credential -- never the raw key). Good enough for a single-task POC; a
multi-replica deployment needs shared state (e.g. a small DynamoDB/Redis
counter), which is Phase 5 hardening, not this POC.
"""

from __future__ import annotations

import time
from collections import OrderedDict, deque


class SlidingWindowRateLimiter:
    """Allows at most ``max_requests`` per ``window_seconds`` per key.

    ``_hits`` keeps one (eventually-empty) deque per key. With ``max_keys``
    unset it is never pruned, which is fine for the app-proxy caller
    specifically because keys are session hashes of real, admin-issued API keys
    (a handful of principals), not attacker-controlled or per-request; an
    unauthenticated caller never reaches that limiter at all.

    **Pass ``max_keys`` whenever the key is not like that.** The password-reset
    limiter (auth/login_flow.py) is the case this was added for: it is the first
    unauthenticated caller here, and it keys on a submitted email address and a
    client IP -- both attacker-varied, so without a cap the dict is a memory
    exhaustion vector rather than a defence.
    """

    def __init__(self, max_requests: int, window_seconds: float,
                 max_keys: int | None = None) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.max_keys = max_keys
        # Insertion-ordered so eviction can be LRU. See `allow`: the order is by
        # last CONTACT, which is not the same as last recorded hit.
        self._hits: OrderedDict[str, deque[float]] = OrderedDict()

    def allow(self, key: str) -> bool:
        """Record one hit for ``key`` and return whether it is within limit."""
        now = time.monotonic()
        window_start = now - self.window_seconds
        hits = self._hits.get(key)
        if hits is None:
            # Only a NEW key can grow the dict, so that is the only place the
            # cap needs checking.
            if self.max_keys is not None and len(self._hits) >= self.max_keys:
                self._evict(window_start)
            hits = deque()
            self._hits[key] = hits
        # Mark the key as contacted even when the answer below is "no". A denied
        # request appends nothing, so ordering eviction by the newest RECORDED
        # hit would make an at-limit key look idle and evict it -- handing a
        # flood a fresh budget for precisely the keys it had already exhausted.
        self._hits.move_to_end(key)
        while hits and hits[0] < window_start:
            hits.popleft()
        if len(hits) >= self.max_requests:
            return False
        hits.append(now)
        return True

    def _evict(self, window_start: float) -> None:
        """Make room under ``max_keys``, cheapest-to-lose first.

        Keys whose window has fully elapsed go first: every entry they hold is
        already outside the window, so the next `allow` would prune them to
        empty anyway and dropping them loses nothing. Under normal load that is
        all of them and no live key is forgotten.

        Only a caller whose keys are ALL still live -- an actual flood --
        reaches the second pass, and there the least recently contacted key is
        the one whose eviction costs the fewest real users: the flood's own keys
        are by definition the most recently contacted, so they are the last to
        be forgiven.
        """
        assert self.max_keys is not None
        stale = [k for k, v in self._hits.items() if not v or v[-1] < window_start]
        for k in stale:
            del self._hits[k]
        while len(self._hits) >= self.max_keys:
            self._hits.popitem(last=False)
