# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Cloud connector registry lookups.

Helpers for translating between canonical connector names (e.g.
`source-github`) and definition IDs (UUIDs) by consulting the public cloud
registry. These functions are presentation-layer-agnostic and are called by
both the MCP tool layer and the CLI dispatcher.
"""

from __future__ import annotations

from functools import lru_cache

import requests
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.constants import CLOUD_REGISTRY_URL


@lru_cache
def _fetch_cloud_registry() -> dict:
    """Fetch and parse the cloud connector registry (cached).

    The result is cached for the lifetime of the process so that multiple
    lookups within a single CLI invocation / cron pass share one HTTP call.

    Wraps `requests.RequestException` (timeouts, DNS failures, etc.) and
    non-200 responses in a `PyAirbyteInputError` so callers receive a
    consistent error type.
    """
    try:
        response = requests.get(CLOUD_REGISTRY_URL, timeout=60)
    except requests.RequestException as e:
        raise PyAirbyteInputError(
            message="Cloud connector registry request failed.",
            context={"url": CLOUD_REGISTRY_URL, "error": str(e)},
        ) from e

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Cloud connector registry returned non-200 status: {response.status_code}",
            context={"response": response.text},
        )

    return response.json()


def resolve_canonical_name_to_definition_id(canonical_name: str) -> str:
    """Resolve a canonical connector name to a definition ID.

    Auto-detects whether the connector is a source or destination based on the
    canonical name prefix (`source-` or `destination-`). If no prefix is
    present, searches both sources and destinations.

    Accepts canonical names (e.g. `source-youtube-analytics`,
    `destination-duckdb`) or display names (e.g. `YouTube Analytics`,
    `DuckDB`). Returns the definition UUID.

    Raises `PyAirbyteInputError` if the canonical name cannot be resolved.
    """
    data = _fetch_cloud_registry()
    normalized_input = canonical_name.lower().strip()

    is_source = normalized_input.startswith("source-")
    is_destination = normalized_input.startswith("destination-")

    if is_source or not is_destination:
        for source in data.get("sources", []):
            source_name = source.get("name", "").lower()
            if source_name == normalized_input:
                return source["sourceDefinitionId"]
            slugified = source_name.replace(" ", "-")
            if (
                slugified == normalized_input
                or f"source-{slugified}" == normalized_input
            ):
                return source["sourceDefinitionId"]

    if is_destination or not is_source:
        for destination in data.get("destinations", []):
            destination_name = destination.get("name", "").lower()
            if destination_name == normalized_input:
                return destination["destinationDefinitionId"]
            slugified = destination_name.replace(" ", "-")
            if (
                slugified == normalized_input
                or f"destination-{slugified}" == normalized_input
            ):
                return destination["destinationDefinitionId"]

    if is_source:
        connector_type = "source"
        hint = (
            "Use the exact canonical name (e.g., 'source-youtube-analytics') "
            "or display name (e.g., 'YouTube Analytics')."
        )
    elif is_destination:
        connector_type = "destination"
        hint = (
            "Use the exact canonical name (e.g., 'destination-duckdb') "
            "or display name (e.g., 'DuckDB')."
        )
    else:
        connector_type = "connector"
        hint = (
            "Use the exact canonical name (e.g., 'source-youtube-analytics', "
            "'destination-duckdb') or display name (e.g., 'YouTube Analytics', 'DuckDB')."
        )

    raise PyAirbyteInputError(
        message=f"Could not find {connector_type} definition for canonical name: {canonical_name}",
        context={
            "hint": hint
            + " You can list available connectors using the connector registry tools.",
            "searched_for": canonical_name,
        },
    )


def resolve_definition_id_to_canonical_info(
    actor_definition_id: str,
) -> tuple[str, str]:
    """Resolve a definition UUID to a canonical name and connector type.

    Performs the inverse of `resolve_canonical_name_to_definition_id`:
    searches both sources and destinations and returns
    `(canonical_name, connector_type)` where `connector_type` is one of
    `"source"` or `"destination"`.

    Defensively skips registry entries that are missing the
    `dockerRepository` field.

    Raises `PyAirbyteInputError` if the UUID is not present in the registry.
    """
    info = resolve_definition_id_to_registry_info(actor_definition_id)
    return info[0], info[1]


def resolve_definition_id_to_registry_info(
    actor_definition_id: str,
) -> tuple[str, str, str, str]:
    """Resolve a definition UUID to connector metadata from the registry.

    Returns `(canonical_name, connector_type, latest_version, docker_repository)`
    where `connector_type` is `"source"` or `"destination"` and `latest_version`
    is the registry's `dockerImageTag` (the GA default version).

    Raises `PyAirbyteInputError` if the UUID is not present in the registry.
    """
    data = _fetch_cloud_registry()
    normalized_id = actor_definition_id.strip().lower()

    for source in data.get("sources", []):
        if source.get("sourceDefinitionId", "").lower() != normalized_id:
            continue
        docker_repository = source.get("dockerRepository")
        if not docker_repository:
            continue
        return (
            docker_repository.split("/")[-1],
            "source",
            source.get("dockerImageTag", ""),
            docker_repository,
        )

    for destination in data.get("destinations", []):
        if destination.get("destinationDefinitionId", "").lower() != normalized_id:
            continue
        docker_repository = destination.get("dockerRepository")
        if not docker_repository:
            continue
        return (
            docker_repository.split("/")[-1],
            "destination",
            destination.get("dockerImageTag", ""),
            docker_repository,
        )

    raise PyAirbyteInputError(
        message=(
            f"Could not find connector definition for actor_definition_id: "
            f"{actor_definition_id}"
        ),
        context={
            "hint": (
                "Verify the actor_definition_id (UUID) matches a connector in "
                "the cloud registry."
            ),
            "searched_for": actor_definition_id,
        },
    )
