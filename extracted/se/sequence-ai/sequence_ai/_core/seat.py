"""
A connected session's seat, from the robot's side (sequence_ai/_core/direct.py's DirectConnection): what gives it back -
at close(), the end of a `with`, the connection's collection, the process's exit, or a signal that ends the process -
and the keepalive that holds it while the robot stays connected.

In one sentence: a DirectConnection holds what its seat needs by a _SeatHold, kept apart from the connection →
weakref.finalize gives the seat back (_give_back, POST /v1/act/release) when the connection is collected or the
process exits → a SIGTERM or SIGHUP that would end the process with no exit hook runs _on_end_signal first: each open
Policy's run reported (on_ending's hooks) and every open connection's seat given back (_LIVE), _GIVE_BACK_WAIT_S at most
→ while it is open, its keepalive's thread (_keep_alive) beats the platform every every_s by either clock, and again
soon after a beat that did not reach it.
WHY a module of its own: sequence_ai/_core/direct.py had passed 1,500 lines; these hold a seat and end a process, and
reach a connection only through what it hands them.
"""
from __future__ import annotations

import os
import signal
import sys
import threading
import time
import weakref
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Callable, Iterator, Optional

if TYPE_CHECKING:
    from .direct import DirectConnection
    from .transport import Transport


class _SeatHold:
    """What a connected session needs to give its seat back, held apart from its connection: the finalizer that gives it
    back when the connection is collected, or when the process exits, must hold no reference to the connection itself
    (one would keep it alive for ever)."""

    __slots__ = ("gateway", "model", "session", "pid", "sent")

    def __init__(self, gateway: Transport, model: str, session: str) -> None:
        self.gateway, self.model, self.session = gateway, model, session

        self.pid = os.getpid()

        self.sent = False


def _give_back(hold: _SeatHold) -> None:
    """Give `hold`'s seat back now (POST /v1/act/release) - or its place in line - instead of when it runs out, so the
    next robot in line starts at once. Called by close() and the end of a `with`, and - through weakref.finalize -
    when the connection is collected or the process exits without either: a robot whose program ends, or raises out,
    without close() no longer holds its seat until it runs out. Once at most (the finalizer runs once); never in a
    process forked from the one that connected; best effort, never raises.

    """
    if not hold.sent or os.getpid() != hold.pid:
        return
    try:
        hold.gateway.post("/v1/act/release", {"model": hold.model, "session": hold.session}, timeout_s=3.0)
    except Exception:
        pass




_LIVE: weakref.WeakSet[DirectConnection] = weakref.WeakSet()



_ENDING_SIGNALS = ("SIGTERM", "SIGHUP")



_GIVE_BACK_WAIT_S = 5.0



_ENDING: list[Callable[[str], None]] = []


def on_ending(hook: Callable[[str], None]) -> None:
    """Have `hook(reason)` called first when a signal ends the process (_on_end_signal)."""
    if hook not in _ENDING:
        _ENDING.append(hook)


_guarded = False
_guard_lock = threading.Lock()


def _guard_signals() -> None:
    """Give back what this process's Policies hold when SIGTERM or SIGHUP ends it, too - not only at close(), the end
    of a `with`, collection or a normal exit: a process stopped by its manager ran no exit hook, and its seat, or its
    place in line, held up the robots behind it until it ran out. Installed once, when a Policy first asks for a place
    (a connect, or a ready() poll that names its session), from the main thread, and over a signal's default action
    only: a program that handles a signal itself keeps its own handler.
 
"""
    global _guarded
    if _guarded or threading.current_thread() is not threading.main_thread():
        return
    with _guard_lock:
        if _guarded:
            return
        _guarded = True
        for name in _ENDING_SIGNALS:
            sig = getattr(signal, name, None)
            if sig is None:
                continue
            try:
                if signal.getsignal(sig) is signal.SIG_DFL:
                    signal.signal(sig, _on_end_signal)
            except (ValueError, OSError):
                continue


def _on_end_signal(signum: int, frame: Any) -> None:
    """SIGTERM / SIGHUP: report each open Policy's run under way, as it stands, and send its reports (_ENDING), and give
    back what every open Policy holds - its seat, the worker its connect started, its place in line - then end as
    the signal would have, its default action raised again. Both run on threads of their own, waited for
    _GIVE_BACK_WAIT_S at most, so a lock the interrupted code held can never keep the process from ending; a seat it did
    not reach runs out on its own (seat_ttl_s, 60 s)."""
    def give_back_all() -> None:
        for conn in list(_LIVE):

            try:
                conn._give_back()
            except Exception:
                continue

    def report_all() -> None:
        try:
            name = signal.Signals(signum).name
        except ValueError:
            name = str(signum)
        for hook in list(_ENDING):
            try:
                hook(f"signal:{name}")
            except Exception:
                continue


    workers = [threading.Thread(target=report_all, name="seq-end-report", daemon=True),
               threading.Thread(target=give_back_all, name="seq-give-back", daemon=True)]
    deadline = time.monotonic() + _GIVE_BACK_WAIT_S
    for w in workers:
        w.start()
    for w in workers:
        w.join(max(0.0, deadline - time.monotonic()))
    signal.signal(signum, signal.SIG_DFL)
    os.kill(os.getpid(), signum)




_SEAT_TICK_S = 1.0

_SEAT_RETRY_S = 2.0


_MOVE_ASK_S = 2.0


def _keep_alive(ref: "weakref.ref[DirectConnection]", stop: threading.Event) -> None:
    """The seat keepalive's thread: every `every_s` the platform's connect named (seat_ttl_s / 3, 20 s), tell it this
    Policy is alive (DirectConnection._keep_seat) until the connection closes or is collected. It holds only a weak
    reference between beats, so a Policy dropped without close() is still collected - and gives its seat back.

    A beat is due by either clock - the wall clock, which goes on while a machine sleeps or a process is paused, and the
    monotonic one, which a clock set back does not move - so a robot that wakes beats within _SEAT_TICK_S. A beat that
    does not reach the platform (the network out) is tried again every _SEAT_RETRY_S while the seat may still be held
    (DirectConnection._may_hold: seat_ttl_s of the platform's last word): an outage that ends inside that keeps the
    seat, where the next beat 20 s on could come after it went. Before, a beat lost to a 25 s Wi-Fi drop was not tried
    again for 20 s, and the seat ran out with the network back.

    """
    due_wall = due_mono = None
    while True:
        conn = ref()
        if conn is None:
            return
        if due_wall is None:
            every = conn._keepalive_every_s or 20.0
            due_wall, due_mono = time.time() + every, time.monotonic() + every
        if conn._move_waits():


            soon = 0.0 if conn._move_ask_now() else _MOVE_ASK_S
            due_wall = min(due_wall, time.time() + soon)
            due_mono = min(due_mono, time.monotonic() + soon)
        del conn
        if stop.wait(max(0.0, min(_SEAT_TICK_S, due_mono - time.monotonic(), due_wall - time.time()))):
            return
        if time.time() < due_wall and time.monotonic() < due_mono:
            continue
        conn = ref()
        if conn is None or conn._closed:
            return
        said = conn._keep_seat()
        if said == "kept":
            conn._renew_ahead()
        if conn._switched:
            conn._report_switch()
        conn._keep_standby()
        again = _SEAT_RETRY_S if said == "unreached" and conn._may_hold() else (conn._keepalive_every_s or 20.0)
        due_wall, due_mono = time.time() + again, time.monotonic() + again
        del conn


class _KeptSeat:
    """A DirectConnection's seat while its Policy is open, mixed into it as _Episodes is: one beat of the keepalive and
    what its answer means (_keep_seat), how long the platform may still hold the seat (_may_hold), what the robot is told
    when it went (_say_seat_went), the keepalive's start (_seat_alive) and a seat given back to connect again (_reseat).
    The connection, its lock and its worker are DirectConnection's (direct.py).
    WHY here: direct.py had passed 1,500 lines again."""

    def _reseat(self, worker: Any, attempt: int) -> None:
        """Its worker has no place for its next episode (429 no_place): its seat goes back and it connects again. From
        before that release until the connect answers, however it answers, its keepalive stands aside: the platform
        holds no seat for it in between, and says so to any beat ("held": false) - of a seat the robot gave back itself.
        Before: a beat in that gap, up to 2 s of backoff long, ended its keepalives until the connect and told the robot
        its seat had gone because no keepalive had reached the platform for 60 s, with its beats reaching it.


        """
        with self._lock:

            self._reseating += 1
            self._given_back += 1
        try:
            _give_back(self._hold)
            self._reconnect(worker, backoff_attempt=attempt)
        finally:
            with self._lock:
                self._reseating -= 1

    @contextmanager
    def waiting_ready(self) -> Iterator[None]:
        """While wait_until_ready() polls: a seat that goes meanwhile is not said (_say_seat_went)."""
        self._waiting_ready = True
        try:
            yield
        finally:
            self._waiting_ready = False

    def _keep_seat(self) -> str:
        """One keepalive (POST /v1/act/keepalive): the seat this session holds is kept seat_ttl_s more. It keeps the
        seat alone - not the worker, which stops idle_timeout after its last act whatever its robots' keepalives say,
        and its seats with it. When the platform says the seat is gone ("held": false - released, run out, or its
        worker stopped), keepalives stop, the robot is told (_say_seat_went), and the next act renews at once, which
        seats the robot again or puts it in line. Unreached: nothing changes; the seat lasts its seat_ttl_s and the
        keepalive tries again soon (_keep_alive). A kept seat's answer may say its worker is leaving (`rotate`, as a
        renewal does): the robot is told once and moves at its next episode boundary. What it came to - "kept", "gone",
        "unreached" or "off" (none asked for, or its seat is going back: _reseat). Never raises."""
        given_back = self._given_back
        if not self._seat_kept or self._reseating:
            return "off"
        sent_on = self._worker
        self._beat_mono = time.monotonic()
        try:

            body = self._gateway.post("/v1/act/keepalive", {"model": self._model, "session": self._session,
                                                            **({"through": True} if self._planner else {})},
                                      timeout_s=5.0)
        except Exception:
            return "unreached"
        if not isinstance(body, dict):
            return "unreached"
        if body.get("held") is False:
            if self._given_back != given_back:
                return "off"
            with self._lock:
                self._seat_kept = False

                if self._worker is not None:
                    self._lease_deadline = time.monotonic()
            self._say_seat_went(body.get("why"))
            return "gone"
        self._kept_at = time.time()
        if "request_timeout_s" in body:


            self._take_request_timeout(body["request_timeout_s"])
        every, ttl = body.get("every_s"), body.get("seat_ttl_s")
        if isinstance(every, (int, float)) and not isinstance(every, bool) and every > 0:
            self._keepalive_every_s = float(every)
        if isinstance(ttl, (int, float)) and not isinstance(ttl, bool) and ttl > 0:
            self._seat_ttl_s = float(ttl)
        if "standby_retry_s" in body:




            with self._lock:
                self._plan_standby_ask(body["standby_retry_s"])
        rotate = body.get("rotate")
        if isinstance(rotate, dict):





            from .direct import _ready
            with self._lock:
                if self._worker is not sent_on:
                    return "kept"
                was, self._rotate = self._rotate, rotate
                if (_ready(rotate) and not _ready(was) and not self._episode_open
                        and self._worker is not None):
                    self._lease_deadline = time.monotonic()
            if not was:
                self._say_moving(rotate)
        return "kept"

    def _may_hold(self) -> bool:
        """Whether the platform may still hold this robot's seat: within seat_ttl_s, by the wall clock, of the last time
        it said so. Past it the seat has gone whatever a beat would say, and the keepalive keeps its own pace."""
        return self._kept_at is not None and time.time() - self._kept_at < self._seat_ttl_s

    def _say_seat_went(self, why: Optional[str] = None) -> None:
        """The robot's place went while its Policy is open: said once each time, on stderr as the line's notices are,
        so a robot that lost its seat while it could not reach the platform - longer than seat_ttl_s - or whose worker
        stopped knows why its next act waits.
 
A robot in line had no seat: it is told it is no longer in line. `why` is the platform's reason when it
        gives one - "stopped": its deployment was stopped, which the line names instead of a lost keepalive.


        A lost keepalive is named only when one was: the platform's last word within seat_ttl_s (_may_hold) means
        nothing ran out. In wait_until_ready() only a stop is said, as its next connect places the robot again. Before,
        both said no keepalive had reached the platform for 60 s.

 
"""
        if self._waiting_ready and why != "stopped":
            return
        in_line = self._in_line
        place = (f"this robot is no longer in line for a seat on {self._model}" if in_line
                 else f"the platform no longer holds this robot's seat on {self._model}")
        then = "the next act " + ("puts it in line again" if in_line else "takes a seat again, or waits in line")
        if why == "stopped":
            cause = (f"{self._model} was stopped; its acts are refused until `seq policy start {self._model}` lets "
                     "robots connect again")
        elif self._may_hold():
            heard = f"the platform heard from it {max(0.0, time.time() - self._kept_at):.0f} s ago"
            cause = (f"{heard} and let its place go; {then}" if in_line
                     else f"{heard}, so its worker stopped or the seat was released; {then}")
        else:
            cause = (f"no keepalive reached it for {self._seat_ttl_s:.0f} s (the network out, or the process paused), "
                     f"or its worker stopped; {then}")
        print(f"[sequences] {place}: {cause}", file=sys.stderr, flush=True)

    def _seat_alive(self, body: dict, *, ready: bool = False) -> None:
        """After a connect, or a ready poll that says what this robot holds (`ready`): keep its place alive as the
        platform asked (`keepalive.every_s`), starting the keepalive's thread on the first such answer. A connect
        always asks (this client asks it to); a ready answer that asks nothing (building, cold: nothing held) leaves
        the keepalives as they were."""
        asked = body.get("keepalive") if ready else body["keepalive"]
        if not isinstance(asked, dict):
            return
        self._keepalive_every_s = float(asked["every_s"])
        self._seat_kept = True
        self._kept_at = time.time()
        ttl = asked.get("seat_ttl_s")
        if isinstance(ttl, (int, float)) and not isinstance(ttl, bool) and ttl > 0:
            self._seat_ttl_s = float(ttl)
        if self._keepalive_thread is None:
            self._keepalive_thread = threading.Thread(
                target=_keep_alive, args=(weakref.ref(self), self._keepalive_stop), daemon=True,
                name="seq-seat-keepalive")
            self._keepalive_thread.start()
