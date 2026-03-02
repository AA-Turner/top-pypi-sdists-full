"""Tool definitions and serialization for world-to-agent tool passing.

Worlds build ToolDefinitions and save them to the workspace via save_tools().
save_tools() pickles the tools AND writes an MCP server + .mcp.json so that
MCP-capable agents (Claude Code) automatically discover them.

Handlers should use get_workspace() for paths instead of closing over
absolute paths, since the workspace path differs between world and agent.

Usage (world side):
    from plato.tools import ToolDefinition, get_workspace, save_tools

    def my_handler(input_data: dict) -> str:
        ws = get_workspace()
        return (ws / "file.txt").read_text()

    tools = [ToolDefinition(name="read", description="...", input_schema={...}, handler=my_handler)]
    save_tools(tools, project_dir)
    # Then launch agent with workspace=project_dir

Usage (agent side):
    from plato.tools import load_tools

    tools = load_tools("/workspace")
    # tools have callable handlers, get_workspace() returns Path("/workspace")
"""

from plato.tools.definition import ToolDefinition, get_workspace, set_workspace
from plato.tools.mcp import write_mcp_config
from plato.tools.serialization import load_tools, save_tools
from plato.tools.server import ToolServer

__all__ = [
    "ToolDefinition",
    "ToolServer",
    "get_workspace",
    "load_tools",
    "save_tools",
    "set_workspace",
    "write_mcp_config",
]
