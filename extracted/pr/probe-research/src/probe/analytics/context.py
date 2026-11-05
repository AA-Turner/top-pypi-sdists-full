"""build the context a detached import worker or an outbox drain reports under, gated on its backend."""

from __future__ import annotations
import os
import re
import uuid
from probe.analytics import core as core
from probe.analytics.analytics import (
    DESKTOP_SURFACE, TelemetryContext, current, is_desktop_launched, null_context,
)
from probe.analytics.generated import ProductSurface
from probe.analytics.outcomes import InvokedBy, Via
from probe.analytics import sender  # call through the module: one binding for tests to patch

#: Set by whoever starts an outbox worker (`probe.sdk.outbox_worker`, drain or rescue): the
#: program that started it, which its events report as (S4). The service sets `service`.
WORKER_SURFACE_ENV = "PROBE_TELEMETRY_SURFACE"


#: Origin fields are validated on the way OUT of the job record, never trusted: the
#: record is a local file that survives upgrades and downgrades.
_ORIGIN_SESSION = re.compile(r"[A-Za-z0-9_-]{1,64}")


def origin_stamp() -> dict | None:
    """Who approved the work about to be persisted, or None when nobody did.

    Goes on the job RECORD, never its `payload`: the payload hash is the job id
    (`import_jobs._identity`), so a session there would defeat the dedup that keeps
    a re-run from importing everything twice.
    """
    context = current()
    if not context.enabled:
        return None
    return {"session_id": context.session_id, "via": str(context.via), "invoked_by": str(context.invoked_by),
            **({"surface": context.surface} if context.surface == DESKTOP_SURFACE else {})}


def job_context(origin: object) -> TelemetryContext:
    """The funnel handle for a detached import worker.

    A new process cannot inherit a context, so the approving `session_id` is replayed
    off the job record: without it "did the approved import finish?" is unanswerable.
    The gate is re-read from the config NOW, so telemetry turned off after approving
    stays off.
    """
    try:
        base_url = core.effective_base_url(core.read_cli_config())
    except Exception:
        base_url = None
    context = TelemetryContext.start(
        via=Via.IMPORT_JOB, interactive=False, base_url=base_url, surface=ProductSurface.CLI
    )
    if not isinstance(origin, dict):
        return context
    session = origin.get("session_id")
    if isinstance(session, str) and _ORIGIN_SESSION.fullmatch(session):
        context.session_id = session
    via = origin.get("via")
    if via in tuple(Via):
        context.via = str(via)
    invoked_by = origin.get("invoked_by")
    if invoked_by in tuple(InvokedBy):
        context.invoked_by = str(invoked_by)
    if origin.get("surface") == DESKTOP_SURFACE:
        context.surface = DESKTOP_SURFACE
    return context


def outbox_context(base_url: str | None, *, surface: ProductSurface) -> TelemetryContext:
    """A context for outbox events, gated on the backend THIS CALLER is using.

    `base_url` is required, never read from the config: the banner may run under
    `probe --base-url` (on `_conn.base_url` only) and the drainer sends to each op's
    PINNED base_url. Fails closed: no backend -> disabled, because `hosted_base_url`
    reads None as "assume hosted". Why: DESIGN.md (outbox_context). `surface`: the caller's
    (the CLI banner's `cli`; a worker's `get_worker_surface()`).
    """
    if not base_url:
        return null_context()
    return TelemetryContext.start(via=Via.OUTBOX, interactive=False, base_url=base_url, surface=surface)


def get_worker_surface() -> ProductSurface:
    """The surface an outbox worker's events report as: `WORKER_SURFACE_ENV` when it names a
    `ProductSurface`, else `sdk`, the original spawner. Outside a worker, `sdk` too."""
    try:
        return ProductSurface(os.environ.get(WORKER_SURFACE_ENV) or ProductSurface.SDK.value)
    except ValueError:
        return ProductSurface.SDK


def detached_context(base_url: str | None, *, via: str, surface: ProductSurface) -> TelemetryContext:
    """`outbox_context`'s gates without becoming THE process's context: sent from a
    daemon thread of any process, whose own session context must stay current."""
    if not base_url:
        return null_context()
    try:
        is_enabled = not core.telemetry_disabled() and core.hosted_base_url(base_url)
    except Exception:
        is_enabled = False
    context = TelemetryContext(
        session_id=uuid.uuid4().hex,
        via=via,
        invoked_by=InvokedBy.AUTOMATION,
        enabled=is_enabled,
        # The app's launch wins here too, as in `TelemetryContext.start` (S4).
        surface=DESKTOP_SURFACE if is_desktop_launched(via) else str(surface),
    )
    if is_enabled:
        try:
            sender._ensure_sender()
        except Exception:
            context.enabled = False
    return context
