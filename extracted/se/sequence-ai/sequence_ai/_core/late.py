"""
Answers that came after their robot played the one before: counted into the robot's on-time share, and said once a
process with what would let it keep moving.

In one sentence: each act answered beside what was left of the answer its robot played as it asked for it - that
answer's action_chunk_valid_len steps at hz from when it was asked for, less the time since: the X-Seq-Chunk-Left-Ms
its act told the worker (worker_transport.post_act; a robot asks at its action_chunk_replan_at step or, having one act
on its way at a time, when the answer before came, whichever is later) → an answer slower than that is late, the arm
standing still for the difference → each stretch of such acts a run: its answers held to the one before, the late
ones and the time stood still, reported as one row (reporting.run_record: what `seq policy status`, `seq usage
--policy` and the console say as its on-time share) as its episode ends, its Policy closes, its robot stops asking in
time (its loop's own pace) or RUN_REPORT_S goes by → and the first late answer starts a count, said SAY_AFTER_S on, or
as its Policy closes before then, once a process: how many came late, and the step to ask at that leaves time for the
slowest - its time split into the worker's own and the rest, on the way - or, where an answer and the one before it
took longer together than an answer plays, that asking earlier does not help: a longer valid length or a shorter
round trip does.
Not held to anything: the first act on a new connection (it also opens it, and nothing was left to say), one that waited
for a starting worker, one sent after its robot had played the answer before, and a policy that declares no valid
length, no hz, or asks at its last valid step (its robot waits for every answer).

WHY: an answer that comes after the robot played its last valid step leaves the robot waiting, and on Wi-Fi a link
stalls now and then for a few hundred milliseconds - nothing said why the robot stopped, nor what would let it keep
moving, and the on-time share run() reported went with run(). Asking earlier makes room for an answer only while the
one before it came by the step asked at: past that a robot asks when the answer before comes, whatever step it names.



"""
from __future__ import annotations

import math
import threading
import time
import uuid
from typing import Any, Callable, Optional

from .capacity import wait_steps
from .warn import warn


SAY_AFTER_S = 60.0

RUN_REPORT_S = 300.0

_SAID = threading.Event()
_LOCK = threading.Lock()
_REST = "a longer action_chunk_valid_len or a shorter round trip does"


def _split(ms: float, worker_ms: Optional[float]) -> str:
    """An answer's time, and its worker's part of it where the worker said it (handler_ms)."""
    if worker_ms is None or not 0 <= worker_ms <= ms:
        return f"{ms:.0f} ms"
    return f"{ms:.0f} ms: {worker_ms:.0f} ms in the worker, {ms - worker_ms:.0f} ms on the way"


def words(late: int, acts: int, hz: float, valid_len: int, *, ask: Optional[int] = None,
          slowest: Optional[tuple] = None, helped: int = 0, worst: Optional[tuple] = None) -> str:
    """What is said: how many of the answers came late; then the step `ask` that leaves time for the `helped` of them
    a step makes room for, `slowest` the slowest of those (ms, its worker's ms) - and, for the rest, `worst` the pair
    that took longest together (the answer before's ms, the answer's ms, its worker's ms), that no step does."""
    whole = valid_len / hz * 1000.0
    lead = (f"{late} of {acts} answers came after this robot played the one before ({valid_len} valid steps, "
            f"{whole:.0f} ms at {hz:g} Hz from when it asked)")
    said = ""
    if ask is not None and slowest is not None:
        for_ = "the slowest" if helped == late else f"{helped} of them, the slowest"
        said = (f"; asking for the next one at step {ask} or earlier (action_chunk_replan_at={ask} on @seq.policy) "
                f"leaves {(valid_len - ask) / hz * 1000.0:.0f} ms, enough for {for_} ({_split(*slowest)})")
    if helped == late or worst is None:
        return lead + said
    before, ms, worker_ms = worst
    if not said:
        return (f"{lead}: a robot has one act on its way at a time, so an answer and the one before it have to come "
                f"within those {whole:.0f} ms together - the slowest two took {before + ms:.0f} ms ({before:.0f} ms, "
                f"then {_split(ms, worker_ms)}): asking earlier does not help; {_REST}")
    return (f"{lead}{said}; the other {late - helped} came with the answer before them past those {whole:.0f} ms "
            f"together, the slowest two {before + ms:.0f} ms, and as a robot has one act on its way at a time no step "
            f"makes room for them: {_REST}")


class LateAnswers:
    """One Policy's answers, each held to what was left of the one before as it asked (see the module); `on_run` takes
    each run's row as it ends."""

    def __init__(self, clock: Callable[[], float] = time.monotonic,
                 on_run: Optional[Callable[[dict], None]] = None) -> None:
        self._clock = clock
        self._on_run = on_run
        self._lock = threading.Lock()
        self.acts = 0
        self.late = 0
        self.helped = 0
        self._ask: Optional[int] = None
        self._slowest: Optional[tuple] = None
        self._worst: Optional[tuple] = None
        self._before_ms: Optional[float] = None
        self._first_late: Optional[float] = None
        self._plays: Optional[tuple] = None
        self._run: Optional[dict] = None

    def answered(self, total_ms: Optional[float], plays: Any, *, counted: bool = True,
                 worker_ms: Optional[float] = None, left_ms: Optional[float] = None) -> None:
        """An act answered just now in `total_ms`, its worker's own part `worker_ms` where it said it (handler_ms), its
        policy playing as `plays` says (hz, action_chunk_valid_len, action_chunk_replan_at, as connect answered them);
        `left_ms` what was left of the answer its robot played as it asked (None: nothing said, a connection's first);
        `counted` False for one that waited for a starting worker or opened its connection - its time is no answer's.
        Said when SAY_AFTER_S went by since the first late answer."""
        if total_ms is None:
            return
        now = self._clock()
        before_ms, self._before_ms = self._before_ms, float(total_ms)
        plays = plays if isinstance(plays, dict) else {}
        hz, valid_len = plays.get("hz"), plays.get("action_chunk_valid_len")
        held = (counted and before_ms is not None and isinstance(left_ms, (int, float)) and left_ms > 0
                and bool(wait_steps(valid_len, plays.get("action_chunk_replan_at")))
                and isinstance(hz, (int, float)) and not isinstance(hz, bool) and hz > 0)
        rows = []
        with self._lock:
            if not held:
                rows.append(self._end_run("paused"))
            else:
                run = self._run
                if run is None:
                    run = self._run = {"began": now - total_ms / 1000.0, "chunks": 0, "underruns": 0,
                                       "underrun_s": 0.0, "chunk_s": round(valid_len / hz, 4)}
                self.acts += 1
                run["chunks"] += 1
                run["last"] = now
                if total_ms > left_ms:
                    run["underruns"] += 1
                    run["underrun_s"] += (total_ms - left_ms) / 1000.0
                    worker = (float(worker_ms) if isinstance(worker_ms, (int, float))
                              and not isinstance(worker_ms, bool) else None)
                    self._count(float(total_ms), worker, before_ms, float(hz), valid_len)
                if now - run["began"] >= RUN_REPORT_S:
                    rows.append(self._end_run("segment"))
            due = self._first_late is not None and self._clock() - self._first_late >= SAY_AFTER_S
        for row in rows:
            self._report(row)
        if due:
            self._say()

    def _count(self, ms: float, worker_ms: Optional[float], before_ms: float, hz: float, valid_len: int) -> None:
        """A late answer of `ms`, after one of `before_ms` (under the lock): asked for at step k it comes in time when
        max(k/hz, before) + ms <= valid_len/hz - room a step makes only while the two together fit."""
        self.late += 1
        self._plays = (hz, valid_len)
        if self._first_late is None:
            self._first_late = self._clock()
        ask = valid_len - math.ceil(ms / 1000.0 * hz - 1e-9)
        if before_ms + ms <= valid_len / hz * 1000.0 and ask >= 1:
            self.helped += 1
            self._ask = ask if self._ask is None else min(self._ask, ask)
            if self._slowest is None or ms > self._slowest[0]:
                self._slowest = (ms, worker_ms)
        elif self._worst is None or before_ms + ms > self._worst[0] + self._worst[1]:
            self._worst = (before_ms, ms, worker_ms)

    def _end_run(self, reason: str) -> Optional[dict]:
        """The run under way ended for `reason` (under the lock): its row, or None where no answer of it was held to the
        one before."""
        run, self._run = self._run, None
        if run is None or not run["chunks"]:
            return None
        return {"run_id": uuid.uuid4().hex, "chunks": run["chunks"], "underruns": run["underruns"],
                "underrun_s": round(run["underrun_s"], 3), "elapsed_s": round(run["last"] - run["began"], 3),
                "reason": reason, "chunk_s": run["chunk_s"]}

    def _report(self, row: Optional[dict]) -> None:
        if row is not None and self._on_run is not None:
            try:
                self._on_run(row)
            except Exception:
                pass

    def end_run(self, reason: str) -> None:
        """Its episode ended (or another reason the robot stops): the run under way is reported now."""
        with self._lock:
            row = self._end_run(reason)
        self._report(row)

    def close(self, reason: str = "closed") -> None:
        """Its Policy closes - or its process ends with it open (`reason`, act/policy._end_reports: "exit", or the signal
        that ends it) -: the run under way is reported, and a count not said yet is said now."""
        self.end_run(reason)
        if self._first_late is not None:
            self._say()

    def _say(self) -> None:
        with _LOCK:
            if _SAID.is_set():
                return
            _SAID.set()
        with self._lock:
            hz, valid_len = self._plays
            said = words(self.late, self.acts, hz, valid_len, ask=self._ask, slowest=self._slowest,
                         helped=self.helped, worst=self._worst)
        warn(said)
