# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
Each client connection's transport-level state, read from the server's own kernel (Linux's TCP_INFO): the smoothed
round-trip time (RTT) and its variance, the retransmitted segments (unacknowledged now, and in total), the congestion
window and the delivery rate. Also how long a request's upload took, from the bytes that carried its head to those that
carried the last part of its body: about one RTT when it was sent in two flights.

    from sequence_ai.network import tcp_link

    tcp_link.read(sock)              # any connected socket's values, or None where the kernel provides none
    tcp_link.of(scope["client"])     # in an ASGI app served with one_write_http(): the request's own connection

In one sentence: the HTTP protocol uvicorn runs registers each connection by its peer's address and records the time
whenever bytes arrive on it (register, Connection.came: one_write.py) → a request's upload time is the interval between
the arrival of its head and the arrival of the last part of its body (Arrival, upload_ms), and its connection's TCP_INFO
is read once its body has arrived (of) → a server keeps each client's recent values in a Window (Window.add) and
summarizes them (Window.summary: the RTT's p50 and p95, retransmitted segments per minute, the share of uploads that
took two round trips or more).

WHY on the server: a client's own OS may not expose its counters to the process that runs there (macOS withholds them
from an unprivileged process), and the server reads every client the same way: these are the numbers a network change is
measured against. Where the kernel provides none (not Linux, or a sandbox that withholds them) the fields are omitted
and the request proceeds. A peer at a private address is a tunnel or a proxy in front of the server (or a client on the
server's own network): its numbers describe that hop, and are marked as such (peer_private). The upload is timed by when
its bytes arrived, not by when the server read them, so a server busy with other requests does not report a two-flight
upload as one.
"""
from __future__ import annotations

import collections
import ipaddress
import socket
import struct
import sys
import time
from typing import Any

# struct tcp_info (linux/tcp.h): the fields read and their byte offsets; a shorter struct (an older kernel) omits
# the fields past its end.
_U32 = {"retrans": 36, "rtt_us": 68, "rttvar_us": 72, "snd_cwnd": 80, "total_retrans": 100}
_DELIVERY_RATE = 160        # __u64 tcpi_delivery_rate, bytes per second (Linux 4.9 and later)
_BUFFER = 232
# parse() reads Linux's struct tcp_info. A Mac's Python can define socket.TCP_INFO too (0x200, for Apple's own struct
# tcp_info, a different layout): read as Linux's, every field would be wrong. So the platform decides, not the name.
_LINUX = sys.platform.startswith("linux")
# The most connections registered at once (closed ones are removed as new ones are registered).
_PEERS_KEPT = 4096
# The shortest upload time counted as two round trips (Window.summary), whatever the RTT.
TWO_TRIP_MIN_MS = 1.0


class Connection:
    """A connection the HTTP protocol serves (register): its transport, and when bytes last arrived on it."""

    __slots__ = ("transport", "last_in")

    def __init__(self, transport) -> None:
        self.transport, self.last_in = transport, None

    def came(self) -> None:
        """Record that bytes arrived: called by the connection's protocol before it reads them."""
        self.last_in = time.perf_counter()


_peers: collections.OrderedDict[tuple[str, int], Connection] = collections.OrderedDict()


def parse(raw: bytes) -> dict | None:
    """The fields read from a struct tcp_info: rtt_ms, rttvar_ms, retrans, total_retrans, cwnd and, where the kernel
    provides it, delivery_kbps. None for a struct too short to hold the RTT."""
    if len(raw) < _U32["rtt_us"] + 4:
        return None
    got = {name: struct.unpack_from("=I", raw, at)[0] for name, at in _U32.items() if len(raw) >= at + 4}
    out = {"rtt_ms": round(got["rtt_us"] / 1000.0, 3)}       # the kernel's microseconds, at full precision
    if "rttvar_us" in got:
        out["rttvar_ms"] = round(got["rttvar_us"] / 1000.0, 3)
    for name, key in (("retrans", "retrans"), ("total_retrans", "total_retrans"), ("snd_cwnd", "cwnd")):
        if name in got:
            out[key] = got[name]
    if len(raw) >= _DELIVERY_RATE + 8:
        out["delivery_kbps"] = round(struct.unpack_from("=Q", raw, _DELIVERY_RATE)[0] * 8 / 1000.0, 1)
    return out


def read(sock: socket.socket | None) -> dict | None:
    """The fields read from `sock`'s TCP_INFO (see parse), or None where the kernel provides none."""
    opt = getattr(socket, "TCP_INFO", None)
    if not _LINUX or opt is None or sock is None:
        return None
    try:
        return parse(sock.getsockopt(socket.IPPROTO_TCP, opt, _BUFFER))
    except (OSError, ValueError, TypeError, struct.error):
        return None


def register(transport: Any) -> Connection | None:
    """Register `transport` (the one asyncio created for a connection, before anything wraps it) under its peer's
    address, and return the Connection its protocol records byte arrivals on. The protocol uvicorn runs calls this as
    each connection is made; connections closed since are removed here. Returns None for a peer with no address (a Unix
    socket)."""
    peer = transport.get_extra_info("peername")
    if not isinstance(peer, tuple) or len(peer) < 2:
        return None
    for key in [k for k, c in _peers.items() if c.transport.is_closing()]:
        del _peers[key]
    key = (str(peer[0]), int(peer[1]))
    conn = _peers[key] = Connection(transport)
    _peers.move_to_end(key)
    while len(_peers) > _PEERS_KEPT:
        _peers.popitem(last=False)
    return conn


def _connection(client) -> Connection | None:
    """The open connection a request arrived on, looked up by `client`, its (host, port) from the ASGI scope; None for
    one that is not registered, is closed, or whose client address a trusted proxy's X-Forwarded-For replaced (uvicorn's
    proxy headers)."""
    if not client or len(client) < 2:
        return None
    try:
        conn = _peers.get((str(client[0]), int(client[1])))
    except (TypeError, ValueError):
        return None
    return conn if conn is not None and not conn.transport.is_closing() else None


def _private(host) -> bool:
    try:
        ip = ipaddress.ip_address(str(host))
    except ValueError:
        return False
    # an IPv4 peer of a dual-stack socket appears as ::ffff:a.b.c.d, and older Python versions report every such
    # address as private
    ip = getattr(ip, "ipv4_mapped", None) or ip
    return ip.is_private or ip.is_loopback


def of(client: Any) -> dict | None:
    """The TCP_INFO fields of the connection a request arrived on (`client` as _connection takes it), with peer_private
    set where that peer is at a private address; None when the connection is not found or the kernel provides none."""
    conn = _connection(client)
    got = read(conn.transport.get_extra_info("socket")) if conn is not None else None
    if got is not None and _private(client[0]):
        got["peer_private"] = True
    return got


def _p(values: list[float], q: float) -> float | None:
    if not values:
        return None
    v = sorted(values)
    return round(v[min(len(v) - 1, int(round(q * (len(v) - 1))))], 3)


class Window:
    """Each robot's link measurements over its recent requests, keyed by a session id the caller chooses: the newest
    `acts` requests of the newest `robots` robots. A robot's retransmitted segments are counted per connection, since
    the kernel's counter is cumulative from the moment a connection opens, so a robot that reconnects is counted from
    the start of its new connection."""

    def __init__(self, acts: int = 300, robots: int = 1024) -> None:
        self._acts, self._robots = acts, robots
        self._by: collections.OrderedDict = collections.OrderedDict()
        self._totals: collections.OrderedDict = collections.OrderedDict()     # a connection's count at its last request

    def add(self, session: str | None, now: float, link: dict | None, upload_ms: float | None,
            client: Any = None) -> None:
        """Record one request from `session`'s client: its connection's fields (of) and its upload time (upload_ms). A
        request whose connection the kernel reported nothing for is skipped, so a server that can read no TCP_INFO
        reports no link summary."""
        if not session or link is None:
            return
        sent_again = 0
        total = link.get("total_retrans")
        if isinstance(total, int) and client:
            key = (str(client[0]), client[1])
            sent_again = max(0, total - self._totals.get(key, 0))
            self._totals[key] = total
            self._totals.move_to_end(key)
            while len(self._totals) > self._robots * 4:
                self._totals.popitem(last=False)
        acts = self._by.get(session)
        if acts is None:
            acts = self._by[session] = collections.deque(maxlen=self._acts)
        self._by.move_to_end(session)
        while len(self._by) > self._robots:
            self._by.popitem(last=False)
        acts.append((now, link.get("rtt_ms"), sent_again, upload_ms, bool(link.get("peer_private"))))

    def summary(self, session: str | None, now: float) -> dict | None:
        """A summary of `session`'s robot over its retained requests: how many and over how long, its RTT p50 and p95,
        its retransmitted segments per minute (computed over at least one minute, so two requests a second apart do not
        appear as a burst), and the share of its uploads that took two round trips or more. An upload counts as two
        round trips when it took at least half its RTT and at least TWO_TRIP_MIN_MS; the second bound keeps the event
        loop's own jitter from counting on a link with an RTT of a fraction of a millisecond, where a second flight
        costs nothing. None for a robot with no requests."""
        acts = self._by.get(session) if session else None
        if not acts:
            return None
        rtts = [a[1] for a in acts if isinstance(a[1], (int, float))]
        span = max(0.0, now - acts[0][0])
        timed = [(a[3], a[1]) for a in acts if isinstance(a[3], (int, float)) and isinstance(a[1], (int, float))]
        out = {"acts": len(acts), "window_s": round(span, 1), "rtt_p50_ms": _p(rtts, 0.5), "rtt_p95_ms": _p(rtts, 0.95),
               "retrans_per_min": round(sum(a[2] for a in acts) / (max(span, 60.0) / 60.0), 2),
               "two_trip_share": round(sum(1 for up, rtt in timed if up >= max(rtt / 2.0, TWO_TRIP_MIN_MS))
                                       / len(timed), 3) if timed else None}
        if any(a[4] for a in acts):
            out["peer_private"] = True
        return out


class Arrival:
    """ASGI middleware, the outermost of an app's. For an HTTP request on a connection the protocol registered
    (register), it records when the request's head arrived and when the last part of its body arrived; upload_ms is the
    time between the two. A body that arrived with its head took no time; one whose last part arrived a flight later
    took about one RTT."""

    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        conn = _connection(scope.get("client")) if scope.get("type") == "http" else None
        if conn is None or conn.last_in is None:
            return await self.app(scope, receive, send)
        # The request starts with the bytes that completed its head, before any later bytes are read.
        state = scope.setdefault("state", {})
        state["sequence_ai_head_in"] = conn.last_in

        async def timed():
            message = await receive()
            if message.get("type") == "http.request" and not message.get("more_body", False):
                state["sequence_ai_body_in"] = conn.last_in        # the arrival time of the last part of its body
            return message

        await self.app(scope, timed, send)


def upload_ms(scope: dict) -> float | None:
    """A request's upload time in ms, from the bytes that carried its head to those that carried the last part of its
    body (Arrival): 0 when the body arrived with the head; None before the body has been read, or for a request no
    Arrival timed (a streamed one, or one on a connection that was not registered)."""
    state = scope.get("state") or {}
    head, body = state.get("sequence_ai_head_in"), state.get("sequence_ai_body_in")
    if not isinstance(head, float) or not isinstance(body, float):
        return None
    return round(max(0.0, body - head) * 1000.0, 3)
