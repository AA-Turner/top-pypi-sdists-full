"""Typed data models for Connector Pinning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from airbyte_ops_mcp.tier_cache import TierFilter
from pydantic import BaseModel

ConnectorType = Literal["source", "destination"]
OverrideAction = Literal["set", "unset"]
ScopeType = Literal["actor", "workspace", "organization"]
VersionOverrideToolName = Literal["set_version_override",]

CustomerTierFilter = TierFilter

__all__ = [
    "ConnectorOption",
    "ConnectorRelease",
    "ConnectorRollout",
    "ConnectorType",
    "ConnectorVersion",
    "ContextResolution",
    "CurrentVersionState",
    "CustomerTierFilter",
    "OperationPreview",
    "OperationResult",
    "OverrideAction",
    "OverridePlan",
    "RolloutSyncSummary",
    "ScopeType",
    "ScopedConfiguration",
    "VersionOverridePayload",
    "VersionOverrideTargetPayload",
    "VersionOverrideToolName",
    "VersionPinRow",
    "build_version_override_payload",
    "version_override_tool_name",
]


class OverridePlan(BaseModel):
    """Connector version override plan staged by the app."""

    action: OverrideAction
    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    scope_type: ScopeType
    organization_id: str
    workspace_id: str | None = None
    actor_id: str | None = None
    scope_id: str = ""
    version: str | None
    override_reason: str
    override_reason_reference_url: str
    approval_comment_url: str | None = None
    user_email: str | None = None
    customer_tier_filter: TierFilter
    force: bool


class VersionOverrideTargetPayload(BaseModel):
    """Normalized target for a connector version override."""

    scope: ScopeType
    organization_id: str
    connector_type: ConnectorType
    workspace_id: str | None = None
    actor_id: str | None = None
    connector_name: str | None = None


class VersionOverridePayload(BaseModel):
    """Payload for a normalized connector version override."""

    target: VersionOverrideTargetPayload
    version: str | None
    unset: bool
    override_reason: str | None
    override_reason_reference_url: str | None
    approval_comment_url: str | None
    ai_agent_session_url: str | None
    user_email: str | None
    force: bool
    customer_tier_filter: TierFilter


class OperationPreview(BaseModel):
    """Safe preview of the tool call that would be made."""

    tool_name: VersionOverrideToolName
    mutating: bool
    mode: str
    payload: VersionOverridePayload
    required_approval_fields: tuple[str, ...]
    warnings: tuple[str, ...]


class OperationResult(BaseModel):
    """Result of applying a connector version override plan."""

    tool_name: VersionOverrideToolName
    success: bool
    mutating: bool
    mode: str
    message: str
    payload: VersionOverridePayload


@dataclass(frozen=True)
class ConnectorOption:
    """Connector definition shown in the search/select flow."""

    id: str
    name: str
    connector_type: ConnectorType
    latest_version: str
    docker_repository: str


@dataclass(frozen=True)
class ConnectorRelease:
    """Recently published connector release option."""

    version_id: str
    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    docker_image_tag: str
    docker_repository: str
    release_stage: str
    last_published: str


@dataclass(frozen=True)
class YankedVersionRow:
    """A connector version that has been yanked from the registry.

    `connector_id` is the actor-definition UUID resolved from the connector's
    canonical name; it is empty when the connector cannot be resolved in the
    registry, in which case the row still renders but is not click-navigable.
    """

    connector_id: str
    connector_name: str
    docker_image_tag: str
    yanked_at: str
    reason: str
    approval_url: str


@dataclass(frozen=True)
class YankMarkerDetail:
    """Parsed contents of a single active `version-yank.yml` marker.

    Returned for the currently-selected version so the Connector Version Status
    panel can render the yank marker's structured fields plus its `raw` YAML
    text. `connector_id` mirrors `YankedVersionRow` so the detail stays
    associated with the resolved connector.
    """

    connector_id: str
    connector_name: str
    docker_image_tag: str
    yanked_at: str
    reason: str
    approval_url: str
    raw: str


@dataclass(frozen=True)
class ProgressiveRolloutMarkerDetail:
    """Parsed contents of a single progressive rollout marker."""

    connector_id: str
    connector_name: str
    docker_image_tag: str
    progressive_rollout: bool
    created_at: str
    promotion_requested_at: str
    promotion_requested_by: str
    rollout_id: str
    raw: str
    state: str = "active"
    marker_date: str = ""


@dataclass(frozen=True)
class ConnectorVersion:
    """Published connector version row."""

    version_id: str
    docker_image_tag: str
    docker_repository: str
    release_stage: str
    support_level: str
    cdk_version: str
    language: str
    last_published: str


@dataclass(frozen=True)
class RolloutSyncSummary:
    """Replica-backed health and population counts for an active rollout.

    The summary uses read-only replica queries for the live actor population and
    actor-scope rollout pins, then applies cached customer-tier data in Python.
    `num_pinned` counts tier-matching pinned actors. `num_healthy` and
    `num_unhealthy` are derived from each pinned actor's latest-job rollup. The
    `health` string contains the four formatted buckets: healthy, unhealthy,
    awaiting, and disabled. `num_eligible` is `None` because connector-wide
    eligibility belongs to the connector population path, not this synchronous
    rollout summary.
    """

    health: str = ""
    num_pinned: int = 0
    # Connector-wide eligibility is owned by ConnectorPopulation; rollout
    # summaries do not calculate it on the synchronous selection path.
    num_eligible: int | None = None
    num_healthy: int = 0
    num_unhealthy: int = 0


@dataclass(frozen=True)
class TierPopulationFactors:
    """Distinct population factors for one rollout tier (nothing collapsed).

    Surfaced so the UI can show every factor and how each denominator is built,
    with traceable arithmetic. The identities that hold by construction:

    - `active = pinned_to_rollout + off_version_pinned + unpinned`
    - `unpinned = gate_pass + gate_excluded_failed + gate_excluded_no_recent_sync`
    - `addressable = active - off_version_pinned` (the honest active-fleet
      denominator)
    - `addressable_gated = gate_pass + pinned_to_rollout` (reproduces the
      platform's `nActorsEligibleOrAlreadyPinned` — its job-status-gated
      denominator)

    `pinned_to_rollout` is the numerator for both denominators. The `gate_*`
    fields reproduce the platform's `filterByJobStatus` gate over the rollout
    window; they are `0` (and `addressable_gated` collapses to
    `pinned_to_rollout`) when no rollout window is available.
    """

    active: int = 0
    pinned_to_rollout: int = 0
    off_version_pinned: int = 0
    unpinned: int = 0
    gate_pass: int = 0
    gate_excluded_failed: int = 0
    gate_excluded_no_recent_sync: int = 0
    addressable: int = 0
    addressable_gated: int = 0


@dataclass(frozen=True)
class ConnectorPopulation:
    """Enabled (active-connection) actor population for a connector, by rollout tier.

    Sourced from the DB-backed `query_actor_population_by_org` +
    `summarize_population` path, counting only actors with at least one active
    connection (`connection.status = 'active'`). Used to (a) show a single
    connector-wide `total_eligible` count (the backend's gated eligibility) on
    the "Eligible Actors" line, and (b) supply each tier's eligible count on the
    rollout cards — for both started and not-yet-started tiers.

    The per-tier `eligible_*` fields are each tier's job-status-*gated* audience
    for the rollout version (`addressable_gated_by_tier`, the backend's
    `nActorsEligibleOrAlreadyPinned`): unpinned actors that pass the gate plus
    actors already pinned to the rollout version. Actors pinned to a different
    version, with a recent failure, or with no recent sync are excluded because
    they are not part of the rollout's realized denominator. `total_active`
    remains the connector-wide active count across every tier (retained for
    fallback), while `total_eligible` is the connector-wide gated-eligible count
    used for the headline. The final `ALL` rollout stage (GA to everyone) is
    surfaced under the `TIER_0` cohort it ultimately brings in.

    The per-tier `pinned_*` fields are each tier's active actors whose effective
    pin is *the rollout version* (`pinned_to_version_active_by_tier`), not merely
    a pin to any version. They come from the same active-only population as
    `eligible_*`, so `pinned_<tier> <= eligible_<tier>` holds by construction —
    unlike the rollout scan's `numPinnedToConnectorRollout`, which counts
    tombstoned/inactive pinned actors and can exceed the active audience.

    The per-tier `factors_*` fields carry every distinct population factor for
    that tier (see `TierPopulationFactors`), so the UI can over-communicate the
    full breakdown and show how both the addressable and the backend-eligible
    denominators are built. They are `None` when tier resolution was unavailable.

    `tier_resolution_available` records whether the per-tier split was
    computed at all. It is `False` only when `get_connector_population`
    returns early before building the breakdown — i.e. no
    `connector_definition_id`, or the actor-population DB query raised — so
    the per-tier `eligible_*` / `pinned_*` counts are unknown rather than a
    genuine zero, letting the UI distinguish "not started, 0 eligible" from
    "not started, eligible unknown". A GCS/credential failure in tier
    resolution does *not* set this flag: it propagates and aborts the page
    rather than degrading to a misleading `0 of 0`.
    """

    total_active: int = 0
    total_eligible: int = 0
    eligible_tier_2: int = 0
    eligible_tier_1: int = 0
    eligible_tier_0: int = 0
    pinned_tier_2: int = 0
    pinned_tier_1: int = 0
    pinned_tier_0: int = 0
    tier_resolution_available: bool = False
    factors_tier_2: TierPopulationFactors | None = None
    factors_tier_1: TierPopulationFactors | None = None
    factors_tier_0: TierPopulationFactors | None = None


@dataclass(frozen=True)
class ConnectorRollout:
    """Active progressive rollout row."""

    rollout_id: str
    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    docker_repository: str
    state: str
    rc_docker_image_tag: str
    initial_docker_image_tag: str
    current_target_rollout_pct: str
    final_target_rollout_pct: str
    created_at: str
    updated_at: str
    rollout_strategy: str = ""
    rc_pin_count: int = 0
    tier: str = "TIER_2"
    tier_is_explicit: bool = True
    release_candidate_version_id: str = ""
    error_msg: str = ""
    failed_reason: str = ""
    paused_reason: str = ""


@dataclass(frozen=True)
class ScopedConfiguration:
    """Connector version override configuration."""

    id: str
    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    scope_type: ScopeType
    scope_id: str
    scope_name: str
    value_name: str
    description: str
    origin_type: str
    origin_name: str
    expires_at: str
    reference_url: str


@dataclass(frozen=True)
class VersionPinRow:
    """A single pin row for display in the version pin list."""

    scope_type: str
    scope_id: str
    scope_url: str
    origin_type: str
    origin_name: str
    description: str
    created_at: str
    created_at_display: str
    expires_at: str
    expires_at_display: str
    reference_url: str
    scope_name: str = ""


@dataclass(frozen=True)
class ContextResolution:
    """Resolved organization/workspace/actor context for a GUID."""

    scope_type: ScopeType
    scope_id: str
    organization_id: str
    scope_name: str = ""
    workspace_id: str | None = None
    workspace_name: str = ""
    organization_name: str = ""
    actor_id: str | None = None
    actor_type: str = ""
    customer_tier: str = ""


@dataclass(frozen=True)
class CurrentVersionState:
    """Current version context for a connector and scope."""

    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    latest_version: str
    active_version: str
    is_version_pinned: bool
    active_scope: ScopeType | None
    active_scope_id: str | None
    ancestor_configurations: tuple[ScopedConfiguration, ...]
    descendant_configurations: tuple[ScopedConfiguration, ...]


def version_override_tool_name(
    scope_type: ScopeType,
) -> VersionOverrideToolName:
    """Return the override tool name for `scope_type`."""
    return "set_version_override"


def build_version_override_payload(
    plan: OverridePlan,
) -> VersionOverridePayload:
    """Build a typed payload for a connector version override plan."""
    if plan.scope_type == "actor":
        target = VersionOverrideTargetPayload(
            scope="actor",
            organization_id=plan.organization_id,
            connector_type=plan.connector_type,
            workspace_id=plan.workspace_id,
            actor_id=plan.actor_id,
        )
    elif plan.scope_type == "workspace":
        target = VersionOverrideTargetPayload(
            scope="workspace",
            organization_id=plan.organization_id,
            connector_type=plan.connector_type,
            workspace_id=plan.workspace_id,
            connector_name=plan.connector_name,
        )
    else:
        target = VersionOverrideTargetPayload(
            scope="organization",
            organization_id=plan.organization_id,
            connector_type=plan.connector_type,
            connector_name=plan.connector_name,
        )
    return VersionOverridePayload(
        target=target,
        version=None if plan.action == "unset" else plan.version,
        unset=plan.action == "unset",
        override_reason=plan.override_reason or None,
        override_reason_reference_url=plan.override_reason_reference_url or None,
        approval_comment_url=plan.approval_comment_url or None,
        ai_agent_session_url=None,
        user_email=plan.user_email,
        force=plan.force,
        customer_tier_filter=plan.customer_tier_filter,
    )
