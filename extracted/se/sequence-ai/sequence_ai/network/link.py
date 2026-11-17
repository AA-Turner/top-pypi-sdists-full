# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The client-side components, applied to one connection to your own server.

    from sequence_ai.network import connect

    link = connect("http://your-gpu:8000")                 # BBR and TCP keepalive, where this machine allows them
    response = link.act({"image": frame, "state": state})  # msgpack both ways; a ping while the connection is idle
    link.close()

observe() then act() is the same request in two calls, the two a robot makes on a policy it reaches by name
(sequence_ai.connect), so one control loop runs against either:

    link.observe({"image": frame, "state": state})         # held here; nothing is sent
    response = link.act()                                   # uploads the newest observation

In one sentence: connect() opens one httpx connection with window.socket_options() on its socket → act() packs the
observation with msgpack_io (its large arrays compressed first, where `compress=True` and that saves time), posts it and
reads the response → between requests a small GET is sent on the same connection after each `ping_every_s` of idle time
(window.Warm) → each request's time is recorded (latency_stats) and read with stats().

WHY one connection and a lock: an HTTP/1.1 client that starts a request while a ping is in flight opens a second
connection for it, with a new handshake and a cold window, which is exactly what the ping is there to prevent. So the
pool holds one connection, a ping is skipped while a request is in flight, and a request that starts while a ping is in
flight waits for it: one round trip at most, and only when the two coincide.

What the server needs: `act_path`, a POST that takes a msgpack body (msgpack_io.unpack reads it) and responds with
msgpack or JSON; and any cheap GET at `ping_path` (None: no pings). `compress=True` needs a server that decompresses the
arrays (compressed.expand): leave it off against one that does not. If the server reports its own processing time in the
standard Server-Timing header (`act;dur=276.0`, milliseconds), that time is excluded from the estimated cost of the
upload; if it does not, a slow model is counted as a slow link, and compression is judged to save more than it does.

Whether any of it helps depends on the link: bench/ measures yours.

Needs httpx, which sequence-ai installs.
"""
from __future__ import annotations

import threading
import time
from typing import Any, Optional

from . import compress as _compress
from . import msgpack_io, wifi_power, window
from .latency_stats import LatencyStats, now_us


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


class Link:
    """One connection to a policy server, with the client-side components applied to it (the module's docstring)."""

    _NONE: Any = object()                    # no observation: act() sends the one observe() was handed last

    def __init__(self, url: str, *, act_path: str = "/act", ping_path: Optional[str] = "/ping",
                 ping_every_s: float = 0.1, ping_for_s: float = 60.0, compress: bool = False, timeout: float = 10.0,
                 headers: Optional[dict] = None, check: bool = True) -> None:
        try:
            import httpx
        except ImportError as missing:
            raise ImportError('connect() uses httpx for its connection, and httpx is not installed: '
                              'pip install httpx') from missing

        if check:
            wifi_power.check_once()          # warns once, on its own thread: Wi-Fi power saving, if it is on
            window.check()                   # warns once: a machine that restarts its window after each pause
        transport = httpx.HTTPTransport(socket_options=window.socket_options(),
                                        limits=httpx.Limits(max_connections=1, max_keepalive_connections=1))
        self._client = httpx.Client(base_url=url, transport=transport, timeout=timeout, headers=headers)
        self._url, self._refused = url, httpx.ConnectError
        self._act_path, self._ping_path = act_path, ping_path
        self._busy = threading.Lock()        # held by the request or the ping in flight: the connection carries one
        self._squeeze = _compress.Squeeze() if compress else None
        self._stats = LatencyStats(counters=["acts", "pings"], latencies=["act_us"])
        self._warm = window.Warm(self._ping, every_s=ping_every_s, for_s=ping_for_s) if ping_path else None
        self._observed: Any = Link._NONE

    def _ping(self) -> None:
        if not self._busy.acquire(blocking=False):
            return                           # a request is in flight: the connection is not idle
        try:
            self._client.get(self._ping_path)
            self._stats.count("pings")
        finally:
            self._busy.release()

    def observe(self, observation: Any) -> None:
        """Hold `observation` for the next act(). Nothing is sent: an act() given no observation uploads the newest
        one held, and only that one."""
        self._observed = observation

    def act(self, observation: Any = _NONE, *, path: Optional[str] = None) -> Any:
        """Post `observation` - given none, the one observe() was handed last - and return the server's response: numpy
        arrays are sent and returned as arrays. A status of 400 or more raises httpx.HTTPStatusError; no server at the
        address raises httpx.ConnectError, with a message stating what to check. With no observation given and none
        observed, ValueError."""
        if observation is Link._NONE:
            if self._observed is Link._NONE:
                raise ValueError("act() was given no observation and observe() has not been called: hand one to either")
            observation = self._observed
        value = self._squeeze.apply(observation) if self._squeeze is not None else observation
        body = msgpack_io.pack(value)
        with self._busy:
            sent, started = now_us(), time.perf_counter()
            try:
                response = self._client.post(path or self._act_path, content=body,
                                             headers={"content-type": msgpack_io.MEDIA_TYPE})
            except self._refused as refused:
                # the same error, with what to check: the operating system's message alone names no address
                raise self._refused(
                    f"{refused}: no response from {self._url}. Is the policy server running there, listening on "
                    "an address this machine can reach (0.0.0.0, not 127.0.0.1, for another machine), on that port?",
                    request=getattr(refused, "_request", None)) from refused
            took = time.perf_counter() - started
        if self._warm is not None:
            self._warm.used()                # idle time counts from the response: no ping for `ping_every_s` after it
        response.raise_for_status()
        if self._squeeze is not None:
            # what this link's bytes cost: the response time, less the processing time the server reports
            carried = took - _server_seconds(response.headers.get("server-timing"))
            self._squeeze.uplink.note(len(body), max(0.0, carried))
        self._stats.since("act_us", sent)
        self._stats.count("acts")
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return msgpack_io.unpack(response.content)

    def stats(self) -> dict:
        """The requests and pings so far and the requests' p50, p95 and p99 (latency_stats.LatencyStats.snapshot)."""
        return self._stats.snapshot()

    def close(self) -> None:
        """Stop the pings and close the connection."""
        if self._warm is not None:
            self._warm.close()
        self._client.close()

    def __enter__(self) -> "Link":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def connect(url: str, **options: Any) -> Link:
    """A Link to the server at `url` (Link's options: act_path, ping_path, ping_every_s, ping_for_s, compress,
    timeout, headers, check)."""
    return Link(url, **options)
