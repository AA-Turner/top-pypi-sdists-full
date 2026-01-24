#!/usr/bin/env python
"""
MCP Agent Template

This template provides a structured way to create agents that use MCP server tools.
It offers a simplified interface for creating specialized agents that can leverage
any MCP server by providing the server configuration.

Features:
- Automatic detection of authentication requirements
- Support for both authenticated and non-authenticated MCP servers
- Flexible agent creation with optional tool filtering
- Health checks for MCP servers

Authentication:
The template automatically detects if an MCP server requires authentication
based on metadata fields:
- requires_api_key: boolean indicating if authentication is needed
- api_key_header: the header name to use (default: "Authorization")
- headers: dictionary containing the actual API key

Usage for MCP Agents:
    1. Import the MCPAgentBuilder from this module
    2. Create your specialized agent(s) with the builder
    3. Create tasks for your agents
    4. Run your agents as a CrewAI crew with MCP server configuration

Example:
    ```python
    from mcp_agent_template import MCPAgentBuilder, run_with_mcp_tools, MCPServerInfo
    
    # Create MCP server info (you would get this from registry or configuration)
    mcp_server = MCPServerInfo(
        id="weather-123",
        name="weather-mcp",
        url="http://localhost:8080",
        description="Weather information MCP server",
        server_type="streamable-http",
        capabilities=["get_weather", "get_forecast"],
        metadata={},
        tags=["weather", "api"]
    )
    
    # For authenticated servers, include auth info in metadata:
    # metadata={
    #     "requires_api_key": True,
    #     "api_key_header": "Authorization",
    #     "headers": {"Authorization": "Bearer YOUR_API_KEY"}
    # }
    
    # Create an agent for the MCP server
    analyst = MCPAgentBuilder.create_agent(
        role="Weather Analyst",
        goal="Analyze weather conditions and provide forecasts",
        backstory="You are an expert meteorologist...",
        verbose=True
    )
    
    # Create task for the agent
    task = Task(
        description="Analyze current weather conditions in New York...",
        expected_output="A comprehensive weather report...",
        agent=analyst
    )
    
    # Run the agent with MCP tools
    result = run_with_mcp_tools([task], mcp_server=mcp_server)
    print(result)
    ```
"""

import os
import sys
import json
import argparse
import logging
import re
from contextlib import ExitStack
from typing import List, Dict, Any, Optional, Union, Callable
from dataclasses import dataclass
from pathlib import Path

# Import CrewAI components
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter

# Import our custom adapters for API key and d402 payment support
from .traia_mcp_adapter import create_mcp_adapter, create_mcp_adapter_with_auth, create_mcp_adapter_with_x402
from .d402_mcp_tool_adapter import create_d402_mcp_adapter

from crewai.tools import BaseTool
from pydantic import PrivateAttr


logger = logging.getLogger(__name__)

# Create default LLM instance
DEFAULT_LLM = LLM(model="openai/gpt-4.1", temperature=0.7)


@dataclass
class MCPServerInfo:
    """Information about an MCP server."""
    id: str
    name: str
    url: str
    description: str
    server_type: str
    capabilities: List[str]
    metadata: Dict[str, Any]
    tags: List[str]


class QualifiedTool(BaseTool):
    """
    Wrapper that exposes a qualified tool name while delegating execution to an
    underlying tool (which keeps its original name for MCP protocol calls).

    This prevents tool-name collisions when aggregating tools from multiple MCP servers.
    """

    _delegate: BaseTool = PrivateAttr()
    _server_name: str = PrivateAttr(default="")
    _original_tool_name: str = PrivateAttr(default="")

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        *,
        qualified_name: str,
        description: str,
        delegate: BaseTool,
        server_name: str,
        original_tool_name: str,
        **data,
    ):
        super().__init__(name=qualified_name, description=description, **data)
        self._delegate = delegate
        self._server_name = server_name
        self._original_tool_name = original_tool_name

        # Preserve args_schema from underlying tool if present so CrewAI extracts args correctly.
        if hasattr(delegate, "args_schema") and delegate.args_schema is not None:
            self.args_schema = delegate.args_schema

    def _set_args_schema(self):
        """Avoid BaseTool overwriting the delegate's args_schema."""
        from crewai.tools.base_tool import BaseTool as BaseToolClass

        if self.args_schema == BaseToolClass._ArgsSchemaPlaceholder:
            super()._set_args_schema()

    def _run(self, **kwargs):
        return self._delegate._run(**kwargs)

    async def _arun(self, **kwargs):
        if hasattr(self._delegate, "_arun"):
            return await self._delegate._arun(**kwargs)
        return self._delegate._run(**kwargs)


class MCPServerConfig:
    """Configuration for an MCP server - used for utility agency creation."""
    
    def __init__(
        self,
        name: str,
        url: str,
        description: str,
        server_type: str = "streamable-http",  # Only streamable-http is supported
        capabilities: List[str] = None,
        metadata: Dict[str, Any] = None
    ):
        self.name = name
        self.url = url
        self.description = description
        self.server_type = server_type
        self.capabilities = capabilities or []
        self.metadata = metadata or {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "server_type": self.server_type,
            "capabilities": self.capabilities,
            "metadata": self.metadata
        }


class MCPAgentBuilder:
    """
    Builder class for creating agents that use MCP server tools.
    """
    
    # Class variable to store tool subsets for agents (using agent id as key)
    _agent_tool_subsets = {}
    
    @staticmethod
    def create_agent(
        role: str,
        goal: str,
        backstory: str,
        verbose: bool = True,
        allow_delegation: bool = False,
        llm: LLM = None,
        tools_subset: List[str] = None,
        memory: bool = False,
        max_iter: int = 25
    ) -> Agent:
        """
        Create a CrewAI agent for use with MCP tools.
        
        Args:
            role: The role of the agent
            goal: The primary goal of the agent
            backstory: Background story for the agent
            verbose: Whether to enable verbose output
            allow_delegation: Whether to allow the agent to delegate tasks
            llm: The LLM instance to use (defaults to gpt-4.1 with temperature 0.7)
            tools_subset: Optional list of specific tool names to include (if None, all tools are included)
            memory: Whether to enable memory for learning and context retention
            max_iter: Maximum number of iterations for tool execution
            
        Returns:
            CrewAI Agent configured for MCP tools
        """
        # Use specified LLM or default
        if llm is None:
            llm = DEFAULT_LLM
        
        # We'll set tools later when run_with_mcp_tools is called
        # This is because tools require the MCP server connection
        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=verbose,
            allow_delegation=allow_delegation,
            llm=llm,
            memory=memory,  # Enable memory for context retention
            max_iter=max_iter  # Allow sufficient iterations to execute tools
        )
        
        # Store the tools_subset in the class dictionary
        if tools_subset is not None:
            MCPAgentBuilder._agent_tool_subsets[id(agent)] = tools_subset
        
        return agent
    
    @staticmethod
    def get_tools_subset(agent: Agent) -> Optional[List[str]]:
        """Get the tools subset for a specific agent"""
        return MCPAgentBuilder._agent_tool_subsets.get(id(agent))


def check_server_health(
    server_info: MCPServerInfo,
    api_key: Optional[str] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> bool:
    """
    Check if the MCP server is running and healthy by attempting to connect
    and list available tools.
    
    Args:
        server_info: MCPServerInfo object with server details
        api_key: Optional API key for authenticated servers
        
    Returns:
        True if the server is healthy, False otherwise
    """
    try:
        # Check if authentication is required
        requires_api_key = server_info.metadata.get("requires_api_key", False)
        api_key_header = server_info.metadata.get("api_key_header", "Authorization")
        
        headers = dict(extra_headers or {})

        # Create appropriate adapter
        if requires_api_key and api_key:
            # Send raw API key - MCP middleware will extract it
            # Tool functions add "Bearer " prefix themselves when calling external APIs
            headers[api_key_header] = api_key
            adapter = create_mcp_adapter(url=server_info.url, headers=headers)
        else:
            # No authentication required or no API key provided
            adapter = create_mcp_adapter(url=server_info.url, headers=headers or None)
        
        # Try to connect and list tools
        with adapter as mcp_tools:
            tools = list(mcp_tools)
            print(f"✓ MCP server '{server_info.name}' is healthy ({len(tools)} tools available)")
            return True
            
    except Exception as e:
        print(f"✗ MCP server '{server_info.name}' health check failed: {e}")
        return False


def _server_lookup_keys(server_info: MCPServerInfo) -> List[str]:
    """Keys usable for mapping lookups (id/name), in priority order."""
    keys: List[str] = []
    if getattr(server_info, "id", None):
        keys.append(server_info.id)
    if getattr(server_info, "name", None) and server_info.name not in keys:
        keys.append(server_info.name)
    return keys


def _resolve_by_server(
    mapping: Optional[Dict[str, Any]],
    server_info: MCPServerInfo,
    default: Any = None,
) -> Any:
    """Resolve a per-server value from a mapping keyed by id or name."""
    if not mapping:
        return default
    for key in _server_lookup_keys(server_info):
        if key in mapping:
            return mapping[key]
    return default


def _sanitize_for_tool_namespace(value: str) -> str:
    """
    Sanitize server/tool identifiers into a CrewAI-friendly tool namespace.
    Keeps alphanumerics and underscores; collapses everything else to underscores.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9_]+", "_", value or "").strip("_")
    return cleaned or "mcp"


def _qualify_tool_name(server_info: MCPServerInfo, tool_name: str, separator: str = "__") -> str:
    server_part = _sanitize_for_tool_namespace(server_info.name or server_info.id)
    tool_part = _sanitize_for_tool_namespace(tool_name)
    return f"{server_part}{separator}{tool_part}"


def run_with_mcp_tools(
    tasks: List[Task], 
    mcp_server: Optional[MCPServerInfo] = None,
    mcp_servers: Optional[List[MCPServerInfo]] = None,
    agents: Optional[List[Agent]] = None,
    process: Process = Process.sequential,
    verbose: bool = True,
    inputs: Optional[Dict[str, Any]] = None,
    skip_health_check: bool = False,
    api_key: Optional[str] = None,
    api_keys: Optional[Dict[str, str]] = None,
    d402_account: Optional[Any] = None,
    d402_wallet_address: Optional[str] = None,
    d402_max_value: Optional[int] = None,
    d402_max_value_token: Optional[str] = None,
    d402_max_value_network: Optional[str] = None,
    d402_servers: Optional[List[str]] = None,
    headers_by_server: Optional[Dict[str, Dict[str, str]]] = None,
    qualify_tool_names: Optional[bool] = None,
    tool_name_separator: str = "__",
    tool_filter: Optional[Callable[[MCPServerInfo, BaseTool], bool]] = None,
) -> Any:
    """
    Run tasks with agents that have access to MCP server tools.
    
    NOTE ON AUTHENTICATION AND PAYMENT:
    This function supports three modes of operation:
    1. Authenticated mode: Provide api_key if server requires authentication
    2. Payment mode: Provide d402_account (CLIENT's account) for servers using HTTP 402 payment protocol
    3. Standard mode: No authentication or payment required

    MULTI-SERVER MODE:
    - Pass multiple servers via `mcp_servers=[...]` to aggregate tools across servers.
    - By default, tool names are qualified as `<server>__<tool>` to prevent collisions.
      If you set `tools_subset` on an agent, use these qualified names.
    - Use `api_keys={server_id_or_name: api_key}` and/or `headers_by_server={server_id_or_name: {...}}`
      for per-server auth configuration.
    
    Args:
        tasks: List of tasks to run
        mcp_server: Single MCPServerInfo (backwards compatible)
        mcp_servers: Optional list of MCPServerInfo to aggregate tools from multiple servers
        agents: Optional list of agents (if None, will use agents from tasks)
        process: CrewAI process type (sequential or hierarchical)
        verbose: Whether to enable verbose output
        inputs: Optional inputs for the crew
        skip_health_check: Skip server health check
        api_key: Optional API key for authenticated MCP servers (single-server convenience)
        api_keys: Optional mapping of server id/name -> API key (multi-server)
        d402_servers: Optional list of server ids/names that should use d402 when d402_account is provided.
                      If not provided, d402 is used only when server.metadata["supports_d402"] (or "d402_enabled") is true.
        d402_account: CLIENT's operator account (EOA) with private key for signing payments.
                      This is the account that signs transactions on behalf of the wallet.
        d402_wallet_address: CLIENT's IATPWallet contract address (holds funds).
                            If None, uses d402_account.address (for testing only).
                            In production, this must be the deployed IATPWallet contract address.
        d402_max_value: Optional safety limit for maximum payment amount per request in base units.
                       This is a global safety check that prevents paying more than intended.
                       Typically, each MCP server uses one primary token, so this limit applies
                       to all endpoints using that token. Set it based on your most expensive
                       expected payment in the token's base units (e.g., for USDC with 6 decimals,
                       $1.00 = 1_000_000 base units).
                       If None, no limit is enforced (not recommended for production).
        d402_max_value_token: Optional token address (e.g., "0x036CbD53842c5426634e7929541eC2318f3dCF7e" for USDC)
                             or token symbol (e.g., "USDC") that this max_value relates to.
                             Used for documentation/clarity - the actual validation is numeric only.
        d402_max_value_network: Optional network name (e.g., "base-sepolia", "sepolia") that this
                                max_value relates to. Used for documentation/clarity.
        headers_by_server: Optional mapping of server id/name -> dict of headers to send with every request
        qualify_tool_names: If True, qualify tool names as `<server>__<tool>` (defaults to True in multi-server mode)
        tool_filter: Optional predicate `(server_info, tool) -> bool` to include/exclude tools before assignment
        
    Returns:
        Result from the crew execution
    """
    # Normalize mcp_server(s) input (backwards compatible).
    if mcp_servers is None:
        if mcp_server is None:
            raise ValueError("You must provide either 'mcp_server' or 'mcp_servers'.")
        mcp_servers = [mcp_server]

    if qualify_tool_names is None:
        qualify_tool_names = len(mcp_servers) > 1

    d402_servers_set = set(d402_servers or [])

    # Check each server health unless skipped (per-server).
    if not skip_health_check:
        for server in mcp_servers:
            resolved_api_key = _resolve_by_server(api_keys, server, api_key)
            extra_headers = _resolve_by_server(headers_by_server, server, {}) or {}
            if not check_server_health(server, resolved_api_key, extra_headers=extra_headers):
                print(f"MCP server '{server.name}' is not healthy.")
                print(f"Server URL: {server.url}")
                sys.exit(1)
    
    # Get agents from tasks if not provided
    if agents is None:
        agents = [task.agent for task in tasks]
        # Remove duplicates while preserving order
        seen = set()
        agents = [agent for agent in agents if not (agent in seen or seen.add(agent))]
    
    try:
        with ExitStack() as stack:
            aggregated_tools: List[BaseTool] = []

            for server in mcp_servers:
                requires_api_key = server.metadata.get("requires_api_key", False)
                api_key_header = server.metadata.get("api_key_header", "Authorization")
                supports_d402 = bool(server.metadata.get("supports_d402") or server.metadata.get("d402_enabled"))

                # Resolve extra headers for this server (if any).
                extra_headers: Dict[str, str] = _resolve_by_server(headers_by_server, server, {}) or {}

                # Resolve whether this server should use d402.
                use_d402 = bool(d402_account) and (
                    (d402_servers is not None and (server.id in d402_servers_set or server.name in d402_servers_set))
                    or (d402_servers is None and supports_d402)
                )

                if use_d402:
                    adapter = create_d402_mcp_adapter(
                        url=server.url,
                        account=d402_account,
                        wallet_address=d402_wallet_address,
                        max_value=d402_max_value,
                        additional_headers=extra_headers,
                    )

                    wallet_info = d402_wallet_address or d402_account.address
                    print(f"\n💳 Using d402 payment protocol for '{server.name}':")
                    print(f"   MCP URL: {server.url}")
                    print(f"   Operator account: {d402_account.address} (signs payments)")
                    print(f"   Wallet address: {wallet_info} ({'IATPWallet' if d402_wallet_address else 'EOA for testing'})")
                    print("   Adapter: D402MCPToolAdapter")

                elif requires_api_key:
                    resolved_api_key = _resolve_by_server(api_keys, server, api_key)
                    if not resolved_api_key:
                        print(f"\n⚠️  WARNING: MCP server '{server.name}' requires authentication")
                        print(f"Expected header: {api_key_header}")
                        print("But no API key was provided for this server.")
                        print("\nProvide api key(s) via:")
                        print("- api_key='...' (single server) or")
                        print("- api_keys={'<server_id_or_name>': '...'} (multi server)")
                        sys.exit(1)

                    auth_headers = dict(extra_headers)
                    # Send raw API key - MCP middleware will extract it
                    # Tool functions add "Bearer " prefix themselves when calling external APIs
                    auth_headers[api_key_header] = resolved_api_key
                    adapter = create_mcp_adapter(url=server.url, headers=auth_headers)
                    print(f"\n🔐 Using authenticated connection for '{server.name}' (header: {api_key_header})")

                else:
                    adapter = create_mcp_adapter(url=server.url, headers=extra_headers or None)
                    print(f"\n🔓 Using standard connection for '{server.name}' (no authentication)")

                server_tools_iter = stack.enter_context(adapter)
                server_tools = list(server_tools_iter)

                if tool_filter is not None:
                    server_tools = [t for t in server_tools if tool_filter(server, t)]

                # Wrap tools to ensure names are unique across servers.
                for tool in server_tools:
                    qualified_name = tool.name
                    if qualify_tool_names:
                        qualified_name = _qualify_tool_name(server, tool.name, separator=tool_name_separator)

                    aggregated_tools.append(
                        QualifiedTool(
                            qualified_name=qualified_name,
                            description=f"[{server.name}] {tool.description}",
                            delegate=tool,
                            server_name=server.name,
                            original_tool_name=tool.name,
                        )
                    )

                print(f"Connected to MCP server '{server.name}' ({len(server_tools)} tools)")

            print(f"\nAggregated tools: {[tool.name for tool in aggregated_tools]}")

            # Assign tools to each agent based on their tools_subset if defined
            for agent in agents:
                tools_subset = MCPAgentBuilder.get_tools_subset(agent)
                if tools_subset:
                    agent.tools = [tool for tool in aggregated_tools if tool.name in tools_subset]
                    print(f"Agent '{agent.role}' assigned tools: {[tool.name for tool in agent.tools]}")
                else:
                    agent.tools = aggregated_tools
                    print(f"Agent '{agent.role}' assigned all available tools")
            
            # Create and run the crew
            crew = Crew(
                agents=agents,
                tasks=tasks,
                verbose=verbose,
                process=process,
                tracing=True if os.getenv("AGENTOPS_API_KEY") else False,
            )
            
            # Kickoff the crew with inputs
            result = crew.kickoff(inputs=inputs or {})
            return result
            
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# Example usage when running this file directly
if __name__ == "__main__":
    # This example shows how to use the template without registry
    print("MCP Agent Template Example")
    print("=" * 80)
    
    # Example MCP server configuration (would normally come from registry or config)
    example_server = MCPServerInfo(
        id="example-123",
        name="example-mcp",
        url="http://localhost:8080/mcp/",  # Add trailing slash
        description="Example MCP server for demonstration",
        server_type="streamable-http",
        capabilities=["example_tool1", "example_tool2"],
        metadata={},
        tags=["example", "demo"]
    )
    
    # Example of MCP server that requires authentication:
    # authenticated_server = MCPServerInfo(
    #     id="news-456",
    #     name="newsapi-mcp",
    #     url="http://localhost:8000/mcp/",  # Add trailing slash
    #     description="NewsAPI MCP server",
    #     server_type="streamable-http",
    #     capabilities=["search_news", "get_headlines"],
    #     metadata={
    #         "requires_api_key": True,
    #         "api_key_header": "Authorization",
    #         "headers": {
    #             "Authorization": "Bearer YOUR_API_KEY"  # Client API key
    #         }
    #     },
    #     tags=["news", "api"]
    # )
    
    print(f"Using MCP Server: {example_server.name}")
    print(f"Description: {example_server.description}")
    print(f"URL: {example_server.url}")
    print(f"Capabilities: {example_server.capabilities}")
    print()
    
    # Create an example agent
    analyst = MCPAgentBuilder.create_agent(
        role="Example Analyst",
        goal="Demonstrate the usage of MCP tools",
        backstory="""
            You are an expert in using MCP server tools.
            Your job is to demonstrate how to use the available tools effectively.
        """,
        verbose=True
    )
    
    # Create a task
    demo_task = Task(
        description="""
            Use the available MCP tools to perform a simple demonstration.
            Show what the tools can do and provide a summary.
        """,
        expected_output="""
            A demonstration report showing the capabilities of the MCP tools.
        """,
        agent=analyst
    )
    
    print("Note: This is a template example. To run actual MCP tools:")
    print("1. Ensure an MCP server is running at the specified URL")
    print("2. Get the server configuration from the registry or config")
    print("3. Create agents and tasks specific to your use case")
    print("4. Run with: run_with_mcp_tools([task], mcp_server)")
    print("=" * 80) 