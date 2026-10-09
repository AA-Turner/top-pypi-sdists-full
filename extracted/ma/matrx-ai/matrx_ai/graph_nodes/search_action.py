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
        "web+news items, best-ranked first. None returns everything Brave sent.",
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
    """One raw Brave result (a ``web.results`` or ``news.results`` item).

    The Brave Search API item is passed through unmodified — declared fields
    are the ones our consumers read (see
    ``matrx_scraper.search.search.generate_search_text_summary``); the many
    provider-specific keys (``meta_url``, ``profile``, ``thumbnail``, …)
    remain reachable via ``extra="allow"`` — a genuinely dynamic passthrough,
    so the open shape stays.
    """

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "raw Brave API item passthrough; consumers read provider keys"
        },
    )

    title: str | None = Field(default=None, description="Result headline supplied by Brave.")
    url: str | None = Field(default=None, description="Canonical destination URL for the result.")
    description: str | None = Field(default=None, description="Primary search-result snippet.")
    extra_snippets: list[str] = Field(
        default_factory=list, description="Additional relevant snippets returned for the result."
    )
    age: str | None = Field(
        default=None, description="Human-readable content age reported by Brave."
    )
    page_age: str | None = Field(
        default=None, description="Published or indexed page-age value reported by Brave."
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


# ── ai.search.rank_sources ───────────────────────────────────────────────────


class RankSourcesInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    results: list[dict] = Field(
        default_factory=list,
        description="Search results to rank (each with url and rank). The same url "
        "appearing for several queries counts toward its breadth.",
    )
    authority: dict[str, int] = Field(
        default_factory=dict,
        description="Optional site authority 0-100 by host name. Unknown hosts score 0.",
    )
    limit: int | None = Field(
        default=None, ge=1, description="Keep only the best this many. Empty = keep all."
    )


def _host(url: str) -> str:
    from urllib.parse import urlparse

    return (urlparse(url).hostname or "").removeprefix("www.")


def rank_sources(
    results: list[dict], authority: dict[str, int], limit: int | None
) -> list[dict]:
    """Best-first by the platform's ONE pre-read score (matrx_ai.search_ranking)."""
    from matrx_ai.search_ranking import KeywordRanking, compute_pre_read_score

    by_url: dict[str, dict] = {}
    rankings: dict[str, list[KeywordRanking]] = {}
    for position, item in enumerate(results, 1):
        url = item.get("url")
        if not url:
            continue
        by_url.setdefault(url, item)
        rank = int(item.get("rank") or position)
        query = str(item.get("query") or "")
        rankings.setdefault(url, [])
        if all(kr.keyword != query for kr in rankings[url]):
            rankings[url].append(KeywordRanking(keyword=query, keyword_weight=1.0, google_rank=rank))
    total_weight = float(len({kr.keyword for krs in rankings.values() for kr in krs}) or 1)
    host_authority = {_host(h) or h: v for h, v in authority.items()}
    scored: list[tuple[float, int, dict]] = []
    for url, item in by_url.items():
        breakdown = compute_pre_read_score(
            rankings[url], total_weight, host_authority.get(_host(url))
        )
        best = min(kr.google_rank for kr in rankings[url])
        scored.append(
            (
                breakdown.pre_read_score,
                best,
                {
                    **item,
                    "url": url,
                    "rank": best,
                    "pre_read_score": round(breakdown.pre_read_score, 3),
                },
            )
        )
    scored.sort(key=lambda t: (-t[0], t[1]))
    ranked = [s for _, _, s in scored]
    return ranked[:limit] if limit is not None else ranked


@register_node(
    name="ai.search.rank_sources",
    display_name="Rank Search Results",
    description="Order search results best-first before reading them.",
    category=NodeCategory.TOOL,
    determinism=ActionTier.PURE,
    input_schema=RankSourcesInput,
    # Same shape as ai.search.brave's output — still search results, now best
    # first, each carrying its pre_read_score.
    output_schema=BraveSearchOutput,
    output_kind="web_search_results",
    icon="list-ordered",
    tags=("search", "rank", "web"),
)
async def ai_search_rank_sources(
    ctx: NodeExecutionContext, inputs: RankSourcesInput
) -> NodeResult[BraveSearchOutput]:
    _ = ctx
    ranked = rank_sources(inputs.results, inputs.authority, inputs.limit)
    return success(
        BraveSearchOutput(
            query=str(inputs.model_extra.get("query") or "") if inputs.model_extra else "",
            results=ranked,
            urls=[r["url"] for r in ranked],
        )
    )
