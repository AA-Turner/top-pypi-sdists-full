# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Fetch connection configuration and catalog from Airbyte Cloud.

This module provides utilities for fetching source configuration and connection
catalog from Airbyte Cloud using the public API.
"""

from __future__ import annotations

import copy
import json
import logging
import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

import requests
from airbyte import constants
from airbyte.cloud import CloudWorkspace
from airbyte.exceptions import PyAirbyteInputError

logger = logging.getLogger(__name__)


@dataclass
class ConnectionData:
    """Data fetched from an Airbyte Cloud connection."""

    connection_id: str
    source_id: str
    source_name: str
    source_definition_id: str
    config: dict[str, Any]
    catalog: dict[str, Any]
    stream_names: list[str]
    workspace_id: str | None = None
    docker_repository: str | None = None
    docker_image_tag: str | None = None
    state: list[dict[str, Any]] | None = field(default=None)

    @property
    def connector_image(self) -> str | None:
        """Get the full connector image name with tag."""
        if self.docker_repository and self.docker_image_tag:
            return f"{self.docker_repository}:{self.docker_image_tag}"
        return None


def _get_access_token(
    client_id: str,
    client_secret: str,
) -> str:
    """Get an access token for Airbyte Cloud API."""
    auth_url = f"{constants.CLOUD_API_ROOT}/applications/token"
    response = requests.post(
        auth_url,
        json={
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to authenticate with Airbyte Cloud: {response.status_code}",
            context={"response": response.text},
        )

    return response.json()["access_token"]


def fetch_connection_data(
    connection_id: str,
    client_id: str | None = None,
    client_secret: str | None = None,
) -> ConnectionData:
    """Fetch connection configuration and catalog from Airbyte Cloud.

    Args:
        connection_id: The connection ID to fetch data for.
        client_id: Airbyte Cloud client ID (defaults to env var).
        client_secret: Airbyte Cloud client secret (defaults to env var).

    Returns:
        ConnectionData with config and catalog.

    Raises:
        PyAirbyteInputError: If the API request fails.
    """
    client_id = client_id or os.getenv("AIRBYTE_CLOUD_CLIENT_ID")
    client_secret = client_secret or os.getenv("AIRBYTE_CLOUD_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise PyAirbyteInputError(
            message="Missing Airbyte Cloud credentials",
            context={
                "hint": "Set AIRBYTE_CLOUD_CLIENT_ID and AIRBYTE_CLOUD_CLIENT_SECRET env vars"
            },
        )

    access_token = _get_access_token(client_id, client_secret)
    public_api_root = constants.CLOUD_API_ROOT
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Get connection details
    conn_response = requests.get(
        f"{public_api_root}/connections/{connection_id}",
        headers=headers,
        timeout=30,
    )

    if conn_response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to get connection: {conn_response.status_code}",
            context={"connection_id": connection_id, "response": conn_response.text},
        )

    conn_data = conn_response.json()
    source_id = conn_data["sourceId"]

    # Get source details (includes config)
    source_response = requests.get(
        f"{public_api_root}/sources/{source_id}",
        headers=headers,
        timeout=30,
    )

    if source_response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to get source: {source_response.status_code}",
            context={"source_id": source_id, "response": source_response.text},
        )

    source_data = source_response.json()
    source_definition_id = source_data.get("definitionId", "")

    # Try to get docker repository and image tag from source definition version
    docker_repository = None
    docker_image_tag = None
    if source_definition_id:
        try:
            # Use the Config API to get version info for the source
            config_api_root = constants.CLOUD_CONFIG_API_ROOT
            version_response = requests.post(
                f"{config_api_root}/actor_definition_versions/get_for_source",
                json={"sourceId": source_id},
                headers=headers,
                timeout=30,
            )
            if version_response.status_code == 200:
                version_data = version_response.json()
                docker_repository = version_data.get("dockerRepository")
                docker_image_tag = version_data.get("dockerImageTag")
        except Exception:
            # Non-fatal: we can still proceed without docker info
            pass

    # Build configured catalog from connection streams
    streams_config = conn_data.get("configurations", {}).get("streams", [])
    stream_names = [s["name"] for s in streams_config]

    # Build Airbyte protocol catalog format
    catalog = _build_configured_catalog(
        streams_config, source_id, headers, public_api_root
    )

    return ConnectionData(
        connection_id=connection_id,
        source_id=source_id,
        source_name=source_data.get("name", ""),
        source_definition_id=source_definition_id,
        config=source_data.get("configuration", {}),
        catalog=catalog,
        stream_names=stream_names,
        workspace_id=conn_data.get("workspaceId"),
        docker_repository=docker_repository,
        docker_image_tag=docker_image_tag,
    )


def _build_configured_catalog(
    streams_config: list[dict[str, Any]],
    source_id: str,
    headers: dict[str, str],
    public_api_root: str,
) -> dict[str, Any]:
    """Build a configured catalog from connection stream configuration.

    This creates a catalog in the Airbyte protocol format that can be used
    with connector commands.

    Args:
        streams_config: List of stream configuration dicts from the connection.
        source_id: The source ID.
        headers: HTTP headers for API requests.
        public_api_root: The Public API root URL (e.g., CLOUD_API_ROOT).

    Returns:
        A configured catalog dict in Airbyte protocol format.
    """
    # For now, create a minimal catalog structure
    # A full implementation would fetch the source's discovered catalog
    # and merge it with the connection's stream configuration
    configured_streams = []

    for stream in streams_config:
        stream_name = stream.get("name", "")
        sync_mode = stream.get("syncMode", "full_refresh")

        # Map API sync modes to protocol sync modes
        destination_sync_mode = "append"
        if "incremental" in sync_mode.lower():
            source_sync_mode = "incremental"
        else:
            source_sync_mode = "full_refresh"

        configured_stream = {
            "stream": {
                "name": stream_name,
                "json_schema": {},  # Schema would come from discover
                "supported_sync_modes": ["full_refresh", "incremental"],
            },
            "sync_mode": source_sync_mode,
            "destination_sync_mode": destination_sync_mode,
        }

        cursor_field = stream.get("cursorField")
        if cursor_field:
            configured_stream["cursor_field"] = (
                cursor_field if isinstance(cursor_field, list) else [cursor_field]
            )

        primary_key = stream.get("primaryKey")
        if primary_key:
            configured_stream["primary_key"] = primary_key

        configured_streams.append(configured_stream)

    return {"streams": configured_streams}


def save_connection_data_to_files(
    connection_data: ConnectionData,
    output_dir: Path,
) -> tuple[Path, Path, Path | None]:
    """Save connection config, catalog, and optionally state to JSON files.

    Args:
        connection_data: The connection data to save.
        output_dir: Directory to save files to.

    Returns:
        Tuple of (config_path, catalog_path, state_path). `state_path` is
        `None` when no state is available on the connection.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    config_path = output_dir / "config.json"
    catalog_path = output_dir / "catalog.json"

    config_path.write_text(json.dumps(connection_data.config, indent=2))
    catalog_path.write_text(json.dumps(connection_data.catalog, indent=2))

    state_path: Path | None = None
    if connection_data.state:
        state_path = output_dir / "state.json"
        state_path.write_text(json.dumps(connection_data.state, indent=2))

    return config_path, catalog_path, state_path


def fetch_connection_state(
    connection_data: ConnectionData,
    client_id: str | None = None,
    client_secret: str | None = None,
) -> list[dict[str, Any]] | None:
    """Fetch the current state artifact for a connection via PyAirbyte.

    Uses the workspace_id stored in `connection_data` (extracted from the
    connection API response) so callers do not need to supply it separately.

    Args:
        connection_data: Connection data (must include `workspace_id`).
        client_id: Airbyte Cloud client ID (defaults to env var).
        client_secret: Airbyte Cloud client secret (defaults to env var).

    Returns:
        List of `AirbyteStateMessage` dicts in protocol format, or `None`
        if no state is available.
    """
    workspace_id = connection_data.workspace_id
    if not workspace_id:
        workspace_id = os.getenv("AIRBYTE_CLOUD_WORKSPACE_ID")

    if not workspace_id:
        return None

    _catalog, state = fetch_connection_artifacts(
        connection_id=connection_data.connection_id,
        workspace_id=workspace_id,
        client_id=client_id,
        client_secret=client_secret,
    )
    return state


def fetch_connection_artifacts(
    connection_id: str,
    workspace_id: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    """Fetch catalog and state artifacts using PyAirbyte's `CloudConnection`.

    Returns both artifacts in Airbyte protocol format (snake_case keys),
    suitable for passing directly to a connector's `--catalog` and `--state`
    flags. Format conversion is handled by PyAirbyte's `dump_raw_catalog()`
    and `dump_raw_state()` methods.

    Returns a tuple of `(catalog, state)` where catalog is a
    `ConfiguredAirbyteCatalog` dict (or `None`) and state is a list of
    `AirbyteStateMessage` dicts (possibly empty).
    """
    workspace_id = workspace_id or os.getenv("AIRBYTE_CLOUD_WORKSPACE_ID")
    client_id = client_id or os.getenv("AIRBYTE_CLOUD_CLIENT_ID")
    client_secret = client_secret or os.getenv("AIRBYTE_CLOUD_CLIENT_SECRET")

    if not workspace_id:
        raise PyAirbyteInputError(
            message="Missing Airbyte Cloud workspace ID",
            context={"hint": "Set AIRBYTE_CLOUD_WORKSPACE_ID env var"},
        )

    workspace = CloudWorkspace(
        workspace_id=workspace_id,
        client_id=client_id,
        client_secret=client_secret,
    )
    connection = workspace.get_connection(connection_id)

    catalog = connection.dump_raw_catalog()
    state = connection.dump_raw_state()

    return catalog, state


def streams_missing_schemas(catalog: dict[str, Any]) -> list[str]:
    """Return names of configured streams whose `json_schema` is empty or absent."""
    return [
        configured.get("stream", {}).get("name", "")
        for configured in catalog.get("streams", [])
        if not configured.get("stream", {}).get("json_schema")
    ]


def merge_stream_schemas(
    catalog: dict[str, Any],
    schema_source_catalog: dict[str, Any],
) -> tuple[dict[str, Any], int]:
    """Fill empty per-stream `json_schema` values from another catalog.

    Both inputs must be in configured-catalog shape (`{"streams":
    [{"stream": {...}}]}`); a flat discovered `AirbyteCatalog` is not
    supported. Matches streams by name and accepts both `jsonSchema`
    (platform camelCase) and `json_schema` (protocol snake_case) keys in the
    source catalog. The public-API catalog carries no stream namespace, so
    matching is name-only; a warning is logged when the source catalog has
    duplicate stream names across namespaces. Streams that already have a
    non-empty `json_schema` are left untouched. The input `catalog` is not
    mutated.

    Returns:
        Tuple of `(merged_catalog, merged_stream_count)`.
    """
    schemas_by_name: dict[str, dict[str, Any]] = {}
    for configured in schema_source_catalog.get("streams", []):
        stream = configured.get("stream", {})
        name = stream.get("name")
        schema = stream.get("jsonSchema") or stream.get("json_schema")
        if name and schema:
            if name in schemas_by_name and schemas_by_name[name] != schema:
                logger.warning(
                    f"Duplicate stream name {name!r} in schema source catalog "
                    "(likely the same table in multiple namespaces); "
                    "name-only matching will use the last occurrence"
                )
            schemas_by_name[name] = schema

    merged_catalog = copy.deepcopy(catalog)
    merged_count = 0
    for configured in merged_catalog.get("streams", []):
        stream = configured.get("stream", {})
        schema = schemas_by_name.get(stream.get("name", ""))
        if schema and not stream.get("json_schema"):
            stream["json_schema"] = schema
            merged_count += 1

    return merged_catalog, merged_count


@dataclass
class CatalogSchemaEnrichment:
    """Result of `enrich_catalog_schemas_from_cloud`.

    `state` carries the connection state fetched alongside the catalog
    (the underlying PyAirbyte call always returns both), so callers that
    need a warm read can reuse it instead of making a second round trip.
    `state` is `None` when the connection has no stored state.
    """

    connection_data: ConnectionData
    merged_count: int
    state: list[dict[str, Any]] | None


def enrich_catalog_schemas_from_cloud(
    connection_data: ConnectionData,
    client_id: str | None = None,
    client_secret: str | None = None,
) -> CatalogSchemaEnrichment:
    """Fill empty per-stream `json_schema` values from the Cloud-stored catalog.

    The minimal catalog built from the public API stream list has empty
    schemas. Some connectors (e.g. property-chunking analytics streams)
    derive the fields they request from the configured catalog schema, so an
    empty schema silently yields zero records. This fetches the connection's
    full configured catalog via PyAirbyte's `dump_raw_catalog()` and merges
    each stream's schema into the existing catalog by stream name, preserving
    the configured sync modes and stream selection.

    The input `connection_data` is not mutated; its `state` field is left
    untouched. The state fetched alongside the catalog is returned on the
    result for callers to reuse.
    """
    catalog, state = fetch_connection_artifacts(
        connection_id=connection_data.connection_id,
        workspace_id=connection_data.workspace_id,
        client_id=client_id,
        client_secret=client_secret,
    )
    if not catalog:
        return CatalogSchemaEnrichment(connection_data, 0, state or None)

    merged_catalog, merged_count = merge_stream_schemas(
        connection_data.catalog, catalog
    )
    if merged_count == 0:
        return CatalogSchemaEnrichment(connection_data, 0, state or None)

    return CatalogSchemaEnrichment(
        replace(connection_data, catalog=merged_catalog), merged_count, state or None
    )
