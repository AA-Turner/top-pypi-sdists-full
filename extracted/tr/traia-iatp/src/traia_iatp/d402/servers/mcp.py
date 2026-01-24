"""D402 payment helpers for MCP servers with official SDK.

This module provides decorators and helper functions for d402 payment protocol
specifically for Model Context Protocol (MCP) servers using FastMCP.

Works with official MCP SDK (mcp.server.fastmcp).
"""

import logging
import os
from typing import Optional, Dict, Any, Callable
from functools import wraps

# Import Context from official SDK
from mcp.server.fastmcp import Context

from starlette.requests import Request
from starlette.responses import JSONResponse
from web3 import Web3

from ..types import PaymentPayload, Price, TokenAmount, TokenAsset, EIP712Domain, PaymentRequirements, d402PaymentRequiredResponse
from ..encoding import safe_base64_decode
from ..common import process_price_to_atomic_amount, d402_VERSION
from ..facilitator import IATPSettlementFacilitator


class D402PaymentRequiredException(Exception):
    """Exception raised when payment is required (HTTP 402)."""
    def __init__(self, payment_response: Dict[str, Any]):
        self.payment_response = payment_response
        super().__init__("Payment required")

logger = logging.getLogger(__name__)


class EndpointPaymentInfo:
    """Payment information for a specific endpoint."""
    def __init__(
        self,
        settlement_token_address: str,
        settlement_token_network: str,
        payment_price_float: float,
        payment_price_wei: str,
        server_address: str
    ):
        self.settlement_token_address = settlement_token_address
        self.settlement_token_network = settlement_token_network
        self.payment_price_float = payment_price_float
        self.payment_price_wei = payment_price_wei
        self.server_address = server_address


def get_active_api_key(context: Any) -> Optional[str]:
    """
    Get the API key to use for calling external APIs.
    
    Returns api_key_to_use which was set by:
    1. D402PaymentMiddleware (in request.state)
    2. @require_payment_for_tool decorator (copied to context.state)
    
    Priority:
    1. context.state.api_key_to_use (set by decorator)
    2. request.state.api_key_to_use (set by middleware)
    
    Args:
        context: MCP context object
        
    Returns:
        API key string (client's OR server's) if authorized, None otherwise
        
    Usage in tools:
        api_key = get_active_api_key(context)
        if api_key:
            headers = {"Authorization": f"Bearer {api_key}"}
    """
    try:
        # Check request.state (set by middleware)
        # Context is a Pydantic model - we can't set arbitrary fields on it
        # So we read directly from request.state where middleware stored it
        logger.debug(f"get_active_api_key: Checking context type={type(context).__name__}")
        logger.debug(f"  has request_context: {hasattr(context, 'request_context')}")
        
        if hasattr(context, 'request_context') and context.request_context:
            logger.debug(f"  request_context exists")
            if hasattr(context.request_context, 'request') and context.request_context.request:
                request = context.request_context.request
                logger.debug(f"  request exists, has state: {hasattr(request, 'state')}")
                if hasattr(request, 'state'):
                    api_key = getattr(request.state, 'api_key_to_use', None)
                    logger.debug(f"  api_key_to_use: {api_key[:10] if api_key else None}")
                    if api_key:
                        return api_key
        
        logger.warning(f"get_active_api_key: Could not find api_key_to_use in request.state")
            
    except Exception as e:
        logger.error(f"get_active_api_key error: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    return None


async def settle_payment(
    context: Any,
    endpoint_info: EndpointPaymentInfo,
    output_data: Any,
    middleware: Optional[Any] = None  # Middleware instance (Starlette or FastMCP)
) -> bool:
    """
    Settle a payment after successful API call with output hash attestation.
    
    Complete 402 settlement flow:
    1. Hash the output data (result returned to client)
    2. Provider signs over output_hash + consumer_request
    3. Submit to facilitator with proof of service completion
    4. Facilitator submits to IATP Settlement Layer on-chain
    
    This should be called AFTER the tool successfully processes the request
    to submit the payment settlement to the facilitator/blockchain.
    
    Args:
        context: MCP context (contains payment_payload)
        endpoint_info: Endpoint payment requirements
        output_data: The actual output/result being returned to client (will be hashed)
        middleware: Optional D402MCPMiddleware instance (for facilitator access)
        
    Returns:
        bool: True if settlement submitted successfully
        
    Usage in tools (for production settlement):
        # Execute API call
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
        result = response.json()
        
        # Settle payment with output hash
        if context.state.payment_payload:
            await settle_payment(context, endpoint_payment, output_data=result, middleware=...)
        
        return result
    """
    try:
        payment_payload = getattr(context.state, 'payment_payload', None) if hasattr(context, 'state') else None
        if not payment_payload:
            logger.debug("No payment to settle (authenticated mode)")
            return True  # Not an error - client used their own API key
        
        # Skip settlement in testing mode
        if middleware and middleware.testing_mode:
            logger.info("⚠️  Testing mode: Skipping payment settlement")
            return True
        
        # Step 1: Hash the output data (proof of service completion)
        import json
        from web3 import Web3
        
        logger.info("🔐 Starting payment settlement process...")
        
        # Serialize output to JSON and hash it
        output_json = json.dumps(output_data, sort_keys=True, separators=(',', ':'))
        output_hash = Web3.keccak(text=output_json).hex()
        logger.info(f"📊 Output data serialized: {len(output_json)} bytes")
        logger.info(f"🔑 Output hash calculated: {output_hash}")
        logger.info(f"   First 1000 chars of output: {output_json[:1000]}")
        
        # Step 2: Get payment_uuid from context (from facilitator verify response)
        # The payment_uuid is the primary payment identifier from the facilitator
        # It was set in verify_endpoint_payment() after facilitator.verify() returned it
        payment_uuid = None
        if hasattr(context, 'state') and hasattr(context.state, 'payment_uuid'):
            payment_uuid = context.state.payment_uuid
        
        if not payment_uuid:
            logger.warning("No payment_uuid found in context - payment may not have been verified via facilitator")
        
        # Step 3: Get facilitator fee from context (set by verify response)
        facilitator_fee_percent = 250  # Default
        if hasattr(context, 'state') and hasattr(context.state, 'facilitator_fee_percent'):
            facilitator_fee_percent = context.state.facilitator_fee_percent
        
        # Step 4: Create PaymentRequirements for this endpoint
        # Include output_hash, payment_uuid, and facilitatorFeePercent in extra data
        extra_data = {
            "output_hash": output_hash,
            "facilitator_fee_percent": facilitator_fee_percent
        }
        if payment_uuid:
            extra_data["payment_uuid"] = payment_uuid
        
        payment_requirements = PaymentRequirements(
            scheme="exact",
            network=endpoint_info.settlement_token_network,
            pay_to=endpoint_info.server_address,
            max_amount_required=endpoint_info.payment_price_wei,
            max_timeout_seconds=300,
            description=f"Service completed - output_hash: {output_hash}",
            resource="",
            mime_type="application/json",
            asset=endpoint_info.settlement_token_address,
            extra=extra_data  # Include output hash, payment_uuid, and facilitatorFeePercent
        )
        
        # Step 4: Settle via facilitator
        # The facilitator will:
        # - Create provider attestation signing over the consumer's request + output_hash
        # - Submit to relayer with proof of service completion
        # - Relayer submits to IATPSettlementLayer on-chain
        if middleware and middleware.facilitator:
            try:
                logger.info(f"📤 Submitting settlement to facilitator...")
                logger.info(f"   Payment UUID: {payment_uuid if payment_uuid else 'N/A'}")
                logger.info(f"   Output hash: {output_hash}")
                logger.info(f"   Amount: {endpoint_info.payment_price_wei} wei")
                
                settle_result = await middleware.facilitator.settle(payment_payload, payment_requirements)
                if settle_result.success:
                    logger.info(f"✅ Payment settlement request accepted by facilitator:")
                    logger.info(f"   Status: PENDING_SETTLEMENT (queued for on-chain settlement)")
                    logger.info(f"   Network: {settle_result.network}")
                    logger.info(f"   Payer: {settle_result.payer}")
                    logger.info(f"   Output Hash: {output_hash}")
                    logger.info(f"   Note: Facilitator cron will batch-settle on-chain")
                    return True
                else:
                    logger.error(f"❌ Payment settlement FAILED: {settle_result.error_reason}")
                    # TODO: Queue for retry
                    return False
            except Exception as e:
                logger.error(f"Error settling payment via facilitator: {e}")
                # Don't fail the request if settlement fails
                # Settlement can be retried later
                logger.warning("Settlement failed but request completed - will retry later")
                # TODO: Queue settlement for retry
                return False
        else:
            logger.warning("No facilitator available for settlement")
            # TODO: Queue settlement for later retry
            return False
            
    except Exception as e:
        import traceback
        logger.error(f"Error in settle_payment: {e}")
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        return False


def require_payment_for_tool(
    price: Price,
    description: str = ""
):
    """
    Decorator for MCP tools that require payment - METADATA ONLY.
    
    This decorator ONLY stores payment configuration metadata on the function.
    All payment processing (verify, settle) is handled by D402PaymentMiddleware.
    
    Usage:
        @mcp.tool()
        @require_payment_for_tool(
            price=TokenAmount(
                amount="1000",
                asset=TokenAsset(
                    address="0xUSDC...",
                    decimals=6,
                    network="base-sepolia",
                    eip712=EIP712Domain(name="IATPWallet", version="1")
                )
            ),
            description="Get cryptocurrency price data"
        )
        async def get_price(context: Context, coin_id: str) -> Dict[str, Any]:
            # Payment already verified by middleware
            api_key = get_active_api_key(context)
            response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
            return response.json()
    
    Args:
        price: Payment configuration (TokenAmount with network, token, etc)
        description: Service description for settlement
    
    Returns:
        Decorator that attaches metadata to the function
    """
    def decorator(func: Callable):
        # Store payment metadata on function for middleware extraction
        func._d402_payment_config = {
            "price": price,
            "description": description
        }
        
        # Return function unchanged - middleware handles all payment logic
        return func
    
    return decorator


__all__ = [
    "D402PaymentRequiredException",
    "EndpointPaymentInfo",
    "get_active_api_key",
    "settle_payment",
    "require_payment_for_tool",
]

