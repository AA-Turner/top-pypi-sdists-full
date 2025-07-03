from typing import Dict, Any, Optional
from contextlib import AsyncExitStack, asynccontextmanager
import logging
import httpx

import typer
from pydantic import AnyUrl
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from mcp_cli.exceptions import ToolExecutionError, NotOAuthCompliantError, MCPOAuthError, extract_exception_details
from mcp_cli.utils import expand_env_vars, parse_tool_result, parse_resource_result
from mcp_cli.types import ServerCapabilities
from mcp_cli.auth.oauth_manager import OAuthManager


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


async def get_server_config_with_auth_headers(server_name: str, server_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add OAuth headers to server config if server supports OAuth and has cached tokens.
    
    This function checks if the server supports OAuth before attempting to add
    authentication headers. Servers that don't support OAuth are left unchanged.
    """
    config_copy = server_config.copy()
    
    # Only try OAuth for servers with HTTP URLs
    if 'url' not in server_config:
        return config_copy
    
    # Quick check: do we have cached tokens for this server?
    oauth_manager = OAuthManager()
    cached_token = await oauth_manager.get_cached_token(server_name, server_config)
    
    if cached_token:
        # We have a cached token - server likely supports OAuth
        if 'headers' not in config_copy:
            config_copy['headers'] = {}
        config_copy['headers']['Authorization'] = f'Bearer {cached_token}'
        logger.debug(f"Applied cached OAuth token for {server_name}")
    else:
        # No cached token - this is normal for:
        # 1. Servers that don't support OAuth
        # 2. Servers that support OAuth but haven't been authenticated yet
        # 3. Servers with expired tokens
        logger.debug(f"No cached OAuth token for {server_name}")
    
    return config_copy


@asynccontextmanager
async def get_server_session(server_name: str, server_config: Dict[str, Any]):
    try:
        async with AsyncExitStack() as exit_stack:
            transport = get_mcp_transport(server_config)

            # Create OAuth manager and auth for HTTP transports
            oauth_headers = {}
            if transport in ['sse', 'shttp']:
                oauth_manager = OAuthManager()
                
                # Check if we have cached token
                cached_token = await oauth_manager.get_cached_token(server_name, server_config)
                if cached_token:
                    oauth_headers['Authorization'] = f'Bearer {cached_token}'
                    logger.info(f"Using cached OAuth token for {server_name}")
                    logger.debug(f"Token preview: Bearer {cached_token[:20]}...")
                else:
                    # No cached token - OAuth will be triggered if server requires it
                    logger.info(f"No cached OAuth token available for {server_name}")

            if transport == 'sse':
                url = server_config['url']
                headers = server_config.get('headers', {})
                
                # Merge OAuth headers if available
                headers = {**headers, **oauth_headers}
                
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
                url = server_config['url']
                headers = server_config.get('headers', {})
                
                # Merge OAuth headers if available
                headers = {**headers, **oauth_headers}
                
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
                server_params = StdioServerParameters(**server_config)

                transport_context = stdio_client(server_params)
                reader, writer = await exit_stack.enter_async_context(transport_context)
                
                session_context = ClientSession(reader, writer)
                session = await exit_stack.enter_async_context(session_context)
                
                await session.initialize() 
                
                yield session
    
    # instead of raising an exceptiongroup here, just raise the first exception
    except Exception as e:
        if isinstance(e, ExceptionGroup) or isinstance(e, BaseExceptionGroup):
            if len(e.exceptions) > 1:
                logger.error(f"Got {len(e.exceptions)} exceptions when connecting to {server_name}")
            if len(e.exceptions) > 0:
                raise e.exceptions[0]
        raise

@asynccontextmanager
async def get_server_session_with_auth(server_name: str, server_config: Dict[str, Any]):
    expanded_server_config = expand_env_vars(server_config)
    total_retries = 0
    must_trigger_oauth = False
    auth = None
    last_exception: Optional[Exception] = None
    
    while True:
        if must_trigger_oauth:
            try:
                oauth_manager = OAuthManager()
                auth = await oauth_manager.authenticate(server_name, expanded_server_config)
            except NotOAuthCompliantError as e:
                # Server doesn't support OAuth - this is not an error condition
                # Just means we should skip OAuth for this server
                logger.info(f"Server {server_name} does not support OAuth, proceeding without authentication")
                raise last_exception or e
            except Exception as e:
                logger.error(f"Failed to trigger OAuth flow for {server_name}: {e}")
                raise
            
            must_trigger_oauth = False
            
            # After OAuth flow, the token should be cached
            logger.info("OAuth flow completed, will use cached token on retry")
           
        
        if auth:
            config_with_auth = await get_server_config_with_auth_headers(server_name, expanded_server_config)
        else:
            config_with_auth = expanded_server_config

        # connect to the server, retry if 401
        try:
            
            async with get_server_session(server_name, config_with_auth) as session:
                logger.info(f"Connected to {server_name}")
                yield session
                break

        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTPStatusError connecting to {server_name}, Status code: {e.response.status_code}")

            if e.response.status_code == 401:
                logger.info(f"Got 401 response from {server_name}, triggering OAuth flow")
                must_trigger_oauth = True
                last_exception = e
                total_retries += 1

                if total_retries == 3:
                    logger.error(f"Failed to connect to {server_name} after 3 retries")
                    error_details = extract_exception_details(e)
                    typer.secho(f"Failed to connect to {server_name}: {error_details}", fg=typer.colors.RED, err=True)
                    raise
                
                continue
            
            # raise non-401 errors
            raise
        
        except NotOAuthCompliantError:
            # Server doesn't support OAuth - re-raise to let caller handle
            raise
                
        except Exception as e:
            logger.exception(f"Failed to connect to {server_name} with unhandled exception")
            raise


async def inspect_server_capabilities(server_name: str, server_config: Dict[str, Any]) -> ServerCapabilities:
    """
    Helper function to connect to a single MCP server and inspect its capabilities.
    Uses the get_server_session context manager for session handling.
    """
    logger.info(f"Inspecting server capabilities: {server_name}...")
    try:
        async with get_server_session_with_auth(server_name, server_config) as session:
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
        logger.exception(f"Failed to fetch tools from {server_name}")
        error_details = extract_exception_details(e)
        typer.secho(f"Failed to fetch tools from {server_name}: {error_details}", fg=typer.colors.RED, err=True)
        raise


async def call_tool_on_server(server_name: str, server_config: Dict[str, Any], tool_name: str, input_args: Dict[str, Any]) -> str:
    """
    Helper function to connect to a single MCP server and call a tool.
    Uses the get_server_session context manager for session handling.
    """
    logger.info(f"Attempting to call tool '{tool_name}' on server: {server_name}")

    try:
        async with get_server_session_with_auth(server_name, server_config) as session:
            result = await session.call_tool(tool_name, input_args)
            
        result_text = parse_tool_result(result)

        if result.isError:
            raise ToolExecutionError(f"Tool '{tool_name}' on {server_name} was executed but returned an error: {result_text}")
        
        return result_text

    except ToolExecutionError as e:
        logger.error(e)
        raise

    except Exception as e: 
        logger.exception(f"Error when calling tool '{tool_name}' on {server_name}")
        raise


async def call_resource_on_server(server_name: str, server_config: Dict[str, Any], resource_name: str) -> str:
    """
    Helper function to connect to a single MCP server and call a resource.
    Uses the get_server_session context manager for session handling.
    """
    logger.info(f"Attempting to call resource '{resource_name}' on server: {server_name}...")   
    
    try:
        async with get_server_session_with_auth(server_name, server_config) as session:
            uri = AnyUrl(resource_name)
            result = await session.read_resource(uri)

            result_text = parse_resource_result(result)

            return result_text

    except Exception as e: 
        logger.exception(f"Error when calling resource '{resource_name}' on {server_name}")
        error_details = extract_exception_details(e)
        typer.secho(f"Error when calling resource '{resource_name}' on {server_name}: {error_details}", fg=typer.colors.RED, err=True)
        raise
