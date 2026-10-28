import asyncio
import random
from typing import Any

from matrx_utils import capture_error, vcprint

from matrx_scraper.search.brave_client import BraveRateLimitError, get_client

verbose = False

#: Why the last search for a query came back empty-handed (bounded). `async_brave_search` keeps its
#: contract — None is a failure — but a caller that reports the failure (research_web) names the real
#: cause instead of "All search queries failed" (2026-10-24: a live failure answered in ~50 ms with no
#: trace anywhere, because the exception was printed and dropped).
_FAILURE_REASONS: dict[str, str] = {}
_MAX_FAILURE_REASONS = 256


def _note_failure(query: str, reason: str) -> None:
    if len(_FAILURE_REASONS) >= _MAX_FAILURE_REASONS:
        _FAILURE_REASONS.pop(next(iter(_FAILURE_REASONS)))
    _FAILURE_REASONS[query] = reason


#: Marker in ``brave_failure_reason`` for a throttle that outlasted every retry — a caller
#: tells "the provider is rate-limiting; try again" apart from any other failure with it.
RATE_LIMITED_REASON = "the search engine is rate-limiting us (HTTP 429)"


def rate_limit_backoff_seconds(attempt: int) -> float:
    """Back-off before throttle retry ``attempt`` (1-based), without jitter: 5 s, 7 s, 9 s, …"""
    return 3.0 + 2.0 * attempt


def brave_failure_reason(query: str) -> str | None:
    """Why the last `async_brave_search` for `query` returned None, or None when it did not fail."""
    return _FAILURE_REASONS.get(query)


def extract_urls_from_search_results(
    queries_with_results: list[tuple[str, dict[str, Any] | None]],
) -> list[dict[str, str]]:
    """Flatten Brave web results into a deduplicated, ordered scrape list.

    The counterpart to `generate_search_text_summary`: that one renders the
    results for a reader, this one hands the search-then-scrape pipeline the
    URLs to fetch. Order is preserved (Brave's relevance ranking) so a caller
    that truncates to an effort budget keeps the best results.
    """
    seen: set[str] = set()
    urls: list[dict[str, str]] = []
    for _query, result in queries_with_results:
        if not result:
            continue
        for item in result.get("web", {}).get("results", []):
            url = item.get("url")
            if not url or url in seen:
                continue
            seen.add(url)
            urls.append(
                {
                    "url": url,
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                }
            )
    return urls


def site_icons_from_search_results(
    queries_with_results: list[tuple[str, dict[str, Any] | None]],
) -> dict[str, str]:
    """Each result URL's own site icon, as Brave reports it (`meta_url.favicon`).

    For the reader's screen only: the summary text the model reads never carries
    these, so they cost no tokens and no share of the result budget.
    """
    icons: dict[str, str] = {}
    for _query, result in queries_with_results:
        if not result:
            continue
        items = (
            result.get("web", {}).get("results", [])
            + result.get("news", {}).get("results", [])
            + result.get("news", {}).get("videos", [])
            + result.get("videos", {}).get("results", [])
        )
        for item in items:
            url = item.get("url")
            favicon = (item.get("meta_url") or {}).get("favicon")
            if url and isinstance(favicon, str) and favicon.startswith("https://") and url not in icons:
                icons[url] = favicon
    return icons


def generate_search_text_summary(
    queries_with_results: list[tuple[str, dict[str, Any] | None]],
) -> str:
    seen_urls: set[str] = set()
    query_counts: list[tuple[str, int]] = []
    body_parts: list[str] = []
    total_result_count = 0

    for query, result in queries_with_results:
        if result:
            items = (
                result.get("web", {}).get("results", [])
                + result.get("news", {}).get("results", [])
                + result.get("news", {}).get("videos", [])
                + result.get("videos", {}).get("results", [])
            )

            query_result_count = 0
            section_lines: list[str] = []
            for item in items:
                url = item.get("url")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    query_result_count += 1
                    total_result_count += 1

                    title = item.get("title", "N/A")
                    description = item.get("description", "N/A")
                    extra_snippets_content = item.get("extra_snippets", [])
                    age = item.get("age", item.get("page_age", "N/A"))
                    age_text = f" ({age})" if age != "N/A" else ""

                    section_lines.append(
                        f"Title: {title}{age_text}\nURL: {url}\nDescription: {description}\n"
                    )
                    if extra_snippets_content:
                        section_lines.append(
                            f"Extra Snippets: {' '.join(extra_snippets_content)}\n"
                        )
                    section_lines.append("\n")

            query_counts.append((query, query_result_count))
            header = f'---\n## "{query}" ({query_result_count} results)\n\n'
            if query_result_count == 0:
                body_parts.append(header + "(No unique results for this query)\n\n")
            else:
                body_parts.append(header + "".join(section_lines))
        else:
            query_counts.append((query, 0))
            body_parts.append(f'---\n## "{query}" (0 results)\n\n(No results for this query)\n\n')

    top_summary = "Searched: " + ", ".join(f'"{q}" ({c})' for q, c in query_counts) + "\n\n"
    body = "".join(body_parts)

    content_length = len(top_summary) + len(body)
    metrics_lines = [
        f"Query count: {len(queries_with_results)}",
        f"Results count: {total_result_count}",
        f"Total character count: {content_length}",
    ]
    bottom_metrics = "\n---\n## Search Summary Metrics:\n\n" + "\n".join(metrics_lines)

    return top_summary + body + bottom_metrics


async def async_brave_search(
    query: str,
    count: int = 20,
    offset: int = 0,
    country: str = "us",
    timeout: int = 10,  # noqa: ASYNC109 - httpx per-request timeout, not a cancellation scope
    extra_snippets: bool = True,
    safe_search: str | None = None,
    freshness: str | None = None,
    max_retries: int = 2,
) -> dict[str, Any] | None:
    """One Brave web search, or ``None`` on a real failure (``brave_failure_reason`` says why).

    A throttle (HTTP 429) is retried ``max_retries`` times with a growing back-off
    (``rate_limit_backoff_seconds``); the host passes its knob, the package keeps 2.
    """
    client = get_client()
    max_retries = max(0, int(max_retries))
    retry_count = 0

    while retry_count <= max_retries:
        try:
            vcprint(
                f"Executing Brave Search query: {query} Country: {country.upper()}",
                verbose=verbose,
                color="blue",
            )

            _FAILURE_REASONS.pop(query, None)
            result = await client.search(
                query=query,
                count=count,
                offset=offset,
                country=country,
                extra_snippets=extra_snippets,
                safe_search=safe_search or "off",
                freshness=freshness,
                timeout=timeout,
            )

            vcprint(
                data=result,
                title=f"Search Results for '{query}'",
                verbose=verbose,
                color="green",
            )
            return result

        except BraveRateLimitError as e:
            # Throttled (HTTP 429). This is NOT zero results — back off and retry
            # so a transient rate limit can never masquerade as an empty search.
            if retry_count < max_retries:
                retry_count += 1
                retry_delay = rate_limit_backoff_seconds(retry_count) + random.uniform(0, 1.0)
                vcprint(
                    f"[brave_search] THROTTLED (429) — retrying in {retry_delay:.1f}s "
                    f"(attempt {retry_count}/{max_retries}): {e}",
                    title=f"Retry for query '{query}'",
                    color="yellow",
                )
                await asyncio.sleep(retry_delay)
                continue

            vcprint(
                f"[brave_search] THROTTLED (429) — exhausted {max_retries} retries "
                f"for query '{query}'. Returning no results (caller MUST treat as "
                f"a failure, not an empty result set).",
                title="Brave throttled",
                color="red",
            )
            _note_failure(query, RATE_LIMITED_REASON)
            return None

        except Exception as e:
            vcprint(
                f"[brave_search] Search failed for query '{query}': {e}",
                title=f"Error for query '{query}'",
                color="red",
            )
            _note_failure(query, f"{type(e).__name__}: {e}")
            # Printed and dropped was the defect: record it where errors are read.
            await capture_error(e, kind="brave_search_failed", context={"query_length": len(query), "country": country})
            return None

    return None


async def wrapped_brave_search(
    queries: list[str],
    count: int = 20,
    offset: int = 0,
    country: str = "us",
    timeout: int = 10,  # noqa: ASYNC109 - httpx per-request timeout, not a cancellation scope
    extra_snippets: bool = True,
    safe_search: str | None = None,
    freshness: str | None = None,
    emitter=None,
    call_id=None,
) -> dict[str, Any]:
    """Execute multiple search queries, emitting progress via an optional Emitter.

    This is a high-level wrapper around async_brave_search that handles
    multi-query execution and result aggregation with optional streaming
    progress events.
    """
    queries_with_results: list[tuple[str, dict[str, Any] | None]] = []

    for query in queries:
        result = await async_brave_search(
            query=query,
            count=count,
            offset=offset,
            country=country,
            timeout=timeout,
            extra_snippets=extra_snippets,
            safe_search=safe_search,
            freshness=freshness,
        )
        if emitter is not None:
            await emitter.send_tool_event(
                {
                    "event": "tool_progress",
                    "call_id": call_id or "",
                    "tool_name": "web_research",
                    "message": f"Searched for: {query}",
                    "show_spinner": True,
                    "data": {"type": "brave_default_page", "content": result},
                }
            )
        queries_with_results.append((query, result))

    unique_text_summary = generate_search_text_summary(queries_with_results)
    original_results = [result for _, result in queries_with_results]

    return {
        "original_results": original_results,
        "unique_text_summary": unique_text_summary,
        "site_icons": site_icons_from_search_results(queries_with_results),
    }
