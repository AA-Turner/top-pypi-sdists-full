"""IATP utility functions for agent card handling and endpoint creation."""

import logging
from typing import Dict, Any, Optional, List
import httpx

from ..core.models import AgentCard, AgentSkill, AgentCapabilities, IATPEndpoints

logger = logging.getLogger(__name__)


async def fetch_agent_card(service_url: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
    """Fetch the agent card from a deployed utility agent.
    
    Args:
        service_url: Base URL of the deployed service
        timeout: Timeout in seconds
        
    Returns:
        Agent card data or None if fetch fails
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            # Try the standard .well-known location
            response = await client.get(f"{service_url}/.well-known/agent.json")
            if response.status_code == 200:
                return response.json()
            
            # Try the /info endpoint as fallback
            response = await client.get(f"{service_url}/info")
            if response.status_code == 200:
                return response.json()
                
    except Exception as e:
        logger.error(f"Error fetching agent card from {service_url}: {e}")
    
    return None


def parse_agent_card(agent_card_data: Dict[str, Any]) -> Optional[AgentCard]:
    """Parse agent card data into an AgentCard model.
    
    Args:
        agent_card_data: Raw agent card data
        
    Returns:
        AgentCard instance or None if parsing fails
    """
    try:
        # Parse skills
        skills = []
        for skill_data in agent_card_data.get("skills", []):
            skill = AgentSkill(
                id=skill_data.get("id", ""),
                name=skill_data.get("name", ""),
                description=skill_data.get("description", ""),
                examples=skill_data.get("examples", []),
                input_modes=skill_data.get("inputModes", []),
                output_modes=skill_data.get("outputModes", []),
                tags=skill_data.get("tags", [])
            )
            skills.append(skill)
        
        # Parse capabilities
        cap_data = agent_card_data.get("capabilities", {})
        capabilities = AgentCapabilities(
            streaming=cap_data.get("streaming", False),
            push_notifications=cap_data.get("pushNotifications", False),
            state_transition_history=cap_data.get("stateTransitionHistory", False),
            custom_features=cap_data.get("customFeatures", {})
        )
        
        # Create agent card
        agent_card = AgentCard(
            name=agent_card_data.get("name", ""),
            description=agent_card_data.get("description", ""),
            version=agent_card_data.get("version", "1.0.0"),
            skills=skills,
            capabilities=capabilities,
            default_input_modes=agent_card_data.get("defaultInputModes", []),
            default_output_modes=agent_card_data.get("defaultOutputModes", []),
            metadata=agent_card_data.get("metadata", {})
        )
        
        return agent_card
        
    except Exception as e:
        logger.error(f"Error parsing agent card: {e}")
        return None


def create_iatp_endpoints(base_url: str, supports_streaming: bool = False) -> IATPEndpoints:
    """Create IATP endpoints configuration from base URL.
    
    The A2A protocol defines specific endpoints:
    - JSON-RPC endpoint at /a2a
    - Agent card at /.well-known/agent.json
    - SSE endpoints at /a2a/tasks/* (if streaming is supported)
    
    Note: Updated to use /a2a as the main JSON-RPC endpoint for consistency
    with D402 payment tracking and endpoint management.
    
    Args:
        base_url: Base URL of the service (e.g., "http://localhost:8000" or "https://service.run.app")
        supports_streaming: Whether the service supports streaming
        
    Returns:
        IATPEndpoints instance with all endpoint URLs configured
    """
    # Ensure base_url doesn't end with a slash
    base_url = base_url.rstrip('/')
    
    endpoints = IATPEndpoints(
        base_url=base_url,
        iatp_endpoint=f"{base_url}/a2a",  # A2A JSON-RPC endpoint is at /a2a
        health_endpoint=None,    # Not part of A2A protocol
        info_endpoint=None,      # Not part of A2A protocol
        agent_card_endpoint=f"{base_url}/.well-known/agent.json"
    )
    
    if supports_streaming:
        endpoints.streaming_endpoint=f"{base_url}/a2a",  # Same /a2a endpoint, different output_mode
        endpoints.subscribe_endpoint = f"{base_url}/a2a/tasks/subscribe"
        endpoints.resubscribe_endpoint = f"{base_url}/a2a/tasks/resubscribe"
    
    return endpoints 