"""FastAPI middleware for d402 payment protocol.

This module provides FastAPI-specific middleware for the d402 payment protocol.
Since FastAPI is built on Starlette, this middleware wraps the Starlette middleware
with FastAPI-friendly configuration and decorators.

Example usage:

```python
from fastapi import FastAPI
from traia_iatp.d402.servers.fastapi import D402FastAPIMiddleware, require_payment

app = FastAPI()

# Add payment middleware
middleware = D402FastAPIMiddleware(
    server_address="0x...",
    internal_api_key="your_api_key",
    facilitator_url="https://facilitator.d402.net"
)
middleware.add_to_app(app)

# Protect specific endpoints with payment
@app.post("/api/analyze")
@require_payment(price_usd=0.01, description="Sentiment analysis")
async def analyze(request: Request):
    return {"result": "analysis complete"}
```
"""

import logging
import os
from typing import Dict, Any, Optional, Callable, List
from functools import wraps

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .starlette import D402PaymentMiddleware
from ..types import TokenAmount, TokenAsset, EIP712Domain, PaymentRequirements
from ..common import process_price_to_atomic_amount

logger = logging.getLogger(__name__)


class D402FastAPIMiddleware:
    """
    FastAPI-specific wrapper for d402 payment middleware.
    
    This class provides a FastAPI-friendly interface to the underlying
    Starlette middleware, with additional utilities for route protection.
    
    Usage:
        middleware = D402FastAPIMiddleware(
            server_address="0x...",
            internal_api_key="your_key",
            facilitator_url="https://facilitator.example.com"
        )
        middleware.add_to_app(app)
    """
    
    def __init__(
        self,
        server_address: str,
        requires_auth: bool = False,
        internal_api_key: Optional[str] = None,
        testing_mode: bool = False,
        facilitator_url: Optional[str] = None,
        facilitator_api_key: Optional[str] = None,
        server_name: Optional[str] = None,
        protected_paths: Optional[List[str]] = None
    ):
        """Initialize FastAPI middleware.
        
        Args:
            server_address: Address where payments should be sent
            requires_auth: Whether server accepts API keys for free access
            internal_api_key: Server's internal API key (used when client pays)
            testing_mode: If True, skip facilitator verification
            facilitator_url: URL of the payment facilitator
            facilitator_api_key: API key for facilitator authentication
            server_name: Name/ID of this server for tracking
            protected_paths: List of path patterns that require payment (e.g., ["/api/*"])
        """
        self.server_address = server_address
        self.requires_auth = requires_auth
        self.internal_api_key = internal_api_key
        self.testing_mode = testing_mode
        self.facilitator_url = facilitator_url
        self.facilitator_api_key = facilitator_api_key
        self.server_name = server_name
        self.protected_paths = protected_paths or []
        
        # Tool payment configs will be populated by decorators
        self.tool_payment_configs: Dict[str, Dict[str, Any]] = {}
    
    def add_to_app(self, app: FastAPI):
        """Add the d402 payment middleware to a FastAPI app.
        
        Args:
            app: FastAPI application instance
        """
        app.add_middleware(
            D402PaymentMiddleware,
            tool_payment_configs=self.tool_payment_configs,
            server_address=self.server_address,
            requires_auth=self.requires_auth,
            internal_api_key=self.internal_api_key,
            testing_mode=self.testing_mode,
            facilitator_url=self.facilitator_url,
            facilitator_api_key=self.facilitator_api_key,
            server_name=self.server_name
        )
        logger.info(f"✅ D402 payment middleware added to FastAPI app")
        logger.info(f"   Server address: {self.server_address}")
        logger.info(f"   Testing mode: {self.testing_mode}")
    
    def register_endpoint(
        self,
        path: str,
        price_wei: str,
        token_address: str,
        network: str,
        description: str = ""
    ):
        """Register an endpoint that requires payment.
        
        Args:
            path: Endpoint path (e.g., "/api/analyze")
            price_wei: Price in wei (smallest unit of token)
            token_address: Token contract address
            network: Network name (e.g., "sepolia", "base-mainnet")
            description: Description of the service
        """
        self.tool_payment_configs[path] = {
            "price_wei": price_wei,
            "token_address": token_address,
            "network": network,
            "description": description,
            "server_address": self.server_address
        }
        logger.info(f"📝 Registered payment endpoint: {path} (price: {price_wei} wei)")


def require_payment(
    price_usd: Optional[float] = None,
    price_wei: Optional[str] = None,
    token_address: Optional[str] = None,
    network: str = "sepolia",
    description: str = ""
):
    """
    Decorator to mark a FastAPI endpoint as requiring payment.
    
    Can specify price in USD (will use default USDC) or in wei with custom token.
    
    Usage with USD:
        @app.post("/api/analyze")
        @require_payment(price_usd=0.01, description="Sentiment analysis")
        async def analyze():
            return {"result": "done"}
    
    Usage with custom token:
        @app.post("/api/analyze")
        @require_payment(
            price_wei="1000",
            token_address="0x...",
            network="base-mainnet",
            description="Sentiment analysis"
        )
        async def analyze():
            return {"result": "done"}
    
    Args:
        price_usd: Price in USD (uses default USDC token)
        price_wei: Price in wei (smallest unit of token)
        token_address: Token contract address (required if price_wei is set)
        network: Network name (default: "sepolia")
        description: Description of the service
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable):
        # Store payment metadata on function
        if price_usd is not None:
            # Convert USD to wei using default USDC
            from ..common import process_price_to_atomic_amount
            from ..types import Money
            
            price = Money(usd=str(price_usd))
            wei_amount, asset_addr, eip712_domain = process_price_to_atomic_amount(price, network)
            
            func._d402_payment_config = {
                "price_wei": wei_amount,
                "token_address": asset_addr,
                "network": network,
                "description": description or f"API call: {func.__name__}"
            }
        elif price_wei is not None and token_address is not None:
            # Use custom token and price
            func._d402_payment_config = {
                "price_wei": price_wei,
                "token_address": token_address,
                "network": network,
                "description": description or f"API call: {func.__name__}"
            }
        else:
            raise ValueError("Must specify either price_usd or (price_wei + token_address)")
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Payment is handled by middleware
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def get_api_key(request: Request) -> Optional[str]:
    """
    Get the active API key for the current request.
    
    This returns the API key that was resolved by the payment middleware:
    - Client's API key if they provided one (Mode 1: Free)
    - Server's API key if client paid (Mode 2: Paid)
    
    Usage:
        @app.post("/api/analyze")
        async def analyze(request: Request):
            api_key = get_api_key(request)
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.example.com", headers=headers)
            return response.json()
    
    Args:
        request: FastAPI request object
        
    Returns:
        API key string if available, None otherwise
    """
    if hasattr(request.state, 'api_key_to_use'):
        return request.state.api_key_to_use
    return None


__all__ = [
    "D402FastAPIMiddleware",
    "require_payment",
    "get_api_key",
]

