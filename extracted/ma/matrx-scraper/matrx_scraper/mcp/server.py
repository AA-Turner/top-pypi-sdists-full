"""MCP server implementation — adapts `ai_tools.ALL_TOOLS` to MCP stdio.

Uses the official `mcp` Python SDK when present (`pip install mcp`). Falls
back to a minimal JSON-RPC-over-stdio loop so the server still works in
environments that don't have the SDK installed yet.

**stdio is the ONLY transport.** A network transport here would expose a
JS-executing browser and 22 tools to whoever can reach the port; the package's
authenticated network surface is the FastAPI microservice
(`python -m matrx_scraper.server`), which is where a network caller belongs.
Do not re-add an HTTP adapter to this module.

The adapter contract is one line: every `ToolSpec` becomes one MCP tool with
the same name, description, and JSON Schema input. Result values are returned
as a single text content block carrying the JSON-encoded result.

Run:
    python -m matrx_scraper.mcp                # stdio (default)
    python -m matrx_scraper.mcp --stdio
    python -m matrx_scraper.mcp --list         # print registered tools and exit
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from typing import Any

from matrx_scraper.ai_tools import ALL_TOOLS, ToolSpec

logger = logging.getLogger(__name__)


# ── SDK detection ────────────────────────────────────────────────────────


def _try_import_mcp() -> Any:
    try:
        import mcp  # noqa: F401
        from mcp.server import Server  # type: ignore
        from mcp.server.stdio import stdio_server  # type: ignore

        return {"Server": Server, "stdio_server": stdio_server}
    except Exception:
        return None


# ── Generic-shape server (works with the `mcp` SDK) ──────────────────────


def build_server(tools: list[ToolSpec] | None = None) -> Any:
    """Build an `mcp.server.Server` instance with our tool set registered.

    Returns `None` if the `mcp` SDK is not installed; callers can fall back
    to `run_stdio()` which has its own minimal JSON-RPC loop.
    """
    sdk = _try_import_mcp()
    if not sdk:
        return None
    Server = sdk["Server"]
    server = Server("matrx-scraper")

    specs = list(tools or ALL_TOOLS)

    # Register a single list_tools handler.
    @server.list_tools()  # type: ignore[misc]
    async def _list_tools() -> list[dict[str, Any]]:
        return [
            {
                "name": spec.name,
                "description": spec.description,
                "inputSchema": spec.input_schema,
            }
            for spec in specs
        ]

    @server.call_tool()  # type: ignore[misc]
    async def _call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
        spec = _find(specs, name)
        if spec is None:
            return [
                {
                    "type": "text",
                    "text": json.dumps(
                        {"success": False, "error_message": f"unknown tool: {name}"}
                    ),
                }
            ]
        try:
            result = await spec.handler(arguments or {})
        except Exception as exc:
            logger.exception("tool %s raised", name)
            result = {
                "success": False,
                "error_type": "handler_crash",
                "error_message": f"{type(exc).__name__}: {exc}",
            }
        return [{"type": "text", "text": json.dumps(result, default=_json_default)}]

    return server


def _find(specs: list[ToolSpec], name: str) -> ToolSpec | None:
    for s in specs:
        if s.name == name:
            return s
    return None


def _json_default(o: Any) -> Any:
    if hasattr(o, "model_dump"):
        return o.model_dump()
    if hasattr(o, "__dict__"):
        return o.__dict__
    return str(o)


# ── stdio runner with SDK fallback ───────────────────────────────────────


async def run_stdio(tools: list[ToolSpec] | None = None) -> int:
    sdk = _try_import_mcp()
    if sdk:
        server = build_server(tools)
        async with sdk["stdio_server"]() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
        return 0
    return await _run_minimal_stdio(list(tools or ALL_TOOLS))


async def _run_minimal_stdio(specs: list[ToolSpec]) -> int:
    """Minimal JSON-RPC loop — barely-correct fallback when the `mcp` SDK
    isn't installed. Implements `initialize`, `tools/list`, `tools/call`.
    """
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    transport, _ = await loop.connect_write_pipe(asyncio.streams.FlowControlMixin, sys.stdout)
    writer = asyncio.StreamWriter(transport, _, reader, loop)

    while True:
        line = await reader.readline()
        if not line:
            return 0
        try:
            req = json.loads(line.decode("utf-8"))
        except Exception:
            continue
        method = req.get("method")
        rpc_id = req.get("id")
        try:
            if method == "initialize":
                resp = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "matrx-scraper", "version": "0.1.0"},
                }
            elif method == "tools/list":
                resp = {
                    "tools": [
                        {
                            "name": s.name,
                            "description": s.description,
                            "inputSchema": s.input_schema,
                        }
                        for s in specs
                    ]
                }
            elif method == "tools/call":
                params = req.get("params", {})
                spec = _find(specs, params.get("name", ""))
                if spec is None:
                    resp = {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(
                                    {
                                        "success": False,
                                        "error_message": f"unknown tool: {params.get('name')}",
                                    }
                                ),
                            }
                        ],
                        "isError": True,
                    }
                else:
                    try:
                        result = await spec.handler(params.get("arguments") or {})
                    except Exception as exc:
                        result = {
                            "success": False,
                            "error_type": "handler_crash",
                            "error_message": f"{type(exc).__name__}: {exc}",
                        }
                    resp = {
                        "content": [
                            {"type": "text", "text": json.dumps(result, default=_json_default)}
                        ]
                    }
            else:
                resp = {"error": {"code": -32601, "message": f"Method not found: {method}"}}
        except Exception as exc:
            resp = {"error": {"code": -32603, "message": f"Internal error: {exc}"}}
        envelope = (
            {"jsonrpc": "2.0", "id": rpc_id, "result": resp}
            if "error" not in resp
            else {"jsonrpc": "2.0", "id": rpc_id, "error": resp["error"]}
        )
        writer.write((json.dumps(envelope) + "\n").encode("utf-8"))
        await writer.drain()


# ── CLI ──────────────────────────────────────────────────────────────────


def main() -> int:
    logging.basicConfig(
        level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    p = argparse.ArgumentParser(
        prog="matrx-scraper-mcp", description="MCP server for matrx-scraper"
    )
    g = p.add_mutually_exclusive_group()
    g.add_argument("--stdio", action="store_true", help="Run over stdio (the only transport).")
    g.add_argument("--list", action="store_true", help="List registered tools and exit.")
    p.add_argument(
        "--groups",
        default="all",
        help="Comma-separated subset: browser,scrape,crawl  (default: all)",
    )
    args = p.parse_args()

    selected = ALL_TOOLS
    if args.groups and args.groups != "all":
        wanted = {g.strip() for g in args.groups.split(",") if g.strip()}
        selected = [t for t in ALL_TOOLS if t.group in wanted]

    if args.list:
        for spec in selected:
            print(f"  {spec.group:<8}  {spec.name:<26}  {spec.description}")
        return 0

    return asyncio.run(run_stdio(selected))


if __name__ == "__main__":
    raise SystemExit(main())
