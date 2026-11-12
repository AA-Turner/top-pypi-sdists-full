"""
A person's console for one robot: sequence_ai.teleop(key=) - with the robot's own key - connects
straight to that robot (WebRTC, teleop_direct.py), the platform carrying only the two sides' first words.

In one sentence: teleop() → an offer of a connection, with what its network looks like, to the platform (POST
/v1/teleop/offer), which hands it to the robot on its link → the robot's answer comes back (GET /v1/teleop/pairing/{id},
long-polled) and the two meet, or it fails saying why - nothing goes any other way → on the reliable channel the robot
says who drives, and take(), release() and stop() are each said and answered with who drives then (Conflict while
another person drives), a heartbeat every HEARTBEAT_S (a driving console silent for 3 s stops its robot) → send(chunk) goes
at once, numbered and timed, stream() hands on the robot's newest step as its observe() made it, states() each step's
arrays alone as soon as they come, requests() each time its policy's plan asks for a person, metrics() how late each
command and step was.
WHY straight and nothing else: a console near its robot and far from its worker paid two trips to the worker for
nothing, one TCP connection held every message behind a lost packet (a p95 of 232 ms measured), and a robot with no policy
has no worker to go through.

WHY no way around a pair that cannot meet: a console that silently went another way would drive at a latency its person
never chose.
"""
from __future__ import annotations

import collections
import queue
import threading
import time
from typing import Any, Iterator, Optional

from ..errors import Conflict, InvalidRequest, MissingPackage, Unavailable
from . import latency_stats as _stats
from . import msgpack_io as _msgpack
from . import teleop_clock as _clock
from . import teleop_direct as _direct
from .names import segment

OFFER = "/v1/teleop/offer"


OFFER_AGAIN_S = 10.0
PAIRING = "/v1/teleop/pairing/{}"

PAIRING_WAIT_S = 20

HEARTBEAT_S = 0.5

_FRAMES_KEPT = 64

_PENDING_KEPT = 4096
LOST_AFTER_S = 2.0

_CLOSING_STOP_S = 0.5


def _codec():
    """The marked items' codec observe() encodes with (marked_observe._codec, sequence-ai[observe]), or None without it:
    the steps as they travel."""
    from .marked_observe import _codec as codec

    try:
        return codec()
    except MissingPackage:
        return None


class Teleop:
    """One console's connection to one robot (module docstring) - from sequence_ai.teleop(), not made directly. Use it
    as a context manager, or close() it: a console that drove the robot and went stops it."""

    def __init__(self, gateway: Any, *, operator: Optional[str], timeout_s: float) -> None:
        _direct.require()
        self.robot: Optional[str] = None
        self.operator = operator
        self.path = "direct"
        self._tracks: list = []
        self._lock = threading.Condition()
        self._driver: dict = {"driver": "model", "by": None, "since": None}
        self._yours = False
        self._opened = False
        self.refused: Optional[dict] = None
        self._refusals = 0
        self.rtt_ms: Optional[float] = None

        self._help: queue.Queue = queue.Queue()
        self._frames: queue.Queue = queue.Queue()
        self._states: queue.Queue = queue.Queue()
        self._closed: Optional[str] = None
        self._sent = 0
        self._clock = _clock.Clock()
        self.stats = _stats.LatencyStats(**_stats.CONSOLE)

        self._pending: "collections.OrderedDict[int, int]" = collections.OrderedDict()
        self._answers = False




        self._newest: tuple = (None, None)
        self._kf_asked = 0.0
        self._link: Optional[Any] = _direct.ConsoleLink(self._said, self._state_changed)
        try:
            self._meet(gateway, max(timeout_s, _direct.OPEN_S))
        except BaseException:
            self.close()
            raise
        threading.Thread(target=self._heartbeat, daemon=True, name="seq-teleop-heartbeat").start()



    def _meet(self, gateway: Any, timeout_s: float) -> None:
        """Connect straight to the robot, the platform carrying the two sides' first words - else what the platform or
        the network said, and nothing else goes in its place."""
        end = time.monotonic() + timeout_s
        link = self._link
        _direct.install_receiving()
        offer = link.offer(timeout_s, tracks=_direct.MOST_TRACKS, on_track=self._took_track)
        placed = self._offered(gateway, {**({"operator": self.operator} if self.operator else {}), "sdp": offer["sdp"],
                                         "nat": offer["nat"]}, min(end, time.monotonic() + OFFER_AGAIN_S))
        self.robot = placed.get("robot")
        answer = self._answer_of(gateway, str(placed.get("pairing")), end)
        link.accept(answer["sdp"], max(1.0, end - time.monotonic()))
        if not link.wait_open(max(1.0, end - time.monotonic())):
            facts = link.facts()
            why = _direct.why_not(offer.get("nat"), answer.get("nat"), facts)
            raise Unavailable(f"no direct connection to the robot: {why}", details={
                "reason": "direct_failed", "console": offer.get("nat"), "robot": answer.get("nat"), **facts})

        with self._lock:
            self._lock.wait_for(lambda: self._opened or self._closed is not None, max(1.0, end - time.monotonic()))
            opened, why = self._opened, self._closed
        if not opened:
            raise Unavailable(f"the robot said nothing on its direct connection: {why or 'no answer in time'}",
                              details={"reason": "direct_failed"})

    @staticmethod
    def _offered(gateway: Any, body: dict, until: float) -> dict:
        """The offer placed with the platform. One it says came too soon after the last of this key's for this robot
        (offer_too_soon) is made again once the wait it names is over, while that ends before `until`; any other refusal,
        or one that names no wait, as it came - no wait of the console's own.

"""
        while True:
            try:
                return gateway.post(OFFER, body)
            except Unavailable as exc:
                wait = exc.retry_after_s
                if ((exc.details or {}).get("reason") != "offer_too_soon" or wait is None or wait < 0
                        or time.monotonic() + wait > until):
                    raise
                time.sleep(wait)

    def _answer_of(self, gateway: Any, pairing: str, end: float) -> dict:
        """The robot's answer to this console's offer, asked for until `end`."""
        path = PAIRING.format(segment(pairing, "pairing"))
        while True:
            left = int(end - time.monotonic())
            if left < 1:
                raise Unavailable("no direct connection to the robot: it did not answer in time",
                                  details={"reason": "direct_failed"})
            said = gateway.get(f"{path}?wait_s={min(left, PAIRING_WAIT_S)}")
            if said.get("state") == "answered" and said.get("sdp"):
                return said
            if said.get("state") == "failed":
                raise Unavailable(f"no direct connection to the robot: it could not answer ({said.get('why')})",
                                  details={"reason": "direct_failed"})

    def _said(self, label: str, data: bytes, at_us: int) -> None:
        """A whole message the robot sent (the direct connection's thread): who drives, a control one, a step."""
        try:
            message = _msgpack.unpack(data)
        except Exception:
            return
        if not isinstance(message, dict):
            return
        if label == "seq-who":
            self._who(message)
            return
        if label == "seq-ctl":
            self._control(message, at_us)
            return
        episode, n, made = message.get("e"), message.get("n"), _clock._micros(message.get("t_us"))
        if not isinstance(n, int):
            return
        if label == "seq-state":
            self._state(episode, n, made, message.get("v"), at_us)
            if message.get("video"):
                return
        self._put(self._frames, {"episode": episode, "steps": [[n, message.get("v")]], "t_us": {n: made}})

    def _took_track(self, track: Any) -> None:
        """One of the robot's cameras as a video track (the connection's thread): its newest frame read as it comes."""
        import asyncio

        from . import teleop_video as _video

        fresh = _video.latest_frame_track(track, on_drop=lambda n: self.stats.count("frames_dropped", n))
        self._tracks.append(fresh)
        asyncio.ensure_future(self._read_track(fresh))

    async def _read_track(self, fresh: Any) -> None:
        while self._closed is None:
            try:
                frame, n, made = await fresh.recv()
            except Exception:
                return
            key = getattr(fresh, "key", None)
            if isinstance(n, int) and key is not None:
                self._put(self._frames, {"episode": getattr(fresh, "episode", None), "steps": [[n, {key: frame}]],
                                         "t_us": {n: made}})

    def _state_changed(self, state: str) -> None:
        """The direct connection's state (its thread): one that failed or closed ends this console."""
        if state in ("failed", "closed"):
            self._ended(f"the direct connection to the robot {state}")

    def _who(self, message: dict) -> None:
        """What the robot says on its reliable channel."""
        kind = message.get("t")
        if kind == "help":
            self._help.put(message)
            return
        with self._lock:
            if kind == "driver":
                since = _clock._micros(message.get("since_us"))
                self._driver = {"driver": message.get("driver"), "by": message.get("by"),
                                "since": since / 1e6 if since is not None else None}
                self._yours = bool(message.get("yours"))
                self._opened = True
            elif kind == "refused":
                self.refused = message
                self._refusals += 1
            elif kind == "pong":
                at = _clock._micros(message.get("at_us"))
                if at is not None:
                    self.rtt_ms = (_clock.now_us() - at) / 1000.0
            self._lock.notify_all()

    def _control(self, message: dict, at_us: int) -> None:
        """The robot's tock, receipt, or what a video track's frame is."""
        kind = message.get("t")
        if kind == "vm":
            i = message.get("i")
            if isinstance(i, int) and 0 <= i < len(self._tracks):
                fresh = self._tracks[i]
                fresh.key, fresh.episode = message.get("key"), message.get("e")
                fresh.feed_meta(message)
        elif kind == "tock":
            trip = self._clock.tock(message, at_us)
            if trip is not None:
                self.stats.sample("rtt_us", trip)
        elif kind == "got":
            with self._lock:
                sent = self._pending.pop(message.get("id"), None)
                self._answers = True
            off, got = self._clock.offset_us, _clock._micros(message.get("got_us"))
            if sent is not None and off is not None and got is not None:
                self.stats.sample("command_us", (got - off) - sent)

    def _saw(self, n: int, made: Optional[int]) -> None:
        """A step handed on to this console's caller: the newest so far, by its capture time, is what the next command
        is made from."""
        if made is None:
            return
        with self._lock:
            if self._newest[1] is None or made > self._newest[1]:
                self._newest = (n, made)

    def _state(self, episode: Any, n: int, made: Optional[int], value: Any, at_us: int) -> None:
        """One step's arrays as they came: to states(), and how late they came."""
        off = self._clock.offset_us
        if made is not None and off is not None:
            self.stats.sample("state_us", at_us - (made - off))
        if value is not None:
            self.stats.count("states_received")
            self._put(self._states, {"episode": episode, "seq": n, "state": value, "t_us": made})

    @staticmethod
    def _put(into: queue.Queue, message: dict) -> None:
        into.put(message)
        while into.qsize() > _FRAMES_KEPT:
            try:
                into.get_nowait()
            except queue.Empty:
                break

    def _ended(self, why: str) -> None:
        with self._lock:
            if self._closed is not None:
                return
            self._closed = why
            self._yours = False
            self._lock.notify_all()
        self._help.put(None)
        self._frames.put(None)
        self._states.put(None)

    def _heartbeat(self) -> None:
        """That it is there, every HEARTBEAT_S, and its clock ticks to the robot."""
        ping_at = tick_at = 0.0
        while self._closed is None:
            link, now = self._link, time.monotonic()
            if link is None:
                return
            if now >= ping_at:
                link.who({"t": "ping", "at_us": _clock.now_us()})
                ping_at = now + HEARTBEAT_S
            if now >= tick_at:
                link.control(self._clock.tick())
                tick_at = now + self._clock.due()
            time.sleep(max(0.005, min(ping_at, tick_at) - time.monotonic()))



    def _say(self, kind: str, done: Any, timeout_s: float) -> dict:
        """Say `kind` and wait for the robot's answer: who drives once `done()` - or the refusal that came after it
        (Conflict)."""
        with self._lock:
            before, link, closed = self._refusals, self._link, self._closed
        if link is None or closed is not None:
            raise Unavailable(f"this console's connection to the robot ended: {closed or 'it was closed'}",
                              hint="connect again (sequence_ai.teleop)")
        link.who({"t": kind, **({"by": self.operator} if self.operator else {})})
        end = time.monotonic() + timeout_s
        with self._lock:
            while True:
                if done():
                    return dict(self._driver)
                if self._refusals > before:
                    refused = self.refused or {}
                    raise Conflict(str(refused.get("why") or "the robot refused it"),
                                   details={k: refused.get(k) for k in ("reason", "driver", "by", "since_us")})
                if self._closed is not None:
                    raise Unavailable(f"this console's connection to the robot ended: {self._closed}",
                                      hint="connect again (sequence_ai.teleop)")
                left = end - time.monotonic()
                if left <= 0:
                    raise Unavailable(f"the robot did not answer {kind} within {timeout_s} s")
                self._lock.wait(left)

    def take(self, timeout_s: float = 5.0) -> dict:
        """Drive the robot from this console: from now its act() hands back the chunks sent here (send) and nothing of
        its model's. One person drives a robot at a time: Conflict while another does, saying who (its details'
        "by"). Who drives then: {"driver": "human", "by": this console's operator name, "since"}."""
        return self._say("take", lambda: self._yours and self._driver.get("driver") == "human", timeout_s)

    def send(self, chunk: Any, *, sampled_us: Optional[int] = None) -> None:
        """One action chunk to the robot, at once - what its next act() hands back, in the form its policy's answers
        have (a dict of arrays: the same keys and shapes), played once: with none newer, its act() hands back its hold
        and it stays where it is. Only while this console drives it (take). Each is numbered and timed, and says the
        newest step this console had as it was sent: the robot plays the newest alone, and drops one made from a view
        older than half a second, or 5 of its policy's steps where that is longer (metrics() counts each).
        `sampled_us`: when the input it was made from was read (this machine's clock, microseconds since the epoch) -
        its metrics say input_us from it."""
        with self._lock:
            if self._closed is not None or self._link is None:
                raise Unavailable(f"{self._closed or 'it was closed'}: connect again (sequence_ai.teleop)",
                                  details={"reason": "direct_lost"})
            if not self._yours:
                raise Conflict("this console does not drive the robot: take() it first",
                               details={"reason": "not_driving", **self._driver})
            self._sent += 1
            number, link = self._sent, self._link
            sent_us = _clock.now_us()
            self._pending[number] = sent_us
            while len(self._pending) > _PENDING_KEPT:
                self._pending.popitem(last=False)
            ref_n, ref_us = self._newest
        self.stats.count("commands_sent")
        if isinstance(sampled_us, int) and not isinstance(sampled_us, bool):
            self.stats.sample("input_us", sent_us - sampled_us)
        link.command(_msgpack.pack({"chunk": chunk, "id": number, "sent_us": sent_us, "off_us": self._clock.offset_us,
                                    "ref_us": ref_us, "ref_n": ref_n}))

    def release(self, timeout_s: float = 5.0) -> dict:
        """Hand the robot back - to its model, or to no one where it has none - from this console's drive, or from a
        stop. Conflict while another person drives it."""
        return self._say("release", lambda: self._driver.get("driver") == "model", timeout_s)

    def stop(self, timeout_s: float = 5.0) -> dict:
        """Stop the robot where it is - whoever drives it, a person or its model: its act() hands back its hold until
        a console takes or releases it."""
        return self._say("stop", lambda: self._driver.get("driver") == "stopped", timeout_s)

    @property
    def driver(self) -> dict:
        """Who drives the robot now, as it last said: {"driver": "model" | "human" | "stopped", "by": the operator's
        name, "plan", or None, "since": its epoch second, or None}. "model" is no one, on a robot with no policy."""
        with self._lock:
            return dict(self._driver)

    @property
    def driving(self) -> bool:
        """Whether this console drives the robot now."""
        with self._lock:
            return self._yours

    def stream(self) -> Iterator[dict]:
        """The robot's newest view each time something new has come: {"episode", "seq", "observation", "t_us"} - the
        observation the newest of each of its items in this episode: the newest step's arrays, its Depth and Tactile items
        decoded back to theirs (sequence-ai[observe]; without it, as they travel), and each camera's newest frame, an RGB
        array. A camera's frame may be a few steps from the arrays beside it, behind them or ahead: each comes its own way,
        and a frame is dropped rather than made to wait. `seq` and `t_us` are the newest thing's: its number in the episode
        and when the robot made it (its clock, microseconds since the epoch). A console that reads slower than the robot
        observes gets the newest each time, never a backlog (metrics' frames_dropped). Ends with the connection.



"""
        marked = _codec()
        streams: dict = {}
        view: dict = {}
        showing: Any = None
        while True:
            message = self._frames.get()
            if message is None:
                self._frames.put(None)
                return
            batch = [message]
            while True:
                try:
                    more = self._frames.get_nowait()
                except queue.Empty:
                    break
                if more is None:
                    self._frames.put(None)
                    break
                batch.append(more)
            newest = None
            for message in batch:
                episode = message.get("episode")
                made = message.get("t_us") or {}
                for n, inputs in message.get("steps") or ():
                    self.stats.count("frames_received")
                    observation = inputs
                    if marked is not None:
                        try:
                            observation = marked.decode(inputs, streams.setdefault(episode, marked.Streams()))
                        except marked.NeedsKeyframe:
                            self._keyframe(episode)
                            continue
                        while len(streams) > 8:
                            streams.pop(next(iter(streams)))
                    if episode != showing:
                        view, showing = {}, episode
                    view.update(observation)
                    if newest is not None and newest["episode"] == episode and newest["seq"] > n:
                        newest["observation"] = dict(view)
                        continue
                    if newest is not None and (newest["episode"] != episode or newest["seq"] != n):
                        self.stats.count("frames_dropped")
                    newest = {"episode": episode, "seq": n, "observation": dict(view), "t_us": made.get(n)}
            if newest is None:
                continue
            off, at = self._clock.offset_us, newest["t_us"]
            if isinstance(at, int) and off is not None:
                self.stats.sample("frame_us", _clock.now_us() - (at - off))
            self._saw(newest["seq"], at)
            yield newest

    def _keyframe(self, episode: Any) -> None:
        """Its decoder lost its place in a video: the robot asked for a keyframe, twice a second at most."""
        now = time.monotonic()
        with self._lock:
            link = self._link
            if link is None or now - self._kf_asked < 0.5 or not isinstance(episode, str):
                return
            self._kf_asked = now
        link.control({"t": "kf", "e": episode})

    def states(self) -> Iterator[dict]:
        """Each step's arrays - its every item that is no Video, Depth or Tactile one - as soon as they come:
        {"episode", "seq", "state", "t_us" (when the robot's observe() made it, by its clock)}. They come on a channel of
        their own, ahead of the step's frames. Ends with the connection."""
        while True:
            message = self._states.get()
            if message is None:
                self._states.put(None)
                return
            self._saw(message["seq"], message.get("t_us"))
            yield message

    def metrics(self) -> dict:
        """How this console's connection to the robot does: {"path": "direct", "latency_us": {name: {"n", "p50", "p95",
        "p99", "max"}}, "counters": {...}, "gauges": {...}} - microseconds, the newest samples of each: command_us (a
        command's one way: sent here → the robot got it), frame_us (a step's glass to glass: the robot's observe() →
        stream() handing it on), state_us (its arrays' one way), rtt_us (the command path's round trip), input_us (an
        input read → send(), where send() was told when); commands_sent, commands_unanswered, frames_received,
        frames_dropped, states_received; clock_offset_us (the robot's clock less this one's) and clock_uncertainty_us
        (how far off that may be). The robot's own side: its handle's teleop_metrics()."""
        now = _clock.now_us()
        unanswered = 0
        with self._lock:
            while self._pending:
                number, sent = next(iter(self._pending.items()))
                if now - sent < LOST_AFTER_S * 1e6:
                    break
                self._pending.popitem(last=False)
                unanswered += int(self._answers)
        if unanswered:
            self.stats.count("commands_unanswered", unanswered)
        self.stats.gauge("clock_offset_us", self._clock.offset_us)
        self.stats.gauge("clock_uncertainty_us", self._clock.error_us)
        return {"path": self.path, **self.stats.snapshot()}

    def requests(self) -> Iterator[dict]:
        """Each time the robot's policy asks for a person (a @seq.plan returning seq.ask_human), as the robot tells this
        console - once a request opens, its reason changes or it turns to hold, and first thing to a console that connects while one
        waits: {"id", "robot" (its name), "reason", "policy", "at" (the epoch second it first asked), "hold", "frame" (a
        small JPEG of its latest frame, or None)}. Ends with the connection.
        """
        while True:
            message = self._help.get()
            if message is None:
                self._help.put(None)
                return

            yield {**{k: v for k, v in message.items() if k != "t"}, "robot": message.get("robot") or self.robot}

    def close(self) -> None:
        """End this console's connection: a robot it drove stops."""
        with self._lock:
            yours = self._yours and self._closed is None
        if yours:
            try:
                self.stop(_CLOSING_STOP_S)
            except (Conflict, Unavailable, InvalidRequest):
                pass
        self._ended("the console closed its connection")
        with self._lock:
            link, self._link = self._link, None
        if link is not None:
            link.close()

    def __enter__(self) -> "Teleop":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
