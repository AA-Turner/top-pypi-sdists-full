"""Base class for sub-agent toolkits.

Provides shared extensibility features that can be used by all toolkit types:
- MCP server integration (from config file or per-agent configs)
- Skills system (load skills from .emdash/skills/)
- Rules loading (from .emdash/rules/)
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from ..tools.base import BaseTool, ToolResult

if TYPE_CHECKING:
    from ..agents import AgentMCPServerConfig
    from ..mcp.manager import MCPServerManager


class BaseToolkit(ABC):
    """Abstract base class for all toolkits.

    Each toolkit provides a curated set of tools appropriate for a specific
    agent type. Toolkits are responsible for:
    - Registering appropriate tools
    - Providing OpenAI function schemas
    - Executing tools by name
    - Managing per-agent MCP servers (optional)
    - Skills support (optional)

    Shared Extensibility Features:
        All toolkits can opt-in to these features:
        - MCP servers: Pass mcp_servers list OR set enable_mcp_config=True
        - Skills: Set enable_skills=True to register skill/list_skills tools
        - Rules: Use load_rules() to load rules from .emdash/rules/

    Tool Registration Pattern:
        Subclasses can either:
        1. Override _register_tools() to register tools directly
        2. Override get_tools() to return a list of tools (preferred for filtering)

    Tool Filtering Pattern:
        To create a toolkit that inherits tools but excludes some:
        ```
        class MyToolkit(ParentToolkit):
            EXCLUDED_TOOLS = {"tool_a", "tool_b"}

            def get_tools(self):
                return [t for t in super().get_tools()
                        if t.name not in self.EXCLUDED_TOOLS]
        ```
    """

    # List of tool names this toolkit provides (for documentation)
    TOOLS: list[str] = []

    # Tools to exclude (for subclasses that filter parent tools)
    EXCLUDED_TOOLS: set[str] = set()

    def __init__(
        self,
        repo_root: Path,
        mcp_servers: Optional[list["AgentMCPServerConfig"]] = None,
        enable_mcp_config: bool = False,
        mcp_config_path: Optional[Path] = None,
        enable_skills: bool = False,
        connection=None,
    ):
        """Initialize the toolkit.

        Args:
            repo_root: Root directory of the repository
            mcp_servers: Optional list of per-agent MCP server configurations
            enable_mcp_config: If True, load MCP servers from config file
            mcp_config_path: Path to MCP config file (defaults to .emdash/mcp.json)
            enable_skills: If True, register skill tools and load skills
            connection: Optional database connection for tools that need it
        """
        self.repo_root = repo_root.resolve()
        self._tools: dict[str, BaseTool] = {}
        self._mcp_manager: Optional["MCPServerManager"] = None
        self._mcp_servers_config = mcp_servers or []
        self._enable_mcp_config = enable_mcp_config
        self._mcp_config_path = mcp_config_path
        self._enable_skills = enable_skills
        self._connection = connection  # Database connection for semantic search etc.

        self._register_tools()

        # Initialize skills if enabled
        if enable_skills:
            self._register_skill_tools()

        # Initialize MCP servers (per-agent configs)
        self._init_mcp_servers()

        # Initialize MCP from config file if enabled
        if enable_mcp_config:
            self._init_mcp_from_config()

    def _register_tools(self) -> None:
        """Register tools for this toolkit.

        Default implementation calls get_tools() and registers each.
        Subclasses can override this or override get_tools().
        """
        for tool in self.get_tools():
            self.register_tool(tool)

    def get_tools(self) -> list[BaseTool]:
        """Return list of tools for this toolkit.

        Override this method to define available tools.
        Use EXCLUDED_TOOLS to filter out tools from parent class.

        Returns:
            List of BaseTool instances
        """
        return []

    def _register_skill_tools(self) -> None:
        """Register skill tools and load skills.

        Skills are loaded from three locations (in order, later overrides earlier):
        1. Built-in (bundled with emdash_core)
        2. Global (~/.emdash/skills/)
        3. Repo-local (.emdash/skills/)

        This method is called when enable_skills=True in __init__.
        """
        from ..tools.skill import SkillTool, ListSkillsTool
        from ..skills import SkillRegistry
        from ...utils.logger import log

        # Load skills from all sources (built-in, global, repo-local)
        # Don't pass args to load from SkillRegistry's three-source loading system
        registry = SkillRegistry.get_instance()
        registry.load_skills()

        # Register skill tools
        self.register_tool(SkillTool(self._connection))
        self.register_tool(ListSkillsTool(self._connection))

        skills_count = len(registry.list_skills())
        if skills_count > 0:
            log.info(f"Registered skill tools with {skills_count} skills available")

    def _init_mcp_from_config(self) -> None:
        """Initialize MCP manager and register tools from config file.

        Loads the MCP configuration file and registers all tools from
        enabled MCP servers. Creates default config if it doesn't exist.

        This method is called when enable_mcp_config=True in __init__.
        """
        from ..mcp import (
            MCPServerManager,
            get_default_mcp_config_path,
            create_tools_from_mcp,
        )
        from ..mcp.config import ensure_mcp_config
        from ...utils.logger import log

        # Determine config path
        config_path = self._mcp_config_path
        if config_path is None:
            config_path = get_default_mcp_config_path()

        # Ensure MCP config exists (creates default with github + emdash-graph)
        ensure_mcp_config(config_path)

        try:
            # Create manager
            self._mcp_manager = MCPServerManager(config_path=config_path)

            # Create and register dynamic tools
            tools = create_tools_from_mcp(self._mcp_manager, self._connection)
            for tool in tools:
                # Skip if tool name conflicts with existing tool
                if tool.name in self._tools:
                    log.warning(f"Skipping MCP tool '{tool.name}': conflicts with existing tool")
                    continue
                self.register_tool(tool)

            if tools:
                log.info(f"Registered {len(tools)} MCP tools from config")

        except Exception as e:
            log.warning(f"Failed to initialize MCP manager: {e}")

    def _init_mcp_servers(self) -> None:
        """Initialize per-agent MCP servers if configured.

        Creates an MCPServerManager with the agent's MCP server configs
        and registers the tools from those servers. Only enabled servers
        are started.

        This handles MCP servers passed via mcp_servers parameter (per-agent configs).
        For global MCP config file, use _init_mcp_from_config() instead.
        """
        if not self._mcp_servers_config:
            return

        # Filter to only enabled servers
        enabled_servers = [s for s in self._mcp_servers_config if s.enabled]
        if not enabled_servers:
            return

        from ..mcp.config import MCPServerConfig, MCPConfigFile
        from ..mcp.manager import MCPServerManager
        from ..mcp.tool_factory import create_tools_from_mcp
        from ...utils.logger import log

        log.info(f"Initializing {len(enabled_servers)} per-agent MCP servers")

        # Create a temporary config file object with our servers
        config = MCPConfigFile()
        for server_cfg in enabled_servers:
            mcp_config = MCPServerConfig(
                name=server_cfg.name,
                command=server_cfg.command,
                args=server_cfg.args,
                env=server_cfg.env,
                enabled=True,
                timeout=server_cfg.timeout,
            )
            config.add_server(mcp_config)

        # Create manager with in-memory config (not from file)
        self._mcp_manager = MCPServerManager(repo_root=self.repo_root)
        self._mcp_manager._config = config  # Inject our config directly

        # Start all servers and register tools
        try:
            started = self._mcp_manager.start_all_enabled()
            log.info(f"Started per-agent MCP servers: {started}")

            # Create tool wrappers and register them
            mcp_tools = create_tools_from_mcp(self._mcp_manager)
            for tool in mcp_tools:
                self.register_tool(tool)
                log.debug(f"Registered MCP tool: {tool.name}")

        except Exception as e:
            log.warning(f"Failed to initialize per-agent MCP servers: {e}")

    def load_rules(self, rule_names: Optional[list[str]] = None) -> str:
        """Load rules from .emdash/rules/ directory.

        Rules are markdown files that provide guidelines and constraints
        for the agent's behavior.

        Args:
            rule_names: Specific rule names to load. If None, loads all rules.

        Returns:
            Combined rules content as a string
        """
        rules_dir = self.repo_root / ".emdash" / "rules"
        if not rules_dir.exists():
            return ""

        parts = []

        if rule_names:
            # Load specific rules by name
            for name in rule_names:
                rule_file = rules_dir / f"{name}.md"
                if rule_file.exists():
                    try:
                        content = rule_file.read_text().strip()
                        if content:
                            parts.append(content)
                    except Exception:
                        pass
        else:
            # Load all rules
            for rule_file in sorted(rules_dir.glob("*.md")):
                try:
                    content = rule_file.read_text().strip()
                    if content:
                        parts.append(content)
                except Exception:
                    pass

        return "\n\n---\n\n".join(parts)

    def get_mcp_manager(self) -> Optional["MCPServerManager"]:
        """Get the MCP manager instance.

        Returns:
            MCPServerManager or None if not initialized
        """
        return self._mcp_manager

    def shutdown(self) -> None:
        """Shutdown the toolkit and cleanup resources.

        Stops any running MCP servers.
        """
        if self._mcp_manager:
            from ...utils.logger import log
            log.info("Shutting down agent MCP servers")
            self._mcp_manager.shutdown_all()
            self._mcp_manager = None

    def __del__(self):
        """Cleanup on garbage collection."""
        try:
            self.shutdown()
        except Exception:
            pass

    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool.

        Args:
            tool: Tool instance to register
        """
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        """List all tool names in this toolkit.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def execute(self, tool_name: str, **params) -> ToolResult:
        """Execute a tool by name.

        Args:
            tool_name: Name of the tool
            **params: Tool parameters

        Returns:
            ToolResult
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult.error_result(
                f"Unknown tool: {tool_name}",
                suggestions=[f"Available tools: {self.list_tools()}"],
            )

        try:
            return tool.execute(**params)
        except Exception as e:
            return ToolResult.error_result(f"Tool execution failed: {str(e)}")

    def get_all_schemas(self) -> list[dict]:
        """Get OpenAI function calling schemas for all tools.

        Returns:
            List of function schemas
        """
        return [tool.get_schema() for tool in self._tools.values()]

    def set_emitter(self, emitter) -> None:
        """Inject emitter into tools that need it.

        Subclasses can override to inject emitter into specific tools.
        Default implementation does nothing.

        Args:
            emitter: AgentEventEmitter for streaming events
        """
        pass

    def reset_session(self) -> None:
        """Reset session state.

        Subclasses can override to clear session-specific state.
        Default implementation does nothing.
        """
        pass

    def partial_reset_for_compaction(self) -> None:
        """Partial reset for context compaction.

        Clears file tracking so the LLM can re-read files whose contents
        are no longer in its context window after compaction.
        Subclasses can override to add additional reset logic.
        """
        pass

    def get_files_read(self) -> list[str]:
        """Get list of files read in this session.

        Returns:
            List of file paths (empty by default)
        """
        return []
