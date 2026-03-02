"""Plan toolkit - read-only exploration tools for planning.

The Plan subagent explores the codebase and returns a plan as text.
The main agent (in plan mode) writes the plan to .emdash/<feature>.md.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from .base import BaseToolkit
from ..tools.coding import ReadFileTool, ListFilesTool
from ..tools.search import SemanticSearchTool, GrepTool, GlobTool
from ...utils.logger import log

if TYPE_CHECKING:
    from ..agents import AgentMCPServerConfig


class PlanToolkit(BaseToolkit):
    """Read-only toolkit for Plan subagent.

    The Plan subagent explores the codebase and returns a structured plan.
    It does NOT write files - the main agent handles that.

    Tools available:
    - read_file: Read file contents
    - list_files: List directory contents
    - glob: Find files by pattern
    - grep: Search file contents
    - semantic_search: AI-powered code search
    - MCP server tools (if configured)
    """

    TOOLS = [
        "read_file",
        "list_files",
        "glob",
        "grep",
        "semantic_search",
    ]

    def __init__(
        self,
        repo_root: Path,
        mcp_servers: Optional[list["AgentMCPServerConfig"]] = None,
    ):
        """Initialize the plan toolkit.

        Args:
            repo_root: Root directory of the repository
            mcp_servers: Optional MCP server configurations for this agent
        """
        super().__init__(repo_root, mcp_servers=mcp_servers)

    def _register_tools(self) -> None:
        """Register read-only exploration tools."""
        # All read-only exploration tools
        self.register_tool(ReadFileTool(repo_root=self.repo_root))
        self.register_tool(ListFilesTool(repo_root=self.repo_root))

        # Pattern-based search
        self.register_tool(GlobTool(connection=None))
        self.register_tool(GrepTool(connection=None))

        # Semantic search (if available)
        try:
            self.register_tool(SemanticSearchTool(connection=None))
        except Exception as e:
            log.debug(f"Semantic search not available: {e}")

        log.debug(f"PlanToolkit registered {len(self._tools)} tools")
