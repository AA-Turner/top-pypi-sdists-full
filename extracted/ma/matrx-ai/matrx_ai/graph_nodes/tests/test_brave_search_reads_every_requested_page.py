"""``ai.search.brave`` reads as many result pages as asked, deduplicated and ranked.

The node used to make ONE provider call, so a workflow could never see past the
first 20 results while the research code path reads five pages per keyword
(``research/search.py::execute_search``) — the depth gap (a) in the 2026-10-07
code-vs-workflow Deep Research comparison."""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.graph_nodes import register_with_graph, search_action
from matrx_ai.graph_nodes.search_action import BraveSearchInput, ai_search_brave
from matrx_ai.graph_nodes.tests.test_node_handlers_execute import _ctx

register_with_graph()


def _page(offset: int, n: int = 20) -> dict[str, Any]:
    return {"web": {"results": [{"url": f"https://ex.com/{offset}/{i}", "title": "t"} for i in range(n)]}}


@pytest.fixture
def calls(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    seen: list[dict[str, Any]] = []
    pages = {0: _page(0), 1: _page(1), 2: {"web": {"results": [{"url": "https://ex.com/0/0"}, {"url": "https://ex.com/2/x"}]}}}

    async def _fake(**kw: Any) -> dict[str, Any]:
        seen.append(kw)
        return pages.get(kw["offset"], {"web": {"results": []}})

    monkeypatch.setitem(_ext._registry, "brave_search", {"async_brave_search": _fake})
    monkeypatch.setattr(search_action, "BRAVE_PAGE_PACING_SECONDS", 0)
    return seen


def _results(res: Any) -> list[dict[str, Any]]:
    return [r.model_dump() if hasattr(r, "model_dump") else r for r in res.result.results]


@pytest.mark.asyncio
async def test_three_pages_requested_three_pages_read_deduped_and_ranked(calls: list[dict[str, Any]]) -> None:
    res = await ai_search_brave(_ctx(), BraveSearchInput(query="q", result_pages=3))
    assert [c["offset"] for c in calls] == [0, 1, 2]
    rows = _results(res)
    assert len(rows) == 41  # 20 + 20 + 1 new (the repeat of /0/0 is dropped)
    assert [r["rank"] for r in rows] == list(range(1, 42))
    assert len(set(res.result.urls)) == 41


@pytest.mark.asyncio
async def test_default_is_one_page(calls: list[dict[str, Any]]) -> None:
    res = await ai_search_brave(_ctx(), BraveSearchInput(query="q"))
    assert [c["offset"] for c in calls] == [0]
    assert len(_results(res)) == 20


@pytest.mark.asyncio
async def test_stops_at_the_first_empty_page(calls: list[dict[str, Any]]) -> None:
    res = await ai_search_brave(_ctx(), BraveSearchInput(query="q", result_pages=6))
    assert [c["offset"] for c in calls] == [0, 1, 2, 3]
    assert len(_results(res)) == 41
