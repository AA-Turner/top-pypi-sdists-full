"""RetryPolicy: deadline and patience scopes, Retry-After, and the pause between attempts."""

from __future__ import annotations
import os
import random
import sys
import time
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

import httpx
from ... import errors

#: The transport's own in-request retries, on the one backoff ladder every durable retry
#: loop uses (`durable.backoff_delays`): 0.2 s doubling to a 2 s ceiling (a blip's scale;
#: someone is usually waiting on the call).
_TRANSPORT_BACKOFF = (0.2, 2.0)

#: The longest server ``Retry-After`` one request waits out. Longer asks go back to the
#: caller at once as the error's ``retry_after``, for its own deadline-aware loop.
_INLINE_RETRY_AFTER_MAX = 10.0


#: A monotonic deadline every request on THIS thread must respect, or None.
#: Set only through :func:`deadline_scope`.
_request_deadline: ContextVar[float | None] = ContextVar("probe_request_deadline", default=None)


@contextmanager
def deadline_scope(deadline: float | None):
    """Bound every request this thread makes to ``deadline`` (``time.monotonic()``).

    `Run.finish()` has ONE budget (plan 0.6). It was checked only after a whole flush
    returned, so one stalled request or a slow backlog held a close far past it (live:
    170 s for ``flush_timeout=10``). In this scope each attempt's timeout is
    ``min(remaining, transport timeout)``, a retry pause never outlives the deadline, and
    a request that would START after it raises :class:`errors.DeadlineExceeded` unsent.

    A ContextVar: it follows the call through the outbox drain, the upload path and any
    client the drain builds, and stops at the thread (the heartbeat and other threads keep
    their own timeouts). Nested scopes keep the EARLIER deadline.
    """
    if deadline is None:
        yield
        return
    outer = _request_deadline.get()
    token = _request_deadline.set(deadline if outer is None else min(outer, deadline))
    try:
        yield
    finally:
        _request_deadline.reset(token)


@contextmanager
def fresh_deadline_scope(deadline: float):
    """Bound this block by ``deadline`` ALONE, replacing any enclosing `deadline_scope`.
    Only for a small, bounded, best-effort request that must go out after the enclosing
    budget is spent: the draining lease beat a deferred close sends (`Run._draining_beat`)."""
    token = _request_deadline.set(deadline)
    try:
        yield
    finally:
        _request_deadline.reset(token)


#: Set by :func:`patience` to the deadline in force OUTSIDE it (often None);
#: `_NOT_PATIENT` elsewhere. Its presence turns the deadline into a retry budget; its
#: value is what :func:`without_patience` restores.
_NOT_PATIENT: Any = object()
_patience_outer: ContextVar[Any] = ContextVar("probe_transport_patience", default=_NOT_PATIENT)

#: The open patience scope's record (budget; whether it has said on stderr it is
#: retrying), or None outside one.
_patience_state: ContextVar[dict | None] = ContextVar("probe_transport_patience_state", default=None)

#: A patient retry's wait: 0.5 s doubling to 10 s on the one ladder
#: (`durable.backoff_delays`), jittered down to half so ranks retrying one outage fall
#: out of step.
_PATIENCE_BACKOFF = (0.5, 10.0)
#: The least time worth a last patient attempt.
_PATIENCE_LAST_ATTEMPT = 1.0

#: The jitter's own generator: `random`'s shared one would shift a training script's
#: seeded stream. OS-seeded, and re-seeded in every forked child so forked ranks do not
#: back off in lockstep.
_JITTER = random.Random()
if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_JITTER.seed)


def _patient() -> bool:
    return _patience_outer.get() is not _NOT_PATIENT


@contextmanager
def patience(seconds: float | None):
    """Retry for up to ``seconds`` of wall clock instead of ``max_retries`` quick tries.

    For when a process cannot go on without an answer (``probe.init()`` opening its run,
    plan 2.5): one refused connection raised into the script after 1.9 s and a blackholed
    API after 122 s (measured).

    Built on :func:`deadline_scope` (attempt timeout capped at time left; nothing sent
    once spent). Added, for :meth:`Transport.request` only:

    * retries are bounded by the deadline, not by ``max_retries``;
    * waits come from `_PATIENCE_BACKOFF`, jittered; a ``Retry-After`` is waited out
      whenever the budget has room;
    * WHAT is retried is unchanged: connect-class failures always, anything else only
      when idempotent, never an answer outside `_RETRYABLE` (401/403/404/409/422 return
      at once). A write that may have landed is never re-sent blind.

    ``seconds`` None or <= 0 = no scope. Best-effort work inside opts out with
    :func:`without_patience`.
    """
    if seconds is None or seconds <= 0:
        yield
        return
    token = _patience_outer.set(_request_deadline.get())
    state_token = _patience_state.set({"seconds": float(seconds), "announced": False})
    try:
        with deadline_scope(time.monotonic() + float(seconds)):
            yield
    finally:
        _patience_state.reset(state_token)
        _patience_outer.reset(token)


@contextmanager
def without_patience():
    """Suspend an enclosing :func:`patience` scope (`probe.init()`'s budget) for a block:
    requests get the transport's own timeouts and quick retries again, and the deadline in
    force OUTSIDE patience (e.g. a close's) comes back.

    For any init step that may outlast the init budget or must not spend it:

    * best-effort capture after the run is open (code snapshot, hardware rail, output
      capture -- `Client.run`);
    * threads started during init (the heartbeat): one inheriting its creator's context
      (free-threaded 3.14) would carry the init deadline for the run's life;
    * a deliberate long wait, e.g. a requeue takeover waiting for a dead incumbent
      (plan 2.3; bound `PROBE_TAKEOVER_WAIT_SEC`).

    A no-op outside patience. ``tests/test_init_resilience.py`` pins that a step wrapped
    in it survives a wait longer than the whole budget."""
    outer = _patience_outer.get()
    if outer is _NOT_PATIENT:
        yield
        return
    deadline_token = _request_deadline.set(outer)
    patience_token = _patience_outer.set(_NOT_PATIENT)
    state_token = _patience_state.set(None)
    try:
        yield
    finally:
        _patience_state.reset(state_token)
        _patience_outer.reset(patience_token)
        _request_deadline.reset(deadline_token)


def deadline_remaining(default: float) -> float:
    """Seconds left in this thread's `deadline_scope`, at most ``default`` (``default``
    outside a scope). For local waits (a scan, a lock) sharing a close's one budget."""
    deadline = _request_deadline.get()
    if deadline is None:
        return default
    return max(0.0, min(default, deadline - time.monotonic()))


def _retry_after_seconds(resp: httpx.Response) -> float | None:
    """The server's ``Retry-After`` in seconds (delta-seconds or an HTTP-date,
    RFC 9110 10.2.3), or None when absent or unreadable. Never negative."""
    raw = (resp.headers.get("Retry-After") or "").strip()
    if not raw:
        return None
    try:
        return max(0.0, float(raw))
    except ValueError:
        pass
    try:
        from datetime import datetime, timezone
        from email.utils import parsedate_to_datetime

        when = parsedate_to_datetime(raw)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())
    except (TypeError, ValueError, IndexError, OverflowError):
        return None


def _announce_patience(status: int | None) -> None:
    """One stderr line when a patience scope first retries, so a quietly waiting job does
    not look hung."""
    state = _patience_state.get()
    if state is None or state.get("announced"):
        return
    state["announced"] = True
    why = f"answered {status}" if status else "is not reachable"
    try:
        print(
            f"probe: the Probe API {why}; probe.init() keeps retrying for up to "
            f"{state['seconds']:g}s (PROBE_INIT_TIMEOUT_SEC)",
            file=sys.stderr,
            flush=True,
        )
    except Exception:  # noqa: BLE001 -- a notice may never break the retry
        pass


def wait_out_retry_after(exc: BaseException, *, minimum: float = 0.0) -> bool:
    """Wait the ``Retry-After`` a failure carried (``RosError.retry_after``), at least
    ``minimum``, before the caller re-sends. False, without waiting, when it does not fit:
    the caller raises at once rather than sleep an hour (``Retry-After: 3600``) or its
    whole budget only to raise anyway.

    "Fits" is the transport's own rule (`Transport._retry_pause`), so a create and a read
    wait alike. Inside :func:`patience` the ONE bound is the budget left, less room for
    the next attempt (`_patient_pause`): ``Retry-After: 30`` 10 s into a 90 s budget is
    waited out. Outside, anything over `_INLINE_RETRY_AFTER_MAX`, or this thread's
    deadline, is not."""
    asked = getattr(exc, "retry_after", None)
    wait = max(float(minimum), float(asked or 0.0))
    deadline = _request_deadline.get()
    if _patient() and deadline is not None:
        if wait > deadline - time.monotonic() - _PATIENCE_LAST_ATTEMPT:
            return False
        _announce_patience(getattr(exc, "status", None))
    else:
        if wait > _INLINE_RETRY_AFTER_MAX:
            return False
        if deadline is not None and deadline - time.monotonic() <= wait:
            return False
    if wait > 0:
        time.sleep(wait)
    return True


def _with_retry_after(error: errors.RosError, resp: httpx.Response) -> errors.RosError:
    """Carry the response's ``Retry-After`` on the error the caller sees, so every retry
    loop above (outbox worker, exporter, `finish()`) waits at least that long (plan 0.4/0.6)."""
    wait = _retry_after_seconds(resp)
    if wait is not None:
        error.retry_after = wait
    return error
