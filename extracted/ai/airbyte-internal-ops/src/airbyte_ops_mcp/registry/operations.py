# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Registry operations for reading connector metadata from GCS.

This module provides functions for reading and listing connector metadata
from the Airbyte connector registry stored in Google Cloud Storage.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import yaml

from airbyte_ops_mcp.registry._constants import (
    LATEST_GCS_FOLDER_NAME,
    METADATA_FILE_NAME,
    METADATA_FOLDER,
    SPEC_FILE_NAME,
)
from airbyte_ops_mcp.registry._enums import (
    ConnectorLanguage,
    ConnectorType,
    SupportLevel,
)
from airbyte_ops_mcp.registry._gcs_helpers import (
    get_gcs_storage_client,
    safe_read_gcs_file,
)

logger = logging.getLogger(__name__)

# Compiled registry index path within the bucket (under optional prefix).
_REGISTRIES_PREFIX = "registries/v0"
_CLOUD_REGISTRY_INDEX = f"{_REGISTRIES_PREFIX}/cloud_registry.json"

# Public CDN base for the compiled registry index.
_CDN_BASE = "https://connectors.airbyte.com/files"


def get_registry_entry(
    connector_name: str,
    bucket_name: str,
    version: str = LATEST_GCS_FOLDER_NAME,
) -> dict[str, Any]:
    """Get a connector's registry entry from GCS.

    Reads metadata for a connector from the registry stored in GCS.

    Args:
        connector_name: The connector name (e.g., "source-faker", "destination-postgres")
        bucket_name: Name of the GCS bucket containing the registry
        version: Version folder name (e.g., "latest", "1.2.3")

    Returns:
        dict: The connector's metadata as a dictionary

    Raises:
        ValueError: If GCS credentials are not configured, or if the metadata has an invalid structure
        FileNotFoundError: If the connector metadata is not found in the registry
        yaml.YAMLError: If the metadata file contains invalid YAML syntax
    """
    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(bucket_name)

    # Construct the path to the metadata file
    # Pattern: metadata/airbyte/{connector_name}/{version}/metadata.yaml
    blob_path = (
        f"{METADATA_FOLDER}/airbyte/{connector_name}/{version}/{METADATA_FILE_NAME}"
    )
    blob = bucket.blob(blob_path)

    logger.info(f"Reading registry entry for {connector_name} from {blob_path}")

    # Read the file
    content = safe_read_gcs_file(blob)
    if content is None:
        raise FileNotFoundError(
            f"Connector metadata not found in registry: {connector_name}. "
            f"Checked path: {blob_path}"
        )

    # Parse YAML
    try:
        metadata = yaml.safe_load(content)
        if metadata is None or not isinstance(metadata, dict):
            raise ValueError(f"Metadata file {blob_path} has an invalid structure")
        return metadata
    except yaml.YAMLError as e:
        logger.error(
            "Failed to parse metadata for %s from %s: %s",
            connector_name,
            blob_path,
            e,
        )
        raise


def get_registry_spec(
    connector_name: str,
    bucket_name: str,
    version: str = LATEST_GCS_FOLDER_NAME,
) -> dict[str, Any]:
    """Get a connector's spec from GCS.

    Reads the connector specification from the registry stored in GCS.

    Args:
        connector_name: The connector name (e.g., "source-faker", "destination-postgres")
        bucket_name: Name of the GCS bucket containing the registry
        version: Version folder name (e.g., "latest", "1.2.3")

    Returns:
        dict: The connector's spec as a dictionary

    Raises:
        ValueError: If GCS credentials are not configured, or if the spec is not a JSON object
        FileNotFoundError: If the connector spec is not found in the registry
        json.JSONDecodeError: If the spec file contains invalid JSON syntax
    """
    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(bucket_name)

    # Construct the path to the spec file
    # Pattern: metadata/airbyte/{connector_name}/{version}/spec.json
    blob_path = f"{METADATA_FOLDER}/airbyte/{connector_name}/{version}/{SPEC_FILE_NAME}"
    blob = bucket.blob(blob_path)

    logger.info(f"Reading spec for {connector_name} from {blob_path}")

    # Read the file
    content = safe_read_gcs_file(blob)
    if content is None:
        raise FileNotFoundError(
            f"Connector spec not found in registry: {connector_name}. "
            f"Checked path: {blob_path}"
        )

    # Parse JSON
    try:
        spec = json.loads(content)
        if spec is None or not isinstance(spec, dict):
            raise ValueError(
                f"Spec file for {connector_name} at {blob_path} is not a JSON object"
            )
        return spec
    except json.JSONDecodeError as e:
        logger.error(
            "Failed to parse spec for %s from %s: %s",
            connector_name,
            blob_path,
            e,
        )
        raise


def list_registry_connectors(bucket_name: str) -> list[str]:
    """List all connectors in the registry.

    Scans the GCS bucket to find all connectors that have metadata files.

    Args:
        bucket_name: Name of the GCS bucket containing the registry

    Returns:
        list[str]: Sorted list of connector names

    Raises:
        ValueError: If GCS credentials are not configured
    """
    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(bucket_name)

    # List all blobs matching the pattern: metadata/airbyte/*/latest/metadata.yaml
    glob_pattern = (
        f"{METADATA_FOLDER}/airbyte/*/{LATEST_GCS_FOLDER_NAME}/{METADATA_FILE_NAME}"
    )
    logger.info(f"Listing connectors with pattern: {glob_pattern}")

    try:
        blobs = bucket.list_blobs(match_glob=glob_pattern)
    except Exception as e:
        logger.error(f"Error listing blobs in bucket {bucket_name}: {e}")
        raise

    # Extract connector names from blob paths
    # Path format: metadata/airbyte/{connector-name}/latest/metadata.yaml
    connector_names: set[str] = set()
    for blob in blobs:
        path_parts = blob.name.split("/")
        # Path should be: metadata / airbyte / connector-name / latest / metadata.yaml
        if len(path_parts) >= 5:
            connector_name = path_parts[2]
            connector_names.add(connector_name)

    return sorted(connector_names)


def list_registry_connectors_filtered(
    bucket_name: str,
    *,
    support_level: SupportLevel | None = None,
    min_support_level: SupportLevel | None = None,
    connector_type: ConnectorType | None = None,
    language: ConnectorLanguage | None = None,
    prefix: str = "",
) -> list[str]:
    """List connectors from the compiled cloud registry index with filtering.

    When any filter is applied, reads the compiled `cloud_registry.json` index
    instead of globbing individual metadata blobs. This is significantly faster
    because the index is a single JSON file containing all connector entries.

    When no filters are applied, falls back to the existing glob-based search
    which captures all connectors (including OSS-only connectors not in the
    Cloud index).

    Args:
        bucket_name: Name of the GCS bucket containing the registry.
        support_level: Exact support level to match (e.g., `SupportLevel.CERTIFIED`).
        min_support_level: Minimum support level threshold. Returns connectors
            at or above this level.
        connector_type: Filter by connector type (`ConnectorType.SOURCE` or
            `ConnectorType.DESTINATION`).
        language: Filter by implementation language (e.g., `ConnectorLanguage.PYTHON`).
        prefix: Optional bucket prefix (e.g., `"aj-test100"`).

    Returns:
        Sorted list of connector technical names (e.g., `"source-github"`).

    Raises:
        ValueError: If `support_level` and `min_support_level` are both provided.
    """
    has_filters = any([support_level, min_support_level, connector_type, language])

    if not has_filters:
        return list_registry_connectors(bucket_name=bucket_name)

    if support_level and min_support_level:
        raise ValueError(
            "Cannot specify both `support_level` and `min_support_level`. "
            "Use `support_level` for an exact match or `min_support_level` for a threshold."
        )

    entries = _read_cloud_registry_index(bucket_name=bucket_name, prefix=prefix)

    # Apply support_level exact match
    if support_level:
        entries = [e for e in entries if e.get("supportLevel") == support_level]

    # Apply min_support_level threshold
    if min_support_level:
        threshold = min_support_level.precedence
        known_levels = {m.value for m in SupportLevel}
        entries = [
            e
            for e in entries
            if e.get("supportLevel")
            and e["supportLevel"] in known_levels
            and SupportLevel(e["supportLevel"]).precedence >= threshold
        ]

    # Apply connector_type filter
    if connector_type == ConnectorType.SOURCE:
        entries = [e for e in entries if "sourceDefinitionId" in e]
    elif connector_type == ConnectorType.DESTINATION:
        entries = [e for e in entries if "destinationDefinitionId" in e]

    # Apply language filter
    if language:
        entries = [e for e in entries if e.get("language") == language]

    # Extract connector names from dockerRepository (e.g., "airbyte/source-github" -> "source-github")
    names: set[str] = set()
    for entry in entries:
        docker_repo = entry.get("dockerRepository", "")
        if "/" in docker_repo:
            names.add(docker_repo.split("/", 1)[1])
        elif docker_repo:
            names.add(docker_repo)

    return sorted(names)


def _read_cloud_registry_index(
    bucket_name: str,
    prefix: str = "",
) -> list[dict[str, Any]]:
    """Read the compiled cloud_registry.json and return all entries.

    Args:
        bucket_name: GCS bucket name.
        prefix: Optional path prefix within the bucket.

    Returns:
        Combined list of source and destination entries from the index.

    Raises:
        FileNotFoundError: If the index file does not exist.
    """
    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(bucket_name)

    path_prefix = f"{prefix}/" if prefix else ""
    blob_path = f"{path_prefix}{_CLOUD_REGISTRY_INDEX}"
    blob = bucket.blob(blob_path)

    logger.info("Reading cloud registry index from %s/%s", bucket_name, blob_path)

    content = safe_read_gcs_file(blob)
    if content is None:
        raise FileNotFoundError(
            f"Cloud registry index not found at gs://{bucket_name}/{blob_path}. "
            "Run `airbyte-ops registry store compile` to generate it."
        )

    data = json.loads(content)
    sources = data.get("sources", [])
    destinations = data.get("destinations", [])
    return sources + destinations


def list_connector_versions(connector_name: str, bucket_name: str) -> list[str]:
    """List all versions of a connector in the registry.

    Scans the GCS bucket to find all versions of a specific connector.

    Args:
        connector_name: The connector name (e.g., "source-faker")
        bucket_name: Name of the GCS bucket containing the registry

    Returns:
        list[str]: Sorted list of version strings (excluding 'latest' and 'release_candidate')

    Raises:
        ValueError: If GCS credentials are not configured
    """
    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(bucket_name)

    # List all blobs matching the pattern: metadata/airbyte/{connector_name}/*/metadata.yaml
    glob_pattern = f"{METADATA_FOLDER}/airbyte/{connector_name}/*/{METADATA_FILE_NAME}"
    logger.info(f"Listing versions for {connector_name} with pattern: {glob_pattern}")

    try:
        blobs = bucket.list_blobs(match_glob=glob_pattern)
    except Exception as e:
        logger.error(f"Error listing blobs in bucket {bucket_name}: {e}")
        raise

    # Extract versions from blob paths
    # Path format: metadata/airbyte/{connector-name}/{version}/metadata.yaml
    versions: set[str] = set()
    for blob in blobs:
        path_parts = blob.name.split("/")
        # Path should be: metadata / airbyte / connector-name / version / metadata.yaml
        if len(path_parts) >= 5:
            version = path_parts[3]
            # Exclude special folders
            if version not in ("latest", "release_candidate"):
                versions.add(version)

    return sorted(versions)
