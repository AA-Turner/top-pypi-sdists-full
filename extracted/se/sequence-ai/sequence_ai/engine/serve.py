# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A policy server in one call: your model as a function, served to robots elsewhere - what `seq serve` runs a
@seq.policy class on.

    from sequence_ai.engine.serve import serve

    def policy(observation):                     # your model: one observation in, what the robot needs out
        return {"actions": model(observation["image"], observation["state"])}

    serve(policy, port=8000, example=observation)

On the robot, sequence_ai.connect("http://<this machine>:8000") gives the same Policy a deployed policy's name gives:
observe(observation) as the robot makes each, act() when it wants an answer.

In one sentence: serve() listens on every address of this machine → a robot opens its stream (GET /stream, a
WebSocket) → each observation goes on it as it is made (POST /observe: a sequence_ai.Video item as video), kept in order
by episode and turned back on a thread of its own (engine.data_plane) → each act names how many observations of its
episode came before it (POST /act, {"call": "act", "episode_id", "seq"}) → once those are in, the policy is called with
the newest on a thread of its own, one call at a time (with `batch`, on a list of the observations waiting) → its
output goes back in msgpack, numpy arrays as arrays, with how long the server took ({"outputs", "perf"}).

What each part does by default, and how to change it:

    one call at a time   the policy runs on one thread of its own, one call at a time; acts that arrive  -
                         meanwhile wait their turn, in order
    batching             off; with batch, the acts that wait while the policy runs go in one call,    batch=[1, 2, 4, 8]
                         none held back for more
    addresses            every address of this machine: 0.0.0.0, and :: where it has IPv6             host="127.0.0.1"
    the robot's stream   each robot's observations and acts on one WebSocket (GET /stream), each        -
                         message answered as a request; the robot pinged every 60 s, let go 20 s after
                         a ping it did not answer; X-Seq-Act-Formats names it on every answer
    an act sent twice    run once: the same act under its request id (X-Seq-Request-Id) - on another     -
                         of the robot's lines, or sent again after its answer was lost - is handed
                         the first's answer, while it runs and for KEPT_S after
    observations         kept by episode, in order, the robot's Video, Depth and Tactile items turned    -
                         back into the arrays they were; one that is missing is asked for again, an
                         act waiting for it (engine.data_plane, engine.stream)
    ping                 GET /ping is answered at once, even while the policy runs: 503 with          -
                         Retry-After until the warm-up is done, then 200 with what it is, as JSON
                         (server, version, up_s, pid, policy, and the speed-ups on: optimized)
    identity             X-Seq-Server: sequence-ai/<version> on every response                        -
    warm-up              with `example`, the policy runs on it twice at each batch size before        example=None
                         /ping says ready, and GET /example hands it out; with hz, a warning where
                         its answer holds fewer steps than a robot plays of each
    speed-ups            during the warm-up, those that keep the policy's outputs exactly as they     cuda_graphs=False
                         are - CUDA graphs of its modules, and of its whole run - each checked on     whole_graph=False
                         `example` (or `examples`) and kept where it is faster (engine.optimize);
                         /ping says which are on. Those that change the outputs are yours to turn     torch_compile=True
                         on, each with the difference you accept                                      tolerance=1e-3
    inputs               numpy arrays as arrays, each the policy's own to write into                  -
    outputs              torch tensors and JAX arrays come back as numpy arrays (bfloat16 as          -
                         float32), copied on the policy's thread
    one write            each response leaves in one write (one_write)                                -
    server time          each answer's perf: handler_ms, from the act's last byte to its answer, and  -
                         inference_ms, the policy call's
    recording            the last minute of the robots' steps in memory, for a recorder to read as     record=False
                         they come (GET /record: engine.recorder, network.record)
    token                none, unless $SEQ_SERVE_TOKEN is set                                         token="..."
    keep-alive           an idle connection is kept open 5 minutes                                    -
    each robot's time    off: no act waits for another. Told how a robot plays an answer, an act      hz=20, ...
                         waits for others only as long as its own robot's answer leaves it time, and
                         a far robot's act goes first, apart, where a batch with the others would make
                         it late (engine.slack.Aligner)
    seats                with hz: a robot is let in at its first act only where every robot let in    -
                         is still answered in time however their acts fall, each by its own round
                         trip, none put out for it (engine.slack.Seating); any other is refused 503,
                         saying why
    several processes    one; started by a launcher as several (torchrun: WORLD_SIZE, RANK,            torchrun
                         MASTER_ADDR, MASTER_PORT), rank 0 serves the robots and every call of the
                         policy goes to every rank first, each running it on its part of the model;
                         a rank that leaves halts them all, each act after refused, saying why
                         (engine.ranks)

Each robot's time and its seat (`hz`, with `action_chunk_valid_len` or `action_chunk_replan_at`, as @seq.policy declares
them; `example` times the batches): the warm-up times each listed batch size (engine.slack.measure's rules: one untimed
run, then slack.RUNS) → a robot's Policy takes them from /ping and names its robot on each act (X-Seq-Session), with the
round trip its acts spend outside the server (X-Seq-Outside-Ms) and what is left of the answer it plays as it asks
(X-Seq-Chunk-Left-Ms) → at a robot's first act it is seated if the robots seated and it are all answered in time
however their acts fall, each by its own round trip (slack.Seating, which runs them on a clock from every start), none
of them put out for it; else that act is refused 503, unavailable, reason not_seated, with why, and so is each next one
until there is room → each act of a seated robot waits for the others' only as long as its own answer leaves it time
(slack.Aligner.hold_s), and goes first, apart, where one batch with them would make it late (Aligner.split) → each
forward pass and each answer's time goes into the times its seats and waits are counted by (slack.Table, slack.Served).
A robot gives its seat up once it has no act in flight and has sent none for slack.GONE_PERIODS of its answers' N steps.
An act that names no robot is served as without `hz`: not seated, and not held. Without `hz` no act waits for another:
what goes in one batch is what waited while the policy ran. The platform's workers seat and hold robots by these rules;
engine/slack.py has the measurements behind them.

WHY a thread of its own: a model's forward pass blocks for tens of milliseconds, and on the event loop it would hold
every ping and every upload in progress for as long: with a 200 ms stand-in model, a ping's p50 was 153 ms with the
model on the event loop and 1.0 ms with it on its own thread. It makes no act faster: with one policy, acts wait their
turn either way (316 ms against 320 ms there), and what serves several robots sooner is `batch`. CUDA and JAX keep
state per thread (the current device and stream, a trace's context), so the policy always runs on the same one, its
warm-up included.
WHY /ping answers from the event loop: a robot asks it while it waits for the server to be ready
(wait_until_ready()), and a ping queued behind the model would tell it nothing until the model is done.
WHY torch and JAX outputs are copied to numpy on the policy's thread: copying a GPU tensor waits for the GPU to finish
it, which must not happen on the event loop; msgpack carries numpy arrays.

`App` is the ASGI app serve() runs, for an ASGI server of your own: uvicorn.run(WholeResponse(App(policy)),
http=one_write_http(), ws=network.websocket.protocol()) is serve() without its listening sockets, logging and limits.

Needs sequence-base (Python 3.10 or later), which sequence-ai installs there; uvicorn, which sequence-ai installs, is
imported when serve() starts.
"""
from __future__ import annotations

import asyncio
import collections
import concurrent.futures
import errno
import hmac
import inspect
import json
import logging
import os
import socket
import sys
import threading
import time
import urllib.parse
from typing import Any, Callable, Iterable, Optional

from .._core.outside import HEADER as OUTSIDE_HEADER
from .._core.outside import LEFT_HEADER
from ..network import msgpack_io
from ..network.loop import steps as _steps
from . import ranks as _ranks
from . import recorder as _record
from . import slack, split_trials

try:                                    # the platform's data plane, where sequence-base is installed (Python 3.10+)
    from .data_plane import Refused as _Refused
except ImportError:                     # none: App() says what to install (_data_plane), and nothing raises this
    class _Refused(Exception):          # type: ignore[no-redef]
        """Never raised: with no data plane there is no App to refuse anything."""
from .batcher import Batcher
from .stream_intake import FORMAT as STREAM_FORMAT
from .stream_intake import StreamIntake

__all__ = ["App", "serve", "TOKEN_ENV", "LIMIT", "KEEP_ALIVE_S"]

log = logging.getLogger("sequence_ai.serve")
# Said once a server starts with no example: what it leaves out, and what gives one
NO_EXAMPLE = ("no example observation, so the policy is not warmed up and no speed-up is tried: add a @seq.sample "
              "method to the policy")

TOKEN_ENV = "SEQ_SERVE_TOKEN"     # read where serve() is given no token, as the check command reads it for --token
LIMIT = 64 << 20                  # the most bytes a request's body, and each item in it restored, may hold
KEEP_ALIVE_S = 300                # how long an idle connection is kept open: a robot paused for minutes resumes on it
RETRY_AFTER_S = 1                 # what a ping during the warm-up says to wait
FAILED_SAID_S = 3.0               # how long a server whose warm-up failed answers /ping 500, why, before it stops
# How long an act's answer is kept for the same act sent again under its request id, and the most answers and bytes of
# them kept at once - the oldest go first past either: a robot sends an act again within its own deadline
KEPT_S, KEPT_MOST, KEPT_BYTES = 40.0, 1024, 64 * 2**20
# The codes of a refusal the policy itself gave - it ran, and raised or ran out of time: kept as the act's answer
_RAN = frozenset({"policy_error", "timeout"})
# A robot's stream (GET /stream): how often the server pings the robot, and how long it waits for the pong before it
# lets the stream go - a robot whose network went holds it no longer than that. The robot's own pings, every 0.1 s
# while it is idle, keep it warm.
WS_PING_S = 60.0
WS_PONG_S = 20.0

SERVER_HEADER = "X-Seq-Server"    # what the server says it is, on every response: sequence-ai/<version>
_TEXT = b"text/plain; charset=utf-8"
_JSON = b"application/json"
_SESSION = b"x-seq-session"
_RID = b"x-seq-request-id"
_SERVER = SERVER_HEADER.lower().encode()
# What X-Seq-Act-Formats names on every answer - the platform's own words: the stream's format, and that the policy
# reads each act's newest observation alone, so a robot leaves out a frame a newer one stood behind before it was sent
# (never a video's).
LATEST_FORMAT = "x-seq-latest/1"
_OUTSIDE, _LEFT = (name.lower().encode() for name in (OUTSIDE_HEADER, LEFT_HEADER))
SESSION_MAX = 128          # the longest robot name X-Seq-Session is read as; a longer one names no robot
NOT_SEATED = 503           # the status of an act whose robot has no seat, with why in its body
NOT_SEATED_REASON = "not_seated"   # and the reason the platform's refusal (ErrorBody) names
# A count of seats runs on a thread of its own, and the interpreter passes from it to the event loop every
# COUNT_SWITCH_S while it runs (_count), where Python's own switch interval (5 ms) is set.
# WHY: a count takes from about 5 ms for 2 robots to seconds for 16 and more (engine/slack.py, in_time). In the serving
# stack these rules were taken from, a count on the event loop held every robot's request for as long (33 ms for a
# server that seated 3, 161 ms for 8); on a thread at Python's own interval, the loop's steps were 16 ms apart while it
# ran, and 1.9 ms at 0.2 ms, against 1.3 ms idle.
_PYTHON_SWITCH_S = 0.005
COUNT_SWITCH_S = 0.0002


class _Seat:
    """A robot seated (_Fleet): the round trip its acts last reported (None: none yet), its acts in flight, and when it
    was last heard - its latest act's arrival or answer."""

    __slots__ = ("outside", "acting", "heard")

    def __init__(self, outside: Optional[float], now: float) -> None:
        self.outside, self.acting, self.heard = outside, 0, now


class _Fleet:
    """The robots App schedules by the slack their chunks leave (engine.slack), told how they play an answer: the time
    each batch size takes, as the warm-up timed it and then as served (slack.Table, slack.Served); each robot's
    requests as they arrive and its answers as they leave (slack.Aligner); and the robots seated, each by the round trip
    it reports (slack.Seating), with why a robot is not."""

    def __init__(self, play: "slack.Playback", plays: dict, sizes: list) -> None:
        self.play, self.plays, self.sizes = play, plays, sizes
        self.table, self.served = slack.Table(), slack.Served()
        self.seats: "dict[str, _Seat]" = {}
        self.aligner = slack.Aligner(self.table, play, seated=self.seats.keys, served=self.served)
        self.seating: Optional[slack.Seating] = None       # once the warm-up has timed each size (timed)
        self.capacity: Optional[int] = None                # the seats the latest count gave
        self.gone_s = slack.GONE_PERIODS * play["play_s"]  # how long a robot with no act in flight keeps its seat
        self._lock: Optional[asyncio.Lock] = None
        self._counter = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="sequence_ai-seats")

    def timed(self) -> None:
        """The seating, once the warm-up has timed each listed size: the capacity of this one policy by the rules the
        platform's workers seat robots by, its largest listed size the most robots it seats."""
        play = self.play
        self.seating = slack.Seating(self.table, play["buffer_s"] * 1000.0, sizes=self.sizes, served=self.served,
                                     cycle_ms=(play["play_s"] - play["buffer_s"]) * 1000.0, most=self.sizes[-1],
                                     wait_ms=play["wait_s"] * 1000.0 if "wait_s" in play else None,
                                     step_ms=play["step_s"] * 1000.0)

    async def count(self, robots: list) -> tuple:
        """seating.seat(robots) - (seats, the robots over them) - on the thread counts run on."""
        return await asyncio.get_running_loop().run_in_executor(self._counter, _count, self.seating, robots)

    async def admit(self, robot: str, outside: Optional[float]) -> Optional[str]:
        """None once `robot` is seated - now, or at an earlier act; else why it is not, in words its robot is shown. A
        robot is seated where fewer robots are seated than its largest batch holds and, beside them, it is not over and
        none of them is put over for it: each by its own round trip (Seating.seat, which takes one that reported none
        at slack.ROUND_TRIP_MS), in every start their requests can fall in (slack.in_time).
        WHY each by its own round trip and not first by the seats: the seats count each robot to come at ROUND_TRIP_MS,
        and a robot nearer than that may fit where they leave none. The platform's workers ask the seats as well, as its
        gateway sends robots to them by the seats; a robot reaches serve() by itself."""
        if robot in self.seats:
            return None
        if self._lock is None:
            self._lock = asyncio.Lock()        # made on the loop that serves: Python 3.9 binds a lock to a loop as made
        async with self._lock:                 # one robot's count at a time: two counted at once would both be seated
            if robot in self.seats:
                return None
            self.let_go(time.perf_counter())
            robots = [(name, seat.outside) for name, seat in self.seats.items()]
            seats, over = await self.count(robots)
            self.capacity = seats
            if len(robots) >= self.sizes[-1]:
                return self._full(robots)
            _, beside = await self.count(robots + [(robot, outside)])
            put_out = set(beside) - set(over) - {robot}
            if robot in beside or put_out:
                return self._late(robot, outside, robots, sorted(put_out))
            self.seats[robot] = _Seat(outside, time.perf_counter())
            log.info("seated a robot %s (%d seated, %d seats)",
                     "that has reported no round trip yet" if outside is None else "by the round trip it reported",
                     len(self.seats), seats)
            return None

    def let_go(self, now: float) -> None:
        """The seats of the robots gone: no act of theirs in flight, and none heard for gone_s. No batch waits for them
        from now on (Aligner.left)."""
        for name in [n for n, seat in self.seats.items() if not seat.acting and now - seat.heard > self.gone_s]:
            del self.seats[name]
            self.aligner.left(name)

    def arrived(self, robot: str, entered: float, outside: Optional[float], left: Optional[float]) -> None:
        """An act of seated `robot` that entered the server at `entered` (its last byte), its robot reporting a round
        trip of `outside` ms and `left` ms of the answer it plays."""
        seat, now = self.seats[robot], time.perf_counter()
        seat.acting, seat.heard = seat.acting + 1, now
        if outside is not None:
            seat.outside = outside
        self.aligner.arrived(robot, now, entered=entered, outside_ms=outside, left_ms=left)

    def answered(self, robot: Optional[str], size: int, dispatched: float, model_s: float) -> None:
        """An act answered, its batch of `size` dispatched at `dispatched` and the policy's call `model_s`: its time in
        the server once dispatched into slack.Served, and its robot's answer, leaving now, into the Aligner."""
        now = time.perf_counter()
        self.served.add(size, (now - dispatched) * 1000.0, model_s * 1000.0)
        if robot is not None:
            self.aligner.answered([robot], now)

    def done(self, robot: str) -> None:
        """An act of `robot` answered, or failed: no longer in flight."""
        seat = self.seats.get(robot)
        if seat is not None:
            seat.acting, seat.heard = max(0, seat.acting - 1), time.perf_counter()

    def close(self) -> None:
        self._counter.shutdown(wait=False, cancel_futures=True)

    def _chunk(self) -> str:
        """What a robot's answers must come within, for a refusal."""
        if "wait_s" in self.play:
            return f"the {self.play['wait_s'] * 1000:.0f} ms a robot waits for an answer"
        plays = self.plays
        return (f"the {self.play['buffer_s'] * 1000:.0f} ms left of each answer as a robot asks for the next "
                f"({plays['action_chunk_valid_len'] - plays['action_chunk_replan_at']} of "
                f"{plays['action_chunk_valid_len']} steps at {plays['hz']:g} Hz)")

    def _batches(self) -> str:
        """What each listed batch size takes here, for a refusal."""
        sizes = [n for n in self.sizes if self.served.post_ms(n, self.table) is not None]
        said = ", ".join(f"{n}: {self.served.post_ms(n, self.table):.0f} ms" for n in sizes)
        return f"a batch takes {said} here"

    def _again(self) -> str:
        return f"a robot gives its place up {self.gone_s:.0f} s after its last act"

    def _full(self, robots: list) -> str:
        return (f"this server already serves {_robots(len(robots))}, as many as its largest batch holds "
                f"({self.sizes[-1]}). Serve this robot from another GPU, or act again once one of them has stopped: "
                f"{self._again()}")

    def _late(self, robot: str, outside: Optional[float], robots: list, put_out: list) -> str:
        """Why `robot` is not seated, in words its robot is shown: by the round trip it reports, or a default one where
        it reported none, each said without a number."""
        away = ("at the round trip it reports" if outside is not None else
                "at a default round trip, having reported none")
        if put_out:
            n = len(put_out)
            why = (f"seated beside the {_robots(len(robots))} it serves, this robot, {away}, would leave "
                   f"{'one of them' if n == 1 else f'{n} of them'} without {'its' if n == 1 else 'their'} answers "
                   f"within {self._chunk()}")
        else:
            why = (f"this server cannot answer this robot within {self._chunk()} beside the {_robots(len(robots))} it "
                   f"serves, however their requests fall, with this robot {away}")
        return (f"{why} ({self._batches()}). Serve it from a GPU nearer it, or from this one once the others have "
                f"stopped: {self._again()}")


def _robots(n: int) -> str:
    return f"{n} robot" if n == 1 else f"{n} robots"


def _count(seating: "slack.Seating", robots: list) -> tuple:
    """seating.seat(robots), on the thread counts run on, the interpreter passing to the event loop every COUNT_SWITCH_S
    while it runs - where Python's own interval is set; one something else set stays as it set it."""
    was = sys.getswitchinterval()
    ours = abs(was - _PYTHON_SWITCH_S) < 1e-9
    if ours:
        sys.setswitchinterval(COUNT_SWITCH_S)
    try:
        return seating.seat(robots)
    finally:
        if ours:
            sys.setswitchinterval(was)


def _plays(hz: Any, valid: Any, replan_at: Any, wait_s: Any) -> Optional[tuple]:
    """(slack.playback's playback, what /ping says of it - @seq.policy's declarations, by their names) for how a robot
    plays an answer: its hz, action_chunk_valid_len, action_chunk_replan_at and max_wait_for_batch; None when none is
    given. ValueError for numbers that do not say it."""
    if hz is None and valid is None and replan_at is None and wait_s is None:
        return None
    whole = [n for n in (valid, replan_at) if n is not None]
    play = slack.playback(hz, valid, replan_at, wait_s)
    if (play is None or any(not isinstance(n, int) or isinstance(n, bool) or n < 1 for n in whole)
            or (wait_s is not None and "wait_s" not in play)):
        raise ValueError(f"serve() times each robot by how it plays an answer: hz, the steps it plays a second "
                         f"(above 0, up to 1000), and action_chunk_valid_len, the steps of an answer it may play, or "
                         f"action_chunk_replan_at, the step at which it asks for the next (whole numbers, 1 or more); "
                         f"max_wait_for_batch, if given, how long it waits for an answer (above 0, up to "
                         f"{slack.WAIT_MAX_S:g} s). It was given hz={hz!r}, action_chunk_valid_len={valid!r}, "
                         f"action_chunk_replan_at={replan_at!r}, max_wait_for_batch={wait_s!r}")
    valid = valid if valid is not None else replan_at
    plays = {"hz": float(hz), "action_chunk_valid_len": valid,
             "action_chunk_replan_at": min(replan_at, valid) if replan_at else valid}
    if wait_s is not None:
        plays["max_wait_for_batch"] = float(wait_s)
    return play, plays


def _refusal(refused: Any) -> tuple:
    """A refusal as an answer to send: (status, its ErrorBody, JSON, Retry-After where it says when to ask again)."""
    extra = [(b"retry-after", str(max(1, int(-(-refused.retry_after_s // 1)))).encode())] \
        if refused.retry_after_s is not None else []
    return refused.status, refused.body(), _JSON, extra


def _sender(scope) -> Optional[tuple]:
    """Who sent an act, as its answer is kept for: its request id (X-Seq-Request-Id), its robot (X-Seq-Session) and
    what it was authorized with - None for an act that names no request id, which runs each time it is sent."""
    rid = _header(scope, _RID).decode("latin-1").strip()
    if not rid or len(rid) > SESSION_MAX:
        return None
    return rid, _header(scope, _SESSION).decode("latin-1").strip(), _header(scope, b"authorization")


def _policy_gave(answer: tuple) -> bool:
    """Whether an act's answer is the policy's own - an answer, or its failure (_RAN) - and not a refusal before it ran,
    which the robot acts on and sends the act again after."""
    status, payload, content_type = answer[:3]
    if 200 <= status < 300:
        return True
    try:
        return content_type == _JSON and json.loads(payload).get("code") in _RAN
    except (ValueError, AttributeError):
        return False


class _Kept:
    """The answers acts were given, by who sent each (_sender), kept KEPT_S after each - the oldest go first past
    KEPT_MOST answers or KEPT_BYTES of them."""

    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._answers: "collections.OrderedDict[tuple, tuple]" = collections.OrderedDict()   # sender -> (until, answer)
        self._bytes = 0

    def keep(self, sender: tuple, answer: tuple) -> None:
        self._expire()
        old = self._answers.pop(sender, None)
        if old is not None:
            self._bytes -= len(old[1][1])
        self._answers[sender] = (self._clock() + KEPT_S, answer)
        self._bytes += len(answer[1])
        while self._answers and (len(self._answers) > KEPT_MOST or self._bytes > KEPT_BYTES):
            self._bytes -= len(self._answers.popitem(last=False)[1][1][1])

    def get(self, sender: tuple) -> Optional[tuple]:
        self._expire()
        kept = self._answers.get(sender)
        return None if kept is None else kept[1]

    def answered(self, rid: str) -> bool:
        """Whether an act sent under request id `rid` was answered, its answer still kept."""
        self._expire()
        return any(sender[0] == rid for sender in self._answers)

    def _expire(self) -> None:
        now = self._clock()
        while self._answers and next(iter(self._answers.values()))[0] <= now:
            self._bytes -= len(self._answers.popitem(last=False)[1][1][1])


def _act_asked(scope) -> Optional[str]:
    """The request id a /ping asks after (/ping?act=<id>, worker_transport.act_running): None where it asks after none,
    or names one longer than SESSION_MAX."""
    asked = urllib.parse.parse_qs((scope.get("query_string") or b"").decode("latin-1")).get("act")
    rid = asked[0].strip() if asked else ""
    return rid if 0 < len(rid) <= SESSION_MAX else None


def _robot(scope) -> Optional[str]:
    """The robot an act names (SESSION_HEADER): None for none, or for a name longer than SESSION_MAX."""
    name = _header(scope, _SESSION).decode("latin-1").strip()
    return name if 0 < len(name) <= SESSION_MAX else None


class App:
    """
    The ASGI app serve() runs (the module's docstring has what each part does): GET /stream, POST /observe, POST /act,
    POST /act/episode_end, GET /ping, GET /example, GET /record. The policy is warmed up when the server starts (its
    lifespan) or, with no lifespan, at the first request. ImportError where sequence-base is not installed.

    policy     a function: an observation in, the response's value out. With `batch`, a function from a list of
               observations to a list of outputs, one for each, in order
    batch      None: one observation per call. A list of sizes, 1 among them: the observations waiting are passed as
               a list of the largest listed size they fill (engine.batcher), none held back for more unless `hz` says
               how long each robot can wait
    token      requests must carry Authorization: Bearer <token>; None or "": no token is asked for
    example    an observation: the warm-up runs the policy on it, and GET /example hands it out
    limit      the most bytes a request's body, or a message of a robot's stream, may hold
    record     whether it keeps the last minute of the robots' steps in memory for a recorder to read as they come
               (GET /record: engine.recorder)
    examples   observations the speed-ups are checked on during the warm-up (engine.optimize); `example` alone when
               none are given, and the first of them is `example` when it is not
    cuda_graphs, whole_graph   None: tried on a PyTorch policy, not a JAX one; True: tried; False: not
               (engine.optimize)
    torch_compile, fused_kernels, tensorrt, precision, tolerance   the speed-ups that change the outputs, tried with
               the `tolerance` given (engine.optimize); ValueError at once when one is on without it
    copy       the copy of the policy each episode's frames go to (engine.episodes.PolicyCopy, a @seq.policy class's:
               its episodes, observe function, on_episode and plans), handed this server's policy thread; None: one
               that keeps each episode's newest observation
    hz, action_chunk_valid_len, action_chunk_replan_at, max_wait_for_batch
               how a robot plays an answer, as @seq.policy declares it: each robot's acts are held and its robots
               seated by it (the module's docstring), with `example` to time the batches. max_wait_for_batch: how long
               a robot waits for an answer at most, in seconds from when it sent its act, which it is held and seated
               by instead
    """

    def __init__(self, policy: Callable[[Any], Any], *, batch: Optional[Iterable[int]] = None,
                 token: Optional[str] = None, example: Any = None, limit: int = LIMIT, record: bool = True,
                 copy: Any = None, hz: Optional[float] = None, action_chunk_valid_len: Optional[int] = None,
                 action_chunk_replan_at: Optional[int] = None, max_wait_for_batch: Optional[float] = None,
                 examples: Optional[list] = None, cuda_graphs: Optional[bool] = None,
                 whole_graph: Optional[bool] = None, torch_compile: bool = False, fused_kernels: bool = False,
                 tensorrt: bool = False, precision: Optional[str] = None, tolerance: Any = None,
                 cfg_parallel: bool = False, pipeline_parallel: bool = False) -> None:
        if not callable(policy):
            hint = ": an object with an infer method is served as policy.infer" if hasattr(policy, "infer") else ""
            raise TypeError(f"serve() takes the policy as a function, an observation in and its output out; it was "
                            f"given a {type(policy).__name__}{hint}")
        if inspect.iscoroutinefunction(policy) or inspect.iscoroutinefunction(type(policy).__call__):
            raise TypeError("the policy is an async function: serve() calls it on a thread of its own, so pass a plain "
                            "function")
        self._policy = policy
        self._sizes = None if batch is None else sorted({int(n) for n in batch})
        if self._sizes is not None and self._sizes[0] < 1:
            raise ValueError(f"batch sizes {self._sizes}: each is a number of observations, 1 or more")
        played = _plays(hz, action_chunk_valid_len, action_chunk_replan_at, max_wait_for_batch)
        if played is not None and example is None:
            raise ValueError("serve() holds and seats robots by the time a batch of each size takes, which its warm-up "
                             "times on the example: pass example=, an observation as a robot sends it")
        # the robots it schedules by their answers' slack: with hz (and action_chunk_valid_len or _replan_at), else None
        self._fleet = None if played is None else _Fleet(*played, sizes=list(self._sizes or (1,)))
        # how its robots play an answer, said on /ping where it seats none by it: what its copy's policy declares (seq
        # serve of a policy with no @seq.sample to time its batches on), which its robots' Policy reads its hz and
        # chunk from - the declarations as serve() takes them, or none where they say no playback
        self._play_said: Optional[dict] = None
        if self._fleet is None and copy is not None:
            declared = getattr(copy, "plays", None) or {}
            try:
                given = _plays(declared.get("hz"), declared.get("action_chunk_valid_len"),
                               declared.get("action_chunk_replan_at"), declared.get("max_wait_for_batch"))
            except ValueError:
                given = None
            self._play_said = given[1] if given else None
        # which of the two said how many steps of an answer a robot plays, for the warm-up's check of the answer
        self._steps_named = "action_chunk_valid_len" if action_chunk_valid_len is not None else "action_chunk_replan_at"
        hold = first = None
        if self._fleet is not None:
            aligner, sizes = self._fleet.aligner, list(self._sizes or (1,))
            hold = lambda keys: aligner.hold_s(keys, time.perf_counter())                       # noqa: E731
            first = lambda keys, free: aligner.split(keys, time.perf_counter(), sizes, free)    # noqa: E731
        # without a robot's time no act waits for another: the batch is what waited while the policy ran
        self._batcher = Batcher(self._run, sizes=self._sizes or (1,), wait_ms=0.0, runners=1, hold=hold,
                                first=first)
        self._token = token.encode() if token else None
        self._limit = int(limit)
        if example is None and examples:
            example = examples[0]
        self._example_body = None if example is None else msgpack_io.pack(example)
        # what the warm-up checks the speed-ups on, and which it tries (engine.optimize); what it kept, for /ping
        self._examples = [example] if example is not None and not examples else list(examples or [])
        from .optimize import check_switches  # a switch that changes the outputs, without a tolerance: said now

        self._speedups = check_switches(cuda_graphs=cuda_graphs, whole_graph=whole_graph, torch_compile=torch_compile,
                                        fused_kernels=fused_kernels, tensorrt=tensorrt, precision=precision,
                                        tolerance=tolerance, cfg_parallel=cfg_parallel,
                                        pipeline_parallel=pipeline_parallel)
        self._cfg_patches: list = []       # cfg_parallel's, put in place on this rank (engine.cfg_parallel)
        # pipeline_parallel's split of this rank's policy and what it was made from (engine.pipeline_parallel)
        self._pp_split: Any = None
        self._pp_spec: Optional[dict] = None
        self._trying = self._speedups["precision"] is not None or any(
            self._speedups[name] or self._speedups[name] is None
            for name in ("cuda_graphs", "whole_graph", "torch_compile", "fused_kernels", "tensorrt"))
        self.optimized: dict = {"on": []}
        # each robot's observations as they are made and its acts after them, on its stream - the platform's data
        # plane (engine.data_plane); the robots' steps for whoever records them, the last minute in memory
        # (engine.recorder)
        self._plane = _data_plane(copy)
        self._window = _record.Window() if record else None
        if self._window is not None:
            self._plane.copy.on_frame = lambda episode, seq, frame: self._window.observe(
                self._robots.get(episode, ""), episode, seq, frame)
        self._robots: "collections.OrderedDict[str, str]" = collections.OrderedDict()   # episode -> its robot's session
        # each act running by who sent it (_sender), and the answers acts were given (_Kept): an act runs once
        self._running: dict = {}
        self._running_began: dict = {}           # when each began, for a robot that asks after it (/ping?act=)
        self._kept = _Kept()
        self._formats = f"{STREAM_FORMAT}, {LATEST_FORMAT}".encode()
        self._intake = StreamIntake(self._http, headers=self._stream_headers, authorized=self._may_open,
                                    carried=(b"authorization", b"x-seq-session", b"user-agent", b"host"))
        # what it says it is, on every response (SERVER_HEADER) and, at more length, in its ping's answer
        self._version, self._began = _version(), time.monotonic()
        self._name = getattr(policy, "__qualname__", None) or type(policy).__name__
        self._identity = f"sequence-ai/{self._version}".encode()
        self._thread = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="sequence_ai-policy")
        # one rank of several, where a launcher started this process so (engine.ranks: WORLD_SIZE, RANK): every call of
        # the policy goes to every rank; rank 0 serves robots, each other rank follows it (serve()). None: alone
        self._group = _ranks.from_env()
        # a copy of the policy's own (engine.episodes.PolicyCopy) runs every call of the policy's code on this thread
        if hasattr(self._plane.copy, "attach"):
            self._plane.copy.attach(self._thread)
        # what a copy of the policy's own runs of its code beside its acts (its observe function, on_episode): on rank
        # 0, sent to every rank before it runs (engine.ranks.Mirrored); on any other rank, run as rank 0 sends it
        self._mirrored: dict = {}
        self._wire = self._unwire = lambda items: items
        if self._group is not None and copy is not None:
            self._mirrored = copy.mirrored()
            self._wire, self._unwire = copy.wire, copy.unwire
            if self._group.leads:
                copy.attach(_ranks.Mirrored(self._thread, self._group, self._mirrored))
        # "starting" until the server starts, "warming" while the policy runs on the example, then "ready" or "failed"
        self._state = "starting"
        self._warming: Optional[asyncio.Future] = None
        self.failure: Optional[BaseException] = None      # what the policy raised on the example, if it did
        self.on_failure: Optional[Callable[[], None]] = None

    @property
    def ready(self) -> bool:
        """Whether /ping says 200: the server has started and the warm-up, if any, is done."""
        return self._state == "ready"

    # ── the policy, on its own thread ────────────────────────────────────────────────────────────────────────────────
    def _call(self, items: list) -> list:
        """On the policy's thread: the policy's outputs for `items`, each with arrays of other libraries as numpy
        arrays, and how long that took, as [(output, seconds)] - on rank 0 of a group, `items` sent to every rank first,
        each rank's policy called on them, and rank 0's outputs (engine.ranks: GroupHalted where a rank failed it)."""
        if self._group is None:
            return self._call_here(items)
        return self._group.run("call", [self._wire(items)], lambda: self._call_here(items))

    def _call_here(self, items: list) -> list:
        """_call, on this process's policy alone - rank 0's own part, and each other rank's when rank 0 sends it."""
        started = time.perf_counter()
        if self._pp_split is not None:
            self._pp_split.begin()             # a new act: its first call of the blocks runs whole, on every rank
        if self._sizes is None:
            outputs = [self._policy(items[0])]
        else:
            got = self._policy(items)
            if isinstance(got, dict) or not hasattr(got, "__len__"):
                raise TypeError(f"the batch function returned a {type(got).__name__} for a batch of {len(items)}: it "
                                "returns a list, one output for each observation, in order")
            outputs = list(got)
            if len(outputs) != len(items):
                raise ValueError(f"the batch function returned {len(outputs)} outputs for a batch of {len(items)}: "
                                 "one output for each observation, in order")
        outputs = [_numpy(output) for output in outputs]
        took = time.perf_counter() - started
        return [(output, took) for output in outputs]

    async def _run(self, items: list) -> list:
        """The batcher's call: each item's (output, the policy's seconds, when its batch was dispatched, its size), the
        forward pass into the times robots are held and seated by."""
        dispatched = time.perf_counter()
        answered = await asyncio.get_running_loop().run_in_executor(self._thread, self._call, items)
        if self._fleet is not None:
            self._fleet.table.add(len(items), answered[0][1] * 1000.0)
        return [(output, took, dispatched, len(items)) for output, took in answered]

    def _start(self) -> None:
        if self._state != "starting":
            return
        if self._example_body is None:
            log.warning(NO_EXAMPLE)
        if self._group is not None:
            self._group.listen()                         # rank 0: the other ranks join it as they come up
        elif self._example_body is None:
            self._state = "ready"
            return
        self._state = "warming"
        self._warming = asyncio.ensure_future(self._warm_up())

    async def _warm_up(self) -> None:
        """Every rank of a group joined first, where this is rank 0 of one; then the policy on the example, twice at
        each batch size: the first call compiles what it compiles, the second shows the time it settles at. The example
        reaches it as a robot's observation does: read back from msgpack."""
        loop = asyncio.get_running_loop()
        if self._group is not None:
            try:
                await loop.run_in_executor(None, self._group.wait_joined)
            except _ranks.GroupHalted as e:
                self._fail(e)
                return
            log.info("every rank joined: %d of %d", self._group.joined(), self._group.size)
        if self._example_body is None:
            self._state = "ready"
            log.info("ready")
            return
        example = _own(msgpack_io.unpack(self._example_body))
        if self._trying and self._group is None:   # a group's ranks serve the policy as it is: a trial
            # runs it on rank 0 alone, where a model that exchanges with its other ranks would wait for them
            try:   # the speed-ups first, so the warm-up below runs, and times, what the robots will be served
                examples = [_own(msgpack_io.unpack(msgpack_io.pack(observation))) for observation in self._examples]
                self.optimized = await loop.run_in_executor(self._thread, self._optimize, examples)
            except Exception as e:  # noqa: BLE001 (the policy raised on an example in eager mode, as it would below)
                self._fail(e)
                return
        if self._speedups["cfg_parallel"]:         # its trial runs every call and every toggle on every rank
            try:
                examples = [_own(msgpack_io.unpack(msgpack_io.pack(observation))) for observation in self._examples]
                tried = await loop.run_in_executor(self._thread, split_trials.cfg_trial, self, examples)
            except Exception as e:  # noqa: BLE001 (the policy raised on an example in eager mode, or a rank left)
                self._fail(e)
                return
            self.optimized = _with_tried(self.optimized, tried)
        if self._speedups["pipeline_parallel"]:    # its trial too: every call and every toggle on every rank
            try:
                examples = [_own(msgpack_io.unpack(msgpack_io.pack(observation))) for observation in self._examples]
                tried = await loop.run_in_executor(self._thread, split_trials.pp_trial, self, examples)
            except Exception as e:  # noqa: BLE001 (the policy raised on an example in eager mode, or a rank left)
                self._fail(e)
                return
            self.optimized = _with_tried(self.optimized, tried)
        runs = 2 if self._fleet is None else 1 + slack.RUNS       # timed as slack.measure times a size
        try:
            for n in self._sizes or [1]:
                took, forward = [], []
                for _ in range(runs):
                    started = time.perf_counter()
                    answered = await loop.run_in_executor(self._thread, self._call, [example] * n)
                    for output, _ in answered:
                        msgpack_io.pack(output)       # an output that cannot be sent fails here, not at a robot
                    took.append(time.perf_counter() - started)
                    forward.append(answered[0][1])
                what = "one observation" if self._sizes is None else f"a batch of {n}"
                if self._fleet is None:
                    log.info("warm-up: %s took %s, then %s", what, _duration(took[0]), _duration(took[1]))
                else:
                    self._fleet.table.first_ms[n] = forward[0] * 1000.0
                    for seconds in forward[1:]:
                        self._fleet.table.add(n, seconds * 1000.0)
                    log.info("warm-up: %s took %s, then %s at the median of %d", what, _duration(took[0]),
                             _duration(sorted(took[1:])[len(took[1:]) // 2]), len(took) - 1)
            if self._fleet is not None:
                self._say_short(answered[0][0])
                self._fleet.timed()
                seats, _ = await self._fleet.count([])
                self._fleet.capacity = seats
                log.info("seats %d robot%s at a default round trip, then each robot by the round trip it reports",
                         seats, "" if seats == 1 else "s")
        except Exception as e:  # noqa: BLE001 (whatever the policy raised: serve() raises it once the server stops)
            self._fail(e)
            return
        self._state = "ready"
        log.info("ready")

    def _say_short(self, output: Any) -> None:
        """A warning where the policy's answer to the example holds fewer steps than its robots are timed to play of
        each answer (action_chunk_valid_len, else action_chunk_replan_at): each robot would run out of steps before its
        next answer comes, and the warm-up would say ready all the same. Its steps are as network.loop.steps reads them;
        an answer it cannot read them from is not checked."""
        try:
            rows = len(_steps(output))
        except (TypeError, ValueError):
            return
        steps = self._fleet.plays["action_chunk_valid_len"]
        if rows >= steps:
            return
        declared = (f"the {steps} it declares valid (action_chunk_valid_len)"
                    if self._steps_named == "action_chunk_valid_len"
                    else f"the {steps} it plays before asking for the next (action_chunk_replan_at)")
        log.warning("the policy answers %d step%s, fewer than %s: its robots run out of steps before the next answer "
                    "comes", rows, "" if rows == 1 else "s", declared)

    def _optimize(self, examples: list) -> dict:
        """On the policy's thread: the speed-ups tried on `examples`, each read back from msgpack as a robot's
        observation is (engine.optimize), and its report. A copy of a @seq.policy class's (engine.episodes.PolicyCopy)
        names the call they are tried on, `checked`: its policy's act function called directly, as the platform tries
        a version's. Its own call holds the policy further down than optimize looks for the policy's modules; they are
        changed in place, so that call then serves what was kept."""
        from .optimize import optimize

        speedups = {name: value for name, value in self._speedups.items()
                    if name not in ("cfg_parallel", "pipeline_parallel")}
        said = optimize(self._checked(), examples, batch=self._sizes, say=lambda line: log.info("%s", line),
                        **speedups)
        return said.report

    def _checked(self) -> Any:
        """What the speed-ups look for the policy's modules in: the copy's call where it names one (`checked`), and a
        policy served with no copy of a class's: the policy itself."""
        return getattr(self._plane.copy, "checked", None) or self._policy

    def _fail(self, e: BaseException) -> None:
        self.failure = e
        self._state = "failed"
        if isinstance(e, _ranks.GroupHalted):
            log.error("the ranks of this server did not come together (%s): stopping", e)
        else:
            log.error("the policy failed on the example (%s): stopping", _said(e))
        if self.on_failure is not None:
            self.on_failure()

    def close(self) -> None:
        """Stop the warm-up and the policy's thread; a call in progress finishes on it."""
        if self._warming is not None and not self._warming.done():
            self._warming.cancel()
        self._plane.close()
        self._thread.shutdown(wait=False, cancel_futures=True)
        if self._fleet is not None:
            self._fleet.close()
        if self._group is not None and self._group.leads:
            self._group.close()                          # each rank told the server stopped: it returns from serve()

    # ── HTTP ──────────────────────────────────────────────────────────────────────────────────────────────────────────
    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] == "lifespan":
            await self._lifespan(receive, send)
            return
        if scope["type"] == "websocket" and self._window is not None and scope.get("path") == _record.PATH:
            await _record.serve_recorder(scope, receive, send, self._window, self._may_open)
            return
        if scope["type"] == "websocket":
            self._start()
            await self._intake(scope, receive, send)     # GET /stream: each message served as a request (_http)
            return
        await self._http(scope, receive, send)

    def _may_open(self, scope) -> bool:
        """Whether a WebSocket's upgrade carries the token, where the server asks for one."""
        return self._token is None or self._authorized(scope)

    def _stream_headers(self) -> list:
        """What the answer that opens a robot's stream carries: the stream's format - and that the policy reads each
        act's newest observation alone, so a robot leaves out a frame a newer one stood behind - beside what every
        answer carries."""
        return [(b"x-seq-act-formats", self._formats), (_SERVER, self._identity)]

    async def _http(self, scope, receive, send) -> None:
        """Every request - over HTTP, or carried by a robot's stream (StreamIntake) - by its path."""
        if scope["type"] == "websocket":                 # a WebSocket at any other path: refused (403)
            if (await receive()).get("type") == "websocket.connect":
                await send({"type": "websocket.close", "code": 1008})
            return
        if scope["type"] != "http":
            return
        self._start()
        path, method = scope["path"], scope["method"]
        if self._token is not None and not self._authorized(scope):
            await self._respond(send, 401, b"this server needs its token: Authorization: Bearer <token>",
                                extra=[(b"www-authenticate", b"Bearer")])
        elif path == "/act":
            if method == "POST":
                await self._act(scope, receive, send)
            else:
                await self._respond(send, 405, b"POST /act", extra=[(b"allow", b"POST")])
        elif path == "/ping":
            if method in ("GET", "HEAD"):
                await self._ping(scope, send)
            else:
                await self._respond(send, 405, b"GET /ping", extra=[(b"allow", b"GET, HEAD")])
        elif path == "/observe":
            if method == "POST":
                await self._observe(scope, receive, send)
            else:
                await self._respond(send, 405, b"POST /observe", extra=[(b"allow", b"POST")])
        elif path == "/act/episode_end":
            if method == "POST":
                await self._episode_end(scope, receive, send)
            else:
                await self._respond(send, 405, b"POST /act/episode_end", extra=[(b"allow", b"POST")])
        elif path == "/example":
            if method != "GET":
                await self._respond(send, 405, b"GET /example", extra=[(b"allow", b"GET")])
            elif self._example_body is None:
                await self._respond(send, 404, b"no example: this server was started without one (serve(example=...))")
            else:
                await self._respond(send, 200, self._example_body, content_type=msgpack_io.MEDIA_TYPE.encode())
        else:
            await self._respond(send, 404, b"this server answers GET /stream, POST /observe, POST /act, "
                                           b"POST /act/episode_end, GET /ping and GET /example")

    async def _lifespan(self, receive, send) -> None:
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                self._start()
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                self.close()
                await send({"type": "lifespan.shutdown.complete"})
                return

    def _authorized(self, scope) -> bool:
        scheme, _, credential = _header(scope, b"authorization").partition(b" ")
        return scheme.lower() == b"bearer" and hmac.compare_digest(credential.strip(), self._token or b"")

    async def _ping(self, scope, send) -> None:
        if self._group is not None and self._group.halted is not None and self._state == "ready":
            await self._respond(send, 500, f"this server's ranks serve no more: {self._group.halted}".encode())
        elif self._state == "ready":
            said = {"server": "sequence-ai", "version": self._version, "up_s": round(time.monotonic() - self._began, 1),
                    "pid": os.getpid(), "policy": self._name,
                    "optimized": list(self.optimized.get("on") or [])}
            if self._fleet is not None:
                # how its robots play an answer, which a robot's Policy counts what is left of one by; the robots
                # seated against the seats the latest count gave; and what a batch of each size takes here, which
                # robots are seated and held by
                fleet = self._fleet
                fleet.let_go(time.perf_counter())
                said.update(play=fleet.plays, robots=len(fleet.seats), seats=fleet.capacity,
                            batch_ms={str(n): round(ms, 1) for n in fleet.sizes
                                      if (ms := fleet.served.post_ms(n, fleet.table)) is not None})
            elif self._play_said:
                # how its robots play an answer where it seats none by it: its policy's declarations, which a robot's
                # Policy reads its hz and chunk from and holds its answers to (late.py)
                said["play"] = dict(self._play_said)
            asked = _act_asked(scope)
            if asked is not None:
                said["act"] = self._act_said(asked)
            await self._respond(send, 200, json.dumps(said).encode(), content_type=b"application/json")
        elif self._state == "failed":
            await self._respond(send, 500, f"the policy failed on the example: {_said(self.failure)}".encode())
        elif self._group is not None and self._group.joined() < self._group.size:
            await self._respond(send, 503, f"waiting for its ranks: {self._group.joined()} of {self._group.size} "
                                           f"joined".encode(), extra=[(b"retry-after", str(RETRY_AFTER_S).encode())])
        else:
            await self._respond(send, 503, b"warming up: the policy is running on the example",
                                extra=[(b"retry-after", str(RETRY_AFTER_S).encode())])

    async def _act(self, scope, receive, send) -> None:
        declared = _header(scope, b"content-length")
        if declared.isdigit() and int(declared) > self._limit:
            await self._too_large(send)
            return
        body = await _body(receive, self._limit)
        if body is None:
            await self._too_large(send)
            return
        await self._act_call(scope, send, body, time.perf_counter(), self._said(scope))

    def _said(self, scope) -> Optional[tuple]:
        """What an act says of its robot, where robots are scheduled: (its name, its round trip in ms, what is left of
        the answer it plays in ms), each None where it says none; None for an act that names no robot."""
        if self._fleet is None:
            return None
        robot = _robot(scope)
        if robot is None:
            return None
        return (robot, slack.outside_ms(_header(scope, _OUTSIDE).decode("latin-1")),
                slack.left_ms(_header(scope, _LEFT).decode("latin-1")))

    # ── a robot's stream: its observations as they are made, and the acts after them ─────────────────────────────────
    async def _observe(self, scope, receive, send) -> None:
        """POST /observe: a post of one episode's observations kept and forwarded (engine.data_plane), answered
        {"through": how far its episode is whole} - or the platform's refusal (ErrorBody)."""
        declared = _header(scope, b"content-length")
        if declared.isdigit() and int(declared) > self._limit:
            await self._too_large(send)
            return
        body = await _body(receive, self._limit)
        if body is None:
            await self._too_large(send)
            return
        kind = _header(scope, b"content-type").split(b";")[0].strip().lower().decode("latin-1")
        try:
            through = await self._plane.observe(body, kind)
        except _Refused as e:
            await self._refuse(send, e)
            return
        await self._respond(send, 200, json.dumps({"through": through}).encode(), content_type=_JSON)

    async def _act_call(self, scope, send, body: bytes, began: float, said: Optional[tuple] = None) -> None:
        """The platform's act (POST /act, JSON): {"call": "act", "episode_id", "seq"} - the policy on its episode's
        newest observation once the `seq` before it are in; answered {"outputs": what the policy returned}, in msgpack
        where the robot asks for it (Accept), else JSON - or the platform's refusal (ErrorBody). `said`: what the act
        says of its robot (_said), which is seated - or refused unavailable for NOT_SEATED_REASON, with why - before the
        act waits for its observation. An act that names its request id runs once (_sender): the same act again - on
        another of the robot's lines, or sent again after its answer was lost - is handed the first's answer, waiting
        for it while it runs, and for KEPT_S after (_Kept)."""
        sender = _sender(scope)
        if sender is None:
            await self._send_answer(send, await self._act_answer(scope, body, began, said))
            return
        run = self._running.get(sender)
        if run is None:
            kept = self._kept.get(sender)
            if kept is not None:
                await self._send_answer(send, kept)
                return
            # a task of its own: it runs on - and the same act sent again is still handed its answer - when this
            # request's client goes before it ends
            run = asyncio.ensure_future(self._act_answer(scope, body, began, said))
            self._running[sender] = run
            self._running_began[sender] = time.monotonic()
            run.add_done_callback(lambda done: self._ran(sender, done))
        await self._send_answer(send, await asyncio.shield(run))

    def _act_said(self, rid: str) -> dict:
        """What /ping?act=<rid> says of the act sent under that request id (X-Seq-Request-Id), as a platform worker
        says it: running, and for how long; else not running, and whether it was answered - so a robot whose act
        outlived its bound is told it still runs here, rather than sending it again (worker_transport.act_running)."""
        began = [at for sender, at in list(self._running_began.items()) if sender[0] == rid]
        if began:
            return {"running": True, "for_s": round(time.monotonic() - min(began), 1)}
        return {"running": False, "answered": self._kept.answered(rid)}

    def _ran(self, sender: tuple, run: "asyncio.Future") -> None:
        """An act's run ended: no longer running, and its answer kept for the same act sent again where the policy gave
        it (_policy_gave)."""
        if self._running.get(sender) is run:
            del self._running[sender]
            self._running_began.pop(sender, None)
        if not run.cancelled() and run.exception() is None and _policy_gave(run.result()):
            self._kept.keep(sender, run.result())

    async def _send_answer(self, send, answer: tuple) -> None:
        status, payload, content_type, extra = answer
        await self._respond(send, status, payload, content_type=content_type, extra=extra)

    async def _act_answer(self, scope, body: bytes, began: float, said: Optional[tuple]) -> tuple:
        """_act_call's answer to one act, as (status, body, its content type, the headers it adds)."""
        try:
            call = json.loads(body)
            if not isinstance(call, dict):
                raise ValueError("an act's body is a JSON object")
        except ValueError as e:
            return _refusal(_Refused("INVALID_REQUEST", f"the act does not read: {e}", details={"reason": "body"}))
        episode = call.get("episode_id")
        robot = _header(scope, _SESSION).decode("latin-1")
        if self._group is not None and self._group.halted is not None:   # no rank answers alone: said before it waits
            return _refusal(_Refused("UNAVAILABLE", f"this server's ranks serve no more: {self._group.halted}",
                                     details={"reason": "crashed"}))
        if said is not None:
            refused = await self._fleet.admit(said[0], said[1])
            if refused is not None:
                return _refusal(_Refused("UNAVAILABLE", refused, details={"reason": NOT_SEATED_REASON}))
        try:
            if call.get("call") == "act" and "inputs" not in call:     # the call alone, as the platform's worker
                observation = _own(await self._plane.act(episode, call.get("seq")))
                if isinstance(episode, str) and robot:
                    self._robots[episode] = robot
                    while len(self._robots) > 1024:
                        self._robots.popitem(last=False)
            else:
                raise _Refused("INVALID_REQUEST", 'an act\'s body is {"call": "act", "episode_id", "seq"}: it '
                               "carries no data, which goes by POST /observe", details={"reason": "call"})
        except _Refused as e:
            return _refusal(e)
        wants = msgpack_io.MEDIA_TYPE.encode() in _header(scope, b"accept").lower()
        status, payload, content_type = await self._policy_on(
            observation, robot=robot, episode=episode if isinstance(episode, str) else None, step=call.get("seq"),
            binary=wants, began=began, said=said)
        return status, payload, content_type, ()

    async def _episode_end(self, scope, receive, send) -> None:
        """POST /act/episode_end {"episode_id"}: everything kept of the episode goes - {"ok": true, "episode_id"}."""
        body = await _body(receive, self._limit)
        try:
            episode = json.loads(body or b"{}").get("episode_id")
        except (ValueError, AttributeError):
            episode = None
        try:
            self._plane.end(episode)
        except _Refused as e:
            await self._refuse(send, e)
            return
        self._robots.pop(episode, None)
        await self._respond(send, 200, json.dumps({"ok": True, "episode_id": episode}).encode(), content_type=_JSON)

    async def _refuse(self, send, refused: Any) -> None:
        await self._send_answer(send, _refusal(refused))

    async def _policy_on(self, observation: Any, *, robot: str = "", episode: Optional[str] = None,
                         step: Optional[int] = None, binary: bool = True,
                         began: Optional[float] = None, said: Optional[tuple] = None) -> tuple:
        """The platform's answer to one act, (status, body, its content type): {"outputs": what the policy returned,
        "perf": {"handler_ms" - from the act's last byte (`began`) to its answer, which the robot takes off its round
        trip -, "inference_ms"}}, in msgpack with `binary`, else JSON - or the platform's refusal (ErrorBody). Kept for
        the recorders (engine.recorder) as an act of `robot`'s answered from the observation `step` of `episode` (None:
        one it carried). `said`: what the act says of a robot seated (_said): its act held for others only as long as
        the answer it plays leaves it (slack.Aligner), from `began`."""
        name = None if said is None else said[0]
        if name is not None:
            self._fleet.arrived(name, time.perf_counter() if began is None else began, said[1], said[2])
        try:
            return await self._answered(observation, robot, episode, step, binary, began, name)
        finally:
            if name is not None:
                self._fleet.done(name)

    async def _answered(self, observation: Any, robot: str, episode: Optional[str], step: Optional[int],
                        binary: bool, began: Optional[float], name: Optional[str]) -> tuple:
        """_policy_on's answer, the policy run on `observation` in its batch (the robot it is held for: `name`)."""
        try:
            output, model_s, dispatched, size = await self._batcher(observation, key=name)
        except _ranks.GroupHalted as e:          # a rank left, or failed a call: no rank can answer alone
            refused = _Refused("UNAVAILABLE", f"this server's ranks serve no more: {e}", details={"reason": "crashed"})
            return refused.status, refused.body(), _JSON
        except Exception as e:  # noqa: BLE001 (whatever the policy raised: the robot is told, and the log has where)
            log.exception("the policy raised on an observation")       # its traceback: here, never to the robot
            refused = _Refused("POLICY_ERROR", f"the policy raised {_said(e)}",
                               details={"exception": {"type": type(e).__name__, "message": str(e)}})
            return refused.status, refused.body(), _JSON
        perf = {"inference_ms": round(model_s * 1000, 3)}
        if began is not None:
            perf["handler_ms"] = round((time.perf_counter() - began) * 1000, 3)
        answer = {"outputs": output, "perf": perf}
        try:
            payload = msgpack_io.pack(answer) if binary else json.dumps(answer).encode()
        except (msgpack_io.MsgpackError, TypeError, ValueError) as e:
            log.error("the policy's output cannot be sent: %s", e)
            refused = _Refused("POLICY_ERROR", f"the policy's answer cannot go back as msgpack: {e}"[:1000])
            return refused.status, refused.body(), _JSON
        if self._fleet is not None:
            self._fleet.answered(name, size, dispatched, model_s)
        if self._window is not None:
            self._window.act(robot, episode, step, output)
        return 200, payload, msgpack_io.MEDIA_TYPE.encode() if binary else _JSON

    async def _too_large(self, send) -> None:
        await self._respond(send, 413, f"the body is over this server's limit of {self._limit} bytes".encode(),
                            close=True)

    async def _respond(self, send, status: int, body: bytes, *, content_type: bytes = _TEXT, close: bool = False,
                       extra: Iterable = ()) -> None:
        headers = [(b"content-type", content_type), (b"content-length", str(len(body)).encode()),
                   (_SERVER, self._identity), (b"x-seq-act-formats", self._formats), *extra]
        if close:
            headers.append((b"connection", b"close"))  # the rest of a body over the limit is not read
        await send({"type": "http.response.start", "status": status, "headers": headers})
        await send({"type": "http.response.body", "body": body})


def _data_plane(copy: Any = None) -> Any:
    """The robots' data plane (engine.data_plane), its frames going to `copy` (engine.episodes.PolicyCopy) where one is
    given. ImportError where sequence-base is not installed (Python 3.9): a robot's stream is the one way a robot
    reaches the server."""
    try:
        from .data_plane import DataPlane
    except ImportError as missing:
        raise ImportError(f"serve() takes each robot's stream, which needs sequence-base: Python 3.10 or later, where "
                          f"pip install sequence-ai installs it ({missing})") from missing
    return DataPlane(copy=copy)


def _header(scope, name: bytes) -> bytes:
    for key, value in scope.get("headers", ()):
        if key.lower() == name:
            return value
    return b""


async def _body(receive, limit: int) -> Optional[bytes]:
    """The request's body, or None once it is over `limit` bytes (what is left of it is not read)."""
    chunks, size = [], 0
    while True:
        message = await receive()
        if message["type"] == "http.disconnect":
            break
        chunk = message.get("body", b"")
        size += len(chunk)
        if size > limit:
            return None
        chunks.append(chunk)
        if not message.get("more_body"):
            break
    return b"".join(chunks)


def _with_tried(optimized: dict, tried: dict) -> dict:
    """What the warm-up kept, with a trial's report added (cfg_parallel's, pipeline_parallel's): its switches and what
    it turned on after the ones before it."""
    return {**optimized, **{k: v for k, v in tried.items() if k not in ("on", "switches")},
            "on": list(optimized.get("on") or []) + list(tried["on"]),
            "switches": {**(optimized.get("switches") or {}), **tried["switches"]}}


def _own(value: Any) -> Any:
    """`value` with each read-only numpy array in it - in dicts, lists and tuples - as a writable copy, the policy's
    own.
    WHY: msgpack hands out arrays that read the request's bytes in place, and torch.from_numpy warns about each of them
    (and torch.as_tensor on the CPU), while a policy that writes into its observation fails; a copy costs a few
    microseconds for a camera frame."""
    if isinstance(value, dict):
        return {key: _own(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return type(value)(_own(item) for item in value)
    flags = getattr(value, "flags", None)
    if flags is not None and hasattr(value, "copy") and not getattr(flags, "writeable", True):
        return value.copy()
    return value


def _numpy(value: Any) -> Any:
    """`value` with each torch tensor and JAX array in it - in dicts, lists and tuples - as a numpy array, a dtype numpy
    or msgpack does not carry (bfloat16) as float32. Everything else is returned as it is: msgpack_io.pack names what it
    cannot send."""
    if isinstance(value, dict):
        return {key: _numpy(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return type(value)(_numpy(item) for item in value)
    if value is None or isinstance(value, (str, bytes, bytearray, bool, int, float)):
        return value
    import numpy as np

    if isinstance(value, np.generic):
        return value
    if not isinstance(value, np.ndarray):
        if callable(getattr(value, "detach", None)) and callable(getattr(value, "cpu", None)):   # a torch tensor
            tensor = value.detach().cpu()
            try:
                return tensor.numpy()
            except TypeError:                         # a dtype numpy has no counterpart for: bfloat16, float8
                return tensor.float().numpy()
        if not hasattr(value, "__array__"):
            return value
        value = np.asarray(value)                     # a JAX array, or another library's that numpy can read
    if value.dtype.kind == "V" and value.dtype.fields is None:
        try:
            return value.astype(np.float32)           # ml_dtypes' bfloat16, as a JAX array reads into numpy
        except (TypeError, ValueError):
            return value                              # raw bytes: msgpack_io.pack names the dtype it cannot send
    return value


def _version() -> str:
    """sequence-ai's version as installed; "dev" in a source checkout that was never installed."""
    try:
        from importlib.metadata import version

        return version("sequence-ai")
    except Exception:  # noqa: BLE001 (no installed metadata: a checkout run as it is)
        return "dev"


def _said(e: BaseException) -> str:
    return f"{type(e).__name__}: {e}" if str(e) else type(e).__name__


def _duration(seconds: float) -> str:
    return f"{seconds:.1f} s" if seconds >= 1 else f"{seconds * 1000:.1f} ms"


# ── serve() ───────────────────────────────────────────────────────────────────────────────────────────────────────────
def serve(policy: Callable[[Any], Any], *, host: Optional[str] = None, port: int = 8000,
          batch: Optional[Iterable[int]] = None, token: Optional[str] = None, example: Any = None,
          limit: int = LIMIT, log_level: str = "info", record: bool = True, copy: Any = None,
          hz: Optional[float] = None, action_chunk_valid_len: Optional[int] = None,
          action_chunk_replan_at: Optional[int] = None, max_wait_for_batch: Optional[float] = None,
          examples: Optional[list] = None, cuda_graphs: Optional[bool] = None, whole_graph: Optional[bool] = None,
          torch_compile: bool = False, fused_kernels: bool = False, tensorrt: bool = False,
          precision: Optional[str] = None, tolerance: Any = None, cfg_parallel: bool = False,
          pipeline_parallel: bool = False) -> None:
    """
    Serve `policy` to robots elsewhere until the process is stopped (Ctrl-C), the module's docstring having what each
    part does by default:

        serve(policy, port=8000, example=observation)                                    # one observation per call
        serve(policy_on_a_list, batch=[1, 2, 4, 8], example=observation)                 # a list per call
        serve(policy_on_a_list, batch=[1, 2, 4], example=observation,                    # each robot by its own time
              hz=20, action_chunk_valid_len=15, action_chunk_replan_at=8)

    policy     a function: an observation in - a dict, as the robot sent it, numpy arrays as arrays, each its own to
               write into - and what the robot gets back out: a dict, an array, a list; torch tensors and JAX arrays
               are sent as numpy
    host       None: every address of this machine (0.0.0.0, and :: where it has IPv6). "127.0.0.1": this machine only
    port       the port, 8000
    batch      None: one observation per call. A list of batch sizes, 1 among them: `policy` takes a list of
               observations and returns a list of outputs, one for each, in order, and is called with the largest
               listed number of the observations waiting; examples/serve_openpi_batched.py has one
    token      a robot must send Authorization: Bearer <token> (connect(url, token=...)); None: $SEQ_SERVE_TOKEN if
               it is set, else no token; "": no token
    example    an observation the policy is run on before /ping says ready, at each batch size, and that GET /example
               hands out (the check command uses it)
    limit      the most bytes a request's body, or a message of a robot's stream, may hold: 64 MB
    log_level  uvicorn's and this module's: "info" says where it listens and how the warm-up went
    record     False: the server keeps nothing of the robots' steps for a recorder (GET /record, engine.recorder); else
               the last minute of them, in memory, for network.record to read as they come
    examples   observations the speed-ups are checked on before /ping says ready (engine.optimize): 32 or more of
               your robot's own check more than `example` alone, which is used when none are given
    cuda_graphs   False: no module of the policy is replayed from CUDA graphs (engine.optimize)
    whole_graph   False: no run's whole call into the model is replayed as one graph
    torch_compile, fused_kernels, tensorrt   True: tried during the warm-up, each kept where its outputs stay within
               `tolerance` of eager mode's and acts are faster (engine.optimize)
    precision  "fp16", "fp32" or "fp8": tried the same way; None, the default: the model's own dtype
    tolerance  the difference you accept from eager mode's outputs for the switches above: a number (the largest
               absolute difference), or {"max_abs": ..., "mean_abs": ..., "cosine": ...}; one of them on without it
               is refused (ValueError) before the server starts
    cfg_parallel  True, on a server of two processes (torchrun --nproc-per-node 2): the policy's model called with its
               guidance's two halves in one batch runs one half in each, tried during rank 0's warm-up and kept where
               its outputs stay within `tolerance` and acts are faster (engine.cfg_parallel)
    pipeline_parallel  True, on a server of two processes or more (torchrun --nproc-per-node N): the run of blocks the
               policy's model calls one after another split into one stage a process, each call of it passed through
               the stages in parts - a diffusion transformer's tokens in patches, or rows of its batch - tried during
               rank 0's warm-up and kept where its outputs stay within `tolerance` and acts are faster
               (engine.pipeline_parallel)
    copy       the copy of the policy each episode's frames go to (engine.episodes.PolicyCopy: a @seq.policy class's
               episodes, observe function, on_episode and plans, as a deployment's worker runs them); `policy` is then
               its call - `seq serve` gives both
    hz, action_chunk_valid_len, action_chunk_replan_at
               how a robot plays an answer, as @seq.policy declares it: how many of an answer's steps it plays a second,
               how many of them it may play (N; None: action_chunk_replan_at) and the step, counted from when an act was
               sent, at which it sends the next (k; None: N, a robot asking once an answer is played out, which leaves
               its acts no time to wait for others). Given, each robot's acts wait for a batch only as long as its own
               answer leaves it time, and only the robots it answers in time are seated, each by its own round trip
               (the module's docstring). Needs `example`, to time the batches
    max_wait_for_batch
               how long a robot waits for an answer at most, in seconds from when it sent its act: its acts are held and
               its robots seated by that instead of what is left of the answer it plays (its actions may run out)

    Raises what the policy raised on the example, once the server has stopped; OSError when the port is taken;
    ImportError where sequence-base is not installed (Python 3.9); ValueError for hz, action_chunk_valid_len,
    action_chunk_replan_at or max_wait_for_batch that do not say how a robot plays an answer, or given with no example.
    """
    if token is None:
        token = os.environ.get(TOKEN_ENV) or None
    app = App(policy, batch=batch, token=token, example=example, limit=limit, record=record, copy=copy, hz=hz,
              action_chunk_valid_len=action_chunk_valid_len, action_chunk_replan_at=action_chunk_replan_at,
              max_wait_for_batch=max_wait_for_batch, examples=examples, cuda_graphs=cuda_graphs,
              whole_graph=whole_graph, torch_compile=torch_compile, fused_kernels=fused_kernels, tensorrt=tensorrt,
              precision=precision, tolerance=tolerance, cfg_parallel=cfg_parallel,
              pipeline_parallel=pipeline_parallel)
    if app._group is not None and not app._group.leads:
        _follow(app, log_level)                       # a rank other than 0: no port of robots', rank 0's calls alone
        return
    server = _uvicorn(app, log_level, limit=limit)
    sockets = _listen(host, port)
    # the policy failed on the example: /ping says so with why for FAILED_SAID_S - a robot waiting on it hears the
    # reason, where a server gone at once left it waiting out its whole bound - then the server stops
    app.on_failure = lambda: threading.Timer(FAILED_SAID_S, lambda: setattr(server, "should_exit", True)).start()
    _log_with(log_level)

    where = " and ".join(_url(sock) for sock in sockets)
    paths = ("GET /stream, POST /observe, POST /act, GET /ping"
             + (", GET /example" if example is not None or examples else "")
             + (", GET /record" if record else ""))
    calls = "one observation per call" if batch is None else \
        f"batches of {', '.join(str(n) for n in sorted({int(n) for n in batch}))}"
    log.info("serving %s on %s (%s); %s", getattr(policy, "__qualname__", type(policy).__name__), where, paths, calls)
    if app._fleet is not None:
        plays = app._fleet.plays
        log.info("holds and seats each robot by its own time: %g Hz, %d valid steps, the next asked for at step %d%s",
                 plays["hz"], plays["action_chunk_valid_len"], plays["action_chunk_replan_at"],
                 f", answers waited for {plays['max_wait_for_batch']:g} s at most" if "max_wait_for_batch" in plays
                 else "")
    if token:
        log.info("a robot needs the token: connect(url, token=...)")
    elif not all(_loopback(sock) for sock in sockets):
        log.warning("no token: anyone who can reach port %d can run the policy (seq serve --token TOKEN or $%s asks "
                    "for one)", sockets[0].getsockname()[1], TOKEN_ENV)
    try:
        server.run(sockets=sockets)
    except KeyboardInterrupt:
        pass                                          # Ctrl-C: uvicorn has shut down, and says so; as uvicorn.run()
    finally:
        app.close()
        for sock in sockets:
            sock.close()
    if app.failure is not None:
        raise app.failure


def _follow(app: App, log_level: Optional[str]) -> None:
    """A rank other than 0 of a group (engine.ranks): rank 0 joined, then each call of the policy it sends run on this
    rank's policy thread - as rank 0 runs its own - until rank 0 stops."""
    group = app._group
    _log_with(log_level)
    log.info("%s: following rank 0 at %s:%d - it serves the robots, and sends this rank each call of the policy",
             group, group.host, group.port)

    def run_one(op: str, args: list) -> Any:
        if op == "call":                              # a batch of acts, or the warm-up's
            return app._thread.submit(app._call_here, app._unwire(args[0])).result()
        if op == "cfg_parallel":                      # the split put in place, or taken out, as on rank 0
            return app._thread.submit(split_trials.cfg_toggle, app, *args).result()
        if op == "pipeline_parallel":                 # the blocks' stages put in place, or taken out, as on rank 0
            app._thread.submit(split_trials.pp_toggle, app, *args).result()
            return None
        fn = app._mirrored.get(op)                    # an episode's frames to its observe function, its end, ...
        if fn is None:
            raise ValueError(f"rank 0 sent a call this rank does not know: {op!r}")
        return app._thread.submit(fn, *args).result()

    try:
        group.follow(run_one)
    except KeyboardInterrupt:
        pass
    finally:
        app.close()
    log.info("%s: rank 0 stopped, and so does this rank", group)


def _uvicorn(app: App, log_level: Optional[str], *, limit: int = LIMIT) -> Any:
    """The uvicorn server serve() runs `app` on: each response in one write, the app's lifespan for its warm-up, a
    robot's stream on the WebSocket network.websocket serves - a message as large as a request may be, the robot pinged
    every WS_PING_S -, no line per request, idle connections kept KEEP_ALIVE_S."""
    try:
        import uvicorn
    except ImportError as missing:
        raise ImportError("serve() runs uvicorn, which sequence-ai installs and this environment lacks: "
                          "pip install sequence-ai") from missing
    from ..network import websocket
    from ..network.one_write import WholeResponse, one_write_http

    config = uvicorn.Config(WholeResponse(app), http=one_write_http(), lifespan="on",
                            ws=websocket.protocol(), ws_max_size=limit + (1 << 20),
                            ws_ping_interval=WS_PING_S, ws_ping_timeout=WS_PONG_S, log_level=log_level,
                            access_log=False, timeout_keep_alive=KEEP_ALIVE_S, server_header=False)
    return uvicorn.Server(config)


def _resolve(host: Optional[str], port: int) -> tuple:
    """The one (family, address) serve() binds for `host`, and the addresses to probe for a server already there. For
    `host` None the bind is None - the caller's dual 0.0.0.0/:: bind - and the probe is this machine's loopback; for a
    wildcard host, the probe is loopback of that family (macOS lets 0.0.0.0 bind over a port held on 127.0.0.1); for a
    concrete host, both are that address."""
    loopbacks = [(socket.AF_INET, "127.0.0.1")] + ([(socket.AF_INET6, "::1")] if socket.has_ipv6 else [])
    if host is None:
        return None, loopbacks
    family, _, _, _, address = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM, flags=socket.AI_PASSIVE)[0]
    if address[0] in ("0.0.0.0", "::"):
        return (family, address[0]), [(f, a) for f, a in loopbacks if f == family]
    return (family, address[0]), [(family, address[0])]


def answered_at(host: Optional[str], port: int) -> None:
    """Raise OSError(EADDRINUSE), worded, when a server already answers at `host`:`port` on this machine; return when
    nothing does. `seq serve` calls this before it prints that it is serving, so a taken port is one line, not a bind
    traceback after the "serving ..." line. `host` is as serve() takes it: None is this machine's loopback."""
    _unanswered(port, _resolve(host, port)[1])


def _listen(host: Optional[str], port: int) -> list:
    """The bound sockets serve() listens on: for `host` None, 0.0.0.0 and, where this machine has IPv6, :: (IPv6 only,
    beside the first, on the same port); else the one address `host` resolves to. OSError when the port is taken - a
    concrete host is probed too, not only a wildcard, so a second server on 127.0.0.1 over one already on 0.0.0.0 is
    refused rather than left to split this machine's robots between the two (macOS)."""
    bind_to, probe = _resolve(host, port)
    _unanswered(port, probe)
    if bind_to is not None:
        family, address = bind_to
        return [_bind(family, address, port)]
    sockets = [_bind(socket.AF_INET, "0.0.0.0", port)]
    if socket.has_ipv6:
        try:
            sockets.append(_bind(socket.AF_INET6, "::", sockets[0].getsockname()[1], v6only=True))
        except OSError as e:
            if e.errno not in (errno.EAFNOSUPPORT, errno.EADDRNOTAVAIL, errno.EPROTONOSUPPORT):
                sockets[0].close()
                raise
            log.debug("no IPv6 address to listen on: %s", e)
    return sockets


def _unanswered(port: int, loopbacks: list) -> None:
    """OSError when a server already answers at `port` on this machine's loopback.
    WHY: macOS lets a socket bind every address (0.0.0.0) at a port another program holds on 127.0.0.1, and a robot on
    this machine then reaches the other program; a server that started all the same would never see its requests."""
    if not port:
        return
    for family, address in loopbacks:
        with socket.socket(family, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.5)
            if probe.connect_ex((address, port)) != 0:
                continue                              # refused, or no such address here: nothing answers there
        where = f"[{address}]:{port}" if family == socket.AF_INET6 else f"{address}:{port}"
        raise OSError(errno.EADDRINUSE, f"port {port} is taken: a server already answers at {where} on this machine "
                                        "(an earlier seq serve still running?); stop it, or give seq serve another "
                                        "--port")


def _bind(family: int, address: str, port: int, *, v6only: Optional[bool] = None) -> socket.socket:
    sock = socket.socket(family, socket.SOCK_STREAM)
    try:
        if os.name != "nt":
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # a restarted server takes its port at once
        if v6only is not None:
            sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, int(v6only))
        sock.bind((address, port))
    except OSError as e:
        sock.close()
        if e.errno == errno.EADDRINUSE:
            raise OSError(e.errno, f"port {port} on {address} is taken: another server listens there (an earlier "
                                   "seq serve still running?); stop it, or give seq serve another --port") from e
        raise
    return sock


def _url(sock: socket.socket) -> str:
    address, port = sock.getsockname()[:2]
    return f"http://[{address}]:{port}" if sock.family == socket.AF_INET6 else f"http://{address}:{port}"


def _loopback(sock: socket.socket) -> bool:
    address = sock.getsockname()[0]
    return address == "::1" or address.startswith("127.")


def _log_with(level: Optional[str]) -> None:
    """This module's lines through uvicorn's own handler, at its level, where nothing else is set up to show them. A
    root logger that would drop them counts as nothing: one a library set up at WARNING on import, as absl does for a
    JAX policy, would hide the warm-up and "ready" lines."""
    if level is None or log.handlers or logging.getLogger("sequence_ai").handlers:
        return
    wanted = logging.getLevelName(level.upper()) if isinstance(level, str) else level
    root = logging.getLogger()
    if root.handlers and root.isEnabledFor(wanted):
        return
    for handler in logging.getLogger("uvicorn").handlers:
        log.addHandler(handler)
    log.setLevel(wanted)
    log.propagate = False
