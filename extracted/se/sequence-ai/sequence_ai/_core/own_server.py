"""
A policy server of the robot's owner (serve(), seq serve) as the platform's client reaches it: connect("http://...")
gives the same Policy that connect("name") gives, whose DirectConnection asks this object - not the platform's gateway -
where its worker is. The answer is always the server at the address: its token as the worker's secret, its certificate's
fingerprint where it serves HTTPS, a lease that does not run out, nothing of seats, standbys or moves. Everything
after it - the robot's stream, its observations as it makes them, sequence_ai.Video sent as video, its acts after them,
sending again what the server names missing - is the platform's data plane as it is.

In one sentence: Policy → DirectConnection → OwnGateway.post("/v1/act/connect") answers {worker_url: the address,
direct_secret: the token, cert_fingerprint: the pin, lease} at once, with no request → _WorkerTransport opens its stream
to the address (plain TCP for http://) → every act, post and episode's end goes there; a ready poll (wait_until_ready)
asks the server's GET /ping, which says 503 while it warms up.

WHY the platform's own client, not a second one: a robot's code, what it can do and the numbers it measures are the same
whether its GPU is its own or the platform's - only what connect() is given changes.

"""
from __future__ import annotations

from typing import Any, Callable, Optional

import httpx

from ..errors import AuthError, InvalidRequest, NotFound, PermissionDenied, Unavailable
from .pinned_tls import build_pinned_ssl_context


_ByDefaultRoute = type("_ByDefaultRoute", (), {"bind": None})()


class _ByLine:
    """What on_reconnect is handed for one of the robot's lines that opened again: the interface it goes out by."""

    __slots__ = ("bind",)

    def __init__(self, name: str) -> None:
        self.bind = name

_LEASE_S = 10 * 365 * 24 * 3600.0


_DECLARED = ("hz", "action_chunk_valid_len", "action_chunk_replan_at", "max_wait_for_batch")


class OwnGateway:
    """The control plane a DirectConnection asks, for a server at `url` (module docstring). `token`: serve()'s token,
    sent as the worker's secret (None: the server asks for none); `fingerprint`: the SHA-256 of the certificate an
    https:// server serves (serve(tls=...)), which the connection pins. `pinged`: the server's GET /ping as connect()
    asked it, to know what it serves - its word on how its robots play kept, and not asked again where it gave it."""



    own = True

    def __init__(self, url: str, *, token: Optional[str] = None, fingerprint: Optional[str] = None,
                 timeout_s: float = 10.0, on_reconnect: Optional[Callable[[Any], bool]] = None,
                 pinged: Any = None) -> None:
        self.base_url = url.rstrip("/")
        self._token, self._fingerprint, self._timeout_s = token, fingerprint, timeout_s


        self._on_reconnect = on_reconnect
        self._connects = 0
        self.answered = True
        self.poll_s = 0.5
        self._heard = False
        self._plays: dict = {}
        self._asked = False
        if pinged is not None:
            self._heard = True
            self._take_play(pinged)
            self._asked = pinged.status_code == 200

    def post(self, path: str, body: Any = None, **_: Any) -> dict:
        """The control plane's answers: a connect - the server at the address, and how its robots play an answer where
        it says that (_declared); a seat's keepalive, a release, an episode's label - nothing to keep, give back or
        file."""
        if path.startswith("/v1/act/connect"):
            self._connects += 1
            if self._connects > 1 and self._on_reconnect is not None:
                self._on_reconnect(_ByDefaultRoute)
            return {"worker_url": self.base_url, "direct_secret": self._token or "",
                    "cert_fingerprint": self._fingerprint, "lease": {"epoch": 1, "ttl_s": _LEASE_S}, "params": {},
                    "keepalive": None,
                    **self._declared()}
        if path.startswith(("/v1/act/keepalive", "/v1/act/release")) or path.endswith("/label"):
            return {}
        raise NotFound(f"{path} is the platform's: a server of your own at {self.base_url} has no such thing")

    def on_line_reopen(self, name: str) -> None:
        """One of the robot's lines (connect(lines=)) opened again: told as a reconnect is, by that line - a GPU's allow
        list lets in the address that line goes out from."""
        if self._on_reconnect is not None:
            self._on_reconnect(_ByLine(name))

    def get(self, path: str, **_: Any) -> dict:
        """A ready poll (/v1/act/ready): the server's GET /ping - 200 ready, 503 while it warms up. Nothing listening
        there is not ready either: not yet (`unreached`), or no longer, where it has answered before (`stopped`) - a
        server restarting, or loading its model before it listens again - which wait_until_ready() waits out to its
        bound, and says once that bound has passed with the server still away. Its 401 or 403 is raised (AuthError,
        PermissionDenied): asking again changes nothing, and the token is the robot's to give.
        
"""
        if not path.startswith("/v1/act/ready"):
            raise NotFound(f"{path} is the platform's: a server of your own at {self.base_url} has no such thing")
        headers = {"Authorization": f"Bearer {self._token}"} if self._token else {}

        verify: Any = build_pinned_ssl_context(self._fingerprint) if self._fingerprint else True
        try:
            r = httpx.get(f"{self.base_url}/ping", headers=headers, timeout=self._timeout_s, verify=verify)
        except httpx.HTTPError as exc:



            stopped = self._heard and _refused(exc)
            return {"ready": False, "status": "stopped" if stopped else "unreached", "eta_s": None,
                    "address": self.base_url}
        self._heard = True
        self._take_play(r)
        serve_said = "x-seq-server" in r.headers
        if r.status_code == 200 and serve_said:
            return {"ready": True, "status": "ready", "eta_s": 0}
        if r.status_code in (401, 403):
            refused = AuthError if r.status_code == 401 else PermissionDenied
            raise refused(f"the server at {self.base_url} refused this robot's ping ({r.status_code})",
                          status=r.status_code, retryable=False,
                          hint=None if self._token else "it asks for its token: connect(url, token=...)")
        if "x-seq-teleop" in r.headers:

            raise InvalidRequest(f"the server at {self.base_url} is a teleop server (seq teleop serve), which had not "
                                 "answered when connect() asked what it serves: connect() to it again, now that it "
                                 "answers")
        if not serve_said:
            raise InvalidRequest(f"the server at {self.base_url} is not one serve() runs: its /ping answered "
                                 f"{r.status_code} without saying what it is (X-Seq-Server) - connect() takes the address "
                                 "of a server serve() or seq serve runs")
        if r.status_code >= 500 and r.status_code != 503:

            raise Unavailable(f"the server at {self.base_url} will not serve: {r.text.strip()[:500]}",
                              status=r.status_code, retryable=False, details={"reason": "worker_failed"})
        return {"ready": False, "status": "loading", "eta_s": None}

    def _take_play(self, r: Any) -> None:
        """What a 200 of the server's /ping says of how its robots play an answer, kept (_declared)."""
        if r.status_code != 200:
            return
        try:
            play = r.json().get("play")
        except (ValueError, AttributeError):
            play = None
        if isinstance(play, dict):
            self._plays = {k: play[k] for k in _DECLARED if play.get(k) is not None}

    def _declared(self) -> dict:
        """How the server's robots play an answer, as its GET /ping says it (serve(hz=, action_chunk_valid_len=,
        action_chunk_replan_at=, max_wait_for_batch=)), by the declarations' names the platform's connect answers with:
        each act then says what is left of the answer its robot plays (X-Seq-Chunk-Left-Ms), which that server holds
        and seats its robots by. Where no ready poll has read it, the first connect asks /ping; nothing where the server
        says none."""
        if not self._plays and not self._asked:
            self._asked = True
            headers = {"Authorization": f"Bearer {self._token}"} if self._token else {}
            verify: Any = build_pinned_ssl_context(self._fingerprint) if self._fingerprint else True
            try:
                self._take_play(httpx.get(f"{self.base_url}/ping", headers=headers, timeout=self._timeout_s,
                                          verify=verify))
            except httpx.HTTPError:
                pass
        return dict(self._plays)

    def close(self) -> None:
        """Nothing held: no gateway connection to close."""


def _refused(exc: BaseException) -> bool:
    """Whether a connection was refused: nothing listens at the address (ECONNREFUSED), anywhere in its causes."""
    seen = 0
    cause: Optional[BaseException] = exc
    while cause is not None and seen < 8:
        if isinstance(cause, ConnectionRefusedError):
            return True
        cause, seen = cause.__cause__ or cause.__context__, seen + 1
    return "connection refused" in str(exc).lower()

