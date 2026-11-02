"""CollectWindow: when a drainer sends a run's queued telemetry. A writer stamps `send_after` on
each mergeable metric/step op; a drainer holds the run's lane until its head's stamp passes."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .... import routes
from ....routes import WriteOp

#: The writer's window, in seconds (0-60, 0 = send at once, as before 0.36x).
SEND_INTERVAL_ENV = "PROBE_SEND_INTERVAL_SEC"
DEFAULT_SEND_INTERVAL_SECONDS = 5.0
MAX_SEND_INTERVAL_SECONDS = 60.0
#: The op field: wall-clock epoch seconds until which a drainer may hold the op. Optional:
#: an op without it (an older writer's, or window 0) is sent at once, by every release.
SEND_AFTER = "send_after"
#: How often a drainer holding a window looks for a write that must go now.
LOOK_SECONDS = 0.25
#: How often it looks while only a run's backoff holds it: each look lists ops/, and a run
#: backing off may have a long queue (review of #3785, I7). Still well inside a backoff (2 s to 300 s).
BACKOFF_LOOK_SECONDS = 1.0

def send_interval() -> float:
    """`PROBE_SEND_INTERVAL_SEC`, clamped to 0-60 s; unset or malformed is the 5 s default."""
    raw = os.environ.get(SEND_INTERVAL_ENV)
    if raw is None or not raw.strip():
        return DEFAULT_SEND_INTERVAL_SECONDS
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_SEND_INTERVAL_SECONDS
    if value != value:  # nan
        return DEFAULT_SEND_INTERVAL_SECONDS
    return min(max(value, 0.0), MAX_SEND_INTERVAL_SECONDS)


def is_collectable(op: dict) -> bool:
    """Whether ``op`` may wait in a window: a plain metrics POST whose every point has a step
    or a wall clock (what `coalesce._merge_key` merges), or a step record POST, to a run named
    by its id. Uploads, PATCHes, creates and closes never wait."""
    if op.get("kind") != "http" or op.get("method") != "POST" or op.get("correlation"):
        return False
    route = routes.classify("POST", op.get("path"))
    if route.op not in (WriteOp.METRICS, WriteOp.STEPS) or not route.exact or not _is_uuid(route.run):
        return False
    body = op.get("body")
    if not isinstance(body, dict):
        return False
    if route.op is WriteOp.STEPS:
        step = body.get("step_index")
        return isinstance(step, int) and not isinstance(step, bool)
    points = body.get("points")
    if not isinstance(points, list) or not points:
        return False
    return all(
        isinstance(point, dict) and (point.get("step_index") is not None or point.get("wall_clock"))
        for point in points
    )


def stamp_send_after(op: dict, interval: float | None = None, *, cap: float | None = None) -> None:
    """Stamp ``op`` with the writer's window, at most ``cap`` seconds (an explicit drain
    interval, review of #3785, I18): nothing at window 0 or for an op that never waits, so those ops
    stay byte-identical to an older writer's."""
    interval = send_interval() if interval is None else interval
    if cap is not None:
        interval = min(interval, max(cap, 0.0))
    if interval > 0 and is_collectable(op):
        op[SEND_AFTER] = round(time.time() + interval, 3)


def _send_after(op: dict) -> float | None:
    value = op.get(SEND_AFTER)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


@dataclass
class LaneLoad:
    """What a held lane would send: metric points, step records and op-file bytes."""

    points: int = 0
    steps: int = 0
    size: int = 0

    def add(self, op: dict, size: int) -> None:
        body = op.get("body") if isinstance(op.get("body"), dict) else {}
        points = body.get("points")
        if isinstance(points, list):
            self.points += len(points)
        else:
            self.steps += 1
        self.size += size

    @property
    def full(self) -> bool:
        """One POST's worth is queued: waiting longer only splits it into more POSTs."""
        from .coalesce import MERGE_MAX_BYTES, MERGE_MAX_POINTS, STEPS_MAX

        return self.points >= MERGE_MAX_POINTS or self.steps >= STEPS_MAX or self.size >= MERGE_MAX_BYTES


@dataclass
class LaneHold:
    """A lane the window holds this pass: ``wait`` seconds until its head may go."""

    wait: float
    load: LaneLoad


class CollectWindow:
    """When a lane sends (plan T2). Only drainers use it (the detached worker, the in-process
    thread); `finish()`, `flush()` and `probe outbox drain` never wait for a window. A lane is
    held only while EVERY op in it is stamped, fresh (no attempt yet), under one POST's caps,
    and its head's `send_after` is ahead; anything else in the lane (an upload, a PATCH, a
    close, an older writer's op, a retry) sends it now. A close waiting for the drain lock
    (`.drain.want`) sends every lane now."""

    def __init__(self, *, clock: Callable[[], float] = time.time) -> None:
        self._clock = clock

    def hold(self, ops: list[tuple[Path, dict]], *, sizes: dict | None = None) -> LaneHold | None:
        """``ops``: a lane's queued ops, head first. ``sizes``: op name -> stat stamp
        (`_DrainHold.stamps`), for the byte cap."""
        if not ops:
            return None
        due = _send_after(ops[0][1])
        if due is None:
            return None
        wait = due - self._clock()
        if wait <= 0 or wait > MAX_SEND_INTERVAL_SECONDS:  # past, or a wall-clock step back
            return None
        load = LaneLoad()
        for path, op in ops:
            if _send_after(op) is None or _attempts(op) > 0:
                return None
            stamp = (sizes or {}).get(path.name)
            load.add(op, int(stamp[1]) if stamp else 0)
            if load.full:
                return None
        return LaneHold(wait, load)

    def is_due(self, op: Any, now: float | None = None) -> bool:
        """Whether a newly queued op must go now, whatever its run's window."""
        if not isinstance(op, dict) or _attempts(op) > 0:
            return True
        due = _send_after(op)
        if due is None:
            return True
        now = self._clock() if now is None else now
        return due <= now or due - now > MAX_SEND_INTERVAL_SECONDS

    def wait(
        self,
        journal,
        *,
        seconds: float,
        seen: set,
        skip: set,
        loads: dict,
        stop=None,
        woken=None,
        asked: Callable[[], bool] | None = None,
    ) -> None:
        """Sleep up to ``seconds``, ending early when a write that must go now is queued: an
        op of a run not in ``skip`` that is due (`is_due`), fills its run's POST (``loads``:
        lane -> `LaneLoad` the pass held) or opens a run whose window ends sooner. ``seen``:
        (queue, name) pairs already looked at. It looks every `LOOK_SECONDS` while a window
        holds, every `BACKOFF_LOOK_SECONDS` while only backoffs do, whoever wrote: another
        process's write sets no event here (review of #3785, I1). ``woken`` (an Event this process's
        writers set) brings the next look forward to `LOOK_SECONDS` after the last. ``stop``
        (an Event) ends it at once; so do ``asked()`` (a pause, a stop file, a sign-in) and a
        volume under the outbox's free-space floor while a window holds (review of #3785, C6)."""
        deadline = time.monotonic() + seconds
        held = set(loads)
        every = LOOK_SECONDS if loads else BACKOFF_LOOK_SECONDS
        looked_at = time.monotonic()
        while True:
            now = time.monotonic()
            if now >= deadline:
                return
            nap = min(deadline, looked_at + every) - now
            if woken is not None and nap > 0 and woken.wait(nap):
                woken.clear()  # a write here, or close() (which sets `stop` too)
                nap = min(deadline, looked_at + LOOK_SECONDS) - time.monotonic()
            elif woken is not None:
                nap = 0.0
            if _pause(stop, nap):
                return
            if (stop is not None and stop.is_set()) or (asked is not None and asked()):
                return
            if loads and is_short_of_disk(journal):
                return  # only a window holds writes back; a backoff wait stays a backoff
            sooner = self._look(journal, seen, skip, loads, held)
            looked_at = time.monotonic()  # after the look: a slow listing is not back to back
            if sooner is not None:
                if sooner <= 0:
                    return
                deadline = min(deadline, time.monotonic() + sooner)

    def _look(self, journal, seen: set, skip: set, loads: dict, held: set) -> float | None:
        """Read each op queued since the last look, once. 0 when one must go now, else the
        seconds until the soonest run not ``held`` by the pass comes due, or None."""
        now = self._clock()
        soonest: float | None = None
        for queue in journal.own_namespaces():
            try:
                names = os.listdir(queue.ops_dir)
            except OSError:
                continue
            for name in names:
                key = (str(queue.dir), name)
                if not name.endswith(".json") or key in seen:
                    continue
                seen.add(key)
                try:
                    raw = (queue.ops_dir / name).read_bytes()
                except FileNotFoundError:
                    continue  # delivered meanwhile (a `finish()` of its run)
                except OSError:
                    return 0.0
                try:
                    op = json.loads(raw)
                except ValueError:
                    return 0.0  # unreadable: a pass sorts it out
                lane = _lane_of(op)
                if lane in skip:
                    continue
                if self.is_due(op, now):
                    return 0.0
                load = loads.setdefault(lane, LaneLoad())
                load.add(op, len(raw))
                if load.full:
                    return 0.0
                if lane not in held:
                    due = (_send_after(op) or now) - now
                    soonest = due if soonest is None else min(soonest, due)
        return soonest


def is_short_of_disk(journal) -> bool:
    """Whether ``journal``'s volume is under its free-space floor right now. There a writer
    sends around the queue only while its run has nothing queued, so a window holding the run
    dropped its writes instead (review of #3785, C6): a drainer holds no window then. One statvfs."""
    try:
        return journal.is_below_floor_now()
    except Exception:  # noqa: BLE001 -- unmeasurable is not short: hold as usual
        return False


def _pause(stop, seconds: float) -> bool:
    """Sleep ``seconds`` (on ``stop`` when given); True when ``stop`` was set."""
    if seconds <= 0:
        return bool(stop is not None and stop.is_set())
    if stop is not None:
        return stop.wait(seconds)
    time.sleep(seconds)
    return False


from probe.sdk.delivery.ops.ops import _attempts, _is_uuid, _lane_of  # noqa: E402 -- pieces need each other; the front door loads this one first
