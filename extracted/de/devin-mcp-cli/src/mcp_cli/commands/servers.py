import typer
from typing import Optional
import asyncio
from rich.console import Console
from rich.table import Table
from rich.spinner import Spinner
from rich.text import Text
from mcp_cli.config import get_servers_config
from mcp_cli.utils import async_command
from mcp_cli.commands.tools import inspect_server_capabilities

server_app = typer.Typer(help="Commands for managing MCP servers.")

console = Console()

@server_app.command("list")
def list_mcp_servers(
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-C",
        help="Path to the server configuration file.",
    )
):
    """
    Lists available MCP servers from the configuration file.
    """
    
    # this does not check if the servers are properly configured, just lists them from the config file
    mcp_servers_config = get_servers_config(config_file)
    servers_list = list(mcp_servers_config.keys())

    if servers_list:
        typer.echo("Available MCP Servers:")
        for s_name in servers_list:
            typer.echo(f"- {s_name}")
    else:
        typer.echo(f"No MCP servers found. Verify the configuration file: '{config_file}'")


@server_app.command("check")
@async_command
async def check_mcp_servers(
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-C",
        help="Path to the server configuration file.",
    )
):
    """
    Check connectivity to all MCP servers and list their available tools.
    Displays a nice terminal UI with loading indicators and status indicators.
    """
    
    mcp_servers_config = get_servers_config(config_file)
    servers_list = list(mcp_servers_config.keys())

    if not servers_list:
        typer.echo(f"No MCP servers found. Verify the configuration file: '{config_file}'")
        return

    # Dictionary to store results for each server
    server_results = {}
    
    # Initialize all servers as "checking"
    for server_name in servers_list:
        server_results[server_name] = {
            'status': 'checking',
            'tools': [],
            'error': None
        }

    async def check_server(server_name: str, server_config: dict):
        """Check a single server and update its status"""
        try:
            capabilities = await inspect_server_capabilities(server_name, server_config)
            server_results[server_name]['status'] = 'success'
            server_results[server_name]['tools'] = capabilities.tools
        except Exception as e:
            server_results[server_name]['status'] = 'error'
            server_results[server_name]['error'] = str(e)

    def create_display():
        """Create the Rich display table"""
        table = Table(title="MCP Server Connection Status", show_header=True, header_style="bold magenta")
        table.add_column("Server", style="cyan", no_wrap=True)
        table.add_column("Status", style="white", no_wrap=True)
        table.add_column("Tools", style="green")

        for server_name in servers_list:
            result = server_results[server_name]
            
            if result['status'] == 'checking':
                status = Spinner("dots", text="Checking...")
                tools_text = "..."
            elif result['status'] == 'success':
                status = Text("✓ Connected", style="green")
                if result['tools']:
                    tool_names = [tool.name for tool in result['tools']]
                    tools_text = f"{len(tool_names)} tools"
                else:
                    tools_text = "No tools available"
            else:  # error
                status = Text("✗ Failed", style="red")
                tools_text = f"Error: {result['error'][:50]}{'...' if len(result['error']) > 50 else ''}"

            table.add_row(server_name, status, tools_text)
        
        return table

    # Show simple checking message
    console.print(f"🔄 Checking {len(servers_list)} MCP servers...")
    
    # Start checking all servers concurrently
    tasks = []
    for server_name, server_config in mcp_servers_config.items():
        task = asyncio.create_task(check_server(server_name, server_config))
        tasks.append(task)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks, return_exceptions=True)
    
    # Add visual separation from any server logs
    console.print("\n" + "="*80)
    
    # Show final results
    console.print(create_display())

    # Show detailed results for successful connections
    console.print("\n" + "="*60)
    console.print("Detailed Tool Information", style="bold blue")
    console.print("="*60)
    
    for server_name in servers_list:
        result = server_results[server_name]
        
        if result['status'] == 'success' and result['tools']:
            console.print(f"\n[bold cyan]{server_name}[/bold cyan] - {len(result['tools'])} tools:")
            
            for tool in result['tools']:
                tool_info = f"  • [green]{tool.name}[/green]"
                if tool.description:
                    # Truncate description for summary view - first at newlines, then by length
                    desc = tool.description.strip()
                    # Truncate at first newline if present
                    desc = desc.split('\n')[0]
                    if len(desc) > 80:
                        desc = desc[:77] + "..."
                    tool_info += f" - {desc}"
                console.print(tool_info)
        
        elif result['status'] == 'success' and not result['tools']:
            console.print(f"\n[bold cyan]{server_name}[/bold cyan] - [yellow]No tools available[/yellow]")
        
        elif result['status'] == 'error':
            console.print(f"\n[bold cyan]{server_name}[/bold cyan] - [red]Connection failed:[/red] {result['error']}")

    console.print()
