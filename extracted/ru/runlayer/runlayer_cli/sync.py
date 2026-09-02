import datetime

from fastmcp.server.proxy import FastMCPProxy
import structlog

from runlayer_cli import flow_trace
from runlayer_cli.api import RunlayerClient
from runlayer_cli.models_mcp import LocalCapabilities

logger = structlog.get_logger()


@flow_trace.operation("cli.sync_capabilities")
async def sync_local_capabilities(
    runlayer_api_client: RunlayerClient,
    proxy: FastMCPProxy,
    server_id: str,
    *,
    server_version: int | None = None,
) -> None:
    async with flow_trace.step("introspect", kind="remote"):
        tools = await proxy.get_tools()
        try:
            resources = await proxy.get_resources()
        except Exception as exc:
            logger.warning(
                "local_capability_resources_sync_failed",
                server_id=server_id,
                error=str(exc),
                error_type=type(exc).__name__,
                exc_info=True,
            )
            resources = {}
        try:
            prompts = await proxy.get_prompts()
        except Exception as exc:
            logger.warning(
                "local_capability_prompts_sync_failed",
                server_id=server_id,
                error=str(exc),
                error_type=type(exc).__name__,
                exc_info=True,
            )
            prompts = {}

    local_capabilities = LocalCapabilities(
        tools={
            name: t.to_mcp_tool(include_fastmcp_meta=False) for name, t in tools.items()
        },
        resources={
            name: r.to_mcp_resource(include_fastmcp_meta=False)
            for name, r in resources.items()
        },
        prompts={
            name: p.to_mcp_prompt(include_fastmcp_meta=False)
            for name, p in prompts.items()
        },
        synced_at=datetime.datetime.now(datetime.timezone.utc),
    )

    with flow_trace.step("upload", kind="http"):
        runlayer_api_client.update_capabilities(
            server_id,
            local_capabilities,
            server_version=server_version,
        )
