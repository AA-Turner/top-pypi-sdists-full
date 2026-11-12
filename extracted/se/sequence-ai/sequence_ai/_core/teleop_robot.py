"""
Who drives a robot connected with "teleop" among its names, judged on the robot: one console at a
time drives it, connected straight to it (WebRTC, teleop_direct.py), and act() answers from what that console sent,
waiting for no network, whichever of the connection's handles its loop calls.

In one sentence: a console's offer reaches the robot from the platform (teleop_link.py) and is answered straight → on the
reliable channel it says take, release, stop and that it is there (a heartbeat), each answered with who drives then -
the first to take drives, a second is told who does, any console may stop it → its commands come on their own channel,
numbered and timed: one no newer than the newest kept from it is dropped ("old"), one made from a view older than
stale_s as it comes ("stale"), one from a console that does not drive it too, and the console told which (a receipt) →
act(), while a person drives, hands back the newest chunk not yet handed back - once: with none newer, it is `hold`,
the robot staying where it is; while stopped, `hold`; while no one drives, its model's, on a handle that has one, else
`hold` → a driving console silent for lost_s, or gone, stops the robot; each change is said to the platform's audit
(teleop_link.py) and told to each worker it is on, which decides nothing by it → a worker says on the robot's stream
that its plan asks for a person: stopped unless a person drives it, the ask handed on to its consoles.
WHY a worker is told at all: it keeps what no one reads for a robot its model does not drive (its unread limit), says a
plan's ask is taken and writes who drove into its records - and it is told only: a telling that does not arrive changes
no stop and no hold.
WHY here and not on a worker: a robot with no policy has no worker, and a robot with one must not need its worker's say
to stop.
WHY once: what an answer means is the policy's own - a dict of arrays, a list - so the SDK cannot take the steps a robot
played off it; handed back twice, a chunk's first steps would be played again.

WHY `hold` is by default the model's last answer emptied (each array's first axis cut to nothing, each list empty): a
loop that plays out["actions"] plays nothing and stays where it is, its code and act()'s answer's form unchanged; {} before
any. {the user 10-27: "just dot he way that is most cofirtable to teleoperator but not changing the act"}
WHY an act's answer is held to who drove as it went (after): a stop, or a person's taking the robot, while an act is on
its way reaches the robot first, and the answer that comes after it is no one's: act() hands back a person's chunk or
`hold` in its place, a release since included.

WHY the newest alone, and none whose view is past stale_s: a direct channel delivers in any order and sends nothing
twice, and a chunk made from a picture that old is what a person meant a while ago - or saw a frozen picture. The view's
age is the robot's own clock alone (`ref_us` to its arrival): no clock estimate in it.


"""
from __future__ import annotations

import threading
import time
import weakref
from collections import deque
from typing import Any, Callable, Optional

from . import latency_stats as _stats
from . import msgpack_io as _msgpack
from . import teleop_clock as _clock
from . import teleop_direct as _direct

DRIVERS = ("model", "human", "stopped")
_EMPTY = object()



STALE_STEPS = 5
STALE_LEAST_S = 0.5
LOST_S = 3.0

_WATCH_S = 0.25



HEADER = "X-Seq-Teleop-Robot"

_SAID_KEPT = 4096


def emptied(value: Any) -> Any:
    """`value` with nothing in it, in its own form: a dict's every value emptied, a list or tuple empty, an array cut to
    none along its first axis; anything else None."""
    if isinstance(value, dict):
        return {k: emptied(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)() if type(value) in (list, tuple) else []
    shape = getattr(value, "shape", None)
    if isinstance(shape, tuple) and len(shape) >= 1:
        try:
            return value[:0]
        except Exception:
            return None
    return None


def _micros(value: Any) -> Optional[int]:
    """A time (or a number) a message carried, as an integer, else None."""
    return int(value) if isinstance(value, int) and not isinstance(value, bool) else None


class Driven:
    """Who drives a robot, as this process judges it (module docstring) - one for all the handles of a connect."""

    def __init__(self, hold: Any = _EMPTY) -> None:
        self._lock = threading.Lock()
        self.driver = "model"
        self.by: Optional[str] = None
        self.since_us: Optional[int] = None
        self.peer: Optional[str] = None
        self._heard: dict = {}
        self._chunk: Any = None
        self._fresh = False
        self._from: Optional[dict] = None
        self._hold = hold
        self._last: Any = _EMPTY
        self.chunks = 0
        self.changes = 0
        self.hz: Optional[float] = None


        self.on_answer: Optional[Callable[[str, dict], None]] = None
        self.on_event: Optional[Callable[[dict], None]] = None
        self.on_close: Optional[Callable[[], None]] = None

        self.refused: Optional[Exception] = None
        self._handles = 0
        self._conns: list = []
        self._says: list = []
        self._said: deque = deque(maxlen=_SAID_KEPT)
        self._sink: Optional[Any] = None
        self._help: Optional[dict] = None
        self._links: Optional[Any] = None
        self._newest: dict = {}
        self.stats = _stats.LatencyStats(**_stats.ROBOT)
        self._keyframed: dict = {}
        self._played_us: Optional[int] = None
        self._watching = False
        self._closed = False

    def bind(self, conn: Any) -> None:
        """One more handle of this robot's connect (a connection, or connect("teleop")'s own), held weakly, as its stream
        holds it: a console whose decoder lost its place in a video asks a keyframe, the next video frame of that
        episode (marked_observe.force), and a connection dropped without close() must still be collected
        (seat._give_back)."""
        with self._lock:
            self._handles += 1
            self._conns = [ref for ref in self._conns if ref() is not None] + [weakref.ref(conn)]

    def unbind(self) -> None:
        """One handle of its connect closed: its consoles go with the last."""
        with self._lock:
            self._handles -= 1
            last = self._handles <= 0
        if last:
            self.close()

    def check(self) -> None:
        """The platform's refusal of this robot's teleop, raised (at each observe() and act()) once it refused."""
        if self.refused is not None:
            raise self.refused

    def refuse(self, exc: Exception) -> None:
        """The platform refused this robot's teleop, or took it off its list: no console more, what drove it stopped."""
        self.refused = exc
        with self._lock:
            drove = self.driver != "model"
            by = self.by
        if drove:
            self._drive("stopped", by=by, peer=None, event="stop")
        links, self._links = self._links, None
        if links is not None:
            links.close()

    def headers(self) -> dict:
        """What its stream's upgrade says of it (HEADER)."""
        said = dict()
        said[HEADER] = "1"
        return said

    def stream_opened(self, say: Callable[[dict], bool]) -> None:
        """A worker's stream of one of its connections opened: told who drives now, each change from now - `say` held
        weakly, as a connection's worker goes with it - and what became of each chunk kept for one."""
        ref = weakref.WeakMethod(say)
        with self._lock:
            if ref not in self._says:
                self._says.append(ref)
            told = self._told()
        say(told)
        self.flush()

    def _told(self) -> dict:
        """Under the lock: what a worker is told of who drives."""
        return {"t": "teleop_driver", "driver": self.driver, "by": self.by, "since_us": self.since_us}

    def _tell_workers(self, told: dict) -> None:
        """`told` to each worker it is on, a stream that is down dropped (it is told anew as it opens). Never its stops'
        condition: this is a telling, and nothing waits for it."""
        for ref in list(self._says):
            say = ref()
            if say is None or not say(told):
                with self._lock:
                    if ref in self._says:
                        self._says.remove(ref)

    def push(self, message: dict) -> None:
        """What a worker says on its stream (the stream's thread): its plan stops the robot - one a person drives stays
        driven, one already stopped stopped - and its plan's ask for a person, handed on to every console."""
        kind = message.get("t")
        if kind == "driver" and message.get("by") == "plan" and message.get("driver") == "stopped":
            with self._lock:
                moved = self.driver == "model"
            if moved:
                self._drive("stopped", by="plan", peer=None, event="stop")
        elif kind == "help":
            with self._lock:
                self._help = message
                consoles = self._links.connected() if self._links is not None else []
            for console in consoles:
                self._reply(console, message, label="seq-who")

    def learn(self, plays: dict) -> None:
        """What a connection learned of how its policy plays (connect's answer): its control rate, which stale_s goes
        by."""
        hz = (plays or {}).get("hz")
        if isinstance(hz, (int, float)) and not isinstance(hz, bool) and hz > 0:
            self.hz = float(hz)

    @property
    def stale_s(self) -> float:
        """A chunk whose view (`ref_us`) is older than this as it comes is dropped: STALE_LEAST_S, or its policy's
        STALE_STEPS steps where that is longer."""
        return max(STALE_LEAST_S, STALE_STEPS / self.hz) if self.hz else STALE_LEAST_S

    def metrics(self) -> dict:
        """Its side's numbers (teleop_metrics()): arrive_us, actuate_us, loop_us, written_us; what became of the chunks
        it was sent; how many consoles are connected straight to it."""
        links = self._links
        self.stats.gauge("consoles", links.peers if links is not None else 0)
        return self.stats.snapshot()



    def offer(self, pairing: str, sdp: str) -> None:
        """A console's offer, from the platform: answered straight (teleop_direct.RobotLinks), the answer back through
        the platform (on_answer)."""
        if self._links is None:
            self._links = _direct.RobotLinks(self._from_console, self._answered, self._console)
        self._links.answer(pairing, str(sdp or ""), self.hz or 30.0)
        if not self._watching:
            self._watching = True
            threading.Thread(target=self._watch, daemon=True, name="seq-teleop-watch").start()

    def _answered(self, pairing: str, message: dict) -> None:
        """Its answer to an offer (teleop_direct.RobotLinks), through the platform."""
        if self.on_answer is not None:
            self.on_answer(pairing, message)

    def _console(self, peer: str, what: str) -> None:
        """A console connected straight, or left (teleop_direct's loop): told who drives; the one that drove, gone, stops
        the robot."""
        if what == "open":
            with self._lock:
                self._heard[peer] = time.monotonic()
                asked = self._help
            self._tell(peer)
            if asked is not None:
                self._reply(peer, asked, label="seq-who")
        else:
            with self._lock:
                self._heard.pop(peer, None)
                drove = self.peer == peer
                self._newest.pop(peer, None)
                by = self.by
            if drove:
                self._drive("stopped", by=by, peer=None, event="timeout")

    def _from_console(self, peer: str, label: str, data: bytes, at_us: int) -> None:
        """A whole message a console sent straight (teleop_direct's loop)."""
        try:
            message = _msgpack.unpack(data)
        except Exception:
            return
        if not isinstance(message, dict):
            return
        with self._lock:
            self._heard[peer] = time.monotonic()
        if label == "seq-cmd":
            self._take(message, peer=peer, got_us=at_us)
        elif label == "seq-ctl":
            self._control(peer, message, at_us)
        elif label == "seq-who":
            self._who(peer, message)

    def _control(self, peer: str, message: dict, got_us: int) -> None:
        """A clock tick (answered at once), a keyframe ask."""
        if message.get("t") == "tick":
            self._reply(peer, _clock.tock(message, got_us))
        elif message.get("t") == "kf" and isinstance(message.get("e"), str):
            self._keyframe(message["e"])

    def _keyframe(self, episode: str) -> None:
        """A console's decoder lost its place in `episode`'s video: its next frame a keyframe - twice a second at
        most, every frame after a keyframe being bigger."""
        from . import marked_observe as _marked

        now = time.monotonic()
        if now - self._keyframed.get(episode, 0.0) < 0.5:
            return
        self._keyframed[episode] = now
        while len(self._keyframed) > 16:
            self._keyframed.pop(next(iter(self._keyframed)))
        for ref in list(self._conns):
            conn = ref()
            if conn is not None:
                _marked.force(conn, episode)

    def _reply(self, peer: Any, message: dict, *, label: str = "seq-ctl") -> None:
        """`message` to console `peer`, straight."""
        if isinstance(peer, str) and self._links is not None:
            self._links.reply(peer, message, label=label)



    def _who(self, peer: str, message: dict) -> None:
        """A console's say of who drives, on the reliable channel: take (one at a time), release (the one who drives, or
        from a stop), stop (any console), its heartbeat."""
        kind = message.get("t")
        if kind == "ping":
            self._reply(peer, {"t": "pong", "at_us": message.get("at_us")}, label="seq-who")
        elif kind == "stop":
            with self._lock:
                stopped = self.driver == "stopped"
            if stopped:
                self._tell(peer)
            else:
                self._drive("stopped", by=self._name(message), peer=None, event="stop")
        elif kind == "take":
            with self._lock:
                held, by = self.peer, self.by
            if held is not None and held != peer:
                self._refuse(peer, "another_operator_drives", f"{by or 'another operator'} drives this robot now: it is "
                             "taken once they release it")
            elif held == peer:
                self._tell(peer)
            else:
                self._drive("human", by=self._name(message), peer=peer, event="take")
        elif kind == "release":
            with self._lock:
                held, by, driver = self.peer, self.by, self.driver
            if held is not None and held != peer:
                self._refuse(peer, "another_operator_drives", f"{by or 'another operator'} drives this robot now: only "
                             "they hand it back")
            elif driver == "model":
                self._tell(peer)
            else:
                self._drive("model", by=self._name(message), peer=None, event="release")
        else:
            self._refuse(peer, "unknown_message", f"no console message {kind!r}: ping, take, release, stop")

    @staticmethod
    def _name(message: dict) -> Optional[str]:
        """The name a console said it goes by, 80 characters at most."""
        by = message.get("by")
        return by[:80] if isinstance(by, str) and by else None

    def _state(self, peer: Optional[str]) -> dict:
        return {"t": "driver", "driver": self.driver, "by": self.by, "since_us": self.since_us, "yours": peer == self.peer
                and peer is not None, "lost_s": LOST_S}

    def _tell(self, peer: str) -> None:
        """Who drives, to one console."""
        with self._lock:
            said = self._state(peer)
        self._reply(peer, said, label="seq-who")

    def _refuse(self, peer: str, reason: str, why: str) -> None:
        with self._lock:
            said = {"t": "refused", "reason": reason, "why": why, "driver": self.driver, "by": self.by,
                    "since_us": self.since_us}
        self._reply(peer, said, label="seq-who")

    def _drive(self, driver: str, *, by: Optional[str], peer: Optional[str], event: str) -> None:
        """Who drives from now, told to every console and said to the platform: a chunk not played is no one's."""
        with self._lock:
            self.changes += driver != self.driver
            self.driver, self.by, self.peer, self.since_us = driver, by, peer, _clock.now_us()
            gone = self._from if self._fresh else None
            self._chunk, self._fresh, self._from = None, False, None
            if driver == "human":
                self._help = None
            consoles = self._links.connected() if self._links is not None else []
            told = [(c, self._state(c)) for c in consoles]
            worker = self._told()
        if gone is not None:
            self._fate(gone, "not_driving")
        for console, said in told:
            self._reply(console, said, label="seq-who")
        self._tell_workers(worker)
        self.flush()
        if self.on_event is not None:
            self.on_event({"event": event, "operator": by, "at": time.time()})

    def _watch(self) -> None:
        """A driving console silent for LOST_S: the robot stops (timeout)."""
        while not self._closed:
            time.sleep(_WATCH_S)
            with self._lock:
                peer, by = self.peer, self.by
                quiet = peer is not None and time.monotonic() - self._heard.get(peer, 0.0) > LOST_S
            if quiet:
                self._drive("stopped", by=by, peer=None, event="timeout")



    def _take(self, message: dict, *, peer: str, got_us: int) -> None:
        """A person's chunk: kept as the newest - or dropped as no newer than the newest kept from `peer` ("old"), as
        made from a view older than stale_s ("stale"), or as from a console that does not drive it ("not_driving") - and
        `peer` told which; what became of it kept for its record (_fate)."""
        number = _micros(message.get("id"))
        sent = {"peer": peer, "id": number, "sent_us": _micros(message.get("sent_us")),
                "off_us": _micros(message.get("off_us")), "ref_us": _micros(message.get("ref_us")),
                "ref_n": _micros(message.get("ref_n")), "got_us": got_us, "chunk": message.get("chunk")}
        if sent["sent_us"] is not None and sent["off_us"] is not None:
            self.stats.sample("arrive_us", got_us - (sent["sent_us"] + sent["off_us"]))
        self.stats.count("commands_received")

        made = sent["ref_us"] if sent["ref_us"] is not None else (
            sent["sent_us"] + sent["off_us"] if sent["sent_us"] is not None and sent["off_us"] is not None else None)
        superseded = None
        with self._lock:
            newest = self._newest.get(peer)
            if number is not None and newest is not None and number <= newest:
                did = "old"
            elif made is not None and got_us - made > self.stale_s * 1e6:
                did = "stale"
            elif self.driver == "human" and peer == self.peer:
                did = "kept"
                superseded = self._keep(sent)
            else:
                did = "not_driving"
        if number is not None:
            self._reply(peer, {"t": "got", "id": number, "got_us": got_us, "did": did})
        if superseded is not None:
            self._fate(superseded, "superseded")
        if did != "kept":
            self._fate(sent, did)
        self.flush()

    def _keep(self, sent: dict) -> Optional[dict]:
        """Under the lock: `sent` the chunk act() hands back next - the one it takes the place of, never played,
        returned."""
        superseded = self._from if self._fresh else None
        self._chunk, self._fresh, self._from = sent["chunk"], True, sent
        if sent["id"] is not None:
            self._newest[sent["peer"]] = sent["id"]
        return superseded

    def _fate(self, sent: dict, did: str, place: Optional[tuple] = None, played_us: Optional[int] = None) -> None:
        """What became of a chunk - "played" at `place` (its episode and step), "superseded" by a newer one before any
        act() took it, or dropped ("old", "stale", "not_driving") - counted, and queued for its record (flush)."""
        self.stats.count({"played": "commands_played", "superseded": "commands_superseded", "old": "commands_dropped",
                          "stale": "commands_expired"}.get(did, "commands_not_driving"))
        episode, step = place[:2] if place else (None, None)
        self._said.append({"t": "teleop_command", "did": did, "path": "direct", "id": sent.get("id"),
                           "chunk": sent.get("chunk"), "by": self.by, "peer": sent.get("peer"), "episode": episode,
                           "step": step, "sent_us": sent.get("sent_us"), "off_us": sent.get("off_us"),
                           "ref_us": sent.get("ref_us"), "ref_n": sent.get("ref_n"), "got_us": sent.get("got_us"),
                           "played_us": played_us})

    def _sink_to(self, say: Optional[Callable[[dict], bool]]) -> None:
        """Where what became of each chunk goes from now: the handle that observed or acted last - the one whose episode
        it belongs in - held weakly."""
        if say is not None:
            self._sink = weakref.WeakMethod(say)

    def flush(self) -> None:
        """What became of each chunk, said to its record - kept for the next stream while none is open. With no lock
        held."""
        while self._said:
            say = self._sink() if self._sink is not None else None
            if say is None:
                return
            try:
                message = self._said[0]
            except IndexError:
                return
            if not say(message):
                return
            try:
                self._said.popleft()
            except IndexError:
                return



    def answer(self, place: Optional[tuple] = None) -> tuple:
        """(whether act() answers here, what): its model's - (False, None) - else a person's newest chunk not handed
        back yet, or `hold`. `place`: (its episode, the step it acts at, where its record goes) - where the chunk is said
        to have been played."""
        self._sink_to(place[2] if place and len(place) > 2 else None)
        with self._lock:
            answered = self._answer(place)
        self.flush()
        return answered

    def after(self, asked: int, place: Optional[tuple] = None) -> tuple:
        """What act() hands back of its model's answer to an act that went at `asked` (`changes` as it went), as
        answer() says it: (False, None) - the answer - while its model drove all along; else a person's newest chunk not
        handed back yet, or `hold` - `hold` too once its model drives again: that answer was asked before a stop, or a
        person's taking it, and is no one's."""
        with self._lock:
            if self.changes == asked:
                return False, None
            here, out = self._answer(place)
            answered = True, out if here else self._held()
        self.flush()
        return answered

    def _answer(self, place: Optional[tuple]) -> tuple:
        """answer(), under the lock."""
        if self.driver == "model":
            return False, None
        if self.driver == "human" and self._fresh:
            self._fresh = False
            self.chunks += 1
            sent = self._from or {}
            played_us = _clock.now_us()
            if sent.get("got_us") is not None:
                self.stats.sample("actuate_us", played_us - sent["got_us"])
            if sent.get("ref_us") is not None:
                self.stats.sample("loop_us", played_us - sent["ref_us"])
            self._fate(sent, "played", place, played_us)
            self._played_us = played_us
            return True, self._chunk
        return True, self._held()

    def held(self) -> Any:
        """`hold`: what act() hands back with nothing else to."""
        with self._lock:
            return self._held()

    def written(self) -> None:
        """The robot's code wrote what act() last handed back of a person's to its motors: written_us, from act() handing
        it back - the last step of a command's way only the robot's own code can see. Once a chunk.
"""
        with self._lock:
            played_us, self._played_us = self._played_us, None
        if played_us is not None:
            self.stats.sample("written_us", _clock.now_us() - played_us)

    def _held(self) -> Any:
        """`hold`, under the lock: the one given, else the model's last answer emptied - {} before any."""
        if self._hold is not _EMPTY:
            return self._hold
        return {} if self._last is _EMPTY else emptied(self._last)

    def answered(self, outputs: Any) -> None:
        """Its model's answer to an act: what the default hold is made from."""
        with self._lock:
            self._last = outputs



    def frames(self, episode: str, inputs: Any, n: int, t_us: int) -> None:
        """A step's camera frames as observe() was handed them, to the consoles that take them as video tracks: nothing
        for none, so a robot no such console watches copies nothing."""
        links = self._links
        if links is not None and links.tracks > 0:
            raw = _direct.videos(inputs)
            if raw:
                links.frames(episode, raw, n, t_us)

    def watched(self) -> bool:
        """Whether any console is connected to see what it observes."""
        links = self._links
        return links is not None and links.peers > 0

    def observed(self, episode: str, n: int, t_us: int, value: Any, sink: Optional[Callable[[dict], bool]] = None) -> None:
        """One step the robot observed - its number `n` in the episode, captured at `t_us` (this robot's clock) -
        `value` with its Video, Depth and Tactile items encoded: straight to every console connected (its arrays on one
        channel, and on another the step less its cameras, which go by video tracks, while it has a Depth or Tactile item).
        Nothing for none - from the robot's observe() thread. `sink`: where what became of its chunks goes from now."""
        self._sink_to(sink)
        links = self._links
        if links is None or links.peers <= 0:
            return
        rest = _direct.without_video(value)
        state, more = _direct.split_step(rest)
        try:
            links.step({"state": _msgpack.pack({"e": episode, "n": n, "t_us": t_us, "v": state, "video": more})
                        if state is not None and (state or not more) else None,
                        "rest": _msgpack.pack({"e": episode, "n": n, "t_us": t_us, "v": rest}) if more else None})
            self.stats.count("frames_sent")
        except Exception:
            pass

    def close(self) -> None:
        """Its link to the platform and its direct connections closed, as the last handle of its connect closes."""
        self._closed = True
        links, self._links = self._links, None
        if links is not None:
            links.close()
        if self.on_close is not None:
            self.on_close()
