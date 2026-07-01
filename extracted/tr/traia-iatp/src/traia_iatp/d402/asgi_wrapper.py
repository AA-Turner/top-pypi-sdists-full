"""
Raw ASGI wrapper for D402 payment enforcement.

This module provides a low-level ASGI wrapper that intercepts requests
BEFORE they reach any framework (Starlette, FastAPI, A2A, etc.).

Use this when BaseHTTPMiddleware doesn't work due to framework compatibility issues.
"""

import json
import logging
from typing import Dict, Any, Optional, Callable

from .types import PaymentRequirements, d402PaymentRequiredResponse, PaymentPayload
from .common import d402_VERSION
from .facilitator import IATPSettlementFacilitator
from .encoding import safe_base64_decode

logger = logging.getLogger(__name__)


def extract_server_url_from_scope(scope: dict) -> str:
    """
    Extract the server's own URL from ASGI scope headers.
    
    This is used for tracking in the facilitator which server a payment came from.
    Works for both local and remote (Cloud Run) deployments.
    
    Args:
        scope: ASGI scope dict with headers
        
    Returns:
        Full server URL (e.g., 'https://my-agent.cloudrun.app' or 'http://localhost:9001')
    """
    # Parse headers (list of tuples of bytes)
    headers = dict(scope.get("headers", []))
    
    # Check X-Forwarded headers first (set by proxies/load balancers like Cloud Run)
    forwarded_proto = headers.get(b"x-forwarded-proto", b"http").decode()
    forwarded_host = headers.get(b"x-forwarded-host", b"").decode()
    
    if forwarded_host:
        # Cloud Run / proxy scenario
        server_url = f"{forwarded_proto}://{forwarded_host}"
        logger.debug(f"Server URL from X-Forwarded headers: {server_url}")
        return server_url
    
    # Fallback to Host header (for local/direct access)
    host = headers.get(b"host", b"localhost:9001").decode()
    
    # Determine protocol
    if "localhost" in host or "127.0.0.1" in host or "host.docker.internal" in host:
        proto = "http"
    else:
        # Remote host without X-Forwarded-Proto, assume https
        proto = "https"
    
    server_url = f"{proto}://{host}"
    logger.debug(f"Server URL from Host header: {server_url}")
    return server_url


class D402ASGIWrapper:
    """
    Raw ASGI wrapper for D402 payment enforcement.
    
    This wraps any ASGI application and intercepts requests at the lowest level,
    before any framework processing occurs. Guaranteed to work regardless of
    framework quirks.
    
    Usage:
        starlette_app = app.build()
        wrapped_app = D402ASGIWrapper(
            app=starlette_app,
            server_address="0x123...",
            endpoint_payment_configs={"/a2a": {...}},
            facilitator_url="http://localhost:7070"
        )
        uvicorn.run(wrapped_app, ...)
    """
    
    def __init__(
        self,
        app: Callable,  # Any ASGI app
        server_address: str,
        endpoint_payment_configs: Dict[str, Dict[str, Any]],
        requires_auth: bool = False,
        internal_api_key: Optional[str] = None,
        testing_mode: bool = False,
        facilitator_url: Optional[str] = None,
        facilitator_api_key: Optional[str] = None,
        server_name: Optional[str] = None
    ):
        """
        Initialize D402 ASGI wrapper.
        
        Args:
            app: The ASGI application to wrap
            server_address: Payment destination address
            endpoint_payment_configs: Dict mapping paths to payment configs
            requires_auth: If True, accepts API key OR payment
            internal_api_key: Server's API key
            testing_mode: If True, skips facilitator
            facilitator_url: Facilitator service URL
            facilitator_api_key: API key for facilitator
            server_name: Server identifier
        """
        self.app = app
        self.server_address = server_address
        self.endpoint_payment_configs = endpoint_payment_configs or {}
        self.requires_auth = requires_auth
        self.internal_api_key = internal_api_key
        self.testing_mode = testing_mode
        
        # Initialize facilitator
        self.facilitator = None
        if not self.testing_mode:
            try:
                import os
                operator_key = (
                    os.getenv("UTILITY_AGENT_OPERATOR_PRIVATE_KEY") or
                    os.getenv("MCP_OPERATOR_PRIVATE_KEY") or
                    os.getenv("OPERATOR_PRIVATE_KEY")
                )
                
                if operator_key:
                    # Note: server_url will be extracted from each request at runtime
                    # This is needed because Cloud Run URLs are not known until deployment
                    # and must be introspected from X-Forwarded-Host and X-Forwarded-Proto headers
                    
                    self.facilitator = IATPSettlementFacilitator(
                        facilitator_url=facilitator_url or "https://facilitator.d402.net",
                        facilitator_api_key=facilitator_api_key,
                        provider_operator_key=operator_key,
                        server_name=server_name or "unknown",
                        server_url=None  # Will be set per-request from headers
                    )
                    logger.info("  Facilitator initialized with operator key")
                    
                    # Store server name for later use
                    self.server_name = server_name or "unknown"
                else:
                    logger.warning("  No operator key - settlement disabled")
            except Exception as e:
                logger.warning(f"  Could not initialize facilitator: {e}")
                self.testing_mode = True
        
        logger.info(f"D402ASGIWrapper initialized:")
        logger.info(f"  Protected endpoints: {list(self.endpoint_payment_configs.keys())}")
        logger.info(f"  Server address: {server_address}")
        logger.info(f"  Testing mode: {self.testing_mode}")
        logger.info(f"  Facilitator: {'Enabled' if self.facilitator else 'Disabled'}")
    
    async def __call__(self, scope, receive, send):
        """
        ASGI entry point - intercepts all requests.
        """
        logger.info(f"🔍 D402ASGIWrapper.__call__: {scope.get('type')} {scope.get('path')}")
        
        # Only process HTTP requests
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # Only intercept POST requests
        if scope["method"] != "POST":
            await self.app(scope, receive, send)
            return
        
        # Check if endpoint is protected
        path = scope["path"].rstrip('/') or '/'
        if path not in self.endpoint_payment_configs:
            logger.debug(f"Path {path} not protected, passing through")
            await self.app(scope, receive, send)
            return
        
        logger.info(f"💰 Protected endpoint {path} - checking payment...")
        
        # Check for X-Payment header
        headers = dict(scope["headers"])
        payment_header = headers.get(b"x-payment", b"").decode()
        
        if not payment_header:
            logger.info(f"💰 No payment header - returning HTTP 402")
            # Return 402 Payment Required
            config = self.endpoint_payment_configs[path]
            await self._send_402_response(send, config, path)
            return
        
        logger.info(f"💰 Payment header received - validating...")
        logger.info(f"📦 Payment header length: {len(payment_header)} bytes")
        
        # Validate payment (copy logic from starlette_middleware.py)
        try:
            # 1. Decode and parse payment header
            payment_data = safe_base64_decode(payment_header)
            if not payment_data:
                logger.error(f"❌ Invalid payment encoding")
                config = self.endpoint_payment_configs[path]
                await self._send_402_response(send, config, path)
                return
            
            payment_dict = json.loads(payment_data)
            
            # 2. Check payment structure
            if not payment_dict.get("payload") or not payment_dict["payload"].get("authorization"):
                logger.error(f"❌ Invalid payment structure")
                config = self.endpoint_payment_configs[path]
                await self._send_402_response(send, config, path)
                return
            
            auth = payment_dict["payload"]["authorization"]
            
            # 3. Verify payment destination
            if auth.get("to", "").lower() != self.server_address.lower():
                logger.error(f"❌ Payment to wrong address")
                config = self.endpoint_payment_configs[path]
                await self._send_402_response(send, config, path)
                return
            
            # 4. Verify payment amount
            config = self.endpoint_payment_configs[path]
            payment_amount = int(auth.get("value", 0))
            required_amount = int(config["price_wei"])
            
            if payment_amount < required_amount:
                logger.error(f"❌ Insufficient payment: {payment_amount} < {required_amount}")
                await self._send_402_response(send, config, path)
                return
            
            # 5. Call facilitator.verify() if available
            payment_uuid = None
            facilitator_fee_percent = 250
            if self.facilitator and not self.testing_mode:
                try:
                    # Extract server's own URL from request headers for tracking
                    server_url = extract_server_url_from_scope(scope)
                    logger.info(f"🌐 Server URL (introspected): {server_url}")
                    
                    # Temporarily update facilitator's server_url for this request
                    original_server_url = self.facilitator.server_url
                    self.facilitator.server_url = server_url
                    
                    payment_payload = PaymentPayload.model_validate(payment_dict)
                    payment_reqs = PaymentRequirements(
                        scheme="exact",
                        network=config["network"],
                        pay_to=config["server_address"],
                        max_amount_required=config["price_wei"],
                        max_timeout_seconds=86400,
                        description=config["description"],
                        resource=path,
                        mime_type="application/json",
                        asset=config["token_address"],
                        extra={}
                    )
                    
                    logger.info(f"🔐 Verifying payment with facilitator...")
                    verify_result = await self.facilitator.verify(payment_payload, payment_reqs)
                    
                    # Restore original server_url
                    self.facilitator.server_url = original_server_url
                    
                    logger.info(f"🔐 Facilitator verify result: {verify_result}")
                    
                    if not verify_result.is_valid:
                        logger.error(f"❌ Facilitator rejected payment: {verify_result.invalid_reason}")
                        await self._send_402_response(send, config, path)
                        return
                    
                    payment_uuid = verify_result.payment_uuid
                    facilitator_fee_percent = verify_result.facilitator_fee_percent or 250
                    logger.info(f"✅ Facilitator verified payment (UUID: {payment_uuid[:20] if payment_uuid else 'N/A'}...)")
                except Exception as e:
                    logger.error(f"❌ Facilitator error: {e}")
                    await self._send_402_response(send, config, path)
                    return
            else:
                logger.info(f"⚠️  Testing mode - skipping facilitator verification")
            
            # Payment validated!
            logger.info(f"✅ Payment VERIFIED successfully")
            logger.info(f"   Payment amount: {payment_amount} wei (required: {required_amount} wei)")
            logger.info(f"   From (wallet): {auth.get('from', 'unknown')}")
            logger.info(f"   To (provider): {auth.get('to', 'unknown')}")
            
            # Store payment info for settlement
            payment_info = {
                "payment_validated": True,
                "payment_dict": payment_dict,
                "payment_payload": PaymentPayload.model_validate(payment_dict),
                "payment_uuid": payment_uuid,
                "facilitator_fee_percent": facilitator_fee_percent,
                "endpoint_path": path,
                "endpoint_config": config
            }
            
        except Exception as e:
            logger.error(f"❌ Payment validation error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            config = self.endpoint_payment_configs[path]
            await self._send_402_response(send, config, path)
            return
        
        # Payment valid - forward to app with response interception for settlement
        response_started = False
        response_status = None
        response_body_chunks = []
        
        async def send_wrapper(message):
            """Wrap send to capture response for settlement."""
            nonlocal response_started, response_status, response_body_chunks
            
            logger.debug(f"🔍 send_wrapper: {message['type']}")
            
            if message["type"] == "http.response.start":
                response_started = True
                response_status = message["status"]
                logger.info(f"📡 Response starting: HTTP {response_status}")
                # Forward the start message
                await send(message)
            elif message["type"] == "http.response.body":
                # Capture body for settlement
                body = message.get("body", b"")
                if body:
                    response_body_chunks.append(body)
                    logger.debug(f"📦 Captured body chunk: {len(body)} bytes")
                # Forward the body message
                await send(message)
                
                # If this is the last chunk, trigger settlement
                if not message.get("more_body", False):
                    logger.info(f"📬 Last body chunk received, total: {sum(len(c) for c in response_body_chunks)} bytes")
                    await self._trigger_settlement(
                        response_status,
                        response_body_chunks,
                        payment_info
                    )
            else:
                # Forward other messages as-is
                await send(message)
        
        # Forward request with wrapped send
        await self.app(scope, receive, send_wrapper)
    
    async def _trigger_settlement(self, status_code: int, body_chunks: list, payment_info: dict):
        """Trigger payment settlement after successful response."""
        # Only settle on successful responses
        if not (200 <= status_code < 300):
            logger.info(f"⚠️  Non-success status {status_code}, skipping settlement")
            return
        
        if not payment_info.get("payment_validated"):
            return
        
        # Combine body chunks
        response_body = b"".join(body_chunks)
        
        # Check for errors in response
        try:
            response_str = response_body.decode() if response_body else ""
            if '"error"' in response_str:
                logger.warning(f"⚠️  Response contains errors - NOT settling payment")
                return
        except:
            pass
        
        logger.info(f"💳 Successful response - triggering settlement")
        
        # Trigger settlement asynchronously
        if self.facilitator and payment_info.get("payment_uuid"):
            import asyncio
            from .mcp_middleware import settle_payment, EndpointPaymentInfo
            
            async def do_settlement():
                try:
                    logger.info(f"🚀 Background settlement started")
                    
                    # Parse response
                    try:
                        output_data = json.loads(response_body.decode())
                    except:
                        output_data = {"response": response_body.decode() if response_body else "completed"}
                    
                    config = payment_info["endpoint_config"]
                    endpoint_info = EndpointPaymentInfo(
                        settlement_token_address=config["token_address"],
                        settlement_token_network=config["network"],
                        payment_price_float=float(config["price_wei"]) / 1e6,
                        payment_price_wei=config["price_wei"],
                        server_address=config["server_address"]
                    )
                    
                    # Create context wrapper
                    class SettlementContext:
                        class State:
                            def __init__(self, payment_info):
                                self.payment_payload = payment_info["payment_payload"]
                                self.payment_uuid = payment_info["payment_uuid"]
                                self.facilitator_fee_percent = payment_info["facilitator_fee_percent"]
                        
                        def __init__(self, payment_info):
                            self.state = SettlementContext.State(payment_info)
                    
                    settlement_ctx = SettlementContext(payment_info)
                    
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
            logger.info(f"📅 Settlement task scheduled")
    
    async def _send_402_response(self, send, config: Dict[str, Any], resource_path: str):
        """Send HTTP 402 Payment Required response."""
        
        payment_req = PaymentRequirements(
            scheme="exact",
            network=config["network"],
            pay_to=config["server_address"],
            max_amount_required=config["price_wei"],
            max_timeout_seconds=86400,
            description=config["description"],
            resource=resource_path,
            mime_type="application/json",
            asset=config["token_address"],
            extra=config.get("eip712_domain", {"name": "IATPWallet", "version": "1"})
        )
        
        response_data = d402PaymentRequiredResponse(
            d402_version=d402_VERSION,
            accepts=[payment_req],
            error="Payment required"
        )
        
        response_body = json.dumps(response_data.model_dump(by_alias=True)).encode()
        
        await send({
            "type": "http.response.start",
            "status": 402,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(response_body)).encode()],
                [b"access-control-expose-headers", b"X-Payment-Response"],
            ],
        })
        await send({
            "type": "http.response.body",
            "body": response_body,
        })
        
        logger.info(f"💰 Sent HTTP 402 response for {resource_path}")


__all__ = ["D402ASGIWrapper"]

