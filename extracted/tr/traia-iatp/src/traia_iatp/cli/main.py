"""IATP CLI interface."""

import asyncio
import json
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from pydantic import HttpUrl

from ..core.models import MCPServer, MCPServerType, UtilityAgent
from ..server.iatp_server_agent_generator import IATPServerAgentGenerator
from ..registry.mongodb_registry import UtilityAgentRegistry, MCPServerRegistry
from ..utils.docker_utils import use_run_local_docker_script, LocalDockerRunner
from ..client.a2a_client import create_utility_agency_tools
from ..mcp.mcp_agent_template import MCPServerConfig
from ..contracts.wallet_creator import create_iatp_wallet

app = typer.Typer(
    name="iatp",
    help="Inter Agent Transfer Protocol - Enable AI Agents to utilize other AI Agents as tools"
)
console = Console()


@app.command(name="create-iatp-wallet")
def create_wallet_cli(
    owner_key: str = typer.Option(..., "--owner-key", help="Owner's private key (REQUIRED INPUT)"),
    operator_address: Optional[str] = typer.Option(None, "--operator-address", help="Operator address (or use --create-operator)"),
    create_operator: bool = typer.Option(False, "--create-operator", help="Generate new operator keypair"),
    wallet_name: str = typer.Option("", "--wallet-name", help="Name for the wallet"),
    wallet_type: str = typer.Option("MCP_SERVER", "--wallet-type", help="Type: CLIENT, HUMAN, MCP_SERVER, WEB_SERVER, AGENT"),
    wallet_description: str = typer.Option("", "--wallet-description", help="Description of the wallet/service"),
    network: str = typer.Option("arbitrum_one", "--network", help="Network (sepolia, arbitrum_one)"),
    rpc_url: Optional[str] = typer.Option(None, "--rpc-url", help="Custom RPC URL"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Save wallet info to JSON file")
):
    """Create a new IATPWallet contract.
    
    The owner creates the wallet themselves (no maintainer key needed).
    
    Examples:
    
      # Create wallet and generate operator (recommended)
      traia-iatp create-iatp-wallet --owner-key 0x... --create-operator --wallet-name "My Server"
      
      # Create wallet with existing operator
      traia-iatp create-iatp-wallet --owner-key 0x... --operator-address 0x... --wallet-type AGENT
    """
    try:
        console.print("\n🔧 Creating IATPWallet...\n", style="bold")
        
        result = create_iatp_wallet(
            owner_private_key=owner_key,
            operator_address=operator_address,
            create_operator=create_operator,
            wallet_name=wallet_name,
            wallet_type=wallet_type,
            wallet_description=wallet_description,
            network=network,
            rpc_url=rpc_url,
            maintainer_private_key=None  # Regular developers don't have maintainer key
        )
        
        # Display results
        console.print("\n" + "="*80, style="green")
        console.print("✅ IATPWallet Created Successfully!", style="bold green")
        console.print("="*80 + "\n", style="green")
        
        # Create table for results
        table = Table(title="Wallet Information", show_header=False)
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Wallet Address", result['wallet_address'])
        table.add_row("Owner", result['owner_address'])
        table.add_row("Operator", result['operator_address'])
        table.add_row("Network", result['network'])
        table.add_row("Transaction", result['transaction_hash'])
        
        if 'operator_private_key' in result:
            table.add_row("Operator Private Key", result['operator_private_key'])
        
        console.print(table)
        
        # Save to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            console.print(f"\n💾 Wallet info saved to: {output}", style="green")
        
        # Show next steps
        console.print("\n📝 Next Steps:", style="bold")
        console.print("1. Save your credentials securely (especially operator private key)")
        console.print("2. Fund the wallet with USDC for payments")
        console.print("3. Set environment variables:")
        console.print(f"   export IATP_WALLET_ADDRESS={result['wallet_address']}")
        if 'operator_private_key' in result:
            console.print(f"   export OPERATOR_PRIVATE_KEY={result['operator_private_key']}")
        console.print("4. Start building with IATP!\n")
        
    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="bold red")
        import traceback
        console.print(traceback.format_exc(), style="red")
        raise typer.Exit(code=1)


@app.command()
def create_agency(
    name: str = typer.Option(..., "--name", "-n", help="Name of the utility agency"),
    description: str = typer.Option(..., "--description", "-d", help="Description of the agency"),
    mcp_name: str = typer.Option(..., "--mcp-name", help="Name of existing MCP server in registry"),
    output_dir: str = typer.Option("utility_agencies", "--output-dir", "-o", help="Output directory"),
    deploy: bool = typer.Option(False, "--deploy", help="Deploy immediately after creation"),
    port: Optional[int] = typer.Option(None, "--port", "-p", help="Port to deploy on"),
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry")
):
    """Create a new utility agency from an existing MCP server in the registry."""
    async def _create():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Creating utility agency...", total=None)
            
            try:
                # Look up MCP server in registry
                mcp_registry = MCPServerRegistry(mongodb_uri)
                try:
                    mcp_data = await mcp_registry.get_mcp_server(mcp_name)
                    
                    if not mcp_data:
                        console.print(f"❌ MCP server '{mcp_name}' not found in registry", style="red")
                        return None, None
                    
                    # Create MCPServer object from registry data
                    mcp_server = MCPServer(
                        id=str(mcp_data.get("_id", "")),
                        name=mcp_data["name"],
                        url=mcp_data["url"],
                        description=mcp_data["description"],
                        server_type=mcp_data.get("server_type", MCPServerType.STREAMABLE_HTTP),
                        capabilities=mcp_data.get("capabilities", []),
                        metadata=mcp_data.get("metadata", {})
                    )
                finally:
                    mcp_registry.close()
                
                # Create agency generator
                generator = IATPServerAgentGenerator(output_base_dir=Path(output_dir))
                
                # Generate the agency
                agency = generator.generate_agent(
                    mcp_server=mcp_server,
                    agency_name=name,
                    agency_description=description,
                    use_simple_server=False  # Use modular server for CLI
                )
                
                folder_path = agency.code_path
                
                progress.update(task, description="Agency created successfully!")
                
                console.print(f"\n✅ Created utility agency: {agency.name}")
                console.print(f"   ID: {agency.id}")
                console.print(f"   Status: {agency.status}")
                console.print(f"   Folder: {folder_path}")
                console.print(f"   MCP Server: {mcp_server.name}")
                console.print(f"   Capabilities: {', '.join(agency.capabilities)}")
                
                if deploy:
                    progress.update(task, description="Deploying agency to Docker...")
                    
                    # Use the docker utilities to run the generated agency
                    runner = LocalDockerRunner()
                    deployment_info = await runner.run_agent_docker(
                        agent_path=Path(folder_path),
                        port=port or 8000,
                        detached=True
                    )
                    
                    if deployment_info["success"]:
                        console.print(f"\n🚀 Deployed agency:")
                        console.print(f"   Base URL: {deployment_info['base_url']}")
                        console.print(f"   IATP Endpoint: {deployment_info['iatp_endpoint']}")
                        console.print(f"   Container: {deployment_info['container_name']}")
                        console.print(f"   Port: {deployment_info['port']}")
                        console.print(f"\n📝 Useful commands:")
                        console.print(f"   View logs: {deployment_info['logs_command']}")
                        console.print(f"   Stop: {deployment_info['stop_command']}")
                        
                        # Register the deployed agency if MongoDB is configured
                        if mongodb_uri:
                            registry = UtilityAgentRegistry(mongodb_uri)
                            try:
                                await registry.add_utility_agency(
                                    agency=agency,
                                    endpoint=deployment_info['iatp_endpoint'],
                                    tags=["docker", "cli-deployed"]
                                )
                                console.print(f"   ✅ Registered in MongoDB")
                            finally:
                                registry.close()
                    else:
                        console.print(f"❌ Deployment failed", style="red")
                
                return agency, folder_path
                
            except Exception as e:
                console.print(f"❌ Error creating agency: {e}", style="red")
                raise
    
    asyncio.run(_create())


@app.command()
def register_mcp(
    name: str = typer.Option(..., "--name", "-n", help="Name of the MCP server"),
    url: str = typer.Option(..., "--url", "-u", help="URL of the MCP server"),
    description: str = typer.Option(..., "--description", "-d", help="Description of the MCP server"),
    server_type: str = typer.Option("streamable-http", "--type", "-t", help="Server type (streamable-http only)"),
    capabilities: Optional[List[str]] = typer.Option(None, "--capability", "-c", help="Server capabilities"),
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry")
):
    """Register an MCP server in the registry."""
    async def _register():
        registry = MCPServerRegistry(mongodb_uri)
        
        try:
            # Convert string to enum if necessary
            if server_type == "streamable-http":
                server_type_enum = MCPServerType.STREAMABLE_HTTP
            else:
                server_type_enum = server_type
                
            server_id = await registry.add_mcp_server(
                name=name,
                url=url,
                description=description,
                server_type=server_type_enum,
                capabilities=capabilities or []
            )
            
            console.print(f"✅ Registered MCP server '{name}' with ID: {server_id}")
            
        finally:
            registry.close()
    
    asyncio.run(_register())


@app.command()
def list_agencies(
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    active_only: bool = typer.Option(True, "--active-only", help="Show only active agencies")
):
    """List all registered utility agencies."""
    async def _list():
        registry = UtilityAgentRegistry(mongodb_uri)
        
        try:
            agencies = await registry.query_agencies(active_only=active_only, limit=100)
            
            if not agencies:
                console.print("No agencies found.", style="yellow")
                return
            
            table = Table(title="Registered Utility Agencies")
            table.add_column("Name", style="cyan")
            table.add_column("ID", style="magenta")
            table.add_column("Endpoint", style="green")
            table.add_column("Capabilities", style="yellow")
            table.add_column("Active", style="blue")
            
            for agency in agencies:
                table.add_row(
                    agency.name,
                    agency.agency_id[:8] + "...",
                    str(agency.endpoint),
                    ", ".join(agency.capabilities[:3]) + ("..." if len(agency.capabilities) > 3 else ""),
                    "✅" if agency.is_active else "❌"
                )
            
            console.print(table)
            
        finally:
            registry.close()
    
    asyncio.run(_list())


@app.command()
def list_mcp_servers(
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    server_type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by server type")
):
    """List all registered MCP servers."""
    async def _list():
        registry = MCPServerRegistry(mongodb_uri)
        
        try:
            servers = await registry.query_mcp_servers(server_type=server_type)
            
            if not servers:
                console.print("No MCP servers found.", style="yellow")
                return
            
            table = Table(title="Registered MCP Servers")
            table.add_column("Name", style="cyan")
            table.add_column("URL", style="green")
            table.add_column("Type", style="yellow")
            table.add_column("Description", style="white")
            table.add_column("Capabilities", style="magenta")
            
            for server in servers:
                table.add_row(
                    server["name"],
                    server["url"],
                    server.get("server_type", "streamable-http"),
                    server["description"][:40] + "..." if len(server["description"]) > 40 else server["description"],
                    ", ".join(server.get("capabilities", [])[:3]) + ("..." if len(server.get("capabilities", [])) > 3 else "")
                )
            
            console.print(table)
            
        finally:
            registry.close()
    
    asyncio.run(_list())


@app.command()
def search_agencies(
    query: Optional[str] = typer.Argument(None, help="Search query"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", "-t", help="Filter by tags"),
    capabilities: Optional[List[str]] = typer.Option(None, "--capability", "-c", help="Filter by capabilities"),
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of results")
):
    """Search for utility agencies."""
    async def _search():
        registry = UtilityAgentRegistry(mongodb_uri)
        
        try:
            agencies = await registry.query_agencies(
                query=query,
                tags=tags,
                capabilities=capabilities,
                active_only=True,
                limit=limit
            )
            
            if not agencies:
                console.print("No agencies found matching criteria.", style="yellow")
                return
            
            table = Table(title=f"Search Results ({len(agencies)} found)")
            table.add_column("Name", style="cyan")
            table.add_column("Description", style="white")
            table.add_column("Capabilities", style="yellow")
            table.add_column("Tags", style="green")
            
            for agency in agencies:
                table.add_row(
                    agency.name,
                    agency.description[:50] + "..." if len(agency.description) > 50 else agency.description,
                    ", ".join(agency.capabilities[:3]) + ("..." if len(agency.capabilities) > 3 else ""),
                    ", ".join(agency.tags[:3]) + ("..." if len(agency.tags) > 3 else "")
                )
            
            console.print(table)
            
        finally:
            registry.close()
    
    asyncio.run(_search())


@app.command()
def deploy(
    agency_path: Path = typer.Argument(..., help="Path to generated agency directory"),
    port: Optional[int] = typer.Option(None, "--port", "-p", help="Port to deploy on"),
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    use_script: bool = typer.Option(False, "--use-script", help="Use the run_local_docker.sh script")
):
    """Deploy a utility agency from a generated directory."""
    async def _deploy():
        if not agency_path.exists():
            console.print(f"❌ Directory not found: {agency_path}", style="red")
            return
        
        # Check if it's a valid agency directory
        required_files = ["Dockerfile", "pyproject.toml"]
        missing_files = [f for f in required_files if not (agency_path / f).exists()]
        if missing_files:
            console.print(f"❌ Invalid agency directory. Missing files: {', '.join(missing_files)}", style="red")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Deploying agency...", total=None)
            
            try:
                if use_script:
                    # Use the generated run_local_docker.sh script
                    script_path = agency_path / "run_local_docker.sh"
                    if not script_path.exists():
                        console.print(f"❌ run_local_docker.sh not found in {agency_path}", style="red")
                        return
                    
                    progress.update(task, description="Running deployment script...")
                    use_run_local_docker_script(str(agency_path))
                    
                    console.print(f"\n🚀 Agency deployed using run_local_docker.sh")
                    console.print(f"   Check the script output for connection details")
                else:
                    # Use LocalDockerRunner
                    runner = LocalDockerRunner()
                    deployment_info = await runner.run_agent_docker(
                        agent_path=agency_path,
                        port=port or 8000,
                        detached=True
                    )
                    
                    if deployment_info["success"]:
                        console.print(f"\n🚀 Deployed agency from: {agency_path}")
                        console.print(f"   Base URL: {deployment_info['base_url']}")
                        console.print(f"   IATP Endpoint: {deployment_info['iatp_endpoint']}")
                        console.print(f"   Container: {deployment_info['container_name']}")
                        console.print(f"   Port: {deployment_info['port']}")
                        console.print(f"\n📝 Useful commands:")
                        console.print(f"   View logs: {deployment_info['logs_command']}")
                        console.print(f"   Stop: {deployment_info['stop_command']}")
                        
                        # If MongoDB URI is provided and agent_config.json exists, register it
                        if mongodb_uri and (agency_path / "agent_config.json").exists():
                            with open(agency_path / "agent_config.json", 'r') as f:
                                agency_data = json.load(f)
                            
                            agency = UtilityAgent(**agency_data)
                            
                            registry = UtilityAgentRegistry(mongodb_uri)
                            try:
                                await registry.add_utility_agency(
                                    agency=agency,
                                    endpoint=deployment_info['iatp_endpoint'],
                                    tags=["docker", "cli-deployed"]
                                )
                                console.print(f"   ✅ Registered in MongoDB")
                            finally:
                                registry.close()
                    else:
                        console.print(f"❌ Deployment failed", style="red")
                
            except Exception as e:
                console.print(f"❌ Deployment failed: {e}", style="red")
                raise
    
    asyncio.run(_deploy())


@app.command()
def find_tools(
    query: Optional[str] = typer.Argument(None, help="Search query for tools"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", "-t", help="Filter by tags"),
    capabilities: Optional[List[str]] = typer.Option(None, "--capability", "-c", help="Filter by capabilities"),
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Save tools configuration to file")
):
    """Find utility agency tools for use in CrewAI."""
    tools = create_utility_agency_tools(
        mongodb_uri=mongodb_uri,
        query=query,
        tags=tags,
        capabilities=capabilities
    )
    
    if not tools:
        console.print("No tools found matching criteria.", style="yellow")
        return
    
    table = Table(title=f"Available Tools ({len(tools)} found)")
    table.add_column("Tool Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Endpoint", style="green")
    
    tools_config = []
    for tool in tools:
        table.add_row(
            tool.name,
            tool.description[:60] + "..." if len(tool.description) > 60 else tool.description,
            tool.endpoint
        )
        
        tools_config.append({
            "name": tool.name,
            "description": tool.description,
            "endpoint": tool.endpoint,
            "agency_id": tool.agency_id,
            "capabilities": tool.capabilities
        })
    
    console.print(table)
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(tools_config, f, indent=2)
        console.print(f"\n💾 Tools configuration saved to: {output_file}", style="green")


@app.command()
def example_crew():
    """Show an example of how to use utility agencies in a CrewAI crew."""
    example_code = '''
# Example: Using utility agencies in a CrewAI crew

from crewai import Agent, Crew, Task
from traia_iatp import create_utility_agency_tools

# Find and create tools from utility agencies
tools = create_utility_agency_tools(
    query="weather data analysis",  # Search for relevant agencies
    tags=["weather", "api"],        # Filter by tags
    capabilities=["forecast"]       # Filter by capabilities
)

# Create an agent with utility agency tools
analyst = Agent(
    role="Data Analyst",
    goal="Analyze weather patterns and provide insights",
    backstory="You are an expert at analyzing weather data and trends.",
    tools=tools,  # Use the utility agency tools
    allow_delegation=False,
    verbose=True
)

# Create a task
analysis_task = Task(
    description="Analyze the weather forecast for New York City for the next week",
    expected_output="A detailed analysis of weather patterns and recommendations",
    agent=analyst
)

# Create and run the crew
crew = Crew(
    agents=[analyst],
    tasks=[analysis_task],
    verbose=True
)

result = crew.kickoff()
print(result)
'''
    
    console.print("📚 Example: Using Utility Agencies in CrewAI\n", style="bold cyan")
    console.print(example_code, style="cyan")


if __name__ == "__main__":
    app() 