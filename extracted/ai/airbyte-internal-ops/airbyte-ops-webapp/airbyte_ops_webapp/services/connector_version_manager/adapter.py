"""Adapters for connector version pinning workflows."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import asdict

from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError
from airbyte_ops_mcp.cloud_admin import api_client
from airbyte_ops_mcp.cloud_admin.registry_lookup import (
    _fetch_cloud_registry,
    resolve_canonical_name_to_definition_id,
    resolve_definition_id_to_canonical_info,
)
from airbyte_ops_mcp.cloud_admin.version_overrides import (
    ResolvedCloudAuth,
    VersionOverrideTarget,
    set_version_override,
)
from airbyte_ops_mcp.prod_db_access.queries import query_connector_versions
from airbyte_ops_mcp.tier_cache import resolve_workspace

from airbyte_ops_webapp.models import (
    ConnectorOption,
    ConnectorType,
    ConnectorVersion,
    CurrentVersionState,
    OperationPreview,
    OperationResult,
    OverridePlan,
    ScopedConfiguration,
    ScopeType,
    build_version_override_payload,
    version_override_tool_name,
)

__all__ = [
    "OpsMcpAdapter",
    "configuration_rows",
    "operation_result_to_json",
    "preview_to_json",
]

SCOPE_PRIORITY: dict[ScopeType, int] = {
    "organization": 0,
    "workspace": 1,
    "actor": 2,
}
REQUIRED_APPROVAL_FIELDS: tuple[str, ...] = (
    "override_reason",
    "override_reason_reference_url",
    "approval_comment_url",
    "customer_tier_filter",
)
SAFE_PREVIEW_WARNINGS: tuple[str, ...] = (
    "Preview only: no connector version override has been executed.",
    "TIER_0 and TIER_1 customers require human escalation before action.",
)


class OpsMcpAdapter:
    """Adapter backed by `airbyte-internal-ops` APIs."""

    mode = "real"

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        config_api_root: str = constants.CLOUD_CONFIG_API_ROOT,
    ) -> None:
        self.bearer_token = bearer_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.config_api_root = config_api_root

    def search_connectors(self, query: str) -> tuple[ConnectorOption, ...]:
        """Resolve a connector name or definition ID into connector options."""
        normalized_query = query.strip()
        if not normalized_query:
            return self.list_connectors()

        connectors: list[ConnectorOption] = []
        connector_by_id = self._connector_from_definition_id(normalized_query)
        if connector_by_id:
            connectors.append(connector_by_id)

        connector_by_name = self._connector_from_name(normalized_query)
        if connector_by_name and connector_by_name not in connectors:
            connectors.append(connector_by_name)

        if connectors:
            return tuple(connectors)

        return self.list_connectors(normalized_query)

    def list_connectors(self, query: str = "") -> tuple[ConnectorOption, ...]:
        """List Cloud registry connectors, optionally filtered by `query`."""
        if self._is_local_config_api:
            return self._list_local_connectors(query)
        data = _fetch_cloud_registry()
        connectors = [
            *(
                self._connector_from_registry_entry(source, "source")
                for source in data.get("sources", [])
                if isinstance(source, Mapping)
            ),
            *(
                self._connector_from_registry_entry(destination, "destination")
                for destination in data.get("destinations", [])
                if isinstance(destination, Mapping)
            ),
        ]
        normalized_query = query.strip().lower()
        if not normalized_query:
            return tuple(sorted(connectors, key=lambda connector: connector.name))
        return tuple(
            connector
            for connector in sorted(connectors, key=lambda connector: connector.name)
            if normalized_query in connector.name.lower()
            or normalized_query in connector.id.lower()
            or normalized_query in connector.docker_repository.lower()
        )

    def get_connector(self, connector_id: str) -> ConnectorOption:
        """Return a connector by definition ID."""
        if self._is_local_config_api:
            for connector in self.list_connectors():
                if connector.id == connector_id:
                    return connector
        connector = self._connector_from_definition_id(connector_id)
        if connector:
            return connector
        raise ValueError(f"Unknown connector ID: {connector_id}")

    def list_versions(self, connector_id: str) -> tuple[ConnectorVersion, ...]:
        """List published versions for a connector definition."""
        if self._is_local_config_api:
            connector = self.get_connector(connector_id)
            return (
                ConnectorVersion(
                    version_id=api_client.resolve_connector_version_id(
                        actor_definition_id=connector.id,
                        connector_type=connector.connector_type,
                        version=connector.latest_version,
                        config_api_root=self.config_api_root,
                        client_id=self.client_id,
                        client_secret=self.client_secret,
                        bearer_token=self.bearer_token,
                    ),
                    docker_image_tag=connector.latest_version,
                    docker_repository=connector.docker_repository,
                    release_stage="",
                    support_level="",
                    cdk_version="",
                    language="",
                    last_published="",
                ),
            )
        return tuple(
            self._version_from_row(row)
            for row in query_connector_versions(connector_definition_id=connector_id)
        )

    def get_current_context(
        self,
        *,
        connector_id: str,
        scope_type: ScopeType,
        scope_id: str,
        workspace_id: str | None = None,
    ) -> CurrentVersionState:
        """Return current version context for a selected scope."""
        connector = self.get_connector(connector_id)
        versions = self.list_versions(connector_id)
        latest_version = (
            versions[0].docker_image_tag if versions else connector.latest_version
        )
        if scope_type in ("workspace", "organization"):
            scoped_configs = self._scope_context(connector, scope_type, scope_id)
            active_config = self._active_config(scoped_configs, scope_type, scope_id)
            return CurrentVersionState(
                connector_id=connector.id,
                connector_name=connector.name,
                connector_type=connector.connector_type,
                latest_version=latest_version,
                active_version=active_config.value_name
                if active_config
                else latest_version,
                is_version_pinned=active_config is not None,
                active_scope=active_config.scope_type if active_config else None,
                active_scope_id=active_config.scope_id if active_config else None,
                ancestor_configurations=tuple(
                    config
                    for config in scoped_configs
                    if SCOPE_PRIORITY[config.scope_type] < SCOPE_PRIORITY[scope_type]
                ),
                descendant_configurations=tuple(
                    config
                    for config in scoped_configs
                    if SCOPE_PRIORITY[config.scope_type] > SCOPE_PRIORITY[scope_type]
                ),
            )
        if scope_type != "actor":
            return CurrentVersionState(
                connector_id=connector.id,
                connector_name=connector.name,
                connector_type=connector.connector_type,
                latest_version=latest_version,
                active_version=latest_version,
                is_version_pinned=False,
                active_scope=None,
                active_scope_id=None,
                ancestor_configurations=(),
                descendant_configurations=(),
            )

        version_data = api_client.get_connector_version(
            connector_id=scope_id,
            connector_type=connector.connector_type,
            config_api_root=self.config_api_root,
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
            workspace_id=workspace_id,
        )
        active_version = (
            self._string_field(version_data, "dockerImageTag") or latest_version
        )
        scoped_configs = self._scoped_configurations(
            connector=connector,
            scoped_configs=version_data.get("scopedConfigs"),
        )
        active_config = self._active_config(scoped_configs, scope_type, scope_id)
        return CurrentVersionState(
            connector_id=connector.id,
            connector_name=connector.name,
            connector_type=connector.connector_type,
            latest_version=latest_version,
            active_version=active_version,
            is_version_pinned=active_config is not None
            or bool(version_data.get("isVersionOverrideApplied")),
            active_scope=active_config.scope_type if active_config else None,
            active_scope_id=active_config.scope_id if active_config else None,
            ancestor_configurations=tuple(
                config
                for config in scoped_configs
                if SCOPE_PRIORITY[config.scope_type] < SCOPE_PRIORITY[scope_type]
            ),
            descendant_configurations=tuple(
                config
                for config in scoped_configs
                if SCOPE_PRIORITY[config.scope_type] > SCOPE_PRIORITY[scope_type]
            ),
        )

    def summary_by_connector(self) -> tuple[dict[str, str | int], ...]:
        """Return override summary rows when available."""
        return ()

    def configuration_rows(self) -> tuple[dict[str, str], ...]:
        """Return scoped override rows when available."""
        return ()

    def list_instance_admin_users(self) -> tuple[dict[str, str], ...]:
        """Return Config API instance-admin users for interactive apply identity."""
        return api_client.list_instance_admin_users(
            config_api_root=self.config_api_root,
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
        )

    def stage_override(self, plan: OverridePlan) -> OperationPreview:
        """Build a non-mutating preview for the matching Ops MCP tool."""
        return OperationPreview(
            tool_name=version_override_tool_name(plan.scope_type),
            mutating=False,
            mode=self.mode,
            payload=build_version_override_payload(plan),
            required_approval_fields=REQUIRED_APPROVAL_FIELDS,
            warnings=SAFE_PREVIEW_WARNINGS,
        )

    def apply_override(self, plan: OverridePlan) -> OperationResult:
        """Apply the matching version override operation."""
        auth = ResolvedCloudAuth(
            bearer_token=self.bearer_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        payload = build_version_override_payload(plan)
        target = self._target_from_plan(plan)
        result = set_version_override(
            auth=auth,
            target=target,
            approval_comment_url=payload.approval_comment_url,
            version=payload.version,
            unset=payload.unset,
            override_reason=payload.override_reason,
            override_reason_reference_url=payload.override_reason_reference_url,
            issue_url=payload.override_reason_reference_url,
            ai_agent_session_url=payload.ai_agent_session_url,
            customer_tier_filter=payload.customer_tier_filter,
            force=payload.force,
            config_api_root=self.config_api_root,
        )

        return OperationResult(
            tool_name=version_override_tool_name(plan.scope_type),
            success=result.success,
            mutating=True,
            mode=self.mode,
            message=result.message,
            payload=payload,
        )

    @property
    def _is_local_config_api(self) -> bool:
        return self.config_api_root.startswith("http://localhost:")

    def _list_local_connectors(self, query: str = "") -> tuple[ConnectorOption, ...]:
        connectors = [
            *self._local_definition_options("source"),
            *self._local_definition_options("destination"),
        ]
        normalized_query = query.strip().lower()
        if not normalized_query:
            return tuple(sorted(connectors, key=lambda connector: connector.name))
        return tuple(
            connector
            for connector in sorted(connectors, key=lambda connector: connector.name)
            if normalized_query in connector.name.lower()
            or normalized_query in connector.id.lower()
            or normalized_query in connector.docker_repository.lower()
        )

    def _local_definition_options(
        self,
        connector_type: ConnectorType,
    ) -> tuple[ConnectorOption, ...]:
        endpoint_name = (
            "source_definitions/list_latest"
            if connector_type == "source"
            else "destination_definitions/list_latest"
        )
        access_token = api_client._get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
            config_api_root=self.config_api_root,
        )
        response = api_client.requests.post(
            f"{self.config_api_root}/{endpoint_name}",
            json={},
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": api_client.ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        if response.status_code != 200:
            raise PyAirbyteInputError(
                message=(
                    f"Failed to list local {connector_type} definitions: "
                    f"{response.status_code} {response.text}"
                ),
                context={"endpoint": f"{self.config_api_root}/{endpoint_name}"},
            )
        key = (
            "sourceDefinitions"
            if connector_type == "source"
            else "destinationDefinitions"
        )
        return tuple(
            self._connector_from_registry_entry(definition, connector_type)
            for definition in response.json().get(key, [])
            if isinstance(definition, Mapping)
        )

    def _scope_context(
        self,
        connector: ConnectorOption,
        scope_type: ScopeType,
        scope_id: str,
    ) -> tuple[ScopedConfiguration, ...]:
        access_token = api_client._get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
            config_api_root=self.config_api_root,
        )
        active_config = api_client._get_scoped_configuration_context(
            actor_definition_id=connector.id,
            scope_type=api_client._ScopeType(scope_type),
            scope_id=scope_id,
            config_api_root=self.config_api_root,
            access_token=access_token,
        )
        if not active_config:
            return ()
        return self._scoped_configurations(
            connector=connector,
            scoped_configs={scope_type: active_config},
        )

    def _target_from_plan(self, plan: OverridePlan) -> VersionOverrideTarget:
        if plan.scope_type == "actor":
            return VersionOverrideTarget(
                scope="actor",
                organization_id=plan.organization_id,
                connector_type=plan.connector_type,
                workspace_id=plan.workspace_id,
                actor_id=plan.actor_id,
            )
        if plan.scope_type == "workspace":
            return VersionOverrideTarget(
                scope="workspace",
                organization_id=plan.organization_id,
                connector_type=plan.connector_type,
                workspace_id=plan.workspace_id,
                connector_name=plan.connector_name,
            )
        return VersionOverrideTarget(
            scope="organization",
            organization_id=plan.organization_id,
            connector_type=plan.connector_type,
            connector_name=plan.connector_name,
        )

    def resolve_organization_id(self, scope_type: ScopeType, scope_id: str) -> str:
        """Return the organization ID for the selected target scope."""
        if scope_type == "organization":
            return scope_id
        if scope_type == "actor":
            return ""
        return resolve_workspace(scope_id).organization_id or ""

    @staticmethod
    def _version_from_row(row: Mapping[str, object]) -> ConnectorVersion:
        return ConnectorVersion(
            version_id=OpsMcpAdapter._string_field(row, "version_id"),
            docker_image_tag=OpsMcpAdapter._string_field(row, "docker_image_tag"),
            docker_repository=OpsMcpAdapter._string_field(row, "docker_repository"),
            release_stage=OpsMcpAdapter._string_field(row, "release_stage"),
            support_level=OpsMcpAdapter._string_field(row, "support_level"),
            cdk_version=OpsMcpAdapter._string_field(row, "cdk_version"),
            language=OpsMcpAdapter._string_field(row, "language"),
            last_published=OpsMcpAdapter._string_field(row, "last_published"),
        )

    @staticmethod
    def _scoped_configurations(
        *,
        connector: ConnectorOption,
        scoped_configs: object,
    ) -> tuple[ScopedConfiguration, ...]:
        if not isinstance(scoped_configs, Mapping):
            return ()

        configs: list[ScopedConfiguration] = []
        for scope_type, config in scoped_configs.items():
            if scope_type in SCOPE_PRIORITY and isinstance(config, Mapping):
                configs.append(
                    ScopedConfiguration(
                        id=OpsMcpAdapter._string_field(config, "id"),
                        connector_id=connector.id,
                        connector_name=connector.name,
                        connector_type=connector.connector_type,
                        scope_type=scope_type,
                        scope_id=OpsMcpAdapter._string_field(config, "scope_id"),
                        scope_name=OpsMcpAdapter._string_field(config, "scope_name"),
                        value_name=OpsMcpAdapter._string_field(config, "value_name"),
                        description=OpsMcpAdapter._string_field(config, "description"),
                        origin_type=OpsMcpAdapter._string_field(config, "origin_type"),
                        origin_name=OpsMcpAdapter._string_field(config, "origin_name"),
                        expires_at=OpsMcpAdapter._string_field(config, "expires_at"),
                        reference_url=OpsMcpAdapter._string_field(
                            config, "reference_url"
                        ),
                    )
                )
        return tuple(configs)

    @staticmethod
    def _active_config(
        configurations: tuple[ScopedConfiguration, ...],
        scope_type: ScopeType,
        scope_id: str,
    ) -> ScopedConfiguration | None:
        scoped = tuple(
            config
            for config in configurations
            if config.scope_type == scope_type and config.scope_id == scope_id
        )
        if scoped:
            return scoped[0]
        inherited = tuple(
            config
            for config in configurations
            if SCOPE_PRIORITY[config.scope_type] < SCOPE_PRIORITY[scope_type]
        )
        if not inherited:
            return None
        return max(inherited, key=lambda config: SCOPE_PRIORITY[config.scope_type])

    @staticmethod
    def _string_field(row: Mapping[str, object], field_name: str) -> str:
        value = row.get(field_name)
        if value is None:
            return ""
        return str(value)

    @staticmethod
    def _connector_from_registry_entry(
        entry: Mapping[str, object],
        connector_type: ConnectorType,
    ) -> ConnectorOption:
        definition_id_field = (
            "sourceDefinitionId"
            if connector_type == "source"
            else "destinationDefinitionId"
        )
        raw_name = OpsMcpAdapter._string_field(entry, "name")
        docker_repository = OpsMcpAdapter._string_field(entry, "dockerRepository")
        canonical_name = docker_repository.rsplit("/", maxsplit=1)[-1] or raw_name
        return ConnectorOption(
            id=OpsMcpAdapter._string_field(entry, definition_id_field),
            name=canonical_name,
            connector_type=connector_type,
            latest_version=OpsMcpAdapter._string_field(entry, "dockerImageTag"),
            docker_repository=docker_repository,
        )

    def _connector_from_definition_id(
        self,
        actor_definition_id: str,
    ) -> ConnectorOption | None:
        try:
            connector_name, connector_type = resolve_definition_id_to_canonical_info(
                actor_definition_id
            )
        except PyAirbyteInputError:
            return None
        typed_connector_type: ConnectorType = (
            "destination" if connector_type == "destination" else "source"
        )
        versions = self.list_versions(actor_definition_id)
        latest_version = versions[0].docker_image_tag if versions else ""
        docker_repository = versions[0].docker_repository if versions else ""
        return ConnectorOption(
            id=actor_definition_id,
            name=connector_name,
            connector_type=typed_connector_type,
            latest_version=latest_version,
            docker_repository=docker_repository,
        )

    def _connector_from_name(self, connector_name: str) -> ConnectorOption | None:
        try:
            actor_definition_id = resolve_canonical_name_to_definition_id(
                connector_name
            )
        except PyAirbyteInputError:
            return None
        return self._connector_from_definition_id(actor_definition_id)


def preview_to_json(preview: OperationPreview) -> str:
    """Serialize an operation preview for display."""
    return json.dumps(
        {
            "tool_name": preview.tool_name,
            "mutating": preview.mutating,
            "payload": preview.payload.model_dump(mode="json"),
            "required_approval_fields": preview.required_approval_fields,
            "warnings": preview.warnings,
        },
        indent=2,
        sort_keys=True,
    )


def operation_result_to_json(result: OperationResult) -> str:
    """Serialize an operation result for display."""
    return json.dumps(
        {
            "tool_name": result.tool_name,
            "success": result.success,
            "mutating": result.mutating,
            "mode": result.mode,
            "message": result.message,
            "payload": result.payload.model_dump(mode="json"),
        },
        indent=2,
        sort_keys=True,
    )


def configuration_rows(
    configurations: tuple[ScopedConfiguration, ...],
) -> tuple[dict[str, str], ...]:
    """Return override rows for display tables."""
    return tuple(asdict(config) for config in configurations)
