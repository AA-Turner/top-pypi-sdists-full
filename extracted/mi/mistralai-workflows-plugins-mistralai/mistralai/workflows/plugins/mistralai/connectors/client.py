from __future__ import annotations

from typing import Any

from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.models import WorkflowContext

from .activities import connector_tool_call
from .constants import MISTRALAI_PLUGIN_KEY
from .decorator import ConnectorError
from .mcp_apps import connector_get_mcp_app_resource_uris
from .models import ResolvedConnectorBinding, resolved_connector_bindings_from_extension
from .run_as import ConnectorRunAs, RunAsArg, normalize_run_as


class ToolCallClient:
    """Client for calling connector tools within workflow activities.

    Created via dependency injection (``Depends(connector("github"))``) or
    directly::

        client = ToolCallClient("github")
        result = await client.call_tool("create_issue", {"title": "bug"})

    The client is safe to construct at worker startup time — it stores only
    the connector name and lazily resolves the binding from workflow context
    when a method is actually called during activity execution.
    """

    def __init__(
        self,
        connector_name: str,
        *,
        credentials_name: str | None = None,
        run_as: RunAsArg = None,
    ):
        self._connector_name = connector_name
        self._credentials_name = credentials_name
        # None means "unspecified" — inherit run_as from the resolved binding at
        # call time. An explicit value always wins.
        self._run_as = normalize_run_as(run_as) if run_as is not None else None
        self._mcp_ui_resource_uris_by_binding: dict[tuple[str, str | None], dict[str, str]] = {}

    @staticmethod
    def _resolved_bindings_from_context(context: WorkflowContext) -> list[ResolvedConnectorBinding]:
        if MISTRALAI_PLUGIN_KEY not in context.trusted_extensions:
            return []
        return resolved_connector_bindings_from_extension(context.trusted_extensions[MISTRALAI_PLUGIN_KEY])

    def _resolve_binding(self) -> ResolvedConnectorBinding:
        """Resolve the connector binding from the current workflow context."""
        context = retrieve_context()
        if context is None:
            raise RuntimeError(
                f"No workflow context available — ToolCallClient for "
                f"'{self._connector_name}' must be used inside a workflow activity"
            )

        resolved_bindings = [
            binding
            for binding in self._resolved_bindings_from_context(context)
            if binding.connector_name == self._connector_name
        ]
        if len(resolved_bindings) > 1:
            raise ConnectorError(
                f"Multiple interceptor-resolved bindings found for connector {self._connector_name!r}. "
                "Connector names must be unique in @uses_connectors(...)."
            )
        if resolved_bindings:
            binding = resolved_bindings[0]
            if self._run_as is not None and self._run_as != binding.run_as:
                raise ConnectorError(
                    f"ToolCallClient for connector {self._connector_name!r} has run_as='{self._run_as.value}' "
                    f"but @uses_connectors(...) resolved run_as='{binding.run_as.value}'. "
                    "Use the same connector declaration for preflight and tool calls."
                )
            return binding
        raise ConnectorError(
            f"Connector {self._connector_name!r} is not resolved for this workflow. Add "
            f'@uses_connectors(connector("{self._connector_name}")) to your workflow class so the '
            f"interceptor runs connector auth preflight before the tool call."
        )

    @property
    def binding(self) -> ResolvedConnectorBinding:
        return self._resolve_binding()

    @property
    def connector_id(self) -> str | None:
        return self._resolve_binding().connector_id

    @property
    def connector_name(self) -> str:
        return self._connector_name

    async def call_tool(self, tool_name: str, arguments: dict[str, Any] | None = None) -> Any:
        """Call a connector tool via the MistralPrivate SDK."""
        binding = self._resolve_binding()
        credentials_name = self._credentials_name or binding.credentials_name
        run_as = binding.run_as
        mcp_ui_resource_uri = await self._get_mcp_ui_resource_uri(binding, credentials_name, tool_name, run_as)
        return await connector_tool_call(
            connector_id_or_name=binding.connector_id or binding.connector_name,
            tool_name=tool_name,
            arguments=arguments,
            credentials_name=credentials_name,
            mcp_ui_resource_uri=mcp_ui_resource_uri,
            run_as=run_as,
        )

    async def _get_mcp_ui_resource_uri(
        self,
        binding: ResolvedConnectorBinding,
        credentials_name: str | None,
        tool_name: str,
        run_as: ConnectorRunAs,
    ) -> str | None:
        if credentials_name == binding.credentials_name and (
            binding.mcp_ui_resource_uris or binding.mcp_ui_resource_uris_fetched
        ):
            return binding.mcp_ui_resource_uris.get(tool_name)

        if not binding.allow_mcp_ui and not binding.mcp_ui_resource_uris:
            return None

        connector_id_or_name = binding.connector_id or binding.connector_name
        cache_key = (connector_id_or_name, credentials_name)
        if cache_key not in self._mcp_ui_resource_uris_by_binding:
            self._mcp_ui_resource_uris_by_binding[cache_key] = await connector_get_mcp_app_resource_uris(
                connector_id_or_name,
                credentials_name=credentials_name,
                run_as=run_as,
            )
        return self._mcp_ui_resource_uris_by_binding[cache_key].get(tool_name)
