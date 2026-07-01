"""Backdated web tools — search and fetch over the GR backdated corpus.

This module owns the *SDK-side* responsibilities for the web tools (the
backend owns egress, extraction and the index):

* input validation (URL shape, query length, domain-list conflicts, ``as_of``)
* the domain ``can_fetch`` preflight
* a process-wide LRU fetch cache (15-min TTL, 50 MB cap)
* cross-host redirect handling (the ``REDIRECT DETECTED`` template)
* the ``Links: <JSON>`` / ``REMINDER`` search envelope the model is trained on

Two ways to use it:

* **Standalone** (no environment needed)::

      from openreward.tools import Backsearch, Backfetch

      bs = Backsearch(as_of="2025-12-01")
      result = await bs.run("ICML 2025 reinforcement learning papers")
      print(result.output)

* **Inside an environment** via :class:`openreward.toolsets.BackSearchToolset`,
  which wraps the same engine functions (:func:`run_search`, :func:`run_fetch`)
  and renders :class:`~openreward.environments.types.ToolOutput`.

Both paths share the engine functions below, so behaviour is identical.
"""

from __future__ import annotations

import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urljoin, urlparse

from openreward.web_service import (
    DomainBlockedError,
    DomainCheckFailedError,
    EgressBlockedError,
    WebServiceClient,
    WebServiceConfig,
    WebServiceError,
    validate_as_of,
)

# Web tool sizing — kept aligned with the standard harness contract.
MAX_URL_LENGTH = 2_000
MAX_FETCH_TEXT_CHARS = 100_000
MIN_SEARCH_QUERY_LENGTH = 2
SEARCH_K = 8  # hardcoded max results cap

# Fetch LRU cache sizing.
FETCH_CACHE_TTL_S = 15 * 60
FETCH_CACHE_MAX_BYTES = 50 * 1024 * 1024


# --------------------------------------------------------------------------- #
# Result type                                                                 #
# --------------------------------------------------------------------------- #


@dataclass
class WebToolResult:
    """Discriminated success/error result shared by the standalone tools and
    the toolset wrappers.

    On success, :attr:`text` is the model-facing rendering and :attr:`data`
    carries the structured payload. On failure, :attr:`error_code` /
    :attr:`error_message` describe a *soft* error the model can recover from
    (bad URL, blocked domain, ...) rather than a crash.
    """

    ok: bool
    text: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    @property
    def output(self) -> str:
        """The string a model should see, whether success or soft error."""
        if self.ok:
            return self.text or ""
        return f"Error [{self.error_code}]: {self.error_message}"

    def raise_for_status(self) -> "WebToolResult":
        if not self.ok:
            raise WebServiceError(0, self.output)
        return self

    @classmethod
    def success(cls, text: str, data: Optional[dict[str, Any]] = None) -> "WebToolResult":
        return cls(ok=True, text=text, data=data)

    @classmethod
    def error(cls, code: str, message: str) -> "WebToolResult":
        return cls(ok=False, error_code=code, error_message=message)


# --------------------------------------------------------------------------- #
# Fetch helpers                                                               #
# --------------------------------------------------------------------------- #


_WEB_FETCH_DESCRIPTION_PREFIX = (
    "IMPORTANT: Backfetch WILL FAIL for authenticated or private URLs. "
    "Before using this tool, check if the URL points to an authenticated service "
    "(e.g. Google Docs, Confluence, Jira, GitHub). If so, look for a specialized "
    "tool that provides authenticated access."
)


def _validate_fetch_url(raw: str) -> tuple[str, Optional[tuple[str, str]]]:
    """Returns ``(post-upgrade-url, None)`` on success, or ``(raw, (code, message))``
    on failure.

    http->https upgrade runs BEFORE the length check; the URL must be parseable,
    <= 2000 chars, carry no userinfo, and have a hostname with >= 2 dot-parts.
    """
    url = raw
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]

    if len(url) > MAX_URL_LENGTH:
        return url, (
            "url-too-long",
            f"URL too long ({len(url)} chars, max {MAX_URL_LENGTH})",
        )
    try:
        parsed = urlparse(url)
    except ValueError:
        return url, ("invalid-url", f'Invalid URL "{raw}". The URL provided could not be parsed.')
    if not parsed.scheme or not parsed.netloc:
        return url, ("invalid-url", f'Invalid URL "{raw}". The URL provided could not be parsed.')
    if parsed.username or parsed.password:
        return url, ("userinfo-not-allowed", f'URL must not include userinfo (got "{raw}")')
    host = parsed.hostname or ""
    if len([p for p in host.split(".") if p]) < 2:
        return url, (
            "hostname-too-shallow",
            f'Hostname must have at least two dot-separated parts (got "{host}")',
        )
    return url, None


def _is_same_host_redirect(original_url: str, target: str) -> bool:
    """Auto-followable: same protocol, same port, no userinfo, same hostname
    modulo a leading ``www.``."""
    try:
        parsed_target = urlparse(urljoin(original_url, target))
        parsed_original = urlparse(original_url)
    except ValueError:
        return False
    if parsed_target.scheme != parsed_original.scheme:
        return False
    if parsed_target.port != parsed_original.port:
        return False
    if parsed_target.username or parsed_target.password:
        return False

    def _strip_www(h: Optional[str]) -> str:
        if not h:
            return ""
        return h.lower().removeprefix("www.")

    return _strip_www(parsed_target.hostname) == _strip_www(parsed_original.hostname)


def _redirect_template(*, original_url: str, redirect_url: str, status: int, prompt: str) -> str:
    return (
        f"REDIRECT DETECTED: The URL redirects to a different host.\n\n"
        f"Original URL: {original_url}\n"
        f"Redirect URL: {redirect_url}\n"
        f"Status: {status}\n\n"
        f"To complete your request, I need to fetch content from the redirected URL. "
        f"Please use Backfetch again with these parameters:\n"
        f'- url: "{redirect_url}"\n'
        f'- prompt: "{prompt}"'
    )


class _FetchCacheEntry:
    __slots__ = ("text", "ts", "nbytes")

    def __init__(self, text: str, ts: float, nbytes: int) -> None:
        self.text = text
        self.ts = ts
        self.nbytes = nbytes


class _UrlLRUCache:
    """LRU keyed by ``(as_of, url)``. 15-min TTL, 50 MB cap by content bytes.

    Module-level singleton — an agent loop makes many short-lived fetch calls
    in a session, so caching across calls is the win. The cache key includes
    ``as_of`` so a backdated fetch never returns content from a different
    cutoff.
    """

    def __init__(self) -> None:
        self._entries: "OrderedDict[str, _FetchCacheEntry]" = OrderedDict()
        self._total = 0

    def get(self, key: str) -> Optional[_FetchCacheEntry]:
        entry = self._entries.get(key)
        if entry is None:
            return None
        if time.monotonic() - entry.ts > FETCH_CACHE_TTL_S:
            self._total -= max(1, entry.nbytes)
            del self._entries[key]
            return None
        self._entries.move_to_end(key)
        return entry

    def put(self, key: str, text: str, nbytes: int) -> None:
        size = max(1, nbytes)
        existing = self._entries.pop(key, None)
        if existing is not None:
            self._total -= max(1, existing.nbytes)
        while self._total + size > FETCH_CACHE_MAX_BYTES and self._entries:
            _, evicted = self._entries.popitem(last=False)
            self._total -= max(1, evicted.nbytes)
        self._entries[key] = _FetchCacheEntry(text=text, ts=time.monotonic(), nbytes=nbytes)
        self._total += size

    def clear(self) -> None:
        self._entries.clear()
        self._total = 0


_url_cache = _UrlLRUCache()


def clear_web_fetch_cache() -> None:
    """Test/admin entry point — drop everything in the fetch LRU."""
    _url_cache.clear()


def _build_fetch_output(*, url: str, text: str, prompt: str) -> dict[str, Any]:
    """Structured payload the calling model can consume directly.

    The SDK does not run a separate summarisation model — the agent's main LLM
    applies ``prompt`` to ``content`` on its next turn. The ``prompt`` field is
    echoed so the model is reminded of its own intent when reading the result
    inside a long transcript.
    """
    return {"url": url, "prompt": prompt, "content": text}


# --------------------------------------------------------------------------- #
# Search helpers                                                              #
# --------------------------------------------------------------------------- #


_WEB_SEARCH_REMINDER = (
    "REMINDER: You MUST include the sources above in your response to the user "
    "using markdown hyperlinks."
)


def _format_search_output(query: str, hits: list[dict[str, Any]]) -> str:
    """Literal ``Links: <JSON>`` envelope + REMINDER trailer.

    Models recognise this exact shape as source-bearing — do NOT pretty-print
    the links block and do NOT drop the REMINDER.
    """
    import json

    lines = [f'Web search results for query: "{query}"', ""]
    # Silently drop None entries (compaction round-trips occasionally leave
    # holes in the list).
    safe_hits = [h for h in hits if isinstance(h, dict) and h.get("url")]
    if not safe_hits:
        lines.append("No links found.")
    else:
        link_objs = [{"title": h.get("title", ""), "url": h.get("url")} for h in safe_hits]
        lines.append("Links: " + json.dumps(link_objs, ensure_ascii=False))
    lines.append("")
    lines.append(_WEB_SEARCH_REMINDER)
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Engine functions (shared by standalone tools and the toolset)              #
# --------------------------------------------------------------------------- #


def _resolve_config(config: Optional[WebServiceConfig]) -> Optional[WebServiceConfig]:
    return config if config is not None else WebServiceConfig.from_env()


async def run_fetch(
    *,
    url: str,
    prompt: str,
    as_of: Optional[str] = None,
    config: Optional[WebServiceConfig] = None,
    client: Optional[WebServiceClient] = None,
) -> WebToolResult:
    """Fetch ``url`` from the backdated corpus and return a model-facing result.

    If ``client`` is provided it is reused (and left open); otherwise a
    short-lived client is created and closed. ``as_of`` overrides the config's
    default cutoff for this call.
    """
    if not url:
        return WebToolResult.error("missing-url", "`url` is required")
    if not prompt:
        return WebToolResult.error("missing-prompt", "`prompt` is required")

    config = _resolve_config(config)
    if config is None:
        return WebToolResult.error(
            "not-configured",
            "Backfetch is not configured. Set OPENREWARD_API_KEY (and optionally "
            "OPENREWARD_WEB_FETCH_URL / OPENREWARD_WEB_DOMAIN_INFO_URL) in your environment.",
        )

    try:
        as_of = validate_as_of(as_of) or validate_as_of(config.default_as_of)
    except ValueError as e:
        return WebToolResult.error("invalid-as-of", str(e))

    clean_url, validation_error = _validate_fetch_url(url)
    if validation_error is not None:
        code, message = validation_error
        return WebToolResult.error(code, message)
    url = clean_url

    hostname = (urlparse(url).hostname or "").lower()
    cache_key = f"{as_of or ''}|{url}"

    owns_client = client is None
    if client is None:
        client = WebServiceClient(config)
    try:
        # Domain preflight (skippable for enterprise networks where the policy
        # endpoint isn't reachable).
        if not config.skip_preflight:
            try:
                info = await client.domain_info(hostname)
            except DomainCheckFailedError as e:
                return WebToolResult.error("domain-check-failed", str(e))
            if not info.get("can_fetch"):
                reason = info.get("reason")
                return WebToolResult.error(
                    "domain-blocked",
                    f"Domain blocked by policy: {hostname}"
                    + (f" ({reason})" if reason else ""),
                )

        # LRU hit returns immediately.
        cached = _url_cache.get(cache_key)
        if cached is not None:
            return WebToolResult.success(
                _render_fetch_text(url, cached.text, prompt, hostname, config),
                _build_fetch_output(url=url, text=cached.text, prompt=prompt),
            )

        try:
            resp = await client.fetch(url=url, as_of=as_of)
        except EgressBlockedError as e:
            return WebToolResult.error("egress-blocked", str(e))
        except DomainBlockedError as e:
            return WebToolResult.error("domain-blocked", str(e))
        except WebServiceError as e:
            return WebToolResult.error("web-service-error", str(e))
        except Exception as e:  # noqa: BLE001 — last-resort transport unwrap
            return WebToolResult.error("fetch-error", f"Fetch error: {e}")
    finally:
        if owns_client:
            await client.aclose()

    # Cross-host redirect surfaces as a structured prompt template rather than
    # auto-following.
    if resp.redirect and not _is_same_host_redirect(url, resp.redirect.get("to", "")):
        return WebToolResult.success(
            _redirect_template(
                original_url=url,
                redirect_url=resp.redirect["to"],
                status=int(resp.redirect.get("status", 302)),
                prompt=prompt,
            ),
            {"redirect": resp.redirect, "url": url},
        )

    text = resp.text or ""
    if not text.strip():
        return WebToolResult.success(
            "(empty response)", {"url": url, "content": "(empty response)"}
        )

    if len(text) > MAX_FETCH_TEXT_CHARS:
        text = text[:MAX_FETCH_TEXT_CHARS] + "\n... (truncated)"

    nbytes = len(text.encode("utf-8"))
    _url_cache.put(cache_key, text, nbytes)

    return WebToolResult.success(
        _render_fetch_text(url, text, prompt, hostname, config),
        _build_fetch_output(url=url, text=text, prompt=prompt),
    )


def _render_fetch_text(
    url: str, text: str, prompt: str, hostname: str, config: WebServiceConfig
) -> str:
    """The string a model sees for a fetch. Preapproved hosts get raw content
    (no prompt-echo wrapper); everything else gets a labelled envelope."""
    if hostname in config.preapproved_hosts and len(text) < MAX_FETCH_TEXT_CHARS:
        return text
    return f"Fetched content from {url}:\n\n{text}"


async def run_search(
    *,
    query: str,
    as_of: Optional[str] = None,
    allowed_domains: Optional[list[str]] = None,
    blocked_domains: Optional[list[str]] = None,
    k: int = SEARCH_K,
    config: Optional[WebServiceConfig] = None,
    client: Optional[WebServiceClient] = None,
) -> WebToolResult:
    """Search the backdated corpus and return the ``Links:`` / REMINDER envelope."""
    query = (query or "").strip()
    if len(query) < MIN_SEARCH_QUERY_LENGTH:
        return WebToolResult.error(
            "missing-query",
            f"Missing query (must be at least {MIN_SEARCH_QUERY_LENGTH} characters)",
        )

    allowed = [d for d in (allowed_domains or []) if d]
    blocked = [d for d in (blocked_domains or []) if d]
    if allowed and blocked:
        return WebToolResult.error(
            "domain-lists-conflict",
            "Cannot specify both allowed_domains and blocked_domains in the same request",
        )

    config = _resolve_config(config)
    if config is None:
        return WebToolResult.error(
            "not-configured",
            "Backsearch is not configured. Set OPENREWARD_API_KEY (and optionally "
            "OPENREWARD_WEB_SEARCH_URL) in your environment.",
        )

    try:
        as_of = validate_as_of(as_of) or validate_as_of(config.default_as_of)
    except ValueError as e:
        return WebToolResult.error("invalid-as-of", str(e))

    owns_client = client is None
    if client is None:
        client = WebServiceClient(config)
    try:
        try:
            resp = await client.search(
                query=query,
                as_of=as_of,
                k=k,
                allowed_domains=allowed or None,
                blocked_domains=blocked or None,
            )
        except EgressBlockedError as e:
            return WebToolResult.error("egress-blocked", str(e))
        except WebServiceError as e:
            return WebToolResult.error("web-service-error", str(e))
        except Exception as e:  # noqa: BLE001
            return WebToolResult.error("search-failed", f"Search error: {e}")
    finally:
        if owns_client:
            await client.aclose()

    hits = list(resp.get("hits") or [])
    return WebToolResult.success(
        _format_search_output(query, hits),
        {"query": query, "hits": hits, "mode": resp.get("mode")},
    )


# --------------------------------------------------------------------------- #
# Standalone tools (environment-independent)                                  #
# --------------------------------------------------------------------------- #


SEARCH_INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "query": {"type": "string", "minLength": MIN_SEARCH_QUERY_LENGTH},
        "allowed_domains": {"type": "array", "items": {"type": "string"}},
        "blocked_domains": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["query"],
}

FETCH_INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "prompt": {"type": "string"},
    },
    "required": ["url", "prompt"],
}

SEARCH_DESCRIPTION = (
    "- Search the backdated web corpus and return a list of source URLs to cite\n"
    "- Results are limited to documents published on or before the configured cutoff date\n"
    "- Returns a list of {title, url} hits; no permission prompt required\n\n"
    "Usage notes:\n"
    "- Queries should be specific and well-scoped; vague queries return generic results\n"
    "- Pass allowed_domains to restrict the search, or blocked_domains to exclude sites — never both\n"
    "- Your final response MUST include a 'Sources:' section with markdown hyperlinks for any URL you cite"
)

FETCH_DESCRIPTION = (
    f"{_WEB_FETCH_DESCRIPTION_PREFIX}\n\n"
    "- Fetches content from a URL as it existed on or before the configured cutoff date\n"
    "- Takes a URL and a prompt as input\n"
    "- HTTP URLs are upgraded to HTTPS before any network call\n"
    "- Use this tool when you need to retrieve and analyze public web content\n\n"
    "Usage notes:\n"
    "- The URL must be a fully-formed valid URL (hostname has at least two dot-parts, no userinfo)\n"
    "- The prompt should describe what information you want to extract from the page\n"
    "- This tool is read-only and does not modify any files\n"
    "- Results are truncated to 100 KB; cross-host redirects return a REDIRECT DETECTED template — re-call with the new URL\n"
    "- Includes a self-cleaning 15-minute cache for faster responses"
)


class Backsearch:
    """Environment-independent backdated web search.

    ::

        bs = Backsearch(as_of="2025-12-01")
        result = await bs.run("ICML 2025 reinforcement learning papers")
        if result.ok:
            print(result.output)

    ``as_of`` (ISO ``YYYY-MM-DD``) sets the corpus cutoff; if omitted, the
    ``OPENREWARD_WEB_AS_OF`` env var (via :meth:`WebServiceConfig.from_env`) is
    used, else the backend defaults to today. Credentials/URLs come from
    ``OPENREWARD_WEB_*`` unless an explicit ``config`` is passed.
    """

    name = "Backsearch"
    description = SEARCH_DESCRIPTION
    input_schema = SEARCH_INPUT_SCHEMA

    def __init__(
        self,
        *,
        as_of: Optional[str] = None,
        config: Optional[WebServiceConfig] = None,
        k: int = SEARCH_K,
    ) -> None:
        # Validation is deferred to the engine, which surfaces a malformed
        # cutoff as a recoverable ``invalid-as-of`` result rather than raising.
        self.as_of = as_of
        self.config = config
        self.k = k

    async def run(
        self,
        query: str,
        *,
        allowed_domains: Optional[list[str]] = None,
        blocked_domains: Optional[list[str]] = None,
        as_of: Optional[str] = None,
    ) -> WebToolResult:
        return await run_search(
            query=query,
            as_of=as_of or self.as_of,
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains,
            k=self.k,
            config=self.config,
        )

    __call__ = run


class Backfetch:
    """Environment-independent backdated web fetch. See :class:`Backsearch`
    for how ``as_of`` and credentials are resolved.

    ::

        bf = Backfetch(as_of="2025-12-01")
        result = await bf.run("https://example.com", "summarise this page")
    """

    name = "Backfetch"
    description = FETCH_DESCRIPTION
    input_schema = FETCH_INPUT_SCHEMA

    def __init__(
        self,
        *,
        as_of: Optional[str] = None,
        config: Optional[WebServiceConfig] = None,
    ) -> None:
        # See Backsearch — cutoff validation is deferred to the engine.
        self.as_of = as_of
        self.config = config

    async def run(
        self,
        url: str,
        prompt: str,
        *,
        as_of: Optional[str] = None,
    ) -> WebToolResult:
        return await run_fetch(
            url=url,
            prompt=prompt,
            as_of=as_of or self.as_of,
            config=self.config,
        )

    __call__ = run
