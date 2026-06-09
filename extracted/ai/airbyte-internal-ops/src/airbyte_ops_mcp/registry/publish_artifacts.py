# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Publish locally generated connector version artifacts to a GCS registry bucket.

This module uses `gcsfs.GCSFileSystem` to upload local artifacts
to the appropriate versioned path inside a GCS registry bucket.

The GCS destination path is:

    gs://<bucket>/[<prefix>/]metadata/airbyte/<connector>/<version>/
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import gcsfs
import yaml

from airbyte_ops_mcp.registry._constants import (
    CONNECTOR_DEPENDENCY_FILE_NAME,
    SBOM_FILE_NAME,
)
from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_credentials_token
from airbyte_ops_mcp.registry._resolve_gcs_paths import (
    dependencies_blob_path,
    sbom_blob_path,
    versioned_blob_root,
)
from airbyte_ops_mcp.registry._sbom_generation import upload_sbom
from airbyte_ops_mcp.registry.markers import (
    PROGRESSIVE_ROLLOUT_MARKER_FILE,
    is_registry_state_marker_file,
)
from airbyte_ops_mcp.registry.store import RegistryStore
from airbyte_ops_mcp.registry.validate import (
    validate_metadata,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------


@dataclass
class PublishArtifactsResult:
    """Result of a version-artifacts publish operation."""

    connector_name: str
    version: str
    target: str
    gcs_destination: str
    files_uploaded: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    validation_errors: list[str] = field(default_factory=list)
    dry_run: bool = False

    @property
    def success(self) -> bool:
        return len(self.errors) == 0 and len(self.validation_errors) == 0

    @property
    def status(self) -> str:
        if self.dry_run:
            return "dry-run"
        if self.errors or self.validation_errors:
            return "completed-with-errors"
        return "success"


# ---------------------------------------------------------------------------
# Core publish logic
# ---------------------------------------------------------------------------


def _log_progress(msg: str, *args: object) -> None:
    """Log a progress message to both the logger and stderr."""
    logger.info(msg, *args)
    formatted = msg % args if args else msg
    print(formatted, file=sys.stderr, flush=True)


def _check_connector_name_matches_docker_repo(
    connector_name: str,
    artifacts_dir: Path,
) -> str | None:
    """Verify that `connector_name` matches the `dockerRepository` in metadata.

    Returns `None` when the names match (or when metadata is unavailable).
    Returns an error message string when a mismatch is detected.
    """
    metadata_file = artifacts_dir / "metadata.yaml"
    if not metadata_file.is_file():
        return None

    raw_metadata = yaml.safe_load(metadata_file.read_text())
    docker_repo: str = (raw_metadata or {}).get("data", {}).get("dockerRepository", "")
    if not docker_repo:
        return None

    docker_name = docker_repo.removeprefix("airbyte/")
    if docker_name == connector_name:
        return None

    return (
        f"Connector directory name '{connector_name}' does not match "
        f"dockerRepository '{docker_repo}' (expected directory name "
        f"'{docker_name}'). Rename the connector directory to '{docker_name}' "
        f"or update dockerRepository in metadata.yaml to "
        f"'airbyte/{connector_name}'."
    )


def _metadata_enables_progressive_rollout(artifacts_dir: Path) -> bool:
    metadata_file = artifacts_dir / "metadata.yaml"
    if not metadata_file.is_file():
        return False
    raw_metadata = yaml.safe_load(metadata_file.read_text())
    return bool(
        (raw_metadata or {})
        .get("data", {})
        .get("releases", {})
        .get("rolloutConfiguration", {})
        .get("enableProgressiveRollout")
    )


def _progressive_rollout_marker_content() -> str:
    return yaml.dump(
        {
            "progressive_rollout": True,
            "created_at": datetime.now(tz=timezone.utc).isoformat(),
        },
        default_flow_style=False,
    )


def publish_version_artifacts(
    connector_name: str,
    version: str,
    artifacts_dir: Path,
    store: RegistryStore,
    dry_run: bool = False,
    with_validate: bool = True,
) -> PublishArtifactsResult:
    """Publish locally generated artifacts to a GCS registry bucket.

    Uses `gcsfs.GCSFileSystem` to upload the local *artifacts_dir* to the
    versioned path inside the target GCS bucket.

    The target GCS path is:
        `gs://<bucket>/[<prefix>/]metadata/airbyte/<connector>/<version>/`

    Before uploading, this function validates that the `connector_name`
    (derived from the connector directory) matches the `dockerRepository`
    declared in `metadata.yaml`.  A mismatch would cause the registry
    compile step to see duplicate definition-ID entries and fail.

    Args:
        connector_name: Connector name (e.g. `source-faker`).
        version: Version string (e.g. `6.2.38`).
        artifacts_dir: Local directory containing artifacts from `generate`.
        store: Parsed store target containing bucket, prefix, and stage info.
        dry_run: If `True`, report what would be uploaded without writing.
        with_validate: If `True` (default), validate metadata before uploading.
            Pass `False` (`--no-validate`) to skip.

    Returns:
        A `PublishArtifactsResult` describing what was published.

    Raises:
        ValueError: If the connector directory name does not match
            `dockerRepository` in the generated metadata.
    """
    if not artifacts_dir.is_dir():
        raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")

    # Fail fast if the connector directory name doesn't match dockerRepository.
    # A mismatch would publish artifacts under the wrong GCS path and corrupt
    # the registry (duplicate definition-IDs under different directory names).
    mismatch_error = _check_connector_name_matches_docker_repo(
        connector_name, artifacts_dir
    )
    if mismatch_error:
        raise ValueError(mismatch_error)

    # Build the GCS destination path
    bucket_name = store.bucket
    prefix = store.prefix
    blob_root = versioned_blob_root(
        connector_name=connector_name, version=version, store=store
    )
    versioned_dest = f"gcs://{bucket_name}/{blob_root}"

    target_label = f"{bucket_name}/{prefix}" if prefix else bucket_name
    should_publish_rollout_marker = _metadata_enables_progressive_rollout(artifacts_dir)
    result = PublishArtifactsResult(
        connector_name=connector_name,
        version=version,
        target=target_label,
        gcs_destination=versioned_dest,
        dry_run=dry_run,
    )

    # --- Pre-publish validation ---
    if with_validate:
        metadata_file = artifacts_dir / "metadata.yaml"
        if metadata_file.is_file():
            raw_metadata = yaml.safe_load(metadata_file.read_text())
            metadata_data = (raw_metadata or {}).get("data", {})
            validation = validate_metadata(metadata_data=metadata_data)
            if not validation.passed:
                for err in validation.errors:
                    logger.error("Pre-publish validation error: %s", err)
                result.validation_errors = validation.errors
                return result
            logger.info(
                "Pre-publish validation passed (%d validators).",
                validation.validators_run,
            )
        else:
            logger.warning("No metadata.yaml in artifacts dir; skipping validation.")

    # Enumerate local files
    local_files = sorted(f for f in artifacts_dir.rglob("*") if f.is_file())
    if not local_files:
        result.errors.append(f"No files found in {artifacts_dir}.")
        return result

    _log_progress(
        "Publishing %d artifacts for %s@%s → %s",
        len(local_files),
        connector_name,
        version,
        versioned_dest,
    )

    # Build references used by both dry-run and real upload paths
    deps_file = artifacts_dir / CONNECTOR_DEPENDENCY_FILE_NAME
    has_deps = deps_file.is_file()
    deps_gcs_key = dependencies_blob_path(
        connector_name=connector_name, version=version, store=store
    )

    sbom_file = artifacts_dir / SBOM_FILE_NAME
    has_sbom = sbom_file.is_file()
    rollout_marker_path = f"{blob_root}/{PROGRESSIVE_ROLLOUT_MARKER_FILE}"

    if dry_run:
        for f in local_files:
            rel = f.relative_to(artifacts_dir)
            result.files_uploaded.append(str(rel))
            _log_progress("  [DRY RUN] would upload: %s", rel)
        # Report the dual-load of dependencies.json to connector_dependencies/
        if has_deps:
            result.files_uploaded.append(deps_gcs_key)
            _log_progress(
                "  [DRY RUN] would also dual-load: %s → gs://%s/%s",
                CONNECTOR_DEPENDENCY_FILE_NAME,
                bucket_name,
                deps_gcs_key,
            )
        # Report the separate sbom/ upload
        if has_sbom:
            sbom_gcs_key = sbom_blob_path(
                connector_name=connector_name,
                version=version,
                store=store,
            )
            result.files_uploaded.append(sbom_gcs_key)
            _log_progress(
                "  [DRY RUN] would also upload: %s → gs://%s/%s",
                SBOM_FILE_NAME,
                bucket_name,
                sbom_gcs_key,
            )
        if should_publish_rollout_marker:
            result.files_uploaded.append(PROGRESSIVE_ROLLOUT_MARKER_FILE)
            _log_progress(
                "  [DRY RUN] would write active marker: gs://%s/%s",
                bucket_name,
                rollout_marker_path,
            )
        return result

    # Authenticate
    token = get_gcs_credentials_token()
    fs = gcsfs.GCSFileSystem(token=token)

    # Strip gcs:// prefix for gcsfs path
    dest_path = versioned_dest.replace("gcs://", "")

    # Upload all files to the versioned path
    _log_progress("Uploading to: %s", versioned_dest)
    for f in local_files:
        rel = f.relative_to(artifacts_dir)
        remote_path = f"{dest_path}/{rel}"
        fs.put(str(f), remote_path)
        result.files_uploaded.append(str(rel))
        _log_progress("  Uploaded: %s", rel)

    # Delete remote files that don't exist locally (sync semantics)
    try:
        remote_files = fs.ls(dest_path, detail=False)
        local_rel_paths = {str(f.relative_to(artifacts_dir)) for f in local_files}
        for remote_file in remote_files:
            # Skip the directory entry itself if it appears in the listing
            if remote_file == dest_path:
                continue
            # Derive the remote relative path, matching upload semantics
            if remote_file.startswith(dest_path + "/"):
                remote_rel = remote_file[len(dest_path) + 1 :]
            else:
                remote_rel = remote_file.split("/")[-1]
            if is_registry_state_marker_file(Path(remote_rel).name):
                continue
            if remote_rel not in local_rel_paths:
                fs.rm(remote_file)
                _log_progress("  Deleted stale remote file: %s", remote_rel)
    except FileNotFoundError:
        pass  # Destination doesn't exist yet, nothing to clean

    _log_progress("Uploaded %d files to %s", len(local_files), versioned_dest)

    if should_publish_rollout_marker:
        marker_remote = f"{bucket_name}/{rollout_marker_path}"
        with fs.open(marker_remote, "w") as marker_file:
            marker_file.write(_progressive_rollout_marker_content())
        result.files_uploaded.append(PROGRESSIVE_ROLLOUT_MARKER_FILE)
        _log_progress("Wrote active marker: gs://%s", marker_remote)

    # --- Dual-load dependencies.json to the connector_dependencies/ path ---
    if not has_deps:
        logger.debug(
            "No %s in artifacts dir — skipping dual-load.",
            CONNECTOR_DEPENDENCY_FILE_NAME,
        )
    else:
        deps_remote = f"{bucket_name}/{deps_gcs_key}"
        _log_progress(
            "Dual-loading %s to gs://%s",
            CONNECTOR_DEPENDENCY_FILE_NAME,
            deps_remote,
        )
        fs.put(str(deps_file), deps_remote)
        result.files_uploaded.append(deps_gcs_key)
        _log_progress("  Uploaded %s (dual-load)", CONNECTOR_DEPENDENCY_FILE_NAME)

    # --- Upload SBOM to the dedicated sbom/ path in GCS ---
    if not has_sbom:
        logger.debug(
            "No %s in artifacts dir — skipping SBOM dual-load.",
            SBOM_FILE_NAME,
        )
    else:
        sbom_gcs_uri = upload_sbom(
            sbom_path=sbom_file,
            connector_name=connector_name,
            version=version,
            store=store,
            dry_run=dry_run,
        )
        result.files_uploaded.append(
            sbom_blob_path(
                connector_name=connector_name,
                version=version,
                store=store,
            ),
        )
        _log_progress("Uploaded SBOM to dedicated path: %s", sbom_gcs_uri)

    return result
