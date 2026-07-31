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
from pydantic import ValidationError

from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition, is_workflow_on_behalf_of
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context, workflow_context_var

from .activities import (
    connector_get_auth_methods,
    connector_get_auth_url,
    connector_list_tools,
    connector_list_user_credentials,
    connector_resolve,
    connector_wait_for_credentials,
)
from .constants import CONNECTORS_KEY, MISTRALAI_PLUGIN_KEY, RESOLVED_CONNECTORS_KEY
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
    MistralaiExtensionPayload,
)
from .run_as import ConnectorRunAs

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
        connector_id=connector_id,
        credentials_name=slot.credentials_name,
        run_as=slot.run_as,
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
    def _extension_bindings() -> list[ConnectorExtensionBinding]:
        """Read connector binding overrides from the workflow context.

        The ``ContextHandlerInterceptor`` (registered on the Temporal client)
        always runs before this worker-level interceptor, so the workflow
        context — including ``extensions`` — is available via
        ``retrieve_context()``.
        """
        ctx = retrieve_context()
        if not ctx or MISTRALAI_PLUGIN_KEY not in ctx.extensions:
            return []
        try:
            payload = MistralaiExtensionPayload.model_validate(ctx.extensions[MISTRALAI_PLUGIN_KEY])
        except ValidationError as exc:
            raise ConnectorError(
                "Malformed runtime connector extension bindings; expected a list of objects with "
                "optional 'connector_name' and 'credentials_name'. Connector identity is "
                "interceptor-owned and must come from @uses_connectors(...)."
            ) from exc
        return payload.connectors.bindings

    @staticmethod
    def _resolve_extension_binding_targets(
        slots: list[ConnectorSlot],
        bindings: list[ConnectorExtensionBinding],
        *,
        workflow_on_behalf_of: bool,
    ) -> list[tuple[ConnectorSlot, ConnectorExtensionBinding]]:
        if not bindings:
            return []
        if not workflow_on_behalf_of:
            raise ConnectorError(
                "Runtime connector credentials_name is only accepted for run_as='auto' connectors "
                "on on_behalf_of=True workflows."
            )

        auto_slots = [slot for slot in slots if slot.run_as == ConnectorRunAs.AUTO]
        auto_slot_by_name = {slot.connector_name: slot for slot in auto_slots}
        if not auto_slot_by_name:
            raise ConnectorError(
                "Runtime connector credentials_name is only accepted when the workflow declares "
                "run_as='auto' connectors."
            )

        connector_name_required = len(auto_slot_by_name) > 1
        targets: list[tuple[ConnectorSlot, ConnectorExtensionBinding]] = []
        bound_connector_names: set[str] = set()
        for binding in bindings:
            connector_name = binding.connector_name
            if connector_name is None:
                if connector_name_required:
                    raise ConnectorError(
                        "Runtime connector credentials_name must include connector_name when the workflow "
                        "declares multiple run_as='auto' connectors."
                    )
                connector_name = next(iter(auto_slot_by_name))

            target_slot = auto_slot_by_name.get(connector_name)
            if target_slot is None:
                raise ConnectorError(
                    "Runtime connector credentials_name can only target declared run_as='auto' connectors. "
                    f"Received {connector_name!r}; declared auto connectors: {sorted(auto_slot_by_name)}."
                )
            if connector_name in bound_connector_names:
                raise ConnectorError(
                    f"Runtime connector credentials_name includes duplicate binding for connector {connector_name!r}."
                )
            bound_connector_names.add(connector_name)
            targets.append((target_slot, binding))

        return targets

    @staticmethod
    def _apply_extension_bindings(
        slots: list[ConnectorSlot],
        bindings: list[ConnectorExtensionBinding],
        *,
        workflow_on_behalf_of: bool,
    ) -> None:
        """Overlay runtime extension bindings onto the static connector slots.

        Runtime connector names are selectors only: each binding must target a
        statically declared ``run_as='auto'`` connector slot.
        """
        targets = ConnectorAuthWorkflowInboundInterceptor._resolve_extension_binding_targets(
            slots,
            bindings,
            workflow_on_behalf_of=workflow_on_behalf_of,
        )
        for slot, binding in targets:
            if binding.credentials_name is not None:
                slot.credentials_name = binding.credentials_name

    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> Any:
        slots = self._get_connector_slots()
        if not slots:
            return await super().execute_workflow(input)

        workflow_on_behalf_of = is_workflow_on_behalf_of(temporalio.workflow.info().workflow_type)
        ext_bindings = self._extension_bindings()

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
        if ext_bindings:
            logger.info(
                "Applying runtime extension bindings",
                bindings=[
                    {
                        "connector_name": b.connector_name,
                        "credentials_name": b.credentials_name,
                    }
                    for b in ext_bindings
                ],
            )
            self._apply_extension_bindings(
                slots,
                ext_bindings,
                workflow_on_behalf_of=workflow_on_behalf_of,
            )

        # Resolve all connectors and run auth preflight for auto_auth ones.
        resolved_bindings: list[dict[str, Any]] = []
        for slot in slots:
            run_as = slot.run_as
            # Resolve every connector to get its connector_id.
            logger.info(
                "Resolving connector",
                connector_name=slot.connector_name,
                credentials_name=slot.credentials_name,
                run_as=run_as,
            )
            resolved = await connector_resolve(slot.connector_name, run_as=run_as)
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
                creds_info = await connector_list_user_credentials(resolved.id, run_as=run_as)
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
                                run_as=run_as,
                            )
                            mcp_ui_resource_uris_fetched = True
                            tools_ok = True
                        except Exception:
                            tools_ok = False
                    else:
                        tools_ok = await connector_list_tools(
                            resolved.id, credentials_name=slot.credentials_name, run_as=run_as
                        )
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
                    auth_methods = await connector_get_auth_methods(resolved.id, run_as=run_as)
                    method_types = {m.method_type for m in auth_methods}
                    if "oauth2" in method_types:
                        if slot.run_as == ConnectorRunAs.DEPLOYMENT:
                            raise ConnectorError(
                                f"Connector '{slot.connector_name}' runs with run_as='deployment' "
                                f"and requires OAuth2 authorization, but deployment-identity connectors "
                                f"cannot complete an interactive OAuth flow. Configure the deployment's "
                                f"credentials for this connector before running the workflow."
                            )
                        logger.info(
                            "Starting OAuth2 auth flow",
                            connector_name=slot.connector_name,
                        )
                        auth_url = await connector_get_auth_url(
                            connector_id_or_name=resolved.id,
                            credentials_name=slot.credentials_name,
                            run_as=run_as,
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
                        run_as=run_as,
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
                    "run_as": slot.run_as.value,
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
        """Persist resolved connector bindings into the worker-only context channel.

        Written to ``trusted_extensions`` — a channel the caller cannot populate — so
        downstream readers (``ToolCallClient``, ``RemoteSession``) can trust the bindings
        as interceptor-owned without any forgery check. Preflight re-runs on every
        execution (including continue-as-new), so this channel is regenerated each run.
        """
        ctx = retrieve_context()
        if ctx is None:
            return

        trusted_extensions = dict(ctx.trusted_extensions or {})
        mistralai_ext = dict(trusted_extensions.get(MISTRALAI_PLUGIN_KEY, {}))

        mistralai_ext[RESOLVED_CONNECTORS_KEY] = {"bindings": bindings}
        trusted_extensions[MISTRALAI_PLUGIN_KEY] = mistralai_ext

        updated_ctx = ctx.model_copy(update={"trusted_extensions": trusted_extensions})
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
                run_as=defn.run_as.value,
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
