from __future__ import annotations

import traceback
from datetime import datetime
from typing import Any

from matrx_ai._ext import get_ext
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.organization_hold import carried_organization_id, organization_required_result

#: Retired 2026-09-28 (Lane H, class fix): this tool used to call the NewsAPI
#: client directly (``api_management/news``, now deleted). It now runs on the
#: SAME native news engine as the ``news_search`` tool
#: (``aidream.services.news.search.search_news``) — the declared arg/output
#: contract (``NewsGetHeadlinesArgs`` / the intro+date+total_results+articles
#: envelope) is unchanged, so every existing agent binding keeps working
#: unmodified. ``tool_def.description`` was updated separately via
#: ``PATCH /admin/tools/news_get_headlines`` (the DB is the source of truth
#: for descriptions — see ``aidream/startup/tools_check.py``).


def _headline_query(args: dict[str, Any]) -> str:
    """One free-text query for the news engine from the legacy NewsAPI-shaped
    args (``query`` / ``category`` / ``country`` / ``sources``) — the engine
    takes a single search string, not NewsAPI's country+category+source
    filters, so a filter-only call (no ``query``) is turned into search terms."""
    query = (args.get("query") or "").strip()
    if query:
        return query
    parts: list[str] = []
    category = args.get("category")
    if category:
        parts.append(str(category).replace("_", " "))
    country = args.get("country")
    if country:
        parts.append(f"{country} news")
    sources = args.get("sources")
    if sources and not parts:
        # Legacy NewsAPI source ids (e.g. "bbc-news,cnn") don't map to the news
        # engine's provider list (google_news / gdelt / hackernews / reddit /
        # brave_news / x_news); carried through as search terms, best effort.
        parts.append(str(sources).replace(",", " "))
    return " ".join(parts).strip() or "top news"


async def news_get_headlines(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import NewsGetHeadlinesArgs
    NewsGetHeadlinesArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)

    country = args.get("country") or None
    category = args.get("category") or None
    query = args.get("query") or None
    sources = args.get("sources") or None

    if not country and not sources and not category and not query:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="Provide at least one of: query, country, sources, or category.",
                suggested_action="Try country='us' for US headlines, or category='technology' for tech news.",
            ),
        )

    organization_id = carried_organization_id(ctx)
    if not organization_id:
        return organization_required_result(
            what="search for news headlines",
            tool_name="news_get_headlines",
            ctx=ctx,
        )

    try:
        news_search = get_ext("news_search")
        result = await news_search(
            _headline_query(args),
            organization_id=organization_id,
            limit=20,
        )

        today = datetime.now().strftime("%A, %B %d, %Y")
        country_label = (country.upper() + " ") if country else ""
        intro = f"Today is {today}. Here are the current top news headlines for {country_label}on {today}:"

        clean_articles = [
            {
                "title": hit.title,
                "source": {
                    "id": hit.source,
                    "name": hit.publisher,
                },
                "author": hit.author,
                "description": hit.excerpt or None,
                "url": hit.url,
                "url_to_image": None,
                "published_at": hit.published_at,
                "content": None,
            }
            for hit in result.hits
        ]

        return ToolResult(
            success=True,
            output={
                "intro": intro,
                "date": today,
                "total_results": result.total_before_limit,
                "articles": clean_articles,
            },
        )

    except ValueError as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=str(e),
            ),
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
