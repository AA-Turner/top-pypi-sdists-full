"""MCP Server Manager for lifecycle and tool registry.

This module provides the MCPServerManager class that handles:
- Loading MCP config from .emdash/mcp.json
- Starting/stopping MCP servers
- Registering tools from all servers
- Handling tool name collisions
"""

import atexit
import hashlib
import json
from pathlib import Path
from typing import Optional

from .client import GenericMCPClient, MCPResponse, MCPToolInfo, MCPError
from .config import MCPConfigFile, MCPServerConfig, get_default_mcp_config_path, ensure_mcp_config
from ...utils.logger import log


class MCPServerManager:
    """Manages lifecycle of multiple MCP servers.

    This class is responsible for:
    - Loading MCP server configurations from file
    - Starting servers on demand (lazy initialization)
    - Maintaining a unified tool registry from all servers
    - Handling tool name collisions with prefixing
    - Graceful shutdown of all servers

    Example:
        manager = MCPServerManager(config_path=Path(".emdash/mcp.json"))

        # List all available tools from all servers
        tools = manager.get_all_tools()

        # Call a tool (server starts automatically if needed)
        result = manager.call_tool("read_file", {"path": "/tmp/test.txt"})

        # Cleanup
        manager.shutdown_all()
    """

    def __init__(self, config_path: Optional[Path] = None, repo_root: Optional[Path] = None):
        """Initialize the MCP server manager.

        Args:
            config_path: Path to mcp.json config file. If None, uses default.
            repo_root: Repository root for default config path resolution.
        """
        self.repo_root = repo_root or Path.cwd()
        self.config_path = config_path or get_default_mcp_config_path(self.repo_root)

        self._config: Optional[MCPConfigFile] = None
        self._clients: dict[str, GenericMCPClient] = {}
        self._tool_registry: dict[str, tuple[str, MCPToolInfo]] = {}  # tool_name -> (server_name, tool_info)
        self._started = False
        self._tools_discovered = False

        # Register atexit handler for cleanup
        atexit.register(self._cleanup)

    def _cleanup(self) -> None:
        """Cleanup handler for atexit."""
        try:
            self.shutdown_all()
        except Exception as e:
            log.warning(f"Error during MCP cleanup: {e}")

    def load_config(self) -> MCPConfigFile:
        """Load MCP configuration from file, creating default if needed.

        Returns:
            MCPConfigFile with loaded server configurations
        """
        if self._config is None:
            self._config = ensure_mcp_config(self.config_path)
        return self._config

    def reload_config(self) -> MCPConfigFile:
        """Reload configuration from file.

        Returns:
            MCPConfigFile with fresh configuration
        """
        self._config = MCPConfigFile.load(self.config_path)
        return self._config

    def save_config(self) -> None:
        """Save current configuration to file."""
        if self._config:
            self._config.save(self.config_path)

    def get_enabled_servers(self) -> list[MCPServerConfig]:
        """Get list of enabled server configurations.

        Returns:
            List of enabled MCPServerConfig instances
        """
        config = self.load_config()
        return config.get_enabled_servers()

    # ── Tool discovery & caching ──────────────────────────────────────────

    def _get_cache_path(self) -> Path:
        """Get path for the MCP tool definition cache file."""
        return self.config_path.parent / ".mcp_tool_cache.json"

    def _compute_config_hash(self) -> str:
        """Compute hash of enabled MCP server configs for cache invalidation."""
        config = self.load_config()
        enabled = config.get_enabled_servers()
        data = json.dumps(
            [s.to_dict() for s in sorted(enabled, key=lambda s: s.name)],
            sort_keys=True,
        )
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _load_tool_cache(self) -> bool:
        """Load tool definitions from disk cache.

        Returns:
            True if cache was valid and loaded, False on cache miss.
        """
        cache_path = self._get_cache_path()
        if not cache_path.exists():
            return False

        try:
            cache_data = json.loads(cache_path.read_text())
            if cache_data.get("config_hash") != self._compute_config_hash():
                log.info("MCP tool cache stale (config changed), will re-discover")
                return False

            for entry in cache_data.get("tools", []):
                tool_info = MCPToolInfo(
                    name=entry["name"],
                    description=entry.get("description", ""),
                    input_schema=entry.get("input_schema", {}),
                )
                registered_name = entry.get("registered_name", entry["name"])
                server_name = entry["server_name"]
                self._tool_registry[registered_name] = (server_name, tool_info)

            log.info(f"Loaded {len(self._tool_registry)} MCP tools from cache")
            return True

        except Exception as e:
            log.warning(f"Failed to load MCP tool cache: {e}")
            return False

    def _save_tool_cache(self) -> None:
        """Persist current tool registry to disk cache."""
        try:
            cache_data = {
                "config_hash": self._compute_config_hash(),
                "tools": [
                    {
                        "registered_name": name,
                        "server_name": server_name,
                        "name": tool_info.name,
                        "description": tool_info.description,
                        "input_schema": tool_info.input_schema,
                    }
                    for name, (server_name, tool_info) in self._tool_registry.items()
                ],
            }
            cache_path = self._get_cache_path()
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(cache_data, indent=2))
            log.info(f"Saved MCP tool cache ({len(cache_data['tools'])} tools)")
        except Exception as e:
            log.warning(f"Failed to save MCP tool cache: {e}")

    def discover_tools(self) -> None:
        """Discover available MCP tools, using disk cache when possible.

        On cache hit: populates the tool registry without starting any servers.
        On cache miss: starts servers to discover tools, then saves cache.
        Servers started for discovery are kept running.
        """
        if self._tools_discovered:
            return

        if self._load_tool_cache():
            self._tools_discovered = True
            return

        # Cache miss — start servers to discover tools
        self.start_all_enabled()
        self._tools_discovered = True
        self._save_tool_cache()

    # ── Server lifecycle ──────────────────────────────────────────────────

    def _resolve_args(self, args: list[str], resolved_env: dict[str, str]) -> list[str]:
        """Resolve ${VAR} placeholders in args using resolved env.

        Args:
            args: List of argument strings
            resolved_env: Already-resolved environment variables

        Returns:
            List of args with placeholders resolved
        """
        import re
        pattern = re.compile(r"\$\{([^}]+)\}")
        resolved = []
        for arg in args:
            def replace_var(m):
                var_name = m.group(1)
                return resolved_env.get(var_name, "")
            resolved.append(pattern.sub(replace_var, arg))
        return resolved

    def start_server(self, name: str) -> GenericMCPClient:
        """Start an MCP server by name.

        Args:
            name: Server name from configuration

        Returns:
            Started GenericMCPClient instance

        Raises:
            MCPError: If server not found in config or fails to start
        """
        # Check if already running
        if name in self._clients and self._clients[name].is_running:
            return self._clients[name]

        config = self.load_config()
        server_config = config.get_server(name)

        if not server_config:
            raise MCPError(f"MCP server '{name}' not found in configuration")

        if not server_config.enabled:
            raise MCPError(f"MCP server '{name}' is disabled")

        # Resolve env vars first, then args
        resolved_env = server_config.get_resolved_env()
        resolved_args = self._resolve_args(server_config.args, resolved_env)

        # Create and start client
        client = GenericMCPClient(
            name=server_config.name,
            command=server_config.command,
            args=resolved_args,
            env=resolved_env,
            timeout=server_config.timeout,
        )

        try:
            client.start()
            self._clients[name] = client

            # Register tools from this server
            self._register_server_tools(name, client)

            return client
        except Exception as e:
            log.error(f"Failed to start MCP server '{name}': {e}")
            raise

    def stop_server(self, name: str) -> bool:
        """Stop an MCP server by name.

        Args:
            name: Server name

        Returns:
            True if server was stopped, False if not running
        """
        if name not in self._clients:
            return False

        client = self._clients[name]
        client.stop()
        del self._clients[name]

        # Unregister tools from this server
        self._unregister_server_tools(name)

        return True

    def start_all_enabled(self) -> list[str]:
        """Start all enabled MCP servers.

        Returns:
            List of server names that were started successfully
        """
        started = []
        for server_config in self.get_enabled_servers():
            try:
                self.start_server(server_config.name)
                started.append(server_config.name)
            except MCPError as e:
                log.warning(f"Failed to start MCP server '{server_config.name}': {e}")

        self._started = True
        return started

    def shutdown_all(self) -> None:
        """Stop all running MCP servers."""
        for name in list(self._clients.keys()):
            try:
                self.stop_server(name)
            except Exception as e:
                log.warning(f"Error stopping MCP server '{name}': {e}")

        self._clients.clear()
        self._tool_registry.clear()
        self._started = False
        self._tools_discovered = False

    def _register_server_tools(self, server_name: str, client: GenericMCPClient) -> None:
        """Register tools from a server into the unified registry.

        Handles name collisions by prefixing with server name.

        Args:
            server_name: Name of the server
            client: Started client to get tools from
        """
        try:
            tools = client.list_tools()
        except MCPError as e:
            log.warning(f"Failed to list tools from '{server_name}': {e}")
            return

        for tool in tools:
            # Check for name collision
            if tool.name in self._tool_registry:
                existing_server, _ = self._tool_registry[tool.name]
                # Use prefixed name for collision
                prefixed_name = f"{server_name}_{tool.name}"
                log.warning(
                    f"Tool name collision: '{tool.name}' exists in '{existing_server}'. "
                    f"Registering as '{prefixed_name}' for server '{server_name}'."
                )
                self._tool_registry[prefixed_name] = (server_name, tool)
            else:
                self._tool_registry[tool.name] = (server_name, tool)

        log.info(f"Registered {len(tools)} tools from MCP server '{server_name}'")

    def _unregister_server_tools(self, server_name: str) -> None:
        """Remove tools from a server from the registry.

        Args:
            server_name: Name of the server
        """
        to_remove = [
            name for name, (srv, _) in self._tool_registry.items()
            if srv == server_name
        ]
        for name in to_remove:
            del self._tool_registry[name]

    def get_all_tools(self) -> list[tuple[str, str, MCPToolInfo]]:
        """Get all registered tools from all servers.

        Uses cached tool definitions when available to avoid starting servers.

        Returns:
            List of (tool_name, server_name, MCPToolInfo) tuples
        """
        if not self._tools_discovered:
            self.discover_tools()

        return [
            (name, server_name, tool_info)
            for name, (server_name, tool_info) in self._tool_registry.items()
        ]

    def get_tool(self, name: str) -> Optional[tuple[str, MCPToolInfo]]:
        """Get a tool by name.

        Uses cached tool definitions when available to avoid starting servers.

        Args:
            name: Tool name (may be prefixed for collisions)

        Returns:
            (server_name, MCPToolInfo) tuple or None if not found
        """
        if not self._tools_discovered:
            self.discover_tools()

        return self._tool_registry.get(name)

    def call_tool(self, tool_name: str, arguments: dict) -> MCPResponse:
        """Call a tool by name.

        Automatically routes to the correct server.

        Args:
            tool_name: Tool name (may be prefixed)
            arguments: Tool arguments

        Returns:
            MCPResponse from the tool call

        Raises:
            MCPError: If tool not found or call fails
        """
        tool_info = self.get_tool(tool_name)
        if not tool_info:
            raise MCPError(f"Tool '{tool_name}' not found in any MCP server")

        server_name, mcp_tool = tool_info

        # Start server on demand if not running (lazy startup)
        if server_name not in self._clients or not self._clients[server_name].is_running:
            self.start_server(server_name)

        client = self._clients[server_name]

        # Use original tool name (strip prefix if present)
        original_name = mcp_tool.name

        return client.call_tool(original_name, arguments)

    def add_server(self, config: MCPServerConfig) -> None:
        """Add a new server to configuration.

        Args:
            config: Server configuration to add
        """
        self.load_config()
        self._config.add_server(config)
        self.save_config()
        log.info(f"Added MCP server '{config.name}' to configuration")

    def remove_server(self, name: str) -> bool:
        """Remove a server from configuration.

        Also stops the server if running.

        Args:
            name: Server name to remove

        Returns:
            True if removed, False if not found
        """
        # Stop if running
        if name in self._clients:
            self.stop_server(name)

        self.load_config()
        if self._config.remove_server(name):
            self.save_config()
            log.info(f"Removed MCP server '{name}' from configuration")
            return True
        return False

    def enable_server(self, name: str) -> bool:
        """Enable a server.

        Args:
            name: Server name

        Returns:
            True if enabled, False if not found
        """
        self.load_config()
        server = self._config.get_server(name)
        if server:
            server.enabled = True
            self.save_config()
            return True
        return False

    def disable_server(self, name: str) -> bool:
        """Disable a server.

        Also stops the server if running.

        Args:
            name: Server name

        Returns:
            True if disabled, False if not found
        """
        # Stop if running
        if name in self._clients:
            self.stop_server(name)

        self.load_config()
        server = self._config.get_server(name)
        if server:
            server.enabled = False
            self.save_config()
            return True
        return False

    def list_servers(self) -> list[dict]:
        """List all configured servers with their status.

        Returns:
            List of server info dicts with keys:
            - name: Server name
            - command: Server command
            - enabled: Whether enabled
            - running: Whether currently running
            - tool_count: Number of tools (if running)
        """
        self.load_config()
        servers = []

        for name, server_config in self._config.servers.items():
            is_running = name in self._clients and self._clients[name].is_running
            tool_count = len([
                1 for _, (srv, _) in self._tool_registry.items()
                if srv == name
            ]) if is_running else 0

            servers.append({
                "name": name,
                "command": server_config.command,
                "args": server_config.args,
                "enabled": server_config.enabled,
                "running": is_running,
                "tool_count": tool_count,
            })

        return servers

    def describe_server(self, name: str) -> Optional[dict]:
        """Get detailed information about a server including its tools.

        Args:
            name: Server name

        Returns:
            Dict with server details and tools, or None if not found
        """
        self.load_config()
        server_config = self._config.get_server(name)

        if not server_config:
            return None

        is_running = name in self._clients and self._clients[name].is_running

        # Get tools for this server
        tools = []
        if is_running:
            for tool_name, (srv, tool_info) in self._tool_registry.items():
                if srv == name:
                    tools.append({
                        "name": tool_name,
                        "original_name": tool_info.name,
                        "description": tool_info.description,
                        "input_schema": tool_info.input_schema,
                    })

        return {
            "name": name,
            "command": server_config.command,
            "args": server_config.args,
            "env": server_config.env,
            "enabled": server_config.enabled,
            "timeout": server_config.timeout,
            "running": is_running,
            "tools": tools,
        }


# Global manager instance (lazy initialization)
_manager: Optional[MCPServerManager] = None


def get_mcp_manager(config_path: Optional[Path] = None) -> MCPServerManager:
    """Get or create the global MCP manager instance.

    Args:
        config_path: Optional path to override default config location

    Returns:
        MCPServerManager instance
    """
    global _manager
    if _manager is None:
        _manager = MCPServerManager(config_path=config_path)
    return _manager


def reset_mcp_manager() -> None:
    """Reset the global MCP manager (for testing)."""
    global _manager
    if _manager:
        _manager.shutdown_all()
    _manager = None
