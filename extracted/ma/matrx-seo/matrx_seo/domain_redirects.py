"""Measured public-origin redirects. Unavailable evidence never becomes a pass."""

from __future__ import annotations

import asyncio
import hashlib
import re
from typing import Literal
from urllib.parse import urljoin, urlsplit

import httpx
from bs4 import BeautifulSoup
from matrx_scraper.utils.url import public_http_client
from pydantic import BaseModel, Field

from .owned_domains import normalize_domain


class RedirectSettings(BaseModel):
    timeout_seconds: float
    max_bytes: int
    max_hops: int
    concurrency: int
    similarity_threshold: float
    minimum_content_words: int


class RedirectHop(BaseModel):
    url: str
    status: int
    location: str | None = None


class VariantResult(BaseModel):
    url: str
    outcome: Literal["pass", "fail", "error"]
    reason: str
    hops: list[RedirectHop] = Field(default_factory=list)
    duplicate: bool | None = None
    similarity: float | None = None
    content_hash: str | None = None
    content_complete: bool = True


class RedirectReport(BaseModel):
    canonical: str
    observed_at: str
    status: Literal["pass", "fail", "error", "n_a"]
    variants: list[VariantResult]
    canonical_hash: str | None
    algorithm: str = "visible-word-shingle-jaccard/v1"
    threshold: float


def origin(url: str) -> str:
    parts = urlsplit(url)
    if (
        parts.scheme not in {"http", "https"}
        or not parts.hostname
        or parts.username
        or parts.password
    ):
        raise ValueError("Canonical address must be a public HTTP or HTTPS URL.")
    host = normalize_domain(parts.hostname)
    port = parts.port
    suffix = f":{port}" if port and port != (443 if parts.scheme == "https" else 80) else ""
    return f"{parts.scheme}://{host}{suffix}"


def content_words(html: bytes) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    for node in soup(["script", "style", "noscript", "svg"]):
        node.decompose()
    return re.findall(r"\w+", soup.get_text(" ", strip=True).casefold())


def shingles(words: list[str]) -> set[str]:
    return {" ".join(words[i : i + 5]) for i in range(max(0, len(words) - 4))}


async def check_redirects(
    canonical_url: str,
    domains: list[str],
    *,
    observed_at: str,
    settings: RedirectSettings,
    http: httpx.AsyncClient | None = None,
    external_candidates: list[str] | None = None,
) -> RedirectReport:
    canonical = origin(canonical_url)
    semaphore = asyncio.Semaphore(settings.concurrency)
    client = http or public_http_client(timeout=settings.timeout_seconds, follow_redirects=False)

    async def capture(url: str) -> tuple[VariantResult, list[str]]:
        hops: list[RedirectHop] = []
        seen: set[str] = set()
        current = url
        permanent = True
        async with semaphore:
            try:
                async with asyncio.timeout(settings.timeout_seconds):
                    for _ in range(settings.max_hops + 1):
                        if current in seen:
                            return VariantResult(
                                url=url, outcome="fail", reason="Redirect loop", hops=hops
                            ), []
                        seen.add(current)
                        # public_http_client revalidates and pins every hop's public IP.
                        async with client.stream(
                            "GET", current, headers={"Accept": "text/html"}
                        ) as response:
                            location = response.headers.get("location")
                            hops.append(
                                RedirectHop(
                                    url=current, status=response.status_code, location=location
                                )
                            )
                            if response.status_code in {301, 302, 303, 307, 308} and location:
                                permanent = permanent and response.status_code in {301, 308}
                                current = urljoin(current, location)
                                continue
                            if response.status_code != 200:
                                # Refusals/challenges and server failures are not content evidence.
                                unknown = (
                                    response.status_code in {401, 403, 429}
                                    or response.status_code >= 500
                                )
                                return VariantResult(
                                    url=url,
                                    outcome="error" if unknown else "fail",
                                    reason=f"Terminal HTTP {response.status_code}",
                                    hops=hops,
                                ), []
                            payload = bytearray()
                            complete = True
                            async for chunk in response.aiter_bytes():
                                room = settings.max_bytes - len(payload)
                                payload.extend(chunk[:room])
                                if len(chunk) > room:
                                    complete = False
                                    break
                            is_html = "html" in response.headers.get("content-type", "").lower()
                            words = content_words(bytes(payload)) if is_html else []
                            if any(
                                phrase in " ".join(words)
                                for phrase in (
                                    "checking your browser",
                                    "verify you are human",
                                    "just a moment",
                                )
                            ):
                                return VariantResult(
                                    url=url, outcome="error", reason="Browser challenge", hops=hops
                                ), []
                            passed = (
                                origin(current) == canonical
                                and permanent
                                and (origin(url) == canonical or len(hops) > 1)
                            )
                            return VariantResult(
                                url=url,
                                outcome="pass" if passed else "fail",
                                reason="Permanent redirect to canonical origin"
                                if passed
                                else (
                                    "Temporary redirect"
                                    if not permanent
                                    else "Serves outside canonical origin"
                                ),
                                hops=hops,
                                content_complete=complete,
                                content_hash=hashlib.sha256(" ".join(words).encode()).hexdigest()
                                if words
                                else None,
                            ), words
                    return VariantResult(
                        url=url, outcome="fail", reason="Redirect hop limit reached", hops=hops
                    ), []
            except (httpx.HTTPError, ValueError, TimeoutError) as exc:
                return VariantResult(
                    url=url,
                    outcome="error",
                    reason=f"Capture unavailable: {type(exc).__name__}",
                    hops=hops,
                ), []

    try:
        baseline, baseline_words = await capture(canonical + "/")
        urls = set()
        owned_hosts = {normalize_domain(domain).removeprefix("www.") for domain in domains}
        external_hosts = {
            normalize_domain(domain).removeprefix("www.") for domain in external_candidates or []
        } - owned_hosts
        for domain in sorted(owned_hosts | external_hosts):
            host = normalize_domain(domain)
            apex = host.removeprefix("www.")
            for variant in {apex, "www." + apex}:
                for scheme in ("http", "https"):
                    url = f"{scheme}://{variant}/"
                    if origin(url) != canonical:
                        urls.add(url)
        captures = await asyncio.gather(*(capture(url) for url in sorted(urls)))
        variants = [result for result, _ in captures]
        baseline_valid = (
            baseline.outcome == "pass"
            and baseline.content_complete
            and len(baseline_words) >= settings.minimum_content_words
        )
        base = shingles(baseline_words)
        for result, words in captures:
            if result.outcome == "fail" and result.hops and result.hops[-1].status == 200:
                if (
                    baseline_valid
                    and result.content_complete
                    and len(words) >= settings.minimum_content_words
                ):
                    current = shingles(words)
                    result.similarity = (
                        len(base & current) / len(base | current) if base | current else None
                    )
                    result.duplicate = (
                        result.similarity is not None
                        and result.similarity >= settings.similarity_threshold
                    )
            external = (urlsplit(result.url).hostname or "").removeprefix("www.") in external_hosts
            if external and result.outcome == "fail" and result.duplicate is not True:
                # A branded-search host is a candidate, not owned-domain proof.
                # An unrelated result has no obligation to redirect to this site.
                known_absent = bool(result.hops and result.hops[-1].status in {404, 410})
                result.outcome = "pass" if result.duplicate is False or known_absent else "error"
                result.reason = (
                    "No duplicate content observed"
                    if result.outcome == "pass"
                    else "Duplicate comparison unavailable"
                )
        status = (
            "fail"
            if any(v.outcome == "fail" for v in variants)
            else "error"
            if baseline.outcome != "pass" or any(v.outcome == "error" for v in variants)
            else "pass"
            if variants
            else "n_a"
        )
        return RedirectReport(
            canonical=canonical,
            observed_at=observed_at,
            status=status,
            variants=variants,
            canonical_hash=baseline.content_hash,
            threshold=settings.similarity_threshold,
        )
    finally:
        if http is None:
            await client.aclose()
