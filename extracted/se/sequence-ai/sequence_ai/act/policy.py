"""
`Policy` — one robot's session on one model: one open connection, and the two calls on it.

    observe(x)                an observation handed over as the robot makes it
    act()                     one request: the policy's act function called, and what it returned

When to ask for the next answer, and how to play it on the robot, is your own code: run() and the Player went with
train br. {the user 10-24: "Users can just do it themselves because they're calling the act anyway ... Okay, yeah,
we should delete them."} An act is served as it comes; how long a robot can wait for an answer - from the step it
asks for the next to its last valid one - the platform reads from the control loop the policy declares:
@seq.policy(hz=, action_chunk_valid_len=, action_chunk_replan_at=). A robot counts action_chunk_replan_at steps from
when it sends an act, then asks for the next answer; how it joins the new rows to the old is its own.


━━━ Where this sits: the fast half of two brains ━━━

A VLM looks at a snapshot, decides *what* to do next, and says it in a sentence. This package
is the *how*: the sentence goes to the policy with the robot's cameras and joints, as any input
does - policy.observe({"instruction": ..., ...}) - and act() asks it for what to do next. The two
halves run at completely different speeds: the brain thinks between subtasks, the arm needs an
answer every second.

    slow brain   POST /v1/chat               messages in, one message out
    fast brain   this package                 observe({"instruction": "pick up the cup", ...}), act()

Wiring them together — retries, failure detection, choosing the next sub-goal — is the
caller's. This package provides inference, not orchestration.




`interrupt()` is the other half of being a tool: a brain that can start a subtask has to be
able to change its mind. It is thread-safe, and it cuts through an act waiting for a starting
worker or a slow answer — the stop latency is never the service's.
"""

from __future__ import annotations

import atexit
import sys
import threading
import time
import uuid
import weakref
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, nullcontext
from typing import Any, Callable

import httpx

from .._core.capacity import default_queue_notice as _default_queue_notice
from .._core.capacity import queue_wait as _queue_wait
from .._core import direct as _direct
from .._core import gil as _gil
from .._core import seat as _seat
from .._core import marked_observe as _marked
from .._core.late import LateAnswers
from .._core.heartbeat import Heartbeat
from .._core.stale import Stale, StaleState, StaleWatch
from .._core.transport import Transport
from .._core.rid import new_rid
from .._core.names import segment
from .._core.warn import warn
from .._core.reporting import (
    OUTCOME_ERROR,
    OUTCOME_SERVED,
    OUTCOME_WARMING,
    CallMetrics,
    Reporter,
    error_of,
)
from .waits import Interrupted, _StartWait, _Waits, _gpu_said
from ..errors import InvalidRequest, SequencesError, Unavailable, WaitingForPlan
from .types import Ready



def _default_warming_notice(waited_s: float, retry_s: float) -> None:
    """Say that a wait is happening, in the caller's terms rather than the wire's.

    WHY this is not `warnings.warn`: a warning reads as "you did something questionable", and
    a cold start is neither the caller's fault nor a mistake. It is also emitted once per
    Python warning registry by default, so the second and later notices during a
    twenty-minute wait vanish -- exactly when a human most needs to see that something is
    still happening.

    It says how long the wait has been and not how long is left: the platform sends no estimate
    of a cold start, only when to ask again (`retry_s`, 2 s), and printed as "about 2s to go"
    that read as nearly done for the whole of a 139 s wait. On stderr, because a robot's program
    writes its own data to stdout.

    """
    print(f"[sequences] starting the model, which can take minutes "
          f"(waited {waited_s:.0f}s so far)", file=sys.stderr, flush=True)


def _unanswered(exc: Unavailable) -> bool:
    """Whether a ready poll, or the connect wait_until_ready() sends, went unanswered for the moment - its read timed out
    or its connection was cut on the way (the transport's "could not reach"), or the gateway answered 502, 503 or 504 -
    rather than answered for good: refused, out of credit, the key's requests a minute (said with how to poll,
    _ready_body), a line or a wait for its card the platform ended."""
    reason = (exc.details or {}).get("reason")
    if reason == "queue_timeout" or (reason == "gpu_low_stock" and (exc.details or {}).get("waited_s") is not None):
        return False
    return isinstance(exc.__cause__, httpx.TransportError) or exc.status in (502, 503, 504)



_STAGE_WORDS = {"loading": "loading the model",
                "waiting": "starting, slower than its start usually takes"}



_NOTHING = object()



_OPEN: "weakref.WeakSet[Policy]" = weakref.WeakSet()


def _end_reports(reason: str) -> None:
    """The process is ending - a signal its manager sent (seat._on_end_signal calls this first, "signal:SIGTERM"), or
    its exit ("exit"): what each open Policy has waiting to be reported is sent now, as the reporter's next batch will
    not come - its run under way first (late.py), as its close() would end it, under `reason`. Best effort, never
    raises. SIGKILL ends a process before any of this runs.
    WHY the run too: a robot whose script ended, or was stopped with Ctrl+C, without closing its Policy - run for less
    than RUN_REPORT_S, or ending no episode - had its acts reported and its run never, so `seq usage --policy` said its
    on-time share as "—".

    """
    for policy in list(_OPEN):
        try:
            late = getattr(policy, "_late", None)
            if late is not None:
                late.close(reason)
            rep = getattr(policy, "_act_reporter", None)
            if rep is not None:
                rep.close()
        except Exception:
            continue


_seat.on_ending(_end_reports)
atexit.register(_end_reports, "exit")


class Policy(_Waits):
    """
    A handle on one model, holding one live connection.

    Obtained from `sequence_ai.connect(...)`; not constructed directly. Use it as a context
    manager so the connection is closed even when your code raises —— that is the whole reason
    `connect()` returns something with `__enter__`.
    """

    def __init__(self, transport: Transport, model: str,
                 startup_timeout_s: float | None = None,
                 on_warming: Callable[[float, float], None] | None = None,
                 reporter: "Reporter | None" = None,
                 on_queue: Callable[[Any, Any, float, Any], None] | None = None,
                 on_stale: Callable[[Stale], None] | None = None,
                 on_resume: Callable[[Stale], None] | None = None) -> None:
        self._t = transport
        self._model = model


        self._late = LateAnswers(on_run=self._report_run)


        self._stale = StaleWatch(on_stale, on_resume)


        self._beat: Heartbeat | None = None


        self._act_reporter = reporter

        if reporter is not None and hasattr(self._t, "on_trace"):
            self._t.on_trace = lambda report: reporter.record({"connect": report})

















        self._startup_timeout_s = startup_timeout_s




        self._on_warming = on_warming or _default_warming_notice



        self._on_queue = on_queue or _default_queue_notice


        self._queue_said: tuple = (None, float("-inf"))

        self._seat_note_said = False


        self._served_once = False

        self._last_episode: str | None = None
        self._closed = False




        self._episode: str | None = None
        self._episode_lock = threading.Lock()



        self._last_perf: dict = {}





        self._pool: ThreadPoolExecutor | None = None




        self._interrupt = threading.Event()


        _OPEN.add(self)


        _seat._guard_signals()

        _gil.shorten()




        self._drive_lock = threading.RLock()



    @contextmanager
    def _driving(self, what: str):
        """
        Refuse a second thread trying to drive the same Policy.

        WHY this raises instead of serialising: a Policy is one robot's session - its episodes, their numbering, its
        seat on its worker - and two threads acting through it would interleave them, each believing it alone drives
        the robot. Serialising with a blocking lock would hide it differently: the second thread's acts would wait
        for the first's, at half the rate it thinks it runs at. observe() is not driving: it takes no part in this
        lock, so a robot observes on one thread while it acts on another.

        The right shape is one Policy per robot, and it costs nothing to follow: the handshake is paid once per
        Policy, not per call.
        """
        if not self._drive_lock.acquire(blocking=False):
            raise SequencesError(
                f"this Policy is already being driven by another thread; {what}() cannot run "
                "concurrently on the same handle. A Policy is one robot's session, and two "
                "threads acting through it interleave its episodes rather than take turns. Open one "
                "Policy per robot — sequence_ai.connect() is cheap, and the connection handshake "
                "is paid once per Policy rather than once per call."
            )
        try:
            yield
        finally:
            self._drive_lock.release()



    def _report_failed(self, metrics: "CallMetrics", exc: Exception) -> None:
        """An attempt that ended without a chunk: reported as warming when the worker is loading (a 503 the caller waits
        out), else as an error — whatever was raised, not only the platform's own errors, so a failure nobody expected
        still shows on the platform beside the acts that were served. Warming and errors are tagged apart so the
        extreme values land away from the served p50."""
        metrics.outcome = OUTCOME_WARMING if isinstance(exc, Unavailable) and exc.warming else OUTCOME_ERROR
        if metrics.outcome == OUTCOME_ERROR:
            metrics.error = error_of(exc)
        metrics.finalize()
        self._report(metrics)

    def _report(self, metrics: "CallMetrics") -> None:
        """Hand one finalized CallMetrics to the reporter, if any. Best-effort and side-effect-free
        on the control loop: the reporter only buffers and never raises. getattr so a Policy built
        via __new__ in a unit test (no __init__) does not blow up here."""
        rep = getattr(self, "_act_reporter", None)
        if rep is not None:
            rep.record(metrics.to_report())

    def label(self, success: bool, notes: str = "", *, episode_id: str | None = None) -> str:
        """Record how an episode went — the last act()'s, unless `episode_id` names another — with the
        deployment's captured field data (`seq policy set <name> capture=on`), so `seq policy data export` carries it
        as that episode's success label.
        Returns the episode id it labelled - after a reset, the new one it went on under (end_episode).

            policy.act(episode_id="e1")
            policy.label(success=gripper_holds_cup(), notes="")
        """
        episode = episode_id or self._last_episode
        if not episode:
            raise InvalidRequest("no episode to label: act() in one first, or pass episode_id=")
        label = getattr(self._t, "label_episode", None)
        if label is not None:
            return label(episode, success=success, notes=notes) or episode
        self._t.post(f"/v1/deployments/{segment(self._model)}/episodes/{segment(episode)}/label",
                     {"success": bool(success), "notes": notes})
        return episode

    def _episode_for(self, episode_id: str | None) -> str:
        """The episode a call goes under (L0): `episode_id` when it names one - this handle's current episode from now
        on - else the current one, opened now by the first observe() or act() after none was, or after end_episode():
        so its observations reach the policy's observe method, in order, before the act that follows them, with no
        episode named."""
        with self._episode_lock:
            if episode_id is not None:
                self._episode = episode_id
            elif self._episode is None:
                self._episode = uuid.uuid4().hex
            return self._episode

    def end_episode(self, episode_id: str | None = None) -> str | None:
        """End an episode on its worker now - this handle's current one (the one its observe() and act() calls go under
        when they name none, or the last they named), unless `episode_id` names another; the next call opens a new one -
        so a policy that keeps an episode's state frees it at once (its end runs) and its copy is free for the robot's
        next episode. close() ends the one left open.
        Returns the id it ended - after a reset (its copy stopped, the robot moved) the new one it went on under, its
        policy's episode.id; None when none was open. Never raises.

            for episode in episodes:
                for obs in episode.observations():
                    policy.observe(obs)
                    if time_to_act():
                        robot.play(policy.act())
                policy.end_episode()

        WHY: a loop of act() calls had no way to end its episode, and a policy of one copy held it until the
        worker's idle time ran out: the next episode's first act waited for it.
"""
        with self._episode_lock:
            episode = episode_id or self._episode or getattr(self._t, "open_episode", None)
            if episode_id is None or episode == self._episode:

                self._episode = None

        late = getattr(self, "_late", None)
        if late is not None:
            late.end_run("episode_end")
        stale = getattr(self, "_stale", None)
        if stale is not None:
            stale.ended()
        end = getattr(self._t, "end_episode", None)
        if not episode or end is None:
            return None
        return end(episode) or episode

    def observe(self, inputs: Any, *, episode_id: str | None = None) -> int:
        """Hand one observation to the policy as the robot makes it, and get its number in the episode at once. Every
        input goes through observe(); act() carries none.

            for obs in camera.frames():
                policy.observe(obs)                 # every one, as it comes
                if time_to_act():
                    actions = policy.act()          # the act function, once every one before it has gone in

        On a policy that names its methods (L0), each goes to its observe function - every one, in order, before the
        next act() calls its act function - on a connection of its own. It waits on nothing but its first connect,
        which waits out a worker that is starting as a first act() does - within the policy's startup_timeout_s (0:
        Unavailable at once) - and never a later one: one made while its worker restarts mid-episode is kept for the
        episode's next act, which waits for the worker and sends it.

        `episode_id`: the episode's, else this handle's current one - opened by the first observe() or act() after none
        was, or after end_episode() - which the next act() goes under too.

        WHY: an act was the only upload, so every frame between two acts waited for the next one - 24 frames, 1.3 MB and
        a read p50 of 425 ms from a robot at home."""
        episode = self._episode_for(episode_id)
        observe = getattr(self._t, "observe", None)
        if observe is None:
            raise InvalidRequest("this connection takes no observations one by one: send them with the act")
        first = getattr(self._t, "contract", None) is None
        if first and (self._startup_timeout_s is None or self._startup_timeout_s > 0):



            self._await_connect(self._startup_timeout_s)
        self._beat_start()
        return observe(inputs, episode)

    def ready(self) -> Ready:
        """
        Is the model loaded and able to serve? Returns `(ready, eta_seconds)` - a `Ready`, which also says, once a
        worker serves, the card it runs on (`card`) and what one worker costs an hour on it, as billed
        (`usd_per_hour`).

        Does not block, does not need an observation, and the poll is not billed. Polling starts nothing: a poll only
        looks at what this robot holds. While it holds nothing - no seat, no worker starting for it, no place in line -
        `ready` is False and the answer says `cold` (its `status`), and `wait_until_ready()` then connects: that seats
        the robot on a running worker with room, or starts a worker for it in the region nearest the robot - by where
        its connect comes from, behind a VPN where the VPN exits - or puts it in line. A worker started for it is
        billed from the moment its machine has its GPU, its start included.

        Poll it every few seconds - as `wait_until_ready()` does (`poll_s`, 5 s). Each poll is one request on your key's
        requests a minute (600 on Starter, 2,400 on Team), which every robot on the key shares, with its connects and
        keepalives; acts go to the worker and do not count. A robot polling every 0.5 s spends 120 of them a minute:
        five such robots fill Starter's, and the key's requests are refused (429) until the minute rolls on.

        `eta_seconds` counts down to when the worker coming up is expected to serve, by what it is
        doing, from the deployment's own measured start; a typical cold
        start (120 s) when the platform has no estimate. Past what its start should take it is None
        and `eta_unknown` is "past_expected" (stage "waiting": most often its card has not come, which a start
        waits for up to the platform's 10 minutes). The `stage` of
        GET /v1/act/ready's answer says which.

        The answer is for this robot: while it waits in line - put there by its connect, its deployment holding its
        `max_gpus` with every slot taken - `ready` is False though a worker is up. The returned `Ready` then says where
        it stands: `queued` is True and `queue_position` its place; its body's `seat_note` says when the seats it waits
        for come back. A poll takes no seat: in line, the robot's connect asks for one at the line's pace (the answer's
        `retry_after_s`: 1 s at the head of the line, 5 s behind it), and says why it waits and about how long - as
        `wait_until_ready()` and `act()` do.

        A seat follows the Policy that holds it: given back the moment that Policy closes (`close()`, the end of a
        `with`) or its process exits or is told to end (SIGTERM, SIGHUP), and within 60 s of a crash; while the Policy
        is open it is kept between acts by a background keepalive - a robot resetting its scene keeps it - though not
        past the worker's own idle window (`idle_timeout` after the worker's last act), when the worker stops and its
        seats go with it. So is what its connect gives this robot before its first act - its seat, the worker started
        for it, its place in line, which its polls keep - so a robot that gives up waiting frees them at once, or within
        60 s when it is killed. A robot whose seat went takes one again at its next act, or waits in line.
        """
        body = self._ready_body()
        return Ready(bool(body.get("ready")), body.get("eta_s"), body.get("card"), body)

    def _ready_body(self) -> dict:
        """The raw `/v1/act/ready` answer: {ready, eta_s, status}, status being `building` (the image is
        still being built — no worker can start yet), `starting` (the worker it holds a place on is booting), `ready`
        (it holds a seat on a running worker), `queued` (this robot waits in line for a slot: `queue_position`, and
        `retry_after_s` for when its connect asks again), or `cold` (it holds nothing: its connect places it, which
        wait_until_ready() sends - a poll only looks, and starts nothing). A starting answer says how long a start waits
        for its card (`start_wait_s`). It names this robot's session, so the platform answers for this robot: a
        deployment that holds its max_gpus with every slot taken is not ready for it though a worker is up.
        
"""
        self._assert_open()
        session = getattr(self._t, "session", None)
        query = f"model={segment(self._model)}" + (f"&session={session}" if session else "")
        try:
            return self._t.get(f"/v1/act/ready?{query}")
        except Unavailable as exc:
            if exc.status != 429:
                raise


            raise Unavailable(
                f"{exc.message} - ready() polls count against the key's requests a minute, with every robot's on "
                "the key: poll every few seconds, as wait_until_ready() does (every 5 s), or at the line's "
                "retry_after_s", status=exc.status, code=exc.code, body=exc.body, details=exc.details,
                retry_after_s=exc.retry_after_s, request_id=exc.request_id, hint=exc.hint) from exc

    def _say_queued(self, position: Any, eta_s: Any, waited_s: float, reason: Any, note: Any = None) -> None:
        """Tell on_queue where this robot stands - as its connect's line answer says it (_wait_out), never a ready
        poll's, which leaves out why it waits and for about how long. The default notice at a new place or after 5 s
        (the head of the line asks every second); one of the caller's own, on every ask. The default notice also says,
        once a Policy, when the seats this robot waits for come back (`note`, the line answer's hint) - so a line that
        stalls behind a robot that left without closing reads as what it is.
        
"""
        now = time.monotonic()
        if self._on_queue is _default_queue_notice and isinstance(note, str) and note and not self._seat_note_said:
            self._seat_note_said = True
            print(f"[sequences] while in line: {note}", file=sys.stderr, flush=True)
        if self._on_queue is _default_queue_notice:
            if position == self._queue_said[0] and now - self._queue_said[1] < 5.0:
                return
            self._queue_said = (position, now)
        self._on_queue(position, eta_s, waited_s, reason)

    def wait_until_ready(self, timeout_s: float | None = None, poll_s: float = 5.0) -> float:
        """
        Block until the model can serve. Returns the seconds spent waiting.

        **Call this before your control loop, not inside it.** Loading pi0.5 on an L4 takes
        117-125 s for a worker that reads its deployment's compile cache - what a robot waking a
        scaled-to-zero deployment waits for; the first worker, the build check `seq deploy` waits
        for, compiles and takes 275-363 s - and a chunk's execution budget is 533 ms, so a cold
        first `act()` is hundreds of times the budget it lives in, and there is no way for the
        loop to tell that apart from a slow model, because both arrive as one long request.
        




        before — the loop's first iteration absorbs the cold start and the timing is unreadable
        after  — connecting is its own phase; every iteration after it measures the model

            policy.wait_until_ready()        # once, before the robot needs to move
            while running:
                policy.observe(observe())
                for step in policy.act().steps:
                    robot.step(step)

        It places the robot itself: its polls only look, and while one says the robot holds nothing (`cold`) it
        connects - at most once every `poll_s` - which seats the robot on a running worker with room, starts a worker
        for it in the region nearest the robot, or puts it in line. In line, its connect asks for a seat again at the
        line's pace (the answer's `retry_after_s`), saying where it stands and why (`on_queue`), until it is seated or
        the platform's queue_timeout_s ends the line; while a worker starts for it, or its version builds, it only
        polls.

        Once it is seated, the connection to the worker is opened before it returns - the TLS handshake done and the
        worker's certificate checked - so an act sent at once waits for neither, and from then on the robot holds its
        place on the worker as a first act would have given it. That takes at most the connection's own timeout
        (connect(timeout_s=), 30 s by default). A connection that fails, or is still opening then, does not hold it: a
        warning says so, and the first act connects or opens its own.

        Interruptible: `interrupt()` during the wait raises out of it rather than making the
        caller sit through the remaining poll interval — a cold start is long enough that a stop
        issued inside one has to take effect inside it too.

        `timeout_s` bounds the wait from its start. Unset, the policy's `startup_timeout_s` (connect()) bounds it, in
        line or not, as it bounds an act's. With neither - or startup_timeout_s=0, which has an act raise at once
        rather than wait, not this wait the robot asked for - it lasts as long as the platform gives the start under way
        - the deadline it says with each starting answer - and 1800 s while it says none; a line lasts until the
        platform's queue_timeout_s ends it.
        """


        with getattr(self._t, "waiting_ready", nullcontext)():
            return self._poll_until_ready(timeout_s, poll_s)

    def _poll_until_ready(self, timeout_s: float | None, poll_s: float) -> float:
        """wait_until_ready()'s wait, until this robot holds a seat on a running worker - its connection to it open - or
        its limit passes: the seconds that took. A poll only looks (GET /v1/act/ready): what places the robot is its
        connect (DirectConnection.place), sent from here - while it holds nothing (`cold`), at most once every `poll_s`,
        so again after a start that failed or a place that went; in line, as its ask for a seat, at the line's pace with
        no poll between, where it stands said in the connect's own words (_wait_out: its reason and its wait's estimate,
        which a poll's answer leaves out) and the line ended here by the caller's own `timeout_s` alone - the platform's
        queue_timeout_s ends it through the connect; never while a worker starts for it (`starting`) or its version
        builds (`building`). Seated by its connect, its connection opens as on a ready answer.
        
"""


        wait_for = (_StartWait(timeout_s, "wait_until_ready timeout_s") if timeout_s is not None
                    else _StartWait(self._startup_timeout_s or None))
        started = wait_for.began
        missed = 0
        placed: float | None = None
        unplaced = 0
        line = False
        body: dict = {}
        while True:
            if line:
                status = "queued"
            else:
                try:
                    body = self._ready_body()
                except Unavailable as exc:






                    if not _unanswered(exc) or time.monotonic() >= wait_for.deadline:
                        raise
                    missed += 1
                    if missed == 1:
                        print(f"[sequences] {self._model}: the platform did not answer a ready poll ({exc.message}); "
                              "asking again", file=sys.stderr, flush=True)
                    wait = max(0.5, min(poll_s, 2.0 ** (missed - 1), wait_for.deadline - time.monotonic()))
                    if self._interrupt.wait(wait):
                        raise Interrupted()
                    continue
                missed = 0
                wait_for.saw(body)
                if body.get("ready"):




                    self._open_connection()
                    return time.monotonic() - started
                status = body.get("status")



            due = (0.0 if line else poll_s if status == "cold"
                   else float(body.get("retry_after_s") or poll_s) if status == "queued" else None)
            if due is not None and (placed is None or time.monotonic() - placed >= due):
                placed = time.monotonic()
                try:
                    self._t.place()
                except Unavailable as exc:
                    if not (exc.queued or exc.warming):





                        if not _unanswered(exc) or (time.monotonic() >= wait_for.deadline
                                                    and (not line or wait_for.bounds_a_line)):
                            raise
                        unplaced += 1
                        if unplaced == 1:
                            print(f"[sequences] {self._model}: the platform did not answer a connect ({exc.message}); "
                                  "asking again", file=sys.stderr, flush=True)
                        wait = max(0.5, min(poll_s, 2.0 ** (unplaced - 1), wait_for.deadline - time.monotonic()))
                        if self._interrupt.wait(wait):
                            raise Interrupted()
                        continue
                    unplaced = 0
                    line = exc.queued
                    if line:
                        self._wait_out(exc, wait_for, started)
                        continue

                    wait_for.saw(exc.details)
                    body, status = {**exc.details, "status": "starting"}, "starting"
                else:

                    self._open_connection()
                    return time.monotonic() - started
            queued = status == "queued"
            eta = body.get("eta_s")


            if time.monotonic() >= wait_for.deadline and (not queued or wait_for.bounds_a_line):



                doing = ("is still building" if status == "building"
                         else (f"had no slot for this robot: it is at position {body.get('queue_position')} in line"
                               + (f" ({body['seat_note']})" if body.get("seat_note") else ""))
                         if queued
                         else "still had no worker or place in line for this robot (cold)" if status == "cold"
                         else f"was still {_STAGE_WORDS.get(body.get('stage'), 'loading')}"

                              + (f"; it reports about {eta:.0f}s to go" if eta is not None else ""))


                gpu = _gpu_said(body.get("gpu"))
                raise Unavailable(
                    f"{self._model} {doing} after {wait_for.after():.0f}s ({wait_for.why()})"
                    + (f"; {gpu}" if gpu else ""),
                    status=503, body={}, retry_after_s=eta, warming=True,
                    details={"gpu": body["gpu"]} if gpu else None,
                )




            asked = body.get("retry_after_s") if queued else None
            wait = max(0.5, min(poll_s, asked or poll_s, wait_for.deadline - time.monotonic()))
            if self._interrupt.wait(wait):
                raise Interrupted()

    def act(self, observation: Any = _NOTHING, *, episode_id: str | None = None, seed: int | None = None) -> Any:
        """
        One act: the policy's act function called, and what it returned - as it returned it.

            policy.observe(x)              # every input goes through observe()
            out = policy.act()             # the act function, once every observation before it has gone in

        act() carries no data. Every input goes through observe(x), and act() calls the policy's act function once every observation the episode's
        observe() handed over before it has gone in, in order (to its observe method, or kept as the latest for an act
        function that reads it), taking no step: act(x) is refused before it goes. What comes back is what the act
        function returned: an array as an array of its dtype and shape, bytes as bytes, a torch tensor as a numpy
        array.


        `episode_id`: the episode the act belongs to - a policy that keeps an episode's state keeps it under that id;
        end it with `end_episode()`. With none named it goes under this handle's current episode, the one observe()
        goes under, so the observations handed over before the act reach the policy first.

        `seed`: the sampling seed the policy's act function is handed, for a reproducible answer - an eval's; None,
        none. Nothing else goes with an act: how many steps of an answer are valid, when the next is asked for and at
        what rate is the policy's to declare (@seq.policy(hz=, action_chunk_valid_len=, action_chunk_replan_at=)), and
        what differs
        between robots goes in their observations.

        What the platform noted of an answer is said with warnings.warn, once for each kind.

        ⚠️ What comes back is model output, not a safe robot command. Nothing in this
        library checks joint limits, reachability, collisions, or whether the step is safe at
        the robot's current velocity. Validate before you actuate.

        A worker that is starting - the first, or one starting because the robot's last one stopped `idle_timeout`
        after its last act - is waited out: within the policy's
        `startup_timeout_s` (by default the platform's deadline for the start; 0 raises `Unavailable` at once
        instead), and `interrupt()` from another thread ends the wait.
        """






        stale = self._interrupt.is_set()
        self._assert_open()
        self._beat_start()
        if _marked.holds(observation):

            raise InvalidRequest("act(): a sequence_ai.Video, Depth or Tactile item goes in observe(), which sends it as "
                                 "what it marks; act() sends no marker")
        with self._driving("act"):


            if stale:
                self._interrupt.clear()
            options: dict[str, Any] = {} if seed is None else {"seed": seed}


            options["episode_id"] = self._episode_for(episode_id)
            driven = getattr(self._t, "teleop", None)
            asked = None
            if driven is not None:


                chunks = driven.chunks
                here, out = driven.answer()
                if here:
                    self._last_episode = options["episode_id"]
                    self._driven_here(driven, chunks)
                    return out
                asked = driven.changes
            if observation is _NOTHING and not isinstance(self._t, _direct.DirectConnection):
                raise InvalidRequest("act() with nothing calls the policy's act function on its worker, which only a "
                                     "direct connection reaches")
            self._last_episode = options["episode_id"]
            return self._answer(observation, options, asked)

    def _answer(self, inputs: Any, options: dict[str, Any], asked: int | None = None) -> Any:
        """
        What one act returns: what the policy's act function returned, as it returned it
. A worker that is starting - or a slot this robot waits in line for - is waited out
        within `startup_timeout_s` rather than raised.

        **act() waits on every call.** One call is one result. A first call can
        find the fleet switched off AND the model unloaded, and pays for both (~180 s for a worker plus 300-1650 s to
        provision and load); a later one can find that the robot's worker stopped `idle_timeout` after its last act,
        its slots with it, and that the one starting in its place is not up yet. Handing the caller the platform's 503
        to decode is what this absorbs: they get a line of English and an answer.
        

        Before, only a policy's first call waited; a later one raised. On dev with 0.35.0, a policy left open had its
        worker stopped 72 s after its last act, and its next call raised Unavailable "the worker is still starting"
        after 7.8 s.
        A teleop robot's act that went while its model drove (`asked`, who drives as it went) is held to who drives as
        its answer comes: stopped or taken by a person on its way, act() hands back what it would answer now - a
        person's chunk, else hold - not the policy's answer, a release since included (_core/teleop_robot.py
        Driven.after).

        """
        body, done = self._arm_watched(inputs, options)
        self._served_once = True
        self._took(body)
        driven = getattr(self._t, "teleop", None)
        if driven is not None:
            driven.answered(body.get("outputs"))
            if asked is not None:
                chunks = driven.chunks
                here, out = driven.after(asked)
                if here:
                    self._driven_here(driven, chunks, done)
                    return out
        watch = getattr(self, "_stale", None)
        if watch is not None:
            watch.resume_owed()
            if done is not None:
                watch.resume(done)
        return body.get("outputs")

    def _driven_here(self, driven: Any, chunks: int, done: Any = None) -> None:
        """act() answered as a person or a stop says, not its model (`chunks`: a person's chunks handed back before it):
        nothing of the policy's to watch, and a stretch with nothing to play that ends with it - under way, or `done` -
        resumed only with a person's chunk in hand: the hold has nothing to play, so its on_resume waits for what does
        (_core/stale.py StaleWatch.taken, resume_owed)."""
        watch = getattr(self, "_stale", None)
        if watch is not None:
            watch.taken(done)
            if driven.chunks != chunks:
                watch.resume_owed()

    def _arm_watched(self, inputs: Any, options: dict[str, Any]) -> tuple:
        """_predict_raw, the arm watched while it is on its way (_core/stale.py): asked while the answer the robot plays
        still has valid steps, it is watched to when that answer runs out, and its own answer after it - (its answer,
        the stretch with nothing to play it ended: None for none), that stretch resumed - on_resume - by _answer before
        act() hands the answer back."""
        watch = getattr(self, "_stale", None)
        chunk_ends = getattr(self._t, "chunk_ends", None)
        if watch is None or not callable(chunk_ends):
            return self._predict_raw(inputs, options), None
        ends = chunk_ends()
        ahead = ends is not None and ends > time.monotonic()
        watch.asking(ends, options.get("episode_id"))
        try:
            body = self._predict_raw(inputs, options)
        except BaseException:
            watch.failed()
            raise
        return body, watch.answered(chunk_ends(), ahead)

    def _beat_start(self) -> None:
        """The heartbeat, from the first observe() or act() on: a robot heard from by its worker (_core/heartbeat.py),
        on a connection that holds one - a direct one."""
        send = getattr(self._t, "heartbeat", None)
        if getattr(self, "_beat", None) is None and callable(send) and not self._closed:
            self._beat = Heartbeat(self)

    @property
    def stale(self) -> StaleState:
        """Whether the arm has nothing valid to play now, and the stretches it had none (_core/stale.py): `.now` the one
        under way (None while it has an answer to play), `.events` how many there were, `.stale_s` how long the ended
        ones lasted together, `.last` the last that ended. connect(on_stale=, on_resume=) is told of each as it goes."""
        return self._stale.state

    def _took(self, body: dict) -> None:
        """An answer on its way to act()'s caller: its perf kept (_last_perf) - each try was reported as it went
        (_predict_raw)."""
        self._last_perf = body.get("perf") if isinstance(body.get("perf"), dict) else {}

    def _note_outside(self, metrics: CallMetrics) -> None:
        """What an act its worker answered spent outside the worker - its time here less the worker's handler_ms - into
        its connection's window, which each next act tells the worker (X-Seq-Outside-Ms): the worker holds an act for
        other robots only within what is left of the robot's buffer after it. Not an act that waited for a starting
        worker, came first after a connect (the connect is in its time) or opened its connection: none of that comes
        again on the next act."""
        note = getattr(self._t, "note_outside", None)
        handler = metrics.perf.get("handler_ms") if isinstance(metrics.perf, dict) else None
        if (note is None or metrics.total_ms is None or metrics.warmup_ms is not None or metrics.first_after_connect
                or metrics.tcp_ms is not None or metrics.tls_ms is not None
                or not isinstance(handler, (int, float)) or isinstance(handler, bool)):
            return
        note(metrics.total_ms - float(handler))

    def _predict_raw(self, inputs: Any, options: dict[str, Any]) -> dict:
        """act() of your own inputs, or of none (a call, L0): one /act carrying {inputs, seed, episode_id, params} -
        none of the inputs for a call - and its worker's answer, its `outputs` untouched. A worker that is starting, or a
        slot this robot waits in line for, is waited out as observe()'s first connect waits it out (_wait_out): each
        retry said, within `startup_timeout_s` - 0 raises at once."""
        payload: dict[str, Any] = {"model": self._model, **({"inputs": inputs} if inputs is not _NOTHING else {})}
        payload.update({k: v for k, v in options.items() if v is not None})
        wait_for = _StartWait(self._startup_timeout_s)
        while True:


            rid = new_rid()
            metrics = CallMetrics(rid=rid)
            stale = getattr(self, "_stale", None)
            if stale is not None:
                stale.trying(rid)
            t0 = time.monotonic()
            try:


                body = self._post_interruptible(dict(payload), rid, metrics)
                metrics.total_ms = (time.monotonic() - t0) * 1000.0
                if isinstance(body, dict) and not isinstance(body.get("perf"), dict):
                    body["perf"] = {}
                metrics.perf = body["perf"] if isinstance(body, dict) else {}





                waited_ms = (t0 - wait_for.began) * 1000.0
                if waited_ms >= 250:
                    metrics.warmup_ms = metrics.perf["warmup_ms"] = round(waited_ms, 2)



                metrics.frames = getattr(self._t, "steps_played", None)
                metrics.outcome = OUTCOME_SERVED


                late = getattr(self, "_late", None)
                if late is not None:
                    late.answered(metrics.total_ms, getattr(self._t, "_plays", None),
                                  counted=not (metrics.first_after_connect or metrics.warmup_ms is not None
                                               or metrics.tcp_ms is not None or metrics.tls_ms is not None),
                                  worker_ms=metrics.perf.get("handler_ms") if isinstance(metrics.perf, dict) else None,
                                  left_ms=metrics.chunk_left_ms)
                metrics.finalize()
                self._note_outside(metrics)



                if metrics.rid_echo is not None and metrics.rid_echo != rid:
                    metrics.rid_mismatch = True
                    warn("the worker answered this act under another request id than the one it was sent, so "
                         "`seq policy logs --rid` cannot join the worker's lines to it")
                self._report(metrics)
                break
            except Unavailable as exc:
                metrics.outcome = OUTCOME_WARMING if exc.warming else OUTCOME_ERROR
                if metrics.outcome == OUTCOME_ERROR:
                    metrics.error = error_of(exc)
                metrics.finalize()
                self._report(metrics)
                self._wait_out(exc, wait_for, wait_for.began)
            except WaitingForPlan:

                metrics.outcome = OUTCOME_WARMING
                metrics.finalize()
                self._report(metrics)
                raise
            except Exception as exc:
                metrics.outcome = OUTCOME_ERROR
                metrics.error = error_of(exc)
                metrics.finalize()
                self._report(metrics)
                raise

        return body

    @property
    def driver(self) -> str:
        """Who drives this robot now: "model", "human" (a person, from their console: sequence_ai.teleop) or "stopped" -
        as its worker last said on its stream, a robot connected with teleop=True; "model" for any other."""
        driven = getattr(self._t, "teleop", None)
        return driven.driver if driven is not None else "model"

    def _queue_wait_for(self, exc: Unavailable) -> float:
        """How long to wait before asking again for a place in line; one place for act() and observe()'s first
        connect."""
        return _queue_wait(exc)

    def _assert_open(self) -> None:
        if self._closed:
            raise SequencesError("this policy is closed; open a new one with sequence_ai.connect()")

    @property
    def model(self) -> str:
        return self._model

    def interrupt(self) -> None:
        """
        Stop what this Policy is waiting on now: an act's wait for a starting worker or a slot, or for its answer, an
        observe()'s first connect, wait_until_ready(). It raises `Interrupted` out of that call. Thread-safe, and the
        only method meant to be called from a thread other than the one driving.

        Idempotent and safe to call when nothing is waiting: the flag is cleared at the start of each act, so an
        interrupt arriving between acts does not cancel the next one.
        """
        self._interrupt.set()

    def _report_run(self, run: dict) -> None:
        """A run of its acts as late.py ended it: one row with its reports, best-effort (reporting.run_record)."""
        rep = getattr(self, "_act_reporter", None)
        if rep is not None:
            rep.record({"run": run})

    def close(self) -> None:
        """Close the connection. Idempotent."""
        if self._closed:
            return
        self._closed = True





        if self._pool is not None:
            self._pool.shutdown(wait=True)
            self._pool = None

        late = getattr(self, "_late", None)
        if late is not None:
            late.close()
        stale = getattr(self, "_stale", None)
        if stale is not None:
            stale.close()
        beat = getattr(self, "_beat", None)
        if beat is not None:
            beat.close()


        rep = getattr(self, "_act_reporter", None)
        if rep is not None:
            rep.close()
        self._t.close()

    def __enter__(self) -> "Policy":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
