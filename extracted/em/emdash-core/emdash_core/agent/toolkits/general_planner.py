"""General Planner toolkit - sub-agent for project planning and organization.

The GeneralPlanner sub-agent specializes in:
- Project and task planning
- Brainstorming ideas
- Organizing information with notes

This is the coworker equivalent of the Plan agent for coding.
Does NOT deal with code - focuses on general project planning.
"""

from pathlib import Path
from typing import Optional, TYPE_CHECKING

from .base import BaseToolkit
from ..tools.base import BaseTool

if TYPE_CHECKING:
    from ..agents import AgentMCPServerConfig


class GeneralPlannerToolkit(BaseToolkit):
    """Toolkit for GeneralPlanner sub-agent - focused on project planning.

    Tools provided:
    - write_todo: Create task items
    - update_todo_list: Update task statuses
    - brainstorm: Generate ideas
    - save_note: Save planning notes
    - recall_notes: Recall saved notes
    - present_options: Present options for decisions

    This toolkit focuses on planning and organization, NOT code.
    """

    TOOLS = ["write_todo", "update_todo_list", "brainstorm", "save_note", "recall_notes", "present_options"]

    def __init__(
        self,
        repo_root: Path,
        mcp_servers: Optional[list["AgentMCPServerConfig"]] = None,
    ):
        """Initialize the general planner toolkit.

        Args:
            repo_root: Root directory (used by BaseToolkit)
            mcp_servers: Optional MCP server configurations
        """
        # Notes storage for this sub-agent session
        self._notes: list[dict] = []

        super().__init__(repo_root=repo_root, mcp_servers=mcp_servers)

    def get_tools(self) -> list[BaseTool]:
        """Return planning-focused tools."""
        from ..tools.tasks import WriteTodoTool, UpdateTodoListTool
        from ..coworker.toolkit import (
            SaveNoteTool,
            RecallNotesTool,
            BrainstormTool,
            PresentOptionsTool,
        )

        return [
            WriteTodoTool(),
            UpdateTodoListTool(),
            BrainstormTool(),
            SaveNoteTool(self._notes),
            RecallNotesTool(self._notes),
            PresentOptionsTool(),
        ]

    def get_notes(self) -> list[dict]:
        """Get notes saved during planning."""
        return self._notes.copy()
