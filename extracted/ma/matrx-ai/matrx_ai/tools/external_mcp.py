from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any

import httpx

from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolError, ToolResult, ToolType

logger = logging.getLogger(__name__)


MCP_PROTOCOL_VERSION = "2025-06-18"
"""Protocol version we advertise in ``initialize``. Servers echo back the
version they chose; we send that one on every subsequent request."""

MCP_ACCEPT = "application/json, text/event-stream"
"""REQUIRED by the Streamable HTTP transport. Omitting it is not a soft
degradation — compliant servers answer **406 Not Acceptable** and nothing
works. (D128: every external MCP call in production 406'd on this.)"""

UCP_AGENT_PROFILE = (
    "https://shopify.dev/ucp/agent-profiles/2026-04-08/valid-with-capabilities.json"
)
"""Public capability profile used for anonymous Shopify UCP catalog calls.

Shopify requires a profile even for its anonymous tier. This official profile
advertises the catalog capabilities exposed by the public endpoint; it is not
an authentication credential or an assertion of Matrx identity.
"""

UCP_USER_AGENT = "AI-Matrx-MCP/1.0 (+https://www.aimatrx.com)"
"""Truthful client identity for direct UCP calls.

Cloudflare rejects the default ``python-httpx`` User-Agent on Shopify's
production path. Keep this scoped to UCP so ordinary MCP transports preserve
their existing wire contract.
"""


@dataclass(frozen=True)
class MCPRuntime:
    transport: str = "http"
    endpoint_url: str | None = None
    command: str | None = None
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    tool_allowlist: frozenset[str] = frozenset()


class ExternalMCPClient:
    """Client for calling tools on remote MCP servers over the MCP
    **Streamable HTTP** transport (JSON-RPC 2.0 over HTTP POST).

    Three things the transport requires that a plain JSON POST does not:

    1. ``Accept: application/json, text/event-stream`` on every request.
    2. An ``initialize`` → ``notifications/initialized`` handshake before any
       other method. Servers may issue an ``Mcp-Session-Id`` there which must
       be echoed on every later request.
    3. Responses may come back as **SSE** (``text/event-stream``) rather than
       JSON — both shapes carry the same JSON-RPC envelope.

    Local ``stdio`` servers use the official Python MCP client and the launch
    recipe stored in ``tool.mcp_config``. The child exists only for the
    discovery/call lifetime and inherits no secret unless the host explicitly
    resolves one into the recipe.
    """

    def __init__(self, timeout: float = 120.0):
        self._timeout = timeout
        self._request_id = 0

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    async def discover_tools(
        self,
        server_url: str | None,
        auth: dict[str, Any] | None = None,
        *,
        transport: str = "http",
        command: str | None = None,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
    ) -> list[ToolDefinition]:
        """Call ``tools/list`` on a remote MCP server and parse into ToolDefinitions."""
        if transport == "stdio":
            return await self.discover_tools_stdio(
                command=command,
                args=args or [],
                env=env or {},
            )
        if not server_url:
            raise ValueError("HTTP MCP discovery requires server_url")
        request_payload = self._build_request(
            "tools/list", self._request_params(server_url, arguments=None)
        )
        raw = await self._send(server_url, request_payload, auth)

        tools: list[ToolDefinition] = []
        for tool_data in raw.get("result", {}).get("tools", []):
            td = ToolDefinition(
                name=tool_data.get("name", ""),
                description=tool_data.get("description", ""),
                parameters=self._schema_to_params(
                    tool_data.get("inputSchema") or tool_data.get("input_schema", {})
                ),
                output_schema=tool_data.get("outputSchema") or tool_data.get("output_schema"),
                tool_type=ToolType.EXTERNAL_MCP,
            )
            tools.append(td)

        return tools

    async def discover_tools_stdio(
        self,
        *,
        command: str | None,
        args: list[str],
        env: dict[str, str],
    ) -> list[ToolDefinition]:
        if not command:
            raise ValueError("stdio MCP discovery requires a command")
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        params = StdioServerParameters(command=command, args=args, env=env or None)
        async with stdio_client(params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                listed = await session.list_tools()
        return [
            ToolDefinition(
                name=tool.name,
                description=tool.description or "",
                parameters=self._schema_to_params(tool.inputSchema or {}),
                output_schema=tool.outputSchema,
                tool_type=ToolType.EXTERNAL_MCP,
                mcp_transport="stdio",
                mcp_command=command,
                mcp_args=args,
                mcp_env=env,
            )
            for tool in listed.tools
        ]

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def call_tool(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
    ) -> ToolResult:
        """Call a tool on the remote MCP server and return a ToolResult."""
        started_at = time.time()
        try:
            runtime = await self._resolve_runtime(tool_def)
        except Exception as exc:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="configuration",
                    message=f"MCP runtime resolution failed for '{tool_def.name}': {exc}",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        local_name = self._strip_namespace(tool_def.name)
        if runtime.tool_allowlist and local_name not in runtime.tool_allowlist:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_allowed",
                    message=f"MCP tool '{local_name}' is outside the server allowlist",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        if runtime.transport == "stdio":
            return await self._call_tool_stdio(tool_def, local_name, args, ctx, runtime, started_at)

        server_url = runtime.endpoint_url
        if not server_url:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="configuration",
                    message=f"No MCP server URL configured for tool '{tool_def.name}'",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        request_payload = self._build_request(
            "tools/call",
            {
                "name": local_name,
                "arguments": self._request_arguments(server_url, args),
            },
        )

        # Note: ``tool_def.name`` here is the canonical ``<slug>:<local>``
        # form post-0022 (e.g. ``supabase:list_projects``). The remote MCP
        # server only knows its own local tool names, so we strip the
        # ``<slug>:`` prefix below in ``_strip_namespace``.

        try:
            raw = await self._send(server_url, request_payload, tool_def.mcp_server_auth)
            result_data = raw.get("result", {})

            content_list = result_data.get("content") or []
            text_parts = [
                item.get("text", "") for item in content_list if item.get("type") == "text"
            ]
            if text_parts:
                output = "\n".join(text_parts)
            elif result_data.get("structuredContent") is not None:
                # MCP allows a successful tool to return structuredContent
                # without the optional content blocks. Shopify's UCP catalog
                # does exactly that; serializing only the absent blocks used
                # to turn a real product result into the misleading value [].
                output = json.dumps(result_data["structuredContent"], default=str)
            else:
                output = json.dumps(content_list)

            is_error = result_data.get("isError", False)
            return ToolResult(
                success=not is_error,
                output=output,
                error=ToolError(error_type="mcp_remote", message=output) if is_error else None,
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )
        except httpx.TimeoutException:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="timeout",
                    message=f"MCP server at {server_url} timed out after {self._timeout}s",
                    is_retryable=True,
                    suggested_action="Try again or check the MCP server status.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="mcp_connection",
                    message=f"Failed to call MCP server: {exc}",
                    is_retryable=True,
                    suggested_action="Check MCP server connectivity.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

    async def _call_tool_stdio(
        self,
        tool_def: ToolDefinition,
        local_name: str,
        args: dict[str, Any],
        ctx: ToolContext,
        runtime: MCPRuntime,
        started_at: float,
    ) -> ToolResult:
        if not runtime.command:
            raise ValueError("stdio MCP call requires a command")
        from mcp import ClientSession, StdioServerParameters, types
        from mcp.client.stdio import stdio_client

        params = StdioServerParameters(
            command=runtime.command,
            args=runtime.args,
            env=runtime.env or None,
        )
        try:
            async with stdio_client(params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    # ``ClientSession.call_tool`` validates the provider's output
                    # schema client-side. Some official servers return additive
                    # fields while their own schema lags; the HTTP path never
                    # applies that extra client gate, so stdio preserves parity by
                    # reading the typed MCP result without re-validating it here.
                    result = await session.send_request(
                        types.ClientRequest(
                            types.CallToolRequest(
                                params=types.CallToolRequestParams(
                                    name=local_name,
                                    arguments=args,
                                )
                            )
                        ),
                        types.CallToolResult,
                    )
            text_parts = [
                item.text for item in result.content if getattr(item, "type", None) == "text"
            ]
            output = "\n".join(text_parts)
            if not output and result.structuredContent is not None:
                output = json.dumps(result.structuredContent, default=str)
            is_error = bool(result.isError)
            return ToolResult(
                success=not is_error,
                output=output,
                error=ToolError(error_type="mcp_remote", message=output) if is_error else None,
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="mcp_connection",
                    message=f"Failed to call stdio MCP server: {exc}",
                    is_retryable=True,
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

    async def _resolve_runtime(self, tool_def: ToolDefinition) -> MCPRuntime:
        direct_transport = (tool_def.mcp_transport or "").strip().lower()
        if direct_transport or tool_def.mcp_server_url or tool_def.mcp_command:
            return MCPRuntime(
                transport=direct_transport or "http",
                endpoint_url=tool_def.mcp_server_url,
                command=tool_def.mcp_command,
                args=list(tool_def.mcp_args),
                env=self._merge_stdio_env(tool_def),
                tool_allowlist=frozenset(tool_def.mcp_tool_allowlist),
            )
        if not tool_def.managed_by_server_id:
            return MCPRuntime(endpoint_url=tool_def.mcp_server_url)

        from matrx_ai.db._registry import get_instance

        server_mgr = get_instance("tool_mcp_server_manager_instance")
        server = await server_mgr.load_by_id(tool_def.managed_by_server_id)
        if server is None:
            raise ValueError(f"MCP server {tool_def.managed_by_server_id} not found")
        server_row = server.to_dict() if hasattr(server, "to_dict") else dict(server)
        transport = str(server_row.get("transport") or "http").lower()
        metadata = server_row.get("metadata") or {}
        raw_allowlist = metadata.get("tool_allowlist") if isinstance(metadata, dict) else None
        allowlist = frozenset(str(name) for name in (raw_allowlist or []) if name)
        if transport != "stdio":
            return MCPRuntime(
                transport=transport,
                endpoint_url=server_row.get("endpoint_url"),
                tool_allowlist=allowlist,
            )

        config_mgr = get_instance("tool_mcp_config_manager_instance")
        configs = await config_mgr.filter_items(
            server_id=tool_def.managed_by_server_id,
            is_default=True,
        )
        if not configs:
            configs = await config_mgr.filter_items(server_id=tool_def.managed_by_server_id)
        if not configs:
            raise ValueError("stdio MCP server has no tool.mcp_config launch recipe")
        config = configs[0]
        row = config.to_dict() if hasattr(config, "to_dict") else dict(config)
        return MCPRuntime(
            transport="stdio",
            command=row.get("command"),
            args=[str(value) for value in (row.get("args") or [])],
            env=self._merge_stdio_env(tool_def),
            tool_allowlist=allowlist,
        )

    @staticmethod
    def _merge_stdio_env(tool_def: ToolDefinition) -> dict[str, str]:
        env = dict(tool_def.mcp_env)
        auth = tool_def.mcp_server_auth
        raw_env = auth.get("env") if isinstance(auth, dict) else None
        if raw_env is None:
            return env
        if not isinstance(raw_env, dict) or any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in raw_env.items()
        ):
            raise ValueError("resolved stdio MCP environment must be a string map")
        env.update(raw_env)
        return env

    # ------------------------------------------------------------------
    # Transport
    # ------------------------------------------------------------------

    async def _send(
        self,
        server_url: str,
        payload: dict[str, Any],
        auth: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        headers = self._auth_headers(auth)
        is_ucp = self._is_ucp_endpoint(server_url)
        if is_ucp:
            headers["User-Agent"] = UCP_USER_AGENT

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            if is_ucp:
                response = await client.post(server_url, json=payload, headers=headers)
                response.raise_for_status()
                return self._parse_rpc(response)
            session_id, protocol_version = await self._handshake(client, server_url, headers)
            call_headers = dict(headers)
            call_headers["MCP-Protocol-Version"] = protocol_version
            if session_id:
                call_headers["Mcp-Session-Id"] = session_id

            response = await client.post(server_url, json=payload, headers=call_headers)
            response.raise_for_status()
            data = self._parse_rpc(response)

        if "error" in data:
            err = data["error"]
            raise RuntimeError(f"MCP error {err.get('code', '?')}: {err.get('message', 'Unknown')}")

        return data

    @staticmethod
    def _is_ucp_endpoint(server_url: str) -> bool:
        """Return whether the endpoint uses the direct UCP MCP binding."""
        return httpx.URL(server_url).path.rstrip("/").endswith("/api/ucp/mcp")

    @classmethod
    def _request_arguments(cls, server_url: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if not cls._is_ucp_endpoint(server_url):
            return arguments
        supplied = dict(arguments)
        meta = dict(supplied.get("meta") or {})
        meta.setdefault("ucp-agent", {"profile": UCP_AGENT_PROFILE})
        supplied["meta"] = meta
        return supplied

    @classmethod
    def _request_params(
        cls, server_url: str, *, arguments: dict[str, Any] | None
    ) -> dict[str, Any]:
        if not cls._is_ucp_endpoint(server_url):
            return {}
        return {"arguments": cls._request_arguments(server_url, arguments or {})}

    def _auth_headers(self, auth: dict[str, Any] | None) -> dict[str, str]:
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": MCP_ACCEPT,
        }
        if auth:
            if "bearer" in auth:
                headers["Authorization"] = f"Bearer {auth['bearer']}"
            elif "api_key" in auth:
                headers["X-API-Key"] = auth["api_key"]
            elif "basic" in auth:
                # "user:pass" — encoded here so resolvers never pre-encode.
                import base64

                headers["Authorization"] = (
                    "Basic " + base64.b64encode(str(auth["basic"]).encode()).decode()
                )
            if isinstance(auth.get("headers"), dict):
                for name, value in auth["headers"].items():
                    headers[str(name)] = str(value)
        return headers

    async def _handshake(
        self, client: httpx.AsyncClient, server_url: str, headers: dict[str, str]
    ) -> tuple[str | None, str]:
        """Run ``initialize`` + ``notifications/initialized``.

        Returns ``(session_id, negotiated_protocol_version)``. The session id
        is None for servers that don't use one (it is optional per spec)."""
        init_payload = self._build_request(
            "initialize",
            {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "matrx-ai", "version": "1.0"},
            },
        )
        response = await client.post(server_url, json=init_payload, headers=headers)
        response.raise_for_status()
        data = self._parse_rpc(response)
        if "error" in data:
            err = data["error"]
            raise RuntimeError(
                f"MCP initialize failed {err.get('code', '?')}: {err.get('message', 'Unknown')}"
            )

        session_id = response.headers.get("mcp-session-id")
        negotiated = data.get("result", {}).get("protocolVersion")
        protocol_version = (
            negotiated if isinstance(negotiated, str) and negotiated else MCP_PROTOCOL_VERSION
        )

        # The spec requires this notification before other methods. It is a
        # notification (no id) — servers answer 202 with no body.
        ack_headers = dict(headers)
        ack_headers["MCP-Protocol-Version"] = protocol_version
        if session_id:
            ack_headers["Mcp-Session-Id"] = session_id
        try:
            ack = await client.post(
                server_url,
                json={"jsonrpc": "2.0", "method": "notifications/initialized"},
                headers=ack_headers,
            )
            ack.raise_for_status()
        except httpx.HTTPError as exc:
            # Some servers reject/ignore the ack but serve requests anyway.
            # Losing the whole call over it would be worse than proceeding.
            logger.warning(
                "[external_mcp] initialized-notification to %s failed (%s) — continuing",
                server_url,
                exc,
            )

        return session_id, protocol_version

    @staticmethod
    def _parse_rpc(response: httpx.Response) -> dict[str, Any]:
        """Read a JSON-RPC envelope from either a plain JSON body or an SSE
        (``text/event-stream``) body — the Streamable HTTP transport lets the
        server pick, so a client that only understands JSON is broken."""
        content_type = response.headers.get("content-type", "")
        if "text/event-stream" not in content_type:
            return response.json()

        for line in response.text.splitlines():
            if not line.startswith("data:"):
                continue
            chunk = line[len("data:") :].strip()
            if not chunk:
                continue
            try:
                parsed = json.loads(chunk)
            except ValueError:
                continue
            if isinstance(parsed, dict) and ("result" in parsed or "error" in parsed):
                return parsed
        raise RuntimeError("MCP server returned an event stream with no JSON-RPC response")

    def _build_request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        self._request_id += 1
        return {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params,
        }

    @staticmethod
    def _strip_namespace(name: str) -> str:
        """Remove the namespace prefix from a canonical tool name.

        Database-discovered MCP tools use ``mcp.<slug>.<local>`` while the
        newer general tool namespace uses ``<namespace>:<local>``. The remote
        MCP server is
        invoked with the local segment only — ``list_projects`` — since
        the namespace is *our* identifier, not the server's.

        A name without a colon carries no namespace and is returned
        UNCHANGED.

        There used to be a "legacy" fallback that split on the first
        underscore when no colon was present. Underscores are the single most
        common character in real MCP tool names, so that fallback silently
        corrupted every un-namespaced name: DeepWiki's ``ask_question``
        became ``question`` and ``read_wiki_contents`` became
        ``wiki_contents``. It mangled both the invoke path and the names
        ``mcp_sync`` registers from remote discovery (remote servers never
        send OUR namespace, so nothing there should be stripped at all).
        Do not reintroduce it. (D128)
        """
        if name.startswith("mcp."):
            parts = name.split(".", 2)
            if len(parts) == 3 and parts[2]:
                return parts[2]
        # General canonical separator is ':'. Split on the FIRST colon so local
        # names that legitimately contain colons (rare but allowed in some
        # MCP specs) round-trip intact.
        if ":" in name:
            return name.split(":", 1)[1]
        return name

    @staticmethod
    def _schema_to_params(input_schema: dict[str, Any]) -> dict[str, Any]:
        """Convert a JSON Schema ``inputSchema`` from MCP into the internal param dict."""
        if not input_schema:
            return {}
        properties = input_schema.get("properties", {})
        required_set = set(input_schema.get("required", []))
        params: dict[str, Any] = {}
        for key, prop in properties.items():
            params[key] = {
                "type": prop.get("type", "string"),
                "description": prop.get("description", ""),
                "required": key in required_set,
            }
            for f in ("items", "enum", "default", "minimum", "maximum"):
                if f in prop:
                    params[key][f] = prop[f]
        return params
