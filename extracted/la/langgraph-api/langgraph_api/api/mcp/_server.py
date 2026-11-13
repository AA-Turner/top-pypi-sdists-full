from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.server.caching import CacheHint
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

from langgraph_api import __version__
from langgraph_api.api.mcp._calls import ToolCallParams
from langgraph_api.api.mcp._tools import AssistantTools
from langgraph_api.config import HTTP_MAX_REQUEST_BODY_BYTES

if TYPE_CHECKING:
    import mcp_types as types
    from mcp.server.context import ServerRequestContext
    from starlette.types import Receive, Scope, Send

    from langgraph_api.api.mcp._pauses import ToolResult

UNCACHED = CacheHint(ttl_ms=0, scope="private")
HTTP_WHITESPACE = b" \t"


async def _list_tools(
    ctx: ServerRequestContext, params: types.PaginatedRequestParams | None
) -> types.ListToolsResult:
    return await AssistantTools.of(ctx).list(params.cursor if params else None)


async def _call_tool(ctx: ServerRequestContext, params: ToolCallParams) -> ToolResult:
    return await AssistantTools.of(ctx).call(params)


def _tools_declare_no_param_headers(_tool_name: str) -> None:
    return None


SERVER = Server(
    "LangGraph",
    version=__version__,
    cache_hints={"server/discover": UNCACHED, "tools/list": UNCACHED},
    get_tool_input_schema=_tools_declare_no_param_headers,
    on_list_tools=_list_tools,
)
SERVER.add_request_handler("tools/call", ToolCallParams, _call_tool)


async def serve(scope: Scope, receive: Receive, send: Send) -> None:
    manager = StreamableHTTPSessionManager(
        SERVER,
        stateless=True,
        json_response=True,
        max_request_body_size=HTTP_MAX_REQUEST_BODY_BYTES,
    )
    async with manager.run():
        await manager.handle_request(_with_trimmed_headers(scope), receive, send)


def _with_trimmed_headers(scope: Scope) -> Scope:
    return {
        **scope,
        "headers": [
            (name, value.strip(HTTP_WHITESPACE)) for name, value in scope["headers"]
        ],
    }
