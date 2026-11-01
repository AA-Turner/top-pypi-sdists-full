"""SDK HTTP transport over the Probe Research v3 contract: a thin httpx wrapper for the two
auth surfaces (``/v1/*`` Bearer ``probe_pat_...``; ``/ingest/*`` Bearer ``ros_ing_...`` plus
optional X-Signature HMAC). Maps HTTP status to ``errors`` types, retries idempotent calls
on 5xx/network blips with capped backoff; paginated reads expose ``X-Next-Cursor`` via
:class:`Page`.
"""

from __future__ import annotations

from ...secret_gate import freeze_stream, freeze_upload

import hashlib
import hmac
import json
import os
import re
import time
from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any

import httpx

from ....foundation.request_identity.request_identity import (
    CLIENT_KIND_HEADER,
    CLIENT_VERSION_HEADER,
    client_version_headers,
    current_client_headers)

from ....foundation.remote_settings import remote_settings as device_mark
from ... import client_status
from .protocols import observer
from ....foundation.durable import durable
from ... import errors
from ....foundation.safe_warn import safe_warn
from ... import session_marker
from ...values import unstorable
from ...settings import workspace_limit as _workspace_limit
from ...settings.settings import DAEMON_SHELL_CONFIG, Settings
from ...agent_session import AGENT_SESSION_HEADER
from ....foundation.request_identity.surface import ATTRIBUTION_HEADER, SURFACE_HEADER, TOOL_HEADER, Surface, current_tool
from ....foundation.tls.tls import ssl_context
from probe.sdk.delivery.transport.blobs import _blob_label, _instrumented, _iter_file, _warn_upload_inspection

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


class Transport:
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
        self._client = client or httpx.Client(
            base_url=settings.base_url,
            timeout=httpx.Timeout(timeout, connect=min(timeout, _DEFAULT_CONNECT_TIMEOUT)),
            verify=ssl_context(),
        )
        # Sessions whose tracking signal this transport already settled, keyed per SESSION:
        # the hosted MCP memoizes one transport per token for many callers, so one boolean
        # would let the first caller's session answer for everyone.
        self._tracking_marked: set[str] = set()

    # -- lifecycle ----------------------------------------------------------
    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "Transport":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- auth ---------------------------------------------------------------
    def _auth_headers(self, path: str, raw_body: bytes) -> dict[str, str]:
        headers: dict[str, str] = {}
        if path.startswith("/public/"):
            # Public reads (Probe's docs) carry no credential: needed most when sign-in
            # broke, and a token there would be ignored.
            return headers
        is_ingest = path.startswith("/ingest")
        if is_ingest:
            if not self.settings.ingest_token:
                raise errors.AuthError("no ingest token configured (set PROBE_INGEST_TOKEN)")
            headers["Authorization"] = f"Bearer {self.settings.ingest_token}"
            if self.settings.hmac_secret:
                sig = hmac.new(
                    self.settings.hmac_secret.encode(), raw_body, hashlib.sha256
                ).hexdigest()
                headers["X-Signature"] = f"sha256={sig}"
        else:
            # /v1 accepts a user PAT (probe_pat_) OR a read-only service token (probe_svc_);
            # the backend dispatches on the prefix. A Reader carries only the service token.
            bearer = self.settings.token or self.settings.service_token
            if not bearer:
                if os.environ.get("PROBE_CONFIG_PATH") == DAEMON_SHELL_CONFIG:
                    raise errors.AuthError(
                        "no API token here: this is the Probe daemon's shell, which has no Probe key on "
                        "purpose. Run the probe command as a command of its own (`probe ...`, or chained: "
                        "`cd x && probe ...`): the daemon writes to Probe only that way, with its checks."
                    )
                raise errors.AuthError(
                    f"no API token configured ({session_marker.WIZARD_HINT}, or set "
                    "PROBE_SERVICE_TOKEN)"
                )
            headers["Authorization"] = f"Bearer {bearer}"
        return headers

    # -- workspace limit -------------------------------------------------------
    def _workspace_limit_headers(self) -> dict[str, str]:
        """The limit headers for one request, read per request like the client identity:
        none inside `workspace_limit.without_limit()` (a picker's list); under the hosted
        MCP's per-request scope the CALLER's (an empty one included: they sent none); else
        this transport's settings'. An environment slug is looked up once, without the
        limit. Raises rather than sending nothing: a limit this process cannot name is
        never dropped."""
        if _workspace_limit.suppressed():
            return {}
        forwarded = _workspace_limit.forwarded()
        if forwarded is not None:
            return dict(forwarded)
        limit = getattr(self.settings, "workspace_limit", None)
        if limit is None:
            return {}

        def listed() -> Any:
            with _workspace_limit.without_limit():
                return self.request("GET", "/v1/workspaces", idempotent=True).json()

        bearer = self.settings.token or self.settings.service_token
        ident = _workspace_limit.resolve_id(
            limit, base_url=self.settings.base_url, list_workspaces=listed,
            account=_workspace_limit.account_key(bearer),
        )
        return _workspace_limit.request_headers(limit, ident)

    # -- deadline -------------------------------------------------------------
    def _attempt_timeout(self, requested: float | None, what: str) -> tuple[Any, bool]:
        """``(timeout kwarg value, clamped)`` for one attempt. Outside a
        :func:`deadline_scope`: ``requested`` untouched (None keeps the client-wide budget),
        ``clamped`` False. Inside: ``min(requested or self.timeout, remaining)``, with
        ``clamped`` saying the deadline set the bound. Raises
        :class:`errors.DeadlineExceeded` when nothing is left: the request is never sent."""
        deadline = _request_deadline.get()
        if deadline is None:
            return requested, False
        left = deadline - time.monotonic()
        if left <= 0:
            raise errors.DeadlineExceeded(f"{what}: deadline passed before it was sent")
        base = float(self.timeout if requested is None else requested)
        bound = min(base, left)
        return httpx.Timeout(bound, connect=min(bound, _DEFAULT_CONNECT_TIMEOUT)), bound < base

    @staticmethod
    def _retry_pause(attempt: int, resp: httpx.Response | None = None) -> bool:
        """Sleep before retry ``attempt + 1``; False, without sleeping, when that retry must
        not happen here (the caller raises the failure it has).

        The wait is the transport's step on the one backoff ladder
        (`durable.backoff_delays`, `_TRANSPORT_BACKOFF`: 0.2 s doubling to 2 s), LENGTHENED
        to the server's ``Retry-After`` when ``resp`` carries one (plan 0.4/0.6: the server
        sends a jittered one on a lock timeout, 5 s on `entitlement_unavailable`). Never
        retries sooner than asked:

        * a ``Retry-After`` over `_INLINE_RETRY_AFTER_MAX` is not waited out inside one
          request: the error goes back at once carrying ``retry_after`` and the caller's own
          loop (outbox worker, exporter, `finish()`, each with its own ceiling and deadline)
          waits;
        * inside a `deadline_scope` with no room for the wait AND another attempt, no retry
          at all rather than retry early.
        """
        deadline = _request_deadline.get()
        retry_after = _retry_after_seconds(resp) if resp is not None else None
        if _patient() and deadline is not None:
            return Transport._patient_pause(
                attempt, retry_after, deadline, status=resp.status_code if resp is not None else None
            )
        (*_, delay) = durable.backoff_delays(attempt + 1, _TRANSPORT_BACKOFF)
        if retry_after is not None and retry_after > _INLINE_RETRY_AFTER_MAX:
            return False
        pause = durable.honor_retry_after(delay, retry_after, ceiling=_INLINE_RETRY_AFTER_MAX)
        if deadline is not None and deadline - time.monotonic() <= pause:
            return False
        time.sleep(pause)
        return True

    @staticmethod
    def _patient_pause(
        attempt: int, retry_after: float | None, deadline: float, *, status: int | None = None
    ) -> bool:
        """`_retry_pause` inside :func:`patience`: the jittered `_PATIENCE_BACKOFF` step,
        lengthened to any ``Retry-After`` the budget can hold, shortened so a last attempt
        fits before the deadline. False when no room. The scope's FIRST retry says so, once,
        on stderr."""
        room = deadline - time.monotonic() - _PATIENCE_LAST_ATTEMPT
        if room <= 0 or (retry_after is not None and retry_after > room):
            return False
        _announce_patience(status)
        (*_, step) = durable.backoff_delays(attempt + 1, _PATIENCE_BACKOFF)
        jittered = step / 2 + _JITTER.uniform(0, step / 2)
        time.sleep(min(durable.honor_retry_after(jittered, retry_after, ceiling=room), room))
        return True

    def _may_retry(self, attempt: int) -> bool:
        """The COUNT half of the retry decision: ``max_retries`` quick tries, or,
        inside :func:`patience`, as many as the deadline allows."""
        return attempt <= self.max_retries or _patient()

    @staticmethod
    def _deadline_error(what: str, exc: BaseException) -> errors.DeadlineExceeded:
        """The deadline cut an attempt: ``sent`` when only the response was lost
        (a read timeout), so the server may have applied the request."""
        return errors.DeadlineExceeded(f"{what}: {exc}", sent=isinstance(exc, httpx.ReadTimeout))

    def _send_within_deadline(self, deadline: float, method: str, path: str, **kwargs) -> httpx.Response:
        """Send, then read the body chunk by chunk, checking ``deadline`` between chunks.
        httpx timeouts bound each socket operation, not the request: a response trickling a
        byte at a time never trips one (live: a close with ``flush_timeout=2`` took 9.8 s).
        Returns an ordinary, fully read response."""
        with self._client.stream(method, path, **kwargs) as resp:
            if resp.is_stream_consumed:  # an in-memory transport already read it
                resp.read()
                return resp
            chunks: list[bytes] = []
            for chunk in resp.iter_raw():
                chunks.append(chunk)
                if time.monotonic() >= deadline:
                    raise errors.DeadlineExceeded(
                        f"{method} {path}: deadline passed while reading the response", sent=True
                    )
        return httpx.Response(
            resp.status_code,
            headers=resp.headers,
            content=b"".join(chunks),
            request=resp.request,
            extensions=resp.extensions,
        )

    @staticmethod
    def _cut_by_deadline(exc: BaseException, clamped: bool) -> bool:
        """A timeout that fired only because the deadline shortened the attempt: our clock
        ran out, not the server's patience."""
        deadline = _request_deadline.get()
        return (
            clamped
            and deadline is not None
            and isinstance(exc, httpx.TimeoutException)
            and time.monotonic() >= deadline
        )

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
        if json_body is not None:
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

        retry = idempotent if idempotent is not None else method.upper() in {"GET", "PUT"}
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
                content=raw_body if json_body is not None or content is not None else None,
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

            _check_clock_skew(resp)
            if (
                resp.status_code in _RETRYABLE
                and retry
                and self._may_retry(attempt)
                and self._retry_pause(attempt, resp)
            ):
                continue

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
            return resp

    def _auto_mark_tracking(self, method: str, path: str, session_id: str | None) -> None:
        """First research write of a coding-agent session SETTLES its tracking signal at the
        process cwd's effective default, so local surfaces stop disagreeing with the backend
        about whether the session is tracked. AFTER success on purpose: a write that never
        landed marks nothing, and a server commit the client never saw heals on the next
        successful write.

        It settles at the DEFAULT, not `on`. A write is the agent's act, not the
        researcher's declaration: it may record the value the session started at, never
        change it. On a default-off machine it writes `off`, so the warn layer keeps warning
        about the write that just happened (the honest reading). SessionStart seeds the same
        value, so this is normally a no-op; it covers a session started before the seed
        shipped.

        Never marks: reads; non-research routes (`_RESEARCH_PATH_PREFIXES`); a session held
        by the `PROBE_SESSION_TRACKING` env override (a signal file would outlive and defeat
        a machine-wide forced-off, so with the env holding the setting, EITHER direction,
        nothing is written); an explicit per-session decision (the helper's own contract).

        ONLY A SETTLED SESSION IS REMEMBERED. `set_tracking_if_absent` returns False for "a
        decision exists" and for a transient I/O failure (read-only state dir, full disk);
        caching on False alone would leave the session unmarked for the transport's life.
        A failure is not remembered: it costs one extra stat on the next write.

        Fail-soft: must never break the write it rides on; any surprise is swallowed and
        not remembered.
        """
        if not session_id or session_id in self._tracking_marked:
            return
        if method.upper() in _READ_METHODS:
            return
        if not _is_research_path(path):
            return
        try:
            # Normal path: SessionStart already settled it. Read before resolving any
            # default so a later folder edit adds no ancestor I/O to every write.
            if session_marker.tracking_signal(session_id) is not None:
                settled = True
            elif session_marker.tracking_env_override() is not None:
                settled = True  # held by the env for this process's lifetime
            elif session_marker.set_tracking_if_absent(
                session_id, session_marker.resolve_tracking_default(None)[0]
            ):
                settled = True  # this call decided it
            else:
                # False is ambiguous: a decision exists, or the write failed.
                settled = session_marker.tracking_signal(session_id) is not None
        except Exception:  # noqa: BLE001 - by the fail-soft contract above
            return
        if not settled:
            return
        if len(self._tracking_marked) >= _TRACKING_MEMO_CAP:
            self._tracking_marked.clear()
        self._tracking_marked.add(session_id)

    def _to_error(self, resp: httpx.Response) -> errors.RosError:
        try:
            body = resp.json()
            detail = body.get("detail")
            if body.get("code") == errors.CLIENT_TOO_OLD:
                min_version = body.get("min_version")
                min_version = min_version if isinstance(min_version, str) else None
                return errors.ClientTooOldError(
                    errors.upgrade_message(errors._detail_message(detail), min_version),
                    status=resp.status_code,
                    detail=detail,
                    min_version=min_version,
                )
            # A run, group, experiment or project in the TRASH answers 410 with a fixed token
            # plus the notice ("in the trash since ..., Probe can restore it until ...").
            # The sentence is what a person or agent needs; the token alone says nothing.
            in_trash = detail == "in_trash"
            if in_trash and isinstance(body.get("message"), str):
                detail = body["message"]
        except (json.JSONDecodeError, ValueError, AttributeError):
            detail, in_trash = resp.text, False
        error = errors.error_for(resp.status_code, detail)
        if in_trash:
            error.in_trash = True
        applied = resp.headers.get(_workspace_limit.APPLIED_HEADER)
        if applied and resp.status_code == 404:
            # The API answered under this computer's workspace limit: what was asked for may
            # exist outside it. Said, never left to read as gone (agents have filed
            # data-loss reports off a silent miss).
            error.workspace_limit_applied = applied
            _workspace_limit.annotate_not_found(
                error,
                _workspace_limit.hidden_hint(applied, getattr(self.settings, "workspace_limit", None)),
            )
        return _with_retry_after(error, resp)

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

    @_instrumented("PUT")
    def put_url(
        self,
        url: str,
        data: bytes,
        *,
        content_type: str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        """Raw PUT of bytes to a presigned URL (artifact upload, fold #16). No
        Authorization header (the URL carries its signature); goes to an absolute URL (R2),
        not the API base; retried on network blips."""
        # No local content scan: the presigned digest pins these bytes, so a scan could only
        # warn; the server inspects every upload and returns its own warning
        # (`_warn_upload_inspection` below).
        data = bytes(data)
        request_headers = dict(headers or {})
        if content_type:
            request_headers.setdefault("Content-Type", content_type)
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            try:
                resp = self._client.put(
                    url,
                    content=data,
                    headers=request_headers,
                    **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _presigned_put_error(resp, url)
            _warn_upload_inspection(resp)
            return

    @freeze_upload
    def put_file(
        self,
        url: str,
        path: str,
        *,
        content_type: str | None = None,
        headers: Mapping[str, str] | None = None,
        chunk_size: int = 1 << 20,
    ) -> None:
        """Stream a local file to a presigned URL without buffering it (an anchored artifact
        can be model weights; reading it into ``bytes`` OOMs the training loop). No
        Authorization header; the URL carries its signature.

        Content-Length is measured from the open file on every attempt, never from a
        caller's size. A generator body makes httpx use ``Transfer-Encoding: chunked`` (a
        presigned R2/S3 PUT rejects it, 411), and a declared length disagreeing with the
        streamed bytes frames the PUT wrong (short truncates the stored object, long hangs
        the connection). Same handle, so header and body stay in lockstep.

        Re-opens ``path`` every attempt: httpx does not rewind a consumed body, so a retry
        must stream from byte 0, else a spent handle sends a truncated body the server
        stores and confirms as complete."""
        request_headers = dict(headers or {})
        if content_type:
            request_headers.setdefault("Content-Type", content_type)
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            try:
                with open(path, "rb") as fh:
                    request_headers["Content-Length"] = str(os.fstat(fh.fileno()).st_size)
                    resp = self._client.put(
                        url,
                        content=_iter_file(fh, chunk_size),
                        headers=request_headers,
                        **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                    )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _presigned_put_error(resp, url)
            _warn_upload_inspection(resp)
            return

    @_instrumented("PUT")
    def put_part(
        self,
        url: str,
        path: str,
        *,
        offset: int,
        length: int,
        chunk_size: int = 1 << 20,
    ) -> str | None:
        """PUT bytes ``[offset, offset + length)`` of ``path`` to a presigned multipart PART
        URL (plan item (g)); returns the store's ETag.

        THE ONE BYTE PATH WITH NO LOCAL CREDENTIAL GATE, on purpose. Every other upload goes
        through `freeze_upload`/`freeze_stream`, which read the whole body, refuse anything
        over the 64 MiB inspection limit and may redact it. A part is a slice of an artifact
        over that limit: redacting would break the sha256 the whole object is verified
        against, and the limit is why the file goes this way. These bytes reach object
        storage BEFORE anything scans them; the server's verifier inspects a bounded prefix
        afterwards and RECORDS what it finds on the artifact; nothing is blocked. The caller
        already refused a credential in the PATH (`secret_gate._check_path`).

        Streams (never buffers), Content-Length fixed to ``length`` and the body cut at it,
        re-opening the file every attempt like `put_file`. No Authorization header."""
        headers = {"Content-Length": str(length)}
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            try:
                with open(path, "rb") as fh:
                    fh.seek(offset)
                    resp = self._client.put(
                        url,
                        content=_iter_file(fh, chunk_size, length),
                        headers=headers,
                        **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                    )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                # #2075: a 401/403 refuses this part's signed URL, never the login (none is
                # sent): `UploadRefused`, not an auth block.
                raise _presigned_put_error(resp, url)
            return resp.headers.get("etag")

    @_instrumented("PUT")
    @freeze_stream
    def put_fileobj(
        self,
        url: str,
        fh: Any,
        *,
        size: int,
        content_type: str | None = None,
        headers: Mapping[str, str] | None = None,
        chunk_size: int = 1 << 20,
    ) -> None:
        """PUT an already-open, already-verified file handle to a presigned URL. The
        per-file capture path hashes a descriptor before streaming it (bytes sent = bytes
        checked); this sibling of :meth:`put_file` takes that descriptor instead of
        re-opening a path it cannot vouch for. Sends exactly ``size`` bytes, rewinding to
        byte 0 every attempt. No Authorization header."""
        request_headers = dict(headers or {})
        if content_type:
            request_headers.setdefault("Content-Type", content_type)
        request_headers["Content-Length"] = str(size)
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            fh.seek(0)
            try:
                resp = self._client.put(
                    url,
                    content=_iter_file(fh, chunk_size, size),
                    headers=request_headers,
                    **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _presigned_put_error(resp, url)
            _warn_upload_inspection(resp)
            return

    @_instrumented("GET")
    def get_url(self, url: str) -> bytes:
        """Raw GET of a presigned URL (artifact download); returns the bytes. No
        Authorization header (the URL carries its signature)."""
        attempt = 0
        while True:
            attempt += 1
            try:
                resp = self._client.get(url)
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                raise errors.TransportError(f"GET {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _with_retry_after(errors.error_for(resp.status_code, resp.text), resp)
            return resp.content

    @_instrumented("GET")
    def download_to(
        self, url: str, dest: str, *, chunk_size: int = 1 << 20, max_bytes: int | None = None
    ) -> tuple[int, str]:
        """Stream a presigned-URL GET to ``dest``; return ``(size_bytes, sha256_hex)``.
        Sibling of :meth:`get_url` for bytes you do NOT want in memory (model weights): it
        hashes while writing, so a caller verifies against a known ``content_hash`` without
        a second pass. No Authorization header. Idempotent: a blip or retryable status
        restarts from byte 0 (``open`` truncates ``dest``). A partial file remains only when
        retries are exhausted mid-stream; the caller owns cleanup on error."""
        if max_bytes is not None and max_bytes < 0:
            raise ValueError("max_bytes must not be negative")
        attempt = 0
        while True:
            attempt += 1
            try:
                with self._client.stream("GET", url) as resp:
                    if (
                        resp.status_code in _RETRYABLE
                        and attempt <= self.max_retries
                        and self._retry_pause(attempt, resp)
                    ):
                        continue
                    if resp.status_code >= 400:
                        resp.read()  # a streamed response has no .text until read
                        raise _with_retry_after(
                            errors.error_for(resp.status_code, resp.text), resp
                        )
                    hasher = hashlib.sha256()
                    size = 0
                    if max_bytes is not None:
                        declared = resp.headers.get("content-length")
                        if declared is not None and int(declared) > max_bytes:
                            raise ValueError("artifact download exceeds its byte budget")
                    with open(dest, "wb") as fh:
                        for chunk in resp.iter_bytes(chunk_size):
                            if max_bytes is not None and size + len(chunk) > max_bytes:
                                raise ValueError("artifact download exceeds its byte budget")
                            fh.write(chunk)
                            hasher.update(chunk)
                            size += len(chunk)
                return size, hasher.hexdigest()
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                raise errors.TransportError(f"GET {_blob_label(url)}: {exc}") from exc


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
    _INLINE_RETRY_AFTER_MAX,
    _JITTER,
    _PATIENCE_BACKOFF,
    _PATIENCE_LAST_ATTEMPT,
    _TRANSPORT_BACKOFF,
    _announce_patience,
    _patient,
    _request_deadline,
    _retry_after_seconds,
    _with_retry_after,
)
from probe.sdk.delivery.transport.failures import _is_trash_notice, _presigned_put_error  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.headers import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    Attribution,
    _attribution_override,
    _device_headers_for,
    _event_at_header,
    _session_headers,
    _write_origin_header,
    resolve_attribution,
)
from probe.sdk.delivery.transport.tracking import _READ_METHODS, _TRACKING_MEMO_CAP, _is_research_path  # noqa: E402 -- pieces need each other; the front door loads this one first
