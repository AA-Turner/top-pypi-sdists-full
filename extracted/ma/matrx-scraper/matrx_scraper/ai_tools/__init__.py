"""Tool descriptor registry — every AI-callable surface the scraper exposes.

The descriptor is the universal contract. Same JSON Schema flows into:

  * matrx-ai's `ToolRegistry` (server-implemented tools).
  * The MCP server (one descriptor → one MCP tool).
  * Direct OpenAI / Anthropic tool definitions (no glue needed).

Each `ToolSpec` holds:

    name        — wire name (snake_case, lowercase).
    description — one sentence; this is what the model reads.
    input_schema — JSON Schema, validated by Pydantic on the way in.
    handler     — async callable (args: dict) -> JSON-serialisable result.

The set is grouped:

    BROWSER_TOOLS  — the 14 browser primitives in `ai_browser.actions`.
    SCRAPE_TOOLS   — quick_preview, scrape, parse_html, audit_html.

Site crawling is NOT here — it is the canonical `web.*` crawler
(`matrx_scraper/web_crawl/`), reached over HTTP via `api/crawl_router.py`.

Hosts compose any subset:

    from matrx_scraper.ai_tools import ALL_TOOLS, BROWSER_TOOLS
    for spec in BROWSER_TOOLS:
        registry.register(spec.name, spec.input_schema, spec.handler)
"""

from __future__ import annotations

from matrx_scraper.ai_tools.specs import (
    ToolSpec,
    BROWSER_TOOLS,
    SCRAPE_TOOLS,
    ALL_TOOLS,
)

__all__ = [
    "ToolSpec",
    "BROWSER_TOOLS",
    "SCRAPE_TOOLS",
    "ALL_TOOLS",
]
