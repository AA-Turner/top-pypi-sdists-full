"""D402-enabled A2A client for IATP with payment support.

This client automatically handles D402 payments when communicating with
utility agents that require payment. It supports:
- Automatic payment creation for 402 responses
- Payment header injection
- Multiple payment schemes (exact, facilitator-verified)
- Network and token selection
"""

import asyncio
import logging
import json
import uuid
from typing import Optional, Dict, Any
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import Message, TextPart, TaskState, SendMessageRequest, MessageSendParams
import httpx

from ..d402.client import D402IATPClient, create_iatp_payment_client
from ..d402.models import D402PaymentInfo
from ..d402.types import d402PaymentRequiredResponse, PaymentRequirements

logger = logging.getLogger(__name__)


class D402A2AClient:
    """A2A client with d402 payment support for IATP.
    
    This client automatically handles d402 payments when communicating with
    utility agents that require payment.
    """
    
    def __init__(
        self,
        agent_endpoint: str,
        agent_card: Any,
        httpx_client: Any,
        payment_client: Optional[D402IATPClient] = None,
        max_payment_usd: Optional[float] = None
    ):
        """Private init - use create() classmethod instead."""
        self.agent_endpoint = agent_endpoint
        self.agent_card = agent_card
        self._httpx_client = httpx_client
        self.payment_client = payment_client
        self.max_payment_usd = max_payment_usd
        
        # Extract d402 payment information if available
        self.d402_info = self._extract_d402_info()
        
        # Initialize A2A client (a2a-sdk 0.3.x API)
        self.a2a_client = A2AClient(
            httpx_client=self._httpx_client,
            agent_card=self.agent_card,
            url=agent_endpoint
        )
    
    @classmethod
    async def create(
        cls,
        agent_endpoint: str,
        payment_client: Optional[D402IATPClient] = None,
        max_payment_usd: Optional[float] = None
    ):
        """Create a D402A2AClient instance (async factory method).
        
        Args:
            agent_endpoint: URL of the utility agent
            payment_client: Optional pre-configured D402IATPClient
            max_payment_usd: Optional maximum payment amount per request
            
        Returns:
            Initialized D402A2AClient instance
        """
        import httpx
        
        # Create HTTP client and resolve agent card
        httpx_client = httpx.AsyncClient(timeout=30.0)
        card_resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=agent_endpoint,
            agent_card_path='/.well-known/agent-card.json'
        )
        agent_card = await card_resolver.get_agent_card()
        
        # Create instance
        return cls(
            agent_endpoint=agent_endpoint,
            agent_card=agent_card,
            httpx_client=httpx_client,
            payment_client=payment_client,
            max_payment_usd=max_payment_usd
        )
    
    async def aclose(self):
        """Close the HTTP client."""
        if hasattr(self, '_httpx_client'):
            await self._httpx_client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.aclose()
        return False
    
    def _extract_d402_info(self) -> Optional[D402PaymentInfo]:
        """Extract d402 payment information from agent card."""
        # In a2a-sdk 0.3.x, AgentCard doesn't have metadata field
        # D402 info will be discovered via 402 responses instead
        # So we always assume payment might be required and handle 402 dynamically
        return None
    
    async def send_message_with_payment(
        self,
        message: str,
        skill_id: Optional[str] = None
    ) -> str:
        """Send a message to the agent, automatically handling d402 payment if required.
        
        Args:
            message: The message to send to the agent
            skill_id: Optional specific skill to invoke
            
        Returns:
            Agent's response text
            
        Raises:
            ValueError: If payment is required but no payment client is configured
            RuntimeError: If task execution fails
        """
        # Prepare the message (a2a-sdk 0.3.x requires message_id)
        import uuid
        msg = Message(
            message_id=str(uuid.uuid4()),
            role="user",
            parts=[TextPart(text=message)]
        )
        
        # Prepare headers (will add payment header if needed)
        headers = {}
        
        # Try to send the request
        async with httpx.AsyncClient(timeout=300.0) as http_client:
            # First attempt without payment to see if it's required
            try:
                # Use A2A client's send_task method
                task = await self.a2a_client.send_task(
                    id=str(asyncio.get_event_loop().time()),
                    message=msg
                )
                
                # Extract response
                return self._extract_response(task)
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 402:
                    # Payment required - handle d402 flow
                    return await self._handle_payment_required(
                        http_client, e.response, message, skill_id
                    )
                else:
                    raise
    
    async def _handle_payment_required(
        self,
        http_client: httpx.AsyncClient,
        response: httpx.Response,
        message: str,
        skill_id: Optional[str]
    ) -> str:
        """Handle 402 Payment Required response.
        
        Args:
            http_client: HTTP client for making requests
            response: 402 response with payment requirements
            message: Original message to send
            skill_id: Optional skill ID
            
        Returns:
            Agent's response after successful payment
            
        Raises:
            ValueError: If payment client not configured or requirements not met
        """
        if not self.payment_client:
            raise ValueError(
                "Payment is required but no payment client configured. "
                "Please provide a payment_client when initializing D402A2AClient."
            )
        
        # Parse payment requirements
        try:
            payment_response = d402PaymentRequiredResponse(**response.json())
        except Exception as e:
            raise ValueError(f"Invalid payment requirements: {e}")
        
        # Select payment requirements
        try:
            selected_requirements = self.payment_client.select_payment_requirements(
                accepts=payment_response.accepts,
                network_filter=None,  # Accept any network
                scheme_filter="exact"  # Only support exact scheme
            )
        except Exception as e:
            raise ValueError(f"Cannot satisfy payment requirements: {e}")
        
        # Check if amount is within maximum
        if self.max_payment_usd:
            # Convert to USD (assuming USDC with 6 decimals)
            amount_usd = int(selected_requirements.max_amount_required) / 1_000_000
            if amount_usd > self.max_payment_usd:
                raise ValueError(
                    f"Payment amount ${amount_usd:.2f} exceeds maximum ${self.max_payment_usd:.2f}"
                )
        
        # Create payment header
        payment_header = self.payment_client.create_payment_header(
            payment_requirements=selected_requirements,
            d402_version=1
        )
        
        # Retry request with payment header
        headers = {"X-PAYMENT": payment_header}
        
        # Make the A2A request with payment
        msg = Message(
            role="user",
            parts=[TextPart(text=message)]
        )
        
        # Send task with payment (we need to make raw HTTP request with headers)
        # Since A2AClient doesn't support custom headers, we'll make the request directly
        request_data = {
            "jsonrpc": "2.0",
            "id": str(asyncio.get_event_loop().time()),
            "method": "message/send",
            "params": {
                "message": msg.model_dump()
            }
        }
        
        response = await http_client.post(
            self.agent_endpoint,
            json=request_data,
            headers={"Content-Type": "application/json", **headers}
        )
        
        if response.status_code == 402:
            raise RuntimeError(f"Payment failed: {response.json().get('error', 'Unknown error')}")
        
        response.raise_for_status()
        
        # Parse JSON-RPC response
        result = response.json()
        if "error" in result:
            raise RuntimeError(f"Agent error: {result['error']}")
        
        # Extract the response text
        task_result = result.get("result", {})
        if isinstance(task_result, dict):
            messages = task_result.get("messages", [])
            for msg in messages:
                if msg.get("role") == "agent":
                    parts = msg.get("parts", [])
                    return " ".join(
                        part.get("text", "")
                        for part in parts
                        if part.get("type") == "text"
                    )
        
        return str(task_result)
    
    def _extract_response(self, task) -> str:
        """Extract text response from task result."""
        if task.status.state == TaskState.COMPLETED:
            # Look for agent's response in messages
            for msg in task.messages:
                if msg.role == "agent":
                    response_text = ""
                    for part in msg.parts:
                        if hasattr(part, 'text'):
                            response_text += part.text
                    return response_text
            
            # If no agent message, check artifacts
            if task.artifacts:
                response_text = ""
                for artifact in task.artifacts:
                    for part in artifact.parts:
                        if hasattr(part, 'text'):
                            response_text += part.text
                return response_text
            
            return "Task completed but no response found"
        else:
            raise RuntimeError(f"Task failed with state: {task.status.state}")


async def create_d402_a2a_client(
    agent_endpoint: str,
    payment_private_key: Optional[str] = None,
    max_payment_usd: Optional[float] = 10.0,
    agent_contract_address: Optional[str] = None
) -> D402A2AClient:
    """Convenience function to create an d402-enabled A2A client (async).
    
    Args:
        agent_endpoint: URL of the utility agent
        payment_private_key: Optional private key for payments (hex encoded)
        max_payment_usd: Maximum payment per request in USD
        agent_contract_address: Optional client agent contract address
        
    Returns:
        Configured D402A2AClient
        
    Example:
        # Create client with payment support
        client = await create_d402_a2a_client(
            agent_endpoint="https://agent.example.com",
            payment_private_key="0x...",
            max_payment_usd=5.0
        )
        
        # Send message (automatically handles payment if required)
        response = await client.send_message_with_payment(
            "Analyze sentiment of: 'Stock prices are rising'"
        )
        print(response)
    """
    payment_client = None
    if payment_private_key:
        payment_client = create_iatp_payment_client(
            private_key=payment_private_key,
            max_value_usd=max_payment_usd,
            agent_contract_address=agent_contract_address
        )
    
    # Use async factory method for a2a-sdk 0.3.x compatibility
    return await D402A2AClient.create(
        agent_endpoint=agent_endpoint,
        payment_client=payment_client,
        max_payment_usd=max_payment_usd
    )

