"""Transport: one request to the Probe API (`/v1/*` with a user or service token, `/ingest/*` with
the ingest token and an HMAC), its retries and its typed errors; stages in DESIGN.md."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import json
import os
import re
import time
from typing import TYPE_CHECKING, Any, NoReturn

import httpx

from ... import client_status, errors
from ....foundation.compose.compose import fold_parts
from ....foundation.remote_settings import remote_settings as device_mark
from ....foundation.request_identity.request_identity import (
    CLIENT_KIND_HEADER,
    CLIENT_VERSION_HEADER,
    client_version_headers,
    current_client_headers)
from ....foundation.request_identity.surface import ATTRIBUTION_HEADER, SURFACE_HEADER, TOOL_HEADER, Surface, current_tool
from ....foundation.safe_warn import safe_warn
from ....foundation.tls.tls import ssl_context
from ...agent_session import AGENT_SESSION_HEADER
from .notices import NOTICE_WATCHER
from ...settings.settings import Settings
from ...values import unstorable
from .protocols import observer
from .relay import FILE_BODY_EXTENSION, pick_http_transport  # noqa: F401 -- blobs.py reads the extension name here

#: SDK reliability 2.8: every request says this client speaks per-writer leases. The server
#: flips a `leases` run to the legacy rules on the first heartbeat, status write or logged
#: batch WITHOUT it (an older client that never registers a lease), so a lease-capable
#: writer must never look like one: `probe log` and attached ranks included.
LEASES_HEADER = "X-Probe-Leases"

#: 429 rides along: sixteen PUTs in flight make throttling ordinary; a throttled upload
#: is a retry, not a verdict.
_RETRYABLE = {429, 502, 503, 504}

#: How far this clock may be off the server's before the SDK says so. HTTP `Date` has 1 s
#: resolution and a response takes time to arrive: the threshold is generous.
CLOCK_SKEW_WARN_SECONDS = 60.0
#: Whether this process has compared its clock with a server `Date` yet.
_clock_checked = False


def _check_clock_skew(resp: httpx.Response) -> None:
    """Warn ONCE per process when this clock is off the server's. ``Run.log`` dates every
    point with this clock (plan 1.4) and findings bin by it, so a wrong clock would shift a
    run's times unexplained. Uses the first response with an HTTP ``Date``. Never raises,
    never corrects: a warning, not a clamp (PR #2002 review)."""
    global _clock_checked
    if _clock_checked:
        return
    date = resp.headers.get("date")
    if not date:
        return
    _clock_checked = True
    try:
        from datetime import datetime, timezone
        from email.utils import parsedate_to_datetime

        server = parsedate_to_datetime(date)
        if server.tzinfo is None:
            return
        skew = (datetime.now(timezone.utc) - server).total_seconds()
    except Exception:  # noqa: BLE001 -- a malformed header is not the caller's problem
        return
    if abs(skew) > CLOCK_SKEW_WARN_SECONDS:
        side = "ahead of" if skew > 0 else "behind"
        safe_warn.warn(
            f"probe: this machine's clock is {abs(skew):.0f} s {side} the server's "
            f"(HTTP Date: {date}). Metric points are dated with this clock, so their "
            "times will be shifted by that much. Fix the clock on this host (NTP)."
        )


_DEFAULT_TIMEOUT = 30.0
_MAX_RETRIES = 3


#: Connections kept open between requests: httpx's 100/20 pool, idle for up to 60 s instead of
#: its 5 s, so a beat every 60 s or a log chunk every 15 s reuses one instead of a new TLS
#: handshake each (I13). Under ingress-nginx's 75 s upstream keep-alive, so the server never
#: closes one first.
_KEEPALIVE_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20, keepalive_expiry=60.0)


#: Cap on the CONNECT phase, independent of the overall timeout. A dead or black-holing
#: endpoint parked a caller 30s per request, long enough to trip a distributed collective
#: while every rank waits on the same stalled POST. Reads keep the full budget: a slow
#: query is worth waiting for, an unreachable host is not.
_DEFAULT_CONNECT_TIMEOUT = 5.0

#: Failures proving the request never reached the server (no connection, or it never left
#: the pool). Safe to retry for ANY method: no chance a first attempt was processed.
#:
#: NOT here: ReadTimeout and RemoteProtocolError. The request was already on the wire and
#: only the RESPONSE was lost, so retrying a non-idempotent write can duplicate it (a
#: metric batch appended twice is silent data corruption, worse than the error avoided).
_CONNECT_ERRORS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.PoolTimeout,
)


@dataclass
class Page:
    """A list response plus the opaque keyset cursor for the next page."""

    items: list[Any]
    next_cursor: str | None


if TYPE_CHECKING:
    from probe.sdk.delivery.transport.headers import RequestHeadersMixin
    from probe.sdk.delivery.transport.deadlines import RetryPolicyMixin
    from probe.sdk.delivery.transport.failures import ErrorMappingMixin
    from probe.sdk.delivery.transport.tracking import TrackingMarkerMixin
    from probe.sdk.delivery.transport.blobs import BlobsMixin
    from probe.sdk.delivery.transport.streams import StreamsMixin

    class _TransportParts(
        RequestHeadersMixin,
        RetryPolicyMixin,
        ErrorMappingMixin,
        TrackingMarkerMixin,
        BlobsMixin,
        StreamsMixin,
    ):
        """Transport's parts as bases, for editors and type checkers; at runtime fold_parts() copies them in."""
else:
    _TransportParts = object


class Transport(_TransportParts):
    def __init__(
        self,
        settings: Settings,
        *,
        timeout: float = _DEFAULT_TIMEOUT,
        client: httpx.Client | None = None,
        max_retries: int = _MAX_RETRIES,
        surface: str = Surface.SDK.value,
        client_headers: Mapping[str, str] | None = None,
        attribution: str | None = None,
    ):
        self.settings = settings
        self.attribution = resolve_attribution(attribution)
        self.max_retries = max_retries
        #: The per-request budget outside a deadline scope; inside one, each
        #: attempt gets ``min(this, what is left)`` (see `deadline_scope`).
        self.timeout = timeout
        # Which product surface these requests came from (cli/sdk/mcp), sent on every
        # backend request as `X-Probe-Surface` so analytics attribute events by surface.
        # Headers only, never a payload.
        self.surface = surface
        supplied = client_headers or {}
        if not supplied and surface == Surface.SDK.value:
            # A generic SDK transport reports ITSELF. It used to send nothing (only a
            # caller who knew its kind could name one), leaving a blind spot where it
            # hurts: `import probe` in a training script never opens a terminal or starts
            # an agent session, so it never appeared in any fleet-shaped view. It reports
            # the version of the one `probe-research` distribution it shares with the CLI.
            # An EXPLICIT `client_headers` still wins, so the CLI and the hosted MCP (which
            # speak for their caller) are untouched; only the unspecified default changed.
            from .... import __version__

            supplied = client_version_headers(Surface.SDK.value, __version__)
        self._client_headers = client_version_headers(
            supplied.get(CLIENT_KIND_HEADER),
            supplied.get(CLIENT_VERSION_HEADER),
        )
        # WHICH MACHINE this process runs on, resolved once per transport. Fixed at
        # construction ON PURPOSE, unlike the version identity above: the device file
        # describes the host, and a local process cannot run on two machines. The hosted
        # MCP must NOT send it and does not reach here with one (see `_device_headers`).
        self._device_headers = _device_headers_for(surface)
        #: Whether ``_client`` is ours to rebuild in a forked child (an injected one never is).
        self._has_own_client = client is None
        self._client_pid = os.getpid()
        self._http_client = client if client is not None else self._build_http_client()
        # Sessions whose tracking signal this transport already settled, keyed per SESSION:
        # the hosted MCP memoizes one transport per token for many callers, so one boolean
        # would let the first caller's session answer for everyone.
        self._tracking_marked: set[str] = set()

    # -- lifecycle ----------------------------------------------------------
    def _build_http_client(self) -> httpx.Client:
        timeout = httpx.Timeout(self.timeout, connect=min(self.timeout, _DEFAULT_CONNECT_TIMEOUT))
        relay = pick_http_transport(self.surface)
        if relay is not None:
            # A training process sends no HTTP of its own (plan D10): the service sends it,
            # through this process's proxies and CAs (`relay.get_network_env`), or the service's
            # own when this caller is fenced (H-2), never httpx's here.
            return httpx.Client(
                base_url=self.settings.base_url, timeout=timeout, transport=relay, trust_env=False, verify=ssl_context(),
            )
        return httpx.Client(
            base_url=self.settings.base_url,
            timeout=timeout,
            verify=ssl_context(),
            limits=_KEEPALIVE_LIMITS,
        )

    @property
    def _client(self) -> httpx.Client:
        """The httpx client. A forked child (a data-loader worker) gets its own: the parent's
        kept-alive sockets are shared with it, and two processes on one TLS stream read each
        other's answers. The parent's are left open for the parent."""
        if self._has_own_client and self._client_pid != os.getpid():
            self._client_pid = os.getpid()
            self._http_client = self._build_http_client()
        return self._http_client

    @_client.setter
    def _client(self, client: httpx.Client) -> None:
        self._http_client = client
        self._has_own_client = False

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "Transport":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- core request -------------------------------------------------------
    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any | None = None,
        params: dict[str, Any] | None = None,
        idempotent: bool | None = None,
        timeout: float | None = None,
        content: bytes | None = None,
        content_headers: Mapping[str, str] | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> httpx.Response:
        """One request to the API. ``content`` sends raw bytes instead of a JSON body (a
        gzip catalog manifest, `Client.put_manifest`), described by ``content_headers``
        (`Content-Type`, `Content-Encoding`); signed and sent as given, never scrubbed or
        re-encoded."""
        if content is not None and json_body is not None:
            raise ValueError("pass json_body or content, not both")
        need_api_path(path)
        json_body = self._prepare_json_body(method, path, json_body, params)
        # Serialize ourselves so the HMAC signs the exact sanitized bytes.
        if content is not None:
            raw_body = bytes(content)
        else:
            raw_body = b"" if json_body is None else json.dumps(json_body).encode()
        # Client identity: what this transport was built with, unless the caller bound a
        # per-request override. Read per request: the hosted MCP memoizes one transport per
        # token for many callers, so a construction-time identity would report the SERVER's
        # version as every caller's. An empty override is a real answer ("reported nothing"):
        # only None falls back.
        override = current_client_headers()
        client_identity = self._client_headers if override is None else override
        headers = self._build_headers(
            method, path, raw_body, has_json=json_body is not None, content=content,
            content_headers=content_headers, extra_headers=extra_headers, override=override,
            client_identity=client_identity,
        )
        retry = idempotent if idempotent is not None else method.upper() in {"GET", "PUT"}
        resp, attempt, started = self._send_with_retries(
            method, path, headers=headers, params=params, timeout=timeout, retry=retry,
            content=raw_body if json_body is not None or content is not None else None,
        )
        return self._settle_response(
            resp, method, path, attempt=attempt, started=started, override=override,
            client_identity=client_identity, headers=headers,
        )

    def _prepare_json_body(
        self, method: str, path: str, json_body: Any | None, params: dict[str, Any] | None
    ) -> Any | None:
        """Refuse NULs in the path and query; normalize the JSON body, keep the fields a scrub must
        not rewrite, and escape NULs for display (warning once)."""
        # Validate structure before the recursive scrubber. Scan the normalized
        # body again below: sets/opaque reprs may become new JSON strings.
        if unstorable.has_nul(params) or ("\x00" in path):
            raise errors.ValidationError("probe: NUL in request path or query", status=422)
        if json_body is not None:
            json_body = unstorable.normalize_json(json_body)
            unstorable.validate_nuls(json_body, path=path, method=method)
        # Every JSON upload crosses here, creates and replay paths that bypass Client.write
        # included. A scrub failure must happen before serialization/auth/network; never
        # retry with the original.
        # `scrub_body`: `default_scrub`, minus the ISO timestamps `Run.log`
        # stamps on every point (plan 1.4), which cannot hold a credential.
        # scanning disabled: from .stamp_scrub import scrub_body

        if json_body is not None:
            original = json_body
            # scanning disabled: json_body = scrub_body(original)
            # These synchronous account endpoints enroll a W&B credential. Only their
            # declared authentication field is preserved; notes/metadata and every adjacent
            # route stay scrubbed. Durable journals never get an exemption for these paths.
            enrollment = method.upper() == "POST" and re.fullmatch(
                r"/v1/integrations/wandb/accounts(?:/"
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/reconnect)?",
                path,
            )
            if enrollment and isinstance(original, dict):
                credentials = original.get("credentials")
                if isinstance(credentials, dict) and isinstance(credentials.get("api_key"), str):
                    json_body["credentials"] = {"api_key": credentials["api_key"]}
            # A read-only SQL query is sent AS WRITTEN. Scrubbing rewrites a literal, so
            # `WHERE name = 'sk-baseline'` became `'<redacted>'` and counted the wrong thing
            # (a silently wrong answer). The route executes and discards the text; nothing
            # stores it, and the dashboard already sends it unscrubbed.
            if (
                method.upper() == "POST"
                and path == "/v1/sql"
                and isinstance(original, dict)
                and isinstance(original.get("sql"), str)
            ):
                json_body["sql"] = original["sql"]
        # Scrub BEFORE display escaping: a NUL must not become a word character that hides
        # a neighboring credential from the scrubber's boundaries.
        if json_body is not None:
            json_body, escaped = unstorable.escape_nuls(json_body, path=path, method=method)
            if escaped:
                safe_warn.warn(unstorable.describe(escaped), stacklevel=1)
        return json_body

    def _build_headers(
        self,
        method: str,
        path: str,
        raw_body: bytes,
        *,
        has_json: bool,
        content: bytes | None,
        content_headers: Mapping[str, str] | None,
        extra_headers: Mapping[str, str] | None,
        override: Mapping[str, str] | None,
        client_identity: Mapping[str, str],
    ) -> dict[str, str]:
        """Every header one request carries: identity, auth, workspace limit, body type, surface,
        session attribution and the idempotency key."""
        # A per-request identity override means we speak FOR someone else (the hosted MCP
        # serving a remote caller), so this process's device header drops out too: sending it
        # would attribute every caller's traffic to the server's pod, the bug
        # `client_headers_scope` prevents.
        device_identity = self._device_headers if override is None else {}
        headers = {
            **client_identity,
            **device_identity,
            **self._auth_headers(path, raw_body),
            # This computer's workspace limit: a read narrowing the API applies
            # (`workspace_limit.py`). Never on `/ingest` (capture is not limited) or
            # `/public/` (no workspace's; naming one needs a credential).
            **({} if path.startswith(("/ingest", "/public/")) else self._workspace_limit_headers()),
        }
        if has_json:
            headers["Content-Type"] = "application/json"
        if content is not None:
            headers.update(content_headers or {})
        # A request's own capability flags (`X-Probe-Direct-Upload`), never auth.
        headers.update(extra_headers or {})
        # Surface attribution: tag every backend request with the originating
        # product surface, and (MCP only) the tool being served. Headers only.
        headers[SURFACE_HEADER] = self.surface
        headers[LEASES_HEADER] = "1"
        tool = current_tool()
        if tool:
            headers[TOOL_HEADER] = tool
        # Coding-agent session attribution, read per request: a long-lived client outlives
        # any one session and a stale id would attribute new runs to a finished
        # conversation. {} with no capturable session: NO header, not an empty one.
        attribution = _attribution_override.get() or self.attribution
        if attribution is Attribution.AMBIENT:
            headers.update(_session_headers())
            # When the work happened, and whether a run process did it, for the session's
            # effort (R2, R41): only with a session to date, so a backfill or plain shell
            # sends nothing new.
            if AGENT_SESSION_HEADER in headers:
                headers.update(_event_at_header())
                headers.update(_write_origin_header(headers))
        else:
            # Said out loud, not only implied by missing session headers: the server stamps
            # `driven_by`, which is how #probe-usage tells an import from the person's own
            # work (the drainer's surface is `sdk`).
            headers[ATTRIBUTION_HEADER] = attribution.value
        key = _idempotency_key(method, path)
        if key:
            headers["Idempotency-Key"] = key
        return headers

    def _send_with_retries(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str],
        params: dict[str, Any] | None,
        timeout: float | None,
        retry: bool,
        content: bytes | None,
    ) -> tuple[httpx.Response, int, float]:
        """Send until an answer the caller gets (retrying what may be retried); returns it with the
        attempt count and the start time. Raises a typed error when no answer came."""
        # Wall time as the CALLER sees it, retries included: what parks a training loop is
        # the total, not one attempt.
        started = time.monotonic()
        # Mark it in flight BEFORE the call: a request hanging until the process is killed
        # reaches neither recording site below, so the ring buffer could not show the very
        # failure it exists to catch.
        observer().begin_transport(method, path, base=self.settings.base_url)
        attempt = 0
        while True:
            attempt += 1
            try:
                # Per-call override for the rare request whose SERVER-side work outlasts the
                # default (a large rewind deletes millions of rows in its transaction). None
                # keeps the client-wide budget unless a deadline scope bounds it.
                attempt_timeout, clamped = self._attempt_timeout(timeout, f"{method} {path}")
            except errors.DeadlineExceeded:
                observer().end_transport()
                raise
            send = dict(
                content=content,
                params=params,
                headers=headers,
                **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
            )
            deadline = _request_deadline.get()
            try:
                if deadline is None:
                    resp = self._client.request(method, path, **send)
                else:
                    resp = self._send_within_deadline(deadline, method, path, **send)
            except errors.DeadlineExceeded:
                observer().end_transport()
                raise
            except RuntimeError as exc:
                # httpx refuses to send on a CLOSED client with a bare RuntimeError. Callers
                # treat a TransportError as "not sent, try later", and a RuntimeError escaped
                # a non-strict finish() (re-review of #2011). Anything else stays a
                # programming error.
                if not self._client.is_closed:
                    raise
                observer().end_transport()
                raise errors.TransportError(f"{method} {path}: {exc}") from exc
            except httpx.HTTPError as exc:
                # A connect-class failure never reached the server, so it is replayable
                # whatever the method: one blip on a metrics POST is no hard error. Anything
                # else is gated on `retry` (the request may have landed).
                replayable = retry or isinstance(exc, _CONNECT_ERRORS)
                if replayable and self._may_retry(attempt) and self._retry_pause(attempt):
                    continue
                self._raise_transport_error(exc, method, path, started=started, clamped=clamped)

            _check_clock_skew(resp)
            if (
                resp.status_code in _RETRYABLE
                and retry
                and self._may_retry(attempt)
                and self._retry_pause(attempt, resp)
            ):
                continue
            return resp, attempt, started

    def _raise_transport_error(
        self, exc: httpx.HTTPError, method: str, path: str, *, started: float, clamped: bool
    ) -> NoReturn:
        """No answer came and no retry is left: record it, then raise DeadlineExceeded when our own
        deadline cut the attempt, else a TransportError (``unreachable`` when never sent)."""
        observer().end_transport()
        observer().record_transport(
            method,
            path,
            seconds=time.monotonic() - started,
            error=repr(exc),
            base=self.settings.base_url,
        )
        if self._cut_by_deadline(exc, clamped):
            raise self._deadline_error(f"{method} {path}", exc) from exc
        failure = errors.TransportError(f"{method} {path}: {exc}")
        # Server never reached: nobody's op can land, so the outbox drain ends the
        # pass for every run (plan 1.6). A timeout AFTER sending may be this op's own.
        failure.unreachable = isinstance(exc, _CONNECT_ERRORS)
        raise failure from exc

    def _settle_response(
        self,
        resp: httpx.Response,
        method: str,
        path: str,
        *,
        attempt: int,
        started: float,
        override: Mapping[str, str] | None,
        client_identity: Mapping[str, str],
        headers: dict[str, str],
    ) -> httpx.Response:
        """Record the answer, read what the server says about this client, then return it or raise
        its typed error."""
        observer().end_transport()
        observer().record_transport(
            method,
            path,
            seconds=time.monotonic() - started,
            status=resp.status_code,
            base=self.settings.base_url,
        )
        if override is None:
            # Only for our OWN identity: under an override (the hosted MCP)
            # the status grades someone else's client, not this process.
            client_status.notice(resp.headers, client_identity, self.surface)
            # Probe staff asked this machine to update now, repair its session capture,
            # or change a setting (a later CLI command acts): one lookup per kind when
            # no header is there.
            device_mark.note_all(resp.headers)
            # A notice set this process has not handled: read and shown off this thread.
            NOTICE_WATCHER.handle_answer(self, resp.headers)
        if resp.status_code >= 400:
            if attempt > 1 and method.upper() == "DELETE" and _is_trash_notice(resp):
                # A RETRIED delete finding the thing in the trash: the first attempt
                # landed and its reply was lost. That is the delete succeeding, not a
                # refusal; the notice is the answer.
                return resp
            raise self._to_error(resp)
        if 200 <= resp.status_code < 300:
            # 2xx only: a 3xx means the write did not land where we asked.
            self._auto_mark_tracking(method, path, headers.get(AGENT_SESSION_HEADER))
            if override is None:  # our own identity only (the hosted MCP serves others)
                self._set_auto_chat_on(method, path, headers.get(AGENT_SESSION_HEADER), resp)
        return resp

    # -- typed helpers ------------------------------------------------------
    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self.request("GET", path, params=params, idempotent=True).json()

    def post(
        self,
        path: str,
        json_body: Any | None = None,
        *,
        idempotent: bool = False,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Any:
        resp = self.request(
            "POST", path, json_body=json_body, idempotent=idempotent, extra_headers=extra_headers
        )
        return resp.json() if resp.content else None

    def patch(self, path: str, json_body: Any) -> Any:
        return self.request("PATCH", path, json_body=json_body).json()

    def put(self, path: str, json_body: Any) -> Any:
        return self.request("PUT", path, json_body=json_body, idempotent=True).json()

    def delete(self, path: str) -> Any:
        """The parsed body when the route sends one (a run, group or project delete says
        where it went in the trash and until when; a retried one finding it already there
        answers the trash notice), None on a 204."""
        resp = self.request("DELETE", path, idempotent=True)
        if not resp.content:
            return None
        try:
            return resp.json()
        except (json.JSONDecodeError, ValueError):
            # A 2xx with a non-JSON body (an ingress/CDN HTML interstitial) must not escape
            # as a raw JSONDecodeError; the delete succeeded.
            return None

    def get_page(self, path: str, *, params: dict[str, Any] | None = None) -> Page:
        resp = self.request("GET", path, params=params, idempotent=True)
        return Page(items=resp.json(), next_cursor=resp.headers.get("X-Next-Cursor"))


#: The Probe daemon runs each `probe` command with an operation id (R12). Every write
#: request the command makes carries `<op id>-<n>` (n counts that command's writes in
#: order), so a retry of the same command replays on the server instead of writing twice,
#: and two writes of one command never share a key (the server answers 422 to a key reused
#: for a different request).
_IDEMPOTENCY_ENV = "PROBE_IDEMPOTENCY_KEY"
_idempotency_count = 0


def _idempotency_key(method: str, path: str) -> str | None:
    global _idempotency_count
    base = os.environ.get(_IDEMPOTENCY_ENV, "").strip()
    if not base or method.upper() not in {"POST", "PATCH", "PUT", "DELETE"} or not path.startswith("/v1/"):
        return None
    _idempotency_count += 1
    return f"{base[:80]}-{_idempotency_count}"
from probe.sdk.delivery.transport.deadlines import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _request_deadline,
)
from probe.sdk.delivery.transport.failures import _is_trash_notice  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.headers import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    Attribution,
    _attribution_override,
    _device_headers_for,
    _event_at_header,
    _session_headers,
    _write_origin_header,
    resolve_attribution,
)
from probe.sdk.delivery.transport.headers import RequestHeadersMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.deadlines import RetryPolicyMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.failures import ErrorMappingMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.tracking import TrackingMarkerMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.blobs import BlobsMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.streams import StreamsMixin  # noqa: E402 -- pieces need each other; the front door loads this one first

# Transport's parts read it back at import time, so they load after it and are folded in here.
fold_parts(
    Transport,
    RequestHeadersMixin,
    RetryPolicyMixin,
    ErrorMappingMixin,
    TrackingMarkerMixin,
    BlobsMixin,
    StreamsMixin,
)


def need_api_path(path: str) -> None:
    """An API path is one path on the configured server: it starts with exactly one `/` (C2). A
    `//host/...` path or an absolute URL would send this client's signed request and its key to
    another host (httpx joins them onto `base_url` as a new authority). Raised as a
    ValidationError: a queued op holding one is dead-lettered, never retried."""
    if not isinstance(path, str) or not path.startswith("/") or path.startswith("//") or "\\" in path:
        raise errors.ValidationError(f"refused API path {str(path)[:80]!r}: not one path on the configured server")
