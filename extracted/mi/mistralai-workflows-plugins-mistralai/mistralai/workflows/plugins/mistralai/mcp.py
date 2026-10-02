import asyncio
import os
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Literal

import httpx
import structlog
from mcp import StdioServerParameters
from mcp.client.stdio import get_default_environment
from pydantic import BaseModel

from mistralai.extra.mcp.base import MCPClientBase
from mistralai.extra.mcp.sse import MCPClientSSE, SSEServerParams
from mistralai.extra.mcp.stdio import MCPClientSTDIO

# Streamable HTTP support requires mistralai>=2.8.0 (client-python#592). The plugin
# keeps a permissive floor (>=2.0.0) to avoid forcing a relock across every in-repo
# dependent; consumers that use MCPStreamableHTTPConfig should pin mistralai>=2.8.0
# in their own project. The import is guarded so stdio/SSE users on older mistralai
# can still load this module (and the plugin package): the error is raised only when
# a Streamable HTTP config is actually opened.
try:
    from mistralai.extra.mcp.streamable_http import MCPClientStreamableHTTP, StreamableHTTPServerParams
except ImportError as exc:  # mistralai < 2.8.0
    MCPClientStreamableHTTP = None  # type: ignore[assignment, misc]
    StreamableHTTPServerParams = None  # type: ignore[assignment, misc]
    _STREAMABLE_HTTP_IMPORT_ERROR: ImportError | None = exc
else:
    _STREAMABLE_HTTP_IMPORT_ERROR = None

from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.utils.cache import in_memory_cache

logger = structlog.get_logger(__name__)


class MCPStdioConfig(BaseModel):
    type: Literal["stdio"] = "stdio"
    command: str
    args: list[str]
    name: str
    env_mapping: dict[str, str] | None = None


def _resolve_env(env_mapping: dict[str, str] | None) -> dict[str, str] | None:
    """Resolve an env_mapping into a concrete subprocess environment.

    The mapping goes from subprocess var name to worker var name, e.g.
    ``{"NOTION_TOKEN": "NOTION_TOKEN_BOT_A"}``. Only the mapping names are ever
    serialized into Temporal activity params and event history; the secret
    values are read from the worker's ``os.environ`` here, inside the activity,
    and must never be logged or serialized.

    Returns ``None`` when ``env_mapping`` is ``None`` (unchanged behavior:
    the subprocess receives ``get_default_environment()`` only). Raises
    ``RuntimeError`` if any source var is missing from the worker environment,
    since these are explicitly declared, not best-effort defaults.
    """
    if env_mapping is None:
        return None
    resolved = get_default_environment()
    for subprocess_name, worker_name in env_mapping.items():
        value = os.environ.get(worker_name)
        if value is None:
            raise RuntimeError(
                f"env_mapping source variable '{worker_name}' "
                f"(for subprocess var '{subprocess_name}') is not set in the worker environment"
            )
        resolved[subprocess_name] = value
    return resolved


def _resolve_headers(headers: dict[str, str] | None, header_mapping: dict[str, str] | None) -> dict[str, str] | None:
    """Resolve static headers plus a header_mapping into concrete request headers.

    The mapping goes from HTTP header name to worker var name, e.g.
    ``{"Notion-Token": "NOTION_TOKEN_BOT_A"}``. Only the mapping names are ever
    serialized into Temporal activity params and event history; the secret values
    are read from the worker's ``os.environ`` here, inside the activity, and must
    never be logged or serialized. Static ``headers`` pass through as-is, so never
    put a secret in them (use ``header_mapping``).

    Returns ``None`` when neither is provided. Raises ``RuntimeError`` if a
    declared worker var is missing or empty/whitespace, since these are
    explicit, not best-effort. Values are stripped, mirroring ``auth_token_env``,
    so a trailing newline from a secret mount cannot corrupt a header.
    """
    if not headers and not header_mapping:
        return None
    resolved: dict[str, str] = dict(headers or {})
    for header_name, worker_name in (header_mapping or {}).items():
        value = (os.environ.get(worker_name) or "").strip()
        if not value:
            raise RuntimeError(
                f"header_mapping source variable '{worker_name}' "
                f"(for header '{header_name}') is not set or is empty/whitespace in the worker environment"
            )
        resolved[header_name] = value
    return resolved


class MCPSSEConfig(BaseModel):
    type: Literal["sse"] = "sse"
    url: str
    timeout: int = 60
    name: str
    headers: dict[str, str] | None = None


class MCPStreamableHTTPConfig(BaseModel):
    type: Literal["streamable_http"] = "streamable_http"
    url: str
    # Applied per phase (client init, then get_tools / execute_tool), so the
    # worst-case wall time before an error surfaces is ~2x this value; size the
    # wrapping activity's StartToCloseTimeout accordingly.
    timeout: int = 60
    name: str
    # Bearer token for the endpoint, read from this worker env var inside the
    # activity and sent as ``Authorization: Bearer <value>``. Store the raw token
    # in your secret manager; the SDK adds the scheme. Only the env var name is
    # serialized into Temporal params, never the token itself.
    auth_token_env: str | None = None
    # Extra per-request headers whose values come from worker env vars, e.g.
    # ``{"Notion-Token": "NOTION_TOKEN_BOT_A"}``. The whole header value is the
    # variable's value. Only the names are serialized; values are read from
    # ``os.environ`` inside the activity.
    header_mapping: dict[str, str] | None = None
    # Extra static, non-secret headers sent as-is. Never put secrets here: they
    # would be serialized into Temporal params and event history.
    headers: dict[str, str] | None = None
    # Whether the httpx client trusts the worker's ambient env (HTTP(S)_PROXY,
    # SSL_CERT_FILE/DIR, .netrc). Default True (httpx default) so external MCPs reach
    # the endpoint through the worker's egress proxy and cert bundle. Set False for an
    # in-cluster MCP on a worker whose external egress goes through a proxy, so the
    # direct in-cluster call isn't routed through that proxy (which would hang).
    # Note: when True, httpx also reads the worker's .netrc, so if it holds an entry
    # for the MCP host those credentials are attached as Authorization. Only point at
    # a trusted host, or set False, if the worker's .netrc carries unrelated secrets.
    trust_env: bool = True
    # Whether httpx follows HTTP redirects (3xx). Default False: on a redirect httpx
    # only strips the Authorization header on cross-origin hops, so the per-request
    # secret headers above (e.g. Notion-Token from header_mapping) would be resent
    # verbatim to the redirect target, letting a compromised or open-redirecting MCP
    # exfiltrate them. Leave False unless the MCP server relies on redirects (e.g.
    # /mcp -> /mcp/) and you trust every host it can redirect to; then set True.
    follow_redirects: bool = False


MCPConfig = MCPStdioConfig | MCPSSEConfig | MCPStreamableHTTPConfig


def _mcp_tools_as_dicts(tools: list) -> list[dict]:
    """Serialize MCP tool objects (or already-plain dicts) to plain dicts."""
    out: list[dict] = []
    for tool in tools:
        if hasattr(tool, "model_dump"):
            out.append(tool.model_dump())
        elif isinstance(tool, dict):
            out.append(tool)
    return out


async def _init_client_and_collect_tools(client: MCPClientBase, timeout: int) -> list[dict]:
    """Initialize an MCP client under a timeout and return its tools as dicts.

    Used by the pooled SSE getter to run initialization and tool collection under
    one shared deadline. (The Streamable HTTP path opens a fresh client per call
    via ``_open_streamable_http_client`` instead, so it does not use this helper.)
    """
    try:
        async with asyncio.timeout(timeout):
            logger.info("initializing mcp client", client=str(client))
            await client.initialize()
            tools = _mcp_tools_as_dicts(await client.get_tools())
            logger.info("mcp client ready", client=str(client), tool_count=len(tools))
            return tools
    except asyncio.TimeoutError:
        logger.error("mcp client initialization timed out", client=str(client), timeout=timeout)
        raise RuntimeError(f"mcp client initialization timed out after {timeout}s: {client}")


@in_memory_cache(ttl=60 * 60, namespace="mcp_sse")  # 1 hour
async def get_sse_client_and_tools(
    url: str, timeout: int, name: str, headers: dict[str, str] | None
) -> tuple[MCPClientSSE, list[dict]]:
    """Get or create a pooled SSE client with its tools (cached 1 hour)."""
    logger.info("creating new sse client", url=url, timeout=timeout, name=name)
    client = MCPClientSSE(sse_params=SSEServerParams(url=url, timeout=timeout, headers=headers), name=name)
    tools = await _init_client_and_collect_tools(client, timeout)
    return client, tools


async def collect_tools_stdio(config: MCPStdioConfig) -> list[dict]:
    """Spawn stdio client temporarily to collect tools."""
    logger.info("collecting tools from stdio mcp", command=config.command)
    client = MCPClientSTDIO(
        stdio_params=StdioServerParameters(
            command=config.command, args=config.args, env=_resolve_env(config.env_mapping)
        ),
        name=config.name,
    )
    try:
        await client.initialize()
        tools = _mcp_tools_as_dicts(await client.get_tools())
        logger.info("collected tools from stdio mcp", command=config.command, tool_count=len(tools))
        return tools
    finally:
        await client.aclose()


async def collect_tools_sse(config: MCPSSEConfig) -> list[dict]:
    """Get tools from pooled SSE client."""
    _, tools = await get_sse_client_and_tools(config.url, config.timeout, config.name, config.headers)
    return tools


def _resolve_streamable_http_headers(config: MCPStreamableHTTPConfig) -> dict[str, str] | None:
    """Resolve a Streamable HTTP config's outgoing request headers, inside the activity.

    Layers, in order: static ``headers``, env-sourced ``header_mapping`` values, and,
    when ``auth_token_env`` is set, an ``Authorization: Bearer <token>`` gate read
    from that worker env var. Secrets are read from ``os.environ`` here and never
    serialized into Temporal params or logged. ``auth_token_env`` owns the
    ``Authorization`` header, so do not also set it via ``header_mapping``/``headers``.
    """
    headers = _resolve_headers(config.headers, config.header_mapping)
    if config.auth_token_env is not None:
        if headers and any(name.lower() == "authorization" for name in headers):
            raise RuntimeError(
                "both auth_token_env and an explicit Authorization header (via headers or header_mapping) "
                "are set; use only one to avoid silently dropping a credential"
            )
        token = (os.environ.get(config.auth_token_env) or "").strip()
        if not token:
            raise RuntimeError(
                f"auth_token_env '{config.auth_token_env}' is not set or is empty/whitespace in the worker environment"
            )
        headers = dict(headers or {})
        headers["Authorization"] = f"Bearer {token}"
    return headers


@asynccontextmanager
async def _open_streamable_http_client(
    config: MCPStreamableHTTPConfig,
) -> AsyncIterator[MCPClientStreamableHTTP]:
    """Open a Streamable HTTP MCP client for one operation, closing it in the same task.

    The mcp Streamable HTTP transport runs an anyio task group whose cancel scope
    must be entered and exited in the same task. So, unlike a long-lived pooled
    client, the session is scoped to a single collect/execute call (mirroring the
    stdio path): opened, used, and torn down within the caller's task, which avoids
    the cross-task teardown error a cached open session raises on eviction. Headers
    are resolved per call, so different callers/tokens never share a session.
    """
    if MCPClientStreamableHTTP is None or StreamableHTTPServerParams is None:
        raise ImportError(
            "MCPStreamableHTTPConfig requires mistralai>=2.8.0 "
            "(mistralai.extra.mcp.streamable_http). Pin mistralai>=2.8.0 in your project."
        ) from _STREAMABLE_HTTP_IMPORT_ERROR
    client = MCPClientStreamableHTTP(
        params=StreamableHTTPServerParams(
            url=config.url,
            headers=_resolve_streamable_http_headers(config),
            timeout=config.timeout,
            trust_env=config.trust_env,
            follow_redirects=config.follow_redirects,
        ),
        name=config.name,
    )
    async with AsyncExitStack() as stack:
        try:
            async with asyncio.timeout(config.timeout):
                logger.info("initializing mcp client", client=str(client))
                await client.initialize(exit_stack=stack)
        except (asyncio.TimeoutError, httpx.TimeoutException):
            logger.error("mcp client initialization timed out", client=str(client), timeout=config.timeout)
            raise RuntimeError(f"mcp client initialization timed out after {config.timeout}s: {client}")
        yield client


async def collect_tools_streamable_http(config: MCPStreamableHTTPConfig) -> list[dict]:
    """Open a Streamable HTTP client, collect its tools, and close it (per call).

    ``get_tools`` runs under its own ``config.timeout``; initialization is bounded
    separately in ``_open_streamable_http_client``. These are two deadlines of
    ``config.timeout`` each (worst case ~2x), not one shared budget like the SSE
    getter, but each phase is bounded so neither can hang indefinitely.
    """
    async with _open_streamable_http_client(config) as client:
        try:
            async with asyncio.timeout(config.timeout):
                tools = _mcp_tools_as_dicts(await client.get_tools())
        except (asyncio.TimeoutError, httpx.TimeoutException):
            logger.error("streamable http mcp tool listing timed out", url=config.url, timeout=config.timeout)
            raise RuntimeError(f"streamable http mcp tool listing timed out after {config.timeout}s: {config.url}")
        logger.info("collected tools from streamable http mcp", url=config.url, tool_count=len(tools))
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
            elif config.type == "streamable_http":
                tools = await collect_tools_streamable_http(config)
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
            stdio_params=StdioServerParameters(
                command=config.command, args=config.args, env=_resolve_env(config.env_mapping)
            ),
            name=config.name,
        )
        try:
            await stdio_client.initialize()
            result = await stdio_client.execute_tool(original_tool_name, params.tool_arguments)
        finally:
            await stdio_client.aclose()

    elif config.type == "sse":
        sse_client, _ = await get_sse_client_and_tools(config.url, config.timeout, config.name, config.headers)
        result = await sse_client.execute_tool(original_tool_name, params.tool_arguments)

    elif config.type == "streamable_http":
        async with _open_streamable_http_client(config) as http_client:
            try:
                async with asyncio.timeout(config.timeout):
                    result = await http_client.execute_tool(original_tool_name, params.tool_arguments)
            except (asyncio.TimeoutError, httpx.TimeoutException):
                logger.error(
                    "streamable http mcp tool execution timed out",
                    tool=original_tool_name,
                    timeout=config.timeout,
                )
                raise RuntimeError(
                    f"streamable http mcp tool execution timed out after {config.timeout}s: {original_tool_name}"
                )

    else:
        raise ValueError(f"unsupported mcp config type: {config.type}")

    if isinstance(result, list):
        result_str = "\n".join([str(chunk.get("text", chunk)) for chunk in result])
    else:
        result_str = str(result)

    logger.info("mcp tool executed", tool=params.tool_name, config_type=config.type)
    return ExecuteMCPToolResult(result=result_str)
