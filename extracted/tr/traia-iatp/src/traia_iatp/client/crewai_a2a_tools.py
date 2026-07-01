"""Enhanced CrewAI tools for A2A integration with utility agencies."""

import asyncio
import logging
import traceback
from typing import Dict, Any, Optional, List, Union, AsyncIterator
from datetime import datetime
import json
import httpx
import uuid
import os
from contextlib import asynccontextmanager
import httpcore
from enum import Enum
import threading

from crewai.tools import BaseTool
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    Message, TextPart, TaskState, SendMessageRequest, MessageSendParams,
    GetTaskRequest, Task, TaskQueryParams, TaskResubscriptionRequest
)
from pydantic import Field, BaseModel

from ..utils import get_now_in_utc
from a2a.client.errors import A2AClientError

logger = logging.getLogger(__name__)

# Thread-local storage for httpx clients
_thread_local = threading.local()


class A2AToolSchema(BaseModel):
    """Input schema for A2A tools."""
    request: str = Field(description="The request or query to send to the A2A agent. Send only 'request' key when using this tool")


class A2AToolConfig(BaseModel):
    """Configuration for A2A tools."""
    endpoint: str = Field(description="The A2A endpoint URL")
    agency_name: str = Field(description="Name of the utility agency")
    agency_description: str = Field(description="Description of what the agency does")
    timeout: int = Field(default=300, description="Timeout in seconds for A2A calls")
    retry_attempts: int = Field(default=3, description="Number of retry attempts")
    poll_interval: int = Field(default=2, description="Interval in seconds between status checks")
    max_poll_attempts: int = Field(default=150, description="Maximum number of polling attempts")
    authentication: Optional[Dict[str, str]] = Field(default=None, description="Authentication credentials if needed")
    # Connection pool settings
    max_keepalive_connections: int = Field(default=20, description="Max keepalive connections in pool")
    max_connections: int = Field(default=100, description="Max total connections in pool")
    keepalive_expiry: int = Field(default=300, description="Keepalive expiry in seconds")
    # Streaming settings
    supports_streaming: bool = Field(default=False, description="Whether the agency supports SSE streaming")
    stream_timeout: int = Field(default=600, description="Timeout for streaming connections")
    iatp_endpoint: Optional[str] = Field(default=None, description="Specific IATP endpoint")


class A2ATool(BaseTool):
    """Enhanced CrewAI tool for A2A utility agencies."""
    
    name: str
    description: str
    args_schema: type[BaseModel] = A2AToolSchema
    config: A2AToolConfig
    
    def __init__(self, config: A2AToolConfig):
        """Initialize the A2A tool with configuration."""
        # Create a tool name from agency name
        tool_name = f"a2a_{config.agency_name.replace(' ', '_').replace('-', '_').lower()}"
        
        super().__init__(
            name=tool_name,
            description=f"Use {config.agency_name} via A2A: {config.agency_description}",
            config=config
        )
    
    async def _run(self, **kwargs) -> str:
        """Async execution of the tool - main CrewAI entry point."""
        # Extract request from kwargs
        request = kwargs.get('request', kwargs.get('query', ''))
        
        logger.info(f"A2ATool._run called with request: {str(request)[:200]}...")
        logger.info(f"Tool name: {self.name}, Endpoint: {self.config.endpoint}")
        
        try:
            # Check if D402 payment credentials are available from environment
            # Use D402_CLIENT_OPERATOR_PRIVATE_KEY for client-side payments
            payment_private_key = os.getenv("D402_CLIENT_OPERATOR_PRIVATE_KEY") or os.getenv("EVM_PRIVATE_KEY")
            wallet_address = os.getenv("D402_CLIENT_WALLET_ADDRESS")
            
            # Create httpx client with D402 payment support if credentials available
            if payment_private_key:
                from eth_account import Account
                from ..d402.clients.httpx import d402HttpxClient
                
                operator_key = payment_private_key if payment_private_key.startswith("0x") else f"0x{payment_private_key}"
                operator_account = Account.from_key(operator_key)
                
                logger.info(f"Using D402 payment client for A2A tool")
                httpx_client = d402HttpxClient(
                    operator_account,
                    wallet_address=wallet_address,
                    timeout=self.config.timeout
                )
            else:
                logger.info(f"No D402 credentials, using standard httpx client")
                httpx_client = httpx.AsyncClient(
                timeout=httpx.Timeout(
                    connect=5.0,
                    read=self.config.timeout,
                    write=self.config.timeout,
                    pool=5.0
                ),
                http2=True
                )
            
            async with httpx_client:
                
                # Resolve agent card
                card_resolver = A2ACardResolver(
                    httpx_client=httpx_client,
                    base_url=self.config.endpoint
                )
                agent_card = await card_resolver.get_agent_card()
                logger.info(f"Resolved agent card for: {agent_card.name}")
                logger.info(f"Agent card URL: {agent_card.url if hasattr(agent_card, 'url') else 'N/A'}")
                
                # Use the URL from agent card (don't override it)
                # The agent card knows the correct A2A endpoint
                
                # Create A2A client
                iatp_endpoint = self.config.iatp_endpoint or agent_card.url
                a2a_client = A2AClient(
                    httpx_client=httpx_client,
                    agent_card=agent_card,
                    url=agent_card.url  # Use agent card's URL (includes /a2a for utility agents)
                )
                
                # Create message
                message_id = f"msg_{uuid.uuid4()}"
                task_id = f"task_{uuid.uuid4()}"
                
                message = Message(
                    messageId=message_id,
                    role="user",
                    parts=[TextPart(text=str(request))]
                )
                
                # Create send message request
                send_request = SendMessageRequest(
                    id=task_id,
                    jsonrpc="2.0",
                    method="message/send",
                    params=MessageSendParams(
                        message=message,
                        configuration=None,
                        metadata=None
                    )
                )
                
                logger.info(f"Sending message with task ID: {task_id}")
                
                # Send message and get response
                response = await a2a_client.send_message(send_request)
                
                # Extract response text
                if hasattr(response, 'error') and response.error:
                    return f"A2A error: {response.error}"
                
                # Handle response
                if hasattr(response, 'root'):
                    result = response.root.result if hasattr(response.root, 'result') else response.root
                else:
                    result = response.result if hasattr(response, 'result') else response
                
                # If it's a task, wait for completion
                if hasattr(result, 'id') and hasattr(result, 'status'):
                    # It's a task - for now just return that we started it
                    # In a real implementation you'd poll for completion
                    return f"Task {result.id} started with status: {result.status.state}"
                
                # Extract text from message response
                response_parts = []
                if hasattr(result, 'parts') and result.parts:
                    for part in result.parts:
                        if hasattr(part, 'root') and hasattr(part.root, 'text'):
                            response_parts.append(part.root.text)
                        elif hasattr(part, 'text'):
                            response_parts.append(part.text)
                elif hasattr(result, 'text'):
                    response_parts.append(result.text)
                elif isinstance(result, dict) and 'text' in result:
                    response_parts.append(result['text'])
                else:
                    response_parts.append(str(result))
                
                return "\n".join(response_parts) if response_parts else "No response content"
                
        except Exception as e:
            logger.error(f"Error in A2A tool {self.name}: {e}")
            return f"Error: {str(e)}"


class A2AToolkit:
    """Toolkit for creating and managing A2A tools for CrewAI."""
    
    @staticmethod
    async def discover_agent_async(endpoint: str) -> Optional[Dict[str, Any]]:
        """Async method to discover agent information."""
        # Create HTTP/2 enabled client for discovery
        transport = httpx.AsyncHTTPTransport(http2=True)
        httpx_client = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0),
            transport=transport
        )
        try:
            card_resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=endpoint
            )
            agent_card = await card_resolver.get_agent_card()
            
            # Check capabilities
            capabilities = {}
            if hasattr(agent_card, 'capabilities'):
                capabilities = {
                    "streaming": getattr(agent_card.capabilities, 'streaming', False),
                    "pushNotifications": getattr(agent_card.capabilities, 'pushNotifications', False),
                    "stateTransitionHistory": getattr(agent_card.capabilities, 'stateTransitionHistory', False)
                }
            
            return {
                "name": agent_card.name,
                "description": agent_card.description,
                "version": agent_card.version,
                "capabilities": capabilities
            }
        except Exception as e:
            logger.warning(f"Could not discover agent info from {endpoint}: {e}")
            return None
        finally:
            await httpx_client.aclose()
    
    @staticmethod
    def create_tool_from_endpoint(
        endpoint: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        timeout: int = 300,
        retry_attempts: int = 3,
        poll_interval: int = 2,
        max_poll_attempts: int = 150,
        authentication: Optional[Dict[str, str]] = None,
        supports_streaming: Optional[bool] = None,
        iatp_endpoint: Optional[str] = None
    ) -> A2ATool:
        """Create an A2A tool from an endpoint."""
        # If name/description not provided, try to discover from endpoint
        discovered_streaming = False
        if not name or not description or supports_streaming is None:
            try:
                # Run async discovery in sync context
                agent_info = asyncio.run(A2AToolkit.discover_agent_async(endpoint))
                if agent_info:
                    name = name or agent_info["name"]
                    description = description or agent_info["description"]
                    discovered_streaming = agent_info.get("capabilities", {}).get("streaming", False)
                else:
                    name = name or "Unknown Agency"
                    description = description or "A2A utility agency"
            except Exception as e:
                logger.warning(f"Could not discover agent info from {endpoint}: {e}")
                name = name or "Unknown Agency"
                description = description or "A2A utility agency"
        
        config = A2AToolConfig(
            endpoint=endpoint,
            agency_name=name,
            agency_description=description,
            timeout=timeout,
            retry_attempts=retry_attempts,
            poll_interval=poll_interval,
            max_poll_attempts=max_poll_attempts,
            authentication=authentication,
            supports_streaming=supports_streaming if supports_streaming is not None else discovered_streaming,
            iatp_endpoint=iatp_endpoint or endpoint  # Default to endpoint if not specified
        )
        
        return A2ATool(config)
    
    @staticmethod
    def create_tools_from_endpoints(
        endpoints: List[Dict[str, Any]],
        default_timeout: int = 300,
        default_retry_attempts: int = 3,
        default_poll_interval: int = 2,
        default_max_poll_attempts: int = 150
    ) -> List[A2ATool]:
        """Create multiple A2A tools from a list of endpoint configurations."""
        tools = []
        
        for ep_config in endpoints:
            tool = A2AToolkit.create_tool_from_endpoint(
                endpoint=ep_config["endpoint"],
                name=ep_config.get("name"),
                description=ep_config.get("description"),
                timeout=ep_config.get("timeout", default_timeout),
                retry_attempts=ep_config.get("retry_attempts", default_retry_attempts),
                poll_interval=ep_config.get("poll_interval", default_poll_interval),
                max_poll_attempts=ep_config.get("max_poll_attempts", default_max_poll_attempts),
                authentication=ep_config.get("authentication"),
                supports_streaming=ep_config.get("supports_streaming"),
                iatp_endpoint=ep_config.get("iatp_endpoint")
            )
            tools.append(tool)
            logger.info(f"Created A2A tool: {tool.name}")
        
        return tools


# Specialized tools for common trading operations
class TradingA2ATool(A2ATool):
    """Specialized A2A tool for trading operations with structured prompts."""
    
    def __init__(self, config: A2AToolConfig):
        super().__init__(config)
        self.description = f"Trading tool via {config.agency_name}: Execute trades, check positions, and analyze markets"
    
    async def get_market_info(self, symbol: str) -> str:
        """Get market information for a symbol."""
        request = f"Get current market information for {symbol} including price, volume, and recent trends"
        return await self._run(request=request)
    
    async def check_positions(self) -> str:
        """Check current trading positions."""
        request = "List all current open positions with their P&L and status"
        return await self._run(request=request)
    
    async def execute_trade(self, action: str, symbol: str, amount: float, price: Optional[float] = None) -> str:
        """Execute a trade."""
        if price:
            request = f"Execute {action} order for {amount} units of {symbol} at price {price}"
        else:
            request = f"Execute {action} market order for {amount} units of {symbol}"
        
        context = {
            "action": action,
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return await self._run(request=request, **context) 