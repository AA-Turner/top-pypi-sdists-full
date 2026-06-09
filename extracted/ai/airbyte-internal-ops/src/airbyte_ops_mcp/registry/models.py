# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Pydantic models for registry connector operations."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ConnectorMetadata(BaseModel):
    """Connector metadata from metadata.yaml.

    This model represents the essential metadata about a connector
    read from its metadata.yaml file in the Airbyte monorepo.
    """

    name: str = Field(description="The connector technical name")
    docker_repository: str = Field(description="The Docker repository")
    docker_image_tag: str = Field(description="The Docker image tag/version")
    support_level: str | None = Field(
        default=None, description="The support level (certified, community, etc.)"
    )
    definition_id: str | None = Field(
        default=None, description="The connector definition ID"
    )


class MetadataPublishResult(BaseModel):
    """Result of a metadata publish operation to GCS.

    This model provides detailed information about the outcome of
    publishing connector metadata to the registry.
    """

    connector_name: str = Field(description="The connector technical name")
    version: str = Field(description="The version that was published")
    bucket_name: str = Field(description="The GCS bucket name")
    versioned_path: str = Field(description="The versioned GCS path")
    latest_path: str | None = Field(
        default=None, description="The latest GCS path if updated"
    )
    versioned_uploaded: bool = Field(
        default=False, description="Whether the versioned metadata was uploaded"
    )
    latest_uploaded: bool = Field(
        default=False, description="Whether the latest metadata was uploaded"
    )
    status: Literal["success", "dry-run", "already-up-to-date"] = Field(
        description="The status of the operation"
    )
    message: str = Field(description="Status message describing the outcome")

    def __str__(self) -> str:
        """Return a string representation of the publish result."""
        return f"[{self.status}] {self.connector_name}:{self.version} -> {self.versioned_path}"


class RegistryEntryResult(BaseModel):
    """Result of reading a registry entry from GCS.

    This model wraps the raw metadata dictionary with additional context.
    """

    connector_name: str = Field(description="The connector technical name")
    version: str = Field(description="The version that was read")
    bucket_name: str = Field(description="The GCS bucket name")
    gcs_path: str = Field(description="The GCS path that was read")
    metadata: dict = Field(description="The raw metadata dictionary")


class ConnectorListResult(BaseModel):
    """Result of listing connectors in the registry."""

    bucket_name: str = Field(description="The GCS bucket name")
    connector_count: int = Field(description="Number of connectors found")
    connectors: list[str] = Field(description="List of connector names")


class VersionListResult(BaseModel):
    """Result of listing versions for a connector."""

    connector_name: str = Field(description="The connector technical name")
    bucket_name: str = Field(description="The GCS bucket name")
    version_count: int = Field(description="Number of versions found")
    versions: list[str] = Field(description="List of version strings")
