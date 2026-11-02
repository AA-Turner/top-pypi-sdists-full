"""
The arm with nothing valid left to play, said the moment it happens: once the answer a robot plays runs out with no
answer after it in hand, connect(on_stale=) is called then, from a thread of the SDK's; once one comes, on_resume,
before act() hands it back. Each is logged on "sequence_ai" and kept on `policy.stale`.

In one sentence: an act sent while the answer its robot plays still has valid steps - the robot asks ahead, as late.py
holds it - → that answer runs out at its own act's send time plus its action_chunk_valid_len steps at hz (what the act
told the worker was left of it, X-Seq-Chunk-Left-Ms), and so, once such an act is answered, does the new one → past that
time with no answer in hand the arm has nothing valid to play: stale - "late" while an act is on its way, "failed" when
the last one raised, "not asked" when the robot's loop asked for none in time (the loop's heartbeat: one that hangs
mid-run is said as surely as a late answer) → the next answer ends it, with how long the arm went without one.
Not watched: a robot that asks only once the answer before ran out (it waits for every answer, its loop's own pace, as
late.py holds none of it), an episode ended (end_episode()), a closed Policy, a teleop robot while a person drives it,
and a policy that declares no valid length or no hz.
WHY: the docs told a robot's code to keep a watchdog of its own, and the deadline it needs - when the answer it plays
runs out - is the SDK's to know. It is no emergency stop: a physical one stays between this library and the motors.


"""
from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional

from .warn import warn

_log = logging.getLogger("sequence_ai")

_SAID = threading.Event()

LATE, FAILED, NOT_ASKED = "late", "failed", "not asked"
_WHY = dict([(LATE, "the act for the next one still on its way"), (FAILED, "the act for the next one raised"),
             (NOT_ASKED, "no act asked for the next one")])


@dataclass(frozen=True)
class Stale:
    """
    One stretch the arm had nothing valid to play: what on_stale and on_resume are called with.

    reason      "late": the act for the next answer was on its way; "failed": the last act raised (the robot's loop
                has its error); "not asked": no act was on its way - the robot's loop asked for none in time
    at          when the answer the robot played ran out (UTC)
    episode_id  the episode it was in
    request_id  the act on its way ("late"): `seq policy logs --rid` finds the worker's lines of it
    stale_s     on_resume's: how long the arm went without an answer; None in on_stale's, said as it ran out
    """
    reason: str
    at: datetime
    episode_id: Optional[str] = None
    request_id: Optional[str] = None
    stale_s: Optional[float] = None


@dataclass(frozen=True)
class StaleState:
    """`policy.stale`: the stretch under way (None while the arm has an answer to play), how many there were and how
    long the ended ones lasted together, the last that ended, and whether the robot asks ahead now - its answer
    watched to when it runs out (what its heartbeat says as "acting")."""
    now: Optional[Stale]
    events: int
    stale_s: float
    last: Optional[Stale]
    ahead: bool = False


class StaleWatch:
    """One Policy's arm, watched (see the module): asking() as an act goes, trying() for each try of it, answered() as
    its answer comes, failed() as it raises, ended() as its episode ends or a person drives, close() with the Policy.
    `thread` False: no watcher of its own - check() is the step it takes, a test's to call."""

    def __init__(self, on_stale: Optional[Callable[[Stale], None]] = None,
                 on_resume: Optional[Callable[[Stale], None]] = None, *,
                 clock: Callable[[], float] = time.monotonic,
                 wall: Callable[[], datetime] = lambda: datetime.now(timezone.utc), thread: bool = True) -> None:
        self._on_stale = on_stale
        self._on_resume = on_resume
        self._clock = clock
        self._wall = wall
        self._threaded = thread
        self._cond = threading.Condition()
        self._ends: Optional[float] = None
        self._asked = False
        self._rid: Optional[str] = None
        self._failed = False
        self._episode: Optional[str] = None
        self._now: Optional[Stale] = None
        self._since: Optional[float] = None
        self._events = 0
        self._stale_s = 0.0
        self._last: Optional[Stale] = None
        self._owed: Optional[Stale] = None
        self._thread: Optional[threading.Thread] = None
        self._closed = False

    @property
    def state(self) -> StaleState:
        with self._cond:
            return StaleState(self._now, self._events, round(self._stale_s, 3), self._last,
                              ahead=self._ends is not None and self._now is None)

    def asking(self, ends: Optional[float], episode: Optional[str]) -> None:
        """An act going now, the answer the robot plays running out at `ends` (the clock's; None: not known)."""
        with self._cond:
            self._asked, self._rid, self._failed, self._episode = True, None, False, episode
            if ends is not None and ends > self._clock():
                self._ends = ends
                self._start()
            elif self._now is None:
                self._ends = None
            self._cond.notify()

    def trying(self, rid: str) -> None:
        """The act on its way goes as `rid` now (each try is a request of its own)."""
        with self._cond:
            self._rid = rid

    def answered(self, ends: Optional[float], ahead: bool) -> Optional[Stale]:
        """Its answer came: the robot plays it to `ends`, watched there if its act was asked ahead and that time is
        still to come (an answer that came after its own valid time, counted from its send as late.py counts it,
        leaves the loop asking once it ran out: its own pace again); the stretch it ends, for resume() - None when
        there was none."""
        with self._cond:
            self._asked, self._rid, self._failed = False, None, False
            self._ends = ends if ahead and ends is not None and ends > self._clock() else None
            done = self._end()
            if self._ends is not None:
                self._start()
            self._cond.notify()
        return done

    def failed(self) -> None:
        """The act raised: the answer the robot plays still runs out when it does, said "failed" then."""
        with self._cond:
            self._asked, self._rid, self._failed = False, None, True
            self._cond.notify()

    def ended(self) -> None:
        """Nothing of the policy's to watch - its episode ended, or a person drives the robot: a stretch under way ends
        with no resume, no answer having come."""
        with self._cond:
            self._ends, self._asked, self._rid, self._failed = None, False, None, False
            done = self._end()
            self._cond.notify()
        if done is not None:
            _log.info("the arm's stretch with nothing to play ended with its episode after %.0f ms (%s)",
                      (done.stale_s or 0.0) * 1000.0, done.reason)

    def close(self) -> None:
        """The Policy closed: nothing more is watched, and its watcher ends."""
        with self._cond:
            self._closed, self._ends = True, None
            self._end()
            self._cond.notify_all()

    def check(self) -> None:
        """Say a stretch that begins now: the watcher's step."""
        with self._cond:
            due = self._due()
        if due is not None:
            self._say(due)

    def taken(self, done: Optional[Stale] = None) -> None:
        """A person drives the robot, or it is stopped (teleop_robot.Driven): nothing of the policy's is watched, and
        the stretch that ends with it - the one under way, or `done`, ended by an answer no one plays - is not resumed:
        on_resume would tell the robot's code its arm has something to play, and it has none. It is owed that resume
        (resume_owed)."""
        with self._cond:
            self._ends, self._asked, self._rid, self._failed = None, False, None, False
            done = self._end() or done
            if done is not None:
                self._owed = done
            self._cond.notify()
        if done is not None:
            _log.info("the arm's stretch with nothing to play ended after %.0f ms with no answer to play: a person "
                      "took the robot, or stopped it (%s)", (done.stale_s or 0.0) * 1000.0, done.reason)

    def resume_owed(self) -> None:
        """The arm has something to play again - a person's chunk, or its model's answer once it drives again: the
        stretch taken() ended is resumed now, once, on the act's own thread. Never resumed, a robot's code that held the
        arm in on_stale would keep it held for good."""
        with self._cond:
            done, self._owed = self._owed, None
        if done is not None:
            self.resume(done)

    def resume(self, done: Stale) -> None:
        """The stretch `done` ended with an answer: logged, and on_resume called, on the act's own thread."""
        _log.info("an answer came after the arm had nothing to play for %.0f ms (%s)", (done.stale_s or 0.0) * 1000.0,
                  done.reason)
        if self._on_resume is not None:
            self._on_resume(done)

    def _due(self) -> Optional[Stale]:
        """Under the lock: the stretch that begins now, the answer the robot plays having run out with none after it."""
        if self._closed or self._ends is None or self._now is not None:
            return None
        now = self._clock()
        if now < self._ends:
            return None
        reason = LATE if self._asked else FAILED if self._failed else NOT_ASKED
        at = self._wall() - timedelta(seconds=now - self._ends)
        self._now = Stale(reason, at, self._episode, self._rid if reason == LATE else None)
        self._since, self._ends = self._ends, None
        self._events += 1
        return self._now

    def _end(self) -> Optional[Stale]:
        """Under the lock: the stretch under way ended, its time counted; None when there was none."""
        if self._now is None:
            return None
        lasted = max(0.0, self._clock() - (self._since or self._clock()))
        self._stale_s += lasted
        done = self._last = replace(self._now, stale_s=round(lasted, 3))
        self._now = self._since = None
        return done

    def _say(self, began: Stale) -> None:
        """A stretch begins: logged, and on_stale called - or, with none set, the first said once a process."""
        _log.info("the answer this robot played ran out with %s: the arm has nothing valid to play", _WHY[began.reason])
        if self._on_stale is None:
            if not _SAID.is_set():
                _SAID.set()
                warn(f"the answer this robot played ran out with {_WHY[began.reason]}: the arm had nothing valid to "
                     f"play until the next came. connect(on_stale=..., on_resume=...) is called the moment that "
                     f"happens, to hold the arm, and as the next answer comes (said once a process; each is on the log "
                     f"of \"sequence_ai\" and in policy.stale)")
            return
        try:
            self._on_stale(began)
        except Exception:
            _log.exception("on_stale raised")

    def _start(self) -> None:
        """Under the lock: the watcher, started with the first deadline - a Policy that never asks ahead runs none."""
        if self._thread is None and self._threaded and not self._closed:
            self._thread = threading.Thread(target=self._watch, daemon=True, name="seq-stale")
            self._thread.start()

    def _watch(self) -> None:
        """The watcher: asleep until the answer the robot plays runs out (woken by every change), then that stretch
        said."""
        while True:
            with self._cond:
                if self._closed:
                    return
                due = self._due()
                if due is None:
                    ends = self._ends if self._now is None else None
                    self._cond.wait(None if ends is None else max(0.001, ends - self._clock()))
                    continue
            self._say(due)
