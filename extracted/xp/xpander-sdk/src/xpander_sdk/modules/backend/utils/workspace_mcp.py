"""Local (stdio) MCP servers hosted in the agent's workspace.

An agent that is not a dedicated container has no place to spawn a stdio server: the
worker is shared, multi-tenant. Its workspace pod is exactly that place, and already
exposes a tool bridge (``mcp_list_tools`` / ``mcp_call_tool``) reachable through the
agent-controller proxy, which auto-starts a workspace that idled out.

This toolkit is the client side: tools are listed at build time and each becomes an agno
``Function`` that posts one call to the bridge. It is shaped like ``MCPTools`` on purpose
(``connect`` / ``close`` / ``initialized`` / ``functions``) so the dynamic-tools collapse
treats a local server exactly like a remote one.
"""

from typing import Any, Callable, Dict, List, Optional, Set

from agno.tools.function import Function, ToolResult
from agno.tools.toolkit import Toolkit
from loguru import logger

from xpander_sdk.consts.api_routes import APIRoute
from xpander_sdk.core.xpander_api_client import APIClient

# Same prefix MCPTools uses, so a tool from a local server and one from a remote server
# are indistinguishable to the model and to the dynamic catalog.
TOOL_NAME_PREFIX = "mcp_tool"

DEFAULT_CALL_TIMEOUT = 120

# Context objects agno passes alongside the model's arguments.
_AGNO_CONTEXT_KEYS = ("run_context", "agent", "team")


class WorkspaceMCPTools(Toolkit):
    """Tools of one local MCP server, executed inside the agent's workspace."""

    def __init__(
        self,
        agent_id: str,
        command: str,
        configuration: Any = None,
        server_name: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        include_tools: Optional[List[str]] = None,
        timeout_seconds: int = DEFAULT_CALL_TIMEOUT,
    ) -> None:
        super().__init__(
            name=f"workspace_mcp_{server_name or command}", auto_register=False
        )
        self.agent_id = agent_id
        self.command = command
        self.server_name = server_name or command
        self.env_vars = env_vars or {}
        self.include_tools = include_tools or None
        self.timeout_seconds = timeout_seconds
        self.configuration = configuration
        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    async def connect(self) -> None:
        """List the server's tools through the workspace bridge and register them.

        Idempotent: the dynamic path connects explicitly, the direct path is already
        connected by the time agno sees the toolkit.
        """
        if self._initialized:
            return
        response = await self._bridge(
            "mcp_list_tools",
            {
                "command": self.command,
                "name": self.server_name,
                "env_vars": self.env_vars,
            },
        )
        tools = (response.get("tools") if isinstance(response, dict) else None) or []
        for tool in tools:
            name = tool.get("name")
            if not name:
                continue
            if self.include_tools is not None and name not in self.include_tools:
                continue
            schema = tool.get("input_schema") or {}
            declared = set((schema.get("properties") or {}).keys())
            function = Function(
                name=f"{TOOL_NAME_PREFIX}_{name}",
                description=tool.get("description") or name,
                parameters=schema,
                entrypoint=self._entrypoint_for(name, declared),
                skip_entrypoint_processing=True,
            )
            self.functions[function.name] = function
        self._initialized = True
        logger.info(
            f"[workspace-mcp] '{self.server_name}' ready: {len(self.functions)} tool(s) "
            f"hosted in workspace {self.agent_id}"
        )

    async def close(self) -> None:
        """Drop the local view. The server itself stays warm in the workspace.

        Re-spawning is expensive and the workspace reaps its own idle sessions, so a
        finished run must not tear down a server the next run would need again.
        """
        self._initialized = False

    def _entrypoint_for(self, tool_name: str, declared: Set[str]) -> Callable[..., Any]:
        """One tool's entrypoint: post its arguments to the bridge, return agno's ToolResult."""

        async def call_tool(**kwargs: Any) -> ToolResult:
            # agno injects context objects, unless the tool declares those names itself.
            arguments = {
                k: v
                for k, v in kwargs.items()
                if k in declared or k not in _AGNO_CONTEXT_KEYS
            }
            try:
                result = await self._bridge(
                    "mcp_call_tool",
                    {
                        "command": self.command,
                        "name": self.server_name,
                        "env_vars": self.env_vars,
                        "tool": tool_name,
                        "arguments": arguments,
                        "timeout": self.timeout_seconds,
                    },
                )
                # A non-JSON 200 comes back as a plain string, so the shape is checked here
                # rather than assumed - an AttributeError would escape as a tool crash.
                body = result if isinstance(result, dict) else {"content": result}
                content = body.get("content") or ""
                is_error = bool(body.get("is_error"))
            except Exception as e:
                logger.warning(
                    f"[workspace-mcp] '{self.server_name}'.{tool_name} failed: {e}"
                )
                return ToolResult(content=f"Error from MCP tool '{tool_name}': {e}")
            if is_error:
                return ToolResult(
                    content=f"Error from MCP tool '{tool_name}': {content}"
                )
            return ToolResult(
                content=content if isinstance(content, str) else str(content)
            )

        return call_tool

    async def _bridge(self, tool_name: str, payload: Dict[str, Any]) -> Any:
        """POST one workspace tool call through the controller, which starts a stopped pod."""
        client = APIClient(configuration=self.configuration)
        return await client.make_request(
            path=str(APIRoute.WorkspaceToolInvoke).format(
                agent_id=self.agent_id, tool_name=tool_name
            ),
            method="POST",
            payload=payload,
        )
