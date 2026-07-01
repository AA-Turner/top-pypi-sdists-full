"""D402 payment middleware for various server frameworks.

This module provides framework-specific middleware implementations for the d402
payment protocol. Each framework has its own module with appropriate middleware.

Supported frameworks:
- Starlette: For Starlette-based applications (including FastMCP)
- FastAPI: For FastAPI applications  
- MCP: For Model Context Protocol (MCP) servers with tool decorators

Usage examples:

1. MCP Server (FastMCP):
    from traia_iatp.d402.servers import D402PaymentMiddleware, require_payment_for_tool
    
    app = mcp.streamable_http_app()
    app.add_middleware(D402PaymentMiddleware, ...)

2. FastAPI Server:
    from traia_iatp.d402.servers.fastapi import D402FastAPIMiddleware, require_payment
    
    app = FastAPI()
    middleware = D402FastAPIMiddleware(...)
    middleware.add_to_app(app)

3. Starlette Server:
    from traia_iatp.d402.servers import D402PaymentMiddleware
    
    app = Starlette()
    app.add_middleware(D402PaymentMiddleware, ...)
"""

from .starlette import (
    D402PaymentMiddleware,
    require_payment,
    extract_payment_configs,
    build_payment_config,
)
from .mcp import (
    EndpointPaymentInfo,
    get_active_api_key,
    require_payment_for_tool,
    settle_payment,
)

__all__ = [
    # Starlette middleware (works for any Starlette-based app)
    "D402PaymentMiddleware",
    
    # Generic decorators and extractors (for any server type)
    "require_payment",
    "extract_payment_configs",
    "build_payment_config",
    
    # MCP-specific helpers (wraps require_payment for MCP tools)
    "EndpointPaymentInfo",
    "get_active_api_key",
    "require_payment_for_tool",
    "settle_payment",
]

