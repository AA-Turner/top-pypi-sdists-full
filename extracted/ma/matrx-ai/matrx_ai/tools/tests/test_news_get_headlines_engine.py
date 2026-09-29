"""Regression guard: ``news_get_headlines`` runs on the native news engine.

Lane H (class fix, 2026-09-28): this tool used to call the NewsAPI client
directly (``api_management/news``, now deleted). It now calls the SAME
service function the ``news_search`` tool and the ``news.search`` workflow
node call (``aidream.services.news.search.search_news``), while keeping its
own declared arg/output contract unchanged — so every existing agent binding
(the ``tool.definition`` row, its id, and every agent's ``tools`` array) keeps
working with zero edits.

These tests were red against the pre-fix implementation (it called
``matrx_ai._ext.get_ext("get_top_headlines")``, never ``search_news``, and
had no organization hold) and are green against the current one.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.tools.implementations.news import _headline_query, news_get_headlines
from matrx_ai.tools.models import ToolContext

ORG_ID = "news-org-11111111-1111-1111-1111-111111111111"


class _NullEmitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...


@pytest.fixture()
def app_ctx_with_active_org():
    tokens: list[Any] = []

    def _make(organization_id: str | None) -> None:
        ctx = AppContext(emitter=_NullEmitter(), user_id="u1", organization_id=organization_id)
        tokens.append(set_app_context(ctx))

    yield _make

    for token in tokens:
        try:
            clear_app_context(token)
        except ValueError:
            pass


def _tool_ctx() -> ToolContext:
    return ToolContext(call_id="test-call")


def _fake_result(query: str):
    return SimpleNamespace(
        query=query,
        hits=[
            SimpleNamespace(
                title="Recycling plant opens",
                url="https://example.com/a",
                source="google_news",
                publisher="example.com",
                published_at="2026-09-28T10:00:00Z",
                excerpt="A new plant opened today.",
                author="Jane Reporter",
            ),
        ],
        total_before_limit=1,
    )


def test_headline_query_prefers_explicit_query() -> None:
    assert _headline_query({"query": "acme corp", "country": "us"}) == "acme corp"


def test_headline_query_falls_back_to_category_and_country() -> None:
    assert _headline_query({"category": "technology", "country": "us"}) == "technology us news"


def test_headline_query_never_empty() -> None:
    assert _headline_query({}) == "top news"


async def test_news_get_headlines_requires_a_filter() -> None:
    result = await news_get_headlines({}, _tool_ctx())
    assert result.success is False
    assert result.error.error_type == "validation"


async def test_news_get_headlines_needs_an_organization() -> None:
    # No AppContext installed -> ToolContext.organization_id is None.
    result = await news_get_headlines({"country": "us"}, _tool_ctx())
    assert result.success is False
    assert result.error is not None


async def test_news_get_headlines_calls_the_news_engine_and_maps_output(
    app_ctx_with_active_org,
) -> None:
    app_ctx_with_active_org(ORG_ID)

    mock_search_news = AsyncMock(side_effect=lambda query, **kw: _fake_result(query))
    with patch("matrx_ai.tools.implementations.news.get_ext", return_value=mock_search_news):
        result = await news_get_headlines(
            {"category": "technology", "country": "us"}, _tool_ctx()
        )

    assert result.success is True
    mock_search_news.assert_awaited_once()
    call_args, call_kwargs = mock_search_news.call_args
    assert call_args[0] == "technology us news"
    assert call_kwargs["organization_id"] == ORG_ID

    assert result.output["total_results"] == 1
    article = result.output["articles"][0]
    assert article["title"] == "Recycling plant opens"
    assert article["url"] == "https://example.com/a"
    assert article["source"] == {"id": "google_news", "name": "example.com"}
    assert article["author"] == "Jane Reporter"
    assert article["description"] == "A new plant opened today."
    assert article["published_at"] == "2026-09-28T10:00:00Z"
    # The news engine carries no image/full-content fields — never fabricated.
    assert article["url_to_image"] is None
    assert article["content"] is None
