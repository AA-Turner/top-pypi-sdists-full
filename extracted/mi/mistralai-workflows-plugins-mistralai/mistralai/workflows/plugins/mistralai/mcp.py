import asyncio
from typing import Literal

import structlog
from mcp import StdioServerParameters
from pydantic import BaseModel

from mistralai.extra.mcp.sse import MCPClientSSE, SSEServerParams
from mistralai.extra.mcp.stdio import MCPClientSTDIO
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.utils.cache import in_memory_cache

logger = structlog.get_logger(__name__)


class MCPStdioConfig(BaseModel):
    type: Literal["stdio"] = "stdio"
    command: str
    args: list[str]
    name: str


class MCPSSEConfig(BaseModel):
    type: Literal["sse"] = "sse"
    url: str
    timeout: int = 60
    name: str
    headers: dict[str, str] | None = None


MCPConfig = MCPStdioConfig | MCPSSEConfig


@in_memory_cache(ttl=60 * 60, namespace="mcp_sse")  # 1 hour
async def get_sse_client_and_tools(
    url: str, timeout: int, name: str, headers: dict[str, str] | None
) -> tuple[MCPClientSSE, list[dict]]:
    """Get or create SSE client with cached tools (cached per URL, expires after 1 hour)."""
    logger.info("creating new sse client", url=url, timeout=timeout, name=name)
    client = MCPClientSSE(sse_params=SSEServerParams(url=url, timeout=timeout, headers=headers), name=name)

    try:
        async with asyncio.timeout(timeout):
            logger.info("initializing sse client", url=url)
            await client.initialize()
            logger.info("sse client initialized", url=url)

            logger.info("fetching tools from sse client", url=url)
            tools_raw = await client.get_tools()
            tools = []
            for tool in tools_raw:
                if hasattr(tool, "model_dump"):
                    tools.append(tool.model_dump())
                elif isinstance(tool, dict):
                    tools.append(tool)

            logger.info("sse client created and cached", url=url, tool_count=len(tools))
            return client, tools
    except asyncio.TimeoutError:
        logger.error("sse client initialization timed out", url=url, timeout=timeout)
        raise RuntimeError(f"sse client initialization timed out after {timeout}s: {url}")


async def collect_tools_stdio(config: MCPStdioConfig) -> list[dict]:
    """Spawn stdio client temporarily to collect tools."""
    logger.info("collecting tools from stdio mcp", command=config.command)
    client = MCPClientSTDIO(
        stdio_params=StdioServerParameters(command=config.command, args=config.args), name=config.name
    )
    try:
        await client.initialize()
        tools_raw = await client.get_tools()
        tools = []
        for tool in tools_raw:
            if hasattr(tool, "model_dump"):
                tools.append(tool.model_dump())
            elif isinstance(tool, dict):
                tools.append(tool)
        logger.info("collected tools from stdio mcp", command=config.command, tool_count=len(tools))
        return tools
    finally:
        await client.aclose()


async def collect_tools_sse(config: MCPSSEConfig) -> list[dict]:
    """Get tools from pooled SSE client."""
    _, tools = await get_sse_client_and_tools(config.url, config.timeout, config.name, config.headers)
    return tools


class CollectMCPToolsParams(BaseModel):
    configs: list[MCPConfig]


class CollectMCPToolsResult(BaseModel):
    tools: list[dict]
    tool_to_config_map: dict[str, int]


@activity()
async def collect_mcp_tools(params: CollectMCPToolsParams) -> CollectMCPToolsResult:
    """Collect tools from MCP configs."""
    if not params.configs:
        return CollectMCPToolsResult(tools=[], tool_to_config_map={})

    all_tools = []
    tool_to_config_map = {}
    failed_configs = []

    for i, config in enumerate(params.configs):
        try:
            if config.type == "stdio":
                tools = await collect_tools_stdio(config)
            elif config.type == "sse":
                tools = await collect_tools_sse(config)
            else:
                continue

            for tool in tools:
                tool_name = tool.get("function", {}).get("name")
                if tool_name:
                    prefixed_name = f"{config.name}_{tool_name}"
                    tool["function"]["name"] = prefixed_name
                    tool_to_config_map[prefixed_name] = i

            all_tools.extend(tools)

        except Exception as e:
            logger.warning(
                "failed to collect tools from mcp config",
                config_type=config.type,
                config_name=config.name,
                error=str(e),
                error_type=type(e).__name__,
            )
            failed_configs.append((config.name or f"config_{i}", e))

    if failed_configs and not all_tools:
        error_summary = "; ".join([f"{name}: {err}" for name, err in failed_configs])
        raise RuntimeError(f"all mcp configs failed: {error_summary}")

    if failed_configs:
        logger.warning(
            "some mcp configs failed, continuing with reduced toolset",
            failed_count=len(failed_configs),
            success_count=len(params.configs) - len(failed_configs),
        )

    return CollectMCPToolsResult(tools=all_tools, tool_to_config_map=tool_to_config_map)


class ExecuteMCPToolParams(BaseModel):
    configs: list[MCPConfig]
    tool_name: str
    tool_arguments: dict
    config_index: int


class ExecuteMCPToolResult(BaseModel):
    result: str


@activity()
async def execute_mcp_tool(params: ExecuteMCPToolParams) -> ExecuteMCPToolResult:
    """Execute MCP tool based on config type."""
    config = params.configs[params.config_index]

    # strip prefix from tool name (format: {config.name}_{original_tool_name})
    original_tool_name = params.tool_name.removeprefix(f"{config.name}_")

    logger.info(
        "executing mcp tool",
        tool=params.tool_name,
        original_tool=original_tool_name,
        config_type=config.type,
        config_name=config.name,
    )

    if config.type == "stdio":
        stdio_client = MCPClientSTDIO(
            stdio_params=StdioServerParameters(command=config.command, args=config.args), name=config.name
        )
        try:
            await stdio_client.initialize()
            result = await stdio_client.execute_tool(original_tool_name, params.tool_arguments)
        finally:
            await stdio_client.aclose()

    elif config.type == "sse":
        sse_client, _ = await get_sse_client_and_tools(config.url, config.timeout, config.name, config.headers)
        result = await sse_client.execute_tool(original_tool_name, params.tool_arguments)

    else:
        raise ValueError(f"unsupported mcp config type: {config.type}")

    if isinstance(result, list):
        result_str = "\n".join([str(chunk.get("text", chunk)) for chunk in result])
    else:
        result_str = str(result)

    logger.info("mcp tool executed", tool=params.tool_name, config_type=config.type)
    return ExecuteMCPToolResult(result=result_str)
