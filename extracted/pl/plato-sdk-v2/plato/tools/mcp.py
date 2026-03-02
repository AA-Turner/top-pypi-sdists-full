"""MCP configuration utilities for agents.

Generates .mcp.json configs that combine remote (HTTP) and local (stdio)
MCP servers into a single file for Claude Code and other MCP-capable agents.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Inline MCP server script for pickled plato tools (stdio transport).
# Written next to tools.pkl and spawned by Claude Code as a subprocess.
LOCAL_TOOLS_MCP_SERVER_SCRIPT = '''\
"""Auto-generated MCP server that exposes pickled plato tools via stdio."""
import json
from pathlib import Path

def _get_schema(td):
    """Get JSON schema from a ToolDefinition."""
    if td.input_model:
        return td.input_model.model_json_schema()
    return {"type": "object", "properties": {}}

def _call_handler(td, arguments):
    """Call a tool handler, constructing a model instance if needed."""
    if td.input_model:
        return td.handler(td.input_model(**arguments))
    return td.handler(arguments)

def main():
    script_dir = Path(__file__).parent
    tools_path = script_dir / "tools.pkl"

    import cloudpickle
    with open(tools_path, "rb") as f:
        tools = cloudpickle.load(f)

    from plato.tools import set_workspace
    set_workspace(script_dir.parent)

    from mcp.server import Server
    from mcp.types import Tool, TextContent
    from mcp.server.stdio import stdio_server

    server = Server("plato-tools")
    tool_map = {td.name: td for td in tools}

    @server.list_tools()
    async def list_tools():
        return [
            Tool(name=td.name, description=td.description, inputSchema=_get_schema(td))
            for td in tools
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        td = tool_map.get(name)
        if not td:
            return [TextContent(type="text", text=f"Error: Unknown tool \\'{name}\\'")]
        try:
            result = _call_handler(td, arguments)
            if isinstance(result, dict):
                text = json.dumps(result, default=str)
            else:
                text = str(result)
            return [TextContent(type="text", text=text)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]

    import asyncio
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    asyncio.run(run())

if __name__ == "__main__":
    main()
'''


def write_mcp_config(
    workspace: Path,
    *,
    remote_url: str | None = None,
    remote_name: str = "datagen",
    tools_path: str | Path | None = None,
    local_server_name: str = "plato-tools",
) -> Path | None:
    """Write a .mcp.json combining remote and local MCP servers.

    Builds a single .mcp.json that can include:
    - Remote HTTP server (world-hosted tools via remote_url)
    - Local stdio server (pickled plato tools from tools.pkl)

    Args:
        workspace: Agent workspace directory (e.g. /workspace).
        remote_url: HTTP MCP server URL for world-hosted tools.
        remote_name: Name key for the remote server in mcpServers.
        tools_path: Path to tools.pkl. Defaults to <workspace>/.plato/tools.pkl.
        local_server_name: Name key for the local stdio server.

    Returns:
        Path to .mcp.json if any servers configured, None otherwise.
    """
    servers: dict[str, Any] = {}

    # Remote HTTP MCP server (world-hosted tools)
    if remote_url:
        servers[remote_name] = {
            "type": "http",
            "url": remote_url,
        }
        logger.info("MCP server: %s (http) -> %s", remote_name, remote_url)

    # Local stdio MCP server (pickled plato tools)
    tools_pkl = Path(tools_path) if tools_path else workspace / ".plato" / "tools.pkl"
    if tools_pkl.exists():
        mcp_server_path = tools_pkl.parent / "mcp_server.py"
        mcp_server_path.write_text(LOCAL_TOOLS_MCP_SERVER_SCRIPT)
        servers[local_server_name] = {
            "command": "python",
            "args": [str(mcp_server_path)],
        }
        logger.info("MCP server: %s (stdio) -> %s", local_server_name, tools_pkl)

    if not servers:
        return None

    mcp_config_path = workspace / ".mcp.json"
    mcp_config_path.write_text(json.dumps({"mcpServers": servers}, indent=2))
    logger.info("Wrote MCP config: path=%s servers=%s", mcp_config_path, list(servers.keys()))
    return mcp_config_path
