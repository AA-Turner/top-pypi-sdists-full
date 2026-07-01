from __future__ import annotations

from typing import Any, Callable, TypeVar

from .client import ToolCallClient
from .constants import CONNECTORS_KEY, MISTRALAI_PLUGIN_KEY

ClassType = TypeVar("ClassType", bound=type)


class ConnectorSlot:
    """A declared connector dependency on a workflow.

    Pure configuration — holds the connector name and authentication type.
    The actual auth flow is driven by
    :class:`~interceptor.ConnectorAuthInterceptor`.
    """

    def __init__(
        self,
        connector_name: str,
        *,
        auto_auth: bool = True,
        credentials_name: str | None = None,
        allow_mcp_ui: bool = False,
    ):
        self.connector_name = connector_name
        self.auto_auth = auto_auth
        self.credentials_name = credentials_name
        self.allow_mcp_ui = allow_mcp_ui

    def __call__(self) -> ToolCallClient:
        """Return a :class:`ToolCallClient` for this connector.

        This makes a ``ConnectorSlot`` usable as a ``Depends`` factory::

            notion = connector("notion")
            async def my_activity(client: ToolCallClient = Depends(notion)): ...

        """
        return ToolCallClient(self.connector_name, credentials_name=self.credentials_name)

    def to_metadata(self) -> dict[str, Any]:
        meta: dict[str, Any] = {
            "connector_name": self.connector_name,
            "auto_auth": self.auto_auth,
        }
        if self.credentials_name is not None:
            meta["credentials_name"] = self.credentials_name
        if self.allow_mcp_ui:
            meta["allow_mcp_ui"] = True
        return meta


def connector(
    name: str,
    *,
    auto_auth: bool = True,
    credentials_name: str | None = None,
    allow_mcp_ui: bool = False,
) -> ConnectorSlot:
    """Declare a connector dependency for a workflow.

    When ``allow_mcp_ui`` is enabled, ``_meta.ui.resourceUri`` declared by MCP
    tools is surfaced as a side app in Vibe after each matching tool call.
    The workflow continues without waiting for, or consuming, app interaction
    results.
    """
    return ConnectorSlot(
        name,
        auto_auth=auto_auth,
        credentials_name=credentials_name,
        allow_mcp_ui=allow_mcp_ui,
    )


class ConnectorError(Exception):
    pass


class ConnectorAuthTimeout(ConnectorError):
    pass


def uses_connectors(*slots: ConnectorSlot) -> Callable[[ClassType], ClassType]:
    """Declare connector slots on a workflow class.

    Attaches metadata to ``cls.__plugin_metadata__`` for ``@workflow.define()``.
    The runtime auth flow is driven by
    :class:`~interceptor.ConnectorAuthInterceptor` which polls for credentials
    server-side.
    """

    def decorator(cls: ClassType) -> ClassType:
        metadata: dict[str, Any] = dict(getattr(cls, "__plugin_metadata__", {}) or {})
        mistralai_meta = metadata.get(MISTRALAI_PLUGIN_KEY, {})
        mistralai_meta[CONNECTORS_KEY] = [s.to_metadata() for s in slots]
        metadata[MISTRALAI_PLUGIN_KEY] = mistralai_meta
        cls.__plugin_metadata__ = metadata  # type: ignore[attr-defined]

        # If @workflow.define already ran, update the stored WorkflowSpec directly.
        defn = getattr(cls, "__workflows_workflow_def", None)
        if defn is not None:
            defn.plugin_metadata = metadata

        return cls

    return decorator
