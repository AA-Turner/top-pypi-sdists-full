"""Utility agent generator for A2A servers.

This module generates utility agents that wrap MCP servers and expose them via A2A protocol.
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from ..core.models import MCPServer, UtilityAgent, UtilityAgentStatus
from .iatp_server_template_generator import IATPServerTemplateGenerator

logger = logging.getLogger(__name__)


class IATPServerAgentGenerator:
    """Generate utility agents from MCP servers using templates."""
    
    def __init__(self, output_base_dir: Optional[Path] = None):
        """Initialize the generator.
        
        Args:
            output_base_dir: Base directory for generated agents
        """
        self.output_base_dir = output_base_dir or Path("generated_agents")
        self.template_generator = IATPServerTemplateGenerator()
    
    def _convert_datetime_to_string(self, obj: Any) -> Any:
        """Convert datetime objects to strings recursively.
        
        Args:
            obj: Object that may contain datetime objects
            
        Returns:
            Object with datetime objects converted to strings
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self._convert_datetime_to_string(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_datetime_to_string(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._convert_datetime_to_string(item) for item in obj)
        else:
            return obj
    
    def generate_agent(
        self,
        mcp_server: MCPServer,
        agent_name: Optional[str] = None,
        agent_id: Optional[str] = None,
        agent_description: Optional[str] = None,
        expose_individual_tools: bool = False,
        auth_required: bool = False,
        auth_schemes: Optional[list] = None,
        use_simple_server: bool = True,
        **kwargs
    ) -> UtilityAgent:
        """Generate a utility agent from an MCP server.
        
        Args:
            mcp_server: MCP server to wrap
            agent_name: Name for the agent (defaults to MCP server name)
            agent_id: Unique ID for the agent (defaults to generated)
            agent_description: Description of the agent
            expose_individual_tools: Whether to expose individual MCP tools
            auth_required: Whether authentication is required
            auth_schemes: Authentication schemes if required
            use_simple_server: Whether to use simplified server template
            **kwargs: Additional template variables
            
        Returns:
            Generated UtilityAgent object
        """
        # Generate defaults
        if agent_name is None:
            agent_name = f"{mcp_server.name} Utility Agent"
        
        if agent_id is None:
            # Generate a clean ID based on MCP server name without timestamp
            base_id = mcp_server.name.lower().replace(' ', '-').replace('_', '-')
            agent_id = f"{base_id}-traia-utility-agent"
        
        if agent_description is None:
            agent_description = f"A2A utility agent that exposes {mcp_server.name} capabilities"
        
        # Prepare capabilities list
        capabilities = []
        if hasattr(mcp_server, 'capabilities') and mcp_server.capabilities:
            if isinstance(mcp_server.capabilities, dict):
                capabilities = list(mcp_server.capabilities.keys())
            elif isinstance(mcp_server.capabilities, list):
                capabilities = mcp_server.capabilities
        
        # Prepare skill examples based on MCP server type
        skill_examples = kwargs.get('skill_examples', [])
        if not skill_examples:
            skill_examples = self._generate_skill_examples(mcp_server)
        
        # Generate output directory path
        output_dir = self.output_base_dir / agent_id
        
        # Get MCP server metadata and convert datetime objects to strings
        mcp_server_metadata = getattr(mcp_server, 'metadata', {})
        mcp_server_metadata_serializable = self._convert_datetime_to_string(mcp_server_metadata)
        
        # Use template generator to create the agent
        generated_path = self.template_generator.generate_agent(
            output_dir=output_dir,
            agent_name=agent_name,
            agent_id=agent_id,
            agent_description=agent_description,
            agent_version="0.1.0",
            mcp_server_name=mcp_server.name,
            mcp_server_url=mcp_server.url,
            mcp_server_description=mcp_server.description,
            mcp_server_type=getattr(mcp_server, 'server_type', 'streamable-http'),
            mcp_server_capabilities=capabilities,
            mcp_server_metadata=mcp_server_metadata_serializable,
            expose_individual_tools=expose_individual_tools,
            auth_required=auth_required,
            auth_schemes=auth_schemes or [],
            skill_examples=skill_examples,
            use_simple_server=use_simple_server,
            **kwargs
        )
        
        # Create UtilityAgent object
        utility_agent = UtilityAgent(
            id=agent_id,
            name=agent_name,
            description=agent_description,
            mcp_server_id=mcp_server.id,
            capabilities=capabilities,
            status=UtilityAgentStatus.GENERATED,
            code_path=str(generated_path),
            created_at=datetime.now(),
            metadata={
                "generated_from": mcp_server.name,
                "use_simple_server": use_simple_server,
                "auth_required": auth_required,
            }
        )
        
        logger.info(f"Generated utility agent '{agent_name}' at {generated_path}")
        return utility_agent
    
    def _generate_skill_examples(self, mcp_server: MCPServer) -> list:
        """Generate example prompts based on MCP server type.
        
        Args:
            mcp_server: MCP server object
            
        Returns:
            List of example prompts
        """
        # Default examples
        examples = [
            f"Help me use {mcp_server.name}",
            f"What can {mcp_server.name} do?",
        ]
        
        # Add type-specific examples
        server_type = mcp_server.name.lower()
        
        if 'search' in server_type:
            examples.extend([
                "Search for information about AI",
                "Find recent news about technology"
            ])
        elif 'file' in server_type or 'filesystem' in server_type:
            examples.extend([
                "List files in the current directory",
                "Read the contents of a file"
            ])
        elif 'database' in server_type or 'db' in server_type:
            examples.extend([
                "Query the database for user information",
                "Show me the database schema"
            ])
        elif 'api' in server_type:
            examples.extend([
                "Call the API to get data",
                "Send a request to the endpoint"
            ])
        elif 'trading' in server_type or 'finance' in server_type:
            examples.extend([
                "Get the current market data",
                "Show me trading opportunities"
            ])
        else:
            # Generic examples
            examples.extend([
                f"Execute a {mcp_server.name} operation",
                f"Process this request using {mcp_server.name}"
            ])
        
        return examples[:5]  # Limit to 5 examples
    
    def update_agent_files(
        self,
        agent_path: Path,
        updates: Dict[str, Any]
    ) -> None:
        """Update existing agent files with new configuration.
        
        Args:
            agent_path: Path to the agent directory
            updates: Dictionary of updates to apply
        """
        # Update agent_config.json if it exists
        config_path = agent_path / "agent_config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Merge updates
            config.update(updates)
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Updated agent configuration at {config_path}")
    
    def cleanup_agent(self, agent_path: Path) -> None:
        """Clean up generated agent files.
        
        Args:
            agent_path: Path to the agent directory
        """
        if agent_path.exists():
            shutil.rmtree(agent_path)
            logger.info(f"Cleaned up agent at {agent_path}") 