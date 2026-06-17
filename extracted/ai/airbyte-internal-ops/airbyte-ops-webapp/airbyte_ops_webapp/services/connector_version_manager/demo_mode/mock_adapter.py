"""Demo-only sample data adapter for connector pinning."""

from __future__ import annotations

from dataclasses import asdict

from airbyte_ops_webapp.models import (
    ConnectorOption,
    ConnectorRelease,
    ConnectorRollout,
    ConnectorVersion,
    ContextResolution,
    CurrentVersionState,
    OperationResult,
    OverridePlan,
    ScopedConfiguration,
    ScopeType,
    VersionPinRow,
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
        ConnectorVersion(
            version_id="adv_github_183",
            docker_image_tag="1.8.3",
            docker_repository="airbyte/source-github",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.35.0",
            language="python",
            last_published="2026-01-29T16:42:00Z",
        ),
        ConnectorVersion(
            version_id="adv_github_174",
            docker_image_tag="1.7.4",
            docker_repository="airbyte/source-github",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.29.1",
            language="python",
            last_published="2025-12-19T13:05:00Z",
        ),
        ConnectorVersion(
            version_id="adv_github_169",
            docker_image_tag="1.6.9",
            docker_repository="airbyte/source-github",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.22.0",
            language="python",
            last_published="2025-11-07T18:33:00Z",
        ),
        ConnectorVersion(
            version_id="adv_github_158",
            docker_image_tag="1.5.8",
            docker_repository="airbyte/source-github",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.18.2",
            language="python",
            last_published="2025-10-02T09:18:00Z",
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

MOCK_VERSION_PINS: dict[str, tuple[VersionPinRow, ...]] = {
    "adv_postgres_371": (
        VersionPinRow(
            scope_type="workspace",
            scope_id="ws_abc123-def456",
            scope_url="https://cloud.airbyte.com/workspaces/ws_abc123-def456",
            origin_type="user",
            origin_name="admin@airbyte.io",
            description="Workspace pinned during regression investigation",
            created_at="2026-04-10T14:30:00Z",
            created_at_display="2026-04-10 (Thu)",
            expires_at="2026-05-15T00:00:00Z",
            expires_at_display="2026-05-15 (Thu)",
            reference_url="https://github.com/airbytehq/airbyte/issues/0000",
        ),
        VersionPinRow(
            scope_type="organization",
            scope_id="org_789012-abcdef",
            scope_url="https://cloud.airbyte.com/organizations/org_789012-abcdef/settings",
            origin_type="user",
            origin_name="ops@airbyte.io",
            description="Org-level temporary pin for customer regression",
            created_at="2026-04-08T10:00:00Z",
            created_at_display="2026-04-08 (Tue)",
            expires_at="2026-05-20T00:00:00Z",
            expires_at_display="2026-05-20 (Tue)",
            reference_url="https://github.com/airbytehq/airbyte/issues/1111",
        ),
        VersionPinRow(
            scope_type="actor",
            scope_id="act_fedcba-987654",
            scope_url="https://cloud.airbyte.com/workspaces",
            origin_type="user",
            origin_name="support@airbyte.io",
            description="Actor canary pin",
            created_at="2026-04-12T09:15:00Z",
            created_at_display="2026-04-12 (Sat)",
            expires_at="",
            expires_at_display="",
            reference_url="",
        ),
    ),
    "adv_github_187": (
        VersionPinRow(
            scope_type="organization",
            scope_id="org_example",
            scope_url="https://cloud.airbyte.com/organizations/org_example/settings",
            origin_type="user",
            origin_name="ops@example.com",
            description="Organization-level temporary pin",
            created_at="2026-03-01T12:00:00Z",
            created_at_display="2026-03-01 (Sat)",
            expires_at="2026-05-30T00:00:00Z",
            expires_at_display="2026-05-30 (Fri)",
            reference_url="https://github.com/airbytehq/airbyte/issues/2222",
        ),
    ),
}

MOCK_ROLLOUTS: dict[str, tuple[ConnectorRollout, ...]] = {
    "b5ea17b1-f170-46dc-bc31-cc744ca984c1": (
        ConnectorRollout(
            rollout_id="mock-postgres-rollout",
            connector_id="b5ea17b1-f170-46dc-bc31-cc744ca984c1",
            connector_name="source-postgres",
            connector_type="source",
            docker_repository="airbyte/source-postgres",
            state="initialized",
            rc_docker_image_tag="3.8.0-rc.12",
            initial_docker_image_tag="3.7.2",
            current_target_rollout_pct="50",
            final_target_rollout_pct="50",
            created_at="2026-04-28T11:00:00Z",
            updated_at="2026-04-28T12:00:00Z",
        ),
    ),
}


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
        self.rollouts = MOCK_ROLLOUTS
        self.version_pins = MOCK_VERSION_PINS

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

    def list_recent_releases(
        self,
        *,
        days: int = 30,
        limit: int | None = None,
    ) -> tuple[ConnectorRelease, ...]:
        """List recent mock releases across connectors."""
        releases: list[ConnectorRelease] = []
        for connector in self.connectors:
            for version in self.versions.get(connector.id, ()):
                releases.append(
                    ConnectorRelease(
                        version_id=version.version_id,
                        connector_id=connector.id,
                        connector_name=connector.name,
                        connector_type=connector.connector_type,
                        docker_image_tag=version.docker_image_tag,
                        docker_repository=version.docker_repository,
                        release_stage=version.release_stage,
                        last_published=version.last_published,
                    )
                )
        sorted_releases = sorted(
            releases,
            key=lambda release: release.last_published,
            reverse=True,
        )
        return tuple(sorted_releases[:limit] if limit is not None else sorted_releases)

    def list_active_rollouts(
        self,
        connector_id: str,
    ) -> tuple[ConnectorRollout, ...]:
        """List active mock rollouts for a connector."""
        return self.rollouts.get(connector_id, ())

    def list_progressive_rollouts(
        self,
        *,
        limit: int | None = None,
    ) -> tuple[ConnectorRollout, ...]:
        """List active mock rollouts across connectors."""
        rollouts = sorted(
            (
                rollout
                for connector_rollouts in self.rollouts.values()
                for rollout in connector_rollouts
            ),
            key=lambda rollout: rollout.updated_at,
            reverse=True,
        )
        return tuple(rollouts[:limit] if limit is not None else rollouts)

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

    def resolve_context_guid(
        self,
        *,
        connector: ConnectorOption,
        context_guid: str,
    ) -> ContextResolution:
        """Resolve a mock context GUID."""
        if context_guid == "actor_example":
            return ContextResolution(
                scope_type="actor",
                scope_id=context_guid,
                organization_id="org_example",
                workspace_id="workspace_example",
                actor_id=context_guid,
            )
        if context_guid == "workspace_example":
            return ContextResolution(
                scope_type="workspace",
                scope_id=context_guid,
                organization_id="org_example",
                workspace_id=context_guid,
            )
        return ContextResolution(
            scope_type="organization",
            scope_id=context_guid,
            organization_id=context_guid,
        )

    def list_version_pins(
        self,
        version_id: str,
        *,
        limit: int = 25,
        offset: int = 0,
    ) -> tuple[list[VersionPinRow], int]:
        """Return mock pins for a connector version."""
        all_pins = list(self.version_pins.get(version_id, ()))
        total = len(all_pins)
        return all_pins[offset : offset + limit], total

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
