import json
import logging
from typing import Optional, Dict, Any
import os
import typer

def load_config(config_file: Optional[str]) -> Dict[str, Any]:
    """Load the configuration file.
    
    Args:
        config_file: Path to the config file. If not provided, the MCP_CLI_CONFIG_PATH environment variable is used, or the config file in the root of the repository.
        
    Returns:
        Dictionary containing the MCP servers configuration.
    """
    env_config_path = os.getenv("MCP_CLI_CONFIG_PATH", None)

    if config_file and os.path.exists(config_file):
        config_file_used = config_file
    elif env_config_path and os.path.exists(env_config_path):
        config_file_used = env_config_path
    else:
        typer.echo(f"Config file not found, please set the MCP_CLI_CONFIG_PATH environment variable to the path where your config lives, e.g. `export MCP_CLI_CONFIG_PATH=~/.mcp/server_config.json` or provide it with the --config flag.")
        raise typer.Exit(code=1)

    try:
        with open(config_file_used, 'r') as f:
            config = json.load(f)
            if "mcpServers" not in config or not isinstance(config["mcpServers"], dict) or not config["mcpServers"]:
                raise ValueError(f"MCP servers configuration ('mcpServers') is missing, not a valid dictionary, or empty in '{config_file_used}'.")
    
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in config file '{config_file_used}'")
        raise
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        raise
    
    return config


def get_servers_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load and validate MCP servers configuration.
    
    Args:
        config_file: Path to the config file
        
    Returns:
        Dictionary containing the MCP servers configuration
        
    Raises:
        typer.Exit: If configuration is invalid or servers not found
    """
    config = load_config(config_file)
    
    if not config or "mcpServers" not in config:
        typer.secho("No MCP servers found in configuration file.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    
    mcp_servers_config: Dict[str, Any] = config["mcpServers"]
    
    if not mcp_servers_config:
        typer.secho("No MCP servers configured.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
        
    return mcp_servers_config


def get_server_config(server_name: str, config_file: Optional[str] = None) -> Dict[str, Any]:
    mcp_servers_config = get_servers_config(config_file)

    if server_name not in mcp_servers_config:
        typer.secho(f"Server '{server_name}' not found in configuration file '{config_file}'.", fg=typer.colors.RED, err=True)
        available_servers = list(mcp_servers_config.keys())
        if available_servers:
            typer.echo("Available servers are: " + ", ".join(available_servers))
        raise typer.Exit(code=1)
        
    server_config_dict = mcp_servers_config[server_name]

    return server_config_dict
