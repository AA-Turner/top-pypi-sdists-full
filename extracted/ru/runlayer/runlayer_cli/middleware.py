"""Basic on_message middleware for MCP CLI with OAuth support."""

import httpx
from fastmcp.server.middleware.middleware import Middleware, MiddlewareContext, CallNext
import structlog
import mcp.types as mt
from runlayer_cli.api import RunlayerClient
from runlayer_cli.sync import sync_local_capabilities

from fastmcp.server.proxy import FastMCPProxy
from fastmcp.tools.tool import ToolResult
from fastmcp.server.proxy import ProxyTool
from runlayer_cli.models import ServerDetails
from runlayer_cli.models_mcp import PostRequest, PreRequest

logger = structlog.get_logger()

# Connection errors that indicate the upstream target is not reachable
_UPSTREAM_CONNECTION_ERRORS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    ConnectionRefusedError,
    ConnectionResetError,
)


class RunlayerMiddleware(Middleware):
    def __init__(
        self,
        runlayer_api_client: RunlayerClient,
        proxy: FastMCPProxy | None,
        server: ServerDetails,
    ):
        self.runlayer_api_client = runlayer_api_client
        self.server = server
        self.proxy = proxy
        # stdio syncs at startup (before proxy.run_stdio_async); other
        # transports need middleware sync after the connection is live.
        self.sync_done = (
            not self.server.sync_required or self.server.transport_type == "stdio"
        )

    async def _sync_capabilities(self) -> None:
        try:
            assert self.proxy is not None
            await sync_local_capabilities(
                self.runlayer_api_client, self.proxy, self.server.id
            )
            self.sync_done = True
            logger.debug("capabilities_synced_via_middleware", server_id=self.server.id)
        except Exception:
            logger.warning("capabilities_sync_failed", exc_info=True)

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        payload = PreRequest(method="tools/call", params=context.message.model_dump())

        pre_response = self.runlayer_api_client.pre(self.server.id, payload)
        if pre_response.status_code != 200:
            raise Exception(pre_response.json())

        pre_json = pre_response.json()
        correlation_id = pre_json["correlation_id"]
        quick_tool_result = pre_json.get("quick_tool_result")
        if quick_tool_result:
            return ToolResult(content=quick_tool_result)

        # Input masking: apply masked arguments from the pre scan before the
        # call reaches the upstream MCP server. Mirrors the hosted proxy, which
        # executes upstream with the masked `tool_arguments` from
        # `pre_on_call_tool`. Also refresh `payload.params` so the post audit
        # records the masked arguments (pre already does).
        modified_args = pre_json.get("modified_args")
        if isinstance(modified_args, dict):
            context.message.arguments = modified_args
            payload.params = context.message.model_dump()

        try:
            result = await call_next(context)
        except _UPSTREAM_CONNECTION_ERRORS:
            logger.warning(
                "upstream_unreachable",
                server_name=self.server.name,
                tool=context.message.name,
            )
            error_result = ToolResult(
                content=f"{self.server.name} is not running. "
                f"Please start the application and try again."
            )
            try:
                post_payload = PostRequest(
                    result=error_result.to_mcp_result(),
                    **(payload.model_dump() or {}),
                    correlation_id=correlation_id,
                )
                self.runlayer_api_client.post(self.server.id, post_payload)
            except Exception:
                logger.warning("post_after_upstream_error_failed", exc_info=True)
            return error_result

        post_payload = PostRequest(
            result=result.to_mcp_result(),
            **(payload.model_dump() or {}),
            correlation_id=correlation_id,
        )

        post_response = self.runlayer_api_client.post(self.server.id, post_payload)
        if post_response.status_code != 200:
            raise Exception(post_response.json())

        # Output masking: apply the masked result the backend produced (PII
        # MASK / hidden-ascii redaction) so the MCP client receives the redacted
        # output instead of the raw upstream payload.
        post_json = post_response.json()
        if isinstance(post_json, dict):
            modified_output = post_json.get("modified_output")
            if isinstance(modified_output, dict):
                modified = mt.CallToolResult.model_validate(modified_output)
                result.content = modified.content
                # `structuredContent` (camelCase, mcp.types) ↔ `structured_content`
                # (snake_case, fastmcp) mirrors fastmcp's own `ToolResult.to_mcp_result`.
                result.structured_content = modified.structuredContent

        return result

    async def on_list_tools(  # type: ignore
        self,
        context: MiddlewareContext[mt.ListToolsRequest],
        call_next: CallNext[mt.ListToolsRequest, list[mt.Tool]],
    ) -> list[ProxyTool]:
        payload = PreRequest(method="tools/list", params=None)

        pre_response = self.runlayer_api_client.pre(self.server.id, payload)
        if pre_response.status_code != 200:
            raise Exception(pre_response.json())

        correlation_id = pre_response.json()["correlation_id"]

        try:
            result = await call_next(context)
        except _UPSTREAM_CONNECTION_ERRORS:
            logger.warning(
                "upstream_unreachable_on_list_tools",
                server_name=self.server.name,
            )
            try:
                post_payload = PostRequest(
                    result=[],
                    **(payload.model_dump() or {}),
                    correlation_id=correlation_id,
                    inject_synthetic_tool_on_policy_block=True,
                )
                self.runlayer_api_client.post(self.server.id, post_payload)
            except Exception:
                logger.warning("post_after_upstream_error_failed", exc_info=True)
            return []

        if not self.sync_done:
            await self._sync_capabilities()

        post_payload = PostRequest(
            result=[t.to_mcp_tool() for t in result],  # type: ignore
            **(payload.model_dump() or {}),
            correlation_id=correlation_id,
            inject_synthetic_tool_on_policy_block=True,
        )

        post_response = self.runlayer_api_client.post(self.server.id, post_payload)
        if post_response.status_code != 200:
            raise Exception(post_response.json())

        assert self.proxy is not None
        filtered_result = [
            ProxyTool.from_mcp_tool(self.proxy, mt.Tool.model_validate(t))  # type: ignore
            for t in post_response.json()
        ]

        return filtered_result
