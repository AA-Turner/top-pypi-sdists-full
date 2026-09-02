"""Tool descriptors — name + description + JSON Schema + async handler.

Keep this file the single source of truth. Anything that surfaces a tool to a
model — matrx-ai registry, MCP server, OpenAI tools array, Anthropic tools
array — reads from `ALL_TOOLS` (or one of the grouped subsets).

Adding a new tool:
    1. Implement the async handler somewhere in the package.
    2. Add a `ToolSpec(...)` entry below with a tight one-line description and
       a complete JSON Schema for `input_schema`.
    3. Append to the matching group list (BROWSER_TOOLS / SCRAPE_TOOLS).
       It is now exposed everywhere automatically.

Naming convention:
    * `browser_*`  — interactive Playwright primitives.
    * `scraper_*`  — one-shot scrape / parse / preview.

There is deliberately NO `crawl_*` group here. Site crawling is the canonical
`web.*` crawler (`matrx_scraper/web_crawl/`), driven by `api/crawl_router.py`
and the `web.crawl_schedule` dispatcher — never by a host-injected `_ext` seam.
The old `crawl_start`/`crawl_status`/`crawl_pages`/`crawl_cancel` descriptors
addressed the retired `scraper.crawl_runs` world (graveyarded 2026-08-09) and
were deleted with it: they were unregistered in `tool.definition`, no host ever
wired their exts, and every call raised. An agent-facing entry point to the
canonical crawler is a NEW tool over `web.crawl_session`, not a revival of these.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from collections.abc import Awaitable, Callable

from matrx_scraper.ai_browser import actions as _b


HandlerT = Callable[[dict[str, Any]], Awaitable[Any]]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: HandlerT
    group: str = "general"  # 'browser' | 'scrape' | 'crawl'


# ── Adapters: descriptor handlers take a single args dict ────────────────


async def _browser_navigate(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.navigate(
        url=args["url"],
        session_id=args.get("session_id"),
        wait_until=args.get("wait_until", "load"),
        timeout_ms=args.get("timeout_ms", 30_000),
        extract_text=args.get("extract_text", False),
        user_agent=args.get("user_agent"),
        viewport=args.get("viewport"),
        proxy=args.get("proxy"),
    )
    return res.model_dump()


async def _browser_click(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.click(
        session_id=args["session_id"],
        selector=args["selector"],
        wait_after_ms=args.get("wait_after_ms", 0),
        timeout_ms=args.get("timeout_ms", 10_000),
    )
    return res.model_dump()


async def _browser_fill(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.fill(
        session_id=args["session_id"],
        selector=args["selector"],
        value=args["value"],
        timeout_ms=args.get("timeout_ms", 10_000),
    )
    return res.model_dump()


async def _browser_type(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.type_text(
        session_id=args["session_id"],
        selector=args["selector"],
        text=args["text"],
        clear_first=args.get("clear_first", False),
        press_enter=args.get("press_enter", False),
        timeout_ms=args.get("timeout_ms", 10_000),
    )
    return res.model_dump()


async def _browser_select_option(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.select_option(
        session_id=args["session_id"],
        selector=args["selector"],
        value=args.get("value"),
        label=args.get("label"),
        timeout_ms=args.get("timeout_ms", 10_000),
    )
    return res.model_dump()


async def _browser_screenshot(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.screenshot(
        session_id=args["session_id"],
        selector=args.get("selector"),
        full_page=args.get("full_page", False),
        width=args.get("width"),
        height=args.get("height"),
        return_base64=args.get("return_base64", True),
    )
    return res.model_dump()


async def _browser_wait_for(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.wait_for(
        session_id=args["session_id"],
        selector=args.get("selector"),
        text=args.get("text"),
        state=args.get("state", "visible"),
        timeout_ms=args.get("timeout_ms", 10_000),
    )
    return res.model_dump()


async def _browser_get_element(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.get_element(
        session_id=args["session_id"],
        selector=args["selector"],
        include_html=args.get("include_html", False),
    )
    return res.model_dump()


async def _browser_query_selectors(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.query_selectors(
        session_id=args["session_id"],
        selectors=args["selectors"],
        attributes=args.get("attributes"),
        limit_per_selector=args.get("limit_per_selector", 50),
    )
    return res.model_dump()


async def _browser_eval_js(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.eval_js(
        session_id=args["session_id"],
        expression=args["expression"],
        allow_eval_js=args.get("allow_eval_js", False),
    )
    return res.model_dump()


async def _browser_scroll(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.scroll(
        session_id=args["session_id"],
        direction=args.get("direction", "down"),
        pixels=args.get("pixels", 500),
        selector=args.get("selector"),
    )
    return res.model_dump()


async def _browser_get_html(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.get_html(
        session_id=args["session_id"],
        cap=args.get("cap", _b.GET_HTML_CAP),
    )
    return res.model_dump()


async def _browser_get_text(args: dict[str, Any]) -> dict[str, Any]:
    res = await _b.get_text(
        session_id=args["session_id"],
        selector=args.get("selector", "body"),
        cap=args.get("cap", _b.GET_TEXT_CAP),
    )
    return res.model_dump()


async def _browser_close(args: dict[str, Any]) -> dict[str, Any]:
    return await _b.close(session_id=args["session_id"])


# ── Scrape / parse / preview ─────────────────────────────────────────────


async def _scraper_quick_preview(args: dict[str, Any]) -> dict[str, Any]:
    from matrx_scraper.preview import quick_preview

    return await quick_preview(args["url"])


async def _scraper_scrape(args: dict[str, Any]) -> dict[str, Any]:
    from matrx_scraper.orchestrator import scrape

    result = await scrape(args["url"], **{k: v for k, v in args.items() if k != "url"})
    return result.model_dump() if hasattr(result, "model_dump") else dict(result)


async def _scraper_audit_html(args: dict[str, Any]) -> dict[str, Any]:
    """Measurements AND verdicts, bounded.

    A model handed `title_length: 74` guesses at the threshold and gets it
    wrong; every verdict here comes from `seo_audit.PAGE_CHECKS`, the ONE
    implementation. The payload is bounded by construction — the problems in
    full with their reasoning, passes as bare names, and the evidence projected
    through `summarize_audit` (no structured-data blob, no resource inventory,
    no link rows) — because a tool result re-enters the prompt on every loop
    iteration. `html` carries no transport facts, so anything the caller does
    not supply comes back `n_a` rather than a silent pass.
    """
    from matrx_scraper.seo_audit import (
        audit_html,
        build_page_check_digest,
        evidence_from_audit,
        summarize_audit,
    )

    url = args.get("url", "")
    audit = audit_html(args["html"], url)
    http_status = args.get("http_status")
    response_time_ms = args.get("response_time_ms")
    ttfb_ms = args.get("ttfb_ms")
    evidence = evidence_from_audit(
        audit,
        http_status=int(http_status) if isinstance(http_status, int | float) else None,
        response_bytes=len(args["html"].encode("utf-8", "ignore")),
        response_time_ms=(
            int(response_time_ms) if isinstance(response_time_ms, int | float) else None
        ),
        ttfb_ms=int(ttfb_ms) if isinstance(ttfb_ms, int | float) else None,
    )
    return {
        "audit": summarize_audit(audit).model_dump(),
        "checks": build_page_check_digest(evidence).model_dump(),
    }


async def _scraper_parse_html(args: dict[str, Any]) -> dict[str, Any]:
    from matrx_scraper.parser import parse_html

    result = parse_html(args["html"], **{k: v for k, v in args.items() if k != "html"})
    return result.model_dump() if hasattr(result, "model_dump") else dict(result)


# ── Schema helpers ───────────────────────────────────────────────────────


def _obj(
    properties: dict[str, Any], required: list[str] | None = None, additional: bool = False
) -> dict[str, Any]:
    schema: dict[str, Any] = {
        "type": "object",
        "properties": properties,
        "additionalProperties": additional,
    }
    if required:
        schema["required"] = required
    return schema


def _str(desc: str = "", **extra: Any) -> dict[str, Any]:
    return {"type": "string", "description": desc, **extra}


def _int(desc: str = "", **extra: Any) -> dict[str, Any]:
    return {"type": "integer", "description": desc, **extra}


def _bool(desc: str = "", default: bool = False) -> dict[str, Any]:
    return {"type": "boolean", "description": desc, "default": default}


# ── Browser tool specs ───────────────────────────────────────────────────

BROWSER_TOOLS: list[ToolSpec] = [
    ToolSpec(
        name="browser_navigate",
        description="Open or reuse a Playwright session and navigate to a URL. Returns a session_id you must pass to subsequent browser_* tools.",
        input_schema=_obj(
            {
                "url": _str("Absolute URL to load."),
                "session_id": _str("If set, reuse this session instead of opening a new one."),
                "wait_until": {
                    "type": "string",
                    "enum": ["load", "domcontentloaded", "networkidle"],
                    "default": "load",
                },
                "timeout_ms": _int("Navigation timeout in ms.", default=30_000),
                "extract_text": _bool("Return body inner_text in `text_preview`."),
                "user_agent": _str("Override the default user agent."),
                "viewport": {
                    "type": "object",
                    "properties": {"width": _int(), "height": _int()},
                    "additionalProperties": False,
                },
                "proxy": _str("HTTP proxy URL."),
            },
            required=["url"],
        ),
        handler=_browser_navigate,
        group="browser",
    ),
    ToolSpec(
        name="browser_click",
        description="Click an element by CSS selector inside an existing browser session.",
        input_schema=_obj(
            {
                "session_id": _str("Session id from browser_navigate."),
                "selector": _str("CSS selector to click."),
                "wait_after_ms": _int(
                    "Wait this long after click for late-rendered DOM.", default=0
                ),
                "timeout_ms": _int("Click timeout.", default=10_000),
            },
            required=["session_id", "selector"],
        ),
        handler=_browser_click,
        group="browser",
    ),
    ToolSpec(
        name="browser_fill",
        description="Set the value of an input/textarea (replaces existing value).",
        input_schema=_obj(
            {
                "session_id": _str(),
                "selector": _str(),
                "value": _str("Value to set."),
                "timeout_ms": _int(default=10_000),
            },
            required=["session_id", "selector", "value"],
        ),
        handler=_browser_fill,
        group="browser",
    ),
    ToolSpec(
        name="browser_type",
        description="Type text into a focused field. Optionally clear first or press Enter and wait for navigation.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "selector": _str(),
                "text": _str(),
                "clear_first": _bool("Clear before typing."),
                "press_enter": _bool("Press Enter after typing."),
                "timeout_ms": _int(default=10_000),
            },
            required=["session_id", "selector", "text"],
        ),
        handler=_browser_type,
        group="browser",
    ),
    ToolSpec(
        name="browser_select_option",
        description="Choose an option in a <select> by value or visible label.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "selector": _str(),
                "value": _str("Option value attribute. Provide this OR `label`."),
                "label": _str("Option visible text. Provide this OR `value`."),
                "timeout_ms": _int(default=10_000),
            },
            required=["session_id", "selector"],
        ),
        handler=_browser_select_option,
        group="browser",
    ),
    ToolSpec(
        name="browser_screenshot",
        description="Capture a PNG of the page, viewport, or a specific element. Returns base64 by default.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "selector": _str("If set, screenshot just this element."),
                "full_page": _bool("Full-page stitched screenshot."),
                "width": _int("Override viewport width."),
                "height": _int("Override viewport height."),
                "return_base64": _bool("Inline PNG bytes as base64.", default=True),
            },
            required=["session_id"],
        ),
        handler=_browser_screenshot,
        group="browser",
    ),
    ToolSpec(
        name="browser_wait_for",
        description="Wait until a CSS selector or visible text appears (or a state is reached). Essential for SPAs.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "selector": _str("Selector to wait for. Provide this OR `text`."),
                "text": _str("Visible text to wait for."),
                "state": {
                    "type": "string",
                    "enum": ["visible", "attached", "detached", "hidden"],
                    "default": "visible",
                },
                "timeout_ms": _int(default=10_000),
            },
            required=["session_id"],
        ),
        handler=_browser_wait_for,
        group="browser",
    ),
    ToolSpec(
        name="browser_get_element",
        description="Inspect a DOM element — text, attributes, bounding box, optionally HTML. Long fields are capped and carry an inline [truncated: …] marker; truncated/total_chars report the real size.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "selector": _str(),
                "include_html": _bool("Include inner_html and outer_html (capped at 50k chars)."),
            },
            required=["session_id", "selector"],
        ),
        handler=_browser_get_element,
        group="browser",
    ),
    ToolSpec(
        name="browser_query_selectors",
        description="Bulk extraction — pull text + attributes for many CSS selectors in one round-trip. Row text is capped and each selector returns at most limit_per_selector elements; match_counts reports the true match count per selector.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "selectors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Selectors to query.",
                },
                "attributes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Attribute names to capture per element.",
                },
                "limit_per_selector": _int(default=_b.ROW_COUNT_CAP),
            },
            required=["session_id", "selectors"],
        ),
        handler=_browser_query_selectors,
        group="browser",
    ),
    ToolSpec(
        name="browser_eval_js",
        description="Evaluate a JavaScript expression in the page context. Disabled unless `allow_eval_js=true`.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "expression": _str("JS expression returning a JSON-serialisable value."),
                "allow_eval_js": _bool("Required: explicit opt-in to run JS.", default=False),
            },
            required=["session_id", "expression"],
        ),
        handler=_browser_eval_js,
        group="browser",
    ),
    ToolSpec(
        name="browser_scroll",
        description="Scroll page or element. Direction: up/down/top/bottom.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "direction": {
                    "type": "string",
                    "enum": ["up", "down", "top", "bottom"],
                    "default": "down",
                },
                "pixels": _int("Scroll amount when direction is up/down.", default=500),
                "selector": _str("Optional element selector to scroll (default: window)."),
            },
            required=["session_id"],
        ),
        handler=_browser_scroll,
        group="browser",
    ),
    ToolSpec(
        name="browser_get_html",
        description="Return the page's full HTML (post-render, post-recipe). Capped (500k chars by default); when the cap fires the content ends with a [truncated: …] marker and truncated/total_chars say so — raise cap to get more.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "cap": _int(default=_b.GET_HTML_CAP),
            },
            required=["session_id"],
        ),
        handler=_browser_get_html,
        group="browser",
    ),
    ToolSpec(
        name="browser_get_text",
        description="Return inner_text of a selector (default: body). Capped (50k chars by default); when the cap fires the content ends with a [truncated: …] marker and truncated/total_chars say so — raise cap or pass a narrower selector.",
        input_schema=_obj(
            {
                "session_id": _str(),
                "selector": _str(default="body"),
                "cap": _int(default=_b.GET_TEXT_CAP),
            },
            required=["session_id"],
        ),
        handler=_browser_get_text,
        group="browser",
    ),
    ToolSpec(
        name="browser_close",
        description="Close a browser session and free its resources.",
        input_schema=_obj({"session_id": _str()}, required=["session_id"]),
        handler=_browser_close,
        group="browser",
    ),
]


# ── Scrape / parse specs ─────────────────────────────────────────────────

SCRAPE_TOOLS: list[ToolSpec] = [
    ToolSpec(
        name="scraper_quick_preview",
        description="Fetch robots.txt + homepage, run an SEO audit, and grab a desktop screenshot. Sub-5s preview card payload.",
        input_schema=_obj({"url": _str("Site URL — bare host or full URL.")}, required=["url"]),
        handler=_scraper_quick_preview,
        group="scrape",
    ),
    ToolSpec(
        name="scraper_scrape",
        description="One-shot scrape — fetch, parse, and return ScrapeResult (title, text, markdown, links, metadata).",
        input_schema=_obj(
            {
                "url": _str(),
                "render_mode": {
                    "type": "string",
                    "enum": [
                        "http_only",
                        "http_first",
                        "browser_always",
                        "browser_with_screenshot",
                    ],
                    "default": "http_first",
                },
                "include_links": _bool(default=True),
                "include_markdown": _bool(default=True),
            },
            required=["url"],
        ),
        handler=_scraper_scrape,
        group="scrape",
    ),
    ToolSpec(
        name="scraper_audit_html",
        description=(
            "SEO-audit a raw HTML string. Returns the measurements "
            "(title/meta/h1/og/schema/word_count/readability) AND the verdicts: "
            "every failing or warning check with a plain-English reason, passing "
            "checks as names. Checks needing transport facts you do not supply "
            "come back not-applicable."
        ),
        input_schema=_obj(
            {
                "html": _str(),
                "url": _str("Page URL for canonical resolution."),
                "http_status": _int("Final HTTP status, if you fetched this HTML yourself."),
                "response_time_ms": _int("Server response time in ms, if you measured it."),
                "ttfb_ms": _int("True time to first response byte in ms, if measured."),
            },
            required=["html"],
        ),
        handler=_scraper_audit_html,
        group="scrape",
    ),
    ToolSpec(
        name="scraper_parse_html",
        description="Run the 8-stage parser on raw HTML — noise removal, main-content detection, link extraction, hashing, markdownify.",
        input_schema=_obj(
            {
                "html": _str(),
                "url": _str("Page URL for link resolution."),
                "include_markdown": _bool(default=True),
            },
            required=["html"],
        ),
        handler=_scraper_parse_html,
        group="scrape",
    ),
]


ALL_TOOLS: list[ToolSpec] = [*BROWSER_TOOLS, *SCRAPE_TOOLS]
