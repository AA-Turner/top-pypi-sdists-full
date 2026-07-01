from __future__ import annotations

from typing import Any

from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context

from .activities import connector_tool_call
from .constants import CONNECTORS_KEY, MISTRALAI_PLUGIN_KEY
from .mcp_apps import connector_get_mcp_app_resource_uris
from .models import ResolvedConnectorBinding


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

    def __init__(self, connector_name: str, *, credentials_name: str | None = None):
        self._connector_name = connector_name
        self._credentials_name = credentials_name
        self._mcp_ui_resource_uris_by_binding: dict[tuple[str, str | None], dict[str, str]] = {}

    def _resolve_binding(self) -> ResolvedConnectorBinding:
        """Resolve the connector binding from the current workflow context."""
        context = retrieve_context()
        if context is None:
            raise RuntimeError(
                f"No workflow context available — ToolCallClient for "
                f"'{self._connector_name}' must be used inside a workflow activity"
            )

        mistralai_ext = context.extensions.get(MISTRALAI_PLUGIN_KEY, {})
        bindings = mistralai_ext.get(CONNECTORS_KEY, {}).get("bindings", [])
        raw = next((b for b in bindings if b["connector_name"] == self._connector_name), None)
        if raw is not None:
            return ResolvedConnectorBinding(**raw)
        return ResolvedConnectorBinding(connector_name=self._connector_name)

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
        mcp_ui_resource_uri = await self._get_mcp_ui_resource_uri(binding, credentials_name, tool_name)
        return await connector_tool_call(
            connector_id_or_name=binding.connector_id or binding.connector_name,
            tool_name=tool_name,
            arguments=arguments,
            credentials_name=credentials_name,
            mcp_ui_resource_uri=mcp_ui_resource_uri,
        )

    async def _get_mcp_ui_resource_uri(
        self,
        binding: ResolvedConnectorBinding,
        credentials_name: str | None,
        tool_name: str,
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
            )
        return self._mcp_ui_resource_uris_by_binding[cache_key].get(tool_name)
