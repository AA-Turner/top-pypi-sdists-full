from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from .constants import CONNECTORS_KEY, MISTRALAI_PLUGIN_KEY
from .run_as import RunAsArg, normalize_run_as

if TYPE_CHECKING:
    from .client import ConnectorClient

ClassType = TypeVar("ClassType", bound=type)


class ConnectorSlot:
    """A declared connector dependency on a workflow.

    Pure configuration — holds the connector name, run_as identity, and
    authentication type. The actual auth flow is driven by
    :class:`~interceptor.ConnectorAuthInterceptor`.

    Args:
        connector_name: The connector's name, such as ``"notion"``.
        run_as: Whose connection the connector uses: ``"auto"`` or ``"deployment"``, as on :func:`connector`.
            ``None`` is ``"auto"``.
        auto_auth: Whether a missing connection starts an authorization flow that asks the user to connect.
        credentials_name: The name of one of the connector's stored credentials, such as ``"team"``.
            ``None`` leaves the choice to the connectors API.
        allow_mcp_ui: Whether MCP app resources the connector's tools declare are shown after their calls.
    """

    def __init__(
        self,
        connector_name: str,
        *,
        run_as: RunAsArg = None,
        auto_auth: bool = True,
        credentials_name: str | None = None,
        allow_mcp_ui: bool = False,
    ):
        self.connector_name = connector_name
        self.run_as_explicit: bool = run_as is not None
        """Whether ``run_as`` was given, rather than left to its default."""
        self.run_as = normalize_run_as(run_as)
        self.auto_auth = auto_auth
        self.credentials_name = credentials_name
        self.allow_mcp_ui = allow_mcp_ui

    def __call__(self) -> ConnectorClient:
        """Return a :class:`ConnectorClient` for this connector.

        This makes a ``ConnectorSlot`` usable as a ``Depends`` factory::

            notion = connector("notion", run_as="deployment")
            async def my_activity(client: ConnectorClient = Depends(notion)):
                async with client.mcp_client() as mcp: ...

        """
        from .client import ConnectorClient

        return ConnectorClient(
            self.connector_name,
            credentials_name=self.credentials_name,
            run_as=self.run_as if self.run_as_explicit else None,
        )

    def to_metadata(self) -> dict[str, Any]:
        """The connector's entry in a workflow's plugin metadata."""
        meta: dict[str, Any] = {
            "connector_name": self.connector_name,
            "auto_auth": self.auto_auth,
            "run_as": self.run_as.value,
        }
        if self.credentials_name is not None:
            meta["credentials_name"] = self.credentials_name
        if self.allow_mcp_ui:
            meta["allow_mcp_ui"] = True
        return meta


def connector(
    name: str,
    *,
    run_as: RunAsArg = None,
    auto_auth: bool = True,
    credentials_name: str | None = None,
    allow_mcp_ui: bool = False,
) -> ConnectorSlot:
    """Declare a connector dependency for a workflow.

    ``run_as`` declares which identity the connector runs as:

    - omitted / ``"auto"`` (default) — follow the workflow's ``on_behalf_of``
      flag: the executing user's credentials when the workflow runs on behalf
      of a user, the deployment's service credentials otherwise.
    - ``"deployment"`` — always the deployment's (worker's) service identity.

    When ``allow_mcp_ui`` is enabled, ``_meta.ui.resourceUri`` declared by MCP
    tools is surfaced as a side app in Vibe after each matching tool call.
    The workflow continues without waiting for, or consuming, app interaction
    results.

    Args:
        name: The connector's name, such as ``"notion"``.
        run_as: Whose connection the connector uses: ``"auto"`` or ``"deployment"``. ``None`` is ``"auto"``.
        auto_auth: Whether a missing connection starts an authorization flow that asks the user to connect.
        credentials_name: The name of one of the connector's stored credentials, such as ``"team"``.
            ``None`` leaves the choice to the connectors API.
        allow_mcp_ui: Whether MCP app resources the connector's tools declare are shown after their calls.
    """
    return ConnectorSlot(
        name,
        run_as=run_as,
        auto_auth=auto_auth,
        credentials_name=credentials_name,
        allow_mcp_ui=allow_mcp_ui,
    )


class ConnectorError(ValueError):
    pass


class ConnectorAuthTimeout(ConnectorError):
    pass


def raise_if_duplicate_connector_names(slots: Sequence[ConnectorSlot]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for slot in slots:
        if slot.connector_name in seen:
            duplicates.add(slot.connector_name)
        seen.add(slot.connector_name)
    if duplicates:
        raise ConnectorError(
            f"Cannot declare duplicate connector_name values {sorted(duplicates)}. "
            "Connector bindings are keyed by connector_name, so each connector must "
            "be declared at most once."
        )


def uses_connectors(*slots: ConnectorSlot) -> Callable[[ClassType], ClassType]:
    """Declare connector slots on a workflow class.

    Attaches metadata to ``cls.__plugin_metadata__`` for ``@workflow.define()``.
    The runtime auth flow is driven by
    :class:`~interceptor.ConnectorAuthInterceptor` which polls for credentials
    server-side.
    """

    def decorator(cls: ClassType) -> ClassType:
        raise_if_duplicate_connector_names(slots)
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
