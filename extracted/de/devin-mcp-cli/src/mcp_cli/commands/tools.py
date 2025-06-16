import logging
import json
from typing import Optional, Dict, Any

import typer

from mcp_cli.config import get_servers_config, get_server_config
from mcp_cli.connection import inspect_server_capabilities, call_tool_on_server, call_resource_on_server
from mcp_cli.console import print_tools
from mcp_cli.utils import async_command

logger = logging.getLogger(__name__)

tool_app = typer.Typer(help="Commands for listing and executing tools on MCP servers.")



def parse_input_args(input_args_json: Optional[str]) -> Dict[str, Any]:
    if input_args_json:
        try:
            return json.loads(input_args_json)
        except json.JSONDecodeError as e:
            typer.secho(f"Error: Invalid JSON provided for --input: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)
    return {}


@tool_app.command("list")
@async_command
async def list_tools(
    server_name: Optional[str] = typer.Option(
        None,
        "--server",
        "-s",
        help="Specify a server to list tools for. If omitted, lists tools for all servers.",
    ),
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-C",
        help="Path to the server configuration file.",
    ),
):
    """
    Lists available tools for MCP servers.
    Lists tools for a specific server if --server is provided,
    otherwise lists tools for all configured servers.
    """
    if server_name:
        server_config_dict = get_server_config(server_name, config_file)

        logger.info(f"Creating connection parameters for server '{server_name}' with config: {server_config_dict}")

        server_capabilities = await inspect_server_capabilities(server_name, server_config_dict)
        
        print_tools(server_name, server_capabilities)
    else:
        # List tools for all servers
        mcp_servers_config = get_servers_config(config_file)
        
        typer.secho(f"\nListing tools for all configured servers...\n", fg=typer.colors.CYAN, bold=True)
        
        for server_name, server_config_dict in mcp_servers_config.items():
            try:
                logger.info(f"Creating connection parameters for server '{server_name}' with config: {server_config_dict}")
                
                server_capabilities = await inspect_server_capabilities(server_name, server_config_dict)
                print_tools(server_name, server_capabilities)
                
            except Exception as e:
                typer.secho(f"Failed to list tools for server '{server_name}': {type(e).__name__} - {e}", fg=typer.colors.RED, err=True)
                # Continue with next server instead of exiting
                continue


@tool_app.command("call")
@async_command
async def execute_tool(
    tool_name: str = typer.Argument(..., help="The name of the tool to execute."),
    server_name: str = typer.Option(
        ..., # Make server mandatory for execute
        "--server",
        "-s",
        help="The MCP server on which to run the tool.",
    ),
    input_args_json: Optional[str] = typer.Option(
        None,
        "--input",
        "-i",
        help="Tool input as a JSON string. E.g., '{\"query\": \"hello world\"}'",
    ),
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-C",
        help="Path to the server configuration file.",
    ),
):
    """
    Executes a given tool on a specified MCP server.
    Tool input can be provided as a JSON string via --input
    or from a JSON file via --input-file.
    """
    typer.echo(
        f"Executing tool: \n"
        f"  Tool name: {tool_name}\n"
        f"  Server: {server_name}\n"
        f"  Input: {input_args_json}\n"
    )

    server_config = get_server_config(server_name, config_file)

    tool_input_args: Dict[str, Any] = parse_input_args(input_args_json)

    try:
        tool_result_text = await call_tool_on_server(server_name, server_config, tool_name, tool_input_args)
        typer.echo(f"Tool result: \n{tool_result_text}\n")
    except Exception:
        raise typer.Exit(code=1)


@tool_app.command("read")
@async_command
async def read_resource(
    uri: str = typer.Argument(
        ...,
        help="The URI of the resource to execute.",
    ),
    server_name: str = typer.Option(
        ..., # Make server mandatory for execute
        "--server",
        "-s",
        help="The MCP server on which to run the tool.",
    ),
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-C",
        help="Path to the server configuration file.",
    ),
):
    """
    Reads a given resource from a specified MCP server.
    """
    typer.echo(
        f"Reading resource: \n"
        f"  Server: {server_name}\n"
        f"  URI: {uri}\n"
    )

    server_config = get_server_config(server_name, config_file)

    try:
        # server_capabilities = await inspect_server_capabilities(server_name, server_config)
        
        # resource = next((resource for resource in server_capabilities.resources if resource.name == uri), None)

        # if not resource:
        #     typer.secho(f"Resource '{uri}' not found on server '{server_name}'.", fg=typer.colors.RED, err=True)
        #     raise typer.Exit(code=1)

        resource_result_text = await call_resource_on_server(server_name, server_config, uri)
        
        typer.echo(f"Resource result: \n{resource_result_text}\n")
    except Exception as e:
        raise typer.Exit(code=1)
