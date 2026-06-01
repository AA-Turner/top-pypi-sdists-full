"""MCP server support for codrninja."""

from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


CONFIG_DIR = Path.home() / ".codrninja"
CONFIG_FILE = CONFIG_DIR / "mcp.json"
CACHE_TTL_SECONDS = 60
FAILURE_THRESHOLD = 3


@dataclass
class MCPServer:
    """Configuration for a single MCP server."""

    name: str
    type: str
    command: Optional[List[str]] = None
    url: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    enabled: bool = True
    tools: List[Dict[str, Any]] = field(default_factory=list)
    failure_count: int = 0


class MCPManager:
    """Manage MCP server configuration, discovery, and tool calls."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = Path(config_path or CONFIG_FILE).expanduser()
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.servers: Dict[str, MCPServer] = {}
        self._tool_cache: Dict[str, Dict[str, Any]] = {}
        self._load_config()

    def _load_config(self):
        if not self.config_path.exists():
            self._save_config()
            return

        with open(self.config_path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)

        self.servers = {}
        for entry in raw.get("servers", []):
            server = MCPServer(
                name=entry["name"],
                type=entry["type"],
                command=entry.get("command"),
                url=entry.get("url"),
                headers=entry.get("headers", {}),
                enabled=entry.get("enabled", True),
                tools=entry.get("tools", []),
                failure_count=entry.get("failure_count", 0),
            )
            self.servers[server.name] = server

    def _save_config(self):
        payload = {
            "servers": [self._server_to_dict(server) for server in self.servers.values()]
        }
        with open(self.config_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def _server_to_dict(self, server: MCPServer) -> Dict[str, Any]:
        data = asdict(server)
        if not data.get("command"):
            data.pop("command", None)
        if not data.get("url"):
            data.pop("url", None)
        return data

    def _resolve_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        resolved = {}
        for key, value in headers.items():
            resolved[key] = os.path.expandvars(value)
        return resolved

    def list_servers(self) -> List[MCPServer]:
        return list(self.servers.values())

    def add_server(self, config: Dict[str, Any]) -> MCPServer:
        server = MCPServer(
            name=config["name"],
            type=config["type"],
            command=config.get("command"),
            url=config.get("url"),
            headers=config.get("headers", {}),
            enabled=config.get("enabled", True),
            tools=config.get("tools", []),
        )
        self.servers[server.name] = server
        self._tool_cache.pop(server.name, None)
        self._save_config()
        return server

    def remove_server(self, name: str) -> bool:
        removed = self.servers.pop(name, None)
        self._tool_cache.pop(name, None)
        if removed:
            self._save_config()
            return True
        return False

    def enable(self, name: str) -> bool:
        server = self.servers.get(name)
        if not server:
            return False
        server.enabled = True
        server.failure_count = 0
        self._save_config()
        return True

    def disable(self, name: str) -> bool:
        server = self.servers.get(name)
        if not server:
            return False
        server.enabled = False
        self._save_config()
        return True

    def discover_tools(self, force: bool = False) -> Dict[str, List[Dict[str, Any]]]:
        discovered: Dict[str, List[Dict[str, Any]]] = {}
        for server in self.servers.values():
            if not server.enabled:
                continue

            cached = self._tool_cache.get(server.name)
            if cached and not force and (time.time() - cached["timestamp"] < CACHE_TTL_SECONDS):
                server.tools = cached["tools"]
                discovered[server.name] = server.tools
                continue

            try:
                tools = self._request_tools(server)
                server.tools = tools
                server.failure_count = 0
                self._tool_cache[server.name] = {"timestamp": time.time(), "tools": tools}
                discovered[server.name] = tools
            except Exception:
                server.failure_count += 1
                if server.failure_count >= FAILURE_THRESHOLD:
                    server.enabled = False
                discovered[server.name] = server.tools

        self._save_config()
        return discovered

    def call_tool(self, server_name: str, tool_name: str, params: Dict[str, Any]) -> Any:
        server = self.servers.get(server_name)
        if not server:
            raise ValueError(f"Unknown MCP server: {server_name}")
        if not server.enabled:
            raise ValueError(f"MCP server '{server_name}' is disabled")

        try:
            result = self._request_tool_call(server, tool_name, params)
            server.failure_count = 0
            self._save_config()
            return result
        except Exception:
            server.failure_count += 1
            if server.failure_count >= FAILURE_THRESHOLD:
                server.enabled = False
            self._save_config()
            raise

    def _request_tools(self, server: MCPServer) -> List[Dict[str, Any]]:
        payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
        response = self._send_request(server, payload)
        return response.get("result", {}).get("tools", [])

    def _request_tool_call(self, server: MCPServer, tool_name: str, params: Dict[str, Any]) -> Any:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": params,
            },
        }
        response = self._send_request(server, payload)
        return response.get("result", response)

    def _send_request(self, server: MCPServer, payload: Dict[str, Any]) -> Dict[str, Any]:
        if server.type == "http":
            return self._send_http_request(server, payload)
        if server.type == "stdio":
            return self._send_stdio_request(server, payload)
        raise ValueError(f"Unsupported MCP server type: {server.type}")

    def _send_http_request(self, server: MCPServer, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not server.url:
            raise ValueError(f"MCP server '{server.name}' is missing a URL")

        response = requests.post(
            server.url,
            json=payload,
            headers=self._resolve_headers(server.headers),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            raise RuntimeError(data["error"])
        return data

    def _send_stdio_request(self, server: MCPServer, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not server.command:
            raise ValueError(f"MCP server '{server.name}' is missing a command")

        process = subprocess.Popen(
            server.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate(json.dumps(payload) + "\n", timeout=30)
        if process.returncode != 0:
            raise RuntimeError(stderr.strip() or f"MCP stdio server exited with code {process.returncode}")

        response_text = stdout.strip().splitlines()[-1] if stdout.strip() else "{}"
        data = json.loads(response_text)
        if "error" in data:
            raise RuntimeError(data["error"])
        return data

    def tool_count(self) -> int:
        return sum(len(server.tools) for server in self.servers.values() if server.enabled)
