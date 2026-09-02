"""``ai.util`` — helper actions for data manipulation in workflows."""

from __future__ import annotations

from matrx_utils import vcprint

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from pydantic import BaseModel, ConfigDict, Field, JsonValue


class ExtractSearchUrlsInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    values: list[dict[str, JsonValue]] = Field(
        default_factory=list, description="List of search results gathered from channels."
    )
    max_urls_per_query: int = Field(default=1)


class ExtractSearchUrlsOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    urls: list[str] = Field(default_factory=list)


@register_node(
    name="ai.util.extract_search_urls",
    display_name="Get Links from Search",
    description="Collect the web links from a set of search results.",
    category=NodeCategory.DATA,
    determinism=ActionTier.PURE,
    input_schema=ExtractSearchUrlsInput,
    output_schema=ExtractSearchUrlsOutput,
    output_kind="web_search_urls",
    icon="link",
    tags=("util", "data", "search"),
)
async def ai_util_extract_search_urls(
    ctx: NodeExecutionContext, inputs: ExtractSearchUrlsInput
) -> NodeResult[ExtractSearchUrlsOutput]:
    urls = []
    for res in inputs.values:
        # If the search result has a pre-extracted 'urls' field, use it
        if "urls" in res and isinstance(res["urls"], list):
            urls.extend(res["urls"][: inputs.max_urls_per_query])
        # Otherwise look into 'results' array
        elif "results" in res and isinstance(res["results"], list):
            count = 0
            for r in res["results"]:
                if count >= inputs.max_urls_per_query:
                    break
                if isinstance(r, dict) and r.get("url"):
                    urls.append(r.get("url"))
                    count += 1

    return success(ExtractSearchUrlsOutput(urls=urls))


class FormatScrapedContentInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    values: list[dict[str, JsonValue]] = Field(
        default_factory=list, description="List of scraped pages gathered from channels."
    )
    max_chars_per_page: int = Field(default=1500)


class FormatScrapedContentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    formatted_text: str = ""
    #: URLs of the pages actually included, in the SAME ORDER as the blocks in
    #: ``formatted_text``. Without this the blob is anonymous: a model cannot
    #: cite which page said what, and a UI cannot link back — from pages we
    #: paid to crawl and whose URLs the node was already holding.
    sources: list[str] = Field(default_factory=list)
    page_count: int = 0
    #: Pages the scraper reported as failed. The node already computed this and
    #: threw it away, so "3 pages combined" and "3 pages, 2 of which failed"
    #: were indistinguishable downstream.
    failed_pages: int = 0


@register_node(
    name="ai.util.format_scraped_content",
    display_name="Combine Web Pages",
    description="Combine the content of several web pages into one block of text.",
    category=NodeCategory.DATA,
    determinism=ActionTier.PURE,
    input_schema=FormatScrapedContentInput,
    output_schema=FormatScrapedContentOutput,
    output_kind="combined_page_text",
    icon="align-left",
    tags=("util", "data", "scrape"),
)
async def ai_util_format_scraped_content(
    ctx: NodeExecutionContext, inputs: FormatScrapedContentInput
) -> NodeResult[FormatScrapedContentOutput]:
    blocks = []
    sources: list[str] = []
    failed_pages = 0
    for page in inputs.values:
        # A page the scraper reported as failed carries no body — count it so
        # an all-failed batch can say THAT, rather than blaming the shape.
        if page.get("success") is False:
            failed_pages += 1
            continue
        # The canonical scraped-page payload (`scraper.scrape` / `scrape_many`)
        # carries `text`, with `markdown` as the richer form. This read
        # `content` — a key nothing in the pipeline produces — so it returned
        # "" for real scraped pages and the run died two steps downstream
        # inside the model call ("prompt: String should have at least 1
        # character"). `content` stays last so any caller genuinely sending it
        # keeps working.
        content = page.get("text") or page.get("markdown") or page.get("content") or ""
        if isinstance(content, str) and content.strip():
            blocks.append(content[: inputs.max_chars_per_page])
            # Keep the block and its source index-aligned.
            url = page.get("url") or page.get("response_url")
            sources.append(str(url) if isinstance(url, str) else "")

    if inputs.values and not blocks:
        # Never hand an empty string downstream: it validates fine here and
        # then fails somewhere else entirely. Fail where the truth is.
        detail = (
            f"all {failed_pages} of them failed to load"
            if failed_pages == len(inputs.values)
            else "none of them carried any readable text"
        )
        return failure(
            "no_readable_content",
            f"Got {len(inputs.values)} page(s) to combine, but {detail}.",
            details={"page_count": len(inputs.values), "failed_pages": failed_pages},
        )

    # Newlines, not the literal characters \n — this was an escaped string, so
    # every joined block was separated by the visible text "\n---\n".
    formatted_text = "\n---\n".join(blocks)
    return success(
        FormatScrapedContentOutput(
            formatted_text=formatted_text,
            sources=sources,
            page_count=len(blocks),
            failed_pages=failed_pages,
        )
    )


class CostSummaryInput(BaseModel):
    model_config = ConfigDict(extra="allow")
    conversation_id: str | None = Field(
        default=None,
        description="The conversation ID to get the cost summary for. If not provided, the current app context's conversation ID is used.",
    )


class CostSummaryOutput(BaseModel):
    # NOTE (Node Result System, Wave 1 P2): field names diverge from the
    # canonical AiUsage vocabulary (total_cost_usd vs cost_usd,
    # total_api_duration_ms vs Timing.elapsed_ms). Renaming payload fields is
    # definition-breaking for authored mappings — the rename is DEFERRED to
    # the DB sweep (docs/workflow/sweep/P2_matrx_ai.md "Decisions").
    model_config = ConfigDict(extra="forbid")
    request_count: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    total_cost_usd: float
    total_api_duration_ms: int
    #: Human-readable model names (``claude-opus-4-7``). This used to carry the
    #: raw ``ai.model_definition`` UUIDs, so a non-technical user was shown
    #: "Models used: 2b6c05fe-c3e9-…". The ids are still available in
    #: ``model_ids`` — an id that cannot be resolved falls back to itself
    #: rather than vanishing.
    models_used: list[str]
    model_ids: list[str] = Field(default_factory=list)
    #: Cache-read tokens. Counted in ``total_tokens`` but NOT in
    #: ``input_tokens``/``output_tokens`` — without this field the arithmetic
    #: simply does not add up, which is exactly what a real conversation showed
    #: (1,381,954 + 2,962 in, 2,384,488 total).
    cached_tokens: int = 0
    providers: list[str] = Field(default_factory=list)


@register_node(
    name="ai.util.cost_summary",
    display_name="Get AI Cost",
    description="Get the total AI cost for a conversation.",
    category=NodeCategory.DATA,
    determinism=ActionTier.PURE,
    input_schema=CostSummaryInput,
    output_schema=CostSummaryOutput,
    output_kind="ai_cost_summary",
    icon="dollar-sign",
    tags=("ai", "cost", "util"),
)
async def ai_util_cost_summary(
    ctx: NodeExecutionContext, inputs: CostSummaryInput
) -> NodeResult[CostSummaryOutput]:
    conversation_id = inputs.conversation_id or getattr(ctx.app, "conversation_id", None)
    if not conversation_id:
        return success(
            CostSummaryOutput(
                request_count=0,
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
                total_cost_usd=0.0,
                total_api_duration_ms=0,
                models_used=[],
                model_ids=[],
                cached_tokens=0,
                providers=[],
            )
        )

    from matrx_ai.db.cx_managers import cxm

    summary = await cxm.get_conversation_cost_summary(conversation_id)
    model_ids = list(summary.models_used)
    return success(
        CostSummaryOutput(
            request_count=summary.request_count,
            input_tokens=summary.input_tokens,
            output_tokens=summary.output_tokens,
            total_tokens=summary.total_tokens,
            total_cost_usd=float(summary.total_cost),
            total_api_duration_ms=summary.total_api_duration_ms,
            models_used=await _resolve_model_names(model_ids),
            model_ids=model_ids,
            cached_tokens=summary.cached_tokens,
            providers=list(summary.providers),
        )
    )


async def _resolve_model_names(model_ids: list[str]) -> list[str]:
    """``ai.model_definition`` ids → their names, id kept when unresolvable.

    ``ConversationCostSummary.models_used`` holds raw UUIDs. Handing those to a
    workflow author (or to a model) as "models used" is degraded data: nobody
    can read it. One indexed lookup turns it into ``claude-opus-4-7``; a
    lookup that fails degrades to the id rather than dropping the model.
    """
    if not model_ids:
        return []
    from matrx_ai.db._registry import get_model

    try:
        rows = await get_model("AiModel").filter(id__in=model_ids).all()
        by_id = {str(row.id): (row.name or str(row.id)) for row in rows}
    except Exception as e:
        # Degrading to ids is the right fallback, but doing it SILENTLY is how
        # unreadable data reaches a user and nobody ever learns why.
        vcprint(
            f"[ai.util.cost_summary] could not resolve model names, falling back "
            f"to ids: {type(e).__name__}: {e}",
            color="yellow",
        )
        return list(model_ids)
    unresolved = [mid for mid in model_ids if mid not in by_id]
    if unresolved:
        vcprint(
            f"[ai.util.cost_summary] {len(unresolved)} model id(s) have no "
            f"ai.model_definition row; showing the raw id: {unresolved}",
            color="yellow",
        )
    return [by_id.get(mid, mid) for mid in model_ids]


class ParseLlmJsonInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: str = Field(
        min_length=1,
        description=(
            "Raw LLM output to parse — fenced ```json blocks, partial "
            "fragments, and surrounding prose are all handled by the "
            "canonical matrx-ai extraction funnel. No second model call."
        ),
    )
    schema_definition: dict[str, JsonValue] = Field(
        default_factory=dict,
        description=(
            "Optional JSON Schema; when set, only candidates matching the "
            "top-level shape are accepted (common shape mismatches are "
            "auto-normalized by the funnel)."
        ),
    )


class ParseLlmJsonOutput(BaseModel):
    # Closed envelope — the parsed payload lives ONLY under `value` (edges
    # reach inside via source-side dot-paths: `value.suggested_keywords`).
    # No root key-spread: spreading made the contract open (`extra="allow"`)
    # forever, the same defect the P1 sweep killed on tool.call.
    model_config = ConfigDict(extra="forbid")

    value: JsonValue = Field(
        default=None,
        description=(
            "The parsed JSON value (always present, whatever its type). "
            "Map nested fields with dot-paths, e.g. `value.suggested_keywords`."
        ),
    )


@register_node(
    name="ai.util.parse_llm_json",
    display_name="Read Data from AI Reply",
    description="Pull the structured data out of an AI's text reply.",
    category=NodeCategory.DATA,
    determinism=ActionTier.PURE,
    input_schema=ParseLlmJsonInput,
    output_schema=ParseLlmJsonOutput,
    output_kind="parsed_json",
    icon="braces",
    tags=("ai", "util", "parse", "json"),
)
async def ai_util_parse_llm_json(
    ctx: NodeExecutionContext, inputs: ParseLlmJsonInput
) -> NodeResult[ParseLlmJsonOutput]:
    _ = ctx
    from matrx_ai.agents.response_parser import extract_json
    from matrx_graph.types.result import failure

    result = extract_json(
        inputs.text,
        schema=inputs.schema_definition or None,
        detailed=True,
    )
    if not result.success or result.data is None:
        return failure(
            "parse_failed",
            f"no JSON found in the text: {result.reason}",
            details={"reason": str(result.reason)},
        )
    return success(ParseLlmJsonOutput(value=result.data))
