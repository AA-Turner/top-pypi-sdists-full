from __future__ import annotations

import asyncio
import enum
import ipaddress
import json
import logging
import os
import random
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from urllib.parse import urljoin, urlparse, urlsplit

import bs4
import httpx
from dotenv import load_dotenv
from httpx import Timeout
from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser

from matrx_utils.outbound_guard import (
    NUMERIC_HOST_SENTENCE,
    OutboundHostUnresolved,
    OutboundUrlRefused,
    resolve_public_address,
    resolve_public_address_sync,
)

from matrx_scraper.utils.proxy import playwright_proxy
from matrx_scraper.user_agents import normalize_user_agent
from matrx_scraper.utils.proxy import redact_url_secrets

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Try to import curl_cffi for better TLS fingerprinting.
# Use the SYNC Session on a worker thread — AsyncSession.__aexit__ calls
# curl_multi_cleanup on the event loop and has stalled aidream-api (~1s+).
try:
    from curl_cffi import CurlInfo, CurlOpt
    from curl_cffi.requests import Session as CurlCffiSession

    CURL_CFFI_AVAILABLE = True
except ImportError:
    CurlInfo = None  # type: ignore[misc, assignment]
    CurlOpt = None  # type: ignore[misc, assignment]
    CurlCffiSession = None  # type: ignore[misc, assignment]
    CURL_CFFI_AVAILABLE = False


def _curl_pin_options(url: str, *, direct: bool) -> dict[Any, Any]:
    """Check one hop; on a direct connection return the curl option that pins it."""
    try:
        # allow_http=True: crawling http sites is this engine's job.
        ip = resolve_public_address_sync(url, allow_http=True)
    except OutboundHostUnresolved:
        if direct:
            raise
        return {}
    if not direct or CurlOpt is None:
        return {}
    parts = urlsplit(url)
    # curl treats a literal-IP host as the address itself and never consults
    # CURLOPT_RESOLVE. The guard admits only CANONICAL literals, so a literal
    # here must equal the checked IP — anything else is refused, never sent.
    literal = (parts.hostname or "").strip("[]")
    try:
        is_literal = bool(ipaddress.ip_address(literal))
    except ValueError:
        is_literal = False
    if is_literal and ipaddress.ip_address(literal) != ipaddress.ip_address(ip):
        raise OutboundUrlRefused(NUMERIC_HOST_SENTENCE)
    port = parts.port or (443 if (parts.scheme or "").lower() == "https" else 80)
    pinned = f"[{ip}]" if ":" in ip else ip
    return {CurlOpt.RESOLVE: [f"{parts.hostname}:{port}:{pinned}"]}


def _curl_cffi_get_sync(
    url: str,
    *,
    impersonate: str,
    headers: dict[str, str],
    proxy: str | None,
    is_likely_binary: bool,
) -> dict[str, Any]:
    """Blocking curl_cffi GET — always run via ``asyncio.to_thread``."""
    assert CurlCffiSession is not None
    # STARTTRANSFER_TIME_T is curl's own time-to-first-byte (microseconds):
    # DNS + connect + TLS + the server's think time, stopping the instant the
    # first response byte lands. It is NOT total elapsed time, which keeps
    # running through the body download — and that difference is the entire
    # point of the `ttfb_server_response` SEO check. Asking for the info costs
    # nothing and changes nothing about how the body is read.
    with CurlCffiSession(
        impersonate=impersonate, curl_infos=[CurlInfo.STARTTRANSFER_TIME_T]
    ) as session:
        current_url = url
        redirect_chain: list[dict[str, Any]] = []
        # Summed across hops — Google's TTFB includes redirect time, so a page
        # that bounces through two 301s owns the latency of all three requests.
        # Goes None the moment ANY hop fails to report: a partial sum is a
        # quietly wrong number, and the check must answer n_a instead.
        ttfb_us: int | None = 0
        max_redirects = 10
        redirect_loop = False
        for redirect_count in range(max_redirects + 1):
            # EVERY hop is checked before it is requested. On a direct
            # connection the hop is also PINNED: CURLOPT_RESOLVE makes curl
            # connect to the exact IP the check approved, so a host whose DNS
            # answers public then private (rebinding) cannot land inside our
            # network. Through a proxy the proxy resolves the name, so the
            # check still runs (a refusal is final) but there is nothing of
            # ours to pin; a name only the proxy can resolve is let through.
            session.curl_options = _curl_pin_options(current_url, direct=proxy is None)
            resp = session.get(
                current_url,
                headers=headers,
                proxies={"http": proxy, "https": proxy} if proxy else None,
                timeout=15,
                allow_redirects=False,
            )
            hop_ttfb = (getattr(resp, "infos", None) or {}).get(CurlInfo.STARTTRANSFER_TIME_T)
            if ttfb_us is not None and isinstance(hop_ttfb, int) and hop_ttfb > 0:
                ttfb_us += hop_ttfb
            else:
                ttfb_us = None
            response_url = str(resp.url)
            location = resp.headers.get("location")
            if resp.status_code not in {301, 302, 303, 307, 308} or not location:
                break
            redirect_chain.append(
                {"status": int(resp.status_code), "url": response_url or current_url}
            )
            next_url = urljoin(response_url or current_url, location)
            if any(hop.get("url") == next_url for hop in redirect_chain):
                # A LOOP is an answer, not a transport failure: the server
                # responded every time, it just never arrives anywhere. Record
                # the revisit as the chain's last hop (so the loop is visible in
                # the evidence) and stop; the caller names it `redirect_loop`.
                # Raising here used to turn it into "status 0, never responded".
                redirect_chain.append({"status": None, "url": next_url, "revisit": True})
                redirect_loop = True
                break
            if redirect_count >= max_redirects:
                raise RuntimeError(f"redirect limit exceeded for {redact_url_secrets(url)!r} ({max_redirects})")
            current_url = next_url

        status_code = resp.status_code
        resp_headers = dict(resp.headers)
        response_url = str(resp.url)
        content_type_raw = resp_headers.get("content-type", "")
        ct_check = content_type_raw.lower()
        content_bytes: bytes | None = None
        content = ""
        if is_likely_binary or "application/pdf" in ct_check or ct_check.startswith("image/"):
            content_bytes = resp.content
        else:
            content = resp.text
        return {
            "status_code": status_code,
            "headers": resp_headers,
            "response_url": response_url,
            "redirect_chain": redirect_chain,
            "content_type_raw": content_type_raw,
            "content": content,
            "content_bytes": content_bytes,
            "ttfb_ms": round(ttfb_us / 1000) if ttfb_us is not None else None,
            "redirect_loop": redirect_loop,
        }


class RequestType(enum.StrEnum):
    BROWSER = "browser"
    NORMAL = "normal"


class ContentType(enum.StrEnum):
    HTML = "html"
    MARKDOWN = "md"
    PDF = "pdf"
    JSON = "json"
    XML = "xml"
    PLAIN_TEXT = "txt"
    IMAGE = "image"
    OTHER = "other"


BINARY_CONTENT_TYPES = {ContentType.PDF, ContentType.IMAGE}

EXTRACTABLE_CONTENT_TYPES = {
    ContentType.HTML,
    ContentType.PDF,
    ContentType.MARKDOWN,
    ContentType.JSON,
    ContentType.XML,
    ContentType.PLAIN_TEXT,
    ContentType.IMAGE,
}


def detect_content_type_from_url(url: str) -> ContentType | None:
    parsed = urlparse(url)
    path_part = parsed.path.rstrip("/")
    ext = path_part.rsplit(".", 1)[-1].lower() if "." in path_part else ""
    URL_EXT_MAP: dict[str, ContentType] = {
        "pdf": ContentType.PDF,
        "json": ContentType.JSON,
        "xml": ContentType.XML,
        "kml": ContentType.XML,
        "md": ContentType.MARKDOWN,
        "txt": ContentType.PLAIN_TEXT,
        "jpg": ContentType.IMAGE,
        "jpeg": ContentType.IMAGE,
        "png": ContentType.IMAGE,
        "gif": ContentType.IMAGE,
        "webp": ContentType.IMAGE,
        "bmp": ContentType.IMAGE,
        "tiff": ContentType.IMAGE,
        "svg": ContentType.IMAGE,
    }
    return URL_EXT_MAP.get(ext)


def content_type_from_header(content_type_raw: str | None) -> ContentType | None:
    """Map a raw ``Content-Type`` header to our token, from the header ALONE.

    The ONE header→token mapping in the codebase. :func:`detect_response_content_type`
    delegates to it (then refines with the body), and the body-less URL verification
    sweep (`web_crawl/url_verify.py`) is its other consumer — a HEAD response has a
    header and nothing else, and it must land on the exact same vocabulary the
    crawler writes to ``web.page.content_type_last`` or the two sources of that
    column would disagree about what a URL is.

    Returns ``None`` when the header is absent, empty, or unrecognized — "the
    response did not tell us", which callers must not confuse with a verdict.
    """

    if not content_type_raw:
        return None
    ct_lower = content_type_raw.lower()
    if "text/html" in ct_lower or "application/xhtml" in ct_lower:
        return ContentType.HTML
    if "text/markdown" in ct_lower or "text/x-markdown" in ct_lower:
        return ContentType.MARKDOWN
    if "application/pdf" in ct_lower:
        return ContentType.PDF
    if "application/json" in ct_lower or "+json" in ct_lower:
        return ContentType.JSON
    if "application/xml" in ct_lower or "text/xml" in ct_lower or "+xml" in ct_lower:
        return ContentType.XML
    if "text/plain" in ct_lower:
        return ContentType.PLAIN_TEXT
    if ct_lower.startswith("image/"):
        return ContentType.IMAGE
    return None


def detect_response_content_type(
    *,
    url: str,
    content_type_raw: str,
    content: str,
    content_bytes: bytes | None = None,
) -> tuple[ContentType, bool]:
    """Classify a fetched response from its headers, signature, body, and URL."""

    ct_lower = content_type_raw.lower()
    url_hint = detect_content_type_from_url(url)
    header_type = content_type_from_header(content_type_raw)
    # HTML and PDF headers are CLAIMS the body must corroborate; the rest of the
    # header mapping is taken at its word. Kept in this order so the body checks
    # below still win over a lying header, exactly as before.
    if "text/html" in ct_lower:
        is_html = bool(re.search(r"<html|<body|<head|<!doctype", content, re.I))
        return (ContentType.HTML if is_html else ContentType.OTHER), is_html
    if "application/pdf" in ct_lower:
        valid_pdf = bool(
            (content_bytes and content_bytes[:5] == b"%PDF-") or content.startswith("%PDF-")
        )
        return (ContentType.PDF if valid_pdf else ContentType.OTHER), False
    if header_type is not None and header_type is not ContentType.HTML:
        return header_type, False
    if content_bytes and content_bytes[:5] == b"%PDF-":
        return ContentType.PDF, False
    if content.startswith("%PDF-"):
        return ContentType.PDF, False
    if re.search(r"<html|<body|<head|<!doctype", content, re.I):
        return ContentType.HTML, True
    if url_hint:
        return url_hint, url_hint == ContentType.HTML
    return ContentType.OTHER, False


class FailureReason(enum.StrEnum):
    NON_HTML_CONTENT = "non_html_content"
    LOW_TEXT_CONTENT = "low_text_content"
    BAD_STATUS = "bad_status"
    PARSE_ERROR = "parse_error"
    CLOUDFLARE_BLOCK = "cloudflare_block"
    BLOCKED = "blocked"
    #: The redirect chain came back to a URL it already visited. Persisted as
    #: `web.crawl_url.reason_code='redirect_loop'` with the chain (revisit last).
    REDIRECT_LOOP = "redirect_loop"
    REQUEST_ERROR = "request_error"
    PROXY_ERROR = "proxy_error"
    #: The address (or a redirect hop) resolves inside a private or internal
    #: network. WE refused it before sending anything; no retry, proxy, direct
    #: fallback or browser changes that.
    ADDRESS_REFUSED = "address_refused"


class ProxyConfigurationError(RuntimeError):
    pass


class ProxyPoolExhaustedError(RuntimeError):
    """Every configured proxy refused a request AND no proxy has carried any
    request within `proxy_health.REFUSAL_MEMORY_SECONDS` — the pool itself is
    down. A full-pool refusal of one destination while other hosts flow is a
    per-host vendor refusal (`proxy_health` `refused_hosts`), never this."""


_proxy_pool_exhausted = False


class CMS(enum.StrEnum):
    WORDPRESS = "wordpress"
    SHOPIFY = "shopify"
    UNKNOWN = "unknown"


class Firewall(enum.StrEnum):
    CLOUDFLARE = "cloudflare"
    AWS_WAF = "aws_waf"
    NONE = "none"
    DATADOME = "datadome"


CLOUDFLARE_RETRY_CSS_SELECTORS = [
    '#turnstile-wrapper iframe[src^="https://challenges.cloudflare.com"]',
]

RETRY_CSS_SELECTORS = [
    *CLOUDFLARE_RETRY_CSS_SELECTORS,
    'div#infoDiv0 a[href*="//www.google.com/policies/terms/"]',
    'iframe[src*="_Incapsula_Resource"]',
]

# A bot-protection interstitial is a BLOCK, not a status code — and it can be
# served with ANY status. Whoever consumes `failed_primary_reason` (the crawler's
# browser escalation, the retry policy, the UI) needs the specific diagnosis, so
# these outrank every other reason regardless of append order.
CHALLENGE_FAILURE_REASONS = (
    FailureReason.CLOUDFLARE_BLOCK,
    FailureReason.BLOCKED,
)


CHALLENGE_TITLE_MARKERS = ("cloudflare", "attention required", "just a moment")

# THE CHALLENGE CENSUS (2026-09-26: a Reddit "Prove your humanity" page landed as a Source).
# Every interstitial below is a wall, whatever status it is served with. Titles are exact
# phrases a vendor's challenge page uses; body phrases are matched only on a SHORT page (a real
# article that happens to embed a captcha on its comment form is not a wall).
BLOCK_TITLE_MARKERS = (
    "prove your humanity",          # Reddit
    "verify you are human",         # Cloudflare Turnstile / generic
    "are you a robot",              # generic
    "robot or human",               # Walmart / PerimeterX variants
    "human verification",           # generic
    "pardon our interruption",      # Imperva / Distil
    "one more step",                # Cloudflare (legacy captcha)
    "checking your browser",        # Cloudflare (legacy) / DDoS-Guard
    "ddos-guard",                   # DDoS-Guard
    "access denied",                # Akamai edge refusal ("Reference #…")
    "security check",               # generic
    "the request could not be satisfied",  # AWS CloudFront 403 ("ERROR: The request could not be satisfied")
)
BLOCK_BODY_MARKERS = (
    "prove your humanity",
    "let us know you're a real person",
    "let us know you’re a real person",
    "verify you are human",
    "checking if the site connection is secure",   # Cloudflare
    "enable javascript and cookies to continue",   # Cloudflare
    "press & hold",                                # PerimeterX
    "please verify you are a human",               # PerimeterX
    "why have i been blocked",                     # Cloudflare block page
    "you don't have permission to access",         # Akamai "Access Denied … Reference #"
    "request unsuccessful. incapsula incident id", # Imperva
    "the request could not be satisfied",          # AWS CloudFront 403
    "please complete the security check",          # Cloudflare legacy captcha ("One more step")
    "completing the captcha proves you are a human",  # Cloudflare legacy captcha
    "let's confirm you are human",                 # generic "Human Verification"
)
BLOCK_WIDGET_SELECTORS = (
    'iframe[src*="hcaptcha.com"]',
    "div.h-captcha",
    'iframe[src*="google.com/recaptcha"]',
    "div.g-recaptcha",
    "#px-captcha",                                  # PerimeterX
    'script[src*="captcha-delivery.com"]',          # DataDome
    'iframe[src*="captcha-delivery.com"]',
)
#: A page at or under this much visible text that shows a challenge phrase or widget is the
#: wall itself, not an article with a captcha somewhere on it.
SHORT_PAGE_CHARS = 2000


def detect_challenge_reasons(
    *,
    soup: HTMLParser | None = None,
    html: str | None = None,
    title: str | None = None,
) -> list[dict]:
    """Bot-protection signatures in a response — ONE classifier, every fetch path.

    The HTTP path passes its already-parsed soup; the crawler's browser capture
    passes raw HTML. A second hand-rolled copy of these checks is exactly how
    the browser path came to label every challenge `bad_status`.
    """
    if soup is None and html:
        try:
            soup = HTMLParser(html)
        except Exception:
            soup = None
    reasons: list[dict] = []
    if soup is not None:
        for selector in RETRY_CSS_SELECTORS:
            if soup.css_first(selector):
                reason = (
                    FailureReason.CLOUDFLARE_BLOCK
                    if selector in CLOUDFLARE_RETRY_CSS_SELECTORS
                    else FailureReason.BLOCKED
                )
                reasons.append({reason: f"Selector matched: {selector}"})
    if title and any(marker in title.lower() for marker in CHALLENGE_TITLE_MARKERS):
        reasons.append({FailureReason.CLOUDFLARE_BLOCK: f"Title indicates block: {title}"})
    elif title and any(marker in title.lower() for marker in BLOCK_TITLE_MARKERS):
        reasons.append({FailureReason.BLOCKED: f"Title is a bot challenge: {title}"})
    if not reasons and soup is not None:
        body = soup.body
        text = " ".join((body.text(separator=" ") if body is not None else "").split()).lower()
        if len(text) <= SHORT_PAGE_CHARS:
            phrase = next((m for m in BLOCK_BODY_MARKERS if m in text), None)
            if phrase:
                reasons.append({FailureReason.BLOCKED: f"Page is a bot challenge: {phrase!r}"})
            else:
                widget = next((sel for sel in BLOCK_WIDGET_SELECTORS if soup.css_first(sel)), None)
                if widget:
                    reasons.append({FailureReason.BLOCKED: f"Short page is a captcha: {widget}"})
    return reasons


def challenge_text_reason(*, title: str | None, text: str | None) -> str | None:
    """The same census over a page already reduced to TITLE + TEXT (no HTML kept).

    For consumers that stored only the extracted text of a capture — coverage keeps an
    excerpt, not the DOM. Only a SHORT page can be the wall itself: a long article whose
    title happens to contain "Access Denied" is an article.
    """
    body = " ".join((text or "").split()).lower()
    if len(body) > SHORT_PAGE_CHARS:
        return None
    lowered_title = (title or "").strip().lower()
    marker = next(
        (m for m in (*CHALLENGE_TITLE_MARKERS, *BLOCK_TITLE_MARKERS) if lowered_title and m in lowered_title),
        None,
    )
    if marker:
        return f"the page title is a bot or access wall ({title!s})"
    phrase = next((m for m in BLOCK_BODY_MARKERS if m in body), None)
    if phrase:
        return f"the page is a bot or access wall ({phrase!r})"
    return None


def wall_reason_from_status(
    status_code: int | None, headers: dict[str, str] | None
) -> tuple[FailureReason, str] | None:
    """A wall the response HEADERS and STATUS declare, with no body marker needed.

    Order (OPENSEO-TOOLS-SPEC §8.1): 429 first — the origin throttling us is the
    crawler's rate-limit path, never a block — then Cloudflare's own
    ``cf-mitigated`` header (its challenge, whatever the status), then 401/403
    (the origin refusing us). A 503 with a challenge marker is already caught by
    :func:`detect_challenge_reasons`. A blocked URL was never seen failing, so
    the audit must never count it as a broken link.
    """
    status = int(status_code or 0)
    if status == 429:
        return None
    mitigated = None
    for key, value in (headers or {}).items():
        if str(key).lower() == "cf-mitigated":
            mitigated = str(value)
            break
    if mitigated:
        return (
            FailureReason.CLOUDFLARE_BLOCK,
            f"Cloudflare mitigated the request (cf-mitigated: {mitigated}, HTTP {status})",
        )
    if status in (401, 403):
        return (FailureReason.BLOCKED, f"The site refused the request (HTTP {status})")
    return None


def primary_failure_reason(fatal_reasons: list[dict]) -> FailureReason:
    """The most SPECIFIC diagnosis, not the first one appended.

    The status check appends BAD_STATUS before the challenge selectors run, so
    first-wins labelled a Cloudflare interstitial served as 503 `bad_status` —
    and the crawler's browser escalation, which keys on that label, skipped the
    one fetch that recovers a challenge page.
    """
    if any(FailureReason.ADDRESS_REFUSED in reason for reason in fatal_reasons):
        return FailureReason.ADDRESS_REFUSED
    for preferred in CHALLENGE_FAILURE_REASONS:
        if any(preferred in reason for reason in fatal_reasons):
            return preferred
    return list(fatal_reasons[0].keys())[0]


ROTATE_PROXY_ERRORS = [
    "ECONNRESET",
    "ECONNREFUSED",
    "ERR_PROXY_CONNECTION_FAILED",
    "ERR_TUNNEL_CONNECTION_FAILED",
    "Proxy responded with",
    "unsuccessful tunnel",
    "TunnelUnsuccessful",
    "CONNECT tunnel failed",
    "response 407",
]

# Coherent browser header profiles for anti-detection
# Using stable impersonate values supported by curl_cffi
HEADER_PROFILES = [
    {
        "name": "Chrome 131 Windows",
        "impersonate": "chrome131",  # For curl_cffi
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Sec-Ch-Ua": '"Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        },
    },
    {
        "name": "Chrome 120 macOS",
        "impersonate": "chrome120",  # Stable version
        "headers": {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Sec-Ch-Ua": '"Chromium";v="120", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        },
    },
    {
        "name": "Chrome 110 Windows",
        "impersonate": "chrome110",  # Fallback stable version
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Ch-Ua": '"Chromium";v="110", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        },
    },
]


def get_random_header_profile() -> dict:
    """Get a random coherent browser header profile"""
    profile = random.choice(HEADER_PROFILES)
    return profile.copy()


async def human_like_delay(min_seconds: float = 1.0, max_seconds: float = 3.0):
    """Add a randomized delay to mimic human browsing behavior"""
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)


def get_random_proxy() -> str | None:
    """Get a random proxy from the available pool"""
    proxies_str = os.getenv("DATACENTER_PROXIES")
    if not proxies_str:
        return None

    proxies = [p.strip() for p in proxies_str.split(",") if p.strip()]
    if not proxies:
        return None

    return random.choice(proxies)


def get_required_random_proxy() -> str:
    proxy = get_random_proxy()
    if not proxy:
        raise ProxyConfigurationError(
            "Proxy-backed fetch requested but DATACENTER_PROXIES is missing or empty"
        )
    return proxy


def _to_iso_timestamp(timestamp: str | None) -> str | None:
    if not timestamp:
        return None
    try:
        # Handle timezone-aware and naive ISO formats first (cheap path).
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.isoformat()
    except (ValueError, TypeError):
        pass
    # Fall back to the permissive parser for the long tail of formats
    # publishers stamp pages with: "10/21/2013 19:00:00", "Mon, 21 Oct 2013",
    # "March 26 2025", etc. Returning the raw string here is a footgun for
    # downstream consumers (every ORM / Pydantic write rejects it), so we
    # either normalise to ISO or return None.
    try:
        from dateutil import parser as _dateutil_parser  # noqa: PLC0415
    except ImportError:
        return None
    try:
        return _dateutil_parser.parse(timestamp, fuzzy=False).isoformat()
    except (ValueError, TypeError, OverflowError):
        return None


def _extract_publication_dates(
    meta_tags: dict[str, Any], json_ld: list[Any]
) -> tuple[str | None, str | None]:
    published = (
        meta_tags.get("article:published_time")
        or meta_tags.get("og:article:published_time")
        or meta_tags.get("datepublished")
        or meta_tags.get("date")
        or None
    )
    modified = (
        meta_tags.get("article:modified_time")
        or meta_tags.get("og:article:modified_time")
        or meta_tags.get("datemodified")
        or meta_tags.get("last-modified")
        or None
    )

    if not published or not modified:
        for ld in json_ld:
            if isinstance(ld, dict):
                pub = ld.get("datePublished")
                mod = ld.get("dateModified")
                if pub:
                    published = published or pub
                if mod:
                    modified = modified or mod
                if "@graph" in ld:
                    for item in ld["@graph"]:
                        if isinstance(item, dict):
                            pub = item.get("datePublished")
                            mod = item.get("dateModified")
                            if pub:
                                published = published or pub
                            if mod:
                                modified = modified or mod
            elif isinstance(ld, list):
                for item in ld:
                    if isinstance(item, dict):
                        pub = item.get("datePublished")
                        mod = item.get("dateModified")
                        if pub:
                            published = published or pub
                        if mod:
                            modified = modified or mod

    return _to_iso_timestamp(published), _to_iso_timestamp(modified)


def extract_publication_dates_from_html(html: str) -> tuple[str | None, str | None]:
    """(published_at, modified_at) ISO strings from raw HTML — the same meta-tag
    + JSON-LD extraction `fetch()` performs, for callers that obtained their
    HTML elsewhere (e.g. a browser-rendered rescue)."""
    if not html:
        return None, None
    try:
        soup = HTMLParser(html)
    except Exception:
        return None, None
    meta_tags: dict[str, Any] = {}
    for meta in soup.css("meta"):
        name = (
            meta.attrs.get("name")
            or meta.attrs.get("property")
            or meta.attrs.get("http-equiv")
            or ""
        ).lower()
        if name:
            meta_tags[name] = meta.attrs.get("content")
    json_ld: list[Any] = []
    for script in soup.css('script[type="application/ld+json"]'):
        try:
            json_ld.append(json.loads(script.text()))
        except json.JSONDecodeError:
            continue
    return _extract_publication_dates(meta_tags, json_ld)


class ScrapingSession:
    """
    Manages a scraping session for same-domain requests.
    Maintains cookies, headers, and proxy consistency across requests.
    """

    def __init__(self, domain: str, proxy: str | None = None, header_profile: dict | None = None):
        self.domain = domain
        self.proxy = proxy or get_required_random_proxy()
        self.header_profile = header_profile or get_random_header_profile()
        self.last_url: str | None = None
        self.request_count = 0

    async def fetch(self, url: str, add_referer: bool = True) -> Response:
        """
        Fetch a URL within this session.
        Automatically adds Referer header for subsequent requests.
        """
        # Add human-like delay between requests (except first)
        if self.request_count > 0:
            await human_like_delay(1.0, 3.0)

        # Prepare headers with Referer if this is a subsequent request
        headers = self.header_profile["headers"].copy()
        if add_referer and self.last_url:
            headers["Referer"] = self.last_url

        # Create a new header profile dict with updated headers
        session_profile = self.header_profile.copy()
        session_profile["headers"] = headers

        # Fetch with session settings
        response = await fetch(
            url=url,
            request_type=RequestType.NORMAL,
            proxy=self.proxy,
            use_curl_cffi=True,
            header_profile=session_profile,
        )

        # Update session state
        self.last_url = url
        self.request_count += 1

        return response


@dataclass
class Response:
    request_url: str
    proxy_used: bool
    request_type: RequestType
    content_type: ContentType
    extension: str
    content_type_raw: str
    response_url: str
    response_headers: dict[str, str]
    status_code: int
    content: str = field(repr=False)
    content_bytes: bytes | None = field(default=None, repr=False)
    failed: bool = False
    failed_primary_reason: FailureReason | None = None
    failed_reasons: list[dict[FailureReason, str]] = field(default_factory=list)
    published_at: str | None = None
    modified_at: str | None = None
    cms_primary: CMS | None = None
    cms_other: list[CMS] = field(default_factory=list)
    firewall: Firewall = Firewall.NONE
    other_extensions: list[str] = field(default_factory=list)
    selectolax_soup: HTMLParser | None = None
    soup: bs4.BeautifulSoup | None = None
    title: str | None = None
    # Multi-hop redirect chain captured from response.history. Each entry
    # is {status: int, url: str}. Empty when the client didn't expose it.
    redirect_chain: list[dict[str, Any]] = field(default_factory=list)
    # TRUE time to first byte, in ms — request start to the first response
    # byte, redirect hops included. Distinct from any wall-clock timing a
    # caller takes around the fetch, which also covers the body download.
    # None means the transport could not report it (today: the Playwright
    # browser path), and every consumer must treat that as "not measured".
    ttfb_ms: int | None = None
    # True when this response came back on a DIRECT connection after the
    # configured proxy pool refused to carry the request (CONNECT 403/407).
    # Never silent: the result carries it to the caller so "we reached this
    # without our proxy" is a stated fact, not an invisible policy change.
    proxy_bypassed: bool = False

    def to_dict(self) -> dict:
        d = {
            k: v.value if isinstance(v, enum.Enum) else v
            for k, v in self.__dict__.items()
            if k not in ["selectolax_soup", "content_bytes"]
        }
        d["other_extensions"] = self.other_extensions
        d["response_headers"] = self.response_headers
        d["cms_other"] = [c.value for c in self.cms_other]
        d["failed_reasons"] = [{k.value: v for k, v in r.items()} for r in self.failed_reasons]
        if self.failed_primary_reason:
            d["failed_primary_reason"] = self.failed_primary_reason.value
        if self.cms_primary:
            d["cms_primary"] = self.cms_primary.value
        d["firewall"] = self.firewall.value
        return d


def _unresolved_text(exc: OutboundHostUnresolved) -> str:
    """The sentence plus the resolver's own words, which `unreachable` reads to
    tell a person the name does not exist (never a bare "request_error")."""
    cause = exc.__cause__
    return f"{exc} ({cause})" if cause is not None else str(exc)


async def _check_proxied_hop(request: httpx.Request) -> None:
    try:
        await resolve_public_address(str(request.url), allow_http=True)
    except OutboundHostUnresolved:
        return  # the proxy resolves the name; nothing of ours is reached
    # OutboundUrlRefused propagates: the hop is never sent.


def address_refused_response(
    url: str,
    request_type: RequestType,
    sentence: str,
    *,
    reason: FailureReason = FailureReason.ADDRESS_REFUSED,
    proxy_used: bool = False,
) -> Response:
    """The response for an address WE refused before sending anything."""
    logger.warning("scraper REFUSED %s: %s", redact_url_secrets(url), sentence)
    return Response(
        request_url=url,
        proxy_used=proxy_used,
        request_type=request_type,
        content_type=ContentType.OTHER,
        extension="",
        content_type_raw="",
        response_url=url,
        response_headers={},
        status_code=0,
        content="",
        failed=True,
        failed_primary_reason=reason,
        failed_reasons=[{reason: sentence}],
    )


async def fetch(
    url: str,
    request_type: RequestType = RequestType.NORMAL,
    proxy: str | None = None,
    use_curl_cffi: bool = True,
    header_profile: dict | None = None,
    user_agent: str | None = None,
) -> Response:
    """`user_agent`, when set, REPLACES the User-Agent this fetch would have
    sent — on the HTTP transports (curl_cffi and httpx) and on the inline
    Playwright branch alike. `None` means "no override": every transport keeps
    its existing behaviour byte-for-byte. See `matrx_scraper.user_agents`."""
    user_agent = normalize_user_agent(user_agent)
    proxy_used = bool(proxy)
    content = ""
    content_bytes: bytes | None = None
    title = None
    response_url = url
    status_code = 500
    headers = {}
    content_type_raw = ""
    failed = False
    failed_reasons = []
    failed_primary_reason = None
    content_type = ContentType.OTHER
    # Multi-hop redirect chain — populated from response.history when the
    # underlying client (curl_cffi or httpx) exposes it. Final response_url
    # is appended at the end so the chain ends at the destination.
    redirect_chain: list[dict[str, Any]] = []
    # True TTFB, filled in by whichever transport can measure it. Stays None
    # for the Playwright path — an unmeasured value, never a guessed one.
    ttfb_ms: int | None = None
    extension = ""
    other_extensions = []
    selectolax_soup = None
    published_at = None
    modified_at = None
    cms_primary = None
    cms_other = []
    firewall = Firewall.NONE

    # THE ADDRESS GATE — first, before anything parses the URL (a malformed
    # host must be a refusal with a sentence, never an exception from a helper),
    # before any engine, proxied or direct, and so before every direct fallback
    # (they all come back through here). allow_http=True: crawling http sites
    # is this engine's job.
    try:
        await resolve_public_address(url, allow_http=True)
    except OutboundHostUnresolved as exc:
        if proxy is None:
            return address_refused_response(
                url, request_type, _unresolved_text(exc), reason=FailureReason.REQUEST_ERROR
            )
    except OutboundUrlRefused as exc:
        return address_refused_response(url, request_type, str(exc), proxy_used=proxy_used)

    url_hint = detect_content_type_from_url(url)
    is_likely_binary = url_hint in BINARY_CONTENT_TYPES

    try:
        if request_type == RequestType.BROWSER:
            async with async_playwright() as p:
                # This is the server-side capture rung, never an interactive
                # handoff browser. It must not create a visible Chromium window
                # on a worker or during an offline crawl.
                launch_kwargs = {"headless": True}
                if proxy:
                    # Note: The proxy string must include the protocol, e.g., "http://127.0.0.1:8080"
                    launch_kwargs["proxy"] = playwright_proxy(proxy)
                browser = await p.chromium.launch(**launch_kwargs)
                # A UA override on the browser transport is a CONTEXT option —
                # there is no header to set. Without an override we still call
                # new_page() directly so the default path is unchanged.
                if user_agent:
                    browser_context = await browser.new_context(user_agent=user_agent)
                    page = await browser_context.new_page()
                else:
                    page = await browser.new_page()
                # Every request the page makes (navigation, each redirect hop,
                # every subresource) is checked; a non-public one is aborted.
                from matrx_scraper.ai_browser.url_guard import install_egress_guard

                await install_egress_guard(page.context)
                resp = await page.goto(url)
                content = await page.content()
                title = await page.title()
                response_url = page.url
                if resp:
                    status_code = resp.status
                    headers = await resp.all_headers()
                    content_type_raw = headers.get("content-type", "")
                    # Playwright tracks navigation redirects on the request
                    # object — walk redirected_from so browser fetches carry
                    # the same hop evidence as the HTTP transports.
                    try:
                        prior_requests = []
                        node = resp.request.redirected_from
                        while node is not None:
                            prior_requests.append(node)
                            node = node.redirected_from
                        for hop_request in reversed(prior_requests):
                            hop_response = await hop_request.response()
                            redirect_chain.append(
                                {
                                    "status": hop_response.status if hop_response else None,
                                    "url": hop_request.url,
                                }
                            )
                    except Exception as chain_exc:
                        logger.warning(
                            "redirect chain capture FAILED for %s — hop evidence lost: %s",
                            redact_url_secrets(url),
                            redact_url_secrets(chain_exc),
                        )
                        redirect_chain = []
                else:
                    status_code = 500
                    failed = True
                    failed_reasons.append(
                        {FailureReason.REQUEST_ERROR: "No response from page.goto"}
                    )
                await browser.close()
        else:
            # Select header profile (use provided or pick random)
            if not header_profile:
                header_profile = get_random_header_profile()

            request_headers = header_profile["headers"].copy()
            if user_agent:
                # Replace, never append. The profile's remaining headers
                # (Accept, Sec-Ch-Ua, ...) stay as-is: they are what make the
                # request coherent, and the caller asked to change WHO we say
                # we are, not to strip the rest of the request.
                request_headers["User-Agent"] = user_agent

            # Use curl_cffi if available (better TLS fingerprinting).
            # Sync Session in a worker thread — avoids blocking the event loop
            # on curl_multi_cleanup (see loop_watchdog stalls on aidream-api).
            if use_curl_cffi and CURL_CFFI_AVAILABLE:
                impersonate = header_profile.get("impersonate", "chrome131")
                fetched = await asyncio.to_thread(
                    _curl_cffi_get_sync,
                    url,
                    impersonate=impersonate,
                    headers=request_headers,
                    proxy=proxy,
                    is_likely_binary=is_likely_binary,
                )
                status_code = fetched["status_code"]
                headers = fetched["headers"]
                response_url = fetched["response_url"]
                redirect_chain.extend(fetched["redirect_chain"])
                content_type_raw = fetched["content_type_raw"]
                content = fetched["content"]
                content_bytes = fetched["content_bytes"]
                # `.get`: a transport result without a timing means "not
                # measured", which is a first-class state everywhere
                # downstream. It must never become a fetch failure.
                ttfb_ms = fetched.get("ttfb_ms")
                if fetched.get("redirect_loop"):
                    failed = True
                    failed_reasons.append(
                        {
                            FailureReason.REDIRECT_LOOP: (
                                f"Redirect loop: {redirect_chain[-1].get('url')} redirects back "
                                "to a URL already in its chain"
                            )
                        }
                    )
            else:
                # Fallback to httpx
                timeout_config = Timeout(15.0, connect=60.0)
                client_kwargs = {"timeout": timeout_config, "headers": request_headers}
                if proxy:
                    # Through a proxy: every hop (httpx follows redirects
                    # inside send) is re-checked by the request hook; the
                    # proxy, not us, resolves the name.
                    client_kwargs["proxy"] = proxy
                    client_kwargs["event_hooks"] = {"request": [_check_proxied_hop]}
                    http_client = httpx.AsyncClient(**client_kwargs)
                else:
                    # Direct: every hop checked AND pinned to the checked IP.
                    from matrx_utils.outbound_guard import public_only_client

                    http_client = public_only_client(allow_http=True, **client_kwargs)

                async with http_client as client:
                    # Sent as a STREAM purely to time the first byte: `send`
                    # returns the moment the response headers land, so the
                    # elapsed time to that point IS the TTFB (redirect hops
                    # included, since httpx follows them inside this call).
                    # `aread()` immediately after restores the ordinary
                    # buffered behaviour — `.text` / `.content` are unaffected.
                    request = client.build_request("GET", url)
                    ttfb_t0 = time.monotonic()
                    resp = await client.send(request, follow_redirects=True, stream=True)
                    ttfb_ms = round((time.monotonic() - ttfb_t0) * 1000)
                    try:
                        await resp.aread()
                    finally:
                        await resp.aclose()
                    status_code = resp.status_code
                    headers = dict(resp.headers)
                    response_url = str(resp.url)
                    # httpx exposes the full hop list on resp.history
                    try:
                        for hop in resp.history or []:
                            redirect_chain.append(
                                {
                                    "status": int(hop.status_code),
                                    "url": str(hop.url),
                                }
                            )
                    except Exception as chain_exc:
                        logger.warning(
                            "redirect chain capture FAILED for %s — hop evidence lost: %s",
                            redact_url_secrets(url),
                            redact_url_secrets(chain_exc),
                        )
                        redirect_chain = []
                    content_type_raw = headers.get("content-type", "")
                    ct_check = content_type_raw.lower()
                    if (
                        is_likely_binary
                        or "application/pdf" in ct_check
                        or ct_check.startswith("image/")
                    ):
                        content_bytes = resp.content
                        content = ""
                    else:
                        content = resp.text

    except Exception as e:
        failed = True
        error_text = _unresolved_text(e) if isinstance(e, OutboundHostUnresolved) else str(e)
        if isinstance(e, OutboundUrlRefused) and not isinstance(e, OutboundHostUnresolved):
            # A redirect hop resolved inside our network: refused, not an error
            # anyone can retry their way past.
            failed_reasons.append({FailureReason.ADDRESS_REFUSED: error_text})
        else:
            if proxy and any(err in error_text for err in ROTATE_PROXY_ERRORS):
                failed_reasons.append({FailureReason.PROXY_ERROR: error_text})
            failed_reasons.append({FailureReason.REQUEST_ERROR: error_text})
        content = ""
        title = None
        response_url = url
        # No answer came back, so there is no HTTP status to report (0), never a made-up 500:
        # a misspelled host read as "the site answered 500" (matrx_scraper.unreachable).
        status_code = 0
        headers = {}
        content_type_raw = ""
        # A failed fetch measured nothing — never carry a partial timing.
        ttfb_ms = None

    # One classifier serves HTTP and browser-backed crawl paths. Keeping this
    # decision centralized prevents a non-HTML response from being fed into the
    # HTML parser merely because Playwright fetched it.
    content_type, is_html = detect_response_content_type(
        url=response_url or url,
        content_type_raw=content_type_raw,
        content=content,
        content_bytes=content_bytes,
    )

    # Extension from URL or content_type
    parsed_url = urlparse(response_url)
    path = parsed_url.path
    if "." in path:
        ext_parts = path.split(".")[1:]
        extension = ext_parts[-1].lower()
        if len(ext_parts) > 1:
            other_extensions = ["." + e for e in ext_parts[:-1]]
    EXTENSION_MAP = {
        ContentType.HTML: "html",
        ContentType.MARKDOWN: "md",
        ContentType.PDF: "pdf",
        ContentType.JSON: "json",
        ContentType.XML: "xml",
        ContentType.PLAIN_TEXT: "txt",
    }
    if content_type in EXTENSION_MAP:
        extension = EXTENSION_MAP[content_type]

    # If is_html, parse
    meta_tags = {}
    json_ld = []
    if is_html:
        try:
            selectolax_soup = HTMLParser(content)
            if title is None:
                title_tag = selectolax_soup.css_first("title")
                title = title_tag.text(strip=True) if title_tag else ""
            # Extract meta tags
            for meta in selectolax_soup.css("meta"):
                name = (
                    meta.attrs.get("name")
                    or meta.attrs.get("property")
                    or meta.attrs.get("http-equiv")
                    or ""
                ).lower()
                if name:
                    meta_tags[name] = meta.attrs.get("content")
            # Extract JSON-LD
            for script in selectolax_soup.css('script[type="application/ld+json"]'):
                try:
                    data = json.loads(script.text())
                    json_ld.append(data)
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            failed = True
            failed_reasons.append({FailureReason.PARSE_ERROR: str(e)})
            selectolax_soup = None

    # Failure checks
    if status_code >= 400:
        failed = True
        failed_reasons.append({FailureReason.BAD_STATUS: f"Status code {status_code}"})
    if not is_html and content_type not in EXTRACTABLE_CONTENT_TYPES:
        failed = True
        failed_reasons.append({FailureReason.NON_HTML_CONTENT: content_type_raw})
    challenge_reasons = detect_challenge_reasons(
        soup=selectolax_soup if is_html else None,
        title=title,
    )
    if challenge_reasons:
        failed = True
        failed_reasons.extend(challenge_reasons)
    wall_reason = wall_reason_from_status(status_code, headers)
    if wall_reason is not None and not any(wall_reason[0] in r for r in failed_reasons):
        failed = True
        failed_reasons.append({wall_reason[0]: wall_reason[1]})

    # CMS detection
    if is_html and selectolax_soup:
        generator = (meta_tags.get("generator") or "").lower()
        if "wordpress" in generator:
            cms_primary = CMS.WORDPRESS
        elif selectolax_soup.css_first('meta[content*="shopify"]'):
            cms_primary = CMS.SHOPIFY
        # Additional fast checks
        if re.search(r"wp-content|wp-includes", content, re.I):
            if cms_primary is None:
                cms_primary = CMS.WORDPRESS
            elif cms_primary != CMS.WORDPRESS:
                cms_other.append(CMS.WORDPRESS)
        if re.search(r"cdn\.shopify\.com|shopify", content, re.I):
            if cms_primary is None:
                cms_primary = CMS.SHOPIFY
            elif cms_primary != CMS.SHOPIFY:
                cms_other.append(CMS.SHOPIFY)
        if cms_primary is None:
            cms_primary = CMS.UNKNOWN

    # Low text content check
    if is_html and selectolax_soup:
        # Create a copy to avoid modifying the original tree if it's needed elsewhere
        body_copy = selectolax_soup.body
        if body_copy:
            junk_selectors = "nav, header, footer, script, noscript, style"
            for node in body_copy.css(junk_selectors):
                node.decompose()
            text_content = body_copy.text(separator=" ", strip=True)
            if len(text_content) < 100:
                failed_reasons.append(
                    {FailureReason.LOW_TEXT_CONTENT: f"Text length {len(text_content)}"}
                )

    fatal_reasons = [
        reason for reason in failed_reasons if FailureReason.LOW_TEXT_CONTENT not in reason
    ]
    if fatal_reasons:
        failed = True
        failed_primary_reason = primary_failure_reason(fatal_reasons)

    # Firewall detection
    if "cf-ray" in headers or "cloudflare" in headers.get("server", "").lower():
        firewall = Firewall.CLOUDFLARE
    elif "x-amzn-requestid" in headers and "aws" in headers.get("server", "").lower():
        firewall = Firewall.AWS_WAF
    if any(FailureReason.CLOUDFLARE_BLOCK in r for r in failed_reasons):
        firewall = Firewall.CLOUDFLARE
    if ("x-datadome" in headers and headers["x-datadome"] == "protected") or any(
        header_key.startswith("x-datadome") for header_key in headers.keys()
    ):
        firewall = Firewall.DATADOME

    # Dates extraction
    if is_html:
        published_at, modified_at = _extract_publication_dates(meta_tags, json_ld)

    # Add the final hop onto the redirect chain so it ends at the
    # destination URL with its actual status, not the redirecting one.
    if not failed and response_url:
        if not redirect_chain or redirect_chain[-1].get("url") != response_url:
            redirect_chain.append({"status": status_code, "url": response_url})

    return Response(
        request_url=url,
        proxy_used=proxy_used,
        request_type=request_type,
        content_type=content_type,
        extension=extension,
        other_extensions=other_extensions,
        content_type_raw=content_type_raw,
        selectolax_soup=selectolax_soup,
        title=title,
        response_url=response_url,
        response_headers=headers,
        status_code=status_code,
        failed=failed,
        failed_primary_reason=failed_primary_reason,
        failed_reasons=failed_reasons,
        published_at=published_at,
        modified_at=modified_at,
        cms_primary=cms_primary,
        cms_other=cms_other,
        firewall=firewall,
        content=content,
        content_bytes=content_bytes,
        redirect_chain=redirect_chain,
        ttfb_ms=ttfb_ms,
    )


def direct_fallback_enabled() -> bool:
    """May a proxy-REFUSED request be retried on a direct connection?

    `fetch_normally_with_proxy` used to mean proxy-only, absolutely, and the
    documented reason was that a direct retry would "silently expose the host
    IP". The silence was the real hazard, not the direct connection: the site
    crawler has always done this fallback (`crawler._emit_proxy_bypass`) and
    is fine, because it ANNOUNCES it. So the absolute is now an announced
    policy — every rescued response carries `proxy_bypassed=True` and the
    result says so in plain English — and an operator who must keep the host
    IP off the wire sets `SCRAPER_DIRECT_FALLBACK=0`.

    Default ON because the alternative is what shipped: on 2026-09-17 our own
    proxy vendor's CONNECT-403 made SEC EDGAR, OSHA, the FDA, the IRS, eCFR,
    the Federal Register, PubMed, California's legislature and courts, and
    `docs.stripe.com` all report as unreachable when every one of them was
    perfectly reachable from a plain connection.
    """
    raw = (os.getenv("SCRAPER_DIRECT_FALLBACK") or "").strip().lower()
    return raw not in {"0", "false", "no", "off"}


def _configured_proxies() -> list[str]:
    proxies_str = os.getenv("DATACENTER_PROXIES")
    if not proxies_str:
        return []
    # Preserve occurrences, not only distinct URLs. Paid rotating gateways can
    # deliberately repeat one URL to request another provider-side peer.
    return [p.strip() for p in proxies_str.split(",") if p.strip()]


def _is_retryable_failure(response: Response) -> bool:
    if not response.failed:
        return False
    for reason_dict in response.failed_reasons:
        for reason in reason_dict:
            if reason in (
                FailureReason.REQUEST_ERROR,
                FailureReason.PROXY_ERROR,
                FailureReason.BAD_STATUS,
            ):
                return True
    return False


async def fetch_normally_with_proxy(
    url: str, use_random_proxy: bool = True, user_agent: str | None = None
) -> Response:
    """Fetch through the datacenter proxy pool, falling back to a DIRECT
    connection when the pool itself refuses to carry the request.

    🚨 A `proxy_error` is OUR infrastructure failing, not the site defending
    itself: `CONNECT tunnel failed, response 403` is the vendor's own edge
    declining the destination, which is why it hit five U.S. government
    domains, PubMed, `docs.stripe.com` and YouTube identically on 2026-09-17
    while those sites were perfectly reachable. Rotating to another proxy —
    the only thing this function used to do — cannot help when the whole
    vendor declines that destination class. The site never blocked us, so the
    honest recovery is the one the crawler has always done
    (`crawler._emit_proxy_bypass`): retry the page directly and say so.
    """
    from matrx_utils import capture_error, vcprint

    from matrx_scraper import proxy_health

    # Refused up front, so a refused address never touches the pool, its
    # health counters, or a direct fallback.
    try:
        await resolve_public_address(url, allow_http=True)
    except OutboundHostUnresolved:
        pass  # the proxy may resolve it; fetch() refuses it on any direct path
    except OutboundUrlRefused as exc:
        return address_refused_response(url, RequestType.NORMAL, str(exc))

    proxies = _configured_proxies()
    if not proxies:
        raise ProxyConfigurationError(
            "Proxy-backed fetch requested but DATACENTER_PROXIES is missing or empty"
        )

    # The pool refused this host minutes ago. Paying for every configured proxy
    # to refuse it again is latency for nothing — go direct first and only pay
    # the proxy path again once the refusal memory ages out.
    if direct_fallback_enabled() and proxy_health.pool_refuses(url):
        vcprint(
            f"[PROXY] Pool recently refused {redact_url_secrets(url)}; going direct first",
            color="yellow",
        )
        proxy_health.record_attempt(proxied=False)
        direct = await fetch(url, RequestType.NORMAL, None, user_agent=user_agent)
        direct.proxy_bypassed = True
        proxy_health.record_direct_fallback(rescued=not direct.failed)
        if not direct.failed:
            return direct
        # Direct did not work either — fall through and give the pool a chance
        # rather than reporting a failure we never re-tested properly.

    if use_random_proxy:
        proxy = random.choice(proxies)
    else:
        proxy = proxies[0]

    proxy_health.record_attempt(proxied=True)
    response = await fetch(url, RequestType.NORMAL, proxy, user_agent=user_agent)

    global _proxy_pool_exhausted

    if response.failed_primary_reason != FailureReason.PROXY_ERROR:
        _proxy_pool_exhausted = False
        proxy_health.record_proxy_carried()
        if not response.failed:
            proxy_health.record_proxy_success(url)

    if not _is_retryable_failure(response):
        return response

    first_reason = response.failed_primary_reason
    all_proxy_errors = first_reason == FailureReason.PROXY_ERROR

    # Try every remaining configured occurrence before declaring exhaustion.
    # Start at a random occurrence when requested, then randomize the rest so
    # concurrent requests do not stampede the same provider-side peer.
    remaining_proxies = list(proxies)
    remaining_proxies.remove(proxy)
    if use_random_proxy:
        random.shuffle(remaining_proxies)
    for alt_proxy in remaining_proxies:
        vcprint(
            f"[RETRY] Different proxy for: {redact_url_secrets(url)} (original failure: {first_reason})", color="cyan"
        )
        proxy_health.record_attempt(proxied=True)
        response = await fetch(url, RequestType.NORMAL, alt_proxy, user_agent=user_agent)
        all_proxy_errors = (
            all_proxy_errors and response.failed_primary_reason == FailureReason.PROXY_ERROR
        )
        if response.failed_primary_reason != FailureReason.PROXY_ERROR:
            _proxy_pool_exhausted = False
            proxy_health.record_proxy_carried()
        if not response.failed:
            vcprint(f"[RETRY] ALT PROXY WORKED: {redact_url_secrets(url)}", color="green")
            proxy_health.record_proxy_success(url)
            return response
        vcprint(
            f"[RETRY] Alt proxy also failed: {redact_url_secrets(url)} ({response.failed_primary_reason})",
            color="yellow",
        )

    vcprint(
        f"[RETRY] Proxy retries exhausted for: {redact_url_secrets(url)} ({response.failed_primary_reason})",
        color="yellow",
    )
    # Every proxy refused THIS request. That is pool exhaustion only when the
    # pool is carrying nothing at all; when it carried another host inside the
    # refusal window, the vendor is declining this one destination — a fact
    # `record_proxy_refusal` keeps per host on `/health/ready`, never a red
    # system_error. Decided BEFORE the direct attempt so a dead pool whose
    # pages are all rescued directly still reports itself (system_error
    # 586170ad, 2026-10-01: a healthy pool — 51/72 proxied successes — was
    # reported "exhausted" because one city site refused proxy AND direct).
    pool_exhausted = all_proxy_errors and not proxy_health.pool_carried_recently()
    direct_rescued: bool | None = None
    if all_proxy_errors and direct_fallback_enabled():
        # EVERY configured proxy refused to carry this request. That is our
        # vendor declining the destination, not the destination declining us —
        # so the page is very probably reachable on a direct connection, and
        # returning `proxy_error` without trying is us reporting our own
        # outage as the web's hostility. Remember the host so the next request
        # for it skips straight to direct.
        proxy_health.record_proxy_refusal(
            url, response.failed_primary_reason.value if response.failed_primary_reason else None
        )
        vcprint(
            f"[PROXY] Whole pool refused {redact_url_secrets(url)}; retrying DIRECT",
            color="yellow",
        )
        proxy_health.record_attempt(proxied=False)
        direct = await fetch(url, RequestType.NORMAL, None, user_agent=user_agent)
        direct.proxy_bypassed = True
        proxy_health.record_direct_fallback(rescued=not direct.failed)
        direct_rescued = not direct.failed
        if direct_rescued:
            vcprint(
                f"[PROXY] DIRECT RESCUED a proxy-refused URL: {redact_url_secrets(url)}",
                color="green",
            )
        # Return the DIRECT response either way: when it failed, its failure
        # is the site's own answer (status code and all), which is the true
        # one — `proxy_error` here would blame our vendor for a wall the site
        # put up.
        response = direct

    if pool_exhausted and not _proxy_pool_exhausted:
        # A pool outage affects every URL in flight. Capture its transition once,
        # then re-arm only after a proxy returns a non-proxy outcome.
        _proxy_pool_exhausted = True
        await capture_error(
            ProxyPoolExhaustedError("Configured proxy pool exhausted"),
            kind="scraper_proxy_pool_exhausted",
            context={
                "url": url,
                "failure_reason": response.failed_primary_reason.value
                if response.failed_primary_reason
                else None,
                "direct_rescued": direct_rescued,
                "proxy_pool": proxy_health.proxy_health_snapshot(),
            },
        )
    return response


def create_scraping_session(url: str) -> ScrapingSession:
    """
    Create a scraping session for a domain.
    Use this when you need to scrape multiple pages from the same site.

    Example:
        session = create_scraping_session("https://example.com")
        page1 = await session.fetch("https://example.com/page1")
        page2 = await session.fetch("https://example.com/page2")  # Will include Referer
    """
    domain = urlparse(url).netloc
    return ScrapingSession(domain=domain)


if __name__ == "__main__":
    import asyncio

    async def main():
        response = await fetch_normally_with_proxy("https://titaniumsuccess.com")
        print(json.dumps(response.to_dict(), indent=2))

    asyncio.run(main())
