from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any
from collections.abc import AsyncGenerator

from matrx_scraper.extractors import (
    extract_text_from_image_bytes,
    extract_text_from_pdf_bytes,
    extract_text_content,
)
from matrx_scraper.parser.core import ParserOrchestrator
from matrx_scraper.parser.extraction_rules import rules
from matrx_scraper.parser.overrides import overrides
from matrx_scraper.seo_audit import security_response_headers
from matrx_scraper.user_agents import normalize_user_agent
from matrx_scraper.scraper import (
    ContentType,
    FailureReason,
    RequestType,
    Response,
    fetch,
    fetch_normally_with_proxy,
    get_required_random_proxy,
)

logger = logging.getLogger(__name__)


@dataclass
class ScrapeResult:
    """
    Rich, fully-populated result from a single scrape+parse operation.

    Field names match the output schema expected by both the React-frontend
    API layer and the research pipeline.

    Legacy compatibility notes:
      - ``success`` (bool) replaces the old string ``status`` field
      - ``failure_reason`` replaces the old ``error`` string field
      - ``scraped_at`` is an ISO-8601 UTC timestamp (was missing before)
      - ``hashes`` is now a dict {minhash, simhash, outline_simhash} instead of list[str]
    """

    url: str
    response_url: str
    success: bool
    content_type: str

    # Timestamp — always populated
    scraped_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    # Page metadata
    title: str | None = None
    published_at: str | None = None
    modified_at: str | None = None
    cms: str | None = None
    firewall: str | None = None
    status_code: int = 0

    # Structured text extractions (from extraction rules)
    ai_content: str | None = None
    ai_research_content: str | None = None
    ai_research_with_images: str | None = None
    markdown_renderable: str | None = None
    markdown_renderable_by_header: dict[str, str] | None = None
    organized_data: Any | None = None
    document_outline: list[Any] | None = None
    tables: list[Any] | None = None
    code_blocks: list[Any] | None = None
    lists: list[Any] | None = None
    images: list[Any] | None = None
    videos: list[Any] | None = None
    audios: list[Any] | None = None

    # Full-pipeline additions
    overview: dict[str, Any] | None = None
    text_data: str | None = None
    main_image: str | None = None
    structured_data: Any | None = None
    # URL buckets — internal/external/images/documents/audio/videos/archives/
    # others, each a list of bare URL strings. Persisted and read by hosts
    # (matrx-local `scrape_store.STORED_FIELDS`, the frontend scraper pages),
    # so the shape is frozen. Anchor text lives in `link_records`, NOT here.
    links: dict[str, list[str]] | None = None
    # One record per <a href>: target_url, anchor_text, text_source, rel,
    # nofollow, link_type, region. Anchor text is the strongest human-authored
    # label a link carries and is unrecoverable without refetching, so the same
    # parse that fills `links` fills this. Key names match `seo_audit.LinkItem`
    # / the `crawl_links` rows so consumers read one vocabulary.
    link_records: list[dict[str, Any]] | None = None
    hashes: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    noise_remover_removal_details: list[dict] | None = None
    content_filter_removal_details: list[dict] | None = None

    # Non-HTML content
    raw_text: str | None = None
    # Original successful response body for archival. Unlike ``raw_text``,
    # this is not extraction output: XML/JSON/text stay intact and binary
    # formats retain their bytes.
    raw_body: str | bytes | None = None
    content_type_raw: str | None = None

    # Raw HTML — populated for HTML responses only. Used by the SEO audit
    # extractor (matrx_scraper.seo_audit) and by hosts that want to persist
    # the original page bytes (e.g. crawler S3 archive). NOT serialised in
    # to_dict() for the cache by default — see to_dict_with_html() below.
    raw_html: str | None = None

    # Redirect chain — list of {status, url} hops, length 1 means no redirect.
    redirect_chain: list[dict[str, Any]] = field(default_factory=list)

    # Security-relevant response headers ONLY (`seo_audit.SECURITY_RESPONSE_HEADERS`)
    # — HSTS, CSP, X-Frame-Options and friends, lower-cased. The full header set
    # is deliberately NOT carried: it contains `set-cookie` and other credential
    # material that must never reach a persisted snapshot. `None` means the
    # transport recorded no headers at all (a cached rebuild), which the security
    # checks answer `n_a` for; `{}` means the server sent none of them.
    security_headers: dict[str, str] | None = None

    # TRUE time to first byte in ms, straight from the transport (curl's
    # STARTTRANSFER_TIME_T, or the httpx streamed-headers timestamp), redirect
    # hops included. NOT the wall-clock time around the whole scrape — that
    # keeps running through the body download and the parse, which is exactly
    # the conflation the `ttfb_server_response` check must avoid. `None` means
    # the transport could not measure it (today: the Playwright browser path),
    # and every consumer must treat that as "not measured", never as fast.
    ttfb_ms: int | None = None

    # Failure info
    failure_reason: str | None = None
    failure_details: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            k: v
            for k, v in self.__dict__.items()
            if v is not None and k not in {"raw_body", "raw_html"}
        }


def _parse_html_content(html: str, url: str | None, fast: bool = False) -> dict[str, Any]:
    """Run the full pipeline and return both extraction-rules output and raw pipeline output."""
    parser = ParserOrchestrator()

    if fast:
        pipeline_result = parser.parse_content(
            html, url, content_filter_overrides=overrides, skip_links=True, skip_hashes=True
        )
    else:
        pipeline_result = parser.parse_content(html, url, content_filter_overrides=overrides)

    organized_data = pipeline_result.get("organized_data")
    extraction_rules_output: dict[str, Any] = {}
    if organized_data is not None:
        if fast:
            from matrx_scraper.parser.extraction_rules import rules as all_rules

            # `rules` is a list of {"name": ..., ...} dicts (see extraction_rules.py),
            # not a name-keyed dict — `.items()` here always raised AttributeError,
            # making `scrape(..., fast=True)` unusable (dead code path, found 2026-07-23
            # while building the WS-14 public SEO tools, the first real caller).
            fast_rules = [r for r in all_rules if r.get("name") == "ai_research_content"]
            extraction_rules_output = organized_data.extract(rules=fast_rules)
        else:
            extraction_rules_output = organized_data.extract(rules=rules)

    extraction_rules_output["links"] = pipeline_result.get("links", {})
    extraction_rules_output["link_records"] = pipeline_result.get("link_records", [])
    extraction_rules_output["_pipeline"] = pipeline_result
    return extraction_rules_output


def _build_result_from_response(response: Response, fast: bool = False) -> ScrapeResult:
    result = ScrapeResult(
        url=response.request_url,
        response_url=response.response_url,
        success=not response.failed,
        content_type=response.content_type.value,
        content_type_raw=response.content_type_raw,
        title=response.title,
        published_at=response.published_at,
        modified_at=response.modified_at,
        cms=response.cms_primary.value if response.cms_primary else None,
        firewall=response.firewall.value if response.firewall else None,
        status_code=response.status_code,
        failure_reason=response.failed_primary_reason.value
        if response.failed_primary_reason
        else None,
        failure_details=[
            {list(r.keys())[0].value: list(r.values())[0]} for r in response.failed_reasons
        ],
    )

    # Multi-hop redirect chain — captured by every transport (curl_cffi,
    # httpx history, Playwright redirected_from). Copied for EVERY content
    # type and even failed fetches: a redirect chain ending at a 404/410 is
    # exactly the evidence the crawl reports need.
    if getattr(response, "redirect_chain", None):
        result.redirect_chain = response.redirect_chain

    # Security headers — filtered at the source, for EVERY content type and even
    # failed fetches (an HSTS header on a 404 is still the site's HSTS policy).
    if getattr(response, "response_headers", None) is not None:
        result.security_headers = security_response_headers(response.response_headers)

    # True TTFB — carried for every content type and for failed fetches too: a
    # 500 that took nine seconds to answer is exactly the evidence worth keeping.
    result.ttfb_ms = getattr(response, "ttfb_ms", None)

    if response.failed:
        return result

    ct = response.content_type
    result.raw_body = (
        response.content_bytes if response.content_bytes is not None else response.content
    )

    if ct == ContentType.HTML:
        if not response.content:
            result.success = False
            result.failure_reason = FailureReason.LOW_TEXT_CONTENT.value
            return result

        # Preserve the raw HTML so callers (crawler SEO audit, archival
        # writers, etc.) can re-parse without refetching.
        result.raw_html = response.content

        extracted = _parse_html_content(response.content, response.response_url, fast=fast)
        pipeline = extracted.pop("_pipeline", {})

        result.ai_content = extracted.get("ai_content")
        result.ai_research_content = extracted.get("ai_research_content")
        result.ai_research_with_images = extracted.get("ai_research_with_images")
        result.markdown_renderable = extracted.get("markdown_renderable")
        result.markdown_renderable_by_header = extracted.get("markdown_renderable_by_header")
        result.organized_data = extracted.get("organized_data")
        result.document_outline = extracted.get("document_outline")
        result.tables = extracted.get("tables")
        result.code_blocks = extracted.get("code_blocks")
        result.lists = extracted.get("lists")
        result.images = extracted.get("images")
        result.videos = extracted.get("videos")
        result.audios = extracted.get("audios")
        result.links = extracted.get("links")
        result.link_records = extracted.get("link_records")

        # Full-pipeline fields
        result.overview = pipeline.get("overview")
        # `text_data` is the page as readable text. The pipeline's own
        # `_build_text_data` hands `json_to_text_lines` the `OrganizedData`
        # OBJECT, while that function only walks dicts/lists — so it fell
        # through every branch and returned "" for EVERY html page (and
        # `overview.char_count` with it). Until that flattener is fixed to take
        # the extracted data form, fall back to the extraction rules' markdown,
        # which is the same text the fields below are built from. A scrape that
        # reports a title, links and 4kB of research content while claiming
        # zero text is the kind of "successful" empty result that poisons
        # everything downstream.
        result.text_data = pipeline.get("text_data") or extracted.get("markdown_renderable")
        result.main_image = pipeline.get("main_image")
        result.structured_data = pipeline.get("structured_data")
        result.hashes = pipeline.get("hashes")
        result.noise_remover_removal_details = pipeline.get("noise_remover_removal_details")
        result.content_filter_removal_details = pipeline.get("content_filter_removal_details")

        overview = pipeline.get("overview") or {}
        result.metadata = overview.get("metadata")

        if not result.title and overview.get("page_title"):
            result.title = overview["page_title"]

    elif ct == ContentType.PDF:
        raw = (
            extract_text_from_pdf_bytes(response.content_bytes) if response.content_bytes else None
        )
        result.raw_text = raw
        if not raw:
            result.success = False
            result.failure_reason = "pdf_extraction_failed"

    elif ct == ContentType.IMAGE:
        raw = (
            extract_text_from_image_bytes(response.content_bytes)
            if response.content_bytes
            else None
        )
        result.raw_text = raw

    else:
        result.raw_text = extract_text_content(response.content, ct.value)

    return result


async def scrape(
    url: str,
    use_proxy: bool = True,
    request_type: RequestType = RequestType.NORMAL,
    fast: bool = False,
    cache: Any = None,
    domain_config: Any = None,
    browser_pool: Any = None,
    user_agent: str | None = None,
) -> ScrapeResult:
    """Fetch and fully parse a single URL. Always async — never blocks.

    `user_agent`, when set, overrides the User-Agent for whichever transport
    this call ends up using (HTTP or browser). `None` = no override.
    """
    user_agent = normalize_user_agent(user_agent)
    if domain_config is not None:
        if not domain_config.is_scrape_allowed(url):
            return ScrapeResult(
                url=url,
                response_url=url,
                success=False,
                content_type="unknown",
                failure_reason="domain_blocked",
            )

    # A UA override changes WHAT the server returns, but the scrape cache is
    # keyed on the URL alone. Serving a Chrome-fetched body for a Googlebot
    # request (or poisoning the shared entry with one) would silently defeat
    # the entire point of the override, so an overridden fetch bypasses the
    # cache in BOTH directions.
    if user_agent:
        cache = None

    if cache is not None:
        from matrx_scraper.utils.url import get_url_info

        url_info = get_url_info(url)
        cached = await cache.get(url_info.unique_page_name)
        if cached is not None:
            content = cached.get("content", {})
            result = ScrapeResult(
                url=url,
                response_url=cached.get("url", url),
                success=True,
                content_type=cached.get("content_type", "html"),
            )
            for k, v in content.items():
                if hasattr(result, k):
                    setattr(result, k, v)
            return result

    proxy_type = "datacenter"
    if domain_config is not None:
        proxy_type = domain_config.get_proxy_type(url)
        if proxy_type == "none":
            use_proxy = False

    if request_type == RequestType.BROWSER:
        if browser_pool is not None:
            proxy = get_required_random_proxy() if use_proxy else None
            # `browser_pool` is a duck-typed injected seam — a host may supply
            # its own. Send the kwarg ONLY when there is something to override,
            # so a pool built before this field existed keeps working unchanged.
            # When an override IS requested, a pool that cannot accept it raises
            # loudly here rather than silently fetching under the wrong
            # identity — which is the failure this whole field exists to avoid.
            pool_kwargs: dict[str, Any] = {"proxy": proxy}
            if user_agent:
                pool_kwargs["user_agent"] = user_agent
            content, response_url, status_code, headers, title = await browser_pool.fetch(
                url, **pool_kwargs
            )
            response = Response(
                request_url=url,
                proxy_used=proxy is not None,
                request_type=RequestType.BROWSER,
                content_type=ContentType.HTML,
                extension="",
                content_type_raw="text/html",
                response_url=response_url,
                response_headers=headers,
                title=title,
                status_code=status_code,
                content=content,
            )
        else:
            proxy = get_required_random_proxy() if use_proxy else None
            response = await fetch(
                url, request_type=RequestType.BROWSER, proxy=proxy, user_agent=user_agent
            )
    elif use_proxy:
        response = await fetch_normally_with_proxy(url, user_agent=user_agent)
    else:
        response = await fetch(url, request_type=RequestType.NORMAL, user_agent=user_agent)

    # Parsing and extraction include CPU-heavy BeautifulSoup work and blocking
    # first-use helpers such as tldextract's suffix-list discovery. Keep the
    # entire response-to-result pipeline off the asyncio event loop.
    result = await asyncio.to_thread(_build_result_from_response, response, fast)

    if cache is not None and result.success:
        from matrx_scraper.utils.url import get_url_info

        url_info = get_url_info(url)
        try:
            await cache.set(
                key=url_info.unique_page_name,
                url=url,
                domain=url_info.full_domain,
                content=result.to_dict(),
                content_type=result.content_type,
                char_count=len(result.text_data or result.ai_research_content or ""),
            )
        except Exception:
            logger.warning("Failed to write cache for %s", url, exc_info=True)

    return result


async def scrape_many(
    urls: list[str],
    use_proxy: bool = True,
    concurrency: int = 20,
    fast: bool = False,
    cache: Any = None,
    domain_config: Any = None,
    browser_pool: Any = None,
) -> list[ScrapeResult]:
    """
    Scrape multiple URLs concurrently and return all results together.

    Uses a semaphore to cap simultaneous in-flight requests.  Each URL is an
    independent coroutine — there is no per-site serialisation.  The semaphore
    prevents overwhelming the local network; ``concurrency=20`` is a safe
    default for mixed-site batches.
    """
    semaphore = asyncio.Semaphore(concurrency)

    async def _bounded(url: str) -> ScrapeResult:
        async with semaphore:
            return await scrape(
                url,
                use_proxy=use_proxy,
                fast=fast,
                cache=cache,
                domain_config=domain_config,
                browser_pool=browser_pool,
            )

    return list(await asyncio.gather(*[_bounded(u) for u in urls]))


async def scrape_many_stream(
    urls: list[str],
    use_proxy: bool = True,
    concurrency: int = 20,
    fast: bool = False,
    cache: Any = None,
    domain_config: Any = None,
    browser_pool: Any = None,
) -> AsyncGenerator[ScrapeResult]:
    """
    Scrape multiple URLs concurrently and **yield each result the moment it
    finishes** — results are NOT batched.

    Key behaviours
    ──────────────
    - All ``len(urls)`` fetches are launched immediately (up to ``concurrency``
      in-flight at once).  Different sites run in parallel — there is no
      per-domain wait unless the semaphore is saturated.
    - ``asyncio.as_completed`` is used so the first URL to finish yields first,
      regardless of its position in the input list.
    - The caller (e.g. ScrapeService) streams each result to the frontend via
      ``emitter.send_data()`` immediately, so the user sees pages arriving one
      by one rather than waiting for the whole batch.

    Example::

        async for result in scrape_many_stream(urls):
            await emitter.send_data(result.to_dict())
    """
    semaphore = asyncio.Semaphore(concurrency)

    async def _bounded(url: str) -> ScrapeResult:
        async with semaphore:
            return await scrape(
                url,
                use_proxy=use_proxy,
                fast=fast,
                cache=cache,
                domain_config=domain_config,
                browser_pool=browser_pool,
            )

    coros = [_bounded(u) for u in urls]
    for future in asyncio.as_completed(coros):
        yield await future
