# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Core logic for connector stub operations.

This module provides the core functionality for managing enterprise connector
stubs in the Airbyte Cloud catalog. The stubs are stored in GCS and appear
in the catalog as placeholder entries that direct users to a sales funnel.

The stubs are stored at:
    gs://prod-airbyte-cloud-connector-metadata-service/resources/connector_stubs/v1/connector_stubs.json
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from airbyte_ops_mcp.registry._gcs_util import (
    get_bucket_name,
    get_gcs_file_text,
    upload_gcs_file_text,
)

# Path to connector stubs file in GCS
CONNECTOR_STUBS_PATH = "resources/connector_stubs/v1/connector_stubs.json"

# Local file name for connector stubs in airbyte-enterprise repo
CONNECTOR_STUBS_FILE = "connector_stubs.json"


class ConnectorStub(BaseModel):
    """A connector stub entry for the enterprise connector catalog.

    Stubs are placeholder entries that appear in the Airbyte Cloud catalog
    for enterprise connectors. When users click on them, they are directed
    to a sales funnel rather than being able to configure the connector directly.
    """

    model_config = {"populate_by_name": True}

    id: str = Field(
        description="Unique identifier for the stub (e.g., 'source-oracle-enterprise')"
    )
    name: str = Field(description="Display name of the connector (e.g., 'Oracle')")
    url: str = Field(
        description="URL to the connector's documentation page (must be publicly accessible)"
    )
    icon: str = Field(
        description="URL to the connector's icon (typically stored in the same GCS bucket)"
    )
    definition_id: str | None = Field(
        default=None,
        description="UUID of the connector definition (if it exists in the registry)",
        alias="definitionId",
    )
    label: str | None = Field(
        default=None, description="Label for the connector (typically 'enterprise')"
    )
    type: str | None = Field(
        default=None,
        description="Type of connector (e.g., 'enterprise_source', 'enterprise_destination')",
    )
    codename: str | None = Field(
        default=None, description="Internal codename for the connector (optional)"
    )


def read_connector_stubs(bucket_name: str) -> list[dict]:
    """Read connector stubs from GCS.

    Args:
        bucket_name: The GCS bucket name.

    Returns:
        List of connector stub dictionaries.

    Raises:
        ValueError: If the file exists but contains invalid data.
    """
    content = get_gcs_file_text(bucket_name, CONNECTOR_STUBS_PATH)

    if content is None:
        return []

    stubs = json.loads(content)

    if not isinstance(stubs, list):
        raise ValueError(
            f"Expected connector_stubs.json to contain a list, got {type(stubs).__name__}"
        )

    return stubs


def write_connector_stubs(bucket_name: str, stubs: list[dict]) -> None:
    """Write connector stubs to GCS.

    Args:
        bucket_name: The GCS bucket name.
        stubs: List of connector stub dictionaries to write.
    """
    content = json.dumps(stubs, indent=2)
    upload_gcs_file_text(
        bucket_name, CONNECTOR_STUBS_PATH, content, content_type="application/json"
    )


def find_stub_by_connector(stubs: list[dict], connector: str) -> dict | None:
    """Find a stub by connector name or ID.

    Matches by:
    - Exact ID match (e.g., 'source-oracle-enterprise')
    - ID with '-enterprise' suffix (e.g., 'source-oracle' matches 'source-oracle-enterprise')
    - Name match (case-insensitive, spaces converted to hyphens)

    Args:
        stubs: List of connector stub dictionaries.
        connector: Connector name or stub ID to find.

    Returns:
        The matching stub dictionary, or None if not found.
    """
    for stub in stubs:
        stub_id = stub.get("id", "")
        # Match by exact ID or by connector name pattern
        if stub_id == connector or stub_id == f"{connector}-enterprise":
            return stub
        # Also check if the connector name matches the stub name
        if stub.get("name", "").lower().replace(" ", "-") == connector.lower():
            return stub
    return None


def load_local_stubs(repo_root: Path) -> list[dict]:
    """Load connector stubs from local repository.

    Args:
        repo_root: Path to the airbyte-enterprise repository root.

    Returns:
        List of connector stub dictionaries.

    Raises:
        FileNotFoundError: If the connector stubs file doesn't exist.
        ValueError: If the file contains invalid data.
    """
    stubs_file = repo_root / CONNECTOR_STUBS_FILE
    if not stubs_file.exists():
        raise FileNotFoundError(f"Connector stubs file not found: {stubs_file}")

    content = stubs_file.read_text()
    stubs = json.loads(content)

    if not isinstance(stubs, list):
        raise ValueError(
            f"Expected {CONNECTOR_STUBS_FILE} to contain a list, got {type(stubs).__name__}"
        )

    return stubs


def save_local_stubs(repo_root: Path, stubs: list[dict]) -> None:
    """Save connector stubs to local repository.

    Args:
        repo_root: Path to the airbyte-enterprise repository root.
        stubs: List of connector stub dictionaries to save.
    """
    stubs_file = repo_root / CONNECTOR_STUBS_FILE
    content = json.dumps(stubs, indent=2) + "\n"
    stubs_file.write_text(content)


# Re-export get_bucket_name for convenience
__all__ = [
    "CONNECTOR_STUBS_FILE",
    "CONNECTOR_STUBS_PATH",
    "ConnectorStub",
    "find_stub_by_connector",
    "get_bucket_name",
    "load_local_stubs",
    "read_connector_stubs",
    "save_local_stubs",
    "write_connector_stubs",
]
