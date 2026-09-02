from __future__ import annotations

from datetime import date, timedelta

import pytest

from matrx_ai._ext import configure_ext
from matrx_ai.tools.implementations.seo import seo_get_keyword_data
from matrx_ai.tools.models import ToolContext


@pytest.mark.asyncio
async def test_keyword_tool_calls_host_seam_with_caller_identity() -> None:
    """The `keyword_research` ext seam is the ONE contract: an async host
    function receiving the caller's identity plus the request knobs, returning
    the DataForSEO live response body (SEO-WS-02 — the legacy sync SDK shape
    with its signature-sniffing compat dance is gone)."""
    from matrx_connect.context.app_context import AppContext, set_app_context

    captured = {}

    async def keyword_research(**kwargs):
        captured.update(kwargs)
        return {
            "status_code": 20000,
            "tasks": [
                {
                    "status_code": 20000,
                    "result": [
                        {
                            "keyword": "synthetic keyword",
                            "search_volume": 123,
                            "cpc": 1.25,
                            "competition": "LOW",
                            "competition_index": 10,
                            "monthly_searches": [],
                        }
                    ],
                }
            ],
        }

    configure_ext(keyword_research=keyword_research)
    ctx = ToolContext(call_id="call-1")
    app_ctx = AppContext(emitter=None, user_id="user-1", organization_id="org-1")
    token = set_app_context(app_ctx)
    today = date.today()
    try:
        result = await seo_get_keyword_data(
            {
                "keywords": ["synthetic keyword"],
                "date_from": (today - timedelta(days=30)).isoformat(),
                "date_to": (today - timedelta(days=1)).isoformat(),
            },
            ctx,
        )
    finally:
        token.var.reset(token)
    assert result.success is True
    assert captured["user_id"] == "user-1"
    assert captured["organization_id"] == "org-1"
    assert captured["keywords"] == ["synthetic keyword"]
    assert result.output["keywords_data"][0]["search_volume"] == 123
