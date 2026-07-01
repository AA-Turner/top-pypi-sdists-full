"""
MCP server creation — exposing Dreadnode tools as MCP servers.
"""

import functools
import inspect
import json
import typing as t

from dreadnode.agents.tools import Tool
from dreadnode.generators.exceptions import Stop
from dreadnode.generators.utils import flatten_list

if t.TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

P = t.ParamSpec("P")
R = t.TypeVar("R")


def _convert_return_to_mcp(result: t.Any) -> t.Any:
    """Convert a return value from a Tool into a type FastMCP can serialize."""
    from mcp.server.fastmcp import Image

    from dreadnode.generators.message import ContentImageUrl, ContentText, Message

    if isinstance(result, Stop):
        return f"Tool requested stop: {result.message}"

    if isinstance(result, Message):
        if len(result.content_parts) == 1:
            return _convert_return_to_mcp(result.content_parts[0])
        return json.dumps([part.model_dump(mode="json") for part in result.content_parts], indent=2)

    if isinstance(result, ContentText):
        return result.text

    if isinstance(result, ContentImageUrl):
        try:
            return Image(data=result.to_bytes())
        except ValueError:
            return result.image_url.url

    return result


def _create_mcp_handler(
    tool: t.Callable[P, t.Any],
) -> t.Callable[P, t.Awaitable[t.Any]]:
    @functools.wraps(tool)
    async def handler(*args: P.args, **kwargs: P.kwargs) -> t.Any:
        try:
            result = tool(*args, **kwargs)
            if inspect.isawaitable(result):
                result = await result
        except Stop as stop:
            result = stop
        return _convert_return_to_mcp(result)

    return handler


def as_mcp(
    *tools: t.Any,
    name: str = "Rigging Tools",
) -> "FastMCP":
    """Serve a collection of tools over the Model Context Protocol (MCP).

    Creates a FastMCP server instance that exposes your tools to any
    compliant MCP client.

    Args:
        tools: Tool objects, raw Python functions, or class instances
            with @tool_method methods.
        name: The name of the MCP server.

    Example:
        ```python
        from dreadnode import tool
        from dreadnode.agents.mcp import as_mcp

        @tool
        def add_numbers(a: int, b: int) -> int:
            \"\"\"Adds two numbers together.\"\"\"
            return a + b

        if __name__ == "__main__":
            as_mcp(add_numbers).run(transport="stdio")
        ```
    """
    from mcp.server.fastmcp import FastMCP
    from mcp.server.fastmcp.tools import Tool as FastMCPTool

    rigging_tools: list[Tool[..., t.Any]] = []
    for tool in flatten_list(list(tools)):
        interior_tools = [
            val
            for _, val in inspect.getmembers(
                tool,
                predicate=lambda x: isinstance(x, Tool),
            )
        ]
        if interior_tools:
            rigging_tools.extend(interior_tools)
        elif not isinstance(tool, Tool):
            rigging_tools.append(Tool.from_callable(tool))
        else:
            rigging_tools.append(tool)

    fastmcp_tools = [
        FastMCPTool.from_function(
            fn=_create_mcp_handler(tool.fn),
            name=tool.name,
            description=tool.description,
        )
        for tool in rigging_tools
    ]
    return FastMCP(name, tools=fastmcp_tools)
