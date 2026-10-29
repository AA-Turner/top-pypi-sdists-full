"""``ai.search.brave`` — execute a Brave web search and return structured results."""

from __future__ import annotations

import asyncio

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from pydantic import BaseModel, ConfigDict, Field

#: Brave serves at most 20 results per page. Provider fact, not a choice.
BRAVE_PAGE_SIZE = 20
#: SAFETY ceiling on pages one step may fetch (Brave's offset tops out at 9).
BRAVE_MAX_RESULT_PAGES = 10
#: Spacing between page calls of ONE query (provider rate limit pacing).
BRAVE_PAGE_PACING_SECONDS = 1.0


class BraveSearchInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    query: str = Field(min_length=1, description="The search query string.")
    freshness: str | None = Field(default=None, description="pd, pw, pm, py, or None")
    country: str = Field(default="US")
    max_results: int | None = Field(
        default=None,
        ge=1,
        description="Cap `results` (and therefore `urls`) at this many combined "
        "web+news items, best-ranked first. None returns everything web search sent.",
    )
    result_pages: int | None = Field(
        default=None,
        ge=1,
        le=BRAVE_MAX_RESULT_PAGES,
        description="How many pages of results to fetch (20 per page), deduplicated by "
        "URL. Empty = one page. Wire a setting in for a governed depth.",
    )
    channel_out: str | None = Field(
        default=None,
        description="Optional channel to write the results to. Used for gather/fan-in patterns.",
    )


class BraveSearchResultItem(BaseModel):
    """One raw web search result (a ``web.results`` or ``news.results`` item).

    The web search API item is passed through unmodified — declared fields
    are the ones our consumers read (see
    ``matrx_scraper.search.search.generate_search_text_summary``); the many
    provider-specific keys (``meta_url``, ``profile``, ``thumbnail``, …)
    remain reachable via ``extra="allow"`` — a genuinely dynamic passthrough,
    so the open shape stays.
    """

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "raw web search API item passthrough; consumers read provider keys"
        },
    )

    title: str | None = Field(default=None, description="Result headline supplied by web search.")
    url: str | None = Field(default=None, description="Canonical destination URL for the result.")
    description: str | None = Field(default=None, description="Primary search-result snippet.")
    extra_snippets: list[str] = Field(
        default_factory=list, description="Additional relevant snippets returned for the result."
    )
    age: str | None = Field(
        default=None, description="Human-readable content age reported by web search."
    )
    page_age: str | None = Field(
        default=None, description="Published or indexed page-age value reported by web search."
    )
    language: str | None = Field(
        default=None, description="Detected language code for the result page."
    )
    rank: int | None = Field(
        default=None, description="1-based position across every fetched page, best first."
    )


class BraveSearchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    results: list[BraveSearchResultItem] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)


@register_node(
    name="ai.search.brave",
    display_name="Web Search",
    description="Search the web and return the top results.",
    category=NodeCategory.TOOL,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=BraveSearchInput,
    output_schema=BraveSearchOutput,
    output_kind="web_search_results",
    icon="search",
    tags=("ai", "search", "web"),
)
async def ai_search_brave(
    ctx: NodeExecutionContext, inputs: BraveSearchInput
) -> NodeResult[BraveSearchOutput]:
    try:
        from matrx_ai._ext import get_ext

        _brave = get_ext("brave_search")
        async_brave_search = _brave["async_brave_search"]

        pages = inputs.result_pages or 1
        combined: list[dict] = []
        seen_urls: set[str] = set()
        for page in range(pages):
            if page:
                await asyncio.sleep(BRAVE_PAGE_PACING_SECONDS)
            result = await async_brave_search(
                query=inputs.query,
                count=BRAVE_PAGE_SIZE,
                offset=page,
                freshness=inputs.freshness,
                country=inputs.country,
                extra_snippets=True,
            )
            if not result:
                break
            page_items = result.get("web", {}).get("results", []) + result.get(
                "news", {}
            ).get("results", [])
            if not page_items:
                break
            for item in page_items:
                url = item.get("url")
                if url and url in seen_urls:
                    continue
                if url:
                    seen_urls.add(url)
                combined.append({**item, "rank": len(combined) + 1})
            if inputs.max_results is not None and len(combined) >= inputs.max_results:
                break

        if inputs.max_results is not None:
            combined = combined[: inputs.max_results]
        # Every result URL, in rank order.
        urls = [r["url"] for r in combined if r.get("url")]

        output = BraveSearchOutput(query=inputs.query, results=combined, urls=urls)

        if inputs.channel_out:
            ctx.channels.write(inputs.channel_out, output)

        return success(output)

    except Exception as e:
        # Node Result System: failure travels in the envelope — nothing is
        # written to channel_out on failure (fan-in consumers see only real
        # results; use on_item_failure='hole' for explicit failed slots).
        return failure(
            "search_failed",
            f"{type(e).__name__}: {e}",
            details={"query": inputs.query},
        )
