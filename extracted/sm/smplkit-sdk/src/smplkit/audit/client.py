"""Audit runtime client.

Public surface (runtime):

    client.audit.events.record(event_type, resource_type, resource_id, ..., flush=False)
    client.audit.events.flush(timeout=5.0)
    client.audit.events.list(...)
    client.audit.events.get(event_id)
    client.audit.resource_types.list(...)
    client.audit.event_types.list(filter_resource_type=None, ...)

The runtime audit client owns event recording and read-side queries —
fire-and-forget ``record``, plus the audit-log list/get and the
distinct-value listings that back the Activity tab filter dropdowns.

Management-plane operations (SIEM forwarder CRUD, ``test_forwarder``,
``wipe``) live on :class:`smplkit.SmplManagementClient` under
``mgmt.audit.*``. ADR-047 §2.7.

By default ``record`` enqueues onto an in-memory bounded buffer
(``smplkit.audit._buffer``) and returns immediately; the buffer's
worker thread retries with exponential backoff on transient failures
and drops the oldest item under back pressure. Pass ``flush=True``
when the caller needs the event durable before continuing — typically
in CLI tools, in-test assertions, or any flow about to terminate the
process.

All HTTP work is delegated to the auto-generated low-level client
under ``smplkit._generated.audit`` — the wrapper does not issue raw
HTTP requests.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

import httpx

from smplkit._generated.audit.api.event_types import (
    list_event_types as _gen_list_event_types,
)
from smplkit._generated.audit.api.events import (
    get_event as _gen_get_event,
    list_events as _gen_list_events,
    record_event as _gen_record_event,
)
from smplkit._generated.audit.api.resource_types import (
    list_resource_types as _gen_list_resource_types,
)
from smplkit._errors import Error as _SmplError, _raise_for_status
from smplkit._generated.audit.client import AuthenticatedClient
from smplkit._generated.audit.models.event import Event as _GenEvent
from smplkit._generated.audit.models.event_data import EventData as _GenEventData
from smplkit._generated.audit.models.event_resource import EventResource as _GenEventResource
from smplkit._generated.audit.models.event_response import EventResponse as _GenEventResponse
from smplkit._generated.audit.types import UNSET
from smplkit.audit._buffer import AuditEventBuffer, _PendingEvent
from smplkit.audit.models import Event, EventType, ResourceType

logger = logging.getLogger("smplkit.audit")


def _expect_status(resp: Any, *expected: int) -> None:
    # The generated client raises JSONDecodeError for unparseable 2xx
    # bodies before we see them, so we only need to handle status-code
    # mismatches here. _raise_for_status maps 4xx/5xx to typed errors
    # (NotFoundError, PaymentRequiredError, ValidationError, ConflictError,
    # Error); a 2xx code the caller didn't expect (e.g. 204 vs 200) falls
    # through to the defensive raise below.
    if resp.status_code not in expected:
        _raise_for_status(resp.status_code, resp.content)
        raise _SmplError(
            f"HTTP {resp.status_code} not among expected {expected}",
            status_code=resp.status_code,
        )


def _extract_next_cursor(body_dict: dict[str, Any]) -> str | None:
    next_link = (body_dict.get("links") or {}).get("next")
    if next_link and "page[after]=" in next_link:
        # The link may include other query params after the cursor; the
        # cursor token is base64-url-safe so we slice at the next ``&``.
        after = next_link.split("page[after]=", 1)[1]
        return after.split("&", 1)[0]
    return None


class EventListPage:
    """A single page from ``client.audit.events.list(...)``.

    ``events`` is the page's events; ``next_cursor`` is the opaque token
    for the next page (or None when this is the last page).
    """

    __slots__ = ("events", "next_cursor")

    def __init__(self, *, events: list[Event], next_cursor: str | None) -> None:
        self.events = events
        self.next_cursor = next_cursor

    def __iter__(self):
        return iter(self.events)

    def __len__(self) -> int:
        return len(self.events)


def _extract_pagination(body_dict: dict[str, Any]) -> dict[str, int]:
    """Return the ``meta.pagination`` block from an offset-paginated list."""
    return (body_dict.get("meta") or {}).get("pagination") or {}


class ResourceTypeListPage:
    """A single page from ``client.audit.resource_types.list(...)``.

    ``resource_types`` is the page; ``pagination`` is the response's
    ``meta.pagination`` block (`page`, `size`, and — only when the
    caller passed `meta_total=True` — `total` and `total_pages`).
    """

    __slots__ = ("resource_types", "pagination")

    def __init__(
        self,
        *,
        resource_types: list[ResourceType],
        pagination: dict[str, int],
    ) -> None:
        self.resource_types = resource_types
        self.pagination = pagination

    def __iter__(self):
        return iter(self.resource_types)

    def __len__(self) -> int:
        return len(self.resource_types)


class EventTypeListPage:
    """A single page from ``client.audit.event_types.list(...)``.

    ``event_types`` is the page; ``pagination`` is the response's
    ``meta.pagination`` block (`page`, `size`, and — only when the
    caller passed `meta_total=True` — `total` and `total_pages`).
    """

    __slots__ = ("event_types", "pagination")

    def __init__(
        self,
        *,
        event_types: list[EventType],
        pagination: dict[str, int],
    ) -> None:
        self.event_types = event_types
        self.pagination = pagination

    def __iter__(self):
        return iter(self.event_types)

    def __len__(self) -> int:
        return len(self.event_types)


class _EventsClient:
    """Surface for ``client.audit.events.*``."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client

        def _post(item: _PendingEvent) -> "int | Exception":
            try:
                idem = item.idempotency_key if item.idempotency_key is not None else UNSET
                resp = _gen_record_event.sync_detailed(
                    client=self._auth,
                    body=item.body,
                    idempotency_key=idem,
                )
                return resp.status_code
            except httpx.HTTPError as exc:
                return exc

        self._buffer = AuditEventBuffer(post_fn=_post)

    def record(
        self,
        event_type: str,
        resource_type: str,
        resource_id: str,
        *,
        occurred_at: datetime | None = None,
        actor_type: str | None = None,
        actor_id: str | None = None,
        actor_label: str | None = None,
        data: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        do_not_forward: bool = False,
        flush: bool = False,
        flush_timeout: float | None = 5.0,
    ) -> None:
        """Enqueue an audit event for asynchronous delivery.

        Returns immediately when ``flush`` is False (the default) — the
        buffer's worker thread performs the actual POST with retry on
        transient failures.

        When ``flush=True``, this call blocks until the buffer has
        drained or ``flush_timeout`` elapses. Use this when the caller
        needs the event durable before continuing — typical examples
        are CLI tools, in-test assertions, and any flow about to exit
        the process. The fire-and-forget default remains the right
        choice on the request-handling hot path.

        Args:
            event_type: What happened (e.g. ``"invoice.created"``). Any
                non-empty string.
            resource_type: Kind of resource the event is about (e.g.
                ``"invoice"``). Any non-empty string. Customer events
                must NOT use the ``smpl.`` prefix — that namespace is
                reserved for smplkit-emitted events and the server will
                reject customer attempts with a 403.
            resource_id: Identifier of the affected resource.
            occurred_at: When the event happened in the originating
                system. Defaults to ``now`` server-side if omitted.
            actor_type: Free-form label for the kind of actor that caused
                the event (e.g. ``"USER"``, ``"API_KEY"``, ``"SYSTEM"``,
                or any custom value). The audit service never backfills
                this from the request credential — supply it explicitly
                when you want the event attributed.
            actor_id: Free-form identifier of the actor that caused the
                event. Any string scheme is accepted.
            actor_label: Human-readable label for the actor (e.g. an
                email address or API key name).
            data: Free-form contextual JSON. To record a resource
                snapshot, place it inside ``data`` -- smplkit's internal
                convention nests it at ``data["snapshot"]`` for
                consistency with the platform's own emissions, but the
                shape is unconstrained::

                    record(
                        "invoice.created", "invoice", "inv-1",
                        data={"snapshot": {"total_cents": 4900}, "ip": "1.2.3.4"},
                    )

            idempotency_key: Optional caller-supplied idempotency key.
                If omitted, the server derives one from event content
                (account_id + event_type + resource_type + resource_id +
                occurred_at + actor_* + data).
            do_not_forward: When True, the audit service records the
                event normally but does NOT POST it through any
                configured SIEM forwarder. A
                ``skipped_do_not_forward`` delivery row is recorded for
                each enabled forwarder so the skip is visible in the
                forwarder delivery log.
            flush: When True, block until the buffer drains (or
                ``flush_timeout`` elapses) before returning.
            flush_timeout: Upper bound on the blocking flush, in seconds.
                Ignored when ``flush`` is False. ``None`` blocks
                indefinitely.
        """
        attrs = _GenEvent(
            event_type=event_type,
            resource_type=resource_type,
            resource_id=resource_id,
        )
        if occurred_at is not None:
            attrs.occurred_at = occurred_at.astimezone(timezone.utc)
        if actor_type is not None:
            attrs.actor_type = actor_type
        if actor_id is not None:
            attrs.actor_id = actor_id
        if actor_label is not None:
            attrs.actor_label = actor_label
        if data is not None:
            attrs.data = _GenEventData.from_dict(data)
        if do_not_forward:
            attrs.do_not_forward = True
        body = _GenEventResponse(
            data=_GenEventResource(id="", attributes=attrs),
        )
        self._buffer.enqueue(body, idempotency_key=idempotency_key)
        if flush:
            self._buffer.flush(timeout=flush_timeout)

    def flush(self, timeout: float | None = 5.0) -> None:
        """Block until the in-memory buffer is drained or ``timeout`` elapses.

        Equivalent to passing ``flush=True`` to a final
        :meth:`record` call. Useful for draining buffered events at
        process shutdown or after a batch of fire-and-forget records.
        """
        self._buffer.flush(timeout=timeout)

    def list(
        self,
        *,
        event_type: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        actor_type: str | None = None,
        actor_id: str | None = None,
        occurred_at_range: str | None = None,
        page_size: int | None = None,
        page_after: str | None = None,
    ) -> EventListPage:
        """List audit events for the authenticated account.

        Filters apply server-side. ``actor_id`` is matched as a literal
        string against whatever the recording call stored. Pagination
        uses an opaque cursor (``page_after``); the returned page
        exposes ``next_cursor`` if more pages are available.
        """
        resp = _gen_list_events.sync_detailed(
            client=self._auth,
            filterevent_type=event_type if event_type is not None else UNSET,
            filterresource_type=resource_type if resource_type is not None else UNSET,
            filterresource_id=resource_id if resource_id is not None else UNSET,
            filteractor_type=actor_type if actor_type is not None else UNSET,
            filteractor_id=actor_id if actor_id is not None else UNSET,
            filteroccurred_at=occurred_at_range if occurred_at_range is not None else UNSET,
            pagesize=page_size if page_size is not None else UNSET,
            pageafter=page_after if page_after is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        events = [Event._from_resource(r) for r in body_dict.get("data", [])]
        return EventListPage(events=events, next_cursor=_extract_next_cursor(body_dict))

    def get(self, event_id: UUID | str) -> Event:
        """Retrieve a single audit event by id.

        Raises :class:`NotFoundError` if no event with that id exists in
        the caller's account.
        """
        eid = event_id if isinstance(event_id, UUID) else UUID(str(event_id))
        resp = _gen_get_event.sync_detailed(eid, client=self._auth)
        _expect_status(resp, 200)
        return Event._from_resource(resp.parsed.to_dict()["data"])

    def _close(self) -> None:
        self._buffer.close()


class _ResourceTypesClient:
    """Surface for ``client.audit.resource_types.*``."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> ResourceTypeListPage:
        """List the distinct ``resource_type`` slugs seen in the account.

        Backed by a maintain-by-write side table (ADR-047 §2.5), so the
        response time is independent of how many years of events the
        account has accumulated. Sorted alphabetically; offset paginated
        per ADR-014.
        """
        resp = _gen_list_resource_types.sync_detailed(
            client=self._auth,
            pagenumber=page_number if page_number is not None else UNSET,
            pagesize=page_size if page_size is not None else UNSET,
            metatotal=meta_total if meta_total is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        rows = [ResourceType._from_resource(r) for r in body_dict.get("data", [])]
        return ResourceTypeListPage(
            resource_types=rows,
            pagination=_extract_pagination(body_dict),
        )


class _EventTypesClient:
    """Surface for ``client.audit.event_types.*``."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client

    def list(
        self,
        *,
        filter_resource_type: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> EventTypeListPage:
        """List the distinct ``event_type`` slugs seen in the account.

        Without ``filter_resource_type``, returns one row per distinct
        event_type — an event_type recorded with multiple resource_types
        appears once. With the filter, returns the event_types seen with
        that specific resource_type, powering the cascading-filter
        behavior on the Activity tab.

        ADR-047 §2.5. Sorted alphabetically; offset paginated per
        ADR-014.
        """
        resp = _gen_list_event_types.sync_detailed(
            client=self._auth,
            filterresource_type=(filter_resource_type if filter_resource_type is not None else UNSET),
            pagenumber=page_number if page_number is not None else UNSET,
            pagesize=page_size if page_size is not None else UNSET,
            metatotal=meta_total if meta_total is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        rows = [EventType._from_resource(r) for r in body_dict.get("data", [])]
        return EventTypeListPage(
            event_types=rows,
            pagination=_extract_pagination(body_dict),
        )


class AuditClient:
    """``client.audit.*`` synchronous runtime surface.

    Constructed by :class:`smplkit.SmplClient`; not intended for direct
    instantiation.
    """

    events: _EventsClient
    resource_types: _ResourceTypesClient
    event_types: _EventTypesClient

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        environment: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._environment = environment
        # Runtime audit ops are environment-scoped: record / list / get /
        # discovery all resolve their environment from the
        # ``X-Smplkit-Environment`` request header (ADR-055). We stamp it
        # once at the client level from the SDK's configured runtime
        # environment so every generated call carries it. A caller-supplied
        # ``extra_headers`` entry of the same name wins (explicit override).
        headers: dict[str, str] = {"Accept": "application/vnd.api+json"}
        if environment is not None:
            headers["X-Smplkit-Environment"] = environment
        headers.update(extra_headers or {})
        self._auth = AuthenticatedClient(
            base_url=self._base_url,
            token=api_key,
            timeout=httpx.Timeout(10.0),
            headers=headers,
        )
        self.events = _EventsClient(auth_client=self._auth)
        self.resource_types = _ResourceTypesClient(auth_client=self._auth)
        self.event_types = _EventTypesClient(auth_client=self._auth)

    def _close(self) -> None:
        try:
            self.events._close()
        finally:
            try:
                self._auth.get_httpx_client().close()
            except Exception:  # pragma: no cover — close is best-effort
                pass


class AsyncAuditClient:
    """``client.audit.*`` async runtime surface — currently delegates to
    the sync client.

    Full async support uses ``httpx.AsyncClient`` and an asyncio task
    per pending emit; that work is deferred to a follow-up because the
    primary smpl audit consumers (FastAPI request handlers, Django
    views, framework middleware) are mostly sync code today.
    """

    events: _EventsClient
    resource_types: _ResourceTypesClient
    event_types: _EventTypesClient

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        environment: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self._inner = AuditClient(
            api_key=api_key,
            base_url=base_url,
            environment=environment,
            extra_headers=extra_headers,
        )
        self.events = self._inner.events
        self.resource_types = self._inner.resource_types
        self.event_types = self._inner.event_types

    async def _close(self) -> None:
        self._inner._close()
