# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for querying the Airbyte Cloud Prod DB Replica.

This module provides MCP tools that wrap the query functions from
airbyte_ops_mcp.prod_db_access.queries for use by AI agents.

## MCP reference

.. include:: ../../../docs/mcp-generated/prod_db_queries.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import json
from datetime import datetime, timezone
from enum import StrEnum
from typing import Annotated, Any

from airbyte.exceptions import PyAirbyteInputError
from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.cloud_admin.registry_lookup import (
    resolve_canonical_name_to_definition_id,
)
from airbyte_ops_mcp.constants import OrganizationAliasEnum, WorkspaceAliasEnum
from airbyte_ops_mcp.prod_db_access.queries import (
    is_source_connector,
    query_actors_pinned_to_version,
    query_connection_sync_activity_from_prod,
    query_connections_by_connector,
    query_connections_by_destination_connector,
    query_connections_by_stream,
    query_connector_rollouts,
    query_connector_versions,
    query_dataplanes_list,
    query_destination_connection_stats,
    query_failed_sync_attempts_for_connector,
    query_new_connector_releases,
    query_recent_syncs_for_connector,
    query_source_connection_stats,
    query_syncs_for_connector_version,
    query_versions_with_pins,
    query_workspace_info,
    query_workspaces_by_email_domain,
    resolve_version_id_by_tag,
    resolve_version_info,
    search_organizations,
    search_workspaces,
)
from airbyte_ops_mcp.tier_cache import (
    TierFilter,
    enrich_rows_by_org,
    filter_rows_by_tier,
    get_org_tiers,
)


class StatusFilter(StrEnum):
    """Filter for job status in sync queries."""

    ALL = "all"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


# Cloud UI base URL for building connection URLs
CLOUD_UI_BASE_URL = "https://cloud.airbyte.com"


def _validate_sync_activity_scope(
    *,
    organization_id: str | None,
    workspace_id: str | None,
    connection_ids: list[str] | None,
) -> None:
    """Require at least one explicit scope filter for sync activity queries."""
    if organization_id or workspace_id or connection_ids:
        return
    raise PyAirbyteInputError(
        message=(
            "Provide at least one scope filter: `organization_id`, `workspace_id`, "
            "or `connection_ids`."
        ),
        context={
            "organization_id": organization_id,
            "workspace_id": workspace_id,
            "connection_ids": connection_ids,
        },
    )


def _validate_sync_activity_window(
    *,
    start_at: datetime,
    end_at: datetime,
) -> tuple[datetime, datetime]:
    """Validate that `start_at` and `end_at` describe a usable window.

    Returns the timestamps normalized to UTC. Raises `PyAirbyteInputError` for
    naive timestamps or inverted ranges. No clock-relative caps are enforced
    here; the caller is trusted to choose a sensible window.
    """
    if start_at.tzinfo is None or end_at.tzinfo is None:
        raise PyAirbyteInputError(
            message="`start_at` and `end_at` must include timezone information.",
            context={
                "start_at": start_at.isoformat(),
                "end_at": end_at.isoformat(),
            },
        )

    normalized_start = start_at.astimezone(timezone.utc)
    normalized_end = end_at.astimezone(timezone.utc)

    if normalized_start >= normalized_end:
        raise PyAirbyteInputError(
            message="`start_at` must be earlier than `end_at`.",
            context={
                "start_at": normalized_start.isoformat(),
                "end_at": normalized_end.isoformat(),
            },
        )
    return normalized_start, normalized_end


# =============================================================================
# Pydantic Models for MCP Tool Responses
# =============================================================================


class OrganizationSearchHit(BaseModel):
    """A single organization returned by a name/email search."""

    organization_id: str = Field(description="The organization UUID")
    organization_name: str = Field(description="The name of the organization")
    email: str | None = Field(
        default=None, description="The email address associated with the organization"
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier (TIER_0, TIER_1, or TIER_2). Enriched from BigQuery tier cache.",
    )


class OrganizationSearchResult(BaseModel):
    """Result of searching organizations by name substring."""

    name_contains: str = Field(description="The search substring that was used")
    total_found: int = Field(description="Total number of organizations matching")
    organizations: list[OrganizationSearchHit] = Field(
        description="List of matching organizations"
    )


class WorkspaceInfo(BaseModel):
    """Information about a workspace."""

    organization_id: str = Field(description="The organization UUID")
    workspace_id: str = Field(description="The workspace UUID")
    workspace_name: str = Field(description="The name of the workspace")
    slug: str | None = Field(
        default=None, description="The workspace slug (URL-friendly identifier)"
    )
    email: str | None = Field(
        default=None, description="The email address associated with the workspace"
    )
    dataplane_group_id: str | None = Field(
        default=None, description="The dataplane group UUID (region)"
    )
    dataplane_name: str | None = Field(
        default=None, description="The name of the dataplane (e.g., 'US', 'EU')"
    )
    created_at: datetime | None = Field(
        default=None, description="When the workspace was created"
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier (TIER_0, TIER_1, or TIER_2). Enriched from BigQuery tier cache.",
    )
    is_eu: bool | None = Field(
        default=None,
        description="Whether the workspace is in the EU region (derived from dataplane_name).",
    )


class WorkspaceSearchResult(BaseModel):
    """Result of searching workspaces by name or email domain."""

    name_contains: str | None = Field(
        default=None, description="The name substring that was searched for"
    )
    email_domain: str | None = Field(
        default=None,
        description="The email domain that was searched for (e.g., 'motherduck.com')",
    )
    total_workspaces_found: int = Field(
        description="Total number of workspaces matching"
    )
    unique_organization_ids: list[str] = Field(
        description="List of unique organization IDs found"
    )
    workspaces: list[WorkspaceInfo] = Field(description="List of matching workspaces")


# Keep backward-compatible alias for any external references
WorkspacesByEmailDomainResult = WorkspaceSearchResult


class LatestAttemptBreakdown(BaseModel):
    """Breakdown of connections by latest attempt status."""

    succeeded: int = Field(
        default=0, description="Connections where latest attempt succeeded"
    )
    failed: int = Field(
        default=0, description="Connections where latest attempt failed"
    )
    cancelled: int = Field(
        default=0, description="Connections where latest attempt was cancelled"
    )
    running: int = Field(
        default=0, description="Connections where latest attempt is still running"
    )
    unknown: int = Field(
        default=0,
        description="Connections with no recent attempts in the lookback window",
    )


class VersionPinStats(BaseModel):
    """Stats for connections pinned to a specific version."""

    pinned_version_id: str | None = Field(
        description="The connector version UUID (None for unpinned connections)"
    )
    docker_image_tag: str | None = Field(
        default=None, description="The docker image tag for this version"
    )
    total_connections: int = Field(description="Total number of connections")
    enabled_connections: int = Field(
        description="Number of enabled (active status) connections"
    )
    active_connections: int = Field(
        description="Number of connections with recent sync activity"
    )
    latest_attempt: LatestAttemptBreakdown = Field(
        description="Breakdown by latest attempt status"
    )


class ConnectorConnectionStats(BaseModel):
    """Aggregate connection stats for a connector."""

    connector_definition_id: str = Field(description="The connector definition UUID")
    connector_type: str = Field(description="'source' or 'destination'")
    canonical_name: str | None = Field(
        default=None, description="The canonical connector name if resolved"
    )
    total_connections: int = Field(
        description="Total number of non-deprecated connections"
    )
    enabled_connections: int = Field(
        description="Number of enabled (active status) connections"
    )
    active_connections: int = Field(
        description="Number of connections with recent sync activity"
    )
    pinned_connections: int = Field(
        description="Number of connections with explicit version pins"
    )
    unpinned_connections: int = Field(
        description="Number of connections on default version"
    )
    latest_attempt: LatestAttemptBreakdown = Field(
        description="Overall breakdown by latest attempt status"
    )
    by_version: list[VersionPinStats] = Field(
        description="Stats broken down by pinned version"
    )


class ConnectorConnectionStatsResponse(BaseModel):
    """Response containing connection stats for multiple connectors."""

    sources: list[ConnectorConnectionStats] = Field(
        default_factory=list, description="Stats for source connectors"
    )
    destinations: list[ConnectorConnectionStats] = Field(
        default_factory=list, description="Stats for destination connectors"
    )
    lookback_days: int = Field(
        description="Lookback window used for 'active' connections"
    )
    generated_at: datetime = Field(description="When this response was generated")


def _opt_str(value: Any) -> str | None:
    """Convert a nullable value to str, returning None if the value is None/falsy."""
    return str(value) if value else None


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_dataplanes() -> list[dict[str, Any]]:
    """List all dataplane groups with workspace counts.

    Returns information about all active dataplane groups in Airbyte Cloud,
    including the number of workspaces in each. Useful for understanding
    the distribution of workspaces across regions (US, US-Central, EU).

    Returns list of dicts with keys: dataplane_group_id, dataplane_name,
    organization_id, enabled, tombstone, created_at, workspace_count
    """
    return query_dataplanes_list()


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_workspace_info(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="Workspace UUID or alias to look up. "
            "Accepts '@devin-ai-sandbox' as an alias for the Devin AI sandbox workspace."
        ),
    ],
) -> dict[str, Any] | None:
    """Get workspace information including dataplane group.

    Returns details about a specific workspace, including which dataplane
    (region) it belongs to. Useful for determining if a workspace is in
    the EU region for filtering purposes.

    Returns dict with keys: workspace_id, workspace_name, slug, organization_id,
    dataplane_group_id, dataplane_name, created_at, tombstone
    Or None if workspace not found.
    """
    # Resolve workspace ID alias (workspace_id is required, so resolved value is never None)
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    assert resolved_workspace_id is not None  # Type narrowing: workspace_id is required

    return query_workspace_info(resolved_workspace_id)


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_connector_versions(
    connector_definition_id: Annotated[
        str,
        Field(description="Connector definition UUID to list versions for"),
    ],
) -> list[dict[str, Any]]:
    """List all versions for a connector definition.

    Returns all published versions of a connector, ordered by last_published
    date descending. Useful for understanding version history and finding
    specific version IDs for pinning or rollout monitoring.

    Returns list of dicts with keys: version_id, docker_image_tag, docker_repository,
    release_stage, support_level, cdk_version, language, last_published, release_date
    """
    return query_connector_versions(connector_definition_id)


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_new_connector_releases(
    days: Annotated[
        int,
        Field(description="Number of days to look back (default: 7)", default=7),
    ] = 7,
    limit: Annotated[
        int,
        Field(description="Maximum number of results (default: 100)", default=100),
    ] = 100,
) -> list[dict[str, Any]]:
    """List recently published connector versions.

    Returns connector versions published within the specified number of days.
    Uses last_published timestamp which reflects when the version was actually
    deployed to the registry (not the changelog date).

    Returns list of dicts with keys: version_id, connector_definition_id, docker_repository,
    docker_image_tag, last_published, release_date, release_stage, support_level,
    cdk_version, language, created_at
    """
    return query_new_connector_releases(days=days, limit=limit)


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_actors_by_pinned_connector_version(
    connector_version_id: Annotated[
        str,
        Field(description="Connector version UUID to find pinned instances for"),
    ],
) -> list[dict[str, Any]]:
    """List actors (sources/destinations) effectively pinned to a specific connector version.

    Returns all actors that are effectively pinned to a specific connector version,
    considering all scope levels: actor-level pins, workspace-level pins, and
    organization-level pins (with actor > workspace > organization precedence).
    Useful for monitoring rollouts and understanding which customers are affected.

    The actor_id field is the actor ID (superset of source_id/destination_id).

    Returns list of dicts with keys: actor_id, connector_definition_id, origin_type,
    origin, description, created_at, expires_at, pin_scope_type, actor_name,
    workspace_id, workspace_name, organization_id, dataplane_group_id, dataplane_name

    pin_scope_type is 'actor', 'workspace', or 'organization' indicating which scope
    level the effective pin came from.
    """
    return query_actors_pinned_to_version(connector_version_id)


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_recent_syncs_for_connector_version(
    connector_version_id: Annotated[
        str | None,
        Field(
            description=(
                "Connector version UUID. Provide this OR "
                "connector_name + connector_version."
            ),
            default=None,
        ),
    ] = None,
    connector_name: Annotated[
        str | None,
        Field(
            description=(
                "Canonical connector name (e.g. `source-pokeapi`, "
                "`destination-duckdb`). Used with `connector_version` to "
                "resolve the version UUID."
            ),
            default=None,
        ),
    ] = None,
    connector_version: Annotated[
        str | None,
        Field(
            description=(
                "Semver version tag (e.g. `0.3.59`). "
                "Used with `connector_name` to resolve the version UUID."
            ),
            default=None,
        ),
    ] = None,
    days: Annotated[
        int,
        Field(description="Number of days to look back (default: 7)", default=7),
    ] = 7,
    limit: Annotated[
        int,
        Field(description="Maximum number of results (default: 100)", default=100),
    ] = 100,
    successful_only: Annotated[
        bool,
        Field(
            description="If `True`, only return successful syncs (default: `False`)",
            default=False,
        ),
    ] = False,
) -> list[dict[str, Any]]:
    """List sync jobs that were run with a specific connector version.

    Works for both source and destination connectors. Automatically detects
    the connector type from the version metadata and uses the appropriate
    query variant.

    Accepts either `connector_version_id` (UUID) or `connector_name` +
    `connector_version` (e.g. `source-pokeapi` + `0.3.59`). When using
    name + version, the `docker_repository` is derived from the canonical
    name (e.g. `source-pokeapi` → `airbyte/source-pokeapi`).

    Filters on the version stamped into `jobs.config` at job-creation time,
    not the current pin state. This avoids false positives (pre-pin syncs
    counted as RC) and false negatives (post-unpin syncs missed).

    Pin columns (`pin_origin_type`, `pin_origin`, `pin_scope_type`) are
    still included as informational output but are not used for filtering.

    Returns list of dicts with keys: `job_id`, `connection_id`, `job_status`,
    `started_at`, `job_updated_at`, `connection_name`, `actor_id`, `actor_name`,
    `actor_definition_id`, `source_definition_version_id`,
    `destination_definition_version_id`, `pin_origin_type`,
    `pin_origin`, `pin_scope_type`, `workspace_id`, `workspace_name`,
    `organization_id`, `dataplane_group_id`, `dataplane_name`.
    """
    # Resolve inputs to a version UUID and connector type.
    if connector_version_id is not None:
        version_info = resolve_version_info(connector_version_id)
        docker_repository = version_info["docker_repository"]
    elif connector_name is not None and connector_version is not None:
        # Derive docker_repository from canonical name.
        docker_repository = f"airbyte/{connector_name}"
        version_info = resolve_version_id_by_tag(
            docker_repository=docker_repository,
            docker_image_tag=connector_version,
        )
        connector_version_id = version_info["version_id"]
    else:
        raise PyAirbyteInputError(
            message=(
                "Provide either `connector_version_id` or both "
                "`connector_name` and `connector_version`."
            ),
        )

    is_destination = not is_source_connector(docker_repository)
    return query_syncs_for_connector_version(
        connector_version_id,
        is_destination=is_destination,
        days=days,
        limit=limit,
        successful_only=successful_only,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def query_prod_recent_syncs_for_connector(
    source_definition_id: Annotated[
        str | None,
        Field(
            description=(
                "Source connector definition ID (UUID) to search for. "
                "Provide this OR source_canonical_name OR destination_definition_id "
                "OR destination_canonical_name (exactly one required). "
                "Example: 'afa734e4-3571-11ec-991a-1e0031268139' for YouTube Analytics."
            ),
            default=None,
        ),
    ],
    source_canonical_name: Annotated[
        str | None,
        Field(
            description=(
                "Canonical source connector name to search for. "
                "Provide this OR source_definition_id OR destination_definition_id "
                "OR destination_canonical_name (exactly one required). "
                "Examples: 'source-youtube-analytics', 'YouTube Analytics'."
            ),
            default=None,
        ),
    ],
    destination_definition_id: Annotated[
        str | None,
        Field(
            description=(
                "Destination connector definition ID (UUID) to search for. "
                "Provide this OR destination_canonical_name OR source_definition_id "
                "OR source_canonical_name (exactly one required). "
                "Example: '94bd199c-2ff0-4aa2-b98e-17f0acb72610' for DuckDB."
            ),
            default=None,
        ),
    ],
    destination_canonical_name: Annotated[
        str | None,
        Field(
            description=(
                "Canonical destination connector name to search for. "
                "Provide this OR destination_definition_id OR source_definition_id "
                "OR source_canonical_name (exactly one required). "
                "Examples: 'destination-duckdb', 'DuckDB'."
            ),
            default=None,
        ),
    ],
    status_filter: Annotated[
        StatusFilter,
        Field(
            description=(
                "Filter by job status: 'all' (default), 'succeeded', or 'failed'. "
                "Use 'succeeded' to find healthy connections with recent successful syncs. "
                "Use 'failed' to find connections with recent failures."
            ),
            default=StatusFilter.ALL,
        ),
    ],
    organization_id: Annotated[
        str | OrganizationAliasEnum | None,
        Field(
            description=(
                "Optional organization ID (UUID) or alias to filter results. "
                "If provided, only syncs from this organization will be returned. "
                "Accepts '@airbyte-internal' as an alias for the Airbyte internal org."
            ),
            default=None,
        ),
    ],
    lookback_days: Annotated[
        int,
        Field(description="Number of days to look back (default: 7)", default=7),
    ],
    limit: Annotated[
        int,
        Field(description="Maximum number of results (default: 100)", default=100),
    ],
    customer_tier_filter: Annotated[
        TierFilter,
        Field(
            description=(
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', or 'ALL'. "
                "Filters results to only include connections belonging to organizations "
                "in the specified tier. Use 'ALL' to include all tiers."
            ),
        ),
    ] = "TIER_2",
    *,
    exclude_pinned: Annotated[
        bool,
        Field(
            description=(
                "If True, exclude syncs for actors that are already pinned to a "
                "specific version (at any scope level: actor, workspace, or organization). "
                "Useful for 'prove fix' workflows where you want to find unpinned "
                "connections for live testing. Default: False (include all syncs)."
            ),
            default=False,
        ),
    ],
    enabled_schedules_only: Annotated[
        bool,
        Field(
            description=(
                "If True, only return syncs for connections that are both active "
                "(not paused/inactive) and on an automated sync schedule "
                "(not manual-trigger-only). Useful for canary workflows where "
                "you need connections that will produce organic syncs during a "
                "monitoring window. Default: False (include all connections)."
            ),
            default=False,
        ),
    ],
) -> list[dict[str, Any]]:
    """List recent sync jobs for ALL actors using a connector type.

    This tool finds all actors with the given connector definition and returns their
    recent sync jobs, regardless of whether they have explicit version pins. It filters
    out deleted actors, deleted workspaces, and deprecated connections.

    Results are always enriched with customer_tier and is_eu fields.
    The customer_tier_filter parameter is required to ensure tier-aware querying.

    Use this tool to:
    - Find healthy connections with recent successful syncs (status_filter='succeeded')
    - Investigate connector issues across all users (status_filter='failed')
    - Get an overview of all recent sync activity (status_filter='all')

    Set `exclude_pinned=True` to filter out syncs for actors that are already pinned to a
    specific version. This is useful for 'prove fix' live connection testing workflows
    where you want to find unpinned connections to test against.

    Set `enabled_schedules_only=True` to restrict results to connections that are both
    enabled (status='active') and on an automated schedule (not manual-trigger-only).
    This is useful for canary prerelease workflows where you need connections that
    will run organically during the monitoring window.

    Supports both SOURCE and DESTINATION connectors. Provide exactly one of:
    source_definition_id, source_canonical_name, destination_definition_id,
    or destination_canonical_name.

    Key fields in results:
    - job_status: 'succeeded', 'failed', 'cancelled', etc.
    - connection_id, connection_name: The connection that ran the sync
    - actor_id, actor_name: The source or destination actor
    - customer_tier: TIER_0, TIER_1, or TIER_2
    - is_eu: Whether the workspace is in the EU region
    - pin_origin_type, pin_origin, pinned_version_id: Version pin context (NULL if not pinned)
    - pin_scope_type: 'actor', 'workspace', or 'organization' (NULL if not pinned)
    """
    # Validate that exactly one connector parameter is provided
    provided_params = [
        source_definition_id,
        source_canonical_name,
        destination_definition_id,
        destination_canonical_name,
    ]
    num_provided = sum(p is not None for p in provided_params)
    if num_provided != 1:
        raise PyAirbyteInputError(
            message=(
                "Exactly one of source_definition_id, source_canonical_name, "
                "destination_definition_id, or destination_canonical_name must be provided."
            ),
        )

    # Determine if this is a destination connector
    is_destination = (
        destination_definition_id is not None or destination_canonical_name is not None
    )

    # Resolve canonical name to definition ID if needed
    resolved_definition_id: str
    if source_canonical_name:
        resolved_definition_id = resolve_canonical_name_to_definition_id(
            canonical_name=source_canonical_name,
        )
    elif destination_canonical_name:
        resolved_definition_id = resolve_canonical_name_to_definition_id(
            canonical_name=destination_canonical_name,
        )
    elif source_definition_id:
        resolved_definition_id = source_definition_id
    else:
        # We've validated exactly one param is provided, so this must be set
        assert destination_definition_id is not None
        resolved_definition_id = destination_definition_id

    # Resolve organization ID alias
    resolved_organization_id = OrganizationAliasEnum.resolve(organization_id)

    rows = query_recent_syncs_for_connector(
        connector_definition_id=resolved_definition_id,
        is_destination=is_destination,
        status_filter=status_filter,
        organization_id=resolved_organization_id,
        days=lookback_days,
        limit=limit,
        exclude_pinned=exclude_pinned,
        enabled_schedules_only=enabled_schedules_only,
    )

    enriched = enrich_rows_by_org(rows)
    return filter_rows_by_tier(enriched, customer_tier_filter)


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def query_prod_failed_sync_attempts_for_connector(
    source_definition_id: Annotated[
        str | None,
        Field(
            description=(
                "Source connector definition ID (UUID) to search for. "
                "Exactly one of this or source_canonical_name is required. "
                "Example: 'afa734e4-3571-11ec-991a-1e0031268139' for YouTube Analytics."
            ),
            default=None,
        ),
    ] = None,
    source_canonical_name: Annotated[
        str | None,
        Field(
            description=(
                "Canonical source connector name to search for. "
                "Exactly one of this or source_definition_id is required. "
                "Examples: 'source-youtube-analytics', 'YouTube Analytics'."
            ),
            default=None,
        ),
    ] = None,
    organization_id: Annotated[
        str | OrganizationAliasEnum | None,
        Field(
            description=(
                "Optional organization ID (UUID) or alias to filter results. "
                "If provided, only failed attempts from this organization will be returned. "
                "Accepts '@airbyte-internal' as an alias for the Airbyte internal org."
            ),
            default=None,
        ),
    ] = None,
    lookback_days: Annotated[
        int,
        Field(description="Number of days to look back (default: 7)", default=7),
    ] = 7,
    limit: Annotated[
        int,
        Field(description="Maximum number of results (default: 100)", default=100),
    ] = 100,
    customer_tier_filter: Annotated[
        TierFilter,
        Field(
            description=(
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', or 'ALL'. "
                "Filters results to only include connections belonging to organizations "
                "in the specified tier. Use 'ALL' to include all tiers."
            ),
        ),
    ] = "TIER_2",
) -> list[dict[str, Any]]:
    """List failed sync attempts for ALL actors using a source connector type.

    This tool finds all actors with the given connector definition and returns their
    failed sync attempts, regardless of whether they have explicit version pins.

    Results are always enriched with customer_tier and is_eu fields.
    The customer_tier_filter parameter is required to ensure tier-aware querying.

    This is useful for investigating connector issues across all users. Use this when
    you want to find failures for a connector type regardless of which version users
    are on.

    Note: This tool only supports SOURCE connectors. For destination connectors,
    a separate tool would be needed.

    Key fields in results:
    - failure_summary: JSON containing failure details including failureType and messages
    - customer_tier: TIER_0, TIER_1, or TIER_2
    - is_eu: Whether the workspace is in the EU region
    - pin_origin_type, pin_origin, pinned_version_id: Version pin context (NULL if not pinned)
    - pin_scope_type: 'actor', 'workspace', or 'organization' (NULL if not pinned)
    """
    # Validate that exactly one of the two parameters is provided
    if (source_definition_id is None) == (source_canonical_name is None):
        raise PyAirbyteInputError(
            message=(
                "Exactly one of source_definition_id or source_canonical_name "
                "must be provided, but not both."
            ),
        )

    # Resolve canonical name to definition ID if needed
    resolved_definition_id: str
    if source_canonical_name:
        resolved_definition_id = resolve_canonical_name_to_definition_id(
            canonical_name=source_canonical_name,
        )
    else:
        resolved_definition_id = source_definition_id  # type: ignore[assignment]

    # Resolve organization ID alias
    resolved_organization_id = OrganizationAliasEnum.resolve(organization_id)

    rows = query_failed_sync_attempts_for_connector(
        connector_definition_id=resolved_definition_id,
        organization_id=resolved_organization_id,
        days=lookback_days,
        limit=limit,
    )
    enriched = enrich_rows_by_org(rows)
    return filter_rows_by_tier(enriched, customer_tier_filter)


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def query_prod_connections_by_connector(
    source_definition_id: Annotated[
        str | None,
        Field(
            description=(
                "Source connector definition ID (UUID) to search for. "
                "Exactly one of source_definition_id, source_canonical_name, "
                "destination_definition_id, or destination_canonical_name is required. "
                "Example: 'afa734e4-3571-11ec-991a-1e0031268139' for YouTube Analytics."
            ),
            default=None,
        ),
    ] = None,
    source_canonical_name: Annotated[
        str | None,
        Field(
            description=(
                "Canonical source connector name to search for. "
                "Exactly one of source_definition_id, source_canonical_name, "
                "destination_definition_id, or destination_canonical_name is required. "
                "Examples: 'source-youtube-analytics', 'YouTube Analytics'."
            ),
            default=None,
        ),
    ] = None,
    destination_definition_id: Annotated[
        str | None,
        Field(
            description=(
                "Destination connector definition ID (UUID) to search for. "
                "Exactly one of source_definition_id, source_canonical_name, "
                "destination_definition_id, or destination_canonical_name is required. "
                "Example: 'e5c8e66c-a480-4a5e-9c0e-e8e5e4c5c5c5' for DuckDB."
            ),
            default=None,
        ),
    ] = None,
    destination_canonical_name: Annotated[
        str | None,
        Field(
            description=(
                "Canonical destination connector name to search for. "
                "Exactly one of source_definition_id, source_canonical_name, "
                "destination_definition_id, or destination_canonical_name is required. "
                "Examples: 'destination-duckdb', 'DuckDB'."
            ),
            default=None,
        ),
    ] = None,
    organization_id: Annotated[
        str | OrganizationAliasEnum | None,
        Field(
            description=(
                "Optional organization ID (UUID) or alias to filter results. "
                "If provided, only connections in this organization will be returned. "
                "Accepts '@airbyte-internal' as an alias for the Airbyte internal org."
            ),
            default=None,
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Maximum number of results (default: 1000)", default=1000),
    ] = 1000,
    customer_tier_filter: Annotated[
        TierFilter,
        Field(
            description=(
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', or 'ALL'. "
                "Filters results to only include connections belonging to organizations "
                "in the specified tier. Use 'ALL' to include all tiers."
            ),
        ),
    ] = "TIER_2",
    *,
    exclude_pinned: Annotated[
        bool,
        Field(
            description=(
                "If True, exclude connections whose connector is already pinned to a "
                "specific version (at any scope level: actor, workspace, or organization). "
                "Useful for 'prove fix' workflows where you want to find unpinned "
                "connections for live testing. Default: False (include all connections)."
            ),
            default=False,
        ),
    ],
    enabled_schedules_only: Annotated[
        bool,
        Field(
            description=(
                "If True, only return connections that are both active "
                "(not paused/inactive) and on an automated sync schedule "
                "(not manual-trigger-only). Useful for canary workflows where "
                "you need connections that will produce organic syncs during a "
                "monitoring window. Default: False (include all connections)."
            ),
            default=False,
        ),
    ],
) -> list[dict[str, Any]]:
    """Search for all connections using a specific source or destination connector type.

    This tool queries the Airbyte Cloud Prod DB Replica directly for fast results.
    It finds all connections where the source or destination connector matches the
    specified type, regardless of how the connector is named by users.

    Results are always enriched with customer_tier and is_eu fields.
    The customer_tier_filter parameter is required to ensure tier-aware querying.

    Optionally filter by organization_id to limit results to a specific organization.
    Use '@airbyte-internal' as an alias for the Airbyte internal organization.

    Set `exclude_pinned=True` to filter out connections that are already pinned to a
    specific version. This is useful for 'prove fix' live connection testing workflows
    where you want to find unpinned connections to test against.

    Set `enabled_schedules_only=True` to restrict results to connections that are both
    enabled (status='active') and on an automated schedule (not manual-trigger-only).
    This is useful for canary prerelease workflows where you need connections that
    will run organically during the monitoring window.

    Returns a list of connection dicts with workspace context and clickable Cloud UI URLs.
    For source queries, returns: connection_id, connection_name, connection_url, source_id,
    source_name, source_definition_id, workspace_id, workspace_name, organization_id,
    dataplane_group_id, dataplane_name, pin_origin_type, pin_origin, pinned_version_id,
    pin_scope_type, customer_tier, is_eu.
    For destination queries, returns: connection_id, connection_name, connection_url,
    destination_id, destination_name, destination_definition_id, workspace_id,
    workspace_name, organization_id, dataplane_group_id, dataplane_name, pin_origin_type,
    pin_origin, pinned_version_id, pin_scope_type, customer_tier, is_eu.

    pin_scope_type is 'actor', 'workspace', or 'organization' indicating which scope
    level the effective pin came from (NULL if not pinned).
    """
    # Validate that exactly one of the four connector parameters is provided
    provided_params = [
        source_definition_id,
        source_canonical_name,
        destination_definition_id,
        destination_canonical_name,
    ]
    num_provided = sum(p is not None for p in provided_params)
    if num_provided != 1:
        raise PyAirbyteInputError(
            message=(
                "Exactly one of source_definition_id, source_canonical_name, "
                "destination_definition_id, or destination_canonical_name must be provided."
            ),
        )

    # Determine if this is a source or destination query and resolve the definition ID
    is_source_query = (
        source_definition_id is not None or source_canonical_name is not None
    )
    resolved_definition_id: str

    if source_canonical_name:
        resolved_definition_id = resolve_canonical_name_to_definition_id(
            canonical_name=source_canonical_name,
        )
    elif source_definition_id:
        resolved_definition_id = source_definition_id
    elif destination_canonical_name:
        resolved_definition_id = resolve_canonical_name_to_definition_id(
            canonical_name=destination_canonical_name,
        )
    else:
        resolved_definition_id = destination_definition_id  # type: ignore[assignment]

    # Resolve organization ID alias
    resolved_organization_id = OrganizationAliasEnum.resolve(organization_id)

    # Query the database based on connector type
    if is_source_query:
        rows = [
            {
                "organization_id": str(row.get("organization_id", "")),
                "workspace_id": str(row["workspace_id"]),
                "workspace_name": row.get("workspace_name", ""),
                "connection_id": str(row["connection_id"]),
                "connection_name": row.get("connection_name", ""),
                "connection_url": (
                    f"{CLOUD_UI_BASE_URL}/workspaces/{row['workspace_id']}"
                    f"/connections/{row['connection_id']}/status"
                ),
                "source_id": str(row["source_id"]),
                "source_name": row.get("source_name", ""),
                "source_definition_id": str(row["source_definition_id"]),
                "dataplane_group_id": str(row.get("dataplane_group_id", "")),
                "dataplane_name": row.get("dataplane_name", ""),
                "pin_origin_type": row.get("pin_origin_type"),
                "pin_origin": row.get("pin_origin"),
                "pinned_version_id": _opt_str(row.get("pinned_version_id")),
                "pin_scope_type": row.get("pin_scope_type"),
            }
            for row in query_connections_by_connector(
                connector_definition_id=resolved_definition_id,
                organization_id=resolved_organization_id,
                limit=limit,
                exclude_pinned=exclude_pinned,
                enabled_schedules_only=enabled_schedules_only,
            )
        ]
    else:
        # Destination query
        rows = [
            {
                "organization_id": str(row.get("organization_id", "")),
                "workspace_id": str(row["workspace_id"]),
                "workspace_name": row.get("workspace_name", ""),
                "connection_id": str(row["connection_id"]),
                "connection_name": row.get("connection_name", ""),
                "connection_url": (
                    f"{CLOUD_UI_BASE_URL}/workspaces/{row['workspace_id']}"
                    f"/connections/{row['connection_id']}/status"
                ),
                "destination_id": str(row["destination_id"]),
                "destination_name": row.get("destination_name", ""),
                "destination_definition_id": str(row["destination_definition_id"]),
                "dataplane_group_id": str(row.get("dataplane_group_id", "")),
                "dataplane_name": row.get("dataplane_name", ""),
                "pin_origin_type": row.get("pin_origin_type"),
                "pin_origin": row.get("pin_origin"),
                "pinned_version_id": _opt_str(row.get("pinned_version_id")),
                "pin_scope_type": row.get("pin_scope_type"),
            }
            for row in query_connections_by_destination_connector(
                connector_definition_id=resolved_definition_id,
                organization_id=resolved_organization_id,
                limit=limit,
                exclude_pinned=exclude_pinned,
                enabled_schedules_only=enabled_schedules_only,
            )
        ]

    enriched = enrich_rows_by_org(rows)
    return filter_rows_by_tier(enriched, customer_tier_filter)


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def query_prod_connections_by_stream(
    stream_name: Annotated[
        str,
        Field(
            description=(
                "Name of the stream to search for in connection catalogs. "
                "This must match the exact stream name as configured in the connection. "
                "Examples: 'global_exclusions', 'campaigns', 'users'."
            ),
        ),
    ],
    source_definition_id: Annotated[
        str | None,
        Field(
            description=(
                "Source connector definition ID (UUID) to search for. "
                "Provide this OR source_canonical_name (exactly one required). "
                "Example: 'afa734e4-3571-11ec-991a-1e0031268139' for YouTube Analytics."
            ),
            default=None,
        ),
    ],
    source_canonical_name: Annotated[
        str | None,
        Field(
            description=(
                "Canonical source connector name to search for. "
                "Provide this OR source_definition_id (exactly one required). "
                "Examples: 'source-klaviyo', 'Klaviyo', 'source-youtube-analytics'."
            ),
            default=None,
        ),
    ],
    organization_id: Annotated[
        str | OrganizationAliasEnum | None,
        Field(
            description=(
                "Optional organization ID (UUID) or alias to filter results. "
                "If provided, only connections in this organization will be returned. "
                "Accepts '@airbyte-internal' as an alias for the Airbyte internal org."
            ),
            default=None,
        ),
    ],
    limit: Annotated[
        int,
        Field(description="Maximum number of results (default: 100)", default=100),
    ],
    customer_tier_filter: Annotated[
        TierFilter,
        Field(
            description=(
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', or 'ALL'. "
                "Filters results to only include connections belonging to organizations "
                "in the specified tier. Use 'ALL' to include all tiers."
            ),
        ),
    ] = "TIER_2",
) -> list[dict[str, Any]]:
    """Find connections that have a specific stream enabled in their catalog.

    This tool searches the connection's configured catalog (JSONB) for streams
    matching the specified name. It's particularly useful when validating
    connector fixes that affect specific streams - you can quickly find
    customer connections that use the affected stream.

    Results are always enriched with customer_tier and is_eu fields.
    The customer_tier_filter parameter is required to ensure tier-aware querying.

    Use cases:
    - Finding connections with a specific stream enabled for regression testing
    - Validating connector fixes that affect particular streams
    - Identifying which customers use rarely-enabled streams

    Returns a list of connection dicts with workspace context and clickable Cloud UI URLs.
    """
    provided_params = [source_definition_id, source_canonical_name]
    num_provided = sum(p is not None for p in provided_params)
    if num_provided != 1:
        raise PyAirbyteInputError(
            message=(
                "Exactly one of source_definition_id or source_canonical_name "
                "must be provided."
            ),
        )

    resolved_definition_id: str
    if source_canonical_name:
        resolved_definition_id = resolve_canonical_name_to_definition_id(
            canonical_name=source_canonical_name,
        )
    else:
        assert source_definition_id is not None
        resolved_definition_id = source_definition_id

    resolved_organization_id = OrganizationAliasEnum.resolve(organization_id)

    rows = [
        {
            "organization_id": str(row.get("organization_id", "")),
            "workspace_id": str(row["workspace_id"]),
            "workspace_name": row.get("workspace_name", ""),
            "connection_id": str(row["connection_id"]),
            "connection_name": row.get("connection_name", ""),
            "connection_status": row.get("connection_status", ""),
            "connection_url": (
                f"{CLOUD_UI_BASE_URL}/workspaces/{row['workspace_id']}"
                f"/connections/{row['connection_id']}/status"
            ),
            "source_id": str(row["source_id"]),
            "source_name": row.get("source_name", ""),
            "source_definition_id": str(row["source_definition_id"]),
            "dataplane_group_id": str(row.get("dataplane_group_id", "")),
            "dataplane_name": row.get("dataplane_name", ""),
        }
        for row in query_connections_by_stream(
            connector_definition_id=resolved_definition_id,
            stream_name=stream_name,
            organization_id=resolved_organization_id,
            limit=limit,
        )
    ]
    enriched = enrich_rows_by_org(rows)
    return filter_rows_by_tier(enriched, customer_tier_filter)


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_organizations(
    name_contains: Annotated[
        str,
        Field(
            description=(
                "Case-insensitive substring to search for in organization name or email. "
                "For example, 'acme' will match organizations named 'Acme Corp' or "
                "with email 'admin@acme.io'."
            ),
        ),
    ],
    limit: Annotated[
        int,
        Field(
            description="Maximum number of organizations to return (default: 20)",
            default=20,
        ),
    ] = 20,
) -> OrganizationSearchResult:
    """Search organizations by name or email substring.

    Performs a case-insensitive substring match on organization name and email.
    Use the returned `organization_id` values with other tools like
    `query_prod_connections_by_connector` or `lookup_customer_tiers`.
    """
    rows = search_organizations(name_contains=name_contains, limit=limit)

    orgs = [
        OrganizationSearchHit(
            organization_id=str(row["organization_id"]),
            organization_name=row.get("organization_name", ""),
            email=row.get("email"),
        )
        for row in rows
    ]

    # Enrich with tier annotation
    org_ids = [o.organization_id for o in orgs]
    tier_results = {r.organization_id: r for r in get_org_tiers(org_ids)}
    for org in orgs:
        tier_result = tier_results.get(org.organization_id)
        if tier_result:
            org.customer_tier = tier_result.customer_tier

    return OrganizationSearchResult(
        name_contains=name_contains,
        total_found=len(orgs),
        organizations=orgs,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_workspaces(
    name_contains: Annotated[
        str | None,
        Field(
            description=(
                "Case-insensitive substring to search for in workspace name or slug. "
                "For example, 'acme' will match workspaces named 'Acme Staging'."
            ),
            default=None,
        ),
    ] = None,
    email_domain: Annotated[
        str | None,
        Field(
            description=(
                "Email domain to search for (e.g., 'motherduck.com'). "
                "Do not include the '@' symbol."
            ),
            default=None,
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(
            description="Maximum number of workspaces to return (default: 100)",
            default=100,
        ),
    ] = 100,
) -> WorkspaceSearchResult:
    """Search workspaces by name substring or email domain.

    At least one of `name_contains` or `email_domain` must be provided.
    When `name_contains` is given, performs a case-insensitive substring match
    on workspace name and slug. When `email_domain` is given, matches
    workspaces by user email domain.

    The returned organization IDs can be used with other tools like
    `query_prod_connections_by_connector` to find connections within
    those organizations for safe testing.
    """
    if not name_contains and not email_domain:
        raise PyAirbyteInputError(
            message="At least one of `name_contains` or `email_domain` must be provided.",
        )

    if name_contains:
        rows = search_workspaces(name_contains=name_contains, limit=limit)
    else:
        assert email_domain is not None
        clean_domain = email_domain.lstrip("@")
        rows = query_workspaces_by_email_domain(email_domain=clean_domain, limit=limit)

    workspaces = [
        WorkspaceInfo(
            organization_id=str(row["organization_id"]),
            workspace_id=str(row["workspace_id"]),
            workspace_name=row.get("workspace_name", ""),
            slug=row.get("slug"),
            email=row.get("email"),
            dataplane_group_id=_opt_str(row.get("dataplane_group_id")),
            dataplane_name=row.get("dataplane_name"),
            created_at=row.get("created_at"),
        )
        for row in rows
    ]

    # Enrich with tier annotation (annotation only, no filtering)
    unique_org_ids = list(dict.fromkeys(w.organization_id for w in workspaces))
    tier_results = {r.organization_id: r for r in get_org_tiers(unique_org_ids)}
    for ws in workspaces:
        tier_result = tier_results.get(ws.organization_id)
        if tier_result:
            ws.customer_tier = tier_result.customer_tier
        ws.is_eu = ws.dataplane_name == "EU" if ws.dataplane_name else False

    return WorkspaceSearchResult(
        name_contains=name_contains,
        email_domain=email_domain.lstrip("@") if email_domain else None,
        total_workspaces_found=len(workspaces),
        unique_organization_ids=unique_org_ids,
        workspaces=workspaces,
    )


# Backward-compatible alias
query_prod_workspaces_by_email_domain = query_prod_workspaces


def _build_connector_stats(
    connector_definition_id: str,
    connector_type: str,
    canonical_name: str | None,
    rows: list[dict[str, Any]],
    version_tags: dict[str, str | None],
) -> ConnectorConnectionStats:
    """Build ConnectorConnectionStats from query result rows."""
    # Aggregate totals across all version groups
    total_connections = 0
    enabled_connections = 0
    active_connections = 0
    pinned_connections = 0
    unpinned_connections = 0
    total_succeeded = 0
    total_failed = 0
    total_cancelled = 0
    total_running = 0
    total_unknown = 0

    by_version: list[VersionPinStats] = []

    for row in rows:
        version_id = row.get("pinned_version_id")
        row_total = int(row.get("total_connections", 0))
        row_enabled = int(row.get("enabled_connections", 0))
        row_active = int(row.get("active_connections", 0))
        row_pinned = int(row.get("pinned_connections", 0))
        row_unpinned = int(row.get("unpinned_connections", 0))
        row_succeeded = int(row.get("succeeded_connections", 0))
        row_failed = int(row.get("failed_connections", 0))
        row_cancelled = int(row.get("cancelled_connections", 0))
        row_running = int(row.get("running_connections", 0))
        row_unknown = int(row.get("unknown_connections", 0))

        total_connections += row_total
        enabled_connections += row_enabled
        active_connections += row_active
        pinned_connections += row_pinned
        unpinned_connections += row_unpinned
        total_succeeded += row_succeeded
        total_failed += row_failed
        total_cancelled += row_cancelled
        total_running += row_running
        total_unknown += row_unknown

        by_version.append(
            VersionPinStats(
                pinned_version_id=str(version_id) if version_id else None,
                docker_image_tag=version_tags.get(str(version_id))
                if version_id
                else None,
                total_connections=row_total,
                enabled_connections=row_enabled,
                active_connections=row_active,
                latest_attempt=LatestAttemptBreakdown(
                    succeeded=row_succeeded,
                    failed=row_failed,
                    cancelled=row_cancelled,
                    running=row_running,
                    unknown=row_unknown,
                ),
            )
        )

    return ConnectorConnectionStats(
        connector_definition_id=connector_definition_id,
        connector_type=connector_type,
        canonical_name=canonical_name,
        total_connections=total_connections,
        enabled_connections=enabled_connections,
        active_connections=active_connections,
        pinned_connections=pinned_connections,
        unpinned_connections=unpinned_connections,
        latest_attempt=LatestAttemptBreakdown(
            succeeded=total_succeeded,
            failed=total_failed,
            cancelled=total_cancelled,
            running=total_running,
            unknown=total_unknown,
        ),
        by_version=by_version,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def query_prod_connector_connection_stats(
    source_definition_ids: Annotated[
        list[str] | None,
        Field(
            description=(
                "List of source connector definition IDs (UUIDs) to get stats for. "
                "Example: ['afa734e4-3571-11ec-991a-1e0031268139']"
            ),
            default=None,
        ),
    ] = None,
    destination_definition_ids: Annotated[
        list[str] | None,
        Field(
            description=(
                "List of destination connector definition IDs (UUIDs) to get stats for. "
                "Example: ['94bd199c-2ff0-4aa2-b98e-17f0acb72610']"
            ),
            default=None,
        ),
    ] = None,
    lookback_days: Annotated[
        int,
        Field(
            description=(
                "Number of days to look back for 'active' connections (default: 7). "
                "Connections with sync activity within this window are counted as active."
            ),
            default=7,
        ),
    ] = 7,
) -> ConnectorConnectionStatsResponse:
    """Get aggregate connection stats for multiple connectors.

    Returns counts of connections grouped by pinned version for each connector,
    including:
    - Total, enabled, and active connection counts
    - Pinned vs unpinned breakdown
    - Latest attempt status breakdown (succeeded, failed, cancelled, running, unknown)

    This tool is designed for release monitoring workflows. It allows you to:
    1. Query recently released connectors to identify which ones to monitor
    2. Get aggregate stats showing how many connections are using each version
    3. See health metrics (pass/fail) broken down by version

    The `lookback_days` parameter controls the lookback window for:
    - Counting 'active' connections (those with recent sync activity)
    - Determining 'latest attempt status' (most recent attempt within the window)

    Connections with no sync activity in the lookback window will have
    'unknown' status in the latest_attempt breakdown.
    """
    # Initialize empty lists if None
    source_ids = source_definition_ids or []
    destination_ids = destination_definition_ids or []

    if not source_ids and not destination_ids:
        raise PyAirbyteInputError(
            message=(
                "At least one of source_definition_ids or destination_definition_ids "
                "must be provided."
            ),
        )

    sources: list[ConnectorConnectionStats] = []
    destinations: list[ConnectorConnectionStats] = []

    # Process source connectors
    for source_def_id in source_ids:
        # Get version info for tag lookup
        versions = query_connector_versions(source_def_id)
        version_tags = {
            str(v["version_id"]): v.get("docker_image_tag") for v in versions
        }

        # Get aggregate stats
        rows = query_source_connection_stats(source_def_id, days=lookback_days)

        sources.append(
            _build_connector_stats(
                connector_definition_id=source_def_id,
                connector_type="source",
                canonical_name=None,
                rows=rows,
                version_tags=version_tags,
            )
        )

    # Process destination connectors
    for dest_def_id in destination_ids:
        # Get version info for tag lookup
        versions = query_connector_versions(dest_def_id)
        version_tags = {
            str(v["version_id"]): v.get("docker_image_tag") for v in versions
        }

        # Get aggregate stats
        rows = query_destination_connection_stats(dest_def_id, days=lookback_days)

        destinations.append(
            _build_connector_stats(
                connector_definition_id=dest_def_id,
                connector_type="destination",
                canonical_name=None,
                rows=rows,
                version_tags=version_tags,
            )
        )

    return ConnectorConnectionStatsResponse(
        sources=sources,
        destinations=destinations,
        lookback_days=lookback_days,
        generated_at=datetime.now(timezone.utc),
    )


# =============================================================================
# Connector Rollout Models and Tools
# =============================================================================


class ConnectorRolloutInfo(BaseModel):
    """Information about a connector rollout."""

    rollout_id: str = Field(description="The rollout UUID")
    actor_definition_id: str = Field(description="The connector definition UUID")
    state: str = Field(
        description="Rollout state: initialized, workflow_started, in_progress, "
        "paused, finalizing, succeeded, errored, failed_rolled_back, canceled"
    )
    initial_rollout_pct: int | None = Field(
        default=None, description="Initial rollout percentage"
    )
    current_target_rollout_pct: int | None = Field(
        default=None, description="Current target rollout percentage"
    )
    final_target_rollout_pct: int | None = Field(
        default=None, description="Final target rollout percentage"
    )
    has_breaking_changes: bool = Field(
        description="Whether the RC has breaking changes"
    )
    max_step_wait_time_mins: int | None = Field(
        default=None, description="Maximum wait time between rollout steps in minutes"
    )
    rollout_strategy: str | None = Field(
        default=None, description="Rollout strategy: manual, automated, overridden"
    )
    updated_by_user_id: str | None = Field(
        default=None,
        description="User ID recorded as last updating the rollout",
    )
    updated_by_user_name: str | None = Field(
        default=None,
        description="Name recorded as last updating the rollout",
    )
    updated_by_user_email: str | None = Field(
        default=None,
        description="Email recorded as last updating the rollout",
    )
    workflow_run_id: str | None = Field(
        default=None, description="Temporal workflow run ID"
    )
    error_msg: str | None = Field(default=None, description="Error message if errored")
    failed_reason: str | None = Field(
        default=None, description="Reason for failure if failed"
    )
    paused_reason: str | None = Field(
        default=None, description="Reason for pause if paused"
    )
    tag: str | None = Field(default=None, description="Optional tag for the rollout")
    created_at: datetime | None = Field(
        default=None, description="When the rollout was created"
    )
    updated_at: datetime | None = Field(
        default=None, description="When the rollout was last updated"
    )
    completed_at: datetime | None = Field(
        default=None, description="When the rollout completed (if terminal)"
    )
    expires_at: datetime | None = Field(
        default=None, description="When the rollout expires"
    )
    rc_docker_image_tag: str | None = Field(
        default=None, description="Docker image tag of the release candidate"
    )
    rc_docker_repository: str | None = Field(
        default=None, description="Docker repository of the release candidate"
    )
    initial_docker_image_tag: str | None = Field(
        default=None, description="Docker image tag of the initial version"
    )
    initial_docker_repository: str | None = Field(
        default=None, description="Docker repository of the initial version"
    )
    filters: dict[str, Any] | None = Field(
        default=None,
        description="Raw rollout filters JSON (e.g., {'tierFilter': {'tier': 'TIER_0'}})",
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier targeted by this rollout (extracted from filters), "
        "e.g., 'TIER_0', 'TIER_1'. None if no tier filter is set.",
    )


def _parse_rollout_filters(filters_raw: Any) -> dict[str, Any] | None:
    """Parse the rollout filters field from a database row.

    The filters field may be a JSON string, a dict, or None.
    """
    if filters_raw is None:
        return None
    if isinstance(filters_raw, dict):
        return filters_raw
    if isinstance(filters_raw, str):
        try:
            parsed = json.loads(filters_raw)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
    return None


def _extract_tier_from_filters(filters_raw: Any) -> str | None:
    """Extract customer tier from rollout filters JSON.

    Supports two formats:
    - Legacy: `{"tierFilter": {"tier": "TIER_0"}}`
    - Current: `{"customerTierFilters": [{"name": "TIER", "value": ["TIER_1"], "operator": "IN"}]}`
    """
    parsed = _parse_rollout_filters(filters_raw)
    if parsed is None:
        return None

    # Current format: customerTierFilters list
    tier_filters = parsed.get("customerTierFilters")
    if isinstance(tier_filters, list):
        for entry in tier_filters:
            if isinstance(entry, dict) and entry.get("name") == "TIER":
                values = entry.get("value")
                if isinstance(values, list) and len(values) == 1:
                    return str(values[0])
                if isinstance(values, list) and len(values) > 1:
                    return ", ".join(str(v) for v in values)

    # Legacy format: tierFilter dict
    tier_filter = parsed.get("tierFilter")
    if isinstance(tier_filter, dict):
        tier = tier_filter.get("tier")
        if isinstance(tier, str):
            return tier

    return None


def _row_to_connector_rollout_info(row: dict[str, Any]) -> ConnectorRolloutInfo:
    """Convert a database row to a ConnectorRolloutInfo model."""
    return ConnectorRolloutInfo(
        rollout_id=str(row["rollout_id"]),
        actor_definition_id=str(row["actor_definition_id"]),
        state=row["state"],
        initial_rollout_pct=row.get("initial_rollout_pct"),
        current_target_rollout_pct=row.get("current_target_rollout_pct"),
        final_target_rollout_pct=row.get("final_target_rollout_pct"),
        has_breaking_changes=row["has_breaking_changes"],
        max_step_wait_time_mins=row.get("max_step_wait_time_mins"),
        rollout_strategy=row.get("rollout_strategy"),
        updated_by_user_id=str(row["updated_by_user_id"])
        if row.get("updated_by_user_id") is not None
        else None,
        updated_by_user_name=row.get("updated_by_user_name"),
        updated_by_user_email=row.get("updated_by_user_email"),
        workflow_run_id=row.get("workflow_run_id"),
        error_msg=row.get("error_msg"),
        failed_reason=row.get("failed_reason"),
        paused_reason=row.get("paused_reason"),
        tag=row.get("tag"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
        completed_at=row.get("completed_at"),
        expires_at=row.get("expires_at"),
        rc_docker_image_tag=row.get("rc_docker_image_tag"),
        rc_docker_repository=row.get("rc_docker_repository"),
        initial_docker_image_tag=row.get("initial_docker_image_tag"),
        initial_docker_repository=row.get("initial_docker_repository"),
        filters=_parse_rollout_filters(row.get("filters")),
        customer_tier=_extract_tier_from_filters(row.get("filters")),
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_connector_rollouts(
    actor_definition_id: Annotated[
        str | None,
        Field(description="Connector definition UUID to filter by (optional)"),
    ] = None,
    rollout_id: Annotated[
        str | None,
        Field(description="Specific rollout UUID to look up (optional)"),
    ] = None,
    active_only: Annotated[
        bool,
        Field(description="If true, only return active (non-terminal) rollouts"),
    ] = False,
    limit: Annotated[
        int,
        Field(description="Maximum number of results (default: 100)"),
    ] = 100,
) -> list[ConnectorRolloutInfo]:
    """Query connector rollouts with flexible filtering.

    Returns rollouts based on the provided filters. If no filters are specified,
    returns all active rollouts. Useful for monitoring rollout status and history.

    Filter behavior:
    - rollout_id: Returns that specific rollout (ignores other filters)
    - active_only: Returns only active (non-terminal) rollouts
    - actor_definition_id: Returns rollouts for that specific connector
    - No filters: Returns all active rollouts (same as active_only=True)
    """
    rows = query_connector_rollouts(
        actor_definition_id=actor_definition_id,
        rollout_id=rollout_id,
        active_only=active_only,
        limit=limit,
    )
    return [_row_to_connector_rollout_info(row) for row in rows]


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def query_prod_connection_sync_activity(
    start_at: Annotated[
        datetime,
        Field(
            description=(
                "Inclusive start timestamp for the sync activity window. "
                "Must be timezone-aware (ISO 8601 with offset or `Z`)."
            ),
        ),
    ],
    end_at: Annotated[
        datetime,
        Field(
            description=(
                "Exclusive end timestamp for the sync activity window. "
                "Must be timezone-aware and strictly after `start_at`."
            ),
        ),
    ],
    organization_id: Annotated[
        str | OrganizationAliasEnum | None,
        Field(
            description=(
                "Optional organization UUID or alias. At least one of "
                "`organization_id`, `workspace_id`, or `connection_ids` is "
                "required. Accepts `@airbyte-internal` as an alias for the "
                "Airbyte internal org."
            ),
            default=None,
        ),
    ] = None,
    workspace_id: Annotated[
        str | WorkspaceAliasEnum | None,
        Field(
            description=(
                "Optional workspace UUID or alias. At least one of "
                "`organization_id`, `workspace_id`, or `connection_ids` is "
                "required. Accepts `@devin-ai-sandbox` as an alias for the "
                "Devin AI sandbox workspace."
            ),
            default=None,
        ),
    ] = None,
    connection_ids: Annotated[
        list[str] | None,
        Field(
            description=(
                "Optional list of connection UUIDs. At least one of "
                "`organization_id`, `workspace_id`, or `connection_ids` is "
                "required."
            ),
            default=None,
        ),
    ] = None,
    status_filter: Annotated[
        StatusFilter,
        Field(
            description=(
                "Filter by job status: `all` (default), `succeeded`, or "
                "`failed`. Applied to `jobs.status` in the Prod DB Replica."
            ),
            default=StatusFilter.ALL,
        ),
    ] = StatusFilter.ALL,
    limit: Annotated[
        int,
        Field(
            description="Maximum number of attempt rows to return.",
            default=1000,
        ),
    ] = 1000,
) -> list[dict[str, Any]]:
    """List recent sync jobs and attempts from the Prod DB Replica.

    Returns one row per `(job, attempt)` pair for sync jobs whose `updated_at`
    falls in `[start_at, end_at)`, scoped to the provided organization,
    workspace, or connection IDs. Designed for live operational lookups —
    e.g. "what happened on this connection in the last hour" — not for
    historical analysis.

    Each row is enriched with `customer_tier` and `is_eu` for the owning
    organization. Tier filtering is intentionally not applied — this is a
    read-only observability query.

    Input requirements:
    - At least one of `organization_id`, `workspace_id`, or `connection_ids`
      must be provided (any combination is accepted).
    - `start_at` and `end_at` must be timezone-aware and `start_at < end_at`.

    Key fields in each row:
    - `job_id`, `attempt_id`, `attempt_number`
    - `job_status`, `attempt_status`
    - `job_started_at`, `job_updated_at`, `attempt_ended_at`
    - `failure_summary` (JSON; populated when an attempt failed)
    - `connection_id`, `connection_name`, `connection_status`
    - `source_actor_id`, `source_actor_name`, `source_actor_definition_id`
    - `destination_actor_id`, `destination_actor_name`,
      `destination_actor_definition_id`
    - `workspace_id`, `workspace_name`, `organization_id`
    - `dataplane_group_id`, `dataplane_name`
    - `customer_tier`, `is_eu` (added by tier enrichment)
    """
    resolved_organization_id = OrganizationAliasEnum.resolve(organization_id)
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    _validate_sync_activity_scope(
        organization_id=resolved_organization_id,
        workspace_id=resolved_workspace_id,
        connection_ids=connection_ids,
    )
    normalized_start_at, normalized_end_at = _validate_sync_activity_window(
        start_at=start_at,
        end_at=end_at,
    )

    rows = query_connection_sync_activity_from_prod(
        start_at=normalized_start_at,
        end_at=normalized_end_at,
        organization_id=resolved_organization_id,
        workspace_id=resolved_workspace_id,
        connection_ids=connection_ids,
        status_filter=status_filter.value,
        limit=limit,
    )
    return enrich_rows_by_org(rows)


# =============================================================================
# Pinned Connector Versions Models and Tools
# =============================================================================


class PinnedConnectorVersionInfo(BaseModel):
    """A connector version that has at least one scoped configuration pin."""

    version_id: str = Field(description="The actor_definition_version UUID")
    connector_definition_id: str = Field(description="The connector definition UUID")
    connector_name: str = Field(description="Human-readable connector name")
    docker_repository: str = Field(description="Docker repository path")
    docker_image_tag: str = Field(description="Docker image tag for this version")
    last_published: str | None = Field(
        default=None, description="ISO timestamp when this version was last published"
    )
    pin_count: int = Field(
        description="Total number of scoped_configuration rows pinning to this version"
    )
    actor_pins: int = Field(description="Number of actor-scoped pins")
    workspace_pins: int = Field(description="Number of workspace-scoped pins")
    org_pins: int = Field(description="Number of organization-scoped pins")


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def query_connector_pin_stats(
    connector_definition_id: Annotated[
        str | None,
        Field(
            description="Connector definition UUID to filter by (optional). "
            "Mutually exclusive with `connector_canonical_name`."
        ),
    ] = None,
    connector_canonical_name: Annotated[
        str | None,
        Field(
            description="Connector canonical name (e.g. `source-postgres`) to filter by. "
            "Resolved to a definition ID via the registry. "
            "Mutually exclusive with `connector_definition_id`."
        ),
    ] = None,
) -> list[PinnedConnectorVersionInfo]:
    """Query connector versions that have at least one scoped configuration pin.

    Returns versions from the prod DB that are referenced by at least one
    `scoped_configuration` pin (`key = 'connector_version'`).  Each version
    appears exactly once with per-scope pin breakdown (actor, workspace, org).

    If neither filter is provided, returns the global superset across all connectors.
    """
    if connector_definition_id and connector_canonical_name:
        raise PyAirbyteInputError(
            message=(
                "Provide at most one of `connector_definition_id` or "
                "`connector_canonical_name`, not both."
            ),
        )

    resolved_id: str | None = None
    if connector_canonical_name:
        resolved_id = resolve_canonical_name_to_definition_id(
            canonical_name=connector_canonical_name,
        )
    elif connector_definition_id:
        resolved_id = connector_definition_id

    rows = query_versions_with_pins(actor_definition_id=resolved_id)
    return [
        PinnedConnectorVersionInfo(
            version_id=str(row["version_id"]),
            connector_definition_id=str(row["connector_definition_id"]),
            connector_name=row["connector_name"],
            docker_repository=row["docker_repository"],
            docker_image_tag=row["docker_image_tag"],
            last_published=(
                row["last_published"].isoformat() if row.get("last_published") else None
            ),
            pin_count=row["pin_count"],
            actor_pins=row.get("actor_pins", 0),
            workspace_pins=row.get("workspace_pins", 0),
            org_pins=row.get("org_pins", 0),
        )
        for row in rows
    ]


def register_prod_db_query_tools(app: FastMCP) -> None:
    """Register prod DB query tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
