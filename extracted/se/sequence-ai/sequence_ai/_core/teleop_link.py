"""
A robot's link to its pairing server, for the consoles that would reach it: GS's platform - a
connect() with "teleop" among its names - or a server of your own, seq teleop serve (teleop_serve.py), reached by its
address. It keeps one long-poll open, and that is all of its teleoperation that goes through either: the two speak the
same requests, so the robot has one way of being reached.

In one sentence: the robot asks where its link is (POST /v1/act/connect, model "teleop": no worker, no seat) → it
long-polls there (POST /v1/robots/link, WAIT_S a round), which says it is online, brings each console's offer and says
whether its list still names teleop, its Record is on, and where a MoQ relay takes its steps for the people watching → each offer is answered by the robot straight (teleop_robot.Driven.offer), its
answer going back through the platform (POST /v1/teleop/answer) → from then on the console and the robot talk to each
other; each change of who drives is said to the platform's audit (POST /v1/robots/teleop-events), on a thread of its own.
WHY a long-poll: a robot with no policy has no worker to be reached through, and every robot on one path is one path to
keep right.
WHY a refusal ends it and a failure does not: a key or a list says no until a person changes it, and the robot is told
at its next observe() or act(); a network that went away comes back, and the robot's loop runs on meanwhile.
"""
from __future__ import annotations

import collections
import logging
import threading
import uuid
from typing import Any, Optional

from sequence_ai.errors import InternalError, SequencesError, Unavailable
from sequence_ai._core.teleop_record import Recording
from sequence_ai._core.transport import Transport, _version

NAME = "teleop"
CONNECT = "/v1/act/connect"
LINK = "/v1/robots/link"
ANSWER = "/v1/teleop/answer"
EVENTS = "/v1/robots/teleop-events"

WAIT_S = 20






READY_WAIT_S = 0
_SLACK_S = 10.0
_CALL_S = 10.0

BACKOFF_S = 0.5
BACKOFF_MOST_S = 5.0

_EVENTS_KEPT = 256
_EVENTS_AGAIN_S = 2.0
_ANSWER_TRIES = 3
_PAIRINGS_KEPT = 64
_EVENTS_A_REQUEST = 64
_log = logging.getLogger("sequence_ai.teleop")

_PASSING = (Unavailable, InternalError)


class RobotLink:
    """One connect()'s link to its pairing server (module docstring): start() it; its threads end with close().
    `own`: a server of your own at `base_url` (seq teleop serve), `api_key` its token - sent as given, nothing of the
    account's (Transport's own); else the platform, with the robot's key."""

    def __init__(self, api_key: Optional[str], base_url: Optional[str], driven: Any, *, own: bool = False) -> None:
        self._api_key = api_key
        self._own = own
        self.where = f"the teleop server at {base_url}" if own else "the platform"
        self._gateway = self._transport(base_url, _CALL_S, robot_of=NAME)
        self._link: Optional[Transport] = None
        self._driven = driven
        self.recording = Recording()
        self.session = uuid.uuid4().hex
        self._lock = threading.Lock()
        self._closing = threading.Event()
        self._closed = False
        self._answered = threading.Event()
        self._wake = threading.Event()
        self._events: list = []


        self._flushing = threading.Lock()
        self._pairings: "collections.OrderedDict[str, bool]" = collections.OrderedDict()
        driven.on_answer, driven.on_event, driven.on_close = self._answer, self._event, self.close

    def start(self) -> None:
        threading.Thread(target=self._poll, daemon=True, name="seq-teleop-link").start()
        threading.Thread(target=self._report, daemon=True, name="seq-teleop-events").start()

    def _transport(self, base_url: Optional[str], timeout_s: float, robot_of: Optional[str] = None) -> Transport:
        if self._own:
            return Transport(api_key=self._api_key or None, base_url=base_url, timeout_s=timeout_s, own=True)
        return Transport(api_key=self._api_key, base_url=base_url, timeout_s=timeout_s, robot_of=robot_of)

    def wait_ready(self, timeout_s: Optional[float]) -> None:
        """Until its server answered this link's first round, its Record on where that answer says so, or refused it.
        Unavailable past `timeout_s`."""
        if not self._answered.wait(timeout_s):
            raise Unavailable(f"{self.where} did not answer this robot's link within {timeout_s} s", hint="ask again")

    def _open(self) -> Transport:
        """Where this robot's link is: its server's answer to a connect naming teleop."""
        said = self._gateway.post(CONNECT, {"model": NAME, "session": self.session})
        url = (said.get("teleop") or {}).get("link_url")
        if not isinstance(url, str) or not url:
            raise InternalError(f"{self.where}'s answer named no link for this robot")
        return self._transport(url, WAIT_S + _SLACK_S)

    def _poll(self) -> None:
        """Its rounds, one after another, for as long as the robot is connected."""
        backoff = 0.0
        while not self._closing.is_set():
            try:
                self._round()
            except Exception as exc:
                if self._closing.is_set():
                    return
                if isinstance(exc, SequencesError) and not isinstance(exc, _PASSING):
                    self._refused(exc)
                    return
                if not backoff:
                    _log.warning("this robot's link to %s failed: %s - asked again; a console cannot reach the "
                                 "robot meanwhile", self.where, exc)
                backoff = min(BACKOFF_MOST_S, backoff * 2 or BACKOFF_S)
                self._closing.wait(backoff)
                continue
            backoff = 0.0

    def _round(self) -> None:
        """One round of the long-poll: what it brought handed on."""
        if self._link is None:
            self._link = self._open()


        wait_s = READY_WAIT_S if not self._answered.is_set() else WAIT_S
        body = self._link.post(LINK, {"session": self.session, "sdk": _version(), "direct": True, "wait_s": wait_s})
        settings = body.get("settings") or {}
        self.recording.configure(settings.get("record"), settings.get("robot"))



        self._answered.set()
        self._driven.moq(settings.get("moq"))
        self._take(body.get("offers") or ())

    def _refused(self, exc: SequencesError) -> None:
        """The platform says no until a person changes it: told at the robot's next observe() or act()."""
        if not self._closing.is_set():
            self._driven.refuse(exc)
        self._answered.set()

    def _take(self, offers: Any) -> None:
        """Each console's offer, answered once, however many rounds brought it."""
        for offer in offers:
            pairing, sdp = offer.get("pairing"), offer.get("sdp")
            if isinstance(pairing, str) and isinstance(sdp, str) and pairing not in self._pairings:
                self._pairings[pairing] = True
                while len(self._pairings) > _PAIRINGS_KEPT:
                    self._pairings.popitem(last=False)
                self._driven.offer(pairing, sdp, offer.get("ice_servers"))

    def _answer(self, pairing: str, message: dict) -> None:
        """The robot's answer to an offer, or why it has none (the direct connection's loop: no request is waited for
        on it)."""
        body = {"pairing": pairing, **{k: message[k] for k in ("sdp", "nat", "error") if k in message}}
        threading.Thread(target=self._send_answer, args=(body,), daemon=True, name="seq-teleop-answer").start()

    def _send_answer(self, body: dict) -> None:
        for n in range(1, _ANSWER_TRIES + 1):
            try:
                self._gateway.post(ANSWER, body)
                return
            except _PASSING as exc:
                if n == _ANSWER_TRIES or self._closing.wait(BACKOFF_S * n):
                    _log.warning("a console's offer was answered but %s did not take the answer: %s", self.where, exc)
                    return
            except (SequencesError, RuntimeError) as exc:
                _log.warning("a console's offer was answered but %s did not take the answer: %s", self.where, exc)
                return

    def _event(self, event: dict) -> None:
        """A change of who drives, for the platform's audit."""
        with self._lock:
            self._events.append({**event, "session": self.session})
            del self._events[:-_EVENTS_KEPT]
        self._wake.set()

    def _report(self) -> None:
        """What changed, said as it changes - asked again while the platform is out of reach."""
        while not self._closing.is_set():
            self._wake.wait()
            self._wake.clear()
            while self._events and not self._closing.is_set():
                if not self._flush(_CALL_S):
                    self._closing.wait(_EVENTS_AGAIN_S)

    def _flush(self, timeout_s: float) -> bool:
        """What is waiting said, up to a request's worth, one flush at a time: False while the platform is out of reach,
        or another flush outlasted `timeout_s`."""
        if not self._flushing.acquire(timeout=timeout_s):
            return False
        try:
            with self._lock:
                batch = self._events[:_EVENTS_A_REQUEST]
            if not batch:
                return True
            try:
                self._gateway.post(EVENTS, {"events": batch}, timeout_s=timeout_s)
            except _PASSING:
                return False
            except (SequencesError, RuntimeError) as exc:
                _log.warning("%s did not take this robot's teleop events: %s", self.where, exc)
            with self._lock:
                del self._events[:len(batch)]
            return True
        finally:
            self._flushing.release()

    def close(self) -> None:
        """The robot's connection closed: what it recorded written to its file and the file closed first
        (Recording.close); then what is left of its events said if the platform answers soon, and its threads ended."""
        with self._lock:
            if self._closed:
                return
            self._closed = True
        try:
            self.recording.close()
        finally:
            self._closing.set()
            self._wake.set()
            self._flush(2.0)
            link, self._link = self._link, None
            if link is not None:
                link.close()
            self._gateway.close()
