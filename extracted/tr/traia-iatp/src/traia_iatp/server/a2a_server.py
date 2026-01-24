"""A2A server implementation for utility agencies using the official a2a-sdk."""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from a2a.server.apps import A2AStarletteApplication
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
from a2a.utils import new_agent_text_message, new_text_artifact
from dataclasses import dataclass
import uvicorn

from ..core.models import UtilityAgent
from .iatp_server_agent_generator import IATPServerAgentGenerator

logger = logging.getLogger(__name__)


class UtilityAgencyExecutor(AgentExecutor):
    """Agent executor that wraps a utility agency and executes tasks via CrewAI."""
    
    def __init__(self, agency: UtilityAgent, agency_generator: IATPServerAgentGenerator):
        self.agency = agency
        self.agency_generator = agency_generator
        self._crew = None
    
    async def _get_crew(self):
        """Lazily build the crew from agency config."""
        if self._crew is None:
            self._crew = await self.agency_generator.build_crew_from_agency(self.agency)
        return self._crew
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute a task using the utility agency crew."""
        try:
            # Get the user's request from context
            user_message = context.get_last_user_message()
            if not user_message:
                await event_queue.enqueue_event(
                    new_agent_text_message("No user message provided")
                )
                return
            
            # Extract text from message parts
            user_text = ""
            for part in user_message.parts:
                if hasattr(part, 'text'):
                    user_text += part.text
            
            if not user_text:
                event_queue.enqueue_event(
                    new_agent_text_message("No text content in user message")
                )
                return
            
            # Build crew and execute
            crew = await self._get_crew()
            
            # Run the crew with the request
            result = crew.kickoff(inputs={"request": user_text})
            
            # Send the result as agent message
            event_queue.enqueue_event(
                new_agent_text_message(str(result))
            )
            
        except Exception as e:
            logger.error(f"Error executing task: {e}")
            event_queue.enqueue_event(
                new_agent_text_message(f"Error processing request: {str(e)}")
            )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel all tasks."""
        pass


class MCPToolExecutor(AgentExecutor):
    """Agent executor for individual MCP tool execution."""
    
    def __init__(self, agency: UtilityAgent, tool_name: str):
        self.agency = agency
        self.tool_name = tool_name
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute a specific MCP tool."""
        try:
            from ..mcp.client import MCPClient
            
            # Get tool arguments from context
            user_message = context.get_last_user_message()
            if not user_message:
                await event_queue.enqueue_event(
                    new_agent_text_message("No arguments provided")
                )
                return
            
            # Extract arguments (assuming they're passed as JSON in text)
            import json
            arguments = {}
            for part in user_message.parts:
                if hasattr(part, 'text'):
                    try:
                        arguments = json.loads(part.text)
                    except:
                        arguments = {"query": part.text}  # Fallback to simple text
            
            # Connect to MCP server and execute tool
            mcp_client = MCPClient(self.agency.mcp_server)
            await mcp_client.connect()
            
            try:
                result = await mcp_client.call_tool(self.tool_name, arguments)
                await event_queue.enqueue_event(
                    new_agent_text_message(str(result))
                )
            finally:
                await mcp_client.disconnect()
                
        except Exception as e:
            logger.error(f"Error executing MCP tool {self.tool_name}: {e}")
            await event_queue.enqueue_event(
                new_agent_text_message(f"Error executing tool: {str(e)}")
            )


def create_a2a_server(
    agency: UtilityAgent,
    agency_generator: IATPServerAgentGenerator,
    host: str = "0.0.0.0",
    port: int = 8000
) -> A2AStarletteApplication:
    """Create an A2A server for a utility agency."""
    
    # Create skills from agency capabilities
    skills = []
    
    # Add main processing skill
    main_skill = AgentSkill(
        id="process_request",
        name=f"Process request using {agency.name}",
        description=f"Process a request using {agency.name} capabilities. {agency.description}",
        examples=[
            f"Help me with {cap}" for cap in agency.mcp_server.capabilities[:2]
        ] if agency.mcp_server.capabilities else ["Process this request for me"]
    )
    skills.append(main_skill)
    
    # Add individual MCP tool skills
    for capability in agency.mcp_server.capabilities:
        skill = AgentSkill(
            id=f"mcp_{capability}",
            name=f"Execute {capability}",
            description=f"Execute {capability} tool on MCP server",
            examples=[f"Run {capability} with these parameters"]
        )
        skills.append(skill)
    
    # Create capabilities
    capabilities = AgentCapabilities(
        streaming=False,  # Not implementing streaming for now
        pushNotifications=False,  # Not implementing push notifications
        stateTransitionHistory=False
    )
    
    # Create agent card with proper URL
    # For Cloud Run: use PUBLIC_URL or SERVICE_URL environment variable
    # For local: use http://{host}:{port}
    import os
    public_url = os.getenv("PUBLIC_URL") or os.getenv("SERVICE_URL")
    if public_url:
        # Cloud Run deployment - use the public URL
        agent_url = public_url
    else:
        # Local deployment - use host:port
        agent_url = f"http://{host}:{port}"
    
    agent_card = AgentCard(
        name=agency.name.replace(" ", "_").lower(),
        description=agency.description,
        url=agent_url,
        version="1.0.0",
        capabilities=capabilities,
        skills=skills,
        # TODO: Add authentication when AgentAuthentication is available
        # authentication=AgentAuthentication(schemes=["Bearer"]) if agency.auth_type else None
    )
    
    # Create executor mapping
    executors = {
        "process_request": UtilityAgencyExecutor(agency, agency_generator)
    }
    
    # Add MCP tool executors
    for capability in agency.mcp_server.capabilities:
        executors[f"mcp_{capability}"] = MCPToolExecutor(agency, capability)
    
    # Create task store and request handler
    task_store = InMemoryTaskStore()
    request_handler = DefaultRequestHandler(
        agent_card=agent_card,
        executors=executors,
        task_store=task_store
    )
    
    # Create the A2A application
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )
    
    return app


async def create_and_start_a2a_server(
    agency: UtilityAgent,
    agency_generator: IATPServerAgentGenerator,
    host: str = "0.0.0.0",
    port: int = 8000
):
    """Create and start an A2A server for a utility agency."""
    app = create_a2a_server(agency, agency_generator, host, port)
    
    logger.info(f"Starting A2A server for {agency.name} on {host}:{port}")
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve() 