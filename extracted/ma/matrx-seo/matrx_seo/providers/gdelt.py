"""GDELT DOC 2.0 — the free, 15-minute news backbone for coverage discovery.

## Why GDELT and never NewsAPI

GDELT scans world news continuously and republishes an article INDEX (url,
title, domain, language, country, when GDELT first saw it) for free, in 100+
languages, refreshed every 15 minutes. NewsAPI's equivalent commercial tier is
$449/mo for a narrower index. The decision is D5 in the outreach decision log
and it is closed: **GDELT is the backbone, NewsAPI is never bought.**

## The license line this module must not cross

`common-docs/systems/marketing/outreach-data/FEATURE.md` rates GDELT as safe for
**ephemeral discovery, not copied article or contact data** — GDELT links to
stories it does not own. So this client returns an INDEX ENTRY and nothing
else: url, title, domain, language, country, seen-at. Article text, bylines and
publication dates come from OUR OWN crawl of the page, under our own robots
compliance. Never persist a GDELT-provided body; there isn't one to persist.

## No credential, no adapter, no budget

Every other provider here is paid, keyed and metered through
`SeoProviderAdapter` + `matrx_seo.budget`. GDELT is free and anonymous, so
wiring it into the credential/cost machinery would add a ceremony that meters
zero dollars and needs a key that does not exist. It gets a plain async client
with polite pacing instead — the simple version, per the prime rule.

## Pacing

GDELT publishes no rate limit and asks callers to be reasonable. One request
at a time, `MIN_INTERVAL_SECONDS` apart, process-wide. A tracker pass issues a
handful of queries; there is no burst to optimize.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from time import monotonic
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, Field

GDELT_DOC_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

#: GDELT's own hard ceiling for ArtList mode.
MAX_RECORDS = 250

#: Polite, process-wide spacing. GDELT's own 429 body states the rule in words:
#: *"Please limit requests to one every 5 seconds."* Measured live 2026-08-16 —
#: pacing at exactly 5.0s still drew a 429, because the clock GDELT measures is
#: not ours. So we pace at 6.5s and treat a 429 as a PACING concern, never a
#: user-facing error (the same doctrine the Brave provider here lives under).
#: pacing at exactly 5.0s still drew a 429, and 6.5s still drew one during a
#: burst — GDELT's counter is per-IP and unforgiving. 8s costs a tracker with
#: three queries under half a minute, on a task that runs every thirty.
MIN_INTERVAL_SECONDS = 8.0

#: A 429 means "you were early", so the answer is to wait and ask again — twice,
#: then give up loudly. Never silently: a swallowed 429 would report "no
#: coverage" for a query that was never actually run.
RATE_LIMIT_RETRIES = 2
RATE_LIMIT_BACKOFF_SECONDS = 20.0

#: Once RATE_LIMIT_RETRIES is exhausted and GDELT is STILL answering 429, this
#: server is inside GDELT's own penalty window, not merely early. Measured
#: 2026-08-16 and again 2026-09-27: the penalty outlives any per-request
#: backoff and holds for several minutes even after pacing resumes. Querying
#: again during that window is itself the abuse GDELT punishes, so every
#: query — this one and every other tracker's, this run and the next — is
#: refused locally (no HTTP call at all) until the window clears. Process-wide,
#: same as the pacing clock: aidream has no shared cross-process store for this
#: today, and a caller inside one process re-poking GDELT while its sibling
#: process is also in the penalty is exactly the "unforgiving per-IP counter"
#: failure this exists to stop; add a shared store here if one is ever wired in.
PENALTY_WINDOW_SECONDS = 300.0

REQUEST_TIMEOUT_SECONDS = 45.0

USER_AGENT = "MatrxCoverageBot/0.1 (+https://aimatrx.com)"

_pace_lock = asyncio.Lock()
_last_request_at: float | None = None
#: `monotonic()` timestamp until which every query is refused locally. `None`
#: outside a penalty.
_penalty_until: float | None = None


def reset_pacing_state_for_tests() -> None:
    """Test-only: clear process-wide pacing/penalty state between test cases.

    The pacing clock and the penalty window are deliberately process-global
    (see `PENALTY_WINDOW_SECONDS`), which means they also leak between test
    functions in the same process unless cleared.
    """
    global _last_request_at, _penalty_until
    _last_request_at = None
    _penalty_until = None


class GdeltUnavailable(RuntimeError):
    """GDELT could not answer. A monitoring pass records this; it never guesses.

    Loudness matters more here than anywhere else in the module: a coverage
    tracker that silently reports "no coverage" because the free index was down
    is indistinguishable from a quiet news week, forever.
    """


class GdeltArticle(BaseModel):
    """One index entry. Deliberately has no body, author or publish date."""

    model_config = ConfigDict(extra="forbid")

    url: str
    title: str = ""
    domain: str = ""
    language: str = ""
    source_country: str = ""
    #: When GDELT first saw the article. NOT the publication date — our crawl
    #: reads that from the page itself.
    seen_at: datetime | None = None
    social_image: str = ""


class GdeltQueryResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    articles: list[GdeltArticle] = Field(default_factory=list)
    #: True when GDELT answered and simply had nothing. An EMPTY ANSWER IS AN
    #: ANSWER; an unavailable service is not, and raises instead.
    answered: bool = True


def build_query(
    *,
    terms: list[str],
    exclude_terms: list[str] | None = None,
    domains: list[str] | None = None,
    language: str | None = None,
    country: str | None = None,
) -> str:
    """Compose one GDELT DOC query from a tracker's saved search.

    Multi-word terms are quoted (GDELT treats an unquoted phrase as an AND of
    its words, which silently widens a brand search into noise).
    """
    if not terms:
        raise ValueError("a GDELT query needs at least one term")

    def literal(value: str) -> str:
        cleaned = value.strip().replace('"', "")
        if not cleaned:
            raise ValueError("a GDELT term cannot be blank")
        return f'"{cleaned}"' if " " in cleaned else cleaned

    positives = [literal(term) for term in terms if term.strip()]
    if not positives:
        raise ValueError("a GDELT query needs at least one non-blank term")
    parts = [f"({' OR '.join(positives)})"] if len(positives) > 1 else [positives[0]]

    if domains:
        scoped = [f"domain:{d.strip().lower()}" for d in domains if d.strip()]
        if scoped:
            parts.append(f"({' OR '.join(scoped)})" if len(scoped) > 1 else scoped[0])
    if language:
        parts.append(f"sourcelang:{language.strip().lower()}")
    if country:
        parts.append(f"sourcecountry:{country.strip().lower()}")
    for term in exclude_terms or []:
        if term.strip():
            parts.append(f"-{literal(term)}")
    return " ".join(parts)


def _parse_seen_at(raw: Any) -> datetime | None:
    # GDELT stamps "20260816T031500Z"; older payloads use "20260816031500".
    if not isinstance(raw, str) or not raw:
        return None
    text = raw.strip().replace("T", "").replace("Z", "")
    if len(text) != 14 or not text.isdigit():
        return None
    try:
        return datetime.strptime(text, "%Y%m%d%H%M%S").replace(tzinfo=UTC)
    except ValueError:
        return None


def parse_articles(payload: Any) -> list[GdeltArticle]:
    """Normalize a DOC ArtList payload. Unknown keys are ignored, never raised on."""
    if not isinstance(payload, dict):
        return []
    raw_articles = payload.get("articles")
    if not isinstance(raw_articles, list):
        return []
    articles: list[GdeltArticle] = []
    for entry in raw_articles:
        if not isinstance(entry, dict):
            continue
        url = str(entry.get("url") or "").strip()
        if not url:
            continue
        articles.append(
            GdeltArticle(
                url=url,
                title=str(entry.get("title") or "").strip(),
                domain=str(entry.get("domain") or "").strip().lower(),
                language=str(entry.get("language") or "").strip(),
                source_country=str(entry.get("sourcecountry") or "").strip(),
                seen_at=_parse_seen_at(entry.get("seendate")),
                social_image=str(entry.get("socialimage") or "").strip(),
            )
        )
    return articles


async def _pace() -> None:
    global _last_request_at
    async with _pace_lock:
        now = monotonic()
        if _last_request_at is not None:
            wait = MIN_INTERVAL_SECONDS - (now - _last_request_at)
            if wait > 0:
                await asyncio.sleep(wait)
        _last_request_at = monotonic()


async def search_articles(
    query: str,
    *,
    timespan: str = "1d",
    max_records: int = 100,
    client: httpx.AsyncClient | None = None,
) -> GdeltQueryResult:
    """Run ONE DOC query. Raises `GdeltUnavailable` rather than reporting silence.

    `timespan` uses GDELT's own vocabulary (`15min`, `1h`, `1d`, `7d`).
    """
    if not query.strip():
        raise ValueError("a GDELT query cannot be blank")
    global _penalty_until
    now = monotonic()
    if _penalty_until is not None and now < _penalty_until:
        remaining = _penalty_until - now
        raise GdeltUnavailable(
            f"GDELT is still inside its post-429 penalty window ({remaining:.0f}s "
            f"left) and did not run {query!r}. Querying again now would only "
            f"extend the penalty; the next scheduled pass retries once it clears. "
            f"Nothing is wrong with the query or the tracker."
        )
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": str(max(1, min(MAX_RECORDS, max_records))),
        "timespan": timespan,
        "sort": "DateDesc",
    }
    owns_client = client is None
    http = client or httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS)
    try:
        for attempt in range(RATE_LIMIT_RETRIES + 1):
            await _pace()
            try:
                response = await http.get(
                    GDELT_DOC_URL, params=params, headers={"User-Agent": USER_AGENT}
                )
            except httpx.HTTPError as exc:
                raise GdeltUnavailable(f"GDELT request failed: {exc}") from exc
            if response.status_code != 429 or attempt == RATE_LIMIT_RETRIES:
                break
            await asyncio.sleep(RATE_LIMIT_BACKOFF_SECONDS * (attempt + 1))
    finally:
        if owns_client:
            await http.aclose()

    if response.status_code == 429:
        # Measured 2026-08-16: GDELT does not merely throttle the next request,
        # it puts a caller that has been impolite into a penalty window that
        # outlives any per-request backoff. Say that plainly — an operator
        # reading "HTTP 429" will otherwise go looking for a bug in the query.
        # Open the local circuit breaker so nothing — this provider, this run,
        # the next scheduled run — pokes GDELT again until the window clears.
        _penalty_until = monotonic() + PENALTY_WINDOW_SECONDS
        raise GdeltUnavailable(
            f"GDELT is rate-limiting this server (HTTP 429) and did not run "
            f"{query!r}. It asks for one request every 5 seconds; after repeated "
            f"bursts it keeps refusing for several minutes even when pacing "
            f"resumes. Nothing is wrong with the query or the tracker — the next "
            f"scheduled pass picks it up. Provider text: {response.text[:200]}"
        )
    if response.status_code != 200:
        raise GdeltUnavailable(
            f"GDELT answered HTTP {response.status_code} for query {query!r}: {response.text[:300]}"
        )
    body = response.text.strip()
    if not body:
        # GDELT returns an empty body for a query it understood and matched
        # nothing on. That is an answer.
        return GdeltQueryResult(query=query, articles=[], answered=True)
    try:
        payload = response.json()
    except ValueError as exc:
        # GDELT reports malformed queries as plain text, HTTP 200. Never let a
        # rejected query masquerade as "no coverage".
        raise GdeltUnavailable(f"GDELT rejected query {query!r}: {body[:300]}") from exc
    return GdeltQueryResult(query=query, articles=parse_articles(payload), answered=True)


__all__ = [
    "GDELT_DOC_URL",
    "MAX_RECORDS",
    "MIN_INTERVAL_SECONDS",
    "PENALTY_WINDOW_SECONDS",
    "RATE_LIMIT_BACKOFF_SECONDS",
    "RATE_LIMIT_RETRIES",
    "GdeltArticle",
    "GdeltQueryResult",
    "GdeltUnavailable",
    "build_query",
    "parse_articles",
    "reset_pacing_state_for_tests",
    "search_articles",
]
