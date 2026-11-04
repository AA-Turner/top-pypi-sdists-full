"""RetryPolicy: deadline and patience scopes, Retry-After, and the pause between attempts."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
import os
import random
import sys
import time
from typing import Any

import httpx

from probe.foundation.durable import durable

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
    """Bound every request this thread makes to ``deadline`` (``time.monotonic()``), `Run.finish`'s one
    budget (plan 0.6): attempts get at most what is left, pauses never outlive it, and a request
    that would start after it raises `errors.DeadlineExceeded` unsent. Nested scopes keep the
    earlier deadline; a ContextVar, so it stops at the thread."""
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


#: Set by :func:`disable_retries`: every request in that block is sent once.
_retries_off: ContextVar[bool] = ContextVar("probe_transport_retries_off", default=False)


@contextmanager
def disable_retries():
    """Send each request in this block once, whatever its method or status: no quick retries, no
    `patience`. For a periodic write whose next tick is its retry (a lease beat, a log chunk):
    retried inline, each failed one cost 4 requests in an outage (I14)."""
    token = _retries_off.set(True)
    try:
        yield
    finally:
        _retries_off.reset(token)


@contextmanager
def patience(seconds: float | None):
    """Retry for up to ``seconds`` of wall clock instead of ``max_retries`` quick tries, for a process
    that cannot go on without an answer (`probe.init()` opening its run, plan 2.5). What is retried
    is unchanged; waits are jittered and honour `Retry-After` when the budget has room. ``seconds``
    None or <= 0: no scope."""
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
def pause_patience():
    """Suspend an enclosing `patience` scope for a block that waits on a person or the Probe
    daemon, not the server, and give the budget back after: its deadline moves on by the time
    spent (a 90 s wait for a run's project never eats `probe.init()`'s 90 s). No-op outside one."""
    outer = _patience_outer.get()
    if outer is _NOT_PATIENT:
        yield
        return
    started = time.monotonic()
    try:
        with without_patience():
            yield
    finally:
        current = _request_deadline.get()
        if current is not None:
            moved = current + (time.monotonic() - started)
            _request_deadline.set(moved if outer is None else min(outer, moved))


@contextmanager
def without_patience():
    """Suspend an enclosing `patience` scope for a block: quick retries again, and the deadline in
    force outside patience (a close's) comes back. For best-effort capture, threads started during
    init, and deliberate long waits; a no-op outside patience."""
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
    """Wait the ``Retry-After`` a failure carried, at least ``minimum``, before the caller re-sends;
    False, without waiting, when it does not fit the transport's own rule (`_retry_pause`)."""
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


class RetryPolicyMixin:
    """Part of Transport: its methods run with `self` the Transport; fold_parts() copies them into Transport."""

    # -- deadline -------------------------------------------------------------
    def _attempt_timeout(self, requested: float | None, what: str) -> tuple[Any, bool]:
        """``(timeout kwarg value, clamped)`` for one attempt. Outside a
        :func:`deadline_scope`: ``requested`` untouched (None keeps the client-wide budget),
        ``clamped`` False. Inside: ``min(requested or self.timeout, remaining)``, with
        ``clamped`` saying the deadline set the bound. Raises
        :class:`errors.DeadlineExceeded` when nothing is left: the request is never sent."""
        deadline = _request_deadline.get()
        if deadline is None:
            return requested, False
        left = deadline - time.monotonic()
        if left <= 0:
            raise errors.DeadlineExceeded(f"{what}: deadline passed before it was sent")
        base = float(self.timeout if requested is None else requested)
        bound = min(base, left)
        return httpx.Timeout(bound, connect=min(bound, _DEFAULT_CONNECT_TIMEOUT)), bound < base

    @staticmethod
    def _retry_pause(attempt: int, resp: httpx.Response | None = None) -> bool:
        """Sleep before retry ``attempt + 1`` (0.2 s doubling to 2 s, lengthened to a `Retry-After`);
        False, without sleeping, when the retry must not happen here: a `Retry-After` over
        `_INLINE_RETRY_AFTER_MAX`, or no room before the deadline."""
        deadline = _request_deadline.get()
        retry_after = _retry_after_seconds(resp) if resp is not None else None
        if _patient() and deadline is not None:
            return Transport._patient_pause(
                attempt, retry_after, deadline, status=resp.status_code if resp is not None else None
            )
        (*_, delay) = durable.backoff_delays(attempt + 1, _TRANSPORT_BACKOFF)
        if retry_after is not None and retry_after > _INLINE_RETRY_AFTER_MAX:
            return False
        pause = durable.honor_retry_after(delay, retry_after, ceiling=_INLINE_RETRY_AFTER_MAX)
        if deadline is not None and deadline - time.monotonic() <= pause:
            return False
        time.sleep(pause)
        return True

    @staticmethod
    def _patient_pause(
        attempt: int, retry_after: float | None, deadline: float, *, status: int | None = None
    ) -> bool:
        """`_retry_pause` inside :func:`patience`: the jittered `_PATIENCE_BACKOFF` step,
        lengthened to any ``Retry-After`` the budget can hold, shortened so a last attempt
        fits before the deadline. False when no room. The scope's FIRST retry says so, once,
        on stderr."""
        room = deadline - time.monotonic() - _PATIENCE_LAST_ATTEMPT
        if room <= 0 or (retry_after is not None and retry_after > room):
            return False
        _announce_patience(status)
        (*_, step) = durable.backoff_delays(attempt + 1, _PATIENCE_BACKOFF)
        jittered = step / 2 + _JITTER.uniform(0, step / 2)
        time.sleep(min(durable.honor_retry_after(jittered, retry_after, ceiling=room), room))
        return True

    def _may_retry(self, attempt: int) -> bool:
        """The COUNT half of the retry decision: ``max_retries`` quick tries, or,
        inside :func:`patience`, as many as the deadline allows; none inside
        :func:`disable_retries`."""
        if _retries_off.get():
            return False
        return attempt <= self.max_retries or _patient()

    @staticmethod
    def _deadline_error(what: str, exc: BaseException) -> errors.DeadlineExceeded:
        """The deadline cut an attempt: ``sent`` when only the response was lost
        (a read timeout), so the server may have applied the request."""
        return errors.DeadlineExceeded(f"{what}: {exc}", sent=isinstance(exc, httpx.ReadTimeout))

    def _send_within_deadline(self, deadline: float, method: str, path: str, **kwargs) -> httpx.Response:
        """Send, then read the body chunk by chunk, checking ``deadline`` between chunks.
        httpx timeouts bound each socket operation, not the request: a response trickling a
        byte at a time never trips one (live: a close with ``flush_timeout=2`` took 9.8 s).
        Returns an ordinary, fully read response."""
        with self._client.stream(method, path, **kwargs) as resp:
            if resp.is_stream_consumed:  # an in-memory transport already read it
                resp.read()
                return resp
            chunks: list[bytes] = []
            for chunk in resp.iter_raw():
                chunks.append(chunk)
                if time.monotonic() >= deadline:
                    raise errors.DeadlineExceeded(
                        f"{method} {path}: deadline passed while reading the response", sent=True
                    )
        return httpx.Response(
            resp.status_code,
            headers=resp.headers,
            content=b"".join(chunks),
            request=resp.request,
            extensions=resp.extensions,
        )

    @staticmethod
    def _cut_by_deadline(exc: BaseException, clamped: bool) -> bool:
        """A timeout that fired only because the deadline shortened the attempt: our clock
        ran out, not the server's patience."""
        deadline = _request_deadline.get()
        return (
            clamped
            and deadline is not None
            and isinstance(exc, httpx.TimeoutException)
            and time.monotonic() >= deadline
        )
from probe.sdk.delivery.transport.transport import Transport  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.transport import _DEFAULT_CONNECT_TIMEOUT  # noqa: E402 -- pieces need each other; the front door loads this one first
