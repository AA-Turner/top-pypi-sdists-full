"""``ai.util`` — helper actions for data manipulation in workflows."""

from __future__ import annotations

from matrx_graph.actions import ActionFailed, declare_action
from typing import Any

from matrx_graph.types.identity_inputs import identity_input
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_utils import vcprint
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


@declare_action(
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
    doors={"step"},
)
async def ai_util_extract_search_urls(
    app: Any, inputs: ExtractSearchUrlsInput
) -> ExtractSearchUrlsOutput:
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

    return ExtractSearchUrlsOutput(urls=urls)


class FormatScrapedContentInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    values: list[dict[str, JsonValue]] = Field(
        default_factory=list, description="List of scraped pages gathered from channels."
    )
    #: None = the organization's research page cap (knob ``agents.research_web/page_max_chars``,
    #: 20,000 standalone) — the same cap ``research_web`` puts on a page before a model reads it.
    #: The old default was 1,500: about one paragraph, so most of every page never reached the
    #: model and nothing said so. A value given here still wins (an authored step keeps its own).
    max_chars_per_page: int | None = Field(default=None, ge=1)


class CombinedPageRecord(BaseModel):
    """What happened to one page on its way into ``formatted_text`` (index-aligned with ``sources``).

    The record survives any later text cut: a reader learns a page was capped from here, not only
    from the marker line inside the text."""

    model_config = ConfigDict(extra="forbid")

    url: str = ""
    #: Characters the scraper returned for the page.
    chars_scraped: int = 0
    #: Characters left after the research cleanup (image markup out, repeated links collapsed).
    chars_after_cleanup: int = 0
    #: Characters of page text that reached ``formatted_text`` (the cap marker line not counted).
    chars_kept: int = 0
    #: True when the page was cut to the cap; its block then ends with the
    #: ``[Page capped: N of M characters kept]`` line.
    capped: bool = False


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
    #: One record per included page, in block order: chars scraped / kept and whether it was capped.
    pages: list[CombinedPageRecord] = Field(default_factory=list)
    #: How many included pages were cut to the cap (0 = every page arrived whole).
    capped_pages: int = 0
    #: The per-page cap this run applied.
    max_chars_per_page: int = 0


@declare_action(
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
    doors={"step"},
)
async def ai_util_format_scraped_content(
    app: Any, inputs: FormatScrapedContentInput
) -> FormatScrapedContentOutput:
    from matrx_scraper.features.research_budget import cap_page_text, clean_page_text

    limit = inputs.max_chars_per_page
    if limit is None:
        from matrx_ai.tools.implementations.web import research_budgets

        limit = int((await research_budgets(getattr(app, "organization_id", None))).page_max_chars)
    blocks = []
    sources: list[str] = []
    records: list[CombinedPageRecord] = []
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
            # The research page preparation (matrx_scraper research_budget): cleaned first, so
            # the cap spends on words rather than image markup; a cut keeps the head and says so
            # in the text AND in the page record — never a silent chop of the end.
            cleaned = clean_page_text(content)
            block, capped = cap_page_text(cleaned, limit)
            blocks.append(block)
            # Keep the block, its source and its record index-aligned.
            url = page.get("url") or page.get("response_url")
            sources.append(str(url) if isinstance(url, str) else "")
            records.append(
                CombinedPageRecord(
                    url=sources[-1],
                    chars_scraped=len(content),
                    chars_after_cleanup=len(cleaned),
                    chars_kept=min(len(cleaned), limit),
                    capped=capped,
                )
            )

    if inputs.values and not blocks:
        # Never hand an empty string downstream: it validates fine here and
        # then fails somewhere else entirely. Fail where the truth is.
        detail = (
            f"all {failed_pages} of them failed to load"
            if failed_pages == len(inputs.values)
            else "none of them carried any readable text"
        )
        raise ActionFailed(
            "no_readable_content",
            f"Got {len(inputs.values)} page(s) to combine, but {detail}.",
            details={"page_count": len(inputs.values), "failed_pages": failed_pages},
        )

    # Newlines, not the literal characters \n — this was an escaped string, so
    # every joined block was separated by the visible text "\n---\n".
    formatted_text = "\n---\n".join(blocks)
    return FormatScrapedContentOutput(
            formatted_text=formatted_text,
            sources=sources,
            page_count=len(blocks),
            failed_pages=failed_pages,
            pages=records,
            capped_pages=sum(1 for r in records if r.capped),
            max_chars_per_page=limit,
        )


class CostSummaryInput(BaseModel):
    model_config = ConfigDict(extra="allow")
    conversation_id: str | None = Field(
        default=None,
        description="The conversation ID to get the cost summary for. If not provided, the current app context's conversation ID is used.",
        # IDENTITY (``matrx_graph.types.identity_inputs``): an inherited id
        # would report a DIFFERENT conversation's spend as this step's.
        json_schema_extra=identity_input(),
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


@declare_action(
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
    doors={"step"},
)
async def ai_util_cost_summary(
    app: Any, inputs: CostSummaryInput
) -> CostSummaryOutput:
    conversation_id = inputs.conversation_id or getattr(app, "conversation_id", None)
    if not conversation_id:
        return CostSummaryOutput(
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

    from matrx_ai.db.cx_managers import cxm

    summary = await cxm.get_conversation_cost_summary(conversation_id)
    model_ids = list(summary.models_used)
    return CostSummaryOutput(
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


@declare_action(
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
    doors={"step"},
)
async def ai_util_parse_llm_json(
    app: Any, inputs: ParseLlmJsonInput
) -> ParseLlmJsonOutput:
    _ = app

    from matrx_ai.agents.response_parser import extract_json

    result = extract_json(
        inputs.text,
        schema=inputs.schema_definition or None,
        detailed=True,
    )
    if not result.success or result.data is None:
        raise ActionFailed(
            "parse_failed",
            f"no JSON found in the text: {result.reason}",
            details={"reason": str(result.reason)},
        )
    return ParseLlmJsonOutput(value=result.data)
