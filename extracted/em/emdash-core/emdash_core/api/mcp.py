"""MCP server configuration endpoints."""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/mcps", tags=["mcp"])


class MCPServerInfo(BaseModel):
    """Information about an MCP server."""

    name: str
    command: str
    args: list[str] = []
    enabled: bool = True
    timeout: int = 30
    source: str = "local"  # "local" or "global"


class MCPListResponse(BaseModel):
    """Response for listing MCP servers."""

    servers: list[MCPServerInfo]
    count: int
    config_path: Optional[str] = None


def _get_global_mcp_config_path() -> Path:
    """Get the global MCP config path."""
    return Path.home() / ".emdash" / "mcp.json"


def _get_local_mcp_config_path() -> Path:
    """Get the local MCP config path."""
    return Path.cwd() / ".emdash" / "mcp.json"


def _load_mcp_servers_from_file(path: Path, source: str) -> list[MCPServerInfo]:
    """Load MCP servers from a config file."""
    import json

    servers = []
    if not path.exists():
        return servers

    try:
        with open(path) as f:
            data = json.load(f)

        mcp_servers = data.get("mcpServers", {})
        for name, config in mcp_servers.items():
            servers.append(
                MCPServerInfo(
                    name=name,
                    command=config.get("command", ""),
                    args=config.get("args", []),
                    enabled=config.get("enabled", True),
                    timeout=config.get("timeout", 30),
                    source=source,
                )
            )
    except Exception:
        pass

    return servers


@router.get("", response_model=MCPListResponse)
async def list_mcp_servers():
    """List all MCP servers from global and local config files.

    MCP servers are loaded from:
    1. Global: ~/.emdash/mcp.json
    2. Local: .emdash/mcp.json (can override global)
    """
    all_servers = []
    seen_names = set()
    config_path = None

    # Load global servers first
    global_path = _get_global_mcp_config_path()
    global_servers = _load_mcp_servers_from_file(global_path, "global")
    for server in global_servers:
        all_servers.append(server)
        seen_names.add(server.name)

    # Load local servers (can override global)
    local_path = _get_local_mcp_config_path()
    local_servers = _load_mcp_servers_from_file(local_path, "local")
    for server in local_servers:
        if server.name in seen_names:
            # Remove global version, local overrides
            all_servers = [s for s in all_servers if s.name != server.name]
        all_servers.append(server)

    if local_path.exists():
        config_path = str(local_path)
    elif global_path.exists():
        config_path = str(global_path)

    return MCPListResponse(
        servers=all_servers,
        count=len(all_servers),
        config_path=config_path,
    )


class CreateMCPRequest(BaseModel):
    """Request to create/update an MCP server."""

    name: str
    command: str
    args: list[str] = []
    enabled: bool = True
    timeout: int = 30


class CreateMCPResponse(BaseModel):
    """Response after creating an MCP server."""

    success: bool
    name: str
    config_path: str


def _save_mcp_server(path: Path, name: str, config: dict) -> None:
    """Add or update an MCP server in a config file."""
    import json

    data = {}
    if path.exists():
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception:
            pass

    if "mcpServers" not in data:
        data["mcpServers"] = {}

    data["mcpServers"][name] = config

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


@router.post("", response_model=CreateMCPResponse)
async def create_mcp_server(request: CreateMCPRequest):
    """Create or update an MCP server in the local .emdash/mcp.json config."""
    local_path = _get_local_mcp_config_path()

    config = {
        "command": request.command,
        "args": request.args,
        "enabled": request.enabled,
        "timeout": request.timeout,
    }

    _save_mcp_server(local_path, request.name, config)

    return CreateMCPResponse(
        success=True,
        name=request.name,
        config_path=str(local_path),
    )


@router.get("/{server_name}")
async def get_mcp_server(server_name: str):
    """Get a specific MCP server by name."""
    from fastapi import HTTPException

    # Check local first, then global
    for path, source in [
        (_get_local_mcp_config_path(), "local"),
        (_get_global_mcp_config_path(), "global"),
    ]:
        servers = _load_mcp_servers_from_file(path, source)
        for server in servers:
            if server.name == server_name:
                return server

    raise HTTPException(status_code=404, detail=f"MCP server '{server_name}' not found")
