"""
Shared helpers for MCP-CLI UIs.
"""
from __future__ import annotations

import asyncio
import gc
import logging
import os
import textwrap

import typer
from rich.console import Console
from mcp.types import Resource, ResourceTemplate
from mcp_cli.types import ServerCapabilities


_console = Console()


def clear_screen() -> None:
    """Clear the terminal (cross-platform)."""
    _console.clear()


def restore_terminal() -> None:
    """Restore terminal settings and clean up asyncio resources."""
    # Restore the terminal settings to normal
    os.system("stty sane")
    
    try:
        # Find and close the event loop if one exists
        try:
            loop = asyncio.get_event_loop_policy().get_event_loop()
            if loop.is_closed():
                return
            
            # Cancel outstanding tasks
            tasks = [t for t in asyncio.all_tasks(loop) if not t.done()]
            for task in tasks:
                task.cancel()
            
            if tasks:
                loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
        except Exception as exc:
            logging.debug(f"Asyncio cleanup error: {exc}")
    finally:
        # Force garbage collection
        gc.collect()


def print_tools(server_name: str, server_capabilities: ServerCapabilities):
    typer.secho(f"\nTools available on server '{server_name}':", fg=typer.colors.CYAN, bold=True)

    for tool in server_capabilities.tools:
        typer.secho(f"\nTool: {tool.name}", fg=typer.colors.GREEN, bold=True)
        
        description = tool.description
        typer.echo("  Description:")
        if description:
            # Dedent the description and remove leading/trailing blank lines from the block
            dedented_description = textwrap.dedent(str(description)).strip()
            if dedented_description: # Ensure there's content after stripping
                description_lines = dedented_description.split('\n')
                for line in description_lines:
                    typer.echo(f"    {line}")
            else:
                typer.echo("    N/A")
        else:
            typer.echo("    N/A")
        
        input_schema = tool.inputSchema 
        
        if input_schema and isinstance(input_schema, dict) and input_schema.get('properties'):
            typer.echo("  Inputs:")
            for prop_name, prop_details in input_schema['properties'].items():
                typer.echo(f"    - {prop_name}:")
                typer.echo(f"        Type: {prop_details.get('type', 'N/A')}")
                if 'description' in prop_details:
                    typer.echo(f"        Description: {prop_details['description']}")
                
                is_required = False
                if 'required' in input_schema and isinstance(input_schema['required'], list):
                    if prop_name in input_schema['required']:
                        is_required = True
                typer.echo(f"        Required: {is_required}")
        elif input_schema and isinstance(input_schema, dict) and not input_schema.get('properties') and input_schema.get('type') == 'object':
            typer.echo("  Inputs: Takes an object, but no specific properties defined (or empty properties section).")
        else:
            typer.echo("  Inputs: None or schema not in expected format")

    for resource in server_capabilities.resources:
        typer.secho(f"\nResource: {resource.name}", fg=typer.colors.GREEN, bold=True)
        
        description = resource.description
        typer.echo("  Description:")
        if description:
            # Dedent the description and remove leading/trailing blank lines from the block
            dedented_description = textwrap.dedent(str(description)).strip()
            if dedented_description: # Ensure there's content after stripping
                description_lines = dedented_description.split('\n')
                for line in description_lines:
                    typer.echo(f"    {line}")
            else:
                typer.echo("    N/A")
        else:
            typer.echo("    N/A")

        if isinstance(resource, Resource):
            uri = resource.uri
            typer.echo(f"  URI:")
            if uri:
                typer.echo(f"    {uri}")
        elif isinstance(resource, ResourceTemplate):
            uri_template = resource.uriTemplate
            typer.echo(f"  URI Template:")
            if uri_template:
                typer.echo(f"    {uri_template}")
        else:
            typer.echo("    N/A")

    if len(server_capabilities.tools) == 0:
        typer.echo(f"No tools listed for server '{server_name}' or an error occurred during fetching.")

