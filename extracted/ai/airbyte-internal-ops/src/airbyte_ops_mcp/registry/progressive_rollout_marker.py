# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Progressive rollout marker lifecycle operations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal

import gcsfs
import yaml
from google.cloud.exceptions import GoogleCloudError

from airbyte_ops_mcp.registry._constants import METADATA_FOLDER
from airbyte_ops_mcp.registry._gcs_helpers import (
    get_gcs_credentials_token,
    get_gcs_storage_client,
)
from airbyte_ops_mcp.registry._resolve_gcs_paths import versioned_blob_root
from airbyte_ops_mcp.registry.markers import (
    PROGRESSIVE_ROLLOUT_MARKER_FILE,
    YANK_MARKER_FILE,
    inactive_progressive_rollout_marker_file,
    inactive_progressive_rollout_marker_parts,
)
from airbyte_ops_mcp.registry.store import RegistryStore
from airbyte_ops_mcp.registry.yank import build_yank_marker_content


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
    yank_path: str | None = None
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
            "yank_path": self.yank_path,
            "dry_run": self.dry_run,
        }


@dataclass
class ProgressiveRolloutMarkerDetail:
    """Parsed contents of an active or finalized progressive rollout marker."""

    connector_name: str
    version: str
    progressive_rollout: bool = False
    created_at: str = ""
    promotion_requested_at: str = ""
    promotion_requested_by: str = ""
    rollout_id: str = ""
    raw: str = ""
    state: Literal["active", "promoted", "aborted"] = "active"
    marker_date: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert the marker detail to a dictionary."""
        return {
            "connector_name": self.connector_name,
            "version": self.version,
            "progressive_rollout": self.progressive_rollout,
            "created_at": self.created_at,
            "promotion_requested_at": self.promotion_requested_at,
            "promotion_requested_by": self.promotion_requested_by,
            "rollout_id": self.rollout_id,
            "raw": self.raw,
            "state": self.state,
            "marker_date": self.marker_date,
        }


@dataclass
class ProgressiveRolloutMarkerAnnotationResult:
    """Result of annotating an active progressive rollout marker."""

    connector_name: str
    version: str
    bucket_name: str
    action: str
    success: bool
    message: str
    marker: ProgressiveRolloutMarkerDetail | None = None
    dry_run: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert the annotation result to a dictionary."""
        return {
            "connector_name": self.connector_name,
            "version": self.version,
            "bucket_name": self.bucket_name,
            "action": self.action,
            "success": self.success,
            "message": self.message,
            "marker": self.marker.to_dict() if self.marker else None,
            "dry_run": self.dry_run,
        }


def get_progressive_rollout_marker(
    connector_name: str,
    version: str,
    bucket_name: str,
) -> ProgressiveRolloutMarkerDetail | None:
    """Read an active or finalized progressive rollout marker.

    Returns `None` when no marker is present. Unparseable YAML is tolerated and
    still returns the marker with its raw contents.
    """
    fs = gcsfs.GCSFileSystem(
        token=get_gcs_credentials_token(),
        skip_instance_cache=True,
        use_listings_cache=False,
    )
    marker_prefix = (
        f"{bucket_name}/{METADATA_FOLDER}/airbyte/{connector_name}/{version}/"
    )
    marker_path = f"{marker_prefix}{PROGRESSIVE_ROLLOUT_MARKER_FILE}"
    state: Literal["active", "promoted", "aborted"] = "active"
    marker_date = ""
    if not fs.exists(marker_path):
        dated_paths = []
        for path in fs.glob(f"{marker_prefix}progressive-rollout-*.yml"):
            parts = inactive_progressive_rollout_marker_parts(path.rsplit("/", 1)[-1])
            if parts is not None:
                dated_paths.append((parts[1], path, parts[0]))
        if not dated_paths:
            return None
        marker_date, marker_path, state = max(dated_paths)
    try:
        raw = fs.cat_file(marker_path).decode("utf-8")
    except (GoogleCloudError, OSError, UnicodeDecodeError):
        return ProgressiveRolloutMarkerDetail(
            connector_name=connector_name,
            version=version,
            state=state,
            marker_date=marker_date,
        )
    try:
        marker = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        marker = {}
    detail = ProgressiveRolloutMarkerDetail(
        connector_name=connector_name,
        version=version,
        raw=raw,
        state=state,
        marker_date=marker_date,
    )
    if isinstance(marker, dict):
        detail.progressive_rollout = bool(marker.get("progressive_rollout", False))
        detail.created_at = str(marker.get("created_at", "") or "")
        detail.promotion_requested_at = str(
            marker.get("promotion_requested_at", "") or ""
        )
        detail.promotion_requested_by = str(
            marker.get("promotion_requested_by", "") or ""
        )
        detail.rollout_id = str(marker.get("rollout_id", "") or "")
    return detail


def annotate_progressive_rollout_marker(
    *,
    connector_name: str,
    version: str,
    bucket_name: str,
    promotion_requested_at: str | None = None,
    promotion_requested_by: str,
    rollout_id: str,
    dry_run: bool = False,
) -> ProgressiveRolloutMarkerAnnotationResult:
    """Annotate an active rollout marker without changing its path."""
    active_marker_path = (
        f"{bucket_name}/{METADATA_FOLDER}/airbyte/{connector_name}/{version}/"
        f"{PROGRESSIVE_ROLLOUT_MARKER_FILE}"
    )
    fs = gcsfs.GCSFileSystem(
        token=get_gcs_credentials_token(),
        skip_instance_cache=True,
        use_listings_cache=False,
    )
    if not fs.exists(active_marker_path):
        return ProgressiveRolloutMarkerAnnotationResult(
            connector_name=connector_name,
            version=version,
            bucket_name=bucket_name,
            action="annotate",
            success=False,
            message=(
                f"No active progressive rollout marker found for "
                f"{connector_name}:{version}."
            ),
            dry_run=dry_run,
        )
    marker = get_progressive_rollout_marker(connector_name, version, bucket_name)
    if marker is None or marker.state != "active":
        return ProgressiveRolloutMarkerAnnotationResult(
            connector_name=connector_name,
            version=version,
            bucket_name=bucket_name,
            action="annotate",
            success=False,
            message=(
                f"No active progressive rollout marker found for "
                f"{connector_name}:{version}."
            ),
            dry_run=dry_run,
        )
    requested_at = promotion_requested_at or datetime.now(timezone.utc).isoformat()
    try:
        values = yaml.safe_load(marker.raw) if marker.raw else {}
    except yaml.YAMLError:
        values = {}
    if not isinstance(values, dict):
        values = {}
    values["promotion_requested_at"] = requested_at
    values["promotion_requested_by"] = promotion_requested_by
    values["rollout_id"] = rollout_id
    content = yaml.safe_dump(values, sort_keys=False)
    if not dry_run:
        storage_client = get_gcs_storage_client()
        blob_path = (
            f"{METADATA_FOLDER}/airbyte/{connector_name}/{version}/"
            f"{PROGRESSIVE_ROLLOUT_MARKER_FILE}"
        )
        storage_client.bucket(bucket_name).blob(blob_path).upload_from_string(
            content,
            content_type="application/x-yaml",
        )
    annotated_marker = ProgressiveRolloutMarkerDetail(
        connector_name=connector_name,
        version=version,
        progressive_rollout=marker.progressive_rollout,
        created_at=marker.created_at,
        promotion_requested_at=requested_at,
        promotion_requested_by=promotion_requested_by,
        rollout_id=rollout_id,
        raw=content,
    )
    return ProgressiveRolloutMarkerAnnotationResult(
        connector_name=connector_name,
        version=version,
        bucket_name=bucket_name,
        action="annotate",
        success=True,
        message=(
            f"{'[DRY RUN] Would annotate' if dry_run else 'Annotated'} "
            f"active progressive rollout marker for {connector_name}:{version}."
        ),
        marker=annotated_marker,
        dry_run=dry_run,
    )


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
    """Finalize a rollout marker by renaming it to a dated audit marker.

    Aborting first writes a `version-yank.yml` marker so the version cannot
    become `latest` after the active rollout marker is renamed.
    """
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
    version_dir = source_path.rsplit("/", maxsplit=1)[0]
    yank_path = f"{version_dir}/{YANK_MARKER_FILE}" if outcome == "aborted" else None

    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(store.bucket)
    source_blob = bucket.blob(source_path)
    source_exists = source_blob.exists()
    target_path = (
        f"{version_dir}/{inactive_progressive_rollout_marker_file(outcome)}"
        if source_exists
        else None
    )
    yank_message = ""
    should_write_yank = False
    if outcome == "aborted":
        metadata_path = f"{version_dir}/metadata.yaml"
        if not bucket.blob(metadata_path).exists():
            yank_path = None
            yank_message = f"Skipped yank because {metadata_path} does not exist"
        elif not source_exists:
            prefix = f"{version_dir}/"
            audit_outcomes: set[str] = set()
            promoted_audit_path = None
            for blob in bucket.list_blobs(prefix=prefix):
                filename = blob.name.removeprefix(prefix)
                if "/" in filename:
                    continue
                parts = inactive_progressive_rollout_marker_parts(filename)
                if parts is None:
                    continue
                audit_outcomes.add(parts[0])
                if parts[0] == "promoted":
                    promoted_audit_path = blob.name
            if promoted_audit_path is not None:
                yank_path = None
                yank_message = (
                    f"Skipped yank because promoted marker {promoted_audit_path} exists"
                )
            elif "aborted" not in audit_outcomes:
                yank_path = None
                yank_message = (
                    "Skipped yank because no aborted rollout audit marker exists "
                    f"in {version_dir}"
                )
            elif bucket.blob(yank_path).exists():
                yank_message = f"Version already yanked at {yank_path}"
            else:
                should_write_yank = True
        else:
            yank_blob = bucket.blob(yank_path)
            if yank_blob.exists():
                yank_message = f"Version already yanked at {yank_path}"
            else:
                should_write_yank = True

    if dry_run:
        if should_write_yank:
            yank_message = f"Would write {yank_path}"
        if outcome == "aborted":
            if source_exists and should_write_yank:
                message = (
                    f"[DRY RUN] {yank_message} and then rename "
                    f"{source_path} to {target_path}."
                )
            else:
                follow_up = (
                    f"would rename {source_path} to {target_path}"
                    if source_exists
                    else f"no active progressive rollout marker found at {source_path}"
                )
                message = f"[DRY RUN] {yank_message}; {follow_up}."
        elif source_exists:
            message = f"[DRY RUN] Would rename {source_path} to {target_path}."
        else:
            message = f"[DRY RUN] No active progressive rollout marker found at {source_path}."
        return ProgressiveRolloutMarkerResult(
            connector_name=connector_name,
            version=resolved_version,
            bucket_name=store.bucket,
            action="finalize",
            outcome=outcome,
            success=True,
            message=message,
            source_path=source_path,
            target_path=target_path,
            yank_path=yank_path,
            dry_run=True,
        )

    if should_write_yank:
        bucket.blob(yank_path).upload_from_string(
            build_yank_marker_content(
                reason=f"Progressive rollout of {resolved_version} aborted."
            ),
            content_type="application/x-yaml",
        )
        yank_message = f"Wrote {yank_path}"

    if not source_exists:
        message = (
            f"{yank_message}; no active progressive rollout marker found at "
            f"{source_path}."
            if outcome == "aborted" and yank_message
            else f"No active progressive rollout marker found at {source_path}."
        )
        return ProgressiveRolloutMarkerResult(
            connector_name=connector_name,
            version=resolved_version,
            bucket_name=store.bucket,
            action="finalize",
            outcome=outcome,
            success=True,
            message=message,
            source_path=source_path,
            yank_path=yank_path,
            dry_run=False,
        )

    assert target_path is not None
    bucket.copy_blob(source_blob, bucket, new_name=target_path)
    source_blob.delete()
    message = (
        f"{yank_message}; renamed {source_path} to {target_path}."
        if outcome == "aborted"
        else f"Renamed {source_path} to {target_path}."
    )
    return ProgressiveRolloutMarkerResult(
        connector_name=connector_name,
        version=resolved_version,
        bucket_name=store.bucket,
        action="finalize",
        outcome=outcome,
        success=True,
        message=message,
        source_path=source_path,
        target_path=target_path,
        yank_path=yank_path,
    )
