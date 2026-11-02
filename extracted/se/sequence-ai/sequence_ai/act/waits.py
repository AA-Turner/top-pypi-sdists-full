"""
What a Policy waits for before an act or an observation goes - a worker that is starting, a place in line for a slot,
the connection to the worker - and how a stop ends the wait (`Interrupted`). A mixin `Policy` inherits
(sequence_ai/act/policy.py): act() waits out a starting worker on every call, observe() its first connect, and
wait_until_ready() opens the connection to the worker before the robot is told to go. run() and the Player went with
train br: when to ask for the next answer, and how to play it, is the caller's own code.

"""
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait as _wait_futures
from datetime import datetime, timezone
from typing import Any

from .._core.capacity import queue_eta as _queue_eta
from .._core.reporting import CallMetrics
from .._core.rid import new_rid
from .._core.warn import warn
from ..errors import Unavailable

def _not_open_said(missed: Any) -> str:
    """The warning for a connection that was not open when the policy was ready (a DirectConnection NotOpen), in plain
    sentences: what was not done, then what the first act does about it."""
    lead = "The policy is ready, but "
    if missed.stage == "connect":
        if missed.failed is None:
            return f"{lead}the connect was not done after {missed.waited_s:.1f} s. The first act waits for it."
        return f"{lead}connecting to it failed: {missed.failed}. The first act connects again."
    if missed.failed is None:
        return (f"{lead}the connection to its worker was still opening after {missed.waited_s:.1f} s. The first act "
                "waits for it.")
    return f"{lead}the connection to its worker did not open: {missed.failed}. The first act opens a new one."


def _span(seconds: float) -> str:
    """A wait in the words a person reads it in: "42 s", "9 min 2 s", "1 h 2 min"."""
    s = int(max(0.0, seconds))
    if s < 60:
        return f"{s} s"
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m} min {s} s"
    h, m = divmod(m, 60)
    return f"{h} h {m} min"


def _gpu_said(gpu: Any, now: float | None = None) -> str | None:
    """Where a start stands on its GPU, as the platform said it - a ready poll's `gpu`, a warming answer's
    `details.gpu`: {"state": "held" | "waiting", "since": Unix seconds, "card"} - in the words a give-up says it in: "it
    has had its GPU (L4) since 03:40:51 EDT (9 min 2 s) and is still starting on it", or "it is still waiting for a GPU
    (L4), since … (…)". None when it said nothing of it (a start not yet looked at).


"""
    if not isinstance(gpu, dict) or gpu.get("state") not in ("held", "waiting"):
        return None
    card = gpu.get("card")
    named = f" ({card})" if isinstance(card, str) and card else ""
    since = ""
    try:
        at = float(gpu["since"])
    except (KeyError, TypeError, ValueError):
        at = None
    if at is not None:
        local = datetime.fromtimestamp(at, tz=timezone.utc).astimezone()
        took = (time.time() if now is None else now) - at
        face = local.strftime("%H:%M:%S %Z").strip()
        since = f" since {face if abs(took) < 86400 else f'{local:%Y-%m-%d} {face}'} ({_span(took)})"
    if gpu["state"] == "held":



        stage = gpu.get("stage")
        if isinstance(stage, str) and stage:
            try:
                began = float(gpu.get("stage_since", at))
            except (TypeError, ValueError):
                began = None
            during = f" for {_span((time.time() if now is None else now) - began)}" if began is not None else ""
            return f"it has had its GPU{named}{since} and has been {stage}{during}"
        return f"it has had its GPU{named}{since} and is still starting on it"
    return f"it is still waiting for a GPU{named}{',' if since else ''}{since}"





_UNSAID_WAIT_S = 1800.0


class _StartWait:
    """How long a wait for a worker to start may go on: the caller's own bound when given (`budget_s`:
    startup_timeout_s, wait_until_ready's timeout_s), else the platform's deadline for the start - `start_deadline_in_s`,
    the seconds it still gives it, on a starting answer (a ready poll's body, a warming answer's details), counted on this
    machine's monotonic clock, so a robot's clock that is off (a Jetson before NTP) does not move it - else _UNSAID_WAIT_S.
    The earliest deadline said is kept: the platform's for one start only ever stays or shrinks, and a start it ends is
    followed by another with a later one, which this wait does not follow - a robot is not held through start after
    start. WHY: the platform gives a start a card's wait and then what its start takes - more than 1800 s for a slow one -
    so a wait of the SDK's own, counted from the robot's first ask, gave up on a start the platform still ran, and the
    machine it got was ended for nothing.

"""

    def __init__(self, budget_s: float | None, named: str = "startup_timeout_s") -> None:
        self.began = time.monotonic()
        self.budget_s = budget_s
        self.named = named
        self._platform: float | None = None

    def saw(self, said: Any) -> None:
        """Take the platform's deadline for the start from an answer: a ready poll's body, a warming answer's details."""
        try:
            in_s = float(said["start_deadline_in_s"])
        except (KeyError, TypeError, ValueError):
            return
        at = time.monotonic() + max(0.0, in_s)
        self._platform = at if self._platform is None else min(self._platform, at)

    @property
    def bounds_a_line(self) -> bool:
        """Whether a wait in line for a slot ends here: the caller's own bound does; without one the platform ends a line
        itself, at the deployment's queue_timeout_s (a 503 queue_timeout, raised with its sentence)."""
        return self.budget_s is not None

    @property
    def deadline(self) -> float:
        """When the wait ends, on the monotonic clock."""
        if self.budget_s is not None:
            return self.began + self.budget_s
        return self._platform if self._platform is not None else self.began + _UNSAID_WAIT_S

    def waited(self) -> float:
        return time.monotonic() - self.began

    def after(self) -> float:
        """The seconds a give-up says it waited: the caller's own bound as they set it, else how long it waited."""
        return self.budget_s if self.budget_s is not None else self.waited()

    def why(self) -> str:
        """What bounded the wait, as a give-up names it."""
        if self.budget_s is not None:
            return self.named
        return ("the platform's deadline for this start" if self._platform is not None
                else f"{_UNSAID_WAIT_S:.0f}s, the wait when the platform names no deadline")

    def until(self) -> str:
        """How long the wait may still go on, as a notice says it."""
        if self.budget_s is not None:
            return f"{self.named}={self.budget_s:.0f}"
        return f"{max(0.0, self.deadline - time.monotonic()):.0f}s left until {self.why()}"


class Interrupted(BaseException):
    """
    Raised out of a wait - act()'s for a starting worker or a slot, observe()'s first connect, wait_until_ready() - when
    `Policy.interrupt()` stops it.

    BaseException and not Exception on purpose: a caller's code around the wait is entitled to `except Exception` around
    its own hardware errors, and an interrupt that such a handler could swallow would leave the robot waiting after a stop
    was requested.
    """


class _Waits:
    """The waits under act(), observe() and wait_until_ready(), for `Policy`. Every attribute it reads is set by
    `Policy.__init__`."""

    def _open_connection(self, *, wait_s: float | None = None) -> None:
        """
        Connect, and open the connection to the worker, once the platform says the policy is ready (wait_until_ready),
        so the act the robot then sends at once waits for neither (DirectConnection.connect_ahead). Waited for at most
        the connection's own timeout, or `wait_s`. A connection that failed, or was still opening then, does not hold the
        robot: a warning says so and the first act connects, or opens its own, as before. An interrupt() during the wait
        ends it (Interrupted), as it ends wait_until_ready()'s polling. A transport with no worker connection of its own
        (the gateway's) has none to open.
        Before: wait_until_ready() returned as the connect began, so a first act - and the observation it carried -
        waited out the connect and the TLS handshake. After: neither does.



        """
        ahead = getattr(self._t, "connect_ahead", None)
        if ahead is None:
            return


        stop = None if self._interrupt.is_set() else self._interrupt
        missed = ahead(wait=True, wait_s=wait_s, stop=stop)
        if stop is not None and stop.is_set():
            raise Interrupted()
        if missed is not None:
            warn(_not_open_said(missed))

    def _await_connect(self, budget_s: float | None) -> None:
        """
        Connect - the handshake a first act makes - waiting out a worker that is starting, or a place in line, as an
        act does (_wait_out), for at most `budget_s` - or, None, until the platform's deadline for this start: what
        observe() does before its first observation, which needs the policy's declaration to be handed over.

        """
        wait_for = _StartWait(budget_s)
        t_wait0 = wait_for.began
        while True:



            metrics, t0 = CallMetrics(rid=new_rid()), time.monotonic()
            try:
                self._t.handshake()
                return
            except Unavailable as exc:
                metrics.total_ms = (time.monotonic() - t0) * 1000.0
                self._report_failed(metrics, exc)
                self._wait_out(exc, wait_for, t_wait0)
            except Exception as exc:
                metrics.total_ms = (time.monotonic() - t0) * 1000.0
                self._report_failed(metrics, exc)
                raise

    def _wait_out(self, exc: Unavailable, wait_for: _StartWait, t_wait0: float) -> None:
        """One answer of a worker not ready for the robot yet, met while waiting for it (an act, _await_connect):
        `queued` - in line for a slot - asked again at the pace the key's rate limit allows, `warming` at the server's
        own retry_after_s, each said as it goes and within `wait_for`'s deadline; any other, or one past the deadline,
        raised. An interrupt() ends the wait (Interrupted)."""
        wait_for.saw(exc.details)
        if exc.queued:



            wait = self._queue_wait_for(exc)
            if wait_for.bounds_a_line and time.monotonic() + wait > wait_for.deadline:
                raise self._gave_up(Unavailable(
                    f"{exc.message}; still queued after {wait_for.after():.0f}s ({wait_for.why()}), "
                    "giving up",
                    status=exc.status, code=exc.code, body=exc.body, details=exc.details,
                    retry_after_s=exc.retry_after_s, request_id=exc.request_id, hint=exc.hint,
                )) from exc
            self._say_queued(exc.queue_position, _queue_eta(exc), time.monotonic() - t_wait0,
                             exc.details.get("reason"))

            warn(f"queued for a seat (position {exc.queue_position}); waiting {wait:.0f}s before asking "
                 f"again ({wait_for.until() if wait_for.bounds_a_line else 'the line ends at the deployment' + chr(39) + 's queue_timeout_s'})")
            if self._interrupt.wait(wait):
                raise self._gave_up(Interrupted())
            return
        if not exc.warming:
            raise exc

        wait = max(1.0, float(exc.retry_after_s or 5.0))
        if time.monotonic() + wait > wait_for.deadline:

            gpu = _gpu_said(exc.details.get("gpu"))
            raise self._gave_up(Unavailable(
                f"{exc.message}; still warming after {wait_for.after():.0f}s ({wait_for.why()}), giving up"
                + (f"; {gpu}" if gpu else ""),
                status=exc.status, body=exc.body, hint=exc.hint, details=exc.details,
                retry_after_s=exc.retry_after_s, warming=True, job_id=exc.job_id,
            )) from exc













        self._on_warming(wait_for.waited(), wait)
        warn(f"model is warming up; waiting {wait:.0f}s before retrying ({wait_for.until()})")


        if self._interrupt.wait(wait):
            raise self._gave_up(Interrupted())

    def _gave_up(self, exc: BaseException) -> BaseException:
        """`exc`, the end of a wait for a worker or a seat - given up, or stopped by interrupt() - said first to the
        connect it was in (DirectConnection.connect_stopped): failed in the stage it waited in, or dropped unsaid."""
        stopped = getattr(self._t, "connect_stopped", None)
        if stopped is not None:
            stopped(None if isinstance(exc, Interrupted) else exc)
        return exc


    def _ensure_pool(self) -> ThreadPoolExecutor:
        """The one thread an act's HTTP call runs on while its caller's thread watches for a stop
        (_post_interruptible), made on first use."""
        if self._pool is None:
            self._pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="sequence-ai-act")
        return self._pool

    def _post_interruptible(self, payload: dict[str, Any], rid: str, metrics: Any) -> Any:
        """One act - a call, or of your own inputs - that a stop can still cut through: its POST on the act's thread, the
        caller's watching for interrupt(). Before, it ran on the caller's thread, and a stop waited out a slow answer.
        {worker 1's README pass 10-24, train br: act() is the robot's one call now}"""
        return self._watched(self._ensure_pool().submit(lambda: self._t.post("/v1/act", payload, rid=rid,
                                                                             metrics=metrics)))

    def _watched(self, fut: Any) -> Any:
        """`fut`'s result, the caller's thread watching for interrupt() meanwhile (Interrupted)."""
        while not fut.done():
            if self._interrupt.is_set():
                raise Interrupted()
            _wait_futures([fut], timeout=0.02)
        return fut.result()

    def _pause(self, seconds: float) -> None:
        """Wait `seconds` before asking again, an interrupt() ending the wait (Interrupted)."""
        if self._interrupt.wait(max(0.0, seconds)):
            raise Interrupted()
