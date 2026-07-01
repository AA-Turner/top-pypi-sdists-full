#!/usr/bin/env python
"""
Traia MCP Adapter

A custom MCP adapter that extends CrewAI's MCPServerAdapter to support
passing headers (like Authorization) and x402 payment protocol to streamable-http MCP servers.

This adapter transparently handles:
- Authenticated connections (via headers)
- Payment-based connections (via x402/d402 protocol)
- Standard connections (no auth or payment)
"""

import logging
from typing import Dict, Any, List, Optional, Union
import httpx
from functools import wraps

from crewai_tools import MCPServerAdapter
from crewai.tools import BaseTool

logger = logging.getLogger(__name__)

# Try to import d402 payment hooks from IATP
try:
    from eth_account import Account
    from traia_iatp.d402.clients.httpx import d402_payment_hooks
    D402_AVAILABLE = True
except ImportError:
    D402_AVAILABLE = False
    logger.warning("d402 payment hooks not available. Ensure traia_iatp.d402 is installed.")


class TraiaMCPAdapter(MCPServerAdapter):
    """
    MCP adapter that supports custom headers for streamable-http transport.
    
    This adapter extracts headers from server_params and injects them into
    all HTTP requests made to the MCP server. It works transparently for
    both authenticated and non-authenticated connections.
    
    Example:
        ```python
        # With authentication headers
        server_params = {
            "url": "https://mcp.example.com/mcp",
            "transport": "streamable-http",
            "headers": {"Authorization": "Bearer YOUR_API_KEY"}
        }
        
        # Without headers (standard connection)
        server_params = {
            "url": "https://mcp.example.com/mcp",
            "transport": "streamable-http"
        }
        
        with TraiaMCPAdapter(server_params) as tools:
            # Use tools with or without authentication
            agent = Agent(tools=tools)
        ```
    """
    
    def __init__(
        self,
        server_params: Union[Dict[str, Any], Any],
        *tool_names: str
    ):
        """
        Initialize the adapter with optional header and x402 payment support.
        
        Args:
            server_params: Server configuration. For streamable-http, can include:
                          - url: The MCP server URL
                          - transport: "streamable-http"
                          - headers: Optional dict of headers to include in requests
                          - x402_account: Optional eth_account.Account for x402 payments
                          - x402_max_value: Optional max payment value
            *tool_names: Optional tool names to filter
        """
        # Handle dict params
        if isinstance(server_params, dict):
            # Extract headers and d402 config if present (don't modify original)
            server_params_copy = server_params.copy()
            self._auth_headers = server_params_copy.pop("headers", {})
            self._d402_account = server_params_copy.pop("d402_account", None)
            self._d402_max_value = server_params_copy.pop("d402_max_value", None)
            
            # IMPORTANT: Also remove any x402_* parameters that shouldn't go to MCP library
            # The MCP library's streamablehttp_client() doesn't accept these
            server_params_copy.pop("x402_account", None)
            server_params_copy.pop("x402_max_value", None)
            
            # Determine connection mode
            if self._d402_account and D402_AVAILABLE:
                logger.info("💳 TraiaMCPAdapter: d402 payment protocol enabled")
                logger.info(f"   Client account: {self._d402_account.address}")
                logger.info(f"   Max value: {self._d402_max_value}")
                logger.info("   Applying httpx monkey-patch for d402 hooks...")
                # Apply d402 payment hooks patch
                self._apply_d402_patch()
                logger.info("   ✅ Monkey-patch applied - ALL new httpx clients will have d402 hooks")
            elif self._auth_headers:
                logger.info(f"TraiaMCPAdapter: Headers configured: {list(self._auth_headers.keys())}")
                # Apply header injection patch
                self._apply_httpx_patch()
            
            # Pass clean params to parent - this will create the MCP client
            logger.info("   Creating parent MCPServerAdapter...")
            super().__init__(server_params_copy, *tool_names)
            logger.info("   ✅ Parent MCPServerAdapter created")
        else:
            # Non-dict params, no headers or payment possible
            self._auth_headers = {}
            self._d402_account = None
            self._d402_max_value = None
            super().__init__(server_params, *tool_names)
    
    def _apply_httpx_patch(self):
        """Monkey-patch httpx.AsyncClient to inject headers."""
        original_init = httpx.AsyncClient.__init__
        auth_headers = self._auth_headers
        
        @wraps(original_init)
        def patched_init(client_self, *args, **kwargs):
            # Get existing headers
            existing_headers = kwargs.get('headers', {})
            if isinstance(existing_headers, dict):
                # Merge our headers
                merged_headers = {**auth_headers, **existing_headers}
                kwargs['headers'] = merged_headers
                logger.debug(f"Injected headers into httpx.AsyncClient: {list(auth_headers.keys())}")
            
            # Also ensure headers are preserved on redirects
            if 'follow_redirects' not in kwargs:
                kwargs['follow_redirects'] = True
            
            # Call original init
            original_init(client_self, *args, **kwargs)
        
        # Apply the patch
        httpx.AsyncClient.__init__ = patched_init
        self._original_httpx_init = original_init
        logger.debug("Applied httpx.AsyncClient monkey patch for headers")
    
    def _apply_d402_patch(self):
        """Monkey-patch httpx.AsyncClient to add d402 payment hooks."""
        if not D402_AVAILABLE:
            raise ImportError("d402 payment hooks not available. Ensure traia_iatp.d402 is installed.")
        
        original_init = httpx.AsyncClient.__init__
        d402_account = self._d402_account  # Keep variable name for compatibility
        d402_max_value = self._d402_max_value
        
        @wraps(original_init)
        def patched_init(client_self, *args, **kwargs):
            # Log client creation
            import traceback
            creation_stack = ''.join(traceback.format_stack()[-4:-1])
            logger.info(f"🔨 httpx.AsyncClient.__init__ called")
            logger.debug(f"   Creation stack: {creation_stack}")
            
            # Call original init first
            original_init(client_self, *args, **kwargs)
            
            # Add d402 payment hooks to the client
            if d402_account:
                try:
                    hooks = d402_payment_hooks(d402_account, max_value=d402_max_value)
                    # Merge with existing hooks if any
                    if hasattr(client_self, 'event_hooks') and client_self.event_hooks:
                        # Merge hooks
                        for event_type, handlers in hooks.items():
                            if event_type in client_self.event_hooks:
                                client_self.event_hooks[event_type].extend(handlers)
                            else:
                                client_self.event_hooks[event_type] = handlers
                    else:
                        client_self.event_hooks = hooks
                    
                        logger.info(f"✅ Applied d402 payment hooks to httpx.AsyncClient")
                        logger.info(f"   Account: {d402_account.address[:10]}...")
                        logger.info(f"   Hooks: {list(hooks.keys())}")
                except Exception as e:
                    logger.error(f"❌ Failed to apply d402 hooks: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    raise
        
        # Apply the patch
        httpx.AsyncClient.__init__ = patched_init
        self._original_httpx_init = original_init
        logger.debug("Applied httpx.AsyncClient monkey patch for d402 payments")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and restore original httpx if patched."""
        # Restore original httpx.AsyncClient.__init__ if we patched it
        if hasattr(self, '_original_httpx_init'):
            httpx.AsyncClient.__init__ = self._original_httpx_init
            logger.debug("Restored original httpx.AsyncClient")
        
        # Call parent exit
        return super().__exit__(exc_type, exc_val, exc_tb)
    
    def __enter__(self) -> List[BaseTool]:
        """Enter context manager."""
        if self._d402_account:
            logger.debug(f"TraiaMCPAdapter: Using d402 payment connection")
        elif self._auth_headers:
            logger.debug(f"TraiaMCPAdapter: Using authenticated connection")
        
        return super().__enter__()


def create_mcp_adapter(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    transport: str = "streamable-http",
    tool_names: Optional[List[str]] = None,
    x402_account: Optional[Any] = None,
    x402_max_value: Optional[int] = None
) -> TraiaMCPAdapter:
    """
    Create a Traia MCP adapter with optional headers and/or d402 payment support.
    
    Args:
        url: MCP server URL
        headers: Optional dictionary of headers to include in requests
        transport: Transport type (default: streamable-http)
        tool_names: Optional list of tool names to filter
        x402_account: Optional eth_account.Account for d402 payment protocol
        x402_max_value: Optional maximum payment value in base units.
                       Typically, each MCP server uses one primary token, so this limit
                       applies to all endpoints using that token. Set based on the token's
                       base units (e.g., USDC with 6 decimals: $1.00 = 1_000_000).
    
    Returns:
        TraiaMCPAdapter configured with headers and/or d402 payments
    
    Example:
        ```python
        # With headers (authenticated)
        adapter = create_mcp_adapter(
            url="https://news-mcp.example.com/mcp",
            headers={"Authorization": "Bearer YOUR_API_KEY"}
        )
        
        # With d402 payments
        from eth_account import Account
        account = Account.from_key("0x...")
        adapter = create_mcp_adapter(
            url="https://news-mcp.example.com/mcp",
            x402_account=account,
            x402_max_value=1_000_000  # $1.00 in USDC (6 decimals)
        )
        
        # Without headers or payment (standard)
        adapter = create_mcp_adapter(
            url="https://news-mcp.example.com/mcp"
        )
        
        with adapter as tools:
            agent = Agent(tools=tools)
        ```
    """
    server_params = {
        "url": url,
        "transport": transport
    }
    
    if headers:
        server_params["headers"] = headers
    
    if x402_account:
        server_params["d402_account"] = x402_account  # Use d402_ internally
        if x402_max_value is not None:
            server_params["d402_max_value"] = x402_max_value  # Use d402_ internally
    
    if tool_names:
        return TraiaMCPAdapter(server_params, *tool_names)
    else:
        return TraiaMCPAdapter(server_params)


def create_mcp_adapter_with_auth(
    url: str,
    api_key: str,
    auth_header: str = "Authorization",
    auth_prefix: str = "Bearer",
    transport: str = "streamable-http",
    tool_names: Optional[List[str]] = None
) -> TraiaMCPAdapter:
    """
    Create a Traia MCP adapter with authentication.
    
    Args:
        url: MCP server URL
        api_key: API key for authentication
        auth_header: Header name for auth (default: Authorization)
        auth_prefix: Auth scheme prefix (default: Bearer)
        transport: Transport type (default: streamable-http)
        tool_names: Optional list of tool names to filter
    
    Returns:
        TraiaMCPAdapter configured with auth headers
    
    Example:
        ```python
        adapter = create_mcp_adapter_with_auth(
            url="https://news-mcp.example.com/mcp",
            api_key="your-api-key"
        )
        
        with adapter as tools:
            # Tools will include Authorization header in all requests
            agent = Agent(tools=tools)
        ```
    """
    headers = {}
    if auth_prefix:
        headers[auth_header] = f"{auth_prefix} {api_key}"
    else:
        headers[auth_header] = api_key
    
    return create_mcp_adapter(url, headers, transport, tool_names)


def create_mcp_adapter_with_x402(
    url: str,
    account: Any,
    max_value: Optional[int] = None,
    transport: str = "streamable-http",
    tool_names: Optional[List[str]] = None
) -> TraiaMCPAdapter:
    """
    Create a Traia MCP adapter with d402 payment protocol support.
    
    Note: Function name uses "x402" for backward compatibility, but it uses
    the d402 implementation from traia_iatp.d402.
    
    Args:
        url: MCP server URL
        account: eth_account.Account instance for signing payments
        max_value: Optional maximum allowed payment amount in base units.
                   Typically, each MCP server uses one primary token, so this limit
                   applies to all endpoints using that token. Set based on the token's
                   base units (e.g., USDC with 6 decimals: $1.00 = 1_000_000).
        transport: Transport type (default: streamable-http)
        tool_names: Optional list of tool names to filter
    
    Returns:
        TraiaMCPAdapter configured with d402 payment hooks
    
    Example:
        ```python
        from eth_account import Account
        
        account = Account.from_key("0x...")
        adapter = create_mcp_adapter_with_x402(
            url="https://news-mcp.example.com/mcp",
            account=account,
            max_value=1_000_000  # $1.00 in USDC (6 decimals) - adjust for your server's token
        )
        
        with adapter as tools:
            # Tools will automatically handle 402 Payment Required responses
            agent = Agent(tools=tools)
        ```
    """
    if not D402_AVAILABLE:
        raise ImportError(
            "d402 payment hooks not available. Ensure traia_iatp.d402 is installed."
        )
    
    return create_mcp_adapter(
        url=url,
        transport=transport,
        tool_names=tool_names,
        x402_account=account,  # Function param uses x402 for backward compat
        x402_max_value=max_value  # Will be converted to d402 internally
    )


# Backwards compatibility aliases
HeaderMCPAdapter = TraiaMCPAdapter
create_mcp_adapter_with_headers = create_mcp_adapter


# Usage examples
USAGE_GUIDE = """
TraiaMCPAdapter Usage Guide
==========================

The TraiaMCPAdapter seamlessly handles both authenticated and non-authenticated
MCP connections. It extracts headers from server_params and injects them into
all HTTP requests when using streamable-http transport.

Basic Usage
-----------
```python
from traia_iatp.mcp import TraiaMCPAdapter

# Standard connection (no authentication)
server_params = {
    "url": "http://localhost:8000/mcp",
    "transport": "streamable-http"
}

# Authenticated connection
server_params = {
    "url": "http://localhost:8000/mcp",
    "transport": "streamable-http",
    "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
    }
}

# Use the same way regardless of authentication
with TraiaMCPAdapter(server_params) as tools:
    agent = Agent(
        role="My Agent",
        tools=tools
    )
```

Using Helper Functions
----------------------
```python
from traia_iatp.mcp import create_mcp_adapter_with_auth

# Create authenticated adapter
adapter = create_mcp_adapter_with_auth(
    url="http://localhost:8000/mcp",
    api_key="your-api-key"
)

with adapter as tools:
    # Use authenticated tools
    pass
```

Multiple Headers
----------------
```python
adapter = create_mcp_adapter(
    url="http://localhost:8000/mcp",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "X-API-Version": "v1",
        "X-Client-ID": "my-client"
    }
)
```

With Tool Filtering
-------------------
```python
adapter = create_mcp_adapter_with_auth(
    url="http://localhost:8000/mcp",
    api_key="your-api-key",
    tool_names=["search_news", "get_api_info"]
)
```

Server-Side Authentication
--------------------------
For MCP servers that require authentication, implement FastMCP middleware:

```python
from fastmcp import FastMCP, Context
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_request, get_context
from starlette.requests import Request

class AuthMiddleware(Middleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        try:
            # Access the raw HTTP request
            request: Request = get_http_request()
            
            # Extract bearer token from Authorization header
            auth = request.headers.get("Authorization", "")
            token = auth[7:].strip() if auth.lower().startswith("bearer ") else None
            
            if not token:
                # Check x-api-key header as alternative (case-insensitive)
                token = request.headers.get("x-api-key", "")
            
            if token:
                # Store the API key in the context state
                if hasattr(context, 'state'):
                    context.state.api_key = token
                else:
                    # Try to store it in the request state as fallback
                    request.state.api_key = token
        except Exception as e:
            logger.debug(f"Could not extract API key from request: {e}")
        
        return await call_next(context)

mcp = FastMCP("My Server", middleware=[AuthMiddleware()])

def get_session_api_key(context: Context) -> Optional[str]:
    '''Get the API key for the current session.'''
    try:
        # Try to get the API key from the context state
        if hasattr(context, 'state') and hasattr(context.state, 'api_key'):
            return context.state.api_key
        
        # Fallback: try to get it from the current HTTP request
        try:
            request: Request = get_http_request()
            if hasattr(request.state, 'api_key'):
                return request.state.api_key
        except Exception:
            pass
        
        # If we're in a tool context, try to get the context using the dependency
        try:
            ctx = get_context()
            if hasattr(ctx, 'state') and hasattr(ctx.state, 'api_key'):
                return ctx.state.api_key
        except Exception:
            pass
    except Exception as e:
        logger.debug(f"Could not retrieve API key from context: {e}")
    
    return None
```

Note: Headers are only applicable for streamable-http transport.
For stdio or SSE transports, authentication must be handled differently.
"""


__all__ = [
    'TraiaMCPAdapter',
    'HeaderMCPAdapter',  # Alias for backward compatibility
    'create_mcp_adapter',
    'create_mcp_adapter_with_auth',
    'create_mcp_adapter_with_x402',
    'create_mcp_adapter_with_headers',  # Alias
    'USAGE_GUIDE'
] 