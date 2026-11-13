"""
The transport every client a `seq` command makes reads the platform through (RetryReads): a GET - a read, which changes
nothing - asked again on a new connection when its connection fails (none made in time, reset, dropped, closed before
the answer came, no answer in time), TRIES tries in all after PAUSES_S, the try after a connection that was never made
going out from the other address family (IPv4 after the first, then IPv6); each retry said on stderr; every try failed,
one sentence - what was read, how many tries over how long, the last failure, that the network between this machine and
the platform failed and that nothing was changed. A write - POST, PUT, PATCH, DELETE - goes out once, as before: it may
have reached the platform. One made to go out over IPv4 alone (local_address, a Transport's ipv4) keeps every try to it.
A test answers through its own transport: RetryReads(inner) wraps it, and _transport() makes every connection the network
gets.

WHY: a user's reads timed out, were reset or took 33 s while the platform answered every one that reached it in
0.7-3.3 s; the machine's connections went out over IPv6 and IPv4 by turns then, and every read command was one try with
one 30 s wait, ending on the transport's own words ("[Errno 54] Connection reset by peer").


"""
from __future__ import annotations

import sys
import time

import httpx

from seq.errors import transport_said
from sequence_ai._core.transport import read_again_wait

TRIES = 3
PAUSES_S = (0.5, 1.5)
CONNECT_S, READ_S = 10.0, 20.0

RETRIED = (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ReadError, httpx.RemoteProtocolError,
           httpx.WriteError, httpx.WriteTimeout)

_FROM = ("0.0.0.0", "::")


class ReadFailed(httpx.TransportError):
    """A read whose every try failed: its text the sentence a command says, after "could not reach the platform at
    <base>:" (seq.errors.unreachable)."""


def _transport(**kwargs) -> httpx.BaseTransport:
    """A transport over the network (`local_address`: where its connections go out from)."""
    return httpx.HTTPTransport(**kwargs)


def _say(line: str) -> None:
    print(line, file=sys.stderr)


class RetryReads(httpx.BaseTransport):
    """A client's transport: its reads asked again while their connection fails, its writes sent once. `inner`: the
    transport a test answers through (every try goes to it); None, the network's - a new connection for each retry."""

    def __init__(self, inner: httpx.BaseTransport | None = None, *, local_address: str | None = None) -> None:
        self._inner = inner
        self._local = local_address
        self._first: httpx.BaseTransport | None = None

    def _pooled(self) -> httpx.BaseTransport:
        if self._first is None:
            self._first = self._inner or _transport(**({"local_address": self._local} if self._local else {}))
        return self._first

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        if request.method != "GET":
            return self._pooled().handle_request(request)
        request.extensions["timeout"] = {**request.extensions.get("timeout", {}), "connect": CONNECT_S, "read": READ_S}
        started, side, last = time.monotonic(), self._local, None
        for n in range(1, TRIES + 1):
            fresh = None
            try:
                if n == 1:
                    transport = self._pooled()
                else:
                    transport = fresh = self._inner or _transport(**({"local_address": side} if side else {}))
                response = transport.handle_request(request)
                response.read()



                wait = read_again_wait(response) if n < TRIES else None
                if wait is None:
                    return response
                response.close()
                if fresh is not None and fresh is not self._inner:
                    fresh.close()
                why = ("this key made more requests than its minute allows" if response.status_code == 429
                       else "the platform's database was busy")
                _say(f"{why}; asking again in {wait:g} s (try {n + 1} of {TRIES})")
                time.sleep(wait)
                continue
            except RETRIED as exc:
                last = exc
                if fresh is not None and fresh is not self._inner:
                    fresh.close()
                if n == TRIES:
                    break
                if isinstance(exc, (httpx.ConnectError, httpx.ConnectTimeout)) and self._local is None:
                    side = _FROM[1] if side == _FROM[0] else _FROM[0]
                _say(f"{transport_said(exc)}; asking the platform again in {PAUSES_S[n - 1]:g} s on a new connection "
                     f"(try {n + 1} of {TRIES})")
                time.sleep(PAUSES_S[n - 1])
        what = request.url.path + (f"?{request.url.query.decode()}" if request.url.query else "")
        raise ReadFailed(f"reading {what}: {TRIES} tries over {time.monotonic() - started:.1f} s failed, the last: "
                         f"{transport_said(last)} ({last}) - the network between this machine and the platform is "
                         "failing; nothing was changed, run the command again", request=request) from last

    def close(self) -> None:
        if self._first is not None:
            self._first.close()
