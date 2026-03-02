"""Explorer toolkit - read-only tools for fast codebase exploration."""

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from .base import BaseToolkit
from ..tools.coding import ReadFileTool, ListFilesTool
from ..tools.search import SemanticSearchTool, GrepTool, GlobTool
from ...utils.logger import log

if TYPE_CHECKING:
    from ..agents import AgentMCPServerConfig


class ExploreToolkit(BaseToolkit):
    """Read-only toolkit for fast codebase exploration.

    Provides tools for:
    - Reading files
    - Listing directory contents
    - Searching with patterns (grep, glob)
    - Semantic code search
    - MCP server tools (if configured)

    All tools are read-only - no file modifications allowed.
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
        """Initialize the explore toolkit.

        Args:
            repo_root: Root directory of the repository
            mcp_servers: Optional MCP server configurations for this agent
        """
        super().__init__(repo_root, mcp_servers=mcp_servers)

    def _register_tools(self) -> None:
        """Register read-only exploration tools."""
        # File reading
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

        log.debug(f"ExploreToolkit registered {len(self._tools)} tools")
