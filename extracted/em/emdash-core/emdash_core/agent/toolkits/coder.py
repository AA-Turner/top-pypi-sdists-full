"""Coder toolkit - sub-agent with main agent capabilities minus mode/task tools.

The Coder sub-agent is essentially the main agent with restrictions:
- No mode tools (enter_plan_mode, exit_plan, get_mode)
- No task tool (cannot spawn any sub-agents)
- Same read/write/execute capabilities as main agent

Simple two-layer model:
- Main agent can spawn Explore, Plan, Coder
- Coder cannot spawn any agents (leaf agent)
"""

from pathlib import Path
from typing import Optional

from ..toolkit import AgentToolkit
from ...utils.logger import log


class CoderToolkit(AgentToolkit):
    """Toolkit for Coder sub-agents - main agent capabilities minus excluded tools.

    Inherits all tools from AgentToolkit, then removes excluded ones.
    This is more explicit than overriding individual _register_* methods.

    Excluded tools:
    - task: Cannot spawn sub-agents (leaf agent)
    - enter_plan_mode: Mode control is main agent only
    - exit_plan: Mode control is main agent only
    - get_mode: Mode control is main agent only
    """

    # Tools to exclude from parent's tool set
    EXCLUDED_TOOLS = {
        "task",           # Cannot spawn sub-agents
        "enter_plan_mode",  # Mode switching is main agent only
        "exit_plan",      # Mode switching is main agent only
        "get_mode",       # Mode info is main agent only
    }

    def __init__(
        self,
        repo_root: Optional[Path] = None,
        **kwargs,
    ):
        """Initialize the Coder toolkit.

        Args:
            repo_root: Root directory of the repository
            **kwargs: Additional arguments passed to AgentToolkit
        """
        # Force code mode (not plan mode) for Coder
        kwargs["plan_mode"] = False

        # Let parent register all tools
        super().__init__(repo_root=repo_root, **kwargs)

        # Remove excluded tools
        self._filter_excluded_tools()

    def _filter_excluded_tools(self) -> None:
        """Remove excluded tools from the registry."""
        removed = []
        for tool_name in self.EXCLUDED_TOOLS:
            if tool_name in self._tools:
                del self._tools[tool_name]
                removed.append(tool_name)

        if removed:
            log.debug(f"CoderToolkit: excluded tools {removed}")
