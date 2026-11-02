"""httpx client for proxying MCP tool calls to cube-cloud."""

from __future__ import annotations

import json
import logging

import httpx

from cube_agent.config import get_cloud_url, get_api_key

logger = logging.getLogger(__name__)


class CloudClientError(Exception):
    """Raised when a cube-cloud API call fails."""


class CloudClient:
    """Thin client that forwards MCP tool calls to cube-cloud.

    Uses the MCP Streamable HTTP transport: POST to /mcp with JSON-RPC.
    Each request is stateless (no session management needed).
    """

    def __init__(self) -> None:
        self._api_key: str | None = None
        self._base_url: str | None = None
        self._http: httpx.AsyncClient | None = None

    async def _ensure_client(self) -> httpx.AsyncClient:
        if self._http is None:
            self._api_key = get_api_key()
            if not self._api_key:
                raise CloudClientError(
                    "Not authenticated. Set CUBE_API_KEY env var or run: cube-agent login <key>"
                )
            self._base_url = get_cloud_url()
            self._http = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=120,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                },
            )
        return self._http

    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Forward a tool call to cube-cloud via MCP JSON-RPC over HTTP.

        The cube-cloud /mcp endpoint speaks MCP Streamable HTTP.
        We POST a tools/call JSON-RPC request and parse the response.
        """
        http = await self._ensure_client()

        # MCP JSON-RPC request
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }

        try:
            resp = await http.post("/mcp/", json=payload)
        except httpx.ConnectError:
            raise CloudClientError(
                f"Cannot connect to cube-cloud at {self._base_url}. "
                "Check CUBE_CLOUD_URL or network connectivity."
            )

        if resp.status_code == 401:
            raise CloudClientError("Authentication failed. Check your API key.")
        if resp.status_code == 403:
            raise CloudClientError("Access denied. Your profile may not have permission for this tool.")
        if resp.status_code != 200:
            raise CloudClientError(f"cube-cloud returned HTTP {resp.status_code}: {resp.text[:500]}")

        body = self._parse_response(resp)

        # JSON-RPC error
        if "error" in body:
            err = body["error"]
            raise CloudClientError(f"Remote error: {err.get('message', err)}")

        # Extract text from MCP tool result
        result = body.get("result", {})
        content = result.get("content", [])
        texts = [c["text"] for c in content if c.get("type") == "text"]
        return "\n".join(texts) if texts else str(result)

    @staticmethod
    def _parse_response(resp: httpx.Response) -> dict:
        """Parse response body, handling both JSON and SSE formats.

        The MCP Streamable HTTP server may respond with either:
        - application/json: direct JSON-RPC body
        - text/event-stream: SSE with `event: message` + `data: {json}`
        """
        content_type = resp.headers.get("content-type", "")
        if "text/event-stream" in content_type:
            # Parse SSE — find the last `data:` line in the response
            for line in reversed(resp.text.splitlines()):
                if line.startswith("data: "):
                    return json.loads(line[6:])
            raise CloudClientError("SSE response contained no data lines")
        return resp.json()

    async def close(self) -> None:
        if self._http:
            await self._http.aclose()
            self._http = None

    async def __aenter__(self) -> CloudClient:
        return self

    async def __aexit__(self, *exc) -> None:
        await self.close()
