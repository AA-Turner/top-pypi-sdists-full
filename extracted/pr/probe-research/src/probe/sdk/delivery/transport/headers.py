"""RequestHeaders: the headers a request carries -- auth, workspace limits, device, attribution, and the session, origin and event-time scopes."""

from __future__ import annotations

from collections.abc import Mapping
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import hmac
import os
from typing import Any

from probe.foundation.compat.compat import StrEnum
from probe.sdk import errors, routes, session_marker
from probe.sdk.settings import workspace_limit as _workspace_limit
from probe.sdk.settings.settings import DAEMON_SHELL_CONFIG

from ....foundation.request_identity.request_identity import device_headers
from ....foundation.request_identity.surface import Surface
from ...agent_session import (
    AGENT_HEADER,
    AGENT_SESSION_HEADER,
    EVENT_AT_ENV,
    EVENT_AT_HEADER,
    RUN_WRITE_ORIGIN,
    WRITE_ORIGIN_HEADER,
    agent_session_headers,
    recorded_session_headers,
    run_write_origin)


class Attribution(StrEnum):
    AMBIENT = "ambient"
    BACKFILL = "backfill"


_attribution_override: ContextVar[Attribution | None] = ContextVar(
    "probe_request_attribution", default=None
)


def resolve_attribution(value: str | None = None) -> Attribution:
    """An explicit client choice, also inherited by wizard subprocesses."""
    return Attribution(
        value if value is not None else os.environ.get("PROBE_ATTRIBUTION", Attribution.AMBIENT)
    )


@contextmanager
def attribution_scope(value: str):
    """Persisted outbox attribution, isolated between concurrent transports."""
    token = _attribution_override.set(Attribution(value))
    try:
        yield
    finally:
        _attribution_override.reset(token)


_event_at: ContextVar[str | None] = ContextVar("probe_request_event_at", default=None)


@contextmanager
def event_at_scope(value: str | None):
    """Date every request in this block at ``value`` (ISO 8601; see
    `agent_session.EVENT_AT_HEADER`). None leaves the enclosing date in force."""
    if not value:
        yield
        return
    token = _event_at.set(str(value))
    try:
        yield
    finally:
        _event_at.reset(token)


#: No `queued_session_scope` in force: this process's own agent session.
_OWN_SESSION = object()
_queued_session: ContextVar[Any] = ContextVar("probe_queued_session", default=_OWN_SESSION)


@contextmanager
def queued_session_scope(recorded: str | None):
    """Send every request in this block as the agent session an outbox op
    recorded (`agent_session.queued_session`), or as none when it recorded
    none: the drainer delivers another writer's op as that writer's."""
    token = _queued_session.set(recorded)
    try:
        yield
    finally:
        _queued_session.reset(token)


def _session_headers() -> dict[str, str]:
    recorded = _queued_session.get()
    return agent_session_headers() if recorded is _OWN_SESSION else recorded_session_headers(recorded)


def _event_at_header() -> dict[str, str]:
    value = _event_at.get() or os.environ.get(EVENT_AT_ENV, "").strip()
    return {EVENT_AT_HEADER: value[:64]} if value else {}


#: No `queued_origin_scope` in force: this process's own (`run_write_origin`).
_OWN_ORIGIN = object()
_queued_origin: ContextVar[Any] = ContextVar("probe_queued_origin", default=_OWN_ORIGIN)


@contextmanager
def queued_origin_scope(recorded: str | None):
    """Send every request in this block with the write origin an outbox op
    recorded (`agent_session.run_write_origin`), or with none: the drainer
    delivers a run's queued write as the run's, and never lends its own."""
    token = _queued_origin.set(recorded)
    try:
        yield
    finally:
        _queued_origin.reset(token)


def _write_origin_header(session: Mapping[str, str]) -> dict[str, str]:
    """`WRITE_ORIGIN_HEADER` for a request sent as the session `session`'s
    headers name (R41): a run process's write says so."""
    recorded = _queued_origin.get()
    if recorded is _OWN_ORIGIN:
        recorded = run_write_origin(f"{session.get(AGENT_HEADER)}:{session.get(AGENT_SESSION_HEADER)}")
    return {WRITE_ORIGIN_HEADER: RUN_WRITE_ORIGIN} if recorded == RUN_WRITE_ORIGIN else {}


#: Surfaces that run ON the machine they report. Not the MCP: the hosted one shares a transport per
#: token across people, so a device identity would name our pod as every caller's machine.
_DEVICE_REPORTING_SURFACES = frozenset({Surface.CLI.value, Surface.SDK.value})


def _device_headers_for(surface: str) -> dict[str, str]:
    """The machine header for a transport on THIS host, or nothing. Fail-quiet: a machine
    whose identity file cannot be read or written reports as a client predating device
    identity (supported), not an error worth failing a research write."""
    if surface not in _DEVICE_REPORTING_SURFACES:
        return {}
    try:
        from ...settings.device_identity import device_instance_id

        return device_headers(device_instance_id())
    except Exception:  # noqa: BLE001 - identity is telemetry, never a hard failure
        return {}


class RequestHeadersMixin:
    """Part of Transport: its methods run with `self` the Transport; fold_parts() copies them into Transport."""

    # -- auth ---------------------------------------------------------------
    def _auth_headers(self, path: str, raw_body: bytes) -> dict[str, str]:
        headers: dict[str, str] = {}
        if routes.is_public(path):
            # Public reads (Probe's docs) carry no credential: needed most when sign-in
            # broke, and a token there would be ignored.
            return headers
        is_ingest = routes.is_ingest(path)
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
                    f"no API token configured ({session_marker.SIGN_IN_HINT}, or set "
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
