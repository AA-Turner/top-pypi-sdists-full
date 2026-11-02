"""
The data plane of a direct connection (direct.py): one robot's stream to a single worker (worker_link.py), its TLS
checked by the pinned fingerprint (pinned_tls.py) or by the CAs for the name the platform gave, and a worker that stopped
answering told apart from one that refused - _WorkerGone, which DirectConnection folds back through the gateway.

WHY its own module: direct.py had grown to 1966 lines, past the ~1500 a file may have
 
; the worker's side of a connection is one responsibility, the gateway's side another.
"""

from __future__ import annotations

import contextlib
import hmac
import logging
import math
import queue
import socket
import threading
import time
from collections import deque
from typing import Any, Callable, Optional

import httpx

from ..errors import CertPinError, SequencesError, StreamRefused, Unavailable
from . import msgpack_io as _msgpack
from . import observe_stream as _observe
from . import outside as _outside
from . import wifi_power
from . import worker_stream as _stream
from .worker_link import StreamLink
from .pinned_tls import build_pinned_ssl_context
from .reporting import error_of
from .rid import HEADER as _RID_HEADER
from .transport import Transport
from .warn import warn



_log = logging.getLogger("sequence_ai._core.direct")






_WORKER_GONE = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.RemoteProtocolError,
    httpx.PoolTimeout,
)



_STILL_OPENING = "still opening"













_TCP_CONGESTION = getattr(socket, "TCP_CONGESTION", None)

_EPISODE_END_S = 5.0





_OBSERVE_STALL_S = 5.0
_SLOWEST_UPLINK_BPS = 125_000
















_WARM_EVERY_S = 0.1
_WARM_FOR_S = 60.0


_BIG_UPLOAD = 256 * 1024

_SLOW_START_AFTER_IDLE = "/proc/sys/net/ipv4/tcp_slow_start_after_idle"

_RESTART_SAID = threading.Event()
_RESTART_LOCK = threading.Lock()






_KEEPALIVE_IDLE_S, _KEEPALIVE_EVERY_S, _KEEPALIVE_ASKS = 20, 5, 3


def _bbr_options() -> Optional[list]:
    """The socket option that has a connection use BBR, when this machine lets a socket take it; else None. Tried on a
    socket of its own first: httpcore sets its socket options as it connects, and one it cannot set fails the connect.
    An unprivileged process may set BBR whenever its kernel has the tcp_bbr module loaded (BBR is not restricted to
    net.ipv4.tcp_allowed_congestion_control); Ubuntu does not load it by default, and the try fails with ENOENT. A
    machine whose `socket` has no TCP_CONGESTION (not Linux) has nothing to try."""
    if _TCP_CONGESTION is None:
        return None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.IPPROTO_TCP, _TCP_CONGESTION, b"bbr")
    except OSError:
        return None
    return [(socket.IPPROTO_TCP, _TCP_CONGESTION, b"bbr")]


def _keepalive_options() -> list:
    """The socket options that turn on TCP keepalive - SO_KEEPALIVE, and its idle, interval and count where this
    machine names them (TCP_KEEPIDLE on Linux and Windows, TCP_KEEPALIVE on macOS) - each tried on a socket of its own
    first, as _bbr_options does: httpcore fails the connect on an option it cannot set, so one this machine refuses is
    left out and the rest kept; none at all where SO_KEEPALIVE itself is refused."""
    idle = getattr(socket, "TCP_KEEPIDLE", None) or getattr(socket, "TCP_KEEPALIVE", None)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            kept = [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]
            for name, value in ((idle, _KEEPALIVE_IDLE_S), (getattr(socket, "TCP_KEEPINTVL", None), _KEEPALIVE_EVERY_S),
                                (getattr(socket, "TCP_KEEPCNT", None), _KEEPALIVE_ASKS)):
                if name is None:
                    continue
                try:
                    probe.setsockopt(socket.IPPROTO_TCP, name, value)
                except OSError:
                    continue
                kept.append((socket.IPPROTO_TCP, name, value))
    except OSError:
        return []
    return kept


def _restarts_after_idle() -> bool:
    """Whether this machine restarts a connection's send window after a pause: Linux with tcp_slow_start_after_idle 1
    (its default). False where it cannot be read - not Linux, a container that hides it."""
    try:
        with open(_SLOW_START_AFTER_IDLE) as f:
            return f.read().strip() == "1"
    except OSError:
        return False


def _port_of(stream: Any) -> Optional[int]:
    """The local port of the connection behind httpcore's network stream `stream`, or None when it cannot be read."""
    try:
        sock = stream.get_extra_info("socket") if stream is not None else None
        return sock.getsockname()[1] if sock is not None else None
    except (OSError, AttributeError, IndexError, TypeError):
        return None


def _congestion_of(stream: Any) -> Optional[str]:
    """The congestion control of the connection behind httpcore's network stream `stream` - "bbr", "cubic" - or None
    when that cannot be read (not Linux, a stream with no socket)."""
    try:
        sock = stream.get_extra_info("socket") if stream is not None else None
        if sock is None or _TCP_CONGESTION is None:
            return None
        return sock.getsockopt(socket.IPPROTO_TCP, _TCP_CONGESTION, 16).split(b"\0", 1)[0].decode() or None
    except (OSError, AttributeError, ValueError):
        return None


def _wait_set(event: threading.Event, timeout_s: float, stop: Optional[threading.Event]) -> bool:
    """`event.wait(timeout_s)`, ended early once `stop` is set: a robot's interrupt() reaches it within 50 ms, as it
    reaches wait_until_ready()'s own polling. True once `event` is set."""
    end = time.monotonic() + max(0.0, timeout_s)
    while True:
        left = end - time.monotonic()
        if event.wait(max(0.0, min(0.05, left))):
            return True
        if left <= 0 or (stop is not None and stop.is_set()):
            return False


class _WorkerGone(Exception):
    """Internal: a worker-side transport failure, already stripped of anything sensitive. `waited_s`: how long an act
    waited for its answer when that wait is what failed (a read timeout) - the act reached its worker and may still be
    running there, which DirectConnection asks (act_running) before it sends it again; None when it may never have
    reached it."""

    def __init__(self, message: str, *, waited_s: Optional[float] = None) -> None:
        super().__init__(message)
        self.waited_s = waited_s




_ALIVE_PROBE_S = 5.0












_STUCK_PERIODS = 3
_STUCK_P99 = 1.5
_STUCK_MIN_S = 0.15
_STUCK_TRIPS = 100
_STUCK_AFTER = 20


_NET_RTT_S = 0.1




_RESENDS = 3





FORMATS_HEADER = "X-Seq-Act-Formats"


LEAVING_HEADER = "X-Seq-Leaving"


def _formats_of(value: Optional[str]) -> set:
    """The formats a FORMATS_HEADER value names ("x-seq-stream/3, ..."): an empty set for none."""
    return {part.strip().lower() for part in (value or "").split(",") if part.strip()}


class _WorkerTransport(StreamLink):
    """
    The robot's stream to a single worker (worker_link.StreamLink): its acts, observation posts and episodes' ends on one
    WebSocket - `_client`, an `httpx.Client` whose transport is that stream - and one plain HTTP connection for what may
    not wait on it, GET /ping alone (`_ask_client`): cert-pinned.

    Holds the per-worker `direct_secret` only as an `Authorization` header inside the client —
    never in an attribute that a repr would print, never in a log line, never interpolated into
    an error. The gateway API key is deliberately absent here: the account key authenticates the
    gateway and is never sent to a worker.
    """

    def __init__(self, worker_url: str, direct_secret: str, fingerprint: Optional[str],
                 timeout_s: float, session: Optional[str] = None, teleop: Optional[Any] = None) -> None:
        self._base = worker_url.rstrip("/")


        self.teleop = teleop

        self._timeout_s = timeout_s



        self._used = False


        self.outside = _outside.Window()


        self.chunk_s: Optional[float] = None
        self._playing_asked: Optional[float] = None

        self.gone = False

        self.leaving_since: Optional[float] = None




        self.connect_ms: Optional[float] = None


        self._warm: Optional[threading.Event] = None
        self._warm_trace: Optional[_ConnectionTrace] = None


        self._warm_failed: Optional[str] = None


        self.connect_trace: Any = None
        self._act_opened: Optional[_ConnectionTrace] = None

        self._keeping = False


        self._used_at = 0.0
        self._warm_stop = threading.Event()
        verify = build_pinned_ssl_context(fingerprint)


        self.bbr = _bbr_options()
        options = [*_keepalive_options(), *(self.bbr or [])]


        self._verify, self._stream_options = verify, options
        self._stream: Optional[_stream.WorkerStream] = None
        self._stream_opening: Optional[threading.Event] = None

        self._stream_error: Optional[Exception] = None


        self._latest: Optional[bool] = None


        self.frames_first: Optional[Callable[[Optional[str], float], bool]] = None


        self.quiet: Optional[tuple[float, Callable[[], None]]] = None
        headers = {
            "Authorization": f"Bearer {direct_secret}",
            "Content-Type": "application/json",




            **({"X-Seq-Session": session} if session else {}),
        }
        self._headers = headers
        self._client = httpx.Client(base_url=self._base, timeout=timeout_s, headers=headers,
                                    transport=_stream.StreamRouted(self._route))



        self._ask_client = httpx.Client(base_url=self._base, timeout=timeout_s, verify=verify,
                                        limits=httpx.Limits(max_connections=2, max_keepalive_connections=1))

        self._sends = threading.Lock()
        self._closed = False




        self._on_way = 0
        self._act_starts: deque = deque(maxlen=6)


        self._trips: deque = deque(maxlen=_STUCK_TRIPS)
        self._nets: deque = deque(maxlen=_STUCK_TRIPS)



        self.congestion: Optional[str] = None
        self._cc_stream: Any = None



        self._resumes: Optional[bool] = None



        self.switched: Optional[str] = None


        wifi_power.check_once()

    def prewarm(self) -> None:
        """Open the robot's stream now, in the background, so its first act and observation find it open rather than
        opening it - and what the worker takes known as they go, from its upgrade's answer: a TLS handshake through a
        worker's tunnel took 54 ms to 3.1 s on dev, and a robot's first act paid it. A request that comes while it opens
        waits for it (_route).
"""
        self._ensure_stream()
        self._warm = self._stream_opening

    def _new_trace(self) -> "_ConnectionTrace":
        return _ConnectionTrace()

    def keep_warm(self) -> None:
        """The robot's stream kept warm from now on (_keep_warm, the block above _WARM_EVERY_S), once: from its first
        observe() on, so a robot that only acts is sent no ping it never needs."""
        with self._sends:
            if self._closed or self._keeping:
                return
            self._keeping = True
        if _WARM_EVERY_S:
            threading.Thread(target=self._keep_warm, daemon=True, name="seq-keep-warm").start()

    def say_restart(self, size: int) -> None:
        """An observation of `size` bytes the robot made (observe(), on its own thread): past _BIG_UPLOAD, on a machine
        that restarts a connection's send window after each pause (Linux, tcp_slow_start_after_idle 1) and whose
        connections carry no BBR, said once a process with warnings.warn - such an observation after a pause goes up in
        several round trips - with how to keep the window."""
        if size <= _BIG_UPLOAD or self.bbr is not None or _RESTART_SAID.is_set() or not _restarts_after_idle():
            return
        with _RESTART_LOCK:
            if _RESTART_SAID.is_set():
                return
            _RESTART_SAID.set()
        warn(f"this machine restarts a connection's send window after each pause (net.ipv4.tcp_slow_start_after_idle "
             f"is 1), so an observation of {size / 1e6:.1f} MB sent after one goes up in several round trips. "
             "`sudo sysctl -w net.ipv4.tcp_slow_start_after_idle=0` keeps the window through pauses (a line in "
             "/etc/sysctl.d/ keeps it after a reboot), as does loading BBR (`sudo modprobe tcp_bbr`), which this client "
             "then uses on its connections")

    def _keep_warm(self) -> None:
        """The stream kept warm (the block above _WARM_EVERY_S): every _WARM_EVERY_S that the robot sent nothing, within
        _WARM_FOR_S of its last observation or act, a ping on it, until close()."""
        while not self._warm_stop.wait(_WARM_EVERY_S):
            quiet = time.monotonic() - self._used_at
            if quiet < _WARM_EVERY_S or quiet > _WARM_FOR_S:
                continue
            stream = self._stream
            if stream is not None and stream.alive:
                stream.ping()

    def wait_open(self, timeout_s: float, stop: Optional[threading.Event] = None) -> Optional[str]:
        """Wait up to `timeout_s` for the stream prewarm() is opening. None once it is open - its TLS handshake done, the
        worker's certificate checked and its upgrade answered - else what it met, or that it was still opening. A
        transport whose stream nobody is opening (prewarm never ran), or one an act already went through, has nothing to
        wait for: None. `stop`, once set, ends the wait early (the robot's interrupt): still opening."""
        warm = self._warm
        if warm is None or self._used:
            return None
        if not _wait_set(warm, timeout_s, stop):
            return _STILL_OPENING
        return self._warm_failed

    def note_outside(self, ms: float) -> None:
        """An act answered on this connection spent `ms` outside the worker."""
        self.outside.add(ms)

    def _trace_opened(self, trace: "_ConnectionTrace") -> None:
        """This transport's connection opened (`trace` its phases): its TCP connect and TLS handshake, to its connect's
        trace while it runs."""
        ct = self.connect_trace
        if ct is not None:
            ct.opened(tcp_ms=trace.ms("connect_tcp"), tls_ms=trace.ms("start_tls"))

    def _trace_streamed(self, began: float) -> None:
        """The robot's stream opened since `began` (monotonic), to its connect's trace while it runs."""
        ct = self.connect_trace
        if ct is not None:
            ct.streamed((time.monotonic() - began) * 1000.0)

    def _stopped_in(self) -> Optional[str]:
        """Where the act that could not reach this worker stopped: in the TCP connect or TLS handshake of the connection
        it opened, or of the opening it waited for - None past both, its act sent or its answer waited for."""
        for trace in (self._act_opened, self._warm_trace):
            stopped = trace.stopped_in() if trace is not None else None
            if stopped is not None:
                return stopped
        return None

    def post_act(self, payload: dict, timeout_s: Optional[float], **kw: Any) -> dict:
        """One act to this worker (_post_act) - and, while the connect that made this transport is traced
        (connect_trace), its end: an answer - the policy's error among them - serves it, its TCP connect and TLS
        handshake those this act opened when the opening ahead had not said them; a worker not reached fails it in
        the stage it stopped in; a worker still loading answers warming and the connect goes on."""
        ct = self.connect_trace
        if ct is None:
            return self._post_act(payload, timeout_s, **kw)
        began = time.monotonic()
        try:
            answer = self._post_act(payload, timeout_s, **kw)
        except Exception as exc:
            if isinstance(exc, (_WorkerGone, CertPinError, StreamRefused, httpx.TransportError)):
                self.connect_trace = None
                ct.failed(error_of(exc), stage=self._stopped_in() or "first_act")
            elif isinstance(exc, Unavailable) and exc.warming:
                ct.wait(queued=False)
            else:
                self.connect_trace = None
                self._trace_served(ct, began, kw.get("metrics"))
            raise
        self.connect_trace = None
        self._trace_served(ct, began, kw.get("metrics"))
        return answer

    @staticmethod
    def _trace_served(ct: Any, began: float, metrics: Any) -> None:
        if metrics is not None:
            ct.opened(tcp_ms=getattr(metrics, "tcp_ms", None), tls_ms=getattr(metrics, "tls_ms", None))
        ct.served((time.monotonic() - began) * 1000.0)

    def _post_act(self, payload: dict, timeout_s: Optional[float], *,
                  rid: Optional[str] = None, metrics: Any = None, answer_s: Optional[float] = None,
                  again: bool = False) -> dict:
        """One act to this worker. `timeout_s` bounds the whole request (the caller's own bound for it); `answer_s`, when
        given instead, only how long its answer is waited for once it is sent - every other phase keeps the connection's
        bound - so a long inference is waited out without a worker that cannot be reached being waited for as long.
        `again`: the act sent once more under its request id, which its worker runs once - no new act of the robot's loop, so
        neither its start nor its round trip is counted (stuck_after)."""


        first = not self._used
        self._used = True
        headers = {_RID_HEADER: rid} if rid else {}
        if self.switched is not None and payload.get("episode_id") == self.switched:
            headers[_observe.SWITCHED_HEADER] = "1"


        said = self.outside.said()
        if said is not None:
            headers[_outside.HEADER] = str(said)

        if self.chunk_s is not None and self._playing_asked is not None:
            left = self.chunk_s - (time.monotonic() - self._playing_asked)
            headers[_outside.LEFT_HEADER] = str(max(0, int(left * 1000.0)))
            if metrics is not None and not again:

                metrics.chunk_left_ms = left * 1000.0
        headers = headers or None
        opened = self._act_opened = _ConnectionTrace()
        t0 = time.monotonic()



        waited: Optional[tuple[float, float]] = None
        sent_at: Optional[float] = None
        warm = self._warm
        if warm is not None and not warm.is_set():
            warm.wait(timeout_s if timeout_s is not None else self._timeout_s)
            waited = (t0, time.monotonic())
        try:
            sent_at = time.monotonic()
            if not again:
                with self._sends:
                    self._act_starts.append(sent_at)
            self._used_at = time.monotonic()
            if self.frames_first is not None:


                self.frames_first(payload.get("episode_id"), min(timeout_s or self._timeout_s, _OBSERVE_STALL_S))
            with self._on_its_way():
                r = self._send_act(payload, timeout_s, headers, opened, answer_s=answer_s)
        except httpx.ReadTimeout:



            waited = time.monotonic() - sent_at if sent_at is not None else None
            raise _WorkerGone(f"worker at {self._base} did not answer in time", waited_s=waited) from None
        except _stream.NotOpened as exc:
            raise _WorkerGone(str(exc)) from None
        except _WORKER_GONE:



            raise _WorkerGone(f"worker at {self._base} did not answer") from None
        except httpx.TimeoutException:
            raise _WorkerGone(f"worker at {self._base} timed out") from None
        except httpx.TransportError:
            raise _WorkerGone(f"could not reach worker at {self._base}") from None

        self._note_congestion(r)
        if metrics is not None:


            metrics.rtt_ms = (time.monotonic() - t0) * 1000.0
            metrics.cc = self.congestion
            metrics.rid_echo = r.headers.get(_RID_HEADER)
            metrics.first_after_connect = first


            metrics.connect_ms = self.connect_ms if first else None

            ahead = self._warm_trace if waited is not None else None
            metrics.tcp_ms = _added(opened.ms("connect_tcp"), ahead.overlap("connect_tcp", *waited) if ahead else None)
            metrics.tls_ms = _added(opened.ms("start_tls"), ahead.overlap("start_tls", *waited) if ahead else None)

        answer = Transport._unwrap(r)

        if not again:
            self._playing_asked = t0





        trip = time.monotonic() - (opened.began("send_request_headers") or sent_at)
        perf = answer.get("perf") if isinstance(answer, dict) else None
        handler = perf.get("handler_ms") if isinstance(perf, dict) else None
        if again or first:



            return answer
        with self._sends:
            self._trips.append(trip)
            if isinstance(handler, (int, float)) and not isinstance(handler, bool):
                self._nets.append(max(0.0, trip - handler / 1000.0))
        return answer

    def stuck_after(self) -> Optional[float]:
        """How long an act on this connection may go unanswered before its worker is asked whether it still runs it:
        max(_STUCK_PERIODS x the control period - the median gap between the acts' starts -, _STUCK_P99 x the p99 of its
        last round trips, _STUCK_MIN_S). None until it has answered _STUCK_AFTER acts."""
        with self._sends:
            if len(self._trips) < _STUCK_AFTER:
                return None
            trips = sorted(self._trips)
            starts = list(self._act_starts)
        p99 = trips[max(0, math.ceil(0.99 * len(trips)) - 1)]
        gaps = sorted(b - a for a, b in zip(starts, starts[1:]))
        period = gaps[len(gaps) // 2] if gaps else 0.0
        return max(_STUCK_PERIODS * period, _STUCK_P99 * p99, _STUCK_MIN_S)

    def stuck_probe(self, waited_s: float, rid: Optional[str] = None) -> Optional[str]:
        """What this worker says of the act it has not answered for `waited_s`, asked with a /ping within 3 network round
        trips and 100 ms: its TCP connect and TLS handshake, and its answer. Asked twice at once, on the robot's stream -
        open, so no handshake - and on a plain connection of its own: a question lost on a line gone silent, or to a
        dropped packet (a lost SYN waits a second), is no worker gone, and the first answer is taken. "running" when it
        says it runs the act of request id `rid` (_ping_act); "answered" when it answered the act, its answer on its
        way; "missing" when the act never reached it; "idle" when it runs no such act and says no more; None when
        neither question was answered in that time.

"""
        net = self._net_rtt()
        said: queue.Queue = queue.Queue()

        def ask(client: Any) -> None:
            try:
                said.put(self._ping_act(waited_s, budget_s=3 * net + 0.1, rid=rid, client=client))
            except BaseException:
                said.put((False, None, None))

        for client in (self._client, self._ask_client):
            threading.Thread(target=ask, args=(client,), daemon=True, name="seq-ask").start()
        for _ in range(2):
            pong, ran, answered = said.get()
            if pong:
                if ran is not None:
                    return "running"
                return "idle" if answered is None else "answered" if answered else "missing"
        return None

    def _net_rtt(self) -> float:
        """The network round trip to this worker: the median of its acts' (their trips less the worker's own time), else
        _NET_RTT_S."""
        with self._sends:
            nets = sorted(self._nets)
        return nets[len(nets) // 2] if nets else _NET_RTT_S

    @contextlib.contextmanager
    def _on_its_way(self):
        """A request on its way over this connection: close() waits it out before it closes the client (_on_way)."""
        with self._sends:
            self._on_way += 1
        try:
            yield
        finally:
            self._done()

    def _done(self) -> None:
        """A request on this connection ended: the client closed now when close() came while it was on its way, and it
        was the last."""
        with self._sends:
            self._on_way -= 1
            shut = self._closed and not self._on_way
        if shut:
            self._close_clients()

    def _close_clients(self) -> None:
        """The robot's stream and the /ping connection, closed together: nothing is on its way over either (_on_way)."""
        self._client.close()
        self._ask_client.close()
        stream, self._stream = self._stream, None
        if stream is not None:
            stream.close()

    def _learn(self, response: Any) -> None:
        """What this worker takes by its policy and deployment, from one of its answers, as its latest answer names it.
        An answer that is no success and names no formats came from in front of the worker - the provider's tunnel
        answering for a worker it cannot reach - and says nothing of it: what is known stays (a worker names its formats
        on every answer, its errors and its guard's 401 included)."""
        said = response.headers.get(FORMATS_HEADER)
        if said is None and not 200 <= response.status_code < 300:
            return
        if self.leaving_since is None and response.headers.get(LEAVING_HEADER):
            self.leaving_since = time.monotonic()
        self._learn_formats(said)

    def _learn_formats(self, said: Optional[str]) -> None:
        """What this worker takes, as an answer or its stream's upgrade named it (_learn)."""
        formats = _formats_of(said)
        self._resumes = _observe.RESUME_FORMAT in formats
        self._latest = _observe.LATEST_FORMAT in formats

    def _send_act(self, payload: dict, timeout_s: Optional[float], headers: Optional[dict], opened: Any, *,
                  answer_s: Optional[float] = None) -> Any:
        """One POST /act, its answer asked for in msgpack and read for what the worker takes (_learn); `answer_s` widens
        only the wait for its answer. An act carries no data, and its answer comes back in msgpack: what the policy's act
        function returns as it is - its arrays as arrays of their dtype and shape, its bytes as bytes (L0), a robot
        without numpy reading arrays as the lists JSON would give."""

        kw: dict = {"extensions": {"trace": opened, _stream.AFTER: payload.get("episode_id")}}
        if timeout_s is not None:
            kw["timeout"] = timeout_s
        elif answer_s is not None:

            kw["timeout"] = httpx.Timeout(self._timeout_s, read=answer_s)
        r = self._client.post("/act", json=payload, headers={**(headers or {}), "Accept": _msgpack.MEDIA_TYPE}, **kw)
        self._learn(r)
        return r

    @property
    def resumes(self) -> Optional[bool]:
        """Whether this worker reads an episode's state back when a robot's act comes to it as the episode's standby
        (plan 99 U8), as its latest answer said: None until it has answered."""
        return self._resumes

    def post_observe(self, body: bytes, episode: Optional[str] = None) -> None:
        """One POST /observe of a msgpack body (observe_stream.ObserveStream's, from any of its threads), of `episode`,
        that found no stream open as it was picked: the stream opened, the post queued on it, and waited for until taken
        - the worker asked at once, as an act that comes waits for this post before it goes (observe_stream.picked), and
        nothing else may say it. Raises what the opening met, as an act's answer does - and httpx's own error when it did
        not land in time, its frames going again."""
        self._open_stream(_OBSERVE_STALL_S)
        finished, said = threading.Event(), []

        def done(exc: Optional[BaseException], took: Optional[float]) -> None:
            said.append(exc)
            finished.set()

        if not self.submit_observe(body, episode, done=done):
            raise httpx.ReadError("the stream to the worker ended before this observation's post was written")
        self.ask_taken()
        if not finished.wait(_OBSERVE_STALL_S + len(body) / _SLOWEST_UPLINK_BPS):
            raise httpx.ReadTimeout("the worker did not take this observation's post in time")
        if said and said[0] is not None:
            raise said[0]

    def alive(self, timeout_s: float = _ALIVE_PROBE_S) -> bool:
        """Whether this worker answers /ping now, on the robot's stream to it - what keeps a standby's stream open between
        the acts it serves none of (DirectConnection._keep_standby). Never raises."""
        try:
            r = self._client.get("/ping", timeout=timeout_s)
            self._learn(r)
            return r.status_code < 400
        except Exception:
            return False

    def act_running(self, waited_s: float, *, budget_s: Optional[float] = None,
                    rid: Optional[str] = None) -> Optional[float]:
        """How long the act a robot waited `waited_s` for has run on this worker, when the worker says it still runs it:
        /ping - unauthenticated, and answered while an inference runs - asked of that act by its request id (`rid`, the
        X-Seq-Request-Id it went with: /ping?act=), which a worker answers {"act": {"running": true, "for_s": ...}} or
        {"act": {"running": false}} - not received, answered, or failed. None when /ping does not answer in time -
        `budget_s`, else the wait itself within 0.5 s and _ALIVE_PROBE_S - (the worker is gone), or says it runs no such
        act."""
        return self._ping_act(waited_s, budget_s=budget_s, rid=rid)[1]

    def _ping_act(self, waited_s: float, *, budget_s: Optional[float], rid: Optional[str],
                  client: Any = None) -> tuple[bool, Optional[float], Optional[bool]]:
        """/ping asked of the act (act_running), on `client` (the plain connection by default): whether the worker answered
        in time; how long the act has run when it says it runs it, else None; and, of one it does not run, whether it
        answered it (`answered`, a worker that runs an act once by its request id) - None when it does not say."""
        try:
            bound = budget_s if budget_s is not None else min(_ALIVE_PROBE_S, max(0.5, waited_s))
            pong = (client or self._ask_client).get("/ping", params={"act": rid} if rid else None, timeout=bound)
            said = pong.json() if pong.status_code == 200 else None
        except Exception:
            return False, None, None
        if not isinstance(said, dict):
            return False, None, None
        act = said.get("act")
        if not isinstance(act, dict) or not isinstance(act.get("running"), bool):
            return True, None, None
        if not act["running"]:
            answered = act.get("answered")
            return True, None, answered if isinstance(answered, bool) else None
        ran = act.get("for_s")
        return (True, float(ran) if isinstance(ran, (int, float)) and not isinstance(ran, bool) else float(waited_s),
                None)

    def post_episode_end(self, episode_id: str) -> None:
        """Tell the worker an episode is over. Best effort: errors are swallowed — a worker that is gone took
        the episode with it, and the worker ends an episode with no act on its own after its TTL."""
        try:
            self._learn(self._client.post("/act/episode_end", json={"episode_id": episode_id}, timeout=_EPISODE_END_S))
        except (httpx.HTTPError, SequencesError):
            pass

    def end_episode_behind(self, episode_id: str) -> threading.Thread:
        """post_episode_end on a thread of its own, for a robot moving off this worker: its connect to the next one does
        not wait for this one's answer. close() leaves the client open until it is sent.
"""
        def send() -> None:
            try:
                self.post_episode_end(episode_id)
            except Exception:
                pass
            finally:
                self._done()

        with self._sends:
            self._on_way += 1
        sender = threading.Thread(target=send, name="seq-episode-end", daemon=True)
        sender.start()
        return sender

    def acted_within(self, seconds: float) -> bool:
        """Whether an act of the robot's began over this transport within the last `seconds`."""
        with self._sends:
            return bool(self._act_starts) and time.monotonic() - self._act_starts[-1] <= seconds

    def same(self, worker_url: str, direct_secret: str) -> bool:
        """Whether a connect's answer names this very connection: the worker at the same address, reached with the same
        secret - read from the header that holds it, never kept apart from it - and not given up (`gone`)."""
        held = str(self._client.headers.get("Authorization", "")).encode()
        return (not self.gone and self._base == str(worker_url).rstrip("/")
                and hmac.compare_digest(held, f"Bearer {direct_secret}".encode()))

    def close(self) -> None:


        self._warm_stop.set()
        with self._sends:
            self._closed = True
            if self._on_way:
                return
        self._close_clients()

    def _note_congestion(self, response: Any) -> None:
        """Read the congestion control of the connection that carried `response`, once for each connection."""
        stream = (getattr(response, "extensions", None) or {}).get("network_stream")
        if stream is not None and stream is self._cc_stream:
            return
        self.congestion, self._cc_stream = _congestion_of(stream), stream


class _ConnectionTrace:
    """httpcore's trace hook for one act (httpx passes `extensions={"trace": ...}` through, httpx 0.24 and up): when the
    TCP connect and the TLS handshake of a connection the act opened began and ended. Its events are named
    "connection.connect_tcp.started" / ".complete" and "connection.start_tls.started" / ".complete"; an act on a
    connection already open sends neither, and its phases are None, never 0. worker_stream tells the same two of a stream's
    opening, and its writing as "http11.send_request_headers"."""

    def __init__(self) -> None:
        self._at: dict = {}
        self.port: Optional[int] = None

    def __call__(self, event: str, info: Any) -> None:
        phase, _, edge = event.rpartition(".")
        if edge in ("started", "complete"):
            self._at[(phase.rpartition(".")[2], edge)] = time.monotonic()
            if event == "connection.connect_tcp.complete":
                self.port = _port_of((info or {}).get("return_value"))

    def ms(self, phase: str) -> Optional[float]:
        start, end = self._at.get((phase, "started")), self._at.get((phase, "complete"))
        return (end - start) * 1000.0 if start is not None and end is not None else None

    def began(self, phase: str) -> Optional[float]:
        """When `phase` began (monotonic seconds) - "send_request_headers", its first byte - or None."""
        return self._at.get((phase, "started"))

    def overlap(self, phase: str, start: float, end: float) -> Optional[float]:
        """The part of `phase` that fell between `start` and `end` (monotonic seconds), in ms: how long an act that
        waited then waited on it. None when the phase was not timed or none of it fell there."""
        began, done = self._at.get((phase, "started")), self._at.get((phase, "complete"))
        if began is None or done is None:
            return None
        ms = (min(done, end) - max(began, start)) * 1000.0
        return ms if ms > 0 else None

    def stopped_in(self) -> Optional[str]:
        """The phase an opening began and never ended in - "tcp" its TCP connect, "tls" its TLS handshake - else None."""
        for phase, stage in (("connect_tcp", "tcp"), ("start_tls", "tls")):
            if (phase, "started") in self._at and (phase, "complete") not in self._at:
                return stage
        return None

    def stuck(self) -> str:
        """Where an opening that never answered was when it was given up, in words for the robot's warning: the phase
        that began and never ended, else the worker's answer it was waiting for (both phases done, or neither begun)."""
        for phase, said in (("connect_tcp", "in its TCP connect"), ("start_tls", "in its TLS handshake")):
            if (phase, "started") in self._at and (phase, "complete") not in self._at:
                return said
        return "waiting for its answer"



def _added(*ms: Optional[float]) -> Optional[float]:
    """The sum of the timings given, None when none was."""
    said = [m for m in ms if m is not None]
    return sum(said) if said else None
