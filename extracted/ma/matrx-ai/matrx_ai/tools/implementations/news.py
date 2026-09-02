from __future__ import annotations

import traceback
from datetime import datetime
from typing import Any

from matrx_ai.tools.models import ToolContext, ToolError, ToolResult


async def news_get_headlines(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import NewsGetHeadlinesArgs
    NewsGetHeadlinesArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    from matrx_ai._ext import get_ext
    get_top_headlines = get_ext("get_top_headlines")

    country = args.get("country") or None
    category = args.get("category") or None
    query = args.get("query") or None
    sources = args.get("sources") or None
    language = args.get("language") or "en"

    if not country and not sources and not category:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="Provide at least one of: country, sources, or category.",
                suggested_action="Try country='us' for US headlines, or category='technology' for tech news.",
            ),
        )

    # The News API does not allow sources to be combined with country or category.
    # If sources is provided alongside country/category, drop sources and use country/category.
    if sources and (country or category):
        sources = None

    try:
        response = get_top_headlines(
            query=query,
            sources=sources,
            category=category,
            language=language,
            country=country,
        )

        if response.get("status") != "ok":
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="api_error",
                    message=f"News API error: {response.get('message', 'Unknown error')}",
                ),
            )

        articles = response.get("articles", [])
        total = response.get("totalResults", 0)
        today = datetime.now().strftime("%A, %B %d, %Y")

        country_label = (country.upper() + " ") if country else ""
        intro = f"Today is {today}. Here are the current top news headlines for {country_label}on {today}:"

        clean_articles = [
            {
                "title": a.get("title"),
                "source": {
                    "id": a.get("source", {}).get("id"),
                    "name": a.get("source", {}).get("name"),
                },
                "author": a.get("author"),
                "description": a.get("description"),
                "url": a.get("url"),
                "url_to_image": a.get("urlToImage"),
                "published_at": a.get("publishedAt"),
                "content": a.get("content"),
            }
            for a in articles
        ]

        return ToolResult(
            success=True,
            output={
                "intro": intro,
                "date": today,
                "total_results": total,
                "articles": clean_articles,
            },
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"Failed to fetch headlines: {e}",
                traceback=traceback.format_exc(),
                is_retryable=True,
            ),
        )
