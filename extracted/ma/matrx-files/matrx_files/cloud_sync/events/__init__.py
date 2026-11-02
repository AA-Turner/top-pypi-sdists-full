"""File-mutation audit events.

Every meaningful file mutation is recorded to the canonical activity log
(``platform.activity_log`` via the ``platform.log_activity`` RPC).
``default_audit_logger`` is a host-injectable callable hosts wire via
``configure_audit_logger(default_audit_logger)``.

Producers call ``fire_audit_event(event_type, payload)`` after a
successful mutation — it invokes whatever logger the host configured
(aidream wires ``audit_bridge.emit_file_audit_event``) and is a no-op
on standalone installs.

(The legacy ``cld_events`` outbox + ``cld_webhooks`` dispatcher pair was
RETIRED in the 2026 DB canonicalization — the outbox was deprecated,
nothing produced or consumed it, and no subscriber-management surface was
ever shipped. File audit now goes straight to ``platform.activity_log``.)
"""

from __future__ import annotations

from typing import Any

from .default_logger import default_audit_logger, INTERESTING_AUDIT_EVENTS


def fire_audit_event(event_type: str, payload: dict[str, Any]) -> None:
    """Invoke the host-configured audit logger. Never raises.

    The ONE producer entry point: every file-mutation site calls this
    after the mutation succeeds. Payload contract (consumed by
    ``default_audit_logger`` / aidream's ``audit_bridge``):
      resource_id, resource_type, organization_id, user_id (the actor),
      plus any event-specific extras (all land in metadata).
    """
    try:
        from matrx_utils.conf import get_audit_logger

        logger = get_audit_logger()
        if logger is None:
            return
        logger(event_type, payload)
    except Exception:
        # Audit must never break the mutation it describes.
        pass


__all__ = [
    "default_audit_logger",
    "fire_audit_event",
    "INTERESTING_AUDIT_EVENTS",
]
