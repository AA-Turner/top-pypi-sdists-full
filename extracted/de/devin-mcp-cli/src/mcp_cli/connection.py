from typing import Dict, Any
from contextlib import AsyncExitStack, asynccontextmanager
import logging

import typer
from pydantic import AnyUrl
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from mcp_cli.utils import expand_env_vars, parse_tool_result, parse_resource_result
from mcp_cli.types import ServerCapabilities

logger = logging.getLogger(__name__)


def get_mcp_transport(server_config: Dict[str, Any]):
    """
    Determine the MCP transport type based on server configuration.
    
    Args:
        server_config: Server configuration dictionary
        
    Returns:
        Transport type: 'sse', 'shttp', or 'stdio'
    """
    if 'url' in server_config:
        url = server_config['url']
        # Check for common SSE endpoint patterns
        if '/sse' in url or server_config.get('transport') == 'sse':
            return 'sse'
        # Check for streamable HTTP patterns
        elif '/mcp' in url or '/stream' in url or server_config.get('transport') == 'shttp':
            return 'shttp'
        # Default to SSE for HTTP URLs if not specified
        else:
            return 'sse'
    
    return 'stdio'

@asynccontextmanager
async def get_server_session(server_name: str, server_config: Dict[str, Any]):
    async with AsyncExitStack() as exit_stack:
        server_params = None
        try:
            expanded_config = expand_env_vars(server_config)

            transport = get_mcp_transport(expanded_config)

            if transport == 'sse':
                url = expanded_config['url']
                headers = expanded_config.get('headers', {})
                
                logger.info(f"Connecting to SSE server at {url}")
                
                transport_context = sse_client(
                    url=url,
                    headers=headers,
                )
                reader, writer = await exit_stack.enter_async_context(transport_context)
                
                session_context = ClientSession(reader, writer)
                session = await exit_stack.enter_async_context(session_context)
                
                await session.initialize()
                
                yield session
                
            elif transport == 'shttp':
                url = expanded_config['url']
                headers = expanded_config.get('headers', {})
                
                logger.info(f"Connecting to Streamable HTTP server at {url}")
                
                transport_context = streamablehttp_client(
                    url=url,
                    headers=headers,
                )
                reader, writer, get_session_id = await exit_stack.enter_async_context(transport_context)
                
                session_context = ClientSession(reader, writer)
                session = await exit_stack.enter_async_context(session_context)
                
                await session.initialize()
                
                yield session
                
            else: # assume stdio
                server_params = StdioServerParameters(**expanded_config)

                transport_context = stdio_client(server_params)
                reader, writer = await exit_stack.enter_async_context(transport_context)
                
                session_context = ClientSession(reader, writer)
                session = await exit_stack.enter_async_context(session_context)
                
                await session.initialize() 
                
                yield session

        except Exception as e:
            typer.secho(f"Error connecting to {server_name}: {e}", fg=typer.colors.RED, err=True)
            raise


async def inspect_server_capabilities(server_name: str, server_config: Dict[str, Any]) -> ServerCapabilities:
    """
    Helper function to connect to a single MCP server and inspect its capabilities.
    Uses the get_server_session context manager for session handling.
    """
    logger.info(f"Inspecting server capabilities: {server_name}...")
    try:
        async with get_server_session(server_name, server_config) as session:
            response_tools = await session.list_tools()
            tools = response_tools.tools

            try:
                response_resources = await session.list_resources()
                response_resource_templates = await session.list_resource_templates()

                all_resources = [*response_resources.resources, *response_resource_templates.resourceTemplates]
            except Exception as e:
                logger.info(f"Error listing resources: {e}")
                all_resources = []

            try:
                response_prompts = await session.list_prompts()
                prompts = response_prompts.prompts
            except Exception as e:
                logger.info(f"Error listing prompts: {e}")
                prompts = []

            return ServerCapabilities(tools=tools, resources=all_resources, prompts=prompts)
        
    except Exception as e:
        typer.secho(f"Failed to fetch tools from {server_name}: {type(e).__name__} - {e}", fg=typer.colors.RED, err=True)
        raise

async def call_tool_on_server(server_name: str, server_config: Dict[str, Any], tool_name: str, input_args: Dict[str, Any]) -> str:
    """
    Helper function to connect to a single MCP server and call a tool.
    Uses the get_server_session context manager for session handling.
    """
    logger.info(f"Attempting to call tool '{tool_name}' on server: {server_name}...")

    try:
        async with get_server_session(server_name, server_config) as session:
            result = await session.call_tool(tool_name, input_args)
            
            if result.isError:
                typer.echo(f"Error when calling tool '{tool_name}' on {server_name}: {','.join(getattr(c, 'text', '') for c in result.content if hasattr(c, 'text'))}")
                raise typer.Exit(code=1)
            
            result_text = parse_tool_result(result)
            return result_text

    except Exception as e: 
        typer.secho(f"Error when calling tool '{tool_name}' on {server_name}: {type(e).__name__} - {e}", fg=typer.colors.RED, err=True)
        raise

async def call_resource_on_server(server_name: str, server_config: Dict[str, Any], resource_name: str) -> str:
    """
    Helper function to connect to a single MCP server and call a resource.
    Uses the get_server_session context manager for session handling.
    """
    logger.info(f"Attempting to call resource '{resource_name}' on server: {server_name}...")   
    
    try:
        async with get_server_session(server_name, server_config) as session:
            uri = AnyUrl(resource_name)
            result = await session.read_resource(uri)

            result_text = parse_resource_result(result)

            return result_text

    except Exception as e: 
        typer.secho(f"Error when calling resource '{resource_name}' on {server_name}: {type(e).__name__} - {e}", fg=typer.colors.RED, err=True)
        raise
