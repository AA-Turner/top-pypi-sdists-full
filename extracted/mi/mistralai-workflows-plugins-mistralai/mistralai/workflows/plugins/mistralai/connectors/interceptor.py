"""Temporal interceptor that auto-manages connector authentication.

For every workflow execution the interceptor:

1. Reads connector slots from the workflow's ``plugin_metadata``.
2. For each ``auto_auth=True`` connector, checks credential status:

   a. If ``credentials_name`` is set, verifies that credential exists.
   b. Otherwise checks for existing user credentials.
   c. If no user credentials but the connector has preset OAuth2 app
      config, emits a marker activity with the OAuth URL and
      polls the connector credentials API until the user completes
      the OAuth flow.
   d. If no credentials and no preset, inspects the connector's
      authentication methods and redirects to OAuth2 when available.
      Bearer tokens must be configured beforehand.

Usage — register alongside the existing ``ContextHandlerInterceptor``::

    worker = Worker(
        ...,
        interceptors=[
            ContextHandlerInterceptor(),
            ConnectorAuthInterceptor(workflows=workflows),
        ],
    )

Workflows declare connectors via ``@uses_connectors``::

    @workflow.define(name="my-workflow")
    @uses_connectors(connector("github"), connector("slack"))
    class MyWorkflow:
        @workflow.entrypoint
        async def run(self, prompt: str) -> dict:
            return await my_activity(prompt)
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any, Sequence, Type

import structlog
import temporalio.worker
import temporalio.workflow

from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context, workflow_context_var

from .activities import (
    connector_get_auth_methods,
    connector_get_auth_url,
    connector_list_tools,
    connector_list_user_credentials,
    connector_resolve,
    connector_wait_for_credentials,
)
from .constants import CONNECTORS_KEY, MISTRALAI_PLUGIN_KEY
from .decorator import ConnectorAuthTimeout, ConnectorError, ConnectorSlot
from .event_activities import (
    _emit_connector_auth_completed,
    _emit_connector_auth_failed,
    _emit_connector_auth_started,
)
from .mcp_apps import connector_get_mcp_app_resource_uris
from .models import (
    ConnectorDefinition,
    ConnectorExtensionBinding,
)

logger = structlog.get_logger(__name__)


def _build_plugin_metadata_index(workflows: Sequence[Type]) -> dict[str, dict[str, Any]]:
    """Build a {workflow_name: plugin_metadata} mapping from workflow classes.

    Reads the ``__workflows_workflow_def`` attribute that ``@workflow.define``
    stores on each class, so the metadata is tied to the classes the worker
    actually registered.
    """
    index: dict[str, dict[str, Any]] = {}
    for wf_cls in workflows:
        defn = get_workflow_definition(wf_cls)
        metadata = defn.plugin_metadata or getattr(wf_cls, "__plugin_metadata__", None)
        if metadata:
            index[defn.name] = metadata
    return index


async def _wait_for_connector_auth(
    slot: ConnectorSlot,
    connector_id: str,
    auth_url: str,
) -> None:
    """Emit a marker with the OAuth URL and poll until credentials appear."""
    task_id = str(temporalio.workflow.uuid4())

    # Emit front-end marker so the UI can detect the auth step and
    # extract the OAuth URL, connector ID, etc.
    await temporalio.workflow.execute_local_activity(
        _emit_connector_auth_started,
        args=[task_id, slot.connector_name, connector_id, auth_url, slot.credentials_name],
        start_to_close_timeout=timedelta(seconds=10),
    )

    # Single long-lived activity that polls the credentials API
    # internally with heartbeats — keeps workflow history clean.
    authenticated = await connector_wait_for_credentials(
        connector_id=connector_id, credentials_name=slot.credentials_name
    )

    if not authenticated:
        await temporalio.workflow.execute_local_activity(
            _emit_connector_auth_failed,
            args=[
                task_id,
                slot.connector_name,
                connector_id,
                f"Connector '{slot.connector_name}' auth timed out",
                slot.credentials_name,
            ],
            start_to_close_timeout=timedelta(seconds=10),
        )
        raise ConnectorAuthTimeout(f"Connector '{slot.connector_name}' auth timed out")

    await temporalio.workflow.execute_local_activity(
        _emit_connector_auth_completed,
        args=[task_id, slot.connector_name, connector_id, slot.credentials_name],
        start_to_close_timeout=timedelta(seconds=10),
    )


class ConnectorAuthWorkflowInboundInterceptor(temporalio.worker.WorkflowInboundInterceptor):
    """Resolves connectors from input, runs auth preflight with server-side polling."""

    # Overridden by the subclass that ConnectorAuthInterceptor creates.
    _metadata_by_name: dict[str, dict[str, Any]] = {}

    @staticmethod
    def _extract_extension_bindings() -> list[ConnectorExtensionBinding]:
        """Read connector binding overrides from the workflow context.

        The ``ContextHandlerInterceptor`` (registered on the Temporal client)
        always runs before this worker-level interceptor, so the workflow
        context — including ``extensions`` — is available via
        ``retrieve_context()``.
        """
        ctx = retrieve_context()
        if not ctx or not ctx.extensions:
            return []
        raw = ctx.extensions.get(MISTRALAI_PLUGIN_KEY, {}).get(CONNECTORS_KEY, {}).get("bindings", [])
        return [ConnectorExtensionBinding.model_validate(b) for b in raw]

    @staticmethod
    def _apply_extension_bindings(
        slots: list[ConnectorSlot],
        bindings: list[ConnectorExtensionBinding],
    ) -> None:
        """Overlay runtime extension bindings onto the static connector slots.

        Raises :class:`ConnectorError` if any binding names a connector
        that is not declared in the workflow's ``@uses_connectors`` slots.
        """
        slot_names = {s.connector_name for s in slots}
        binding_by_name = {b.connector_name: b for b in bindings}

        unknown = set(binding_by_name) - slot_names
        if unknown:
            raise ConnectorError(
                f"Extension bindings reference unknown connectors: {sorted(unknown)}. "
                f"Declared connectors: {sorted(slot_names)}"
            )

        for slot in slots:
            override = binding_by_name.get(slot.connector_name)
            if override is None:
                continue
            if override.credentials_name is not None:
                slot.credentials_name = override.credentials_name

    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> Any:
        slots = self._get_connector_slots()
        if not slots:
            return await super().execute_workflow(input)

        # Log what was passed to the workflow
        ctx = retrieve_context()
        raw_extensions = ctx.extensions if ctx else None
        logger.info(
            "Starting connector auth preflight",
            connector_slots=[s.connector_name for s in slots],
            workflow_extensions=raw_extensions,
        )

        # Merge runtime extension bindings (e.g. credentials_name overrides)
        # into the static slots from the workflow decorator.
        ext_bindings = self._extract_extension_bindings()
        if ext_bindings:
            logger.info(
                "Applying runtime extension bindings",
                bindings=[
                    {
                        "connector_name": b.connector_name,
                        "credentials_name": b.credentials_name,
                        "connector_id": b.connector_id,
                    }
                    for b in ext_bindings
                ],
            )
            self._apply_extension_bindings(slots, ext_bindings)

        # Resolve all connectors and run auth preflight for auto_auth ones.
        resolved_bindings: list[dict[str, Any]] = []
        for slot in slots:
            # Resolve every connector to get its connector_id.
            logger.info(
                "Resolving connector",
                connector_name=slot.connector_name,
                credentials_name=slot.credentials_name,
            )
            resolved = await connector_resolve(slot.connector_name)
            logger.info(
                "Connector resolved",
                connector_name=slot.connector_name,
                connector_id=resolved.id,
            )

            mcp_ui_resource_uris: dict[str, str] = {}
            mcp_ui_resource_uris_fetched = False

            if not slot.auto_auth:
                logger.info(
                    "Skipping auth preflight (auto_auth=False)",
                    connector_name=slot.connector_name,
                )
            else:
                # 1. List user credentials for this connector.
                creds_info = await connector_list_user_credentials(resolved.id)
                user_creds = creds_info.credentials
                preset_auth = creds_info.connector_preset_credentials_for_auth

                logger.info(
                    "Credential check",
                    connector_name=slot.connector_name,
                    credentials_name=slot.credentials_name,
                    credential_count=len(user_creds),
                    preset_auth_types=preset_auth,
                )

                # 2. When a specific credentials_name is requested, verify it exists.
                if slot.credentials_name:
                    has_cred = any(c.name == slot.credentials_name for c in user_creds)
                    if not has_cred:
                        logger.warning(
                            "Named credential not found",
                            connector_name=slot.connector_name,
                            credentials_name=slot.credentials_name,
                            available_credentials=[c.name for c in user_creds],
                        )
                        raise ConnectorError(
                            f"Credential '{slot.credentials_name}' not found for connector '{slot.connector_name}'"
                        )

                credentials_verified = False
                # 3. If user has credentials, verify they're still usable via list_tools.
                if user_creds:
                    if slot.allow_mcp_ui:
                        # MCP app discovery already lists tools, so use that
                        # call as the credential usability check and reuse the
                        # discovered URIs below. Raising keeps "auth failed"
                        # distinct from "valid connector with no app tools".
                        try:
                            mcp_ui_resource_uris = await connector_get_mcp_app_resource_uris(
                                resolved.id,
                                credentials_name=slot.credentials_name,
                                raise_on_error=True,
                            )
                            mcp_ui_resource_uris_fetched = True
                            tools_ok = True
                        except Exception:
                            tools_ok = False
                    else:
                        tools_ok = await connector_list_tools(resolved.id, credentials_name=slot.credentials_name)
                    if tools_ok:
                        logger.info(
                            "Credentials verified, skipping auth",
                            connector_name=slot.connector_name,
                            credentials_name=slot.credentials_name,
                            credential_names=[c.name for c in user_creds],
                        )
                        credentials_verified = True
                    else:
                        # Credentials exist but need re-authorization — fall through.
                        logger.warning(
                            "Credentials need re-authorization",
                            connector_name=slot.connector_name,
                            credentials_name=slot.credentials_name,
                            credential_names=[c.name for c in user_creds],
                        )

                if not credentials_verified:
                    # 4. No credentials and no preset — check the connector's
                    #    authentication methods to decide the flow.
                    auth_methods = await connector_get_auth_methods(resolved.id)
                    method_types = {m.method_type for m in auth_methods}
                    if "oauth2" in method_types:
                        logger.info(
                            "Starting OAuth2 auth flow",
                            connector_name=slot.connector_name,
                        )
                        auth_url = await connector_get_auth_url(
                            connector_id_or_name=resolved.id, credentials_name=slot.credentials_name
                        )
                        await _wait_for_connector_auth(slot, resolved.id, auth_url)
                    elif "bearer" in method_types:
                        raise ConnectorError(
                            f"Connector '{slot.connector_name}' requires bearer authentication "
                            f"but no credentials are configured. Create credentials for this "
                            f"connector before running the workflow."
                        )
                    else:
                        logger.info(
                            "No auth needed for connector",
                            connector_name=slot.connector_name,
                            method_types=sorted(method_types),
                        )

            if slot.allow_mcp_ui and slot.auto_auth:
                if not mcp_ui_resource_uris_fetched:
                    mcp_ui_resource_uris = await connector_get_mcp_app_resource_uris(
                        resolved.id,
                        credentials_name=slot.credentials_name,
                    )
                    mcp_ui_resource_uris_fetched = True
                logger.info(
                    "Resolved MCP app resource URIs",
                    connector_name=slot.connector_name,
                    connector_id=resolved.id,
                    tool_names=list(mcp_ui_resource_uris),
                    uri_count=len(mcp_ui_resource_uris),
                )
            elif slot.allow_mcp_ui:
                logger.info(
                    "Skipping MCP app resource URI discovery (auto_auth=False)",
                    connector_name=slot.connector_name,
                    connector_id=resolved.id,
                )

            resolved_bindings.append(
                {
                    "connector_name": slot.connector_name,
                    "connector_id": resolved.id,
                    "credentials_name": slot.credentials_name,
                    "allow_mcp_ui": slot.allow_mcp_ui,
                    "mcp_ui_resource_uris": mcp_ui_resource_uris,
                    "mcp_ui_resource_uris_fetched": mcp_ui_resource_uris_fetched,
                    "status": "ready",
                }
            )

        # Persist resolved bindings into workflow context so downstream code
        # (e.g. RemoteSession) can build CustomConnector objects from them.
        self._store_resolved_bindings(resolved_bindings)

        return await super().execute_workflow(input)

    @staticmethod
    def _store_resolved_bindings(bindings: list[dict[str, Any]]) -> None:
        """Persist resolved connector bindings into the workflow context.

        Merges with any existing extension bindings, preferring the freshly
        resolved ``connector_id`` values.  The updated context is visible to
        all subsequent activities and session code via ``retrieve_context()``.
        """
        ctx = retrieve_context()
        if ctx is None:
            return

        extensions = dict(ctx.extensions or {})
        mistralai_ext = dict(extensions.get(MISTRALAI_PLUGIN_KEY, {}))
        connectors_ext = dict(mistralai_ext.get(CONNECTORS_KEY, {}))

        # Merge: resolved bindings take precedence over existing ones.
        existing = connectors_ext.get("bindings", [])
        by_name = {b["connector_name"]: b for b in existing}
        for binding in bindings:
            by_name[binding["connector_name"]] = binding
        connectors_ext["bindings"] = list(by_name.values())

        mistralai_ext[CONNECTORS_KEY] = connectors_ext
        extensions[MISTRALAI_PLUGIN_KEY] = mistralai_ext

        updated_ctx = ctx.model_copy(update={"extensions": extensions})
        workflow_context_var.set(updated_ctx.model_dump_json())

    @classmethod
    def _get_connector_slots(cls) -> list[ConnectorSlot]:
        """Reconstruct ConnectorSlot objects from the workflow's plugin metadata."""
        workflow_name = temporalio.workflow.info().workflow_type
        metadata = cls._metadata_by_name.get(workflow_name, {})
        raw_defs = metadata.get(MISTRALAI_PLUGIN_KEY, {}).get(CONNECTORS_KEY, [])
        return [
            ConnectorSlot(
                defn.connector_name,
                auto_auth=defn.auto_auth,
                credentials_name=defn.credentials_name,
                allow_mcp_ui=defn.allow_mcp_ui,
            )
            for defn in (ConnectorDefinition.model_validate(d) for d in raw_defs)
        ]


class ConnectorAuthInterceptor(temporalio.worker.Interceptor):
    """Temporal worker interceptor — register this on the Worker to enable connector auth.

    Args:
        workflows: The workflow classes registered on this worker.  The
            interceptor reads ``plugin_metadata`` directly from these classes
            so it doesn't depend on process-global state.
    """

    def __init__(self, workflows: Sequence[Type]) -> None:
        self._metadata_by_name = _build_plugin_metadata_index(workflows)

    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> Type[temporalio.worker.WorkflowInboundInterceptor] | None:
        # Create a subclass that carries this worker's metadata mapping
        metadata = self._metadata_by_name

        class _BoundInterceptor(ConnectorAuthWorkflowInboundInterceptor):
            _metadata_by_name = metadata

        return _BoundInterceptor
