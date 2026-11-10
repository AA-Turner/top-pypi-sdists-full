"""
The HTTP layer. One connection, held open.

── The entire reason this file exists ────────────────────────────────
One connection, held open. Every /v1/act reuses a single kept-alive TCP+TLS connection instead
of paying a fresh handshake per call — that saving is the whole latency story below, and the
reason the SDK, not a hand-rolled HTTP call, is the way in.

Measured against the production gateway on 2026-09-06, six samples each:

    new connection each time   median 305.9 ms   (min 246.7, max 766.7)
    one reused connection      median 121.0 ms   (min 116.8, max 133.4)

    handshake cost = 184.9 ms per call, 60% of the total





That 184.9 ms is easy to lose: any client that opens a new connection per call pays it back in
full and makes the platform look three times slower than it is. The SDK holds one connection so
every caller is on the fast path by default rather than by remembering to be.

Why it matters concretely: a chunk covers between 0.50 s and 2.13 s of motion depending on the
model, and a refill has to finish inside that window or the arm stops between chunks. On
pi05-droid, whose chunk covers 1.00 s, a warm end-to-end /v1/act measured 793 ms — so 184.9 ms
of handshake is not a rounding error against it; it is a fifth of the entire budget.




An earlier version of this note said "128 ms of inference" and concluded that reuse took the
window from 87% to 50%. That number is the model's **GPU time on an H100**
— it
excludes the gateway hop, the dispatch to a worker, image upload and decode, and the return trip. Using
it as the cost of a refill understated the real figure by roughly six times, and the 87%/50%
arithmetic built on it did not hold. The correction is left visible because the mistake is an
easy one to repeat: the catalogue publishes a latency per model, and it is not end-to-end.
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Callable, Iterator
from typing import Any, Optional

import httpx

from .rid import HEADER as RID_HEADER

DEFAULT_BASE_URL = "https://api.generalsequences.com"



DEFAULT_TIMEOUT_S = 30.0

from ..errors import (
    AuthError,
    Unavailable,
    from_response,
    not_the_platform,
)







_THROUGH: Optional[Callable[[], httpx.BaseTransport]] = None







DATABASE_BUSY = "database_busy"
BUSY_TRIES = 3
BUSY_MAX_S = 5.0


def database_busy_wait(response: httpx.Response) -> Optional[float]:
    """Seconds to wait before asking a read again when `response` is the gateway's database_busy 503; else None. Its
    body read here (`response.read()`), so the caller can still use it."""
    if response.status_code != 503:
        return None
    try:
        body = json.loads(response.read() or b"null")
        details = body.get("details") if isinstance(body, dict) else None
        if not isinstance(details, dict) or details.get("reason") != DATABASE_BUSY:
            return None
        asked = float(response.headers.get("Retry-After") or 1.0)
    except (ValueError, TypeError, httpx.HTTPError):
        return None
    return max(0.0, min(asked, BUSY_MAX_S))


def rate_limited_wait(response: httpx.Response) -> Optional[float]:
    """Seconds to wait before asking a read again when `response` is the gateway's 429 for a key over its requests a
    minute, its Retry-After the seconds until the minute frees one (at most BUSY_MAX_S); else None - a 429 naming no
    wait is the caller's.
"""
    if response.status_code != 429:
        return None
    try:
        asked = float(response.headers.get("Retry-After") or "")
    except (ValueError, TypeError):
        return None
    return max(0.0, min(asked, BUSY_MAX_S))




_STRANGER_WAITS = (0.2, 0.8)



_SAID_BY_ITS_STATUS = frozenset({405, 413, 414, 429, 431, 502, 503, 504})


def _by_the_platform(r: httpx.Response) -> bool:
    """Whether a server of ours wrote this answer: its request id, or its error body's own fields."""
    if r.headers.get(RID_HEADER):
        return True
    try:
        body = r.json()
    except Exception:
        return False
    return isinstance(body, dict) and ("code" in body or "detail" in body)


def _a_strangers(r: httpx.Response) -> bool:
    """Whether this answer from the gateway's address is a non-2xx no server of ours wrote (errors.not_the_platform)."""
    return r.status_code >= 300 and r.status_code not in _SAID_BY_ITS_STATUS and not _by_the_platform(r)


def read_again_wait(response: httpx.Response) -> Optional[float]:
    """Seconds to wait before asking a read again - the platform's database busy (database_busy_wait), its key over its
    requests a minute (rate_limited_wait) - else None."""
    wait = database_busy_wait(response)
    return wait if wait is not None else rate_limited_wait(response)


def _no_key(login: bool, robot_of: Optional[str]) -> str:
    """What a call with no key is told: a robot's (connect(), `robot_of` the policy it connects to), how its robot key is
    made - a robot never uses your seq login sign-in; any other, where a key is set or made.
    
"""
    if robot_of:
        return (f"no API key. A robot connects with its policy's robot key, which seq robot add --policy {robot_of} "
                "makes: set SEQUENCES_API_KEY to it or pass api_key=... (a seq login sign-in is yours, never a robot's)")
    return ("no API key. Set SEQUENCES_API_KEY or pass api_key=..." + (", or sign in with seq login" if login else "")
            + ". Create a key at https://app.generalsequences.com/")


def send_through(make: Optional[Callable[[], httpx.BaseTransport]]) -> None:
    """Every Transport made from now on in this process sends through `make()`, a transport of its own each; None puts
    httpx's own back. For a command-line process around its command - never a robot's."""
    global _THROUGH
    _THROUGH = make


class Transport:
    """
    A thin wrapper over one long-lived `httpx.Client`.

    Not a connection pool per call, not a new client per call — one client, created in
    `connect()` and closed when the context manager exits. `httpx` keeps the underlying
    connection alive between requests on its own; the only thing required of us is to stop
    throwing the client away.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout_s: float | None = DEFAULT_TIMEOUT_S,
        *,
        require_key: bool = True,
        login: bool = False,
        person: bool = False,
        robot_of: str | None = None,
    ) -> None:
        self._base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")




        from sequence_ai._core.login import PERSON_REFUSAL, LoginAuth, login_for

        key = None if person else (api_key or os.environ.get("SEQUENCES_API_KEY"))
        signed_in = login_for(self._base) if (person or (login and not key)) else None
        if person and signed_in is None:
            raise AuthError(PERSON_REFUSAL, details={"reason": "person_only"})








        if not key and signed_in is None and require_key:
            raise AuthError(_no_key(login, robot_of))



        self.answered = False
        self._client = httpx.Client(
            base_url=self._base,



            timeout=DEFAULT_TIMEOUT_S if timeout_s is None else timeout_s,
            headers={



                **({"Authorization": f"Bearer {key}"} if key else {}),
                "Content-Type": "application/json",




                "User-Agent": f"sequence-ai-python/{_version()}",
            },


            limits=httpx.Limits(max_keepalive_connections=4, keepalive_expiry=300.0),

            **({"transport": _THROUGH()} if _THROUGH is not None else {}),

            **({"auth": LoginAuth(signed_in)} if signed_in is not None else {}),
        )

    def post(self, path: str, payload: dict[str, Any],
             timeout_s: float | None = None, *,
             rid: Optional[str] = None, metrics: Any = None) -> dict[str, Any]:
        """
        POST and translate the outcome into one of our typed errors.

        `timeout_s` overrides the client default for this one call. It exists for exactly one
        situation: a run's first act, whose worker may still compile the batch size it is first
        sent - a first forward at a size it has not run compiles there, past 30 s for pi05-droid
        v19 on dev (10-15, p95 31469 ms). Against the 30 s default that is a timeout, so
        `startup_timeout_s` would never get the chance to wait.


        Deliberately per-call and not a new default: a long read timeout in the steady-state
        loop would turn a hung worker into an arm that waits two minutes instead of reporting
        an underrun and holding position.

        `rid` (when given) is sent as the `X-Seq-Request-Id` header so this call can be correlated
        end to end. `metrics` (a `CallMetrics`) is filled with the pure-HTTP `rtt_ms` and the rid the
        server echoed back — measured around the socket call so it is the round trip and nothing else.
        Both are optional and default off, so every existing caller of `post()` is unchanged.
        """
        headers = {RID_HEADER: rid} if rid else None
        t0 = time.monotonic()
        try:
            if timeout_s is None:
                r = self._past_strangers(lambda: self._client.post(path, json=payload, headers=headers))
            else:
                r = self._past_strangers(lambda: self._client.post(path, json=payload, timeout=timeout_s,
                                                                   headers=headers))
        except httpx.TimeoutException as exc:
            raise Unavailable(f"request timed out after {self._client.timeout.read}s") from exc
        except httpx.TransportError as exc:



            raise Unavailable(f"could not reach {self._base}: {exc}") from exc
        if metrics is not None:


            metrics.rtt_ms = (time.monotonic() - t0) * 1000.0
            metrics.rid_echo = r.headers.get(RID_HEADER)
        return self._answer(r)

    def get(self, path: str) -> dict[str, Any]:
        """GET `path`: its JSON, or its typed error. A read the platform's database did not answer in time, or its key
        over its requests a minute (read_again_wait), is asked again here, up to BUSY_TRIES tries - in a robot's process;
        a command line's reads are asked again by RetryReads, which every client of it sends through (send_through),
        never twice over."""
        for n in range(1, BUSY_TRIES + 1):
            try:
                r = self._past_strangers(lambda: self._client.get(path))
            except httpx.TransportError as exc:
                raise Unavailable(f"could not reach {self._base}: {exc}") from exc
            wait = read_again_wait(r) if _THROUGH is None and n < BUSY_TRIES else None
            if wait is None:
                return self._answer(r)
            time.sleep(wait)
        return self._answer(r)

    def put(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """PUT a settings change (a deployment's scaling) and return what the server now holds."""
        try:
            r = self._past_strangers(lambda: self._client.put(path, json=payload))
        except httpx.TransportError as exc:
            raise Unavailable(f"could not reach {self._base}: {exc}") from exc
        return self._answer(r)

    def post_sse(self, path: str, payload: dict[str, Any],
                 timeout_s: float | None = None) -> Iterator[Any]:
        """
        POST and iterate the reply's server-sent events: each `data:` line decoded from JSON, then
        the literal "[DONE]" that ends the stream.

        The request is sent HERE, eagerly, so a refusal before the stream began — 401, 402, 429, 503,
        a bad body — raises the same typed error post() would, at call time, not on the first next().
        Only after a 2xx is the event iterator returned. The connection is released when the iterator
        ends or is closed, so a caller who stops reading early does not leak it. `timeout_s` bounds
        each read (the gap between events), not the whole stream.
        """
        try:
            cm = (self._client.stream("POST", path, json=payload) if timeout_s is None
                  else self._client.stream("POST", path, json=payload, timeout=timeout_s))
            r = cm.__enter__()
        except httpx.TimeoutException as exc:
            raise Unavailable(f"request timed out after {self._client.timeout.read}s") from exc
        except httpx.TransportError as exc:
            raise Unavailable(f"could not reach {self._base}: {exc}") from exc
        if r.status_code >= 300:

            try:
                r.read()
            finally:
                cm.__exit__(None, None, None)
            self._answer(r)
        return self._sse_events(cm, r)

    def _sse_events(self, cm: Any, r: httpx.Response) -> Iterator[Any]:
        """The decoded `data:` payloads of an open event-stream response; closes it on any exit."""
        try:
            for line in r.iter_lines():
                if not line.startswith("data: "):
                    continue
                data = line[len("data: "):]
                if data == "[DONE]":
                    yield "[DONE]"
                    return
                yield json.loads(data)
        except httpx.TimeoutException as exc:
            raise Unavailable(f"the stream stalled for more than {self._client.timeout.read}s") from exc
        except httpx.TransportError as exc:
            raise Unavailable(f"the stream from {self._base} broke: {exc}") from exc
        finally:
            cm.__exit__(None, None, None)

    @staticmethod
    def _past_strangers(send: Callable[[], httpx.Response]) -> httpx.Response:
        """`send()`'s answer, sent again while it is a 4xx no server of ours wrote (_STRANGER_WAITS): every robot's call
        to the gateway comes through here - its connect, its ready polls, its keepalives. A 5xx is not: something past
        that may have reached the platform."""
        for wait in _STRANGER_WAITS:
            r = send()
            if not (_a_strangers(r) and r.status_code < 500):
                return r
            time.sleep(wait)
        return send()

    def _answer(self, r: httpx.Response) -> dict[str, Any]:
        """`_unwrap` for a call to the gateway: a non-2xx no server of ours wrote is the platform not having answered
        (errors.not_the_platform); a worker's own answers go to `_unwrap` alone. `answered`: a word of the platform's
        has come on this transport, which says its address is right (Policy._nothing_of_ours_there)."""
        if _a_strangers(r):
            raise not_the_platform(r.status_code, text=r.text, headers=r.headers)
        if r.status_code < 300 or _by_the_platform(r):
            self.answered = True
        return self._unwrap(r)

    @staticmethod
    def _unwrap(r: httpx.Response) -> dict[str, Any]:
        """
        The JSON of a 2xx response, or the exception for any other — mapped by `errors.from_response`,
        the one place the SDK does that, so the gateway and a worker answer the same way.

        The server's own message is passed through untouched. It is written for the person
        reading it — replacing it with something generic here would throw away the only part
        of the response that says *why*.
        """
        if r.status_code < 300:
            if (r.headers.get("content-type") or "").startswith("application/x-seq-msgpack"):

                from sequence_ai._core import msgpack_io

                return msgpack_io.unpack(r.content)
            return r.json()
        try:
            body = r.json()
        except Exception:
            body = None
        raise from_response(r.status_code, body, text=r.text, headers=r.headers)

    @property
    def base_url(self) -> str:
        """The host this transport talks to, after the env-var and default fallbacks."""
        return self._base

    def close(self) -> None:
        self._client.close()


def _version() -> str:
    """Package version, or 'dev' when running from a source checkout that was never built."""
    try:
        from importlib.metadata import version

        return version("sequence-ai")
    except Exception:
        return "dev"
