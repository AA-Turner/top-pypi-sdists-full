"""A fan-out of one person's requests never exhausts the pool behind the current-login check.

Incidents 2026-10-19 08:00Z, 2026-10-20 00:52Z and 2026-10-21 15:49Z (aidream production logs): the
database pool degraded (``Pool: size=1/10, idle=0`` while pools were replaced and re-created), and
1,314 requests in ten minutes were refused 503 ``session_authority_unavailable`` after every
attempt of the per-request login check timed out. The Files service, polled by a desktop sync,
was refused the same way through its remote check. One person's desktop sync or agent-mail burst
sends many requests with ONE token at once; each ran its own identical login lookup, so N callers
queued N queries on the few connections left, every waiter missed its per-attempt deadline, and the
retries re-queued behind each other. Identical concurrent checks now share one query, and a check
never answers a caller with a lookup that started before that caller arrived (a logout is seen by
everyone who asks after it).

The pool double is a FIFO bounded resource (``asyncio.Semaphore``): a waiter whose deadline passes
leaves the queue, as an ``asyncpg`` pool acquire does, and a query reads the session's state when it
runs, as a SELECT does. It cannot hold a state the real pool cannot.
"""

from __future__ import annotations

import asyncio
import time

import jwt
import pytest

from matrx_connect.middleware.auth import AuthMiddleware
from matrx_connect.middleware.session_authority import SessionAuthorityUnavailable

SECRET = "synthetic-test-key-not-a-deployment-secret"
SUBJECT = "00000000-0000-4000-8000-000000000001"
SESSION = "00000000-0000-4000-8000-000000000002"


def _token() -> str:
    return jwt.encode(
        {"sub": SUBJECT, "session_id": SESSION, "aud": "authenticated", "exp": int(time.time()) + 3600},
        SECRET,
        algorithm="HS256",
    )


class _DegradedPool:
    """Two connections left; each login lookup holds one for ``service`` seconds."""

    def __init__(self, connections: int = 2, service: float = 0.02) -> None:
        self._slots = asyncio.Semaphore(connections)
        self._service = service
        self.queries = 0
        self.in_flight = 0
        self.peak = 0
        self.session_active = True
        self.started_at: list[float] = []
        self.first_started = asyncio.Event()

    async def lookup(self, _verified) -> bool:
        async with self._slots:
            self.queries += 1
            self.in_flight += 1
            self.peak = max(self.peak, self.in_flight)
            self.started_at.append(time.monotonic())
            self.first_started.set()
            seen = self.session_active  # the snapshot the SELECT reads when it runs
            try:
                await asyncio.sleep(self._service)
                return seen
            finally:
                self.in_flight -= 1


def _middleware(pool: _DegradedPool, *, attempt_timeout: float = 0.3) -> AuthMiddleware:
    return AuthMiddleware(
        lambda *_: None,
        jwt_secret=SECRET,
        resolve_current_session=pool.lookup,
        session_resolve_timeout=attempt_timeout,
        log_requests=False,
    )


@pytest.mark.asyncio
async def test_two_hundred_concurrent_checks_of_one_login_are_all_admitted() -> None:
    pool = _DegradedPool()
    mw = _middleware(pool)
    bearer = _token()

    async def one() -> str:
        try:
            verified = await mw.verify_token_raw(bearer)
        except SessionAuthorityUnavailable:
            return "refused"
        return "admitted" if verified is not None else "anonymous"

    results = await asyncio.wait_for(asyncio.gather(*(one() for _ in range(200))), timeout=20)
    refused = results.count("refused")
    assert refused == 0, (
        f"{refused}/200 concurrent checks of ONE login were refused session_authority_unavailable "
        f"on a pool that answers each lookup in 20 ms ({pool.queries} lookups queued)"
    )
    assert results.count("admitted") == 200
    # One lookup running, at most one more waiting to start: never a queue of identical queries.
    assert pool.queries <= 4, f"{pool.queries} identical lookups for one login"


@pytest.mark.asyncio
async def test_a_check_never_answers_a_caller_who_arrived_after_its_lookup_started() -> None:
    pool = _DegradedPool(connections=1, service=0.2)
    mw = _middleware(pool, attempt_timeout=2.0)
    bearer = _token()

    first = asyncio.create_task(mw.verify_token_raw(bearer))
    await pool.first_started.wait()  # the first lookup is now reading the session
    pool.session_active = False  # the person logs out while that lookup is in flight
    late = asyncio.create_task(mw.verify_token_raw(bearer))

    assert await first is not None  # it asked before the logout
    assert await late is None, "a caller who asked after the logout was admitted by an earlier lookup"
    assert pool.queries == 2


@pytest.mark.asyncio
async def test_a_hung_lookup_does_not_hold_later_checks_past_their_budget() -> None:
    hung = asyncio.Event()
    calls = 0

    async def lookup(_verified) -> bool:
        nonlocal calls
        calls += 1
        if calls == 1:
            await hung.wait()  # a connection that stopped answering
        return True

    mw = AuthMiddleware(lambda *_: None, jwt_secret=SECRET, resolve_current_session=lookup,
                        session_resolve_timeout=0.2, log_requests=False)
    started = time.monotonic()
    verified = await asyncio.wait_for(mw.verify_token_raw(_token()), timeout=5)
    assert verified is not None, "the retry never got a fresh lookup after the first one hung"
    assert time.monotonic() - started < 0.2 * 3 + 1.0
    hung.set()
