"""Scraper actions — typed wrappers over ``matrx_scraper`` public API.

Three actions cover the 80% of scraper use in workflows:

- ``scraper.scrape``       — one URL → structured page
- ``scraper.scrape_many``  — parallel scrape of N URLs with bounded concurrency
- ``scraper.crawl_site``   — BFS crawl of a site, capped at max_pages

Node Result System (docs/workflow/NODE_RESULT_CONTRACT.md): every action
returns ``NodeResult[T]``. ``scraper.scrape`` treats a failed scrape of THE
one URL as a node ``Failure("scrape_failed")`` (with ``details.url`` +
``details.failure_reason``); its success payload ``ScrapedPage`` carries no
``success``/``failure_reason`` fields. ``scrape_many`` / ``crawl_site`` treat
per-page failure as Success DATA — each ``pages[]`` item is a
``ScrapedPageItem`` that keeps per-page ``success`` + ``failure_reason``
(nested, legal — the reserved-field rule is top-level only); only a systemic
failure (the scrape/crawl machinery itself blowing up) is a node Failure.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.actions import ActionFailed, declare_action, register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field


class ScrapedPage(BaseModel):
    """Canonical scraped-page success payload for ``scraper.scrape``.

    Lightweight projection over ``matrx_scraper.ScrapeResult``. Authors
    typically want ``text`` (the cleanest readable form) and optional
    metadata. Failure semantics live in the NodeResult envelope — this
    payload has no ``success``/``failure_reason`` fields.

    Fully closed shape: the only constructor site
    (``_scrape_result_to_page`` + the dump-copy in ``scraper_scrape``)
    passes exactly the declared fields — nothing dynamic is spread in.
    """

    url: str
    response_url: str | None = None
    status_code: int = 0
    title: str | None = None
    published_at: str | None = None
    modified_at: str | None = None
    content_type: str | None = None
    text: str = Field(
        default="",
        description="Best-available readable text: the article body (main content) when the page is article-like, else the full page (ai_research_content \u2192 markdown_renderable \u2192 text_data \u2192 raw_text).",
    )
    markdown: str | None = None
    scraped_at: str | None = None


class ScrapedPageItem(ScrapedPage):
    """Per-page entry inside ``scrape_many``/``crawl_site`` results.

    Partial failure across a batch is Success DATA, so each item keeps its
    own ``success`` flag + ``failure_reason`` (nested fields — the
    reserved-payload-field rule applies to the TOP level of a payload only).
    """

    success: bool = False
    failure_reason: str | None = None
    char_count: int = Field(default=0, description="How many characters of text were read.")
    is_good: bool = Field(
        default=False,
        description="True when the page read and has at least good_min_chars of text "
        "(scrape_many only).",
    )


class ScrapeInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str = Field(
        min_length=1,
        description="Full URL to fetch.",
        json_schema_extra=field_extras(widget="text", placeholder="https://example.com/article"),
    )
    use_proxy: bool = Field(
        default=True,
        description="Route through the scraper's proxy pool. Disable for local/dev.",
        json_schema_extra=field_extras(widget="toggle"),
    )
    fast: bool = Field(
        default=False,
        description="Skip link/hash extraction for speed.",
        json_schema_extra=field_extras(widget="toggle"),
    )


@declare_action(
    name="scraper.scrape",
    display_name="Read a Web Page",
    description="Fetch a web page and return its text and details.",
    category=NodeCategory.IO,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ScrapeInput,
    output_schema=ScrapedPage,
    output_kind="scraped_page",
    icon="globe",
    tags=("scrape", "web", "fetch"),
    doors={"step"},
)
async def scraper_scrape(app: Any, inputs: ScrapeInput) -> ScrapedPage:
    """ONE Action (engine ``code``): a step, and — like every Action — a directive
    (``directive_v1_action_scraper_scrape``). A failed read is ``ActionFailed("scrape_failed")``,
    which the step door turns into the node failure it always was."""
    _ = app
    from matrx_scraper import scrape as raw_scrape

    from matrx_scraper.utils.proxy import redact_url_secrets

    shown = redact_url_secrets(inputs.url)
    try:
        result = await raw_scrape(url=inputs.url, use_proxy=inputs.use_proxy, fast=inputs.fast)
    except Exception as e:
        reason = redact_url_secrets(f"{type(e).__name__}: {e}")
        raise ActionFailed(
            "scrape_failed",
            f"scrape of {shown} raised {reason}",
            details={"url": shown, "failure_reason": reason},
        ) from e
    page = _scrape_result_to_page(result)
    if not page.success:
        reason = redact_url_secrets(page.failure_reason or "unknown failure")
        raise ActionFailed(
            "scrape_failed",
            f"scrape of {shown} failed: {reason}",
            details={"url": shown, "failure_reason": reason},
        )
    return ScrapedPage(**page.model_dump(exclude={"success", "failure_reason", "char_count", "is_good"}))


class ScrapeManyInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    urls: list[str] = Field(
        default_factory=list,
        description="URLs to scrape in parallel.",
        json_schema_extra=field_extras(widget="tag_input"),
    )
    use_proxy: bool = True
    fast: bool = False
    concurrency: int = Field(default=10, ge=1, le=100, description="Max in-flight requests.")
    stop_after_good: int | None = Field(
        default=None,
        ge=1,
        description="Read the links in order, a wave at a time, and stop once this many "
        "good pages are in hand. Empty = read every link.",
    )
    good_min_chars: int = Field(
        default=0,
        ge=0,
        description="A page counts as good when it read and has at least this many characters.",
    )


class ScrapeManyOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pages: list[ScrapedPageItem] = Field(default_factory=list)
    successful: int = 0
    failed: int = 0
    good_pages: list[ScrapedPageItem] = Field(
        default_factory=list,
        description="The good pages, in link order (capped at stop_after_good when set).",
    )
    good: int = 0
    not_attempted: int = Field(
        default=0, description="Links left unread because enough good pages were in hand."
    )


def _is_good(page: ScrapedPageItem, min_chars: int) -> bool:
    return bool(page.success) and len(page.text or "") >= min_chars


@register_node(
    name="scraper.scrape_many",
    display_name="Read Many Web Pages",
    description="Fetch and read many web pages at once.",
    category=NodeCategory.IO,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ScrapeManyInput,
    output_schema=ScrapeManyOutput,
    output_kind="scraper_batch_result",
    icon="globe",
    tags=("scrape", "web", "parallel"),
)
async def scraper_scrape_many(
    ctx: NodeExecutionContext, inputs: ScrapeManyInput
) -> NodeResult[ScrapeManyOutput]:
    _ = ctx
    from matrx_scraper import scrape_many as raw_scrape_many

    if not inputs.urls:
        return success(ScrapeManyOutput())

    target = inputs.stop_after_good
    pages: list[ScrapedPageItem] = []
    good_pages: list[ScrapedPageItem] = []
    cursor = 0
    while cursor < len(inputs.urls):
        # One wave = every remaining link (no target), or exactly as many links as
        # good pages are still missing — the research code path's
        # scrape-until-N loop (research/scraper.py::scrape_keyword_sources).
        wave_size = len(inputs.urls) if target is None else target - len(good_pages)
        wave = inputs.urls[cursor : cursor + wave_size]
        cursor += len(wave)
        try:
            results = await raw_scrape_many(
                urls=wave,
                use_proxy=inputs.use_proxy,
                fast=inputs.fast,
                concurrency=inputs.concurrency,
            )
        except Exception as e:
            # Systemic failure — the batch machinery itself broke, not one page.
            return failure(
                "scrape_failed",
                f"scrape_many of {len(wave)} urls raised {type(e).__name__}: {e}",
            )
        for page in (_scrape_result_to_page(r) for r in results):
            page.is_good = _is_good(page, inputs.good_min_chars)
            pages.append(page)
            if page.is_good and (target is None or len(good_pages) < target):
                good_pages.append(page)
        if target is not None and len(good_pages) >= target:
            break
    successful = sum(1 for p in pages if p.success)
    return success(
        ScrapeManyOutput(
            pages=pages,
            successful=successful,
            failed=len(pages) - successful,
            good_pages=good_pages,
            good=len(good_pages),
            not_attempted=len(inputs.urls) - cursor,
        )
    )


class CrawlSiteInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    seed_url: str = Field(
        min_length=1,
        description="Starting URL for the crawl.",
        json_schema_extra=field_extras(widget="text"),
    )
    max_pages: int = Field(
        default=50,
        ge=1,
        le=1000,
        description="Hard cap on pages fetched.",
    )
    concurrency: int = Field(default=10, ge=1, le=50)
    # NO use_proxy: the crawler has no proxy switch. The field existed here and
    # was passed straight through to `crawl_site()`, which made EVERY crawl a
    # TypeError -> failure("crawl_failed"). Never add it back without a
    # parameter on the engine to receive it (AD191).
    include_patterns: list[str] = Field(
        default_factory=list,
        description=(
            "If set, only URLs whose path matches one of these regular expressions "
            "are crawled. Matched anywhere in the path, not anchored — '/blog' also "
            "matches '/news/blog'. Use '^/blog' to match a prefix."
        ),
    )
    exclude_patterns: list[str] = Field(
        default_factory=list,
        description=(
            "URLs whose path matches one of these regular expressions are skipped. "
            "Applied before include_patterns. Same unanchored matching."
        ),
    )


class CrawlSiteOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seed_url: str
    pages: list[ScrapedPageItem] = Field(default_factory=list)
    total_pages: int = 0


@register_node(
    name="scraper.crawl_site",
    display_name="Explore a Website",
    description="Follow links across a website and read its pages, up to a limit.",
    category=NodeCategory.IO,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=CrawlSiteInput,
    output_schema=CrawlSiteOutput,
    output_kind="scraper_crawl_result",
    icon="compass",
    tags=("scrape", "web", "crawl"),
)
async def scraper_crawl_site(
    ctx: NodeExecutionContext, inputs: CrawlSiteInput
) -> NodeResult[CrawlSiteOutput]:
    _ = ctx
    from matrx_scraper import crawl_site as raw_crawl_site

    try:
        raw = await raw_crawl_site(
            seed_url=inputs.seed_url,
            max_pages=inputs.max_pages,
            concurrency=inputs.concurrency,
            include_patterns=inputs.include_patterns or None,
            exclude_patterns=inputs.exclude_patterns or None,
        )
    except Exception as e:
        # Systemic failure — the crawler itself broke, not one page.
        return failure(
            "crawl_failed",
            f"crawl of {inputs.seed_url} raised {type(e).__name__}: {e}",
        )
    pages = [_scrape_result_to_page(r) for r in (raw or {}).values()]
    return success(CrawlSiteOutput(seed_url=inputs.seed_url, pages=pages, total_pages=len(pages)))


def _scrape_result_to_page(result: Any) -> ScrapedPageItem:
    """Defensive projection over ScrapeResult → ScrapedPageItem.

    ``text`` is the most useful field for downstream LLM nodes. The scraper
    has several candidates depending on pipeline options — prefer the
    richest one that's populated.
    """
    get = _getter(result)
    text = (
        # THE MAIN-CONTENT LAW (parser/main_content.py): the article body first
        # — an LLM node handed the whole page learns the site's furniture.
        get("main_content_text")
        or get("ai_research_content")
        or get("ai_content")
        or get("markdown_renderable")
        or get("text_data")
        or get("raw_text")
        or ""
    )
    return ScrapedPageItem(
        url=str(get("url") or ""),
        response_url=get("response_url"),
        success=bool(get("success") or False),
        status_code=int(get("status_code") or 0),
        title=get("title"),
        published_at=get("published_at"),
        modified_at=get("modified_at"),
        content_type=get("content_type"),
        text=str(text or ""),
        char_count=len(str(text or "")),
        markdown=get("markdown_renderable"),
        failure_reason=get("failure_reason"),
        scraped_at=get("scraped_at"),
    )


def _getter(result: Any):
    """Access-agnostic getter — works for dataclass instances and plain dicts."""
    if isinstance(result, dict):

        def g(key: str):
            return result.get(key)
    else:

        def g(key: str):
            return getattr(result, key, None)

    return g
