"""Smpl Audit SDK runtime namespace.

ADR-047. The audit subsystem records who did what to which resource and
when. The runtime client owns event recording and read-side queries:

* ``client.audit.events.record(..., flush=False)`` — enqueue an audit
  event for asynchronous delivery; pass ``flush=True`` to block until
  the buffer drains.
* ``client.audit.events.flush(timeout=...)`` — drain the buffer.
* ``client.audit.events.list(...)`` / ``client.audit.events.get(id)`` —
  query the audit log.
* ``client.audit.resource_types.list(...)`` and
  ``client.audit.event_types.list(...)`` — distinct-value listings that
  back the Activity tab filter dropdowns.

SIEM forwarder CRUD lives on :class:`smplkit.SmplManagementClient`
under ``mgmt.audit.forwarders.*``. See ``smplkit.management.audit``.

The shared dataclasses (``Event``, ``Forwarder``, ``HttpConfiguration``,
``HttpHeader``, ``ResourceType``, ``EventType``) plus the
``ForwarderType``, ``HttpMethod``, and ``TransformType`` enums live in
:mod:`smplkit.audit.models` and are re-exported here for convenience —
both the runtime and the management clients return them.
"""

from smplkit.audit.client import AsyncAuditClient, AuditClient
from smplkit.audit.models import (
    Event,
    EventType,
    Forwarder,
    ForwarderEnvironment,
    ForwarderType,
    HttpConfiguration,
    HttpHeader,
    HttpMethod,
    ResourceType,
    TransformType,
)

__all__ = [
    "AsyncAuditClient",
    "AuditClient",
    "Event",
    "EventType",
    "Forwarder",
    "ForwarderEnvironment",
    "ForwarderType",
    "HttpConfiguration",
    "HttpHeader",
    "HttpMethod",
    "ResourceType",
    "TransformType",
]
