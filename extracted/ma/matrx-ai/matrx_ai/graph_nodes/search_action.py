"""``ai.search.brave`` — execute a Brave web search and return structured results."""

from __future__ import annotations

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from pydantic import BaseModel, ConfigDict, Field


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

        result = await async_brave_search(
            query=inputs.query,
            freshness=inputs.freshness,
            country=inputs.country,
            extra_snippets=True,
        )

        combined = []
        urls = []
        if result:
            combined = result.get("web", {}).get("results", []) + result.get("news", {}).get(
                "results", []
            )
            if inputs.max_results is not None:
                combined = combined[: inputs.max_results]
            # Every result URL, in rank order (was combined[:1] — a bug that
            # made `urls` a single-element list no matter the result count).
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
