"""MCPTool — lets the LLM agent add, remove, and manage MCP servers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, TYPE_CHECKING

from .base import BaseTool, ToolCategory, ToolResult

if TYPE_CHECKING:
    from ..toolkits.base import BaseToolkit

log = logging.getLogger(__name__)


class MCPTool(BaseTool):
    """Add, remove, list, enable, or disable MCP servers.

    MCP (Model Context Protocol) servers extend the agent with new tools.
    Configuration is persisted to ``.emdash/mcp.json``.
    """

    name = "manage_mcp"
    description = (
        "Add, remove, list, enable, or disable MCP (Model Context Protocol) servers. "
        "MCP servers extend your capabilities with new tools. "
        "Use action='add' with name/command/args to register a new server, "
        "action='list' to see configured servers, "
        "action='remove'/'enable'/'disable' to manage existing ones."
    )
    category = ToolCategory.LEARNING

    def __init__(self, toolkit: BaseToolkit | None = None):
        super().__init__(connection=False)
        self._toolkit = toolkit

    # -- Schema --------------------------------------------------------------

    def get_schema(self) -> dict:
        return self._make_schema(
            {
                "action": {
                    "type": "string",
                    "enum": ["add", "remove", "list", "enable", "disable"],
                    "description": "Action to perform.",
                },
                "name": {
                    "type": "string",
                    "description": "Server name (required for add/remove/enable/disable).",
                },
                "command": {
                    "type": "string",
                    "description": (
                        "Command to run the MCP server (required for add). "
                        "E.g. 'npx', 'uvx', 'docker'."
                    ),
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Command arguments (for add).",
                },
                "env": {
                    "type": "object",
                    "description": (
                        "Environment variables as {KEY: VALUE} (for add). "
                        "Use ${VAR} syntax to reference host env vars."
                    ),
                },
            },
            required=["action"],
        )

    # -- Execute -------------------------------------------------------------

    def execute(self, **kwargs: Any) -> ToolResult:
        action: str = kwargs.get("action", "")
        name: str | None = kwargs.get("name")
        command: str | None = kwargs.get("command")
        args: list[str] | None = kwargs.get("args")
        env: dict[str, str] | None = kwargs.get("env")

        dispatch = {
            "add": self._add,
            "remove": self._remove,
            "list": self._list,
            "enable": self._enable,
            "disable": self._disable,
        }
        handler = dispatch.get(action)
        if handler is None:
            return ToolResult.error_result(
                f"Unknown action: {action}",
                suggestions=["Use one of: add, remove, list, enable, disable"],
            )
        return handler(name=name, command=command, args=args, env=env)

    # -- Helpers -------------------------------------------------------------

    def _config_path(self) -> Path:
        if self._toolkit and self._toolkit._mcp_manager:
            return self._toolkit._mcp_manager.config_path
        return Path.cwd() / ".emdash" / "mcp.json"

    def _try_hot_load(self, server_name: str) -> list[str]:
        """Start the server and register its tools into the running toolkit."""
        new_tool_names: list[str] = []
        if not self._toolkit:
            return new_tool_names

        try:
            from ..mcp.manager import MCPServerManager
            from ..mcp.tool_factory import create_tools_from_mcp

            manager = self._toolkit._mcp_manager
            if manager is None:
                manager = MCPServerManager(config_path=self._config_path())
                self._toolkit._mcp_manager = manager
            else:
                manager.reload_config()

            manager.start_server(server_name)

            for tool in create_tools_from_mcp(manager):
                tool_entry = manager.get_tool(tool.name)
                if tool_entry and tool_entry[0] == server_name:
                    if tool.name not in self._toolkit._tools:
                        self._toolkit.register_tool(tool)
                        new_tool_names.append(tool.name)
        except Exception as exc:
            log.debug("Hot-load of MCP server '%s' failed: %s", server_name, exc)

        return new_tool_names

    # -- Actions -------------------------------------------------------------

    def _add(self, *, name: str | None, command: str | None, args: list[str] | None, env: dict | None) -> ToolResult:
        if not name:
            return ToolResult.error_result("'name' is required for add action.")
        if not command:
            return ToolResult.error_result("'command' is required for add action.")

        from ..mcp.config import MCPServerConfig, MCPConfigFile

        config_path = self._config_path()
        config_file = MCPConfigFile.load(config_path) if config_path.exists() else MCPConfigFile()

        config_file.add_server(MCPServerConfig(
            name=name,
            command=command,
            args=args or [],
            env=env or {},
            enabled=True,
        ))
        config_file.save(config_path)

        new_tools = self._try_hot_load(name)

        msg = f"MCP server '{name}' added and saved to {config_path}."
        if new_tools:
            msg += f" {len(new_tools)} tools now available: {', '.join(new_tools)}"
        else:
            msg += " Tools will be available on next session."

        return ToolResult.success_result(data={
            "name": name,
            "command": command,
            "args": args or [],
            "config_path": str(config_path),
            "hot_loaded_tools": new_tools,
            "message": msg,
        })

    def _remove(self, *, name: str | None, **_: Any) -> ToolResult:
        if not name:
            return ToolResult.error_result("'name' is required for remove action.")

        from ..mcp.config import MCPConfigFile

        config_path = self._config_path()
        if not config_path.exists():
            return ToolResult.error_result(f"No MCP config at {config_path}")

        config_file = MCPConfigFile.load(config_path)
        if not config_file.remove_server(name):
            return ToolResult.error_result(f"MCP server '{name}' not found.")

        config_file.save(config_path)

        if self._toolkit and self._toolkit._mcp_manager:
            try:
                self._toolkit._mcp_manager.stop_server(name)
            except Exception:
                pass

        return ToolResult.success_result(data={
            "name": name,
            "message": f"MCP server '{name}' removed.",
        })

    def _list(self, **_: Any) -> ToolResult:
        from ..mcp.config import MCPConfigFile

        config_path = self._config_path()
        if not config_path.exists():
            return ToolResult.success_result(data={"servers": [], "config_path": str(config_path)})

        config_file = MCPConfigFile.load(config_path)
        servers = []
        for srv_name, server in config_file.servers.items():
            is_running = False
            tool_count = 0
            if self._toolkit and self._toolkit._mcp_manager:
                mgr = self._toolkit._mcp_manager
                is_running = srv_name in mgr._clients and mgr._clients[srv_name].is_running
                if is_running:
                    tool_count = sum(
                        1 for _, (srv, _) in mgr._tool_registry.items() if srv == srv_name
                    )

            servers.append({
                "name": srv_name,
                "command": server.command,
                "args": server.args,
                "enabled": server.enabled,
                "running": is_running,
                "tool_count": tool_count,
            })

        return ToolResult.success_result(data={
            "servers": servers,
            "config_path": str(config_path),
        })

    def _enable(self, *, name: str | None, **_: Any) -> ToolResult:
        if not name:
            return ToolResult.error_result("'name' is required for enable action.")

        from ..mcp.config import MCPConfigFile

        config_path = self._config_path()
        if not config_path.exists():
            return ToolResult.error_result(f"No MCP config at {config_path}")

        config_file = MCPConfigFile.load(config_path)
        server = config_file.get_server(name)
        if not server:
            return ToolResult.error_result(f"MCP server '{name}' not found.")

        server.enabled = True
        config_file.save(config_path)

        new_tools = self._try_hot_load(name)

        msg = f"MCP server '{name}' enabled."
        if new_tools:
            msg += f" {len(new_tools)} tools now available."

        return ToolResult.success_result(data={
            "name": name,
            "enabled": True,
            "hot_loaded_tools": new_tools,
            "message": msg,
        })

    def _disable(self, *, name: str | None, **_: Any) -> ToolResult:
        if not name:
            return ToolResult.error_result("'name' is required for disable action.")

        from ..mcp.config import MCPConfigFile

        config_path = self._config_path()
        if not config_path.exists():
            return ToolResult.error_result(f"No MCP config at {config_path}")

        config_file = MCPConfigFile.load(config_path)
        server = config_file.get_server(name)
        if not server:
            return ToolResult.error_result(f"MCP server '{name}' not found.")

        server.enabled = False
        config_file.save(config_path)

        if self._toolkit and self._toolkit._mcp_manager:
            try:
                self._toolkit._mcp_manager.stop_server(name)
            except Exception:
                pass

        return ToolResult.success_result(data={
            "name": name,
            "enabled": False,
            "message": f"MCP server '{name}' disabled.",
        })
