"""Cursor walk semantics for sync and async paginators (SPEC 2.5, 3.5)."""

from __future__ import annotations

import json

import httpx

from getanyapi._pagination import apaginate, paginate
from conftest import (
    json_response,
    make_async_client,
    make_sync_client,
    run_envelope,
)


def _page(items: list[dict[str, int]], next_cursor: str | None) -> dict:
    return run_envelope(
        {"ads": items, "nextCursor": next_cursor},
        items=len(items),
    )


def _multi_page_responder():
    pages = [
        _page([{"id": 1}, {"id": 2}], "c1"),
        _page([{"id": 3}, {"id": 4}], "c2"),
        _page([{"id": 5}], None),
    ]
    state = {"i": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        body = pages[state["i"]]
        state["i"] += 1
        return json_response(200, body)

    return respond


def test_sync_walks_all_pages_flattening_items() -> None:
    client, rec = make_sync_client(_multi_page_responder())
    p = paginate(client, "facebook.ads_search", {"q": "x"}, "ads")
    ids = [item["id"] for item in p]
    assert ids == [1, 2, 3, 4, 5]
    assert len(rec.requests) == 3
    # cursor is injected on page 2+ only.
    assert "cursor" not in json.loads(rec.requests[0].content)
    assert json.loads(rec.requests[1].content)["cursor"] == "c1"
    assert json.loads(rec.requests[2].content)["cursor"] == "c2"


def test_sync_pages_yields_whole_run_results() -> None:
    client, _ = make_sync_client(_multi_page_responder())
    p = paginate(client, "facebook.ads_search", {"q": "x"}, "ads")
    pages = list(p.pages())
    assert len(pages) == 3
    assert all(page.cost_usd > 0 for page in pages)
    assert pages[0].output.data["ads"][0]["id"] == 1


def test_sync_derives_distinct_bounded_idempotency_key_per_page() -> None:
    client, rec = make_sync_client(_multi_page_responder())
    base_key = "k" * 255
    pages = list(
        paginate(
            client,
            "facebook.ads_search",
            {"q": "x"},
            "ads",
            options={"idempotency_key": base_key},
        ).pages()
    )

    assert len(pages) == 3
    keys = [request.headers["idempotency-key"] for request in rec.requests]
    assert [len(key) for key in keys] == [255, 255, 255]
    assert keys[0].endswith("-p1")
    assert keys[1].endswith("-p2")
    assert keys[2].endswith("-p3")
    assert len(set(keys)) == 3


def test_sync_stops_on_not_found() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope(None, found=False))

    client, rec = make_sync_client(respond)
    p = paginate(client, "facebook.ads_search", {"q": "x"}, "ads")
    assert list(p) == []
    assert len(rec.requests) == 1


def test_sync_stops_on_empty_cursor() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, _page([{"id": 1}], ""))

    client, rec = make_sync_client(respond)
    p = paginate(client, "facebook.ads_search", {"q": "x"}, "ads")
    assert [i["id"] for i in p] == [1]
    assert len(rec.requests) == 1  # empty cursor ends the walk


def test_sync_max_items_caps_mid_page() -> None:
    client, rec = make_sync_client(_multi_page_responder())
    p = paginate(
        client,
        "facebook.ads_search",
        {"q": "x"},
        "ads",
        options={"max_items": 3},
    )
    ids = [item["id"] for item in p]
    assert ids == [1, 2, 3]  # capped mid second page
    # The wire request must NOT carry max_items (iterator paces itself).
    for req in rec.requests:
        assert "max_items" not in req.url.params


def test_sync_yields_validated_item_models_attribute_access() -> None:
    # B3: with an item model, yielded items are pydantic models (attribute access),
    # not raw dicts. Guards against the "iter_* yields dicts" regression.
    from pydantic import BaseModel

    class _Ad(BaseModel):
        id: int

    client, _ = make_sync_client(_multi_page_responder())
    p = paginate(
        client,
        "facebook.ads_search",
        {"q": "x"},
        "ads",
        item_model=_Ad,
        data_model=None,
        bare=False,
    )
    items = list(p)
    assert [item.id for item in items] == [1, 2, 3, 4, 5]
    assert all(isinstance(item, _Ad) for item in items)


def test_sync_bare_envelope_walks_output_root() -> None:
    # A synthetic future bare operation has no found/data wrapper. Its page data IS output,
    # so the walk reads posts/nextCursor off output directly.
    from pydantic import BaseModel

    class _Post(BaseModel):
        id: int

    pages = [
        {
            "output": {"posts": [{"id": 1}, {"id": 2}], "nextCursor": "c1"},
            "replayed": False,
            "provider": "AnyAPI",
            "costUsd": 0.003,
            "items": 2,
        },
        {
            "output": {"posts": [{"id": 3}], "nextCursor": ""},
            "replayed": False,
            "provider": "AnyAPI",
            "costUsd": 0.003,
            "items": 1,
        },
    ]
    state = {"i": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        body = pages[state["i"]]
        state["i"] += 1
        return json_response(200, body)

    client, rec = make_sync_client(respond)
    p = paginate(
        client,
        "fixture.bare_paginated",
        {"query": "x"},
        "posts",
        item_model=_Post,
        data_model=None,
        bare=True,
    )
    ids = [post.id for post in p]
    assert ids == [1, 2, 3]
    assert len(rec.requests) == 2
    assert json.loads(rec.requests[1].content)["cursor"] == "c1"


async def test_async_walks_all_pages() -> None:
    client, rec = make_async_client(_multi_page_responder())
    p = apaginate(client, "facebook.ads_search", {"q": "x"}, "ads")
    ids = [item["id"] async for item in p]
    assert ids == [1, 2, 3, 4, 5]
    assert len(rec.requests) == 3
    await client.aclose()


async def test_async_pages_and_max_items() -> None:
    client, _ = make_async_client(_multi_page_responder())
    p = apaginate(
        client,
        "facebook.ads_search",
        {"q": "x"},
        "ads",
        options={"max_items": 2},
    )
    ids = [item["id"] async for item in p]
    assert ids == [1, 2]

    client2, _ = make_async_client(_multi_page_responder())
    p2 = apaginate(client2, "facebook.ads_search", {"q": "x"}, "ads")
    pages = [page async for page in p2.pages()]
    assert len(pages) == 3
    await client.aclose()
    await client2.aclose()


async def test_async_derives_distinct_idempotency_key_per_page() -> None:
    client, rec = make_async_client(_multi_page_responder())
    paginator = apaginate(
        client,
        "facebook.ads_search",
        {"q": "x"},
        "ads",
        options={"idempotency_key": "customer-key"},
    )
    pages = [page async for page in paginator.pages()]

    assert len(pages) == 3
    assert [
        request.headers["idempotency-key"] for request in rec.requests
    ] == ["customer-key-p1", "customer-key-p2", "customer-key-p3"]
    await client.aclose()
