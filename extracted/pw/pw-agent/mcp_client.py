"""MCP (Model Context Protocol) client for pw-agent.

Connects to MCP servers over stdio and exposes their tools to the LLM
as if they were native pw-agent tools. Tool names are namespaced as
`mcp_<server>_<tool>` to avoid collisions.

Protocol: JSON-RPC 2.0 over stdin/stdout (one JSON message per line).
Spec: https://modelcontextprotocol.io

Config file: ~/.pw-agent/mcp.json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "env": {}
    }
  }
}

Usage from the agent:
    manager = MCPManager()
    manager.start_all()
    for tool in manager.list_tools():
        # tool is a dict with name, description, inputSchema
        ...
    result = manager.call_tool("mcp_filesystem_read_file", {"path": "/tmp/x"})
"""

import json
import os
import subprocess
import threading
import time
import uuid
from typing import Optional


DEFAULT_MCP_CONFIG = os.path.expanduser("~/.pw-agent/mcp.json")
PROTOCOL_VERSION = "2024-11-05"
CLIENT_NAME = "pw-agent"


class MCPClient:
    """Single MCP server connection over stdio."""

    def __init__(self, name: str, command: str, args: list[str] = None, env: dict = None):
        self.name = name
        self.command = command
        self.args = args or []
        self.env = env or {}
        self.proc: Optional[subprocess.Popen] = None
        self.tools: list[dict] = []
        self._next_id = 1
        self._lock = threading.Lock()
        self._reader_thread: Optional[threading.Thread] = None
        self._pending: dict[int, dict] = {}  # id → response
        self._pending_event = threading.Event()
        self._initialized = False
        self._stderr_buffer: list[str] = []

    def start(self, timeout: float = 30.0) -> tuple[bool, str]:
        """Spawn the server, perform handshake, fetch tools.

        Returns (success, message).
        """
        full_env = {**os.environ, **self.env}
        try:
            self.proc = subprocess.Popen(
                [self.command, *self.args],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=full_env,
                bufsize=1,  # line buffered (correct for text mode)
                text=True,
                encoding="utf-8",
            )
        except FileNotFoundError:
            return False, f"command not found: {self.command}"
        except Exception as e:
            return False, f"failed to spawn: {e}"

        # Start the reader thread
        self._reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._reader_thread.start()

        # Drain stderr in background so the buffer doesn't fill up
        threading.Thread(target=self._stderr_loop, daemon=True).start()

        # Initialize handshake
        try:
            init_resp = self._request("initialize", {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": CLIENT_NAME, "version": "1.21.0"},
            }, timeout=timeout)
            if "error" in init_resp:
                err = init_resp["error"].get("message", "unknown")
                return False, f"initialize failed: {err}"

            # Send initialized notification (no id, no response expected)
            self._notify("notifications/initialized", {})
            self._initialized = True

            # Fetch tools list
            tools_resp = self._request("tools/list", {}, timeout=timeout)
            if "error" in tools_resp:
                # Server might not support tools — that's OK
                self.tools = []
            else:
                self.tools = tools_resp.get("result", {}).get("tools", [])

            return True, f"connected ({len(self.tools)} tools)"
        except TimeoutError as e:
            return False, str(e)
        except Exception as e:
            return False, f"handshake error: {e}"

    def stop(self):
        """Terminate the server process."""
        if self.proc:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            except Exception:
                pass
            self.proc = None

    def _next_request_id(self) -> int:
        with self._lock:
            i = self._next_id
            self._next_id += 1
            return i

    def _send(self, payload: dict):
        if not self.proc or not self.proc.stdin:
            raise RuntimeError("not connected")
        line = json.dumps(payload) + "\n"
        try:
            self.proc.stdin.write(line)
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError) as e:
            raise RuntimeError(f"send failed: {e}")

    def _notify(self, method: str, params: dict):
        """Send a notification (no response expected, no id)."""
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def _request(self, method: str, params: dict, timeout: float = 30.0) -> dict:
        """Send a request and wait for the matching response."""
        req_id = self._next_request_id()
        self._send({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params})

        # Wait for response
        deadline = time.time() + timeout
        while time.time() < deadline:
            with self._lock:
                if req_id in self._pending:
                    return self._pending.pop(req_id)
            time.sleep(0.05)

        raise TimeoutError(f"MCP request '{method}' timed out after {timeout}s")

    def _reader_loop(self):
        """Background thread that reads stdout lines and dispatches responses.

        Uses readline() instead of `for line in f` because the latter uses
        Python's buffered iterator which can hang waiting for buffer fill.
        """
        if not self.proc or not self.proc.stdout:
            return
        while True:
            try:
                line = self.proc.stdout.readline()
            except Exception:
                return
            if not line:
                # EOF — process exited
                return
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_id = msg.get("id")
            if msg_id is not None:
                # It's a response — match by id
                with self._lock:
                    self._pending[msg_id] = msg
            # Notifications (no id) are ignored for now

    def _stderr_loop(self):
        """Background drain for stderr to avoid buffer fill."""
        if not self.proc or not self.proc.stderr:
            return
        while True:
            try:
                line = self.proc.stderr.readline()
            except Exception:
                return
            if not line:
                return
            line = line.rstrip()
            if line:
                self._stderr_buffer.append(line)
                if len(self._stderr_buffer) > 200:
                    self._stderr_buffer.pop(0)

    def call_tool(self, tool_name: str, arguments: dict, timeout: float = 60.0) -> str:
        """Call an MCP tool and return the textual result.

        MCP tool results have a 'content' array with type:'text' items.
        """
        if not self._initialized:
            return f"Error: MCP server '{self.name}' not initialized"

        try:
            resp = self._request("tools/call", {
                "name": tool_name,
                "arguments": arguments,
            }, timeout=timeout)
        except TimeoutError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error: MCP call failed — {e}"

        if "error" in resp:
            err = resp["error"]
            return f"Error: MCP {self.name}.{tool_name} — {err.get('message', 'unknown')} (code {err.get('code', '?')})"

        result = resp.get("result", {})
        if result.get("isError"):
            return f"Error: tool reported failure"

        # Extract text content
        content = result.get("content", [])
        text_parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
            elif isinstance(item, dict) and item.get("type") == "image":
                text_parts.append(f"[image: {item.get('mimeType', 'unknown')}]")
        return "\n".join(text_parts) or "(empty response)"


class MCPManager:
    """Manages all configured MCP servers."""

    def __init__(self, config_path: str = DEFAULT_MCP_CONFIG):
        self.config_path = config_path
        self.clients: dict[str, MCPClient] = {}

    def load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            return {"servers": {}}
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except Exception:
            return {"servers": {}}

    def save_config(self, config: dict):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)

    def start_all(self) -> dict[str, tuple[bool, str]]:
        """Start every server in the config. Returns {name: (ok, msg)}."""
        config = self.load_config()
        results = {}
        for name, server_cfg in config.get("servers", {}).items():
            client = MCPClient(
                name=name,
                command=server_cfg.get("command", ""),
                args=server_cfg.get("args", []),
                env=server_cfg.get("env", {}),
            )
            ok, msg = client.start()
            results[name] = (ok, msg)
            if ok:
                self.clients[name] = client
        return results

    def stop_all(self):
        for client in self.clients.values():
            client.stop()
        self.clients.clear()

    def list_tools(self) -> list[dict]:
        """List all tools from all servers, with namespaced names."""
        result = []
        for server_name, client in self.clients.items():
            for tool in client.tools:
                tool_name = tool.get("name", "")
                if not tool_name:
                    continue
                namespaced = f"mcp_{server_name}_{tool_name}"
                result.append({
                    "name": namespaced,
                    "description": f"[MCP/{server_name}] {tool.get('description', '')}",
                    "inputSchema": tool.get("inputSchema", {}),
                    "_server": server_name,
                    "_original_name": tool_name,
                })
        return result

    def call_tool(self, namespaced_name: str, arguments: dict) -> str:
        """Route a tool call to the right server."""
        if not namespaced_name.startswith("mcp_"):
            return f"Error: not an MCP tool: {namespaced_name}"

        # Parse: mcp_<server>_<tool> — server name might contain underscores
        # so we match against known clients
        rest = namespaced_name[4:]
        for server_name in self.clients:
            prefix = f"{server_name}_"
            if rest.startswith(prefix):
                tool_name = rest[len(prefix):]
                return self.clients[server_name].call_tool(tool_name, arguments)

        return f"Error: no MCP server matches {namespaced_name}"

    def add_server(self, name: str, command: str, args: list[str] = None, env: dict = None):
        """Persist a new server to the config."""
        config = self.load_config()
        if "servers" not in config:
            config["servers"] = {}
        config["servers"][name] = {
            "command": command,
            "args": args or [],
            "env": env or {},
        }
        self.save_config(config)

    def remove_server(self, name: str) -> bool:
        """Remove a server from the config."""
        config = self.load_config()
        if name in config.get("servers", {}):
            del config["servers"][name]
            self.save_config(config)
            return True
        return False
