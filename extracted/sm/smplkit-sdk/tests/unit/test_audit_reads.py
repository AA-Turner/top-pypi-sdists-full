"""Tests for the audit runtime read surfaces — ``client.audit.events.list``,
``client.audit.events.get``, ``client.audit.resource_types.list``, and
``client.audit.event_types.list``.

The fire-and-forget ``record`` path is covered in ``test_audit.py`` and
``test_audit_coverage.py``; this file covers the synchronous read
endpoints colocated on the runtime audit client.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

import httpx
import pytest

from smplkit import Error, NotFoundError
from smplkit.audit import Event, EventType, ResourceType
from smplkit.audit.client import (
    AsyncAuditClient,
    AuditClient,
    EventListPage,
    EventTypeListPage,
    ResourceTypeListPage,
)


def _client_with_handler(handler) -> AuditClient:
    client = AuditClient(api_key="sk_api_test", base_url="https://audit.example.com")
    client._auth.set_httpx_client(
        httpx.Client(
            transport=httpx.MockTransport(handler),
            base_url="https://audit.example.com",
        )
    )
    return client


def _event_resource(event_id: str = "11111111-2222-3333-4444-555555555555") -> dict:
    return {
        "id": event_id,
        "type": "event",
        "attributes": {
            "event_type": "user.created",
            "resource_type": "user",
            "resource_id": "u-1",
            "occurred_at": "2026-05-06T12:00:00+00:00",
            "created_at": "2026-05-06T12:00:01+00:00",
            "actor_type": "API_KEY",
            "actor_id": None,
            "actor_label": "",
            "data": {},
            "idempotency_key": "k",
        },
    }


def _resource_type_resource(*, key: str, created_at: str = "2026-04-12T15:23:01Z") -> dict[str, Any]:
    return {
        "id": key,
        "type": "resource_type",
        "attributes": {"resource_type": key, "created_at": created_at},
    }


def _event_type_resource(*, key: str, created_at: str = "2026-04-12T15:23:01Z") -> dict[str, Any]:
    return {
        "id": key,
        "type": "event_type",
        "attributes": {"event_type": key, "created_at": created_at},
    }


# ---------------------------------------------------------------------------
# events.list
# ---------------------------------------------------------------------------


class TestEventsList:
    def test_threads_filter_and_pagination_params(self):
        seen_urls: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            seen_urls.append(str(req.url))
            return httpx.Response(
                200,
                json={"data": [], "links": {}, "meta": {"page_size": 50}},
            )

        client = _client_with_handler(handler)
        try:
            client.events.list(
                event_type="user.created",
                resource_type="user",
                resource_id="u-1",
                actor_type="USER",
                actor_id=UUID("11111111-2222-3333-4444-555555555555"),
                occurred_at_range="[2026-04-01T00:00:00Z,*)",
                page_size=25,
                page_after="abc",
            )
            u = seen_urls[0]
            for needle in [
                "filter%5Bevent_type%5D=user.created",
                "filter%5Bresource_type%5D=user",
                "filter%5Bresource_id%5D=u-1",
                "filter%5Bactor_type%5D=USER",
                "filter%5Boccurred_at%5D=",
                "page%5Bsize%5D=25",
                "page%5Bafter%5D=abc",
            ]:
                assert needle in u
        finally:
            client._close()

    def test_paginates(self):
        pages = [
            {
                "data": [_event_resource("11111111-1111-1111-1111-111111111111")],
                "links": {"next": "/api/v1/events?page[size]=1&page[after]=tok-2"},
                "meta": {"page_size": 1},
            },
            {
                "data": [_event_resource("22222222-2222-2222-2222-222222222222")],
                "meta": {"page_size": 1},
            },
        ]
        call_count = [0]

        def handler(req):
            page = pages[call_count[0]]
            call_count[0] += 1
            return httpx.Response(200, json=page)

        client = _client_with_handler(handler)
        try:
            first = client.events.list(page_size=1)
            assert len(first.events) == 1
            assert first.next_cursor == "tok-2"
            second = client.events.list(page_size=1, page_after=first.next_cursor)
            assert len(second.events) == 1
            assert second.next_cursor is None
        finally:
            client._close()

    def test_5xx_raises_generic_error(self):
        client = _client_with_handler(lambda req: httpx.Response(503, json={}))
        try:
            with pytest.raises(Error):
                client.events.list()
        finally:
            client._close()

    def test_event_list_page_iter_and_len(self):
        client = _client_with_handler(
            lambda req: httpx.Response(
                200,
                json={"data": [_event_resource()], "meta": {"page_size": 1}},
            )
        )
        try:
            page = client.events.list()
            assert isinstance(page, EventListPage)
            assert len(page) == 1
            assert [e.id for e in page] == [UUID("11111111-2222-3333-4444-555555555555")]
        finally:
            client._close()


# ---------------------------------------------------------------------------
# events.get
# ---------------------------------------------------------------------------


class TestEventsGet:
    def test_round_trips(self):
        event_id = UUID("11111111-2222-3333-4444-555555555555")

        def handler(req: httpx.Request) -> httpx.Response:
            assert str(event_id) in req.url.path
            return httpx.Response(200, json={"data": _event_resource(str(event_id))})

        client = _client_with_handler(handler)
        try:
            ev = client.events.get(event_id)
            assert ev.id == event_id
            assert ev.event_type == "user.created"
        finally:
            client._close()

    def test_get_accepts_string_id(self):
        event_id = "11111111-2222-3333-4444-555555555555"
        client = _client_with_handler(lambda req: httpx.Response(200, json={"data": _event_resource(event_id)}))
        try:
            ev = client.events.get(event_id)
            assert ev.id == UUID(event_id)
        finally:
            client._close()

    def test_404_raises_not_found(self):
        client = _client_with_handler(lambda req: httpx.Response(404, json={}))
        try:
            with pytest.raises(NotFoundError):
                client.events.get(UUID("00000000-0000-0000-0000-000000000099"))
        finally:
            client._close()

    def test_event_model_round_trips_z_suffix_timestamps(self):
        # Defensive: the Event model accepts trailing-Z timestamps that
        # JS clients commonly produce.
        ev = Event._from_resource(
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "type": "event",
                "attributes": {
                    "event_type": "x",
                    "resource_type": "y",
                    "resource_id": "z",
                    "occurred_at": "2026-05-06T12:00:00Z",
                    "created_at": "2026-05-06T12:00:01Z",
                    "actor_type": "API_KEY",
                    "actor_label": "",
                },
            }
        )
        assert ev.occurred_at.tzinfo is not None


# ---------------------------------------------------------------------------
# resource_types.list
# ---------------------------------------------------------------------------


class TestResourceTypesList:
    def test_returns_sorted_rows(self):
        def handler(req: httpx.Request) -> httpx.Response:
            assert req.method == "GET"
            assert "/api/v1/resource_types" in str(req.url)
            return httpx.Response(
                200,
                json={
                    "data": [
                        _resource_type_resource(key="account"),
                        _resource_type_resource(key="user"),
                    ],
                    "meta": {"pagination": {"page": 1, "size": 1000}},
                },
            )

        c = _client_with_handler(handler)
        try:
            page = c.resource_types.list()
            assert isinstance(page, ResourceTypeListPage)
            assert len(page) == 2
            assert [r.id for r in page] == ["account", "user"]
            assert page.pagination == {"page": 1, "size": 1000}
        finally:
            c._close()

    def test_pagination_params_propagate(self):
        captured: list[str] = []

        def handler(req):
            captured.append(str(req.url))
            return httpx.Response(
                200,
                json={
                    "data": [_resource_type_resource(key="alpha")],
                    "meta": {"pagination": {"page": 2, "size": 1, "total": 3, "total_pages": 3}},
                },
            )

        c = _client_with_handler(handler)
        try:
            page = c.resource_types.list(page_size=1, page_number=2, meta_total=True)
            url = captured[0]
            assert "page%5Bsize%5D=1" in url or "page[size]=1" in url
            assert "page%5Bnumber%5D=2" in url or "page[number]=2" in url
            assert "meta%5Btotal%5D=true" in url or "meta[total]=true" in url
            assert page.pagination == {"page": 2, "size": 1, "total": 3, "total_pages": 3}
        finally:
            c._close()

    def test_empty_response(self):
        def handler(req):
            return httpx.Response(
                200,
                json={"data": [], "meta": {"pagination": {"page": 1, "size": 1000}}},
            )

        c = _client_with_handler(handler)
        try:
            page = c.resource_types.list()
            assert len(page) == 0
            assert page.pagination == {"page": 1, "size": 1000}
            assert list(page) == []
        finally:
            c._close()

    def test_5xx_raises_generic_error(self):
        def handler(req):
            return httpx.Response(500, json={"errors": [{"status": "500"}]})

        c = _client_with_handler(handler)
        try:
            with pytest.raises(Error):
                c.resource_types.list()
        finally:
            c._close()

    def test_unexpected_2xx_status_raises_error(self):
        # Defensive: a 2xx code the caller didn't expect (e.g. 204 when
        # 200 was expected) also surfaces as a generic Error.
        def handler(req):
            return httpx.Response(204)

        c = _client_with_handler(handler)
        try:
            with pytest.raises(Error):
                c.resource_types.list()
        finally:
            c._close()


# ---------------------------------------------------------------------------
# event_types.list
# ---------------------------------------------------------------------------


class TestEventTypesList:
    def test_unfiltered(self):
        def handler(req):
            url = str(req.url)
            assert "/api/v1/event_types" in url
            assert "filter%5Bresource_type%5D" not in url
            assert "filter[resource_type]" not in url
            return httpx.Response(
                200,
                json={
                    "data": [
                        _event_type_resource(key="account.updated"),
                        _event_type_resource(key="user.login"),
                    ],
                    "meta": {"pagination": {"page": 1, "size": 1000}},
                },
            )

        c = _client_with_handler(handler)
        try:
            page = c.event_types.list()
            assert isinstance(page, EventTypeListPage)
            assert [a.id for a in page] == ["account.updated", "user.login"]
        finally:
            c._close()

    def test_filter_by_resource_type(self):
        captured_url: list[str] = []

        def handler(req):
            captured_url.append(str(req.url))
            return httpx.Response(
                200,
                json={
                    "data": [_event_type_resource(key="user.login")],
                    "meta": {"pagination": {"page": 1, "size": 1000}},
                },
            )

        c = _client_with_handler(handler)
        try:
            page = c.event_types.list(filter_resource_type="user")
            url = captured_url[0]
            assert "filter%5Bresource_type%5D=user" in url or "filter[resource_type]=user" in url
            assert [a.id for a in page] == ["user.login"]
        finally:
            c._close()

    def test_pagination_params_propagate_with_filter(self):
        captured: list[str] = []

        def handler(req):
            captured.append(str(req.url))
            return httpx.Response(
                200,
                json={
                    "data": [_event_type_resource(key="a.x")],
                    "meta": {"pagination": {"page": 2, "size": 1, "total": 5, "total_pages": 5}},
                },
            )

        c = _client_with_handler(handler)
        try:
            page = c.event_types.list(
                page_size=1,
                page_number=2,
                meta_total=True,
                filter_resource_type="user",
            )
            url = captured[0]
            assert "page%5Bnumber%5D=2" in url or "page[number]=2" in url
            assert "filter%5Bresource_type%5D=user" in url or "filter[resource_type]=user" in url
            assert page.pagination["total"] == 5
        finally:
            c._close()

    def test_empty_response(self):
        def handler(req):
            return httpx.Response(
                200,
                json={"data": [], "meta": {"pagination": {"page": 1, "size": 1000}}},
            )

        c = _client_with_handler(handler)
        try:
            page = c.event_types.list()
            assert page.pagination == {"page": 1, "size": 1000}
        finally:
            c._close()

    def test_event_type_list_page_len_and_iter(self):
        # Direct __len__ check — coverage gate requires every wrapper line.
        page = EventTypeListPage(
            event_types=[
                EventType._from_resource(_event_type_resource(key="a.x")),
                EventType._from_resource(_event_type_resource(key="b.y")),
            ],
            pagination={"page": 1, "size": 2},
        )
        assert len(page) == 2
        assert [a.id for a in page] == ["a.x", "b.y"]


# ---------------------------------------------------------------------------
# Models — fallback paths
# ---------------------------------------------------------------------------


class TestModels:
    def test_resource_type_falls_back_to_id_when_attribute_missing(self):
        # Defensive: if the server ever omits ``attributes.resource_type``
        # the wrapper still surfaces the ``id`` so callers don't see
        # ``None`` — JSON:API guarantees ``id`` is always present.
        body = {
            "id": "smpl.flag",
            "attributes": {"created_at": "2026-04-12T15:23:01Z"},
        }
        rt = ResourceType._from_resource(body)
        assert rt.resource_type == "smpl.flag"

    def test_event_type_falls_back_to_id_when_attribute_missing(self):
        body = {"id": "x.y", "attributes": {"created_at": "2026-04-12T15:23:01Z"}}
        a = EventType._from_resource(body)
        assert a.event_type == "x.y"


# ---------------------------------------------------------------------------
# AsyncAuditClient surface
# ---------------------------------------------------------------------------


def test_async_client_exposes_read_namespaces():
    """The runtime ``AsyncAuditClient`` mirrors the sync one — the same
    events / resource_types / event_types surfaces must reach async callers."""
    client = AsyncAuditClient(api_key="sk_api_test", base_url="https://audit.example.com")
    try:
        assert client.events is not None
        assert client.resource_types is not None
        assert client.event_types is not None
    finally:
        import asyncio

        asyncio.run(client._close())
