# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
Scheduling by the slack an action chunk leaves, for one replica of a model: how many robots the replica can serve, how
long a robot's request may wait for a batch, and which requests are dispatched first.

    from sequence_ai.engine import slack

    table = slack.measure(forward_of, sizes=[1, 2, 4])               # forward_of(n): one forward pass of n requests
    play = slack.playback(hz=20, valid_len=15, replan_at=8)          # 15 valid steps, the next requested at the 8th
    seating = slack.Seating(table, play["buffer_s"] * 1000, sizes=[1, 2, 4],
                            cycle_ms=(play["play_s"] - play["buffer_s"]) * 1000)
    seats, over = seating.seat([("near", 30.0), ("far", 200.0)])     # (robot, its RTT in ms)

    aligner = slack.Aligner(table, play, seated=lambda: ["near", "far"])
    aligner.arrived("near", now, outside_ms=30.0)                    # each request as it arrives
    wait_s = aligner.hold_s(["near"], now)                           # how long the open batch may wait; 0.0: run it
    first = aligner.split(["near", "far"], now, [1, 2, 4], free=False)    # which go first, apart; None: as one batch
    aligner.answered(["near"], now)                                  # as a batch's responses leave

With batches of 1, 2 and 4 that take 80, 110 and 130 ms, `seats, over` is `4, ["far"]`: the replica has capacity for
four robots, and the one 200 ms away is the one to move: its request may arrive as the near robot's batch runs, and
would then miss its deadline. A batch of four answers a robot 100 ms away within the buffer, and four such robots, run
on a clock with these batch times, had every response in time.

Terms. A *request* is one robot's request for its next response, which carries an action chunk. A *replica* is one
loaded model, which runs one batch at a time (replicas.py runs each as a process). A robot's *RTT* is the time its
requests spend outside the server: uplink, downlink, and the client's own encoding and decoding. The *buffer* is the
playback time left in the chunk a robot is executing when it sends its next request. A request's *slack* is what is left
of the buffer after what the request spends before its response arrives: its robot's RTT, its wait for a batch, its
batch's time and a margin.

In one sentence: a policy responds with a chunk of which N steps are valid, and its robot requests the next at step k,
so (N - k) / hz of playback is left when it sends the request → a request may take that long to come back, less its
robot's own RTT and a margin, so a batch must run within what the tightest of its robots has left → Seating computes how
many robots a replica can serve under that constraint, by running them on a clock as a server serves them (on_a_clock),
and which it cannot (the furthest ones) → Aligner computes, as requests arrive, how long the open batch may wait for the
replica's other robots and which requests must be dispatched first.

WHY from the chunk: the deadline is the policy's own. Nothing is declared for each request and nothing is read from a
response: two numbers of the policy and the rate it runs at determine how long every one of its robots can wait.
WHY each robot by its own RTT: a robot further away has less of its buffer left for the server. When every robot was
evaluated by the furthest robot's RTT, one far robot lowered the batch size, and with it the capacity, of every near
robot on the same replica. Here a far robot is batched by its own fit, costs only its own batches' load, is the first a
replica cannot serve, and is dispatched ahead of a batch that would make it late, so it does not hold back the others.
WHY only the sizes listed: a model is traced, compiled or graphed for the shapes it has seen (batcher.py).

Relation to batcher.py: Batcher dispatches a batch when it is full, or `wait_ms` after its first call, and has no notion
of a robot. This file answers the two questions that leaves open: how many robots a replica can serve at all, and, for
the requests waiting now, how long they may wait and which are dispatched first. It runs no model and sets no timer of
its own (measure aside): the server that owns the batches calls it, and passes it the current time.

Measured with this file, once: π0.5 on one L4, in a test server built from it around the model's batched call (15 valid
steps, the next requested at the 8th, simulated robots, 60 s per cell). At 15 Hz (a 467 ms buffer; batches of 1, 2 and 3
in 195, 312 and 429 ms) per_replica computed a capacity of 2: 2 robots had no late response, 3 had 21% and 26%, and 4
had 99%. At 20 Hz (350 ms) it computed 1, and 2 robots had 40% and 90% late. That server admitted every robot: it did
not call Seating.seat(). Batching added no capacity on that model and GPU: openpi's own server, one request at a time,
served the same 2 robots.

Measured with this file on three models, each on one L4 with simulated robots of a 15 Hz policy 20 ms away, 60 s per
cell, when per_replica computed the load by a formula: for π0.5 and GR00T N1.6 it computed 2, and 2 robots had no late
response (0.4% in one cell of eight). For SmolVLA (batches of 1, 2, 4 and 8 in 256, 273, 303 and 377 ms) it computed 8,
and 4 robots had 95% and 97% of their responses late, 8 had 99%: the four ran as two fixed pairs, each request behind
the other pair's batch, 553 ms against the 467 ms buffer. The formula assumed that robots whose batches of one size do
not fit in a cycle share larger batches; robots send on their own clocks, and nothing here brings their requests
together. The capacity is computed on a clock since (on_a_clock): from those three timing tables it is 2, 2 and 1, and
of four SmolVLA robots' responses under 1% are in time. For robots 100 ms away it is 1 for all three (the formula: 1,
2 and 4): of two GR00T N1.6 robots' responses 8% are late over the starts, those to a request that arrives 37 to 81 ms
after the other robot's and runs behind its batch. examples/fleet_on_a_clock.py prints what the clock runs for a
model's batch times.

Measured with this file, with the capacity computed on a clock: SmolVLA on one L4, the same policy and test server,
simulated robots about 30 ms away. The clock gave a capacity of 1, by the load. Two robots, one more than that, had no
late response in 226 (their requests 150 ms apart, 60 s) and none in 1,125 (270 ms apart, 300 s, a load of 0.94);
three had 5% and 29% of their responses late in two starts; and where the server asked Seating.seat() as each robot
connected, it admitted one and refused the next two.

Measured in the serving stack this was taken from, not with this file (the numbers the docstrings below give for what
happened in service are from that stack too):
- Four robots on one replica for two minutes: 20 Hz, 15 valid steps, the next requested at the 8th (a 350 ms buffer), a
  stand-in model on a CPU. With every robot assumed to have a fixed 100 ms RTT and a batch timed by its forward pass
  alone, 459 of 1,114 responses arrived after their robot had run out of steps: a request waited a median 58 ms for a
  batch, took 197 ms more in the server and about 131 ms outside it, 386 ms against 350. Each robot's own RTT
  (Aligner.arrived) and a batch's time as served (Served) were added because of that. The late share after them, at the
  same settings, was not recorded cleanly.
- Four robots, 300 s and about 2,100 requests per run: a stand-in on a CPU paced like a 15 Hz policy (15 valid steps,
  the next requested at the 8th: a 467 ms buffer, 533 ms between a robot's requests; batches of 1, 2 and 4 in 234, 254
  and 299 ms). All four on one replica (two batches of two in each 533 ms, a load of 0.95) had 85.7% of their responses
  back within the 467 ms; two per replica on two replicas (two batches of one, a load of 0.88) had 94.1%, on the slower
  network of the two runs. LOAD_MAX is set from those two runs.
- A simulation of one replica (15 Hz, a 467 ms buffer, a batch of one 234 ms, 120 s per run): a robot 60 ms away, beside
  one 300 ms away, was answered in time 80% and 83% of the time in two runs, and 88% and 92% once the far robot's
  request was dispatched separately (Aligner.split). In a third run the replica was too loaded for the two and neither
  was answered in time, either way: that case is for the capacity limit to prevent.

Where it does nothing: a policy whose robot sends its request at its last valid step (k = N) leaves no slack, so no
request is held and a replica serves one robot, unless `max_wait_s` allows the robot to wait; a policy with no rate or
no chunk length is not scheduled at all; a robot that does not report its own RTT is assumed to have ROUND_TRIP_MS.

Standard library only. Taken from the scheduling General Sequences serves with: its rules and its code, less what read
that server's own settings and health report.
"""
from __future__ import annotations

import heapq
import itertools
import math
import re
import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Sequence, TypedDict

# The margin kept between a batch's response and its robot's deadline: room for the downlink and one control step.
MARGIN_MS = 50.0
# Runs kept for each batch size: the timed runs at first, then the latest ones the server ran.
WINDOW = 64
# Timed runs of each batch size (measure), after one untimed run of that size, which compiles it if nothing has.
# One policy's first run of batch 2, 4 and 8 took 31 to 38 s where its later runs took 0.3 to 0.8 s.
RUNS = 3
# The most robots one replica serves, however fast its forward pass: past some number the server's own handling of the
# requests (parsing, checking, the hop to the replica), not the GPU, is what they wait for, and that is not timed here.
MAX_ROBOTS_PER_REPLICA = 64
# The largest share of a replica's cycle (the time between one robot's requests, k / hz) that its robots' batches may
# fill before a new one would queue behind the others instead of running between them: periodic robots offset
# themselves and barely wait while their batches fit in a cycle, and queue up past it (the module's docstring has the
# measurement; on_a_clock has how the share is counted).
LOAD_MAX = 0.9
# The RTT (uplink and downlink of a request and its response) assumed for a robot that has not reported its own.
ROUND_TRIP_MS = 100.0
# A robot's reported RTT (the time its requests spend outside the server) is read only as a whole number of ms up to
# this; anything else counts as not reported, and the robot is assumed to have ROUND_TRIP_MS.
OUTSIDE_MAX_MS = 5000
# A batch size is timed by what its batches took once this many of its requests were answered (Served.post_ms);
# before that, by its forward pass plus the server's own handling of a batch measured so far, or by its forward pass
# alone while no handling has been measured.
SERVED_MIN = 8
# The playback time a robot reports as left in the chunk it is executing when it sends a request is read only as a
# whole number of ms up to this. One request is in flight per robot, so a response that arrived late moves its next
# request past k / hz, and less is left than (N - k) / hz: a robot that reports what is left is scheduled by that.
LEFT_MAX_MS = 600_000
# The longest `max_wait_s` a policy may set (playback), in seconds.
WAIT_MAX_S = 60.0
# A replica's robots run on a clock (on_a_clock): the cycles each start is run for, of which the first CLOCK_WARM are
# not counted (a robot's first request has no chunk executing and is never held, so until every robot has a response
# the batches are not those of a running fleet), and the most starts a number of robots is run from (starts).
CLOCK_CYCLES = 48
CLOCK_WARM = 8
CLOCK_STARTS = 128
# The share of a fleet's responses that must be back before their robot's buffer runs out, over the starts it is run
# from, for the fleet to be in time (in_time).
IN_TIME_MIN = 0.95
# The clock's resolution: each batch time is rounded up to this many significant bits (by 3% at most, and at least to
# a whole ms), and each RTT up to a multiple of CLOCK_RTT_MS. A server's batch times and its robots' reported RTTs
# move by a few ms from one request to the next; rounded, they ask a question that was already answered (in_time).
CLOCK_BITS = 6
CLOCK_RTT_MS = 10.0
# A robot not heard from for this many of its periods is treated as gone, whether or not it disconnected: no batch
# waits for it.
GONE_PERIODS = 4
# The weight of a new gap between a robot's requests in its smoothed period.
PERIOD_WEIGHT = 0.2

_WHOLE_MS = re.compile(r"[0-9]{1,7}")


# ── what a robot reports about itself ────────────────────────────────────────────────────────────────────────────────

def outside_ms(value: Any) -> float | None:
    """A robot's reported RTT (the time its requests spend outside the server), given as a header's text or a number in
    a message, parsed as a whole number of ms from 0 to OUTSIDE_MAX_MS; else None, as if nothing was reported."""
    return _whole_ms(value, OUTSIDE_MAX_MS)


def left_ms(value: Any) -> float | None:
    """The playback time a robot reports as left in the chunk it is executing when it sends a request, parsed as
    outside_ms is: 0 to LEFT_MAX_MS."""
    return _whole_ms(value, LEFT_MAX_MS)


def _whole_ms(value: Any, most: int) -> float | None:
    """A whole number of ms from 0 to `most`, else None. ASCII digits only: int() would also accept other scripts'
    digits."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        ms = value
    elif isinstance(value, str) and _WHOLE_MS.fullmatch(value.strip()):
        ms = int(value.strip())
    else:
        return None
    return float(ms) if 0 <= ms <= most else None


# ── how long a batch takes ───────────────────────────────────────────────────────────────────────────────────────────

def quantile(values: Iterable[float], q: float) -> float:
    """The nearest-rank quantile: the p95 of three runs is the slowest of them."""
    s = sorted(values)
    return s[min(len(s) - 1, max(0, math.ceil(q * len(s)) - 1))]


class Table:
    """Forward-pass time by batch size, in ms: the timed runs (measure), then each forward pass the server runs, keeping
    the latest WINDOW of each size."""

    def __init__(self) -> None:
        self._ms: dict[int, deque] = {}
        # each size's first run, not counted above (measure): its compile time where nothing had compiled that size
        self.first_ms: dict[int, float] = {}

    def add(self, size: int, ms: float) -> None:
        """Record that a forward pass of `size` requests took `ms`."""
        self._ms.setdefault(int(size), deque(maxlen=WINDOW)).append(float(ms))

    def sizes(self) -> list[int]:
        """The batch sizes timed, smallest first."""
        return sorted(self._ms)

    def _runs(self, size: int) -> deque | None:
        """The runs of `size`, else of the smallest timed size above it (a policy pads a batch up to a size it was
        built for); None when nothing at or above it was timed."""
        for s in self.sizes():
            if s >= size:
                return self._ms[s]
        return None

    def p50(self, size: int) -> float | None:
        """The median forward-pass time of `size`, or of the smallest timed size above it; None past the largest timed
        size."""
        runs = self._runs(size)
        return quantile(runs, 0.5) if runs else None

    def p95(self, size: int) -> float | None:
        """The p95 forward-pass time of `size`, or of the smallest timed size above it; past the largest one, its time
        per request times `size`, which is an over-estimate, since a batch costs less than its requests run one by one.
        None when nothing is timed."""
        runs = self._runs(size)
        if runs:
            return quantile(runs, 0.95)
        if not self._ms:
            return None
        top = self.sizes()[-1]
        return quantile(self._ms[top], 0.95) * size / top

    def as_dict(self) -> dict[str, dict]:
        """Each timed size's p50, p95 and number of runs, keyed by its size as text: what a server may report about
        itself."""
        return {str(s): {"p50": round(quantile(r, 0.5), 1), "p95": round(quantile(r, 0.95), 1), "n": len(r)}
                for s, r in sorted(self._ms.items())}

    def take(self, other: "Table") -> None:
        """Adopt `other`'s runs and first runs, each in one assignment: whoever holds this Table (a server and each of
        its replicas' aligners) sees a timing made later, and a reader on another thread iterates the dict it already
        had."""
        self._ms, self.first_ms = dict(other._ms), dict(other.first_ms)

    def drop(self, size: int) -> None:
        """Forget the runs of `size`: a size whose timing failed partway, which no batch is dispatched in (measure)."""
        self._ms.pop(int(size), None)
        self.first_ms.pop(int(size), None)


class Served:
    """The time a batch takes in its server once dispatched (passing its inputs, the hop to its replica, the forward
    pass, building the response), by batch size, recorded as each of its requests was answered (the latest WINDOW of a
    size); and how much of that was not the forward pass (the server's own handling), which is used to time a size
    served too few times so far.

    WHY in addition to the Table: a forward pass timed alone leaves out what the server adds around it. In the
    measurement in the module's docstring a batch took 197 ms in the server, where the capacity had counted its forward
    pass alone."""

    def __init__(self) -> None:
        self._ms: dict[int, deque] = {}
        self._handling: deque = deque(maxlen=WINDOW)

    def add(self, size: int, post_ms: float, forward_ms: float | None = None) -> None:
        """Record that a request of a batch of `size` was answered `post_ms` after its batch was dispatched, of which
        the forward pass took `forward_ms`."""
        self._ms.setdefault(int(size), deque(maxlen=WINDOW)).append(float(post_ms))
        if forward_ms is not None and post_ms >= forward_ms:
            self._handling.append(float(post_ms) - float(forward_ms))

    def post_ms(self, size: int, table: Table) -> float | None:
        """The time of a batch of `size` once dispatched, in ms: the p90 of the smallest size at or above it that was
        served SERVED_MIN times (a batch of an unlisted size is timed as the listed ones, as the Table reads it); else
        its forward pass as `table` times it plus the server's own handling, the p90 of what it added to each forward
        pass served, or nothing while none was served. A server that has served nothing yet computes capacity from its
        forward passes and not from a guessed handling time: a guessed 50 ms once gave a capacity of two robots per
        replica where the same batches, timed, gave four. None when neither was timed."""
        for s in sorted(self._ms):
            if s >= size and len(self._ms[s]) >= SERVED_MIN:
                return quantile(self._ms[s], 0.9)
        forward = table.p95(size)
        if forward is None:
            return None
        return forward + (quantile(self._handling, 0.9) if self._handling else 0.0)

    def typical_ms(self, size: int, table: Table) -> float | None:
        """The p50 time of a batch of `size` once dispatched, in ms: how much of a cycle it fills, which the load is
        counted by (not its post_ms p90, which the waiting rule and a run on a clock use). The median of the smallest
        size at or above it that was served SERVED_MIN times, else its forward pass's median from `table` plus the
        server's own handling, or nothing while none was served. None when neither was timed."""
        for s in sorted(self._ms):
            if s >= size and len(self._ms[s]) >= SERVED_MIN:
                return quantile(self._ms[s], 0.5)
        forward = table.p50(size)
        if forward is None:
            return None
        return forward + (quantile(self._handling, 0.5) if self._handling else 0.0)


class SizeFailed(Exception):
    """A batch size whose forward pass raised while it was timed (measure): `size`, what it raised (`error`, also its
    __cause__), and the sizes timed below it (`table`), so a server can report which size its GPU could not run and what
    the smaller ones took."""

    def __init__(self, size: int, table: Table, error: BaseException) -> None:
        super().__init__(f"batch size {size}: {type(error).__name__}: {error}")
        self.size, self.table, self.error = size, table, error


def measure(run: Callable[[int], Any], *, sizes: Iterable[int], runs: int = RUNS,
            clock: Callable[[], float] = time.perf_counter, table: Table | None = None) -> Table:
    """Time `run(size)` (one forward pass of `size` requests, including returning its output) at each of `sizes`, in
    order, `runs` times each after one untimed run (which compiles that size if nothing has; its time is kept separately
    in table.first_ms), into `table` (a new one by default), which it returns. A size whose forward pass raises ends the
    timing with SizeFailed, carrying that size and the sizes timed below it; the runs of the size that failed are not
    kept."""
    table = table if table is not None else Table()
    for size in sizes:
        try:
            t = clock()
            run(size)
            table.first_ms[size] = (clock() - t) * 1000.0
            for _ in range(runs):
                t = clock()
                run(size)
                table.add(size, (clock() - t) * 1000.0)
        except Exception as exc:  # noqa: BLE001 (the caller decides; it gets the size and the sizes timed before it)
            table.drop(size)
            raise SizeFailed(size, table, exc) from exc
    return table


# ── how a policy's chunks are executed ───────────────────────────────────────────────────────────────────────────────

class _Played(TypedDict):
    play_s: float
    buffer_s: float
    step_s: float


class Playback(_Played, total=False):
    """How one response of a policy is executed by its robots (playback): `play_s`, its N valid steps at its rate, which
    a robot executes from when the response left; `buffer_s`, the playback time left when its robot requests the next,
    (N - k) / hz; `step_s`, one control step; and `wait_s` where the policy sets how long its robot waits."""

    wait_s: float


def playback(hz: float | None, valid_len: int | None = None, replan_at: int | None = None,
             max_wait_s: float | None = None) -> Playback | None:
    """How one response of a policy is executed by its robots, which is what a replica's robots are scheduled by: the
    policy runs at `hz`, `valid_len` steps of a response are valid (N), and its robot requests the next at step
    `replan_at`, counted from when its request is sent (k). `replan_at` not given: its robot sends a request once a
    response is fully executed, so there is no buffer; `valid_len` not given: its `replan_at` steps are all it is known
    to execute. None when it has no rate (0 < hz <= 1000) or neither number: its robots are not batched with others, one
    per replica. Nothing is read from a response.

    `max_wait_s` (0 < W <= WAIT_MAX_S): how long a robot may wait for a response, from when its request is sent, so that
    its request can share a batch. When set, a replica's capacity and the holding of its robots' requests use it in
    place of the playback time left when they send their requests (their actions may run out, and they wait); when not
    set, there is no `wait_s`."""
    if not _positive(hz, 1000.0):
        return None
    valid = valid_len if _whole(valid_len) else (replan_at if _whole(replan_at) else None)
    if valid is None:
        return None
    replan = min(replan_at, valid) if _whole(replan_at) else valid
    rate = float(hz)
    play: Playback = {"play_s": valid / rate, "buffer_s": (valid - replan) / rate, "step_s": 1.0 / rate}
    if _positive(max_wait_s, WAIT_MAX_S):
        play["wait_s"] = float(max_wait_s)
    return play


def _positive(value: Any, most: float) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and 0.0 < float(value) <= most


def _whole(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


# ── how many robots a replica can serve ──────────────────────────────────────────────────────────────────────────────

def per_replica(table: Table, buffer_ms: float, *, sizes: list[int], served: Served | None = None,
                outside_ms: float | None = None, cycle_ms: float | None = None, wait_ms: float | None = None,
                step_ms: float | None = None) -> int:
    """The capacity of one replica, in robots, for robots that all have the same RTT and whose buffer is `buffer_ms`
    ((N - k) / hz: the playback time left when a robot requests the next response, playback's buffer_s).

    First the capacity by latency: the largest of the policy's listed batch sizes whose batch answers in time with its
    robots' RTT and MARGIN_MS to spare: its time in the server once dispatched (`served`'s post_ms; the forward pass's
    p95 alone without one) + the RTT (`outside_ms`: the largest RTT its robots report; ROUND_TRIP_MS when none reports
    one) + MARGIN_MS <= buffer_ms. Then, given `cycle_ms` (the time between one robot's requests, k / hz: play_s less
    buffer_s), the capacity on a clock: 2, 3 and more robots are run as a server serves them (in_time), and the first
    number of whose responses fewer than IN_TIME_MIN are back in time over the starts they are run from, or whose
    batches fill more than LOAD_MAX of a cycle in one of them (on_a_clock's load), ends the count. `step_ms`: one
    control step (1000 / hz), which the clock's Aligner uses as a server's does; without it no batch waits a step for
    a nearer robot's request. The clock only lowers the count, never raises it above the capacity by latency. The
    first call for a table runs the clock (about 5 ms of one core for a capacity of 2, 35 ms for 4, 0.2 s for 8 and
    1 s for 16); in_time keeps each verdict, and a later call reads it.

    At least 1: a replica too slow even for one robot still serves one, as does one whose robots leave no slack (k = N).
    A size that was not timed is not used.

    WHY on a clock: whether robots share a batch depends on how their requests fall, which a formula for the load
    assumed (on_a_clock has the measurement). WHY a number that fails ends the count: robots are admitted one at a time,
    so a replica reaches a number of robots through every smaller one. A count that returned the largest number passing
    its load rule passed 3 to 8 robots where 2 failed, and a server that asked as each robot arrived stopped at 1.

    `wait_ms` (playback's wait_s, in ms): when set, the latency rule uses it in place of buffer_ms, and the load is by
    formula, not on a clock: the largest number of robots whose batches fill no more than LOAD_MAX of each batch size's
    own time between a robot's requests (wait_fill)."""
    best = 1
    timed = [b for b in sorted(sizes) if b in set(table.sizes())]
    trip = ROUND_TRIP_MS if outside_ms is None else outside_ms
    limit_ms = buffer_ms if wait_ms is None else wait_ms
    for b in timed:
        took = served.post_ms(b, table) if served is not None else table.p95(b)
        if took is not None and took + trip + MARGIN_MS <= limit_ms:
            best = max(best, b)
    best = min(best, MAX_ROBOTS_PER_REPLICA)
    if cycle_ms is None or cycle_ms <= 0.0 or not timed:
        return best
    capped = 1
    if wait_ms is not None:
        for n in range(1, best + 1):
            share = wait_fill(n, table, timed=timed, cycle_ms=cycle_ms, slack_ms=buffer_ms, trip_ms=trip, served=served)
            if share is not None and share[1] <= LOAD_MAX:
                capped = n
        return capped
    play = _played(buffer_ms, cycle_ms, step_ms)
    for n in range(2, best + 1):
        if not in_time(table, play, [trip] * n, sizes=timed, served=served):
            break
        capped = n
    return capped


def _played(buffer_ms: float, cycle_ms: float, step_ms: float | None) -> Playback:
    """The playback of a policy whose robots have `buffer_ms` left when they send a request every `cycle_ms`, for a run
    on a clock."""
    return {"play_s": (buffer_ms + cycle_ms) / 1000.0, "buffer_s": buffer_ms / 1000.0,
            "step_s": (step_ms or 0.0) / 1000.0}


def wait_fill(n: int, table: Table, *, timed: list[int], cycle_ms: float, slack_ms: float, trip_ms: float,
              served: Served | None = None, up_to: int | None = None) -> tuple[int, float] | None:
    """For a policy that sets `max_wait_s`: the batch size B that n robots run in (the smallest of the `timed` listed
    sizes, up to `up_to`, whose ceil(n / B) batches fit in its own time between requests), and the share of that time
    their batches fill. Each size has its own time between requests, because its robots wait for their responses: the
    replan step `cycle_ms` (k / hz) after the longer of the playback time left when the robot sends its request
    (`slack_ms`, (N - k) / hz) and its earliest response, B's typical time plus the robot's RTT (`trip_ms`). None when
    even the largest size does not fit in its own time between requests."""
    for b in timed:
        if up_to is not None and b > up_to:
            break
        took = served.typical_ms(b, table) if served is not None else table.p50(b)
        if took is None:
            continue
        between = cycle_ms + max(slack_ms, took + trip_ms)
        if math.ceil(n / b) * took <= between:
            return b, math.ceil(n / b) * took / between
    return None


class Seating:
    """The capacity of one replica when each robot is evaluated by its own RTT: per_replica's rules (the latency a
    batch answers in, then the robots run on a clock) for robots that are not all at the same distance.

    In one sentence: each robot's own fit (the largest listed size whose batch, as `served` timed it, answers within
    `buffer_ms` with that robot's own RTT and MARGIN_MS to spare) → robots with the same fit are batched together in
    sizes up to it, and each fit's batches run alongside the others' → the robots on the replica are admitted nearest
    first, as many as fit together (answered in time on a clock, each by its own RTT, at a load of no more than
    LOAD_MAX; no more than `most` robots; and each fit's batch still in time behind the longest batch of another fit,
    since the replica runs one batch at a time), and the rest are over capacity → remaining capacity: how many more
    robots at ROUND_TRIP_MS the replica can serve beside them (seat).

    WHY: a robot further away fits only smaller batches. When capacity was computed from the furthest robot's RTT, one
    far robot lowered the batch size, and with it the capacity, of every near robot on the same replica: a replica with
    capacity for four reported one, and the three robots on it were not answered in time. Here a far robot is batched by
    its own fit and costs only its own batches' load; with robots admitted nearest first, it is the first a replica
    cannot serve, so it is the one to move. For robots that all have the same RTT the capacity equals per_replica's. An
    empty replica admits one robot whatever its RTT, as per_replica's minimum is one; a robot that is late even alone,
    where a robot at ROUND_TRIP_MS is not, is admitted only in that case."""

    def __init__(self, table: Table, buffer_ms: float, *, sizes: list[int], served: Served | None = None,
                 cycle_ms: float | None = None, most: int = MAX_ROBOTS_PER_REPLICA,
                 wait_ms: float | None = None, step_ms: float | None = None) -> None:
        self._table, self._buffer_ms, self._served, self._cycle_ms = table, buffer_ms, served, cycle_ms
        # one control step, 1000 / hz: what the clock's Aligner caps a far batch's wait for a nearer request at
        self._step_ms = step_ms
        # playback's wait_s, in ms: the limit for each response in place of the buffer; the load rule then uses each
        # fit's own time between requests (wait_fill)
        self._wait_ms = wait_ms
        self._limit_ms = buffer_ms if wait_ms is None else wait_ms
        self._timed = [b for b in sorted(sizes) if b in set(table.sizes())]
        self._most = max(1, min(int(most), MAX_ROBOTS_PER_REPLICA))
        # a replica too slow for a robot at ROUND_TRIP_MS serves one robot at a time, per per_replica's minimum of one
        self._slow = self.fit(None) == 0

    def fit(self, outside_ms: float | None) -> int:
        """The largest listed size in which a robot whose RTT is `outside_ms` (None: ROUND_TRIP_MS) is answered in time:
        its batch's time in the server (`served`'s post_ms; the forward pass's p95 without it) + its RTT + MARGIN_MS <=
        buffer_ms (or the wait, where one is set), the rule Aligner batches it by; 0 when not even the smallest timed
        size is in time."""
        trip = ROUND_TRIP_MS if outside_ms is None else outside_ms
        best = 0
        for b in self._timed:
            took = self._served.post_ms(b, self._table) if self._served is not None else self._table.p95(b)
            if took is not None and took + trip + MARGIN_MS <= self._limit_ms:
                best = max(best, b)
        return min(best, MAX_ROBOTS_PER_REPLICA)

    def _took(self, n: int) -> float | None:
        """The time a batch of n robots takes once dispatched, at the smallest listed size that holds it (`served`'s
        post_ms; the forward pass's p95 without it): how long a request from a robot of another fit may wait behind
        it."""
        for b in self._timed:
            if b >= n:
                return self._served.post_ms(b, self._table) if self._served is not None else self._table.p95(b)
        return None

    def _holds(self, counts: dict[int, int], trips: dict[int, float], late: int | None = None,
               near: dict[int, float] | None = None, each: Sequence[float] = ()) -> bool:
        """Whether one replica can serve robots with these fits: no more robots of a fit than the fit itself
        (per_replica's latency rule), and no more than `most` in total; with robots of more than one fit on it, each
        fit's batch answered in time behind the longest batch of another fit: its batch + that batch + the RTT of its
        furthest robot (`trips`) + MARGIN_MS <= buffer_ms. A replica runs one batch at a time, and a robot of one fit is
        not held for another fit's batch (Aligner), so their batches run in separate phases and a request may arrive
        while another fit's batch runs. They must also be answered in time on a clock, each by its own RTT (`each`;
        in_time), at a load of no more than LOAD_MAX (with no cycle known, or nothing timed: latency alone, as
        per_replica). `late`: the fit of a robot admitted alone although late even alone: its own deadline is
        not met however it is batched, its own responses are not counted on the clock, and its batch is still what the
        others may wait behind. When capacity was computed from the fits alone, a far robot's request that waited behind
        the near robots' batch left 43 ms late in one test, and near robots' requests behind a far robot's batch left
        103 ms late in another. Where a wait is set, a response is limited by it in place of buffer_ms, and the load is
        by formula: each fit's batches over its nearest robot's own time between requests (`near`; wait_fill), together
        no more than LOAD_MAX."""
        if sum(counts.values()) > self._most or any(n > fit for fit, n in counts.items()):
            return False
        live = [fit for fit, n in counts.items() if n]
        if len(live) > 1:
            runs = {fit: self._took(min(counts[fit], fit)) for fit in live}
            if any(ms is None for ms in runs.values()):
                return False
            for fit in live:
                behind = max(runs[other] for other in live if other != fit)
                if fit != late and runs[fit] + behind + trips[fit] + MARGIN_MS > self._limit_ms:
                    return False
        if self._cycle_ms is None or self._cycle_ms <= 0.0 or not self._timed:
            return True
        if self._wait_ms is not None:
            share = 0.0
            for fit, n in counts.items():
                got = wait_fill(n, self._table, timed=self._timed, cycle_ms=self._cycle_ms, slack_ms=self._buffer_ms,
                                trip_ms=(near or trips)[fit], served=self._served, up_to=fit) if n else (fit, 0.0)
                if got is None:
                    return False
                share += got[1]
            return share <= LOAD_MAX
        if len(each) < 2:
            return True
        play = _played(self._buffer_ms, self._cycle_ms, self._step_ms)
        excused = [0] if late is not None else []          # nearest first: a robot late even alone is the first
        return in_time(self._table, play, each, sizes=self._timed, served=self._served, excused=excused)

    def _class(self, outside_ms: float | None) -> int:
        """The fit a robot is batched by here: its own, or 1 on a replica too slow for any robot (one at a time); 0 when
        it is late even alone where a robot at ROUND_TRIP_MS is not."""
        fit = self.fit(outside_ms)
        return 1 if fit == 0 and self._slow else fit

    def seat(self, robots: list[tuple[str, float | None]]) -> tuple[int, list[str]]:
        """(seats, over) for `robots`, given as [(robot, its RTT in ms, or None)], on this replica: taken nearest first
        (ties by name), as many of them as fit together, the first that does not fit ending the count, as per_replica's
        does; the first is always admitted, since an empty replica admits one robot, late or not; then as many
        additional robots at ROUND_TRIP_MS as still fit beside them. `seats` is the replica's capacity in total; `over`
        is the robots beyond it, the furthest last. A robot that is late even alone is admitted only when it is first.
        Where a wait is set, the largest number that fits is taken, which may follow one that does not (wait_fill)."""
        order = sorted(robots, key=lambda r: (ROUND_TRIP_MS if r[1] is None else r[1], r[0]))
        counts: dict[int, int] = {}
        trips: dict[int, float] = {}               # each fit's furthest robot's RTT
        near: dict[int, float] = {}                # ... and its nearest's: the earliest next request of that fit
        held, held_counts, held_trips, held_near, late = 0, {}, {}, {}, None
        each: list[float] = []                     # each robot's own RTT, nearest first: what the clock runs
        by_formula = self._wait_ms is not None     # a policy that sets a wait: the largest number that fits
        for k, (_, ms) in enumerate(order, start=1):
            fit = self._class(ms)
            if fit == 0:
                if k > 1:
                    break                          # late even alone: no larger count fits (it is the furthest)
                fit = late = 1
            trip = ROUND_TRIP_MS if ms is None else ms
            counts[fit] = counts.get(fit, 0) + 1
            trips[fit] = max(trips.get(fit, 0.0), trip)
            near[fit] = min(near.get(fit, trip), trip)
            each.append(trip)
            if k == 1 or self._holds(counts, trips, late, near, each):
                held, held_counts, held_trips, held_near = k, dict(counts), dict(trips), dict(near)
            elif not by_formula:
                break
        each = each[:held]
        fit = max(self._class(None), 1)
        more_trips = {**held_trips, fit: max(held_trips.get(fit, 0.0), ROUND_TRIP_MS)}
        more_near = {**held_near, fit: min(held_near.get(fit, ROUND_TRIP_MS), ROUND_TRIP_MS)}
        more = 0
        for m in range(1, self._most - held + 1):
            if (held == 0 and m == 1) or self._holds({**held_counts, fit: held_counts.get(fit, 0) + m}, more_trips,
                                                     late, more_near, each + [ROUND_TRIP_MS] * m):
                more = m
            elif not by_formula:
                break
        return held + more, [robot for robot, _ in order[held:]]


# ── how long an open batch may wait, and which requests go first ─────────────────────────────────────────────────────

@dataclass
class _Robot:
    seen: float                      # when its latest request arrived
    period_s: float | None = None    # time between its requests as they arrive (smoothed)
    spread_s: float | None = None    # a gap's deviation from that period (smoothed): when its next request may arrive
    dry_at: float | None = None      # when the actions sent to it run out
    entered: float | None = None     # when its latest request entered the server, which its buffer is counted from
    outside_s: float | None = None   # its last reported RTT (the time its requests spend outside the server)
    left_s: float | None = None      # the playback time left that its latest request reported


class Aligner:
    """One replica's robots, tracked as their requests arrive and their responses leave: how long an open batch may wait
    for the rest of them (hold_s), and which of its requests are dispatched first, separately (split).

    In one sentence: a robot requests its next response with N - k steps left in the chunk it is executing, its buffer →
    its request may wait, from when it entered the server, that long less its robot's reported RTT (ROUND_TRIP_MS when
    none is reported), and never past when the actions sent to it run out (N steps from when the last response left),
    each less the batch's time in the server with one more request in it and MARGIN_MS → the open batch waits for the
    replica's other robots until every one of them has a request in it, or until the first of its requests can wait no
    longer → it runs then, with the requests that arrived.

    WHY from when the request arrived: a robot sends requests on its own clock, k steps after its previous request, so
    holding its response does not move its next request. A wait measured from its last response would grow every round
    it was held, each response older than the last. The robots are not synchronized: those that arrive within what the
    first can wait share its batch, and the rest share the next. Nothing is predicted about a robot that has not arrived
    except when its next request is due: k steps after its last, as its own requests have arrived (_next). The batch
    waits for every robot admitted to the replica whose request is due before it must be dispatched, and for no other:
    four robots batched two by two once had each pair held for the other, which could not arrive in time, and 45% of
    their responses left late.

    Not held: any robot of a policy with no playback (nothing states how long it can wait), and the request of a robot
    that has no response from this replica being executed, that is, its first.

    `play`: how the policy's responses are executed by its robots (playback); with None, nothing is ever held. `seated`:
    the robots admitted to the replica now, by the names their requests arrive under. Its batch times are `served`'s
    (what the server's batches took once dispatched), else `table`'s (forward passes alone)."""

    def __init__(self, table: Table, play: Playback | None, seated: Callable[[], Iterable[str]],
                 served: Served | None = None) -> None:
        self._table = table
        self._served = served
        self.replay(play)
        self._seated = seated
        self._robots: dict[str, _Robot] = {}

    def replay(self, play: Playback | None) -> None:
        """Update how the policy's responses are executed from now on (playback): its parameters changed while it
        serves. A robot that reports the playback time it has left is still scheduled by that report; this applies to
        robots that report none."""
        self._play_s = play["play_s"] if play else None
        self._buffer_s = play["buffer_s"] if play else None
        # where the policy sets it: how long a robot waits for a response from when its request is sent
        self._wait_s = play.get("wait_s") if play else None
        # a control step: how much earlier than its replan step a robot's next request may arrive (its RTT varies)
        self._step_s = play.get("step_s") if play else None

    def arrived(self, robot: str | None, now: float, *, entered: float | None = None,
                outside_ms: float | None = None, left_ms: float | None = None) -> None:
        """Record that a request from `robot` arrived at `now`, having entered the server at `entered` (now, unless
        given), with its robot reporting an RTT of `outside_ms` (None: nothing reported this time, and its last report
        stands) and `left_ms` of playback left in the chunk it is executing (None: its policy's (N - k) / hz, for this
        request)."""
        if not robot or self._play_s is None:
            return
        for name in [n for n, r in self._robots.items() if self._gone(r, now)]:
            del self._robots[name]
        r = self._robots.get(robot)
        if r is None:
            r = self._robots[robot] = _Robot(seen=now)
        else:
            gap = now - r.seen
            if r.period_s is not None:
                off = abs(gap - r.period_s)
                r.spread_s = off if r.spread_s is None else (1.0 - PERIOD_WEIGHT) * r.spread_s + PERIOD_WEIGHT * off
            r.period_s = gap if r.period_s is None else (1.0 - PERIOD_WEIGHT) * r.period_s + PERIOD_WEIGHT * gap
            r.seen = now
        r.entered = now if entered is None else entered
        if outside_ms is not None:
            r.outside_s = outside_ms / 1000.0
        r.left_s = None if left_ms is None else left_ms / 1000.0

    def hold_s(self, waiting: list[str | None], now: float) -> float:
        """How long the open batch (the requests of `waiting`, by their robots) may wait for the replica's other robots
        to join it; 0 to run it now: when every robot admitted to the replica has a request in it, or none of the rest
        is due before it must be dispatched, or one of its robots has no chunk executing. Never past the time the
        first of its requests can wait no longer: when it entered the server plus its robot's buffer less the robot's
        RTT, or when its robot's actions run out, whichever is first, less the batch's time with one more request in it
        and MARGIN_MS. The tightest robot of the batch determines it."""
        robots = [self._robots.get(w) if w else None for w in waiting]
        if self._play_s is None or not robots or any(r is None or r.dry_at is None for r in robots):
            return 0.0
        last = min(self._end(r) for r in robots)
        batch_ms = self._batch_ms(len(waiting) + 1) or self._batch_ms(len(waiting)) or 0.0
        until = last - (batch_ms + MARGIN_MS) / 1000.0        # the latest it may be dispatched
        if not self._to_come(waiting, now, until) or until <= now:
            # every robot of the replica is in it, none of the rest is due by then, or it may wait no longer: it is
            # dispatched, except that a far robot's batch is not run ahead of a nearer robot's request that would be
            # late behind it (_guard)
            return self._guard(waiting, robots, now)
        return until - now

    def _guard(self, waiting: list[str | None], robots: list[_Robot], now: float) -> float:
        """How long a batch of far robots' requests (a batch none of whose robots' deadlines allow one more request
        beside them, _shares) waits for a robot of the replica whose next request is due while the batch would run and
        would leave late behind it: that request would wait for the whole batch, then run alone, and keep less than
        MARGIN_MS before its deadline. The batch waits for that request, which then joins it within its robot's own
        deadline. It waits past the time the request is due by at most its robot's tolerance (_give), then is
        dispatched. A wait that ended before the request arrived would only move the far batch onto it. 0 for any other
        batch, or when there is no such robot: a near robot's batch is held by its own robots' deadlines alone.

        WHY: a replica runs one batch at a time, so a request that arrived while a far robot's batch ran waited for the
        whole batch. A near robot beside one 250 ms further away ran out of actions 31 times in 240 s, and not once
        alone.
        WHY at most one control step: a far robot that is already late is not held tens of ms more for a near request
        that is not about to arrive. Waiting the whole gap once held a far robot 107 ms for a near one."""
        size = len(waiting)
        took, alone = self._batch_ms(size), self._batch_ms(1)
        if took is None or alone is None or any(self._shares(r, size + 1) for r in robots):
            return 0.0
        seated, latest = set(self._seated()), now
        for name, r in self._robots.items():
            if (name in waiting or name not in seated or self._gone(r, now) or r.dry_at is None
                    or not self._shares(r, size + 1)):
                continue
            outside = r.outside_s if r.outside_s is not None else ROUND_TRIP_MS / 1000.0
            left = self._left(r)
            # its next request, arriving at t, waits for this batch and runs alone: out at now + took + alone, due at
            # t + left - outside, so the margin is kept only once t is past `safe`
            safe = now + (took + alone + MARGIN_MS) / 1000.0 - (left - outside)
            due = r.seen + (r.period_s if r.period_s is not None else (self._play_s or 0.0) - (self._buffer_s or 0.0))
            give = self._give(r)
            if due - give < safe and due + give > now:
                latest = max(latest, due + give)
        return min(latest - now, self._step_s or 0.0)

    def _give(self, r: _Robot) -> float:
        """The tolerance around when `r`'s next request is due: three times the spread of its gaps, at least half a
        control step and at most a whole one. With arrivals jittered by up to 60 ms in a simulation at 15 Hz, a fixed
        half step (33 ms) let 141 of 4,104 of a near robot's requests arrive late behind a far robot's batch, no fewer
        than with no wait at all (132)."""
        step = self._step_s or 0.0
        return min(step, max(step / 2.0, 3.0 * (r.spread_s or 0.0)))

    def split(self, waiting: list[str | None], now: float, sizes: list[int], free: bool) -> list[int] | None:
        """Which of the open requests of `waiting` (by their robots) are dispatched first, separately, where the batch
        they would all go in (the largest of `sizes` they fill) would miss one robot's deadline: the requests whose
        robots' deadlines cannot be met even alone, together, in the largest of `sizes` they fill; else the request due
        first and those due next, in the largest of `sizes` its deadline allows (the smallest where none does). Returns
        their indexes in `waiting`, to send now.

        None to send them as one batch, as a batcher would without this: every robot's deadline allows the whole batch,
        one of the robots is not tracked, or dispatching separately would make a remaining request worse off. The
        remaining requests run on another replica at once (`free`: one is free besides the one this batch takes), else
        after the first batch; each must then keep what the whole batch would have left it when the first batch is
        requests that are late even alone, and otherwise its deadline and MARGIN_MS.

        Call it only when a replica is free to run the batch: a batch taken while every replica is busy waits behind
        theirs, and `now` is not when it runs."""
        robots = [self._robots.get(w) if w else None for w in waiting]
        if self._play_s is None or not robots or any(r is None or r.dry_at is None for r in robots):
            return None
        size = max((n for n in sizes if n <= len(waiting)), default=0)
        took = self._batch_ms(size) if size > 1 else None
        if took is None:
            return None
        ends = sorted((self._end(r), i) for i, r in enumerate(robots))              # due first
        whole = now + took / 1000.0                                                   # when the whole batch is out
        margin = MARGIN_MS / 1000.0
        if whole + margin <= ends[0][0]:
            return None                                       # every robot's deadline allows the whole batch
        alone = self._batch_ms(min(sizes))
        hopeless = sum(1 for end, _ in ends if alone is not None and now + alone / 1000.0 > end)   # margin excluded
        if hopeless:
            lead = max((n for n in sizes if n <= hopeless), default=min(sizes))
        else:
            fits = [n for n in sizes if n < size and (ms := self._batch_ms(n)) is not None
                    and now + ms / 1000.0 + margin <= ends[0][0]]
            lead = max(fits) if fits else min(sizes)
        if lead >= len(waiting):
            return None
        rest = [end for end, _ in ends[lead:]]
        after = max((n for n in sizes if n <= len(rest)), default=0)
        ms = self._batch_ms(after) if after else None
        if ms is None:
            return None
        out = (now if free else now + (self._batch_ms(lead) or 0.0) / 1000.0) + ms / 1000.0
        if not all(_kept(whole, out, end, margin) if hopeless else out + margin <= end for end in rest):
            return None
        return sorted(i for _, i in ends[:lead])

    def _end(self, r: _Robot) -> float:
        """The latest time `r`'s open request may leave the server answered: its own deadline (_due), or when its
        actions run out, whichever is first. The run-out time is not adjusted by its RTT: the downlink delay applies
        both to the response that left and to the next one, so it cancels. Its deadline alone where a wait is set: its
        robot waits once its actions run out."""
        if self._wait_s is not None:
            return self._due(r)
        return min(self._due(r), r.dry_at) if r.dry_at is not None else self._due(r)

    def _left(self, r: _Robot) -> float:
        """How long `r`'s request may take to come back answered, counted from when it was sent: the wait where its
        policy sets one; else the playback time its robot reported as left when it sent the request; else its policy's
        buffer ((N - k) / hz)."""
        if self._wait_s is not None:
            return self._wait_s
        if r.left_s is not None:
            return r.left_s
        return self._buffer_s if self._buffer_s is not None else 0.0

    def _shares(self, r: _Robot, size: int) -> bool:
        """Whether `r`'s deadline allows a batch of `size`: the playback time left when it sends its request, less its
        RTT, against the batch's time plus MARGIN_MS. A robot too far from its server for that is dispatched separately
        (split), so no batch waits for it. A size that was not timed is allowed for any robot."""
        ms = self._batch_ms(size)
        left = self._left(r)
        outside = r.outside_s if r.outside_s is not None else ROUND_TRIP_MS / 1000.0
        return ms is None or left - outside >= (ms + MARGIN_MS) / 1000.0

    def _due(self, r: _Robot) -> float:
        """The latest time its request's response may leave the server and still reach the robot before the chunk it is
        executing runs out: based on the playback time its robot reported as left when it sent the request, else its
        policy's buffer ((N - k) / hz), or the wait where one is set (_left). One request is in flight per robot, so a
        robot whose last response arrived late sends its next request past k / hz, with less left."""
        outside = r.outside_s if r.outside_s is not None else ROUND_TRIP_MS / 1000.0
        return (r.seen if r.entered is None else r.entered) + self._left(r) - outside

    def _batch_ms(self, size: int) -> float | None:
        return self._served.post_ms(size, self._table) if self._served is not None else self._table.p95(size)

    def due(self, robot: str | None) -> float | None:
        """The latest time `robot`'s open request may leave the server answered; subtracting the time it actually leaves
        gives the margin it had when its batch was dispatched. None for a robot that is not tracked."""
        r = self._robots.get(robot) if robot else None
        return self._due(r) if r is not None and self._buffer_s is not None else None

    def outsides_ms(self, now: float) -> dict[str, float | None]:
        """Each robot admitted now (heard from within GONE_PERIODS), with its last reported RTT in ms, or None for one
        that has not reported it. Its items are what Seating.seat takes, each robot with its own RTT."""
        seated = set(self._seated())
        return {name: (r.outside_s * 1000.0 if r.outside_s is not None else None) for name, r in self._robots.items()
                if not self._gone(r, now) and name in seated}

    def _to_come(self, waiting: list[str | None], now: float, until: float | None = None) -> bool:
        """Whether a robot of the replica has no request in `waiting` and is due before `until`: one that is admitted,
        was heard from within GONE_PERIODS of its period, and whose next request is due by then (_next). A robot sends
        its next request k steps after its previous one (one request in flight), so one whose next request is due after
        `until` does not join the batch, and waiting for it only idles the replica while the robots queued behind it
        wait. Due by then means likely to have arrived by then: a robot whose requests stray from their period is waited
        for only where even a late one arrives in time (_next). It must also be one whose deadline allows the batch
        (_shares): a far robot is dispatched separately (split)."""
        seated = set(self._seated())
        return any(name not in waiting and not self._gone(r, now) and name in seated
                   and (until is None or self._next(r) <= until) and self._shares(r, len(waiting) + 1)
                   for name, r in self._robots.items())

    def _next(self, r: _Robot) -> float:
        """The latest `r`'s next request is likely to arrive in the server: its last request's arrival plus the time
        between its requests as they have arrived (until two have: the k steps its robot executes before it sends the
        next one, N / hz less (N - k) / hz), plus three times the spread of those gaps, at most one control step.

        WHY the latest, not the earliest it could arrive (one control step sooner, for a faster uplink): a batch held
        for a robot that arrives just after the batch had to go runs without it, late in its own buffer, and that
        robot's request then waits behind it for a whole batch. With SmolVLA on an L4 (batches of 1 and 2 in 256 and
        273 ms; 15 Hz, a 467 ms buffer) and two simulated robots whose requests were 150 ms apart, the first request
        was held 115 ms for the second, which arrived 35 ms after the batch had to go: 55 of the second robot's 56
        responses were late, and none of them in a server that held no batch.
        WHY the spread is added: the two mistakes do not cost the same. A robot not waited for that arrives before the
        batch had to go only waits for what is left of a batch dispatched earlier; a robot waited for that arrives
        after is late. With the spread subtracted (when it is due, at the earliest), a stand-in for that model on a
        laptop, two robots whose requests were 120 to 149 ms apart, had 31 of the second robot's 113 responses late,
        against 2 of 512 where they were closer and none of 267 where they were further apart. On a clock with
        requests arriving 5 ms early or late (standard deviation), two such robots had 6.4% of their responses late
        with the spread subtracted, 1.7% with no spread term and 0.02% with it added."""
        came = r.seen if r.entered is None else r.entered
        every = r.period_s if r.period_s is not None else (self._play_s or 0.0) - (self._buffer_s or 0.0)
        return came + every + min(self._step_s or 0.0, 3.0 * (r.spread_s or 0.0))

    def _gone(self, r: _Robot, now: float) -> bool:
        return now - r.seen > GONE_PERIODS * max(r.period_s or 0.0, self._play_s or 0.0)

    def answered(self, robots: list[str | None], at: float) -> None:
        """Record that a batch's responses left at `at`: each of its robots runs out of those actions N valid steps
        later."""
        for robot in robots:
            r = self._robots.get(robot) if robot else None
            if r is not None and self._play_s is not None:
                r.dry_at = at + self._play_s

    def left(self, robot: str | None) -> None:
        """`robot` has finished, or is no longer admitted: none of the replica's batches waits for it from now on."""
        if robot:
            self._robots.pop(robot, None)


def _kept(whole: float, apart: float, end: float, margin: float) -> bool:
    """Whether a request due out by `end`, which is out at `apart` once the requests before it were dispatched
    separately instead of at `whole` with them, keeps what the whole batch left it: its deadline and the margin where it
    had both, its deadline where it had only that, and no later than `whole` where it had neither."""
    if whole + margin <= end:
        return apart + margin <= end
    return apart <= end if whole <= end else apart <= whole


# ── a replica's robots, run on a clock ───────────────────────────────────────────────────────────────────────────────

# Each robot past the second is moved on, from one start to the next, by a step of its own that never brings it back
# to where it was: the fractional part of a prime's square root, of a cycle.
_STEPS = [math.sqrt(p) % 1.0 for p in range(2, 300) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def starts(robots: int, cycle_s: float, count: int | None = None) -> list[list[float]]:
    """When each of `robots` robots sends its first request, in seconds into a cycle, for each of `count` runs on a
    clock, spread evenly over every way the robots' requests can fall: the first robot at 0, the second at evenly
    spaced gaps after it (the first 32 starts a 32nd of a cycle apart, the first 64 a 64th, the first 128 a 128th), and
    each further robot moved on by a step of its own from one start to the next (_STEPS). With no `count`: half of
    CLOCK_STARTS for two robots, between whose requests one gap is all that differs, and CLOCK_STARTS for more. The
    same number of robots is always run the same way, and one robot has one start.

    WHY several: robots send on their own clocks, and whether two of them share a batch depends on how far apart their
    requests are. Their phases drift, so over a long run a fleet meets every way its requests can fall.
    WHY spread evenly and not drawn: in_time takes the share of responses in time over the starts. With 40 starts drawn
    from a seed, that share for two robots was up to 6.7 points from what 2,048 starts gave, enough to turn a capacity
    of 2 into 1. On 150 fleets with 0.5% to 20% of their responses late, against 1,024 starts: 64 of these starts were
    within 0.9 points for two robots; 128 within 0.8 for three robots and 1.9 for four to six, where 64 were up to 4
    points off."""
    if robots <= 1:
        return [[0.0] * max(robots, 0)]
    if count is None:
        count = CLOCK_STARTS // 2 if robots == 2 else CLOCK_STARTS
    out = []
    for i in range(max(count, 0)):
        gap, part, left = 0.0, 0.5, i
        while left:                                # i's bits in reverse: 0, 1/2, 1/4, 3/4, 1/8, ...
            gap, part, left = gap + part * (left & 1), part / 2.0, left >> 1
        # a third of the finest step off: two robots alike are then run at a gap and never at its mirror image
        begin = [0.0, (gap + 1.0 / (3.0 * CLOCK_STARTS)) % 1.0 * cycle_s]
        begin += [(i + 1) * _STEPS[j % len(_STEPS)] % 1.0 * cycle_s for j in range(robots - 2)]
        out.append(begin[:robots])
    return out


def on_a_clock(table: Table, play: Playback, outsides_ms: Sequence[float | None], begin: Sequence[float], *,
               sizes: list[int], served: Served | None = None, cycles: int = CLOCK_CYCLES,
               early: bool = False, excused: Sequence[int] = (),
               spare_ms: float = 0.0) -> tuple[int, int, float]:
    """One replica and its robots for `cycles` cycles on a simulated clock: (late responses, responses, the load),
    counted from the CLOCK_WARM-th cycle on. `outsides_ms`: each robot's RTT (None: ROUND_TRIP_MS); `begin`: when each
    sends its first request (starts). No model runs: a batch advances the clock by its time as timed (`served`'s
    post_ms; the forward pass's p95 without it), and nothing is added to `table` or `served`. `excused`: the robots, by
    their place in `outsides_ms`, whose own late responses are not counted (a robot too far to be answered in time even
    alone).

    `early`: return once the run repeats itself, with (late responses, responses, the load) of the stretch that
    repeats, which is what in_time asks for.
    A run repeats from when, as a batch ends, everything the rest of it depends on (what the Aligner has of each robot,
    the requests waiting, in a batch and on their way, each time counted from that moment) is what it was as an earlier
    batch ended: the same follows. Most runs repeat within their first eight cycles, every cycle or every few. The
    outcome is that of the run of every cycle, except where a request falls due at the very instant its batch must go:
    that choice rests on the last bit of a sum, a run of every cycle can make it differently in a later cycle, and the
    two outcomes can differ (in 1 of 24,000 random runs, whose batch times added up to its cycle to the ms).

    The load is the share of a cycle (k / hz) the robots' batches fill when each robot sends one request in it: what
    the batches the replica ran typically take (`served`'s typical_ms; the forward pass's p50 without it) for each
    request they answered, times the number of robots, over the cycle. For robots that all send every cycle that is the
    share of the time the replica typically runs a batch. WHY not the share of the time it ran: a robot whose response
    takes longer than a cycle sends its next request when the response is back, so a replica too slow for its robots
    is busy all the time less their RTT, and that share fell below LOAD_MAX for robots 100 ms away and not for the same
    robots 47 ms away. WHY typical times for the load and the slower ones for the clock: a response must be in time
    when its batch is a slow one, and a cycle is filled by what batches take on average.

    The clock's resolution: each listed size's two times are rounded up to CLOCK_BITS significant bits (by 3% at most)
    and each RTT up to a multiple of CLOCK_RTT_MS, so a run is of a model slightly slower and robots slightly further
    away than timed. WHY: a server's batch times and its robots' reported RTTs move by a few ms from one request to the
    next, and each new value would otherwise be a new question for in_time.

    In one sentence: each robot sends a request every cycle (k / hz) from its own start, or as soon as a response is
    back that took longer than that → each request arrives half its RTT later and is handled as a server handles it
    (Aligner.arrived, hold_s as each request arrives and as each batch ends, split as a batch is dispatched, the
    largest listed size the waiting requests fill, Aligner.answered) → a response is late when it is back after the
    chunk its robot is executing ran out (with `spare_ms`: when it is not back that long before): N steps from when the
    request before it was sent, which for a request sent on time is its time in the server and its robot's RTT against
    the buffer. A request sent late has less than the buffer left, and its robot reports it (left_ms), as a robot
    does.

    WHY the loop and not a formula: whether robots share a batch depends on how their requests fall, and on what
    hold_s and split then do. A formula for the load that assumed robots share larger batches once their batches of one
    size no longer fit in a cycle gave a capacity of 8 for a model with batches of 1, 2, 4 and 8 in 256, 273, 303 and
    377 ms (15 Hz, a 467 ms buffer), and four simulated robots on an L4 had 95% of their responses late: they ran as two
    fixed pairs, each request behind the other pair's batch. This loop, with those times, gives the same."""
    timed = [b for b in sorted(sizes) if b in set(table.sizes())]
    if not timed or not outsides_ms:
        return 0, 0, 0.0
    # the listed sizes alone, each at what it takes once dispatched (what a batch lasts here and the Aligner holds
    # by) and at what it typically takes (what the load is counted by): a size that was timed and is not listed is not
    # run, and a batch smaller than the smallest listed size is timed as that size, as the Table reads an unlisted size
    table = _of_times(_resolved(table, served, timed))

    def took(n: int) -> float:
        return (table.p95(n) or 0.0) / 1000.0

    def fills(n: int) -> float:
        return (table.p50(n) or 0.0) / 1000.0

    buffer_s, cycle_s = play["buffer_s"], play["play_s"] - play["buffer_s"]
    names = [f"robot-{i}" for i in range(len(outsides_ms))]
    trip = {name: _far(ms) / 1000.0 for name, ms in zip(names, outsides_ms)}
    aligner = Aligner(table, play, seated=lambda: names)
    forgiven = {names[i] for i in excused}
    order = itertools.count()
    # a request: (robot, sent at, when the chunk its robot is executing runs out; None for its first, which has none)
    events = [(at + trip[name] / 2.0, next(order), "request", (name, at, None)) for name, at in zip(names, begin)]
    heapq.heapify(events)
    counted_from, until = CLOCK_WARM * cycle_s, cycles * cycle_s
    waiting: list[tuple[str, float, float | None]] = []
    busy, timer, late, total, ran, answered = False, None, 0, 0, 0.0, 0
    per_cycle = len(names) / max(cycle_s, 1e-9)        # requests in a second, each robot sending one every cycle
    # for `early`: the same four counts from the run's start, and what they were at each state the run has been in
    whole = [0, 0, 0.0, 0]
    been: dict[int, tuple[int, int, float, int]] = {}

    def state(now: float) -> int:
        def since(at: float | None) -> int | None:
            return None if at is None else round((at - now) * 1e7)                 # to 0.1 µs

        def span(s: float | None) -> int | None:
            return None if s is None else round(s * 1e7)

        def asked(request: tuple[str, float, float | None]) -> tuple:
            return request[0], since(request[1]), since(request[2])

        ahead = []
        for at, _, kind, what in sorted(events):
            ahead.append((since(at), kind, asked(what) if kind == "request" else since(what) if kind == "timer"
                          else (since(what[0]), tuple(asked(w) for w in what[1]))))
        robots = tuple((name, since(r.seen), since(r.entered), since(r.dry_at), span(r.period_s), span(r.spread_s),
                        span(r.left_s)) for name, r in sorted(aligner._robots.items()))
        return hash((robots, tuple(asked(w) for w in waiting), tuple(ahead), busy, since(timer)))

    def send(now: float) -> None:
        nonlocal waiting, busy, timer
        ahead = aligner.split([w[0] for w in waiting], now, timed, free=False)
        fill = [b for b in timed if b <= len(waiting)]
        batch = [waiting[i] for i in ahead] if ahead else waiting[:max(fill)] if fill else list(waiting)
        waiting = [w for w in waiting if w not in batch]
        busy, timer = True, None
        heapq.heappush(events, (now + took(len(batch)), next(order), "done", (now, batch)))

    def go_or_wait(now: float) -> None:
        nonlocal timer
        hold = aligner.hold_s([w[0] for w in waiting], now)
        if hold <= 0.0:
            send(now)
        else:
            timer = now + hold
            heapq.heappush(events, (timer, next(order), "timer", timer))

    while events:
        now, _, kind, what = heapq.heappop(events)
        if now > until:
            break
        if kind == "request":
            name, sent, runs_out = what
            left = None if runs_out is None or runs_out - sent >= buffer_s - 1e-9 else max(0.0, runs_out - sent)
            aligner.arrived(name, now, outside_ms=trip[name] * 1000.0, left_ms=None if left is None else left * 1000.0)
            waiting.append((name, sent, runs_out))
            if not busy:
                go_or_wait(now)                    # asked again as each request arrives, which can end the wait
        elif kind == "timer":
            if timer == what and not busy:
                send(now)
        else:
            dispatched, batch = what
            whole[2], whole[3] = whole[2] + fills(len(batch)), whole[3] + len(batch)
            if dispatched >= counted_from:
                ran, answered = ran + fills(len(batch)), answered + len(batch)
            aligner.answered([w[0] for w in batch], now)
            for name, sent, runs_out in batch:
                back = now + trip[name] / 2.0
                if runs_out is not None and name not in forgiven:
                    is_late = back + spare_ms / 1000.0 > runs_out + 1e-9
                    whole[0], whole[1] = whole[0] + is_late, whole[1] + 1
                    if sent >= counted_from:
                        total, late = total + 1, late + is_late
                # its next request: k steps after this one was sent, or at once when the response took longer; the
                # chunk it then executes is this response's, N steps from when this request was sent
                again = max(sent + cycle_s, back)
                heapq.heappush(events, (again + trip[name] / 2.0, next(order), "request",
                                        (name, again, sent + play["play_s"])))
            busy = False
            if waiting:
                go_or_wait(now)
            if early:
                was = been.setdefault(state(now), (whole[0], whole[1], whole[2], whole[3]))
                if whole[3] > was[3]:              # in this state before: what happened since happens again
                    return (whole[0] - was[0], whole[1] - was[1],
                            (whole[2] - was[2]) / (whole[3] - was[3]) * per_cycle)
    return late, total, ran / max(answered, 1) * per_cycle


def _up(ms: float | None) -> float:
    """A batch time rounded up to the clock's resolution. Read to the nanosecond first: a time that a difference of two
    clock readings gives as 312.00000000000006 ms is 312, where rounding it up as it stands made it 320."""
    whole = math.ceil(round(ms or 0.0, 6))
    step = 2 ** max(0, math.frexp(whole)[1] - CLOCK_BITS)
    return float(math.ceil(whole / step) * step)


def _far(ms: float | None) -> float:
    """An RTT rounded up to the clock's resolution; ROUND_TRIP_MS for a robot that reported none."""
    return math.ceil((ROUND_TRIP_MS if ms is None else ms) / CLOCK_RTT_MS) * CLOCK_RTT_MS


def _resolved(table: Table, served: Served | None, timed: list[int]) -> list[tuple[int, float, float]]:
    """Each of the `timed` sizes as the clock runs it: (size, what it typically takes, what it takes once dispatched),
    each rounded up to the clock's resolution."""
    return [(b, _up(served.typical_ms(b, table) if served is not None else table.p50(b)),
             _up(served.post_ms(b, table) if served is not None else table.p95(b))) for b in timed]


def _of_times(times: Iterable[tuple[int, float | None, float | None]]) -> Table:
    """A table of these sizes, each given as (size, its p50 in ms, its p95 in ms)."""
    table = Table()
    for size, usual, slow in times:
        for ms in (usual, usual, slow):            # of three runs the median is the second, the p95 the slowest
            table.add(size, float(ms or 0.0))
    return table


def _most_load(table: Table, robots: int, cycle_s: float, timed: list[int]) -> float:
    """The most `robots` robots' batches can fill a cycle however their requests fall: on_a_clock's load is what the
    batches it ran typically take for each request they answered, times the robots, over the cycle, and no batch costs
    a request more than the costliest of the sizes a batch of these robots can have: a request alone at the time of
    the smallest listed size, where two share one for less each."""
    most = min(robots, timed[-1]) if timed else 0
    costliest = max(((table.p50(n) or 0.0) / n for n in range(1, most + 1)), default=0.0)
    return robots / max(cycle_s, 1e-9) * costliest / 1000.0


# in_time's verdicts, by what it was asked: a server asks again as each robot connects, mostly the same question.
# Kept under a lock and read in one step: a server may ask from its loop and from a thread that times its model.
_CLOCKED: dict = {}
_CLOCKED_MOST = 1024
_KEEPING = threading.Lock()


def in_time(table: Table, play: Playback, outsides_ms: Sequence[float | None], *, sizes: list[int],
            served: Served | None = None, excused: Sequence[int] = ()) -> bool:
    """Whether one replica answers robots with these RTTs in time: run on a clock from starts spread over every way
    their requests can fall (on_a_clock, starts), at least IN_TIME_MIN of their responses are back before their robot's
    buffer runs out, each start counting the same, and in no start is the load more than LOAD_MAX. `excused`: robots
    whose own late responses are not counted (on_a_clock).

    WHY a share, not every response in every start: robots send on their own clocks and their phases drift, so the
    share over the starts is the share of a long run, and a fleet is not refused for an arrangement it is seldom in.
    Two π0.5 robots 100 ms away (batches of 1 and 2 in 195 and 312 ms; 15 Hz, a 467 ms buffer) are late only while
    their requests fall 5 to 25 ms apart, 4% of their responses over the starts; on an L4 two such robots had no late
    response in 225, and every response in every start gave them a capacity of 1.

    The starts are run until the verdict cannot change, and it is the verdict of running them all: not in time as
    soon as too many responses are late or a start's load is above LOAD_MAX; in time once every start left could be
    all late without making too many, where no start can be above LOAD_MAX at all (_most_load), which leaves 3 starts
    of 64 and 6 of 128 unrun.

    The verdict is kept by what the clock runs: each listed size's times and each RTT at the clock's resolution
    (on_a_clock), so the same question is run once. WHY kept: a server asks as each robot connects and as its timings
    move, on the loop that answers its robots, and a verdict takes about 5 ms of one core for two robots, 40 ms for
    eight and 90 ms for sixteen, more where the runs do not come to repeat (on_a_clock)."""
    timed = [b for b in sorted(sizes) if b in set(table.sizes())]
    took = _resolved(table, served, timed)
    trips = tuple(_far(ms) for ms in outsides_ms)
    key = (tuple(took), play["play_s"], play["buffer_s"], play.get("step_s"), trips, tuple(excused))
    kept = _CLOCKED.get(key)
    if kept is not None:
        return kept
    rounded = _of_times(took)
    cycle_s = play["play_s"] - play["buffer_s"]
    begins = starts(len(trips), cycle_s)
    most = (1.0 - IN_TIME_MIN) * len(begins) + 1e-9        # of each start's share of late responses, summed
    verdict, late_share = True, 0.0
    never_full = _most_load(rounded, len(trips), cycle_s, timed) <= LOAD_MAX + 1e-9
    for left, begin in zip(range(len(begins) - 1, -1, -1), begins):
        late, total, load = on_a_clock(rounded, play, trips, begin, sizes=timed, early=True, excused=excused)
        late_share += late / total if total else 0.0
        if late_share > most or load > LOAD_MAX + 1e-9:    # a load of exactly LOAD_MAX passes, however it was summed
            verdict = False
            break
        if never_full and late_share + left <= most:
            break                                  # in time whatever the starts left give: all late, still enough
    with _KEEPING:
        if len(_CLOCKED) >= _CLOCKED_MOST:
            del _CLOCKED[next(iter(_CLOCKED))]
        _CLOCKED[key] = verdict
    return verdict
