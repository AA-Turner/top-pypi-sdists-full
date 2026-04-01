"""Integration tests: save_tools → MCP server → Claude Code.

These tests verify the full pipeline:
  1. save_tools() pickles tools
  2. write_mcp_config() writes MCP server + .mcp.json
  3. Claude Code discovers tools via .mcp.json and calls them

Requires:
  - ANTHROPIC_API_KEY env var
  - `claude` CLI installed
  - `mcp` package installed
"""

import os
import subprocess
import tempfile
from pathlib import Path

import pytest

from plato.tools import ToolDefinition, get_workspace, save_tools, set_workspace, write_mcp_config

DEFAULT_TOOLS_FILE = ".plato/tools.pkl"

# Skip all tests if no API key available
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not ANTHROPIC_API_KEY, reason="ANTHROPIC_API_KEY not set"),
]


def _run_claude(workspace: str, prompt: str, timeout: int = 60) -> str:
    """Run Claude Code in print mode with MCP config from workspace."""
    mcp_config_path = str(Path(workspace) / ".mcp.json")

    result = subprocess.run(
        [
            "claude",
            "-p",
            prompt,
            "--mcp-config",
            mcp_config_path,
            "--strict-mcp-config",
            "--dangerously-skip-permissions",
            "--model",
            "haiku",
            "--no-session-persistence",
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=workspace,
        env={
            **os.environ,
            "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
            "CLAUDECODE": "",  # Allow nested invocation
        },
    )

    if result.returncode != 0:
        raise RuntimeError(f"Claude exited with {result.returncode}:\nstdout: {result.stdout}\nstderr: {result.stderr}")

    return result.stdout


# ============================================================================
# Tests
# ============================================================================


def test_claude_discovers_and_calls_simple_tool():
    """Claude can discover an MCP tool and call it to get a result."""
    tools = [
        ToolDefinition(
            name="add_numbers",
            description="Add two numbers together and return the sum",
            input_schema={
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "First number"},
                    "b": {"type": "integer", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
            handler=lambda x: {"sum": x["a"] + x["b"]},
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        save_tools(tools, Path(tmpdir) / DEFAULT_TOOLS_FILE)
        write_mcp_config(Path(tmpdir))
        output = _run_claude(
            tmpdir,
            "Use the add_numbers tool to add 17 and 25. Just tell me the result number, nothing else.",
        )
        assert "42" in output


def test_claude_calls_tool_with_closure():
    """Claude can call a tool whose handler closes over data."""
    inventory = {
        "apple": {"price": 1.50, "stock": 100},
        "banana": {"price": 0.75, "stock": 200},
        "cherry": {"price": 3.00, "stock": 50},
    }

    def lookup_handler(input_data: dict) -> dict:
        item = input_data["item"].lower()
        if item in inventory:
            return {"found": True, "item": item, **inventory[item]}
        return {"found": False, "item": item}

    tools = [
        ToolDefinition(
            name="lookup_item",
            description="Look up an item in the inventory to get its price and stock count",
            input_schema={
                "type": "object",
                "properties": {
                    "item": {"type": "string", "description": "Item name to look up"},
                },
                "required": ["item"],
            },
            handler=lookup_handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        save_tools(tools, Path(tmpdir) / DEFAULT_TOOLS_FILE)
        write_mcp_config(Path(tmpdir))
        output = _run_claude(
            tmpdir,
            'Use the lookup_item tool with item="banana". Report the price.',
        )
        assert "0.75" in output


def test_claude_calls_multiple_tools():
    """Claude can discover and use multiple tools in one conversation."""
    tools = [
        ToolDefinition(
            name="multiply",
            description="Multiply two numbers",
            input_schema={
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
            },
            handler=lambda x: {"result": x["a"] * x["b"]},
        ),
        ToolDefinition(
            name="subtract",
            description="Subtract b from a (returns a - b)",
            input_schema={
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
            },
            handler=lambda x: {"result": x["a"] - x["b"]},
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        save_tools(tools, Path(tmpdir) / DEFAULT_TOOLS_FILE)
        write_mcp_config(Path(tmpdir))
        output = _run_claude(
            tmpdir,
            "First use multiply to compute 6 * 7, then use subtract to compute 100 - 58. Tell me both results.",
        )
        assert "42" in output


def test_claude_tool_with_workspace():
    """Claude can call a tool that uses get_workspace() to resolve paths."""

    def list_files_handler(input_data: dict) -> dict:
        ws = get_workspace()
        files = [f.name for f in ws.iterdir() if f.is_file()]
        return {"workspace": str(ws), "files": sorted(files)}

    tools = [
        ToolDefinition(
            name="list_workspace_files",
            description="List all files in the workspace directory",
            input_schema={"type": "object", "properties": {}},
            handler=list_files_handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test file in the workspace
        (Path(tmpdir) / "hello.txt").write_text("hello world")
        save_tools(tools, Path(tmpdir) / DEFAULT_TOOLS_FILE)
        write_mcp_config(Path(tmpdir))

        output = _run_claude(
            tmpdir,
            "Use list_workspace_files to see what files are in the workspace. Tell me the filenames you see.",
        )
        assert "hello.txt" in output

    set_workspace("/workspace")
