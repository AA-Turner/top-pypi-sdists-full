"""gRPC-based A2A client for high-performance agent communication."""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Union, AsyncIterator
from datetime import datetime
import json
import uuid
from contextlib import asynccontextmanager

import grpc
from grpc import aio
from crewai.tools import BaseTool
from pydantic import Field, BaseModel

# Note: These imports assume the A2A proto files have been compiled
# In practice, you'd need to generate these from the A2A .proto definitions
# from a2a.proto import a2a_pb2, a2a_pb2_grpc

logger = logging.getLogger(__name__)


class GrpcA2AConfig(BaseModel):
    """Configuration for gRPC A2A tools."""
    endpoint: str = Field(description="The gRPC endpoint (host:port)")
    agency_name: str = Field(description="Name of the utility agency")
    agency_description: str = Field(description="Description of what the agency does")
    timeout: int = Field(default=300, description="Timeout in seconds for gRPC calls")
    retry_attempts: int = Field(default=3, description="Number of retry attempts")
    
    # gRPC specific settings
    max_message_length: int = Field(default=4 * 1024 * 1024, description="Max message size (4MB default)")
    keepalive_time_ms: int = Field(default=10000, description="Keepalive ping interval")
    keepalive_timeout_ms: int = Field(default=5000, description="Keepalive timeout")
    max_concurrent_streams: int = Field(default=100, description="Max concurrent gRPC streams")
    
    # Connection pool settings
    pool_size: int = Field(default=10, description="Number of gRPC channels in pool")
    use_tls: bool = Field(default=False, description="Whether to use TLS")
    tls_cert_path: Optional[str] = Field(default=None, description="Path to TLS certificate")


class GrpcChannelPool:
    """Manages a pool of gRPC channels for load distribution."""
    
    def __init__(self, config: GrpcA2AConfig):
        self.config = config
        self.channels: List[aio.Channel] = []
        self.current_index = 0
        self._lock = asyncio.Lock()
    
    async def initialize(self):
        """Initialize the channel pool."""
        options = [
            ('grpc.max_send_message_length', self.config.max_message_length),
            ('grpc.max_receive_message_length', self.config.max_message_length),
            ('grpc.keepalive_time_ms', self.config.keepalive_time_ms),
            ('grpc.keepalive_timeout_ms', self.config.keepalive_timeout_ms),
            ('grpc.http2.max_concurrent_streams', self.config.max_concurrent_streams),
            ('grpc.enable_http_proxy', 0),  # Disable proxy for direct connection
        ]
        
        for _ in range(self.config.pool_size):
            if self.config.use_tls:
                # Load TLS credentials
                if self.config.tls_cert_path:
                    with open(self.config.tls_cert_path, 'rb') as f:
                        credentials = grpc.ssl_channel_credentials(f.read())
                else:
                    credentials = grpc.ssl_channel_credentials()
                
                channel = aio.secure_channel(
                    self.config.endpoint,
                    credentials,
                    options=options
                )
            else:
                channel = aio.insecure_channel(
                    self.config.endpoint,
                    options=options
                )
            
            self.channels.append(channel)
        
        logger.info(f"Initialized gRPC channel pool with {self.config.pool_size} channels")
    
    async def get_channel(self) -> aio.Channel:
        """Get the next available channel (round-robin)."""
        async with self._lock:
            channel = self.channels[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.channels)
            return channel
    
    async def close(self):
        """Close all channels in the pool."""
        for channel in self.channels:
            await channel.close()
        self.channels.clear()


class GrpcA2ATool(BaseTool):
    """gRPC-based A2A tool for high-performance agent communication."""
    
    name: str
    description: str
    config: GrpcA2AConfig
    _channel_pool: Optional[GrpcChannelPool] = None
    _initialized: bool = False
    
    def __init__(self, config: GrpcA2AConfig):
        """Initialize the gRPC A2A tool."""
        tool_name = f"grpc_a2a_{config.agency_name.replace(' ', '_').replace('-', '_').lower()}"
        
        super().__init__(
            name=tool_name,
            description=f"Use {config.agency_name} via gRPC A2A: {config.agency_description}",
            config=config
        )
        self._channel_pool = None
        self._initialized = False
    
    async def _ensure_initialized(self):
        """Ensure the gRPC channel pool is initialized."""
        if not self._initialized:
            self._channel_pool = GrpcChannelPool(self.config)
            await self._channel_pool.initialize()
            self._initialized = True
    
    async def _execute_unary(self, request: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Execute a unary (request-response) gRPC call."""
        await self._ensure_initialized()
        
        # Get a channel from the pool
        channel = await self._channel_pool.get_channel()
        
        # Create stub (lightweight, can be created per request)
        # stub = a2a_pb2_grpc.A2AServiceStub(channel)
        
        # For now, return a placeholder since we don't have the actual proto files
        # In a real implementation, you would:
        # 1. Create the request message
        # 2. Call the appropriate gRPC method
        # 3. Handle the response
        
        return f"gRPC call to {self.config.agency_name} with request: {request}"
    
    async def _execute_streaming(self, request: str, context: Optional[Dict[str, Any]] = None) -> AsyncIterator[str]:
        """Execute a server-streaming gRPC call."""
        await self._ensure_initialized()
        
        # Get a channel from the pool
        channel = await self._channel_pool.get_channel()
        
        # Create stub
        # stub = a2a_pb2_grpc.A2AServiceStub(channel)
        
        # For demonstration, yield simulated chunks
        for i in range(5):
            yield f"Chunk {i} from {self.config.agency_name}"
            await asyncio.sleep(0.1)
    
    async def _execute_with_retry(self, request: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Execute request with retry logic."""
        last_error = None
        
        for attempt in range(self.config.retry_attempts):
            try:
                return await self._execute_unary(request, context)
                
            except grpc.RpcError as e:
                last_error = f"gRPC error: {e.code()}: {e.details()}"
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
                
                # Check if retryable
                if e.code() in [
                    grpc.StatusCode.UNAVAILABLE,
                    grpc.StatusCode.DEADLINE_EXCEEDED,
                    grpc.StatusCode.INTERNAL
                ]:
                    # Wait before retry with exponential backoff
                    if attempt < self.config.retry_attempts - 1:
                        await asyncio.sleep(2 ** attempt)
                else:
                    # Non-retryable error
                    break
                    
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.config.retry_attempts - 1:
                    await asyncio.sleep(2 ** attempt)
        
        return f"Failed after {self.config.retry_attempts} attempts. Last error: {last_error}"
    
    async def _arun(self, request: str, **kwargs) -> str:
        """Async execution of the tool."""
        try:
            context = kwargs.get('context', {})
            return await self._execute_with_retry(request, context)
        except Exception as e:
            logger.error(f"Error in gRPC A2A tool {self.name}: {e}")
            return f"Error: {str(e)}"
    
    def _run(self, request: str, **kwargs) -> str:
        """Sync execution of the tool."""
        try:
            loop = asyncio.get_running_loop()
            return asyncio.run_coroutine_threadsafe(
                self._arun(request, **kwargs),
                loop
            ).result()
        except RuntimeError:
            return asyncio.run(self._arun(request, **kwargs))
    
    async def stream(self, request: str, **kwargs) -> AsyncIterator[str]:
        """Stream responses using server-streaming gRPC."""
        try:
            context = kwargs.get('context', {})
            async for chunk in self._execute_streaming(request, context):
                yield chunk
        except Exception as e:
            logger.error(f"Error in gRPC streaming: {e}")
            yield f"Streaming error: {str(e)}"
    
    async def close(self):
        """Close the gRPC channel pool."""
        if self._channel_pool:
            await self._channel_pool.close()
            self._channel_pool = None
            self._initialized = False
        logger.info(f"Closed gRPC connections for {self.name}")
    
    def __del__(self):
        """Cleanup gRPC channels when tool is destroyed."""
        if self._channel_pool:
            try:
                loop = asyncio.get_running_loop()
                asyncio.create_task(self.close())
            except RuntimeError:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.close())
                loop.close()
            except Exception:
                pass


class GrpcA2AToolkit:
    """Toolkit for creating gRPC-based A2A tools."""
    
    @staticmethod
    def create_tool_from_endpoint(
        endpoint: str,
        name: str,
        description: str,
        timeout: int = 300,
        retry_attempts: int = 3,
        pool_size: int = 10,
        use_tls: bool = False,
        tls_cert_path: Optional[str] = None
    ) -> GrpcA2ATool:
        """Create a gRPC A2A tool from an endpoint."""
        config = GrpcA2AConfig(
            endpoint=endpoint,
            agency_name=name,
            agency_description=description,
            timeout=timeout,
            retry_attempts=retry_attempts,
            pool_size=pool_size,
            use_tls=use_tls,
            tls_cert_path=tls_cert_path
        )
        
        return GrpcA2ATool(config)
    
    @staticmethod
    def create_tools_from_endpoints(
        endpoints: List[Dict[str, Any]],
        default_timeout: int = 300,
        default_retry_attempts: int = 3,
        default_pool_size: int = 10
    ) -> List[GrpcA2ATool]:
        """Create multiple gRPC A2A tools."""
        tools = []
        
        for ep_config in endpoints:
            tool = GrpcA2AToolkit.create_tool_from_endpoint(
                endpoint=ep_config["endpoint"],
                name=ep_config["name"],
                description=ep_config["description"],
                timeout=ep_config.get("timeout", default_timeout),
                retry_attempts=ep_config.get("retry_attempts", default_retry_attempts),
                pool_size=ep_config.get("pool_size", default_pool_size),
                use_tls=ep_config.get("use_tls", False),
                tls_cert_path=ep_config.get("tls_cert_path")
            )
            tools.append(tool)
            logger.info(f"Created gRPC A2A tool: {tool.name}")
        
        return tools


# Example usage with both HTTP/2 and gRPC
async def compare_protocols():
    """Compare HTTP/2 and gRPC performance."""
    from .crewai_a2a_tools import A2AToolkit as HttpA2AToolkit
    
    # Create HTTP/2 tool
    http_tool = HttpA2AToolkit.create_tool_from_endpoint(
        endpoint="http://localhost:8000",
        name="Trading Agency HTTP",
        description="Trading via HTTP/2"
    )
    
    # Create gRPC tool
    grpc_tool = GrpcA2AToolkit.create_tool_from_endpoint(
        endpoint="localhost:50051",
        name="Trading Agency gRPC",
        description="Trading via gRPC",
        pool_size=20  # More channels for high load
    )
    
    # Run parallel requests
    import time
    
    # HTTP/2 test
    start = time.time()
    http_tasks = [
        http_tool._arun(f"Get price for BTC {i}")
        for i in range(100)
    ]
    await asyncio.gather(*http_tasks)
    http_time = time.time() - start
    
    # gRPC test
    start = time.time()
    grpc_tasks = [
        grpc_tool._arun(f"Get price for BTC {i}")
        for i in range(100)
    ]
    await asyncio.gather(*grpc_tasks)
    grpc_time = time.time() - start
    
    print(f"HTTP/2 time: {http_time:.2f}s")
    print(f"gRPC time: {grpc_time:.2f}s")
    
    # Cleanup
    await http_tool.close()
    await grpc_tool.close() 