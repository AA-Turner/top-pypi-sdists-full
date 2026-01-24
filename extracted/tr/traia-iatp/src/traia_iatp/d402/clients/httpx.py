"""HTTPX client integration for d402 payments."""

import logging
from typing import Optional, Dict, List
from httpx import Request, Response, AsyncClient
from eth_account import Account
from functools import wraps

from .base import (
    d402Client,
    MissingRequestConfigError,
    PaymentError,
    PaymentSelectorCallable,
    decode_x_payment_response,
)
from ..types import d402PaymentRequiredResponse

logger = logging.getLogger(__name__)


class HttpxHooks:
    """Event hooks for httpx client to handle d402 payments."""

    def __init__(self, client: d402Client, httpx_client: AsyncClient = None):
        self.client = client
        self.httpx_client = httpx_client  # Reference to the httpx client for retries
        self._is_retry = False

    async def on_request(self, request: Request):
        """Handle request before it is sent."""
        #TODO: (TBD) if mongodb had endpoints data for each mcp server then the client herre could apriori get the payment details and construct the payment payload.
        pass

    async def on_response(self, response: Response) -> Response:
        """Handle response after it is received.

        When a 402 Payment Required response is received:
        1. Parse payment requirements from the response
        2. Select appropriate payment option (token/network)
        3. Create EIP-3009 signed payment authorization
        4. Retry the original request with X-Payment header
        """

        # Log every response for debugging
        logger.debug(f"d402 hook: on_response called - status={response.status_code}, url={response.url}")

        # If this is not a 402, just return the response
        if response.status_code != 402:
            return response

        # If this is a retry response, just return it (avoid infinite loop)
        if self._is_retry:
            logger.debug(f"d402 hook: This is a retry response, returning as-is")
            return response
        
        logger.info(f"🔔 d402 hook: Intercepted HTTP 402 - creating payment...")

        try:
            if not response.request:
                raise MissingRequestConfigError("Missing request configuration")

            # Read the response content before parsing
            await response.aread()

            # Parse payment requirements from 402 response
            data = response.json()
            payment_response = d402PaymentRequiredResponse(**data)

            # Select payment requirements (matches token/network, checks max_value)
            selected_requirements = self.client.select_payment_requirements(
                payment_response.accepts
            )

            # The server sets the resource field in payment_requirements
            # This is the authoritative requestPath for the signature
            # The server knows what endpoint is being called and sets it correctly
            print(f"📍 DEBUG: Request path from server resource field: '{selected_requirements.resource}'")
            logger.info(f"💳 Creating payment header for retry...")

            # Create signed payment header using CLIENT's account
            # Use payment_requirements.resource (don't override)
            payment_header = self.client.create_payment_header(
                selected_requirements, 
                payment_response.d402_version
                # No request_path parameter - uses payment_requirements.resource
            )

            # Mark as retry to avoid infinite loop
            self._is_retry = True
            logger.info(f"💳 Payment header created, preparing retry...")
            
            # Get the original request and add payment header
            request = response.request
            request.headers["X-Payment"] = payment_header
            request.headers["Access-Control-Expose-Headers"] = "X-Payment-Response"
            logger.info(f"💳 Added X-Payment header to request")

            # Retry the request using the httpx client
            # Priority:
            # 1. self.httpx_client (if set by d402HttpxClient)
            # 2. response.request.extensions.get("client") (if available)
            # 3. Fallback: create new client (may lose hooks)
            
            retry_client = None
            if self.httpx_client:
                logger.info(f"💳 Using self.httpx_client for retry (d402HttpxClient)")
                print(f"💳 Using d402HttpxClient instance for retry")
                retry_client = self.httpx_client
            else:
                original_client = response.request.extensions.get("client")
                logger.info(f"💳 original_client from extensions: {original_client is not None}")
                
                if original_client and isinstance(original_client, AsyncClient):
                    logger.info(f"💳 Using original client from extensions...")
                    retry_client = original_client
            
            if retry_client:
                logger.info(f"💳 Retrying with client that has hooks...")
                retry_response = await retry_client.send(request)
            else:
                # No client with hooks available - can't retry safely
                # Just return the 402 response as-is
                logger.error(f"❌ No client available for retry, cannot handle payment")
                print(f"❌ Cannot retry payment - no httpx client with hooks available")
                self._is_retry = False
                return response

            logger.info(f"💳 Retry response received: HTTP {retry_response.status_code}")
            print(f"💳 RETRY RESPONSE: HTTP {retry_response.status_code}")

            # Copy the retry response data to the original response object
            response.status_code = retry_response.status_code
            response.headers = retry_response.headers
            response._content = retry_response._content
            
            logger.info(f"✅ Payment handling complete, returning response")
            print(f"✅ Payment retry complete, returning HTTP {response.status_code}")
            return response

        except PaymentError as e:
            self._is_retry = False
            print(f"❌ PaymentError in hook: {e}")
            raise e
        except Exception as e:
            self._is_retry = False
            print(f"❌ Exception in payment hook: {e}")
            import traceback
            traceback.print_exc()
            raise PaymentError(f"Failed to handle payment: {str(e)}") from e


def d402_payment_hooks(
    operator_account: Account,
    wallet_address: str = None,
    max_value: Optional[int] = None,
    payment_requirements_selector: Optional[PaymentSelectorCallable] = None,
    httpx_client: AsyncClient = None,
) -> Dict[str, List]:
    """Create httpx event hooks dictionary for handling 402 Payment Required responses.

    Args:
        operator_account: Operator account with private key for signing payments (EOA)
        wallet_address: Consumer's IATPWallet contract address (if None, uses operator_account.address for testing)
        max_value: Optional maximum allowed payment amount in base units
        payment_requirements_selector: Optional custom selector for payment requirements.
            Should be a callable that takes (accepts, network_filter, scheme_filter, max_value)
            and returns a PaymentRequirements object.

    Returns:
        Dictionary of event hooks that can be directly assigned to client.event_hooks

    Example:
        ```python
        from eth_account import Account
        from traia_iatp.d402.clients.httpx import d402_payment_hooks
        import httpx

        # For testing (uses EOA as wallet)
        operator_account = Account.from_key("0x...")
        client.event_hooks = d402_payment_hooks(operator_account)
        
        # For production (with IATPWallet contract)
        operator_account = Account.from_key("0x...")  # Operator key
        wallet = "0x..."  # IATPWallet contract address
        client.event_hooks = d402_payment_hooks(operator_account, wallet_address=wallet)
        ```
    """
    # Create d402Client
    client = d402Client(
        operator_account,
        wallet_address=wallet_address,
        max_value=max_value,
        payment_requirements_selector=payment_requirements_selector,
    )

    # Create hooks with optional httpx_client reference
    hooks = HttpxHooks(client, httpx_client=httpx_client)

    # Return event hooks dictionary
    return {
        "request": [hooks.on_request],
        "response": [hooks.on_response],
    }


class d402HttpxClient(AsyncClient):
    """AsyncClient with built-in d402 payment handling."""

    def __init__(
        self,
        operator_account: Account,
        wallet_address: str = None,
        max_value: Optional[int] = None,
        payment_requirements_selector: Optional[PaymentSelectorCallable] = None,
        **kwargs,
    ):
        """Initialize an AsyncClient with d402 payment handling.

        Args:
            operator_account: Operator account with private key for signing payments (EOA)
            wallet_address: Consumer's IATPWallet contract address (if None, uses operator_account.address for testing)
            max_value: Optional maximum allowed payment amount in base units
            payment_requirements_selector: Optional custom selector for payment requirements.
                Should be a callable that takes (accepts, network_filter, scheme_filter, max_value)
                and returns a PaymentRequirements object.
            **kwargs: Additional arguments to pass to AsyncClient

        Example:
            ```python
            from eth_account import Account
            from traia_iatp.d402.clients.httpx import d402HttpxClient

            # For testing (uses EOA as wallet)
            operator_account = Account.from_key("0x...")
            async with d402HttpxClient(operator_account, base_url="https://api.example.com") as client:
                response = await client.get("/protected-endpoint")
                
            # For production (with IATPWallet contract)
            operator_account = Account.from_key("0x...")  # Operator key
            wallet = "0x..."  # IATPWallet contract
            async with d402HttpxClient(operator_account, wallet_address=wallet, base_url="https://api.example.com") as client:
                response = await client.get("/protected-endpoint")
            ```
        """
        super().__init__(**kwargs)
        
        # Create d402Client
        payment_client = d402Client(
            operator_account,
            wallet_address=wallet_address,
            max_value=max_value,
            payment_requirements_selector=payment_requirements_selector,
        )
        
        # Create hooks with reference to this httpx client
        hooks = HttpxHooks(payment_client, httpx_client=self)
        
        # Set event hooks
        self.event_hooks = {
            "request": [hooks.on_request],
            "response": [hooks.on_response],
        }


__all__ = ["d402_payment_hooks", "d402HttpxClient", "HttpxHooks"]

