"""
Streaming scrape endpoints — quick-scrape, search, search-and-scrape.

Depends on: matrx_connect (AppContext, context_dep, Emitter, create_streaming_response)
"""

from __future__ import annotations

import logging
import traceback
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from matrx_connect import AppContext, Emitter, context_dep
from matrx_connect.streaming import create_streaming_response
from matrx_connect.context.events import InfoPayload
from matrx_scraper.service import ScrapeOptions, ScrapeService

logger = logging.getLogger(__name__)

router = APIRouter()

# /browser-fetch limits — CAPS constants, never env vars. The timeout ceiling
# bounds how long one caller can hold a pooled browser; the char cap bounds the
# response a caller (and the parser downstream) has to hold in memory.
BROWSER_FETCH_DEFAULT_TIMEOUT_MS = 25_000
BROWSER_FETCH_MAX_HTML_CHARS = 5_000_000
# /browser-inspect: each device profile in `kinds` costs its own navigation and
# its own pooled-browser hold, so the count is capped rather than free-form.
BROWSER_INSPECT_MAX_KINDS = 6
# `/page-capture` returns analysis-grade text, not raw HTML. The durable cache
# keeps the complete parsed result; this cap only bounds the synchronous wire
# response consumed by aidream's backlink enrichment batch.
PAGE_CAPTURE_MAX_TEXT_CHARS = 80_000
PAGE_CAPTURE_MAX_MATCHED_LINKS = 50


class ScrapeOptionsBase(BaseModel):
    get_organized_data: bool = Field(default=False)
    get_structured_data: bool = Field(default=False)
    get_overview: bool = Field(default=False)
    get_text_data: bool = Field(default=True)
    get_main_image: bool = Field(default=False)
    get_links: bool = Field(default=False)
    get_content_filter_removal_details: bool = Field(default=False)
    include_highlighting_markers: bool = Field(default=True)
    include_media: bool = Field(default=True)
    include_media_links: bool = Field(default=True)
    include_media_description: bool = Field(default=True)
    include_anchors: bool = Field(default=True)
    anchor_size: int = Field(default=100, ge=10, le=1000)


class QuickScrapeRequest(ScrapeOptionsBase):
    urls: list[str] = Field(...)
    use_cache: bool = Field(default=True)
    stream: bool = Field(default=False)


class PageCaptureRequest(BaseModel):
    """One cache-backed parsed page capture for server-side enrichment."""

    url: str
    target_url: str | None = None
    use_cache: bool = True
    capture_screenshot: bool = False
    organization_id: str | None = None
    site_id: str | None = None
    backlink_id: str | None = None


class CapturedLink(BaseModel):
    """One anchor on the captured page pointing at the requested target.

    Key names match ``LinkExtractor.extract_anchors`` / ``seo_audit.LinkItem``
    / the ``crawl_links`` rows, so every consumer reads one vocabulary.
    """

    target_url: str
    anchor_text: str = ""
    text_source: Literal["anchor", "image_alt", ""] = ""
    rel: str | None = None
    nofollow: bool = False
    link_type: Literal["internal", "subdomain", "external"] = "external"
    region: str = "body"


class PageCaptureResult(BaseModel):
    success: bool
    status_code: int = 0
    final_url: str
    title: str | None = None
    content_type: str = ""
    scraped_at: str | None = None
    published_at: str | None = None
    modified_at: str | None = None
    cms: str | None = None
    cache_key: str
    from_cache: bool = False
    char_count: int = 0
    content: str = ""
    content_truncated: bool = False
    links_to_target: list[CapturedLink] = Field(default_factory=list)
    screenshot_file_id: str | None = None
    screenshot_width: int | None = None
    screenshot_height: int | None = None
    screenshot_kind: str | None = None
    screenshot_highlighted: bool = False
    screenshot_failure_reason: str | None = None
    failure_reason: str | None = None
    failure_details: list[dict[str, str]] = Field(default_factory=list)


def _highlight_target_link_script(target_url: str) -> str:
    """Programmatic browser action that focuses and marks matching anchors."""

    import json

    encoded_target = json.dumps(target_url)
    return rf"""
(() => {{
  const target = new URL({encoded_target}, document.baseURI);
  const canonical = (value) => {{
    const url = new URL(value, document.baseURI);
    const host = url.hostname.toLowerCase().replace(/^www\./, "");
    const path = url.pathname === "/" ? "/" : url.pathname.replace(/\/+$/, "");
    const query = [...url.searchParams.entries()]
      .sort(([ak, av], [bk, bv]) => ak.localeCompare(bk) || av.localeCompare(bv));
    return `${{host}}${{url.port ? `:${{url.port}}` : ""}}${{path}}?${{new URLSearchParams(query)}}`;
  }};
  const expected = canonical(target.href);
  const matches = [...document.querySelectorAll("a[href]")]
    .filter((anchor) => {{
      try {{ return canonical(anchor.href) === expected; }} catch {{ return false; }}
    }});
  for (const anchor of matches) {{
    anchor.style.setProperty("outline", "4px solid #f59e0b", "important");
    anchor.style.setProperty("outline-offset", "4px", "important");
    anchor.style.setProperty("background", "rgba(245, 158, 11, 0.24)", "important");
    anchor.style.setProperty("box-shadow", "0 0 0 8px rgba(245, 158, 11, 0.14)", "important");
    anchor.style.setProperty("border-radius", "3px", "important");
    anchor.dataset.matrxBacklinkEvidence = "true";
  }}
  if (matches[0]) matches[0].scrollIntoView({{ block: "center", inline: "center" }});
  document.documentElement.dataset.matrxBacklinkMatches = String(matches.length);
}})()
"""


async def _capture_backlink_screenshot(
    *,
    request: PageCaptureRequest,
    target_url: str,
    ctx: AppContext,
) -> dict[str, object]:
    """Render, highlight, and store one human-review screenshot, best effort."""

    from uuid import uuid4

    from matrx_files import SCRAPER, FileManager
    from matrx_files.service import FileService
    from matrx_scraper._ext import get_ext, has_ext
    from matrx_scraper.recipe_runtime import execute_directives
    from matrx_scraper.recipes import RecipeAction
    from matrx_scraper.utils.url import validate_public_http_url

    if not request.capture_screenshot:
        return {}
    if not (request.organization_id and request.site_id and request.backlink_id and ctx.user_id):
        return {
            "screenshot_failure_reason": (
                "screenshot context is incomplete; organization, site, backlink, "
                "and authenticated user identities are required"
            )
        }
    if not has_ext("browser_pool") or not has_ext("file_manager"):
        return {"screenshot_failure_reason": "browser or canonical file pipeline is unavailable"}

    try:
        rendered = await get_ext("browser_pool").fetch_with_capture(
            target_url,
            screenshot_kinds=["viewport_desktop"],
            recipe_actions=[
                RecipeAction(
                    type="evaluate",
                    script=_highlight_target_link_script(request.target_url or ""),
                )
            ],
            action_runner=execute_directives,
            preserve_scroll=True,
        )
        await validate_public_http_url(rendered.response_url or target_url)
        if not rendered.screenshots:
            reason = (
                rendered.screenshot_failures[0].error_message
                if rendered.screenshot_failures
                else "browser returned no screenshot"
            )
            return {"screenshot_failure_reason": reason}
        shot = rendered.screenshots[0]
        import re

        highlighted_match = re.search(r'data-matrx-backlink-matches="(\d+)"', rendered.content)
        highlighted_count = int(highlighted_match.group(1)) if highlighted_match else 0
        capture_id = str(uuid4())
        file_path = SCRAPER.path(
            "seo",
            request.site_id,
            "backlinks",
            request.backlink_id,
            f"{capture_id}-link-evidence.png",
        )
        file_manager: FileManager = get_ext("file_manager")
        upload = await FileService(file_manager).upload_with_intent(
            shot.bytes,
            intent="force_new_copy",
            file_path=file_path,
            owner_id=ctx.user_id,
            organization_id=request.organization_id,
            mime_type="image/png",
            visibility="internal",
            change_summary="Backlink source-page link evidence",
            metadata={
                "organization_id": request.organization_id,
                "system_artifact": True,
                "system_immutable": True,
                "artifact_domain": "seo_backlink",
                "artifact_kind": "screenshot:link_evidence",
                "site_id": request.site_id,
                "backlink_id": request.backlink_id,
                "capture_id": capture_id,
                "target_url": request.target_url,
            },
            reason="Backlink evidence captures are immutable observations",
            auto_thumbnail=False,
            auto_rekey=False,
        )
        return {
            "screenshot_file_id": str(upload["file_id"]),
            "screenshot_width": shot.width,
            "screenshot_height": shot.height,
            "screenshot_kind": "link_evidence",
            "screenshot_highlighted": highlighted_count > 0,
        }
    except Exception as exc:
        logger.warning("backlink screenshot failed for %s: %s", target_url, exc, exc_info=True)
        return {"screenshot_failure_reason": f"{type(exc).__name__}: {exc}"}


@router.post(
    "/page-capture",
    summary="Capture and parse one public page into the durable scrape cache",
    response_model=PageCaptureResult,
)
async def page_capture(
    request: PageCaptureRequest,
    ctx: AppContext = Depends(context_dep),
) -> PageCaptureResult:
    """The non-streaming server primitive for backlink/source enrichment.

    Unlike ``/quick-scrape`` this endpoint returns one typed result and always
    routes successful pages through the package's two-tier cache. It exposes
    bounded analysis text and only the link records matching ``target_url``;
    the complete parsed artifact remains in ``scraper.scrape_parsed_page``.
    """

    from matrx_scraper._ext import get_ext, has_ext
    from matrx_scraper.orchestrator import scrape
    from matrx_scraper.utils.url import get_url_info, normalize_url, validate_public_http_url

    try:
        target_url = await validate_public_http_url(request.url)
    except Exception as exc:
        logger.info("page-capture rejected %r: %s", request.url, exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="url must be a publicly routable http(s) address",
        )

    cache = get_ext("cache")
    cache_key = get_url_info(target_url).unique_page_name
    from_cache = request.use_cache and await cache.get(cache_key) is not None
    result = await scrape(
        target_url,
        use_proxy=True,
        cache=cache if request.use_cache else None,
        domain_config=get_ext("domain_config"),
        browser_pool=get_ext("browser_pool") if has_ext("browser_pool") else None,
    )
    final_url = result.response_url or target_url
    try:
        await validate_public_http_url(final_url)
    except Exception as exc:
        logger.warning(
            "page-capture discarded a non-public final url (%s -> redacted): %s",
            target_url,
            exc,
        )
        return PageCaptureResult(
            success=False,
            final_url=target_url,
            cache_key=cache_key,
            failure_reason="navigation ended on a non-public address; response discarded",
        )

    text = (
        result.ai_research_content or result.text_data or result.ai_content or result.raw_text or ""
    )
    content_truncated = len(text) > PAGE_CAPTURE_MAX_TEXT_CHARS
    content = text[:PAGE_CAPTURE_MAX_TEXT_CHARS]
    normalized_target = normalize_url(request.target_url) if request.target_url else ""
    matching: list[CapturedLink] = []
    if normalized_target:
        for record in result.link_records or []:
            raw_candidate = str(record.get("target_url") or "")
            candidate = normalize_url(raw_candidate) if raw_candidate else ""
            if candidate == normalized_target:
                matching.append(CapturedLink.model_validate(record))
                if len(matching) >= PAGE_CAPTURE_MAX_MATCHED_LINKS:
                    break

    screenshot = await _capture_backlink_screenshot(
        request=request,
        target_url=target_url,
        ctx=ctx,
    )

    return PageCaptureResult(
        success=result.success,
        status_code=result.status_code,
        final_url=final_url,
        title=result.title,
        content_type=result.content_type,
        scraped_at=result.scraped_at,
        published_at=result.published_at,
        modified_at=result.modified_at,
        cms=result.cms,
        cache_key=cache_key,
        from_cache=from_cache,
        char_count=len(text),
        content=content,
        content_truncated=content_truncated,
        links_to_target=matching,
        **screenshot,
        failure_reason=result.failure_reason,
        failure_details=result.failure_details,
    )


class SearchKeywordsRequest(BaseModel):
    keywords: list[str] = Field(...)
    country_code: str = Field(default="all")
    total_results_per_keyword: int = Field(default=5, ge=1, le=100)
    search_type: str = Field(default="all")


class SearchAndScrapeRequest(ScrapeOptionsBase):
    keywords: list[str] = Field(...)
    country_code: str = Field(default="all")
    total_results_per_keyword: int = Field(default=10, ge=10, le=30)
    search_type: str = Field(default="all")


class SearchAndScrapeLimitedRequest(ScrapeOptionsBase):
    keyword: str = Field(...)
    country_code: str = Field(default="all")
    max_page_read: int = Field(default=10, ge=1, le=20)
    search_type: str = Field(default="all")


def _build_options(opts: ScrapeOptionsBase) -> ScrapeOptions:
    return ScrapeOptions(
        get_organized_data=opts.get_organized_data,
        get_structured_data=opts.get_structured_data,
        get_overview=opts.get_overview,
        get_text_data=opts.get_text_data,
        get_main_image=opts.get_main_image,
        get_links=opts.get_links,
        get_content_filter_removal_details=opts.get_content_filter_removal_details,
        include_highlighting_markers=opts.include_highlighting_markers,
        include_media=opts.include_media,
        include_media_links=opts.include_media_links,
        include_media_description=opts.include_media_description,
        include_anchors=opts.include_anchors,
        anchor_size=opts.anchor_size,
    )


class BrowserFetchRequest(BaseModel):
    """One-shot browser-rendered fetch of a single URL.

    The stateless sibling of the /browser/* session API: no session to create
    or close, no DOM automation — render the page in the pooled headless
    Chromium and return the post-JS HTML. This is the remote escalation path
    for Chromium-less hosts (aidream runs no browser by design; see its
    Dockerfile note): when a plain HTTP fetch is blocked or returns a JS
    shell, the host calls this instead of failing the page.
    """

    url: str
    # Ceiling is deliberately LOW: every in-flight request holds one of the
    # deployment's few pooled browsers (DEFAULT_BROWSER_POOL_SIZE = 5, shared
    # with live crawls), so a caller-controlled long timeout is a cheap
    # starvation lever. A page that needs >30s is a miss, not a slow success.
    timeout_ms: int = Field(default=BROWSER_FETCH_DEFAULT_TIMEOUT_MS, ge=1_000, le=30_000)
    use_proxy: bool = True


class BrowserFetchResult(BaseModel):
    """Typed OUT shape for /browser-fetch — one model, never a hand-built dict."""

    success: bool
    status_code: int = 0
    final_url: str
    title: str | None = None
    content_type: str = ""
    html: str = ""
    error: str | None = None
    truncated: bool = False


@router.post(
    "/browser-fetch",
    summary="Render ONE URL in the pooled browser and return its HTML",
    response_model=BrowserFetchResult,
)
async def browser_fetch(
    request: BrowserFetchRequest,
    ctx: AppContext = Depends(context_dep),
) -> BrowserFetchResult:
    from matrx_scraper._ext import get_ext, has_ext
    from matrx_scraper.scraper import ProxyConfigurationError, get_required_random_proxy
    from matrx_scraper.utils.url import validate_public_http_url

    if not has_ext("browser_pool"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="browser pool is not enabled on this scraper deployment",
        )
    # SSRF gate, part 1 — only publicly-routable http(s) targets. The validator
    # returns the CORRECTED url; navigate that, never the raw input, or we
    # validate one thing and fetch another. The rejection reason is NOT echoed:
    # it names the resolved address, which turns this into an internal-network
    # resolution oracle for any authenticated caller.
    try:
        target_url = await validate_public_http_url(request.url)
    except Exception as exc:
        logger.info("browser-fetch rejected %r: %s", request.url, exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="url must be a publicly routable http(s) address",
        )

    pool = get_ext("browser_pool")
    try:
        proxy = get_required_random_proxy() if request.use_proxy else None
    except ProxyConfigurationError as exc:
        # A configuration gap must not 500 a caller — this endpoint's contract
        # is a structured result, and its own consumers treat any failure as
        # "the escalation didn't help".
        logger.warning("browser-fetch proxy unavailable: %s", exc)
        return BrowserFetchResult(
            success=False, final_url=request.url, error=f"proxy unavailable: {exc}"
        )
    try:
        content, response_url, status_code, headers, title = await pool.fetch(
            target_url, proxy=proxy, timeout_ms=request.timeout_ms
        )
    except Exception as exc:
        # Loud: a render failure is invisible to the calling host beyond a
        # yellow line, so the service that actually failed must say so.
        logger.warning("browser-fetch render failed for %s: %s", target_url, exc, exc_info=True)
        return BrowserFetchResult(
            success=False, final_url=target_url, error=f"{type(exc).__name__}: {exc}"
        )

    final_url = response_url or target_url
    # SSRF gate, part 2 — the browser FOLLOWS redirects, so the page we
    # actually rendered may be an internal host reached via a public 302 (or a
    # DNS rebind between validation and navigation). The crawler already
    # post-validates its final URL; do the same here AND withhold the body,
    # because by now the bytes have been read. Never return internal content.
    try:
        await validate_public_http_url(final_url)
    except Exception as exc:
        logger.warning(
            "browser-fetch discarded a non-public final url (%s → redacted): %s",
            target_url,
            exc,
        )
        return BrowserFetchResult(
            success=False,
            final_url=target_url,
            error="navigation ended on a non-public address; response discarded",
        )

    html = content or ""
    truncated = False
    if len(html) > BROWSER_FETCH_MAX_HTML_CHARS:
        html = html[:BROWSER_FETCH_MAX_HTML_CHARS]
        truncated = True
        logger.warning(
            "browser-fetch truncated %s at %d chars", final_url, BROWSER_FETCH_MAX_HTML_CHARS
        )
    return BrowserFetchResult(
        success=bool(html) and status_code < 400,
        status_code=status_code,
        final_url=final_url,
        title=title or None,
        content_type=headers.get("content-type", ""),
        html=html,
        error=None,
        truncated=truncated,
    )


class BrowserInspectRequest(BaseModel):
    """One-shot render CHECK of a single URL — errors, DOM probes, screenshots.

    The third stateless sibling of `/browser-fetch` (HTML only) and the
    `/browser/*` session API (DOM automation). Neither of those can answer
    "did this page render correctly for a visitor": that needs the console
    error stream, the failed-request stream and a DOM probe, all of which
    only exist while the page is open. Chromium-less hosts (aidream runs no
    browser by design; see its Dockerfile note) call this instead of
    launching a local browser.
    """

    url: str
    # Same ceiling reasoning as /browser-fetch: every in-flight request holds
    # pooled browsers shared with live crawls.
    timeout_ms: int = Field(default=BROWSER_FETCH_DEFAULT_TIMEOUT_MS, ge=1_000, le=30_000)
    # Screenshot kinds, e.g. ["viewport_desktop", "viewport_mobile"]. Kinds
    # spanning device profiles cost ONE navigation each — hence the low cap.
    kinds: list[str] = Field(default_factory=list, max_length=BROWSER_INSPECT_MAX_KINDS)
    expect_text: str | None = None
    expect_selector: str | None = None
    user_agent_suffix: str | None = Field(default=None, max_length=200)
    # Defaults FALSE, unlike /browser-fetch: a render check targets a site the
    # caller OWNS, and routing our own page through a residential proxy adds
    # latency, failure modes and cost for nothing.
    use_proxy: bool = False


class InspectedScreenshot(BaseModel):
    kind: str
    width: int
    height: int
    image_base64: str


class ScreenshotFailure(BaseModel):
    kind: str
    error_class: str
    error_message: str


class BrowserInspectResult(BaseModel):
    """Typed OUT shape for /browser-inspect — one model, never a hand-built dict."""

    success: bool
    http_status: int | None = None
    final_url: str
    title: str = ""
    console_errors: list[str] = Field(default_factory=list)
    failed_requests: list[str] = Field(default_factory=list)
    expect_text_found: bool | None = None
    expect_selector_found: bool | None = None
    screenshots: list[InspectedScreenshot] = Field(default_factory=list)
    screenshot_failures: list[ScreenshotFailure] = Field(default_factory=list)
    error: str | None = None
    # True when the render failed in a way a retry could fix (timeout, transport)
    # as opposed to a permanent one (bad selector, blocked URL).
    retryable: bool = False


@router.post(
    "/browser-inspect",
    summary="Navigate ONE URL in the pooled browser and report render evidence",
    response_model=BrowserInspectResult,
)
async def browser_inspect(
    request: BrowserInspectRequest,
    ctx: AppContext = Depends(context_dep),
) -> BrowserInspectResult:
    import base64

    from matrx_scraper._ext import get_ext, has_ext
    from matrx_scraper.browser_pool import BrowserInspectTimeout
    from matrx_scraper.scraper import ProxyConfigurationError, get_required_random_proxy
    from matrx_scraper.utils.url import validate_public_http_url

    if not has_ext("browser_pool"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="browser pool is not enabled on this scraper deployment",
        )
    # SSRF gate, part 1 — identical contract to /browser-fetch: navigate the
    # CORRECTED url, never the raw input, and never echo the rejection reason
    # (it names the resolved address, an internal-network oracle).
    try:
        target_url = await validate_public_http_url(request.url)
    except Exception as exc:
        logger.info("browser-inspect rejected %r: %s", request.url, exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="url must be a publicly routable http(s) address",
        )

    pool = get_ext("browser_pool")
    proxy: str | None = None
    if request.use_proxy:
        try:
            proxy = get_required_random_proxy()
        except ProxyConfigurationError as exc:
            logger.warning("browser-inspect proxy unavailable: %s", exc)
            return BrowserInspectResult(
                success=False,
                final_url=request.url,
                error=f"proxy unavailable: {exc}",
                retryable=True,
            )
    try:
        inspection = await pool.inspect_url(
            target_url,
            kinds=request.kinds,
            expect_text=request.expect_text,
            expect_selector=request.expect_selector,
            proxy=proxy,
            user_agent_suffix=request.user_agent_suffix,
            nav_timeout_ms=request.timeout_ms,
        )
    except BrowserInspectTimeout as exc:
        return BrowserInspectResult(
            success=False, final_url=target_url, error=str(exc), retryable=True
        )
    except ValueError as exc:
        # Unknown screenshot kind / kinds the caller mis-specified — permanent.
        logger.info("browser-inspect bad request for %s: %s", target_url, exc)
        return BrowserInspectResult(
            success=False, final_url=target_url, error=str(exc), retryable=False
        )
    except Exception as exc:
        # Loud: a render failure is invisible to the calling host beyond a
        # yellow line, so the service that actually failed must say so.
        logger.warning("browser-inspect render failed for %s: %s", target_url, exc, exc_info=True)
        return BrowserInspectResult(
            success=False,
            final_url=target_url,
            error=f"{type(exc).__name__}: {exc}",
            retryable=True,
        )

    # SSRF gate, part 2 — the browser FOLLOWS redirects, so the page we
    # actually rendered may be an internal host reached via a public 302. By
    # now we hold its pixels and its DOM answers; withhold ALL of it.
    try:
        await validate_public_http_url(inspection.final_url)
    except Exception as exc:
        logger.warning(
            "browser-inspect discarded a non-public final url (%s → redacted): %s",
            target_url,
            exc,
        )
        return BrowserInspectResult(
            success=False,
            final_url=target_url,
            error="navigation ended on a non-public address; response discarded",
            retryable=False,
        )

    return BrowserInspectResult(
        success=True,
        http_status=inspection.http_status,
        final_url=inspection.final_url,
        title=inspection.title,
        console_errors=inspection.console_errors,
        failed_requests=inspection.failed_requests,
        expect_text_found=inspection.dom_text_found,
        expect_selector_found=inspection.dom_selector_found,
        screenshots=[
            InspectedScreenshot(
                kind=shot.kind,
                width=shot.width,
                height=shot.height,
                image_base64=base64.b64encode(shot.bytes).decode("ascii"),
            )
            for shot in inspection.screenshots
        ],
        screenshot_failures=[
            ScreenshotFailure(
                kind=failure.kind,
                error_class=failure.error_class,
                error_message=failure.error_message,
            )
            for failure in inspection.screenshot_failures
        ],
    )


async def _run_quick_scrape(emitter: Emitter, request: QuickScrapeRequest) -> None:
    try:
        service = ScrapeService(emitter=emitter)
        service.urls = request.urls
        service.use_cache = request.use_cache
        service.options = _build_options(request)
        await emitter.send_info(
            InfoPayload(
                code="scrape_start",
                system_message=f"Scraping {len(request.urls)} URLs",
                user_message="Fetching pages...",
            )
        )
        await service.quick_scrape_stream()
        await emitter.send_end()
    except Exception as e:
        await emitter.fatal_error(
            error_type="scrape_error",
            message=str(e),
            user_message="Failed to scrape URLs. Please try again.",
            details={"traceback": traceback.format_exc()},
        )


@router.post("/quick-scrape")
async def quick_scrape(
    request: QuickScrapeRequest,
    ctx: AppContext = Depends(context_dep),
):
    return create_streaming_response(
        ctx,
        _run_quick_scrape,
        request,
        initial_message="Connecting to scraper...",
        debug_label="QuickScrape",
    )


async def _run_search_keywords(emitter: Emitter, request: SearchKeywordsRequest) -> None:
    try:
        service = ScrapeService(emitter=emitter)
        service.keywords = request.keywords
        service.country_code = request.country_code
        service.total_results_per_keyword = request.total_results_per_keyword
        service.search_type = request.search_type
        await emitter.send_info(
            InfoPayload(
                code="scrape_start",
                system_message=f"Searching {len(request.keywords)} keywords",
                user_message="Searching...",
            )
        )
        await service.search_keywords()
        await emitter.send_end()
    except Exception as e:
        await emitter.fatal_error(
            error_type="search_error",
            message=str(e),
            user_message="Failed to search keywords. Please try again.",
            details={"traceback": traceback.format_exc()},
        )


@router.post("/search")
async def search_keywords(
    request: SearchKeywordsRequest,
    ctx: AppContext = Depends(context_dep),
):
    return create_streaming_response(
        ctx,
        _run_search_keywords,
        request,
        initial_message="Connecting to search...",
        debug_label="SearchKeywords",
    )


async def _run_search_and_scrape(emitter: Emitter, request: SearchAndScrapeRequest) -> None:
    try:
        service = ScrapeService(emitter=emitter)
        service.keywords = request.keywords
        service.country_code = request.country_code
        service.total_results_per_keyword = request.total_results_per_keyword
        service.search_type = request.search_type
        service.options = _build_options(request)
        await emitter.send_info(
            InfoPayload(
                code="scrape_start",
                system_message=f"Searching and scraping {len(request.keywords)} keywords",
                user_message="Searching and reading pages...",
            )
        )
        await service.search_and_scrape()
        await emitter.send_end()
    except Exception as e:
        await emitter.fatal_error(
            error_type="scrape_error",
            message=str(e),
            user_message="Failed to search and scrape. Please try again.",
            details={"traceback": traceback.format_exc()},
        )


@router.post("/search-and-scrape")
async def search_and_scrape(
    request: SearchAndScrapeRequest,
    ctx: AppContext = Depends(context_dep),
):
    return create_streaming_response(
        ctx,
        _run_search_and_scrape,
        request,
        initial_message="Connecting...",
        debug_label="SearchAndScrape",
    )


async def _run_search_and_scrape_limited(
    emitter: Emitter,
    request: SearchAndScrapeLimitedRequest,
) -> None:
    try:
        service = ScrapeService(emitter=emitter)
        service.keyword = request.keyword
        service.country_code = request.country_code
        service.max_page_read = request.max_page_read
        service.search_type = request.search_type
        service.options = _build_options(request)
        await emitter.send_info(
            InfoPayload(
                code="scrape_start",
                system_message=f"Searching '{request.keyword}' and scraping up to {request.max_page_read} pages",
                user_message=f"Searching for '{request.keyword}'...",
            )
        )
        await service.search_and_scrape_limited()
        await emitter.send_end()
    except Exception as e:
        await emitter.fatal_error(
            error_type="scrape_error",
            message=str(e),
            user_message="Failed to search and scrape. Please try again.",
            details={"traceback": traceback.format_exc()},
        )


@router.post("/search-and-scrape-limited")
async def search_and_scrape_limited(
    request: SearchAndScrapeLimitedRequest,
    ctx: AppContext = Depends(context_dep),
):
    return create_streaming_response(
        ctx,
        _run_search_and_scrape_limited,
        request,
        initial_message="Connecting...",
        debug_label="SearchAndScrapeLimited",
    )
