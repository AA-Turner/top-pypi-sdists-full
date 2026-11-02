"""Bounded retry for authority checks that can only fail TRANSIENTLY.

An authority check (is this login still current, is this file-session source live, is this person a
member of the named organization) has two kinds of outcome: a DECISION (yes / no / not found /
archived) and "could not decide" (the database stalled, the pool timed out, a connection dropped).
A decision is final and is never retried. "Could not decide" used to be a refusal on the FIRST miss:
on 2026-10-19 22:50:51Z one ~5 s database stall turned an ordinary chat continuation into a 503
``session_authority_unavailable`` (real test PB-08, turn 6). Each check now gets
``ATTEMPTS`` tries, each under its own per-attempt timeout, with short pauses between; only when
every attempt fails does the caller see the same honest, retryable failure as before.

Pauses are jittered so a burst of callers that missed together does not retry together. Identical
concurrent checks (one person's desktop sync or agent burst, one token) share one lookup through
``FreshFlight``: on 2026-10-21 15:49Z a degraded pool (1 of 10 connections) faced 1,314 identical
lookups queued behind each other, and every one missed its deadline. A shared lookup never answers
a caller who arrived after it started, so a logout is seen by everyone who asks after it.
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from collections.abc import Awaitable, Callable, Hashable
from typing import TypeVar

T = TypeVar("T")

ATTEMPTS = 3
BACKOFF_SECONDS = (0.15, 0.4)
#: Per-attempt deadline of a login / file-session check when a host names none.
DEFAULT_SESSION_ATTEMPT_SECONDS = 5.0


def authority_budget_seconds(attempt_timeout: float) -> float:
    """The longest one ``call_authority`` can take: every attempt plus every (jittered) pause."""
    return max(0.001, attempt_timeout) * ATTEMPTS + sum(BACKOFF_SECONDS) * 1.5 + 0.05


#: Per-try deadline of a REMOTE check (a host asking aidream's ``/auth/session/status``). The
#: authority runs its own ``call_authority`` behind that URL, so one outer try must outlast the
#: whole inner budget; a shorter outer try abandons a check the authority would still have answered
#: (2026-10-21: Files gave up at 3 s while aidream's own lookup allowed 5 s per attempt).
REMOTE_AUTHORITY_TRY_SECONDS = authority_budget_seconds(DEFAULT_SESSION_ATTEMPT_SECONDS) + 1.0

_log = logging.getLogger(__name__)


async def call_authority(
    call: Callable[[], Awaitable[T]],
    *,
    attempt_timeout: float,
    label: str,
    decisions: tuple[type[BaseException], ...] = (),
) -> T:
    """Run ``call`` with up to ``ATTEMPTS`` tries; re-raise the last failure when all miss.

    ``decisions`` are exception types that ARE an answer (e.g. organization not found): raised
    at once, never retried. ``CancelledError`` always propagates. A recovery after a miss is
    logged at WARNING so a degrading authority is visible before it starts refusing people.
    """
    budget = authority_budget_seconds(attempt_timeout)
    deadline = time.monotonic() + budget
    failures: list[str] = []
    last: Exception | None = None
    for attempt in range(ATTEMPTS):
        remaining = deadline - time.monotonic()
        if attempt and remaining <= 0:
            break
        try:
            async with asyncio.timeout(min(attempt_timeout, max(remaining, 0.001))):
                result = await call()
        except asyncio.CancelledError:
            raise
        except decisions:
            raise
        except Exception as exc:  # noqa: BLE001 — classified by the caller after the last attempt
            failures.append(type(exc).__name__)
            if attempt + 1 >= ATTEMPTS:
                raise
            base = BACKOFF_SECONDS[min(attempt, len(BACKOFF_SECONDS) - 1)]
            pause = random.uniform(base * 0.5, base * 1.5)  # noqa: S311 — spreading retries, not secrecy
            if deadline - time.monotonic() <= pause:
                raise
            await asyncio.sleep(pause)
            last = exc
            continue
        if failures:
            _log.warning(
                "%s recovered on attempt %d after %s", label, attempt + 1, ", ".join(failures)
            )
        return result
    assert last is not None  # the loop only exits here after a recorded failure
    raise last  # budget ran out between attempts


class FreshFlight[K: Hashable, T]:
    """Coalesce identical concurrent authority checks without ever answering from the past.

    Per key, at most one lookup runs and at most one more waits to start. A caller joins the
    WAITING lookup (it has not started, so it will read state after the caller arrived), or starts
    one. A running lookup is never joined. Each lookup is bounded by ``limit_seconds`` so a connection
    that stopped answering cannot hold the next one back past one attempt; a caller's own deadline
    cancels only its wait, never the shared lookup.
    """

    def __init__(self) -> None:
        self._waiting: dict[K, asyncio.Task[T]] = {}
        self._running: dict[K, asyncio.Task[T]] = {}

    async def do(self, key: K, call: Callable[[], Awaitable[T]], *, limit_seconds: float) -> T:
        flight = self._waiting.get(key)
        if flight is None:
            flight = asyncio.ensure_future(self._run(key, call, limit_seconds))
            flight.add_done_callback(_retrieve)
            self._waiting[key] = flight
        return await asyncio.shield(flight)

    async def _run(self, key: K, call: Callable[[], Awaitable[T]], limit_seconds: float) -> T:
        me = asyncio.current_task()
        prior = self._running.get(key)
        if prior is not None and not prior.done():
            await asyncio.wait([prior])  # bounded: every lookup carries its own timeout
        # Start NOW: from this instant new callers form the next waiting lookup.
        if self._waiting.get(key) is me:
            del self._waiting[key]
        self._running[key] = me  # type: ignore[assignment]
        try:
            async with asyncio.timeout(max(0.001, limit_seconds)):
                return await call()
        finally:
            if self._running.get(key) is me:
                del self._running[key]


def _retrieve(task: asyncio.Task[object]) -> None:
    """Every caller may have stopped waiting; never leave an unretrieved failure behind."""
    if not task.cancelled():
        task.exception()
