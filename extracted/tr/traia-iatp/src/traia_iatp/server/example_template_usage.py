"""Example usage of the utility agent template generator.

This script demonstrates how to generate a utility agent from an MCP server.
"""

from pathlib import Path
from ..core.models import MCPServer, MCPServerType
from .iatp_server_agent_generator import IATPServerAgentGenerator


def main():
    """Example of generating a utility agent."""
    
    # Create an MCP server specification
    mcp_server = MCPServer(
        id="hyperliquid-mcp-001",
        name="hyperliquid-mcp",
        url="http://localhost:3000/mcp",
        server_type=MCPServerType.STREAMABLE_HTTP,
        description="Implements comprehensive trading tools for Hyperliquid L1",
        capabilities=[
            "market_data",
            "place_order",
            "cancel_order",
            "get_positions",
            "get_account_info"
        ],
        metadata={
            "version": "1.0.0",
            "author": "Traia"
        }
    )
    
    # Create the generator
    generator = IATPServerAgentGenerator(
        output_base_dir=Path("generated_agents")
    )
    
    # Generate the utility agent
    agent = generator.generate_agent(
        mcp_server=mcp_server,
        agent_name="Hyperliquid Trading",
        agent_id="hyperliquid-mcp-traia-utility-agent",
        agent_description="A utility agent that exposes Hyperliquid trading capabilities via A2A protocol",
        expose_individual_tools=False,  # Just expose one main skill
        auth_required=False,
        use_simple_server=True,  # Use the simplified server template
        skill_examples=[
            "Get current market data for ETH-USD",
            "Place a limit order to buy 1 ETH at $3000",
            "Show my current positions",
            "Cancel order with ID 12345",
            "Get my account balance and margin"
        ]
    )
    
    print(f"Generated utility agent: {agent.name}")
    print(f"ID: {agent.id}")
    print(f"Status: {agent.status}")
    print(f"Code path: {agent.code_path}")
    print(f"Capabilities: {agent.capabilities}")
    
    # The generated agent can now be:
    # 1. Pushed to GitHub using push_agency_to_repo
    # 2. Deployed to Cloud Run using cloudrun_deployer
    # 3. Registered in MongoDB for discovery
    
    return agent


if __name__ == "__main__":
    main() 