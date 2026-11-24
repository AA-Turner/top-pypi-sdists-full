"""A search answer is a provider answer: recorded once and served again exactly, like a page (lane H2, 2026-11-16).

A fresh-topic side-by-side proof searches the same keywords twice, once per engine. Brave's ranking moves between
calls, so the copies kept different sources for the website's reasons, not the engines'. With the host's
``page_replay`` ext registered, the second identical search is served the first one's answer; a different search
(another query or page) is still live, and with no ext every search is live.
"""

from __future__ import annotations

import itertools
from typing import Any

import pytest

from matrx_scraper import _ext
from matrx_scraper.search import search


class _Store:
    def __init__(self) -> None:
        self.answers: dict[tuple[str, str], Any] = {}

    async def lookup(self, kind: str, url: str) -> Any:
        return self.answers.get((kind, url))

    async def record(self, kind: str, url: str, answer: Any) -> None:
        self.answers[(kind, url)] = answer


class _MovingClient:
    """Brave, whose top result changes every call."""

    def __init__(self) -> None:
        self.calls = 0
        self._n = itertools.count()

    async def search(self, **kw: Any) -> dict[str, Any]:
        self.calls += 1
        n = next(self._n)
        return {"web": {"results": [{"title": f"result {n}", "url": f"https://example.com/{n}", "description": kw["query"]}]}}


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> _MovingClient:
    c = _MovingClient()
    monkeypatch.setattr(search, "get_client", lambda: c)
    return c


@pytest.mark.asyncio
async def test_a_second_identical_search_is_served_the_first_answer(monkeypatch, client) -> None:
    store = _Store()
    monkeypatch.setitem(_ext._registry, "page_replay", store)
    first = await search.async_brave_search("idaho dance", offset=0)
    second = await search.async_brave_search("idaho dance", offset=0)
    assert second == first
    assert client.calls == 1, "the replayed search must not reach the provider"
    assert [k for k, _ in store.answers] == ["search"]
    other = await search.async_brave_search("idaho dance", offset=1)
    assert other != first and client.calls == 2, "another page of results is a different search: live"


@pytest.mark.asyncio
async def test_with_no_host_every_search_is_live(monkeypatch, client) -> None:
    monkeypatch.delitem(_ext._registry, "page_replay", raising=False)
    a = await search.async_brave_search("idaho dance")
    b = await search.async_brave_search("idaho dance")
    assert a != b and client.calls == 2
