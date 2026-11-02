"""Default audit-event logger for matrx-utils file mutations.

Hosts wire this via ``configure_audit_logger(default_audit_logger)``.
Every meaningful file mutation is recorded to the canonical activity log
(``platform.activity_log`` via the ``platform.log_activity`` RPC). The
deprecated ``cld_events`` outbox is gone in the 2026 DB canonicalization,
so the webhook fan-out path it fed has been retired.

For aidream-specific bridging (Sentry breadcrumbs + the existing
``audit_bridge.py``), hosts can wrap this with their own callable that
calls both.
"""

from __future__ import annotations

import asyncio
from typing import Any

from matrx_utils import capture_error, supervised_task, vcprint


# High-signal events that get persisted to platform.activity_log.
# Low-signal events (every read, every URL mint) are deliberately
# skipped so the activity log doesn't saturate.
INTERESTING_AUDIT_EVENTS: frozenset[str] = frozenset({
    "file.uploaded",
    "file.replaced",
    "file.deleted",
    "file.hard_deleted",
    "file.restored",
    "file.renamed",
    "file.moved",
    "file.copied",
    "file.version_bumped",
    "file.published_to_web_changed",
    "file.shown_to_changed",
    "asset.uploaded",
    "asset.variants_added",
    "share_link.created",
    "share_link.revoked",
    "share_link.consumed",
    "permission.granted",
    "permission.revoked",
})


def default_audit_logger(event_type: str, payload: dict[str, Any]) -> None:
    """Persist high-signal file mutations to platform.activity_log.

    Designed for ``matrx_utils.conf.configure_audit_logger(...)``. Never
    raises — failure to persist falls through quietly so a file
    operation doesn't fail just because the audit log is unavailable.

    The dispatch is fire-and-forget — we spawn an asyncio task and
    return immediately. Within the task, exceptions are swallowed and
    logged with ``vcprint``.
    """
    if event_type not in INTERESTING_AUDIT_EVENTS:
        return
    loop = None
    try:
        loop = asyncio.get_event_loop()
        if loop is not None and loop.is_running():
            supervised_task(
                _persist(event_type, payload),
                kind="file_audit_persistence_failed",
                name=f"file-audit:{event_type}",
                context={"event_type": event_type},
            )
        else:
            # Synchronous fallback — run-to-completion. Avoids dropping
            # events in environments where the event loop isn't running
            # yet (eg. host startup).
            asyncio.run(_persist(event_type, payload))
    except Exception as e:
        vcprint(f"[default_audit_logger] dispatch failed: {e!r}", color="yellow")
        if loop.is_running():
            supervised_task(
                capture_error(e, kind="file_audit_dispatch_failed"),
                kind="file_audit_capture_failed",
                name="file-audit-dispatch-capture",
            )


async def _persist(event_type: str, payload: dict[str, Any]) -> None:
    """Write a single audit row to platform.activity_log via the
    log_activity RPC. Best-effort — never raises out.

    Field mapping (cld_events → platform.activity_log):
      event_type   -> action
      resource_type-> entity_type
      resource_id  -> entity_id
      organization_id -> organization_id
      everything else (+ actor + request_id) -> metadata jsonb

    NOTE: the acting user (payload.user_id) is passed as the explicit
    ``p_actor`` (6-arg log_activity overload) so file events match
    owner-scoped webhooks — the base 5-arg overload stamps auth.uid(),
    which is NULL for the service-role key this layer uses. It is also
    mirrored into metadata.actor_id for consumers of the raw payload.
    """
    try:
        # Resolve the active FileManager via the user's wiring. Hosts
        # call ``configure_settings`` + ``configure_context`` before
        # the first file write, so FileManager.get_instance() is
        # already populated.
        from matrx_files import FileManager
        fm = FileManager.get_instance()
        if fm is None or fm.sync_engine is None:
            return
        db = fm.sync_engine.db
        actor_id = payload.get("user_id") or payload.get("actor_id")
        metadata = {
            k: v for k, v in payload.items()
            if k not in (
                "resource_id", "resource_type", "organization_id",
            )
        }
        metadata.setdefault("actor_id", actor_id)
        # activity_log.organization_id is NOT NULL, and the organization it
        # gets is the one the EVENT carries, else the one on the active request
        # context — never an organization picked for the actor. An audit row filed in
        # the wrong tenant is invisible where the action happened and nobody is
        # told (context-is-carried-never-rebuilt.md rule 4).
        org_id = payload.get("organization_id")
        if not org_id:
            from matrx_utils.ctx import get_active_organization_id

            org_id = get_active_organization_id()
        if not org_id:
            vcprint(
                f"[default_audit_logger] dropping {event_type}: the event carries no "
                "organization and the request context carries none either. Emit the "
                "event with organization_id (the file row's own organization), or emit "
                "it inside a context that carries one — an audit row is never filed in "
                "the actor's personal organization.",
                color="yellow",
            )
            return
        # 6-arg platform.log_activity overload, positional:
        # (p_org, p_action, p_entity_type, p_entity_id, p_metadata, p_actor).
        await db._rpc(
            "platform",
            "log_activity",
            org_id,
            event_type,
            payload.get("resource_type"),
            payload.get("resource_id"),
            metadata,
            actor_id,
            mode="none",
        )
    except Exception as e:
        vcprint(
            f"[default_audit_logger] log_activity failed: {e!r}", color="yellow"
        )


__all__ = ["default_audit_logger", "INTERESTING_AUDIT_EVENTS"]
