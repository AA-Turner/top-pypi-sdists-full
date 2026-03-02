"""Toolkit for the Open Agent.

Extends the CoworkerToolkit with self-modification tools that allow
the agent to learn, evolve, and manage its own capabilities.

Includes memory tools:
- memory_search: Full-text search over MEMORY.md + daily logs (OpenClaw)
- memory_get: Read exact content from memory files
- remember: Write to memory (auto-routed or explicit target)

Legacy memory tools (backward compat):
- recall, forget, list_memories, etc. via inline wrappers

User identity is stored in .emdash/rules/USER.md.
"""

import logging
from typing import Optional
from pathlib import Path

from ..toolkits.base import BaseToolkit
from ..tools.base import BaseTool, ToolResult
from .capabilities import CapabilityRegistry
from .tools import (
    AddCapabilityTool,
    RemoveCapabilityTool,
    ListCapabilitiesTool,
)
from .memory import HierarchicalMemory
from .memory_tools import MemoryToolSet
from .memory_store import MemoryStore
from .memory_index import MemoryIndex

logger = logging.getLogger(__name__)


class OpenToolkit(BaseToolkit):
    """Toolkit for Open Agent with OpenClaw memory and self-modification.

    Inherits base tools from the toolkit system and adds:
    - Capability tools (learned behaviors)
    - OpenClaw memory tools (memory_search, memory_get, remember)
    - Legacy memory tools (backward compatibility wrappers)
    """

    TOOLS = [
        # Capability tools
        "add_capability",
        "remove_capability",
        "list_capabilities",
        # OpenClaw memory tools
        "memory_search",
        "memory_get",
        "remember",
        # Legacy memory tools (kept for backward compat)
        "recall",
        "forget",
        "list_memories",
        "suggest_consolidation",
        "export_memory",
        "show_memory_stats",
        "reset_memory",
        # Channel management
        "manage_channel",
        # MCP server management
        "manage_mcp",
        # Automation (cron, heartbeat, webhooks)
        "manage_automation",
        # Inherited from base:
        "read_file",
        "write_to_file",
        "edit_file",
        "list_files",
        "glob",
        "grep",
        "semantic_search",
        "web_search",
        "execute_command",
        "task",
        "write_todo",
        "update_todo_list",
        "complete_todo",
        "get_claimable_todos",
        "skill",
        "list_skills",
    ]

    def __init__(
        self,
        repo_root: Path,
        capability_registry: Optional[CapabilityRegistry] = None,
        hierarchical_memory: Optional[HierarchicalMemory] = None,
        memory_tools: Optional[MemoryToolSet] = None,
        memory_store: Optional[MemoryStore] = None,
        memory_index: Optional[MemoryIndex] = None,
        **kwargs,
    ):
        """Initialize the Open Toolkit.

        Args:
            repo_root: Root directory of the repository
            capability_registry: Optional pre-configured CapabilityRegistry
            hierarchical_memory: Optional pre-configured HierarchicalMemory
            memory_tools: Optional pre-configured MemoryToolSet
            memory_store: OpenClaw MemoryStore for markdown file operations
            memory_index: OpenClaw MemoryIndex for full-text search
            **kwargs: Additional arguments passed to BaseToolkit
        """
        # Initialize all fields BEFORE super().__init__() because it calls _register_tools()

        # Initialize or use provided capability registry
        if capability_registry:
            self._capabilities = capability_registry
        else:
            self._capabilities = CapabilityRegistry(
                emdash_dir=repo_root / ".emdash",
            )

        # Initialize or use provided hierarchical memory
        if hierarchical_memory:
            self._memory = hierarchical_memory
        elif memory_tools:
            self._memory = memory_tools.memory
        else:
            self._memory = HierarchicalMemory(
                session_id="default",
                emdash_dir=repo_root / ".emdash",
            )

        # Initialize memory tools wrapper
        if memory_tools:
            self._memory_tools = memory_tools
        else:
            self._memory_tools = MemoryToolSet(self._memory)

        # OpenClaw memory system
        self._memory_store = memory_store
        self._memory_index = memory_index

        # OpenAgent uses the shared .emdash/mcp.json config, seeding it
        # from the open-agent template when the file doesn't exist yet.
        enable_mcp_config = kwargs.pop("enable_mcp_config", True)
        mcp_config_path = kwargs.pop("mcp_config_path", None)
        if mcp_config_path is None:
            mcp_config_path = repo_root / ".emdash" / "mcp.json"
        mcp_config_path = Path(mcp_config_path)

        if enable_mcp_config:
            self._ensure_open_mcp_config(mcp_config_path)

        super().__init__(
            repo_root=repo_root,
            enable_mcp_config=enable_mcp_config,
            mcp_config_path=mcp_config_path,
            **kwargs,
        )

    def _ensure_open_mcp_config(self, config_path: Path) -> None:
        """Ensure MCP config contains the open-agent default servers.

        If the config file doesn't exist, create it with open-agent defaults.
        If it already exists, merge in any missing open-agent servers.
        """
        try:
            from ..mcp.config import MCPConfigFile, get_open_agent_mcp_servers

            open_servers = get_open_agent_mcp_servers()

            if config_path.exists():
                config = MCPConfigFile.load(config_path)
                changed = False
                for name, server in open_servers.items():
                    if config.get_server(name) is None:
                        config.add_server(server)
                        changed = True
                if changed:
                    config.save(config_path)
            else:
                config = MCPConfigFile(servers=open_servers)
                config.save(config_path)
        except Exception as exc:
            logger.warning(f"Failed to ensure OpenAgent MCP config at {config_path}: {exc}")

    def _register_tools(self) -> None:
        """Register all tools for the Open Agent."""
        # Import base tools
        from ..tools.coding import ReadFileTool, WriteToFileTool, EditFileTool, ListFilesTool, ExecuteCommandTool
        from ..tools.search import GlobTool, GrepTool, SemanticSearchTool
        from ..tools.web import WebTool
        from ..tools.task import TaskTool
        from ..tools.tasks import (
            WriteTodoTool,
            UpdateTodoListTool,
            CompleteTodoTool,
            GetClaimableTodosTool,
            RequestBrowserHandoffTool,
        )
        from ..tools.skill import SkillTool, ListSkillsTool

        # Register base tools
        self._tools["read_file"] = ReadFileTool(repo_root=self.repo_root)
        self._tools["write_to_file"] = WriteToFileTool(repo_root=self.repo_root)
        self._tools["edit_file"] = EditFileTool(repo_root=self.repo_root)
        self._tools["list_files"] = ListFilesTool(repo_root=self.repo_root)
        self._tools["glob"] = GlobTool()
        self._tools["grep"] = GrepTool()
        self._tools["semantic_search"] = SemanticSearchTool()
        self._tools["web_search"] = WebTool()
        self._tools["execute_command"] = ExecuteCommandTool(repo_root=self.repo_root)
        self._tools["task"] = TaskTool(repo_root=self.repo_root)
        self._tools["write_todo"] = WriteTodoTool()
        self._tools["update_todo_list"] = UpdateTodoListTool()
        self._tools["complete_todo"] = CompleteTodoTool()
        self._tools["get_claimable_todos"] = GetClaimableTodosTool()
        self._tools["request_browser_handoff"] = RequestBrowserHandoffTool()
        self._tools["skill"] = SkillTool()
        self._tools["list_skills"] = ListSkillsTool()

        # Load skills from registry (built-in, global, repo-local)
        # This must happen so SkillTool can find skills like /telegram
        from ..skills import SkillRegistry
        registry = SkillRegistry.get_instance()
        registry.load_skills()

        # Register channel management tool
        from ..tools.channel import ChannelTool
        self._tools["manage_channel"] = ChannelTool()

        # Register MCP management tool (pass self so it can hot-load tools)
        from ..tools.mcp import MCPTool
        self._tools["manage_mcp"] = MCPTool(toolkit=self)

        # Register automation tool (cron, heartbeat, webhooks)
        from ..tools.automation import AutomationTool
        self._tools["manage_automation"] = AutomationTool()

        # Register capability tools
        self._tools["add_capability"] = AddCapabilityTool(self._capabilities)
        self._tools["remove_capability"] = RemoveCapabilityTool(self._capabilities)
        self._tools["list_capabilities"] = ListCapabilitiesTool(self._capabilities)

        # Register OpenClaw memory tools (if MemoryStore/Index available)
        if self._memory_store and self._memory_index:
            self._register_openclaw_memory_tools()

        # Register legacy memory tools (backward compat)
        self._register_legacy_memory_tools()

    # ------------------------------------------------------------------
    # OpenClaw memory tools
    # ------------------------------------------------------------------

    def _register_openclaw_memory_tools(self) -> None:
        """Register the OpenClaw-style memory tools (memory_search, memory_get, remember)."""
        from .memory_tools_v2 import MemorySearchTool, MemoryGetTool, RememberTool

        self._tools["memory_search"] = MemorySearchTool(self._memory_index)
        self._tools["memory_get"] = MemoryGetTool(self._memory_store)
        self._tools["remember"] = RememberTool(self._memory_store, self._memory_index)

    # ------------------------------------------------------------------
    # Legacy memory tools (backward compat)
    # ------------------------------------------------------------------

    def _register_legacy_memory_tools(self) -> None:
        """Register legacy memory tools as callable tools."""
        from ..tools.base import ToolCategory

        memory_tools = self._memory_tools

        # Only register 'remember' if OpenClaw didn't already register it
        if "remember" not in self._tools:
            class RememberToolLegacy(BaseTool):
                name = "remember"
                category = ToolCategory.LEARNING
                description = "Store information in memory (long_term/short_term)"
                def __init__(self, mt): super().__init__(); self._mt = mt
                def get_schema(self):
                    return self._make_schema({"content": {"type": "string", "description": "The information to remember"}, "key": {"type": "string", "description": "Optional identifier for this memory (auto-generated if omitted)"}, "layer": {"type": "string", "description": "Which layer (long_term/short_term)"}, "importance": {"type": "number", "description": "Importance 0.0-1.0"}, "context": {"type": "string", "description": "Category"}, "tags": {"type": "array", "items": {"type": "string"}, "description": "List of tags"}}, required=["content"])
                def execute(self, content: str, key: str = None, layer: str = "long_term", importance: float = 0.5, context: str = "general", tags: list = None, **kwargs):
                    result = self._mt.remember(content, layer, key, importance, context, tags or [])
                    return ToolResult.success_result(data=result) if result.get("success") else ToolResult.error_result(result.get("error", "Unknown error"))
            self._tools["remember"] = RememberToolLegacy(memory_tools)

        class RecallTool(BaseTool):
            name = "recall"
            category = ToolCategory.LEARNING
            description = "Search memory for stored information"
            def __init__(self, mt): super().__init__(); self._mt = mt
            def get_schema(self):
                return self._make_schema({"query": {"type": "string", "description": "Search query"}, "layers": {"type": "array", "items": {"type": "string"}, "description": "Which layers to search"}, "context": {"type": "string", "description": "Filter by context"}, "top_k": {"type": "integer", "description": "Max results"}}, required=["query"])
            def execute(self, query: str, layers: list = None, context: str = None, top_k: int = 5, **kwargs):
                result = self._mt.recall(query, layers, context, top_k)
                return ToolResult.success_result(data=result) if result.get("success") else ToolResult.error_result(result.get("error", "Unknown error"))

        class ForgetTool(BaseTool):
            name = "forget"
            category = ToolCategory.LEARNING
            description = "Remove a memory entry by key from long_term layer"
            def __init__(self, mt): super().__init__(); self._mt = mt
            def get_schema(self):
                return self._make_schema({"key": {"type": "string", "description": "Memory key to remove"}, "layer": {"type": "string", "description": "Which layer (long_term)"}}, required=["key"])
            def execute(self, key: str, layer: str = "long_term", **kwargs):
                result = self._mt.forget(key, layer)
                return ToolResult.success_result(data=result) if result.get("success") else ToolResult.error_result(result.get("error", "Unknown error"))

        class ListMemoriesTool(BaseTool):
            name = "list_memories"
            category = ToolCategory.LEARNING
            description = "List stored memories"
            def __init__(self, mt): super().__init__(); self._mt = mt
            def get_schema(self):
                return self._make_schema({"layer": {"type": "string", "description": "Which layer (long_term/short_term)"}, "context": {"type": "string", "description": "Filter by context"}, "limit": {"type": "integer", "description": "Max results"}})
            def execute(self, layer: str = "long_term", context: str = None, limit: int = 20, **kwargs):
                result = self._mt.list_memories(layer, context, limit)
                return ToolResult.success_result(data=result) if result.get("success") else ToolResult.error_result(result.get("error", "Unknown error"))

        class SuggestConsolidationTool(BaseTool):
            name = "suggest_consolidation"
            category = ToolCategory.LEARNING
            description = "Analyze short-term memory and suggest what to remember long-term"
            def __init__(self, mt): super().__init__(); self._mt = mt
            def get_schema(self):
                return self._make_schema({})
            def execute(self, **kwargs):
                result = self._mt.suggest_consolidation()
                return ToolResult.success_result(data=result) if result.get("success") else ToolResult.error_result(result.get("error", "Unknown error"))

        class ExportMemoryTool(BaseTool):
            name = "export_memory"
            category = ToolCategory.LEARNING
            description = "Export all memory layers"
            def __init__(self, mt): super().__init__(); self._mt = mt
            def get_schema(self):
                return self._make_schema({"layer": {"type": "string", "description": "Specific layer or all"}})
            def execute(self, layer: str = None, **kwargs):
                result = self._mt.export_memory(layer)
                return ToolResult.success_result(data=result) if result.get("success") else ToolResult.error_result(result.get("error", "Unknown error"))

        class ShowMemoryStatsTool(BaseTool):
            name = "show_memory_stats"
            category = ToolCategory.LEARNING
            description = "Show memory usage statistics"
            def __init__(self, mt): super().__init__(); self._mt = mt
            def get_schema(self):
                return self._make_schema({})
            def execute(self, **kwargs):
                result = self._mt.get_memory_stats()
                return ToolResult.success_result(data=result) if result.get("success") else ToolResult.error_result(result.get("error", "Unknown error"))

        class ResetMemoryTool(BaseTool):
            name = "reset_memory"
            category = ToolCategory.LEARNING
            description = "Reset memory layer(s) - use with caution"
            def __init__(self, mt): super().__init__(); self._mt = mt
            def get_schema(self):
                return self._make_schema({"layer": {"type": "string", "description": "Which layer or 'all'"}, "confirm": {"type": "boolean", "description": "Must be True to proceed"}})
            def execute(self, layer: str = None, confirm: bool = False, **kwargs):
                result = self._mt.reset_memory(layer, confirm)
                return ToolResult.success_result(data=result) if result.get("success") else ToolResult.error_result(result.get("error", "Unknown error"))

        self._tools["recall"] = RecallTool(memory_tools)
        self._tools["forget"] = ForgetTool(memory_tools)
        self._tools["list_memories"] = ListMemoriesTool(memory_tools)
        self._tools["suggest_consolidation"] = SuggestConsolidationTool(memory_tools)
        self._tools["export_memory"] = ExportMemoryTool(memory_tools)
        self._tools["show_memory_stats"] = ShowMemoryStatsTool(memory_tools)
        self._tools["reset_memory"] = ResetMemoryTool(memory_tools)

    @property
    def capability_registry(self) -> CapabilityRegistry:
        """Get the capability registry."""
        return self._capabilities

    @property
    def hierarchical_memory(self) -> HierarchicalMemory:
        """Get the hierarchical memory."""
        return self._memory

    @property
    def memory_tools(self) -> MemoryToolSet:
        """Get the memory tools wrapper."""
        return self._memory_tools

    def get_files_read(self) -> list[str]:
        """Get list of files read by the toolkit tools."""
        files = []
        if "read_file" in self._tools:
            read_tool = self._tools["read_file"]
            if hasattr(read_tool, "get_files_read"):
                files.extend(read_tool.get_files_read())
        return files
