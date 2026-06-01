import datetime

from fastmcp.server.proxy import FastMCPProxy

from runlayer_cli.api import RunlayerClient
from runlayer_cli.models_mcp import LocalCapabilities


async def sync_local_capabilities(
    runlayer_api_client: RunlayerClient,
    proxy: FastMCPProxy,
    server_id: str,
) -> None:
    tools = await proxy.get_tools()
    resources = await proxy.get_resources()
    prompts = await proxy.get_prompts()

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

    runlayer_api_client.update_capabilities(server_id, local_capabilities)
