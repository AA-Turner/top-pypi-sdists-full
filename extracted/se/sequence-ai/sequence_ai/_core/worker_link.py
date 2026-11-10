"""
The robot's stream as its worker transport keeps it:
opened as the robot connects, its upgrade's answer saying what the worker takes; every request of the robot's waiting for
it while it opens, and for the next one after it breaks; what stopped it said - a network that lets no WebSocket through,
a worker built before it took one, a worker that cannot be reached - and its observation posts queued on it with no thread
waiting (submit_observe), the worker asked which it took when nothing else says it (ask_taken). The stream itself is
worker_stream's; the transport's own state - its lock and what is on its way - is the transport's.
"""
from __future__ import annotations

import logging
import socket
import ssl
import threading
import time
from typing import Any, Callable, Optional

import httpx

from ..errors import AuthError, CertPinError, InvalidRequest, StreamRefused
from . import msgpack_io as _msgpack
from . import observe_stream as _observe
from . import teleop_robot as _teleop
from . import worker_stream as _stream
from .transport import Transport






OPEN_TRIES_S = (5.0, 10.0)

_TELEOP_AGAIN_S = 0.5

_log = logging.getLogger("sequence_ai._core.direct")

_NO_WEBSOCKET = ("a robot's requests reach its worker on one WebSocket (wss, GET /stream), and the network between this "
                 "machine and its worker did not let it through")
_MAY_BE_THE_NETWORK = ("a robot's key that was not revoked may still meet this: a proxy on the way that refuses the "
                       "WebSocket (wss) a robot reaches its worker on")


def _gone_cert(exc: BaseException) -> bool:
    """Whether an opening failed on the TLS check refusing the worker's certificate."""
    seen = 0
    cause: Optional[BaseException] = exc
    while cause is not None and seen < 8:
        if isinstance(cause, ssl.SSLCertVerificationError):
            return True
        cause, seen = cause.__cause__ or cause.__context__, seen + 1
    return False


def why_not_opened(exc: BaseException) -> str:
    """What stopped the stream from opening, in words that carry no secret."""
    if _gone_cert(exc):
        return "the worker's certificate was refused"
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return "the worker did not answer in time"
    if isinstance(exc, _stream.StreamClosed):
        return str(exc)
    if isinstance(exc, OSError):
        return "the worker could not be reached"
    return f"opening it failed with {type(exc).__name__}"


def _built_before() -> InvalidRequest:
    """What a robot is told of a worker built before a robot's requests went on its stream alone - never its address."""
    return InvalidRequest("the worker was built before a robot's requests went on one WebSocket alone",
                          hint="`seq deploy` the same code again")


def _refused(exc: _stream.StreamRefused) -> Optional[Exception]:
    """What a robot is told when its stream's upgrade was answered `exc.status`: its secret turned away (AuthError: a new
    worker epoch, DirectConnection connects again) - or a proxy's refusal, which reads the same; a worker built before it
    took a stream; a worker in front of which something answered for it (5xx: None - a worker not reached, as any); anything
    else, a network that lets no WebSocket through."""
    if exc.status in (401, 403):
        return AuthError(f"the worker refused this robot's stream ({exc})", status=exc.status,
                         hint=_MAY_BE_THE_NETWORK)
    if exc.status == 404:
        return _built_before()
    if exc.status >= 500:
        return None
    return StreamRefused(f"{_NO_WEBSOCKET}: the answer was \"{exc}\"", status=exc.status or None,
                         hint="let wss to the policy's workers through this network's proxy or firewall")


class StreamLink:
    """The stream's half of a worker transport (module docstring)."""

    def _ensure_stream(self) -> None:
        """Open the robot's stream to this worker in the background (worker_stream.open_stream), unless one is open or
        opening: its TCP connect, TLS handshake and upgrade, with the robot's Authorization and session, within
        OPEN_TRIES_S a try. What it opened to says what the worker takes (_learn_formats); what stopped it is kept
        (_stream_error, _warm_failed) for the request that waits for it (_route). On its way as an act is
        (_on_its_way): a close() meanwhile closes the stream once it ended."""
        with self._sends:
            if (self._closed or (self._stream is not None and self._stream.alive)
                    or (self._stream_opening is not None and not self._stream_opening.is_set())):
                return
            self._stream_opening = opening = threading.Event()
            self._on_way += 1

        def _open() -> None:
            began, tries = time.monotonic(), 0
            quiet_s, on_quiet = self.quiet if self.quiet is not None else (None, None)
            headers, driven = dict(self._headers), self.teleop
            if driven is not None:
                headers[_teleop.HEADER] = driven.said
            while True:
                tries += 1
                left = self._timeout_s - (time.monotonic() - began)
                bound = min(left, OPEN_TRIES_S[tries - 1]) if tries <= len(OPEN_TRIES_S) else left
                trace = self._warm_trace = self._new_trace()
                try:
                    asked = time.monotonic()
                    stream = _stream.open_stream(self._base, self._verify, headers, timeout_s=max(0.001, bound),
                                                 options=self._stream_options,
                                                 quiet_s=quiet_s, on_quiet=on_quiet,
                                                 on_push=driven.push if driven is not None else None,
                                                 on_end=self._stream_ended if driven is not None else None,
                                                 trace=trace)
                except Exception as exc:
                    took = time.monotonic() - began
                    if isinstance(exc, (TimeoutError, socket.timeout)) and bound < left and not self._closed:
                        continue
                    self._stream_error = (exc if isinstance(exc, CertPinError)
                                          else _refused(exc) if isinstance(exc, _stream.StreamRefused)
                                          else CertPinError("worker certificate is not valid for the name it was "
                                                            "given; refusing to connect") if _gone_cert(exc) else None)
                    self._warm_failed = (str(self._stream_error) if self._stream_error is not None else
                                         f"{why_not_opened(exc)} ({tries} {'try' if tries == 1 else 'tries'} in "
                                         f"{took:.1f} s, the last {trace.stuck()})")
                    _log.debug("the connection to its worker: its stream did not open: %s", self._warm_failed)
                    return
                break
            said = stream.said.get("x-seq-act-formats")
            if _stream.FORMAT not in {part.strip().lower() for part in (said or "").split(",")}:
                stream.close()
                self._stream_error = _built_before()
                self._warm_failed = str(self._stream_error)
                _log.debug("the connection to its worker: its stream did not open: %s", self._warm_failed)
                return
            self._learn_formats(said)
            self.outside.ping_ms = trace.ms("connect_tcp") or (time.monotonic() - asked) * 1000.0
            with self._sends:
                closed = self._closed
                if not closed:
                    self._stream, self._warm_failed, self._stream_error = stream, None, None
            if closed:
                stream.close()
                return
            self._trace_opened(trace)
            self._trace_streamed(began)

        def run() -> None:
            try:
                _open()
            finally:
                opening.set()
                self._done()

        threading.Thread(target=run, daemon=True, name="seq-stream-open").start()

    def _stream_ended(self, why: str) -> None:
        """A teleop robot's stream ended: stopped here while a person drove it (teleop_robot.Driven.ended), and opened
        again _TELEOP_AGAIN_S on while this transport is open - a robot stopped here sends no act that would open it,
        and only on it can a console release it."""
        self.teleop.ended(why)
        if not self._closed:
            timer = threading.Timer(_TELEOP_AGAIN_S, self._ensure_stream)
            timer.daemon = True
            timer.start()

    def _open_stream(self, timeout_s: float) -> "_stream.WorkerStream":
        """The open stream: one that ended opened again, and one opening waited for, `timeout_s` at most. Past that, or
        when it did not open: what its opening met - the worker's refusal, a network that lets no WebSocket through -
        else worker_stream.NotOpened, a worker not reached, which DirectConnection meets as it meets any."""
        stream = self._stream
        if stream is not None and stream.alive:
            return stream
        if stream is not None:
            _log.debug("the stream to its worker ended (%s): opened again", stream.why_closed)
            with self._sends:
                if self._stream is stream:
                    self._stream = None
        self._ensure_stream()
        opening = self._stream_opening
        if opening is not None and not opening.wait(timeout_s):
            raise _stream.NotOpened(f"the stream to the worker did not open in {timeout_s:.1f} s")
        stream = self._stream
        if stream is not None and stream.alive:
            return stream
        if self._stream_error is not None:
            raise self._stream_error
        raise _stream.NotOpened(f"the stream to the worker did not open: "
                                f"{self._warm_failed or 'it ended as it opened'}")

    def _route(self, request: Any) -> "_stream.WorkerStream":
        """The stream a request goes on (worker_stream.StreamRouted): _open_stream, within the request's own bound."""
        bounds = request.extensions.get("timeout") or {}
        return self._open_stream(bounds.get("connect") or self._timeout_s)

    @property
    def streaming(self) -> bool:
        """Whether the robot's stream to this worker is open now."""
        stream = self._stream
        return stream is not None and stream.alive

    @property
    def latest_only(self) -> bool:
        """Whether, on the robot's stream, an observation a newer one stood behind before it was posted is left out: the
        worker's policy reads each act's latest observation alone (x-seq-latest/1). Not for a teleop robot: its operators
        watch every frame, and what it is driven by may read each."""
        return self._latest is True and self.teleop is None

    def room(self, timeout_s: float = 0.0) -> bool:
        """Whether the robot's stream has room for another observation post (worker_stream.WorkerStream.room), waited
        for up to `timeout_s`. None while it opens: the observations wait where they were handed over and go as it opens,
        in turn, the act behind them - as a post that opened nothing would. True with none open or opening: the post
        opens it, or meets what stops it (post_observe). {dev 10-30, worker 4: an act right after a robot's first
        observation took 6.2 s against 190 ms: that post, queued as the stream opened, waited for a word it was taken
        that only the act's answer would bring, and the act waited for the post}"""
        stream = self._stream
        if stream is not None and stream.alive:
            return stream.room(timeout_s)
        opening = self._stream_opening
        if opening is None or opening.is_set():
            return True
        opening.wait(timeout_s)
        return False

    def submit_observe(self, body: bytes, episode: Optional[str] = None, *,
                       done: Callable[[Optional[BaseException], Optional[float]], None]) -> bool:
        """One observation post queued on the robot's stream now, behind every request handed over before it, never
        waiting (observe_stream queues them under its lock, in the order it picks them): True, and `done(error,
        write_s)` called once it is taken - None, and how long its writing took - or refused or lost: what post_observe
        raises. False while no stream is open: the post waits for one by post_observe."""
        stream = self._stream
        if stream is None or not stream.alive:
            return False
        headers = [["content-type", _msgpack.MEDIA_TYPE]]
        if self.switched is not None and episode == self.switched:
            headers.append([_observe.SWITCHED_HEADER, "1"])
        self._used_at = time.monotonic()

        def finished(pending: Any) -> None:
            try:
                if pending.error is not None:
                    raise httpx.ReadError(f"the observations' post on the stream did not land: {pending.error}")
                if pending.answer is not None:
                    status, said, content = pending.answer
                    r = httpx.Response(status, headers=said, content=content,
                                       request=httpx.Request("POST", f"{self._base}{_observe.PATH}"))
                    self._learn(r)
                    Transport._unwrap(r)
                took = (pending.sent_at - pending.began_at) if pending.sent_at and pending.began_at else None
                done(None, took)
            except Exception as exc:
                done(exc, None)
            finally:
                self._done()

        with self._sends:
            self._on_way += 1
        try:
            stream.submit("POST", _observe.PATH, headers, body, silent=True, on_done=finished, key=episode)
        except _stream.StreamClosed:
            self._done()
            return False
        return True

    def ask_taken(self) -> None:
        """Ask the worker, on the robot's stream, which observation posts it took: a ping behind them, whose answer
        names the last served (worker_stream THROUGH_HEADER) - for a stream that waits on them with no act coming
        (observe_stream.flush). Nothing with no stream open."""
        stream = self._stream
        if stream is not None and stream.alive:
            try:
                stream.submit("GET", "/ping", [], b"")
            except _stream.StreamClosed:
                pass

    def post_heartbeat(self, body: dict) -> None:
        """The robot's SDK heard from (heartbeat.py): one message on the robot's stream, ahead of everything waiting - no
        request, so nothing it answers and no place among the numbered requests it could take from a frame still
        waiting (X-Seq-Stream-Through). Nothing while no stream is open: a heartbeat not sent is one not heard, which is
        what its worker says of a robot it cannot hear. It is counted in nothing of the acts'."""
        stream = self._stream
        if stream is not None and stream.alive:
            try:
                stream.send_message({"t": "heartbeat", **body})
            except _stream.StreamClosed:
                pass
