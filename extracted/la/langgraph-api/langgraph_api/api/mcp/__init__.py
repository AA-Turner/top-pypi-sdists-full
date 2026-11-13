import structlog

from langgraph_api.api.mcp._sdk import InstalledSdk
from langgraph_api.config import MCP_ENABLED

__all__ = ["MCP_SERVED", "mcp_routes"]

logger = structlog.stdlib.get_logger(__name__)
SDK = InstalledSdk.find()
MCP_SERVED = MCP_ENABLED and SDK.is_supported

if SDK.is_supported:
    from langgraph_api.api.mcp._routes import mcp_routes
else:
    mcp_routes = []
    if MCP_ENABLED:
        logger.error(
            "MCP endpoint disabled: the installed MCP SDK is not supported",
            required=str(SDK.required.specifier),
            installed=SDK.installed,
        )
