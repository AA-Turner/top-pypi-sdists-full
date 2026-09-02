from __future__ import annotations

import asyncio
import time
import traceback
from typing import Any

from matrx_utils import vcprint
from pydantic import ValidationError

from matrx_ai.tools.arg_models.web_args import (
    RESEARCH_DEPTH_CONFIG,
    WebArgs,
    WebBatchReadWire,
    WebReadArgs,
    WebReadWire,
    WebResearchArgs,
    WebSearchArgs,
    WebSearchWire,
)
from matrx_ai.tools.implementations._web_read_caps import (
    RESULT_BUDGET_CHARS,
    enforce_result_budget,
    extract_page_text,
    per_url_budget,
    resolve_chars,
    window_page_content,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS, cap_text
from matrx_ai.tools.streaming import ToolStreamManager

_RESEARCH_REPORT_CHAR_BUDGET = 32_000
_RESEARCH_FINAL_CHAR_BUDGET = 45_000
_SEARCH_RESULT_CHAR_BUDGET = TOOL_RESULT_SOFT_CAP_CHARS - 1_000


def _cap_research_section(text: str, *, limit: int, label: str) -> tuple[str, bool]:
    capped, info = cap_text(text, limit=limit)
    if not info.truncated:
        return capped, False
    notice = (
        f"\n\n[Research output section '{label}' was shortened from "
        f"{info.total_chars:,} to {info.shown_chars:,} characters. Use web "
        "action='read' on the cited URLs or run research_web with narrower "
        "queries for more detail.]"
    )
    return capped + notice, True


def _resolve_read_chars(args: dict[str, Any], fields_set: set[str] | None = None) -> int:
    return resolve_chars(
        chars=args.get("chars"),
        max_content_length=args.get("max_content_length"),
        fields_set=fields_set or set(args.keys()),
    )


# ---------------------------------------------------------------------------
# Register AI condensers with the scraper package on import.
# The scraper has no dependency on matrx_ai; instead it exposes an extension
# registry that any caller can populate.  We do it here so that any app which
# imports matrx_ai's web tool automatically gets the condensers wired in.
# ---------------------------------------------------------------------------
try:
    from matrx_scraper.features.extensions import configure_extensions

    from matrx_ai.agent_runners.research import (
        scrape_research_condenser_agent_1,
        scrape_research_condenser_agent_2,
    )

    configure_extensions(
        condenser_1=scrape_research_condenser_agent_1,
        condenser_2=scrape_research_condenser_agent_2,
    )
except ImportError:
    pass


async def web_search(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = WebSearchArgs(**args)
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "web_search")

    try:
        from matrx_scraper.features.quick_search import (
            search_web_mcp_quick,
        )

        all_text_results: list[str] = []
        for query in parsed.queries:
            await stream.progress(f"Searching: {query}")
            results = await search_web_mcp_quick(
                queries=[query],
                freshness=parsed.freshness,
                count=parsed.max_results_per_query,
                emitter=ctx.emitter,
                call_id=ctx.call_id,
            )
            if isinstance(results, dict) and results.get("status") == "success":
                text_content = results.get("result", "")
                if text_content:
                    all_text_results.append(text_content)

        combined_text = "\n\n".join(all_text_results)

        if not combined_text.strip():
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="execution",
                    message="No search results found for the given queries.",
                    is_retryable=True,
                    suggested_action="Try different or broader search queries.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="web_search",
                call_id=ctx.call_id,
            )

        query_label = f"{len(parsed.queries)} quer{'ies' if len(parsed.queries) != 1 else 'y'}"
        await stream.progress(f"Search complete — {query_label} finished")

        capped, info = cap_text(combined_text, limit=_SEARCH_RESULT_CHAR_BUDGET)
        if info.truncated:
            capped += (
                f"\n\n[Search results shortened from {info.total_chars:,} to "
                f"{info.shown_chars:,} characters. Narrow queries or use web "
                "action='read' on specific URLs for more detail.]"
            )

        return ToolResult(
            success=True,
            output=capped,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web_search",
            call_id=ctx.call_id,
            output_self_capped=True,
        )

    except ImportError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="import",
                message=f"Scraper module not available: {exc}",
                suggested_action="Ensure the scraper package is installed.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web_search",
            call_id=ctx.call_id,
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="execution",
                message=f"Web search failed: {exc}",
                is_retryable=True,
                suggested_action="Try with different queries or fewer queries.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web_search",
            call_id=ctx.call_id,
        )


async def web_read(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Read/scrape web pages with standard offset/chars paging."""
    started_at = time.time()
    parsed = WebReadArgs(**args)
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "web_read")
    offset = max(0, int(args.get("offset", parsed.offset) or 0))
    chars = _resolve_read_chars(args, set(args.keys()))
    url_budget = per_url_budget(len(parsed.urls))

    try:
        from matrx_scraper.features.read_page import (
            read_page_mcp_quick,
        )

        pages: list[dict[str, Any]] = []
        for url in parsed.urls:
            await stream.progress(f"Reading: {url[:60]}...")
            result = await read_page_mcp_quick(url=url)
            text = extract_page_text(result)
            if isinstance(result, dict) and result.get("status") == "error":
                pages.append(
                    window_page_content(
                        "",
                        url=url,
                        offset=0,
                        chars=chars,
                        success=False,
                        error=text or "Sorry could not access this page.",
                    )
                )
                continue
            pages.append(
                window_page_content(
                    text,
                    url=url,
                    offset=offset,
                    chars=chars,
                    per_url_budget=url_budget,
                )
            )

        if parsed.summarize and parsed.instructions:
            await stream.step("summarize", "Summarizing page content...")
            from matrx_ai.tools.implementations._summarize_helper import (
                summarize_content,
            )

            # Summarize from the windowed pages (already bounded).
            combined = "\n\n---\n\n".join(f"URL: {p['url']}\n{p.get('content', '')}" for p in pages)
            summary, child_usages = await summarize_content(
                content=combined,
                instructions=parsed.instructions,
                ctx=ctx,
            )
            capped_summary, info = cap_text(summary, limit=_SEARCH_RESULT_CHAR_BUDGET)
            if info.truncated:
                capped_summary += (
                    f"\n\n[Summary shortened from {info.total_chars:,} to "
                    f"{info.shown_chars:,} characters.]"
                )
            return ToolResult(
                success=True,
                output=capped_summary,
                child_usages=child_usages,
                started_at=started_at,
                completed_at=time.time(),
                tool_name="web_read",
                call_id=ctx.call_id,
                output_self_capped=True,
            )

        output = enforce_result_budget(
            {
                "pages": pages,
                "count": len(pages),
                "succeeded": sum(1 for p in pages if p.get("success")),
                "failed": sum(1 for p in pages if not p.get("success")),
            },
            budget=RESULT_BUDGET_CHARS,
        )
        return ToolResult(
            success=True,
            output=output,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web_read",
            call_id=ctx.call_id,
            output_self_capped=True,
        )

    except ImportError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="import",
                message=f"Scraper module not available: {exc}",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web_read",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="execution",
                message=f"Web read failed: {exc}",
                is_retryable=True,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web_read",
            call_id=ctx.call_id,
        )


async def research_web(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    from matrx_ai.tools._generated_declarations import ResearchWebArgs

    ResearchWebArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    parsed = WebResearchArgs(**args)
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "research_web")

    depth_cfg = RESEARCH_DEPTH_CONFIG[parsed.research_depth]
    urls_per_query = depth_cfg["urls_per_query"]
    good_scrape_threshold = depth_cfg["good_scrape_threshold"]
    target_good_per_query = depth_cfg["target_good_per_query"]

    timing: dict[str, Any] = {}

    try:
        from matrx_ai._ext import get_ext

        _brave = get_ext("brave_search")
        async_brave_search = _brave["async_brave_search"]
        generate_search_text_summary = _brave["generate_search_text_summary"]
        from matrx_scraper.features.mcp_tool_helpers import (
            scrape_urls_from_search_result,
        )
        from matrx_scraper.features.utils import (
            format_scraped_pages_section,
        )

        # ------------------------------------------------------------------
        # Phase 1: Concurrent search — fire all queries at once
        # ------------------------------------------------------------------
        search_start = time.perf_counter()

        async def _search_with_query(query: str) -> tuple[str, dict[str, Any] | None]:
            result = await async_brave_search(
                query=query,
                freshness=parsed.freshness,
                country=parsed.country,
                extra_snippets=True,
            )
            return (query, result)

        search_tasks = [_search_with_query(q) for q in parsed.queries]

        queries_with_results: list[tuple[str, dict[str, Any] | None]] = []
        # Global dedup set populated synchronously in the sequential search loop
        # so that each concurrent scraping task receives a filtered search result
        # containing only URLs not yet seen — eliminating the TOCTOU that would
        # arise from sharing a mutable set across concurrent asyncio tasks.
        seen_urls: set[str] = set()
        scraping_tasks: list[asyncio.Task[list[dict[str, Any]]]] = []
        scraping_start_time: float | None = None

        for search_coro in asyncio.as_completed(search_tasks):
            query, search_result = await search_coro

            if not search_result:
                continue

            queries_with_results.append((query, search_result))

            await stream.progress(f"Searched: {query}")

            if scraping_start_time is None:
                scraping_start_time = time.perf_counter()

            # Pre-filter URLs here (sequential — no concurrency) and build a
            # task-local search result containing only the unseen URLs.  The
            # concurrent scraping task then receives an empty seen_urls so the
            # URL-selection logic inside scrape_urls_from_search_result is
            # effectively a no-op filter and scrapes exactly what we selected.
            combined = search_result.get("web", {}).get("results", []) + search_result.get(
                "news", {}
            ).get("results", [])
            filtered_results: list[dict[str, Any]] = []
            for r in combined[:urls_per_query]:
                url = r.get("url")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    filtered_results.append(r)

            if not filtered_results:
                continue

            task_search_result = {
                "web": {"results": filtered_results},
                "news": {"results": []},
            }

            scraping_task = asyncio.create_task(
                scrape_urls_from_search_result(
                    search_result=task_search_result,
                    seen_urls=set(),  # already deduplicated above
                    urls_per_query=urls_per_query,
                    good_scrape_threshold=good_scrape_threshold,
                    emitter=ctx.emitter,
                    call_id=ctx.call_id,
                )
            )
            scraping_tasks.append(scraping_task)

        if not queries_with_results:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="execution",
                    message="All search queries failed to return results.",
                    is_retryable=True,
                    suggested_action="Try different search queries or check network connectivity.",
                ),
                started_at=started_at,
                completed_at=time.time(),
            )

        # ------------------------------------------------------------------
        # Phase 2: Wait for all scraping to complete
        # ------------------------------------------------------------------
        all_scraped_results = await asyncio.gather(*scraping_tasks)
        all_scraped_pages = [page for result in all_scraped_results for page in result]

        # ------------------------------------------------------------------
        # Zero-evidence guard — NEVER run the condenser on an empty corpus.
        #
        # The condenser is an LLM told to "assemble a detailed report." Given no
        # evidence it fabricates one (the hallucination incident). The old
        # `if not queries_with_results` guard above is insufficient: a throttled
        # or degraded Brave returns truthy-but-empty 200 dicts (`web.results == []`),
        # so `queries_with_results` is non-empty while carrying zero real hits, and
        # the static "SEARCH RESULT PREVIEWS" header keeps `full_context` non-blank.
        #
        # Real evidence = (search hits across all queries) OR (scraped pages).
        # Snippets alone are legitimate evidence, so we only bail when BOTH are zero.
        # This is cause-agnostic: throttle, empty-200, or network failure all land here.
        total_search_hits = sum(
            len(sr.get("web", {}).get("results", [])) + len(sr.get("news", {}).get("results", []))
            for _, sr in queries_with_results
            if sr
        )
        if total_search_hits == 0 and len(all_scraped_pages) == 0:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="execution",
                    message=(
                        f"Research produced zero evidence: {len(parsed.queries)} "
                        f"queries returned no usable search results and no pages were "
                        f"scraped. Refusing to synthesize a report from an empty corpus."
                    ),
                    is_retryable=True,
                    suggested_action=(
                        "The search provider may be throttling or temporarily "
                        "degraded. Retry shortly, or try broader/different queries."
                    ),
                ),
                started_at=started_at,
                completed_at=time.time(),
            )

        search_and_scrape_end = time.perf_counter()
        timing["total_search_time"] = round(search_and_scrape_end - search_start, 2)
        timing["total_scraping_time"] = (
            round(search_and_scrape_end - scraping_start_time, 2) if scraping_start_time else 0
        )

        good_scrapes = [s for s in all_scraped_pages if s.get("is_good_scrape", False)]
        thin_scrapes = [s for s in all_scraped_pages if not s.get("is_good_scrape", False)]
        limited_good_scrapes = good_scrapes[: target_good_per_query * len(parsed.queries)]

        total_attempted = len(seen_urls)
        failed_count = total_attempted - len(all_scraped_pages)

        await stream.step(
            "scraping_complete",
            f"Scraped {len(all_scraped_pages)} pages ({len(good_scrapes)} good, {len(thin_scrapes)} thin, {failed_count} failed)",
        )

        # ------------------------------------------------------------------
        # Phase 3: Format context for the condensation agent
        # ------------------------------------------------------------------
        scraped_pages_content = format_scraped_pages_section(
            limited_good_scrapes=limited_good_scrapes,
            thin_scrapes=thin_scrapes,
        )

        search_previews_raw = generate_search_text_summary(queries_with_results)
        search_previews_content = (
            f"=== SEARCH RESULT PREVIEWS (Not Fully Scraped) ===\n\n{search_previews_raw}"
        )

        full_context_for_agent = scraped_pages_content + "\n" + search_previews_content

        # ------------------------------------------------------------------
        # Phase 4: Run the research condensation agent
        # ------------------------------------------------------------------
        research_report = ""
        agent_child_usages: list = []

        if full_context_for_agent.strip():
            await stream.step(
                "condensing", "Conducting in-depth research analysis on scraped content"
            )

            from matrx_ai.agent_runners.research import scrape_research_condenser_agent_1

            queries_str = ", ".join(parsed.queries)

            agent_result = await scrape_research_condenser_agent_1(
                instructions=parsed.instructions,
                scraped_content=full_context_for_agent,
                queries=queries_str,
                search_results=search_previews_raw,
                ctx=ctx,
            )

            if agent_result.success and agent_result.output:
                capped_report, report_truncated = _cap_research_section(
                    agent_result.output,
                    limit=_RESEARCH_REPORT_CHAR_BUDGET,
                    label="curated_report",
                )
                research_report = (
                    f"\n# Curated Research Results\n\n"
                    f"The following is the result of successfully scraping {len(good_scrapes)} pages "
                    f"and an agent conducting a full review of the top results:\n\n"
                    f"{capped_report}\n---\n"
                )
                if report_truncated:
                    timing["research_report_truncated"] = True
                agent_child_usages = agent_result.usage_history
            else:
                research_report = (
                    "\n# Research Condensation\n\n"
                    "The research agent was unable to produce a condensed report. "
                    "Raw search results and scraped content are provided below.\n---\n"
                )

        # ------------------------------------------------------------------
        # Phase 5: Assemble final output
        # ------------------------------------------------------------------
        all_search_results_text = f"\n# All Search Results:\n\n{search_previews_raw}\n---\n"

        next_steps = (
            "\n## Next steps:\n\n"
            "Assess if this context answers the user's query. If gaps remain or more detail is needed, take action:\n"
            "- Use `web_read` to get complete content from any of the URLs shown in the search results above\n"
            "- Use `web_read` on any specific URLs the user mentioned that seem relevant\n"
            "- Use `web_search` with different or more specific terms if these results miss the mark\n"
            "- Do a new research, just like this one, but with new queries and more specific instructions.\n\n"
            "If the context above sufficiently answers the query, respond directly to the user."
        )

        final_text = (
            f"Comprehensive research using the following queries: {', '.join(parsed.queries)}.\n"
            + all_search_results_text
            + research_report
            + next_steps
        )
        final_text, final_truncated = _cap_research_section(
            final_text,
            limit=_RESEARCH_FINAL_CHAR_BUDGET,
            label="final_result",
        )

        end_time = time.perf_counter()
        timing["condensation_time"] = round(end_time - search_and_scrape_end, 2)
        timing["total_execution_time"] = round(
            end_time - (started_at if isinstance(started_at, float) else search_start),
            2,
        )
        timing["queries_count"] = len(parsed.queries)
        timing["urls_attempted"] = total_attempted
        timing["urls_scraped"] = len(all_scraped_pages)
        timing["good_scrapes"] = len(good_scrapes)
        timing["thin_scrapes"] = len(thin_scrapes)
        timing["failed_scrapes"] = failed_count
        timing["research_depth"] = parsed.research_depth
        if final_truncated:
            timing["final_result_truncated"] = True

        return ToolResult(
            success=True,
            output=final_text,
            child_usages=agent_child_usages,
            started_at=started_at,
            completed_at=time.time(),
            output_self_capped=True,
        )

    except ImportError as exc:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="import",
                message=f"Required module not available: {exc}",
                traceback=traceback.format_exc(),
                suggested_action="Ensure scraper and API management packages are installed.",
            ),
            started_at=started_at,
            completed_at=time.time(),
        )

    except Exception as exc:
        vcprint(
            f"web_research failed: {exc}\n{traceback.format_exc()}",
            "[web_research] Unhandled exception",
            color="red",
        )
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"Web research failed: {exc}",
                traceback=traceback.format_exc(),
                is_retryable=True,
                suggested_action="Try with different queries or reduce research_depth.",
            ),
            started_at=started_at,
            completed_at=time.time(),
        )


# ---------------------------------------------------------------------------
# web — unified action dispatcher (search / read / batch_read)
# ---------------------------------------------------------------------------

# Valid `web` actions are enforced by the WebArgs discriminated union
# (arg_models/web_args.py) + tool_def.parameters."$variants" — the source of truth.


def _web_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "web"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _web_validation_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="web",
        call_id=ctx.call_id,
    )


async def _web_batch_read(args: dict[str, Any], ctx: ToolContext, started_at: float) -> ToolResult:
    """Concurrent fetch of many URLs — paged + whole-result budgeted."""
    urls = args.get("urls") or []
    if not isinstance(urls, list) or not urls:
        return _web_validation_error(
            "urls must be a non-empty list of strings for action=batch_read.",
            started_at,
            ctx,
        )

    offset = max(0, int(args.get("offset", 0) or 0))
    chars = _resolve_read_chars(args, set(args.keys()))
    url_budget = per_url_budget(len(urls))
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "web")

    try:
        from matrx_scraper.features.read_page import read_page_mcp_quick

        await stream.progress(f"Reading {len(urls)} URLs concurrently...")

        async def _one(url: str) -> dict[str, Any]:
            try:
                result = await read_page_mcp_quick(url=url)
                text = extract_page_text(result)
                if isinstance(result, dict) and result.get("status") == "error":
                    return window_page_content(
                        "",
                        url=url,
                        offset=0,
                        chars=chars,
                        success=False,
                        error=text or "Sorry could not access this page.",
                    )
                return window_page_content(
                    text,
                    url=url,
                    offset=offset,
                    chars=chars,
                    per_url_budget=url_budget,
                )
            except Exception as e:
                return window_page_content(
                    "",
                    url=url,
                    offset=0,
                    chars=chars,
                    success=False,
                    error=str(e),
                )

        pages = list(await asyncio.gather(*[_one(u) for u in urls]))
        succeeded = sum(1 for p in pages if p.get("success"))
        await stream.progress(f"Batch read complete: {succeeded}/{len(urls)} succeeded")

        output = enforce_result_budget(
            {
                "pages": pages,
                "count": len(pages),
                "succeeded": succeeded,
                "failed": len(pages) - succeeded,
            },
            budget=RESULT_BUDGET_CHARS,
        )
        return ToolResult(
            success=True,
            output=output,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web",
            call_id=ctx.call_id,
            output_self_capped=True,
        )

    except ImportError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc, error_type="import", message=f"Scraper module not available: {exc}"
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"Batch read failed: {exc}",
                is_retryable=True,
                traceback=traceback.format_exc(),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web",
            call_id=ctx.call_id,
        )


async def web(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    # The executor already validated `args` against WebArgs (the discriminated
    # union) before dispatch; we re-derive the typed variant here so the body is
    # genuinely bound to the per-action contract the drift gate proves against the
    # DB — not an `args.get()` shadow contract.
    try:
        parsed = WebArgs.model_validate(args).root
    except ValidationError as exc:
        # Single shared formatter so the model always sees the same readable
        # "loc: msg" shape, never raw Pydantic vomit.
        from matrx_ai.tools._dispatch_util import format_args_error

        return _web_validation_error(
            f"Invalid web arguments: {format_args_error(exc)}", started_at, ctx
        )

    if isinstance(parsed, WebSearchWire):
        return _web_stamp(
            await web_search(
                {
                    "queries": parsed.queries,
                    "freshness": parsed.freshness,
                    "max_results_per_query": parsed.max_results_per_query,
                },
                ctx,
            ),
            started_at,
            ctx,
        )

    if isinstance(parsed, WebReadWire):
        fields = set(parsed.model_fields_set)
        return _web_stamp(
            await web_read(
                {
                    "urls": [parsed.url],
                    "instructions": parsed.instructions or "",
                    "summarize": parsed.summarize,
                    "offset": parsed.offset,
                    "chars": resolve_chars(
                        chars=parsed.chars,
                        max_content_length=parsed.max_content_length,
                        fields_set=fields,
                    ),
                    "max_content_length": parsed.max_content_length,
                },
                ctx,
            ),
            started_at,
            ctx,
        )

    # WebBatchReadWire — concurrent fetch
    assert isinstance(parsed, WebBatchReadWire)
    fields = set(parsed.model_fields_set)
    return await _web_batch_read(
        {
            "urls": parsed.urls,
            "offset": parsed.offset,
            "chars": resolve_chars(
                chars=parsed.chars,
                max_content_length=parsed.max_content_length,
                fields_set=fields,
            ),
            "max_content_length": parsed.max_content_length,
        },
        ctx,
        started_at,
    )
