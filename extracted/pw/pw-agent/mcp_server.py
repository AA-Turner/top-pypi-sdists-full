"""MCP server mode — expose pw-agent's tools (and the fleet LLM) via JSON-RPC.

Flips pw-agent around: instead of being a REPL that *consumes* MCP servers,
this mode makes pw-agent *be* an MCP server. Cursor, Claude Desktop, and
other MCP clients can then connect over stdio and call the user's GPU
fleet through it.

Run as:
    pw-agent serve-mcp
or:
    pw-agent --mcp-server

Speaks JSON-RPC 2.0 over stdin/stdout, line-delimited JSON. Implements:
  - initialize / notifications/initialized
  - tools/list — exposes pw-agent's native tools
  - tools/call — routes calls to local handlers
  - shutdown / exit

Exposed tools:
  - All native pw-agent tools (read_file, bash, web_search, etc.)
  - chat_with_fleet(prompt) — chats with the user's Ollama LLM via the
    cloud broker (the killer feature: gives Cursor access to the fleet)
  - search_codebase(query) — if a codebase index exists for cwd

Add to Claude Desktop's MCP config:

  "pw-agent": {
    "command": "pw-agent",
    "args": ["serve-mcp"]
  }

Or for Cursor's MCP settings, same thing.
"""

import json
import os
import sys
from typing import Any


PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "pw-agent"


def _convert_tool_def(tool: dict) -> dict:
    """Convert pw-agent's TOOL_DEFINITIONS format to MCP's tool schema."""
    # MCP expects: {name, description, inputSchema: {type, properties, required}}
    properties = {}
    for param_name, param_spec in tool.get("parameters", {}).items():
        properties[param_name] = {
            "type": param_spec.get("type", "string"),
            "description": param_spec.get("description", ""),
        }
    return {
        "name": tool["name"],
        "description": tool["description"],
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": tool.get("required", []),
        },
    }


def _build_tool_list() -> list[dict]:
    """Return the MCP-formatted tool list — pw-agent natives + fleet chat."""
    from tools import TOOL_DEFINITIONS

    # Hide tools that don't make sense in MCP mode
    HIDDEN = {
        "spawn_agent", "spawn_agents",  # No subagent context here
        "speak_text",                    # Local audio playback won't work over MCP
        "search_codebase",               # Handled separately if index exists
    }

    tools = []
    for t in TOOL_DEFINITIONS:
        if t["name"] in HIDDEN:
            continue
        tools.append(_convert_tool_def(t))

    # Add the fleet chat tool — this is the killer feature
    tools.append({
        "name": "chat_with_fleet",
        "description": (
            "Send a prompt to the user's PastaWater GPU fleet LLM and get the response. "
            "Use this to leverage the user's locally-hosted Ollama models from another "
            "MCP client. Note: this is a single-turn chat — no conversation history."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The prompt to send to the fleet LLM."},
                "system": {"type": "string", "description": "Optional system prompt."},
                "temperature": {"type": "number", "description": "Sampling temperature 0-2. Default 0.3."},
            },
            "required": ["prompt"],
        },
    })

    return tools


def _handle_tool_call(name: str, arguments: dict, client=None) -> dict:
    """Execute a tool call and return MCP-shaped result."""
    from tools import execute_tool, TOOL_MAP

    # Special: chat_with_fleet uses the LLM client
    if name == "chat_with_fleet":
        if not client:
            return {
                "content": [{"type": "text", "text": "Error: no LLM client configured (pw-agent has no saved instance)"}],
                "isError": True,
            }
        prompt = arguments.get("prompt", "")
        system = arguments.get("system", "")
        temperature = float(arguments.get("temperature", 0.3))
        if not prompt:
            return {"content": [{"type": "text", "text": "Error: prompt is required"}], "isError": True}

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            response = client.chat(messages, temperature=temperature)
            return {
                "content": [{"type": "text", "text": response or "(empty response)"}],
                "isError": False,
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error calling fleet: {e}"}],
                "isError": True,
            }

    # Native pw-agent tools
    if name in TOOL_MAP:
        try:
            result = execute_tool(name, arguments)
            is_error = isinstance(result, str) and result.startswith("Error")
            return {
                "content": [{"type": "text", "text": result}],
                "isError": is_error,
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error: {e}"}],
                "isError": True,
            }

    return {
        "content": [{"type": "text", "text": f"Error: unknown tool '{name}'"}],
        "isError": True,
    }


def _send(msg: dict):
    """Write a JSON message to stdout, line-delimited."""
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def _make_response(req_id: Any, result: Any = None, error: dict = None) -> dict:
    """Build a JSON-RPC 2.0 response."""
    msg = {"jsonrpc": "2.0", "id": req_id}
    if error:
        msg["error"] = error
    else:
        msg["result"] = result
    return msg


def run_mcp_server(client=None):
    """Main JSON-RPC loop. Reads from stdin, writes to stdout.

    client: an LLMClient instance for the chat_with_fleet tool. If None,
    chat_with_fleet returns an error but other tools still work.
    """
    # Suppress all stderr from imports — MCP clients are sensitive
    # (any output to stdout that isn't valid JSON-RPC breaks them)

    initialized = False

    while True:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            return
        if not line:
            return  # EOF

        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = req.get("method", "")
        params = req.get("params", {}) or {}
        req_id = req.get("id")

        # ─── Lifecycle methods ─────────────────────────────────────────
        if method == "initialize":
            _send(_make_response(req_id, result={
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {
                    "tools": {"listChanged": False},
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": "1.24.0",
                },
            }))
            continue

        if method == "notifications/initialized":
            # No response for notifications
            initialized = True
            continue

        if method in ("shutdown", "exit"):
            if req_id is not None:
                _send(_make_response(req_id, result=None))
            return

        # ─── Tools ─────────────────────────────────────────────────────
        if method == "tools/list":
            _send(_make_response(req_id, result={"tools": _build_tool_list()}))
            continue

        if method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {}) or {}
            result = _handle_tool_call(tool_name, arguments, client=client)
            _send(_make_response(req_id, result=result))
            continue

        # ─── Unknown method ────────────────────────────────────────────
        if req_id is not None:
            _send(_make_response(req_id, error={
                "code": -32601,
                "message": f"Method not found: {method}",
            }))
