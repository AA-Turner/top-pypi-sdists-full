"""Demo-only sample data adapter for connector pinning."""

from __future__ import annotations

from dataclasses import asdict

from airbyte_ops_webapp.models import (
    ConnectorOption,
    ConnectorVersion,
    CurrentVersionState,
    OperationResult,
    OverridePlan,
    ScopedConfiguration,
    ScopeType,
    build_version_override_payload,
    version_override_tool_name,
)
from airbyte_ops_webapp.services.connector_version_manager.adapter import OpsMcpAdapter

SCOPE_PRIORITY: dict[ScopeType, int] = {
    "organization": 0,
    "workspace": 1,
    "actor": 2,
}

MOCK_CONNECTORS: tuple[ConnectorOption, ...] = (
    ConnectorOption(
        id="b5ea17b1-f170-46dc-bc31-cc744ca984c1",
        name="source-postgres",
        connector_type="source",
        latest_version="3.7.2",
        docker_repository="airbyte/source-postgres",
    ),
    ConnectorOption(
        id="ef69ef6e-aa7f-4af1-a01d-ef775033524e",
        name="source-github",
        connector_type="source",
        latest_version="1.9.4",
        docker_repository="airbyte/source-github",
    ),
    ConnectorOption(
        id="25c5221d-dce2-4163-ade9-739ef790f503",
        name="destination-snowflake",
        connector_type="destination",
        latest_version="3.3.1",
        docker_repository="airbyte/destination-snowflake",
    ),
)

MOCK_VERSIONS: dict[str, tuple[ConnectorVersion, ...]] = {
    "b5ea17b1-f170-46dc-bc31-cc744ca984c1": (
        ConnectorVersion(
            version_id="adv_postgres_372",
            docker_image_tag="3.7.2",
            docker_repository="airbyte/source-postgres",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.48.3",
            language="python",
            last_published="2026-04-21T18:21:00Z",
        ),
        ConnectorVersion(
            version_id="adv_postgres_371",
            docker_image_tag="3.7.1",
            docker_repository="airbyte/source-postgres",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.47.0",
            language="python",
            last_published="2026-04-07T15:03:00Z",
        ),
        ConnectorVersion(
            version_id="adv_postgres_360",
            docker_image_tag="3.6.0",
            docker_repository="airbyte/source-postgres",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.42.0",
            language="python",
            last_published="2026-03-11T09:40:00Z",
        ),
    ),
    "ef69ef6e-aa7f-4af1-a01d-ef775033524e": (
        ConnectorVersion(
            version_id="adv_github_194",
            docker_image_tag="1.9.4",
            docker_repository="airbyte/source-github",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.44.1",
            language="python",
            last_published="2026-04-26T14:12:00Z",
        ),
        ConnectorVersion(
            version_id="adv_github_187",
            docker_image_tag="1.8.7",
            docker_repository="airbyte/source-github",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.38.2",
            language="python",
            last_published="2026-02-18T20:15:00Z",
        ),
    ),
    "25c5221d-dce2-4163-ade9-739ef790f503": (
        ConnectorVersion(
            version_id="adv_snowflake_331",
            docker_image_tag="3.3.1",
            docker_repository="airbyte/destination-snowflake",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.41.0",
            language="python",
            last_published="2026-04-15T12:08:00Z",
        ),
    ),
}

MOCK_CONFIGURATIONS: tuple[ScopedConfiguration, ...] = (
    ScopedConfiguration(
        id="scoped_workspace_pin",
        connector_id="b5ea17b1-f170-46dc-bc31-cc744ca984c1",
        connector_name="source-postgres",
        connector_type="source",
        scope_type="workspace",
        scope_id="workspace_example",
        scope_name="Example Workspace",
        value_name="3.6.0",
        description="Workspace pinned during regression investigation",
        origin_type="user",
        origin_name="ops@example.com",
        expires_at="2026-05-15T00:00:00Z",
        reference_url="https://github.com/airbytehq/airbyte/issues/0000",
    ),
    ScopedConfiguration(
        id="scoped_actor_pin",
        connector_id="b5ea17b1-f170-46dc-bc31-cc744ca984c1",
        connector_name="source-postgres",
        connector_type="source",
        scope_type="actor",
        scope_id="actor_example",
        scope_name="Example Postgres Source",
        value_name="3.7.1",
        description="Actor-level canary pin",
        origin_type="user",
        origin_name="ops@example.com",
        expires_at="2026-05-20T00:00:00Z",
        reference_url="https://github.com/airbytehq/airbyte/issues/1111",
    ),
    ScopedConfiguration(
        id="scoped_org_pin",
        connector_id="ef69ef6e-aa7f-4af1-a01d-ef775033524e",
        connector_name="source-github",
        connector_type="source",
        scope_type="organization",
        scope_id="org_example",
        scope_name="Example Org",
        value_name="1.8.7",
        description="Organization-level temporary pin",
        origin_type="user",
        origin_name="ops@example.com",
        expires_at="2026-05-30T00:00:00Z",
        reference_url="https://github.com/airbytehq/airbyte/issues/2222",
    ),
)


class MockPinningAdapter(OpsMcpAdapter):
    """In-memory data source for demos and tests."""

    mode = "mock"

    def __init__(self) -> None:
        super().__init__()
        self.bearer_token = None
        self.config_api_root = "mock://config-api"
        self.connectors = MOCK_CONNECTORS
        self.versions = MOCK_VERSIONS
        self.configurations = MOCK_CONFIGURATIONS

    def search_connectors(self, query: str) -> tuple[ConnectorOption, ...]:
        """Search connectors by name, ID, or Docker repository."""
        return self.list_connectors(query)

    def list_connectors(self, query: str = "") -> tuple[ConnectorOption, ...]:
        """List connectors by name, ID, or Docker repository."""
        normalized_query = query.strip().lower()
        if not normalized_query:
            return self.connectors
        return tuple(
            connector
            for connector in self.connectors
            if normalized_query in connector.name.lower()
            or normalized_query in connector.id.lower()
            or normalized_query in connector.docker_repository.lower()
        )

    def get_connector(self, connector_id: str) -> ConnectorOption:
        """Return a connector by ID."""
        for connector in self.connectors:
            if connector.id == connector_id:
                return connector
        raise ValueError(f"Unknown connector ID: {connector_id}")

    def list_versions(self, connector_id: str) -> tuple[ConnectorVersion, ...]:
        """List published versions for a connector."""
        return self.versions.get(connector_id, ())

    def get_current_context(
        self,
        *,
        connector_id: str,
        scope_type: ScopeType,
        scope_id: str,
    ) -> CurrentVersionState:
        """Return mocked scope context for selected connector and scope."""
        connector = self.get_connector(connector_id)
        matching_configs = tuple(
            config
            for config in self.configurations
            if config.connector_id == connector_id
        )
        active_config = self._active_config(matching_configs, scope_type, scope_id)
        active_version = (
            active_config.value_name if active_config else connector.latest_version
        )
        return CurrentVersionState(
            connector_id=connector.id,
            connector_name=connector.name,
            connector_type=connector.connector_type,
            latest_version=connector.latest_version,
            active_version=active_version,
            is_version_pinned=active_config is not None,
            active_scope=active_config.scope_type if active_config else None,
            active_scope_id=active_config.scope_id if active_config else None,
            ancestor_configurations=tuple(
                config
                for config in matching_configs
                if SCOPE_PRIORITY[config.scope_type] < SCOPE_PRIORITY[scope_type]
            ),
            descendant_configurations=tuple(
                config
                for config in matching_configs
                if SCOPE_PRIORITY[config.scope_type] > SCOPE_PRIORITY[scope_type]
            ),
        )

    def summary_by_connector(self) -> tuple[dict[str, str | int], ...]:
        """Summarize user-originated overrides by connector."""
        summary: dict[str, dict[str, str | int | set[str]]] = {}
        for config in self.configurations:
            connector_summary = summary.setdefault(
                config.connector_id,
                {
                    "id": config.connector_id,
                    "connector": config.connector_name,
                    "connector_type": config.connector_type,
                    "versions": set(),
                    "version_count": 0,
                    "override_count": 0,
                },
            )
            versions = connector_summary["versions"]
            assert isinstance(versions, set)
            versions.add(config.value_name)
            override_count = connector_summary["override_count"]
            assert isinstance(override_count, int)
            connector_summary["override_count"] = override_count + 1

        rows: list[dict[str, str | int]] = []
        for values in summary.values():
            versions = values["versions"]
            assert isinstance(versions, set)
            override_count = values["override_count"]
            assert isinstance(override_count, int)
            rows.append(
                {
                    "id": str(values["id"]),
                    "connector": str(values["connector"]),
                    "connector_type": str(values["connector_type"]),
                    "versions": ", ".join(sorted(versions)),
                    "version_count": len(versions),
                    "override_count": override_count,
                }
            )
        return tuple(rows)

    def configuration_rows(self) -> tuple[dict[str, str], ...]:
        """Return override rows for display tables."""
        return tuple(asdict(config) for config in self.configurations)

    def resolve_organization_id(self, scope_type: ScopeType, scope_id: str) -> str:
        """Return a demo organization ID for the selected target scope."""
        if scope_type == "organization":
            return scope_id
        return "org_example"

    def apply_override(self, plan: OverridePlan) -> OperationResult:
        """Apply the override flow without calling Airbyte Cloud."""
        version_label = (
            "cleared" if plan.action == "unset" else f"set to {plan.version}"
        )
        return OperationResult(
            tool_name=version_override_tool_name(plan.scope_type),
            success=True,
            mutating=False,
            mode=self.mode,
            message=(
                "Mock mode completed the apply flow with no Airbyte Cloud change. "
                f"{plan.scope_type.title()} override for {plan.connector_name} "
                f"would be {version_label}."
            ),
            payload=build_version_override_payload(plan),
        )
