"""
A person's console for one robot: sequence_ai.teleop(policy, robot=, key=) - with the robot's own
key - finds the worker the robot is on (POST /v1/teleop/connect) and opens one connection to it (GET /teleop), on which
it watches the robot, takes it, drives it, hands it back or stops it.

In one sentence: teleop() → the platform answers where the robot is now - its worker's address, the certificate to
check it by, a token of the robot's session - and who drives it → one WebSocket to that worker (worker_stream's, path
/teleop), pinged every HEARTBEAT_S - a driving console silent for 3 s stops its robot → take(), release() and stop()
each said and answered with who drives then (Conflict while another person drives), send(chunk) each chunk to the robot
at once - what its act() hands back, in its policy's answers' form - stream() each step the robot observes, as its
observe() made it, requests() each time its policy's plan asks for a person.
WHY one hop to the worker: the robot's frames and acts are already there - a person's chunk reaches the robot in one
trip. {the user 10-27: "we should do 1 jump by direct connnect gpu to telloerpator"; "key doesnt need to change key is
the same robot key"}
"""
from __future__ import annotations

import logging
import queue
import threading
import time
from typing import Any, Iterator, Optional

from ..errors import Conflict, InvalidRequest, MissingPackage, Unavailable
from . import worker_stream as _stream
from .pinned_tls import build_pinned_ssl_context

PATH = "/teleop"
CONNECT = "/v1/teleop/connect"

HEARTBEAT_S = 0.5

_FRAMES_KEPT = 64
_REFUSALS_KEPT = 16
_log = logging.getLogger("sequence_ai.teleop")


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

    def __init__(self, answer: dict, *, operator: Optional[str], robot: Optional[str], timeout_s: float) -> None:
        self.policy: Optional[str] = answer.get("policy")

        self.robot: Optional[str] = answer.get("robot") or robot
        self.session: Optional[str] = answer.get("session")
        self.operator = operator
        self._lock = threading.Condition()
        self._driver = dict(answer.get("driver") or {"driver": "model", "by": None, "since": None})
        self._yours = False

        self.robot_connected: Optional[bool] = None
        self._refusals: list = []
        self.refused: Optional[dict] = None
        self.rtt_ms: Optional[float] = None

        self._help: queue.Queue = queue.Queue()
        self._frames: queue.Queue = queue.Queue()
        self._closed: Optional[str] = None
        self._opened = False
        self._sent = 0
        token = answer.get("token")
        if not token or not answer.get("worker_url"):
            raise InvalidRequest("the platform's answer names no worker for this robot")
        verify = build_pinned_ssl_context(answer.get("cert_fingerprint"))
        headers = {"Authorization": f"Bearer {token}", **({"X-Seq-Operator": operator} if operator else {})}
        try:
            self._stream = _stream.open_stream(answer["worker_url"], verify, headers, timeout_s=timeout_s,
                                               path=PATH, on_push=self._said,
                                               on_end=self._ended)
        except _stream.StreamClosed as exc:
            raise Unavailable(f"the robot's worker did not take this console: {exc}", hint="ask again: the robot may "
                              "be moving to another worker") from None
        self._pinging = threading.Thread(target=self._heartbeat, daemon=True, name="seq-teleop-heartbeat")
        self._pinging.start()

        with self._lock:
            self._lock.wait_for(lambda: self._opened or self._refusals or self._closed is not None, timeout_s)
            opened, refused, why = self._opened, (self._refusals or [None])[0], self._closed
        if not opened:
            self.close()
            if refused is not None:
                raise Conflict(str(refused.get("why") or "the robot's worker refused this console"),
                               details={"reason": refused.get("reason")})
            raise Unavailable(f"the robot's worker said nothing of the robot: {why or 'no answer in time'}",
                              hint="ask again")



    def _said(self, message: dict) -> None:
        """One message of its worker's (the stream's thread): steps and help to their queues, the rest kept."""
        kind = message.get("t")
        if kind == "frames":
            self._frames.put(message)
            while self._frames.qsize() > _FRAMES_KEPT:
                try:
                    self._frames.get_nowait()
                except queue.Empty:
                    break
            return
        if kind == "help":
            self._help.put(message)
            return
        with self._lock:
            if kind == "driver":
                self._driver = {k: message.get(k) for k in ("driver", "by", "since")}
                self._yours = bool(message.get("yours"))
                self._opened = True
            elif kind == "robot":
                self.robot_connected = bool(message.get("connected"))
            elif kind == "refused":
                self.refused = message
                self._refusals.append(message)
                del self._refusals[:-_REFUSALS_KEPT]
                if message.get("reason") == "key_revoked":
                    _log.warning("%s", message.get("why"))
            elif kind == "pong" and isinstance(message.get("at"), (int, float)):
                self.rtt_ms = (time.time() - float(message["at"])) * 1000.0
            self._lock.notify_all()

    def _ended(self, why: str) -> None:
        with self._lock:
            if self._closed is None:
                self._closed = why
            self._yours = False
            self._lock.notify_all()
        self._help.put(None)
        self._frames.put(None)

    def _heartbeat(self) -> None:
        while self._closed is None:
            try:
                self._stream.send_message({"t": "ping", "at": time.time()})
            except _stream.StreamClosed:
                return
            time.sleep(HEARTBEAT_S)



    def _send(self, message: dict) -> None:
        try:
            self._stream.send_message(message)
        except _stream.StreamClosed as exc:
            raise Unavailable(f"this console's connection to the robot's worker ended: {exc}",
                              hint="connect again (sequence_ai.teleop)") from None

    def _say(self, kind: str, done, timeout_s: float) -> dict:
        """Say `kind` and wait for its worker's answer: who drives once `done()` - or the refusal that came after it
        (Conflict)."""
        with self._lock:
            before = len(self._refusals)
        self._send({"t": kind})
        end = time.monotonic() + timeout_s
        with self._lock:
            while True:
                if done():
                    return dict(self._driver)
                if len(self._refusals) > before:
                    refused = self._refusals[-1]
                    raise Conflict(str(refused.get("why") or "the robot's worker refused it"),
                                   details={k: refused.get(k) for k in ("reason", "driver", "by", "since")})
                if self._closed is not None:
                    raise Unavailable(f"this console's connection to the robot's worker ended: {self._closed}",
                                      hint="connect again (sequence_ai.teleop)")
                left = end - time.monotonic()
                if left <= 0:
                    raise Unavailable(f"the robot's worker did not answer {kind} within {timeout_s} s")
                self._lock.wait(left)

    def take(self, timeout_s: float = 5.0) -> dict:
        """Drive the robot from this console: from now its act() hands back the chunks sent here (send) and nothing of
        its model's. One person drives a robot at a time: Conflict while another does, saying who (its details'
        "by"). Who drives then: {"driver": "human", "by": this console's operator name, "since"}."""
        return self._say("take", lambda: self._yours and self._driver.get("driver") == "human", timeout_s)

    def send(self, chunk: Any) -> None:
        """One action chunk to the robot, at once - what its next act() hands back, in the form its policy's answers
        have (a dict of arrays: the same keys and shapes), played once: with none newer, its act() hands back its hold
        and it stays where it is. Only while this console drives it (take)."""
        with self._lock:
            if not self._yours:
                raise Conflict("this console does not drive the robot: take() it first",
                               details={"reason": "not_driving", **self._driver})
            self._sent += 1
            number = self._sent
        self._send({"t": "chunk", "chunk": chunk, "id": number})

    def release(self, timeout_s: float = 5.0) -> dict:
        """Hand the robot back to its model - from this console's drive, or from a stop. Conflict while another person
        drives it."""
        return self._say("release", lambda: self._driver.get("driver") == "model", timeout_s)

    def stop(self, timeout_s: float = 5.0) -> dict:
        """Stop the robot where it is - whoever drives it, a person or its model: its act() hands back its hold until
        a console takes or releases it."""
        return self._say("stop", lambda: self._driver.get("driver") == "stopped", timeout_s)

    @property
    def driver(self) -> dict:
        """Who drives the robot now, as its worker last said: {"driver": "model" | "human" | "stopped", "by": the
        operator's name, "plan", or None, "since": its epoch second, or None}."""
        with self._lock:
            return dict(self._driver)

    @property
    def driving(self) -> bool:
        """Whether this console drives the robot now."""
        with self._lock:
            return self._yours

    def stream(self) -> Iterator[dict]:
        """Each step the robot observes, as it comes: {"episode", "seq", "observation"} - the observation as its observe()
        made it, a Video's, Depth's or Tactile's item decoded back to its array (sequence-ai[observe]; without it, as it
        travels). A console far behind skips to the newest, from a video's next keyframe. Ends with the connection."""
        marked = _codec()
        streams: dict = {}
        while True:
            message = self._frames.get()
            if message is None:
                self._frames.put(None)
                return
            episode = message.get("episode")
            for seq, inputs in message.get("steps") or ():
                observation = inputs
                if marked is not None:
                    try:
                        observation = marked.decode(inputs, streams.setdefault(episode, marked.Streams()))
                    except marked.NeedsKeyframe:
                        continue
                    while len(streams) > 8:
                        streams.pop(next(iter(streams)))
                yield {"episode": episode, "seq": seq, "observation": observation}

    def requests(self) -> Iterator[dict]:
        """Each time the robot's policy asks for a person (a @seq.plan returning seq.ask_human), as its worker tells this
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
        """End this console's connection: a robot it drove stops (its worker's rule for a console that goes)."""
        self._stream.close("the console closed its connection")

    def __enter__(self) -> "Teleop":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
