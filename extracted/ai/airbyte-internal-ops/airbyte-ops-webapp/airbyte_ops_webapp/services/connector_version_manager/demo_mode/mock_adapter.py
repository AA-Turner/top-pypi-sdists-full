"""Demo-only sample data adapter for connector pinning."""

from __future__ import annotations

import time
from dataclasses import asdict

from airbyte_ops_mcp.connector_ops.rollouts.constants import (
    NO_OP_EMPTY_TIER_MARKER,
    CustomerTier,
)
from airbyte_ops_mcp.registry.progressive_rollout_marker import (
    ProgressiveRolloutMarkerAnnotationResult,
)

from airbyte_ops_webapp.models import (
    ConnectorOption,
    ConnectorPopulation,
    ConnectorRelease,
    ConnectorRollout,
    ConnectorVersion,
    ContextResolution,
    CurrentVersionState,
    OperationResult,
    OverridePlan,
    ProgressiveRolloutMarkerDetail,
    RolloutSyncSummary,
    ScopedConfiguration,
    ScopeType,
    TierPopulationFactors,
    VersionPinRow,
    YankedVersionRow,
    YankMarkerDetail,
    build_version_override_payload,
    version_override_tool_name,
)
from airbyte_ops_webapp.services.connector_version_manager.adapter import (
    SCOPE_PRIORITY,
    OpsMcpAdapter,
)

# Artificial delays for realistic tab-loading UX in mock/demo mode.
_MOCK_DELAY_DEFAULT = 0.75
_MOCK_DELAY_HEAVY = 2.5


def _mock_tier_factors(addressable: int, pinned: int) -> TierPopulationFactors:
    """Synthesize a tier's `TierPopulationFactors` for demo mode.

    Derives an illustrative but internally-consistent factor breakdown from the
    tier's addressable and rollout-pinned counts so the demo UI can show the
    traceable arithmetic (`active = pinned + off-version + unpinned`,
    `unpinned = gate_pass + failed + no_recent_sync`). Values are fabricated for
    the demo; the live adapter derives them from the population query.
    """
    off_version = round(addressable * 0.08)
    unpinned = max(addressable - pinned, 0)
    gate_pass = round(unpinned * 0.45)
    gate_failed = round(unpinned * 0.15)
    gate_no_recent_sync = max(unpinned - gate_pass - gate_failed, 0)
    return TierPopulationFactors(
        active=addressable + off_version,
        pinned_to_rollout=pinned,
        off_version_pinned=off_version,
        unpinned=unpinned,
        gate_pass=gate_pass,
        gate_excluded_failed=gate_failed,
        gate_excluded_no_recent_sync=gate_no_recent_sync,
        addressable=addressable,
        addressable_gated=gate_pass + pinned,
    )


def _mock_population(
    tier_2: tuple[int, int],
    tier_1: tuple[int, int],
    tier_0: tuple[int, int],
) -> ConnectorPopulation:
    """Build a demo `ConnectorPopulation` from per-tier `(addressable, pinned)`.

    Each tier's eligible denominator is the gated-eligible count
    (`gate_pass + pinned`, matching the live adapter and the card's "Eligible"
    row), and `total_eligible` is their sum. `total_active` remains the
    connector-wide active count (retained for fallback).
    """
    factors = {
        tier: _mock_tier_factors(addressable, pinned)
        for tier, (addressable, pinned) in (
            (CustomerTier.TIER_2, tier_2),
            (CustomerTier.TIER_1, tier_1),
            (CustomerTier.TIER_0, tier_0),
        )
    }
    f2, f1, f0 = (
        factors[CustomerTier.TIER_2],
        factors[CustomerTier.TIER_1],
        factors[CustomerTier.TIER_0],
    )
    return ConnectorPopulation(
        total_active=f2.active + f1.active + f0.active,
        total_eligible=f2.addressable_gated
        + f1.addressable_gated
        + f0.addressable_gated,
        eligible_tier_2=f2.addressable_gated,
        eligible_tier_1=f1.addressable_gated,
        eligible_tier_0=f0.addressable_gated,
        pinned_tier_2=f2.pinned_to_rollout,
        pinned_tier_1=f1.pinned_to_rollout,
        pinned_tier_0=f0.pinned_to_rollout,
        tier_resolution_available=True,
        factors_tier_2=f2,
        factors_tier_1=f1,
        factors_tier_0=f0,
    )


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
            version_id="adv_github_1100rc1",
            docker_image_tag="1.10.0-rc.1",
            docker_repository="airbyte/source-github",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.50.0",
            language="python",
            last_published="2026-06-20T11:30:00Z",
        ),
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


def _generate_bulk_pins(count: int = 210) -> tuple[VersionPinRow, ...]:
    """Generate bulk mock pins for scrollbar testing."""
    scope_types = ("actor", "workspace", "organization")
    origins = ("user", "connector_rollout", "user")
    reasons = (
        "Customer regression investigation",
        "Pinned pending patch release",
        "Rollout canary hold",
        "Support escalation pin",
        "Temporary hold for data integrity check",
    )
    scope_name_prefixes = {
        "actor": "Mock Source",
        "workspace": "Mock Workspace",
        "organization": "Mock Organization",
    }
    pins: list[VersionPinRow] = []
    for i in range(count):
        scope_t = scope_types[i % 3]
        pins.append(
            VersionPinRow(
                scope_type=scope_t,
                scope_id=f"{scope_t[:3]}_{i:04d}-mock-{i:08x}",
                scope_url=f"https://cloud.airbyte.com/workspaces/{scope_t[:3]}_{i:04d}",
                origin_type=origins[i % 3],
                origin_name=f"user{i}@airbyte.io",
                description=""
                if origins[i % 3] == "connector_rollout"
                else reasons[i % 5],
                created_at=f"2026-04-{(i % 28) + 1:02d}T10:00:00Z",
                created_at_display=f"2026-04-{(i % 28) + 1:02d}",
                expires_at="2026-07-01T00:00:00Z" if i % 4 == 0 else "",
                expires_at_display="2026-07-01" if i % 4 == 0 else "",
                reference_url=f"https://github.com/airbytehq/airbyte/issues/{3000 + i}",
                scope_name=f"{scope_name_prefixes[scope_t]} {i}",
            )
        )
    return tuple(pins)


MOCK_VERSION_PINS: dict[str, tuple[VersionPinRow, ...]] = {
    "adv_postgres_372": _generate_bulk_pins(210),
    "adv_postgres_371": (
        VersionPinRow(
            scope_type="actor",
            scope_id="act_bc0001-breaking",
            scope_url="https://cloud.airbyte.com/workspaces",
            origin_type="breaking_change",
            origin_name="3.8.0",
            description="",
            created_at="2026-04-15T08:00:00Z",
            created_at_display="2026-04-15 (Tue)",
            expires_at="",
            expires_at_display="",
            reference_url="",
            scope_name="Customer Source A",
        ),
        VersionPinRow(
            scope_type="actor",
            scope_id="act_bc0002-breaking",
            scope_url="https://cloud.airbyte.com/workspaces",
            origin_type="breaking_change",
            origin_name="3.8.0",
            description="",
            created_at="2026-04-15T08:01:00Z",
            created_at_display="2026-04-15 (Tue)",
            expires_at="",
            expires_at_display="",
            reference_url="",
            scope_name="Customer Source B",
        ),
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
            scope_name="Acme Corp Production",
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
            scope_name="Globex Industries",
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
            scope_name="My Postgres Source",
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
            scope_name="Example Org",
        ),
    ),
}

# Org IDs below match the demo orgs returned by the org-lookup search mock
# (`shared_components/org_search.py`), so selecting an org in the Organization
# Pins tab returns a coherent, org-specific set of pins:
#   * Acme         -> manual pins only, one connector across two versions
#   * MotherDuck   -> an active rollout pin + a manual pin on the same version
#   * Airbyte      -> an org-scoped manual pin + a breaking-change pin
#   * Dataflow Labs-> no pins (exercises the empty state)
_MOCK_ORG_PINS: dict[str, tuple[dict[str, object], ...]] = {
    # Acme Corp: manual pins at workspace and actor scope on source-postgres.
    "00000000-0000-0000-0000-000000000001": (
        {
            "connector_definition_id": "b5ea17b1-f170-46dc-bc31-cc744ca984c1",
            "connector_name": "source-postgres",
            "docker_repository": "airbyte/source-postgres",
            "version_id": "adv_postgres_360",
            "docker_image_tag": "3.6.0",
            "last_published": "2026-03-11T09:40:00Z",
            "pin_scope_type": "workspace",
            "scope_id": "aaaaaaaa-0000-0000-0000-000000000001",
            "scope_name": "Acme Production",
            "origin_type": "user",
            "set_by": "eng@acme.io",
            "description": "Workspace pinned during regression investigation",
            "reference_url": "https://github.com/airbytehq/airbyte/issues/0000",
            "created_at": "2026-04-10T14:30:00Z",
            "expires_at": "2026-05-15T00:00:00Z",
            "rollout_id": None,
            "rollout_state": None,
        },
        {
            "connector_definition_id": "b5ea17b1-f170-46dc-bc31-cc744ca984c1",
            "connector_name": "source-postgres",
            "docker_repository": "airbyte/source-postgres",
            "version_id": "adv_postgres_371",
            "docker_image_tag": "3.7.1",
            "last_published": "2026-04-07T15:03:00Z",
            "pin_scope_type": "actor",
            "scope_id": "actor-acme-0001",
            "scope_name": "Acme Prod Postgres",
            "origin_type": "user",
            "set_by": "eng@acme.io",
            "description": "Actor-level canary pin",
            "reference_url": "https://github.com/airbytehq/airbyte/issues/1111",
            "created_at": "2026-04-12T09:15:00Z",
            "expires_at": "",
            "rollout_id": None,
            "rollout_state": None,
        },
    ),
    # MotherDuck: an active rollout pin plus a manual hold on source-postgres
    # 3.7.2 -- shows the rollout state + has_active_rollout alongside a manual pin.
    "00000000-0000-0000-0000-000000000002": (
        {
            "connector_definition_id": "b5ea17b1-f170-46dc-bc31-cc744ca984c1",
            "connector_name": "source-postgres",
            "docker_repository": "airbyte/source-postgres",
            "version_id": "adv_postgres_372",
            "docker_image_tag": "3.7.2",
            "last_published": "2026-04-21T18:21:00Z",
            "pin_scope_type": "actor",
            "scope_id": "actor-md-0001",
            "scope_name": "MotherDuck Analytics Source",
            "origin_type": "connector_rollout",
            "set_by": None,
            "description": "",
            "reference_url": "",
            "created_at": "2026-04-28T11:00:00Z",
            "expires_at": "",
            "rollout_id": "mock-postgres-rollout",
            "rollout_state": "in_progress",
        },
        {
            "connector_definition_id": "b5ea17b1-f170-46dc-bc31-cc744ca984c1",
            "connector_name": "source-postgres",
            "docker_repository": "airbyte/source-postgres",
            "version_id": "adv_postgres_372",
            "docker_image_tag": "3.7.2",
            "last_published": "2026-04-21T18:21:00Z",
            "pin_scope_type": "workspace",
            "scope_id": "bbbbbbbb-0000-0000-0000-000000000001",
            "scope_name": "MotherDuck Analytics",
            "origin_type": "user",
            "set_by": "analytics@motherduck.com",
            "description": "Workspace held pending rollout validation",
            "reference_url": "https://github.com/airbytehq/airbyte/issues/2020",
            "created_at": "2026-05-01T10:00:00Z",
            "expires_at": "2026-07-01T00:00:00Z",
            "rollout_id": None,
            "rollout_state": None,
        },
    ),
    # Airbyte: an org-scoped manual pin and a breaking-change pin on source-github.
    "00000000-0000-0000-0000-000000000003": (
        {
            "connector_definition_id": "ef69ef6e-aa7f-4af1-a01d-ef775033524e",
            "connector_name": "source-github",
            "docker_repository": "airbyte/source-github",
            "version_id": "adv_github_187",
            "docker_image_tag": "1.8.7",
            "last_published": "2026-02-18T20:15:00Z",
            "pin_scope_type": "organization",
            "scope_id": "00000000-0000-0000-0000-000000000003",
            "scope_name": "Airbyte",
            "origin_type": "user",
            "set_by": "admin@airbyte.io",
            "description": "Organization-level temporary pin",
            "reference_url": "https://github.com/airbytehq/airbyte/issues/2222",
            "created_at": "2026-03-01T12:00:00Z",
            "expires_at": "2026-05-30T00:00:00Z",
            "rollout_id": None,
            "rollout_state": None,
        },
        {
            "connector_definition_id": "ef69ef6e-aa7f-4af1-a01d-ef775033524e",
            "connector_name": "source-github",
            "docker_repository": "airbyte/source-github",
            "version_id": "adv_github_194",
            "docker_image_tag": "1.9.4",
            "last_published": "2026-04-26T14:12:00Z",
            "pin_scope_type": "actor",
            "scope_id": "actor-ab-0001",
            "scope_name": "Airbyte Dogfood GitHub",
            "origin_type": "breaking_change",
            "set_by": None,
            "description": "",
            "reference_url": "",
            "created_at": "2026-04-26T14:12:00Z",
            "expires_at": "",
            "rollout_id": None,
            "rollout_state": None,
        },
    ),
    # Dataflow Labs (00000000-0000-0000-0000-000000000004) intentionally omitted:
    # selecting it exercises the "no pins under this organization" empty state.
}

_ROLLOUT_ACTIVE_STATES = frozenset(
    {
        "initialized",
        "workflow_started",
        "in_progress",
        "paused",
        "finalizing",
        "errored",
    }
)


MOCK_ROLLOUTS: dict[str, tuple[ConnectorRollout, ...]] = {
    "b5ea17b1-f170-46dc-bc31-cc744ca984c1": (
        ConnectorRollout(
            rollout_id="mock-postgres-rollout",
            connector_id="b5ea17b1-f170-46dc-bc31-cc744ca984c1",
            connector_name="source-postgres",
            connector_type="source",
            docker_repository="airbyte/source-postgres",
            # Autopilot pauses (rather than cancels) a tier whose failure
            # threshold trips, writing FAILURE_THRESHOLD_EXCEEDED_MARKER into
            # `paused_reason`. The later TIER_1 rollout below is already
            # running, so this row also covers the inference-rule regression:
            # a held tier must stay ⚠️ and never be promoted to ☑️.
            state="paused",
            paused_reason=(
                "Failure threshold exceeded: 2 failures (threshold=1). "
                "Pause/rollback recommended."
            ),
            rc_docker_image_tag="3.8.0-rc.12",
            initial_docker_image_tag="3.7.2",
            current_target_rollout_pct="50",
            final_target_rollout_pct="100",
            created_at="2026-04-28T11:00:00Z",
            updated_at="2026-06-22T14:30:00Z",
            rollout_strategy="auto",
            rc_pin_count=2,
            tier=CustomerTier.TIER_2,
        ),
        ConnectorRollout(
            rollout_id="mock-postgres-rollout-t1",
            connector_id="b5ea17b1-f170-46dc-bc31-cc744ca984c1",
            connector_name="source-postgres",
            connector_type="source",
            docker_repository="airbyte/source-postgres",
            state="in_progress",
            rc_docker_image_tag="3.8.0-rc.12",
            initial_docker_image_tag="3.7.2",
            current_target_rollout_pct="30",
            final_target_rollout_pct="100",
            created_at="2026-05-02T11:00:00Z",
            updated_at="2026-06-23T09:15:00Z",
            rollout_strategy="auto",
            rc_pin_count=2,
            tier=CustomerTier.TIER_1,
        ),
    ),
    "ef69ef6e-aa7f-4af1-a01d-ef775033524e": (
        ConnectorRollout(
            rollout_id="mock-github-rollout-t2",
            connector_id="ef69ef6e-aa7f-4af1-a01d-ef775033524e",
            connector_name="source-github",
            connector_type="source",
            docker_repository="airbyte/source-github",
            state="in_progress",
            rc_docker_image_tag="1.10.0-rc.1",
            initial_docker_image_tag="1.9.4",
            current_target_rollout_pct="100",
            final_target_rollout_pct="100",
            created_at="2026-06-18T09:00:00Z",
            updated_at="2026-06-19T12:00:00Z",
            rollout_strategy="manual",
            rc_pin_count=3,
            tier=CustomerTier.TIER_2,
        ),
        ConnectorRollout(
            rollout_id="mock-github-rollout",
            connector_id="ef69ef6e-aa7f-4af1-a01d-ef775033524e",
            connector_name="source-github",
            connector_type="source",
            docker_repository="airbyte/source-github",
            state="initialized",
            rc_docker_image_tag="1.10.0-rc.1",
            initial_docker_image_tag="1.9.4",
            current_target_rollout_pct="0",
            final_target_rollout_pct="100",
            created_at="2026-06-20T09:00:00Z",
            updated_at="2026-06-20T09:00:00Z",
            rollout_strategy="manual",
            rc_pin_count=0,
            tier=CustomerTier.TIER_1,
        ),
    ),
    "25c5221d-dce2-4163-ade9-739ef790f503": (
        ConnectorRollout(
            rollout_id="mock-snowflake-rollout",
            connector_id="25c5221d-dce2-4163-ade9-739ef790f503",
            connector_name="destination-snowflake",
            connector_type="destination",
            docker_repository="airbyte/destination-snowflake",
            state="paused",
            rc_docker_image_tag="3.4.0-rc.5",
            initial_docker_image_tag="3.3.1",
            current_target_rollout_pct="25",
            final_target_rollout_pct="100",
            created_at="2026-06-15T16:00:00Z",
            updated_at="2026-06-21T10:45:00Z",
            rollout_strategy="auto",
            rc_pin_count=1,
            tier=CustomerTier.TIER_0,
        ),
        ConnectorRollout(
            rollout_id="mock-snowflake-rollout-t1",
            connector_id="25c5221d-dce2-4163-ade9-739ef790f503",
            connector_name="destination-snowflake",
            connector_type="destination",
            docker_repository="airbyte/destination-snowflake",
            # Autopilot creates and immediately cancels a tier with no eligible
            # customers, recording NO_OP_EMPTY_TIER_MARKER. Such a tier renders
            # as `Empty` rather than ☑️ Complete.
            state="canceled",
            error_msg=NO_OP_EMPTY_TIER_MARKER,
            rc_docker_image_tag="3.4.0-rc.5",
            initial_docker_image_tag="3.3.1",
            current_target_rollout_pct="0",
            final_target_rollout_pct="100",
            created_at="2026-06-16T16:00:00Z",
            updated_at="2026-06-20T10:00:00Z",
            rollout_strategy="auto",
            rc_pin_count=0,
            tier=CustomerTier.TIER_1,
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

    def list_versions_with_pins(self) -> list[dict[str, object]]:
        """Return mock versions that have at least one pin (no rollout data)."""
        time.sleep(_MOCK_DELAY_HEAVY)
        result: list[dict[str, object]] = []
        for connector_id, versions in self.versions.items():
            for version in versions:
                pins = self.version_pins.get(version.version_id, ())
                if pins:
                    breaking_change_pins = sum(
                        1
                        for p in pins
                        if p.scope_type == "actor"
                        and p.origin_type == "breaking_change"
                    )
                    rollout_pins = sum(
                        1 for p in pins if p.origin_type == "connector_rollout"
                    )
                    actor_pins = sum(
                        1
                        for p in pins
                        if p.scope_type == "actor"
                        and p.origin_type
                        not in ("breaking_change", "connector_rollout")
                    )
                    workspace_pins = sum(1 for p in pins if p.scope_type == "workspace")
                    org_pins = sum(1 for p in pins if p.scope_type == "organization")
                    result.append(
                        {
                            "version_id": version.version_id,
                            "connector_definition_id": connector_id,
                            "connector_name": "",
                            "docker_repository": version.docker_repository,
                            "docker_image_tag": version.docker_image_tag,
                            "last_published": version.last_published,
                            "pin_count": len(pins),
                            "breaking_change_pins": breaking_change_pins,
                            "rollout_pins": rollout_pins,
                            "actor_pins": actor_pins,
                            "workspace_pins": workspace_pins,
                            "org_pins": org_pins,
                        }
                    )
        return result

    def list_org_pin_stats(
        self,
        organization_id: str,
    ) -> list[dict[str, object]]:
        """Return mock aggregate pin stats for the pins under an organization.

        Aggregates the org's curated pins into one row per pinned version, with
        per-origin and per-scope counts. Unknown orgs return an empty list.
        """
        time.sleep(_MOCK_DELAY_HEAVY)
        pins = _MOCK_ORG_PINS.get(organization_id, ())
        by_version: dict[str, list[dict[str, object]]] = {}
        for pin in pins:
            by_version.setdefault(str(pin["version_id"]), []).append(pin)

        result: list[dict[str, object]] = []
        for version_id, version_pins in by_version.items():
            first = version_pins[0]
            origins = [p["origin_type"] for p in version_pins]
            scopes = [p["pin_scope_type"] for p in version_pins]
            result.append(
                {
                    "version_id": version_id,
                    "connector_definition_id": first["connector_definition_id"],
                    "connector_name": first["connector_name"],
                    "docker_repository": first["docker_repository"],
                    "docker_image_tag": first["docker_image_tag"],
                    "last_published": first["last_published"],
                    "pin_count": len(version_pins),
                    "manual_pins": sum(
                        1
                        for o in origins
                        if o not in ("breaking_change", "connector_rollout")
                    ),
                    "rollout_pins": sum(1 for o in origins if o == "connector_rollout"),
                    "breaking_change_pins": sum(
                        1 for o in origins if o == "breaking_change"
                    ),
                    # `actor_pins` counts only custom (manual) actor-scoped pins,
                    # excluding system origins, to match `SELECT_ORG_PIN_STATS`.
                    "actor_pins": sum(
                        1
                        for p in version_pins
                        if p["pin_scope_type"] == "actor"
                        and p["origin_type"]
                        not in ("breaking_change", "connector_rollout")
                    ),
                    "workspace_pins": sum(1 for s in scopes if s == "workspace"),
                    "org_pins": sum(1 for s in scopes if s == "organization"),
                    "has_active_rollout": any(
                        str(p["rollout_state"]) in _ROLLOUT_ACTIVE_STATES
                        for p in version_pins
                    ),
                }
            )
        return result

    def list_org_connector_pins(
        self,
        organization_id: str,
        *,
        pinned_version_id: str | None = None,
    ) -> list[dict[str, object]]:
        """Return the mock individual pins under an org, optionally one version.

        Unknown orgs return an empty list.
        """
        time.sleep(_MOCK_DELAY_DEFAULT)
        result: list[dict[str, object]] = []
        for pin in _MOCK_ORG_PINS.get(organization_id, ()):
            if pinned_version_id and pin["version_id"] != pinned_version_id:
                continue
            set_by = pin["set_by"]
            result.append(
                {
                    "pinned_version_id": pin["version_id"],
                    "connector_definition_id": pin["connector_definition_id"],
                    "connector_name": pin["connector_name"],
                    "docker_repository": pin["docker_repository"],
                    "pinned_version_tag": pin["docker_image_tag"],
                    "pin_scope_type": pin["pin_scope_type"],
                    "scope_id": pin["scope_id"],
                    "scope_name": pin["scope_name"],
                    "origin_type": pin["origin_type"] or None,
                    "origin": set_by,
                    "pinned_by_user_name": set_by,
                    "pinned_by_user_email": set_by,
                    "description": pin["description"],
                    "reference_url": pin["reference_url"],
                    "created_at": pin["created_at"],
                    "expires_at": pin["expires_at"],
                    "rollout_id": pin["rollout_id"],
                    "rollout_state": pin["rollout_state"],
                }
            )
        return result

    def list_yanked_versions(self) -> tuple[YankedVersionRow, ...]:
        """Return a fixed set of mock yanked versions for demos and tests."""
        time.sleep(_MOCK_DELAY_DEFAULT)
        return (
            YankedVersionRow(
                connector_id="ef69ef6e-aa7f-4af1-a01d-ef775033524e",
                connector_name="source-github",
                docker_image_tag="1.9.3",
                yanked_at="2026-06-18T14:30:00Z",
                reason="Regression in incremental sync cursor handling.",
                approval_url="",
            ),
            YankedVersionRow(
                connector_id="25c5221d-dce2-4163-ade9-739ef790f503",
                connector_name="destination-snowflake",
                docker_image_tag="3.2.0",
                yanked_at="2026-05-02T09:15:00Z",
                reason="Data corruption on schema migration.",
                approval_url="",
            ),
        )

    def get_yank_marker(
        self,
        connector_name: str,
        version: str,
    ) -> YankMarkerDetail | None:
        """Return a mock yank marker for a yanked version, else `None`.

        Derives the detail from `list_yanked_versions` so the mock stays
        internally consistent, synthesizing a `raw` `version-yank.yml` body that
        mirrors the shape written by the real yank workflow.
        """
        for row in self.list_yanked_versions():
            if row.connector_name == connector_name and row.docker_image_tag == version:
                raw_lines = ["yanked: true", f"yanked_at: '{row.yanked_at}'"]
                if row.reason:
                    raw_lines.append(f"reason: {row.reason}")
                if row.approval_url:
                    raw_lines.append(f"approval_url: {row.approval_url}")
                return YankMarkerDetail(
                    connector_id=row.connector_id,
                    connector_name=row.connector_name,
                    docker_image_tag=row.docker_image_tag,
                    yanked_at=row.yanked_at,
                    reason=row.reason,
                    approval_url=row.approval_url,
                    raw="\n".join(raw_lines) + "\n",
                )
        return None

    def get_progressive_rollout_marker(
        self,
        connector_name: str,
        version: str,
    ) -> ProgressiveRolloutMarkerDetail | None:
        """Return a realistic pending promotion marker for the demo RC."""
        if connector_name == "source-github" and version == "1.10.0-rc.1":
            return ProgressiveRolloutMarkerDetail(
                connector_id="ef69ef6e-aa7f-4af1-a01d-ef775033524e",
                connector_name=connector_name,
                docker_image_tag=version,
                progressive_rollout=True,
                created_at="2026-06-20T11:30:00Z",
                promotion_requested_at="2026-06-20T15:00:00Z",
                promotion_requested_by="ops@example.com",
                rollout_id="rollout_demo_github",
                raw=(
                    "progressive_rollout: true\n"
                    "created_at: '2026-06-20T11:30:00Z'\n"
                    "promotion_requested_at: '2026-06-20T15:00:00Z'\n"
                    "promotion_requested_by: ops@example.com\n"
                    "rollout_id: rollout_demo_github\n"
                ),
                state="active",
                marker_date="",
            )
        if connector_name == "source-github" and version == "1.10.0":
            return ProgressiveRolloutMarkerDetail(
                connector_id="ef69ef6e-aa7f-4af1-a01d-ef775033524e",
                connector_name=connector_name,
                docker_image_tag=version,
                progressive_rollout=True,
                created_at="2026-06-20T11:30:00Z",
                promotion_requested_at="2026-06-20T15:00:00Z",
                promotion_requested_by="ops@example.com",
                rollout_id="rollout_demo_github",
                raw=(
                    "progressive_rollout: true\n"
                    "created_at: '2026-06-20T11:30:00Z'\n"
                    "promotion_requested_at: '2026-06-20T15:00:00Z'\n"
                    "promotion_requested_by: ops@example.com\n"
                    "rollout_id: rollout_demo_github\n"
                ),
                state="promoted",
                marker_date="20260620",
            )
        return None

    def annotate_progressive_rollout_marker(
        self,
        connector_name: str,
        version: str,
        *,
        promotion_requested_by: str,
        rollout_id: str,
    ) -> ProgressiveRolloutMarkerAnnotationResult:
        """Return a successful demo annotation result."""
        marker = self.get_progressive_rollout_marker(connector_name, version)
        if marker is None:
            return ProgressiveRolloutMarkerAnnotationResult(
                connector_name=connector_name,
                version=version,
                bucket_name="mock",
                action="annotate",
                success=False,
                message="No active progressive rollout marker found.",
            )
        return ProgressiveRolloutMarkerAnnotationResult(
            connector_name=connector_name,
            version=version,
            bucket_name="mock",
            action="annotate",
            success=True,
            message="Annotated active progressive rollout marker.",
            marker=marker,
        )

    def list_recent_releases(
        self,
        *,
        days: int = 30,
        limit: int | None = None,
    ) -> tuple[ConnectorRelease, ...]:
        """List recent mock releases across connectors."""
        time.sleep(_MOCK_DELAY_DEFAULT)
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
        return tuple(
            rollout
            for rollout in self.rollouts.get(connector_id, ())
            if rollout.state in _ROLLOUT_ACTIVE_STATES
        )

    def list_active_rollouts_with_siblings(
        self,
        connector_id: str,
    ) -> tuple[ConnectorRollout, ...]:
        """List active mock rollouts and their sibling tiers for a connector."""
        active = self.list_active_rollouts(connector_id)
        rc_tags = {rollout.rc_docker_image_tag for rollout in active}
        return tuple(
            rollout
            for rollout in self.rollouts.get(connector_id, ())
            if rollout.rc_docker_image_tag in rc_tags
        )

    def list_progressive_rollouts(
        self,
        *,
        limit: int | None = None,
    ) -> tuple[ConnectorRollout, ...]:
        """List active mock rollouts across connectors."""
        time.sleep(_MOCK_DELAY_HEAVY)
        rollouts = sorted(
            (
                rollout
                for connector_rollouts in self.rollouts.values()
                for rollout in connector_rollouts
                if rollout.state in _ROLLOUT_ACTIVE_STATES
            ),
            key=lambda rollout: rollout.updated_at,
            reverse=True,
        )
        return tuple(rollouts[:limit] if limit is not None else rollouts)

    def list_progressive_rollouts_with_siblings(
        self,
        *,
        limit: int | None = None,
    ) -> tuple[ConnectorRollout, ...]:
        """List active mock rollouts and their sibling tiers."""
        active = self.list_progressive_rollouts(limit=limit)
        pairs = {
            (rollout.connector_id, rollout.rc_docker_image_tag) for rollout in active
        }
        rollouts = sorted(
            (
                rollout
                for connector_rollouts in self.rollouts.values()
                for rollout in connector_rollouts
                if (rollout.connector_id, rollout.rc_docker_image_tag) in pairs
            ),
            key=lambda rollout: rollout.updated_at,
            reverse=True,
        )
        return tuple(rollouts)

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
        if context_guid == "actor_example" or context_guid.startswith("act_"):
            return ContextResolution(
                scope_type="actor",
                scope_id=context_guid,
                organization_id="org_example",
                scope_name=f"Mock {connector.connector_type.title()}",
                workspace_id="workspace_example",
                workspace_name="Mock Workspace",
                organization_name="Mock Organization",
                actor_id=context_guid,
                actor_type=connector.connector_type,
                customer_tier="TIER_2",
            )
        if context_guid == "workspace_example" or context_guid.startswith("ws_"):
            return ContextResolution(
                scope_type="workspace",
                scope_id=context_guid,
                organization_id="org_example",
                scope_name="Mock Workspace",
                workspace_id=context_guid,
                workspace_name="Mock Workspace",
                organization_name="Mock Organization",
                customer_tier="TIER_2",
            )
        return ContextResolution(
            scope_type="organization",
            scope_id=context_guid,
            organization_id=context_guid,
            scope_name="Mock Organization",
            organization_name="Mock Organization",
            # A sensitive tier in demo mode so the modal's approval warning is
            # exercisable without touching a real customer.
            customer_tier="TIER_0",
        )

    def get_rollout_sync_summary(
        self,
        rollout_id: str,
        *,
        tier: str = "",
        is_destination: bool,
    ) -> RolloutSyncSummary:
        """Return a mock rollout health + population summary, keyed by rollout.

        Distinct values per rollout ID so the per-tier cards render realistic
        (differing) breakdowns in demo mode.
        """
        if not rollout_id:
            return RolloutSyncSummary()
        per_rollout = {
            # source-github T2: 100% deployed, no failures -> 🟢 Complete
            "mock-github-rollout-t2": RolloutSyncSummary(
                health="18 healthy | 0 unhealthy | 2 awaiting",
                num_pinned=20,
                num_eligible=20,
                num_healthy=18,
                num_unhealthy=0,
            ),
            # source-github T1: initialized (not started) -> ⚪ Not started
            "mock-github-rollout": RolloutSyncSummary(
                health="0 healthy | 0 unhealthy | 0 awaiting",
                num_pinned=0,
                num_eligible=60,
                num_healthy=0,
                num_unhealthy=0,
            ),
            # source-postgres T2: 50% deployed with failures -> 🟡 Attention
            "mock-postgres-rollout": RolloutSyncSummary(
                health="30 healthy | 3 unhealthy | 12 awaiting",
                num_pinned=45,
                num_eligible=65,
                num_healthy=30,
                num_unhealthy=3,
            ),
            # source-postgres T1: 30% deployed, no failures -> 🔵 In progress
            "mock-postgres-rollout-t1": RolloutSyncSummary(
                health="10 healthy | 0 unhealthy | 2 awaiting",
                num_pinned=12,
                num_eligible=23,
                num_healthy=10,
                num_unhealthy=0,
            ),
            # destination-snowflake: paused -> ⏸️ Paused
            "mock-snowflake-rollout": RolloutSyncSummary(
                health="9 healthy | 0 unhealthy | 3 awaiting",
                num_pinned=12,
                num_eligible=30,
                num_healthy=9,
                num_unhealthy=0,
            ),
        }
        return per_rollout.get(
            rollout_id,
            RolloutSyncSummary(
                health="8 healthy | 1 unhealthy | 1 awaiting",
                num_pinned=12,
                num_eligible=40,
                num_healthy=8,
                num_unhealthy=1,
            ),
        )

    def get_rollout_sync_summaries_by_tier(
        self,
        rollout_id: str,
        *,
        is_destination: bool,
    ) -> dict[str, RolloutSyncSummary]:
        if not rollout_id:
            return {}
        return {
            CustomerTier.TIER_2.value: self.get_rollout_sync_summary(
                rollout_id,
                is_destination=is_destination,
            )
        }

    def get_connector_population(
        self,
        connector_definition_id: str,
        *,
        is_destination: bool,
        target_version_id: str = "",
        rollout_created_at: str = "",
    ) -> ConnectorPopulation:
        """Return a mock enabled (active-only) population, keyed by connector.

        Each tier is seeded from `(addressable, pinned)` counts; the eligible
        denominator surfaced on the card is the gated-eligible count
        (`gate_pass + pinned`), and `pinned_<tier>` is a subset of it, so the
        card's `pinned / eligible` numerator never exceeds its denominator.
        `total_eligible` is the connector-wide gated-eligible count and
        `total_active` the connector-wide active count. Each `factors_<tier>`
        carries the full distinct-factor breakdown (see
        `airbyte_ops_webapp.models.TierPopulationFactors`) so the demo UI can show
        the traceable arithmetic. `target_version_id` and `rollout_created_at` are
        accepted for parity with the live adapter but the mock values are already
        version-scoped.
        """
        per_connector = {
            # source-github
            "ef69ef6e-aa7f-4af1-a01d-ef775033524e": _mock_population(
                (20, 20), (60, 0), (4, 0)
            ),
            # source-postgres (T2 in-progress w/ failures, T1 in-progress clean)
            "b5ea17b1-f170-46dc-bc31-cc744ca984c1": _mock_population(
                (90, 45), (36, 12), (6, 0)
            ),
            # destination-snowflake (T0 is rolling out; T1 has no customers at
            # all, so its rollout was canceled as a no-op and renders `Empty`)
            "25c5221d-dce2-4163-ade9-739ef790f503": _mock_population(
                (50, 0), (0, 0), (40, 12)
            ),
        }
        return per_connector.get(
            connector_definition_id,
            _mock_population((40, 32), (10, 0), (2, 0)),
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

    def apply_override(
        self,
        plan: OverridePlan,
    ) -> OperationResult:
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
