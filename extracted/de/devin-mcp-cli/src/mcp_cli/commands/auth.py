"""Authentication commands for MCP CLI."""

import typer
import logging
from typing import Optional
from rich.console import Console
from rich.table import Table

from mcp_cli.config import get_servers_config
from mcp_cli.auth.oauth_manager import OAuthManager
from mcp_cli.exceptions import NotOAuthCompliantError
from mcp_cli.utils import async_command

auth_app = typer.Typer()
console = Console()
logger = logging.getLogger(__name__)


@auth_app.command()
@async_command
async def login(
    server_name: str = typer.Argument(help="Name of the server to authenticate with")
):
    """Authenticate with an OAuth-enabled MCP server."""
    
    servers = get_servers_config()
    
    if server_name not in servers:
        typer.secho(f"Server '{server_name}' not found in configuration", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    
    server_config = servers[server_name]
    
    # Check if server has URL (required for OAuth)
    if 'url' not in server_config:
        typer.secho(
            f"Server '{server_name}' is not HTTP-based (no URL configured). "
            f"OAuth is only available for HTTP transports.", 
            fg=typer.colors.YELLOW
        )
        raise typer.Exit(code=1)
    
    try:
        # Create OAuth manager
        oauth_manager = OAuthManager()
        
        typer.secho(f"Starting OAuth authentication for '{server_name}'...", fg=typer.colors.BLUE)
        
        await oauth_manager.authenticate(server_name, server_config)
        typer.secho(f"Successfully authenticated with '{server_name}'!", fg=typer.colors.GREEN)
        
    except NotOAuthCompliantError:
        typer.secho(f"Server {server_name} does not support OAuth", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    except Exception as e:
        typer.secho(f"Authentication failed: {e}", fg=typer.colors.RED, err=True)
        logger.exception("Authentication failed")
        raise typer.Exit(code=1)


@auth_app.command()
@async_command
async def status():
    """Show authentication status for all servers."""
    
    servers = get_servers_config()
    oauth_manager = OAuthManager()
    
    table = Table(title="OAuth Authentication Status")
    table.add_column("Server", style="cyan")
    table.add_column("HTTP Transport", style="yellow")
    table.add_column("Authenticated", style="green")
    table.add_column("Discovery", style="blue")
    
    for server_name, server_config in servers.items():
        # OAuth is available for HTTP-based servers
        has_url = 'url' in server_config
        
        authenticated = "N/A"
        discovery = "N/A"
        
        if has_url:
            try:
                oauth_compatible = await oauth_manager.check_oauth_compatibility(server_config)
                discovery = "Auto"
            except Exception as e:
                logger.error(f"Error checking OAuth compatibility for {server_name}: {e}")
                discovery = "Error"
                
            if oauth_compatible:
                try:
                    token = await oauth_manager.get_cached_token(server_name, server_config)
                    authenticated = "✓" if token else "✗"
                except Exception:
                    authenticated = "Error"
        
        table.add_row(
            server_name,
            "✓" if has_url else "✗",
            authenticated,
            discovery
        )
    
    console.print(table)

@auth_app.command()
@async_command
async def logout(
    server_name: str = typer.Argument(..., help="Name of the server to logout from")
):
    """Clear stored OAuth tokens for a specific server."""
    
    oauth_manager = OAuthManager()
    
    servers = get_servers_config()
    if server_name not in servers:
        typer.secho(f"Server '{server_name}' not found in configuration", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    
    # Confirm before clearing specific server tokens
    if not typer.confirm(f"Are you sure you want to clear authentication for '{server_name}'?"):
        typer.secho("Operation cancelled.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=0)
    
    await oauth_manager.clear_tokens(server_name)
    typer.secho(f"Cleared authentication for '{server_name}'", fg=typer.colors.GREEN)


if __name__ == "__main__":
    auth_app()