"""A2A client implementation for CrewAI integration using the official a2a-sdk."""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import Message, TextPart, TaskState
from crewai.tools import BaseTool
import os

from ..core.models import UtilityAgentRegistryEntry
from ..registry.mongodb_registry import UtilityAgentRegistry

logger = logging.getLogger(__name__)


class UtilityAgencyTool(BaseTool):
    """CrewAI tool wrapper for utility agencies accessed via A2A."""
    
    name: str
    description: str
    endpoint: str
    agency_id: str
    capabilities: List[str]
    _client: Optional[A2AClient] = None
    
    def __init__(self, registry_entry: UtilityAgentRegistryEntry):
        """Initialize from a registry entry."""
        super().__init__(
            name=f"utility_agency_{registry_entry.name.replace(' ', '_').lower()}",
            description=registry_entry.description,
            endpoint=str(registry_entry.endpoint),
            agency_id=registry_entry.agency_id,
            capabilities=registry_entry.capabilities
        )
        self._client = None
    
    async def _get_client(self) -> A2AClient:
        """Get or create the A2A client."""
        if self._client is None:
            # Resolve agent card
            card_resolver = A2ACardResolver(self.endpoint)
            agent_card = card_resolver.get_agent_card()
            
            # Create client with authentication if needed
            auth_credentials = None
            if agent_card.authentication:
                # Get credentials from environment or registry
                # This is a simplified example - in production, use proper credential management
                auth_credentials = os.getenv(f"{self.agency_id.upper()}_AUTH")
            
            self._client = A2AClient(
                agent_card=agent_card,
                credentials=auth_credentials
            )
        return self._client
    
    async def _arun(self, request: str, **kwargs) -> str:
        """Async execution of the tool."""
        try:
            client = await self._get_client()
            
            # Create task message
            message = Message(
                role="user",
                parts=[TextPart(text=request)]
            )
            
            # Send task and wait for completion
            # The send_task method expects id and message as parameters
            task = await client.send_task(
                id=str(asyncio.get_event_loop().time()),  # Simple unique ID
                message=message
            )
            
            # Extract response
            if task.status.state == TaskState.COMPLETED:
                # Look for agent's response in messages
                for msg in task.messages:
                    if msg.role == "agent":
                        # Combine all text parts
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
                return f"Task failed with state: {task.status.state}"
                
        except Exception as e:
            logger.error(f"Error calling A2A agent: {e}")
            return f"Error: {str(e)}"
    
    def _run(self, request: str, **kwargs) -> str:
        """Sync execution of the tool."""
        return asyncio.run(self._arun(request, **kwargs))


class A2AAgencyDiscovery:
    """Helper class to discover A2A-compatible utility agencies."""
    
    @staticmethod
    async def discover_agent(endpoint: str) -> Optional[Dict[str, Any]]:
        """Discover an agent at the given endpoint."""
        try:
            card_resolver = A2ACardResolver(endpoint)
            agent_card = card_resolver.get_agent_card()
            
            # Test connectivity with a simple health check
            client = A2AClient(agent_card=agent_card)
            # The A2A protocol doesn't define a standard health check,
            # but we can try to fetch the agent card as a connectivity test
            
            return {
                "name": agent_card.name,
                "description": agent_card.description,
                "skills": [
                    {"id": skill.id, "name": skill.name, "description": skill.description}
                    for skill in agent_card.skills
                ],
                "capabilities": agent_card.capabilities.model_dump(),
                "authentication": agent_card.authentication.schemes if agent_card.authentication else None
            }
        except Exception as e:
            logger.error(f"Failed to discover agent at {endpoint}: {e}")
            return None


class UtilityAgencyFinder:
    """Helper class to find and create tools from utility agencies."""
    
    def __init__(self, registry: UtilityAgentRegistry):
        self.registry = registry
    
    async def find_tools(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        capabilities: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[UtilityAgencyTool]:
        """Find utility agencies and create CrewAI tools from them."""
        # Search the registry
        entries = await self.registry.query_agencies(
            query=query,
            tags=tags,
            capabilities=capabilities,
            active_only=True,
            limit=limit
        )
        
        # Create tools from entries with discovery check
        tools = []
        for entry in entries:
            # Verify the agency is discoverable
            agent_info = await A2AAgencyDiscovery.discover_agent(str(entry.endpoint))
            if agent_info:
                tool = UtilityAgencyTool(entry)
                tools.append(tool)
                logger.info(f"Created tool for agency: {entry.name}")
            else:
                logger.warning(f"Agency {entry.name} is not discoverable")
                # Update health status in registry
                await self.registry.update_health_status(entry.agency_id, is_healthy=False)
        
        return tools
    
    async def get_tool_by_id(self, agency_id: str) -> Optional[UtilityAgencyTool]:
        """Get a specific utility agency tool by ID."""
        entry = await self.registry.get_agency_by_id(agency_id)
        if entry:
            agent_info = await A2AAgencyDiscovery.discover_agent(str(entry.endpoint))
            if agent_info:
                return UtilityAgencyTool(entry)
        return None


def create_utility_agency_tools(
    mongodb_uri: Optional[str] = None,
    query: Optional[str] = None,
    tags: Optional[List[str]] = None,
    capabilities: Optional[List[str]] = None
) -> List[UtilityAgencyTool]:
    """Convenience function to create utility agency tools for CrewAI.
    
    Args:
        mongodb_uri: MongoDB connection string (uses MONGODB_URI env var if not provided)
        query: Search query for agencies
        tags: Filter by tags
        capabilities: Filter by capabilities
    
    Returns:
        List of CrewAI-compatible tools
    """
    async def _create_tools():
        # MongoDB URI is required
        if not mongodb_uri and not os.getenv("MONGODB_URI"):
            raise ValueError("MongoDB URI is required. Set MONGODB_URI environment variable or pass mongodb_uri parameter.")
        
        registry = UtilityAgentRegistry(mongodb_uri)
        finder = UtilityAgencyFinder(registry)
        
        try:
            tools = await finder.find_tools(
                query=query,
                tags=tags,
                capabilities=capabilities
            )
            return tools
        finally:
            registry.close()
    
    return asyncio.run(_create_tools())


# Example usage for direct A2A client without CrewAI
class SimpleA2AClient:
    """Simple A2A client for direct agent communication."""
    
    def __init__(self, agent_endpoint: str, credentials: Optional[str] = None):
        self.agent_endpoint = agent_endpoint
        self.credentials = credentials
        self._client = None
    
    async def connect(self):
        """Connect to the A2A agent."""
        card_resolver = A2ACardResolver(self.agent_endpoint)
        agent_card = card_resolver.get_agent_card()
        
        self._client = A2AClient(
            agent_card=agent_card,
            credentials=self.credentials
        )
        logger.info(f"Connected to agent: {agent_card.name}")
    
    async def send_message(self, message: str) -> str:
        """Send a message to the agent and get response."""
        if not self._client:
            await self.connect()
        
        msg = Message(
            role="user",
            parts=[TextPart(text=message)]
        )
        
        task = await self._client.send_task(
            id=str(asyncio.get_event_loop().time()),
            message=msg
        )
        
        # Extract response
        if task.status.state == TaskState.COMPLETED:
            for msg in task.messages:
                if msg.role == "agent":
                    return " ".join(part.text for part in msg.parts if hasattr(part, 'text'))
            return "No response from agent"
        else:
            raise RuntimeError(f"Task failed: {task.status.state}")
    
    async def close(self):
        """Close the client connection."""
        # A2A client doesn't have explicit close, but we can clean up
        self._client = None 