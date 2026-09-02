"""Pen CRUD on both clients, mocked at the httpx transport layer via respx."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
import respx

from conftest import TEST_BASE_URL
from hogland import AsyncHogland, ConflictError, Hogland, Pen


def make_client() -> Hogland:
    return Hogland(token="t", base_url=TEST_BASE_URL)


def pen_json(name: str = "pr-1234", **overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "id": "pen-abc123def456",
        "owner_id": "user-1",
        "name": name,
        "created_at": "2026-06-12T00:00:00Z",
        "updated_at": "2026-06-12T00:00:00Z",
    }
    base.update(overrides)
    return base


@respx.mock
def test_create_pen_sends_body() -> None:
    route = respx.post(f"{TEST_BASE_URL}/v1/pens").mock(
        return_value=httpx.Response(
            201,
            json=pen_json(
                on_idle="hibernate",
                wake="on-request",
                metadata={"pr": "1234", "repo": "posthog/posthog"},
            ),
        ),
    )
    client = make_client()
    pen = client.create_pen(
        "pr-1234",
        on_idle="hibernate",
        wake="on-request",
        spec={"kind": "preview", "web_port": 8000},
        metadata={"pr": "1234", "repo": "posthog/posthog"},
    )
    assert isinstance(pen, Pen)
    assert pen.id == "pen-abc123def456"
    assert pen.metadata == {"pr": "1234", "repo": "posthog/posthog"}

    sent = json.loads(route.calls.last.request.content)
    assert sent["name"] == "pr-1234"
    assert sent["on_idle"] == "hibernate"
    assert sent["spec"]["web_port"] == 8000
    assert sent["metadata"]["repo"] == "posthog/posthog"


@respx.mock
def test_create_pen_conflict_raises() -> None:
    respx.post(f"{TEST_BASE_URL}/v1/pens").mock(
        return_value=httpx.Response(
            409,
            json={"title": "Conflict", "status": 409, "detail": "pen already exists"},
        ),
    )
    with pytest.raises(ConflictError):
        make_client().create_pen("pr-1234")


@respx.mock
def test_get_and_list_pens() -> None:
    respx.get(f"{TEST_BASE_URL}/v1/pens/pr-1234").mock(
        return_value=httpx.Response(200, json=pen_json()),
    )
    respx.get(f"{TEST_BASE_URL}/v1/pens").mock(
        return_value=httpx.Response(200, json={"items": [pen_json(), pen_json(name="other")]}),
    )
    client = make_client()
    assert client.get_pen("pr-1234").name == "pr-1234"
    page = client.list_pens()
    assert [p.name for p in page.items] == ["pr-1234", "other"]


@respx.mock
def test_update_pen_sends_only_passed_fields() -> None:
    route = respx.patch(f"{TEST_BASE_URL}/v1/pens/pr-1234").mock(
        return_value=httpx.Response(200, json=pen_json(latest_snapshot_id="snap-9")),
    )
    client = make_client()
    # Explicit empty string clears the box pointer; untouched fields
    # must be absent from the body (pointer-typed server patch).
    pen = client.update_pen("pr-1234", current_box_id="", latest_snapshot_id="snap-9")
    assert pen.latest_snapshot_id == "snap-9"

    sent = json.loads(route.calls.last.request.content)
    assert sent == {"current_box_id": "", "latest_snapshot_id": "snap-9"}


@respx.mock
def test_update_pen_metadata_clear_sends_empty_map() -> None:
    route = respx.patch(f"{TEST_BASE_URL}/v1/pens/pr-1234").mock(
        return_value=httpx.Response(200, json=pen_json()),
    )
    make_client().update_pen("pr-1234", metadata={})
    sent = json.loads(route.calls.last.request.content)
    assert sent == {"metadata": {}}


def test_update_pen_no_fields_raises() -> None:
    with pytest.raises(ValueError, match="at least one field"):
        make_client().update_pen("pr-1234")


def test_update_pen_explicit_none_raises() -> None:
    # None is ambiguous (a JSON null reads as "absent" to the server's
    # pointer-typed patch) — the builder rejects it and points at the
    # correct spelling instead of silently doing nothing.
    with pytest.raises(ValueError, match="current_box_id=None is ambiguous"):
        make_client().update_pen("pr-1234", current_box_id=None)  # ty: ignore[invalid-argument-type]
    with pytest.raises(ValueError, match="metadata=None is ambiguous"):
        make_client().update_pen("pr-1234", metadata=None)  # ty: ignore[invalid-argument-type]


@respx.mock
def test_delete_pen() -> None:
    route = respx.delete(f"{TEST_BASE_URL}/v1/pens/pr-1234").mock(
        return_value=httpx.Response(204),
    )
    make_client().delete_pen("pr-1234")
    assert route.called


@respx.mock
def test_delete_pen_expected_current_box_id() -> None:
    route = respx.delete(
        f"{TEST_BASE_URL}/v1/pens/pr-1234",
        params={"expected_current_box_id": "box-1"},
    ).mock(return_value=httpx.Response(204))
    make_client().delete_pen("pr-1234", expected_current_box_id="box-1")
    assert route.called


@respx.mock
async def test_async_pen_round_trip() -> None:
    respx.post(f"{TEST_BASE_URL}/v1/pens").mock(
        return_value=httpx.Response(201, json=pen_json()),
    )
    route = respx.patch(f"{TEST_BASE_URL}/v1/pens/pr-1234").mock(
        return_value=httpx.Response(200, json=pen_json(current_box_id="box-1")),
    )
    respx.delete(f"{TEST_BASE_URL}/v1/pens/pr-1234").mock(
        return_value=httpx.Response(204),
    )
    async with AsyncHogland(token="t", base_url=TEST_BASE_URL) as client:
        pen = await client.create_pen("pr-1234", metadata={"pr": "1234"})
        assert pen.id.startswith("pen-")
        updated = await client.update_pen("pr-1234", current_box_id="box-1")
        assert updated.current_box_id == "box-1"
        sent = json.loads(route.calls.last.request.content)
        assert sent == {"current_box_id": "box-1"}
        await client.delete_pen("pr-1234")


@respx.mock
def test_hibernate_pen() -> None:
    route = respx.post(f"{TEST_BASE_URL}/v1/pens/pr-1234/hibernate").mock(
        return_value=httpx.Response(200, json=pen_json(latest_snapshot_id="snap-1")),
    )
    pen = make_client().hibernate_pen("pr-1234")
    assert isinstance(pen, Pen)
    assert pen.latest_snapshot_id == "snap-1"
    assert route.called


@respx.mock
def test_wake_pen() -> None:
    route = respx.post(f"{TEST_BASE_URL}/v1/pens/pr-1234/wake").mock(
        return_value=httpx.Response(200, json=pen_json(current_box_id="box-1")),
    )
    pen = make_client().wake_pen("pr-1234")
    assert isinstance(pen, Pen)
    assert pen.current_box_id == "box-1"
    assert route.called


@respx.mock
async def test_async_hibernate_wake() -> None:
    respx.post(f"{TEST_BASE_URL}/v1/pens/pr-1234/hibernate").mock(
        return_value=httpx.Response(200, json=pen_json(latest_snapshot_id="snap-1")),
    )
    respx.post(f"{TEST_BASE_URL}/v1/pens/pr-1234/wake").mock(
        return_value=httpx.Response(200, json=pen_json(current_box_id="box-1")),
    )
    async with AsyncHogland(token="t", base_url=TEST_BASE_URL) as client:
        hib = await client.hibernate_pen("pr-1234")
        assert hib.latest_snapshot_id == "snap-1"
        woke = await client.wake_pen("pr-1234")
        assert woke.current_box_id == "box-1"
