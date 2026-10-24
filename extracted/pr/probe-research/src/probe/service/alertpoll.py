"""Run alerts for every daemon session on the machine, asked for here once (plan Q2).

Each daemon worker used to ask the server for its own session's run alerts
every 30 s (`probe.daemon.run_alerts`), each time on a new HTTPS client. Now
the service asks for all of them, on one kept connection per endpoint, and
leaves each answer where that session's worker reads it:

    every POLL_S, while a live daemon-mode session is registered:
        each such session (registered from outside any sandbox: the state
        folder it names is where the answers go) whose worker asked for it:
        its `.worker.json` marker (`probe.daemon.mailbox.offer_run_alerts`)
        says `run_alerts`, names a process that runs outside any sandbox, and
        names the CLI config that worker reads
        -> GET /v1/sessions/{sid}/run-alerts with that config's daemon key
           and endpoint (`probe.daemon.model.endpoint`, minus the environment:
           a worker whose key or endpoint comes from its environment never
           asks), one session after another
        -> the answer as the server gave it, in `<state>/reads/alerts/<sid>.json`:
           {sid, polled_at, alerts (a listing, or null: no answer),
            refused_until (null, or when the paused key is asked again),
            every (POLL_S: when the next hand-off is due), pid}
    the worker reads that file instead of asking, and does with the listing
    what it always did: dedupe by id, publish ONE message, record it
    (`RunAlertLane.hand_over`). With no fresh hand-off (no service, an older
    one, a stalled one) the worker asks the server itself, as before: a crash
    here loses nothing (the server keeps two hours of alerts).

BACKOFF. A refused key (a 401, or a 403 that names the credential:
`probe.sdk.key_refusal`) pauses that key REFUSED_WAIT_S, as the worker did; a
429 pauses it for its Retry-After, within [POLL_S, REFUSED_WAIT_S]. While a key
is paused its sessions' hand-offs still go out (saying until when), so no
worker takes over a poll the service holds back. An endpoint that does not
answer at all (a timeout, no network) ends its round and is asked again after
a pause that doubles from POLL_S up to REFUSED_WAIT_S, and one that answered
anything but a listing NONE_LIMIT rounds in a row is treated the same: no
hand-off goes out for either, and each worker asks itself again. This
service starts with a clean environment and may lack the proxy or the CA
bundle the worker's names, or meet a gateway the worker's proxy would not.

On its own daemon thread, never the event loop, and never a thread the
process's exit waits for (a request stuck past its deadline). One request has
REQUEST_DEADLINE_S, a round ROUND_BUDGET_S; one session's failure costs only
its own answer; a round still running when the next is due delays that one,
and a round cut short starts the next where it stopped.

Stdlib only; the TLS trust and the client headers come from `probe` modules
loaded on the thread, off the start path.
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import json
import os
import secrets
import socket
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urlsplit

from . import caller
from .mailwatch import DaemonLane, read_json, safe

#: The server is asked this often (`probe.daemon.run_alerts.RUN_ALERT_POLL_S`).
POLL_S = 30.0
#: After Probe refused the key (`run_alerts.RUN_ALERT_REFUSED_WAIT_S`).
REFUSED_WAIT_S = 5 * 60.0
#: One socket operation, at most (`probe_api.RUN_ALERTS_TIMEOUT_S`)...
TIMEOUT_S = 10.0
#: ...and one request, start to finish (a server that drips its answer).
REQUEST_DEADLINE_S = 15.0
#: An endpoint that answered anything but a listing this many rounds in a row
#: is left to the workers, as one that does not answer is.
NONE_LIMIT = 3
#: One round, at most: the sessions it did not reach go first in the next.
ROUND_BUDGET_S = 20.0
#: A listing larger than this is no answer (the server sends at most 200 short rows).
MAX_BODY_BYTES = 1024 * 1024
#: The worker's marker larger than this is not read.
MAX_MARKER_BYTES = 64 * 1024
#: What the hand-off files are called, under `<state>/reads/`.
HANDOFF_DIR = "alerts"
#: Test-only: a shorter POLL_S (nothing in production sets it).
POLL_ENV = "PROBE_SERVICE_ALERT_POLL_S"


def poll_interval() -> float:
    try:
        value = float(os.environ.get(POLL_ENV) or POLL_S)
    except ValueError:
        return POLL_S
    return value if value > 0 else POLL_S


def handoff_path(state: str, sid: str) -> Path:
    """`probe.daemon.mailbox.alerts_handoff_path` for a session under `state`."""
    return Path(state) / "reads" / HANDOFF_DIR / f"{safe(sid)}.json"


def marker_path(state: str, sid: str) -> Path:
    """`probe.daemon.mailbox.worker_marker_path` for a session under `state`."""
    return Path(state) / "reads" / "requests" / safe(sid) / ".worker.json"


def _pid_runs(pid: object) -> bool:
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 1:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def wanted(state: str, sid: str) -> str | None:
    """The CLI config the session's worker reads, when that worker asked the
    service to poll for it, still runs and is no more confined than this
    service (`caller.sandboxed`); else None."""
    data = read_json(str(marker_path(state, sid)), MAX_MARKER_BYTES)
    if not isinstance(data, dict) or data.get("run_alerts") != 1 or not _pid_runs(data.get("pid")):
        return None
    config = data.get("config")
    if not isinstance(config, str) or not config.startswith("/") or "\0" in config:
        return None
    return None if caller.sandboxed(data["pid"]) else config


@dataclass(frozen=True)
class Endpoint:
    base_url: str
    key: str


def endpoint(config: str, keys: tuple[str, ...] = ("companion_token",)) -> Endpoint | None:
    """`probe.daemon.model.endpoint()` without the environment: the daemon key
    and API of `config`'s current context (a v1 flat file is its one context).
    `keys`: the context's credentials to use, the first one present wins (the
    hint lane reads with the read-only key first, `hints.KEYS`)."""
    try:
        data = json.loads(caller._read_config(Path(config)))
    except (OSError, ValueError, RecursionError):
        return None
    if not isinstance(data, dict):
        return None
    contexts = data.get("contexts")
    row = contexts.get(data.get("current_context") or "default") if isinstance(contexts, dict) else data
    if not isinstance(row, dict):
        return None
    key = next((row.get(name) for name in keys if isinstance(row.get(name), str) and row.get(name)), None)
    base = row.get("base_url") or caller.DEFAULT_BASE_URL
    if not isinstance(key, str) or not key or not key.isascii() or not key.isprintable() or " " in key:
        return None
    if not isinstance(base, str) or not base.startswith(("https://", "http://")) or any(ch.isspace() for ch in base):
        return None
    try:
        url = urlsplit(base)
        url.port  # noqa: B018 -- raises ValueError for a port that is not one
    except ValueError:
        return None
    if not url.hostname:
        return None
    return Endpoint(base_url=base.rstrip("/"), key=key)


class Answer:
    """What one request came back with."""

    LISTING = "listing"
    REFUSED = "refused"  # the key itself
    LIMITED = "limited"  # 429
    NONE = "none"  # any other answer: ask again next round
    UNREACHED = "unreached"  # no answer at all: this endpoint's round ends


def _retry_after(value: str | None) -> float:
    try:
        seconds = float(value) if value else POLL_S
    except ValueError:
        seconds = POLL_S
    return min(max(seconds, POLL_S), REFUSED_WAIT_S)


class Fetcher:
    """GET one session's run alerts over a kept connection per endpoint."""

    #: One socket operation, at most (a subclass with another route sets its own).
    timeout = TIMEOUT_S

    def __init__(self, version: str) -> None:
        self.version = version
        self._conns: dict = {}
        self._context = None
        self._headers: dict | None = None

    def _client_headers(self) -> dict:
        if self._headers is None:
            try:
                from probe.client_headers import client_version_headers

                self._headers = dict(client_version_headers("cli", self.version))
            except Exception:  # noqa: BLE001 -- the poll goes out without them
                self._headers = {}
        return self._headers

    def _ssl(self):
        if self._context is None:
            try:
                from probe.sdk.tls import ssl_context

                self._context = ssl_context()
            except Exception:  # noqa: BLE001 -- the OS store still verifies
                import ssl

                self._context = ssl.create_default_context()
        return self._context

    def _connection(self, base: str):
        conn = self._conns.get(base)
        if conn is None:
            import http.client

            url = urlsplit(base)
            if url.scheme == "https":
                conn = http.client.HTTPSConnection(url.hostname, url.port, timeout=self.timeout, context=self._ssl())
            else:
                conn = http.client.HTTPConnection(url.hostname, url.port, timeout=self.timeout)
            self._conns[base] = conn
        return conn

    def drop(self, base: str) -> None:
        conn = self._conns.pop(base, None)
        if conn is not None:
            with contextlib.suppress(Exception):
                conn.close()

    def close(self) -> None:
        for base in list(self._conns):
            self.drop(base)

    def abort(self, base: str | None = None) -> None:
        """From another thread: end a request in flight now (a socket shut
        down wakes the thread blocked on it; closing it would not). Every
        endpoint's, or `base`'s."""
        conns = list(self._conns.values()) if base is None else [self._conns.get(base)]
        for conn in conns:
            sock = getattr(conn, "sock", None)
            if sock is not None:
                with contextlib.suppress(OSError):
                    sock.shutdown(socket.SHUT_RDWR)

    @staticmethod
    def _read(resp, deadline: float) -> bytes | None:
        """The body, at most MAX_BODY_BYTES + 1, by `deadline` (else None)."""
        chunks: list = []
        size = 0
        while size <= MAX_BODY_BYTES:
            if time.monotonic() > deadline:
                return None
            chunk = resp.read1(65536) if hasattr(resp, "read1") else resp.read(65536)
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
        return b"".join(chunks)

    def __call__(self, ep: Endpoint, sid: str) -> tuple[str, object]:
        """`(Answer.*, the listing | the pause in seconds | None)`."""
        prefix = urlsplit(ep.base_url).path.rstrip("/")
        path = f"{prefix}/v1/sessions/{quote(sid, safe='')}/run-alerts"
        headers = {
            "Authorization": f"Bearer {ep.key}",
            "Accept": "application/json",
            "User-Agent": f"probe-service/{self.version}",
            **self._client_headers(),
        }
        deadline = time.monotonic() + REQUEST_DEADLINE_S
        # The whole request, connect and headers included: a server that drips
        # them a byte at a time would hold every session's poll otherwise.
        cutoff = threading.Timer(REQUEST_DEADLINE_S, self.abort, args=(ep.base_url,))
        cutoff.daemon = True
        cutoff.start()
        try:
            return self._get(ep, path, headers, deadline)
        finally:
            cutoff.cancel()

    def _get(self, ep: Endpoint, path: str, headers: dict, deadline: float) -> tuple[str, object]:
        import http.client

        for attempt in (1, 2):
            try:
                conn = self._connection(ep.base_url)
                conn.request("GET", path, headers=headers)
                resp = conn.getresponse()
                body = self._read(resp, deadline)
                status, retry = resp.status, resp.getheader("Retry-After")
                if body is None or len(body) > MAX_BODY_BYTES or not resp.isclosed():
                    self.drop(ep.base_url)  # cut short, or unread bytes left on it
                elif resp.getheader("Connection", "").lower() == "close" or resp.will_close:
                    self.drop(ep.base_url)
                if body is None:
                    return Answer.UNREACHED, None
                break
            except (http.client.RemoteDisconnected, BrokenPipeError, ConnectionResetError):
                # A kept connection the server closed meanwhile: once more, fresh.
                self.drop(ep.base_url)
                if attempt == 2:
                    return Answer.UNREACHED, None
            except (OSError, ValueError, http.client.HTTPException):
                self.drop(ep.base_url)
                return Answer.UNREACHED, None
        try:
            data = json.loads(body.decode("utf-8")) if len(body) <= MAX_BODY_BYTES else None
        except (UnicodeDecodeError, ValueError, RecursionError):
            data = None
        if status in (401, 403):
            from probe.sdk.key_refusal import credential_refused

            detail = data.get("detail") if isinstance(data, dict) else None
            message = detail.get("message") if isinstance(detail, dict) else detail
            text = message if isinstance(message, str) else body[:2000].decode("utf-8", "replace")
            if credential_refused(status, text):
                return Answer.REFUSED, REFUSED_WAIT_S
            return Answer.NONE, None
        if status == 429:
            return Answer.LIMITED, _retry_after(retry)
        if status != 200 or not isinstance(data, dict) or not isinstance(data.get("alerts"), list):
            return Answer.NONE, None
        return Answer.LISTING, [a for a in data["alerts"] if isinstance(a, dict)]


def write_handoff(state: str, sid: str, alerts: list | None, refused_until: float | None,
                  every: float = POLL_S) -> None:
    """The answer for the worker, whole: a temp file, then `os.replace`. Only
    for a session whose worker's marker asked for it (`wanted`). `every`: how
    often the service asks, so the worker knows when to look for the next."""
    path = handoff_path(state, sid)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "sid": sid,
        "polled_at": time.time(),
        "alerts": alerts,
        "refused_until": refused_until,
        "every": every,
        "pid": os.getpid(),
    }
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{secrets.token_hex(3)}.tmp")
    try:
        tmp.write_text(json.dumps(body, sort_keys=True), encoding="utf-8")
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(OSError):
            tmp.unlink()


class AlertPoller:
    """The service's one run-alert poller (see the module docstring).

    `sessions()` is the live daemon-mode sessions as `(sid, state)`, asked on
    the loop; `fetch(endpoint, sid)` is a Fetcher (swapped in tests)."""

    def __init__(
        self,
        *,
        loop_getter: Callable[[], asyncio.AbstractEventLoop | None],
        sessions: Callable[[], list],
        log: Callable[[str], None],
        version: str = "0.0.0",
        fetch: Callable | None = None,
        poll_s: float | None = None,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._loop_getter = loop_getter
        self._sessions = sessions
        self._log = log
        self.fetch = fetch if fetch is not None else Fetcher(version)
        self.poll_s = poll_interval() if poll_s is None else poll_s
        self.clock = clock
        #: (base URL, key digest) or base URL -> (when it may be asked again
        #: (`clock`), why: an Answer). A refused or limited KEY is paused (another
        #: config's key at the same address is not); an unanswering ADDRESS is.
        self.paused: dict = {}
        #: base URL -> how many rounds in a row it did not answer at all
        self.unreached: dict = {}
        #: base URL -> how many rounds in a row it answered but sent no listing
        self.nones: dict = {}
        #: The last round's `(sid, state)` it did not reach: first next time.
        self._behind: list = []
        self._lane = DaemonLane("alertpoll")
        self._handle: asyncio.TimerHandle | None = None
        self._running = False
        self._closed = False
        #: What the last round did, for tests and the log.
        self.last_round: dict = {}

    # -- the thread ------------------------------------------------------------

    def poll_round(self, targets: list) -> dict:
        """Ask for every session that wants it; write each hand-off. Runs on the thread."""
        start = time.monotonic()
        order = [t for t in self._behind if t in targets] + [t for t in targets if t not in self._behind]
        self._behind = []
        done = {"asked": 0, "handed": 0, "skipped": 0}
        asked: set = set()  # the endpoints asked this round
        for index, (sid, state) in enumerate(order):
            if time.monotonic() - start > ROUND_BUDGET_S:
                self._behind = order[index:]
                break
            try:
                self._poll_one(sid, state, done, asked)
            except Exception as exc:  # noqa: BLE001 -- the other sessions are still asked for
                self._log(f"run alerts: session {sid} failed: {exc!r}")
        self.last_round = done
        return done

    def _poll_one(self, sid: str, state: str, done: dict, asked: set) -> None:
        config = wanted(state, sid)
        ep = endpoint(config) if config is not None else None
        if ep is None:
            done["skipped"] += 1
            return
        key = (ep.base_url, hashlib.sha256(ep.key.encode("utf-8")).hexdigest()[:16])
        alerts: list | None = None
        until: float | None = None
        holds = [h for h in (self.paused.get(ep.base_url), self.paused.get(key)) if h and self.clock() < h[0]]
        if holds:
            until, kind = holds[0]
        else:
            kind, value = self.fetch(ep, sid)
            done["asked"] += 1
            if kind != Answer.UNREACHED:
                self.unreached.pop(ep.base_url, None)
                self.paused.pop(ep.base_url, None)
            if kind == Answer.LISTING:
                alerts = value
                self.paused.pop(key, None)
                self.nones.pop(ep.base_url, None)
            elif kind in (Answer.REFUSED, Answer.LIMITED):
                until = self.clock() + float(value)
                self.paused[key] = (until, kind)
                self._log(f"run alerts: {ep.base_url} answered {kind}; asking with that key again in "
                          f"{float(value):.0f} s")
            elif kind == Answer.UNREACHED:
                streak = self.unreached.get(ep.base_url, 0) + 1
                self.unreached[ep.base_url] = streak
                self.paused[ep.base_url] = (self._backoff(streak), kind)
            else:
                self.paused.pop(key, None)
                if ep.base_url not in asked:  # counted once a round
                    self.nones[ep.base_url] = self.nones.get(ep.base_url, 0) + 1
                over = self.nones.get(ep.base_url, 0) - NONE_LIMIT + 1
                if over > 0:
                    # Answers, but never a listing (a gateway this service meets
                    # and the worker's proxy would not): the workers ask again.
                    if over == 1 and ep.base_url not in asked:
                        self._log(f"run alerts: {ep.base_url} sent no listing {NONE_LIMIT} rounds running; "
                                  "leaving the poll to the workers until it does")
                    self.paused[ep.base_url] = (self._backoff(over), Answer.UNREACHED)
                    kind = Answer.UNREACHED
            asked.add(ep.base_url)
        if kind == Answer.UNREACHED:
            # No answer from here worth handing over: no hand-off, so the
            # worker's own poll takes over once the last one is stale.
            return
        try:
            write_handoff(state, sid, alerts, self._wall(until), self.poll_s)
            done["handed"] += 1
        except OSError as exc:
            self._log(f"run alerts: could not hand session {sid}'s answer over: {exc}")

    def _backoff(self, streak: int) -> float:
        """When an address that did not answer `streak` rounds running is asked
        again (`clock`): the next round, then one round in two, four...; a
        second early so the round due then still asks."""
        return self.clock() + min(self.poll_s * 2 ** min(streak - 1, 16), REFUSED_WAIT_S) - 1.0

    def _wall(self, until: float | None) -> float | None:
        """`until` (this poller's clock) as epoch seconds, for the worker."""
        if until is None:
            return None
        return time.time() + max(0.0, until - self.clock())

    # -- the loop --------------------------------------------------------------

    def changed(self) -> None:
        """The registry changed: start the rounds when a daemon session is live."""
        if self._closed or self._handle is not None:
            return
        loop = self._loop_getter()
        if loop is None or not self._sessions():
            return
        self._handle = loop.call_later(self.poll_s, self._tick)

    def _tick(self) -> None:
        self._handle = None
        loop = self._loop_getter()
        if self._closed or loop is None:
            return
        targets = self._sessions()
        if not targets:
            return
        if not self._running:
            try:
                future = asyncio.wrap_future(self._lane.submit(self.poll_round, targets), loop=loop)
            except RuntimeError:
                return
            self._running = True
            future.add_done_callback(self._ended)
        self._handle = loop.call_later(self.poll_s, self._tick)

    def _ended(self, future: asyncio.Future) -> None:
        self._running = False
        if not future.cancelled() and future.exception() is not None:
            self._log(f"run alerts: a round failed: {future.exception()!r}")

    def close(self) -> None:
        self._closed = True
        if self._handle is not None:
            self._handle.cancel()
            self._handle = None
        abort = getattr(self.fetch, "abort", None)
        if abort is not None:
            with contextlib.suppress(Exception):
                abort()  # a request in flight ends now
        with contextlib.suppress(RuntimeError):
            self._lane.submit(getattr(self.fetch, "close", lambda: None))
        self._lane.close()


__all__ = ["AlertPoller", "Answer", "Endpoint", "Fetcher", "POLL_S", "endpoint", "handoff_path", "wanted"]
