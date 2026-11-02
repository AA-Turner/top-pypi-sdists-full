"""POST /v1/hints over a kept connection, with the session's own key and every credential scrubbed from the text."""

from __future__ import annotations
import json
import threading
import time
from urllib.parse import urlsplit

from ..watch.alertpoll import Endpoint, Fetcher, endpoint
from probe.service.hints.trigger import Trigger
from probe.service.hints.triggers.window import MAX_TEXT_CHARS
ROUTE = "/v1/hints"
#: One request, connect to last byte.
TIMEOUT_S = 5.0
#: A window request (plan hints-window-trigger W1/W3): the server spends up to
#: its 4 s engine budget and then at most five database statements (1.5 s
#: deadline each) before it answers.
WINDOW_TIMEOUT_S = 12.0
#: The CLI config's credentials, the read-only one first: the route only reads.
KEYS = ("mcp_token", "token", "companion_token")
#: The CLI's environment overrides of the config's endpoint and keys
#: (`sdk.config.resolve`, `daemon.model.endpoint`): a session with one talks to
#: another deployment or as another key, so the lane never asks for it.
_ENV_OVERRIDES = ("PROBE_BASE_URL", "PROBE_MCP_TOKEN", "PROBE_TOKEN", "PROBE_DAEMON_KEY")


# -- the request ------------------------------------------------------------------


def scrubbed(text: str, limit: int = MAX_TEXT_CHARS) -> str:
    """`text` as it may leave this machine: every credential the capture's one
    detector finds replaced (`probe.tap_core.secrets`, as the daemon's store and
    the tap's journal do before transcript text goes out), then cut to `limit`."""
    from probe.tap_core import secrets as detector  # not the stdlib `secrets` this module uses

    clean, _rules = detector.redact(text)
    return clean[:limit]


def names_trigger(data: object) -> bool:
    """A 422 whose detail names the `trigger` field: a server that knows no
    `window` lookup (any other 422 is about one request's content)."""
    detail = data.get("detail") if isinstance(data, dict) else None
    return isinstance(detail, list) and any(
        isinstance(item, dict) and "trigger" in (item.get("loc") or []) for item in detail)


def credentials(env: dict) -> Endpoint | None:
    """The API and the read key of the CLI config the session's own processes
    read (its PROBE_CONFIG_PATH / XDG_CONFIG_HOME / HOME), its current context's
    address only (`caller.known_endpoint`: a key goes nowhere else). None when
    the session's environment overrides the endpoint or a key (_ENV_OVERRIDES)."""
    from ..actions import caller

    if any(env.get(name) for name in _ENV_OVERRIDES):  # the session's own (its recorder's `env`)
        return None
    try:
        return endpoint(str(caller._config_path(env)), KEYS, environ=env)
    except Exception:  # noqa: BLE001
        return None


class HintFetcher(Fetcher):
    """POST /v1/hints over a kept connection per endpoint (`alertpoll.Fetcher`'s)."""

    timeout = TIMEOUT_S
    #: Set by `abort()` for every endpoint (the lane closing): no request, and
    #: no second try of one in flight, goes after it.
    closing = False

    def abort(self, base: str | None = None) -> None:
        if base is None:
            self.closing = True
        super().abort(base)

    def __call__(self, ep: Endpoint, body: dict) -> tuple[int | None, object]:
        """`(HTTP status, the JSON answer)`, or `(None, None)` with no answer in time."""
        if self.closing:
            return None, None
        prefix = urlsplit(ep.base_url).path.rstrip("/")
        headers = {
            "Authorization": f"Bearer {ep.key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"probe-service/{self.version}",
            **self._client_headers(),
            **self._limit_headers(ep),
        }
        payload = json.dumps(body).encode("utf-8")
        limit = WINDOW_TIMEOUT_S if body.get("trigger") == Trigger.WINDOW else TIMEOUT_S
        deadline = time.monotonic() + limit
        cutoff = threading.Timer(limit, self.abort, args=(ep.base_url,))
        cutoff.daemon = True
        cutoff.start()
        try:
            return self._post(ep, f"{prefix}{ROUTE}", payload, headers, deadline, limit)
        finally:
            cutoff.cancel()

    def _post(self, ep: Endpoint, path: str, payload: bytes, headers: dict, deadline: float, limit: float):
        import http.client

        for attempt in (1, 2):
            try:
                conn = self._connection(ep.base_url)
                # One socket operation, at most this request's own limit: a kept
                # connection's next connect, and its socket now.
                conn.timeout = limit
                if conn.sock is not None:
                    conn.sock.settimeout(limit)
                conn.request("POST", path, body=payload, headers=headers)
                resp = conn.getresponse()
                body = self._read(resp, deadline)
                if body is None or not resp.isclosed() or resp.will_close:
                    self.drop(ep.base_url)
                if body is None:
                    return None, None
                break
            except (http.client.RemoteDisconnected, BrokenPipeError, ConnectionResetError):
                # A kept connection the server closed meanwhile: once more, fresh
                # (the route only reads, so asking twice is safe). Never past the
                # deadline: the cutoff's own shutdown lands here too, and a second
                # try then would ask a slow server twice and wait on it again.
                self.drop(ep.base_url)
                if attempt == 2 or time.monotonic() >= deadline or self.closing:
                    return None, None
            except (OSError, ValueError, http.client.HTTPException):
                self.drop(ep.base_url)
                return None, None
        try:
            data = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError, RecursionError):
            data = None
        return resp.status, data
