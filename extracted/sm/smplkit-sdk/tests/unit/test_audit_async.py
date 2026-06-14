"""Tests for the genuinely-async audit client (``AsyncAuditClient``).

After the audit runtime/management unification the async client is no longer
a sync delegate: reads, discovery, and forwarder CRUD perform real awaited
round-trips (``asyncio_detailed``); only ``events.record`` stays
fire-and-forget. These tests drive every async path through an
``httpx.MockTransport`` async client and cover the transport-resolution and
close branches that the sync tests don't reach.
"""

from __future__ import annotations

import asyncio
from uuid import UUID

import httpx
import pytest

from smplkit import Error, NotFoundError
from smplkit._generated.audit.client import AuthenticatedClient as _AuditAuthClient
from smplkit.audit import AsyncForwarder, ForwarderType, HttpConfiguration
from smplkit.audit.clients import AsyncAuditClient

BASE = "https://audit.example.com"
EVENT_ID = "11111111-2222-3333-4444-555555555555"
FWD_ID = "datadog-prod"


def _event_resource(event_id: str = EVENT_ID) -> dict:
    return {
        "id": event_id,
        "type": "event",
        "attributes": {
            "event_type": "invoice.created",
            "resource_type": "invoice",
            "resource_id": "inv-1",
            "occurred_at": "2026-05-06T12:00:00+00:00",
            "created_at": "2026-05-06T12:00:01+00:00",
            "actor_type": "API_KEY",
            "actor_id": None,
            "actor_label": "",
            "category": "billing",
            "data": {},
            "idempotency_key": "k",
            "environment": "production",
        },
    }


def _disc_resource(type_: str, key: str) -> dict:
    attr = {"created_at": "2026-04-12T15:23:01Z"}
    attr[{"resource_type": "resource_type", "event_type": "event_type", "category": "category"}[type_]] = key
    return {"id": key, "type": type_, "attributes": attr}


def _forwarder_resource(*, id_: str = FWD_ID, version: int = 1) -> dict:
    return {
        "id": id_,
        "type": "forwarder",
        "attributes": {
            "name": "Datadog production",
            "forwarder_type": "datadog",
            "enabled": False,
            "forward_smplkit_events": False,
            "environments": {},
            "description": None,
            "filter": None,
            "transform": None,
            "transform_type": None,
            "configuration": {
                "method": "POST",
                "url": "https://siem.example.com/in",
                "headers": [{"name": "DD-API-KEY", "value": "dd-api-key-plaintext"}],
                "success_status": "2xx",
            },
            "created_at": "2026-05-07T12:00:00+00:00",
            "updated_at": "2026-05-07T12:00:00+00:00",
            "deleted_at": None,
            "version": version,
        },
    }


_DISCOVERY_META = {"meta": {"pagination": {"page": 1, "size": 1000}}}


def _handler(req: httpx.Request) -> httpx.Response:
    m, path = req.method, req.url.path
    if path == "/api/v1/events" and m == "POST":
        return httpx.Response(201, json={"data": _event_resource()})
    if path == "/api/v1/events" and m == "GET":
        return httpx.Response(200, json={"data": [_event_resource()], "links": {}, "meta": {"page_size": 50}})
    if path.startswith("/api/v1/events/") and m == "GET":
        return httpx.Response(200, json={"data": _event_resource()})
    if path == "/api/v1/resource_types":
        return httpx.Response(200, json={"data": [_disc_resource("resource_type", "invoice")], **_DISCOVERY_META})
    if path == "/api/v1/event_types":
        return httpx.Response(200, json={"data": [_disc_resource("event_type", "invoice.created")], **_DISCOVERY_META})
    if path == "/api/v1/categories":
        return httpx.Response(200, json={"data": [_disc_resource("category", "billing")], **_DISCOVERY_META})
    if path == "/api/v1/forwarders" and m == "POST":
        return httpx.Response(201, json={"data": _forwarder_resource()})
    if path == "/api/v1/forwarders" and m == "GET":
        return httpx.Response(
            200, json={"data": [_forwarder_resource()], "meta": {"pagination": {"page": 1, "size": 1000}}}
        )
    if path.startswith("/api/v1/forwarders/") and m == "GET":
        return httpx.Response(200, json={"data": _forwarder_resource()})
    if path.startswith("/api/v1/forwarders/") and m == "PUT":
        return httpx.Response(200, json={"data": _forwarder_resource(version=2)})
    if path.startswith("/api/v1/forwarders/") and m == "DELETE":
        return httpx.Response(204)
    raise AssertionError(f"unexpected {m} {path}")


def _async_client(handler=_handler) -> AsyncAuditClient:
    auth = _AuditAuthClient(base_url=BASE, token="sk_api_test", headers={"Accept": "application/vnd.api+json"})
    auth.set_async_httpx_client(httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url=BASE))
    return AsyncAuditClient(auth_client=auth)


class TestAsyncEvents:
    def test_record_fire_and_forget_then_flush(self):
        async def _run():
            c = _async_client()
            # Fire-and-forget: returns without awaiting a round-trip.
            await c.events.record("invoice.created", "invoice", "inv-1", category="billing")
            # flush drains off the loop (executor) without blocking it.
            await c.events.flush(timeout=2.0)

        asyncio.run(_run())

    def test_record_with_flush_true(self):
        async def _run():
            c = _async_client()
            await c.events.record("invoice.created", "invoice", "inv-1", flush=True, flush_timeout=2.0)

        asyncio.run(_run())

    def test_list_and_get(self):
        async def _run():
            c = _async_client()
            page = await c.events.list(resource_type="invoice", environments=["production", "smplkit"])
            assert [e.resource_id for e in page.events] == ["inv-1"]
            assert page.events[0].category == "billing"
            ev = await c.events.get(EVENT_ID)
            assert ev.id == UUID(EVENT_ID)
            ev2 = await c.events.get(UUID(EVENT_ID))
            assert ev2.event_type == "invoice.created"

        asyncio.run(_run())

    def test_list_search_filter_threaded(self):
        seen: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            seen.append(str(req.url))
            return httpx.Response(200, json={"data": [], "links": {}, "meta": {"page_size": 50}})

        async def _run():
            c = _async_client(handler)
            await c.events.list(search="inv-42")
            assert "filter%5Bsearch%5D=inv-42" in seen[0]
            # Omitted → the param is left off the wire entirely.
            await c.events.list()
            assert "filter%5Bsearch%5D" not in seen[1]

        asyncio.run(_run())

    def test_get_404_raises(self):
        async def _run():
            c = _async_client(lambda req: httpx.Response(404, json={}))
            with pytest.raises(NotFoundError):
                await c.events.get(EVENT_ID)

        asyncio.run(_run())


class TestAsyncDiscovery:
    def test_resource_types_event_types_categories(self):
        async def _run():
            c = _async_client()
            assert [r.id for r in await c.resource_types.list()] == ["invoice"]
            assert [e.id for e in await c.event_types.list(filter_resource_type="invoice")] == ["invoice.created"]
            assert [cat.id for cat in await c.categories.list(environments=["smplkit"])] == ["billing"]

        asyncio.run(_run())

    def test_discovery_5xx_raises(self):
        async def _run():
            c = _async_client(lambda req: httpx.Response(503, json={}))
            with pytest.raises(Error):
                await c.resource_types.list()

        asyncio.run(_run())


class TestAsyncForwarders:
    def test_new_save_creates_then_updates(self):
        async def _run():
            c = _async_client()
            fwd = c.forwarders.new(
                FWD_ID,
                forwarder_type=ForwarderType.DATADOG,
                configuration=HttpConfiguration(url="https://siem.example.com/in"),
            )
            assert isinstance(fwd, AsyncForwarder)
            assert fwd.created_at is None
            await fwd.save()  # create
            assert fwd.created_at is not None and fwd.version == 1
            await fwd.save()  # update (created_at now set)
            assert fwd.version == 2

        asyncio.run(_run())

    def test_get_list_delete(self):
        async def _run():
            c = _async_client()
            got = await c.forwarders.get(FWD_ID)
            assert isinstance(got, AsyncForwarder) and got.id == FWD_ID
            page = await c.forwarders.list(forwarder_type=ForwarderType.DATADOG, meta_total=True)
            assert [f.id for f in page] == [FWD_ID]
            await c.forwarders.delete(FWD_ID)
            await got.delete()  # active-record delete

        asyncio.run(_run())

    def test_delete_non_204_raises(self):
        async def _run():
            c = _async_client(lambda req: httpx.Response(500, json={"errors": [{"status": "500"}]}))
            with pytest.raises(Error):
                await c.forwarders.delete(FWD_ID)

        asyncio.run(_run())

    def test_delete_unexpected_2xx_raises(self):
        # A non-204 success still surfaces the defensive Error (covers the
        # ``raise _SmplError`` after ``_raise_for_status`` returns without raising).
        async def _run():
            c = _async_client(lambda req: httpx.Response(200, json={}))
            with pytest.raises(Error):
                await c.forwarders.delete(FWD_ID)

        asyncio.run(_run())

    def test_update_requires_id(self):
        async def _run():
            c = _async_client()
            fwd = c.forwarders.new(
                "x", forwarder_type=ForwarderType.HTTP, configuration=HttpConfiguration(url="https://x")
            )
            fwd.id = ""  # force the update-guard
            with pytest.raises(ValueError):
                await c.forwarders._update(fwd)

        asyncio.run(_run())

    def test_create_requires_id(self):
        async def _run():
            c = _async_client()
            fwd = c.forwarders.new(
                "x", forwarder_type=ForwarderType.HTTP, configuration=HttpConfiguration(url="https://x")
            )
            fwd.id = ""  # force the create-guard
            with pytest.raises(ValueError):
                await c.forwarders._create(fwd)

        asyncio.run(_run())

    def test_async_forwarder_unsaved_guards(self):
        async def _run():
            fwd = AsyncForwarder(
                None,
                id="x",
                name="x",
                forwarder_type=ForwarderType.HTTP,
                configuration=HttpConfiguration(url="https://x"),
            )
            with pytest.raises(RuntimeError):
                await fwd.save()
            with pytest.raises(RuntimeError):
                await fwd.delete()

        asyncio.run(_run())


class TestAsyncConstructionAndClose:
    def test_standalone_resolves_transport_without_base_url(self):
        # No base_url -> _audit_transport takes the resolve branch.
        c = AsyncAuditClient(api_key="sk_test", base_domain="example.com", scheme="https", environment="staging")
        assert c._owns_transport is True
        # Environment routes through the body / filter[environment], not a header.
        assert "X-Smplkit-Environment" not in c._auth._headers
        assert c._environment == "staging"
        assert "audit.example.com" in str(c._auth._base_url)

    def test_owned_async_transport_closed(self):
        async def _run():
            c = AsyncAuditClient(api_key="sk_test", base_url=BASE)
            c._auth.set_async_httpx_client(httpx.AsyncClient(transport=httpx.MockTransport(_handler), base_url=BASE))
            await c.resource_types.list()
            await c.aclose()
            assert c._auth._async_client is None
            await c.aclose()  # idempotent

        asyncio.run(_run())

    def test_borrowed_async_transport_not_closed(self):
        async def _run():
            auth = _AuditAuthClient(base_url=BASE, token="sk_test")
            auth.set_async_httpx_client(httpx.AsyncClient(transport=httpx.MockTransport(_handler), base_url=BASE))
            c = AsyncAuditClient(auth_client=auth)
            assert c._owns_transport is False
            await c.aclose()  # borrowed: must not close
            assert auth._async_client is not None

        asyncio.run(_run())

    def test_async_context_manager(self):
        async def _run():
            async with AsyncAuditClient(api_key="sk_test", base_url=BASE) as c:
                assert isinstance(c, AsyncAuditClient)

        asyncio.run(_run())
