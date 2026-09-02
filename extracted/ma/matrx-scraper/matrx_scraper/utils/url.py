from __future__ import annotations

import asyncio
import hashlib
import ipaddress
import os
import re
import socket
from functools import lru_cache
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import tldextract
from pydantic import BaseModel


class URLInfo(BaseModel):
    url: str
    website: str
    full_domain: str
    subdomain: str
    path: str
    domain_type: str
    unique_page_name: str
    extension: str | None = None
    path_segments: list[str] = []

    @classmethod
    def from_url(cls, raw_url: str) -> URLInfo:
        cleaned = _clean_url(raw_url)
        parsed = urlparse(cleaned)
        extracted = tldextract.extract(parsed.netloc)

        website = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
        full_domain = f"{extracted.subdomain}.{website}" if extracted.subdomain else website
        path = _construct_path(parsed)
        unique_page_name = re.sub(r"[^a-zA-Z0-9]", "_", full_domain + path)
        ext_raw = os.path.splitext(parsed.path)[1][1:]
        extension = ext_raw if ext_raw else None
        segments = [seg for seg in path.split("/") if seg.strip() and "?" not in seg]

        return cls(
            url=cleaned,
            website=website,
            full_domain=full_domain,
            subdomain=extracted.subdomain,
            path=path,
            domain_type=extracted.suffix,
            unique_page_name=unique_page_name,
            extension=extension,
            path_segments=segments,
        )


@lru_cache(maxsize=2000)
def get_url_info(url: str) -> URLInfo:
    return URLInfo.from_url(url)


def extract_domain(url: str) -> str:
    try:
        extracted = tldextract.extract(url)
        website = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
        return f"{extracted.subdomain}.{website}" if extracted.subdomain else website
    except Exception:
        parsed = urlparse(url)
        return parsed.netloc or url


def normalize_url(url: str) -> str:
    """THE canonical stored identity of an observed HTTP(S) URL.

    This is the ONE canonicalizer for the crawl system's stored identity: it feeds
    `url_hash` and is the key every ingestion source (crawl, sitemap, GSC, links)
    dedups on. Per the Identity Contract (common-docs/policies/durable-work-queue-
    standard.md) there must be exactly one such function — do not add a second.
    `url_match_key` (below) is a deliberately looser ALIAS matcher, not a rival
    identity; `url_utils.normalize_url` is INPUT ACCEPTANCE, not identity.

    Rules currently applied (each locked by a test in test_url_identity.py):
      - scheme + host lowercased; path case preserved (paths are case-sensitive)
      - fragment stripped
      - empty path -> "/"; trailing slash stripped except at root
      - params + query preserved verbatim

    Deliberately NOT yet applied (each would CHANGE the stored hash, so completing
    the Identity Contract spec is a migration-coupled decision — see the crawler
    handoff, not a silent edit): default-port removal (:80/:443), tracking-param
    removal (utm_*/gclid/fbclid), query-param ordering, percent-encoding
    normalization, per-site www policy.
    """

    parsed = urlparse(url.strip())
    scheme = (parsed.scheme or "https").lower()
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return urlunparse((scheme, netloc, path, parsed.params, parsed.query, ""))


def url_hash(url: str) -> str:
    """THE stored identity digest — ``sha256`` of :func:`normalize_url`.

    The `(site_id, url_hash)` unique arbiter on ``web.page`` is what stops every
    ingestion source (crawl, sitemap, GSC, GA4, Bing, manual, the CMS bridge)
    from minting a duplicate page. It lives here, beside the normalizer it
    depends on, so the digest cannot be computed from a second normalizer.
    ``web_crawl.persistence.url_hash`` and ``url_identity._url_hash`` are
    re-exports of this function; never re-implement it.
    """

    return hashlib.sha256(normalize_url(url).encode("utf-8")).hexdigest()


def page_route_key(url_or_path: str) -> str:
    """THE comparable ROUTE of a page — one rule, every repo, every caller.

    A route is the address a page is *planned* at (`plan.node.route`), *served*
    at (`client_pages.route`) and *measured* at (`web.page.path`). Those three
    live in two Supabase projects with no foreign key between them, so the route
    is the only thing they can be compared on — and until 2026-08-10 four
    different functions did that comparison with four different rule sets (one of
    them lower-cased the path, which the stored identity does not, so a page at
    `/About` matched a plan route `/about` and then hashed to a DIFFERENT
    `web.page` row). This is the one function.

    It is DERIVED from :func:`normalize_url` so it can never disagree with the
    stored identity. Accepts a full URL or a bare path; returns the path only:

      - leading ``/``; empty input -> ``/``
      - trailing ``/`` stripped except at the root
      - empty segments collapsed (``/a//b`` -> ``/a/b``, what the renderer serves)
      - scheme, host, port, params, query and fragment dropped — a route has none
      - **case preserved** (paths are case-sensitive, and so is the stored hash)

    Case-insensitive comparison is a deliberately separate, looser key —
    :func:`page_route_match_key` — exactly as :func:`url_match_key` is the looser
    twin of :func:`normalize_url`. Match on this key first; fall back to the
    looser one only when it names exactly one candidate.
    """

    raw = (url_or_path or "").strip()
    if not raw:
        return "/"
    if "://" not in raw:
        # A bare path (or a bare path with a query). Park it on a placeholder
        # origin so ONE normalizer sees it — never a second parse path here.
        raw = "https://route.invalid" + (raw if raw.startswith("/") else f"/{raw}")
    path = urlparse(normalize_url(raw)).path or "/"
    segments = [segment for segment in path.split("/") if segment]
    return "/" + "/".join(segments) if segments else "/"


def page_route_match_key(url_or_path: str) -> str:
    """Case-insensitive ALIAS key for a route — never the stored identity.

    The looser twin of :func:`page_route_key`, in the same relationship
    :func:`url_match_key` has to :func:`normalize_url`. Its ONLY sanctioned use
    is reconciling a route that failed an exact match, and only when it resolves
    to exactly one candidate; anything else silently merges two real pages.
    """

    return page_route_key(url_or_path).casefold()


def url_match_key(url: str) -> str:
    """Scheme/www-insensitive key used only to find likely URL aliases.

    The full normalized URL remains the stored identity. This key lets an
    HTTP GSC URL, an HTTPS sitemap URL, and a www crawl URL meet in the
    canonical matcher without erasing the distinct observed aliases.
    """

    parsed = urlparse(normalize_url(url))
    host = (parsed.hostname or "").lower().removeprefix("www.")
    port = parsed.port
    if port is not None and not (
        (parsed.scheme == "http" and port == 80) or (parsed.scheme == "https" and port == 443)
    ):
        host = f"{host}:{port}"
    return urlunparse(("", host, parsed.path or "/", parsed.params, parsed.query, ""))


def _clean_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
        parsed = urlparse(url)

    url = url.split("#")[0]
    parsed = urlparse(url)

    query_params = parse_qs(parsed.query)
    query_params = {k: v for k, v in query_params.items() if v and v[0]}
    query_string = urlencode(query_params, doseq=True)

    extracted = tldextract.extract(parsed.netloc)
    subdomain = extracted.subdomain
    domain = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
    netloc = f"{subdomain}.{domain}" if subdomain else domain

    path = parsed.path
    if path == "/":
        path = ""

    if query_string:
        return f"{parsed.scheme}://{netloc}{path}?{query_string}"
    return f"{parsed.scheme}://{netloc}{path}"


def _construct_path(parsed: object) -> str:
    path = parsed.path  # type: ignore[attr-defined]
    if path == "/":
        path = ""
    elif path.endswith("/"):
        path = path.rstrip("/")

    query_params = parse_qs(parsed.query)  # type: ignore[attr-defined]
    query_params = {k: v for k, v in query_params.items() if v and v[0]}
    query_string = urlencode(query_params, doseq=True)

    if query_string:
        path += f"?{query_string}"
    return path


def validate_and_correct_url(url: str) -> str:
    if not url:
        raise ValueError("URL cannot be empty")

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        if re.match(r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}", url):
            url = "https://" + url
        elif re.match(r"^www\.", url):
            url = "https://" + url

    parsed = urlparse(url)

    if not parsed.scheme:
        raise ValueError("URL scheme is missing and cannot be inferred")
    if not parsed.netloc:
        raise ValueError("URL domain is missing")
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"URL scheme must be http or https, got: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL domain is missing")

    if hostname == "localhost" or hostname.startswith("127."):
        raise ValueError(f"URL points to localhost: {url}")
    if hostname.endswith((".local", ".internal", ".intranet", ".corp")):
        raise ValueError(f"URL points to internal network: {url}")
    if hostname == "::1":
        raise ValueError(f"URL points to localhost IPv6: {url}")

    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        ip = None
    if ip is not None and not ip.is_global:
        raise ValueError(f"URL points to a non-public IP address: {url}")

    netloc_lower = parsed.netloc.lower()

    def _apply_google_docs_mobilebasic(p: object) -> object:
        path_parts = p.path.strip("/").split("/")  # type: ignore[attr-defined]
        if len(path_parts) >= 3 and path_parts[0] == "document" and path_parts[1] == "d":
            doc_id = path_parts[2]
            if not p.path.endswith("/mobilebasic"):  # type: ignore[attr-defined]
                return p._replace(path=f"/document/d/{doc_id}/mobilebasic", query="", fragment="")  # type: ignore[attr-defined]
        elif len(path_parts) >= 3 and path_parts[0] == "spreadsheets" and path_parts[1] == "d":
            doc_id = path_parts[2]
            if not p.path.endswith("/htmlview"):  # type: ignore[attr-defined]
                return p._replace(path=f"/spreadsheets/d/{doc_id}/htmlview", query="", fragment="")  # type: ignore[attr-defined]
        return p

    rules: dict[str, object] = {
        "docs.google.com": _apply_google_docs_mobilebasic,
    }

    if netloc_lower in rules:
        transformation_func = rules[netloc_lower]
        modified_parsed = transformation_func(parsed)  # type: ignore[operator]
        if modified_parsed != parsed:
            url = urlunparse(modified_parsed)

    return url


async def validate_public_http_url(url: str) -> str:
    """Validate scheme/host and fail closed when DNS resolves off the public internet.

    Direct site crawls are allowed only for publicly routable websites. The
    check runs immediately before crawler fetches, not only when a site row is
    created, so literal-IP and DNS-based SSRF targets are rejected.
    """

    corrected = validate_and_correct_url(url)
    parsed = urlparse(corrected)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL domain is missing")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        addresses = await asyncio.get_running_loop().getaddrinfo(
            hostname,
            port,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as exc:
        raise ValueError(f"URL host could not be resolved: {hostname}") from exc
    resolved = {entry[4][0] for entry in addresses if entry[4]}
    if not resolved:
        raise ValueError(f"URL host resolved to no addresses: {hostname}")
    for address in resolved:
        ip = ipaddress.ip_address(address)
        if not ip.is_global:
            raise ValueError(
                f"URL host resolves to a non-public IP address: {hostname} ({address})"
            )
    return corrected


def match_path(path: str, patterns: list[str]) -> str | None:
    normalized_path = path
    if path != "/" and path.endswith("/"):
        normalized_path = path[:-1]

    for pattern in patterns:
        normalized_pattern = pattern
        if pattern != "/" and pattern.endswith("/"):
            normalized_pattern = pattern[:-1]
        if normalized_path == normalized_pattern or path == pattern:
            return pattern

    matches: list[tuple[str, int]] = []

    for pattern in patterns:
        if "*" in pattern:
            pattern_parts = [p for p in pattern.split("/") if p]
            path_parts = [p for p in path.split("/") if p]

            non_wildcard_parts = [p for p in pattern_parts if p != "*"]
            if len(non_wildcard_parts) > len(path_parts):
                continue

            is_match = True
            specificity = 0
            pattern_idx = 0

            for path_part in path_parts:
                if pattern_idx >= len(pattern_parts):
                    if "*" not in pattern_parts:
                        is_match = False
                        break
                    continue

                pattern_part = pattern_parts[pattern_idx]
                if pattern_part == "*":
                    specificity += 1
                elif pattern_part != path_part:
                    is_match = False
                    break
                else:
                    specificity += 10

                pattern_idx += 1

            while pattern_idx < len(pattern_parts):
                if pattern_parts[pattern_idx] != "*":
                    is_match = False
                    break
                pattern_idx += 1

            if is_match:
                matches.append((pattern, specificity))

        elif pattern == "/*" and len(patterns) > 0:
            matches.append((pattern, 1))

    if matches:
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[0][0]

    if path == "/" and "/" in patterns:
        return "/"

    return None
