"""Connector MCP capability adapter."""

import asyncio
import contextlib
import itertools
from collections.abc import Callable
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

import httpx
import structlog

from mistralai.vibe.sdk.capabilities.mcp.adapters.base import McpAdapterBase
from mistralai.vibe.sdk.capabilities.mcp.config import (
    ConnectorMcpConfig,
    ConnectorMcpDirectTransport,
    ConnectorMcpSdkTransport,
)
from mistralai.vibe.sdk.capabilities.mcp.types import McpToolDescriptor

if TYPE_CHECKING:
    from mistralai.client import Mistral


logger = structlog.get_logger()

_JSONRPC_VERSION = "2.0"
_CONNECTOR_ID_PLACEHOLDER = "{{connector_id}}"


class ConnectorMcpError(RuntimeError):
    """Raised when the connector MCP proxy returns an error or malformed payload."""


def build_mistral_client(transport: ConnectorMcpSdkTransport) -> "Mistral":
    from mistralai.client import Mistral

    return Mistral(api_key=transport.api_key, **transport.client_extra_params())


def build_http_client(
    transport: ConnectorMcpDirectTransport,
    *,
    network_transport: httpx.AsyncBaseTransport | None = None,
) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=transport.base_url.rstrip("/"),
        headers={"x-internal-service": transport.origin_service, **transport.headers},
        timeout=httpx.Timeout(transport.timeout_ms / 1000),
        transport=network_transport,
    )


class ConnectorMcpAdapter(McpAdapterBase[ConnectorMcpConfig]):
    """Lifecycle wrapper around a single connector-backed MCP server."""

    def __init__(
        self,
        config: ConnectorMcpConfig,
        *,
        mistral_client_factory: Callable[[ConnectorMcpSdkTransport], "Mistral"] | None = None,
        http_client_factory: Callable[[ConnectorMcpDirectTransport], httpx.AsyncClient]
        | None = None,
    ) -> None:
        super().__init__(config)
        self._mistral_client_factory = mistral_client_factory or build_mistral_client
        self._http_client_factory = http_client_factory or build_http_client
        self._stack: contextlib.AsyncExitStack | None = None
        self._sdk_client: Mistral | None = None
        self._http_client: httpx.AsyncClient | None = None
        self._lifecycle_lock = asyncio.Lock()
        self._jsonrpc_id_counter = itertools.count(1)

    async def setup(self) -> None:
        """Open the transport needed to talk to the connector."""
        async with self._lifecycle_lock:
            if self._stack is not None:
                return

            stack = contextlib.AsyncExitStack()
            try:
                match self._config.transport:
                    case ConnectorMcpSdkTransport() as transport:
                        await self._setup_sdk_client(stack, transport)
                    case ConnectorMcpDirectTransport() as transport:
                        await self._setup_direct_client(stack, transport)
                    case _ as transport:
                        raise TypeError(f"Unsupported connector MCP transport: {type(transport)}")
            except BaseException:
                await stack.aclose()
                raise
            self._stack = stack

    async def list_tools(self) -> list[McpToolDescriptor]:
        """List tools advertised by the connector."""
        if self._stack is None:
            raise RuntimeError("ConnectorMcpAdapter.setup() must be called before use")

        match self._config.transport:
            case ConnectorMcpSdkTransport():
                raw_tools = await self._list_tools_sdk_client()
            case ConnectorMcpDirectTransport() as transport:
                raw_tools = await self._list_tools_direct_client(transport)
            case _ as transport:
                raise TypeError(f"Unsupported connector MCP transport: {type(transport)}")

        return self._normalize_tools(raw_tools)

    async def invoke_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Invoke a tool on the connector."""
        if self._stack is None:
            raise RuntimeError("ConnectorMcpAdapter.setup() must be called before use")
        match self._config.transport:
            case ConnectorMcpSdkTransport():
                result = await self._invoke_tool_sdk_client(tool_name, arguments)
            case ConnectorMcpDirectTransport() as transport:
                result = await self._invoke_tool_direct_client(transport, tool_name, arguments)
            case _ as transport:
                raise TypeError(f"Unsupported connector MCP transport: {type(transport)}")
        return result

    async def teardown(self) -> None:
        """Tear down the transport and clean up resources."""
        async with self._lifecycle_lock:
            stack, self._stack = self._stack, None
            self._sdk_client = None
            self._http_client = None
            if stack is None:
                return

            try:
                await stack.aclose()
            except Exception as exc:
                logger.warning(
                    "mcp.teardown.failed",
                    mcp_server_key=self.server_key,
                    **self._log_context,
                    exc_info=exc,
                )

    async def _setup_sdk_client(
        self,
        stack: contextlib.AsyncExitStack,
        transport: ConnectorMcpSdkTransport,
    ) -> None:
        client = await stack.enter_async_context(self._mistral_client_factory(transport))
        await client.beta.connectors.get_async(
            connector_id_or_name=self._config.connector_id_or_name,
        )

        self._sdk_client = client

    async def _setup_direct_client(
        self,
        stack: contextlib.AsyncExitStack,
        transport: ConnectorMcpDirectTransport,
    ) -> None:
        self._http_client = await stack.enter_async_context(self._http_client_factory(transport))

    async def _list_tools_sdk_client(self) -> list[Any]:
        client = self._require_sdk_client()
        kwargs: dict[str, Any] = {"connector_id_or_name": self._config.connector_id_or_name}
        if self._config.credentials_name is not None:
            kwargs["credentials_name"] = self._config.credentials_name

        result = await client.beta.connectors.list_tools_async(**kwargs)

        return list(result)

    async def _list_tools_direct_client(self, transport: ConnectorMcpDirectTransport) -> list[Any]:
        result = await self._call_direct_jsonrpc(transport, "tools/list", {})
        if not isinstance(result, dict) or not isinstance(result.get("tools"), list):
            name = self._config.connector_id_or_name
            raise ConnectorMcpError(
                f"Connector MCP proxy response for connector {name} is missing result.tools"
            )

        return result["tools"]

    async def _invoke_tool_sdk_client(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        client = self._require_sdk_client()
        kwargs: dict[str, Any] = {
            "connector_id_or_name": self._config.connector_id_or_name,
            "tool_name": tool_name,
            "arguments": arguments,
        }
        if self._config.credentials_name is not None:
            kwargs["credentials_name"] = self._config.credentials_name

        result = await client.beta.connectors.call_tool_async(**kwargs)

        return result

    async def _invoke_tool_direct_client(
        self, transport: ConnectorMcpDirectTransport, tool_name: str, arguments: dict[str, Any]
    ) -> Any:
        return await self._call_direct_jsonrpc(
            transport,
            "tools/call",
            {"name": tool_name, "arguments": arguments},
        )

    async def _call_direct_jsonrpc(
        self, transport: ConnectorMcpDirectTransport, method: str, params: dict[str, Any]
    ) -> Any:
        client = self._require_http_client()
        connector = quote(self._config.connector_id_or_name, safe="")
        path = transport.mcp_path_template.replace(_CONNECTOR_ID_PLACEHOLDER, connector)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self._config.credentials_name is not None:
            headers["x-credentials-name"] = self._config.credentials_name

        response = await client.post(
            path,
            headers=headers,
            json={
                "jsonrpc": _JSONRPC_VERSION,
                "id": next(self._jsonrpc_id_counter),
                "method": method,
                "params": params,
            },
        )
        response.raise_for_status()
        name = self._config.connector_id_or_name
        envelope = response.json()
        if not isinstance(envelope, dict):
            raise ConnectorMcpError(f"Connector MCP returned a non-object response for {name}")

        error = envelope.get("error")
        if error is not None:
            message = error.get("message") if isinstance(error, dict) else error
            raise ConnectorMcpError(
                f"Connector MCP proxy call failed for connector {name} and method {method}: "
                f"{message}"
            )

        if "result" not in envelope:
            raise ConnectorMcpError(
                f"Connector MCP proxy response for connector {name} and method {method} "
                "is missing result"
            )

        return envelope["result"]

    @property
    def _log_context(self) -> dict[str, Any]:
        return {"connector_id_or_name": self._config.connector_id_or_name}

    def _require_sdk_client(self) -> "Mistral":
        if self._sdk_client is None:
            raise RuntimeError("ConnectorMcpAdapter.setup() must be called before use")
        return self._sdk_client

    def _require_http_client(self) -> httpx.AsyncClient:
        if self._http_client is None:
            raise RuntimeError("ConnectorMcpAdapter.setup() must be called before use")
        return self._http_client


__all__ = [
    "ConnectorMcpAdapter",
    "ConnectorMcpError",
]
