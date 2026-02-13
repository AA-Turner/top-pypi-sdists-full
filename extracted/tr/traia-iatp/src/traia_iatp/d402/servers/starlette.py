"""
Starlette middleware for d402 payment protocol.

This middleware works with Starlette apps (including FastMCP's streamable_http_app())
to provide HTTP 402 payment support and authentication.

Can be used for:
- Starlette applications
- FastAPI applications (FastAPI is built on Starlette)
- FastMCP servers (FastMCP uses Starlette for HTTP transport)
- A2A servers (Agent-to-Agent protocol)
- Any ASGI application using Starlette middleware

Pattern:
1. Use @require_payment decorator to mark endpoints
2. Extract payment configs with extract_payment_configs()
3. Add middleware with extracted configs
"""

import logging
import json
import os
from typing import Dict, Any, Optional, Callable
from functools import wraps

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..types import PaymentRequirements, d402PaymentRequiredResponse, PaymentPayload, TokenAmount
from ..common import d402_VERSION
from ..facilitator import IATPSettlementFacilitator
from ..encoding import safe_base64_decode

logger = logging.getLogger(__name__)


# ============================================================================
# URL EXTRACTION HELPERS
# ============================================================================

def extract_server_url_from_request(request: Request) -> str:
    """
    Extract the server's own URL from the HTTP request headers.
    
    This is used for tracking in the facilitator which server a payment came from.
    Works for both local and remote (Cloud Run) deployments.
    
    Args:
        request: Starlette Request object
        
    Returns:
        Full server URL (e.g., 'https://my-server.cloudrun.app' or 'http://localhost:8000')
    """
    # Check X-Forwarded headers first (set by proxies/load balancers like Cloud Run)
    forwarded_proto = request.headers.get("X-Forwarded-Proto", "http")
    forwarded_host = request.headers.get("X-Forwarded-Host")
    
    if forwarded_host:
        # Cloud Run / proxy scenario
        server_url = f"{forwarded_proto}://{forwarded_host}"
        logger.debug(f"Server URL from X-Forwarded headers: {server_url}")
        return server_url
    
    # Fallback to Host header (for local/direct access)
    host = request.headers.get("Host", "localhost:8000")
    
    # Determine protocol (https if forwarded, otherwise check if local)
    if "localhost" in host or "127.0.0.1" in host or "host.docker.internal" in host:
        proto = "http"
    else:
        # Remote host without X-Forwarded-Proto, assume https
        proto = "https"
    
    server_url = f"{proto}://{host}"
    logger.debug(f"Server URL from Host header: {server_url}")
    return server_url


# ============================================================================
# DECORATORS - Generic payment requirement markers
# ============================================================================

def require_payment(
    price: TokenAmount,
    endpoint_path: str = "",
    description: str = ""
) -> Callable:
    """
    Decorator to mark an endpoint as requiring D402 payment.
    
    Works with any function/endpoint - not specific to MCP or A2A.
    
    Usage with FastAPI/Starlette:
        @app.post("/analyze")
        @require_payment(
            price=TokenAmount(
                amount="10000",
                asset=TokenAsset(address="0x...", decimals=6, network="sepolia")
            ),
            endpoint_path="/analyze",
            description="Analyze text"
        )
        async def analyze(request: Request):
            ...
    
    Usage with A2A handlers:
        @require_payment(
            price=TokenAmount(...),
            endpoint_path="/",
            description="A2A JSON-RPC request"
        )
        async def handle_a2a_request(request: Request):
            ...
    
    Args:
        price: TokenAmount specifying the payment amount and token
        endpoint_path: The endpoint path (e.g., "/analyze", "/"). Auto-detected if empty.
        description: Human-readable description of what the endpoint does
    
    Returns:
        Decorator function that adds payment metadata to the function
    """
    def decorator(func: Callable) -> Callable:
        # Store payment metadata on the function
        if not hasattr(func, '_d402_payment_info'):
            func._d402_payment_info = {}
        
        func._d402_payment_info = {
            'price': price,
            'endpoint_path': endpoint_path,
            'description': description,
            'requires_payment': True
        }
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        
        # Preserve metadata on wrapper
        wrapper._d402_payment_info = func._d402_payment_info
        
        return wrapper
    
    return decorator


def extract_payment_configs(
    app: Any,
    server_address: str,
    endpoint_mapping: Optional[Dict[str, str]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Extract payment configs from decorated endpoints in any app.
    
    Works with:
    - FastAPI apps
    - Starlette apps  
    - A2A handlers
    - Custom routers
    
    Args:
        app: The application or handler object to extract from
        server_address: Payment destination address
        endpoint_mapping: Optional mapping of function names to endpoint paths
                         (useful when path can't be auto-detected)
    
    Returns:
        Dict mapping endpoint paths to payment configs
    
    Example:
        # Extract from FastAPI app
        configs = extract_payment_configs(app, SERVER_ADDRESS)
        
        # Extract from A2A handlers (with manual mapping)
        configs = extract_payment_configs(
            a2a_handlers,
            SERVER_ADDRESS,
            endpoint_mapping={"handle_request": "/"}
        )
    """
    configs = {}
    endpoint_mapping = endpoint_mapping or {}
    
    # Try to extract from FastAPI/Starlette routes
    if hasattr(app, 'routes'):
        for route in app.routes:
            if hasattr(route, 'endpoint'):
                endpoint_func = route.endpoint
                if hasattr(endpoint_func, '_d402_payment_info'):
                    info = endpoint_func._d402_payment_info
                    path = info.get('endpoint_path') or getattr(route, 'path', '/')
                    
                    configs[path] = build_payment_config(
                        price=info['price'],
                        server_address=server_address,
                        description=info.get('description', f"Request to {path}")
                    )
    
    # Try to extract from dict/module of handlers
    elif hasattr(app, '__dict__'):
        for name, func in app.__dict__.items():
            if hasattr(func, '_d402_payment_info'):
                info = func._d402_payment_info
                path = info.get('endpoint_path') or endpoint_mapping.get(name, f"/{name}")
                
                configs[path] = build_payment_config(
                    price=info['price'],
                    server_address=server_address,
                    description=info.get('description', f"Request to {path}")
                )
    
    # Handle direct function (single handler case)
    elif hasattr(app, '_d402_payment_info'):
        info = app._d402_payment_info
        path = info.get('endpoint_path') or endpoint_mapping.get('default', '/')
        
        configs[path] = build_payment_config(
            price=info['price'],
            server_address=server_address,
            description=info.get('description', f"Request to {path}")
        )
    
    return configs


def build_payment_config(
    price: TokenAmount,
    server_address: str,
    description: str
) -> Dict[str, Any]:
    """
    Build payment config dict from TokenAmount.
    
    Converts a TokenAmount object into the standard payment config format
    used by D402PaymentMiddleware.
    
    Args:
        price: TokenAmount with payment amount and token details
        server_address: Payment destination address
        description: Human-readable description of the endpoint
    
    Returns:
        Dict with payment configuration
    
    Example:
        from traia_iatp.d402 import D402PriceBuilder
        from traia_iatp.d402.servers import build_payment_config
        
        builder = D402PriceBuilder(...)
        price = builder.create_price(0.01)
        
        config = build_payment_config(
            price=price,
            server_address="0x...",
            description="API request"
        )
        # Returns: {"price_wei": "10000", "token_address": "0x...", ...}
    """
    return {
        "price_wei": price.amount,
        "price_float": float(price.amount) / (10 ** price.asset.decimals),
        "token_address": price.asset.address,
        "token_symbol": getattr(price.asset, 'symbol', 'TOKEN'),
        "token_decimals": price.asset.decimals,
        "network": price.asset.network,
        "server_address": server_address,
        "description": description,
        "eip712_domain": {
            "name": price.asset.eip712.name,
            "version": price.asset.eip712.version
        }
    }


# ============================================================================
# MIDDLEWARE - D402 Payment Enforcement
# ============================================================================


class D402PaymentMiddleware(BaseHTTPMiddleware):
    """
    Universal D402 payment middleware for any Starlette-based server.
    
    This middleware:
    1. Extracts API key if present → stores in request.state
    2. Checks if endpoint requires payment
    3. Returns HTTP 402 if no payment (and no API key if auth enabled)
    4. Validates payment with facilitator
    5. Settles payment after successful response
    
    Supports:
    - MCP servers (POST /mcp with tools/call)
    - A2A servers (POST / with JSON-RPC)
    - FastAPI/Starlette servers (any POST endpoint)
    - Multiple endpoints with different prices
    
    Usage Pattern 1 - MCP Servers (with decorators):
        from traia_iatp.d402.starlette_middleware import D402PaymentMiddleware
        from traia_iatp.d402.payment_introspection import extract_payment_configs_from_mcp
        
        configs = extract_payment_configs_from_mcp(mcp, SERVER_ADDRESS)
        app.add_middleware(
            D402PaymentMiddleware,
            server_address=SERVER_ADDRESS,
            tool_payment_configs=configs,
            requires_auth=True,
            internal_api_key=API_KEY
        )
    
    Usage Pattern 2 - A2A Servers (manual config):
        from traia_iatp.d402.servers import D402PaymentMiddleware
        from traia_iatp.d402.servers.starlette import build_payment_config
        
        configs = {
            "/": build_payment_config(
                price=TokenAmount(...),
                server_address=SERVER_ADDRESS,
                description="A2A request"
            )
        }
        
        app.add_middleware(
            D402PaymentMiddleware,
            server_address=SERVER_ADDRESS,
            tool_payment_configs=configs,
            requires_auth=False  # Payment only
        )
    
    Usage Pattern 3 - General Servers (with decorators - future):
        from traia_iatp.d402.servers import (
            D402PaymentMiddleware,
            require_payment,
            extract_payment_configs
        )
        
        @app.post("/analyze")
        @require_payment(price=TokenAmount(...), description="Analysis")
        async def analyze(): pass
        
        configs = extract_payment_configs(app, SERVER_ADDRESS)
        app.add_middleware(
            D402PaymentMiddleware,
            server_address=SERVER_ADDRESS,
            tool_payment_configs=configs
        )
    """
    
    def __init__(
        self,
        app,
        server_address: str,
        # Payment configs (from decorators or manual)
        tool_payment_configs: Dict[str, Dict[str, Any]],
        # Auth and facilitator config
        requires_auth: bool = False,
        internal_api_key: Optional[str] = None,
        testing_mode: bool = False,
        facilitator_url: Optional[str] = None,
        facilitator_api_key: Optional[str] = None,
        server_name: Optional[str] = None
    ):
        """
        Initialize D402 payment middleware.
        
        Args:
            app: Starlette/FastAPI app
            server_address: Payment destination address
            tool_payment_configs: Dict mapping endpoint paths to payment configs.
                                 Use extract_payment_configs() to generate from decorators.
            requires_auth: If True, accepts API key OR payment. If False, payment only.
            internal_api_key: Server's API key (used when client pays in payment mode)
            testing_mode: If True, skips facilitator (for local testing)
            facilitator_url: Facilitator service URL
            facilitator_api_key: API key for facilitator
            server_name: Server identifier for logging
        
        Example:
            # Option 1: Extract from decorators (recommended)
            configs = extract_payment_configs(app, SERVER_ADDRESS)
            app.add_middleware(
                D402PaymentMiddleware,
                server_address=SERVER_ADDRESS,
                tool_payment_configs=configs
            )
            
            # Option 2: Manual configs (MCP servers)
            configs = extract_payment_configs_from_mcp(mcp, SERVER_ADDRESS)
            app.add_middleware(
                D402PaymentMiddleware,
                server_address=SERVER_ADDRESS,
                tool_payment_configs=configs
            )
        """
        super().__init__(app)
        
        self.tool_payment_configs = tool_payment_configs or {}
        self.server_address = server_address
        self.requires_auth = requires_auth
        self.internal_api_key = internal_api_key  # Server's internal API key
        self.testing_mode = testing_mode or os.getenv("D402_TESTING_MODE", "false").lower() == "true"
        
        # Initialize facilitator for payment verification and settlement
        self.facilitator = None
        if not self.testing_mode:
            try:
                # Try multiple operator key env var names (for different server types)
                operator_key = (
                    os.getenv("UTILITY_AGENT_OPERATOR_PRIVATE_KEY") or  # A2A utility agents
                    os.getenv("MCP_OPERATOR_PRIVATE_KEY") or             # MCP servers
                    os.getenv("OPERATOR_PRIVATE_KEY")                    # Generic
                )
                
                # Get server name/ID from initialization or environment
                server_name_var = server_name or os.getenv("MCP_SERVER_NAME", os.getenv("MCP_SERVER_ID", "unknown"))
                
                # Note: server_url will be extracted from each request at runtime
                # This is needed because Cloud Run URLs are not known until deployment
                # and must be introspected from X-Forwarded-Host and X-Forwarded-Proto headers
                
                self.facilitator = IATPSettlementFacilitator(
                    facilitator_url=facilitator_url or os.getenv("D402_FACILITATOR_URL", "https://facilitator.d402.net"),
                    facilitator_api_key=facilitator_api_key or os.getenv("D402_FACILITATOR_API_KEY"),
                    provider_operator_key=operator_key,
                    server_name=server_name_var,
                    server_url=None  # Will be set per-request from headers
                )
                
                # Store server name for later use
                self.server_name = server_name_var
                if operator_key:
                    logger.info(f"  Facilitator initialized with operator key (settlement enabled)")
                else:
                    logger.warning(f"  No operator key - settlement disabled")
            except Exception as e:
                logger.warning(f"  Could not initialize facilitator: {e}")
                self.testing_mode = True
        
        logger.info(f"D402PaymentMiddleware initialized:")
        logger.info(f"  Payment-enabled endpoints: {len(self.tool_payment_configs)}")
        if self.tool_payment_configs:
            logger.info(f"  Protected paths: {list(self.tool_payment_configs.keys())}")
        logger.info(f"  Server address: {server_address}")
        logger.info(f"  Testing mode: {self.testing_mode}")
        logger.info(f"  Facilitator: {'Enabled' if self.facilitator else 'Disabled (testing)'}")
    
    async def __call__(self, scope, receive, send):
        """Override ASGI __call__ to add debug logging and ensure proper invocation."""
        logger.info(f"🔍 D402PaymentMiddleware.__call__ invoked: {scope.get('type', 'unknown')} {scope.get('path', 'unknown')}")
        
        # If not HTTP, pass through immediately
        if scope["type"] != "http":
            logger.debug(f"Non-HTTP scope type: {scope['type']}, passing through")
            await self.app(scope, receive, send)
            return
        
        logger.info(f"🔍 HTTP request detected, calling parent BaseHTTPMiddleware.__call__")
        # Call parent's __call__ which will invoke dispatch()
        return await super().__call__(scope, receive, send)
    
    async def dispatch(self, request: Request, call_next):
        """
        Intercept requests for auth and payment checking.
        
        Handles both:
        1. If server requires auth: Extract API key and store in request.state
        2. If tool requires payment: Check payment or auth, return HTTP 402 if missing
        """
        
        # Debug: Confirm dispatch is being called
        logger.info(f"🔍 D402 middleware dispatch called: {request.method} {request.url.path}")
        
        # Step 0: Skip payment processing on URLs that will redirect (trailing slash)
        # This prevents duplicate payments when /mcp/ redirects to /mcp
        if request.url.path.endswith('/') and request.url.path != '/':
            # This request will likely redirect, skip payment processing
            logger.debug(f"Skipping payment processing for trailing slash URL: {request.url.path}")
            return await call_next(request)
        
        # Step 1: Store middleware reference for decorator access (for settlement)
        request.state.d402_middleware = self
        
        # Step 2: Extract and store API key if present (for all requests)
        if self.requires_auth:
            auth = request.headers.get("Authorization", "")
            if auth:
                # Strip "Bearer " prefix if present, otherwise use raw value
                if auth.lower().startswith("bearer "):
                    token = auth[7:].strip()
                else:
                    token = auth.strip()
                request.state.api_key = token
                request.state.authenticated = True
                logger.debug(f"D402: API key stored from Authorization: {token[:10]}...")
            # Check for X-API-Key header (case-insensitive)
            elif request.headers.get("x-api-key"):  # Starlette headers are case-insensitive when using lowercase
                token = request.headers.get("x-api-key")
                request.state.api_key = token
                request.state.authenticated = True
                logger.debug(f"D402: X-API-Key stored: {token[:10]}...")
            else:
                request.state.api_key = None
                request.state.authenticated = False
        
        # Step 3: Check payment for API calls
        # Only intercept POST requests
        if request.method != "POST":
            return await call_next(request)
        
        # Check if this endpoint is protected
        request_path = request.url.path.rstrip('/') or '/'
        logger.debug(f"D402 middleware inspecting request path: {request_path}")
        
        # Skip if no payment configs
        if not self.tool_payment_configs:
            return await call_next(request)
        
        try:
            # Read body to identify the request
            body = await request.body()
            data = json.loads(body)
            
            # Determine endpoint type and extract identifier
            tool_name = None
            tool_path = request_path
            
            # MCP Pattern: /mcp with tools/call method
            if request_path == "/mcp" and data.get("method") == "tools/call":
                tool_name = data.get("params", {}).get("name")
                # For MCP servers: /mcp/tools/{tool_name}
                tool_path = f"/mcp/tools/{tool_name}"
            
            # A2A Pattern: / (root) with JSON-RPC methods
            # A2A uses methods like "message/send", "tasks/get", etc.
            elif request_path in self.tool_payment_configs:
                # Direct endpoint match (e.g., "/" for A2A)
                tool_name = request_path
                tool_path = request_path
            
            # Generic pattern: check if path matches any configured pattern
            elif "*" in self.tool_payment_configs:
                # Wildcard - protect all endpoints
                tool_name = "*"
                tool_path = request_path
            
            # If no tool/endpoint identified, pass through
            if not tool_name:
                logger.debug(f"D402 middleware: no payment config match for path '{request_path}', skipping")
                return await self._continue_with_body(request, body, call_next)
            
            # Check if tool requires payment
            if tool_name in self.tool_payment_configs:
                logger.debug(f"D402 middleware: enforcing payment for tool '{tool_name}'")
                # Mode 1: If server requires auth AND client has API key → FREE
                if self.requires_auth and request.state.authenticated:
                    logger.info(f"✅ {tool_name}: Client authenticated with API key (Mode 1: Free)")
                    # Set api_key_to_use = client's key
                    request.state.api_key_to_use = request.state.api_key
                    # Continue to FastMCP
                    return await self._continue_with_body(request, body, call_next)
                
                # Mode 2: No API key → Client must pay, server uses internal API key
                else:
                    payment_header = request.headers.get("X-Payment")
                    if not payment_header:
                        logger.info(f"💰 {tool_name}: Payment required (Mode 2) - HTTP 402")
                        config = self.tool_payment_configs[tool_name]
                        return self._create_402_response(config, "Payment required", request_path=tool_path)
                    else:
                        # Payment header present - VALIDATE IT!
                        logger.info(f"💰 {tool_name}: Payment header RECEIVED - validating...")
                        logger.info(f"📦 Payment header length: {len(payment_header)} bytes")
                        
                        # TODO: Add full payment validation:
                        # 1. Decode and parse payment header
                        # 2. Verify EIP-3009 signature
                        # 3. Check amount >= required
                        # 4. Verify pay_to == SERVER_ADDRESS
                        # 5. Check timestamp validity
                        # 6. Call facilitator.verify() if not testing mode
                        
                        # For now: Basic validation in testing mode
                        try:
                            from ..encoding import safe_base64_decode
                            payment_data = safe_base64_decode(payment_header)
                            if not payment_data:
                                logger.error(f"❌ {tool_name}: Invalid payment encoding")
                                # Return 402 with error
                                config = self.tool_payment_configs[tool_name]
                                return self._create_402_response(config, "Invalid payment encoding", request_path=tool_path)
                            
                            payment_dict = json.loads(payment_data)
                            
                            # Basic validation: check structure
                            if not payment_dict.get("payload") or not payment_dict["payload"].get("authorization"):
                                logger.error(f"❌ {tool_name}: Invalid payment structure")
                                config = self.tool_payment_configs[tool_name]
                                return self._create_402_response(config, "Invalid payment structure", request_path=tool_path)
                            
                            auth = payment_dict["payload"]["authorization"]
                            
                            # Verify payment destination
                            if auth.get("to", "").lower() != self.server_address.lower():
                                logger.error(f"❌ {tool_name}: Payment to wrong address")
                                config = self.tool_payment_configs[tool_name]
                                return self._create_402_response(config, "Payment to wrong address", request_path=tool_path)
                            
                            # Verify payment amount
                            config = self.tool_payment_configs[tool_name]
                            payment_amount = int(auth.get("value", 0))
                            required_amount = int(config["price_wei"])
                            
                            if payment_amount < required_amount:
                                logger.error(f"❌ {tool_name}: Insufficient payment: {payment_amount} < {required_amount}")
                                return self._create_402_response(config, f"Insufficient payment: {payment_amount} < {required_amount}", request_path=tool_path)
                            
                            # Call facilitator.verify() if available (production mode)
                            if self.facilitator and not self.testing_mode:
                                try:
                                    # Create PaymentPayload for facilitator
                                    payment_payload = PaymentPayload.model_validate(payment_dict)
                                    
                                    # Create PaymentRequirements with full token info
                                    # Include client information in extra field for facilitator tracking
                                    extra_data = {
                                        "client_url": request.headers.get("referer") or request.headers.get("origin"),
                                        "client_ip": request.client.host if request.client else None,
                                        "user_agent": request.headers.get("user-agent")
                                    }
                                    
                                    payment_reqs = PaymentRequirements(
                                        scheme="exact",
                                        network=config["network"],
                                        pay_to=config["server_address"],
                                        max_amount_required=config["price_wei"],
                                        max_timeout_seconds=86400,  # 24 hours for settlement window
                                        description=config["description"],
                                        resource=tool_path,
                                        mime_type="application/json",
                                        asset=config["token_address"],
                                        extra=extra_data
                                    )
                                    
                                    # Extract server's own URL from request headers for tracking
                                    server_url = extract_server_url_from_request(request)
                                    logger.info(f"🌐 Server URL (introspected): {server_url}")
                                    
                                    # Temporarily update facilitator's server_url for this request
                                    original_server_url = self.facilitator.server_url
                                    self.facilitator.server_url = server_url
                                    
                                    # Verify with facilitator
                                    logger.info(f"🔐 Verifying payment with facilitator...")
                                    #==============================================================
                                    verify_result = await self.facilitator.verify(payment_payload, payment_reqs)
                                    #==============================================================
                                    
                                    # Restore original server_url
                                    self.facilitator.server_url = original_server_url
                                    
                                    logger.info(f"🔐 Facilitator verify result: {verify_result}")
                                    if not verify_result.is_valid:
                                        logger.error(f"❌ {tool_name}: Facilitator rejected payment: {verify_result.invalid_reason}")
                                        return self._create_402_response(config, f"Payment verification failed: {verify_result.invalid_reason}", request_path=tool_path)
                                    
                                    # Store payment_uuid and facilitatorFeePercent for settlement
                                    request.state.payment_uuid = verify_result.payment_uuid
                                    request.state.facilitator_fee_percent = verify_result.facilitator_fee_percent or 250
                                    logger.info(f"✅ {tool_name}: Facilitator verified payment (UUID: {verify_result.payment_uuid[:20] if verify_result.payment_uuid else 'N/A'}...)")
                                    logger.info(f"   Facilitator fee: {request.state.facilitator_fee_percent} basis points")
                                    
                                except Exception as e:
                                    logger.error(f"❌ {tool_name}: Facilitator error: {e}")
                                    return self._create_402_response(config, f"Facilitator verification failed: {str(e)}", request_path=tool_path)
                            else:
                                logger.info(f"⚠️  {tool_name}: Testing mode - skipping facilitator verification")
                            
                            # Payment validated! Set api_key_to_use
                            logger.info(f"✅ {tool_name}: Payment VERIFIED successfully (Mode 2: Paid)")
                            logger.info(f"   Payment amount: {payment_amount} wei (required: {required_amount} wei)")
                            logger.info(f"   From (wallet): {auth.get('from', 'unknown')}")
                            logger.info(f"   To (provider): {auth.get('to', 'unknown')}")
                            request.state.api_key_to_use = self.internal_api_key
                            request.state.payment_validated = True
                            request.state.payment_dict = payment_dict
                            request.state.tool_name = tool_name  # Store for settlement
                            
                            # Store payment info for settlement
                            request.state.payment_payload = PaymentPayload.model_validate(payment_dict)
                            logger.info(f"💾 {tool_name}: Payment payload stored for settlement")
                            
                        except Exception as e:
                            logger.error(f"❌ {tool_name}: Payment validation error: {e}")
                            config = self.tool_payment_configs[tool_name]
                            return self._create_402_response(config, f"Payment validation failed: {str(e)}", request_path=tool_path)
            
            # Continue with reconstructed request
            response = await self._continue_with_body(request, body, call_next)
            
            # If payment was validated and response is successful, settle the payment
            if hasattr(request.state, 'payment_validated') and request.state.payment_validated:
                if 200 <= response.status_code < 300:
                    payment_uuid = getattr(request.state, 'payment_uuid', None)
                    
                    # Read response body ONCE (handle different response types)
                    response_body = b""
                    try:
                        # StreamingResponse has body_iterator, Response has body attribute
                        if hasattr(response, 'body_iterator'):
                            async for chunk in response.body_iterator:
                                response_body += chunk
                        elif hasattr(response, 'body'):
                            # Regular Response - body is bytes
                            response_body = response.body
                        else:
                            logger.warning("Response has no body_iterator or body attribute")
                            response_body = b""
                    except Exception as e:
                        logger.error(f"Error reading response body: {e}")
                        response_body = b""
                    
                    # Check if response contains errors - don't settle if upstream API failed
                    should_settle = True
                    try:
                        response_str = response_body.decode() if response_body else ""
                        # Check for MCP error indicators
                        if '"isError":true' in response_str or '"isError": true' in response_str:
                            logger.warning(f"⚠️  Tool returned isError=true - NOT settling payment")
                            should_settle = False
                        # Check for error field in response (indicates API failure)
                        elif '"error":' in response_str or '"error" :' in response_str:
                            logger.warning(f"⚠️  Tool response contains error field - NOT settling payment")
                            should_settle = False
                        # Check for HTTP error codes in response body (e.g., "401 Client Error", "500 Internal Server Error")
                        elif any(code in response_str for code in ['"401', '"403', '"404', '"500', '"502', '"503', 'Unauthorized', 'Forbidden', 'Internal Server Error']):
                            logger.warning(f"⚠️  Tool response contains HTTP error indicators - NOT settling payment")
                            should_settle = False
                        
                        # Recreate response for return with buffered body
                        from starlette.responses import Response
                        response = Response(
                            content=response_body,
                            status_code=response.status_code,
                            headers=dict(response.headers),
                            media_type=response.media_type
                        )
                    except Exception as e:
                        logger.error(f"Error checking response for errors: {e}")
                        # If we can't check, don't settle to be safe
                        should_settle = False
                    
                    if not should_settle:
                        logger.info(f"💳 Skipping settlement due to tool error")
                        return response
                    
                    logger.info(f"💳 Successful response with validated payment - triggering settlement")
                    logger.info(f"   Payment UUID: {payment_uuid}")
                    
                    # Trigger settlement asynchronously (fire-and-forget)
                    if payment_uuid and self.facilitator:
                        import asyncio
                        from .mcp import settle_payment, EndpointPaymentInfo
                        
                        # Parse for settlement (runs async after response sent)
                        async def do_settlement():
                            try:
                                logger.info(f"🚀 Background settlement started (async - client already has response)")
                                
                                # Parse response body
                                try:
                                    output_data = json.loads(response_body.decode())
                                except:
                                    output_data = {"response": response_body.decode() if response_body else "completed"}
                                
                                # Get tool config
                                tool_name = getattr(request.state, 'tool_name', 'unknown')
                                config = self.tool_payment_configs.get(tool_name, {})
                                
                                # Create endpoint info
                                endpoint_info = EndpointPaymentInfo(
                                    settlement_token_address=config.get("token_address"),
                                    settlement_token_network=config.get("network"),
                                    payment_price_float=float(config.get("price_wei", 0)) / 1e6,
                                    payment_price_wei=config.get("price_wei"),
                                    server_address=config.get("server_address")
                                )
                                
                                # Create context wrapper
                                class SettlementContext:
                                    class State:
                                        def __init__(self):
                                            self.payment_payload = getattr(request.state, 'payment_payload', None)
                                            self.payment_uuid = payment_uuid
                                            self.facilitator_fee_percent = getattr(request.state, 'facilitator_fee_percent', 250)
                                    
                                    def __init__(self):
                                        self.state = SettlementContext.State()
                                
                                settlement_ctx = SettlementContext()
                                
                                # Use actual response data for output hash
                                logger.info(f"📊 Using actual response data for settlement")
                                logger.info(f"   Output data size: {len(str(output_data))} chars")
                                
                                settlement_success = await settle_payment(
                                    context=settlement_ctx,
                                    endpoint_info=endpoint_info,
                                    output_data=output_data,
                                    middleware=self
                                )
                                
                                if settlement_success:
                                    logger.info(f"✅ Background settlement completed")
                                else:
                                    logger.warning(f"⚠️  Background settlement failed")
                                    
                            except Exception as e:
                                logger.error(f"❌ Settlement error: {e}")
                                import traceback
                                logger.error(traceback.format_exc())
                        
                        asyncio.create_task(do_settlement())
                        logger.info(f"📅 Settlement task scheduled - client gets response immediately")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in D402PaymentMiddleware: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # Continue on error
            return await call_next(request)
    
    async def _continue_with_body(self, request: Request, body: bytes, call_next):
        """Continue request processing with body we already read."""
        # Create new request with reconstructed receive
        async def receive():
            return {"type": "http.request", "body": body, "more_body": False}
        
        from starlette.requests import Request as NewRequest
        new_request = NewRequest(request.scope, receive)
        return await call_next(new_request)
    
    def _create_402_response(self, config: Dict[str, Any], error_message: str, request_path: str = "/mcp") -> JSONResponse:
        """Helper to create HTTP 402 response with request path."""
        # Include EIP712 domain in extra for client to sign payment
        # This should be IATPWallet domain (consumer's wallet contract)
        extra_data = config.get("eip712_domain", {
            "name": "IATPWallet",  # Consumer's wallet contract
            "version": "1"
        })
        
        logger.info(f"   🔧 Creating 402 response with resource: {request_path}")
        
        payment_req = PaymentRequirements(
            scheme="exact",
            network=config["network"],
            pay_to=config["server_address"],
            max_amount_required=config["price_wei"],
            max_timeout_seconds=86400,  # 24 hours for settlement window
            description=config["description"],
            resource=request_path,  # API path for resource identification
            mime_type="application/json",
            asset=config["token_address"],
            extra=extra_data  # EIP712 domain for signature
        )
        
        response_data = d402PaymentRequiredResponse(
            d402_version=d402_VERSION,
            accepts=[payment_req],
            error=error_message
        )
        
        return JSONResponse(
            status_code=402,
            content=response_data.model_dump(by_alias=True),
            headers={"Access-Control-Expose-Headers": "X-Payment-Response"}
        )


__all__ = [
    "D402PaymentMiddleware",
    "require_payment",
    "extract_payment_configs",
    "build_payment_config",
]

