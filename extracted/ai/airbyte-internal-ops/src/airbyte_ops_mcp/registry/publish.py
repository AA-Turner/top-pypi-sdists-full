# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Core logic for registry connector publish operations.

This module provides the core functionality for publishing connectors
to the Airbyte registry, including:
- Deleting release candidate metadata blobs from GCS
- Publishing metadata to GCS
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Any

import yaml

from airbyte_ops_mcp.registry._constants import (
    LATEST_GCS_FOLDER_NAME,
    METADATA_FILE_NAME,
    METADATA_FOLDER,
    RELEASE_CANDIDATE_GCS_FOLDER_NAME,
)
from airbyte_ops_mcp.registry._gcs_helpers import (
    get_gcs_storage_client,
    upload_file_if_changed,
)
from airbyte_ops_mcp.registry.models import (
    ConnectorMetadata,
    ConnectorPublishResult,
    MetadataPublishResult,
)

logger = logging.getLogger(__name__)

CONNECTOR_PATH_PREFIX = "airbyte-integrations/connectors"


def get_connector_metadata(repo_path: Path, connector_name: str) -> ConnectorMetadata:
    """Read connector metadata from metadata.yaml.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: The connector technical name (e.g., 'source-github').

    Returns:
        ConnectorMetadata object with the connector's metadata.

    Raises:
        FileNotFoundError: If the connector directory or metadata file doesn't exist.
    """
    connector_dir = repo_path / CONNECTOR_PATH_PREFIX / connector_name
    if not connector_dir.exists():
        raise FileNotFoundError(f"Connector directory not found: {connector_dir}")

    metadata_file = connector_dir / METADATA_FILE_NAME
    if not metadata_file.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")

    with open(metadata_file) as f:
        metadata = yaml.safe_load(f)

    data = metadata.get("data", {})
    return ConnectorMetadata(
        name=connector_name,
        docker_repository=data.get("dockerRepository", f"airbyte/{connector_name}"),
        docker_image_tag=data.get("dockerImageTag", "unknown"),
        support_level=data.get("supportLevel"),
        definition_id=data.get("definitionId"),
    )


def is_valid_for_progressive_rollout(version: str) -> bool:
    """Check if a version string is valid for progressive rollout.

    Currently rejects only `-preview` versions.  All other semver
    versions (GA and RC alike) are accepted.  This gate is intentionally
    kept generic so it can be tightened or turned into a no-op in the
    future.

    Args:
        version: The version string to check.

    Returns:
        True if the version may be used in a progressive rollout,
        False if the version format is explicitly disallowed.
    """
    return "-preview." not in version


def strip_rc_suffix(version: str) -> str:
    """Strip the release candidate suffix from a version string.

    Args:
        version: The version string (e.g., '1.2.3-rc.1').

    Returns:
        The base version without RC suffix (e.g., '1.2.3').
        Returns the original version if no RC suffix is present.
    """
    if "-rc." in version:
        return version.split("-rc.")[0]
    return version


def create_progressive_rollout_blob(
    repo_path: Path,
    connector_name: str,
    dry_run: bool = False,
    bucket_name: str | None = None,
) -> ConnectorPublishResult:
    """Create the `release_candidate/metadata.yaml` blob in GCS.

    Copies the versioned metadata (e.g. `1.2.3-rc.1/metadata.yaml` or
    `2.1.0/metadata.yaml` for GA progressive rollouts) to
    `release_candidate/metadata.yaml` so the platform knows a progressive
    rollout is active for this connector.

    The connector's `metadata.yaml` on disk must declare a version that
    is valid for progressive rollout (i.e. not a `-preview` build).
    The versioned blob must already exist in GCS (i.e. the version must
    have been published first).

    Requires `GCS_CREDENTIALS` environment variable to be set.
    """
    if not bucket_name:
        raise ValueError("bucket_name is required for progressive rollout create.")

    metadata = get_connector_metadata(repo_path, connector_name)
    version = metadata.docker_image_tag
    docker_repo = metadata.docker_repository

    if not is_valid_for_progressive_rollout(version):
        return ConnectorPublishResult(
            connector=metadata.name,
            version=version,
            action="progressive-rollout-create",
            status="failure",
            docker_image=f"{docker_repo}:{version}",
            registry_updated=False,
            message=f"Version '{version}' is not valid for progressive rollout. "
            "Preview versions are not supported.",
        )

    gcp_connector_dir = f"{METADATA_FOLDER}/{docker_repo}"
    versioned_path = f"{gcp_connector_dir}/{version}/{METADATA_FILE_NAME}"
    rc_path = (
        f"{gcp_connector_dir}/{RELEASE_CANDIDATE_GCS_FOLDER_NAME}/{METADATA_FILE_NAME}"
    )

    if dry_run:
        return ConnectorPublishResult(
            connector=metadata.name,
            version=version,
            action="progressive-rollout-create",
            status="dry-run",
            docker_image=f"{docker_repo}:{version}",
            registry_updated=False,
            message=f"Would copy {versioned_path} to {rc_path}",
        )

    storage_client = get_gcs_storage_client()
    gcs_bucket = storage_client.bucket(bucket_name)

    # Verify the versioned blob exists
    versioned_blob = gcs_bucket.blob(versioned_path)
    if not versioned_blob.exists():
        return ConnectorPublishResult(
            connector=metadata.name,
            version=version,
            action="progressive-rollout-create",
            status="failure",
            docker_image=f"{docker_repo}:{version}",
            registry_updated=False,
            message=f"Versioned metadata not found: {versioned_path}. "
            "The version must be published before creating the progressive rollout marker.",
        )

    # Copy the versioned metadata to the release_candidate/ path
    gcs_bucket.copy_blob(versioned_blob, gcs_bucket, rc_path)
    logger.info(
        "Created progressive rollout metadata blob: %s (copied from %s)",
        rc_path,
        versioned_path,
    )

    return ConnectorPublishResult(
        connector=metadata.name,
        version=version,
        action="progressive-rollout-create",
        status="success",
        docker_image=f"{docker_repo}:{version}",
        registry_updated=True,
        message=f"Created release_candidate/ blob for {metadata.name} at {rc_path} "
        f"(copied from {versioned_path}).",
    )


def delete_progressive_rollout_blob(
    repo_path: Path,
    connector_name: str,
    dry_run: bool = False,
    bucket_name: str | None = None,
) -> ConnectorPublishResult:
    """Delete the `release_candidate/` metadata blob from GCS.

    This is the only GCS operation needed when finalizing a progressive
    rollout (both promote and rollback).  The versioned blob (e.g.
    `1.2.3-rc.1/metadata.yaml`) is intentionally preserved as an
    audit trail of what was actually deployed during the rollout.

    Requires `GCS_CREDENTIALS` environment variable to be set.
    """
    if not bucket_name:
        raise ValueError("bucket_name is required for progressive rollout cleanup.")

    metadata = get_connector_metadata(repo_path, connector_name)
    version = metadata.docker_image_tag
    docker_repo = metadata.docker_repository

    # NOTE: We intentionally do NOT gate on version format here.
    # In the promote workflow the on-disk version will already be bumped
    # to GA (e.g. 1.2.3) before cleanup runs.  The rc_path is derived
    # solely from docker_repo + the fixed RELEASE_CANDIDATE_GCS_FOLDER_NAME
    # constant, so the on-disk version is irrelevant.

    gcp_connector_dir = f"{METADATA_FOLDER}/{docker_repo}"
    rc_path = (
        f"{gcp_connector_dir}/{RELEASE_CANDIDATE_GCS_FOLDER_NAME}/{METADATA_FILE_NAME}"
    )

    if dry_run:
        return ConnectorPublishResult(
            connector=metadata.name,
            version=version,
            action="progressive-rollout-cleanup",
            status="dry-run",
            docker_image=f"{docker_repo}:{version}",
            registry_updated=False,
            message=f"Would delete release_candidate/ blob for {metadata.name} "
            f"(version {version}) at {rc_path}",
        )

    storage_client = get_gcs_storage_client()
    gcs_bucket = storage_client.bucket(bucket_name)
    rc_blob = gcs_bucket.blob(rc_path)

    if not rc_blob.exists():
        logger.info(
            "Progressive rollout metadata already deleted (idempotent): %s", rc_path
        )
        return ConnectorPublishResult(
            connector=metadata.name,
            version=version,
            action="progressive-rollout-cleanup",
            status="success",
            docker_image=f"{docker_repo}:{version}",
            registry_updated=False,
            message=f"Progressive rollout metadata already deleted (no-op): {rc_path}",
        )

    rc_blob.delete()
    logger.info("Deleted progressive rollout metadata blob: %s", rc_path)

    return ConnectorPublishResult(
        connector=metadata.name,
        version=version,
        action="progressive-rollout-cleanup",
        status="success",
        docker_image=f"{docker_repo}:{version}",
        registry_updated=True,
        message=f"Deleted release_candidate/ blob for {metadata.name} at {rc_path}.",
    )


def get_gcs_publish_path(
    connector_name: str,
    artifact_type: str,
    version: str = LATEST_GCS_FOLDER_NAME,
) -> str:
    """Compute the GCS path for a connector artifact for publishing.

    All connectors use the airbyte/{connector_name} convention.
    """
    artifact_files = {
        "metadata": METADATA_FILE_NAME,
        "spec": "spec.json",
        "icon": "icon.svg",
        "doc": "doc.md",
    }

    if artifact_type not in artifact_files:
        raise ValueError(
            f"Unknown artifact type: {artifact_type}. "
            f"Valid types are: {', '.join(artifact_files.keys())}"
        )

    file_name = artifact_files[artifact_type]
    return f"{METADATA_FOLDER}/airbyte/{connector_name}/{version}/{file_name}"


def publish_connector_metadata(
    connector_name: str,
    metadata: dict[str, Any],
    bucket_name: str,
    version: str,
    update_latest: bool = True,
    dry_run: bool = False,
) -> MetadataPublishResult:
    """Publish connector metadata to GCS.

    Uploads the metadata to the registry bucket at a versioned path, and optionally
    also updates the 'latest' pointer. Uses MD5 hash comparison to avoid re-uploading
    unchanged files.

    Requires GCS_CREDENTIALS environment variable to be set.
    """
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary")

    if "data" not in metadata:
        raise ValueError("Metadata must contain 'data' field")

    # Construct GCS paths using airbyte/{connector_name} convention
    versioned_blob_path = get_gcs_publish_path(connector_name, "metadata", version)
    latest_blob_path = get_gcs_publish_path(
        connector_name, "metadata", LATEST_GCS_FOLDER_NAME
    )

    if dry_run:
        message = f"[DRY RUN] Would upload metadata to gs://{bucket_name}/{versioned_blob_path}"
        if update_latest:
            message += f" and gs://{bucket_name}/{latest_blob_path}"
        logger.info(message)
        return MetadataPublishResult(
            connector_name=connector_name,
            version=version,
            bucket_name=bucket_name,
            versioned_path=versioned_blob_path,
            latest_path=latest_blob_path if update_latest else None,
            versioned_uploaded=False,
            latest_uploaded=False,
            status="dry-run",
            message=message,
        )

    # Get GCS client and bucket
    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(bucket_name)

    # Write metadata to temp file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False
    ) as tmp_file:
        yaml.dump(metadata, tmp_file)
        tmp_path = Path(tmp_file.name)

    try:
        # Upload versioned file
        versioned_uploaded, _ = upload_file_if_changed(
            local_file_path=tmp_path,
            bucket=bucket,
            blob_path=versioned_blob_path,
            disable_cache=True,
        )

        if versioned_uploaded:
            logger.info(
                f"Uploaded metadata for {connector_name} v{version} to {versioned_blob_path}"
            )
        else:
            logger.info(
                f"Versioned metadata for {connector_name} v{version} is already up to date"
            )

        # Optionally update latest pointer
        latest_uploaded = False
        if update_latest:
            latest_uploaded, _ = upload_file_if_changed(
                local_file_path=tmp_path,
                bucket=bucket,
                blob_path=latest_blob_path,
                disable_cache=True,
            )
            if latest_uploaded:
                logger.info(f"Updated latest pointer for {connector_name}")
            else:
                logger.info(
                    f"Latest pointer for {connector_name} is already up to date"
                )
    finally:
        # Clean up temp file even if upload fails
        tmp_path.unlink(missing_ok=True)

    # Determine status
    if versioned_uploaded or latest_uploaded:
        status = "success"
        message = f"Published metadata for {connector_name} v{version}"
        if versioned_uploaded:
            message += f" to {versioned_blob_path}"
        if latest_uploaded:
            message += " and updated latest"
    else:
        status = "already-up-to-date"
        message = f"Metadata for {connector_name} v{version} is already up to date"

    return MetadataPublishResult(
        connector_name=connector_name,
        version=version,
        bucket_name=bucket_name,
        versioned_path=versioned_blob_path,
        latest_path=latest_blob_path if update_latest else None,
        versioned_uploaded=versioned_uploaded,
        latest_uploaded=latest_uploaded,
        status=status,
        message=message,
    )
