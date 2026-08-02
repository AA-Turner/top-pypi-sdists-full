"""Adapter that lets an MCP server tool ride the dynamic-tools mechanism.

When ``agent.use_dynamic_tools`` is on, MCP servers are connected at build time
and each of their tools is wrapped as an ``MCPToolProxy`` instead of being handed
to agno directly. The proxy exposes the same small surface the dynamic meta-tools
already read off an xpander ``Tool`` (``id``/``name``/``description`` plus a schema)
so ``xp_list_tools``/``xp_search_tools``/``xp_get_tool``/``xp_execute_tool`` can
disclose and run MCP tools with no special-casing beyond the raw-schema render.

An MCP tool's schema is a raw JSON-schema dict (``Function.parameters``), not a
pydantic model, and it takes flat kwargs (no ``payload``/``body_params`` envelope);
both differences are handled where the proxy is consumed.
"""

from typing import Any, Dict, List, Optional


class MCPToolProxy:
    """Dynamic-catalog entry backed by one live agno MCP ``Function``."""

    # Marker read by the dynamic-tools code to branch on MCP vs xpander tools.
    is_mcp_proxy: bool = True

    def __init__(
        self,
        agno_function: Any,
        server_name: Optional[str] = None,
        server_url: Optional[str] = None,
    ):
        # ``Function.name`` is already prefixed ("mcp_tool_<tool>") and unique, so
        # it doubles as the id the model passes to xp_get_tool / xp_execute_tool.
        self.id: str = agno_function.name
        self.name: str = agno_function.name
        self.description: str = agno_function.description or agno_function.name
        # Raw MCP inputSchema; rendered directly (not via a pydantic model class).
        self.raw_json_schema: Dict[str, Any] = agno_function.parameters or {}
        # Source server identity — rendered into the catalog XML so the agent knows
        # which MCP server a tool belongs to (url is None for local/stdio servers).
        self.server_name: Optional[str] = server_name
        self.server_url: Optional[str] = server_url
        self._agno_function = agno_function

    async def ainvoke(self, arguments: Optional[Dict[str, Any]] = None) -> Any:
        """Run the MCP tool via the live session; return its text content."""
        result = await self._agno_function.entrypoint(**(arguments or {}))
        # agno wraps output as a ToolResult (content str, optional images); MCP
        # failures come back as content prefixed "Error from MCP tool ...".
        return getattr(result, "content", result)


def build_mcp_proxies(
    mcp_tool: Any,
    server_name: Optional[str] = None,
    server_url: Optional[str] = None,
) -> List[MCPToolProxy]:
    """Wrap every tool of a connected agno ``MCPTools`` toolkit as a proxy."""
    return [
        MCPToolProxy(fn, server_name=server_name, server_url=server_url)
        for fn in (mcp_tool.functions or {}).values()
    ]
