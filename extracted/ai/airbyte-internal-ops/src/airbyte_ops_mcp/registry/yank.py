# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Version yank operations for the connector registry.

This module provides functions to mark connector versions as yanked (withdrawn)
by placing or removing a `version-yank.yml` marker file in the version's
GCS directory. A yanked version is excluded when determining the "latest"
version of a connector.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import gcsfs
import yaml
from google.cloud.exceptions import GoogleCloudError

from airbyte_ops_mcp.registry._constants import METADATA_FOLDER
from airbyte_ops_mcp.registry._gcs_helpers import (
    get_gcs_credentials_token,
    get_gcs_storage_client,
)
from airbyte_ops_mcp.registry.markers import YANK_MARKER_FILE, unyanked_marker_file

logger = logging.getLogger(__name__)

YANK_FILE_NAME = YANK_MARKER_FILE


@dataclass
class YankResult:
    """Result of a yank or unyank operation."""

    connector_name: str
    version: str
    bucket_name: str
    action: str  # "yank" or "unyank"
    success: bool
    message: str
    dry_run: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary for JSON serialization."""
        return {
            "connector_name": self.connector_name,
            "version": self.version,
            "bucket_name": self.bucket_name,
            "action": self.action,
            "success": self.success,
            "message": self.message,
            "dry_run": self.dry_run,
        }


@dataclass
class YankedVersion:
    """A single yanked connector version discovered from its marker file."""

    connector_name: str
    version: str
    yanked_at: str = ""
    reason: str = ""
    approval_url: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary for JSON serialization."""
        return {
            "connector_name": self.connector_name,
            "version": self.version,
            "yanked_at": self.yanked_at,
            "reason": self.reason,
            "approval_url": self.approval_url,
        }


@dataclass
class YankMarkerDetail:
    """Parsed contents of a single active `version-yank.yml` marker.

    Extends the fields of `YankedVersion` with `raw`, the verbatim YAML text of
    the marker file, so callers can render either the structured fields or the
    raw marker.
    """

    connector_name: str
    version: str
    yanked_at: str = ""
    reason: str = ""
    approval_url: str = ""
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary for JSON serialization."""
        return {
            "connector_name": self.connector_name,
            "version": self.version,
            "yanked_at": self.yanked_at,
            "reason": self.reason,
            "approval_url": self.approval_url,
            "raw": self.raw,
        }


def _yanked_version_from_marker_path(
    path: str,
    *,
    base: str,
) -> tuple[str, str] | None:
    """Extract `(connector_name, version)` from a yank-marker path.

    `path` is the marker location relative to `base` (e.g. the GCS blob name
    `metadata/airbyte/{connector}/{version}/version-yank.yml` with
    `base="metadata/airbyte"`).

    Returns `None` when the path does not match the expected layout.
    """
    prefix = f"{base}/"
    if not path.startswith(prefix):
        return None
    parts = path[len(prefix) :].split("/")
    if len(parts) != 3 or parts[2] != YANK_FILE_NAME:
        return None
    return parts[0], parts[1]


def list_yanked_versions(
    bucket_name: str,
    *,
    with_details: bool = True,
) -> list[YankedVersion]:
    """List every yanked connector version in a registry bucket.

    Matches `version-yank.yml` markers under `metadata/airbyte/*/*/` with a GCS
    **server-side** `matchGlob` list, so only the marker objects are returned
    rather than enumerating the whole metadata tree (which would list every
    connector's every version's every file just to find a handful of markers).
    Returns one `YankedVersion` per marker, sorted by connector name then
    version. When `with_details` is `True`, each marker's contents are read to
    populate `yanked_at`, `reason`, and `approval_url`; markers that cannot be
    parsed still yield a row with those fields left blank.

    Requires GCS credentials resolvable by `get_gcs_credentials_token` (env
    service-account JSON or Application Default Credentials).
    """
    storage_client = get_gcs_storage_client()
    base = f"{METADATA_FOLDER}/airbyte"
    marker_glob = f"{base}/*/*/{YANK_FILE_NAME}"

    yanked: list[YankedVersion] = []
    for blob in storage_client.list_blobs(bucket_name, match_glob=marker_glob):
        parsed = _yanked_version_from_marker_path(blob.name, base=base)
        if parsed is None:
            continue
        connector_name, version = parsed
        entry = YankedVersion(connector_name=connector_name, version=version)
        if with_details:
            try:
                marker = yaml.safe_load(blob.download_as_text()) or {}
            except (GoogleCloudError, yaml.YAMLError, UnicodeDecodeError):
                # A missing/corrupt marker shouldn't hide the yanked row itself.
                marker = {}
            if isinstance(marker, dict):
                entry.yanked_at = str(marker.get("yanked_at", "") or "")
                entry.reason = str(marker.get("reason", "") or "")
                entry.approval_url = str(marker.get("approval_url", "") or "")
        yanked.append(entry)

    yanked.sort(key=lambda item: (item.connector_name, item.version))
    return yanked


def get_yank_marker(
    connector_name: str,
    version: str,
    bucket_name: str,
) -> YankMarkerDetail | None:
    """Read the active `version-yank.yml` marker for a single connector version.

    Returns a `YankMarkerDetail` (with `raw` set to the marker's verbatim YAML
    text and the parsed fields populated) when the version currently has an
    active yank marker, or `None` when it is not yanked. Historical
    `version-unyanked-*.yml` audit markers are ignored — only the live
    `version-yank.yml` marker counts.

    Requires GCS credentials resolvable by `get_gcs_credentials_token` (env
    service-account JSON or Application Default Credentials).
    """
    fs = gcsfs.GCSFileSystem(token=get_gcs_credentials_token())
    marker_path = f"{bucket_name}/{_get_yank_blob_path(connector_name, version)}"
    if not fs.exists(marker_path):
        return None
    try:
        raw = fs.cat_file(marker_path).decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return YankMarkerDetail(connector_name=connector_name, version=version)
    try:
        marker = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        marker = {}
    detail = YankMarkerDetail(
        connector_name=connector_name,
        version=version,
        raw=raw,
    )
    if isinstance(marker, dict):
        detail.yanked_at = str(marker.get("yanked_at", "") or "")
        detail.reason = str(marker.get("reason", "") or "")
        detail.approval_url = str(marker.get("approval_url", "") or "")
    return detail


def _get_yank_blob_path(connector_name: str, version: str) -> str:
    """Get the GCS blob path for a version-yank.yml marker file."""
    return f"{METADATA_FOLDER}/airbyte/{connector_name}/{version}/{YANK_FILE_NAME}"


def _get_metadata_blob_path(connector_name: str, version: str) -> str:
    """Get the GCS blob path for the version's metadata.yaml file."""
    return f"{METADATA_FOLDER}/airbyte/{connector_name}/{version}/metadata.yaml"


def yank_connector_version(
    connector_name: str,
    version: str,
    bucket_name: str,
    reason: str = "",
    approval_url: str = "",
    dry_run: bool = False,
) -> YankResult:
    """Mark a connector version as yanked by writing a version-yank.yml marker.

    The marker file is placed at:
        metadata/airbyte/{connector_name}/{version}/version-yank.yml

    Args:
        connector_name: The connector name (e.g., "source-faker").
        version: The version to yank (e.g., "1.2.3").
        bucket_name: The GCS bucket name.
        reason: Optional reason for yanking the version.
        approval_url: Optional approval evidence URL to record in the marker.
        dry_run: If True, report what would be done without writing.

    Returns:
        YankResult with details of the operation.

    Raises:
        ValueError: If the bucket is the production bucket and no override is set,
            or if the version does not exist.
    """
    yank_path = _get_yank_blob_path(connector_name, version)
    metadata_path = _get_metadata_blob_path(connector_name, version)

    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(bucket_name)

    # Verify the version exists
    metadata_blob = bucket.blob(metadata_path)
    if not metadata_blob.exists():
        return YankResult(
            connector_name=connector_name,
            version=version,
            bucket_name=bucket_name,
            action="yank",
            success=False,
            message=f"Version {version} not found for {connector_name} in {bucket_name}.",
            dry_run=dry_run,
        )

    # Check if already yanked
    yank_blob = bucket.blob(yank_path)
    if yank_blob.exists():
        return YankResult(
            connector_name=connector_name,
            version=version,
            bucket_name=bucket_name,
            action="yank",
            success=False,
            message=f"Version {version} of {connector_name} is already yanked.",
            dry_run=dry_run,
        )

    if dry_run:
        return YankResult(
            connector_name=connector_name,
            version=version,
            bucket_name=bucket_name,
            action="yank",
            success=True,
            message=f"[DRY RUN] Would yank {connector_name} {version}.",
            dry_run=True,
        )

    # Write the yank marker file
    yank_content: dict[str, Any] = {
        "yanked": True,
        "yanked_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    if reason:
        yank_content["reason"] = reason
    if approval_url:
        yank_content["approval_url"] = approval_url

    yank_yaml = yaml.dump(yank_content, default_flow_style=False)
    yank_blob.upload_from_string(yank_yaml, content_type="application/x-yaml")

    logger.info("Yanked %s version %s in %s", connector_name, version, bucket_name)

    return YankResult(
        connector_name=connector_name,
        version=version,
        bucket_name=bucket_name,
        action="yank",
        success=True,
        message=f"Successfully yanked {connector_name} {version}.",
    )


def unyank_connector_version(
    connector_name: str,
    version: str,
    bucket_name: str,
    dry_run: bool = False,
) -> YankResult:
    """Rename the active yank marker to an unyanked audit marker.

    Moves the active version-yank.yml marker at:
        metadata/airbyte/{connector_name}/{version}/version-yank.yml
    to:
        metadata/airbyte/{connector_name}/{version}/version-unyanked-yyyymmdd.yml

    Args:
        connector_name: The connector name (e.g., "source-faker").
        version: The version to unyank (e.g., "1.2.3").
        bucket_name: The GCS bucket name.
        dry_run: If True, report what would be done without writing.

    Returns:
        YankResult with details of the operation.
    """
    yank_path = _get_yank_blob_path(connector_name, version)

    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(bucket_name)

    # Check if yank marker exists
    yank_blob = bucket.blob(yank_path)
    if not yank_blob.exists():
        return YankResult(
            connector_name=connector_name,
            version=version,
            bucket_name=bucket_name,
            action="unyank",
            success=False,
            message=f"Version {version} of {connector_name} is not yanked.",
            dry_run=dry_run,
        )

    if dry_run:
        return YankResult(
            connector_name=connector_name,
            version=version,
            bucket_name=bucket_name,
            action="unyank",
            success=True,
            message=f"[DRY RUN] Would unyank {connector_name} {version}.",
            dry_run=True,
        )

    unyanked_path = _get_yank_blob_path(connector_name, version).replace(
        YANK_FILE_NAME,
        unyanked_marker_file(),
    )
    bucket.copy_blob(yank_blob, bucket, new_name=unyanked_path)
    yank_blob.delete()

    logger.info("Unyanked %s version %s in %s", connector_name, version, bucket_name)

    return YankResult(
        connector_name=connector_name,
        version=version,
        bucket_name=bucket_name,
        action="unyank",
        success=True,
        message=f"Successfully unyanked {connector_name} {version}.",
    )
