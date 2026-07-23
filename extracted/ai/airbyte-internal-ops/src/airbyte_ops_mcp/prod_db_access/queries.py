# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Query execution functions for Airbyte Cloud Prod DB Replica.

This module provides functions that execute SQL queries against the Prod DB Replica
and return structured results. Each function wraps a SQL template from sql.py.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from time import perf_counter
from typing import Any

import sqlalchemy
from airbyte.exceptions import PyAirbyteInputError
from google.cloud import secretmanager

from airbyte_ops_mcp.gcp_auth import get_secret_manager_client
from airbyte_ops_mcp.prod_db_access.db_engine import (
    get_pool,
)
from airbyte_ops_mcp.prod_db_access.sql import (
    SEARCH_ORGANIZATIONS,
    SEARCH_WORKSPACES,
    SELECT_ACTIVE_CONNECTOR_ROLLOUTS,
    SELECT_ACTIVE_CONNECTOR_ROLLOUTS_BY_DEFINITION,
    SELECT_ACTORS_PINNED_TO_VERSION,
    SELECT_CONNECTION_SYNC_ACTIVITY,
    SELECT_CONNECTION_WORKSPACE_DETAILS,
    SELECT_CONNECTIONS_BY_CONNECTOR,
    SELECT_CONNECTIONS_BY_CONNECTOR_AND_ORG,
    SELECT_CONNECTIONS_BY_DESTINATION_CONNECTOR,
    SELECT_CONNECTIONS_BY_DESTINATION_CONNECTOR_AND_ORG,
    SELECT_CONNECTIONS_BY_SOURCE_CONNECTOR_AND_STREAM,
    SELECT_CONNECTIONS_BY_SOURCE_CONNECTOR_AND_STREAM_AND_ORG,
    SELECT_CONNECTOR_ROLLOUT_BY_ID,
    SELECT_CONNECTOR_ROLLOUTS,
    SELECT_CONNECTOR_VERSIONS,
    SELECT_DATAPLANES_LIST,
    SELECT_DESTINATION_ACTOR_POPULATION_BY_ORG,
    SELECT_DESTINATION_CONNECTION_STATS,
    SELECT_DESTINATION_SUCCESSFUL_SYNCS_FOR_VERSION,
    SELECT_DESTINATION_SYNC_RESULTS_FOR_VERSION,
    SELECT_DESTINATION_VERSION_ACTOR_HEALTH,
    SELECT_FAILED_SYNC_ATTEMPTS_FOR_CONNECTOR,
    SELECT_NEW_CONNECTOR_RELEASES,
    SELECT_ORG_CONNECTOR_PINS,
    SELECT_ORG_PIN_STATS,
    SELECT_ORG_WORKSPACES,
    SELECT_ORGANIZATION_AGENTIC_FLAGS,
    SELECT_RAW_PINS_FOR_VERSION,
    SELECT_RECENT_FAILED_SYNCS_FOR_DESTINATION_CONNECTOR,
    SELECT_RECENT_FAILED_SYNCS_FOR_SOURCE_CONNECTOR,
    SELECT_RECENT_SUCCESSFUL_SYNCS_FOR_DESTINATION_CONNECTOR,
    SELECT_RECENT_SUCCESSFUL_SYNCS_FOR_SOURCE_CONNECTOR,
    SELECT_RECENT_SYNCS_FOR_DESTINATION_CONNECTOR,
    SELECT_RECENT_SYNCS_FOR_SOURCE_CONNECTOR,
    SELECT_SOURCE_ACTOR_POPULATION_BY_ORG,
    SELECT_SOURCE_CONNECTION_STATS,
    SELECT_SOURCE_SUCCESSFUL_SYNCS_FOR_VERSION,
    SELECT_SOURCE_SYNC_RESULTS_FOR_VERSION,
    SELECT_SOURCE_VERSION_ACTOR_HEALTH,
    SELECT_VERSION_ID_BY_TAG,
    SELECT_VERSION_INFO_BY_ID,
    SELECT_VERSIONS_WITH_PINS,
    SELECT_VERSIONS_WITH_PINS_BY_DEFINITION,
    SELECT_WORKSPACE_INFO,
    SELECT_WORKSPACES_BY_EMAIL_DOMAIN,
)

logger = logging.getLogger(__name__)

# SQL fragment appended to WHERE clauses when exclude_pinned=True.
# Requires the query to already have LEFT JOINs aliased actor_pin, ws_pin, org_pin.
_EXCLUDE_PINNED_SQL = (
    " AND actor_pin.id IS NULL AND ws_pin.id IS NULL AND org_pin.id IS NULL"
)

# SQL fragment appended to WHERE clauses when enabled_schedules_only=True.
# Requires the query to already JOIN the `connection` table.
# Filters to connections that are both active (not paused/inactive) and on an
# automated sync schedule (not manual-trigger-only).
_ENABLED_SCHEDULES_ONLY_SQL = (
    " AND connection.status = 'active' AND connection.manual = false"
)


def _inject_sql_filter(
    statement: sqlalchemy.sql.elements.TextClause,
    sql_fragment: str,
) -> sqlalchemy.sql.elements.TextClause:
    """Return a new TextClause with additional WHERE conditions injected.

    Inserts the fragment before ORDER BY (if present) or before LIMIT,
    so the filter is always part of the WHERE clause — not after ORDER BY.
    """
    sql_str = str(statement.text)
    if "ORDER BY" in sql_str:
        sql_str = sql_str.replace("ORDER BY", f"{sql_fragment}\n    ORDER BY", 1)
    else:
        sql_str = sql_str.replace("LIMIT :", f"{sql_fragment}\n    LIMIT :")
    return sqlalchemy.text(sql_str)


def _inject_exclude_pinned(
    statement: sqlalchemy.sql.elements.TextClause,
) -> sqlalchemy.sql.elements.TextClause:
    """Return a new TextClause with pin-exclusion conditions in the WHERE clause."""
    return _inject_sql_filter(statement, _EXCLUDE_PINNED_SQL)


def _inject_enabled_schedules_only(
    statement: sqlalchemy.sql.elements.TextClause,
) -> sqlalchemy.sql.elements.TextClause:
    """Return a new TextClause filtering to active, scheduled connections."""
    return _inject_sql_filter(statement, _ENABLED_SCHEDULES_ONLY_SQL)


def _without_limit_clause(
    statement: sqlalchemy.sql.elements.TextClause,
) -> sqlalchemy.sql.elements.TextClause:
    """Return a new SQL text clause without the final `LIMIT :limit` clause."""
    sql_str = str(statement.text).replace("    LIMIT :limit", "")
    return sqlalchemy.text(sql_str)


def _run_sql_query(
    statement: sqlalchemy.sql.elements.TextClause,
    parameters: Mapping[str, Any] | None = None,
    *,
    query_name: str | None = None,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Execute a SQL text statement and return rows as list[dict], logging elapsed time.

    Args:
        statement: SQLAlchemy text clause to execute
        parameters: Query parameters to bind
        query_name: Optional name for logging (defaults to first line of SQL)
        gsm_client: GCP Secret Manager client for retrieving credentials.
            If None, a new client will be instantiated.

    Returns:
        List of row dicts from the query result
    """
    if gsm_client is None:
        gsm_client = get_secret_manager_client()
    pool = get_pool(gsm_client)
    start = perf_counter()
    with pool.connect() as conn:
        result = conn.execute(statement, parameters or {})
        rows = [dict(row._mapping) for row in result]
    elapsed = perf_counter() - start

    name = query_name or "SQL query"
    logger.info("Prod DB query %s returned %d rows in %.3f s", name, len(rows), elapsed)

    return rows


def query_organization_agentic_flags(
    organization_ids: list[str],
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query current `is_agentic` flag values for organizations."""
    return _run_sql_query(
        SELECT_ORGANIZATION_AGENTIC_FLAGS,
        parameters={"organization_ids": organization_ids},
        query_name="SELECT_ORGANIZATION_AGENTIC_FLAGS",
        gsm_client=gsm_client,
    )


def query_connection_sync_activity_from_prod(
    *,
    start_at: datetime,
    end_at: datetime,
    organization_id: str | None = None,
    workspace_id: str | None = None,
    connection_ids: list[str] | None = None,
    status_filter: str = "all",
    limit: int = 1000,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query recent sync jobs and attempts from the Prod DB Replica."""
    return _run_sql_query(
        SELECT_CONNECTION_SYNC_ACTIVITY,
        {
            "start_at": start_at,
            "end_at": end_at,
            "organization_id": organization_id,
            "workspace_id": workspace_id,
            "connection_ids": connection_ids or [],
            "connection_ids_is_empty": not connection_ids,
            "status_filter": status_filter,
            "limit": limit,
        },
        query_name="connection_sync_activity",
        gsm_client=gsm_client,
    )


def query_connections_by_connector(
    connector_definition_id: str,
    organization_id: str | None = None,
    limit: int | None = 1000,
    *,
    exclude_pinned: bool = False,
    enabled_schedules_only: bool = False,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query connections by source connector type, optionally filtered by organization.

    Args:
        connector_definition_id: Connector definition UUID to filter by
        organization_id: Optional organization UUID to search within
        limit: Maximum number of results (default: 1000). Pass `None` to return
            every matching row (the `LIMIT` clause is dropped) — use this when an
            exact count is required and truncation to an arbitrary sample would
            be incorrect.
        exclude_pinned: If True, exclude connections where the actor has a
            version pin at any scope (actor, workspace, or organization).
            Filtering is applied at the SQL level so the full `limit`
            rows are returned.
        enabled_schedules_only: If `True`, restrict results to connections that
            are both active (not paused/inactive) and on an automated sync
            schedule (not manual-trigger-only).  Filtering is applied at the
            SQL level.
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of connection records with workspace and dataplane info
    """
    # Use separate queries to avoid pg8000 NULL parameter type issues
    # pg8000 cannot determine the type of NULL parameters in patterns like
    # "(:param IS NULL OR column = :param)"
    if organization_id is None:
        query = SELECT_CONNECTIONS_BY_CONNECTOR
        if exclude_pinned:
            query = _inject_exclude_pinned(query)
        if enabled_schedules_only:
            query = _inject_enabled_schedules_only(query)
        parameters: dict[str, Any] = {
            "connector_definition_id": connector_definition_id
        }
        if limit is None:
            query = _without_limit_clause(query)
        else:
            parameters["limit"] = limit
        return _run_sql_query(
            query,
            parameters=parameters,
            query_name="SELECT_CONNECTIONS_BY_CONNECTOR",
            gsm_client=gsm_client,
        )

    query = SELECT_CONNECTIONS_BY_CONNECTOR_AND_ORG
    if exclude_pinned:
        query = _inject_exclude_pinned(query)
    if enabled_schedules_only:
        query = _inject_enabled_schedules_only(query)
    parameters = {
        "connector_definition_id": connector_definition_id,
        "organization_id": organization_id,
    }
    if limit is None:
        query = _without_limit_clause(query)
    else:
        parameters["limit"] = limit
    return _run_sql_query(
        query,
        parameters=parameters,
        query_name="SELECT_CONNECTIONS_BY_CONNECTOR_AND_ORG",
        gsm_client=gsm_client,
    )


def query_connections_by_destination_connector(
    connector_definition_id: str,
    organization_id: str | None = None,
    limit: int | None = 1000,
    *,
    exclude_pinned: bool = False,
    enabled_schedules_only: bool = False,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query connections by destination connector type, optionally filtered by organization.

    Args:
        connector_definition_id: Destination connector definition UUID to filter by
        organization_id: Optional organization UUID to search within
        limit: Maximum number of results (default: 1000). Pass `None` to return
            every matching row (the `LIMIT` clause is dropped) — use this when an
            exact count is required and truncation to an arbitrary sample would
            be incorrect.
        exclude_pinned: If True, exclude connections where the actor has a
            version pin at any scope (actor, workspace, or organization).
            Filtering is applied at the SQL level so the full `limit`
            rows are returned.
        enabled_schedules_only: If `True`, restrict results to connections that
            are both active (not paused/inactive) and on an automated sync
            schedule (not manual-trigger-only).  Filtering is applied at the
            SQL level.
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of connection records with workspace and dataplane info
    """
    # Use separate queries to avoid pg8000 NULL parameter type issues
    if organization_id is None:
        query = SELECT_CONNECTIONS_BY_DESTINATION_CONNECTOR
        if exclude_pinned:
            query = _inject_exclude_pinned(query)
        if enabled_schedules_only:
            query = _inject_enabled_schedules_only(query)
        parameters: dict[str, Any] = {
            "connector_definition_id": connector_definition_id
        }
        if limit is None:
            query = _without_limit_clause(query)
        else:
            parameters["limit"] = limit
        return _run_sql_query(
            query,
            parameters=parameters,
            query_name="SELECT_CONNECTIONS_BY_DESTINATION_CONNECTOR",
            gsm_client=gsm_client,
        )

    query = SELECT_CONNECTIONS_BY_DESTINATION_CONNECTOR_AND_ORG
    if exclude_pinned:
        query = _inject_exclude_pinned(query)
    if enabled_schedules_only:
        query = _inject_enabled_schedules_only(query)
    parameters = {
        "connector_definition_id": connector_definition_id,
        "organization_id": organization_id,
    }
    if limit is None:
        query = _without_limit_clause(query)
    else:
        parameters["limit"] = limit
    return _run_sql_query(
        query,
        parameters=parameters,
        query_name="SELECT_CONNECTIONS_BY_DESTINATION_CONNECTOR_AND_ORG",
        gsm_client=gsm_client,
    )


def query_connector_versions(
    connector_definition_id: str,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query all versions for a connector definition.

    Args:
        connector_definition_id: Connector definition UUID
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of version records ordered by last_published DESC
    """
    return _run_sql_query(
        SELECT_CONNECTOR_VERSIONS,
        parameters={"actor_definition_id": connector_definition_id},
        query_name="SELECT_CONNECTOR_VERSIONS",
        gsm_client=gsm_client,
    )


def query_new_connector_releases(
    days: int = 7,
    limit: int | None = 100,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query recently published connector versions.

    Args:
        days: Number of days to look back (default: 7)
        limit: Maximum number of results (default: 100). Pass `None` for no limit.
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of recently published connector versions
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    statement = (
        SELECT_NEW_CONNECTOR_RELEASES
        if limit is not None
        else _without_limit_clause(SELECT_NEW_CONNECTOR_RELEASES)
    )
    parameters: dict[str, Any] = {"cutoff_date": cutoff_date}
    if limit is not None:
        parameters["limit"] = limit
    return _run_sql_query(
        statement,
        parameters=parameters,
        query_name="SELECT_NEW_CONNECTOR_RELEASES",
        gsm_client=gsm_client,
    )


def query_actors_pinned_to_version(
    connector_version_id: str,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query actors (sources/destinations) pinned to a specific connector version.

    Args:
        connector_version_id: Connector version UUID to search for
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of actors pinned to the specified version
    """
    return _run_sql_query(
        SELECT_ACTORS_PINNED_TO_VERSION,
        parameters={"actor_definition_version_id": connector_version_id},
        query_name="SELECT_ACTORS_PINNED_TO_VERSION",
        gsm_client=gsm_client,
    )


def query_raw_pins_for_version(
    connector_version_id: str,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Return raw `scoped_configuration` entries pinned to a version.

    Unlike `query_actors_pinned_to_version` (which expands workspace/org pins
    into per-actor rows), this returns the actual pin records directly. The
    total count matches the rollout dashboard's `rc_pin_count`.
    """
    return _run_sql_query(
        SELECT_RAW_PINS_FOR_VERSION,
        parameters={"actor_definition_version_id": connector_version_id},
        query_name="SELECT_RAW_PINS_FOR_VERSION",
        gsm_client=gsm_client,
    )


def resolve_version_info(
    connector_version_id: str,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> dict[str, Any]:
    """Resolve a version UUID to its `docker_repository` and `docker_image_tag`.

    Returns a single-row dict with keys `version_id`, `actor_definition_id`,
    `docker_repository`, `docker_image_tag`.

    Raises `PyAirbyteInputError` if the UUID is not found.
    """
    rows = _run_sql_query(
        SELECT_VERSION_INFO_BY_ID,
        parameters={"version_id": connector_version_id},
        query_name="SELECT_VERSION_INFO_BY_ID",
        gsm_client=gsm_client,
    )
    if not rows:
        raise PyAirbyteInputError(
            message=f"No connector version found for UUID: {connector_version_id}",
        )
    return rows[0]


def resolve_version_id_by_tag(
    docker_repository: str,
    docker_image_tag: str,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> dict[str, Any]:
    """Resolve a `docker_repository` + `docker_image_tag` to a version UUID.

    Returns a single-row dict with keys `version_id`, `actor_definition_id`,
    `docker_repository`, `docker_image_tag`.

    Raises `PyAirbyteInputError` if the combination is not found.
    """
    rows = _run_sql_query(
        SELECT_VERSION_ID_BY_TAG,
        parameters={
            "docker_repository": docker_repository,
            "docker_image_tag": docker_image_tag,
        },
        query_name="SELECT_VERSION_ID_BY_TAG",
        gsm_client=gsm_client,
    )
    if not rows:
        raise PyAirbyteInputError(
            message=(
                f"No connector version found for {docker_repository}:{docker_image_tag}"
            ),
        )
    return rows[0]


def is_source_connector(docker_repository: str) -> bool:
    """Return `True` if `docker_repository` identifies a source connector."""
    return docker_repository.startswith("airbyte/source-")


def query_syncs_for_connector_version(
    connector_version_id: str,
    is_destination: bool,
    days: int = 7,
    limit: int = 100,
    successful_only: bool = False,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query sync jobs that were run with a specific connector version.

    Filters on the version stamped into `jobs.config` at job-creation time
    rather than the current pin state. This matches the backend's approach
    in `RolloutActorFinder.jobDefinitionVersionIdEq`.

    Args:
        connector_version_id: Connector version UUID to filter by
        is_destination: `True` for destination connectors, `False` for source
        days: Number of days to look back (default: 7)
        limit: Maximum number of results (default: 100)
        successful_only: If `True`, only return successful syncs (default: `False`)
        gsm_client: GCP Secret Manager client. If `None`, a new client will be instantiated.

    Returns:
        List of sync job results
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    if is_destination:
        query = (
            SELECT_DESTINATION_SUCCESSFUL_SYNCS_FOR_VERSION
            if successful_only
            else SELECT_DESTINATION_SYNC_RESULTS_FOR_VERSION
        )
        query_name = (
            "SELECT_DESTINATION_SUCCESSFUL_SYNCS_FOR_VERSION"
            if successful_only
            else "SELECT_DESTINATION_SYNC_RESULTS_FOR_VERSION"
        )
    else:
        query = (
            SELECT_SOURCE_SUCCESSFUL_SYNCS_FOR_VERSION
            if successful_only
            else SELECT_SOURCE_SYNC_RESULTS_FOR_VERSION
        )
        query_name = (
            "SELECT_SOURCE_SUCCESSFUL_SYNCS_FOR_VERSION"
            if successful_only
            else "SELECT_SOURCE_SYNC_RESULTS_FOR_VERSION"
        )
    return _run_sql_query(
        query,
        parameters={
            "actor_definition_version_id": connector_version_id,
            "cutoff_date": cutoff_date,
            "limit": limit,
        },
        query_name=query_name,
        gsm_client=gsm_client,
    )


def query_version_actor_health(
    connector_version_id: str,
    is_destination: bool,
    days: int = 7,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Aggregate per-actor sync health for a specific connector version.

    Returns one row per actor that ran the version within the last `days`,
    with `total_jobs`, `succeeded_jobs`, `failed_jobs`, `latest_status`, plus
    `organization_id` and `dataplane_name` for tier resolution. Filters on the
    version stamped into `jobs.config` at job-creation time (the same primitive
    as `query_syncs_for_connector_version`), so the population reflects actors
    that actually ran this version rather than the current pin state.

    Args:
        connector_version_id: Connector version UUID to summarize.
        is_destination: `True` for destination connectors, `False` for source.
        days: Number of days to look back (default: 7).
        gsm_client: GCP Secret Manager client. If `None`, a new client is created.
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    if is_destination:
        query = SELECT_DESTINATION_VERSION_ACTOR_HEALTH
        query_name = "SELECT_DESTINATION_VERSION_ACTOR_HEALTH"
    else:
        query = SELECT_SOURCE_VERSION_ACTOR_HEALTH
        query_name = "SELECT_SOURCE_VERSION_ACTOR_HEALTH"
    return _run_sql_query(
        query,
        parameters={
            "actor_definition_version_id": connector_version_id,
            "cutoff_date": cutoff_date,
        },
        query_name=query_name,
        gsm_client=gsm_client,
    )


def query_actor_population_by_org(
    actor_definition_id: str,
    is_destination: bool,
    *,
    target_version_id: str | None = None,
    rollout_created_at: str | None = None,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Aggregate the active-actor population for a connector definition by org.

    Returns one row per organization with `actor_count` (enabled actors of the
    definition that have at least one *active* connection, i.e.
    `connection.status = 'active'` \u2014 inactive/disabled and deprecated
    connections are excluded) and
    `pinned_actor_count` (those with an effective `connector_version` pin at any
    scope). Each row also carries `organization_id` and `dataplane_name` so the
    caller can resolve customer tiers. The eligible (unpinned) population is
    `actor_count - pinned_actor_count`.

    When `target_version_id` is supplied, each row also carries
    `pinned_to_version_count` \u2014 active actors whose *effective* pin is that
    version. Actors pinned to a *different* version are then
    `pinned_actor_count - pinned_to_version_count`, letting the caller exclude
    them from a specific-version rollout's addressable audience. When it is
    `None`, `pinned_to_version_count` is `0` for every row.

    Every row also carries three mutually-exclusive job-status factors that
    partition the *unpinned* active actors, reproducing the platform's
    `filterByJobStatus` eligibility gate over the window starting at
    `rollout_created_at`:

    - `eligible_gated_count`: most-recent `sync` succeeded on a non-manual
      active connection and failed on none (the gate the backend applies).
    - `gate_excluded_failed_count`: at least one recent failed sync.
    - `gate_excluded_no_recent_sync_count`: no qualifying sync in the window.

    Keeping the exclusion reasons distinct lets the caller surface every factor
    instead of collapsing them. When `rollout_created_at` is `None` the window
    matches nothing, so every unpinned actor lands in
    `gate_excluded_no_recent_sync_count` and the caller should fall back to the
    ungated population.

    Args:
        actor_definition_id: Connector definition UUID to summarize.
        is_destination: `True` for destination connectors, `False` for source.
        target_version_id: Release-candidate `actor_definition_version` UUID to
            attribute pins to. `None` disables the per-version breakdown.
        rollout_created_at: The rollout's `created_at` timestamp (ISO string)
            used as the job-status window start. `None` disables the gate.
        gsm_client: GCP Secret Manager client. If `None`, a new client is created.
    """
    if is_destination:
        query = SELECT_DESTINATION_ACTOR_POPULATION_BY_ORG
        query_name = "SELECT_DESTINATION_ACTOR_POPULATION_BY_ORG"
    else:
        query = SELECT_SOURCE_ACTOR_POPULATION_BY_ORG
        query_name = "SELECT_SOURCE_ACTOR_POPULATION_BY_ORG"
    return _run_sql_query(
        query,
        parameters={
            "actor_definition_id": actor_definition_id,
            "target_version_id": target_version_id,
            "rollout_created_at": rollout_created_at,
        },
        query_name=query_name,
        gsm_client=gsm_client,
    )


def query_failed_sync_attempts_for_connector(
    connector_definition_id: str,
    organization_id: str | None = None,
    days: int = 7,
    limit: int = 100,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query failed sync attempts for ALL actors using a connector definition.

    Finds all actors with the given actor_definition_id and returns their failed
    sync attempts, regardless of whether they have explicit version pins.

    This is useful for investigating connector issues across all users.

    Note: This query only supports SOURCE connectors (joins via connection.source_id).
    For destination connectors, a separate query would be needed.

    Args:
        connector_definition_id: Connector definition UUID to filter by
        organization_id: Optional organization UUID to filter results by (post-query filter)
        days: Number of days to look back (default: 7)
        limit: Maximum number of results (default: 100)
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of failed sync attempt records with failure_summary and workspace info
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    results = _run_sql_query(
        SELECT_FAILED_SYNC_ATTEMPTS_FOR_CONNECTOR,
        parameters={
            "connector_definition_id": connector_definition_id,
            "cutoff_date": cutoff_date,
            "limit": limit,
        },
        query_name="SELECT_FAILED_SYNC_ATTEMPTS_FOR_CONNECTOR",
        gsm_client=gsm_client,
    )

    # Post-query filter by organization_id if provided
    if organization_id is not None:
        results = [
            r for r in results if str(r.get("organization_id")) == organization_id
        ]

    return results


def query_recent_syncs_for_connector(
    connector_definition_id: str,
    is_destination: bool = False,
    status_filter: str = "all",
    organization_id: str | None = None,
    days: int = 7,
    limit: int = 100,
    *,
    exclude_pinned: bool = False,
    enabled_schedules_only: bool = False,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query recent sync jobs for ALL actors using a connector definition.

    Finds all actors with the given actor_definition_id and returns their sync jobs,
    regardless of whether they have explicit version pins. Filters out deleted actors,
    deleted workspaces, and deprecated connections.

    This is useful for finding healthy connections with recent successful syncs,
    or for investigating connector issues across all users.

    Args:
        connector_definition_id: Connector definition UUID to filter by
        is_destination: If True, query destination connectors; if False, query sources
        status_filter: Filter by job status - "all", "succeeded", or "failed"
        organization_id: Optional organization UUID to filter results by (post-query filter)
        days: Number of days to look back (default: 7)
        limit: Maximum number of results (default: 100)
        exclude_pinned: If True, exclude actors that have a version pin at
            any scope (actor, workspace, or organization).  Filtering is
            applied at the SQL level so the full `limit` rows are returned.
        enabled_schedules_only: If `True`, restrict results to connections that
            are both active (not paused/inactive) and on an automated sync
            schedule (not manual-trigger-only).  Filtering is applied at the
            SQL level.
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of sync job records with workspace info and optional pin context
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Select the appropriate query based on connector type and status filter
    if is_destination:
        if status_filter == "succeeded":
            query = SELECT_RECENT_SUCCESSFUL_SYNCS_FOR_DESTINATION_CONNECTOR
            query_name = "SELECT_RECENT_SUCCESSFUL_SYNCS_FOR_DESTINATION_CONNECTOR"
        elif status_filter == "failed":
            query = SELECT_RECENT_FAILED_SYNCS_FOR_DESTINATION_CONNECTOR
            query_name = "SELECT_RECENT_FAILED_SYNCS_FOR_DESTINATION_CONNECTOR"
        else:
            query = SELECT_RECENT_SYNCS_FOR_DESTINATION_CONNECTOR
            query_name = "SELECT_RECENT_SYNCS_FOR_DESTINATION_CONNECTOR"
    else:
        if status_filter == "succeeded":
            query = SELECT_RECENT_SUCCESSFUL_SYNCS_FOR_SOURCE_CONNECTOR
            query_name = "SELECT_RECENT_SUCCESSFUL_SYNCS_FOR_SOURCE_CONNECTOR"
        elif status_filter == "failed":
            query = SELECT_RECENT_FAILED_SYNCS_FOR_SOURCE_CONNECTOR
            query_name = "SELECT_RECENT_FAILED_SYNCS_FOR_SOURCE_CONNECTOR"
        else:
            query = SELECT_RECENT_SYNCS_FOR_SOURCE_CONNECTOR
            query_name = "SELECT_RECENT_SYNCS_FOR_SOURCE_CONNECTOR"

    if exclude_pinned:
        query = _inject_exclude_pinned(query)
    if enabled_schedules_only:
        query = _inject_enabled_schedules_only(query)

    results = _run_sql_query(
        query,
        parameters={
            "connector_definition_id": connector_definition_id,
            "cutoff_date": cutoff_date,
            "limit": limit,
        },
        query_name=query_name,
        gsm_client=gsm_client,
    )

    # Post-query filter by organization_id if provided
    if organization_id is not None:
        results = [
            r for r in results if str(r.get("organization_id")) == organization_id
        ]

    return results


def query_dataplanes_list(
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query all dataplane groups with workspace counts.

    Args:
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of dataplane groups ordered by workspace count DESC
    """
    return _run_sql_query(
        SELECT_DATAPLANES_LIST,
        query_name="SELECT_DATAPLANES_LIST",
        gsm_client=gsm_client,
    )


def query_workspace_info(
    workspace_id: str,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> dict[str, Any] | None:
    """Query workspace info including dataplane group.

    Args:
        workspace_id: Workspace UUID
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        Workspace info dict, or None if not found
    """
    rows = _run_sql_query(
        SELECT_WORKSPACE_INFO,
        parameters={"workspace_id": workspace_id},
        query_name="SELECT_WORKSPACE_INFO",
        gsm_client=gsm_client,
    )
    return rows[0] if rows else None


def query_org_workspaces(
    organization_id: str,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query all workspaces in an organization with dataplane info.

    Args:
        organization_id: Organization UUID
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of workspaces in the organization
    """
    return _run_sql_query(
        SELECT_ORG_WORKSPACES,
        parameters={"organization_id": organization_id},
        query_name="SELECT_ORG_WORKSPACES",
        gsm_client=gsm_client,
    )


def query_workspaces_by_email_domain(
    email_domain: str,
    limit: int = 100,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query workspaces by email domain.

    This is useful for identifying workspaces based on user email domains.
    For example, searching for "motherduck.com" will find workspaces where users have
    @motherduck.com email addresses, which may belong to partner accounts.

    Args:
        email_domain: Email domain to search for (e.g., "motherduck.com", "fivetran.com").
            Do not include the "@" symbol.
        limit: Maximum number of results (default: 100)
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of workspace records with organization_id, workspace_id, workspace_name,
        slug, email, dataplane_group_id, dataplane_name, and created_at.
        Results are ordered by organization_id and workspace_name.
    """
    # Strip leading @ if provided
    clean_domain = email_domain.lstrip("@")

    return _run_sql_query(
        SELECT_WORKSPACES_BY_EMAIL_DOMAIN,
        parameters={"email_domain": clean_domain, "limit": limit},
        query_name="SELECT_WORKSPACES_BY_EMAIL_DOMAIN",
        gsm_client=gsm_client,
    )


def search_organizations(
    name_contains: str,
    limit: int = 20,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Search organizations by name/email substring (case-insensitive ILIKE)."""
    name_contains = name_contains.strip()
    if not name_contains:
        return []

    return _run_sql_query(
        SEARCH_ORGANIZATIONS,
        parameters={"name_contains": name_contains, "limit": limit},
        query_name="SEARCH_ORGANIZATIONS",
        gsm_client=gsm_client,
    )


def search_workspaces(
    name_contains: str,
    limit: int = 100,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Search workspaces by name/slug substring (case-insensitive ILIKE)."""
    name_contains = name_contains.strip()
    if not name_contains:
        return []

    return _run_sql_query(
        SEARCH_WORKSPACES,
        parameters={"name_contains": name_contains, "limit": limit},
        query_name="SEARCH_WORKSPACES",
        gsm_client=gsm_client,
    )


def query_connection_workspace_details(
    connection_ids: list[str],
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Resolve connection IDs to their workspace and organization context.

    Args:
        connection_ids: List of connection UUIDs to resolve
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of dicts with connection_id, workspace_id, organization_id,
        dataplane_group_id, and dataplane_name.
    """
    return _run_sql_query(
        SELECT_CONNECTION_WORKSPACE_DETAILS,
        parameters={"connection_ids": connection_ids},
        query_name="SELECT_CONNECTION_WORKSPACE_DETAILS",
        gsm_client=gsm_client,
    )


def query_source_connection_stats(
    connector_definition_id: str,
    days: int = 7,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query aggregate connection stats for a SOURCE connector.

    Returns counts of connections grouped by pinned version, including:
    - Total, enabled, and active connection counts
    - Pinned vs unpinned breakdown
    - Latest attempt status breakdown (succeeded, failed, cancelled, running, unknown)

    Args:
        connector_definition_id: Source connector definition UUID
        days: Number of days to look back for "active" connections (default: 7)
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of dicts with aggregate counts grouped by pinned_version_id
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    return _run_sql_query(
        SELECT_SOURCE_CONNECTION_STATS,
        parameters={
            "connector_definition_id": connector_definition_id,
            "cutoff_date": cutoff_date,
        },
        query_name="SELECT_SOURCE_CONNECTION_STATS",
        gsm_client=gsm_client,
    )


def query_destination_connection_stats(
    connector_definition_id: str,
    days: int = 7,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query aggregate connection stats for a DESTINATION connector.

    Returns counts of connections grouped by pinned version, including:
    - Total, enabled, and active connection counts
    - Pinned vs unpinned breakdown
    - Latest attempt status breakdown (succeeded, failed, cancelled, running, unknown)

    Args:
        connector_definition_id: Destination connector definition UUID
        days: Number of days to look back for "active" connections (default: 7)
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of dicts with aggregate counts grouped by pinned_version_id
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    return _run_sql_query(
        SELECT_DESTINATION_CONNECTION_STATS,
        parameters={
            "connector_definition_id": connector_definition_id,
            "cutoff_date": cutoff_date,
        },
        query_name="SELECT_DESTINATION_CONNECTION_STATS",
        gsm_client=gsm_client,
    )


def query_connections_by_stream(
    connector_definition_id: str,
    stream_name: str,
    organization_id: str | None = None,
    limit: int = 100,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query connections by source connector type that have a specific stream enabled.

    This searches the connection's configured catalog (JSONB) for streams matching
    the specified name. Useful for finding connections that use a particular stream
    when validating connector fixes that affect specific streams.

    Args:
        connector_definition_id: Source connector definition UUID to filter by
        stream_name: Name of the stream to search for in the connection's catalog
        organization_id: Optional organization UUID to filter results by
        limit: Maximum number of results (default: 100)
        gsm_client: GCP Secret Manager client. If None, a new client will be instantiated.

    Returns:
        List of connection records with workspace and dataplane info
    """
    if organization_id is None:
        return _run_sql_query(
            SELECT_CONNECTIONS_BY_SOURCE_CONNECTOR_AND_STREAM,
            parameters={
                "connector_definition_id": connector_definition_id,
                "stream_name": stream_name,
                "limit": limit,
            },
            query_name="SELECT_CONNECTIONS_BY_SOURCE_CONNECTOR_AND_STREAM",
            gsm_client=gsm_client,
        )

    return _run_sql_query(
        SELECT_CONNECTIONS_BY_SOURCE_CONNECTOR_AND_STREAM_AND_ORG,
        parameters={
            "connector_definition_id": connector_definition_id,
            "stream_name": stream_name,
            "organization_id": organization_id,
            "limit": limit,
        },
        query_name="SELECT_CONNECTIONS_BY_SOURCE_CONNECTOR_AND_STREAM_AND_ORG",
        gsm_client=gsm_client,
    )


def query_connector_rollouts(
    actor_definition_id: str | None = None,
    rollout_id: str | None = None,
    active_only: bool = False,
    limit: int | None = 100,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query connector rollouts with flexible filtering.

    This is the unified query function for connector rollouts. Based on the
    arguments provided, it will:
    - If rollout_id is provided: Return that specific rollout (as a single-item list)
    - If active_only is True AND actor_definition_id is provided: Return active rollouts for that connector
    - If active_only is True: Return all active (non-terminal) rollouts
    - If actor_definition_id is provided: Return all rollouts for that connector (including terminal)
    - Otherwise: Return all active rollouts (up to limit)

    `actor_definition_id` and `rollout_id` narrow the returned rollout records.
    `active_only` excludes terminal rollout states.
    """
    limit_statement = (
        _without_limit_clause if limit is None else lambda statement: statement
    )
    parameters: dict[str, Any] = {}
    if limit is not None:
        parameters["limit"] = limit

    if rollout_id is not None:
        rows = _run_sql_query(
            SELECT_CONNECTOR_ROLLOUT_BY_ID,
            parameters={"rollout_id": rollout_id},
            query_name="SELECT_CONNECTOR_ROLLOUT_BY_ID",
            gsm_client=gsm_client,
        )
        return rows

    # Handle active_only with optional actor_definition_id filter
    if active_only:
        if actor_definition_id is not None:
            # Filter by both active states AND actor_definition_id
            parameters["actor_definition_id"] = actor_definition_id
            return _run_sql_query(
                limit_statement(SELECT_ACTIVE_CONNECTOR_ROLLOUTS_BY_DEFINITION),
                parameters=parameters,
                query_name="SELECT_ACTIVE_CONNECTOR_ROLLOUTS_BY_DEFINITION",
                gsm_client=gsm_client,
            )
        # Only active filter, no actor_definition_id
        return _run_sql_query(
            limit_statement(SELECT_ACTIVE_CONNECTOR_ROLLOUTS),
            parameters=parameters,
            query_name="SELECT_ACTIVE_CONNECTOR_ROLLOUTS",
            gsm_client=gsm_client,
        )

    # Not active_only, but filter by actor_definition_id (all states)
    if actor_definition_id is not None:
        parameters["actor_definition_id"] = actor_definition_id
        return _run_sql_query(
            limit_statement(SELECT_CONNECTOR_ROLLOUTS),
            parameters=parameters,
            query_name="SELECT_CONNECTOR_ROLLOUTS",
            gsm_client=gsm_client,
        )

    # Default: return active rollouts if no filters specified
    return _run_sql_query(
        limit_statement(SELECT_ACTIVE_CONNECTOR_ROLLOUTS),
        parameters=parameters,
        query_name="SELECT_ACTIVE_CONNECTOR_ROLLOUTS",
        gsm_client=gsm_client,
    )


def query_connector_rollouts_for_connector(
    *,
    actor_definition_id: str,
    active_only: bool = True,
    limit: int | None = 100,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query connector rollouts for a specific connector definition."""
    return query_connector_rollouts(
        actor_definition_id=actor_definition_id,
        active_only=active_only,
        limit=limit,
        gsm_client=gsm_client,
    )


def query_versions_with_pins(
    actor_definition_id: str | None = None,
    *,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query connector versions that have at least one pin.

    Does NOT join `connector_rollout`, so each version appears exactly once
    regardless of how many rollouts reference it.  Includes per-scope pin
    breakdown (`actor_pins`, `workspace_pins`, `org_pins`).

    Args:
        actor_definition_id: Optional connector definition UUID to filter results.
            If `None`, returns the global superset across all connectors.
        gsm_client: GCP Secret Manager client. If `None`, a new client will be instantiated.

    Returns:
        List of version dicts ordered by `pin_count` DESC, `created_at` DESC.
    """
    if actor_definition_id is not None:
        return _run_sql_query(
            SELECT_VERSIONS_WITH_PINS_BY_DEFINITION,
            parameters={"actor_definition_id": actor_definition_id},
            query_name="SELECT_VERSIONS_WITH_PINS_BY_DEFINITION",
            gsm_client=gsm_client,
        )
    return _run_sql_query(
        SELECT_VERSIONS_WITH_PINS,
        parameters=None,
        query_name="SELECT_VERSIONS_WITH_PINS",
        gsm_client=gsm_client,
    )


def query_org_pin_stats(
    organization_id: str,
    *,
    connector_definition_id: str | None = None,
    limit: int = 1000,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Query connector versions pinned anywhere under an organization.

    Aggregates every `connector_version` pin whose scope belongs to the
    organization — the org itself, one of its workspaces, or an actor within
    one of those workspaces — into one row per pinned version with the
    per-scope breakdown (`actor_pins`, `workspace_pins`, `org_pins`),
    `manual_pins` / `rollout_pins` / `breaking_change_pins`, and a
    `has_active_rollout` flag.

    Pass `connector_definition_id` to restrict to a single connector. Results
    are ordered by `pin_count` DESC, then version `created_at` DESC.
    """
    return _run_sql_query(
        SELECT_ORG_PIN_STATS,
        parameters={
            "organization_id": organization_id,
            "connector_definition_id": connector_definition_id,
            "limit": limit,
        },
        query_name="SELECT_ORG_PIN_STATS",
        gsm_client=gsm_client,
    )


def query_org_connector_pins(
    organization_id: str,
    *,
    connector_definition_id: str | None = None,
    pinned_version_id: str | None = None,
    limit: int = 1000,
    gsm_client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Return the individual `scoped_configuration` pins under an organization.

    Unlike `query_org_pin_stats` (one aggregate row per version), this returns
    one row per pin — resolving the pinned connector + version, the scope's
    display name, the manual author's email, and — for rollout-origin pins —
    the backing `connector_rollout` id and state.

    Optional filters:

    - `connector_definition_id`: restrict to a single connector definition.
    - `pinned_version_id`: restrict to pins targeting one version (the
      post-selection filter for the organization pins tab).

    Filtering by pin origin (manual / rollout / breaking-change) is done by the
    caller in Python on the returned rows via their `origin_type`, not in SQL.
    """
    return _run_sql_query(
        SELECT_ORG_CONNECTOR_PINS,
        parameters={
            "organization_id": organization_id,
            "connector_definition_id": connector_definition_id,
            "pinned_version_id": pinned_version_id,
            "limit": limit,
        },
        query_name="SELECT_ORG_CONNECTOR_PINS",
        gsm_client=gsm_client,
    )
