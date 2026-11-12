"""
A teleop connection's measures, read as one snapshot: counters, gauges, and latencies in microseconds - each latency's
p50, p95 and p99 over its latest 256 samples.

In one sentence: the transport counts what it sent, received, dropped and let expire (count), sets what holds now
(gauge: the robot clock's offset), and times each latency it can (sample, or since a stamp) into that latency's window
of the latest 256 → snapshot() reads them all at once - each counter, each gauge, and per latency its window's n, total,
last, mean, max and nearest-rank p50 / p95 / p99, a percentile None until the window holds enough samples for it →
reset() starts the counts and the windows over, leaving the gauges. A console's and a robot's measures are declared
(CONSOLE, ROBOT) so each snapshot holds every one of them from the start; where a command's time goes is its legs, each
a latency of its own: arrive_us (sent → the robot has it), actuate_us (→ act() hands it back), written_us (→ the robot's
code wrote it to its motors), loop_us (the frame it answered, captured → act()).
WHY microseconds, a window of 256 and a snapshot: LiveKit Portal's metrics (Apache-2.0), whose design this borrows




WHY these names: the direct connection's own, which calls this module from its transport - shared by the console, the
robot and the bench.

WHY nearest-rank: the baseline the direct connection is measured against was computed so, and a percentile of ours
reads against it only if it is the same one.

WHY no percentile below its floor: of fewer than 1/(1-q) samples a q-percentile is the window's max - p99 of 20 samples
is the worst of 20 - so p50 needs 2 samples, p95 20 and p99 100; until then it reads None - not enough samples - rather
than a number that reads like a percentile and is not one.
Cost: count, gauge and sample each take the lock and do O(1) work - a ring buffer written in place, its sum kept as it
goes; the sort is snapshot()'s alone, of at most 256 numbers per latency.
"""
from __future__ import annotations

import math
import threading
import time
from typing import Dict, Iterable, List, Optional


WINDOW = 256

PERCENTILES = ((50, 2), (95, 20), (99, 100))




COMMAND_US = "command_us"
RTT_US = "rtt_us"
FRAME_US = "frame_us"
STATE_US = "state_us"
INPUT_US = "input_us"


ARRIVE_US = "arrive_us"
ACTUATE_US = "actuate_us"
LOOP_US = "loop_us"

WRITTEN_US = "written_us"



COMMANDS_SENT = "commands_sent"
COMMANDS_UNANSWERED = "commands_unanswered"
FRAMES_RECEIVED = "frames_received"
FRAMES_DROPPED = "frames_dropped"

FRAMES_EXPIRED = "frames_expired"
STATES_RECEIVED = "states_received"
COMMANDS_RECEIVED = "commands_received"
COMMANDS_PLAYED = "commands_played"
COMMANDS_SUPERSEDED = "commands_superseded"
COMMANDS_DROPPED = "commands_dropped"
COMMANDS_EXPIRED = "commands_expired"
COMMANDS_NOT_DRIVING = "commands_not_driving"
FRAMES_SENT = "frames_sent"

CLOCK_OFFSET_US = "clock_offset_us"
CLOCK_UNCERTAINTY_US = "clock_uncertainty_us"
CONSOLES = "consoles"


CONSOLE = {
    "counters": (COMMANDS_SENT, COMMANDS_UNANSWERED, FRAMES_RECEIVED, FRAMES_DROPPED, FRAMES_EXPIRED, STATES_RECEIVED),
    "gauges": (CLOCK_OFFSET_US, CLOCK_UNCERTAINTY_US),
    "latencies": (COMMAND_US, RTT_US, FRAME_US, STATE_US, INPUT_US),
}
ROBOT = {
    "counters": (COMMANDS_RECEIVED, COMMANDS_PLAYED, COMMANDS_SUPERSEDED, COMMANDS_DROPPED, COMMANDS_EXPIRED,
                 COMMANDS_NOT_DRIVING, FRAMES_SENT, FRAMES_DROPPED),
    "gauges": (CONSOLES,),
    "latencies": (ARRIVE_US, ACTUATE_US, LOOP_US, WRITTEN_US),
}


def now_us() -> int:
    """The wall clock in whole microseconds: what a stamp that travels to another process or machine is written in,
    and what since() reads its latency against."""
    return time.time_ns() // 1000


def nearest_rank(ordered: List[int], q: int) -> Optional[int]:
    """The q-th percentile (q a whole number, 0 < q <= 100) of `ordered` - its values sorted, smallest first - by nearest
    rank: the ceil(q/100 * n)-th smallest, in integers so no float rounding moves it; None for no values. A
    percentile's floor (PERCENTILES) is its caller's to keep."""
    if not ordered:
        return None
    return ordered[max(0, -(-q * len(ordered) // 100) - 1)]


def _microseconds(us) -> int:
    """`us` as whole microseconds; a value that is not a finite number raises - a bad stamp is the caller's bug to
    see, not a sample to drop quietly."""

    if isinstance(us, bool) or not isinstance(us, (int, float)):
        raise TypeError(f"a latency is a number of microseconds, not {type(us).__name__}")

    if isinstance(us, float) and not math.isfinite(us):
        raise ValueError(f"a latency is a finite number of microseconds, not {us}")
    return int(round(us))


class _Window:
    """One latency's latest WINDOW samples, written in place over the oldest, with their sum kept as they come: adding
    one is O(1). Its lock is its LatencyStats's."""

    __slots__ = ("values", "n", "at", "sum", "last", "total")

    def __init__(self) -> None:
        self.values: List[int] = [0] * WINDOW
        self.clear()

    def clear(self) -> None:
        """Empty, as after reset(): the slots stay, their contents no longer count."""
        self.n = 0
        self.at = 0
        self.sum = 0
        self.last: Optional[int] = None
        self.total = 0

    def add(self, us: int) -> None:

        if self.n == WINDOW:
            self.sum -= self.values[self.at]
        else:
            self.n += 1
        self.values[self.at] = us
        self.sum += us
        self.at = self.at + 1 if self.at + 1 < WINDOW else 0
        self.last = us
        self.total += 1

    def read(self) -> dict:
        """The window as snapshot() says it: n, total, last, mean, max and the percentiles, None where it lacks the
        samples. Called under the lock; the sort, of at most WINDOW numbers, is here alone."""

        ordered = sorted(self.values[:self.n])
        out = {"n": self.n, "total": self.total, "last": self.last,
               "mean": round(self.sum / self.n) if self.n else None, "max": ordered[-1] if ordered else None}
        for q, floor in PERCENTILES:

            out[f"p{q}"] = nearest_rank(ordered, q) if self.n >= floor else None
        return out


class LatencyStats:
    """
    One connection's measures (module docstring): counters (count), gauges (gauge) and latencies in microseconds
    (sample, since), read together by snapshot() and started over by reset(). Safe from any thread - a transport's
    loop writes while the caller reads - each call O(1) but snapshot().

    counters, gauges, latencies   names to hold from the start, a counter at 0, a gauge and each percentile at None;
                                  any other name is taken as it first comes. LatencyStats(**CONSOLE) holds a teleop
                                  console's, LatencyStats(**ROBOT) a teleop robot's.
    """

    def __init__(self, counters: Iterable[str] = (), gauges: Iterable[str] = (), latencies: Iterable[str] = ()) -> None:

        self._lock = threading.Lock()
        self._counters: Dict[str, int] = {name: 0 for name in counters}
        self._gauges: Dict[str, Optional[int]] = {name: None for name in gauges}
        self._windows: Dict[str, _Window] = {name: _Window() for name in latencies}

    def count(self, name: str, n: int = 1) -> None:
        """Add n to the counter `name`: what was sent, received, dropped or let expire since the start or reset()."""
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + n

    def gauge(self, name: str, value) -> None:
        """Set the gauge `name` to what holds now (the clock's offset, a queue's depth); None says it is not known."""
        with self._lock:
            self._gauges[name] = value

    def sample(self, name: str, us) -> None:
        """One latency of `name`, in microseconds, into its window of the latest WINDOW: O(1). A value that is not a
        finite number raises TypeError or ValueError, and nothing is kept."""
        value = _microseconds(us)
        with self._lock:
            self._window(name).add(value)

    def _window(self, name: str) -> _Window:
        """The window of `name`, made as it first comes. Under the lock."""
        window = self._windows.get(name)
        if window is None:
            window = self._windows[name] = _Window()
        return window

    def since(self, name: str, stamp_us) -> None:
        """The latency of `name` from `stamp_us` - a wall-clock stamp in microseconds (now_us(), or the robot's clock
        with its offset applied) - to now."""
        self.sample(name, now_us() - _microseconds(stamp_us))

    def snapshot(self) -> dict:
        """Everything at one moment, as plain JSON that no later event changes: {"counters": {name: int}, "gauges":
        {name: value}, "latency_us": {name: {"n", "total", "last", "mean", "max", "p50", "p95", "p99"}}} - "n" the
        samples in the window, "total" all since the start or reset(), a percentile None until "n" reaches 2 for p50,
        20 for p95 and 100 for p99."""
        with self._lock:
            return {"counters": dict(self._counters), "gauges": dict(self._gauges),
                    "latency_us": {name: window.read() for name, window in self._windows.items()}}

    def reset(self) -> None:
        """Start over: every counter to 0 and every window emptied, their names kept. The gauges stay: each is what
        holds now, not a count since a start - an offset zeroed would read as a clock that lost its sync.
        

"""
        with self._lock:
            for name in self._counters:
                self._counters[name] = 0
            for window in self._windows.values():
                window.clear()
