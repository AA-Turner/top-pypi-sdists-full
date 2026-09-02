import asyncio
import random
from typing import Any

from matrx_utils import vcprint

from matrx_scraper.search.brave_client import BraveRateLimitError, get_client

verbose = False


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
) -> dict[str, Any] | None:
    client = get_client()
    max_retries = 2
    retry_count = 0

    while retry_count <= max_retries:
        try:
            vcprint(
                f"Executing Brave Search query: {query} Country: {country.upper()}",
                verbose=verbose,
                color="blue",
            )

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
                base_delay = 3 + (retry_count * 2)
                jitter = random.uniform(0, 1.0)
                retry_delay = base_delay + jitter
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
            return None

        except Exception as e:
            vcprint(
                f"[brave_search] Search failed for query '{query}': {e}",
                title=f"Error for query '{query}'",
                color="red",
            )
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
    }
