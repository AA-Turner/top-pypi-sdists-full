"""Researcher toolkit - sub-agent for web research and information gathering.

The Researcher sub-agent specializes in:
- Web search and URL fetching
- Information summarization
- Note-taking for findings

This is the coworker equivalent of the Explore agent for coding.
"""

from pathlib import Path
from typing import Optional, TYPE_CHECKING

from .base import BaseToolkit
from ..tools.base import BaseTool

if TYPE_CHECKING:
    from ..agents import AgentMCPServerConfig


class ResearcherToolkit(BaseToolkit):
    """Toolkit for Researcher sub-agent - focused on web research.

    Tools provided:
    - web: Search the web and fetch URLs
    - save_note: Save findings to session memory
    - recall_notes: Recall saved notes
    - summarize: Summarize text content

    This is a read-only toolkit focused on gathering and organizing information.
    """

    TOOLS = ["web", "save_note", "recall_notes", "summarize"]

    def __init__(
        self,
        repo_root: Path,
        mcp_servers: Optional[list["AgentMCPServerConfig"]] = None,
    ):
        """Initialize the researcher toolkit.

        Args:
            repo_root: Root directory (used by BaseToolkit)
            mcp_servers: Optional MCP server configurations
        """
        # Notes storage for this sub-agent session
        self._notes: list[dict] = []

        super().__init__(repo_root=repo_root, mcp_servers=mcp_servers)

    def get_tools(self) -> list[BaseTool]:
        """Return research-focused tools."""
        from ..tools.web import WebTool
        from ..coworker.toolkit import SaveNoteTool, RecallNotesTool, SummarizeTool

        return [
            WebTool(connection=None),
            SaveNoteTool(self._notes),
            RecallNotesTool(self._notes),
            SummarizeTool(),
        ]

    def get_notes(self) -> list[dict]:
        """Get notes saved during research."""
        return self._notes.copy()
