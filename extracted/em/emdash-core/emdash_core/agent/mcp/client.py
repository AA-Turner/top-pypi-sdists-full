"""Generic MCP client for communicating with MCP servers.

This module provides a generic client that can communicate with any
MCP-compliant server over stdio.
"""

import json
import subprocess
import threading
from dataclasses import dataclass, field
from typing import Any, Optional
from queue import Queue, Empty

from ...utils.logger import log


class MCPError(Exception):
    """Error from MCP server communication."""
    pass


@dataclass
class MCPToolInfo:
    """Information about a tool provided by an MCP server.

    Attributes:
        name: Tool name
        description: Tool description
        input_schema: JSON Schema for tool input
    """
    name: str
    description: str
    input_schema: dict = field(default_factory=dict)


@dataclass
class MCPResponse:
    """Response from an MCP tool call.

    Attributes:
        content: Response content (list of content items)
        is_error: Whether this is an error response
    """
    content: list[dict] = field(default_factory=list)
    is_error: bool = False

    def get_text(self) -> str:
        """Extract text content from response.

        Returns:
            Concatenated text content
        """
        texts = []
        for item in self.content:
            if item.get("type") == "text":
                texts.append(item.get("text", ""))
        return "\n".join(texts)


class GenericMCPClient:
    """Generic client for MCP servers.

    Communicates with MCP servers over stdio using JSON-RPC.

    Example:
        client = GenericMCPClient(
            name="github",
            command="github-mcp-server",
            args=["stdio"],
            env={"GITHUB_TOKEN": "..."},
        )
        client.start()

        tools = client.list_tools()
        result = client.call_tool("search_code", {"query": "auth"})

        client.stop()
    """

    def __init__(
        self,
        name: str,
        command: str,
        args: list[str] = None,
        env: dict[str, str] = None,
        timeout: int = 30,
    ):
        """Initialize the MCP client.

        Args:
            name: Name for this client (for logging)
            command: Command to run the server
            args: Command arguments
            env: Environment variables
            timeout: Timeout for operations in seconds
        """
        self.name = name
        self.command = command
        self.args = args or []
        self.env = env or {}
        self.timeout = timeout

        self._process: Optional[subprocess.Popen] = None
        self._request_id = 0
        self._pending: dict[int, Queue] = {}
        self._reader_thread: Optional[threading.Thread] = None
        self._running = False
        self._tools: list[MCPToolInfo] = []

    @property
    def is_running(self) -> bool:
        """Check if the client is running."""
        return self._running and self._process is not None

    def start(self) -> None:
        """Start the MCP server process."""
        if self._running:
            return

        import os

        # Build environment
        full_env = os.environ.copy()
        full_env.update(self.env)

        try:
            self._process = subprocess.Popen(
                [self.command] + self.args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=full_env,
                text=True,
                bufsize=1,
            )
        except FileNotFoundError:
            raise MCPError(f"MCP server command not found: {self.command}")
        except Exception as e:
            raise MCPError(f"Failed to start MCP server: {e}")

        self._running = True

        # Start reader thread
        self._reader_thread = threading.Thread(target=self._read_responses, daemon=True)
        self._reader_thread.start()

        # Initialize the connection
        self._initialize()

        log.info(f"Started MCP server: {self.name}")

    def stop(self) -> None:
        """Stop the MCP server process."""
        self._running = False

        if self._process:
            try:
                self._process.terminate()
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
            except Exception:
                pass
            finally:
                self._process = None

        self._tools = []
        log.info(f"Stopped MCP server: {self.name}")

    def _initialize(self) -> None:
        """Initialize the MCP connection."""
        # Send initialize request
        response = self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "emdash",
                "version": "1.0.0",
            },
        })

        # Send initialized notification
        self._send_notification("notifications/initialized", {})

    def _send_request(self, method: str, params: dict) -> dict:
        """Send a JSON-RPC request and wait for response.

        Args:
            method: RPC method name
            params: Method parameters

        Returns:
            Response result

        Raises:
            MCPError: On communication error or error response
        """
        if not self._process or not self._running:
            raise MCPError("MCP client not running")

        self._request_id += 1
        request_id = self._request_id

        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }

        # Create response queue
        response_queue: Queue = Queue()
        self._pending[request_id] = response_queue

        try:
            # Send request
            request_line = json.dumps(request) + "\n"
            self._process.stdin.write(request_line)
            self._process.stdin.flush()

            # Wait for response
            try:
                response = response_queue.get(timeout=self.timeout)
            except Empty:
                raise MCPError(f"Timeout waiting for response to {method}")

            if "error" in response:
                error = response["error"]
                raise MCPError(f"MCP error: {error.get('message', 'Unknown error')}")

            return response.get("result", {})

        finally:
            del self._pending[request_id]

    def _send_notification(self, method: str, params: dict) -> None:
        """Send a JSON-RPC notification (no response expected).

        Args:
            method: Notification method
            params: Method parameters
        """
        if not self._process or not self._running:
            return

        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
        }

        notification_line = json.dumps(notification) + "\n"
        self._process.stdin.write(notification_line)
        self._process.stdin.flush()

    def _read_responses(self) -> None:
        """Background thread to read responses from the server."""
        while self._running and self._process:
            try:
                line = self._process.stdout.readline()
                if not line:
                    break

                try:
                    response = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                # Route to pending request
                request_id = response.get("id")
                if request_id and request_id in self._pending:
                    self._pending[request_id].put(response)

            except Exception as e:
                if self._running:
                    log.warning(f"Error reading MCP response: {e}")
                break

    def list_tools(self) -> list[MCPToolInfo]:
        """List available tools from the server.

        Returns:
            List of MCPToolInfo
        """
        if self._tools:
            return self._tools

        result = self._send_request("tools/list", {})

        tools = []
        for tool_data in result.get("tools", []):
            tools.append(MCPToolInfo(
                name=tool_data.get("name", ""),
                description=tool_data.get("description", ""),
                input_schema=tool_data.get("inputSchema", {}),
            ))

        self._tools = tools
        return tools

    def call_tool(self, name: str, arguments: dict) -> MCPResponse:
        """Call a tool on the server.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            MCPResponse with tool result
        """
        result = self._send_request("tools/call", {
            "name": name,
            "arguments": arguments,
        })

        return MCPResponse(
            content=result.get("content", []),
            is_error=result.get("isError", False),
        )


# Legacy client for backward compatibility
class GitHubMCPClient(GenericMCPClient):
    """GitHub-specific MCP client.

    Deprecated: Use GenericMCPClient directly with appropriate config.
    """

    def __init__(self, token: Optional[str] = None, timeout: int = 30):
        """Initialize GitHub MCP client.

        Args:
            token: GitHub token. If None, reads from environment.
            timeout: Operation timeout in seconds.
        """
        import os

        github_token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

        super().__init__(
            name="github",
            command="github-mcp-server",
            args=["stdio"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": github_token or ""},
            timeout=timeout,
        )
