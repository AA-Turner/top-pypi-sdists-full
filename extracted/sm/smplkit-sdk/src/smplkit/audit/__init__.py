"""Smpl Audit SDK namespace.

The audit subsystem records who did what to which resource and when. A
single :class:`AuditClient` (sync) / :class:`AsyncAuditClient` (async)
exposes the full surface and is reachable as ``client.audit`` on
:class:`smplkit.SmplClient` or constructed directly via
:class:`AuditClient`.

The client owns event recording and read-side queries plus SIEM forwarder
CRUD:

* ``audit.events.record(..., flush=False)`` — enqueue an audit event for
  asynchronous delivery; pass ``flush=True`` to block until the buffer drains.
* ``audit.events.flush(timeout=...)`` — drain the buffer.
* ``audit.events.list(...)`` / ``audit.events.get(id)`` — query the audit log.
* ``audit.resource_types.list(...)``, ``audit.event_types.list(...)``, and
  ``audit.categories.list(...)`` — distinct-value listings that back the
  Activity tab filter dropdowns.
* ``audit.forwarders.new/get/list/save/delete`` — manage SIEM forwarders.

The shared dataclasses (``Event``, ``Forwarder``, ``AsyncForwarder``,
``HttpConfiguration``, ``HttpHeader``, ``ResourceType``, ``EventType``,
``Category``) plus the ``ForwarderType``, ``HttpMethod``, and
``TransformType`` enums live in :mod:`smplkit.audit.models` and are
re-exported here for convenience.
"""

from smplkit.audit._client import (
    AsyncCategoriesClient,
    AsyncEventsClient,
    AsyncEventTypesClient,
    AsyncResourceTypesClient,
    CategoriesClient,
    CategoryListPage,
    EventListPage,
    EventsClient,
    EventTypeListPage,
    EventTypesClient,
    ResourceTypeListPage,
    ResourceTypesClient,
)
from smplkit.audit._forwarders import (
    AsyncForwardersClient,
    ForwarderListPage,
    ForwardersClient,
)
from smplkit.audit.models import (
    AsyncForwarder,
    Category,
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
    "AsyncCategoriesClient",
    "AsyncEventTypesClient",
    "AsyncEventsClient",
    "AsyncForwarder",
    "AsyncForwardersClient",
    "AsyncResourceTypesClient",
    "CategoriesClient",
    "Category",
    "CategoryListPage",
    "Event",
    "EventListPage",
    "EventType",
    "EventTypeListPage",
    "EventTypesClient",
    "EventsClient",
    "Forwarder",
    "ForwarderEnvironment",
    "ForwarderListPage",
    "ForwarderType",
    "ForwardersClient",
    "HttpConfiguration",
    "HttpHeader",
    "HttpMethod",
    "ResourceType",
    "ResourceTypeListPage",
    "ResourceTypesClient",
    "TransformType",
]
