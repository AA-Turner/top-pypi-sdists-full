from __future__ import annotations

import asyncio
import json
import time
import traceback
from collections.abc import Awaitable, Callable
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
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult, tool_output_text
from matrx_ai.utils.carried_failure import carried_exception
from matrx_ai.tools.output_caps import (
    TOOL_RESULT_ABSOLUTE_CEILING_CHARS,
    TOOL_RESULT_SOFT_CAP_CHARS,
    cap_text,
)
from matrx_ai.tools.streaming import ToolStreamManager

# summarize=true reads the WHOLE page up to this knob (agents.web_read / summarize_max_input_chars),
# not the offset/chars window — see web_read. Re-exported for callers that import it from here.
from matrx_ai.tools.tool_knobs import SUMMARIZE_MAX_INPUT_CHARS  # noqa: F401

_SEARCH_RESULT_CHAR_BUDGET = TOOL_RESULT_SOFT_CAP_CHARS - 1_000

#: Knob (Arman, 2026-09-09: "opinions become knobs"): below this size the raw
#: page is returned instead of paying for a summary that is often larger.
SUMMARIZE_MIN_INPUT_CHARS = 4_000
#: The knob address — ``platform.feature_knob`` seeded by aidream
#: ``db/migrations/ai_096`` with the value above, overridable per ORGANIZATION.
#: The constant is only the standalone (no-host) posture.
SUMMARIZE_MIN_INPUT_CHARS_KNOB = ("agents.web_read", "summarize_min_input_chars")

#: ``async (organization_id) -> int``.
SummarizeMinInputCharsResolver = Callable[[str | None], Awaitable[int]]

_SUMMARIZE_MIN_RESOLVER: SummarizeMinInputCharsResolver | None = None


def set_summarize_min_input_chars_resolver(
    resolver: SummarizeMinInputCharsResolver | None,
) -> None:
    """Install the host's per-organization knob reader (``None`` = standalone)."""
    global _SUMMARIZE_MIN_RESOLVER
    _SUMMARIZE_MIN_RESOLVER = resolver


async def summarize_min_input_chars(organization_id: str | None) -> int:
    """Below this many page chars ``web_read`` returns the page raw instead of
    summarizing it — this organization's value. A resolver failure (e.g. the
    host's ``KnobNotRegisteredError``) is announced in red; the page read never
    fails over it."""
    resolver = _SUMMARIZE_MIN_RESOLVER
    if resolver is None:
        return SUMMARIZE_MIN_INPUT_CHARS
    try:
        return int(await resolver(organization_id))
    except Exception as exc:  # noqa: BLE001 — one failure shape, said out loud
        vcprint(
            f"[web_read] {SUMMARIZE_MIN_INPUT_CHARS_KNOB[0]}/{SUMMARIZE_MIN_INPUT_CHARS_KNOB[1]} "
            f"could not be resolved for organization {organization_id!r} "
            f"({type(exc).__name__}: {exc}); using {SUMMARIZE_MIN_INPUT_CHARS:,}. Fix the "
            "knob row or the host resolver.",
            color="red",
        )
        return SUMMARIZE_MIN_INPUT_CHARS


#: research_web's size knobs (feature ``agents.research_web``), org-overridable; the package
#: defaults (``matrx_scraper.features.research_budget``) are only the standalone posture.
RESEARCH_WEB_KNOB_FEATURE = "agents.research_web"
RESEARCH_WEB_KNOB_KEYS = (
    "page_max_chars",
    "condense_max_chars",
    "listings_max_chars",
    "fallback_max_chars",
    "page_floor_chars",
    "listings_detail",
    "page_char_counts",
)
#: Knob keys that may be 0 (off); every other research_web knob is at least 1.
_RESEARCH_WEB_ZERO_OK = frozenset({"listings_detail", "page_char_counts"})

#: ``async (organization_id) -> {knob key: int}``.
_RESEARCH_BUDGETS_RESOLVER: Callable[[str | None], Awaitable[dict[str, int]]] | None = None


def set_research_budgets_resolver(
    resolver: Callable[[str | None], Awaitable[dict[str, int]]] | None,
) -> None:
    """Install the host's per-organization research_web size knob reader (``None`` = standalone)."""
    global _RESEARCH_BUDGETS_RESOLVER
    _RESEARCH_BUDGETS_RESOLVER = resolver


async def research_budgets(organization_id: str | None) -> Any:
    """This organization's research_web budgets. A resolver failure is announced in red and the
    package defaults hold; the research never fails over it."""
    from matrx_scraper.features.research_budget import Budgets

    budgets = Budgets()
    resolver = _RESEARCH_BUDGETS_RESOLVER
    if resolver is None:
        return budgets
    try:
        got = await resolver(organization_id) or {}
        for key in RESEARCH_WEB_KNOB_KEYS:
            if got.get(key) is not None:
                setattr(budgets, key, max(0 if key in _RESEARCH_WEB_ZERO_OK else 1, int(got[key])))
    except Exception as exc:  # noqa: BLE001 — one failure shape, said out loud
        vcprint(
            f"[research_web] {RESEARCH_WEB_KNOB_FEATURE} knobs could not be resolved for organization "
            f"{organization_id!r} ({type(exc).__name__}: {exc}); using the package defaults. Fix the "
            "knob rows or the host resolver.",
            color="red",
        )
    return budgets


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
    from matrx_ai.tools.arg_models.web_args import MAX_SEARCH_QUERIES, one_query_is_a_list

    queries = one_query_is_a_list(args.get("queries"))
    skipped: list[str] = []
    if isinstance(queries, list) and len(queries) > MAX_SEARCH_QUERIES:
        # Run the first five and say which were not run, instead of refusing the whole search.
        skipped = [str(q) for q in queries[MAX_SEARCH_QUERIES:]]
        args = {**args, "queries": queries[:MAX_SEARCH_QUERIES]}
    parsed = WebSearchArgs(**args)
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "web_search")

    try:
        from matrx_scraper.features.quick_search import (
            search_web_mcp_quick,
        )

        all_text_results: list[str] = []
        site_icons: dict[str, str] = {}
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
                for url, icon in (results.get("site_icons") or {}).items():
                    site_icons.setdefault(url, icon)

        combined_text = "\n\n".join(all_text_results)

        if not combined_text.strip():
            return ToolResult(
                success=False,
                error=ToolError(
                    reported_failure="the web search provider",
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
        if skipped:
            capped += (
                f"\n\n[Not searched: one search runs at most {MAX_SEARCH_QUERIES} queries, so these "
                f"{len(skipped)} were skipped: {json.dumps(skipped)}. Search them in another call if you need them.]"
            )

        return ToolResult(
            success=True,
            output=capped,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web_search",
            call_id=ctx.call_id,
            output_self_capped=True,
            site_icons=site_icons or None,
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


def _stamp_read_engine(result: Any, page: dict[str, Any]) -> dict[str, Any]:
    """Carry the reader's announcement onto the tool page: which engine answered (``advanced_read``
    when the organization's advanced fallback opened a page our scraper could not) and what it said."""
    if isinstance(result, dict):
        if result.get("provenance"):
            page["engine"] = result.get("engine")
            page["provenance"] = result["provenance"]
        if result.get("advanced_read"):
            page["engine"] = result.get("engine") or page.get("engine")
            page["advanced_read"] = result["advanced_read"]
        if result.get("notice"):
            page["notice"] = result["notice"]
    return page


def _failed_page(result: Any, text: str, *, url: str, chars: int) -> dict[str, Any]:
    """A page our reader could not open: the honest error plus, when the read was judged, the
    ``verdict`` and the ``coverage`` (which readers could get it, speed, points) — the UI's
    "Try advanced reader" button and the agent hint both read these."""
    page = window_page_content("", url=url, offset=0, chars=chars, success=False,
                               error=text or "Sorry could not access this page.")
    if isinstance(result, dict):
        for key in ("verdict", "coverage", "advanced_read"):
            if result.get(key):
                page[key] = result[key]
    return page


def coverage_hint(pages: list[dict[str, Any]]) -> str | None:
    """ONE line for the model when failed pages are covered by a paid reader (``None`` otherwise)."""
    try:
        from matrx_scraper.coverage import hint_line
    except ImportError:  # pragma: no cover - matrx_scraper is how these tools read at all
        return None
    return hint_line([(str(p.get("url") or ""), p.get("coverage") or []) for p in pages
                      if not p.get("success") and not (p.get("advanced_read") or {}).get("ok")])


def all_pages_failed(
    pages: list[dict[str, Any]], output: Any, *, tool_name: str, started_at: float, ctx: ToolContext
) -> ToolResult | None:
    """A read where EVERY page failed is a failed call naming each page's reason (``None`` otherwise).

    Work that produced nothing is never success (agent-tools VISION, "Research tool results"); the
    pages stay on ``output`` so the verdict/coverage facts still reach the model and the UI."""
    if not pages or any(p.get("success") for p in pages):
        return None
    reasons = "; ".join(
        f"{p.get('url') or '(no url)'}: {p.get('error') or 'the reader gave no reason'}" for p in pages
    )
    return ToolResult(
        success=False,
        output=output,
        error=ToolError.declared(
            "all_pages_failed",
            f"None of the {len(pages)} page{'s' if len(pages) != 1 else ''} could be read. {reasons}",
            reported_failure="the page reader",
            suggested_action="Try other sources, or the advanced reader when the hint names one.",
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=ctx.call_id,
        output_self_capped=True,
    )


def _with_hint(result: ToolResult, pages: list[dict[str, Any]]) -> ToolResult:
    line = coverage_hint(pages)
    if line:
        result.model_notices.append(line)
    return result


async def land_agent_read(result: Any, ctx: ToolContext, page: dict[str, Any]) -> dict[str, Any]:
    """Land one page an agent read as a Source and stamp the tool's page dict (SOURCE-CONVERGENCE §4.5).

    In-process, through ``matrx_scraper``'s injected landing hook (aidream wires ``land_source``):
    ``origin_client='agent'``, unkept (so intelligence follows the kind's policy — ``on_signal``
    defers it until someone keeps it), not published to the web — the run's person owns it and a
    colleague reaches it only through a conveying association. The page dict gains
    ``processed_document_id`` (``None`` when it did not land) and ``notices`` saying why.
    A host with no landing hook at all is announced on the result and in the log — the read still
    answers, the gap never goes quiet.
    """
    if not (isinstance(result, dict) and result.get("status") == "success" and result.get("page")):
        return page
    try:
        from matrx_scraper.source_landing import (
            SourceLandingNotConfigured,
            land_page_result,
            stamp_page,
        )
    except ImportError:  # pragma: no cover — matrx_scraper is how this tool reads at all
        return page
    try:
        outcome = await land_page_result(
            result["page"],
            organization_id=str(ctx.organization_id or "") or None,
            user_id=str(ctx.user_id or "") or None,
            origin_client="agent",
            keep=False,
        )
    except SourceLandingNotConfigured as exc:
        vcprint(f"[web_read] {exc}", color="red")
        outcome = {
            "processed_document_id": None,
            "source_id": None,
            "notices": [
                {
                    "code": "landing_not_configured",
                    "message": "This page was read but not saved as a Source: this server has no landing door wired.",
                    "remedy": "wire_matrx_scraper_source_landing_at_startup",
                }
            ],
        }
    return stamp_page(page, outcome)


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
        # Full page text per URL, kept for summarize=true. The summarizer used
        # to be fed the offset/chars WINDOW, so it compressed the same slice a
        # raw read returns and could never spare a paging call (measured
        # 2026-09-09: an agent re-read one pricing page three times because
        # 87% of it never reached the summarizer). It now reads the whole page,
        # capped at SUMMARIZE_MAX_INPUT_CHARS and honest about the cut.
        full_texts: list[tuple[str, str, bool]] = []  # (url, text, truncated)
        summarize_cap = SUMMARIZE_MAX_INPUT_CHARS
        if parsed.summarize and parsed.instructions:
            from matrx_ai.tools.tool_knobs import tool_knob_int

            summarize_cap = await tool_knob_int(
                "summarize_max_input_chars", SUMMARIZE_MAX_INPUT_CHARS, ctx.organization_id
            )
        for url in parsed.urls:
            await stream.progress(f"Reading: {url[:60]}...")
            result = await read_page_mcp_quick(url=url)
            text = extract_page_text(result)
            if not (isinstance(result, dict) and result.get("status") == "error"):
                full_texts.append(
                    (url, text[:summarize_cap], len(text) > summarize_cap)
                )
            if isinstance(result, dict) and result.get("status") == "error":
                pages.append(_failed_page(result, text, url=url, chars=chars))
                continue
            pages.append(
                _stamp_read_engine(
                    result,
                    await land_agent_read(
                        result,
                        ctx,
                        window_page_content(
                            text,
                            url=url,
                            offset=offset,
                            chars=chars,
                            per_url_budget=url_budget,
                        ),
                    ),
                )
            )

        total_full_chars = sum(len(t) for _, t, _ in full_texts)
        summarize_floor = (
            await summarize_min_input_chars(ctx.organization_id)
            if parsed.summarize and parsed.instructions and full_texts
            else SUMMARIZE_MIN_INPUT_CHARS
        )
        if (
            parsed.summarize
            and parsed.instructions
            and full_texts
            and total_full_chars < summarize_floor
        ):
            # Knob: a page this small is cheaper to read raw than to pay an
            # LLM call for — and measured summaries of dense content came back
            # LARGER than the source. Return the raw page and say why.
            for p in pages:
                p["summarize_skipped"] = (
                    f"Page is {total_full_chars:,} chars (under "
                    f"{summarize_floor:,}); returned raw instead of summarizing."
                )
        elif parsed.summarize and parsed.instructions and full_texts:
            await stream.step("summarize", "Summarizing page content...")
            from matrx_ai.tools.implementations._summarize_helper import (
                SUMMARIZE_FAILURE_PREFIX,
                summarize_content,
            )

            # Summarize the FULL page text (not the offset/chars window).
            combined = "\n\n---\n\n".join(
                f"URL: {u}\n{t}"
                + (
                    f"\n\n[Source truncated at {summarize_cap:,} characters — "
                    "facts beyond this point are NOT in this content; say so if asked about them.]"
                    if cut
                    else ""
                )
                for u, t, cut in full_texts
            )
            summary, child_usages = await summarize_content(
                content=combined,
                instructions=parsed.instructions,
                ctx=ctx,
            )
            if summary.startswith(SUMMARIZE_FAILURE_PREFIX):
                # Nothing fails silently: a failed summarization is a FAILED
                # tool call, not a successful result whose text happens to be
                # an apology. The model must see the error and the remedy.
                return ToolResult(
                    success=False,
                    error=ToolError.declared(
                        "execution",
                        summary,
                        exc=carried_exception(summary),
                        reported_failure="the summarize_content agent",
                        is_retryable=True,
                        suggested_action=(
                            "Re-read the page with summarize=false (raw text, "
                            "paged with offset/chars) — the page itself was "
                            "fetched fine; only the summarization step failed."
                        ),
                    ),
                    child_usages=child_usages,
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name="web_read",
                    call_id=ctx.call_id,
                )
            capped_summary, info = cap_text(summary, limit=_SEARCH_RESULT_CHAR_BUDGET)
            if info.truncated:
                capped_summary += (
                    f"\n\n[Summary shortened from {info.total_chars:,} to "
                    f"{info.shown_chars:,} characters.]"
                )
            return _with_hint(ToolResult(
                success=True,
                output=capped_summary,
                child_usages=child_usages,
                started_at=started_at,
                completed_at=time.time(),
                tool_name="web_read",
                call_id=ctx.call_id,
                output_self_capped=True,
            ), pages)

        output = enforce_result_budget(
            {
                "pages": pages,
                "count": len(pages),
                "succeeded": sum(1 for p in pages if p.get("success")),
                "failed": sum(1 for p in pages if not p.get("success")),
            },
            budget=RESULT_BUDGET_CHARS,
        )
        failed = all_pages_failed(pages, output, tool_name="web_read", started_at=started_at, ctx=ctx)
        if failed is not None:
            return _with_hint(failed, pages)
        return _with_hint(ToolResult(
            success=True,
            output=output,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web_read",
            call_id=ctx.call_id,
            output_self_capped=True,
        ), pages)

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


def _sources_text(read_failures: list[dict[str, Any]]) -> str:
    """The sources block for a run that read nothing: what failed to load and why, appended to the plain error."""
    from matrx_scraper.features.research_budget import sources_block, unique_failed

    return "\n\n" + sources_block([], unique_failed([(f.get("url") or "", _failure_reason(f)) for f in read_failures]))


def _failure_reason(failure: dict[str, Any]) -> str:
    verdict = failure.get("verdict") or {}
    return str(verdict.get("detail") or verdict.get("reason") or "the page could not be read")


RESEARCH_NEXT_STEPS = (
    "Each report covers its group's queries. Every page in run.pages names how to read its full text; "
    "a listing marked 'not read: search snippet only' was never opened, so never cite it as read. "
    "If gaps remain, read pages with web action='read' or run research_web with narrower queries."
)


#: research_web's declared result: what :func:`research_output` returns, as the stored
#: ``tool.definition.output_schema`` must say. The rebuild changed the result from one markdown string
#: to ``{run, reports, listings}``, the stored schema kept saying ``string``, and every successful
#: call filed a ToolOutputContractDrift (2026-11-17). The live row is written from THIS constant;
#: ``tests/test_research_web_rebuild.py`` proves every outcome (success, partial, failed) fits it.
RESEARCH_WEB_OUTPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": (
        "Research run: run facts (status, queries, groups, pages read and how to read each in full, "
        "scrape failures, budgets, timing, next steps), one condensed report per query group "
        "(or its failure reason and fallback page text), and the search listings."
    ),
    "required": ["run", "reports", "listings", "sources"],
    "properties": {
        "run": {
            "type": "object",
            "required": ["status", "partial", "queries", "research_depth", "groups", "pages"],
            "properties": {
                "status": {"type": "string", "enum": ["success", "partial", "failed"]},
                "partial": {"type": "boolean"},
                "queries": {"type": "array", "items": {"type": "string"}},
                "research_depth": {"type": "string"},
                "results_per_query": {"type": "object", "additionalProperties": {"type": "integer"}},
                "groups": {"type": "array", "items": {"type": "object"}},
                "pages": {"type": "array", "items": {"type": "object"}},
                "scrape_failures": {"type": "array", "items": {"type": "object"}},
                "budgets": {"type": "object"},
                "timing": {"type": "object"},
                "next_steps": {"type": "string"},
                "listings_trimmed": {"type": "object"},
            },
        },
        "reports": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["group", "queries", "status"],
                "properties": {
                    "group": {"type": "integer"},
                    "queries": {"type": "array", "items": {"type": "string"}},
                    "status": {"type": "string", "enum": ["reported", "failed"]},
                    "report": {"type": "string"},
                    "reason": {"type": "string"},
                    "citations": {
                        "type": "object",
                        "description": "Plain counts: how many distinct pages read in this run the report cites, and how many pages were read. 0 cited means the report opens with an uncited notice.",
                        "properties": {
                            "read_pages_cited": {"type": "integer"},
                            "pages_read": {"type": "integer"},
                        },
                    },
                    "fallback_pages": {"type": "array", "items": {"type": "object"}},
                },
            },
        },
        "listings": {"type": "array", "items": {"type": "object"}},
        "sources": {"type": "string"},
    },
}


def research_output(
    *,
    queries: list[str],
    research_depth: str,
    groups: list[Any],
    page_plans: list[Any],
    outcomes: list[Any],
    listings: list[dict[str, Any]],
    read_failures: list[dict[str, Any]],
    budgets: Any,
    timing: dict[str, Any],
    result_limit: int,
    instructions: str = "",
) -> tuple[dict[str, Any], list[Any], str]:
    """research_web's result — ``(output, child_usages, outcome)``, outcome ``success|partial|failed``.

    ``run`` and ``reports`` are never cut. A failed group says its real reason and carries its
    top-ranked page text (``budgets.fallback_max_chars``). When the whole result is over
    ``result_limit`` the listings — and only the listings — are trimmed, lowest rank first.
    """
    from matrx_scraper.features.research_budget import (
        citation_notice,
        compact_listings,
        fallback_pages,
        is_vendor_source,
        listings_chars,
        sources_block,
        trim_listings,
        unique_failed,
        verify_report,
    )

    counts = bool(budgets.page_char_counts)
    terms_text = " ".join([*queries, instructions])
    # Pages this run actually read (a duplicate copy was read too); the ones that failed to load.
    run_read = [p.url for p in page_plans if not p.dropped or p.dropped == "duplicate"]
    failed_sources = [(f.get("url") or "", _failure_reason(f)) for f in read_failures]

    reports: list[dict[str, Any]] = []
    group_records: list[dict[str, Any]] = []
    child_usages: list[Any] = []
    for group, outcome in zip(groups, outcomes, strict=True):
        record = group.record(counts=counts)
        entry: dict[str, Any] = {"group": group.index, "queries": group.queries}
        reason: str | None = None
        if isinstance(outcome, BaseException):
            reason = f"{type(outcome).__name__}: {outcome}"
        elif outcome is None:
            reason = "nothing to condense: no pages and no search listings for these queries"
        else:
            child_usages.extend(getattr(outcome, "usage_history", None) or [])
            text = getattr(outcome, "output", "") or ""
            if getattr(outcome, "success", False) and text.strip():
                # Every citation an inline URL, checked against the pages this run read (lane D, 2026-11-17).
                checked, citation_check = verify_report(
                    text,
                    read_pages=group.pages,
                    terms_text=terms_text,
                    run_read_urls=run_read,
                )
                record["citation_check"] = citation_check
                # A report citing none of the pages read says so at its top, and a consumer can test the field.
                coverage = citation_check["coverage"]
                notice = citation_notice(coverage)
                entry.update(status="reported", report=f"{notice}\n\n{checked}" if notice else checked, citations=coverage)
            else:
                reason = getattr(outcome, "error", None) or "the condenser returned no report text"
        if reason is not None:
            fallback = fallback_pages(group, budgets.fallback_max_chars)
            entry.update(status="failed", reason=reason, fallback_pages=fallback)
            record["condenser"] = "failed"
            record["reason"] = reason
        else:
            record["condenser"] = "reported"
        reports.append(entry)
        group_records.append(record)

    reported = sum(1 for r in reports if r["status"] == "reported")
    fallback_count = sum(len(r.get("fallback_pages") or []) for r in reports)
    if reported == len(reports) and reports:
        outcome_name = "success"
    elif reported or fallback_count:
        outcome_name = "partial"
    else:
        outcome_name = "failed"

    query_results = {e["query"]: e["result_count"] for e in listings}
    run: dict[str, Any] = {
        "status": outcome_name,
        "partial": outcome_name == "partial",
        "queries": queries,
        "research_depth": research_depth,
        "results_per_query": {q: query_results.get(q, 0) for q in queries},
        "groups": group_records,
        "pages": [
            {**p.record(counts=counts), **({"vendor_authored": True} if is_vendor_source(p.url, terms_text) else {})}
            for p in sorted(page_plans, key=lambda p: (p.group, p.rank or 999))
        ],
        "scrape_failures": [
            {"url": f.get("url"), "reason": _failure_reason(f)}
            for f in read_failures
        ],
        "budgets": budgets.record(),
        "timing": timing,
        "next_steps": RESEARCH_NEXT_STEPS,
        "listings_detail": {0: "none", 1: "compact", 2: "full"}.get(budgets.listings_detail, "full"),
    }
    # The result's listings: none, compact (rank, title, link, read label) or full, per the knob.
    full_listings = listings
    listings = [] if budgets.listings_detail <= 0 else full_listings if budgets.listings_detail >= 2 else compact_listings(full_listings)
    # The sources block is stated ONCE per tool result, on every outcome (reported, fallback or failed).
    output: dict[str, Any] = {
        "run": run,
        "reports": reports,
        "listings": listings,
        "sources": sources_block(
            [(p.url, is_vendor_source(p.url, terms_text), p.unsure) for p in page_plans if not p.dropped],
            unique_failed(failed_sources),
        ),
    }
    total = len(tool_output_text(output)[0])
    if total >= result_limit:
        all_results = sum(len(e["results"]) for e in listings)
        # The note is part of the result: it is written BEFORE the room is measured, at its widest
        # value, so adding it can never push a trimmed result back over the limit (it did, by 155
        # characters, on 2026-11-17: a 50,155-character result against the 50,000 limit).
        run["listings_trimmed"] = {
            "results_removed": all_results,
            "why": f"the result was {total:,} characters (limit {result_limit:,}); listings go first",
        }
        fixed = len(tool_output_text(output)[0]) - len(tool_output_text(listings)[0])
        room = max(result_limit - 1 - fixed, 0)
        trimmed, removed = trim_listings(listings, room)
        output["listings"] = trimmed
        # Judged on the WHOLE result as it will be measured, never on the listings alone.
        while removed < all_results and len(tool_output_text(output)[0]) >= result_limit:
            trimmed, removed = trim_listings(listings, max(listings_chars(trimmed) - 2_000, 0))
            output["listings"] = trimmed
        run["listings_trimmed"]["results_removed"] = removed
    return output, child_usages, outcome_name


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
        from matrx_scraper.features.mcp_tool_helpers import (
            scrape_urls_from_search_result,
        )
        from matrx_scraper.features.research_budget import build_listings, plan_groups
        from matrx_scraper.search.search import brave_failure_reason

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
        #: Pages judged failed (bot wall, HTTP error, empty, JS shell, sign-in wall) with their coverage.
        read_failures: list[dict[str, Any]] = []
        scraping_tasks: list[tuple[str, asyncio.Task[list[dict[str, Any]]]]] = []
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
                    failures=read_failures,
                )
            )
            scraping_tasks.append((query, scraping_task))

        if not queries_with_results:
            return ToolResult(
                success=False,
                error=ToolError(
                    reported_failure="the web search provider",
                    error_type="execution",
                    # The search helper returns None on failure; name its recorded cause, never just "failed".
                    message="All search queries failed to return results."
                    + "".join(
                        f" {q!r}: {why}."
                        for q in parsed.queries
                        if (why := brave_failure_reason(q))
                    ),
                    is_retryable=True,
                    suggested_action="Try different search queries or check network connectivity.",
                ),
                started_at=started_at,
                completed_at=time.time(),
            )

        # ------------------------------------------------------------------
        # Phase 2: Wait for all scraping to complete
        # ------------------------------------------------------------------
        all_scraped_results = await asyncio.gather(*(task for _, task in scraping_tasks))
        all_scraped_pages = [
            {**page, "query": query}
            for (query, _), result in zip(scraping_tasks, all_scraped_results, strict=True)
            for page in result
        ]

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
                    reported_failure="the web search provider",
                    error_type="execution",
                    message=(
                        f"Research produced zero evidence: {len(parsed.queries)} "
                        f"queries returned no usable search results and no pages were "
                        f"scraped. Refusing to synthesize a report from an empty corpus."
                        + _sources_text(read_failures)
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
        failed_count = len(seen_urls) - len(all_scraped_pages)
        await stream.step(
            "scraping_complete",
            f"Scraped {len(all_scraped_pages)} pages ({len(good_scrapes)} good, {len(thin_scrapes)} thin, {failed_count} failed)",
        )

        # ------------------------------------------------------------------
        # Phase 3: Plan every group's condenser input (pure: research_budget)
        # ------------------------------------------------------------------
        budgets = await research_budgets(ctx.organization_id)
        # A per-call ask beats the organization knob; a caller that needs full listings asks for them here.
        if parsed.listings is not None:
            budgets.listings_detail = {"none": 0, "compact": 1, "full": 2}[parsed.listings]
        if parsed.page_char_counts is not None:
            budgets.page_char_counts = int(parsed.page_char_counts)
        # Search order is the caller's query order, so "the first query that found a page" is stable.
        order = {q: i for i, q in enumerate(parsed.queries)}
        queries_with_results.sort(key=lambda qr: order.get(qr[0], len(order)))
        listings = build_listings(queries_with_results, {p.get("url") or "" for p in all_scraped_pages})
        groups, page_plans = plan_groups(
            queries=list(parsed.queries),
            instructions=parsed.instructions,
            listings=listings,
            pages=all_scraped_pages,
            budgets=budgets,
            max_pages_per_query=target_good_per_query,
        )
        # The writer is told, in its own input, which pages failed to load (run facts), so it cannot attribute to them.
        for group in groups:
            group.failed_sources = [(f.get("url") or "", _failure_reason(f)) for f in read_failures]

        # ------------------------------------------------------------------
        # Phase 4: Condense every group concurrently
        # ------------------------------------------------------------------
        await stream.step(
            "condensing",
            f"Condensing {len(groups)} report{'s' if len(groups) != 1 else ''} from the scraped pages",
        )
        from matrx_ai.agent_runners.research import scrape_research_condenser_agent_1

        async def _condense(group: Any) -> Any:
            if not any(not p.dropped for p in group.pages) and not group.listings:
                return None
            return await scrape_research_condenser_agent_1(
                instructions=parsed.instructions,
                scraped_content=group.scraped_content(),
                queries=", ".join(group.queries),
                search_results=group.search_results(),
                ctx=ctx,
            )

        condense_start = time.perf_counter()
        outcomes = await asyncio.gather(*(_condense(g) for g in groups), return_exceptions=True)
        timing["condensation_time"] = round(time.perf_counter() - condense_start, 2)
        timing["urls_attempted"] = len(seen_urls)
        timing["urls_scraped"] = len(all_scraped_pages)
        timing["good_scrapes"] = len(good_scrapes)
        timing["thin_scrapes"] = len(thin_scrapes)
        timing["failed_scrapes"] = failed_count
        timing["total_execution_time"] = round(time.time() - started_at, 2)

        output, child_usages, outcome = research_output(
            queries=list(parsed.queries),
            research_depth=parsed.research_depth,
            groups=groups,
            page_plans=page_plans,
            outcomes=list(outcomes),
            listings=listings,
            read_failures=read_failures,
            budgets=budgets,
            timing=timing,
            result_limit=TOOL_RESULT_SOFT_CAP_CHARS,
            instructions=parsed.instructions,
        )

        from matrx_scraper.search.search import site_icons_from_search_results

        coverage = [{"url": f["url"], "success": False, "coverage": f.get("coverage") or [],
                     "advanced_read": f.get("advanced_read")} for f in read_failures]
        if outcome == "failed":
            return _with_hint(ToolResult(
                success=False,
                error=ToolError.declared(
                    "execution",
                    "Every research report failed and no page text could be delivered: "
                    + "; ".join(
                        f"group {g['group']}: {g.get('reason') or g['condenser']}" for g in output["run"]["groups"]
                    )
                    + "\n\n" + output["sources"],
                    exc=carried_exception(str(output["run"]["groups"])),
                    reported_failure="the research condenser",
                    is_retryable=True,
                    suggested_action="Read the listed URLs with web action='read', or retry with fewer queries.",
                ),
                child_usages=child_usages,
                started_at=started_at,
                completed_at=time.time(),
            ), coverage)
        serialized = len(tool_output_text(output)[0])
        return _with_hint(ToolResult(
            success=True,
            output=output,
            child_usages=child_usages,
            started_at=started_at,
            completed_at=time.time(),
            output_self_capped=True,
            # run + reports always arrive whole: past the absolute ceiling this result authorizes itself.
            approved_max_chars=serialized if serialized > TOOL_RESULT_ABSOLUTE_CEILING_CHARS else None,
            site_icons=site_icons_from_search_results(queries_with_results) or None,
        ), coverage)

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


def _web_validation_error(message: str, started_at: float, ctx: ToolContext, *, exc: BaseException | None = None) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError.declared("validation", message, exc=exc),
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
                    return _failed_page(result, text, url=url, chars=chars)
                return _stamp_read_engine(
                    result,
                    await land_agent_read(
                        result,
                        ctx,
                        window_page_content(
                            text,
                            url=url,
                            offset=offset,
                            chars=chars,
                            per_url_budget=url_budget,
                        ),
                    ),
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
        failed = all_pages_failed(pages, output, tool_name="web", started_at=started_at, ctx=ctx)
        if failed is not None:
            return _with_hint(failed, pages)
        return _with_hint(ToolResult(
            success=True,
            output=output,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="web",
            call_id=ctx.call_id,
            output_self_capped=True,
        ), pages)

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
        , exc=exc)

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
