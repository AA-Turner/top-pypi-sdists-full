"""MCP client wrapper for connecting to MCP servers with streamable-http support."""

import asyncio
import logging
from typing import Any, Dict, Optional, List, AsyncIterator
import httpx
import json

from ..core.models import MCPServer, MCPServerType

logger = logging.getLogger(__name__)


class MCPClient:
    """Wrapper for MCP client connections with streamable-http support."""
    
    def __init__(self, mcp_server: MCPServer):
        self.mcp_server = mcp_server
        self._available_tools: List[Dict[str, Any]] = []
        self._http_client: Optional[httpx.AsyncClient] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Connect to the MCP server using streamable-http."""
        try:
            if self.mcp_server.server_type != MCPServerType.STREAMABLE_HTTP:
                raise ValueError(f"Only streamable-http is supported, got: {self.mcp_server.server_type}")
                
            await self._connect_streamable_http()
                
        except Exception as e:
            logger.error(f"Failed to connect to MCP server {self.mcp_server.name}: {e}")
            raise
    
    async def _connect_streamable_http(self) -> None:
        """Connect using streamable-http for real-time updates."""
        url = str(self.mcp_server.url)
        
        logger.info(f"Connecting to MCP server {self.mcp_server.name} via streamable-http at {url}")
        
        # Initialize HTTP client for persistent connection
        self._http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
            http2=True  # Enable HTTP/2 for better streaming support
        )
        
        # Test connection and get available tools
        try:
            response = await self._http_client.get(f"{url}/tools")
            response.raise_for_status()
            tools_data = response.json()
            self._available_tools = tools_data.get("tools", [])
            self._connected = True
            logger.info(f"Connected to {self.mcp_server.name}, found {len(self._available_tools)} tools")
            
            # Update capabilities in the MCP server model
            self.mcp_server.capabilities = [tool["name"] for tool in self._available_tools]
        except Exception as e:
            await self._http_client.aclose()
            self._http_client = None
            raise RuntimeError(f"Failed to connect to MCP server: {e}")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on the MCP server."""
        if not self._connected or not self._http_client:
            # Reconnect if needed
            await self.connect()
            
        # Find the tool
        tool = next((t for t in self._available_tools if t["name"] == tool_name), None)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
            
        # Call the tool
        url = str(self.mcp_server.url).rstrip('/') + '/call'
        
        response = await self._http_client.post(
            url,
            json={"name": tool_name, "input": arguments}
        )
        response.raise_for_status()
        return response.json()
    
    async def call_tool_streaming(self, tool_name: str, arguments: Dict[str, Any]) -> AsyncIterator[Any]:
        """Call a tool with streaming response support."""
        if not self._connected:
            await self.connect()
        
        # Stream the tool call response
        async for chunk in self._stream_tool_call(tool_name, arguments):
            yield chunk
    
    async def _stream_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> AsyncIterator[Any]:
        """Stream a tool call response for streamable-http connections."""
        if not self._http_client:
            raise RuntimeError("HTTP client not initialized")
        
        url = str(self.mcp_server.url).rstrip('/') + '/call'
        
        # Make streaming request
        async with self._http_client.stream(
            "POST",
            url,
            json={"name": tool_name, "input": arguments},
            headers={"Accept": "text/event-stream"}
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]  # Remove "data: " prefix
                    if data:
                        try:
                            yield json.loads(data)
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse streaming data: {data}")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools."""
        if not self._connected:
            await self.connect()
            
        return self._available_tools
    
    async def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        self._connected = False
        self._available_tools = []
        
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None
    
    async def health_check(self) -> bool:
        """Check if the MCP server connection is healthy."""
        try:
            if not self._connected or not self._http_client:
                return False
                
            # Try to ping the server
            response = await self._http_client.get(f"{self.mcp_server.url}/health")
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Health check failed for {self.mcp_server.name}: {e}")
            return False
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


class MCPToolWrapper:
    """Wrapper to expose MCP tools as CrewAI-compatible tools with connection pooling."""
    
    # Class-level connection pool
    _connection_pool: Dict[str, MCPClient] = {}
    _pool_lock = asyncio.Lock()
    
    def __init__(self, mcp_server: MCPServer, tool_name: str, tool_description: str):
        self.mcp_server = mcp_server
        self.tool_name = tool_name
        self.description = tool_description
        self.name = tool_name
    
    @classmethod
    async def get_or_create_client(cls, mcp_server: MCPServer) -> MCPClient:
        """Get or create a client from the connection pool."""
        server_key = f"{mcp_server.name}:{mcp_server.url}"
        
        async with cls._pool_lock:
            if server_key not in cls._connection_pool:
                # Create new client
                client = MCPClient(mcp_server)
                await client.connect()
                cls._connection_pool[server_key] = client
            else:
                # Check if existing client is healthy
                client = cls._connection_pool[server_key]
                if not await client.health_check():
                    # Reconnect if unhealthy
                    await client.disconnect()
                    await client.connect()
            
            return cls._connection_pool[server_key]
    
    async def __call__(self, **kwargs) -> Any:
        """Execute the MCP tool using pooled connection."""
        client = await self.get_or_create_client(self.mcp_server)
        return await client.call_tool(self.tool_name, kwargs)
    
    @classmethod
    async def cleanup_pool(cls):
        """Clean up all connections in the pool."""
        async with cls._pool_lock:
            for client in cls._connection_pool.values():
                await client.disconnect()
            cls._connection_pool.clear() 