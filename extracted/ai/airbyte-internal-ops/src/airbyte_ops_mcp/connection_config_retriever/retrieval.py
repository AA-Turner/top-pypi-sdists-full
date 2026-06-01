# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Core retrieval logic for connection config retrieval.

Refactored from: live_tests/_connection_retriever/retrieval.py
Original source: airbyte-platform-internal/tools/connection-retriever/src/connection_retriever/retrieval.py

This is a minimal subset focused on retrieving unmasked source config.
For testing candidate discovery, see issue #91.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from typing import Any, Mapping

import requests
import sqlalchemy
from google.cloud import secretmanager

from airbyte_ops_mcp.connection_config_retriever.audit_logging import audit
from airbyte_ops_mcp.connection_config_retriever.secrets_resolution import (
    get_resolved_config,
)
from airbyte_ops_mcp.constants import CLOUD_REGISTRY_URL, ConnectionObject
from airbyte_ops_mcp.gcp_auth import get_secret_manager_client
from airbyte_ops_mcp.prod_db_access.db_engine import get_pool

LOGGER = logging.getLogger(__name__)

# SQL Queries
SELECT_ON_CONNECTION_NOT_EU = sqlalchemy.text(
    """
    SELECT
        source_id,
        destination_id,
        source_catalog_id,
        catalog
    FROM
        connection
    JOIN
        actor ON connection.source_id = actor.id
    JOIN
        workspace ON actor.workspace_id = workspace.id
    JOIN
        dataplane_group ON workspace.dataplane_group_id = dataplane_group.id
    WHERE
        connection.id = :connection_id
        AND dataplane_group.name != 'EU'
    """
)

SELECT_ON_CONNECTION_DATAPLANE_GROUP_IS_EU = sqlalchemy.text(
    """
    SELECT
        CASE WHEN dataplane_group.name = 'EU' THEN TRUE ELSE FALSE END AS is_eu
    FROM
        connection
    JOIN
        actor ON connection.source_id = actor.id
    JOIN
        workspace ON actor.workspace_id = workspace.id
    JOIN
        dataplane_group ON workspace.dataplane_group_id = dataplane_group.id
    WHERE
        connection.id = :connection_id
    """
)

SELECT_ON_ACTOR_WITH_ORGANIZATION = sqlalchemy.text(
    """
    SELECT
        organization_id,
        workspace_id,
        actor_definition_id,
        configuration
    FROM
        actor
    JOIN
        workspace ON workspace.id = actor.workspace_id
    WHERE
        actor.id = :actor_id
    """
)

SELECT_ON_OAUTH_PARAMETER = sqlalchemy.text(
    """
    SELECT
        organization_id,
        workspace_id,
        configuration
    FROM
        actor_oauth_parameter
    WHERE
        actor_definition_id = :actor_definition_id
    ORDER BY created_at ASC;
    """
)


@dataclass
class RetrievalMetadata:
    """Metadata about a retrieval operation for audit logging."""

    connection_id: str
    connection_object: ConnectionObject
    retrieval_reason: str


@dataclass
class TestingCandidate:
    """A connection candidate for testing."""

    connection_id: str
    connection_url: str | None = None
    stream_count: int | None = None
    last_attempt_duration_in_microseconds: int | None = None
    is_internal: bool | None = None
    streams_with_data: list[str] | None = None

    # ConnectionObject fields
    connection: str | None = None
    source_id: str | None = None
    destination_id: str | None = None

    destination_config: Mapping | None = None
    source_config: Mapping | None = None
    catalog: Mapping | None = None
    configured_catalog: Mapping | None = None
    state: list[Mapping] | None = None

    workspace_id: str | None = None
    destination_docker_image: str | None = None
    source_docker_image: str | None = None

    def update(self, **kwargs: Any) -> None:
        """Update fields from keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(
                    f"{key} is not a valid field of {self.__class__.__name__}"
                )


class ConnectionNotFoundError(Exception):
    """Raised when a connection cannot be found."""

    pass


@audit
def get_connection(
    connection_id: str,
    db_conn: sqlalchemy.Connection,
) -> Mapping | None:
    """Get connection details from the database."""
    connection_result = db_conn.execute(
        SELECT_ON_CONNECTION_NOT_EU, parameters={"connection_id": connection_id}
    ).first()
    if connection_result is None:
        raise ValueError(f"Could not find connection {connection_id}.")
    return {
        "source_id": connection_result[0],
        "destination_id": connection_result[1],
        "source_catalog_id": connection_result[2],
        "catalog": connection_result[3],
    }


def get_actor_config(
    actor_id: str,
    db_conn: sqlalchemy.Connection,
    secret_manager_client: secretmanager.SecretManagerServiceClient,
) -> Mapping | None:
    """Get resolved actor configuration with secrets."""
    actor_result = db_conn.execute(
        SELECT_ON_ACTOR_WITH_ORGANIZATION, parameters={"actor_id": actor_id}
    ).first()
    if actor_result is None:
        raise ValueError(f"Could not find actor configuration for actor {actor_id}.")
    organization_id, workspace_id, actor_definition_id, actor_configuration = (
        actor_result
    )

    spec = get_spec(actor_definition_id)
    oauth_parameter_configuration = _get_oauth_parameters_overrides(
        db_conn, actor_definition_id, organization_id, workspace_id
    )
    return get_resolved_config(
        secret_manager_client, actor_configuration, oauth_parameter_configuration, spec
    )


def _get_oauth_parameters_overrides(
    db_conn: sqlalchemy.Connection,
    actor_definition_id: str,
    actor_organization_id: str,
    actor_workspace_id: str,
) -> dict:
    """Get OAuth parameter overrides for an actor.

    Priority:
    1. Same workspace and organization id
    2. Same workspace
    3. Same organization
    4. Default parameters
    """
    oauth_actor_parameters = db_conn.execute(
        SELECT_ON_OAUTH_PARAMETER,
        parameters={"actor_definition_id": actor_definition_id},
    ).fetchall()
    if not oauth_actor_parameters:
        return {}

    organization_override = None
    workspace_override = None
    default = None
    for (
        oauth_organization_id,
        oauth_workspace_id,
        oauth_parameter_configuration,
    ) in oauth_actor_parameters:
        if (
            oauth_organization_id == actor_organization_id
            and oauth_workspace_id == actor_workspace_id
        ):
            # Most precise case - return early
            return oauth_parameter_configuration

        if (
            oauth_organization_id == actor_organization_id
            and oauth_workspace_id is None
        ):
            if organization_override is not None:
                raise ValueError(
                    "Multiple oauth parameters overrides for this actor_definition_id "
                    "for this organization"
                )
            organization_override = oauth_parameter_configuration
        elif oauth_workspace_id == actor_workspace_id:
            if workspace_override is not None:
                raise ValueError(
                    "Multiple oauth parameters overrides for this actor_definition_id "
                    "for this workspace"
                )
            workspace_override = oauth_parameter_configuration
        elif oauth_organization_id is None and oauth_workspace_id is None:
            default = oauth_parameter_configuration

    if workspace_override is not None:
        return workspace_override
    elif organization_override is not None:
        return organization_override
    elif default is not None:
        return default
    return {}


@audit
def get_source_config(
    source_id: str,
    db_conn: sqlalchemy.Connection,
    secret_manager_client: secretmanager.SecretManagerServiceClient,
) -> Mapping | None:
    """Get resolved source configuration with secrets."""
    return get_actor_config(source_id, db_conn, secret_manager_client)


def get_registry_entries() -> list[dict]:
    """Fetch connector entries from the cloud registry."""
    registry_response = requests.get(CLOUD_REGISTRY_URL)
    registry_response.raise_for_status()
    registry = registry_response.json()
    return registry["sources"] + registry["destinations"]


def get_spec(actor_definition_id: uuid.UUID) -> dict:
    """Get connector spec from the cloud registry for a given actor definition id."""
    entries = get_registry_entries()
    try:
        return next(
            entry["spec"]
            for entry in entries
            if (
                entry.get("sourceDefinitionId") == str(actor_definition_id)
                or entry.get("destinationDefinitionId") == str(actor_definition_id)
            )
        )
    except StopIteration as err:
        raise ValueError(
            f"Could not find spec for actor definition {actor_definition_id}."
        ) from err


def retrieve_objects(
    connection_objects: list[ConnectionObject],
    retrieval_reason: str,
    connection_id: str,
) -> list[TestingCandidate]:
    """Retrieve connection objects for a given connection ID.

    This is a simplified version that only supports retrieval by connection_id.
    For testing candidate discovery by docker image, see issue #91.
    """
    connection_candidates = [TestingCandidate(connection_id=connection_id)]

    secret_manager_client = get_secret_manager_client()
    connection_pool = get_pool(secret_manager_client)

    with connection_pool.connect() as db_conn:
        for candidate in connection_candidates.copy():
            is_eu_result = db_conn.execute(
                SELECT_ON_CONNECTION_DATAPLANE_GROUP_IS_EU,
                parameters={"connection_id": candidate.connection_id},
            ).first()
            if is_eu_result is None:
                raise ConnectionNotFoundError(
                    f"Credentials were not found for connection ID {candidate.connection_id}."
                )
            elif is_eu_result[0] is True:
                connection_candidates.remove(candidate)
                LOGGER.warning(
                    f"Credential retrieval not permitted; the data residency for "
                    f"connection ID {candidate.connection_id} is within the EU. "
                    f"Candidate will be removed from the list"
                )
                continue

            candidate.update(
                **{
                    connection_object.value.replace("-", "_"): retrieve_object(
                        candidate.connection_id,
                        connection_object,
                        retrieval_reason,
                        db_conn,
                        secret_manager_client,
                    )
                    for connection_object in connection_objects
                }
            )

    return connection_candidates


def retrieve_object(
    connection_id: str,
    connection_object: ConnectionObject,
    retrieval_reason: str,
    db_conn: sqlalchemy.Connection,
    secret_manager_client: secretmanager.SecretManagerServiceClient,
) -> Mapping | list[Mapping] | str | None:
    """Retrieve a single connection object."""
    retrieval_metadata = RetrievalMetadata(
        connection_id, connection_object, retrieval_reason
    )
    connection = get_connection(retrieval_metadata, connection_id, db_conn)

    if connection_object == ConnectionObject.SOURCE_ID:
        return connection["source_id"]
    elif connection_object == ConnectionObject.DESTINATION_ID:
        return connection["destination_id"]
    elif connection_object == ConnectionObject.SOURCE_CONFIG:
        return get_source_config(
            retrieval_metadata,
            connection["source_id"],
            db_conn,
            secret_manager_client,
        )
    elif connection_object == ConnectionObject.CONFIGURED_CATALOG:
        return connection["catalog"]
    else:
        raise NotImplementedError(
            f"Connection object {connection_object} not implemented in vendored version. "
            f"Only SOURCE_CONFIG, SOURCE_ID, DESTINATION_ID, and CONFIGURED_CATALOG are supported."
        )
