"""Model Context Protocol (MCP) server for the matrx-scraper toolset.

Exposes everything in `matrx_scraper.ai_tools.ALL_TOOLS` over the standard MCP
transport so any MCP-compatible client (Claude Desktop, the matrx-ai
`ExternalMCPClient`, third-party agents, the cursor/zed/vs code MCP plugins)
can call our scraper, parser, browser primitives, and crawler.

**stdio is the ONLY transport.** Run via:

    python -m matrx_scraper.mcp           # auto-detects stdio
    python -m matrx_scraper.mcp --stdio

There is deliberately no network transport: it would hand a JS-executing
browser and all 22 tools to any caller who can reach the port. A network
caller uses the authenticated FastAPI microservice
(`python -m matrx_scraper.server`) instead.

The server itself is a thin adapter — every tool maps 1:1 to a `ToolSpec`. We
do NOT redefine schemas here; we read them from the registry. This keeps a
single source of truth: add a tool to `ai_tools.specs.ALL_TOOLS`, and it shows
up automatically over MCP.
"""

from __future__ import annotations

from matrx_scraper.mcp.server import (
    build_server,
    run_stdio,
    main,
)

__all__ = [
    "build_server",
    "run_stdio",
    "main",
]
