"""The Smpl Audit client.

Audit installs no in-process machinery, so a single client exposes the
full surface: one :class:`AuditClient` (sync) / :class:`AsyncAuditClient`
(async), reachable as ``client.audit`` or standalone:

    audit.events.record(event_type, resource_type, resource_id, ..., flush=False)
    audit.events.flush(timeout=5.0)
    audit.events.list(...)
    audit.events.get(event_id)
    audit.resource_types.list(...)
    audit.event_types.list(filter_resource_type=None, ...)
    audit.categories.list(...)
    audit.forwarders.new/get/list/save/delete(...)

The async client is genuinely async: reads, discovery, and forwarder CRUD
perform their network round-trips with ``await``. Only ``events.record`` is
fire-and-forget (it enqueues onto a background worker thread and returns
without awaiting), which is the correct shape for the hot path.

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

import asyncio
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import UUID

import httpx

from smplkit._config import _service_url, resolve_client_config

from smplkit._generated.audit.api.categories import (
    list_categories as _gen_list_categories,
)
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
from smplkit.audit.models import Category, Event, EventType, ResourceType

if TYPE_CHECKING:  # pragma: no cover
    from smplkit.audit._forwarders import AsyncForwardersClient, ForwardersClient

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


def _join_environments(environments: list[str] | None) -> str | Any:
    """Comma-join an ``environments`` filter list for ``filter[environment]``.

    Returns ``UNSET`` when the caller passes ``None`` or an empty list so
    the query param is omitted entirely (preserving the pre-filter wire
    shape). When non-empty, the values are joined with ``,`` to form the
    comma-separated set the audit read endpoints expect — each value is a
    real environment key or the reserved ``"smplkit"`` control-plane
    bucket.
    """
    if not environments:
        return UNSET
    return ",".join(environments)


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


class CategoryListPage:
    """A single page from ``client.audit.categories.list(...)``.

    ``categories`` is the page; ``pagination`` is the response's
    ``meta.pagination`` block (`page`, `size`, and — only when the
    caller passed `meta_total=True` — `total` and `total_pages`).
    """

    __slots__ = ("categories", "pagination")

    def __init__(
        self,
        *,
        categories: list[Category],
        pagination: dict[str, int],
    ) -> None:
        self.categories = categories
        self.pagination = pagination

    def __iter__(self):
        return iter(self.categories)

    def __len__(self) -> int:
        return len(self.categories)


def _audit_transport(
    *,
    api_key: str | None,
    base_url: str | None,
    environment: str | None,
    profile: str | None,
    base_domain: str | None,
    scheme: str | None,
    debug: bool | None,
    extra_headers: dict[str, str] | None,
) -> AuthenticatedClient:
    """Build a standalone audit transport from resolved config.

    ``base_url``/``api_key`` are used directly when both are supplied (the
    path a top-level client takes after it has already resolved them);
    otherwise the config resolver fills in whatever is missing
    (``~/.smplkit`` / env vars / defaults). ``environment`` is optional —
    when present it is stamped as ``X-Smplkit-Environment`` so event
    recording and reads scope to it server-side (ADR-055); when absent the
    client still works (forwarder CRUD and discovery are environment-agnostic,
    and reads accept an explicit ``environments=[...]`` filter).
    """
    if api_key is None or base_url is None:
        cfg = resolve_client_config(
            profile=profile,
            api_key=api_key,
            base_domain=base_domain,
            scheme=scheme,
            debug=debug,
        )
        api_key = api_key if api_key is not None else cfg.api_key
        base_url = base_url if base_url is not None else _service_url(cfg.scheme, "audit", cfg.base_domain)
        cfg_extra = cfg.extra_headers
    else:
        cfg_extra = None
    headers: dict[str, str] = {"Accept": "application/vnd.api+json"}
    if environment is not None:
        headers["X-Smplkit-Environment"] = environment
    headers.update(cfg_extra or {})
    headers.update(extra_headers or {})
    return AuthenticatedClient(
        base_url=base_url.rstrip("/"),
        token=api_key,
        timeout=httpx.Timeout(10.0),
        headers=headers,
    )


def _build_record_body(
    event_type: str,
    resource_type: str,
    resource_id: str,
    *,
    occurred_at: datetime | None,
    actor_type: str | None,
    actor_id: str | None,
    actor_label: str | None,
    category: str | None,
    data: dict[str, Any] | None,
    do_not_forward: bool,
) -> _GenEventResponse:
    """Build the generated event-record request body (shared sync/async)."""
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
    if category is not None:
        attrs.category = category
    if data is not None:
        attrs.data = _GenEventData.from_dict(data)
    if do_not_forward:
        attrs.do_not_forward = True
    return _GenEventResponse(data=_GenEventResource(id="", attributes=attrs))


def _record_post_fn(auth: AuthenticatedClient):
    """Build the buffer ``post_fn`` that POSTs a pending event synchronously.

    The audit event buffer drains on a background worker thread, so the POST
    is synchronous even for the async client — it runs off the event loop and
    never blocks it.
    """

    def _post(item: _PendingEvent) -> "int | Exception":
        try:
            idem = item.idempotency_key if item.idempotency_key is not None else UNSET
            resp = _gen_record_event.sync_detailed(
                client=auth,
                body=item.body,
                idempotency_key=idem,
            )
            return resp.status_code
        except httpx.HTTPError as exc:
            return exc

    return _post


class EventsClient:
    """Surface for ``client.audit.events.*`` (sync)."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client
        self._buffer = AuditEventBuffer(post_fn=_record_post_fn(auth_client))

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
        category: str | None = None,
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
            category: Optional free-form bucket label for the event (e.g.
                ``"auth"``, ``"billing"``, ``"config-change"``). Stored
                exactly as supplied; powers the audit log's category
                filter and the ``categories`` discovery listing
                (:meth:`AuditClient.categories`). Omit it to leave the
                event uncategorized.
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
        body = _build_record_body(
            event_type,
            resource_type,
            resource_id,
            occurred_at=occurred_at,
            actor_type=actor_type,
            actor_id=actor_id,
            actor_label=actor_label,
            category=category,
            data=data,
            do_not_forward=do_not_forward,
        )
        self._buffer.enqueue(body, idempotency_key=idempotency_key)
        if flush:
            self._buffer.flush(timeout=flush_timeout)

    def flush(self, timeout: float | None = 5.0) -> None:
        """Block until the in-memory buffer is drained or ``timeout`` elapses.

        Equivalent to passing ``flush=True`` to a final
        :meth:`record` call. Useful for draining buffered events at
        process shutdown or after a batch of fire-and-forget records.

        Args:
            timeout: Upper bound on the blocking flush, in seconds.
                ``None`` blocks indefinitely. Defaults to ``5.0``.
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
        search: str | None = None,
        environments: list[str] | None = None,
        page_size: int | None = None,
        page_after: str | None = None,
    ) -> EventListPage:
        """List audit events for the authenticated account.

        Filters apply server-side. ``actor_id`` is matched as a literal
        string against whatever the recording call stored. Pagination
        uses an opaque cursor (``page_after``); the returned page
        exposes ``next_cursor`` if more pages are available.

        ``search`` is an optional free-text filter: pass a string to
        return only events whose ``resource_id`` or ``description``
        contains it as a case-insensitive substring; omit it (the
        default) to disable text filtering. A ``search`` filter must be
        scoped — combine it with ``occurred_at_range``, or with both
        ``resource_type`` and ``resource_id`` — or the request is
        rejected.

        ``environments`` scopes the read to a set of environments: pass
        a list of environment keys and/or the reserved ``"smplkit"``
        control-plane bucket; the values are sent comma-separated as
        ``filter[environment]``. Omit it (the default) to leave the
        param off entirely and let environment scope fall back to the
        ``X-Smplkit-Environment`` request header.

        Args:
            event_type: Return only events with this ``event_type``. Omit
                to match any.
            resource_type: Return only events about this ``resource_type``.
                Omit to match any.
            resource_id: Return only events about this resource id. Omit
                to match any.
            actor_type: Return only events whose ``actor_type`` equals this
                value. Omit to match any.
            actor_id: Return only events whose ``actor_id`` matches this
                value as a literal string. Omit to match any.
            occurred_at_range: Restrict to events whose ``occurred_at``
                falls in this range. Omit to leave the time window open.
            search: Optional free-text filter — returns only events whose
                ``resource_id`` or ``description`` contains it as a
                case-insensitive substring. Must be scoped (combine with
                ``occurred_at_range``, or with both ``resource_type`` and
                ``resource_id``) or the request is rejected. Omit to
                disable text filtering.
            environments: Environment keys and/or the reserved
                ``"smplkit"`` control-plane bucket to scope the read to.
                Omit to leave the filter off entirely.
            page_size: Maximum number of events to return in this page.
            page_after: Opaque cursor from a previous page's
                ``next_cursor``. Omit for the first page.

        Returns:
            An :class:`EventListPage` of the matching events; its
            ``next_cursor`` is set when more pages are available.
        """
        resp = _gen_list_events.sync_detailed(
            client=self._auth,
            filterevent_type=event_type if event_type is not None else UNSET,
            filterresource_type=resource_type if resource_type is not None else UNSET,
            filterresource_id=resource_id if resource_id is not None else UNSET,
            filteractor_type=actor_type if actor_type is not None else UNSET,
            filteractor_id=actor_id if actor_id is not None else UNSET,
            filteroccurred_at=occurred_at_range if occurred_at_range is not None else UNSET,
            filtersearch=search if search is not None else UNSET,
            filterenvironment=_join_environments(environments),
            pagesize=page_size if page_size is not None else UNSET,
            pageafter=page_after if page_after is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        events = [Event._from_resource(r) for r in body_dict.get("data", [])]
        return EventListPage(events=events, next_cursor=_extract_next_cursor(body_dict))

    def get(self, event_id: UUID | str) -> Event:
        """Retrieve a single audit event by id.

        Args:
            event_id: The event's UUID, as a :class:`uuid.UUID` or a
                string parseable as one.

        Returns:
            The matching :class:`Event`.

        Raises:
            NotFoundError: If no event with that id exists in the
                caller's account.
        """
        eid = event_id if isinstance(event_id, UUID) else UUID(str(event_id))
        resp = _gen_get_event.sync_detailed(eid, client=self._auth)
        _expect_status(resp, 200)
        return Event._from_resource(resp.parsed.to_dict()["data"])

    def _close(self) -> None:
        self._buffer.close()


class ResourceTypesClient:
    """Surface for ``client.audit.resource_types.*``."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client

    def list(
        self,
        *,
        environments: list[str] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> ResourceTypeListPage:
        """List the distinct ``resource_type`` slugs seen in the account.

        Response time is independent of how many years of events the
        account has accumulated. Sorted alphabetically; offset paginated.

        ``environments`` scopes the listing to a set of environments:
        pass a list of environment keys and/or the reserved ``"smplkit"``
        control-plane bucket; the values are sent comma-separated as
        ``filter[environment]``. Omit it (the default) to leave the
        param off entirely.

        Args:
            environments: Environment keys and/or the reserved
                ``"smplkit"`` control-plane bucket to scope the listing
                to. Omit to leave the filter off entirely.
            page_number: 1-based page index. Omit for the first page.
            page_size: Maximum number of slugs to return in this page.
            meta_total: When ``True``, populate ``total`` and
                ``total_pages`` in the returned page's ``pagination``
                dict (costs an extra count server-side). Omit to skip it.

        Returns:
            A :class:`ResourceTypeListPage` of the matching resource-type
            slugs.
        """
        resp = _gen_list_resource_types.sync_detailed(
            client=self._auth,
            filterenvironment=_join_environments(environments),
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


class EventTypesClient:
    """Surface for ``client.audit.event_types.*``."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client

    def list(
        self,
        *,
        filter_resource_type: str | None = None,
        environments: list[str] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> EventTypeListPage:
        """List the distinct ``event_type`` slugs seen in the account.

        Without ``filter_resource_type``, returns one row per distinct
        event_type — an event_type recorded with multiple resource_types
        appears once. With the filter, returns the event_types seen with
        that specific resource_type, which supports building a cascading
        resource-type-then-event-type filter.

        ``environments`` scopes the listing to a set of environments:
        pass a list of environment keys and/or the reserved ``"smplkit"``
        control-plane bucket; the values are sent comma-separated as
        ``filter[environment]``. Omit it (the default) to leave the
        param off entirely.

        Sorted alphabetically; offset paginated.

        Args:
            filter_resource_type: Restrict the listing to event_types seen
                with this ``resource_type``. Omit to list every distinct
                event_type.
            environments: Environment keys and/or the reserved
                ``"smplkit"`` control-plane bucket to scope the listing
                to. Omit to leave the filter off entirely.
            page_number: 1-based page index. Omit for the first page.
            page_size: Maximum number of slugs to return in this page.
            meta_total: When ``True``, populate ``total`` and
                ``total_pages`` in the returned page's ``pagination``
                dict (costs an extra count server-side). Omit to skip it.

        Returns:
            An :class:`EventTypeListPage` of the matching event-type
            slugs.
        """
        resp = _gen_list_event_types.sync_detailed(
            client=self._auth,
            filterresource_type=(filter_resource_type if filter_resource_type is not None else UNSET),
            filterenvironment=_join_environments(environments),
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


class CategoriesClient:
    """Surface for ``client.audit.categories.*``."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client

    def list(
        self,
        *,
        environments: list[str] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> CategoryListPage:
        """List the distinct ``category`` values seen in the account.

        Response time is independent of how many years of events the
        account has accumulated. Sorted alphabetically; offset paginated.

        ``environments`` scopes the listing to a set of environments:
        pass a list of environment keys and/or the reserved ``"smplkit"``
        control-plane bucket; the values are sent comma-separated as
        ``filter[environment]``. Omit it (the default) to leave the
        param off entirely.

        Args:
            environments: Environment keys and/or the reserved
                ``"smplkit"`` control-plane bucket to scope the listing
                to. Omit to leave the filter off entirely.
            page_number: 1-based page index. Omit for the first page.
            page_size: Maximum number of categories to return in this page.
            meta_total: When ``True``, populate ``total`` and
                ``total_pages`` in the returned page's ``pagination``
                dict (costs an extra count server-side). Omit to skip it.

        Returns:
            A :class:`CategoryListPage` of the matching category values.
        """
        resp = _gen_list_categories.sync_detailed(
            client=self._auth,
            filterenvironment=_join_environments(environments),
            pagenumber=page_number if page_number is not None else UNSET,
            pagesize=page_size if page_size is not None else UNSET,
            metatotal=meta_total if meta_total is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        rows = [Category._from_resource(r) for r in body_dict.get("data", [])]
        return CategoryListPage(
            categories=rows,
            pagination=_extract_pagination(body_dict),
        )


class AsyncEventsClient:
    """Surface for ``client.audit.events.*`` (async)."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client
        self._buffer = AuditEventBuffer(post_fn=_record_post_fn(auth_client))

    async def record(
        self,
        event_type: str,
        resource_type: str,
        resource_id: str,
        *,
        occurred_at: datetime | None = None,
        actor_type: str | None = None,
        actor_id: str | None = None,
        actor_label: str | None = None,
        category: str | None = None,
        data: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        do_not_forward: bool = False,
        flush: bool = False,
        flush_timeout: float | None = 5.0,
    ) -> None:
        """Enqueue an audit event for asynchronous delivery.

        Fire-and-forget: the event is appended to an in-memory buffer drained
        by a background worker thread, so this returns without awaiting any
        network round-trip — nothing blocks the event loop. When
        ``flush=True`` the buffer drain is awaited off the loop (run in a
        thread executor) so it stays loop-safe.

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
            category: Optional free-form bucket label for the event (e.g.
                ``"auth"``, ``"billing"``, ``"config-change"``). Stored
                exactly as supplied; powers the audit log's category
                filter and the ``categories`` discovery listing. Omit it
                to leave the event uncategorized.
            data: Free-form contextual JSON. To record a resource
                snapshot, place it inside ``data`` — smplkit's own
                convention nests it at ``data["snapshot"]`` for
                consistency, but the shape is unconstrained.
            idempotency_key: Optional caller-supplied idempotency key. If
                omitted, the server derives one from event content
                (account_id + event_type + resource_type + resource_id +
                occurred_at + actor_* + data).
            do_not_forward: When ``True``, the audit service records the
                event normally but does NOT POST it through any configured
                SIEM forwarder. A ``skipped_do_not_forward`` delivery row
                is recorded for each enabled forwarder so the skip is
                visible in the forwarder delivery log.
            flush: When ``True``, await the buffer drain (or until
                ``flush_timeout`` elapses) before returning.
            flush_timeout: Upper bound on the awaited flush, in seconds.
                Ignored when ``flush`` is ``False``. ``None`` waits
                indefinitely. Defaults to ``5.0``.
        """
        body = _build_record_body(
            event_type,
            resource_type,
            resource_id,
            occurred_at=occurred_at,
            actor_type=actor_type,
            actor_id=actor_id,
            actor_label=actor_label,
            category=category,
            data=data,
            do_not_forward=do_not_forward,
        )
        self._buffer.enqueue(body, idempotency_key=idempotency_key)
        if flush:
            await self.flush(timeout=flush_timeout)

    async def flush(self, timeout: float | None = 5.0) -> None:
        """Drain the in-memory buffer, awaited off the event loop.

        Use this to drain buffered events at process shutdown or after a
        batch of fire-and-forget records. The drain runs in a thread
        executor so it never blocks the event loop.

        Args:
            timeout: Upper bound on the awaited drain, in seconds. ``None``
                waits indefinitely. Defaults to ``5.0``.
        """
        await asyncio.get_running_loop().run_in_executor(None, self._buffer.flush, timeout)

    async def list(
        self,
        *,
        event_type: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        actor_type: str | None = None,
        actor_id: str | None = None,
        occurred_at_range: str | None = None,
        search: str | None = None,
        environments: list[str] | None = None,
        page_size: int | None = None,
        page_after: str | None = None,
    ) -> EventListPage:
        """List audit events for the authenticated account, awaited.

        Filters apply server-side. ``actor_id`` is matched as a literal
        string against whatever the recording call stored. Pagination
        uses an opaque cursor (``page_after``); the returned page
        exposes ``next_cursor`` if more pages are available.

        ``search`` is an optional free-text filter: pass a string to
        return only events whose ``resource_id`` or ``description``
        contains it as a case-insensitive substring; omit it (the
        default) to disable text filtering. A ``search`` filter must be
        scoped — combine it with ``occurred_at_range``, or with both
        ``resource_type`` and ``resource_id`` — or the request is
        rejected.

        ``environments`` scopes the read to a set of environments: pass
        a list of environment keys and/or the reserved ``"smplkit"``
        control-plane bucket; the values are sent comma-separated as
        ``filter[environment]``. Omit it (the default) to leave the
        param off entirely and let environment scope fall back to the
        ``X-Smplkit-Environment`` request header.

        Args:
            event_type: Return only events with this ``event_type``. Omit
                to match any.
            resource_type: Return only events about this ``resource_type``.
                Omit to match any.
            resource_id: Return only events about this resource id. Omit
                to match any.
            actor_type: Return only events whose ``actor_type`` equals this
                value. Omit to match any.
            actor_id: Return only events whose ``actor_id`` matches this
                value as a literal string. Omit to match any.
            occurred_at_range: Restrict to events whose ``occurred_at``
                falls in this range. Omit to leave the time window open.
            search: Optional free-text filter — returns only events whose
                ``resource_id`` or ``description`` contains it as a
                case-insensitive substring. Must be scoped (combine with
                ``occurred_at_range``, or with both ``resource_type`` and
                ``resource_id``) or the request is rejected. Omit to
                disable text filtering.
            environments: Environment keys and/or the reserved
                ``"smplkit"`` control-plane bucket to scope the read to.
                Omit to leave the filter off entirely.
            page_size: Maximum number of events to return in this page.
            page_after: Opaque cursor from a previous page's
                ``next_cursor``. Omit for the first page.

        Returns:
            An :class:`EventListPage` of the matching events; its
            ``next_cursor`` is set when more pages are available.
        """
        resp = await _gen_list_events.asyncio_detailed(
            client=self._auth,
            filterevent_type=event_type if event_type is not None else UNSET,
            filterresource_type=resource_type if resource_type is not None else UNSET,
            filterresource_id=resource_id if resource_id is not None else UNSET,
            filteractor_type=actor_type if actor_type is not None else UNSET,
            filteractor_id=actor_id if actor_id is not None else UNSET,
            filteroccurred_at=occurred_at_range if occurred_at_range is not None else UNSET,
            filtersearch=search if search is not None else UNSET,
            filterenvironment=_join_environments(environments),
            pagesize=page_size if page_size is not None else UNSET,
            pageafter=page_after if page_after is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        events = [Event._from_resource(r) for r in body_dict.get("data", [])]
        return EventListPage(events=events, next_cursor=_extract_next_cursor(body_dict))

    async def get(self, event_id: UUID | str) -> Event:
        """Retrieve a single audit event by id, awaited.

        Args:
            event_id: The event's UUID, as a :class:`uuid.UUID` or a
                string parseable as one.

        Returns:
            The matching :class:`Event`.

        Raises:
            NotFoundError: If no event with that id exists in the
                caller's account.
        """
        eid = event_id if isinstance(event_id, UUID) else UUID(str(event_id))
        resp = await _gen_get_event.asyncio_detailed(eid, client=self._auth)
        _expect_status(resp, 200)
        return Event._from_resource(resp.parsed.to_dict()["data"])

    def _close(self) -> None:
        self._buffer.close()


class AsyncResourceTypesClient:
    """Surface for ``client.audit.resource_types.*`` (async)."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client

    async def list(
        self,
        *,
        environments: list[str] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> ResourceTypeListPage:
        """List the distinct ``resource_type`` slugs seen in the account, awaited.

        Response time is independent of how many years of events the
        account has accumulated. Sorted alphabetically; offset paginated.

        ``environments`` scopes the listing to a set of environments:
        pass a list of environment keys and/or the reserved ``"smplkit"``
        control-plane bucket; the values are sent comma-separated as
        ``filter[environment]``. Omit it (the default) to leave the
        param off entirely.

        Args:
            environments: Environment keys and/or the reserved
                ``"smplkit"`` control-plane bucket to scope the listing
                to. Omit to leave the filter off entirely.
            page_number: 1-based page index. Omit for the first page.
            page_size: Maximum number of slugs to return in this page.
            meta_total: When ``True``, populate ``total`` and
                ``total_pages`` in the returned page's ``pagination``
                dict (costs an extra count server-side). Omit to skip it.

        Returns:
            A :class:`ResourceTypeListPage` of the matching resource-type
            slugs.
        """
        resp = await _gen_list_resource_types.asyncio_detailed(
            client=self._auth,
            filterenvironment=_join_environments(environments),
            pagenumber=page_number if page_number is not None else UNSET,
            pagesize=page_size if page_size is not None else UNSET,
            metatotal=meta_total if meta_total is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        rows = [ResourceType._from_resource(r) for r in body_dict.get("data", [])]
        return ResourceTypeListPage(resource_types=rows, pagination=_extract_pagination(body_dict))


class AsyncEventTypesClient:
    """Surface for ``client.audit.event_types.*`` (async)."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client

    async def list(
        self,
        *,
        filter_resource_type: str | None = None,
        environments: list[str] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> EventTypeListPage:
        """List the distinct ``event_type`` slugs seen in the account, awaited.

        Without ``filter_resource_type``, returns one row per distinct
        event_type — an event_type recorded with multiple resource_types
        appears once. With the filter, returns the event_types seen with
        that specific resource_type, which supports building a cascading
        resource-type-then-event-type filter.

        ``environments`` scopes the listing to a set of environments:
        pass a list of environment keys and/or the reserved ``"smplkit"``
        control-plane bucket; the values are sent comma-separated as
        ``filter[environment]``. Omit it (the default) to leave the
        param off entirely.

        Sorted alphabetically; offset paginated.

        Args:
            filter_resource_type: Restrict the listing to event_types seen
                with this ``resource_type``. Omit to list every distinct
                event_type.
            environments: Environment keys and/or the reserved
                ``"smplkit"`` control-plane bucket to scope the listing
                to. Omit to leave the filter off entirely.
            page_number: 1-based page index. Omit for the first page.
            page_size: Maximum number of slugs to return in this page.
            meta_total: When ``True``, populate ``total`` and
                ``total_pages`` in the returned page's ``pagination``
                dict (costs an extra count server-side). Omit to skip it.

        Returns:
            An :class:`EventTypeListPage` of the matching event-type
            slugs.
        """
        resp = await _gen_list_event_types.asyncio_detailed(
            client=self._auth,
            filterresource_type=(filter_resource_type if filter_resource_type is not None else UNSET),
            filterenvironment=_join_environments(environments),
            pagenumber=page_number if page_number is not None else UNSET,
            pagesize=page_size if page_size is not None else UNSET,
            metatotal=meta_total if meta_total is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        rows = [EventType._from_resource(r) for r in body_dict.get("data", [])]
        return EventTypeListPage(event_types=rows, pagination=_extract_pagination(body_dict))


class AsyncCategoriesClient:
    """Surface for ``client.audit.categories.*`` (async)."""

    def __init__(self, *, auth_client: AuthenticatedClient) -> None:
        self._auth = auth_client

    async def list(
        self,
        *,
        environments: list[str] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> CategoryListPage:
        """List the distinct ``category`` values seen in the account, awaited.

        Response time is independent of how many years of events the
        account has accumulated. Sorted alphabetically; offset paginated.

        ``environments`` scopes the listing to a set of environments:
        pass a list of environment keys and/or the reserved ``"smplkit"``
        control-plane bucket; the values are sent comma-separated as
        ``filter[environment]``. Omit it (the default) to leave the
        param off entirely.

        Args:
            environments: Environment keys and/or the reserved
                ``"smplkit"`` control-plane bucket to scope the listing
                to. Omit to leave the filter off entirely.
            page_number: 1-based page index. Omit for the first page.
            page_size: Maximum number of categories to return in this page.
            meta_total: When ``True``, populate ``total`` and
                ``total_pages`` in the returned page's ``pagination``
                dict (costs an extra count server-side). Omit to skip it.

        Returns:
            A :class:`CategoryListPage` of the matching category values.
        """
        resp = await _gen_list_categories.asyncio_detailed(
            client=self._auth,
            filterenvironment=_join_environments(environments),
            pagenumber=page_number if page_number is not None else UNSET,
            pagesize=page_size if page_size is not None else UNSET,
            metatotal=meta_total if meta_total is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        rows = [Category._from_resource(r) for r in body_dict.get("data", [])]
        return CategoryListPage(categories=rows, pagination=_extract_pagination(body_dict))


class AuditClient:
    """The Smpl Audit client (sync).

    Audit installs no in-process machinery, so a single client exposes the
    full surface — event recording and reads, distinct-value discovery, and
    SIEM forwarder CRUD — reachable as ``client.audit``
    (:class:`smplkit.SmplClient`) or constructed directly::

        from smplkit import AuditClient

        with AuditClient(environment="production") as audit:
            audit.events.record("invoice.created", "invoice", "inv-1", flush=True)
            for ft in audit.forwarders.list():
                ...

    Namespaces: ``events`` (record/flush/list/get), ``resource_types``,
    ``event_types``, ``categories`` (discovery), and ``forwarders`` (CRUD).

    Args:
        api_key: API key. When omitted, resolved from ``SMPLKIT_API_KEY`` or
            ``~/.smplkit``.
        environment: Deployment environment to scope recording and reads to,
            sent as ``X-Smplkit-Environment``. Optional — forwarder CRUD and
            discovery are environment-agnostic, and reads accept an explicit
            ``environments=[...]`` filter. When reached via ``SmplClient`` this
            is the SDK's configured runtime environment; on a standalone client
            without it, recording falls back to the server-side default
            environment.
        profile: Named ``~/.smplkit`` profile section.
        base_url: Full audit-service base URL. Usually resolved from
            ``base_domain``/``scheme``; supplied directly by the top-level
            clients which have already computed it.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable SDK debug logging.
        extra_headers: Extra headers attached to every request. An
            ``X-Smplkit-Environment`` entry here wins over ``environment``.
        auth_client: Internal — a pre-built transport supplied by a top-level
            client so the audit surface shares one connection pool. Not for
            direct use.
    """

    events: EventsClient
    resource_types: ResourceTypesClient
    event_types: EventTypesClient
    categories: CategoriesClient
    forwarders: ForwardersClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        environment: str | None = None,
        base_url: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
        auth_client: AuthenticatedClient | None = None,
    ) -> None:
        self._environment = environment
        if auth_client is not None:
            self._auth = auth_client
            self._owns_transport = False
        else:
            self._auth = _audit_transport(
                api_key=api_key,
                base_url=base_url,
                environment=environment,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._owns_transport = True
        # Lazy import breaks the cycle: smplkit.audit._forwarders imports the
        # shared audit dataclasses from smplkit.audit.models, which is loaded
        # before this client module.
        from smplkit.audit._forwarders import ForwardersClient

        self.events = EventsClient(auth_client=self._auth)
        self.resource_types = ResourceTypesClient(auth_client=self._auth)
        self.event_types = EventTypesClient(auth_client=self._auth)
        self.categories = CategoriesClient(auth_client=self._auth)
        self.forwarders = ForwardersClient(auth_client=self._auth)

    def _close(self) -> None:
        try:
            self.events._close()
        finally:
            if self._owns_transport:
                try:
                    self._auth.get_httpx_client().close()
                except Exception:  # pragma: no cover — close is best-effort
                    pass

    def close(self) -> None:
        """Release HTTP resources — only when this client owns its transport."""
        self._close()

    def __enter__(self) -> "AuditClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncAuditClient:
    """The Smpl Audit client (async) — counterpart of :class:`AuditClient`.

    Genuinely async: event reads, discovery, and forwarder CRUD perform their
    network round-trips with ``await``; only ``events.record`` is
    fire-and-forget (it enqueues onto a background worker thread and returns
    without awaiting), which is the correct shape for the hot path.
    """

    events: AsyncEventsClient
    resource_types: AsyncResourceTypesClient
    event_types: AsyncEventTypesClient
    categories: AsyncCategoriesClient
    forwarders: AsyncForwardersClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        environment: str | None = None,
        base_url: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
        auth_client: AuthenticatedClient | None = None,
    ) -> None:
        self._environment = environment
        if auth_client is not None:
            self._auth = auth_client
            self._owns_transport = False
        else:
            self._auth = _audit_transport(
                api_key=api_key,
                base_url=base_url,
                environment=environment,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._owns_transport = True
        from smplkit.audit._forwarders import AsyncForwardersClient

        self.events = AsyncEventsClient(auth_client=self._auth)
        self.resource_types = AsyncResourceTypesClient(auth_client=self._auth)
        self.event_types = AsyncEventTypesClient(auth_client=self._auth)
        self.categories = AsyncCategoriesClient(auth_client=self._auth)
        self.forwarders = AsyncForwardersClient(auth_client=self._auth)

    async def _close(self) -> None:
        try:
            self.events._close()
        finally:
            if self._owns_transport:
                ac = self._auth._async_client
                if ac is not None:
                    await ac.aclose()
                    self._auth._async_client = None

    async def aclose(self) -> None:
        """Release async HTTP resources — only when this client owns its transport."""
        await self._close()

    async def __aenter__(self) -> "AsyncAuditClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()


# The events / resource_types / event_types / categories sub-clients are
# reached through ``client.audit.<name>``; present them as
# ``smplkit.audit.<Name>`` in IDE hover / help() rather than the private
# ``smplkit.audit._client`` path.
EventsClient.__module__ = "smplkit.audit"
AsyncEventsClient.__module__ = "smplkit.audit"
ResourceTypesClient.__module__ = "smplkit.audit"
AsyncResourceTypesClient.__module__ = "smplkit.audit"
EventTypesClient.__module__ = "smplkit.audit"
AsyncEventTypesClient.__module__ = "smplkit.audit"
CategoriesClient.__module__ = "smplkit.audit"
AsyncCategoriesClient.__module__ = "smplkit.audit"
