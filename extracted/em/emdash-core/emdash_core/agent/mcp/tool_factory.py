"""Tool factory for creating BaseTool instances from MCP servers.

This module provides functions to dynamically create agent tools
from MCP server tool definitions.
"""

import json
from typing import Any, Optional

from ..tools.base import BaseTool, ToolResult, ToolCategory
from .manager import MCPServerManager
from .client import MCPToolInfo, MCPError
from ...utils.logger import log


class MCPDynamicTool(BaseTool):
    """A tool dynamically created from an MCP server tool definition.

    This allows MCP tools to be used seamlessly alongside native tools
    in the agent toolkit.
    """

    def __init__(
        self,
        mcp_manager: MCPServerManager,
        tool_name: str,
        tool_info: MCPToolInfo,
        server_name: str,
        connection: Any = None,
    ):
        """Initialize the dynamic tool.

        Args:
            mcp_manager: MCP server manager for calling tools
            tool_name: Tool name (may be prefixed)
            tool_info: Tool info from MCP server
            server_name: Name of the source server
            connection: Optional Kuzu connection (for compatibility)
        """
        super().__init__(connection)
        self._mcp_manager = mcp_manager
        self._tool_name = tool_name
        self._tool_info = tool_info
        self._server_name = server_name

        # Set BaseTool attributes
        self.name = tool_name
        self.description = tool_info.description or f"MCP tool: {tool_name}"
        self.category = self._infer_category(tool_name, tool_info)

    def _infer_category(self, name: str, info: MCPToolInfo) -> ToolCategory:
        """Infer tool category from name and description.

        Args:
            name: Tool name
            info: Tool info

        Returns:
            Inferred ToolCategory
        """
        name_lower = name.lower()
        desc_lower = (info.description or "").lower()

        # Search-related
        if any(kw in name_lower for kw in ["search", "find", "query", "grep"]):
            return ToolCategory.SEARCH

        # Traversal-related
        if any(kw in name_lower for kw in ["expand", "caller", "callee", "dependency", "neighbor"]):
            return ToolCategory.TRAVERSAL

        # Analytics-related
        if any(kw in name_lower for kw in ["pagerank", "community", "importance", "metric"]):
            return ToolCategory.ANALYTICS

        # History-related (PRs, commits)
        if any(kw in name_lower for kw in ["pr", "commit", "history", "github"]):
            return ToolCategory.HISTORY

        # Default to search
        return ToolCategory.SEARCH

    def execute(self, **kwargs) -> ToolResult:
        """Execute the MCP tool.

        Args:
            **kwargs: Tool arguments

        Returns:
            ToolResult with tool output
        """
        try:
            response = self._mcp_manager.call_tool(self._tool_name, kwargs)

            if response.is_error:
                return ToolResult.error_result(
                    f"MCP tool error: {response.get_text()}",
                )

            # Parse response content
            result_data = self._parse_response(response)

            return ToolResult.success_result(
                data=result_data,
                metadata={
                    "server": self._server_name,
                    "tool": self._tool_name,
                },
            )

        except MCPError as e:
            return ToolResult.error_result(
                f"MCP error: {str(e)}",
                suggestions=["Check if the MCP server is running"],
            )
        except Exception as e:
            log.exception(f"MCP tool execution error: {self._tool_name}")
            return ToolResult.error_result(
                f"Tool execution failed: {str(e)}",
            )

    def _parse_response(self, response) -> dict:
        """Parse MCP response into result data.

        Args:
            response: MCPResponse

        Returns:
            Parsed result dict
        """
        result = {"content": [], "text": ""}

        for item in response.content:
            if item.get("type") == "text":
                text = item.get("text", "")
                result["text"] += text + "\n"

                # Try to parse as JSON
                try:
                    parsed = json.loads(text)
                    if isinstance(parsed, dict):
                        result.update(parsed)
                    elif isinstance(parsed, list):
                        result["results"] = parsed
                except json.JSONDecodeError:
                    pass

            result["content"].append(item)

        result["text"] = result["text"].strip()
        return result

    def get_schema(self) -> dict:
        """Get OpenAI function calling schema.

        Returns:
            OpenAI function schema dict
        """
        input_schema = self._tool_info.input_schema or {}

        # Convert MCP schema to OpenAI format
        parameters = {
            "type": "object",
            "properties": input_schema.get("properties", {}),
            "required": input_schema.get("required", []),
        }

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": parameters,
            },
        }


def create_tools_from_mcp(
    manager: MCPServerManager,
    connection: Any = None,
) -> list[BaseTool]:
    """Create BaseTool instances from all MCP server tools.

    This function queries all enabled MCP servers and creates
    dynamic tool wrappers for each tool they provide.

    Args:
        manager: MCP server manager
        connection: Optional Kuzu connection

    Returns:
        List of MCPDynamicTool instances
    """
    tools = []

    try:
        all_tools = manager.get_all_tools()

        for tool_name, server_name, tool_info in all_tools:
            tool = MCPDynamicTool(
                mcp_manager=manager,
                tool_name=tool_name,
                tool_info=tool_info,
                server_name=server_name,
                connection=connection,
            )
            tools.append(tool)
            log.debug(f"Created MCP tool: {tool_name} from {server_name}")

    except Exception as e:
        log.warning(f"Failed to create tools from MCP: {e}")

    return tools
