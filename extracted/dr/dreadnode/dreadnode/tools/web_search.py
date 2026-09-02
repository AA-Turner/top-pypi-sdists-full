"""Web search tool with pluggable backend adapters.

The agent-facing surface (:func:`web_search` and :class:`WebSearchResponse`)
is stable. Backend selection is internal — the runtime picks the provider
from env config and the auto fallback chain; the agent does not choose.
New providers plug in by registering a :class:`Backend` in :data:`_BACKENDS`.
"""

import asyncio
import os
import typing as t
from dataclasses import dataclass, field
from urllib.parse import parse_qs, urlparse

import httpx
from loguru import logger

from dreadnode.agents.tools import tool

# ---------------------------------------------------------------------------
# Public response shape
# ---------------------------------------------------------------------------


class WebSearchResult(t.TypedDict):
    title: str
    url: str
    snippet: str
    rank: int
    domain: str


class WebSearchFilters(t.TypedDict):
    allowed_domains: list[str]
    blocked_domains: list[str]


class WebSearchResponse(t.TypedDict):
    success: bool
    query: str
    backend: str
    result_count: int
    applied_filters: WebSearchFilters
    warnings: list[str]
    results: list[WebSearchResult]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_RESULTS = 10
DEFAULT_HTTP_TIMEOUT = 30.0

_BACKEND_ENV_VAR = "DREADNODE_WEB_SEARCH_BACKEND"

# Set by the platform when the deployment has no public egress. Mirrors
# ``DREADNODE_CAPABILITY_INSTALL`` (WP1-59): a directive about one behaviour,
# not a description of the deployment. The SDK also runs on laptops, in CI
# and inside a customer's own process, and none of those should be reasoning
# about our deployment posture — only a sandbox is ever told this.
#
# Distinct from ``_BACKEND_ENV_VAR``, which picks *which* backend answers.
# This one decides whether a backend that reaches a public host may answer
# at all.
_SEARCH_MODE_ENV = "DREADNODE_WEB_SEARCH_MODE"

# Surfaced when sealed mode leaves no backend able to answer. "No results"
# and "there is no search here" are different facts, and a task authored
# against a connected deployment has to be able to tell them apart
# (WP1-72) rather than reading a silent empty set as a real one.
SEALED_WARNING = (
    "Web search is unavailable: this deployment has no public egress, and no "
    "internal search backend is configured."
)

# Auto-mode picks the first configured backend in this order. DuckDuckGo
# is last because it needs no credentials and so reports as configured on
# any runtime that is not sealed, so stronger providers win when their
# keys are present. ``platform`` leads
# the chain when an authenticated dreadnode profile is present
# (WS-SDK-002); a 5xx from the hosted endpoint advances to the next.
_AUTO_PREFERENCE_ORDER: tuple[str, ...] = (
    "platform",
    "firecrawl",
    "exa",
    "google",
    "duckduckgo",
)

_FIRECRAWL_DEFAULT_API_URL = "https://api.firecrawl.dev"

# Surfaced verbatim in `warnings` when a backend succeeds with zero hits.
# `_summarize_web_search` (TUI) keys off this to distinguish "genuinely empty"
# from "all results filtered out by domain rules".
NO_RESULTS_WARNING = "No results for this query."


# ---------------------------------------------------------------------------
# Backend plumbing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BackendOutcome:
    """What a backend returns to the resolver.

    ``hits`` is the unranked list of ``{title, url, snippet}`` dicts.
    Rank and domain are added later by :func:`_rank_results`. A non-empty
    ``error`` means the backend itself failed — callers surface it via
    ``warnings`` and flip ``success=False`` on the final response.

    ``should_fall_through`` opts the failure into the auto-chain cascade
    (WS-SDK-004): a transient/upstream failure where the next backend in
    ``_AUTO_PREFERENCE_ORDER`` should be tried. Default is False so
    existing backends — which surface a single attempt — keep their
    behaviour. The hosted ``platform`` backend sets this for 5xx and
    transport errors; 4xx (auth/credits) keep it False so the call
    surfaces to the caller per WS-SDK-005.
    """

    hits: list[dict[str, str]]
    warnings: list[str] = field(default_factory=list)
    error: str | None = None
    should_fall_through: bool = False


BackendSearchFn = t.Callable[[str, int], t.Awaitable[BackendOutcome]]


@dataclass(frozen=True)
class Backend:
    name: str
    search: BackendSearchFn
    is_configured: t.Callable[[], bool]


# ---------------------------------------------------------------------------
# Backend adapters
# ---------------------------------------------------------------------------


async def _duckduckgo_backend(query: str, num_results: int) -> BackendOutcome:
    """DuckDuckGo search. No credentials required.

    Falls through to the HTML lite scraper when ``ddgs`` is missing OR when
    it returns zero hits — a broken client returning silent empties is
    indistinguishable from a real zero-hit response at this layer, and the
    lite endpoint is more durable than any wrapper library.
    """
    try:
        from ddgs import DDGS
    except ImportError:
        return await _duckduckgo_lite_backend(query, num_results)

    def _run() -> list[dict[str, t.Any]]:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=num_results))

    try:
        results = await asyncio.to_thread(_run)
    except Exception as exc:
        return BackendOutcome(hits=[], error=f"DuckDuckGo search failed: {exc}")

    if not results:
        return await _duckduckgo_lite_backend(query, num_results)

    return BackendOutcome(
        hits=[
            {
                "title": str(item.get("title") or "No title"),
                "url": _unwrap_ddg_redirect(str(item.get("href") or item.get("link") or "")),
                "snippet": str(item.get("body") or item.get("snippet") or ""),
            }
            for item in results
        ]
    )


async def _duckduckgo_lite_backend(query: str, num_results: int) -> BackendOutcome:
    """HTML-scrape fallback for DuckDuckGo when the Python client is absent."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return BackendOutcome(
            hits=[],
            error="DuckDuckGo lite scraper is unavailable: install 'beautifulsoup4'.",
        )

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_HTTP_TIMEOUT) as client:
            response = await client.get(
                "https://lite.duckduckgo.com/lite/",
                params={"q": query},
                headers={"User-Agent": "Mozilla/5.0"},
            )
            response.raise_for_status()
    except Exception as exc:
        return BackendOutcome(hits=[], error=f"DuckDuckGo search failed: {exc}")

    soup = BeautifulSoup(response.text, "html.parser")
    hits: list[dict[str, str]] = []
    for link in soup.select("a.result-link")[:num_results]:
        snippet_elem = link.find_next("td", class_="result-snippet")
        hits.append(
            {
                "title": link.get_text(strip=True),
                "url": _unwrap_ddg_redirect(str(link.get("href") or "")),
                "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
            }
        )
    return BackendOutcome(hits=hits)


def _unwrap_ddg_redirect(url: str) -> str:
    """Return the real target hidden inside a DuckDuckGo ``/l/?uddg=...`` link.

    DDG's lite interface wraps outbound results in a redirect and the href
    arrives as ``//duckduckgo.com/l/?uddg=<encoded-target>`` (sometimes
    ``https:``-prefixed or path-only). Feeding that into ``fetch`` /
    ``web_extract`` would just hit the redirector. Non-redirect URLs pass
    through unchanged.
    """
    if not url:
        return url
    candidate = url
    if candidate.startswith("//"):
        candidate = "https:" + candidate
    elif candidate.startswith("/"):
        candidate = "https://duckduckgo.com" + candidate

    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower()
    if not (host == "duckduckgo.com" or host.endswith(".duckduckgo.com")):
        return url
    if not parsed.path.startswith("/l/"):
        return url

    target = parse_qs(parsed.query).get("uddg")
    if not target or not target[0]:
        return url
    return target[0]


async def _google_backend(query: str, num_results: int) -> BackendOutcome:
    """Google Custom Search API. Requires GOOGLE_API_KEY + GOOGLE_CSE_ID."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    cse_id = os.environ.get("GOOGLE_CSE_ID")
    if not api_key or not cse_id:
        return BackendOutcome(hits=[], error="Google search is not configured.")

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_HTTP_TIMEOUT) as client:
            response = await client.get(
                "https://www.googleapis.com/customsearch/v1",
                params={
                    "key": api_key,
                    "cx": cse_id,
                    "q": query,
                    "num": num_results,
                },
            )
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        return BackendOutcome(hits=[], error=f"Google search failed: {exc}")

    items = data.get("items") or []
    return BackendOutcome(
        hits=[
            {
                "title": str(item.get("title") or "No title"),
                "url": str(item.get("link") or ""),
                "snippet": str(item.get("snippet") or ""),
            }
            for item in items
        ]
    )


async def _exa_backend(query: str, num_results: int) -> BackendOutcome:
    """Exa neural search. Requires EXA_API_KEY.

    Exa returns a richer record than we expose — we keep the common shape
    so downstream consumers don't fork on provider. See
    https://docs.exa.ai/reference/search.
    """
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        return BackendOutcome(hits=[], error="Exa search is not configured.")

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_HTTP_TIMEOUT) as client:
            response = await client.post(
                "https://api.exa.ai/search",
                headers={"x-api-key": api_key, "content-type": "application/json"},
                json={
                    "query": query,
                    "numResults": num_results,
                    "type": "auto",
                    "contents": {"highlights": {"numSentences": 2}},
                },
            )
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        return BackendOutcome(hits=[], error=f"Exa search failed: {exc}")

    items = data.get("results") or []
    return BackendOutcome(
        hits=[
            {
                "title": str(item.get("title") or "No title"),
                "url": str(item.get("url") or ""),
                "snippet": _exa_snippet(item),
            }
            for item in items
        ]
    )


def _exa_snippet(item: dict[str, t.Any]) -> str:
    """Pick the best short snippet Exa gave us."""
    highlights = item.get("highlights")
    if isinstance(highlights, list):
        for candidate in highlights:
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
    for key in ("summary", "text"):
        candidate = item.get(key)
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()[:400]
    return ""


async def _platform_backend(query: str, num_results: int) -> BackendOutcome:
    """Hosted Brave-backed search via ``POST /org/{org}/tools/search``.

    Auth/server/org are read off the configured ``Dreadnode`` singleton so
    env vars, CLI args, and on-disk profiles all flow through the same
    resolution path. ``ApiClient`` is sync — offload to a thread to keep
    this coroutine non-blocking, mirroring how ``profile_manager`` calls
    sync API methods.

    5xx (incl. 503 from a deployment without a Brave key) returns a
    fall-through-eligible outcome; 4xx (auth/credits) is fatal so the
    error surfaces to the caller (WS-SDK-004 / WS-SDK-005).
    """
    from dreadnode import get_default_instance
    from dreadnode.app.api.client import (
        AuthenticationError as ApiAuthError,
    )
    from dreadnode.app.api.client import (
        PlatformBackendUnavailableError,
    )
    from dreadnode.core.exceptions import InsufficientCreditsError

    instance = get_default_instance()
    try:
        api = instance.api  # raises if unconfigured
    except RuntimeError as exc:
        return BackendOutcome(
            hits=[],
            error=f"Platform search unavailable: {exc}",
            should_fall_through=True,
        )

    try:
        response = await asyncio.to_thread(
            api.search_web,
            query=query,
            num_results=num_results,
            org=str(instance.organization),
        )
    except PlatformBackendUnavailableError as exc:
        return BackendOutcome(
            hits=[],
            error=f"Platform search unavailable: {exc}",
            should_fall_through=True,
        )
    except (ApiAuthError, InsufficientCreditsError) as exc:
        return BackendOutcome(
            hits=[],
            error=f"Platform search rejected: {exc}",
        )
    except RuntimeError as exc:
        return BackendOutcome(
            hits=[],
            error=f"Platform search failed: {exc}",
        )

    return BackendOutcome(
        hits=[{"title": r.title, "url": r.url, "snippet": r.snippet} for r in response.results]
    )


def _platform_is_configured() -> bool:
    """True iff the Dreadnode singleton has server + api_key + organization."""
    try:
        from dreadnode import get_default_instance

        instance = get_default_instance()
        return bool(
            instance._initialized and instance.server and instance.api_key and instance.organization
        )
    except Exception:
        return False


async def _firecrawl_backend(query: str, num_results: int) -> BackendOutcome:
    """Firecrawl search. Requires FIRECRAWL_API_KEY.

    ``FIRECRAWL_API_URL`` overrides the base URL (for self-hosted Firecrawl
    or a managed gateway). See https://docs.firecrawl.dev/api-reference/v2-search.
    """
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        return BackendOutcome(hits=[], error="Firecrawl search is not configured.")

    base_url = (os.environ.get("FIRECRAWL_API_URL") or _FIRECRAWL_DEFAULT_API_URL).rstrip("/")

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_HTTP_TIMEOUT) as client:
            response = await client.post(
                f"{base_url}/v2/search",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={"query": query, "limit": num_results},
            )
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        return BackendOutcome(hits=[], error=f"Firecrawl search failed: {exc}")

    items = _firecrawl_extract_items(data)
    return BackendOutcome(
        hits=[
            {
                "title": str(item.get("title") or "No title"),
                "url": str(item.get("url") or ""),
                "snippet": str(
                    item.get("description") or item.get("snippet") or item.get("content") or ""
                ),
            }
            for item in items
        ]
    )


def _firecrawl_extract_items(payload: t.Any) -> list[dict[str, t.Any]]:
    """Firecrawl has shipped several response shapes; coerce them to one list.

    Observed shapes: ``{"data": [...]}``, ``{"data": {"web": [...]}}``,
    ``{"data": {"results": [...]}}``, or the top-level variants without the
    ``data`` wrapper.
    """
    if not isinstance(payload, dict):
        return []

    data = payload.get("data")
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("web", "results"):
            items = data.get(key)
            if isinstance(items, list):
                return [item for item in items if isinstance(item, dict)]

    for key in ("web", "results"):
        items = payload.get(key)
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
    return []


# ---------------------------------------------------------------------------
# Registry + resolver
# ---------------------------------------------------------------------------


def _sealed() -> bool:
    """Whether this runtime must answer searches without reaching a network."""
    return os.environ.get(_SEARCH_MODE_ENV, "").strip().lower() == "sealed"


async def _sealed_backend(_query: str, _num_results: int) -> BackendOutcome:
    """Terminal backend for a sealed runtime with nothing configured.

    Opens no socket. It exists so the resolver has somewhere to land other
    than DuckDuckGo, and so the response names ``sealed`` as the backend
    instead of reporting a public one that was never actually consulted.
    ``should_fall_through`` stays False — there is nothing to fall through
    to, and the cascade must not resume walking the chain.
    """
    return BackendOutcome(hits=[], error=SEALED_WARNING)


_BACKENDS: dict[str, Backend] = {
    "duckduckgo": Backend(
        name="duckduckgo",
        search=_duckduckgo_backend,
        # The only backend needing no credentials, so it is the only one a
        # sealed runtime can reach by accident. Reporting it unconfigured
        # gates the auto chain, the fall-through cascade and the
        # ``DREADNODE_WEB_SEARCH_BACKEND`` pin in one place (WP1-72).
        is_configured=lambda: not _sealed(),
    ),
    "google": Backend(
        name="google",
        search=_google_backend,
        is_configured=lambda: bool(
            os.environ.get("GOOGLE_API_KEY") and os.environ.get("GOOGLE_CSE_ID")
        ),
    ),
    "exa": Backend(
        name="exa",
        search=_exa_backend,
        is_configured=lambda: bool(os.environ.get("EXA_API_KEY")),
    ),
    "firecrawl": Backend(
        name="firecrawl",
        search=_firecrawl_backend,
        is_configured=lambda: bool(os.environ.get("FIRECRAWL_API_KEY")),
    ),
    "platform": Backend(
        name="platform",
        search=_platform_backend,
        is_configured=_platform_is_configured,
    ),
}

# Deliberately outside ``_BACKENDS`` and ``_AUTO_PREFERENCE_ORDER``: it must
# not be selectable by name, by the auto chain, or by the cascade. The
# resolver returns it directly as the terminal case.
_SEALED_BACKEND = Backend(
    name="sealed",
    search=_sealed_backend,
    is_configured=lambda: True,
)


def _next_in_auto_chain(after: str) -> Backend | None:
    """Return the first configured backend that follows ``after`` in the chain.

    Used by the fall-through cascade (WS-SDK-004): we keep walking
    ``_AUTO_PREFERENCE_ORDER`` regardless of the env-pin choice, because
    if the env-pinned backend itself failed transiently the user still
    wants results from the next-best option.
    """
    try:
        start = _AUTO_PREFERENCE_ORDER.index(after) + 1
    except ValueError:
        return None
    for name in _AUTO_PREFERENCE_ORDER[start:]:
        candidate = _BACKENDS.get(name)
        if candidate and candidate.is_configured():
            return candidate
    return None


def _resolve_backend() -> tuple[Backend, list[str]]:
    """Pick a backend from env preference, then the auto fallback chain.

    ``DREADNODE_WEB_SEARCH_BACKEND`` is a soft preference: if it names an
    unknown or unconfigured backend, we emit a warning and fall through to
    the auto order — we never skip straight to DuckDuckGo while a stronger
    provider is configured.
    """
    warnings: list[str] = []

    env_pref = (os.environ.get(_BACKEND_ENV_VAR) or "").strip().lower() or None
    if env_pref and env_pref != "auto":
        pinned = _BACKENDS.get(env_pref)
        if pinned is None:
            warnings.append(f"Unknown {_BACKEND_ENV_VAR} value {env_pref!r}; using auto selection.")
        elif pinned.is_configured():
            return pinned, warnings
        else:
            warnings.append(
                f"{pinned.name} (from {_BACKEND_ENV_VAR}) is not configured; "
                "falling through to auto selection."
            )

    for name in _AUTO_PREFERENCE_ORDER:
        candidate = _BACKENDS.get(name)
        if candidate and candidate.is_configured():
            return candidate, warnings

    # Only reachable in sealed mode: DuckDuckGo reports configured whenever
    # the runtime is not sealed, so an unsealed runtime always matched above.
    if _sealed():
        return _SEALED_BACKEND, warnings

    return _BACKENDS["duckduckgo"], warnings


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def _normalize_domains(domains: list[str] | None) -> list[str]:
    if not domains:
        return []

    normalized: list[str] = []
    for domain in domains:
        cleaned = domain.strip().lower()
        if cleaned.startswith(("http://", "https://")):
            cleaned = urlparse(cleaned).hostname or ""
        cleaned = cleaned.lstrip(".")
        if cleaned and cleaned not in normalized:
            normalized.append(cleaned)
    return normalized


def _extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return (parsed.hostname or "").lower()


def _domain_matches(candidate: str, domains: list[str]) -> bool:
    return any(candidate == domain or candidate.endswith(f".{domain}") for domain in domains)


def _filter_results(
    results: list[dict[str, str]],
    allowed_domains: list[str],
    blocked_domains: list[str],
) -> list[dict[str, str]]:
    filtered: list[dict[str, str]] = []
    for result in results:
        domain = _extract_domain(result.get("url", ""))
        if allowed_domains and not _domain_matches(domain, allowed_domains):
            continue
        if blocked_domains and _domain_matches(domain, blocked_domains):
            continue
        filtered.append(result)
    return filtered


def _rank_results(results: list[dict[str, str]]) -> list[WebSearchResult]:
    ranked: list[WebSearchResult] = []
    for index, result in enumerate(results, start=1):
        url = result.get("url", "")
        ranked.append(
            {
                "title": result.get("title") or "No title",
                "url": url,
                "snippet": result.get("snippet") or "",
                "rank": index,
                "domain": _extract_domain(url),
            }
        )
    return ranked


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------


@tool
async def web_search(
    query: t.Annotated[str, "Search query"],
    *,
    num_results: t.Annotated[int, "Number of results to return (max 10)"] = 5,
    allowed_domains: t.Annotated[
        list[str] | None, "Only include results from these domains or their subdomains"
    ] = None,
    blocked_domains: t.Annotated[
        list[str] | None, "Exclude results from these domains or their subdomains"
    ] = None,
) -> WebSearchResponse:
    """
    Search the web and return structured results.

    Returns a stable payload (``title``, ``url``, ``snippet``, ``domain``,
    ``rank``) regardless of which provider answered. Provider selection is
    handled by the runtime; the response includes a ``backend`` field for
    observability, but the agent does not choose it.

    Backend errors produce ``success=False`` with an empty result set and
    an entry in ``warnings``.
    """
    if allowed_domains and blocked_domains:
        raise ValueError("Cannot specify both allowed_domains and blocked_domains.")

    normalized_num_results = max(1, min(num_results, MAX_RESULTS))
    normalized_allowed = _normalize_domains(allowed_domains)
    normalized_blocked = _normalize_domains(blocked_domains)

    chosen, warnings = _resolve_backend()
    logger.info("Searching ({}): {}", chosen.name, query)

    outcome = await chosen.search(query, normalized_num_results)
    warnings = [*warnings, *outcome.warnings]
    if outcome.error:
        warnings.append(outcome.error)

    # WS-SDK-004: cascade through the auto chain when the chosen backend
    # asks for fall-through (e.g. platform 5xx). Skip 4xx (WS-SDK-005)
    # because those backends return ``should_fall_through=False``.
    while outcome.error and outcome.should_fall_through:
        next_backend = _next_in_auto_chain(chosen.name)
        if next_backend is None:
            break
        chosen = next_backend
        logger.info("Falling through to backend: {}", chosen.name)
        outcome = await chosen.search(query, normalized_num_results)
        warnings.extend(outcome.warnings)
        if outcome.error:
            warnings.append(outcome.error)

    # The cascade dead-ends on the platform 503 in a sealed runtime, leaving
    # "Platform search unavailable" as the only reason — true, but it reads
    # as transient when it is permanent here. Name the actual condition.
    if outcome.error and _sealed() and chosen.name != _SEALED_BACKEND.name:
        warnings.append(SEALED_WARNING)

    success = outcome.error is None

    filtered = _filter_results(outcome.hits, normalized_allowed, normalized_blocked)
    ranked = _rank_results(filtered)

    if success and not ranked:
        warnings.append(
            NO_RESULTS_WARNING
            if not outcome.hits
            else "All results were filtered out by domain rules."
        )

    return {
        "success": success,
        "query": query,
        "backend": chosen.name,
        "result_count": len(ranked),
        "applied_filters": {
            "allowed_domains": normalized_allowed,
            "blocked_domains": normalized_blocked,
        },
        "warnings": warnings,
        "results": ranked,
    }
