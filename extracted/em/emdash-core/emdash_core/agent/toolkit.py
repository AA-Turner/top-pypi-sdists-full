"""Main AgentToolkit class for LLM agent graph exploration."""

import os
from pathlib import Path
from typing import Optional

from ..graph.connection import KuzuConnection, get_connection, KUZU_AVAILABLE
from .tools.base import BaseTool, ToolResult, ToolCategory
from .toolkits.base import BaseToolkit
from .session import AgentSession
from ..utils.logger import log


class AgentToolkit(BaseToolkit):
    """Main agent toolkit - full-featured toolkit for the primary agent.

    Inherits from BaseToolkit and adds:
    - Kuzu database connection for semantic search
    - Session tracking for exploration state
    - Plan mode support
    - MCP server integration

    Inheritance hierarchy:
        BaseToolkit          (base class with tool registry)
            └── AgentToolkit     (main agent - all tools)
                    └── CoderToolkit (sub-agent - filtered tools via EXCLUDED_TOOLS)

    Example:
        toolkit = AgentToolkit()

        # Search for relevant code
        result = toolkit.search("user authentication")

        # Get OpenAI schemas for function calling
        schemas = toolkit.get_all_schemas()

        # With custom MCP servers
        toolkit = AgentToolkit(mcp_config_path=Path(".emdash/mcp.json"))
    """

    def __init__(
        self,
        connection: Optional[KuzuConnection] = None,
        enable_session: bool = True,
        mcp_config_path: Optional[Path] = None,
        repo_root: Optional[Path] = None,
        plan_mode: bool = False,
        plan_file_path: Optional[str] = None,
    ):
        """Initialize the agent toolkit.

        Args:
            connection: Kuzu connection. If None, uses global connection.
            enable_session: Whether to track exploration state across calls.
            mcp_config_path: Path to MCP config file for dynamic tool registration.
                           If None, checks for .emdash/mcp.json in cwd.
            repo_root: Root directory of the repository for file operations.
                      If None, uses repo_root from config or current working directory.
            plan_mode: Whether to restrict to read-only tools for planning.
            plan_file_path: Path to the plan file (only writable file in plan mode).
        """
        # Handle connection - Kuzu is optional
        if connection is not None:
            self.connection = connection
        elif KUZU_AVAILABLE:
            try:
                self.connection = get_connection()
            except Exception as e:
                log.warning(f"Failed to connect to Kuzu database: {e}")
                log.warning("Semantic search will be disabled. Other tools will work normally.")
                self.connection = None
        else:
            log.info("Kuzu not installed - semantic search disabled. Install with: pip install kuzu")
            self.connection = None

        self.session = AgentSession() if enable_session else None
        self.plan_mode = plan_mode
        self.plan_file_path = plan_file_path

        # Get repo_root from config if not explicitly provided
        if repo_root is None:
            from ..config import get_config
            config = get_config()
            if config.repo_root:
                repo_root = Path(config.repo_root)
        resolved_repo_root = repo_root or Path.cwd()

        # Configure mode state if plan mode
        if plan_mode:
            from .tools.modes import ModeState, AgentMode
            mode_state = ModeState.get_instance()
            mode_state.current_mode = AgentMode.PLAN

        # Store as _repo_root for compatibility with existing code
        # NOTE: Must be set BEFORE super().__init__() because _register_tools() uses it
        self._repo_root = resolved_repo_root

        # Initialize base class with shared extensibility features
        # - enable_skills=True: Register skill tools from .emdash/skills/
        # - enable_mcp_config=True: Load MCP servers from config file
        super().__init__(
            repo_root=resolved_repo_root,
            mcp_servers=None,
            enable_mcp_config=True,
            mcp_config_path=mcp_config_path,
            enable_skills=True,
            connection=self.connection,
        )

    def _register_tools(self) -> None:
        """Override: Register all main agent tools.

        Called by BaseToolkit.__init__. AgentToolkit registers many tool categories.
        """
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        """Register all built-in tools.

        Note: Skill tools and MCP tools are registered by BaseToolkit
        after this method completes (via enable_skills and enable_mcp_config).
        """
        # Import tools here to avoid circular imports
        from .tools.search import (
            SemanticSearchTool,
            GrepTool,
            GlobTool,
        )
        from .tools.web import WebTool
        from .tools.coding import (
            ReadFileTool,
            ListFilesTool,
        )

        # Register search tools
        # SemanticSearchTool requires Kuzu database
        if self.connection is not None:
            self.register_tool(SemanticSearchTool(self.connection))
        # These tools work without database connection
        self.register_tool(GrepTool(self.connection))
        self.register_tool(GlobTool(self.connection))
        self.register_tool(WebTool(self.connection))

        # NOTE: Skill tools are registered by BaseToolkit (enable_skills=True)

        # Register read-only file tools (always available)
        self.register_tool(ReadFileTool(self._repo_root, self.connection))
        self.register_tool(ListFilesTool(self._repo_root, self.connection))

        # Register write tools - always available regardless of mode
        # Plan mode is now prompt-level guidance, not tool restriction
        from .tools.coding import (
            WriteToFileTool,
            DeleteFileTool,
            ExecuteCommandTool,
        )
        self.register_tool(WriteToFileTool(self._repo_root, self.connection))
        self.register_tool(DeleteFileTool(self._repo_root, self.connection))
        self.register_tool(ExecuteCommandTool(self._repo_root, self.connection))

        # Toggle between apply_diff (default) and edit_file based on env var
        if os.getenv("EMDASH_ENABLE_APPLY_DIFF", "true").lower() in ("0", "false", "no"):
            from .tools.coding import EditFileTool
            self.register_tool(EditFileTool(self._repo_root, self.connection))
        else:
            from .tools.coding import ApplyDiffTool
            self.register_tool(ApplyDiffTool(self._repo_root, self.connection))

        # Register sub-agent tools for spawning lightweight agents
        self._register_subagent_tools()

        # Register mode tools
        self._register_mode_tools()

        # Register task management tools (always full set)
        self._register_task_tools()

        # Traversal tools (expand_node, get_callers, etc.) and analytics tools
        # (get_area_importance, get_top_pagerank, etc.) are now provided
        # by the emdash-graph MCP server - registered via _init_mcp_manager()

        # NOTE: GitHub MCP tools are registered via _init_mcp_manager()
        # from the MCP config file (e.g., .emdash/mcp.json)
        # This allows using the official github-mcp-server directly

        log.debug(f"Registered {len(self._tools)} agent tools")

    def _register_subagent_tools(self) -> None:
        """Register sub-agent and background task management tools.

        These tools allow:
        - Spawning specialized sub-agents as subprocesses
        - Running shell commands in the background
        - Getting output from background tasks
        - Killing background tasks
        - Listing all background tasks
        """
        from .tools.task import TaskTool
        from .tools.task_output import TaskOutputTool, KillTaskTool, ListTasksTool

        self.register_tool(TaskTool(repo_root=self._repo_root, connection=self.connection))
        self.register_tool(TaskOutputTool(repo_root=self._repo_root, connection=self.connection))
        self.register_tool(KillTaskTool(repo_root=self._repo_root, connection=self.connection))
        self.register_tool(ListTasksTool(repo_root=self._repo_root, connection=self.connection))

    def _register_mode_tools(self) -> None:
        """Register mode tools.

        Only get_mode is registered - plan mode is now controlled via config.json
        (default_plan_mode setting) rather than enter/exit tools, so EmDash works
        in UIs that don't implement plan mode approval flows.
        """
        from .tools.modes import GetModeTool

        # get_mode is always available to check current mode
        self.register_tool(GetModeTool())

    def _register_plan_mode_task_tools(self) -> None:
        """Register subset of task tools for plan mode.

        In plan mode, the agent can ask clarifying questions,
        write plans to .emdash/plans/, and doesn't need completion/todo
        tools since exit_plan handles that.
        """
        from .tools.tasks import AskChoiceQuestionsTool
        from .tools.plan_write import WritePlanTool

        self.register_tool(AskChoiceQuestionsTool())
        self.register_tool(WritePlanTool(self._repo_root, self.connection))

    def _register_task_tools(self) -> None:
        """Register task management tools.

        These tools enable structured task tracking with todos,
        user interaction via follow-up questions, and completion signaling.

        When EMDASH_TASKS_V2 is enabled, registers additional tools for
        multi-agent task coordination with labels, dependencies, and claiming.
        """
        from emdash_core.tasks import is_tasks_v2_enabled

        if is_tasks_v2_enabled():
            # V2: Full task coordination tools for multi-agent workflows
            from .tools.tasks import (
                WriteTodoTool,
                UpdateTodoListTool,
                AskChoiceQuestionsTool,
                AttemptCompletionTool,
                RequestBrowserHandoffTool,
                ClaimTodoTool,
                CompleteTodoTool,
                GetClaimableTodosTool,
                GetTodosByLabelsTool,
                WaitForTodoTool,
                ReleaseTodoTool,
            )

            self.register_tool(WriteTodoTool())
            self.register_tool(UpdateTodoListTool())
            self.register_tool(AskChoiceQuestionsTool())
            self.register_tool(AttemptCompletionTool())
            self.register_tool(RequestBrowserHandoffTool())
            self.register_tool(ClaimTodoTool())
            self.register_tool(CompleteTodoTool())
            self.register_tool(GetClaimableTodosTool())
            self.register_tool(GetTodosByLabelsTool())
            self.register_tool(WaitForTodoTool())
            self.register_tool(ReleaseTodoTool())
        else:
            # V1: Basic todo tracking
            from .tools.tasks import (
                WriteTodoTool,
                UpdateTodoListTool,
                AskChoiceQuestionsTool,
                AttemptCompletionTool,
                RequestBrowserHandoffTool,
            )

            self.register_tool(WriteTodoTool())
            self.register_tool(UpdateTodoListTool())
            self.register_tool(AskChoiceQuestionsTool())
            self.register_tool(AttemptCompletionTool())
            self.register_tool(RequestBrowserHandoffTool())

    # NOTE: _register_skill_tools() and _init_mcp_from_config() are now
    # inherited from BaseToolkit and called automatically during __init__
    # when enable_skills=True and enable_mcp_config=True are passed.

    # get_mcp_manager() is also inherited from BaseToolkit

    def set_emitter(self, emitter) -> None:
        """Inject emitter into tools that need it.

        This should be called by the runner after toolkit creation
        to enable event streaming from tools like TaskTool.

        Args:
            emitter: AgentEventEmitter for streaming events
        """
        # Inject emitter into TaskTool for sub-agent event streaming
        task_tool = self.get_tool("task")
        if task_tool and hasattr(task_tool, "emitter"):
            task_tool.emitter = emitter
            log.debug("Injected emitter into TaskTool")

    def list_tools(self) -> list[dict]:
        """List all available tools.

        Returns:
            List of tool info dicts with name, description, category
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "category": tool.category.value,
            }
            for tool in self._tools.values()
        ]

    def execute(self, tool_name: str, **params) -> ToolResult:
        """Execute a tool by name with parameters.

        Args:
            tool_name: Name of the tool to execute
            **params: Tool-specific parameters

        Returns:
            ToolResult with success/data or error
        """
        tool = self.get_tool(tool_name)

        if not tool:
            return ToolResult.error_result(
                f"Unknown tool: {tool_name}",
                suggestions=[f"Available tools: {list(self._tools.keys())}"],
            )

        try:
            result = tool.execute(**params)

            # Track in session if enabled
            if self.session:
                self.session.record_action(tool_name, params, result)

            return result

        except Exception as e:
            log.exception(f"Tool execution error: {tool_name}")
            return ToolResult.error_result(
                f"Tool execution failed: {str(e)}",
                suggestions=["Check the parameters and try again"],
            )

    def get_schemas_by_category(self, category: str) -> list[dict]:
        """Get schemas for tools in a specific category.

        Args:
            category: Category name (search, traversal, analytics, history, planning)

        Returns:
            List of OpenAI function schemas for that category
        """
        return [
            tool.get_schema()
            for tool in self._tools.values()
            if tool.category.value == category
        ]

    def get_tools_by_category(self, category: str) -> list[BaseTool]:
        """Get all tools in a category.

        Args:
            category: Category name

        Returns:
            List of tool instances
        """
        return [
            tool
            for tool in self._tools.values()
            if tool.category.value == category
        ]

    def get_session_context(self) -> Optional[dict]:
        """Get current session context summary.

        Returns:
            Session context dict or None if session disabled
        """
        if self.session:
            return self.session.get_context_summary()
        return None

    def get_exploration_steps(self) -> list:
        """Get exploration steps from the current session.

        Returns:
            List of ExplorationStep objects or empty list if session disabled
        """
        if self.session:
            return self.session.steps
        return []

    def get_files_read(self) -> list[str]:
        """Get list of file paths that have been read in this session.

        Returns:
            List of file paths or empty list if session disabled
        """
        if self.session:
            return self.session.get_files_read()
        return []

    def reset_session(self) -> None:
        """Reset the exploration session state."""
        if self.session:
            self.session.reset()
        # Also reset task state
        from .tools.tasks import TaskState
        TaskState.reset()

    def partial_reset_for_compaction(self) -> None:
        """Partial reset for context compaction.

        Clears file tracking so the LLM can re-read files whose contents
        are no longer in its context window after compaction.
        """
        if self.session:
            self.session.partial_reset_for_compaction()

    # Convenience methods for common operations

    def search(self, query: str, **kwargs) -> ToolResult:
        """Convenience method for semantic search.

        Args:
            query: Natural language search query
            **kwargs: Additional parameters (entity_types, limit, min_score)

        Returns:
            ToolResult with matching entities
        """
        return self.execute("semantic_search", query=query, **kwargs)

    def expand(
        self,
        node_type: str,
        identifier: str,
        **kwargs,
    ) -> ToolResult:
        """Convenience method for node expansion.

        Args:
            node_type: Type of node (Function, Class, File)
            identifier: Qualified name or file path
            **kwargs: Additional parameters (max_hops)

        Returns:
            ToolResult with expanded graph context
        """
        return self.execute(
            "expand_node",
            node_type=node_type,
            identifier=identifier,
            **kwargs,
        )
