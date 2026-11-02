"""Short-TTL per-profile cache for the console's Apollo reads (spec §4.6).

**Why this exists.** The read path is slower than it looks. Every MCP tool that
takes an `environment` runs `_resolve_environment`, which issues
`LIST_ENVIRONMENTS` — every environment (202 as of 2026-09-21, drained across
pages) *with its full `rolePolicy`* — and
`get_user_team_names` issues `MY_TEAMS`, both *before* the query the caller
actually asked for. A cube detail view is therefore three Apollo round-trips, two
of them repeating exactly what the list page just fetched.

**What this is and is not.** It caches *visibility* — which cubes a profile can
see — and two per-cube payloads: the Resources tab's utilization
(`utilization:<cube>:<window>`) and, since the cube page's service lines, each
cube's Service list (`services:<cube>:<env_id>`, written on EVERY cube-page load). It does **not** cache authentication:
`validate_key` runs in the middleware on every single request, so a revoked or
expired key fails immediately regardless of anything in here. Authorization is
re-checked above this cache on every read, so a hit can never substitute for a
permission check.

**The key space is not fixed, so expired slots are SWEPT, not just purged on
read.** This was written for two constant keys per profile (`environments`,
`teams`), where purge-on-read inside `_live_value` was sufficient because both
slots are re-read constantly. The per-cube keys are not: a cube nobody revisits was
never re-read, so its entry stayed resident for the life of the ECS task — browsing
the fleet pinned one Service list per cube per profile, never reclaimed.
`_sweep_if_due` now drops every expired entry at most once per
`_SWEEP_INTERVAL_SECONDS`, from `get_or_set` itself, so what stays resident is the
working set of roughly the last TTL plus that interval. Adding another per-entity
key needs no further eviction work; it does still need its own TTL argument. And do
not describe a TTL as bounding upstream load in general — it bounds *repeat* reads
of one key, not a sweep across many.

The staleness window is **symmetric**, which is worth stating plainly: a cube
newly granted to your team may not appear for up to the TTL, *and* a cube whose
role was just revoked stays visible for up to the TTL. Neither direction crosses a
tenant boundary — entries are keyed by profile, and a profile is exactly what
`auth/profiles.py::get_credentials` resolves to an Apollo credential, so two API
keys sharing a profile always resolve to the same Apollo identity at the same
instant.

**Scope.** In-process, per ECS task. Two tasks may hold different snapshots inside
the TTL window; that is a deliberate trade, documented so nobody debugs it as a
bug.
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Awaitable, Callable

from cube_cloud.config import settings

logger = logging.getLogger(__name__)

# (profile, key) -> (expires_at_monotonic, value)
_entries: dict[tuple[str, str], tuple[float, Any]] = {}
# One lock per (profile, key) so a cache miss under concurrent requests issues ONE
# Apollo query rather than N.
_locks: dict[tuple[str, str], asyncio.Lock] = {}

# How often `get_or_set` sweeps expired entries out of `_entries`. Purge-on-read alone
# never reclaims a per-cube slot nobody opens again; see the module docstring.
_SWEEP_INTERVAL_SECONDS = 60.0
_next_sweep = 0.0

# Ceiling on how long a caller will queue behind another caller's in-flight fetch
# before giving up on the lock and fetching itself. See the convoy note in
# `get_or_set`.
_ACQUIRE_TIMEOUT_SECONDS = 20.0


def _now() -> float:
    # Monotonic: immune to wall-clock jumps (NTP correction, container drift),
    # which could otherwise make an entry look valid for a very long time.
    return time.monotonic()


def _live_value(slot: tuple[str, str]) -> tuple[bool, Any]:
    """(hit, value) for `slot`, purging the entry if it has expired.

    Purge-on-read matters for more than tidiness: the `environments` value holds
    every tenant's environment names AND their full `rolePolicy` — the whole
    tenancy graph. Leaving an expired entry in the dict keeps that resident for the
    task's lifetime instead of the TTL, a far longer exposure window than this
    module's design implies. Dropping the lock alongside it also bounds `_locks`
    and clears any lock bound to a dead event loop (see `_lock_for`).
    """
    hit = _entries.get(slot)
    if hit is None:
        return False, None
    if hit[0] > _now():
        return True, hit[1]
    _entries.pop(slot, None)
    _locks.pop(slot, None)
    return False, None


def _sweep_if_due() -> None:
    """Drop every expired entry, at most once per `_SWEEP_INTERVAL_SECONDS`.

    A slot's lock goes with it unless it is HELD — a caller mid-`produce()` on an
    expired slot still owns it, and replacing the lock under it would let a second
    caller issue the same fetch. A lock with no entry and no holder is dropped too, so
    `_locks` cannot outgrow `_entries` for slots whose fetch failed (nothing cached).
    """
    global _next_sweep
    now = _now()
    if now < _next_sweep:
        return
    _next_sweep = now + _SWEEP_INTERVAL_SECONDS
    for slot in [s for s, (expires, _v) in _entries.items() if expires <= now]:
        _entries.pop(slot, None)
    for slot in [s for s, lock in _locks.items() if s not in _entries and not lock.locked()]:
        _locks.pop(slot, None)


def _lock_for(slot: tuple[str, str]) -> asyncio.Lock:
    """The lock for `slot`, replacing one bound to a dead event loop.

    `asyncio.Lock` binds to a loop lazily — in 3.10 only on the *contended*
    `acquire` path — so a lock created and contended under one loop raises
    `RuntimeError: ... is bound to a different event loop` if it is later contended
    under another. Because the object was previously never replaced, that wedged
    the slot with a permanent 500 for the process lifetime.

    Not reachable under ECS (one loop per process) but reachable under
    `uvicorn --reload`, any future worker-thread loop, and in tests. Recovering is
    strictly better than failing, and costs one attribute check.
    """
    lock = _locks.get(slot)
    if lock is not None:
        bound = getattr(lock, "_get_loop", None)
        try:
            if bound is not None and lock.locked():
                bound()  # raises RuntimeError if bound to another loop
            return lock
        except RuntimeError:
            logger.warning(
                "console cache lock for %s was bound to a dead event loop; replacing", slot
            )
    lock = asyncio.Lock()
    _locks[slot] = lock
    return lock


async def get_or_set(
    profile: str,
    key: str,
    produce: Callable[[], Awaitable[Any]],
    ttl: float | None = None,
    ttl_for: Callable[[Any], float] | None = None,
) -> Any:
    """Return the cached value for (profile, key), else await `produce()` and cache it.

    `produce` is awaited only on a miss, and normally by one caller at a time.

    `ttl` overrides `console_cache_ttl_seconds` for this call. It exists because the
    two callers are bounding different costs and so cannot share a number: visibility
    caching trades staleness against Apollo latency, while the Resources tab's entry
    trades it against a SHARED Groundcover rate budget that other tenants' reads draw
    on too. Its value is chosen against that feature's query step, not against this
    module's default — see `console_utilization_cache_ttl_seconds`. The single-flight
    and bounded-acquire behaviour below is what both callers actually want in common,
    and is the reason this is a parameter rather than a second cache.

    `ttl_for`, when given, picks the TTL from the VALUE produced, clamped to `ttl` so it
    can only ever shorten an entry (and `ttl <= 0` still disables caching outright). It
    exists for a read that reports failure as a value rather than by raising — the
    services read returns "could not look" as a payload — so that a failure can be held
    briefly, which stops a convoy of page loads each re-running a slow upstream, without
    being held as long as a success. A value it maps to 0 is not cached at all.

    **The lock is an optimization, never a correctness gate.** A failed `produce()`
    caches nothing (deliberately — a poisoned entry would be worse), so during an
    Apollo outage every waiter re-checks, misses, and tries itself. With
    `httpx.AsyncClient(timeout=90)` and a token round-trip in front of every query,
    one failed attempt can run for a long time, and N queued callers would
    serialize into N × that. So acquisition is bounded: past
    `_ACQUIRE_TIMEOUT_SECONDS` a caller stops waiting and fetches concurrently.
    That trades a possible duplicate query for a bounded tail latency, which is the
    right way round for a read path.
    """
    if ttl is None:
        ttl = settings.console_cache_ttl_seconds
    if ttl <= 0:  # 0 disables caching entirely — an escape hatch for debugging
        return await produce()

    _sweep_if_due()
    slot = (profile, key)
    hit, value = _live_value(slot)
    if hit:
        return value

    lock = _lock_for(slot)
    try:
        await asyncio.wait_for(lock.acquire(), timeout=_ACQUIRE_TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        logger.warning(
            "console cache: gave up waiting %.0fs for %s; fetching concurrently",
            _ACQUIRE_TIMEOUT_SECONDS, slot,
        )
        return await produce()

    try:
        # Re-check inside the lock: another coroutine may have filled it while we
        # waited, in which case we must not issue a second identical query.
        hit, value = _live_value(slot)
        if hit:
            return value
        value = await produce()
        keep = ttl if ttl_for is None else min(ttl, ttl_for(value))
        if keep > 0:
            _entries[slot] = (_now() + keep, value)
        return value
    finally:
        lock.release()


def invalidate(profile: str | None = None) -> None:
    """Drop cached entries for one profile, or all of them.

    Not wired to a route on purpose — there is no cache-busting endpoint, because
    an unauthenticated or cheaply-triggered one would be a way to force expensive
    Apollo queries. Present for tests and for a future mutation path to call
    locally after it changes state.
    """
    global _next_sweep
    if profile is None:
        _entries.clear()
        _locks.clear()
        _next_sweep = 0.0
        return
    for slot in [s for s in _entries if s[0] == profile]:
        _entries.pop(slot, None)
        _locks.pop(slot, None)
