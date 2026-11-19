# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The client-side components, applied to one connection to your own server.

    from sequence_ai.network import connect

    link = connect("http://your-gpu:8000")                 # BBR and TCP keepalive, where this machine allows them
    link.wait_until_ready()                                 # until the server answers its ping with 200
    response = link.act({"image": frame, "state": state})  # msgpack both ways; a ping while the connection is idle
    link.close()

observe() then act() is the same request in two calls, the two a robot makes on a policy it reaches by name
(sequence_ai.connect), so one control loop runs against either (loop.play is one):

    link.observe({"image": frame, "state": state})         # held here; nothing is sent
    response = link.act()                                   # uploads the newest observation

What it does by default, and how to turn each off:
    pictures as JPEG    each picture in the observation - a numpy array of shape HxWx3 and dtype uint8, or an RGB PIL
                        image as frames.resize_image returns it, under any key - sent as JPEG (frames.pack_pictures),
                        while the server names "jpeg" in the X-Seq-Reads header of its responses (serve() does, on
                        every answer; with nothing heard yet, the first act asks its ping first)        jpeg=False
    compression         large arrays compressed where that saves upload time (compress.Squeeze), while the server names
                        a codec this robot has ("zstd", "zlib") there                                   compress=False
    a longer first wait the first act waits up to `first_timeout` (120 s) for its response, the others `timeout` (10 s):
                        a server compiles its model on its first inference         first_timeout=10.0
    pings when idle     a GET at `ping_path` after each `ping_every_s` (100 ms) of idle time      ping_path=None
    pings out of the    once the robot's acts come at a steady spacing, a ping whose answer would still be on its
     acts' way          way when the next act is due is not sent: that act would wait for it, a round trip at most.
                        On Linux without BBR, where a pause restarts the window, the ping that alone keeps it - the
                        connection's silence still under a round trip and 200 ms, Linux's least retransmission
                        timeout - is sent all the same (pings_yielded counts those left out)       ping_yield=False
    an act in halves    on Linux without BBR, an act sent after a silence past a round trip and 200 ms - or after a
                        ping sent past it - meets a window restarted to 10 packets: when its body is more than that
                        first flight carries (9 packets of the connection's segment size, the request's headers in
                        the tenth: 13,032 bytes on Ethernet) and no more than two, it goes in two halves at once,
                        each on a connection of its own, to a server that joins them (X-Seq-Reads names "split";
                        serve() does): each half fits its own first flight (acts_in_halves)        split=False
    BBR, keepalive      on the connection's socket, where this machine allows them (window)
    kept while idle     each connection kept 240 s with nothing sent on it (KEPT_S), where an HTTP client keeps
                        5 s, under serve()'s 300 s: a robot back from a pause past its pings acts on the connection
                        it had, a handshake sooner
jpeg=True and compress=True send them whatever the server says, for a server that restores them and does not say so.
`token` sends `Authorization: Bearer <token>`, for a server started with one.

In one sentence: connect() opens one httpx connection with window.socket_options() on its socket → each response's
X-Seq-Reads says what the server restores (the latest one counts) → act() packs the observation with msgpack_io, its
pictures as JPEG and its large arrays compressed where the server restores them, posts it - in two halves on two
connections when its window has restarted and it is one to two first flights long - and reads the response → between
requests a small GET is sent on the same connection after each `ping_every_s` of idle time (window.Warm) → each
request's time is recorded (latency_stats) and read with stats().

WHY one connection and a lock: an HTTP/1.1 client that starts a request while a ping is in flight opens a second
connection for it, with a new handshake and a cold window, which is exactly what the ping is there to prevent. So the
pool holds one connection, a ping is skipped while a request is in flight, and a request that starts while a ping is in
flight waits for it: one round trip at most, and only when the two coincide. That wait is in each act's time (act_us,
counted from when act() queued the request) and also on its own (ping_wait_us, acts_behind_ping), so it shows; and
with ping_yield, a ping that would meet the next act is left out (the defaults above), so the two coincide only when
the robot's act comes off its spacing. The second connection carries only acts' second halves, opened before the first.
WHY halves, and only then: Linux restarts the window of a connection that sent nothing past its retransmission timeout
(window), and a body that does not fit the restarted window's first flight waits a round trip for the rest; another
connection has a first flight of its own. Measured on Linux 6.10 over a 1500-byte MTU, a policy of 200 ms - its silence
spends the timeout before any ping can keep the window - and an act every 533 ms: at a 50 ms round trip (80 acts
each), bodies of 13.2 to 26.1 KB took a p50 of 108 to 111 ms whole and 56.5 to 57.0 ms in halves (p99 117 to 118
against 62 to 64); at 20 and 100 ms (40 acts each), 48 to 50 against 26, and 211 to 212 against 107 to 109; with a 10
Mbit/s uplink, 110 to 115 against 68 to 78. Where the window was kept - pings with a 5 ms policy, net.ipv4.tcp_slow_start_after_idle 0 as with
BBR - a whole act took one round trip already and halves saved nothing; and a body of more than two first flights took
two round trips either way (28 to 120 KB).
WHY each connection is kept 240 s while idle: an HTTP client closes an idle connection after 5 s of its own, so a robot
whose pings had stopped (ping_for_s) paid a new connection's handshake on its next act - the round trip the pings, BBR
and halves are there to save. Measured as above, 8 acts each 8 s after the pings stopped: kept, a p50 of 64.2 ms, all
on one connection; at 5 s, 121.5 ms, each on a new one.
WHY JPEG only for HxWx3 uint8 arrays, and only while the server says it reads it: JPEG changes a picture's values a
little (frames.DEFAULT_JPEG_QUALITY has how much), and a server that does not restore the map it is sent as would hand
the map to its policy.

What the server needs: `act_path`, a POST that takes a msgpack body (msgpack_io.unpack reads it) and responds with
msgpack or JSON; and any cheap GET at `ping_path` (None: no pings, and wait_until_ready() waits for nothing). If the
server reports its own processing time in the standard Server-Timing header (`act;dur=276.0`, milliseconds), that time
is excluded from the estimated cost of the upload; if it does not, a slow model is counted as a slow link, and
compression is judged to save more than it does. serve() (sequence_ai.serve) does all of this.

Whether any of it helps depends on the link: `python -m sequence_ai.check <url>` says what is on for yours, and bench/
measures it.

Needs httpx, which sequence-ai installs.
"""
from __future__ import annotations

import concurrent.futures
import socket
import threading
import time
import uuid
from collections import deque
from typing import Any, Callable, NamedTuple, Optional

from . import _warn
from . import compress as _compress
from . import bind as _bind
from . import compressed as _compressed
from . import frames, msgpack_io, wifi_power, window
from .latency_stats import LatencyStats, now_us

# The header in which a server names what it restores from an observation, in each response: "jpeg" for pictures sent
# as frames.pack_pictures writes them, "zstd" and "zlib" for items compressed as compressed.py writes them.
READS_HEADER = "X-Seq-Reads"
# The header in which serve() says what it is, in each response: "sequence-ai/<version>". Its ping's answer says more,
# as JSON: {"server": "sequence-ai", "version", "up_s" (how long it has run), "pid", "policy"}. A server that says
# nothing of it may be another program at the address the robot was given.
SERVER_HEADER = "X-Seq-Server"
# The header that names one act: the same id on every copy of it a robot sends (network.lines sends each act over each
# of its uplinks). A server that runs an act once by it says so with ONCE in READS_HEADER; the platform's workers run an
# act once by the same header (_core/rid.py's HEADER, pinned equal by tests/network/test_lines.py).
REQUEST_HEADER = "X-Seq-Request-Id"
ONCE = "once"
# The header on the answer to a copy of an act whose answer another copy got: the policy ran once, for the other.
COPY_HEADER = "X-Seq-Request-Copy"
# An act sent in two halves, each on a connection of its own (split): each half is a POST to the act's path with the
# act's REQUEST_HEADER and HALF_HEADER "1/2" (the body's first bytes) or "2/2" (the rest). A server that joins them says
# SPLIT in READS_HEADER; it answers the first half with the act's answer and the second with 202 as soon as it has it,
# and the first half with HALF_MISSING when the second has not come within its wait - the robot then sends the act whole.
HALF_HEADER = "X-Seq-Half"
SPLIT = "split"
HALF_MISSING = 424
FIRST_TIMEOUT_S = 120.0        # the first act's wait: a policy compiled on its first inference took 32 to 43 s
# A ping that yields to the robot's next act (Link._yields_now): the acts' spacing is the median of the gaps between the
# last YIELD_ACTS + 1 acts asked for, read once YIELD_MIN_GAPS of them are known; a ping is left out only while the
# connection's silence stays under RTO_FLOOR_S more than a ping's round trip - Linux's least retransmission timeout above
# the round trip (tcp_rto_min, 200 ms), past which it restarts the window of a connection that sends nothing - and the
# round trip is FIRST_TRIP_S until a ping has measured one.
YIELD_ACTS = 8
YIELD_MIN_GAPS = 3
RTO_FLOOR_S = 0.2
FIRST_TRIP_S = 0.1
RECHECK_S = 0.01               # how close to that silence's end a ping left out is asked about again
# when a ping now would be back (_yields_now): the YIELD_TRIP_Q quantile of the last YIELD_TRIPS pings' round trips,
# not their median - on a line whose round trips jitter (a home network out cellular: p50 52 ms, p90 128, p99 253) the
# median of the last 8 fell short of the next by 40 ms or more one time in five, and the ping it let go met the act
YIELD_TRIP_Q = 0.9
YIELD_TRIPS = 32
# split: an act goes in two halves when its connection's window restarts at its send (Link._restarts_now) and its body
# is more than a first flight after a pause carries and no more than two: FIRST_FLIGHT packets of the connection's
# segment size (MSS until it is read from the socket), its request's headers in the first of them. After a half that did
# not reach the server, acts go whole for WHOLE_AGAIN_S.
FIRST_FLIGHT = 10
MSS = 1448
WHOLE_AGAIN_S = 60.0
# How long each connection is kept while nothing is sent on it: an HTTP client's own default is 5 s, after which the
# robot's next request paid a new connection's handshake - one round trip more, the one split, BBR and the pings are
# there to save - once its pings had stopped (ping_for_s), and the second connection between halves. Under serve()'s
# 300 s (engine.serve.KEEP_ALIVE_S), so that the server never closes one as a request goes; TCP keepalive (window) keeps
# a router's record of it meanwhile, and finds one that died.
KEPT_S = 240.0


def _request_id() -> str:
    """A new act's id: `r-` and 8 hex characters, as the platform's are (_core/rid.py)."""
    return "r-" + uuid.uuid4().hex[:8]


class Packed(NamedTuple):
    """One act's request as Link.pack() made it: its body, how many pictures went as JPEG, and the compression that
    packed it (None for none), whose estimate of the uplink the answer's time goes into."""
    body: bytes
    pictures: int
    squeeze: Optional[Any]


def _server_seconds(header: Optional[str]) -> float:
    """The first duration in a Server-Timing header, in seconds; 0 where it has none."""
    for part in (header or "").replace(",", ";").split(";"):
        name, _, value = part.strip().partition("=")
        if name == "dur":
            try:
                return max(0.0, float(value) / 1000.0)
            except ValueError:
                return 0.0
    return 0.0


def _mss_of(response: Any) -> Optional[int]:
    """The segment size of the connection `response` came on, from its socket (TCP_MAXSEG); None where it cannot be
    read."""
    try:
        sock = response.extensions["network_stream"].get_extra_info("socket")
        return int(sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_MAXSEG)) or None
    except Exception:  # noqa: BLE001 - no socket to read (a transport of another kind): MSS is taken
        return None


def reads_of(header: Optional[str]) -> frozenset:
    """What an X-Seq-Reads header names, lowercased: an empty set for none."""
    return frozenset(part.strip().lower() for part in (header or "").split(",") if part.strip())


class Link:
    """One connection to a policy server, with the client-side components applied to it (the module's docstring)."""

    _NONE: Any = object()                    # no observation: act() sends the one observe() was handed last

    def __init__(self, url: str, *, act_path: str = "/act", ping_path: Optional[str] = "/ping",
                 ping_every_s: float = 0.1, ping_for_s: float = 60.0, ping_yield: bool = True,
                 compress: Optional[bool] = None,
                 jpeg: Optional[bool] = None, timeout: float = 10.0, first_timeout: float = FIRST_TIMEOUT_S,
                 token: Optional[str] = None, headers: Optional[dict] = None, check: bool = True,
                 bind: Optional[str] = None, on_unreachable: Optional[Callable[["Link"], bool]] = None,
                 split: bool = True) -> None:
        try:
            import httpx
        except ImportError as missing:
            raise ImportError('connect() uses httpx for its connection, and httpx is not installed: '
                              'pip install httpx') from missing

        if check:
            wifi_power.check_once()          # warns once, on its own thread: Wi-Fi power saving, if it is on
            window.check()                   # warns once: a machine that restarts its window after each pause
        self._options = window.socket_options()
        self.bind = bind
        headers = dict(headers or {})
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        self._httpx, self._url, self._refused, self._headers = httpx, url, httpx.ConnectError, headers
        self._act_path, self._ping_path = act_path, ping_path
        self._timeout, self._first_timeout = float(timeout), float(first_timeout)
        self._client = self._connection()        # the link's own connection, kept KEPT_S while idle
        self._busy = threading.Lock()        # held by the request or the ping in flight: the connection carries one
        self._jpeg, self._compress = jpeg, compress
        self._reads: Optional[frozenset] = None          # what the server's latest X-Seq-Reads named; None: not heard
        self._squeeze: Optional[_compress.Squeeze] = _compress.Squeeze() if compress is True else None
        self._squeeze_for: Optional[frozenset] = None    # the codecs an automatic Squeeze was made for
        self._answered = False               # whether an act was answered: the first waits first_timeout
        self._stats = LatencyStats(counters=["acts", "pings", "pings_yielded", "acts_behind_ping", "pictures",
                                             "unreachable_retries", "acts_in_halves", "acts_whole_again"],
                                   latencies=["act_us", "ping_wait_us", "pack_us"])
        # an act in two halves (split): the second connection, its own thread, the last thing sent on it (the GET that
        # opened it, or a second half; None until the server says it joins halves), whether it has answered, and
        # until when acts go whole after a half that did not reach the server
        self._split = bool(split)
        self._second = self._connection() if self._split else None
        self._second_thread = concurrent.futures.ThreadPoolExecutor(
            max_workers=1, thread_name_prefix="sequence-ai-second") if self._split else None
        self._second_sent: Optional[concurrent.futures.Future] = None
        self._second_ready = False
        self._whole_until = 0.0
        self._mss: Optional[int] = None      # the connection's segment size, read from its socket (_learn)
        self._warm = window.Warm(self._ping, every_s=ping_every_s, for_s=ping_for_s) if ping_path else None
        # pings that yield to the robot's next act (_yields_now): when its last acts were sent, its last pings' round
        # trips, and when anything was last sent on the connection
        # called with this link when a request cannot reach the server (_unreachable): True, and the act goes once more
        self._on_unreachable = on_unreachable
        self._yield = ping_yield
        # whether a pause restarts this connection's window: Linux with net.ipv4.tcp_slow_start_after_idle 1 and no BBR
        # (macOS keeps it, BBR skips the restart) - only then can a ping keep what a pause would take
        self._window_at_stake = window.restarts_after_idle() and window.bbr_options() is None
        self._timing = threading.Lock()
        self._act_starts: deque = deque(maxlen=YIELD_ACTS + 1)
        self._ping_trips: deque = deque(maxlen=YIELD_TRIPS)
        self._last_send: Optional[float] = None
        self._restarted = False              # whether a ping since the last act restarted the window (_restarts_now)
        self._observed: Any = Link._NONE
        # the last act answered: the time its server says its model took (Server-Timing; None where it says none), and
        # the size of the request's body as sent
        self.last_server_s: Optional[float] = None
        self.last_carried_s: Optional[float] = None
        self.last_body_bytes: Optional[int] = None
        # what the server says it is (SERVER_HEADER, and its ping's JSON): None until it has said so
        self.server: Optional[dict] = None
        self._check, self._told, self._warmed = check, False, False
        self._asked = False                  # whether the first act asked the server what it reads (_ask_first)

    # ── what the server says it reads ─────────────────────────────────────────────────────────────────────────────
    def _learn(self, response: Any) -> None:
        """The server's X-Seq-Reads and X-Seq-Server, from one of its responses: the latest one counts. A success that
        names nothing says the server restores nothing; an error that names nothing came from in front of it (a proxy)
        or from a server that is not serving yet, and changes nothing known. The first success that does not say it is
        serve() is told once (with `check`): defaults that wait for the server's word stay off on it, and it may be
        another program at this address."""
        said, server = response.headers.get(READS_HEADER), response.headers.get(SERVER_HEADER)
        if self._mss is None:
            self._mss = _mss_of(response)
        if server is not None:
            name, _, version = server.partition("/")
            self.server = {**(self.server or {}), "server": name.strip(), "version": version.strip()}
        if said is None and not 200 <= response.status_code < 300:
            return
        self._reads = reads_of(said)
        if self._split and SPLIT in self._reads:
            self._open_second()              # opened now: an act goes in halves only once it has answered
        if self.sends_jpeg and not self._warmed:
            # Pillow and its JPEG encoder loaded now, on a thread of their own, not in the first act that sends a
            # picture: tens of milliseconds
            self._warmed = True
            threading.Thread(target=frames.warm, daemon=True, name="sequence-ai-jpeg-warm").start()
        if server is None and self._check and not self._told:
            self._told = True
            _warn.warn(f"{self._url} does not say it is sequence-ai's serve() (no {SERVER_HEADER} in its answer): if "
                       "serve() was started there, another program answers at that address; if the server is one of "
                       "your own, it restores neither JPEG nor compression as far as connect() knows, and both stay "
                       "off")

    def _take_identity(self, response: Any) -> None:
        """What a ping's JSON answer says the server is (SERVER_HEADER's comment): kept in `server`."""
        if "json" not in response.headers.get("content-type", ""):
            return
        try:
            said = response.json()
        except ValueError:
            return
        if isinstance(said, dict) and said.get("server"):
            kept = {key: said[key] for key in ("server", "version", "up_s", "pid", "policy") if key in said}
            self.server = {**(self.server or {}), **kept}

    @property
    def reads(self) -> Optional[frozenset]:
        """What the server's latest X-Seq-Reads header named ("jpeg", "zstd", "zlib"): None before any response."""
        return self._reads

    @property
    def sends_jpeg(self) -> bool:
        """Whether act() sends the observation's pictures as JPEG now (the module's docstring: `jpeg`)."""
        return self._jpeg is True or (self._jpeg is None and frames.PICTURE_KIND in (self._reads or ()))

    def _squeeze_now(self) -> Optional[_compress.Squeeze]:
        """The compression act() applies now: compress=True's, or - compress=None - one for the codecs the server last
        named that this robot has; None when there is none."""
        if self._compress is not None:
            return self._squeeze
        codecs = frozenset(_compressed.CODECS) & (self._reads or frozenset())
        if not codecs or _compress.codec_for(codecs) is None:
            return None
        if self._squeeze is None or self._squeeze_for != codecs:
            self._squeeze, self._squeeze_for = _compress.Squeeze(codecs), codecs
        return self._squeeze

    @property
    def compresses(self) -> bool:
        """Whether act() compresses the observation's large items now, where that saves time (the module's
        docstring: `compress`)."""
        return self._squeeze_now() is not None

    # ── the connection ────────────────────────────────────────────────────────────────────────────────────────────
    def _connection(self) -> Any:
        """A client of one connection to the server, kept KEPT_S while nothing is sent on it: window.socket_options() on
        its socket, by the network interface `bind` names (network.bind) whatever the default route, with this link's
        headers."""
        httpx = self._httpx
        made = dict(socket_options=self._options, limits=httpx.Limits(max_connections=1, max_keepalive_connections=1,
                                                                      keepalive_expiry=KEPT_S))
        transport = _bind.transport(httpx, self.bind, **made) if self.bind is not None else httpx.HTTPTransport(**made)
        return httpx.Client(base_url=self._url, transport=transport, timeout=self._timeout, headers=self._headers)

    def _ping(self) -> bool:
        """The idle connection's ping (window.Warm calls it): sent, and True - or left out, and False, while a request
        is in flight or while it yields to the robot's next act (_yields_now)."""
        if self._yields_now():
            self._stats.count("pings_yielded")
            return False
        if not self._busy.acquire(blocking=False):
            return False                     # a request is in flight: the connection is not idle
        began = time.perf_counter()
        try:
            response = self._client.get(self._ping_path)
            self._stats.count("pings")
        finally:
            self._busy.release()
        self._ping_done(began, time.perf_counter())
        self._learn(response)
        return True

    def _ping_done(self, began: float, ended: float) -> None:
        """A ping sent on this connection at `began` and answered at `ended` (time.perf_counter()): the last thing sent,
        and one round trip more for the pings that may yield."""
        with self._timing:
            if self._last_send is None or began > self._last_send:
                self._restarted = self._restarted or self._past_deadline(began)
            self._last_send = began
            self._ping_trips.append(ended - began)

    def _act_sent(self, asked: float, sent: float) -> None:
        """An act the robot asked for at `asked` and that was sent on this connection at `sent` (time.perf_counter()):
        later, when it waited for a ping in flight. The acts' spacing is the robot's own, read from when each was asked
        for - from when each was sent, a wait behind a ping would put every act after it that much later - and `sent` is
        the last thing sent."""
        with self._timing:
            self._last_send = sent
            self._act_starts.append(asked)
            self._restarted = False              # the act's own upload grows the window again

    def _yields_now(self) -> bool:
        """Whether the ping due now is left out for the robot's next act: an act that started while a ping was in flight
        waited for its answer, a round trip at most. With `ping_yield`, once YIELD_MIN_GAPS gaps between acts are known,
        the next act is expected the median gap after the last was asked for. A ping whose answer would come after that
        - or within a twentieth of the gap before it - is left out while the act is not a tenth of the gap late, and
        window.Warm is asked about it again then (check_in): should the act not have come, the ping goes.
        One ping is still sent though it meets the act: on a machine where a pause restarts the window (Linux without
        BBR, net.ipv4.tcp_slow_start_after_idle 1), the one that alone keeps it - the connection has sent something
        within a ping's round trip and RTO_FLOOR_S, and the act is expected after that, when Linux would restart the
        window at the act's own send. A ping left out short of that is asked about again before it (check_in). Once
        that silence is past - a long inference spends it, from the act sent to its answer - the next send restarts the
        window, ping or act, and the ping would only meet the act; and where nothing restarts it (macOS, BBR), the ping
        keeps nothing either."""
        if not self._yield or self._warm is None:
            return False
        with self._timing:
            starts, trips, last = list(self._act_starts), sorted(self._ping_trips), self._last_send
        if len(starts) <= YIELD_MIN_GAPS or last is None:
            return False
        gaps = sorted(b - a for a, b in zip(starts, starts[1:]))
        gap = gaps[len(gaps) // 2]
        trip = trips[len(trips) // 2] if trips else FIRST_TRIP_S
        back = trips[min(len(trips) - 1, int(YIELD_TRIP_Q * len(trips)))] if trips else FIRST_TRIP_S
        now = time.perf_counter()
        due = starts[-1] + gap                                   # when the next act is expected
        late = due + 0.1 * gap                                   # past this, it is late: pings as usual
        if now + back <= due - 0.05 * gap or now >= late:
            return False                                         # back before the act, or the act is late
        deadline = last + trip + RTO_FLOOR_S                     # the latest the connection's next send may go
        if self._window_at_stake and now + RECHECK_S < deadline:
            if due > deadline - RECHECK_S:
                return False                                     # the window kept by this ping alone: it goes
            self._warm.check_in(min(late, deadline - RECHECK_S) - now)
            return True
        self._warm.check_in(late - now)                          # nothing for the ping to keep: it would meet the act
        return True

    # ── an act in two halves ──────────────────────────────────────────────────────────────────────────────────────
    def _open_second(self) -> None:
        """The second connection opened, once: a GET at ping_path (act_path without one) on its own thread. Any answer
        opens it; a failure leaves acts whole for WHOLE_AGAIN_S, then it is opened again (_splits_now)."""
        with self._timing:
            if self._second_sent is None:
                self._second_sent = self._second_thread.submit(self._hello)

    def _hello(self) -> None:
        try:
            self._second.get(self._ping_path or self._act_path)
        except (self._httpx.TransportError, self._httpx.TimeoutException):
            self._whole_until = time.monotonic() + WHOLE_AGAIN_S
            return
        self._second_ready = True

    def _splits_now(self, size: int) -> bool:
        """Whether an act of a `size`-byte body goes in two halves now (the module's docstring: `split`): the server
        says it joins them; the body is more than this connection's first flight after a pause carries, and no more
        than two; the window restarts at this send (_restarts_now); the second connection has answered and carries
        nothing; and no half failed in the last WHOLE_AGAIN_S."""
        flight = (FIRST_FLIGHT - 1) * (self._mss or MSS)
        if (not self._split or not flight < size <= 2 * flight or SPLIT not in (self._reads or ())
                or not self._restarts_now()):
            return False
        with self._timing:
            last = self._second_sent
            if last is None or not last.done():
                return False                 # not opened yet, or its last half still on its way
            if not self._second_ready or not self._reached(last):
                self._second_ready = False
                if time.monotonic() >= self._whole_until:
                    self._second_sent = self._second_thread.submit(self._hello)    # opened again
                return False
            return time.monotonic() >= self._whole_until

    def _restarts_now(self) -> bool:
        """Whether the next act meets a restarted window on this connection: on a machine where a pause restarts it
        (Linux without BBR), once a send since the last act - a ping, or this act - follows a silence past a ping's
        round trip and RTO_FLOOR_S (_yields_now's deadline), or before anything was sent. A ping sent after the
        silence restarts the window as the act would, and the act finds it at its start."""
        if not self._window_at_stake:
            return False
        with self._timing:
            return self._restarted or self._past_deadline(time.perf_counter())

    def _past_deadline(self, at: float) -> bool:
        """Whether a send at `at` follows a silence past the connection's deadline (_yields_now). With _timing held."""
        trips = sorted(self._ping_trips)
        trip = trips[len(trips) // 2] if trips else FIRST_TRIP_S
        return self._last_send is None or at > self._last_send + trip + RTO_FLOOR_S

    def _reached(self, sent: concurrent.futures.Future) -> bool:
        """Whether what went on the second connection reached the server: an answer, and to a half, a success."""
        if sent.exception() is not None:
            self._whole_until = time.monotonic() + WHOLE_AGAIN_S
            return False
        response = sent.result()
        if response is not None and not 200 <= response.status_code < 300:
            self._whole_until = time.monotonic() + WHOLE_AGAIN_S
            return False
        return True

    def _post_halves(self, path: str, body: bytes, timeout: Any, sent: dict) -> Any:
        """The act in two halves at once (split), each on a connection of its own: the body's second half on the second
        connection's thread, its first half here, on this link's connection, whose answer is the act's. Should the
        server answer the first half HALF_MISSING - the second did not reach it - the act goes whole on this connection,
        and the acts after it whole for WHOLE_AGAIN_S."""
        cut = len(body) // 2
        second = self._second_thread.submit(self._second.post, path, content=body[cut:], timeout=self._timeout,
                                            headers={**sent, HALF_HEADER: "2/2"})
        with self._timing:
            self._second_sent = second
        response = self._client.post(path, content=body[:cut], timeout=timeout, headers={**sent, HALF_HEADER: "1/2"})
        self._stats.count("acts_in_halves")
        if response.status_code != HALF_MISSING:
            return response
        self._stats.count("acts_whole_again")
        self._whole_until = time.monotonic() + WHOLE_AGAIN_S
        return self._client.post(path, content=body, timeout=timeout, headers=sent)

    def wait_until_ready(self, timeout_s: float = 600.0, *, poll_s: float = 0.5, example: Any = _NONE) -> None:
        """
        Wait, up to `timeout_s`, until the server answers its ping with 200: a server still loading or warming its
        model answers 503 (serve() does, with Retry-After), and one not listening yet refuses the connection. Then,
        given an `example` observation, send it once and wait for its response, `first_timeout` at most: the model is
        compiled for it before the robot needs it, and the robot's first act waits as long as any other. With no
        `ping_path` there is nothing to ask: only the example is sent.

        TimeoutError past `timeout_s`; httpx.HTTPStatusError when the server refuses the ping (401: the token).
        """
        end = time.monotonic() + timeout_s
        last: Optional[int] = None                       # the status of the last answer, for the error
        while self._ping_path is not None:
            left = end - time.monotonic()
            wait = poll_s
            try:
                with self._busy:
                    response = self._client.get(self._ping_path, timeout=max(0.001, min(self._timeout, left)))
            except (self._httpx.TransportError, self._httpx.TimeoutException) as failed:
                response = None                          # not listening yet, or not answering: asked again
                if isinstance(failed, (self._refused, self._httpx.ConnectTimeout)) and self._on_unreachable:
                    try:
                        self._on_unreachable(self)       # once this round: what it changes, the next round finds
                    except Exception:  # noqa: BLE001 - the wait goes on, and says what it last met
                        pass
            if response is not None:
                last = response.status_code
                self._learn(response)
                if response.status_code == 200:
                    self._take_identity(response)
                    break
                if response.status_code == 404:
                    break                                # no ping here: a server that answers is as ready as it says
                if 400 <= response.status_code < 500:
                    response.raise_for_status()          # refused (401, 403: the token): asking again changes nothing
                try:
                    wait = max(poll_s, float(response.headers.get("retry-after") or poll_s))
                except ValueError:
                    pass
            left = end - time.monotonic()
            if left <= 0:
                raise TimeoutError(f"{self._url} was not ready in {timeout_s:g} s"
                                   + (f": its last answer {last}" if last is not None else ": nothing answered"))
            time.sleep(min(wait, left))
        if example is not Link._NONE:
            self.act(example)

    def _ask_first(self) -> None:
        """Before the first act, when nothing the server said has been heard yet: one GET at `ping_path`, so that the
        first act already sends its pictures as JPEG and its arrays compressed where the server restores them (serve()
        names what it reads on every answer, its warm-up's 503 among them). Asked once; whatever stops it - no answer,
        an error - leaves the first act to go as it would have, and its own answer says what the server reads.
        WHY: a robot that acts without wait_until_ready() first sent its first act as arrays, 301,473 bytes where the
        next ones were about 15 KB."""
        self._asked = True
        try:
            with self._busy:
                response = self._client.get(self._ping_path, timeout=self._timeout)
        except (self._httpx.TransportError, self._httpx.TimeoutException):
            return
        self._learn(response)
        if response.status_code == 200:
            self._take_identity(response)

    def observe(self, observation: Any) -> None:
        """Hold `observation` for the next act(). Nothing is sent: an act() given no observation uploads the newest
        one held, and only that one."""
        self._observed = observation

    def pack(self, observation: Any = _NONE) -> "Packed":
        """The body act() sends for `observation` - given none, the one observe() was handed last - as this link sends
        it now: its pictures as JPEG and its large arrays compressed while the server restores them. Made once, it may
        be sent by post() on this link or on another to the same server: network.lines sends one act's body on each of
        a robot's uplinks. With no observation given and none observed, ValueError."""
        if observation is Link._NONE:
            if self._observed is Link._NONE:
                raise ValueError("act() was given no observation and observe() has not been called: hand one to either")
            observation = self._observed
        if (self._reads is None and not self._asked and self._ping_path is not None
                and (self._jpeg is None or self._compress is None)):
            self._ask_first()                # nothing heard yet: what the server reads, before the first act
        packing = time.perf_counter()
        value, pictures = observation, 0
        if self.sends_jpeg:
            try:
                value, pictures = frames.pack_pictures(observation)
            except ImportError as missing:       # no Pillow on this robot: its pictures go as arrays
                if self._jpeg is True:
                    raise
                self._jpeg = False
                _warn.warn(f"the server reads pictures as JPEG, and this robot cannot encode them ({missing}); they "
                           "are sent as arrays")
        squeeze = self._squeeze_now()
        value = squeeze.apply(value) if squeeze is not None else value
        body = msgpack_io.pack(value)
        self._stats.sample("pack_us", (time.perf_counter() - packing) * 1e6)
        return Packed(body, pictures, squeeze)

    def post(self, packed: "Packed", *, path: Optional[str] = None, request_id: Optional[str] = None,
             note: bool = True) -> Any:
        """Send `packed`, pack()'s body, and return the server's response as act() does. `request_id` names the act
        (REQUEST_HEADER), the same on each copy of it. `note`: whether this answer's time goes into the compression's
        estimate of the uplink - network.lines notes the answer it uses alone. The request's time on the way, less
        the server's own, is kept as `last_carried_s`."""
        body, pictures, squeeze = packed
        sent = {"content-type": msgpack_io.MEDIA_TYPE}
        halves = self._splits_now(len(body))
        if request_id is not None or halves:     # the act its halves are joined into, by the server
            sent[REQUEST_HEADER] = request_id or _request_id()
        first = not self._answered
        waits = max(self._timeout, self._first_timeout) if first else self._timeout
        timeout = self._httpx.Timeout(self._timeout, read=waits) if first else self._timeout
        queued_us, queued = now_us(), time.perf_counter()
        response, started, took = self._post_once(path, body, timeout, sent, queued, waits, halves=halves)
        if response is None:                     # unreachable, and on_unreachable said to go once more
            response, started, took = self._post_once(path, body, timeout, sent, queued, waits, halves=halves,
                                                      again=True)
        if started - queued > 0.0005:            # it waited for a ping in flight on the connection
            self._stats.count("acts_behind_ping")
            self._stats.sample("ping_wait_us", (started - queued) * 1e6)
        return self._answered_with(response, body, pictures, squeeze, took, queued_us, note)

    def _post_once(self, path: Optional[str], body: bytes, timeout: Any, sent: dict, queued: float, waits: float, *,
                   halves: bool = False, again: bool = False) -> "tuple[Any, float, float]":
        """The act's request, sent once - in two halves, with `halves` (_post_halves): (its response, when it was sent,
        how long it took) - the response None when it could not reach the server and on_unreachable (not called yet
        for this act: `again` False) answered True. Every other failure raises, as act() says."""
        unreached: Optional[BaseException] = None
        with self._busy:
            started = time.perf_counter()
            self._act_sent(queued, started)
            try:
                if halves:
                    response = self._post_halves(path or self._act_path, body, timeout, sent)
                else:
                    response = self._client.post(path or self._act_path, content=body, timeout=timeout, headers=sent)
            except self._httpx.ReadTimeout as late:
                # the server may still be running it, and the next act waits behind it: as long as a first one
                self._answered = False
                raise self._httpx.ReadTimeout(
                    f"no response from {self._url} in {waits:g} s. The server may still be running this act - a "
                    "model's first inference compiles it, often for tens of seconds - and the next act waits for it "
                    "first, as long as a first act waits. Wait for the server once, before the robot moves, with "
                    "wait_until_ready(example=observation), or give connect() a longer first_timeout= (now "
                    f"{self._first_timeout:g} s) or timeout= (now {self._timeout:g} s)",
                    request=getattr(late, "_request", None)) from late
            except (self._refused, self._httpx.ConnectTimeout) as failed:
                unreached = failed
            took = time.perf_counter() - started
        if unreached is not None:
            if not again and self._unreachable(unreached):
                self._stats.count("unreachable_retries")
                return None, started, took
            if isinstance(unreached, self._refused):
                # the same error, with what to check: the operating system's message alone names no address
                raise self._refused(
                    f"{unreached}: no response from {self._url}. Is the policy server running there, listening on "
                    "an address this machine can reach (0.0.0.0, not 127.0.0.1, for another machine), on that port?",
                    request=getattr(unreached, "_request", None)) from unreached
            raise unreached
        return response, started, took

    def _unreachable(self, failed: BaseException) -> bool:
        """on_unreachable's word on a request that could not reach the server (`failed`): True to send it once more.
        False with none given; the callback's own error raises `failed`, with the callback's as its cause."""
        if self._on_unreachable is None:
            return False
        try:
            return bool(self._on_unreachable(self))
        except Exception as e:  # noqa: BLE001 - the robot meets its request's own error, the callback's beneath it
            raise failed from e

    def _answered_with(self, response: Any, body: bytes, pictures: int, squeeze: Any, took: float, queued_us: int,
                       note: bool) -> Any:
        """The act's answer, from its response: what the response says learned, its times kept, its body read."""
        if self._warm is not None:
            self._warm.used()                # idle time counts from the response: no ping for `ping_every_s` after it
        self._learn(response)
        response.raise_for_status()
        self._answered = True
        timing = response.headers.get("server-timing")
        self.last_server_s = _server_seconds(timing) if timing else None
        self.last_body_bytes = len(body)
        # what this link's bytes cost: the response time, less the processing time the server reports
        self.last_carried_s = max(0.0, took - _server_seconds(timing))
        if squeeze is not None and note:
            squeeze.uplink.note(len(body), self.last_carried_s)
        self._stats.since("act_us", queued_us)
        self._stats.count("acts")
        if pictures:
            self._stats.count("pictures", pictures)
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return msgpack_io.unpack(response.content)

    def act(self, observation: Any = _NONE, *, path: Optional[str] = None) -> Any:
        """Post `observation` - given none, the one observe() was handed last - and return the server's response: numpy
        arrays are sent and returned as arrays. A status of 400 or more raises httpx.HTTPStatusError; no server at the
        address raises httpx.ConnectError, with a message stating what to check. With no observation given and none
        observed, ValueError. Until one act has been answered, an act waits up to `first_timeout` for its response."""
        return self.post(self.pack(observation), path=path)

    def stats(self) -> dict:
        """The requests and pings so far and the latencies' p50, p95 and p99 (latency_stats.LatencyStats.snapshot):
        act_us from when act() queued each request to its response, ping_wait_us for those that waited behind a ping in
        flight (acts_behind_ping counts them), pack_us for building each request's body; pings_yielded, the pings left
        out for the robot's next act (ping_yield); acts_in_halves, the acts sent in two halves (split), and
        acts_whole_again, those of them sent whole again when the second half did not reach the server."""
        return self._stats.snapshot()

    def close(self) -> None:
        """Stop the pings and close the connections."""
        if self._warm is not None:
            self._warm.close()
        self._client.close()
        if self._second is not None:
            self._second_thread.shutdown(wait=False, cancel_futures=True)
            self._second.close()

    def __enter__(self) -> "Link":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def connect(url: str, *, lines: Optional[Any] = None, **options: Any) -> Any:
    """A Link to the server at `url` (Link's options: act_path, ping_path, ping_every_s, ping_for_s, ping_yield,
    compress, jpeg, timeout, first_timeout, token, headers, check, bind - the network interface it leaves by,
    network.bind -, on_unreachable - called with the link when an act cannot reach the server: True, and the act goes
    once more -, split - an act in two halves on two connections when its window has restarted). With
    `lines` - network interfaces (["eth0", "wwan0"]), or {interface: address} where the server has another address by
    each - a network.lines.Lines: a connection by each, every act sent on each, the first answer used."""
    if lines is not None:
        from . import lines as _lines      # here: lines.py imports this module
        return _lines.connect(url, lines=lines, **options)
    return Link(url, **options)
