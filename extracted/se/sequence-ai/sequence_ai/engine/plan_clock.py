# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A policy's plan clock: its @seq.plan called in the background for each episode a server holds - on a GPU of your own
(serve()) and in a deployment's worker alike, this one module in both - and what a plan returns kept where the
episode's acts read it.

    clock = PlanClock(policy, every_s=2.0)      # policy: plan_episode(episode_id), plan(episode), plan_is_async
    clock.start()                               # once the policy is loaded and warmed up
    clock.observe(episode_id, step, wake=...)   # each new observation of an episode: cheap, never waits on a plan
    clock.forget(episode_id)                    # the episode ended
    drain_events()                              # each plan's outcome since the last drain, for the server's log
    clock.stop()

In one sentence: each new observation of an episode is noted (observe) and nothing waits on it → the clock keeps when
the episode's next plan may begin: every_s after its last one began → an episode that is due and had an observation
since its last plan began is planned at once - a plain plan on a thread of its own, an async one as a task on the
clock's own event loop - one plan at a time each episode, so a plan that runs past its next tick is followed by the
next the moment it returns → what plan returns, when it is not None, is appended to the episode's
state["seq.plans"] as {"step": the number of the episode's latest observation then, "value": what it returned},
where its acts read the newest and never wait on one; None changes nothing.
WHY a clock of its own: a plan's round trip is slow - hundreds of milliseconds to seconds, a VLM naming the next step -
so nothing a robot waits on may wait on it.

What a plan's failure does: nothing to any robot. The error is noted for the server's log (plan.error) - first in plain
words when the next call will meet it again (a refused key, a certificate the server does not trust, an address that
does not resolve or refuses, a model or address that is not there) - the episode keeps its newest plan, and the next
tick calls plan again.

A plan's own calls - a model through sequence_ai.chat(), the platform's or a model service of your own with
server=... - run entirely inside the plan; nothing here records what they cost.

Two things a host may replace, as module attributes: `redact(text)`, applied to what a plan's outcome says before it is
noted - a host that knows its secrets masks them, since an error may quote a key - and `described(exc)`, how an
exception is said. Unset, nothing is masked and an exception reads "<Type>: <message>".

Standard library only.
"""
from __future__ import annotations

import asyncio
import collections
import errno
import inspect
import reprlib
import socket
import ssl
import sys
import threading
import time
from typing import Any, Awaitable, Callable, Protocol

__all__ = ["FORGET_AFTER_S", "PLANS", "PlanClock", "PlannerAuthError", "PlannerError", "asks_human",
           "classify_plan_error", "described", "drain_events", "redact", "unrecoverable"]


def redact(text: str) -> str:
    """What a plan's outcome says, masked before it is noted: nothing, unless a host that knows its secrets replaces
    this (plan_clock.redact = its own)."""
    return text


def described(exc: BaseException) -> str:
    """How a plan's exception is said: "<Type>: <message>", or its type alone when it says nothing - unless a host
    replaces this (plan_clock.described = its own)."""
    return f"{type(exc).__name__}: {exc}" if str(exc) else type(exc).__name__


# ── what a plan.error note calls a failure ────────────────────────────────────────────────────────────────────────
class PlannerError(Exception):
    """Base for a plan's (a VLM call's) failure."""


class PlannerAuthError(PlannerError):
    """A plan's failure the next call will meet again - the key of the model service it calls is invalid, revoked or
    unauthorized (401/403). A plan that raises it is noted kind=permanent; planning goes on, and no act fails for it."""


def classify_plan_error(exc: BaseException) -> str:
    """"permanent" for an auth failure, "transient" for everything else: the kind a plan.error note says, nothing more -
    no failure stops planning or fails an act. A PlannerAuthError, or the platform refusing the policy's own model call
    - sequence_ai's AuthError (401: no credential, or a session token that lapsed) or PermissionDenied (403: a model the
    policy did not declare) - is one a retry cannot fix: said as permanent, so its log line is not read as a passing
    hiccup while the robots run on their last plan."""
    return "permanent" if isinstance(exc, PlannerAuthError) or _platform_refused(exc) else "transient"


def _platform_refused(exc: BaseException) -> bool:
    """Whether `exc` is sequence_ai's 401 / 403. Read from sys.modules: a plan that raised one has imported it, and this
    module imports nothing a plan does not."""
    errors = sys.modules.get("sequence_ai.errors")
    refused = tuple(c for c in (getattr(errors, "AuthError", None), getattr(errors, "PermissionDenied", None)) if c)
    return bool(refused) and isinstance(exc, refused)


def _chain(exc: BaseException):
    """`exc` and every exception behind it: its cause, its context (kept even under `raise ... from None`, which only
    hides it from a traceback) and a urllib URLError's reason."""
    seen: set[int] = set()
    todo: list[BaseException | None] = [exc]
    while todo:
        e = todo.pop()
        if e is None or id(e) in seen:
            continue
        seen.add(id(e))
        yield e
        todo += [e.__cause__, e.__context__]
        reason = getattr(e, "reason", None)
        if isinstance(reason, BaseException):
            todo.append(reason)


def _status(e: BaseException) -> int | None:
    """An HTTP failure's status however its client raised it: sequence_ai's (.status), urllib's HTTPError (.code),
    httpx's / requests' (.response.status_code)."""
    for v in (getattr(e, "status", None), getattr(e, "code", None),
              getattr(getattr(e, "response", None), "status_code", None)):
        if isinstance(v, int) and not isinstance(v, bool):
            return v
    return None


def unrecoverable(exc: BaseException) -> str | None:
    """Why `exc` is a plan's failure a retry will not fix, in plain words, which its plan.error note says first - or
    None for one that may pass: a timeout, a 5xx, a 429, anything unknown. A client may raise its own error from the
    transport's (sequence_ai raises Unavailable("could not reach ...")), so the reason is looked for along the chain."""
    for e in _chain(exc):
        if isinstance(e, ssl.SSLCertVerificationError) or (
                isinstance(e, ssl.SSLError) and "CERTIFICATE_VERIFY_FAILED" in str(e)):
            return "the plan's address presents a certificate this worker does not trust"
        if isinstance(e, socket.gaierror):
            return "the plan's address does not resolve"
        if isinstance(e, ConnectionRefusedError):
            return "the plan's address refuses connections"
        # no route to it: an IPv6 address from a machine that has IPv4 alone, or a network that is down - an address
        # given as a number fails this way (the worker: whatever machine runs the policy)
        if isinstance(e, OSError) and e.errno == errno.ENETUNREACH:
            return "the plan's address is unreachable from this worker"
        if _status(e) == 404:
            return "the plan's model or address was not found (404)"
    return None


# ── the policy the clock drives ───────────────────────────────────────────────────────────────────────────────────
class _PlannablePolicy(Protocol):
    plan_every_s: float | None
    plan_is_async: bool          # its plan is an async def: planned on the clock's event loop

    def plan_episode(self, episode_id: str): ...    # the episode's seq.Episode on this server, or None

    def plan(self, episode): ...                     # its plan on it: what it returns, or (async) its coroutine


# ── what the clock reports ────────────────────────────────────────────────────────────────────────────────────────
# Each plan's outcome, for the server's log: a host drains these (drain_events) and writes them as its own
# `plan.done` / `plan.error` lines. Bounded: while nothing drains them only the newest are kept - room for every robot a
# copy of a policy serves at once to note a few plans between two drains.
_EVENTS: collections.deque = collections.deque(maxlen=256)

# What a plan returned, said short whatever it is: a dict of a model's whole exchange is never written out to be cut.
_SAID = reprlib.Repr()
_SAID.maxstring = _SAID.maxother = 120
_SAID.maxdict = _SAID.maxlist = _SAID.maxtuple = 8
_SAID.maxlevel = 3


def drain_events() -> list[dict]:
    """Every outcome noted since the last drain, oldest first."""
    out = []
    while _EVENTS:
        try:
            out.append(_EVENTS.popleft())
        except IndexError:
            break
    return out


def asks_human(value: Any) -> bool:
    """Whether what a plan returned is the mark seq.ask_human returns: hand the robot to a person."""
    return isinstance(value, dict) and value.get("__seq__") == "ask_human"


def _failed(env_id: str, exc: BaseException) -> None:
    """One episode's plan raised: noted as plan.error (env, kind, error) for the server's log, and nothing else - the
    episode keeps its newest plan and its next tick calls plan again. Masked here (redact), where a host's secrets are
    known: the message may quote a key. One the next call will meet again is kind=permanent, and says why in plain
    words first when unrecoverable() names it."""
    reason = unrecoverable(exc)
    kind = "permanent" if reason is not None or classify_plan_error(exc) == "permanent" else "transient"
    detail = redact(described(exc))
    _EVENTS.append({"ev": "plan.error", "env": env_id, "kind": kind,
                    "error": f"{reason}: {detail}" if reason else detail})


def _planned(env_id: str, value: Any, ms: int) -> None:
    """One episode's plan returned: noted as plan.done (env, ms, step - what it returned as a short text, absent when it
    returned None and the episode's plans stay as they were)."""
    said = (f"ask_human: {value.get('reason')}" if asks_human(value)
            else value if isinstance(value, str) else _SAID.repr(value))
    _EVENTS.append({"ev": "plan.done", "env": env_id, "ms": ms,
                    "step": redact(said)[:120] if value is not None else None})


# The key of an episode's state its plans are kept under, the newest last: the server's, as "seq." says.
PLANS = "seq.plans"


def _keep_plan(episode, step: int | None, value: Any) -> None:
    """Append what one plan returned to its episode's plans, as it returned it: the one place they are written. Called
    under the clock's lock, so nothing is appended once the episode's end has reached PlanClock.forget. The mark
    seq.ask_human returns is never kept: it goes to the robot's operators, where its host has any (the event
    plan.ask_human)."""
    if asks_human(value):
        _EVENTS.append({"ev": "plan.ask_human", "env": episode.id, "reason": value.get("reason"),
                        "hold": value.get("hold") is not False})
        return
    episode.state.setdefault(PLANS, []).append({"step": step, "value": value})


async def _awaited(awaitable):
    """What a plain plan handed back to be awaited, awaited: a wrapper of an async function that is not one."""
    return await awaitable


# ── the episodes' clock ───────────────────────────────────────────────────────────────────────────────────────────
# An episode that sends nothing for this long is planned no more: one whose robot left without ending it would
# otherwise be planned for as long as its server runs.
FORGET_AFTER_S = 600.0


class _Entry:
    """What the clock keeps of one episode, read and written under the clock's lock."""

    __slots__ = ("seen", "step", "sent", "used", "due", "busy", "task", "wake")

    def __init__(self, now: float) -> None:
        self.seen = now        # when its latest observation came (the clock's time)
        self.step = None       # that observation's number in the episode
        self.sent = 0          # how many observations came
        self.used = 0          # how many had come when its latest plan began
        self.due = now         # when its next plan may begin: at once, the first time
        self.busy = False      # a plan of it is in flight
        self.task = None       # an async plan's task, cancelled when its episode ends
        self.wake = False      # an observation came that wakes its plan at once, due or not (wake_on)

    @property
    def fresh(self) -> bool:
        """An observation came that its latest plan began before."""
        return self.sent > self.used


class PlanClock:
    """Server-side planning: every episode on a clock of its own.

    An episode may be planned when its last plan began `every_s` ago (its first, the moment its first observation
    comes) and an observation came since that plan began: an episode whose robot stopped sending is not planned again
    until it sends again, since planning on the same frame over and over changes nothing anyone reads and a model is
    billed per call. One plan of an episode is in flight at a time: one that runs past its next tick is followed by the
    next the moment it returns, then one every every_s again.
    An observation that holds a key the plan's wake_on names wakes its episode's plan at once, its clock going on
    beside as the fallback; woken while a plan of it runs, the next begins the moment that one returns, however many
    woke it meanwhile.

    One scheduler thread keeps the episodes' times and starts each plan: a plain plan on a thread of its own, so
    episodes due together are planned at once and none waits for another's answer; an async one as a task on the
    clock's own event loop, which runs on a thread of its own. Neither is the thread an act runs on, and nothing bounds
    the plans in flight but the episodes a server holds.

    Decoupled from the act rate: a flood of acts never plans an episode more often than its clock allows, and no act
    ever waits on a plan. Lifecycle: it is start()-ed only after the policy is loaded and warmed up; an episode that
    ends (forget) or sends nothing for FORGET_AFTER_S is planned no more, and what a plan of it in flight returns is
    dropped (an async one is cancelled); stop() waits for the scheduler and the plans in flight within a grace budget,
    so no planning survives shutdown."""

    def __init__(self, handler: _PlannablePolicy, *, every_s: float, forget_after_s: float = FORGET_AFTER_S,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._handler = handler
        self._every_s = float(every_s)
        self._forget_after_s = float(forget_after_s)
        self._clock = clock
        self._cv = threading.Condition()
        self._episodes: dict[str, _Entry] = {}
        self._stopping = False
        self._thread: threading.Thread | None = None
        # an async plan's event loop and the thread it runs on, made at start()
        self._aloop: asyncio.AbstractEventLoop | None = None
        self._aloop_thread: threading.Thread | None = None
        self.in_flight = 0     # plans in flight
        self.plan_calls = 0    # plans started

    # ── the act path: cheap, and never waits on a plan ──
    def observe(self, episode_id: str, step: int, *, wake: bool = False) -> None:
        """Note a new observation of the episode - its number in the episode `step` (the stream's frame number) - and
        wake the scheduler when it makes the episode due again; the first one starts its planning. `wake`: it holds a
        key of wake_on, so the episode is planned at once, or the moment its plan in flight returns."""
        now = self._clock()
        with self._cv:
            e = self._episodes.get(episode_id)
            if e is None:
                e = self._episodes[episode_id] = _Entry(now)
            e.seen = now
            e.step = step
            e.sent += 1
            e.wake = e.wake or wake
            if (wake or e.sent == e.used + 1) and not e.busy:
                self._cv.notify_all()      # it has something to be planned on again: the scheduler keeps its time

    def set_every_s(self, seconds: float) -> None:
        """A new clock for every episode, from now (a setting changed while the policy runs): each episode's next plan
        is due `seconds` after its last began, so one waiting on the old clock moves at once. ValueError for a clock
        that is no positive number of seconds."""
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not seconds > 0:
            raise ValueError(f"a plan's clock is a positive number of seconds; got {seconds!r}")
        with self._cv:
            moved = float(seconds) - self._every_s
            self._every_s = float(seconds)
            for e in self._episodes.values():
                e.due += moved                 # its last plan's start + the new clock
            self._cv.notify_all()

    def forget(self, episode_id: str) -> None:
        """The episode ended: no plan of it starts again, what one in flight returns is dropped and an async one is
        cancelled - so once this returns nothing more is appended to its plans (_settled checks under the same lock)."""
        with self._cv:
            e = self._episodes.pop(episode_id, None)
            if e is not None and e.task is not None and self._aloop is not None:
                self._aloop.call_soon_threadsafe(e.task.cancel)

    def run(self, awaitable: Awaitable[Any]) -> Any:
        """`awaitable` run to its end where this clock's async plans run - on its loop, from another thread - and what
        it returned or raised: a plan run once outside every clock (a deploy's check, an eval's step), so what the plan
        keeps of a loop (an async client) is of the loop its plans after it run on."""
        if self._aloop is None:
            return asyncio.run(_awaited(awaitable))
        return asyncio.run_coroutine_threadsafe(_awaited(awaitable), self._aloop).result()

    # ── the scheduler ──
    def start(self) -> None:
        """Begin planning: the scheduler's thread, and an async plan's event loop on a thread of its own. A second call
        does nothing."""
        if self._thread is not None:
            return
        if getattr(self._handler, "plan_is_async", False):
            self._aloop = asyncio.new_event_loop()
            self._aloop_thread = threading.Thread(target=self._aloop.run_forever, name="seq-plan-loop", daemon=True)
            self._aloop_thread.start()
        self._thread = threading.Thread(target=self._loop, name="seq-planner", daemon=True)
        self._thread.start()

    def stop(self, grace: float = 30.0) -> None:
        """Start no more plans, cancel the async ones, and wait - within `grace` in all - for the scheduler and the
        plans in flight (a clean stop inside a server's shutdown grace); what they return then is dropped."""
        deadline = time.monotonic() + grace
        with self._cv:
            self._stopping = True
            for e in self._episodes.values():
                if e.task is not None and self._aloop is not None:
                    self._aloop.call_soon_threadsafe(e.task.cancel)
            self._cv.notify_all()
        if self._thread is not None:
            self._thread.join(timeout=max(0.0, deadline - time.monotonic()))
            self._thread = None
        with self._cv:
            while self.in_flight and time.monotonic() < deadline:
                self._cv.wait(timeout=max(0.0, deadline - time.monotonic()))
        if self._aloop is not None:
            # every task of it done (or the grace spent): its loop stops after the callbacks it already has
            self._aloop.call_soon_threadsafe(self._aloop.stop)
            if self._aloop_thread is not None:
                self._aloop_thread.join(timeout=max(0.0, deadline - time.monotonic()))

    def _loop(self) -> None:
        with self._cv:
            while not self._stopping:
                try:
                    wait = self._schedule(self._clock())
                except Exception as exc:  # noqa: BLE001 - the scheduler must outlive a fault of its own
                    print(f"plan scheduling error: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
                    wait = 1.0
                self._cv.wait(timeout=wait)

    def _schedule(self, now: float) -> float | None:
        """Start a plan for every episode that is ready; how long until another may be (None: none is waiting)."""
        nxt: float | None = None

        def at(t: float) -> None:
            nonlocal nxt
            nxt = t if nxt is None else min(nxt, t)

        for episode_id, e in list(self._episodes.items()):
            if e.busy:
                continue
            if now - e.seen >= self._forget_after_s:
                # its robot sent nothing for that long: an episode that ended without its end reaching this server
                del self._episodes[episode_id]
                continue
            at(e.seen + self._forget_after_s)
            ready = e.fresh
            if ready and (e.due <= now or e.wake):
                self._start(episode_id, e, now)
            elif ready:
                at(e.due)
        return None if nxt is None else max(0.0, nxt - now)

    def _start(self, episode_id: str, e: _Entry, now: float) -> None:
        """Begin one plan of the episode, on the observation it has: its next may begin every_s from now (start to
        start), or the moment this one returns when it takes longer."""
        e.busy, e.used, e.due, e.wake = True, e.sent, now + self._every_s, False
        self.in_flight += 1
        self.plan_calls += 1
        if self._aloop is not None:
            self._aloop.call_soon_threadsafe(self._begin, episode_id, e, e.step)
        else:
            threading.Thread(target=self._plan_sync, args=(episode_id, e, e.step), name="seq-plan",
                             daemon=True).start()

    def _begin(self, episode_id: str, e: _Entry, step: int | None) -> None:
        """On the clock's loop: an async plan of the episode as a task of its own - its end, however it ends (a cancel
        before it ever ran too), frees its place - unless the episode ended before the loop got to it.
        WHY the task's own callback, not the future run_coroutine_threadsafe returns: that future is done the moment it
        is cancelled, while its task still runs to its next await, so stop() could end the loop under a task."""
        with self._cv:
            if self._stopping or self._episodes.get(episode_id) is not e:
                self._free_locked(e)
                return
            e.task = self._aloop.create_task(self._plan_async(episode_id, e, step))
            e.task.add_done_callback(lambda _task, e=e: self._free(e))

    def _plan_sync(self, episode_id: str, e: _Entry, step: int | None) -> None:
        """One plain plan, on its own thread. Nothing escapes it (_settled)."""
        t0 = time.perf_counter()
        episode = got = error = None
        try:
            episode = self._handler.plan_episode(episode_id)
            if episode is not None:
                got = self._handler.plan(episode)
                if inspect.isawaitable(got):        # a plain function that hands back what is to be awaited
                    got = asyncio.run(_awaited(got))
        except Exception as exc:  # noqa: BLE001 — a plan's error must NEVER escape
            error = exc
        try:
            self._settled(episode_id, e, episode, step, got, error, t0)
        finally:
            self._free(e)

    async def _plan_async(self, episode_id: str, e: _Entry, step: int | None) -> None:
        """One async plan, a task on the clock's loop. Nothing escapes it but its cancel (its episode ended, or the
        clock stopped), which keeps nothing."""
        t0 = time.perf_counter()
        episode = got = error = None
        try:
            episode = self._handler.plan_episode(episode_id)
            if episode is not None:
                got = await self._handler.plan(episode)
        except Exception as exc:  # noqa: BLE001 — a plan's error must NEVER escape; CancelledError is no Exception
            error = exc
        self._settled(episode_id, e, episode, step, got, error, t0)

    def _settled(self, episode_id: str, e: _Entry, episode, step: int | None, got: Any, error: Exception | None,
                 t0: float) -> None:
        """One plan came back: what it returned kept in its episode's plans (None: nothing) and its outcome noted -
        unless its episode ended or the clock stopped while it ran, when it is dropped."""
        ms = round((time.perf_counter() - t0) * 1000)
        with self._cv:
            if self._stopping or self._episodes.get(episode_id) is not e:
                return
            if episode is None and error is None:
                return          # no episode of that id on this server (none made yet, or pushed out): nothing planned
            if error is None and got is not None:
                try:
                    _keep_plan(episode, step, got)
                except Exception as exc:  # noqa: BLE001 — a state the policy made into one that keeps no list there
                    error = exc
            if error is not None:
                _failed(episode_id, error)
            else:
                _planned(episode_id, got, ms)

    def _free(self, e: _Entry) -> None:
        with self._cv:
            self._free_locked(e)

    def _free_locked(self, e: _Entry) -> None:
        """A plan of the episode is over: another may begin when it is due."""
        e.busy, e.task = False, None
        self.in_flight -= 1
        self._cv.notify_all()
