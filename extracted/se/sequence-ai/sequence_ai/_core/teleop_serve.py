"""
seq teleop serve: a robot and the consoles that drive it finding each other through a server of your own - the pairing
GS's platform does for a robot connected by its key, with nothing of the platform's: no account, no key, nothing kept.

In one sentence: the robot connects to this server's address (sequence_ai.connect("http://ADDRESS:8200", token=...))
and long-polls it (POST /v1/robots/link) → a console - sequence_ai.teleop("http://ADDRESS:8200", token=...), or the page
this server serves at / - offers to connect (POST /v1/teleop/offer) → the robot's next round takes the offer, its answer
comes back (POST /v1/teleop/answer) and the console reads it (GET /v1/teleop/pairing/{id}) → from then on the two talk
to each other straight, past this server, as they do past the platform. Who drove the robot is said here (POST
/v1/robots/teleop-events) and logged.
WHY the platform's requests, word for word: the robot and the console each have one way of being paired, so the same
robot script runs against either server, its connect() the one line changed.

WHY a token by default: whoever reaches this server can offer to drive the robot. With none given one is made, and
printed once with the page's address; --token "" serves with none, warned of as seq serve warns of it.

WHY one robot a server: the platform names a robot by its key, and a server of your own has one token - its robot is
the one --robot names, on the machine it runs on or one it can reach.
WHY a relay only where it is named, and its credentials for one pairing: two sides behind NATs that give each peer a
port of its own meet through a TURN server (--turn) or not at all; each side is handed a username and password good
for --turn-ttl (coturn's use-auth-secret: the username "<expiry>:<who>", its password the base64 of its HMAC-SHA1 by
--turn-secret), so no long-lived password goes to a browser. Both sides still try every direct way first, and a
console that will not take a relay says so (teleop(direct_only=True)).


WHY a MoQ relay for the people watching: each console straight to the robot is one more upload from it, and many watching
one robot are many uploads; through a relay (--moq-port serves one in this process, --moq names one of your own) the
robot uploads once and the relay makes the copies (teleop_moq.py). Each round of the robot's link says where, and a
console asks (GET /v1/teleop/moq): teleop(url, token=..., via="moq") watches, and one person still drives over WebRTC.

"""
from __future__ import annotations

import base64
import collections
import hashlib
import hmac
import json
import logging
import pathlib
import re
import secrets
import socket
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Optional
from urllib.parse import parse_qs, urlsplit

NAME = "teleop"
PORT = 8200
TOKEN_ENV = "SEQ_TELEOP_TOKEN"
HEADER = "X-Seq-Teleop"

LINK_WAIT_MOST_S = 25.0
PAIRING_WAIT_MOST_S = 20.0

ONLINE_S = 35.0

OFFER_S = 60.0
EVENTS_KEPT = 1000
TURN_TTL_S = 12 * 3600
TURN_SECRET_ENV = "SEQ_TELEOP_TURN_SECRET"
BODY_MOST = 256 * 1024
SDP_MOST = 64 * 1024
_PAIRING = re.compile(r"^/v1/teleop/pairing/([0-9a-f-]{36})$")
_ASSET = re.compile(r"^(?:vendor/)?[a-z0-9-]+\.(js|css|html)$")
_TYPES = {".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
          ".html": "text/html; charset=utf-8"}
CONSOLE = pathlib.Path(__file__).with_name("teleop_console")


_CSP = ("default-src 'self'; img-src 'self' data: blob:; media-src 'self' blob:; style-src 'self' 'unsafe-inline'; "
        "frame-ancestors 'none'")
_PAGE_HEADERS = (("X-Content-Type-Options", "nosniff"), ("Referrer-Policy", "no-referrer"))
log = logging.getLogger("sequence_ai.teleop")


class Refused(Exception):
    """A refusal in the platform's shape (ErrorBody): what Transport and the page read, details.reason first."""

    def __init__(self, status: int, code: str, detail: str, reason: str, *, hint: Optional[str] = None) -> None:
        super().__init__(detail)
        self.status, self.code, self.detail, self.reason, self.hint = status, code, detail, reason, hint

    def body(self) -> dict:
        return {"code": self.code, "detail": self.detail, "details": {"reason": self.reason},
                **({"hint": self.hint} if self.hint else {})}


def _sdp(value: Any) -> str:
    """One side's SDP as it is handed on, or 400 direct_refused: text that starts with v=, at most 64 KB, naming a
    certificate fingerprint - what the platform's check takes."""
    if not isinstance(value, str) or not value.startswith("v=") or len(value) > SDP_MOST or "a=fingerprint:" not in value:
        raise Refused(400, "invalid_request", "this SDP cannot be used for a direct connection: it must start with v=, "
                      "be at most 64 KB and name a certificate fingerprint", "direct_refused")
    return value


def _fingerprint(sdp: str) -> Optional[str]:
    found = re.search(r"^a=fingerprint:(\S+ \S+)", sdp, re.MULTILINE)
    return found.group(1) if found else None


class Pairings:
    """One robot's pairings (module docstring), held in memory: who of it is heard, the offers no round has taken, and
    each offer's state until its console reads its outcome."""

    def __init__(self, robot: str, record: bool = False, clock: Any = time.monotonic) -> None:
        self.robot = robot
        self.record = record
        self._clock = clock
        self._lock = threading.Condition()
        self._heard: dict = {}
        self._waiting: list = []
        self._handed: dict = {}
        self._offers: dict = {}
        self._events: collections.deque = collections.deque(maxlen=EVENTS_KEPT)
        self._closed = False

    def link(self, session: str, direct: bool, wait_s: float) -> list:
        """A robot's round: it is heard, and handed the offers its session has not been handed yet, as they come within
        `wait_s`. An offer stays until it is answered or expires: a round whose robot went away as it waited - its
        answer written to no one - takes it from no later session, and the robot's own SDK answers each once, however
        many rounds bring it (teleop_link's _take).
"""
        end = self._clock() + wait_s
        with self._lock:
            self._heard[session] = (self._clock(), direct)
            handed = self._handed.setdefault(session, set())
            offers: list = []
            while not self._closed:
                offers = [o for o in self._waiting if o["pairing"] not in handed
                          and self._offers.get(o["pairing"], {}).get("state") == "offered"]
                left = end - self._clock()
                if offers or left <= 0:
                    break
                self._lock.wait(left)
            handed.update(o["pairing"] for o in offers)
            self._heard[session] = (self._clock(), direct)
            return offers

    def offer(self, sdp: Any, nat: Any, operator: Optional[str], ice_servers: Optional[list] = None) -> dict:
        """A console's offer, placed for the robot's next round with the relays the robot may use (`ice_servers`): 409
        while no robot is connected, or none that takes a direct connection."""
        side = _sdp(sdp)
        with self._lock:
            now = self._clock()
            self._expire(now)
            direct = [takes for at, takes in self._heard.values() if now - at < ONLINE_S]
            if not direct:
                raise Refused(409, "conflict", f"robot '{self.robot}' is not connected: a console reaches a robot once "
                              "it is connected", "robot_not_connected",
                              hint=f'start the robot\'s own loop (sequence_ai.connect("http://<this server>:{PORT}", '
                                   'token=...)) and ask again')
            if not any(direct):
                raise Refused(409, "conflict", f"robot '{self.robot}' cannot take a direct connection",
                              "robot_not_direct", hint="install sequence-ai[teleop] on the robot and connect it again")
            pairing = str(uuid.uuid4())
            self._offers[pairing] = {"state": "offered", "made": now, "answer": None}
            self._waiting.append({"pairing": pairing, "sdp": side, "nat": nat if isinstance(nat, dict) else None,
                                  "operator": operator, **({"ice_servers": ice_servers} if ice_servers else {})})
            self._lock.notify_all()
        log.info("%s: an offer to drive it%s", self.robot, f" from {operator}" if operator else "")
        return {"pairing": pairing, "robot": self.robot, "lost_s_hint": None}

    def answer(self, pairing: str, sdp: Any, nat: Any, error: Any) -> None:
        """The robot's answer to an offer, or why it has none: 404 for one unknown, gone, or answered already."""
        side = {"error": str(error)[:500]} if error is not None else {"sdp": _sdp(sdp),
                                                                     "nat": nat if isinstance(nat, dict) else None}
        with self._lock:
            self._expire(self._clock())
            row = self._offers.get(pairing)
            if row is None or row["state"] != "offered":
                raise Refused(404, "not_found", "no such pairing", "no_pairing")
            row["state"], row["answer"] = ("failed" if error is not None else "answered"), side
            self._lock.notify_all()

    def outcome(self, pairing: str, wait_s: float) -> dict:
        """What the console reads of its offer within `wait_s`: {"state": "offered"} to ask again, or its outcome -
        read once, then gone with both addresses in it."""
        end = self._clock() + wait_s
        with self._lock:
            while True:
                self._expire(self._clock())
                row = self._offers.get(pairing)
                if row is None:
                    raise Refused(404, "not_found", "no such pairing", "no_pairing")
                left = end - self._clock()
                if row["state"] != "offered" or left <= 0 or self._closed:
                    break
                self._lock.wait(min(left, 1.0))
            if row["state"] == "offered":
                return {"state": "offered"}
            del self._offers[pairing]
        answer = row["answer"] or {}
        if row["state"] == "answered":
            return {"state": "answered", "sdp": answer["sdp"], "nat": answer.get("nat"),
                    "fingerprint": _fingerprint(answer["sdp"])}
        return {"state": "failed", "why": answer.get("error") or "the robot did not answer"}

    def _expire(self, now: float) -> None:
        """An offer older than OFFER_S with no answer fails; a robot unheard past ONLINE_S is forgotten."""
        for row in self._offers.values():
            if row["state"] == "offered" and now - row["made"] > OFFER_S:
                row["state"], row["answer"] = "failed", {"error": "the robot did not answer in time"}
        self._waiting = [o for o in self._waiting if self._offers.get(o["pairing"], {}).get("state") == "offered"]
        for session in [s for s, (at, _) in self._heard.items() if now - at > ONLINE_S]:
            del self._heard[session]
            self._handed.pop(session, None)
        waiting = {o["pairing"] for o in self._waiting}
        for handed in self._handed.values():
            handed &= waiting
        if len(self._offers) > 1000:
            for pairing in sorted(self._offers, key=lambda p: self._offers[p]["made"])[:len(self._offers) - 1000]:
                del self._offers[pairing]

    def note(self, events: Any) -> None:
        """Who the robot says drove it - take, release, stop, timeout - kept (events()) and logged."""
        for event in events if isinstance(events, list) else ():
            if not isinstance(event, dict) or event.get("event") not in ("take", "release", "stop", "timeout"):
                continue
            kept = {k: event.get(k) for k in ("event", "operator", "at", "session") if event.get(k) is not None}
            self._events.append(kept)
            by = f" by {kept['operator']}" if kept.get("operator") else ""
            log.info("%s: %s%s", self.robot, kept["event"], by)

    def events(self) -> list:
        return list(self._events)

    def connected(self) -> bool:
        now = self._clock()
        with self._lock:
            return any(now - at < ONLINE_S for at, _ in self._heard.values())

    def close(self) -> None:
        with self._lock:
            self._closed = True
            self._lock.notify_all()


class _Handler(BaseHTTPRequestHandler):
    """One request of the server's (TeleopServer.app the pairings and token)."""

    protocol_version = "HTTP/1.1"
    server_version = "seq-teleop"
    app: "TeleopServer"

    def log_message(self, format: str, *args: Any) -> None:
        log.debug("%s %s", self.address_string(), format % args)

    def do_GET(self) -> None:
        self._serve("GET")

    def do_POST(self) -> None:
        self._serve("POST")

    def _serve(self, method: str) -> None:
        parts = urlsplit(self.path)
        try:


            self._raw = self._read()
            if method == "GET" and parts.path in ("/v1/health", "/ping"):
                self._json(200, {"status": "ok", "serves": NAME, "robot": self.app.pairings.robot})
            elif method == "GET" and (parts.path in ("/", "/index.html") or parts.path.startswith("/assets/")):
                self._file("index.html" if not parts.path.startswith("/assets/") else parts.path[len("/assets/"):])
            elif parts.path.startswith("/v1/"):
                self._authorized()
                self._json(200, self._call(method, parts.path, parse_qs(parts.query)))
            else:
                raise Refused(404, "not_found", f"{parts.path} is no part of a teleop server", "no_route")
        except Refused as refused:
            self._json(refused.status, refused.body())

    def _authorized(self) -> None:
        token = self.app.token
        if not token:
            return
        said = self.headers.get("Authorization") or ""
        given = said[len("Bearer "):] if said.startswith("Bearer ") else ""
        if not hmac.compare_digest(given.encode(), token.encode()):
            raise Refused(401, "unauthenticated", "this teleop server asks for its token" if not given else
                          "this teleop server's token is not the one given", "token",
                          hint='connect("http://<this server>", token=...) or teleop("http://<this server>", token=...)')

    def _read(self) -> bytes:
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = -1
        if length < 0 or length > BODY_MOST:
            self.close_connection = True
            raise Refused(413, "payload_too_large", f"a request's body is {BODY_MOST} bytes at most", "body")
        return self.rfile.read(length) if length else b""

    def _body(self) -> dict:
        try:
            body = json.loads(self._raw or b"{}")
        except ValueError:
            raise Refused(400, "invalid_request", "the body does not read as JSON", "body") from None
        if not isinstance(body, dict):
            raise Refused(400, "invalid_request", "the body is a JSON object", "body")
        return body

    def _call(self, method: str, path: str, query: dict) -> dict:
        pairings = self.app.pairings
        found = _PAIRING.match(path)
        if method == "GET" and path == "/v1/teleop/ice":

            return {"ice_servers": self.app.ice_servers("console")}
        if method == "GET" and path == "/v1/teleop/moq":

            where = self.app.moq_where(self._host())
            if where is None:
                raise Refused(409, "conflict", "this teleop server names no MoQ relay", "moq_not_served",
                              hint="seq teleop serve --moq-port 4443 serves one, or --moq URL names yours")
            return {**where, "robot": pairings.robot}
        if method == "GET" and found:
            try:
                wait_s = float((query.get("wait_s") or ["20"])[0])
            except ValueError:
                wait_s = PAIRING_WAIT_MOST_S
            return pairings.outcome(found.group(1), max(0.0, min(wait_s, PAIRING_WAIT_MOST_S)))
        if method != "POST":
            raise Refused(404, "not_found", f"{path} is no part of a teleop server", "no_route")
        body = self._body()
        if path == "/v1/act/connect":
            if body.get("model") != NAME:
                raise Refused(400, "invalid_request", f"this server pairs robots and consoles for teleop: "
                              f"connect to {body.get('model')!r} is a policy server's", "not_teleop",
                              hint="a policy is served by seq serve, at its own address")
            return {"teleop": {"link_url": self._own_url()}}
        if path == "/v1/robots/link":
            session = body.get("session")
            if not isinstance(session, str) or not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", session):
                raise Refused(400, "invalid_request", "a round names its session", "session")
            try:
                wait_s = max(0.0, min(float(body.get("wait_s") or 0.0), LINK_WAIT_MOST_S))
            except (TypeError, ValueError):
                wait_s = 0.0
            offers = pairings.link(session, body.get("direct") is not False, wait_s)
            where = self.app.moq_where(self._host())
            return {"offers": offers, "settings": {"teleop": True, "record": pairings.record, "robot": pairings.robot,
                                                   **({"moq": where} if where is not None else {})}}
        if path == "/v1/teleop/offer":
            operator = body.get("operator")
            operator = operator[:80] if isinstance(operator, str) and operator else None
            robot = body.get("robot")
            if isinstance(robot, str) and robot and robot != pairings.robot:
                raise Refused(404, "not_found", f"no robot '{robot}': this server's is '{pairings.robot}'", "no_robot")

            relays = [] if body.get("direct_only") is True else self.app.ice_servers("robot")
            return pairings.offer(body.get("sdp"), body.get("nat"), operator, relays)
        if path == "/v1/teleop/answer":
            pairing = body.get("pairing")
            if not isinstance(pairing, str):
                raise Refused(404, "not_found", "no such pairing", "no_pairing")
            pairings.answer(pairing, body.get("sdp"), body.get("nat"), body.get("error"))
            return {}
        if path == "/v1/robots/teleop-events":
            pairings.note(body.get("events"))
            return {}
        raise Refused(404, "not_found", f"{path} is no part of a teleop server", "no_route")

    def _csp(self) -> str:
        """The page's: this server alone, and its MoQ relay where it names one - its address over https (WebTransport)
        and over http (its certificate's fingerprint, read as MoQ's browser library reads it)."""
        where = self.app.moq_where(self._host())
        if where is None:
            return _CSP
        relay = urlsplit(str(where["url"])).netloc
        return f"{_CSP}; connect-src 'self' https://{relay} http://{relay}"

    def _host(self) -> str:
        """The host this server was reached at: its request's Host without the port, an IPv6 address in brackets."""
        host = self.headers.get("Host") or ""
        if host.startswith("["):
            return host[:host.index("]") + 1] if "]" in host else host
        if host and host.count(":") <= 1:
            return host.split(":")[0]
        bound = self.server.server_address[0]
        return "127.0.0.1" if bound in ("0.0.0.0", "") else (f"[{bound}]" if ":" in bound else bound)

    def _own_url(self) -> str:
        """This server as the robot reached it: where its link goes - the same server."""
        scheme = "https" if (self.headers.get("X-Forwarded-Proto") or "").lower() == "https" else "http"
        host = self.headers.get("Host") or f"{self.server.server_address[0]}:{self.server.server_address[1]}"
        return f"{scheme}://{host}"

    def _json(self, status: int, body: dict) -> None:
        try:
            self._write_json(status, body)
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True
            log.debug("%s went before its answer", self.address_string())

    def _write_json(self, status: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header(HEADER, "1")
        self.end_headers()
        self.wfile.write(data)

    def _file(self, name: str) -> None:
        path = CONSOLE / name
        if not _ASSET.match(name) or not path.is_file():
            raise Refused(404, "not_found", f"no such file: {name}", "no_file")
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", _TYPES[path.suffix])
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header(HEADER, "1")
        self.send_header("Content-Security-Policy", self._csp())
        for header, value in _PAGE_HEADERS:
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(data)


class _Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class TeleopServer:
    """The server (module docstring): serve_forever() it, or start() it on a thread of its own; close() ends it.
    `token` None or "": none asked for. `robot` the name its robot goes by (this machine's, unnamed); `record` whether
    the robot keeps its steps in a file of its own (its Record, as the platform's robot settings say it). `turn` the
    TURN servers both sides may relay through ("turn:host:3478", "turns:host:5349?transport=tcp"), their credentials
    made by `turn_secret` (coturn's static-auth-secret), good for `turn_ttl_s`. `moq_port` a MoQ relay served here, on
    that UDP port (0: any free one), for the people watching the robot; `moq` instead a relay of your own, its address
    (teleop_moq.external)."""

    def __init__(self, host: str = "0.0.0.0", port: int = PORT, *, token: Optional[str] = None,
                 robot: Optional[str] = None, record: bool = False, turn: Any = (), turn_secret: Optional[str] = None,
                 turn_ttl_s: float = TURN_TTL_S, moq: Optional[str] = None, moq_port: Optional[int] = None) -> None:
        self.token = token or None
        self.turn = tuple(turn or ())
        if self.turn and not turn_secret:
            raise ValueError(f"a TURN server's credentials are made with its secret: --turn-secret, or ${TURN_SECRET_ENV}")
        if moq and moq_port is not None:
            raise ValueError("--moq names a MoQ relay of your own and --moq-port serves one here: one of the two")
        self._turn_secret, self.turn_ttl_s = turn_secret, turn_ttl_s
        self.pairings = Pairings(robot or _this_machine(), record)

        self.broadcast = f"{self.pairings.robot}-{secrets.token_hex(4)}"
        self._moq_given: Optional[dict] = None
        self.relay: Any = None
        if moq:
            from sequence_ai._core import teleop_moq

            self._moq_given = teleop_moq.external(moq)
        self._http = _Server((host, port), type("Handler", (_Handler,), {"app": self}))
        if moq_port is not None:
            from sequence_ai._core import teleop_moq

            try:
                self.relay = teleop_moq.Relay(host, moq_port).start()
            except BaseException:
                self._http.server_close()
                raise
        self._thread: Optional[threading.Thread] = None

    def moq_where(self, host: str) -> Optional[dict]:
        """Where the robot's steps go for the people watching, as a client that reached this server at `host` (its
        Host, no port) reaches the relay: {"url", "broadcast", "fingerprints"} - None with no relay."""
        if self.relay is not None:
            where = self.relay.where(host)
        elif self._moq_given is not None:
            where = dict(self._moq_given)
        else:
            return None
        return {**where, "broadcast": self.broadcast}

    def ice_servers(self, who: str, now: Optional[float] = None) -> list:
        """The relays a pairing's side may use, as an RTCIceServer each: every TURN server given, with a username
        "<expiry>:<who>" and its password, the base64 of the username's HMAC-SHA1 by the secret - what coturn's
        use-auth-secret checks, and refuses past the expiry. None without --turn."""
        if not self.turn:
            return []
        username = f"{int((time.time() if now is None else now) + self.turn_ttl_s)}:{who}"
        digest = hmac.new(str(self._turn_secret).encode(), username.encode(), hashlib.sha1).digest()
        return [{"urls": list(self.turn), "username": username, "credential": base64.b64encode(digest).decode()}]

    @property
    def port(self) -> int:
        return self._http.server_address[1]

    @property
    def url(self) -> str:
        host = self._http.server_address[0]
        return f"http://{'127.0.0.1' if host in ('0.0.0.0', '::') else host}:{self.port}"

    def serve_forever(self) -> None:
        self._http.serve_forever(poll_interval=0.2)

    def start(self) -> "TeleopServer":
        self._thread = threading.Thread(target=self.serve_forever, daemon=True, name="seq-teleop-serve")
        self._thread.start()
        return self

    def close(self) -> None:
        self.pairings.close()
        if self._thread is not None:
            self._http.shutdown()
        self._http.server_close()
        if self.relay is not None:
            self.relay.close()

    def __enter__(self) -> "TeleopServer":
        return self.start()

    def __exit__(self, *exc: Any) -> None:
        self.close()


def _this_machine() -> str:
    """This machine's name, as a robot's name is written: letters, digits, '-' and '_'."""
    name = re.sub(r"[^A-Za-z0-9_-]+", "-", socket.gethostname().split(".")[0]).strip("-")
    return name[:64] or "robot"


def new_token() -> str:
    return secrets.token_urlsafe(24)


def _loopback(host: str) -> bool:
    return host in ("127.0.0.1", "::1", "localhost")


def serve(host: Optional[str] = None, port: int = PORT, *, token: Optional[str] = None, robot: Optional[str] = None,
          record: bool = False, turn: Any = (), turn_secret: Optional[str] = None, turn_ttl_s: float = TURN_TTL_S,
          moq: Optional[str] = None, moq_port: Optional[int] = None, echo: Any = None) -> int:
    """`seq teleop serve`: this server until Ctrl-C. `token` None: one made, and said once; "": none, warned of
    where an address other than this machine's own can reach it."""
    echo = echo or print
    if not log.handlers and not logging.getLogger().handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S"))
        log.addHandler(handler)
        log.setLevel(logging.INFO)
        log.propagate = False
    made = token is None
    if made:
        token = new_token()
    server = TeleopServer(host or "0.0.0.0", port, token=token, robot=robot, record=record, turn=turn,
                          turn_secret=turn_secret, turn_ttl_s=turn_ttl_s, moq=moq, moq_port=moq_port)
    shown = f"http://{_address_of(host)}:{server.port}"
    echo(f"teleop for robot '{server.pairings.robot}' at {shown}")
    echo(f'  the robot:    sequence_ai.connect("{shown}"' + (', token=TOKEN)' if token else ")"))
    echo(f'  a console:    sequence_ai.teleop("{shown}"' + (', token=TOKEN)' if token else ")")
         + f", or the page at {shown}/")
    if record:
        echo("  its Record is on: the robot writes its steps to a file on its own machine "
             "($SEQUENCES_RECORD_DIR, else the folder it runs in)")
    if server.turn:
        ttl = server.turn_ttl_s
        echo(f"  a relay where the two cannot meet directly: {', '.join(server.turn)}, each side's credentials good "
             f"for {f'{ttl / 3600:g} h' if ttl >= 3600 else f'{ttl:g} s'}")
    if server.relay is not None or moq:
        from sequence_ai._core.teleop_moq import shown as _shown

        at = f"UDP port {server.relay.port}" if server.relay is not None else _shown(moq)
        echo(f"  many watching through a MoQ relay ({at}): sequence_ai.teleop(\"{shown}\"" +
             (', token=TOKEN' if token else '') + ', via="moq"), the robot uploading once')
    if token and made:
        echo(f"  TOKEN, made for this run (--token or ${TOKEN_ENV} keeps one): {token}")
        echo(f"  the page with it: {shown}/#token={token}")
    elif not token and not _loopback(host or "0.0.0.0"):
        log.warning("no token: anyone who can reach port %d can drive the robot (seq teleop serve --token TOKEN or $%s "
                    "asks for one)", server.port, TOKEN_ENV)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
    return 0


def _address_of(host: Optional[str]) -> str:
    """The address a robot or console on another machine reaches this one at, for the lines printed: the host given,
    else this machine's address on its default route, else its name."""
    if host and host not in ("0.0.0.0", "::"):
        return host
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("192.0.2.1", 9))
            return s.getsockname()[0]
    except OSError:
        return socket.gethostname()
