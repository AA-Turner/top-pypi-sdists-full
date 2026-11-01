"""RequestHeaders: the headers a request carries -- auth, workspace limits, device, attribution, and the session, origin and event-time scopes."""

from __future__ import annotations
import os
from contextlib import contextmanager
from contextvars import ContextVar
from probe.foundation.compat.compat import StrEnum
from collections.abc import Mapping
from typing import Any

from ....foundation.request_identity.request_identity import device_headers
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
from ....foundation.request_identity.surface import Surface


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


#: Surfaces that genuinely run ON the machine they report. The MCP is excluded on
#: purpose: `_client_for_token` is shared by the local stdio server and the HOSTED one,
#: which memoizes a transport per token for many people, so a fixed device identity
#: would report our pod as every caller's machine (the bug `client_headers_scope` fixed
#: for versions).
#:
#: So an MCP-only report carries no device. The server closes the gap:
#: `current_client_versions` resolves a device-less report through the token's live
#: device bindings when exactly one device holds it, so the plugin's version lands on the
#: right machine, not a second one.
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
