# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Progressive rollout marker lifecycle operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from airbyte_ops_mcp.registry._constants import METADATA_FOLDER
from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_storage_client
from airbyte_ops_mcp.registry._resolve_gcs_paths import versioned_blob_root
from airbyte_ops_mcp.registry.markers import (
    PROGRESSIVE_ROLLOUT_MARKER_FILE,
    inactive_progressive_rollout_marker_file,
)
from airbyte_ops_mcp.registry.store import RegistryStore


@dataclass
class ProgressiveRolloutMarkerResult:
    """Result of a progressive rollout marker operation."""

    connector_name: str
    version: str | None
    bucket_name: str
    action: str
    outcome: Literal["promoted", "aborted"]
    success: bool
    message: str
    source_path: str | None = None
    target_path: str | None = None
    dry_run: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "connector_name": self.connector_name,
            "version": self.version,
            "bucket_name": self.bucket_name,
            "action": self.action,
            "outcome": self.outcome,
            "success": self.success,
            "message": self.message,
            "source_path": self.source_path,
            "target_path": self.target_path,
            "dry_run": self.dry_run,
        }


def _active_marker_blob_path(
    store: RegistryStore, connector_name: str, version: str
) -> str:
    return (
        f"{versioned_blob_root(connector_name=connector_name, version=version, store=store)}"
        f"/{PROGRESSIVE_ROLLOUT_MARKER_FILE}"
    )


def _extract_version_from_marker_path(path: str, *, connector_name: str) -> str | None:
    parts = path.split("/")
    try:
        marker_idx = len(parts) - 1
        if parts[marker_idx] != PROGRESSIVE_ROLLOUT_MARKER_FILE:
            return None
        connector_idx = parts.index(connector_name)
        version = parts[connector_idx + 1]
    except (ValueError, IndexError):
        return None
    if version in {"latest", "release_candidate"}:
        return None
    return version


def _find_active_marker_versions(
    *,
    store: RegistryStore,
    connector_name: str,
) -> list[str]:
    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(store.bucket)
    prefix_parts = [
        part
        for part in [store.prefix, METADATA_FOLDER, "airbyte", connector_name]
        if part
    ]
    prefix = "/".join(prefix_parts) + "/"
    suffix = f"/{PROGRESSIVE_ROLLOUT_MARKER_FILE}"
    versions: list[str] = []
    for blob in bucket.list_blobs(prefix=prefix):
        if not blob.name.endswith(suffix):
            continue
        version = _extract_version_from_marker_path(
            blob.name, connector_name=connector_name
        )
        if version is not None:
            versions.append(version)
    return sorted(set(versions))


def finalize_progressive_rollout_marker(
    *,
    connector_name: str,
    store: RegistryStore,
    outcome: Literal["promoted", "aborted"],
    version: str | None = None,
    dry_run: bool = False,
) -> ProgressiveRolloutMarkerResult:
    """Rename an active progressive rollout marker to a dated audit marker."""
    versions = (
        [version]
        if version
        else _find_active_marker_versions(
            store=store,
            connector_name=connector_name,
        )
    )
    if not versions:
        return ProgressiveRolloutMarkerResult(
            connector_name=connector_name,
            version=version,
            bucket_name=store.bucket,
            action="finalize",
            outcome=outcome,
            success=True,
            message=f"No active progressive rollout marker found for {connector_name}.",
            dry_run=dry_run,
        )
    if len(versions) > 1:
        return ProgressiveRolloutMarkerResult(
            connector_name=connector_name,
            version=None,
            bucket_name=store.bucket,
            action="finalize",
            outcome=outcome,
            success=False,
            message=(
                f"Found multiple active progressive rollout markers for {connector_name}: "
                f"{', '.join(versions)}. Pass --version to disambiguate."
            ),
            dry_run=dry_run,
        )

    resolved_version = versions[0]
    source_path = _active_marker_blob_path(store, connector_name, resolved_version)
    target_path = (
        source_path.rsplit("/", maxsplit=1)[0]
        + "/"
        + inactive_progressive_rollout_marker_file(outcome)
    )

    if dry_run:
        return ProgressiveRolloutMarkerResult(
            connector_name=connector_name,
            version=resolved_version,
            bucket_name=store.bucket,
            action="finalize",
            outcome=outcome,
            success=True,
            message=f"[DRY RUN] Would rename {source_path} to {target_path}.",
            source_path=source_path,
            target_path=target_path,
            dry_run=True,
        )

    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(store.bucket)
    source_blob = bucket.blob(source_path)
    if not source_blob.exists():
        return ProgressiveRolloutMarkerResult(
            connector_name=connector_name,
            version=resolved_version,
            bucket_name=store.bucket,
            action="finalize",
            outcome=outcome,
            success=True,
            message=f"No active progressive rollout marker found at {source_path}.",
            source_path=source_path,
            dry_run=False,
        )

    bucket.copy_blob(source_blob, bucket, new_name=target_path)
    source_blob.delete()
    return ProgressiveRolloutMarkerResult(
        connector_name=connector_name,
        version=resolved_version,
        bucket_name=store.bucket,
        action="finalize",
        outcome=outcome,
        success=True,
        message=f"Renamed {source_path} to {target_path}.",
        source_path=source_path,
        target_path=target_path,
    )
