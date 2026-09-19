from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any
from collections.abc import AsyncGenerator

from matrx_scraper._ext import get_ext, has_ext
from matrx_scraper.content_sanity import assess as assess_content
from matrx_scraper.escalation import (
    ENGINE_BROWSER,
    ENGINE_CACHE,
    ENGINE_HTTP,
    EscalationPolicy,
    can_render,
    escalation_sentence,
)
from matrx_scraper.ladder import (
    RESIDENTIAL_RUNG,
    STOP_NOT_ESCALATABLE,
    LadderPolicy,
    LadderTrail,
    classify_login_wall,
)
from matrx_scraper.ladder import trail_entry as ladder_trail_entry
from matrx_scraper.extractors import (
    extract_text_from_image_bytes,
    extract_text_from_pdf_bytes_or_reason,
    extract_text_content,
)
from matrx_scraper.parser.core import ParserOrchestrator
from matrx_scraper.parser.extraction_rules import rules
from matrx_scraper.parser.overrides import overrides
from matrx_scraper.seo_audit import security_response_headers
from matrx_utils.block_sink import announce_block
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
from matrx_scraper.utils.proxy import redact_url_secrets

logger = logging.getLogger(__name__)

# ── Where a fetch left from ─────────────────────────────────────────────────
#: Our datacenter proxy pool — the default exit for everything.
EGRESS_DATACENTER = "datacenter"
#: This server's own address, because no proxy was used (or the pool refused).
EGRESS_DIRECT = "direct"
#: The person's OWN computer, used only after a site blocked our servers.
EGRESS_RESIDENTIAL = "residential"

#: The host ext that mints a residential-egress ticket for one acting user.
#: `async (acting_user_id: str, token: str | None) -> dict | None`, returning
#: `{"ticket", "consume_url", "device_name"}` or
#: `{"unavailable": <reason>, "message": <sentence>}`. aidream wires it in
#: `aidream/package_integration.py`; a host that does not wire it gets no
#: residential retry and a trail entry that says exactly that.
EGRESS_TICKET_EXT = "residential_egress_ticket"
#: The host ext that reads the `residential_egress.retry_reasons` knob.
#: `async () -> list[str]`.
EGRESS_RETRY_REASONS_EXT = "residential_egress_retry_reasons"

#: The knob's own starting value, used when the host wires a ticket ext but no
#: reasons ext. Never a silent hardcode: the knob is the authority and this is
#: the value the contract seeds it with.
DEFAULT_RESIDENTIAL_RETRY_REASONS: tuple[str, ...] = (
    "cloudflare_block",
    "blocked",
    "bad_status:403",
    "bad_status:429",
)


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
    # THE MAIN-CONTENT LAW (parser/main_content.py): the article body with the
    # site's furniture (nav, sponsor lines, staff bios, tag lists, donate and
    # newsletter CTAs, related rails) stripped. None/empty when the page is not
    # article-like — a consumer then keeps the full page, knowingly.
    main_content_text: str | None = None
    #: Which root selector produced `main_content_text` (evidence, never silent).
    main_content_selector: str | None = None
    main_content_removal_details: list[dict] | None = None
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
    #: Plain-English cause, safe to show a non-technical person verbatim. A
    #: screen must never have to render `failure_reason` or a stack trace.
    failure_message: str | None = None

    # ── Engine provenance — never silent about HOW this content was obtained ──
    #: "http" | "browser" | "cache". Which engine actually produced `content`.
    engine: str = ENGINE_HTTP
    #: True when the plain HTTP fetch failed and the server browser was used.
    escalated: bool = False
    #: The named failure that triggered the hand-off (`cloudflare_block`, …).
    escalation_reason: str | None = None
    #: One plain-English sentence explaining the hand-off, or explaining why a
    #: hand-off that SHOULD have happened could not.
    escalation_note: str | None = None
    #: True when the datacenter proxy pool refused the request and the page was
    #: fetched on a direct connection instead.
    proxy_bypassed: bool = False
    #: WHERE this page was fetched FROM — `datacenter` (our proxy pool),
    #: `direct` (this server's own address) or `residential` (the person's own
    #: computer, after a site blocked our servers). Never silent about it:
    #: contract `common-docs/systems/platform/residential-egress/FEATURE.md`.
    egress: str = EGRESS_DATACENTER
    #: The computer the page came through, in the person's own words
    #: ("Arman's MacBook Pro"). Set only when `egress == "residential"`.
    egress_device_name: str | None = None
    #: Longest extracted text length the content-sanity gate measured.
    content_chars: int = 0
    #: "thin_content" / "wrong_resource" — the result is usable but suspect.
    content_warning: str | None = None
    #: True when the server answered from a materially different address than
    #: the one requested (the Pinterest decoy-profile class).
    redirected_off_requested_path: bool = False
    #: True the moment the server-browser leg is actually dispatched. Needed
    #: because `escalation_reason` is also set when a hand-off SHOULD have
    #: happened and could not, and the ladder trail must not claim a rung was
    #: tried when it never ran.
    browser_attempted: bool = False

    # ── The capture ladder (matrx_scraper.ladder) ───────────────────────────
    #: One entry per rung attempted, in order. See the ladder module.
    rung_trail: list[dict[str, Any]] = field(default_factory=list)
    #: The rung that could read this page next — `own_browser` (the person's
    #: own logged-in Chrome, through matrx-extend) or `human_drive`. `None`
    #: when nothing follows, in which case `stopped_because` says why.
    next_rung: str | None = None
    next_rung_reason: str | None = None
    #: One plain-English sentence a non-technical person reads verbatim.
    next_rung_note: str | None = None
    #: One plain-English sentence for what the PERSON does, set only when the
    #: next rung is `human_drive`.
    next_rung_what_to_do: str | None = None
    next_rung_estimated_seconds: int | None = None
    #: `rung_disabled` | `not_escalatable` | `exhausted`. Exactly one of this
    #: and `next_rung` is set on any unusable result; both empty is the silent
    #: failure the ladder guard exists to prevent.
    stopped_because: str | None = None

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
        result.main_content_text = pipeline.get("main_content_text") or None
        result.main_content_selector = pipeline.get("main_content_selector")
        result.main_content_removal_details = pipeline.get("main_content_removal_details")
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
        raw, reason = (
            extract_text_from_pdf_bytes_or_reason(response.content_bytes)
            if response.content_bytes
            else (None, "no response bytes")
        )
        result.raw_text = raw
        if not raw:
            result.success = False
            # The cause rides with the code — a missing [pdf] extra on the
            # host must read as a deployment defect, never as "bad PDF".
            result.failure_reason = f"pdf_extraction_failed: {reason}"

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


#: Delay before the ONE retry a bot-check gets. A Cloudflare interstitial is
#: frequently transient — the 2026-09-17 hunt watched a Medium URL 403 and then
#: return 200 to a near-identical request seconds later — and a cheap delayed
#: retry beats spending a pooled browser. Short enough that a person watching
#: the screen does not think it hung.
CHALLENGE_RETRY_DELAY_SECONDS = 2.0


def _apply_content_sanity(result: ScrapeResult) -> None:
    """Never let a result with no content in it claim success. In place."""
    verdict = assess_content(result)
    result.content_chars = verdict.content_chars
    result.redirected_off_requested_path = verdict.redirected_off_requested_path
    if verdict.is_failure:
        result.success = False
        result.failure_reason = verdict.failure_reason
        result.failure_message = verdict.message
    elif verdict.warning:
        result.content_warning = verdict.warning
        if result.failure_message is None:
            result.failure_message = verdict.message


def _resolve_browser_pool(browser_pool: Any) -> Any:
    """The pool a caller injected, else the host-registered one.

    🚨 This resolution is the entire reason the general scrape path never
    escalated. `ScrapeService` (and therefore `/quick-scrape`, the AI tool
    surface and the MCP surface) called `scrape_many_stream()` without a
    `browser_pool`, so `scrape()` had nothing to hand off TO — while the very
    same process had a fully wired `browser_pool` ext that the crawler used all
    day. The capability was present and unreachable.
    """
    if browser_pool is not None:
        return browser_pool
    if has_ext("browser_pool"):
        try:
            return get_ext("browser_pool")
        except Exception:  # noqa: BLE001 — an absent pool is never fatal here
            return None
    return None


async def _fetch_and_parse(
    url: str,
    *,
    request_type: RequestType,
    use_proxy: bool,
    fast: bool,
    browser_pool: Any,
    user_agent: str | None,
    proxy_override: str | None = None,
) -> ScrapeResult:
    """One transport round-trip, fully parsed, tagged with the engine used.

    `proxy_override`, when set, REPLACES the datacenter proxy pool for this one
    round-trip — it is the loopback address of a running `EgressAdapter`, so the
    request leaves from the person's own computer. `use_proxy` is then ignored:
    the caller has already chosen the exit.
    """
    if request_type == RequestType.BROWSER:
        if browser_pool is not None:
            proxy = proxy_override or (get_required_random_proxy() if use_proxy else None)
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
            proxy = proxy_override or (get_required_random_proxy() if use_proxy else None)
            response = await fetch(
                url, request_type=RequestType.BROWSER, proxy=proxy, user_agent=user_agent
            )
    elif proxy_override:
        response = await fetch(
            url,
            request_type=RequestType.NORMAL,
            proxy=proxy_override,
            user_agent=user_agent,
        )
    elif use_proxy:
        response = await fetch_normally_with_proxy(url, user_agent=user_agent)
    else:
        response = await fetch(url, request_type=RequestType.NORMAL, user_agent=user_agent)

    # Parsing and extraction include CPU-heavy BeautifulSoup work and blocking
    # first-use helpers such as tldextract's suffix-list discovery. Keep the
    # entire response-to-result pipeline off the asyncio event loop.
    result = await asyncio.to_thread(_build_result_from_response, response, fast)
    result.engine = ENGINE_BROWSER if request_type == RequestType.BROWSER else ENGINE_HTTP
    result.proxy_bypassed = bool(getattr(response, "proxy_bypassed", False))
    if proxy_override is not None:
        result.egress = EGRESS_RESIDENTIAL
    elif use_proxy and not result.proxy_bypassed:
        result.egress = EGRESS_DATACENTER
    else:
        result.egress = EGRESS_DIRECT
    if result.proxy_bypassed and result.success:
        result.escalation_note = (
            "Our proxy network refused to carry this request, so we fetched the page "
            "on a direct connection instead."
        )
    return result


async def _maybe_escalate_to_browser(
    result: ScrapeResult,
    *,
    url: str,
    use_proxy: bool,
    fast: bool,
    browser_pool: Any,
    user_agent: str | None,
    escalate: bool | None,
) -> ScrapeResult:
    """The platform hand-off: a failed HTTP scrape reaches for the browser.

    Announced in every direction — when it happens, when it happens and does
    not help, and when it should have happened but this host has no browser.
    A hand-off nobody can see is exactly the silent automation the owner has
    told us not to build.
    """
    policy = EscalationPolicy.from_env()
    if escalate is True:
        policy = EscalationPolicy(enabled=True, reasons=policy.reasons)
    elif escalate is False:
        return result

    reason = result.failure_reason or result.content_warning
    if not policy.wants(reason):
        return result
    if not can_render(result.content_type):
        # A PDF/JSON/image cannot be improved by rendering it.
        return result

    if browser_pool is None:
        from matrx_scraper.browser_pool import PLAYWRIGHT_AVAILABLE

        if not PLAYWRIGHT_AVAILABLE:
            result.escalation_reason = reason
            result.escalation_note = (
                "This page needs a real browser to read, and this deployment has no "
                "browser available. The scraper service can render it."
            )
            return result

    # The browser must not re-enter a tunnel the pool has already refused.
    # Proven by the 60-URL battery on 2026-09-17: the HTTP leg was rescued by
    # the direct fallback, then the browser leg navigated through the SAME
    # proxy and died with `net::ERR_TUNNEL_CONNECTION_FAILED` — our own outage
    # defeating our own rescue.
    from matrx_scraper import proxy_health

    browser_use_proxy = use_proxy and not (
        result.proxy_bypassed or proxy_health.pool_refuses(url)
    )
    # `route` rather than the flag itself: the redaction census (rightly) treats
    # any proxy/url-shaped name in a log call as a credential risk, and a bool
    # is not worth weakening that guard for.
    route = "proxied" if browser_use_proxy else "direct"
    logger.info(
        "browser escalation for %s (reason=%s, route=%s)",
        redact_url_secrets(url),
        reason,
        route,
    )
    result.browser_attempted = True
    try:
        rendered = await _fetch_and_parse(
            url,
            request_type=RequestType.BROWSER,
            use_proxy=browser_use_proxy,
            fast=fast,
            browser_pool=browser_pool,
            user_agent=user_agent,
        )
    except Exception as exc:  # noqa: BLE001 — a rescue that fails is not fatal
        logger.warning(
            "browser escalation FAILED for %s: %s",
            redact_url_secrets(url),
            redact_url_secrets(exc),
        )
        result.escalation_reason = reason
        result.escalation_note = (
            f"We tried our server browser as well and it could not open the page "
            f"({type(exc).__name__})."
        )
        return result

    _apply_content_sanity(rendered)
    rendered.browser_attempted = True
    # Adopt the browser result ONLY when it is genuinely better. A browser that
    # returns the same wall, or less text, must not overwrite an honest answer.
    if rendered.success and rendered.content_chars > result.content_chars:
        rendered.escalated = True
        rendered.escalation_reason = reason
        rendered.escalation_note = escalation_sentence(reason)
        return rendered

    result.escalation_reason = reason
    result.escalation_note = (
        "We also opened this page in our server browser and it did not return more "
        "content, so this is the site's real answer."
    )
    return result


def _usable(result: ScrapeResult) -> bool:
    """Did this result actually give a person the page they asked for?

    `success` alone is not the answer: the content-sanity gate exists because
    the old scraper called a 34-character JS shell a success. A result with a
    `thin_content` / `wrong_resource` warning is honest about being suspect, and
    a suspect page is exactly what a person's own browser is for.
    """
    return bool(result.success) and result.content_warning in (None, "")


def _ladder_reason(result: ScrapeResult) -> str | None:
    """The one class name the ladder reasons about, from what we observed."""
    if classify_login_wall(
        status_code=result.status_code,
        response_url=result.response_url,
        requested_url=result.url,
    ):
        return "login_wall"
    return result.failure_reason or result.content_warning


# ── Residential egress: the person's own computer as the exit ───────────────
#
# THE RULE (contract: `common-docs/systems/platform/residential-egress/FEATURE.md`):
# never by default, only that user's own computer, only after a site blocked our
# servers, only for the retry of that same page — and the result always SAYS so,
# including when the retry could not happen and why.


def _reason_earns_residential_retry(
    reason: str | None, status_code: int | None, reasons: list[str]
) -> bool:
    """Is this failure one the knob says earns one retry from a home computer?

    An entry is either a bare failure class (`cloudflare_block`) or a class with
    a status qualifier (`bad_status:403`) — the same spelling the knob's own
    starting value uses, so an admin reading the knob and a reader of this code
    see one vocabulary.
    """
    if not reason:
        return False
    for entry in reasons:
        text = str(entry).strip()
        if not text:
            continue
        name, separator, qualifier = text.partition(":")
        if name.strip() != reason:
            continue
        if not separator:
            return True
        qualifier = qualifier.strip()
        if qualifier.isdigit() and int(qualifier) == int(status_code or 0):
            return True
    return False


async def _residential_retry_reasons() -> list[str]:
    """The knob's list, through the host ext; the contract's own start value
    when a host wires the ticket ext but no reasons ext."""
    if not has_ext(EGRESS_RETRY_REASONS_EXT):
        return list(DEFAULT_RESIDENTIAL_RETRY_REASONS)
    try:
        value = get_ext(EGRESS_RETRY_REASONS_EXT)()
        if hasattr(value, "__await__"):
            value = await value
        if value is None:
            return list(DEFAULT_RESIDENTIAL_RETRY_REASONS)
        return [str(item) for item in value]
    except Exception:  # noqa: BLE001 — announced, never fatal
        logger.warning(
            "the residential-egress retry-reason knob could not be read; using the "
            "platform's starting list for this scrape",
            exc_info=True,
        )
        return list(DEFAULT_RESIDENTIAL_RETRY_REASONS)


def _residential_entry(
    *, ok: bool, reason: str | None, note: str, chars: int = 0
) -> dict[str, Any]:
    return ladder_trail_entry(
        rung=RESIDENTIAL_RUNG, ok=ok, reason=reason, note=note, chars=chars
    )


async def _maybe_retry_through_residential_egress(
    result: ScrapeResult,
    *,
    url: str,
    acting_user_id: str | None,
    fast: bool,
    browser_pool: Any,
    user_agent: str | None,
    proxy_forbidden_by_policy: bool,
) -> tuple[ScrapeResult, dict[str, Any] | None]:
    """One retry of a blocked page through the acting user's own computer.

    Returns the result to keep and the trail entry to record, or `(result, None)`
    when this failure was never a candidate at all (a 404 is a 404 from any
    address). Every OTHER outcome — no signed-in person, nothing wired, no
    computer, the retry itself — produces an entry, because a retry that quietly
    did not happen is exactly the silent automation this platform forbids.
    """
    if _usable(result):
        return result, None

    # The RAW failure class, not `_ladder_reason`: the knob's vocabulary is the
    # scraper's own failure names (`cloudflare_block`, `bad_status:403`), while
    # `_ladder_reason` re-reads a 401/403 as `login_wall` for the person's-own-
    # browser rungs. Matching on that one would silently exclude every 403 the
    # knob explicitly names.
    reason = result.failure_reason or result.content_warning
    reasons = await _residential_retry_reasons()
    if not _reason_earns_residential_retry(reason, result.status_code, reasons):
        return result, None

    if proxy_forbidden_by_policy:
        # WE chose a direct connection for this address. Sending it out of a
        # person's home instead would be the same policy broken, louder.
        return result, _residential_entry(
            ok=False,
            reason=reason,
            note=(
                "This address is set to be fetched on a direct connection, so we did "
                "not try it through anyone's home computer."
            ),
        )

    if not has_ext(EGRESS_TICKET_EXT):
        return result, _residential_entry(
            ok=False,
            reason=reason,
            note="residential egress is not wired on this host",
        )

    if not acting_user_id:
        return result, _residential_entry(
            ok=False,
            reason=reason,
            note=(
                "Nobody was signed in for this request, so there was no home computer "
                "of yours to ask. A scheduled or service run never uses one."
            ),
        )

    try:
        grant = get_ext(EGRESS_TICKET_EXT)(acting_user_id, None)
        if hasattr(grant, "__await__"):
            grant = await grant
    except Exception:  # noqa: BLE001 — a rescue that fails is not fatal
        logger.warning("residential egress ticket failed", exc_info=True)
        return result, _residential_entry(
            ok=False,
            reason=reason,
            note="We could not ask for your home connection just now, so we did not try it.",
        )

    if not grant or not isinstance(grant, dict) or grant.get("unavailable"):
        note = ""
        if isinstance(grant, dict):
            note = str(grant.get("message") or "")
        return result, _residential_entry(
            ok=False,
            reason=reason,
            note=note
            or "You have no home computer available right now, so we did not try one.",
        )

    device_name = str(grant.get("device_name") or "your computer")
    from matrx_scraper.egress_adapter import EgressAdapter

    try:
        adapter = await EgressAdapter.start(str(grant["ticket"]), str(grant["consume_url"]))
    except Exception:  # noqa: BLE001
        logger.warning("residential egress adapter would not start", exc_info=True)
        return result, _residential_entry(
            ok=False,
            reason=reason,
            note=(
                f"We could not open a connection through {device_name}, so this is our "
                "own answer."
            ),
        )

    try:
        retried = await _fetch_and_parse(
            url,
            request_type=RequestType.NORMAL,
            use_proxy=False,
            fast=fast,
            browser_pool=browser_pool,
            user_agent=user_agent,
            proxy_override=adapter.proxy_url,
        )
        _apply_content_sanity(retried)

        if not _usable(retried) and can_render(retried.content_type):
            # Still a wall from the person's own address: the page needs a real
            # browser AND that address. Same adapter, same computer.
            try:
                rendered = await _fetch_and_parse(
                    url,
                    request_type=RequestType.BROWSER,
                    use_proxy=False,
                    fast=fast,
                    browser_pool=browser_pool,
                    user_agent=user_agent,
                    proxy_override=adapter.proxy_url,
                )
                _apply_content_sanity(rendered)
                rendered.browser_attempted = True
                if rendered.success and rendered.content_chars > retried.content_chars:
                    retried = rendered
            except Exception as exc:  # noqa: BLE001 — the HTTP leg's answer stands
                logger.warning(
                    "residential browser leg failed for %s: %s",
                    redact_url_secrets(url),
                    type(exc).__name__,
                )
    except Exception:  # noqa: BLE001
        logger.warning(
            "residential egress retry failed for %s", redact_url_secrets(url), exc_info=True
        )
        return result, _residential_entry(
            ok=False,
            reason=reason,
            note=f"We tried this page through {device_name} as well and the connection failed.",
        )
    finally:
        await adapter.close()

    if _usable(retried):
        retried.egress = EGRESS_RESIDENTIAL
        retried.egress_device_name = device_name
        retried.escalated = True
        retried.escalation_reason = reason
        retried.escalation_note = (
            f"The site blocked our servers, so we fetched it through {device_name}."
        )
        # The browser leg the SERVER spent still happened; the trail must not
        # lose it because a later rung replaced the result object.
        retried.browser_attempted = retried.browser_attempted or result.browser_attempted
        return retried, _residential_entry(
            ok=True,
            reason=None,
            note=f"Fetched through {device_name}.",
            chars=retried.content_chars,
        )

    result.escalation_reason = reason
    result.escalation_note = (
        f"We also tried this page through {device_name} and the site refused that too, "
        "so this is the site's real answer."
    )
    return result, _residential_entry(
        ok=False,
        reason=_ladder_reason(retried) or reason,
        note=f"We tried through {device_name} and the site refused that too.",
        chars=retried.content_chars,
    )


def _seal_ladder(
    result: ScrapeResult,
    *,
    request_type: RequestType,
    http_ok: bool,
    http_reason: str | None,
    http_chars: int,
    policy: LadderPolicy,
    organization_id: str | None = None,
    residential_entry: dict[str, Any] | None = None,
) -> ScrapeResult:
    """Write the rung trail and, on an unusable result, what comes next.

    THE LADDER LAW lives here: the trail is built through `LadderTrail`, which
    refuses a skipped rung at the moment it would happen, and the verdict type
    refuses to carry neither a next rung nor a reason for stopping. A silent
    dead end is not expressible through this function.
    """
    trail = LadderTrail()
    if request_type == RequestType.BROWSER:
        # The caller asked for the server browser directly. Rung 1 was not
        # tried — said out loud rather than skipped, so the trail stays legal
        # and a reader can see a human made that choice.
        trail.record(
            "http",
            ok=False,
            note=(
                "The caller asked for our server browser directly, so the plain "
                "fetch was not tried."
            ),
        )
        trail.record(
            "browser",
            ok=_usable(result),
            reason=None if _usable(result) else _ladder_reason(result),
            chars=result.content_chars,
        )
    else:
        trail.record(
            "http",
            ok=http_ok,
            reason=None if http_ok else http_reason,
            chars=http_chars,
        )
        if result.browser_attempted:
            trail.record(
                "browser",
                ok=result.engine == ENGINE_BROWSER and _usable(result),
                reason=None if _usable(result) else _ladder_reason(result),
                note=result.escalation_note,
                chars=result.content_chars,
            )
        elif not _usable(result):
            # The server browser was NOT spent — because this failure is not one
            # it can beat, because the deployment has no browser, or because an
            # operator turned the hand-off off. Recording it as a declined rung
            # rather than leaving it out is the difference between a trail that
            # says "we chose not to" and a verdict that points at a rung nobody
            # will ever run: `next_rung: "browser"` on a scrape that has already
            # finished is a dead end, and it was a real one (LinkedIn's feed,
            # 2026-09-17, came back `wrong_resource` — a class the browser leg
            # does not take — and the ladder pointed at a rung that would never
            # happen).
            trail.record(
                "browser",
                ok=False,
                reason=_ladder_reason(result),
                note=(
                    result.escalation_note
                    or "We did not spend our server browser on this: it is not a wall "
                    "a renderer gets past."
                ),
                chars=result.content_chars,
            )

    if residential_entry is not None:
        # An optional entry: it never changes which rung may follow, and a trail
        # without it is still complete (`matrx_scraper.ladder.OPTIONAL_RUNGS`).
        trail.entries = [*trail.entries, residential_entry]

    result.rung_trail = trail.entries

    if _usable(result):
        return result

    verdict = trail.verdict(reason=_ladder_reason(result), policy=policy)
    for key, value in verdict.as_fields().items():
        setattr(result, key, value)

    # A BLOCK IS A FINDING. This is the one place an unusable scrape is finally judged, so it
    # is the one place the wall is announced — every content-sanity refusal, every proxy
    # refusal, every bad status, with the trail exactly as it stands. The host decides whether
    # anything is written; announcing never raises and never waits.
    _announce_the_wall(result, verdict=verdict, organization_id=organization_id)
    return result


def _announce_the_wall(
    result: ScrapeResult,
    *,
    verdict: Any,
    organization_id: str | None,
) -> None:
    """Hand this failure to whatever ledger the host wired up. Never raises."""
    reason = _ladder_reason(result) or "unusable_result"
    sentence = (
        result.failure_message
        or getattr(verdict, "note", "")
        or escalation_sentence(reason)
        or f"The scraper could not read this page: {reason}."
    )
    announce_block(
        organization_id=organization_id,
        input_ref=result.url,
        input_label=(result.title or "")[:300],
        source_type="web_page",
        engine="server_browser" if result.engine == ENGINE_BROWSER else "scraper",
        rung="browser" if result.engine == ENGINE_BROWSER else "http",
        rung_trail=list(result.rung_trail or []),
        error_class=reason,
        error_sentence=sentence,
        detail={
            "status_code": result.status_code,
            "response_url": result.response_url,
            "engine": result.engine,
            "content_chars": result.content_chars,
            "proxy_bypassed": getattr(result, "proxy_bypassed", None),
            "next_rung": getattr(result, "next_rung", None),
            "stopped_because": getattr(result, "stopped_because", None),
        },
    )


async def scrape(
    url: str,
    use_proxy: bool = True,
    request_type: RequestType = RequestType.NORMAL,
    fast: bool = False,
    cache: Any = None,
    domain_config: Any = None,
    browser_pool: Any = None,
    user_agent: str | None = None,
    escalate: bool | None = None,
    ladder_policy: LadderPolicy | None = None,
    organization_id: str | None = None,
    acting_user_id: str | None = None,
) -> ScrapeResult:
    """Fetch and fully parse a single URL. Always async — never blocks.

    `user_agent`, when set, overrides the User-Agent for whichever transport
    this call ends up using (HTTP or browser). `None` = no override.

    `organization_id` is the organization this scrape ACTS IN, and it only
    matters when a `cache` is passed: the cached page is an org-scoped row, so
    the read is filtered by it and the write carries it. A router resolves it at
    the boundary (`confirm_request_organization`); leaving it `None` makes the
    cache read the carried request context, and a cache operation that finds no
    organization at all REFUSES rather than defaulting one.

    `escalate` overrides the deployment's `SCRAPER_BROWSER_ESCALATION` setting
    for this one call: `True` forces the browser hand-off on a failure the
    browser could plausibly beat, `False` forbids it (a caller reproducing a
    raw HTTP result), `None` follows the setting. The result ALWAYS states
    which engine produced it (`engine`) and, when it escalated, why
    (`escalation_reason`, `escalation_note`).

    `ladder_policy` says which of the two CLIENT rungs — the person's own
    logged-in Chrome (`own_browser`) and the person driving it themselves
    (`human_drive`) — the caller's organization allows. Neither runs here; the
    result simply names which one could read this page next, and why, so the
    queue in aidream and the screens in matrx-frontend / matrx-extend all read
    one answer. Contract:
    `common-docs/projects/acquisition-frontier/extension-ladder/CONTRACT.md`.

    `acting_user_id` is the PERSON this scrape is running for, and it is the
    only thing that can unlock residential egress: after the ladder ends in a
    block, this page gets exactly one retry through a computer THAT PERSON
    registered, and never through anyone else's. A run with no acting user (a
    schedule, a service token) gets no retry and the trail says so. Contract:
    `common-docs/systems/platform/residential-egress/FEATURE.md`.
    """
    ladder_policy = ladder_policy or LadderPolicy()
    user_agent = normalize_user_agent(user_agent)
    if domain_config is not None:
        if not domain_config.is_scrape_allowed(url):
            # WE refused this, not the site. No rung of the ladder changes that,
            # and offering a person their own browser for it would be a lie.
            blocked = ScrapeResult(
                url=url,
                response_url=url,
                success=False,
                content_type="unknown",
                failure_reason="domain_blocked",
            )
            blocked.rung_trail = [
                ladder_trail_entry(
                    rung="http",
                    ok=False,
                    reason="domain_blocked",
                    note="This address is on this deployment's do-not-scrape list.",
                )
            ]
            blocked.next_rung_reason = "domain_blocked"
            blocked.stopped_because = STOP_NOT_ESCALATABLE
            blocked.next_rung_note = (
                "We did not try this page at all: this address is on the "
                "do-not-scrape list, and no browser changes that."
            )
            return blocked

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
        cached = await cache.get(
            url_info.unique_page_name, organization_id=organization_id
        )
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
            # A cached body is not an engine result — say where it came from,
            # while preserving which engine originally produced it.
            result.engine = ENGINE_CACHE
            if content.get("engine") in (ENGINE_HTTP, ENGINE_BROWSER):
                result.escalation_note = (
                    f"Served from our cache; originally captured by the {content['engine']} engine."
                )
            result.rung_trail = [
                ladder_trail_entry(
                    rung="http",
                    ok=True,
                    note="Served from our cache — no new request was made.",
                    chars=result.content_chars,
                )
            ]
            return result

    proxy_type = "datacenter"
    # WE decided this address leaves on a direct connection. That decision binds
    # every exit, including a person's home computer — a policy that only holds
    # until the first block is not a policy.
    proxy_forbidden_by_policy = False
    if domain_config is not None:
        proxy_type = domain_config.get_proxy_type(url)
        if proxy_type == "none":
            use_proxy = False
            proxy_forbidden_by_policy = True

    pool = _resolve_browser_pool(browser_pool)
    result = await _fetch_and_parse(
        url,
        request_type=request_type,
        use_proxy=use_proxy,
        fast=fast,
        browser_pool=pool,
        user_agent=user_agent,
    )
    _apply_content_sanity(result)
    # Rung 1's own verdict, snapshotted BEFORE the browser leg can replace the
    # result object — otherwise an escalation that succeeds erases the evidence
    # that the plain fetch ever failed, and the trail lies by omission.
    http_ok = _usable(result)
    http_reason = None if http_ok else _ladder_reason(result)
    http_chars = result.content_chars

    if request_type != RequestType.BROWSER:
        # A bot check is often transient — one cheap delayed retry before we
        # spend a pooled browser (proven live on Medium, 2026-09-17: 403 then
        # 200 seconds later on a near-identical request).
        if result.failure_reason == FailureReason.CLOUDFLARE_BLOCK.value:
            await asyncio.sleep(CHALLENGE_RETRY_DELAY_SECONDS)
            retried = await _fetch_and_parse(
                url,
                request_type=RequestType.NORMAL,
                use_proxy=use_proxy,
                fast=fast,
                browser_pool=pool,
                user_agent=user_agent,
            )
            _apply_content_sanity(retried)
            if retried.success:
                retried.escalation_note = (
                    "The site showed a bot check on the first try; a second attempt "
                    "moments later went through."
                )
                result = retried

        result = await _maybe_escalate_to_browser(
            result,
            url=url,
            use_proxy=use_proxy,
            fast=fast,
            browser_pool=pool,
            user_agent=user_agent,
            escalate=escalate,
        )

    # The last exit we own: the acting person's own computer, once, for this
    # page only. It runs BEFORE the ladder is sealed so a page it rescues never
    # lands a block in the ledger, and so the trail carries the attempt either
    # way.
    result, residential_entry = await _maybe_retry_through_residential_egress(
        result,
        url=url,
        acting_user_id=acting_user_id,
        fast=fast,
        browser_pool=pool,
        user_agent=user_agent,
        proxy_forbidden_by_policy=proxy_forbidden_by_policy,
    )

    result = _seal_ladder(
        result,
        request_type=request_type,
        http_ok=http_ok,
        http_reason=http_reason,
        http_chars=http_chars,
        policy=ladder_policy,
        organization_id=organization_id,
        residential_entry=residential_entry,
    )

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
                organization_id=organization_id,
            )
        except Exception:
            logger.warning("Failed to write cache for %s", redact_url_secrets(url), exc_info=True)

    return result


async def scrape_many(
    urls: list[str],
    use_proxy: bool = True,
    concurrency: int = 20,
    fast: bool = False,
    cache: Any = None,
    domain_config: Any = None,
    browser_pool: Any = None,
    escalate: bool | None = None,
    ladder_policy: LadderPolicy | None = None,
    organization_id: str | None = None,
    acting_user_id: str | None = None,
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
                escalate=escalate,
                ladder_policy=ladder_policy,
                organization_id=organization_id,
                acting_user_id=acting_user_id,
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
    escalate: bool | None = None,
    ladder_policy: LadderPolicy | None = None,
    organization_id: str | None = None,
    acting_user_id: str | None = None,
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
                escalate=escalate,
                ladder_policy=ladder_policy,
                organization_id=organization_id,
                acting_user_id=acting_user_id,
            )

    coros = [_bounded(u) for u in urls]
    for future in asyncio.as_completed(coros):
        yield await future
