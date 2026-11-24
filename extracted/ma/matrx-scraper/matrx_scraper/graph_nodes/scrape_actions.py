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

from matrx_graph.actions import ActionFailed, declare_action

from typing import Any, Literal

from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue


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


#: How much text a page judge reads: the head every wall, block, consent overlay and 404 announces itself in.
HEAD_CHARS = 6000


class RuleWall(BaseModel):
    """One wall the scraper's rule judge (``matrx_scraper.read_judge.judge_read``) names on a read: a FACT about
    the page (a bot check, a sign-in wall, an error status, an unrendered app shell, an empty page, a page that
    says it does not exist). What a wall means for the caller is the caller's rule, never this Action's."""

    model_config = ConfigDict(extra="forbid")

    kind: str = Field(
        description="challenge | http_error | empty | js_shell | sign_in_wall | not_found | fetch_error "
        "(read_judge's closed vocabulary)."
    )
    detail: str = Field(default="", description="Plain words plus the specific signal seen.")
    coverable: bool = Field(
        default=True, description="False when the page is missing everywhere (HTTP 404 / 410): no other reader finds it."
    )


class ScrapedPageFacts(ScrapedPage):
    """``scraper.scrape``'s payload: the page, plus the facts a workflow step judges it by. No verdict: whether
    the page is good, worth a browser retry or worth keeping is a step's rule (research/FEATURE.md § Actions a research workflow may run)."""

    model_config = ConfigDict(extra="forbid")

    read: bool = Field(
        default=True,
        description="True when the scraper produced a page; False (only with when_unread = facts) when it did not.",
    )
    failure_reason: str | None = Field(default=None, description="The scraper's own reason when read is False.")
    mode: Literal["auto", "browser"] = Field(default="auto", description="How the page was asked for.")
    engine: str | None = Field(default=None, description="Which engine produced the page (http, browser, ...).")
    char_count: int = Field(default=0, description="Characters of text.")
    main_text: str | None = Field(
        default=None,
        description="The host's main text: its site-rules CSS selector run over the page. Empty when the host "
        "has no selector or there was no HTML.",
    )
    main_text_chars: int | None = Field(
        default=None, description="Characters of main_text; empty when the host has no selector or no HTML."
    )
    main_text_selector: str | None = Field(default=None, description="The host's selector that produced main_text.")
    host_category: str | None = Field(default=None, description="The host's site-rules category (e.g. gated_login).")
    links: list[str] = Field(default_factory=list, description="Page links: internal, then external.")
    media: list[str] = Field(
        default_factory=list, description="Media the page links: images, videos, audio, documents."
    )
    rule_walls: list[RuleWall] = Field(
        default_factory=list, description="Walls the rule judge names on this read (empty when it names none)."
    )
    head_walls: list[RuleWall] = Field(
        default_factory=list,
        description="Walls the rule judge names reading only the status, the title and the first 6,000 characters "
        "of text (no HTML, no fetch failure): the facts a page judge sees.",
    )
    min_content_chars: int | None = Field(
        default=None, description="The host's minimum characters of text (site rules); empty when it sets none."
    )
    min_real_content_chars: int | None = Field(
        default=None, description="The host's minimum characters of main text (site rules); empty when it sets none."
    )
    policy_action: str | None = Field(
        default=None, description="The host's site-rules action (block, force_l3, force_l4) when it has one."
    )
    policy_pattern: str | None = Field(default=None, description="The site-rules pattern that matched this url.")
    ai_text: str = Field(
        default="", description="The page's text written for an AI reader (the parse's ai_research_content, else ai_content)."
    )
    ai_text_with_images: str = Field(
        default="",
        description="The same text with the page's images written in (the parse's ai_research_with_images, else "
        "ai_text): what a browser capture stores as its content.",
    )
    link_records: list[dict[str, JsonValue]] = Field(
        default_factory=list, description="Every link as {url, text, is_internal}: external first, then internal."
    )
    image_records: list[dict[str, JsonValue]] = Field(
        default_factory=list,
        description="Every image as {src, alt, caption, width, height, title, srcset}; inline data: images dropped.",
    )
    video_records: list[dict[str, JsonValue]] = Field(default_factory=list, description="The page's <video> tags as parsed.")
    audio_records: list[dict[str, JsonValue]] = Field(default_factory=list, description="The page's <audio> tags as parsed.")
    iframe_srcs: list[str] = Field(
        default_factory=list,
        description="Every <iframe> src of the page's HTML, in page order (embedded players), so a later step needs "
        "these and never the HTML.",
    )
    dates: dict[str, str | None] = Field(
        default_factory=dict,
        description="For each name in date_candidates: the first candidate that is a real ISO date (trimmed, as "
        "given), else empty.",
    )
    page: dict[str, JsonValue] | None = Field(
        default=None,
        description="The whole parse (with url, title and raw HTML), kept on the server in this run: only its "
        "reference travels. Hand it to sources.land so the page lands exactly as every scraped page does. Empty "
        "unless hold_page_in_run is given and the page was parsed.",
    )


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
    mode: Literal["auto", "browser"] = Field(
        default="auto",
        description="auto: the scraper's own ladder (HTTP first, a browser when it is blocked). browser: render "
        "the page in a browser from the start.",
        json_schema_extra=field_extras(widget="select"),
    )
    when_unread: Literal["fail", "facts"] = Field(
        default="fail",
        description="fail: a page that could not be read fails the step. facts: it returns read = false with the "
        "failure reason, status and rule walls, so a later step decides what to do.",
        json_schema_extra=field_extras(widget="select"),
    )
    host_interval_seconds: float = Field(
        default=2.0,
        ge=0,
        le=60,
        description="Seconds between two reads of the same host (measured from the end of the last one). "
        "Different hosts are never held.",
    )
    skip_policy_actions: list[str] = Field(
        default_factory=list,
        description="Site-rule actions (block, force_l3, force_l4) that mean: do not fetch. Such a url comes back "
        "unread (read false) with the host's rule facts, and nothing is fetched.",
    )
    hold_page_in_run: str | None = Field(
        default=None,
        description='This run\'s id ({"$run": "id"}). When given, the whole parse is kept on the server in this run '
        "and returned as a reference in page (for sources.land).",
    )
    host_interval_jitter_seconds: float = Field(
        default=0.75,
        ge=0,
        le=30,
        description="Up to this many extra seconds, at random, on top of the host interval.",
    )
    html: str | None = Field(
        default=None,
        description="The page's HTML already in hand (a browser capture of url). When given, nothing is fetched: "
        "the scraper's own parse reads this HTML as the page at url, and every fact comes from it (engine "
        "'supplied'). Empty HTML is an unread page.",
        json_schema_extra=field_extras(widget="textarea"),
    )
    title: str | None = Field(
        default=None, description="With html: the page's title as captured (else the parse finds one)."
    )
    date_candidates: dict[str, list[str | None]] = Field(
        default_factory=dict,
        description="Dates found beside the page, by name, in the order to try (e.g. published_at: the page's "
        "published_time, then each JSON-LD datePublished). dates answers the first of each that is a real ISO date.",
    )
    head_reads: Literal["fetch", "capture"] = Field(
        default="fetch",
        description="What head_walls judges. fetch: the response status and the page's plain text. capture: what a "
        "browser capture stores (the text with its images written in) and no status, since nothing was fetched.",
        json_schema_extra=field_extras(widget="select"),
    )


#: One per-host pacer for every ``scraper.scrape`` step in this process: same-host reads serialize, separated by
#: the step's host interval; a 429 / 503 seen here (or by the crawler, through the shared throttle memory) widens
#: the gap. The token bucket is generous so the end-gap is what paces (research/scraper.py's pacer, same values).
_host_pacer: Any = None


def _pacer() -> Any:
    global _host_pacer
    if _host_pacer is None:
        from matrx_scraper.rate_limiter import HostRateLimiter

        _host_pacer = HostRateLimiter(default_rps=2.0, default_burst=4.0, max_wait_seconds=30.0)
    return _host_pacer


def _list_of_str(value: Any) -> list[str]:
    return [str(v) for v in value if v] if isinstance(value, list | tuple | set) else []


def has_browser_lane() -> bool:
    from matrx_scraper.browser_lane import has_browser_lane as _has

    return _has()


async def _render_in_lane(inputs: ScrapeInput) -> Any:
    """One render in the host's browser lane, parsed like any fetch (``orchestrator._build_result_from_response``)."""
    from matrx_scraper.browser_lane import render_in_browser_lane
    from matrx_scraper.cpu_lane import run_cpu
    from matrx_scraper.orchestrator import _build_result_from_response

    response = await render_in_browser_lane(inputs.url, trigger="step")
    if response is None:
        return {"url": inputs.url, "success": False, "failure_reason": "browser_render_miss", "engine": "browser_lane"}
    # The parse is seconds of BeautifulSoup/lxml CPU: off the loop, like every other fetch's parse (live 2026-11-19: a
    # rendered page parsed here froze the whole API process ~2.2 s, event_loop_stall in workflow_step:thin_rescue).
    result = await run_cpu(_build_result_from_response, response, inputs.fast)
    result.engine = "browser_lane"
    return result


async def _held_page(app: Any, inputs: ScrapeInput, page: ScrapedPageItem, parsed: Any, raw_html: str | None) -> Any:
    """The parse as research lands it (``research_page_landing``: the parse, the url asked for, the served url, the
    title, the raw HTML), stored once in the run's value store; the reference is what travels."""
    import json

    from matrx_graph.checkpoint.value_store import hold_on_server

    whole = dict(parsed) if isinstance(parsed, dict) else (parsed.to_dict() if hasattr(parsed, "to_dict") else vars(parsed))
    whole = {
        **whole,
        "url": inputs.url,
        "response_url": page.response_url or inputs.url,
        "title": page.title or whole.get("title"),
        **({"raw_html": raw_html} if raw_html else {}),
    }
    whole = json.loads(json.dumps(whole, default=str))
    org = getattr(app, "organization_id", None)
    return await hold_on_server(str(inputs.hold_page_in_run), whole, organization_id=str(org) if org else None)


async def _page_facts(result: Any, inputs: ScrapeInput, page: ScrapedPageItem, app: Any = None) -> ScrapedPageFacts:
    """The facts beside the page: host main text, links, media and the rule judge's walls (never a verdict)."""
    from matrx_scraper import site_rules
    from matrx_scraper.read_judge import judge_read

    get = _getter(result)
    policy = await site_rules.resolve(inputs.url)
    selector = policy.content_selector
    main = site_rules.main_text(get("raw_html"), selector)
    buckets = get("links") if isinstance(get("links"), dict) else {}
    verdict = judge_read(
        status=page.status_code or None,
        text=page.text,
        html=get("raw_html"),
        title=page.title,
        fetch_failure=None if page.success else page.failure_reason,
    )
    walls = (
        [RuleWall(kind=str(verdict.reason), detail=verdict.detail, coverable=verdict.coverable)]
        if verdict.failed and verdict.reason
        else []
    )
    from matrx_scraper.page_records import iframe_sources, page_records, page_text

    # Research's own read re-parses the page's HTML (research/scraper.py _extract_html_payload); the records
    # and the AI text come from that same parse here, so a workflow saves exactly what the code saves.
    raw_html = get("raw_html")
    is_html = "html" in str(page.content_type or "html").lower()
    # An empty_content read answered HTML with no words (an app shell): research keeps it as a read with its links,
    # so it is parsed like a read page. Any other failure (a bot wall's HTML) is not a page and gets no records.
    from matrx_scraper.content_sanity import EMPTY_CONTENT

    parse_it = page.success or page.failure_reason == EMPTY_CONTENT
    if parse_it and is_html and raw_html:
        from matrx_scraper.parser.core import parse_html

        parsed = await parse_html(raw_html, page.response_url or inputs.url)
        ai_text = page_text(parsed)
        with_images = str(parsed.get("ai_research_with_images") or "") if isinstance(parsed, dict) else ""
        links, images, videos, audios, _ = page_records(parsed)
        iframes = iframe_sources(raw_html)
        held = await _held_page(app, inputs, page, parsed, raw_html) if inputs.hold_page_in_run else None
    else:
        ai_text = page.text if page.success else ""
        with_images = ""
        links, images, videos, audios = [], [], [], []
        iframes = []
        held = None
    if inputs.head_reads == "capture":
        # A browser capture is judged as research's extension door judges it (research/domain_policy._rule_verdict over
        # build_capture_offer): the stored text, images written in, and no HTTP status.
        head = judge_read(status=None, text=(with_images or ai_text or "")[:HEAD_CHARS], title=page.title)
    else:
        head = judge_read(status=page.status_code or None, text=(page.text or "")[:HEAD_CHARS], title=page.title)
    head_walls = (
        [RuleWall(kind=str(head.reason), detail=head.detail, coverable=head.coverable)]
        if head.failed and head.reason
        else []
    )
    return ScrapedPageFacts(
        **page.model_dump(exclude={"success", "failure_reason", "char_count", "is_good"}),
        read=bool(page.success),
        failure_reason=None if page.success else page.failure_reason,
        mode=inputs.mode,
        engine=get("engine"),
        char_count=page.char_count,
        main_text=main if main is not None else None,
        main_text_chars=len(main) if main is not None else None,
        main_text_selector=selector if main is not None else None,
        host_category=policy.category,
        links=_list_of_str(buckets.get("internal")) + _list_of_str(buckets.get("external")),
        media=[u for k in ("images", "videos", "audio", "documents") for u in _list_of_str(buckets.get(k))],
        rule_walls=walls,
        head_walls=head_walls,
        min_content_chars=policy.min_content_chars,
        min_real_content_chars=policy.min_real_content_chars,
        policy_action=policy.policy_action,
        policy_pattern=policy.matched_pattern,
        ai_text=ai_text,
        ai_text_with_images=with_images or ai_text,
        link_records=links,
        image_records=images,
        video_records=videos,
        audio_records=audios,
        iframe_srcs=iframes,
        page=held,
        dates={name: first_iso_date(candidates) for name, candidates in inputs.date_candidates.items()},
    )


def valid_iso_date(value: Any) -> str | None:
    """``value`` trimmed when it is a real ISO date (``datetime.fromisoformat``; a trailing ``Z`` read as UTC), else
    None. The one date rule for a page's untrusted dates (research's extension door stores what this answers)."""
    from datetime import datetime

    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError:
        return None
    return text


def first_iso_date(candidates: list[str | None]) -> str | None:
    return next((d for d in (valid_iso_date(c) for c in candidates) if d), None)


@declare_action(
    name="scraper.scrape",
    display_name="Read a Web Page",
    description="Fetch a web page (or read HTML already captured) and return its text and details.",
    category=NodeCategory.IO,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ScrapeInput,
    output_schema=ScrapedPageFacts,
    # No curated kind: ``scraped_page`` is the distilled page record (links as objects, no facts), so
    # declaring it made every live run fail kind enforcement ("Additional properties are not allowed").
    icon="globe",
    tags=("scrape", "web", "fetch"),
    doors={"step"},
)
async def scraper_scrape(app: Any, inputs: ScrapeInput) -> ScrapedPageFacts:
    """ONE Action (engine ``code``): a step, and — like every Action — a directive
    (``directive_v1_action_scraper_scrape``). A failed read is ``ActionFailed("scrape_failed")``,
    which the step door turns into the node failure it always was — unless ``when_unread = facts``,
    which returns the failed read's facts instead. Same-host reads are paced (``host_interval_seconds``)."""
    _ = app
    from matrx_scraper import scrape as raw_scrape
    from matrx_scraper.scraper import RequestType

    from matrx_scraper.utils.proxy import redact_url_secrets

    shown = redact_url_secrets(inputs.url)
    if inputs.skip_policy_actions:
        from matrx_scraper import site_rules

        policy = await site_rules.resolve(inputs.url)
        if policy.policy_action and policy.policy_action in inputs.skip_policy_actions:
            # Not read, on purpose: the host's site rule says so. Facts only; nothing was fetched.
            return ScrapedPageFacts(
                url=inputs.url, read=False, mode=inputs.mode, failure_reason=f"policy:{policy.policy_action}",
                host_category=policy.category, min_content_chars=policy.min_content_chars,
                min_real_content_chars=policy.min_real_content_chars, policy_action=policy.policy_action,
                policy_pattern=policy.matched_pattern,
            )
    if inputs.html is not None:
        # A capture already in hand: the scraper's own read of it, nothing fetched, no host pacing.
        from matrx_scraper.orchestrator import scrape_supplied_html

        result = await scrape_supplied_html(inputs.url, inputs.html, title=inputs.title, fast=inputs.fast)
        page = _scrape_result_to_page(result)
        if not page.success and inputs.when_unread == "fail":
            raise ActionFailed(
                "scrape_failed",
                f"the supplied page {shown} could not be read: {page.failure_reason or 'unknown failure'}",
                details={"url": shown, "failure_reason": page.failure_reason or "unknown failure"},
            )
        return await _page_facts(result, inputs, page, app)
    request_type = RequestType.BROWSER if inputs.mode == "browser" else RequestType.NORMAL
    pacer = _pacer()
    try:
        async with pacer.slot(
            inputs.url, min_interval=inputs.host_interval_seconds, jitter=inputs.host_interval_jitter_seconds
        ):
            if inputs.mode == "browser" and has_browser_lane():
                # The host's browser lane (the scraper service's pooled browser) — the same render research's
                # own rescue takes. A miss is an unread page, never a local browser this host does not have.
                result = await _render_in_lane(inputs)
            else:
                result = await raw_scrape(
                    url=inputs.url, use_proxy=inputs.use_proxy, fast=inputs.fast, request_type=request_type
                )
        pacer.observe_status(inputs.url, _getter(result)("status_code"))
    except Exception as e:
        reason = redact_url_secrets(f"{type(e).__name__}: {e}")
        raise ActionFailed(
            "scrape_failed",
            f"scrape of {shown} raised {reason}",
            details={"url": shown, "failure_reason": reason},
        ) from e
    page = _scrape_result_to_page(result)
    if not page.success and inputs.when_unread == "fail":
        reason = redact_url_secrets(page.failure_reason or "unknown failure")
        raise ActionFailed(
            "scrape_failed",
            f"scrape of {shown} failed: {reason}",
            details={"url": shown, "failure_reason": reason},
        )
    if not page.success:
        page.failure_reason = redact_url_secrets(page.failure_reason or "unknown failure")
    return await _page_facts(result, inputs, page, app)


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


@declare_action(
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
    doors={"step"},
)
async def scraper_scrape_many(
    app: Any, inputs: ScrapeManyInput
) -> ScrapeManyOutput:
    _ = app
    from matrx_scraper import scrape_many as raw_scrape_many

    if not inputs.urls:
        return ScrapeManyOutput()

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
            raise ActionFailed(
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
    return ScrapeManyOutput(
            pages=pages,
            successful=successful,
            failed=len(pages) - successful,
            good_pages=good_pages,
            good=len(good_pages),
            not_attempted=len(inputs.urls) - cursor,
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


@declare_action(
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
    doors={"step"},
)
async def scraper_crawl_site(
    app: Any, inputs: CrawlSiteInput
) -> CrawlSiteOutput:
    _ = app
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
        from matrx_scraper.utils.proxy import redact_url_secrets

        raise ActionFailed(
            "crawl_failed",
            f"crawl of {redact_url_secrets(inputs.seed_url)} raised "
            f"{redact_url_secrets(f'{type(e).__name__}: {e}')}",
        ) from e
    pages = [_scrape_result_to_page(r) for r in (raw or {}).values()]
    return CrawlSiteOutput(seed_url=inputs.seed_url, pages=pages, total_pages=len(pages))


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
