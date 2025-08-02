#!/usr/bin/env python3
"""MCP Web Automation Server main entry point."""

import asyncio
import logging
from typing import Any

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from va.mcp_server.web_automation import WebAutomationTools, create_tools
from va.playwright.tools import ALL_TOOL_HANDLERS

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

# Global instances
web_tools = WebAutomationTools()
server_mode = "full"  # Default mode

# Create the MCP server
server = Server("web-automation")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    log.info(f"Listing available tools in {server_mode} mode")
    tools = create_tools(server_mode)
    log.info(f"Returning {len(tools)} tools")
    return tools


@server.call_tool()
async def call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}

    # Check if tool is available in current mode
    available_tools = {tool.name for tool in create_tools(server_mode)}
    if name not in available_tools:
        return [
            types.TextContent(
                type="text", text=f"Tool '{name}' not available in {server_mode} mode"
            )
        ]

    try:
        if name in ALL_TOOL_HANDLERS:
            page = await web_tools._get_or_create_page()
            handler = ALL_TOOL_HANDLERS[name]
            return await handler(page, arguments)

        elif name == "navigate_to_url":
            url = arguments.get("url", "")
            result = await web_tools.navigate_to_url(url)
            return [types.TextContent(type="text", text=result)]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        log.error(f"Error in tool call {name}: {e}")
        return [types.TextContent(type="text", text=f"Error: {e}")]


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available resources."""
    return []


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource."""
    return f"Resource {uri} not found"


async def main(mode: str = "full"):
    """Main entry point for the MCP server."""
    global server_mode
    server_mode = mode

    try:
        # Browser will be started on-demand when first tool is called
        log.info(f"Starting MCP Web Automation Server in {mode} mode...")

        # Run the server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )

    except KeyboardInterrupt:
        log.info("Server interrupted by user")
    except Exception as e:
        log.error(f"Server error: {e}")
        raise
    finally:
        log.info("Cleaning up...")
        await web_tools.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
