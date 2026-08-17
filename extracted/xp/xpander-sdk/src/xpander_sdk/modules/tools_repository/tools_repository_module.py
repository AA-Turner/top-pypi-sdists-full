"""
Tools Repository module for managing tools in the xpander.ai platform.

This module provides functionality to register, list, and manage tools within
the xpander.ai Backend-as-a-Service platform, supporting tool syncronization and
integration with AI agents.
"""

from inspect import Parameter, Signature
from typing import Any, Callable, ClassVar, List, Optional, Type
from pydantic import BaseModel, PrivateAttr, computed_field
from xpander_sdk.consts.api_routes import APIRoute
from xpander_sdk.core.xpander_api_client import APIClient
from xpander_sdk.exceptions.module_exception import ModuleException
from xpander_sdk.models.configuration import Configuration
from xpander_sdk.models.shared import XPanderSharedModel
from xpander_sdk.modules.tools_repository.sub_modules.tool import Tool
from xpander_sdk.modules.tools_repository.utils.schemas import PAYLOAD_WRAPPER_RULE
from xpander_sdk.modules.tools_repository.sub_modules.dynamic_tools import (
    build_dynamic_tools_hint,
    build_meta_tools,
    dynamic_tools_active,
    is_always_loaded,
)
from xpander_sdk.utils.cache import cached_tool_json_schema
from xpander_sdk.utils.event_loop import run_sync


class ToolsRepository(XPanderSharedModel):
    """
    Repository for managing tools in xpander.ai.

    This class provides methods for tool registration, discovery, and
    management. It supports dealing with both local tools defined via decorators
    and tools managed by the backend, ensuring integration consistency.

    Attributes:
        configuration (Optional[Configuration]): SDK configuration.
        tools (List[Tool]): List of tools managed by the backend.
        _local_tools (ClassVar[List[Tool]]): Registry of tools defined via decorators.

    Methods:
        register_tool: Register a local tool.
        list: Return a list of all tools.
        get_tool_by_id: Retrieve a tool by its ID.
        should_sync_local_tools: Check if local tools need syncing.
        get_local_tools_for_sync: Retrieve local tools that require syncing.
        functions: Return normalized callable functions for each tool.

    Example:
        >>> repo = ToolsRepository()
        >>> tools = repo.list
        >>> specific_tool = repo.get_tool_by_id("tool-id")
    """

    configuration: Optional[Configuration] = Configuration()

    # Mutable list that can be set/overwritten by backend
    tools: List[Tool] = []

    agent_graph: Optional[Any] = None
    is_async: Optional[bool] = True

    # Immutable registry for tools defined via decorator
    _local_tools: ClassVar[List[Tool]] = []

    # Dynamic-tools schema gate: ids the model has inspected via xp_get_tool
    # (or xp_search_tools detail='full'). Repo-scoped so the gate survives any
    # re-materialization of the non-cached `functions` property within a run.
    _dynamic_inspected: set = PrivateAttr(default_factory=set)

    # MCP server tools collapsed into the dynamic catalog for this run (populated
    # by the agno framework layer when use_dynamic_tools is on). The meta-tools
    # list/search/get/execute over these alongside repo.list.
    _dynamic_mcp_proxies: List[Any] = PrivateAttr(default_factory=list)

    # The live agno MCPTools toolkits backing the proxies above. The SDK owns
    # their session (they are kept out of the agno agent's tools so the LLM never
    # sees them); the worker closes them post-run via args["_xpander_hidden_mcp_toolkits"].
    _dynamic_mcp_toolkits: List[Any] = PrivateAttr(default_factory=list)

    @classmethod
    def register_tool(cls, tool: Tool):
        """
        Register a new local tool.

        Args:
            tool (Tool): The tool to register.
        """
        cls._local_tools.append(tool)

    @computed_field
    @property
    def list(self) -> List[Tool]:
        """
        Return a list of all available tools.

        Merges both backend-managed tools and locally registered tools,
        ensuring no duplicate IDs. Sets each tool's configuration for
        further communication.

        Returns:
            List[Tool]: A list of all available tools.
        """
        # Merge _local_tools and _tools, ensuring no duplicates by id
        all_tools = {tool.id: tool for tool in self.tools}
        for local_tool in self._local_tools:
            all_tools.setdefault(local_tool.id, local_tool)

        tools: List[Tool] = list(all_tools.values())

        for tool in tools:
            tool.set_configuration(configuration=self.configuration)
            if self.agent_graph:
                tool.set_schema_overrides(agent_graph=self.agent_graph)

        return tools

    @property
    def dynamic_catalog(self) -> List[Any]:
        """All targets the dynamic meta-tools operate over: xpander tools plus any
        MCP proxies collapsed into the catalog for this run."""
        return self.list + self._dynamic_mcp_proxies

    def get_tool_by_id(self, tool_id: str):
        """
        Retrieve a tool by its unique identifier.

        Args:
            tool_id (str): The ID of the tool to retrieve.

        Returns:
            Tool: The tool corresponding to the given ID.
        """
        return next((tool for tool in self.dynamic_catalog if tool.id == tool_id), None)

    def get_tool_by_name(self, tool_name: str):
        """
        Retrieve a tool by its unique identifier.

        Args:
            tool_name (str): The ID of the tool to retrieve.

        Returns:
            Tool: The tool corresponding to the given ID.
        """
        return next((tool for tool in self.dynamic_catalog if tool.name == tool_name), None)

    def should_sync_local_tools(self):
        """
        Determine if local tools need to be synchronized with the backend.

        Checks whether any local tool is marked for graph addition and
        has not been synced yet.

        Returns:
            bool: True if any local tools need syncing, False otherwise.
        """
        return any(tool.is_local and tool.should_add_to_graph for tool in self.list)

    def get_local_tools_for_sync(self):
        """
        Retrieve local tools that require synchronization with the backend.

        Returns:
            List[Tool]: List of local tools marked for graph addition that are not yet synced.
        """
        return [
            tool
            for tool in self.list
            if tool.is_local and tool.should_add_to_graph and not tool.is_synced
        ]

    @computed_field
    @property
    def functions(self) -> List[Callable[..., Any]]:
        """
        Get a list of normalized callable functions for each registered tool.

        Each function is designed to accept a single payload matching the
        tool's expected schema, allowing for direct execution with
        schema-validated data.

        Returns:
            List[Callable[..., Any]]: List of callable functions corresponding to tools.
        """
        fn_list = []

        # When dynamic tools are enabled, hide the bulk catalog from the LLM and
        # expose it through the four xp_* meta-tools instead. xp*/mcp* tools stay
        # loaded; knowledge-base and MCP tools never pass through here (they are
        # injected by the framework layer), so they are unaffected by design.
        agent = getattr(self.configuration.state, "agent", None)
        use_dynamic = dynamic_tools_active(agent, self)

        source_tools = self.list
        if use_dynamic:
            source_tools = [t for t in source_tools if is_always_loaded(t)]

        for tool in source_tools:

            # memoized: build_model_from_schema no longer re-runs per access
            schema_cls: Type[BaseModel] = tool.schema

            # Create closure to capture tool and schema_cls
            def make_tool_function(tool_ref, schema_ref, is_async: bool = False):
                """
                Factory that builds a normalized tool function.
                - If is_async=True, returns an async function (awaitable).
                - If is_async=False, returns a sync function (blocking, calls run_sync).
                """

                async def _execute(payload_dict: dict) -> Any:
                    return await tool_ref.ainvoke(
                        agent_id=self.configuration.state.agent.id,
                        agent_version=self.configuration.state.agent.version,
                        payload=payload_dict,
                        configuration=self.configuration,
                        task_id=(
                            self.configuration.state.task.id
                            if self.configuration.state.task
                            else None
                        ),
                    )

                if is_async:

                    async def tool_function(payload: schema_ref) -> Any:
                        """
                        Normalized async tool function that accepts a single Pydantic model payload.
                        """
                        payload_dict = payload.model_dump(exclude_none=True)
                        return await _execute(payload_dict)

                else:

                    def tool_function(payload: schema_ref) -> Any:
                        """
                        Normalized sync tool function that accepts a single Pydantic model payload.
                        """
                        if isinstance(payload, dict):
                            payload_dict = payload
                        else:
                            payload_dict = payload.model_dump(exclude_none=True)
                        return run_sync(_execute(payload_dict))

                # --- Metadata ---
                tool_function.__name__ = tool_ref.id

                # Build comprehensive docstring with parameter structure guidance
                base_doc = tool_ref.description or tool_ref.name

                # Extract schema properties for examples
                schema_props = cached_tool_json_schema(schema_ref, "validation").get("properties", {})
                param_names = list(schema_props.keys())

                # Create example structure
                example_parts = []
                for prop_name in param_names:
                    prop_info = schema_props.get(prop_name, {})
                    if prop_info.get("type") == "object" and prop_info.get(
                        "properties"
                    ):
                        # Show nested structure
                        nested_props = list(prop_info["properties"].keys())
                        if nested_props:
                            example_parts.append(
                                f'"{prop_name}": {{"{nested_props[0]}": ...}}'
                            )
                        else:
                            example_parts.append(f'"{prop_name}": {{}}')
                    else:
                        example_parts.append(f'"{prop_name}": ...')

                example_json = "{" + ", ".join(example_parts) + "}"

                tool_function.__doc__ = (
                    f"{base_doc}\n\n"
                    f'{PAYLOAD_WRAPPER_RULE}: {{"payload": {example_json}}}'
                )

                # --- Signature ---
                payload_param = Parameter(
                    name="payload",
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=schema_ref,
                )
                tool_function.__signature__ = Signature(
                    [payload_param],
                    return_annotation=Any,
                )

                # --- Annotations (for libraries that read __annotations__) ---
                ann = getattr(tool_function, "__annotations__", {})
                ann["payload"] = schema_ref
                ann["return"] = Any
                tool_function.__annotations__ = ann

                return tool_function

            fn = make_tool_function(tool, schema_cls, self.is_async)
            fn_list.append(fn)

        if use_dynamic:
            fn_list.extend(build_meta_tools(self))

        return fn_list

    def build_dynamic_tools_hint(self) -> str:
        """Instruction-hint block describing the hidden tool catalog and the
        xp_* meta-tools. Empty when there is nothing hidden. See
        ``sub_modules/dynamic_tools.build_dynamic_tools_hint``."""
        return build_dynamic_tools_hint(self)

    async def abuild_dynamic_tools_hint(self) -> str:
        """Async variant of :meth:`build_dynamic_tools_hint`. The work is pure
        (no I/O); provided for async/sync API parity."""
        return build_dynamic_tools_hint(self)

    async def aload_tool_by_id(self, tool_id: str):
        try:
            connector_id, operation_id = tool_id.split("_")
            client = APIClient(configuration=self.configuration)
            tool = await client.make_request(
                path=APIRoute.GetOrInvokeToolById.format(tool_id=tool_id)
            )
            self.tools = [
                Tool(
                    configuration=self.configuration,
                    **tool,
                    method="POST",
                    path="tool",
                    is_standalone=True,
                    connector_id=connector_id,
                    operation_id=operation_id,
                )
            ]
        except Exception as e:
            raise ModuleException(500, f"Failed to load tool by id - {str(e)}")

    def load_tool_by_id(self, tool_id: str):
        return run_sync(self.aload_tool_by_id(tool_id=tool_id))
