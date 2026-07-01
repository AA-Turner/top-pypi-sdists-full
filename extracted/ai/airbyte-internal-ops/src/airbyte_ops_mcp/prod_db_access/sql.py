# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""SQL query templates and schema documentation for Airbyte Cloud Prod DB Replica.

Prod DB Replica Schema Reference
================================

Database: prod-configapi
Instance: prod-ab-cloud-proj:us-west3:prod-pgsql-replica

connection
----------
id, namespace_definition, namespace_format, prefix, source_id, destination_id, name,
catalog, status, schedule, manual, resource_requirements, created_at, updated_at,
source_catalog_id, schedule_type, schedule_data, non_breaking_change_preference,
breaking_change, field_selection_data, destination_catalog_id, status_reason

actor
-----
id, workspace_id, actor_definition_id, name, configuration, actor_type, tombstone,
created_at, updated_at, resource_requirements

workspace
---------
id, customer_id, name, slug, email, initial_setup_complete, anonymous_data_collection,
send_newsletter, send_security_updates, display_setup_wizard, tombstone, notifications,
first_sync_complete, feedback_complete, created_at, updated_at, webhook_operation_configs,
notification_settings, organization_id, dataplane_group_id

dataplane_group
---------------
id, organization_id, name, enabled, created_at, updated_at, tombstone

organization
------------
id, name, user_id, email, created_at, updated_at, tombstone, is_agentic

Note: Main dataplane groups are:
- 645a183f-b12b-4c6e-8ad3-99e165603450 = US (default, ~133K workspaces)
- 153996d3-208e-4887-b8b1-e5fe48104450 = US-Central (~12K workspaces)
- b9e48d61-f082-4a14-a8d0-799a907938cb = EU (~3K workspaces)

actor_definition_version
------------------------
id, actor_definition_id, created_at, updated_at, documentation_url, docker_repository,
docker_image_tag, spec, protocol_version, release_date, normalization_repository,
normalization_tag, supports_dbt, normalization_integration_type, allowed_hosts,
suggested_streams, release_stage, support_state, support_level, supports_refreshes,
cdk_version, last_published, internal_support_level, language, supports_file_transfer,
supports_data_activation, connector_ipc_options

scoped_configuration
--------------------
id, key, resource_type, resource_id, scope_type, scope_id, value, description,
reference_url, origin_type, origin, expires_at, created_at, updated_at

Note: Version overrides are stored with key='connector_version', resource_type='actor_definition',
and value=actor_definition_version.id (UUID).
Pin scope levels (scope_type / scope_id):
  - 'actor'        / actor.id              — pins a single connection's connector instance
  - 'workspace'    / workspace.id          — pins every instance of that connector in the workspace
  - 'organization' / organization_id       — pins every instance of that connector across the org
Effective pin precedence: actor > workspace > organization (most-specific wins).

jobs
----
id, config_type, scope (connection_id), config, status, started_at, created_at,
updated_at, metadata, is_scheduled

Note: status values: 'succeeded', 'failed', 'cancelled', 'running', 'incomplete'
      config_type values: 'sync', 'reset_connection', 'refresh'

attempts
--------
id, job_id, attempt_number, log_path, output, status, created_at, updated_at,
ended_at, failure_summary, processing_task_queue, attempt_sync_config

connector_rollout
-----------------
id, actor_definition_id, release_candidate_version_id, initial_version_id, state,
initial_rollout_pct, current_target_rollout_pct, final_target_rollout_pct,
has_breaking_changes, max_step_wait_time_mins, updated_by, created_at, updated_at,
completed_at, expires_at, error_msg, failed_reason, rollout_strategy, workflow_run_id,
paused_reason, filters, tag

Note: state values: 'initialized', 'workflow_started', 'in_progress', 'paused',
      'finalizing', 'succeeded', 'errored', 'failed_rolled_back', 'canceled'
      Active states: initialized, workflow_started, in_progress, paused, finalizing, errored
      Terminal states: succeeded, failed_rolled_back, canceled
"""

from __future__ import annotations

import sqlalchemy

# =============================================================================
# Connection Queries
# =============================================================================

SELECT_ORGANIZATION_AGENTIC_FLAGS = sqlalchemy.text(
    """
    SELECT
         organization.id AS organization_id,
         organization.name AS organization_name,
         organization.email,
         organization.tombstone,
         organization.is_agentic
    FROM organization
    WHERE organization.id = ANY(:organization_ids)
    ORDER BY organization.name ASC
    """
)

# Query connections by connector type (no organization filter)
# Note: pg8000 cannot determine the type of NULL parameters in patterns like
# "(:param IS NULL OR column = :param)", so we use separate queries instead
SELECT_CONNECTIONS_BY_CONNECTOR = sqlalchemy.text(
    """
    SELECT
         connection.id AS connection_id,
         connection.name AS connection_name,
         connection.source_id,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         source_actor.actor_definition_id AS source_definition_id,
         source_actor.name AS source_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM connection
    JOIN actor AS source_actor
      ON connection.source_id = source_actor.id
     AND source_actor.tombstone = false
    JOIN workspace
      ON source_actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = source_actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = source_actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = source_actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = source_actor.actor_definition_id
    WHERE
         source_actor.actor_definition_id = :connector_definition_id
     AND connection.status != 'deprecated'
    LIMIT :limit
    """
)

# Query connections by connector type, filtered by organization
SELECT_CONNECTIONS_BY_CONNECTOR_AND_ORG = sqlalchemy.text(
    """
    SELECT
         connection.id AS connection_id,
         connection.name AS connection_name,
         connection.source_id,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         source_actor.actor_definition_id AS source_definition_id,
         source_actor.name AS source_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM connection
    JOIN actor AS source_actor
      ON connection.source_id = source_actor.id
     AND source_actor.tombstone = false
    JOIN workspace
      ON source_actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = source_actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = source_actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = source_actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = source_actor.actor_definition_id
    WHERE
         source_actor.actor_definition_id = :connector_definition_id
     AND workspace.organization_id = :organization_id
     AND connection.status != 'deprecated'
    LIMIT :limit
    """
)

# Query connections by DESTINATION connector type (no organization filter)
SELECT_CONNECTIONS_BY_DESTINATION_CONNECTOR = sqlalchemy.text(
    """
    SELECT
         connection.id AS connection_id,
         connection.name AS connection_name,
         connection.destination_id,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         destination_actor.actor_definition_id AS destination_definition_id,
         destination_actor.name AS destination_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM connection
    JOIN actor AS destination_actor
      ON connection.destination_id = destination_actor.id
     AND destination_actor.tombstone = false
    JOIN workspace
      ON destination_actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = destination_actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = destination_actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = destination_actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = destination_actor.actor_definition_id
    WHERE
         destination_actor.actor_definition_id = :connector_definition_id
     AND connection.status != 'deprecated'
    LIMIT :limit
    """
)

# Query connections by DESTINATION connector type, filtered by organization
SELECT_CONNECTIONS_BY_DESTINATION_CONNECTOR_AND_ORG = sqlalchemy.text(
    """
    SELECT
         connection.id AS connection_id,
         connection.name AS connection_name,
         connection.destination_id,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         destination_actor.actor_definition_id AS destination_definition_id,
         destination_actor.name AS destination_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM connection
    JOIN actor AS destination_actor
      ON connection.destination_id = destination_actor.id
     AND destination_actor.tombstone = false
    JOIN workspace
      ON destination_actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = destination_actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = destination_actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = destination_actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = destination_actor.actor_definition_id
    WHERE
         destination_actor.actor_definition_id = :connector_definition_id
     AND workspace.organization_id = :organization_id
     AND connection.status != 'deprecated'
    LIMIT :limit
    """
)

# =============================================================================
# Connector Version Queries
# =============================================================================

SELECT_CONNECTOR_VERSIONS = sqlalchemy.text(
    """
    SELECT
         actor_definition_version.id AS version_id,
         actor_definition_version.docker_image_tag,
         actor_definition_version.docker_repository,
         actor_definition_version.release_stage,
         actor_definition_version.support_level,
         actor_definition_version.cdk_version,
         actor_definition_version.language,
         actor_definition_version.last_published,
         actor_definition_version.release_date
    FROM actor_definition_version
    WHERE
         actor_definition_version.actor_definition_id = :actor_definition_id
    ORDER BY
         actor_definition_version.last_published DESC NULLS LAST,
         actor_definition_version.created_at DESC
    """
)

# List new connector releases within the last N days
# Uses last_published (timestamp) rather than release_date (date only, often NULL)
# Note: No index on last_published, but table is small (~39K rows)
SELECT_NEW_CONNECTOR_RELEASES = sqlalchemy.text(
    """
    SELECT
         actor_definition_version.id AS version_id,
         actor_definition_version.actor_definition_id,
         actor_definition_version.docker_repository,
         actor_definition_version.docker_image_tag,
         actor_definition_version.last_published,
         actor_definition_version.release_date,
         actor_definition_version.release_stage,
         actor_definition_version.support_level,
         actor_definition_version.cdk_version,
         actor_definition_version.language,
         actor_definition_version.created_at
    FROM actor_definition_version
    WHERE
         actor_definition_version.last_published >= :cutoff_date
    ORDER BY
         actor_definition_version.last_published DESC
    LIMIT :limit
    """
)

# Find actors effectively pinned to a specific version across all scope levels.
# An actor is effectively pinned if:
#   1. It has a direct actor-level pin to that version, OR
#   2. Its workspace has a workspace-level pin to that version
#      AND the actor does NOT have an actor-level pin (which would take precedence), OR
#   3. Its organization has an org-level pin to that version
#      AND the actor has no actor-level pin AND its workspace has no workspace-level pin.
# Results include a pin_scope_type column indicating which scope the pin came from.
SELECT_ACTORS_PINNED_TO_VERSION = sqlalchemy.text(
    """
    WITH actor_pins AS (
        SELECT
             sc.scope_id AS actor_id,
             sc.resource_id AS actor_definition_id,
             sc.origin_type,
             sc.origin,
             sc.description,
             sc.reference_url,
             sc.created_at,
             sc.expires_at,
             'actor' AS pin_scope_type
        FROM scoped_configuration sc
        WHERE
             sc.key = 'connector_version'
         AND sc.scope_type = 'actor'
         AND sc.value = :actor_definition_version_id
    ),
    ws_pins AS (
        SELECT
             actor.id AS actor_id,
             actor.actor_definition_id,
             sc.origin_type,
             sc.origin,
             sc.description,
             sc.reference_url,
             sc.created_at,
             sc.expires_at,
             'workspace' AS pin_scope_type
        FROM scoped_configuration sc
        JOIN actor
          ON actor.actor_definition_id = sc.resource_id
        JOIN workspace
          ON actor.workspace_id = workspace.id
         AND sc.scope_id = workspace.id
        WHERE
             sc.key = 'connector_version'
         AND sc.scope_type = 'workspace'
         AND sc.value = :actor_definition_version_id
         AND NOT EXISTS (
             SELECT 1 FROM scoped_configuration ap
             WHERE ap.scope_type = 'actor'
               AND ap.scope_id = actor.id
               AND ap.key = 'connector_version'
               AND ap.resource_id = actor.actor_definition_id
         )
    ),
    org_pins AS (
        SELECT
             actor.id AS actor_id,
             actor.actor_definition_id,
             sc.origin_type,
             sc.origin,
             sc.description,
             sc.reference_url,
             sc.created_at,
             sc.expires_at,
             'organization' AS pin_scope_type
        FROM scoped_configuration sc
        JOIN workspace
          ON sc.scope_id = workspace.organization_id
        JOIN actor
          ON actor.workspace_id = workspace.id
         AND actor.actor_definition_id = sc.resource_id
        WHERE
             sc.key = 'connector_version'
         AND sc.scope_type = 'organization'
         AND sc.value = :actor_definition_version_id
         AND NOT EXISTS (
             SELECT 1 FROM scoped_configuration ap
             WHERE ap.scope_type = 'actor'
               AND ap.scope_id = actor.id
               AND ap.key = 'connector_version'
               AND ap.resource_id = actor.actor_definition_id
         )
         AND NOT EXISTS (
             SELECT 1 FROM scoped_configuration wp
             WHERE wp.scope_type = 'workspace'
               AND wp.scope_id = workspace.id
               AND wp.key = 'connector_version'
               AND wp.resource_id = actor.actor_definition_id
         )
    ),
    all_pins AS (
        SELECT * FROM actor_pins
        UNION ALL
        SELECT * FROM ws_pins
        UNION ALL
        SELECT * FROM org_pins
    )
    SELECT
         all_pins.actor_id,
         all_pins.actor_definition_id,
         all_pins.origin_type,
         all_pins.origin AS pinned_by_user_id,
         all_pins.description,
         all_pins.reference_url,
         all_pins.created_at,
         all_pins.expires_at,
         all_pins.pin_scope_type,
         actor.name AS actor_name,
         actor.actor_type,
         actor.workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         origin_user.name AS pinned_by_user_name,
         origin_user.email AS pinned_by_user_email
    FROM all_pins
    JOIN actor
      ON all_pins.actor_id = actor.id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN "user" origin_user
      ON all_pins.origin = CAST(origin_user.id AS TEXT)
    ORDER BY
         all_pins.created_at DESC
    """
)

# Raw scoped_configuration entries for a given version UUID.
# Unlike SELECT_ACTORS_PINNED_TO_VERSION (which expands workspace/org pins into
# per-actor rows), this returns the actual scoped_configuration rows directly.
# The total count matches the rollout query's rc_pin_count CTE.
SELECT_RAW_PINS_FOR_VERSION = sqlalchemy.text(
    """
    SELECT
         sc.scope_type AS pin_scope_type,
         sc.scope_id,
         sc.origin_type,
         sc.origin AS pinned_by_user_id,
         sc.description,
         sc.reference_url,
         sc.created_at,
         sc.expires_at,
         origin_user.name AS pinned_by_user_name,
         origin_user.email AS pinned_by_user_email
    FROM scoped_configuration sc
    LEFT JOIN "user" origin_user
        ON sc.origin = CAST(origin_user.id AS TEXT)
    WHERE sc.key = 'connector_version'
      AND sc.value = :actor_definition_version_id
    ORDER BY sc.created_at DESC
    """
)

# =============================================================================
# Sync Results Queries
# =============================================================================

# Resolve a connector version UUID to its docker_repository and docker_image_tag.
SELECT_VERSION_INFO_BY_ID = sqlalchemy.text(
    """
    SELECT
         actor_definition_version.id AS version_id,
         actor_definition_version.actor_definition_id,
         actor_definition_version.docker_repository,
         actor_definition_version.docker_image_tag
    FROM actor_definition_version
    WHERE actor_definition_version.id = :version_id
    """
)

# Resolve a connector name + version tag to a version UUID.
SELECT_VERSION_ID_BY_TAG = sqlalchemy.text(
    """
    SELECT
         actor_definition_version.id AS version_id,
         actor_definition_version.actor_definition_id,
         actor_definition_version.docker_repository,
         actor_definition_version.docker_image_tag
    FROM actor_definition_version
    WHERE actor_definition_version.docker_repository = :docker_repository
      AND actor_definition_version.docker_image_tag = :docker_image_tag
    """
)

# Get sync results for jobs that were run with a specific SOURCE connector version.
# Filters on `jobs.config->'sync'->>'sourceDefinitionVersionId'` — the version
# resolved at job-creation time — rather than the current pin state. This avoids
# false positives (pre-pin syncs counted as RC) and false negatives (post-unpin
# syncs missed). Pin columns are kept as informational output.
SELECT_SOURCE_SYNC_RESULTS_FOR_VERSION = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS job_status,
         jobs.started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         jobs.config->'sync'->>'sourceDefinitionVersionId' AS source_definition_version_id,
         jobs.config->'sync'->>'destinationDefinitionVersionId' AS destination_definition_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.source_id = actor.id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.config->'sync'->>'sourceDefinitionVersionId' = :actor_definition_version_id
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Get successful sync results for jobs that were run with a specific SOURCE version.
SELECT_SOURCE_SUCCESSFUL_SYNCS_FOR_VERSION = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         jobs.config->'sync'->>'sourceDefinitionVersionId' AS source_definition_version_id,
         jobs.config->'sync'->>'destinationDefinitionVersionId' AS destination_definition_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.source_id = actor.id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.status = 'succeeded'
     AND jobs.config->'sync'->>'sourceDefinitionVersionId' = :actor_definition_version_id
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Get sync results for jobs that were run with a specific DESTINATION connector version.
SELECT_DESTINATION_SYNC_RESULTS_FOR_VERSION = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS job_status,
         jobs.started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         jobs.config->'sync'->>'sourceDefinitionVersionId' AS source_definition_version_id,
         jobs.config->'sync'->>'destinationDefinitionVersionId' AS destination_definition_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.destination_id = actor.id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.config->'sync'->>'destinationDefinitionVersionId' = :actor_definition_version_id
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Get successful sync results for jobs that were run with a specific DESTINATION version.
SELECT_DESTINATION_SUCCESSFUL_SYNCS_FOR_VERSION = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         jobs.config->'sync'->>'sourceDefinitionVersionId' AS source_definition_version_id,
         jobs.config->'sync'->>'destinationDefinitionVersionId' AS destination_definition_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.destination_id = actor.id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.status = 'succeeded'
     AND jobs.config->'sync'->>'destinationDefinitionVersionId' = :actor_definition_version_id
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Get recent sync results for ALL actors using a SOURCE connector definition.
# Finds all actors with the given actor_definition_id and returns their sync attempts,
# regardless of whether they have explicit version pins.
# Query starts from jobs table to leverage indexed columns.
# Three LEFT JOINs on scoped_configuration resolve the effective pin across all scope
# levels (actor > workspace > organization precedence via CASE WHEN).
# Status filtering ('all', 'succeeded', 'failed') is handled at the application layer by
# selecting among different SQL query constants; this query returns all statuses.
SELECT_CONNECTION_SYNC_ACTIVITY = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS job_status,
         jobs.started_at AS job_started_at,
         jobs.created_at AS job_created_at,
         jobs.updated_at AS job_updated_at,
         attempts.id AS attempt_id,
         attempts.attempt_number,
         attempts.status AS attempt_status,
         attempts.created_at AS attempt_created_at,
         attempts.updated_at AS attempt_updated_at,
         attempts.ended_at AS attempt_ended_at,
         attempts.failure_summary,
         attempts.processing_task_queue,
         connection.name AS connection_name,
         connection.status AS connection_status,
         source_actor.id AS source_actor_id,
         source_actor.name AS source_actor_name,
         source_actor.actor_definition_id AS source_actor_definition_id,
         destination_actor.id AS destination_actor_id,
         destination_actor.name AS destination_actor_name,
         destination_actor.actor_definition_id AS destination_actor_definition_id,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor AS source_actor
      ON connection.source_id = source_actor.id
     AND source_actor.tombstone = false
    JOIN actor AS destination_actor
      ON connection.destination_id = destination_actor.id
     AND destination_actor.tombstone = false
    JOIN workspace
      ON source_actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN attempts
      ON attempts.job_id = jobs.id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.updated_at >= :start_at
     AND jobs.updated_at < :end_at
     AND (
          CAST(:status_filter AS text) = 'all'
          OR jobs.status::text = CAST(:status_filter AS text)
     )
     AND (CAST(:organization_id AS uuid) IS NULL OR workspace.organization_id = CAST(:organization_id AS uuid))
     AND (CAST(:workspace_id AS uuid) IS NULL OR workspace.id = CAST(:workspace_id AS uuid))
     AND (
          :connection_ids_is_empty
          OR jobs.scope = ANY(CAST(:connection_ids AS text[]))
     )
    ORDER BY
         jobs.updated_at DESC,
         attempts.attempt_number DESC NULLS LAST
    LIMIT :limit
    """
)

SELECT_RECENT_SYNCS_FOR_SOURCE_CONNECTOR = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS job_status,
         jobs.started_at AS job_started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         actor.tombstone AS actor_tombstone,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.source_id = actor.id
     AND actor.actor_definition_id = :connector_definition_id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Same as above but filtered to only successful syncs
SELECT_RECENT_SUCCESSFUL_SYNCS_FOR_SOURCE_CONNECTOR = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS job_status,
         jobs.started_at AS job_started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         actor.tombstone AS actor_tombstone,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.source_id = actor.id
     AND actor.actor_definition_id = :connector_definition_id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.status = 'succeeded'
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Same as above but filtered to only failed syncs
SELECT_RECENT_FAILED_SYNCS_FOR_SOURCE_CONNECTOR = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS job_status,
         jobs.started_at AS job_started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         actor.tombstone AS actor_tombstone,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.source_id = actor.id
     AND actor.actor_definition_id = :connector_definition_id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.status = 'failed'
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Get recent sync results for ALL actors using a DESTINATION connector definition.
SELECT_RECENT_SYNCS_FOR_DESTINATION_CONNECTOR = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS job_status,
         jobs.started_at AS job_started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         actor.tombstone AS actor_tombstone,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.destination_id = actor.id
     AND actor.actor_definition_id = :connector_definition_id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Same as above but filtered to only successful syncs
SELECT_RECENT_SUCCESSFUL_SYNCS_FOR_DESTINATION_CONNECTOR = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS job_status,
         jobs.started_at AS job_started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         actor.tombstone AS actor_tombstone,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.destination_id = actor.id
     AND actor.actor_definition_id = :connector_definition_id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.status = 'succeeded'
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Same as above but filtered to only failed syncs
SELECT_RECENT_FAILED_SYNCS_FOR_DESTINATION_CONNECTOR = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS job_status,
         jobs.started_at AS job_started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         actor.tombstone AS actor_tombstone,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type
    FROM jobs
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.destination_id = actor.id
     AND actor.actor_definition_id = :connector_definition_id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         jobs.config_type = 'sync'
     AND jobs.status = 'failed'
     AND jobs.updated_at >= :cutoff_date
    ORDER BY
         jobs.updated_at DESC
    LIMIT :limit
    """
)

# Get failed attempt results for ALL actors using a connector definition.
# Finds all actors with the given actor_definition_id and returns their failed sync attempts,
# regardless of whether they have explicit version pins.
# Query starts from attempts table to leverage indexed columns (ended_at, status).
# Note: This query only supports SOURCE connectors (joins via connection.source_id).
# Three LEFT JOINs on scoped_configuration resolve the effective pin across all scope
# levels (actor > workspace > organization precedence via CASE WHEN).
# Filters tombstoned actors / tombstoned workspaces / deprecated connections to match
# the convention used by sibling SELECT_RECENT_*_SYNCS_FOR_*_CONNECTOR queries.
SELECT_FAILED_SYNC_ATTEMPTS_FOR_CONNECTOR = sqlalchemy.text(
    """
    SELECT
         jobs.id AS job_id,
         jobs.scope AS connection_id,
         jobs.status AS latest_job_status,
         jobs.started_at AS job_started_at,
         jobs.updated_at AS job_updated_at,
         connection.name AS connection_name,
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin_type
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin_type
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin_type
           ELSE NULL
         END AS pin_origin_type,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.origin
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.origin
           WHEN org_pin.id IS NOT NULL THEN org_pin.origin
           ELSE NULL
         END AS pin_origin,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
           WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
           WHEN org_pin.id IS NOT NULL THEN org_pin.value
           ELSE NULL
         END AS pinned_version_id,
         CASE
           WHEN actor_pin.id IS NOT NULL THEN 'actor'
           WHEN ws_pin.id IS NOT NULL THEN 'workspace'
           WHEN org_pin.id IS NOT NULL THEN 'organization'
           ELSE NULL
         END AS pin_scope_type,
         attempts.id AS failed_attempt_id,
         attempts.attempt_number AS failed_attempt_number,
         attempts.status AS failed_attempt_status,
         attempts.created_at AS failed_attempt_created_at,
         attempts.ended_at AS failed_attempt_ended_at,
         attempts.failure_summary,
         attempts.processing_task_queue
    FROM attempts
    JOIN jobs
      ON jobs.id = attempts.job_id
     AND jobs.config_type = 'sync'
     AND jobs.updated_at >= :cutoff_date
    JOIN connection
      ON jobs.scope = connection.id::text
     AND connection.status != 'deprecated'
    JOIN actor
      ON connection.source_id = actor.id
     AND actor.actor_definition_id = :connector_definition_id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    LEFT JOIN scoped_configuration AS actor_pin
      ON actor_pin.scope_id = actor.id
     AND actor_pin.scope_type = 'actor'
     AND actor_pin.key = 'connector_version'
     AND actor_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS ws_pin
      ON ws_pin.scope_id = workspace.id
     AND ws_pin.scope_type = 'workspace'
     AND ws_pin.key = 'connector_version'
     AND ws_pin.resource_id = actor.actor_definition_id
    LEFT JOIN scoped_configuration AS org_pin
      ON org_pin.scope_id = workspace.organization_id
     AND org_pin.scope_type = 'organization'
     AND org_pin.key = 'connector_version'
     AND org_pin.resource_id = actor.actor_definition_id
    WHERE
         attempts.ended_at >= :cutoff_date
     AND attempts.status = 'failed'
    ORDER BY
         attempts.ended_at DESC
    LIMIT :limit
    """
)

# =============================================================================
# Dataplane and Workspace Queries
# =============================================================================

# List all dataplane groups with workspace counts
SELECT_DATAPLANES_LIST = sqlalchemy.text(
    """
    SELECT
         dataplane_group.id AS dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         dataplane_group.organization_id,
         dataplane_group.enabled,
         dataplane_group.tombstone,
         dataplane_group.created_at,
         COUNT(workspace.id) AS workspace_count
    FROM dataplane_group
    LEFT JOIN workspace
      ON workspace.dataplane_group_id = dataplane_group.id
     AND workspace.tombstone = false
    WHERE
         dataplane_group.tombstone = false
    GROUP BY
         dataplane_group.id,
         dataplane_group.name,
         dataplane_group.organization_id,
         dataplane_group.enabled,
         dataplane_group.tombstone,
         dataplane_group.created_at
    ORDER BY
         workspace_count DESC
    """
)

# Get workspace info including dataplane group for EU filtering
SELECT_WORKSPACE_INFO = sqlalchemy.text(
    """
    SELECT
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.slug,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         workspace.created_at,
         workspace.tombstone
    FROM workspace
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    WHERE
         workspace.id = :workspace_id
    """
)

# Get all workspaces in an organization with dataplane info
SELECT_ORG_WORKSPACES = sqlalchemy.text(
    """
    SELECT
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.slug,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         workspace.created_at,
         workspace.tombstone
    FROM workspace
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    WHERE
         workspace.organization_id = :organization_id
     AND workspace.tombstone = false
    ORDER BY
         workspace.name
    """
)

# =============================================================================
# Workspace Lookup by Email Domain
# =============================================================================

# Find workspaces by email domain
# This is useful for identifying workspaces based on user email domains
# (e.g., finding partner accounts like MotherDuck by searching for "motherduck.com")
SELECT_WORKSPACES_BY_EMAIL_DOMAIN = sqlalchemy.text(
    """
    SELECT DISTINCT
         workspace.organization_id,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.slug,
         workspace.email,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         workspace.created_at
    FROM workspace
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    WHERE
         workspace.email LIKE '%@' || :email_domain
     AND workspace.tombstone = false
    ORDER BY
         workspace.organization_id,
         workspace.name
    LIMIT :limit
    """
)

# =============================================================================
# Organization / Workspace Name Search
# =============================================================================

# Case-insensitive substring search on organization name and email.
SEARCH_ORGANIZATIONS = sqlalchemy.text(
    """
    SELECT
         organization.id AS organization_id,
         organization.name AS organization_name,
         organization.email
    FROM organization
    WHERE organization.tombstone = false
      AND (
          organization.name ILIKE '%' || :name_contains || '%'
          OR organization.email ILIKE '%' || :name_contains || '%'
      )
    ORDER BY organization.name ASC
    LIMIT :limit
    """
)

# Case-insensitive substring search on workspace name and slug.
SEARCH_WORKSPACES = sqlalchemy.text(
    """
    SELECT DISTINCT
         workspace.organization_id,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.slug,
         workspace.email,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         workspace.created_at
    FROM workspace
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    WHERE workspace.tombstone = false
      AND (
          workspace.name ILIKE '%' || :name_contains || '%'
          OR workspace.slug ILIKE '%' || :name_contains || '%'
      )
    ORDER BY workspace.name ASC
    LIMIT :limit
    """
)

# =============================================================================
# Connector Connection Stats Queries (Aggregate Counts)
# =============================================================================

# Count connections by SOURCE connector with latest attempt status breakdown
# Groups by pinned version and provides counts of succeeded/failed/other attempts
# Uses a CTE to get the latest attempt per connection, then aggregates
# Three LEFT JOINs on scoped_configuration resolve the effective pin across all scope
# levels (actor > workspace > organization precedence via CASE WHEN).
SELECT_SOURCE_CONNECTION_STATS = sqlalchemy.text(
    """
    WITH latest_attempts AS (
        SELECT DISTINCT ON (connection.id)
            connection.id AS connection_id,
            connection.status AS connection_status,
            CASE
              WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
              WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
              WHEN org_pin.id IS NOT NULL THEN org_pin.value
              ELSE NULL
            END AS pinned_version_id,
            attempts.status::text AS latest_attempt_status
        FROM connection
        JOIN actor
          ON connection.source_id = actor.id
         AND actor.actor_definition_id = :connector_definition_id
         AND actor.tombstone = false
        JOIN workspace
          ON actor.workspace_id = workspace.id
         AND workspace.tombstone = false
        LEFT JOIN scoped_configuration AS actor_pin
          ON actor_pin.scope_id = actor.id
         AND actor_pin.scope_type = 'actor'
         AND actor_pin.key = 'connector_version'
         AND actor_pin.resource_id = actor.actor_definition_id
        LEFT JOIN scoped_configuration AS ws_pin
          ON ws_pin.scope_id = workspace.id
         AND ws_pin.scope_type = 'workspace'
         AND ws_pin.key = 'connector_version'
         AND ws_pin.resource_id = actor.actor_definition_id
        LEFT JOIN scoped_configuration AS org_pin
          ON org_pin.scope_id = workspace.organization_id
         AND org_pin.scope_type = 'organization'
         AND org_pin.key = 'connector_version'
         AND org_pin.resource_id = actor.actor_definition_id
        LEFT JOIN jobs
          ON jobs.scope = connection.id::text
         AND jobs.config_type = 'sync'
         AND jobs.updated_at >= :cutoff_date
        LEFT JOIN attempts
          ON attempts.job_id = jobs.id
        WHERE
             connection.status != 'deprecated'
        ORDER BY
             connection.id,
             attempts.ended_at DESC NULLS LAST
    )
    SELECT
        pinned_version_id,
        COUNT(*) AS total_connections,
        COUNT(*) FILTER (WHERE connection_status = 'active') AS enabled_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status IS NOT NULL) AS active_connections,
        COUNT(*) FILTER (WHERE pinned_version_id IS NOT NULL) AS pinned_connections,
        COUNT(*) FILTER (WHERE pinned_version_id IS NULL) AS unpinned_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status = 'succeeded') AS succeeded_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status = 'failed') AS failed_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status = 'cancelled') AS cancelled_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status = 'running') AS running_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status IS NULL) AS unknown_connections
    FROM latest_attempts
    GROUP BY pinned_version_id
    ORDER BY total_connections DESC
    """
)

# Count connections by DESTINATION connector with latest attempt status breakdown
SELECT_DESTINATION_CONNECTION_STATS = sqlalchemy.text(
    """
    WITH latest_attempts AS (
        SELECT DISTINCT ON (connection.id)
            connection.id AS connection_id,
            connection.status AS connection_status,
            CASE
              WHEN actor_pin.id IS NOT NULL THEN actor_pin.value
              WHEN ws_pin.id IS NOT NULL THEN ws_pin.value
              WHEN org_pin.id IS NOT NULL THEN org_pin.value
              ELSE NULL
            END AS pinned_version_id,
            attempts.status::text AS latest_attempt_status
        FROM connection
        JOIN actor
          ON connection.destination_id = actor.id
         AND actor.actor_definition_id = :connector_definition_id
         AND actor.tombstone = false
        JOIN workspace
          ON actor.workspace_id = workspace.id
         AND workspace.tombstone = false
        LEFT JOIN scoped_configuration AS actor_pin
          ON actor_pin.scope_id = actor.id
         AND actor_pin.scope_type = 'actor'
         AND actor_pin.key = 'connector_version'
         AND actor_pin.resource_id = actor.actor_definition_id
        LEFT JOIN scoped_configuration AS ws_pin
          ON ws_pin.scope_id = workspace.id
         AND ws_pin.scope_type = 'workspace'
         AND ws_pin.key = 'connector_version'
         AND ws_pin.resource_id = actor.actor_definition_id
        LEFT JOIN scoped_configuration AS org_pin
          ON org_pin.scope_id = workspace.organization_id
         AND org_pin.scope_type = 'organization'
         AND org_pin.key = 'connector_version'
         AND org_pin.resource_id = actor.actor_definition_id
        LEFT JOIN jobs
          ON jobs.scope = connection.id::text
         AND jobs.config_type = 'sync'
         AND jobs.updated_at >= :cutoff_date
        LEFT JOIN attempts
          ON attempts.job_id = jobs.id
        WHERE
             connection.status != 'deprecated'
        ORDER BY
             connection.id,
             attempts.ended_at DESC NULLS LAST
    )
    SELECT
        pinned_version_id,
        COUNT(*) AS total_connections,
        COUNT(*) FILTER (WHERE connection_status = 'active') AS enabled_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status IS NOT NULL) AS active_connections,
        COUNT(*) FILTER (WHERE pinned_version_id IS NOT NULL) AS pinned_connections,
        COUNT(*) FILTER (WHERE pinned_version_id IS NULL) AS unpinned_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status = 'succeeded') AS succeeded_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status = 'failed') AS failed_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status = 'cancelled') AS cancelled_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status = 'running') AS running_connections,
        COUNT(*) FILTER (WHERE latest_attempt_status IS NULL) AS unknown_connections
    FROM latest_attempts
    GROUP BY pinned_version_id
    ORDER BY total_connections DESC
    """
)

# =============================================================================
# Stream-based Connection Queries
# =============================================================================

# Query connections by source connector type that have a specific stream enabled
# The catalog field is JSONB with structure: {"streams": [{"stream": {"name": "..."}, ...}, ...]}
SELECT_CONNECTIONS_BY_SOURCE_CONNECTOR_AND_STREAM = sqlalchemy.text(
    """
    SELECT
         connection.id AS connection_id,
         connection.name AS connection_name,
         connection.source_id,
         connection.status AS connection_status,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         source_actor.actor_definition_id AS source_definition_id,
         source_actor.name AS source_name
    FROM connection
    JOIN actor AS source_actor
      ON connection.source_id = source_actor.id
     AND source_actor.tombstone = false
    JOIN workspace
      ON source_actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    WHERE
         source_actor.actor_definition_id = :connector_definition_id
     AND connection.status = 'active'
     AND EXISTS (
         SELECT 1 FROM jsonb_array_elements(connection.catalog->'streams') AS stream
         WHERE stream->'stream'->>'name' = :stream_name
     )
    LIMIT :limit
    """
)

# Query connections by source connector type and stream, filtered by organization
SELECT_CONNECTIONS_BY_SOURCE_CONNECTOR_AND_STREAM_AND_ORG = sqlalchemy.text(
    """
    SELECT
         connection.id AS connection_id,
         connection.name AS connection_name,
         connection.source_id,
         connection.status AS connection_status,
         workspace.id AS workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name,
         source_actor.actor_definition_id AS source_definition_id,
         source_actor.name AS source_name
    FROM connection
    JOIN actor AS source_actor
      ON connection.source_id = source_actor.id
     AND source_actor.tombstone = false
    JOIN workspace
      ON source_actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    WHERE
         source_actor.actor_definition_id = :connector_definition_id
     AND workspace.organization_id = :organization_id
     AND connection.status = 'active'
     AND EXISTS (
         SELECT 1 FROM jsonb_array_elements(connection.catalog->'streams') AS stream
         WHERE stream->'stream'->>'name' = :stream_name
     )
    LIMIT :limit
    """
)

# =============================================================================
# Connection Resolution Queries
# =============================================================================

# Resolve connection IDs to their workspace and organization context
# Used by tier lookup to resolve connection_id -> workspace_id -> organization_id
SELECT_CONNECTION_WORKSPACE_DETAILS = sqlalchemy.text(
    """
    SELECT
         connection.id AS connection_id,
         actor.workspace_id,
         workspace.organization_id,
         workspace.dataplane_group_id,
         dataplane_group.name AS dataplane_name
    FROM connection
    JOIN actor
      ON connection.source_id = actor.id
    JOIN workspace
      ON actor.workspace_id = workspace.id
    LEFT JOIN dataplane_group
      ON workspace.dataplane_group_id = dataplane_group.id
    WHERE
         connection.id = ANY(:connection_ids)
     AND actor.tombstone = false
     AND workspace.tombstone = false
    """
)

# =============================================================================
# Connector Rollout Queries
# =============================================================================

# List all rollouts for a connector definition, with version details
SELECT_CONNECTOR_ROLLOUTS = sqlalchemy.text(
    """
    SELECT
         cr.id AS rollout_id,
         cr.actor_definition_id,
         cr.state,
         cr.initial_rollout_pct,
         cr.current_target_rollout_pct,
         cr.final_target_rollout_pct,
         cr.has_breaking_changes,
         cr.max_step_wait_time_mins,
         cr.updated_by AS updated_by_user_id,
         rollout_user.name AS updated_by_user_name,
         rollout_user.email AS updated_by_user_email,
         cr.rollout_strategy,
         cr.workflow_run_id,
         cr.error_msg,
         cr.failed_reason,
         cr.paused_reason,
         cr.filters,
         cr.tag,
         cr.created_at,
         cr.updated_at,
         cr.completed_at,
         cr.expires_at,
         rc_version.docker_image_tag AS rc_docker_image_tag,
         rc_version.docker_repository AS rc_docker_repository,
         initial_version.docker_image_tag AS initial_docker_image_tag,
         initial_version.docker_repository AS initial_docker_repository
    FROM connector_rollout cr
    JOIN actor_definition_version rc_version
      ON cr.release_candidate_version_id = rc_version.id
    LEFT JOIN actor_definition_version initial_version
      ON cr.initial_version_id = initial_version.id
    LEFT JOIN "user" rollout_user
      ON cr.updated_by = rollout_user.id
    WHERE
         cr.actor_definition_id = :actor_definition_id
    ORDER BY
         cr.created_at DESC
    LIMIT :limit
    """
)

# List all active (non-terminal) rollouts across all connectors
# Active states: initialized, workflow_started, in_progress, paused, finalizing, errored
SELECT_ACTIVE_CONNECTOR_ROLLOUTS = sqlalchemy.text(
    """
    SELECT
         cr.id AS rollout_id,
         cr.actor_definition_id,
         cr.state,
         cr.initial_rollout_pct,
         cr.current_target_rollout_pct,
         cr.final_target_rollout_pct,
         cr.has_breaking_changes,
         cr.max_step_wait_time_mins,
         cr.updated_by AS updated_by_user_id,
         rollout_user.name AS updated_by_user_name,
         rollout_user.email AS updated_by_user_email,
         cr.rollout_strategy,
         cr.workflow_run_id,
         cr.error_msg,
         cr.failed_reason,
         cr.paused_reason,
         cr.filters,
         cr.tag,
         cr.created_at,
         cr.updated_at,
         cr.completed_at,
         cr.expires_at,
         rc_version.docker_image_tag AS rc_docker_image_tag,
         rc_version.docker_repository AS rc_docker_repository,
         initial_version.docker_image_tag AS initial_docker_image_tag,
         initial_version.docker_repository AS initial_docker_repository,
         COALESCE(rc_pins.pin_count, 0) AS rc_pin_count
    FROM connector_rollout cr
    JOIN actor_definition_version rc_version
      ON cr.release_candidate_version_id = rc_version.id
    LEFT JOIN actor_definition_version initial_version
      ON cr.initial_version_id = initial_version.id
    LEFT JOIN "user" rollout_user
      ON cr.updated_by = rollout_user.id
    LEFT JOIN (
        SELECT value::uuid AS version_id, COUNT(*) AS pin_count
        FROM scoped_configuration
        WHERE key = 'connector_version'
        GROUP BY value::uuid
    ) rc_pins ON rc_version.id = rc_pins.version_id
    WHERE
         cr.state IN ('initialized', 'workflow_started', 'in_progress', 'paused', 'finalizing', 'errored')
    ORDER BY
         cr.created_at DESC
    LIMIT :limit
    """
)

# List active (non-terminal) rollouts for a specific connector definition
# Active states: initialized, workflow_started, in_progress, paused, finalizing, errored
SELECT_ACTIVE_CONNECTOR_ROLLOUTS_BY_DEFINITION = sqlalchemy.text(
    """
    SELECT
         cr.id AS rollout_id,
         cr.actor_definition_id,
         cr.state,
         cr.initial_rollout_pct,
         cr.current_target_rollout_pct,
         cr.final_target_rollout_pct,
         cr.has_breaking_changes,
         cr.max_step_wait_time_mins,
         cr.updated_by AS updated_by_user_id,
         rollout_user.name AS updated_by_user_name,
         rollout_user.email AS updated_by_user_email,
         cr.rollout_strategy,
         cr.workflow_run_id,
         cr.error_msg,
         cr.failed_reason,
         cr.paused_reason,
         cr.filters,
         cr.tag,
         cr.created_at,
         cr.updated_at,
         cr.completed_at,
         cr.expires_at,
         rc_version.docker_image_tag AS rc_docker_image_tag,
         rc_version.docker_repository AS rc_docker_repository,
         initial_version.docker_image_tag AS initial_docker_image_tag,
         initial_version.docker_repository AS initial_docker_repository,
         COALESCE(rc_pins.pin_count, 0) AS rc_pin_count
    FROM connector_rollout cr
    JOIN actor_definition_version rc_version
      ON cr.release_candidate_version_id = rc_version.id
    LEFT JOIN actor_definition_version initial_version
      ON cr.initial_version_id = initial_version.id
    LEFT JOIN "user" rollout_user
      ON cr.updated_by = rollout_user.id
    LEFT JOIN (
        SELECT value::uuid AS version_id, COUNT(*) AS pin_count
        FROM scoped_configuration
        WHERE key = 'connector_version'
        GROUP BY value::uuid
    ) rc_pins ON rc_version.id = rc_pins.version_id
    WHERE
         cr.actor_definition_id = :actor_definition_id
     AND cr.state IN ('initialized', 'workflow_started', 'in_progress', 'paused', 'finalizing', 'errored')
    ORDER BY
         cr.created_at DESC
    LIMIT :limit
    """
)

# Get a specific rollout by ID
SELECT_CONNECTOR_ROLLOUT_BY_ID = sqlalchemy.text(
    """
    SELECT
         cr.id AS rollout_id,
         cr.actor_definition_id,
         cr.state,
         cr.initial_rollout_pct,
         cr.current_target_rollout_pct,
         cr.final_target_rollout_pct,
         cr.has_breaking_changes,
         cr.max_step_wait_time_mins,
         cr.updated_by AS updated_by_user_id,
         rollout_user.name AS updated_by_user_name,
         rollout_user.email AS updated_by_user_email,
         cr.rollout_strategy,
         cr.workflow_run_id,
         cr.error_msg,
         cr.failed_reason,
         cr.paused_reason,
         cr.filters,
         cr.tag,
         cr.created_at,
         cr.updated_at,
         cr.completed_at,
         cr.expires_at,
         rc_version.docker_image_tag AS rc_docker_image_tag,
         rc_version.docker_repository AS rc_docker_repository,
         initial_version.docker_image_tag AS initial_docker_image_tag,
         initial_version.docker_repository AS initial_docker_repository
    FROM connector_rollout cr
    JOIN actor_definition_version rc_version
      ON cr.release_candidate_version_id = rc_version.id
    LEFT JOIN actor_definition_version initial_version
      ON cr.initial_version_id = initial_version.id
    LEFT JOIN "user" rollout_user
      ON cr.updated_by = rollout_user.id
    WHERE
         cr.id = :rollout_id
    """
)

# =============================================================================
# Versions with Pins (pins-only, no rollout JOIN)
# =============================================================================

# Connector versions that have at least one scoped_configuration pin.
# Does NOT join connector_rollout, so each version appears exactly once.
SELECT_VERSIONS_WITH_PINS = sqlalchemy.text(
    """
    WITH pin_counts AS (
        SELECT
            value::uuid AS version_id,
            COUNT(*) AS pin_count,
            COALESCE(SUM(CASE WHEN origin_type = 'breaking_change' THEN 1 END), 0) AS breaking_change_pins,
            COALESCE(SUM(CASE WHEN origin_type = 'connector_rollout' THEN 1 END), 0) AS rollout_pins,
            COALESCE(SUM(CASE WHEN (origin_type IS NULL OR origin_type NOT IN ('breaking_change', 'connector_rollout'))
                          AND scope_type = 'actor' THEN 1
                END), 0) AS actor_pins,
            COALESCE(SUM(CASE WHEN scope_type = 'workspace' THEN 1 END), 0) AS workspace_pins,
            COALESCE(SUM(CASE WHEN scope_type = 'organization' THEN 1 END), 0) AS org_pins
        FROM scoped_configuration
        WHERE key = 'connector_version'
        GROUP BY value::uuid
    )
    SELECT
         versions.id AS version_id,
         versions.actor_definition_id AS connector_definition_id,
         definitions.name AS connector_name,
         versions.docker_repository,
         versions.docker_image_tag,
         versions.last_published,
         pins.pin_count,
         pins.breaking_change_pins,
         pins.rollout_pins,
         pins.actor_pins,
         pins.workspace_pins,
         pins.org_pins
    FROM actor_definition_version AS versions
    JOIN actor_definition AS definitions
      ON versions.actor_definition_id = definitions.id
    JOIN pin_counts AS pins
      ON versions.id = pins.version_id
    ORDER BY
         pins.pin_count DESC,
         versions.created_at DESC
    """
)

# Same as above but filtered by actor_definition_id.
SELECT_VERSIONS_WITH_PINS_BY_DEFINITION = sqlalchemy.text(
    """
    WITH pin_counts AS (
        SELECT
            value::uuid AS version_id,
            COUNT(*) AS pin_count,
            COALESCE(SUM(CASE WHEN origin_type = 'breaking_change' THEN 1 END), 0) AS breaking_change_pins,
            COALESCE(SUM(CASE WHEN origin_type = 'connector_rollout' THEN 1 END), 0) AS rollout_pins,
            COALESCE(SUM(CASE WHEN (origin_type IS NULL OR origin_type NOT IN ('breaking_change', 'connector_rollout'))
                          AND scope_type = 'actor' THEN 1
                END), 0) AS actor_pins,
            COALESCE(SUM(CASE WHEN scope_type = 'workspace' THEN 1 END), 0) AS workspace_pins,
            COALESCE(SUM(CASE WHEN scope_type = 'organization' THEN 1 END), 0) AS org_pins
        FROM scoped_configuration
        WHERE key = 'connector_version'
        GROUP BY value::uuid
    )
    SELECT
         versions.id AS version_id,
         versions.actor_definition_id AS connector_definition_id,
         definitions.name AS connector_name,
         versions.docker_repository,
         versions.docker_image_tag,
         versions.last_published,
         pins.pin_count,
         pins.breaking_change_pins,
         pins.rollout_pins,
         pins.actor_pins,
         pins.workspace_pins,
         pins.org_pins
    FROM actor_definition_version AS versions
    JOIN actor_definition AS definitions
      ON versions.actor_definition_id = definitions.id
    JOIN pin_counts AS pins
      ON versions.id = pins.version_id
    WHERE versions.actor_definition_id = :actor_definition_id
    ORDER BY
         pins.pin_count DESC,
         versions.created_at DESC
    """
)


# =============================================================================
# Connector Rollout Monitoring Queries
# =============================================================================

# Get actors pinned to a specific rollout (via scoped_configuration.origin = rollout_id)
# This shows which actors are currently participating in the rollout
SELECT_ACTORS_PINNED_TO_ROLLOUT = sqlalchemy.text(
    """
    SELECT
         actor.id AS actor_id,
         actor.name AS actor_name,
         actor.actor_definition_id,
         actor.workspace_id,
         workspace.name AS workspace_name,
         workspace.organization_id,
         scoped_configuration.origin_type AS pin_origin_type,
         scoped_configuration.origin AS pin_origin,
         scoped_configuration.created_at AS pin_created_at,
         scoped_configuration.value AS pinned_version_id
    FROM scoped_configuration
    JOIN actor
      ON scoped_configuration.scope_id = actor.id
     AND actor.tombstone = false
    JOIN workspace
      ON actor.workspace_id = workspace.id
     AND workspace.tombstone = false
    WHERE
         scoped_configuration.key = 'connector_version'
     AND scoped_configuration.scope_type = 'actor'
     AND scoped_configuration.origin = :rollout_id
    ORDER BY
         scoped_configuration.created_at DESC
    """
)
