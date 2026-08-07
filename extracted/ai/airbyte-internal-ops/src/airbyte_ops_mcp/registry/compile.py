# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Registry compile operations.

This module provides the core logic for the `registry compile` command,
which scans a registry bucket, determines the "latest" GA version for each
connector, ensures `latest/` directories are up-to-date, and writes
global registry JSON index files plus per-connector version indexes.

High-level algorithm
--------------------
1. **Scan** -- glob for `metadata.yaml` files to discover all
   (connector, version) tuples.  No file *contents* are downloaded.
2. **Marker sets** -- glob for `version-yank.yml` and
   `progressive-rollout.yml` markers.  No file contents are downloaded.
3. **Compute latest** -- for each connector, pick the highest GA semver
   that is not yanked, not a pre-release, and not mid-progressive-rollout.
4. **Compute rollout candidates** -- for each connector, pick the highest
   non-yanked progressive rollout candidate version that is not already promoted
   to `latest/`.
5. **Fast-check latest/** -- glob for `version=*` marker files inside
   `latest/` directories.  Compare with the computed latest.  Only
   connectors whose marker disagrees (or is missing) need a resync.
6. **Resync stale latest/** -- delete the old `latest/` directory,
   ensure a `version=<x.y.z>` marker exists in the versioned
   directory, then recursively copy the versioned directory to
   `latest/`.
7. **Write index files**:
   a. Global `registries/v0/cloud_registry.json` and
      `registries/v0/oss_registry.json` (backwards-compatible).
   b. Per-connector `versions.json` (new).
   c. Combined `registries/v0/composite_registry.json` — a superset
      of the cloud and oss registries with an added top-level
      `availability` field on each entry (one of `["cloud"]`,
      `["oss"]`, or `["cloud", "oss"]`).  When a definitionId
      appears in both registries, the cloud entry is preferred
      (cloud-specific overrides already applied).

When `with_secrets_mask=True`, the compile step also regenerates
`registries/v0/specs_secrets_mask.yaml` by scanning all connector specs
for properties marked `airbyte_secret: true`.
"""

from __future__ import annotations

import contextlib
import copy
import json
import logging
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any

import dpath.util
import gcsfs
import yaml
from packaging.version import InvalidVersion, Version

from airbyte_ops_mcp.registry._constants import (
    METADATA_FOLDER,
    VALID_REGISTRIES,
)
from airbyte_ops_mcp.registry._gcs_helpers import (
    get_gcs_credentials_token,
    get_gcs_storage_client,
)
from airbyte_ops_mcp.registry.generate import (
    _get_registry_override,
    is_registry_enabled,
)
from airbyte_ops_mcp.registry.markers import (
    PROGRESSIVE_ROLLOUT_MARKER_FILE,
    YANK_MARKER_FILE,
)
from airbyte_ops_mcp.registry.metrics import (
    apply_metrics_to_registry_entries,
    read_latest_connector_metrics,
)
from airbyte_ops_mcp.registry.store import RegistryStore, StoreType

logger = logging.getLogger(__name__)

# Regex for the `version=<semver>` marker filename inside `latest/`
_VERSION_MARKER_RE = re.compile(r"^version=(.+)$")

# Registry index output path (relative to bucket root)
_REGISTRIES_PREFIX = "registries/v0"

# Cache-Control header for CDN-served registry index files.
# The bucket default is `public, max-age=3600` (1 hour), which causes the
# CDN to serve stale registry content for up to an hour after a connector
# publish.  Setting a short max-age ensures updates propagate within minutes
# while still allowing the CDN to absorb traffic spikes.
_REGISTRY_INDEX_CACHE_CONTROL = "public, max-age=300"

# Specs secrets mask filename
_SPECS_SECRETS_MASK_FILENAME = "specs_secrets_mask.yaml"


# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------


@dataclass
class CompileResult:
    """Result of a registry compile operation."""

    target: str
    connectors_scanned: int = 0
    versions_found: int = 0
    yanked_versions: int = 0
    latest_updated: int = 0
    latest_already_current: int = 0
    cloud_registry_entries: int = 0
    oss_registry_entries: int = 0
    composite_registry_entries: int = 0
    metrics_connector_count: int = 0
    metrics_registry_entries: int = 0
    metrics_source: str | None = None
    metrics_error: str | None = None
    version_indexes_written: int = 0
    specs_secrets_mask_properties: int = 0
    errors: list[str] = field(default_factory=list)
    dry_run: bool = False

    @property
    def status(self) -> str:
        if self.dry_run:
            return "dry-run"
        if self.errors:
            return "completed-with-errors"
        return "success"

    def summary(self) -> str:
        return (
            f"[{self.status}] Scanned {self.connectors_scanned} connectors, "
            f"{self.versions_found} versions ({self.yanked_versions} yanked). "
            f"Latest updated: {self.latest_updated}, "
            f"already current: {self.latest_already_current}. "
            f"Registry entries: cloud={self.cloud_registry_entries}, "
            f"oss={self.oss_registry_entries}, "
            f"composite={self.composite_registry_entries}. "
            f"Metrics loaded for {self.metrics_connector_count} connectors, "
            f"injected into {self.metrics_registry_entries} registry entries. "
            f"Version indexes: {self.version_indexes_written}. "
            f"Specs secrets mask: {self.specs_secrets_mask_properties} properties. "
            f"Errors: {len(self.errors)}."
        )


@dataclass
class PurgeLatestResult:
    """Result of a purge-latest operation."""

    target: str
    connectors_found: int = 0
    latest_dirs_deleted: int = 0
    errors: list[str] = field(default_factory=list)
    dry_run: bool = False

    @property
    def status(self) -> str:
        if self.dry_run:
            return "dry-run"
        if self.errors:
            return "completed-with-errors"
        return "success"

    def summary(self) -> str:
        return (
            f"[{self.status}] Found {self.connectors_found} connectors, "
            f"deleted {self.latest_dirs_deleted} latest/ directories. "
            f"Errors: {len(self.errors)}."
        )


@dataclass
class ConnectorVersionInfo:
    """Lightweight info about a single published version."""

    version: str
    yanked: bool = False
    is_latest: bool = False
    release_stage: str | None = None
    support_level: str | None = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _log_progress(msg: str, *args: object) -> None:
    """Log a progress message to both the logger and stderr."""
    logger.info(msg, *args)
    formatted = msg % args if args else msg
    print(formatted, file=sys.stderr, flush=True)


def _is_ga_version(version_str: str) -> bool:
    """Return True if the version string is a GA (non-prerelease) semver."""
    try:
        v = Version(version_str)
    except InvalidVersion:
        return False
    return not v.is_prerelease and not v.is_devrelease


def _parse_version(version_str: str) -> Version | None:
    """Parse a version string, returning None if it is not valid semver."""
    try:
        return Version(version_str)
    except InvalidVersion:
        return None


def _is_release_candidate_version(version_str: str) -> bool:
    """Return `True` if the version string is an RC semver."""
    parsed = _parse_version(version_str)
    return parsed is not None and parsed.pre is not None and parsed.pre[0] == "rc"


def _write_gcs_blob_with_custom_ttl(
    bucket_name: str,
    blob_path: str,
    content: str,
    *,
    content_type: str = "application/json",
    cache_control: str | None = None,
) -> None:
    """Write a blob to GCS with an optional custom `Cache-Control` header.

    Uses `google.cloud.storage` directly (rather than `gcsfs`) so that
    blob metadata such as `Cache-Control` can be set at write time.
    Without an explicit header the CDN inherits the bucket / GCS default
    (typically `public, max-age=3600`), which can cause stale content to
    be served for up to an hour.
    """
    client = get_gcs_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    if cache_control is not None:
        blob.cache_control = cache_control
    blob.upload_from_string(content, content_type=content_type)

    # Reload to confirm the write and log verification metadata.
    try:
        blob.reload()
        logger.info(
            "Wrote %s: updated=%s, md5=%s, size=%s, cache_control=%s",
            blob_path,
            blob.updated,
            blob.md5_hash,
            blob.size,
            blob.cache_control,
        )
    except Exception:
        logger.warning(
            "Wrote %s but could not reload blob metadata for verification",
            blob_path,
        )


def _extract_connector_version(
    path: str,
    *,
    store: RegistryStore,
) -> tuple[str, str] | None:
    """Extract (connector_name, version) from a GCS path.

    Expected path format:
        `<bucket>/[<prefix>/]metadata/airbyte/<connector>/<version>/metadata.yaml`

    Args:
        path: Full GCS path returned by glob.
        store: Registry store (bucket + optional prefix).

    Returns None if the path does not match.
    """
    expected_prefix = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/"
    if not path.startswith(expected_prefix):
        return None
    remainder = path[len(expected_prefix) :]
    parts = remainder.split("/")
    if len(parts) < 2:
        return None
    connector = parts[0]
    version = parts[1]
    # Skip non-version dirs like "latest", "release_candidate"
    if version in ("latest", "release_candidate"):
        return None
    return connector, version


# ---------------------------------------------------------------------------
# Step 4: Compute active release candidates
# ---------------------------------------------------------------------------


def _compute_highest_ga_versions(
    *,
    connector_versions: dict[str, list[str]],
    yanked: set[tuple[str, str]],
    progressive_rollouts: set[tuple[str, str]],
) -> dict[str, tuple[Version, str]]:
    """Return each connector's highest non-yanked GA version."""
    highest: dict[str, tuple[Version, str]] = {}
    for connector, versions in connector_versions.items():
        candidates: list[tuple[Version, str]] = []
        for version_str in versions:
            if (connector, version_str) in yanked:
                continue
            if (connector, version_str) in progressive_rollouts:
                continue
            if not _is_ga_version(version_str):
                continue
            parsed = _parse_version(version_str)
            if parsed is not None:
                candidates.append((parsed, version_str))
        if candidates:
            highest[connector] = max(candidates)
    return highest


def _compute_release_candidates(
    *,
    connector_versions: dict[str, list[str]],
    yanked: set[tuple[str, str]],
    progressive_rollouts: set[tuple[str, str]],
) -> dict[str, list[str]]:
    """Derive the active release candidate from versioned marker files.

    For each connector, considers all progressive rollout candidate versions
    that are newer than the latest GA version and not yanked, then advertises
    only the highest (newest) one — the single version a rollout should be
    advancing toward.

    Advertising superseded candidates alongside the active one deadlocks
    rollouts. Even after deletion/cancellation, the platform auto-recreates new
    rollout records for every advertised candidate - resulting in an infinite
    loop of deletion/recreation if older candidates continue to be presented.

    Additionally, older candidates are already registered platform-side, so
    only the newest needs to be discoverable within the compiled index.

    Returns:
        dict mapping connector_name -> single-element list holding the highest
        rollout candidate version string.
    """
    highest_ga = _compute_highest_ga_versions(
        connector_versions=connector_versions,
        yanked=yanked,
        progressive_rollouts=progressive_rollouts,
    )
    rc_versions: dict[str, list[str]] = {}
    for connector, versions in connector_versions.items():
        latest_ga = highest_ga.get(connector)
        if latest_ga is None:
            continue
        latest_ga_version, latest_ga_str = latest_ga
        ga_candidates: list[tuple[Version, str]] = []
        rc_candidates: list[tuple[Version, str]] = []
        for version_str in versions:
            if (connector, version_str) in yanked:
                continue
            if (connector, version_str) not in progressive_rollouts:
                continue
            parsed = _parse_version(version_str)
            if parsed is None:
                continue
            is_ga_version = _is_ga_version(version_str)
            is_release_candidate_version = _is_release_candidate_version(version_str)
            if not is_ga_version and not is_release_candidate_version:
                continue
            if parsed <= latest_ga_version:
                continue
            if is_ga_version:
                ga_candidates.append((parsed, version_str))
            else:
                rc_candidates.append((parsed, version_str))
        candidates = ga_candidates or rc_candidates
        if candidates:
            # Only the newest candidate is advertised; older ones are superseded.
            sorted_candidates = sorted(candidates, reverse=True)
            active_candidate = sorted_candidates[0][1]
            rc_versions[connector] = [active_candidate]
            logger.info(
                "Computed active rollout candidate for %s: %s "
                "(superseded: %s, latest GA: %s)",
                connector,
                active_candidate,
                [v_str for _, v_str in sorted_candidates[1:]],
                latest_ga_str,
            )
    return rc_versions


def _read_rc_registry_entry(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector: str,
    rc_version: str,
    registry_type: str,
) -> dict[str, Any] | None:
    """Read a release candidate's cloud.json or oss.json from its versioned dir.

    Returns the parsed JSON dict, or None if the file does not exist.
    """
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte"
    entry_path = f"{base}/{connector}/{rc_version}/{registry_type}.json"
    try:
        if not fs.exists(entry_path):
            return None
        with fs.open(entry_path, "r") as f:
            return json.load(f)  # type: ignore[no-any-return]
    except Exception as exc:
        logger.warning(
            "Failed to read RC %s.json for %s@%s: %s",
            registry_type,
            connector,
            rc_version,
            exc,
        )
        return None


def _apply_release_candidates_to_entries(
    entries: list[dict[str, Any]],
    rc_entries: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Inject `releases.releaseCandidates` into global registry entries.

    For each entry whose `dockerRepository` has active rollout candidates,
    adds:

        {
            "releases": {
                "releaseCandidates": {
                    "<rollout_version>": { ...full candidate registry entry... }
                }
            }
        }

    The platform creates a rollout record for every entry it finds here, so
    `_compute_release_candidates` advertises only the active (highest)
    candidate — see its docstring for why superseded candidates are excluded.

    Args:
        entries: List of registry entry dicts (from `_compile_global_registry`).
        rc_entries: Mapping of `dockerRepository` -> list of
            `{"version": str, "entry": dict}` dicts, ordered highest-first.

    Returns:
        New list with rollout candidate info injected.
    """
    result: list[dict[str, Any]] = []
    for entry in entries:
        docker_repo = entry.get("dockerRepository", "")
        if docker_repo in rc_entries:
            rc_infos = rc_entries[docker_repo]
            updated = copy.deepcopy(entry)
            updated.setdefault("releases", {})
            updated["releases"]["releaseCandidates"] = {
                rc_info["version"]: rc_info["entry"] for rc_info in rc_infos
            }
            result.append(updated)
        else:
            result.append(entry)
    return result


# ---------------------------------------------------------------------------
# Steps 1 and 2: Scan versions and yank markers via glob
# ---------------------------------------------------------------------------


def _scan_versions_and_markers(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector_name: list[str] | None = None,
) -> tuple[
    dict[str, list[str]],
    set[tuple[str, str]],
    set[tuple[str, str]],
]:
    """Scan the registry for versions, yank markers, and rollout markers.

    Uses efficient glob patterns -- no file contents are downloaded.

    Args:
        fs: Authenticated GCSFileSystem.
        store: Registry store (bucket + optional prefix).
        connector_name: If provided, only scan these connector names.

    Returns:
        Tuple of:
        - dict mapping connector_name -> list of version strings
        - set of (connector_name, version) tuples that are yanked
        - set of (connector_name, version) tuples with active progressive rollout
    """
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte"

    # Step 1: glob for metadata.yaml to discover all versions
    if connector_name:
        metadata_paths: list[str] = []
        for name in connector_name:
            pattern = f"{base}/{name}/*/metadata.yaml"
            metadata_paths.extend(fs.glob(pattern))
    else:
        pattern = f"{base}/*/*/metadata.yaml"
        metadata_paths = fs.glob(pattern)

    _log_progress("Glob found %d metadata.yaml files", len(metadata_paths))

    connector_versions: dict[str, list[str]] = {}
    for path in metadata_paths:
        parsed = _extract_connector_version(path, store=store)
        if parsed is None:
            continue
        connector, version = parsed
        connector_versions.setdefault(connector, []).append(version)

    # Step 2: glob for version-yank.yml markers
    if connector_name:
        yank_paths: list[str] = []
        for name in connector_name:
            yank_pattern = f"{base}/{name}/*/{YANK_MARKER_FILE}"
            yank_paths.extend(fs.glob(yank_pattern))
    else:
        yank_pattern = f"{base}/*/*/{YANK_MARKER_FILE}"
        yank_paths = fs.glob(yank_pattern)

    _log_progress("Glob found %d %s markers", len(yank_paths), YANK_MARKER_FILE)

    yanked: set[tuple[str, str]] = set()
    for path in yank_paths:
        parsed = _extract_connector_version(path, store=store)
        if parsed is not None:
            connector, version = parsed
            yanked.add((connector, version))
        else:
            logger.warning("Could not parse yank path: %s", path)

    if connector_name:
        rollout_paths: list[str] = []
        for name in connector_name:
            rollout_pattern = f"{base}/{name}/*/{PROGRESSIVE_ROLLOUT_MARKER_FILE}"
            rollout_paths.extend(fs.glob(rollout_pattern))
    else:
        rollout_pattern = f"{base}/*/*/{PROGRESSIVE_ROLLOUT_MARKER_FILE}"
        rollout_paths = fs.glob(rollout_pattern)

    _log_progress(
        "Glob found %d %s markers",
        len(rollout_paths),
        PROGRESSIVE_ROLLOUT_MARKER_FILE,
    )

    progressive_rollouts: set[tuple[str, str]] = set()
    for path in rollout_paths:
        parsed = _extract_connector_version(path, store=store)
        if parsed is not None and parsed not in yanked:
            progressive_rollouts.add(parsed)
        elif parsed is None:
            logger.warning("Could not parse progressive rollout path: %s", path)

    return connector_versions, yanked, progressive_rollouts


# ---------------------------------------------------------------------------
# Step 3: Compute latest GA version per connector
# ---------------------------------------------------------------------------


def _compute_latest_versions(
    *,
    connector_versions: dict[str, list[str]],
    yanked: set[tuple[str, str]],
    progressive_rollouts: set[tuple[str, str]],
) -> dict[str, str]:
    """For each connector, determine the highest GA semver that is not yanked.

    Versions with an active `progressive-rollout.yml` marker are skipped so
    that an in-progress progressive rollout does not become the default/latest
    version.

    Returns:
        dict mapping connector_name -> latest version string.
        Connectors with no eligible GA versions are omitted.
    """
    latest: dict[str, str] = {}
    for connector, versions in connector_versions.items():
        candidates: list[tuple[Version, str]] = []
        for v_str in versions:
            if (connector, v_str) in yanked:
                continue
            if (connector, v_str) in progressive_rollouts:
                continue
            if not _is_ga_version(v_str):
                continue
            parsed = _parse_version(v_str)
            if parsed is not None:
                candidates.append((parsed, v_str))
        if not candidates:
            logger.warning(
                "No eligible GA version found for %s (%d total versions, all yanked or pre-release).",
                connector,
                len(versions),
            )
            continue

        _, chosen = max(candidates)
        latest[connector] = chosen
    return latest


# ---------------------------------------------------------------------------
# Step 5: Check version markers in latest/ directories
# ---------------------------------------------------------------------------


def _scan_latest_markers(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector_name: list[str] | None = None,
) -> dict[str, str]:
    """Glob for `version=*` marker files in `latest/` directories.

    Returns:
        dict mapping connector_name -> current marker version string.
    """
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte"

    if connector_name:
        marker_paths: list[str] = []
        for name in connector_name:
            marker_pattern = f"{base}/{name}/latest/version=*"
            marker_paths.extend(fs.glob(marker_pattern))
    else:
        marker_pattern = f"{base}/*/latest/version=*"
        marker_paths = fs.glob(marker_pattern)

    _log_progress("Glob found %d version marker files in latest/", len(marker_paths))

    markers: dict[str, str] = {}
    for path in marker_paths:
        filename = path.split("/")[-1]
        match = _VERSION_MARKER_RE.match(filename)
        if not match:
            continue
        version_str = match.group(1)
        # Extract connector name from path
        parts = path.split("/")
        try:
            meta_idx = parts.index("metadata")
            connector = parts[meta_idx + 2]
            markers[connector] = version_str
        except (ValueError, IndexError):
            logger.warning("Could not parse marker path: %s", path)

    return markers


def _requires_pinned_override_synthesis(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector: str,
    version: str,
) -> bool:
    """Return whether `latest/` is missing registry entries that a pin can supply."""
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/{connector}"
    latest_dir = f"{base}/latest"
    if all(
        fs.exists(f"{latest_dir}/{registry_type}.json")
        for registry_type in VALID_REGISTRIES
    ):
        return False

    metadata_path = f"{latest_dir}/metadata.yaml"
    try:
        with fs.open(metadata_path, "r") as f:
            raw_metadata = yaml.safe_load(f)
    except FileNotFoundError:
        return False
    except Exception as exc:
        logger.warning("Failed to read metadata for %s: %s", connector, exc)
        return False

    if not isinstance(raw_metadata, dict):
        logger.warning("Metadata for %s is not a mapping", connector)
        return False

    metadata_data = raw_metadata.get("data", {})
    if not isinstance(metadata_data, dict):
        return False

    for registry_type in VALID_REGISTRIES:
        if fs.exists(f"{latest_dir}/{registry_type}.json"):
            continue

        override = _get_registry_override(metadata_data, registry_type)
        if override.get("enabled", True) is False:
            continue

        pinned_tag = override.get("dockerImageTag")
        if not pinned_tag or pinned_tag == version:
            continue

        pinned_entry_path = f"{base}/{pinned_tag}/{registry_type}.json"
        if fs.exists(pinned_entry_path):
            return True

        logger.warning(
            "Pinned version %s/%s.json not found for %s",
            pinned_tag,
            registry_type,
            connector,
        )

    return False


# ---------------------------------------------------------------------------
# Step 6: Resync stale latest/ directories
# ---------------------------------------------------------------------------


def _delete_latest_dir(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector: str,
) -> None:
    """Delete a connector's `latest/` directory recursively.

    This is the shared primitive used by both compile (step 6, before
    copying the new version) and delete-dev-latest (standalone purge).

    Silently succeeds if the directory does not exist.
    """
    latest_path = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/{connector}/latest"
    with contextlib.suppress(FileNotFoundError):
        fs.rm(latest_path, recursive=True)


def _ensure_version_marker(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector: str,
    version: str,
) -> None:
    """Ensure a `version=<semver>` marker file exists in the versioned dir.

    If the marker already exists this is a no-op.  Otherwise a zero-byte
    file is created so that it will be included in the recursive copy to
    `latest/`.
    """
    marker_path = (
        f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/{connector}"
        f"/{version}/version={version}"
    )
    if not fs.exists(marker_path):
        with fs.open(marker_path, "w") as f:
            f.write("")
        _log_progress("  Created missing marker in versioned dir: version=%s", version)


def _sync_latest_dir(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector: str,
    version: str,
    dry_run: bool = False,
) -> None:
    """Replace `latest/` with a recursive copy of the versioned directory.

    Algorithm:
    1. Ensure a `version=<semver>` marker exists in the versioned dir
       (backfill; once the publish pipeline writes it, this becomes a no-op).
    2. Delete `latest/` recursively via `_delete_latest_dir()`.
    3. Recursively copy the entire versioned directory to `latest/`.
    """
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/{connector}"
    source_dir = f"{base}/{version}"
    dest_dir = f"{base}/latest"

    if dry_run:
        _log_progress(
            "  [DRY RUN] Would sync %s/ → %s/",
            source_dir,
            dest_dir,
        )
        return

    _log_progress("  Syncing %s/ → %s/", source_dir, dest_dir)

    # 1. Ensure marker exists in the versioned directory.
    _ensure_version_marker(
        fs,
        store=store,
        connector=connector,
        version=version,
    )

    # 2. Delete existing latest/ directory.
    _delete_latest_dir(
        fs,
        store=store,
        connector=connector,
    )

    # 3. Recursive copy from versioned dir → latest/.
    fs.copy(source_dir, dest_dir, recursive=True)

    _log_progress("  Synced %s/ → %s/", source_dir, dest_dir)


def _apply_overrides_to_latest_entry(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector: str,
    version: str,
) -> None:
    """Post-process `latest/` registry entries after syncing from a versioned dir.

    When the compile step copies files from `{version}/` to `latest/`, the
    embedded `cloud.json` and `oss.json` still contain version-specific
    values.  This function:

    1. Applies `registryOverrides` from the metadata so that the `latest/`
       entry reflects the overridden values (e.g. a pinned `dockerImageTag`).
    2. When an override pins `dockerImageTag` to a different version, copies
       version-sensitive fields (`spec`, `packageInfo`) from the pinned
       version's entry so that `latest/` is fully consistent.
    3. Updates `generated.source_file_info.metadata_file_path` to reference
       the `latest/` path instead of the versioned path.
    """
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/{connector}"
    latest_dir = f"{base}/latest"

    # Read metadata.yaml from latest/ to get registry overrides.
    metadata_path = f"{latest_dir}/metadata.yaml"
    try:
        with fs.open(metadata_path, "r") as f:
            raw_metadata = yaml.safe_load(f)
    except FileNotFoundError:
        logger.warning(
            "No metadata.yaml in latest/ for %s, skipping override application",
            connector,
        )
        return
    except Exception as exc:
        logger.warning("Failed to read metadata for %s: %s", connector, exc)
        return

    metadata_data: dict[str, Any] = raw_metadata.get("data", {})
    latest_metadata_file_path = (
        f"{METADATA_FOLDER}/airbyte/{connector}/latest/metadata.yaml"
    )

    for registry_type in VALID_REGISTRIES:
        entry_path = f"{latest_dir}/{registry_type}.json"
        override = copy.deepcopy(_get_registry_override(metadata_data, registry_type))
        registry_enabled = override.get("enabled", True) is not False
        overrides = {
            k: v for k, v in override.items() if k != "enabled" and v is not None
        }
        pinned_tag = overrides.get("dockerImageTag")

        try:
            if fs.exists(entry_path):
                with fs.open(entry_path, "r") as f:
                    entry = json.load(f)
                modified = False
            elif registry_enabled and pinned_tag and pinned_tag != version:
                pinned_entry_path = f"{base}/{pinned_tag}/{registry_type}.json"
                if not fs.exists(pinned_entry_path):
                    logger.warning(
                        "Pinned version %s/%s.json not found for %s",
                        pinned_tag,
                        registry_type,
                        connector,
                    )
                    continue
                with fs.open(pinned_entry_path, "r") as fp:
                    entry = json.load(fp)
                modified = True
            else:
                continue
        except Exception as exc:
            logger.warning(
                "Failed to read %s.json for %s: %s", registry_type, connector, exc
            )
            continue

        # --- Apply registry overrides (skip_docker_image_tag=False for latest) ---
        if overrides:
            entry.update(overrides)
            modified = True

        # --- When dockerImageTag is overridden to a different version, copy
        #     version-sensitive fields from the pinned version's entry. ---
        if pinned_tag and pinned_tag != version:
            pinned_entry_path = f"{base}/{pinned_tag}/{registry_type}.json"
            try:
                if fs.exists(pinned_entry_path):
                    with fs.open(pinned_entry_path, "r") as fp:
                        pinned_entry = json.load(fp)
                    for field_name in ("spec", "packageInfo"):
                        if field_name in pinned_entry:
                            entry[field_name] = pinned_entry[field_name]
                            modified = True
                else:
                    logger.warning(
                        "Pinned version %s/%s.json not found for %s",
                        pinned_tag,
                        registry_type,
                        connector,
                    )
            except Exception as exc:
                logger.warning(
                    "Failed to read pinned entry %s/%s.json for %s: %s",
                    pinned_tag,
                    registry_type,
                    connector,
                    exc,
                )

        # --- Update metadata_file_path to point to latest/ ---
        generated = entry.get("generated")
        if isinstance(generated, dict):
            source_file_info = generated.get("source_file_info")
            if isinstance(source_file_info, dict):
                current_path = source_file_info.get("metadata_file_path")
                if current_path != latest_metadata_file_path:
                    source_file_info["metadata_file_path"] = latest_metadata_file_path
                    modified = True

        if modified:
            content = json.dumps(entry, indent=2, sort_keys=True) + "\n"
            with fs.open(entry_path, "w") as fout:
                fout.write(content)


# ---------------------------------------------------------------------------
# Step 9: Compile global registry JSONs
# ---------------------------------------------------------------------------


# Legacy strict-encrypt (and -secure) connectors that share a definition ID
# with their base connector.  No new variants are being created, so this is a
# closed set.  The *value* is the docker image name that should be **dropped**
# when the collision is encountered; the base connector always wins.
#
# This deduplication logic can be removed once strict-encrypt connectors are
# fully sunsetted.
_KNOWN_STRICT_ENCRYPT_COLLISIONS: dict[str, str] = {
    # destination-elasticsearch / destination-elasticsearch-strict-encrypt
    "68f351a7-2745-4bef-ad7f-996b8e51bb8c": "airbyte/destination-elasticsearch-strict-encrypt",
    # destination-mongodb / destination-mongodb-strict-encrypt
    "8b746512-8c2e-6ac1-4adc-b59faafd473c": "airbyte/destination-mongodb-strict-encrypt",
    # destination-mysql / destination-mysql-strict-encrypt
    "ca81ee7c-3163-4246-af40-094cc31e5e42": "airbyte/destination-mysql-strict-encrypt",
    # destination-oracle / destination-oracle-strict-encrypt
    "3986776d-2319-4de9-8af8-db14c0996e72": "airbyte/destination-oracle-strict-encrypt",
    # source-clickhouse / source-clickhouse-strict-encrypt
    "bad83517-5e54-4a3d-9b53-63e85fbd4d7c": "airbyte/source-clickhouse-strict-encrypt",
    # source-file / source-file-secure (same pattern, -secure suffix)
    "778daa7c-feaf-4db6-96f3-70fd645acc77": "airbyte/source-file-secure",
    # source-oracle / source-oracle-strict-encrypt
    "b39a7370-74c3-45a6-ac3a-380d48520a83": "airbyte/source-oracle-strict-encrypt",
}


def _resolve_definition_id_collision(
    image_name_a: str,
    image_name_b: str,
    definition_id: str,
) -> str:
    """Decide which docker image name wins when two share a definition ID.

    Only the hard-coded set of legacy strict-encrypt collisions in
    `_KNOWN_STRICT_ENCRYPT_COLLISIONS` is handled.  The base connector
    always wins (the strict-encrypt variant is dropped).  Any other
    collision is unrecognised and raises `ValueError` so the compile step
    fails loudly rather than silently picking the wrong entry.

    Note: This deduplication logic can be removed once strict-encrypt
    connectors are fully sunsetted.

    Args:
        image_name_a: Docker image name of the first entry.
        image_name_b: Docker image name of the second entry.
        definition_id: The shared definition ID (for error messages).

    Returns:
        The docker image name that should be kept.

    Raises:
        ValueError: If the collision is not in the known allowlist.
    """
    drop_repo = _KNOWN_STRICT_ENCRYPT_COLLISIONS.get(definition_id)
    if drop_repo is None:
        raise ValueError(
            f"Unhandled definition-ID collision for {definition_id}: "
            f"{image_name_a} vs {image_name_b}. "
            f"This collision is not in the known strict-encrypt allowlist."
        )

    if image_name_a == drop_repo:
        return image_name_b
    if image_name_b == drop_repo:
        return image_name_a

    # Neither side matches the expected drop target.
    raise ValueError(
        f"Definition-ID collision for {definition_id} is in the known "
        f"allowlist (expected to drop {drop_repo}), but neither entry "
        f"matches: {image_name_a} vs {image_name_b}."
    )


def _compile_global_registry(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    latest_versions: dict[str, str],
    registry_type: str,
) -> list[dict[str, Any]]:
    """Read cloud.json or oss.json from each connector's latest/ dir.

    Reads are parallelised with up to `_COMPILE_READ_MAX_WORKERS` threads
    to avoid the ~150 s serial penalty on a full registry (~1 250 files).

    When multiple connectors share the same `definitionId`, the collision
    is resolved by `_resolve_definition_id_collision()`.  Only the
    hard-coded set of legacy strict-encrypt collisions is handled (the
    base connector wins); any other collision raises `ValueError` so
    the compile step fails loudly.

    Args:
        registry_type: "cloud" or "oss".

    Returns:
        List of registry entry dicts (deterministic order, sorted by connector name).
    """
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte"
    sorted_connectors = sorted(latest_versions)

    def _read_one(connector: str) -> dict[str, Any] | None:
        json_path = f"{base}/{connector}/latest/{registry_type}.json"
        try:
            if not fs.exists(json_path):
                return None
            with fs.open(json_path, "r") as f:
                return json.load(f)  # type: ignore[no-any-return]
        except Exception as exc:
            logger.warning(
                "Failed to read %s for %s: %s", registry_type, connector, exc
            )
            return None

    entries: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=_COMPILE_READ_MAX_WORKERS) as pool:
        results = list(pool.map(_read_one, sorted_connectors))
    for result in results:
        if result is not None:
            entries.append(result)

    # --- Deduplicate by definition ID ---
    seen: dict[str, tuple[str, int]] = {}  # definitionId -> (dockerRepository, index)
    deduplicated: list[dict[str, Any]] = []
    for entry in entries:
        def_id = entry.get("sourceDefinitionId") or entry.get("destinationDefinitionId")
        if not def_id:
            deduplicated.append(entry)
            continue
        docker_repo = entry.get("dockerRepository", "")
        if def_id not in seen:
            seen[def_id] = (docker_repo, len(deduplicated))
            deduplicated.append(entry)
            continue

        existing_image, existing_idx = seen[def_id]
        winner = _resolve_definition_id_collision(existing_image, docker_repo, def_id)
        if winner == docker_repo:
            # New entry wins — replace the previously kept entry.
            logger.warning(
                "Duplicate definitionId %s: replacing %s with %s "
                "(strict-encrypt variant dropped)",
                def_id,
                existing_image,
                docker_repo,
            )
            deduplicated[existing_idx] = entry
            seen[def_id] = (docker_repo, existing_idx)
        else:
            logger.warning(
                "Duplicate definitionId %s: keeping %s, dropping %s "
                "(strict-encrypt variant dropped)",
                def_id,
                existing_image,
                docker_repo,
            )

    if len(deduplicated) < len(entries):
        _log_progress(
            "  Deduplicated %s index: %d → %d entries (%d duplicates removed)",
            registry_type,
            len(entries),
            len(deduplicated),
            len(entries) - len(deduplicated),
        )

    return deduplicated


def _build_global_registry_json(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Assemble the global registry JSON from a list of connector entries.

    Splits entries into sources and destinations based on the presence of
    `sourceDefinitionId` or `destinationDefinitionId`.
    """
    sources = []
    destinations = []
    for entry in entries:
        if "sourceDefinitionId" in entry:
            sources.append(entry)
        elif "destinationDefinitionId" in entry:
            destinations.append(entry)
        else:
            # Fallback: guess from dockerRepository
            docker_repo = entry.get("dockerRepository", "")
            if "destination" in docker_repo:
                destinations.append(entry)
            else:
                sources.append(entry)

    return {"sources": sources, "destinations": destinations}


def _entry_definition_id(entry: dict[str, Any]) -> str | None:
    """Return the definitionId for a registry entry, source or destination."""
    return entry.get("sourceDefinitionId") or entry.get("destinationDefinitionId")


def _entry_composite_key(entry: dict[str, Any]) -> str:
    """Return the key used to dedupe entries in the composite registry.

    Prefers `definitionId` (source or destination); falls back to
    `dockerRepository` so that entries missing a definitionId — which
    `_compile_global_registry` explicitly preserves — are still carried
    through the composite registry without being silently dropped.
    """
    def_id = _entry_definition_id(entry)
    if def_id:
        return f"def:{def_id}"
    docker_repo = entry.get("dockerRepository", "")
    if docker_repo:
        return f"repo:{docker_repo}"
    # Last-resort: id() of the dict — guarantees uniqueness so the entry
    # is still emitted once, even if it has neither a definitionId nor a
    # dockerRepository.
    return f"obj:{id(entry)}"


def _build_composite_registry_json(
    *,
    cloud_entries: list[dict[str, Any]],
    oss_entries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a composite registry JSON that is a superset of cloud + oss.

    For each unique connector — keyed by `definitionId` when present,
    falling back to `dockerRepository` — a single merged entry is
    emitted.  The cloud entry (if any) is preferred as the source of
    truth for per-connector fields because cloud-specific overrides have
    already been applied.  The oss entry is used only when the connector
    is OSS-only.

    Entries missing both a `definitionId` and a `dockerRepository` are
    still carried through (unkeyed) so the composite output is truly a
    superset of both inputs — this matches `_compile_global_registry`,
    which also preserves such entries.

    Each emitted entry has an added top-level `availability` field
    listing which registries it appears in.  Valid values are:

    * `["oss"]`        — only in `oss_registry.json`
    * `["cloud"]`      — only in `cloud_registry.json`
    * `["cloud", "oss"]` — in both (order is always alphabetical)

    Args:
        cloud_entries: Entries from the cloud registry (already deduped).
        oss_entries: Entries from the oss registry (already deduped).

    Returns:
        A dict with `sources` and `destinations` keys, each a list of
        merged registry entries.
    """
    cloud_by_key: dict[str, dict[str, Any]] = {}
    for entry in cloud_entries:
        cloud_by_key[_entry_composite_key(entry)] = entry

    oss_by_key: dict[str, dict[str, Any]] = {}
    for entry in oss_entries:
        oss_by_key[_entry_composite_key(entry)] = entry

    all_keys: set[str] = set(cloud_by_key) | set(oss_by_key)

    merged: list[dict[str, Any]] = []
    for key in all_keys:
        in_cloud = key in cloud_by_key
        in_oss = key in oss_by_key
        # Prefer the cloud entry (has cloud-specific overrides applied).
        source_entry = cloud_by_key[key] if in_cloud else oss_by_key[key]
        entry = copy.deepcopy(source_entry)
        availability: list[str] = []
        if in_cloud:
            availability.append("cloud")
        if in_oss:
            availability.append("oss")
        entry["availability"] = availability
        merged.append(entry)

    # Sort for deterministic output: by dockerRepository then definitionId.
    merged.sort(
        key=lambda e: (
            e.get("dockerRepository", ""),
            _entry_definition_id(e) or "",
        )
    )

    return _build_global_registry_json(merged)


# ---------------------------------------------------------------------------
# Step 12: Specs secrets mask
# ---------------------------------------------------------------------------


def _extract_secret_property_names(
    entries: list[dict[str, Any]],
) -> set[str]:
    """Extract property names marked as `airbyte_secret` from connector specs.

    Walks the `spec.connectionSpecification.properties` tree of each entry
    and collects the leaf property name for every node that has
    `airbyte_secret: true`.

    Args:
        entries: List of registry entry dicts (from cloud or oss registries).

    Returns:
        A set of property names that are marked as secrets.
    """
    secret_names: set[str] = set()
    for entry in entries:
        spec = entry.get("spec", {})
        conn_spec = spec.get("connectionSpecification", {})
        properties = conn_spec.get("properties")
        if not properties:
            continue
        for type_path, _ in dpath.util.search(properties, "**/type", yielded=True):
            absolute_path = f"/{type_path}"
            if "/" in type_path:
                property_path, _ = absolute_path.rsplit(sep="/", maxsplit=1)
            else:
                property_path = absolute_path
            try:
                property_definition = dpath.util.get(properties, property_path)
            except KeyError:
                continue
            if isinstance(property_definition, dict) and property_definition.get(
                "airbyte_secret", False
            ):
                secret_names.add(property_path.split("/")[-1])
    return secret_names


# ---------------------------------------------------------------------------
# Step 11: Per-connector version index
# ---------------------------------------------------------------------------


def _build_version_index(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector: str,
    versions: list[str],
    yanked: set[tuple[str, str]],
    latest_version: str | None,
    rc_version: str | None = None,
    rc_versions_all: list[str] | None = None,
) -> dict[str, Any]:
    """Build the per-connector versions.json content.

    For each version, reads `metadata.yaml` to extract `releaseStage`
    and `supportLevel` (only for the latest version to keep scanning fast).

    If `rc_version` is provided, the matching rollout candidate entry is
    annotated with the legacy `"is_release_candidate": true` field and a
    top-level `"release_candidate"` field is added to the index.

    If `rc_versions_all` is provided (list of all RC versions, highest-first),
    all matching versions are annotated. When more than one RC version is
    present, a `"release_candidates"` list is added to the index.
    """
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/{connector}"
    rc_version_set = set(rc_versions_all) if rc_versions_all else set()

    version_entries: list[dict[str, Any]] = []
    for v_str in sorted(
        versions, key=lambda s: _parse_version(s) or Version("0"), reverse=True
    ):
        is_yanked = (connector, v_str) in yanked
        is_latest = v_str == latest_version
        is_rc = v_str == rc_version or v_str in rc_version_set

        entry: dict[str, Any] = {
            "version": v_str,
            "yanked": is_yanked,
            "is_latest": is_latest,
        }
        if is_rc:
            entry["is_release_candidate"] = True

        # For the latest version, enrich with metadata fields
        if is_latest:
            try:
                meta_path = f"{base}/{v_str}/metadata.yaml"
                with fs.open(meta_path, "r") as f:
                    raw = yaml.safe_load(f)
                data = raw.get("data", {})
                entry["release_stage"] = data.get("releaseStage")
                entry["support_level"] = data.get("supportLevel")
            except Exception as exc:
                logger.warning(
                    "Failed to read metadata for %s@%s: %s", connector, v_str, exc
                )

        version_entries.append(entry)

    definition_id = None
    if latest_version:
        # Try to get the definition ID from the latest version's metadata
        try:
            meta_path = f"{base}/{latest_version}/metadata.yaml"
            with fs.open(meta_path, "r") as f:
                raw = yaml.safe_load(f)
            data = raw.get("data", {})
            definition_id = data.get("definitionId")
        except Exception:
            pass

    result: dict[str, Any] = {
        "connector": connector,
        "versions": version_entries,
    }
    if definition_id:
        result["definition_id"] = definition_id
    if rc_version:
        result["release_candidate"] = rc_version
    if rc_versions_all and len(rc_versions_all) > 1:
        result["release_candidates"] = rc_versions_all

    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


_PURGE_LATEST_MAX_WORKERS = 20
"""DoP for purge-latest bulk deletes."""

_COMPILE_SYNC_MAX_WORKERS = 80
"""DoP for Step 6 — resync stale latest/ directories."""

_COMPILE_READ_MAX_WORKERS = 20
"""DoP for Step 9 — read cloud.json / oss.json from latest/ dirs."""

_COMPILE_WRITE_MAX_WORKERS = 80
"""DoP for Step 11 — write per-connector versions.json indexes."""

# Supported legacy migration versions.
LEGACY_MIGRATION_VERSIONS = ("v1",)


# ---------------------------------------------------------------------------
# Legacy migration: v1 — delete disabled registry entries
# ---------------------------------------------------------------------------


def _cleanup_disabled_registry_entries(
    fs: gcsfs.GCSFileSystem,
    *,
    store: RegistryStore,
    connector_versions: dict[str, list[str]],
    dry_run: bool = False,
) -> dict[str, list[str]]:
    """Delete `{registry_type}.json` files for disabled connectors.

    Reads `latest/metadata.yaml` for each connector to check
    `registryOverrides.{cloud,oss}.enabled`.  When `enabled` is
    `false`, deletes the corresponding `{registry_type}.json` from
    **every** version directory and from `latest/`.

    This is a one-time migration step (`--with-legacy-migration=v1`)
    that cleans up artifacts produced by the legacy pipeline which did
    not respect the `enabled` flag at generation time.

    Returns:
        Mapping of connector name → list of deleted GCS paths.
    """
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte"
    deleted: dict[str, list[str]] = {}

    for connector in sorted(connector_versions):
        metadata_path = f"{base}/{connector}/latest/metadata.yaml"
        try:
            if not fs.exists(metadata_path):
                continue
            with fs.open(metadata_path, "r") as mf:
                raw_meta = yaml.safe_load(mf)
        except Exception as exc:
            logger.warning(
                "legacy-migration: failed to read metadata for %s: %s",
                connector,
                exc,
            )
            continue

        if not isinstance(raw_meta, dict):
            logger.warning(
                "legacy-migration: unexpected metadata structure for %s, skipping",
                connector,
            )
            continue

        metadata_data = raw_meta.get("data", {})
        versions = connector_versions[connector]
        dirs = [*versions, "latest"]

        for registry_type in VALID_REGISTRIES:
            if is_registry_enabled(metadata_data, registry_type):
                continue

            # enabled=false → delete {registry_type}.json from all dirs
            for version_or_latest in dirs:
                json_path = (
                    f"{base}/{connector}/{version_or_latest}/{registry_type}.json"
                )
                try:
                    if not fs.exists(json_path):
                        continue
                except Exception:
                    continue

                if dry_run:
                    _log_progress(
                        "  [DRY RUN] Would delete %s",
                        json_path,
                    )
                else:
                    try:
                        fs.rm(json_path)
                    except Exception as exc:
                        logger.warning(
                            "legacy-migration: failed to delete %s: %s",
                            json_path,
                            exc,
                        )
                        continue

                deleted.setdefault(connector, []).append(json_path)

    return deleted


def purge_latest_dirs(
    *,
    store: RegistryStore,
    connector_name: list[str] | None = None,
    dry_run: bool = False,
) -> PurgeLatestResult:
    """Delete all `latest/` directories from the registry store.

    Discovers connector directories via glob, then deletes each
    `latest/` subdirectory in parallel using a thread pool.

    Args:
        store: Registry store (bucket + optional prefix).
        connector_name: If provided, only purge these connectors.
        dry_run: If True, report what would be done without deleting.

    Returns:
        A `PurgeLatestResult` describing what was done.
    """
    result = PurgeLatestResult(target=store.bucket_root, dry_run=dry_run)

    token = get_gcs_credentials_token()
    fs = gcsfs.GCSFileSystem(token=token)

    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte"

    # Discover latest/ dirs by listing connector directories that contain
    # a `latest/` subdirectory.
    _log_progress("Discovering latest/ directories...")
    base_with_slash = f"{base}/"
    if connector_name:
        # Check each requested connector for a latest/ dir
        seen: set[str] = set()
        connectors_with_latest: list[str] = []
        for name in connector_name:
            if name in seen:
                continue
            latest_path = f"{base}/{name}/latest"
            if fs.exists(latest_path):
                connectors_with_latest.append(name)
                seen.add(name)
    else:
        # Glob for all connectors, then filter to those with latest/
        all_connector_dirs = fs.glob(f"{base}/*/latest")
        seen = set()
        connectors_with_latest = []
        for path in all_connector_dirs:
            # Strip the known base prefix and take the first component
            if not path.startswith(base_with_slash):
                logger.warning("Could not parse latest path: %s", path)
                continue
            relative = path[len(base_with_slash) :]
            connector = relative.split("/")[0]
            if connector and connector not in seen:
                connectors_with_latest.append(connector)
                seen.add(connector)

    result.connectors_found = len(connectors_with_latest)
    _log_progress(
        "Found %d connectors with latest/ directories",
        result.connectors_found,
    )

    if not connectors_with_latest:
        _log_progress("Nothing to purge.")
        _log_progress(result.summary())
        return result

    if dry_run:
        for connector in sorted(connectors_with_latest):
            _log_progress("  [DRY RUN] Would delete %s/latest/", connector)
        result.latest_dirs_deleted = len(connectors_with_latest)
        _log_progress(result.summary())
        return result

    # Delete latest/ dirs in parallel using the shared helper.
    def _delete_one(connector: str) -> str | None:
        """Delete a single connector's latest/ dir. Returns error string or None."""
        try:
            _delete_latest_dir(
                fs,
                store=store,
                connector=connector,
            )
            return None
        except Exception as exc:
            return f"Failed to delete latest/ for {connector}: {exc}"

    _log_progress(
        "Deleting %d latest/ directories (max_workers=%d)...",
        len(connectors_with_latest),
        _PURGE_LATEST_MAX_WORKERS,
    )

    with ThreadPoolExecutor(max_workers=_PURGE_LATEST_MAX_WORKERS) as pool:
        futures = {
            pool.submit(_delete_one, c): c for c in sorted(connectors_with_latest)
        }
        for i, future in enumerate(as_completed(futures), 1):
            connector = futures[future]
            error = future.result()
            if error:
                logger.error(error)
                result.errors.append(error)
            else:
                result.latest_dirs_deleted += 1
            if i % 100 == 0:
                _log_progress("  Deleted %d / %d...", i, len(connectors_with_latest))

    _log_progress(result.summary())
    return result


def compile_registry(
    *,
    store: RegistryStore,
    connector_name: list[str] | None = None,
    dry_run: bool = False,
    with_secrets_mask: bool = False,
    with_legacy_migration: str | None = None,
    with_metrics: bool = True,
    force: bool = False,
) -> CompileResult:
    """Compile the registry: sync latest/ dirs and write index files.

    Steps:
        1. Glob for all `metadata.yaml` to discover (connector, version) pairs.
        2. Glob for active marker files.
        3. Compute the latest GA semver per connector.
        4. Compute active release candidates from versioned markers.
        5. Glob for `version=*` markers in `latest/` dirs for a fast check.
        6. Delete stale `latest/` dirs and recursively copy the versioned dir.
        7. Synthesize missing registry entries from pinned latest overrides.
        8. (Optional) Legacy migration: delete disabled registry entries.
        9. (Optional) Read latest connector metrics.
        10. Write global registry JSONs.
        11. Write composite registry JSON.
        12. Write per-connector `versions.json`.
        13. (Optional) Regenerate `specs_secrets_mask.yaml`.

    Args:
        store: Registry store (bucket + optional prefix).
        connector_name: If provided, only resync `latest/` directories for
            these connectors (steps 5-6).  Index rebuilds (steps 9-12)
            always operate on the full set of connectors so that global
            registry files remain complete.
        dry_run: If True, report what would be done without writing.
        with_secrets_mask: If True, regenerate `specs_secrets_mask.yaml`.
        with_legacy_migration: If set, run the named migration step.
            Currently supported: `"v1"` — delete `{registry_type}.json`
            files for connectors whose `registryOverrides.{registry}.enabled`
            is `false`.
        with_metrics: If True, inject latest connector metrics from the
            analytics JSONL export into `generated.metrics`.
        force: If True, resync all connectors' latest/ directories even if the
            existing version marker matches the computed latest version. This
            is useful when metadata content changes without a version bump.

    Returns:
        A `CompileResult` describing what was done.
    """
    if with_legacy_migration and with_legacy_migration not in LEGACY_MIGRATION_VERSIONS:
        raise ValueError(
            f"Unknown legacy migration version: {with_legacy_migration!r}. "
            f"Supported: {', '.join(LEGACY_MIGRATION_VERSIONS)}"
        )

    result = CompileResult(target=store.bucket_root, dry_run=dry_run)

    token = get_gcs_credentials_token()
    fs = gcsfs.GCSFileSystem(token=token)

    # --- Steps 1 and 2: Scan versions and active markers ---
    # Always scan ALL connectors so that index rebuilds are complete.
    _log_progress("Step 1-2: Scanning versions and active markers...")
    connector_versions, yanked, progressive_rollouts = _scan_versions_and_markers(
        fs,
        store=store,
        connector_name=None,
    )
    result.connectors_scanned = len(connector_versions)
    result.versions_found = sum(len(v) for v in connector_versions.values())
    result.yanked_versions = len(yanked)
    _log_progress(
        "  Found %d connectors, %d versions, %d yanked",
        result.connectors_scanned,
        result.versions_found,
        result.yanked_versions,
    )
    _log_progress("  Found %d progressive rollout markers", len(progressive_rollouts))

    # --- Step 3: Compute latest ---
    _log_progress("Step 3: Computing latest GA version per connector...")
    latest_versions = _compute_latest_versions(
        connector_versions=connector_versions,
        yanked=yanked,
        progressive_rollouts=progressive_rollouts,
    )
    _log_progress("  Computed latest for %d connectors", len(latest_versions))

    # --- Step 4: Compute release candidates ---
    _log_progress("Step 4: Computing active release candidates...")
    rc_versions = _compute_release_candidates(
        connector_versions=connector_versions,
        yanked=yanked,
        progressive_rollouts=progressive_rollouts,
    )
    _log_progress("  Computed %d active release candidates", len(rc_versions))

    # --- Step 5: Check existing latest markers ---
    # When --connector-name is set, only check/sync those connectors (steps 5-6).
    # Index rebuilds always use the full unfiltered data.
    if connector_name:
        connector_name_set = set(connector_name)
        sync_scope = {
            c: v for c, v in latest_versions.items() if c in connector_name_set
        }
        _log_progress(
            "  --connector-name filter: syncing %d of %d connectors",
            len(sync_scope),
            len(latest_versions),
        )
    else:
        sync_scope = latest_versions

    _log_progress("Step 5: Checking existing latest/ markers...")
    sync_scope_names = list(sync_scope) if connector_name else None
    existing_markers = _scan_latest_markers(
        fs,
        store=store,
        connector_name=sync_scope_names,
    )
    _log_progress("  Found %d existing markers", len(existing_markers))

    stale_connectors: list[str] = []
    pinned_override_synthesis_connectors: list[str] = []
    for connector, expected_version in sync_scope.items():
        current_marker = existing_markers.get(connector)
        if force or current_marker != expected_version:
            stale_connectors.append(connector)
            continue

        if _requires_pinned_override_synthesis(
            fs,
            store=store,
            connector=connector,
            version=expected_version,
        ):
            pinned_override_synthesis_connectors.append(connector)
            continue

        result.latest_already_current += 1

    _log_progress(
        "  %d connectors need latest/ update, %d already current",
        len(stale_connectors),
        result.latest_already_current,
    )

    # --- Step 6: Resync stale latest/ dirs (parallel) ---
    if stale_connectors:
        _log_progress(
            "Step 6: Syncing %d stale latest/ directories (max_workers=%d)...",
            len(stale_connectors),
            _COMPILE_SYNC_MAX_WORKERS,
        )

        def _sync_one_connector(connector: str) -> None:
            """Sync a single connector's latest/ dir."""
            version = latest_versions[connector]
            _sync_latest_dir(
                fs,
                store=store,
                connector=connector,
                version=version,
                dry_run=dry_run,
            )
            if not dry_run:
                _apply_overrides_to_latest_entry(
                    fs,
                    store=store,
                    connector=connector,
                    version=version,
                )

        sorted_stale = sorted(stale_connectors)
        with ThreadPoolExecutor(max_workers=_COMPILE_SYNC_MAX_WORKERS) as pool:
            futures = {pool.submit(_sync_one_connector, c): c for c in sorted_stale}
            for i, future in enumerate(as_completed(futures), 1):
                connector = futures[future]
                try:
                    future.result()
                    result.latest_updated += 1
                except Exception as exc:
                    error_msg = f"Failed to sync latest/ for {connector}: {exc}"
                    logger.error(error_msg)
                    result.errors.append(error_msg)
                    # Delete the (possibly partial) latest/ dir so the next
                    # compile retries this connector from scratch.
                    try:
                        _delete_latest_dir(
                            fs,
                            store=store,
                            connector=connector,
                        )
                        logger.info(
                            "Cleaned up partial latest/ for %s after failure",
                            connector,
                        )
                    except Exception as cleanup_exc:
                        logger.warning(
                            "Could not clean up latest/ for %s: %s",
                            connector,
                            cleanup_exc,
                        )
                if i % 100 == 0:
                    _log_progress("  Synced %d / %d...", i, len(sorted_stale))
    else:
        _log_progress("Step 6: All latest/ directories are current, nothing to sync.")

    # --- Step 7: Synthesize missing latest entries from pinned overrides ---
    if pinned_override_synthesis_connectors:
        _log_progress(
            "Step 7: Synthesizing %d latest/ registry entries from pinned overrides...",
            len(pinned_override_synthesis_connectors),
        )
        for connector in sorted(pinned_override_synthesis_connectors):
            if dry_run:
                _log_progress(
                    "  [DRY RUN] Would synthesize pinned latest entries for %s",
                    connector,
                )
                result.latest_updated += 1
                continue
            try:
                _apply_overrides_to_latest_entry(
                    fs,
                    store=store,
                    connector=connector,
                    version=sync_scope[connector],
                )
                result.latest_updated += 1
            except Exception as exc:
                error_msg = (
                    f"Failed to synthesize pinned latest entries for {connector}: {exc}"
                )
                logger.error(error_msg)
                result.errors.append(error_msg)

    # --- Step 8: Legacy migration (optional) ---
    if with_legacy_migration == "v1":
        _log_progress(
            "Step 8: Legacy migration v1 — deleting disabled registry entries..."
        )
        migration_deleted = _cleanup_disabled_registry_entries(
            fs,
            store=store,
            connector_versions=connector_versions,
            dry_run=dry_run,
        )
        total_deleted = sum(len(v) for v in migration_deleted.values())
        if migration_deleted:
            for conn, paths in sorted(migration_deleted.items()):
                _log_progress(
                    "  %s: %s %d files",
                    conn,
                    "would delete" if dry_run else "deleted",
                    len(paths),
                )
        _log_progress(
            "  Migration v1: %s %d files across %d connectors",
            "would delete" if dry_run else "deleted",
            total_deleted,
            len(migration_deleted),
        )

    # --- Step 9: Read latest connector metrics (optional) ---
    metrics_bundle = None
    if with_metrics and store.store_type == StoreType.CORAL:
        _log_progress("Step 9: Reading latest connector metrics JSONL...")
        try:
            metrics_bundle = read_latest_connector_metrics()
            result.metrics_source = metrics_bundle.blob_path
            result.metrics_connector_count = metrics_bundle.connector_count
            if metrics_bundle.blob_path:
                _log_progress(
                    "  Loaded metrics for %d connectors from gs://%s",
                    metrics_bundle.connector_count,
                    metrics_bundle.blob_path,
                )
            else:
                _log_progress("  No connector metrics JSONL file found.")
        except Exception as exc:
            error_msg = f"Failed to read connector metrics JSONL: {exc}"
            logger.warning(error_msg)
            result.metrics_error = error_msg
            _log_progress("  %s", error_msg)
    elif with_metrics:
        _log_progress("Step 9: Skipping connector metrics for non-coral registry.")
    else:
        _log_progress("Step 9: Connector metrics injection disabled.")

    # --- Step 10: Compile global registry JSONs ---
    _log_progress("Step 10: Compiling global registry JSON files...")
    all_registry_entries: list[dict[str, Any]] = []  # collected for Step 13
    entries_by_registry_type: dict[str, list[dict[str, Any]]] = {}
    for registry_type in VALID_REGISTRIES:
        entries = _compile_global_registry(
            fs,
            store=store,
            latest_versions=latest_versions,
            registry_type=registry_type,
        )

        # Inject release candidate info into entries that have active RCs.
        if rc_versions:
            rc_entries: dict[str, list[dict[str, Any]]] = {}
            for connector, rc_ver_list in rc_versions.items():
                for rc_ver in rc_ver_list:
                    rc_entry = _read_rc_registry_entry(
                        fs,
                        store=store,
                        connector=connector,
                        rc_version=rc_ver,
                        registry_type=registry_type,
                    )
                    if rc_entry:
                        docker_repo = rc_entry.get(
                            "dockerRepository",
                            f"airbyte/{connector}",
                        )
                        rc_entries.setdefault(docker_repo, []).append(
                            {
                                "version": rc_ver,
                                "entry": rc_entry,
                            }
                        )
            if rc_entries:
                entries = _apply_release_candidates_to_entries(entries, rc_entries)
                total_rcs = sum(len(v) for v in rc_entries.values())
                _log_progress(
                    "  Injected %d release candidate(s) for %d connector(s) into %s registry",
                    total_rcs,
                    len(rc_entries),
                    registry_type,
                )

        if metrics_bundle is not None:
            injected = apply_metrics_to_registry_entries(entries, metrics_bundle)
            result.metrics_registry_entries += injected
            _log_progress(
                "  Injected metrics into %d %s registry entries",
                injected,
                registry_type,
            )

        all_registry_entries.extend(entries)
        entries_by_registry_type[registry_type] = entries
        registry_json = _build_global_registry_json(entries)
        entry_count = len(registry_json["sources"]) + len(registry_json["destinations"])

        if registry_type == "cloud":
            result.cloud_registry_entries = entry_count
        else:
            result.oss_registry_entries = entry_count

        if dry_run:
            _log_progress(
                "  [DRY RUN] Would write %s_registry.json (%d entries)",
                registry_type,
                entry_count,
            )
        else:
            content = json.dumps(registry_json, indent=2, sort_keys=True) + "\n"
            path_prefix = f"{store.prefix}/" if store.prefix else ""
            _write_gcs_blob_with_custom_ttl(
                bucket_name=store.bucket,
                blob_path=f"{path_prefix}{_REGISTRIES_PREFIX}/{registry_type}_registry.json",
                content=content,
                cache_control=_REGISTRY_INDEX_CACHE_CONTROL,
            )
            _log_progress(
                "  Wrote %s_registry.json (%d entries)",
                registry_type,
                entry_count,
            )

    # --- Step 11: Compile composite registry JSON (superset) ---
    _log_progress("Step 11: Compiling composite_registry.json (superset)...")
    composite_json = _build_composite_registry_json(
        cloud_entries=entries_by_registry_type.get("cloud", []),
        oss_entries=entries_by_registry_type.get("oss", []),
    )
    composite_entry_count = len(composite_json["sources"]) + len(
        composite_json["destinations"]
    )
    result.composite_registry_entries = composite_entry_count
    if dry_run:
        _log_progress(
            "  [DRY RUN] Would write composite_registry.json (%d entries)",
            composite_entry_count,
        )
    else:
        composite_content = json.dumps(composite_json, indent=2, sort_keys=True) + "\n"
        path_prefix = f"{store.prefix}/" if store.prefix else ""
        _write_gcs_blob_with_custom_ttl(
            bucket_name=store.bucket,
            blob_path=f"{path_prefix}{_REGISTRIES_PREFIX}/composite_registry.json",
            content=composite_content,
            cache_control=_REGISTRY_INDEX_CACHE_CONTROL,
        )
        _log_progress(
            "  Wrote composite_registry.json (%d entries)",
            composite_entry_count,
        )

    # --- Step 12: Per-connector version indexes (parallel) ---
    _log_progress(
        "Step 12: Writing per-connector version indexes (max_workers=%d)...",
        _COMPILE_WRITE_MAX_WORKERS,
    )
    base = f"{store.bucket_root}/{METADATA_FOLDER}/airbyte"
    sorted_connectors = sorted(connector_versions)

    def _write_one_version_index(connector: str) -> None:
        """Build and write a single connector's versions.json."""
        versions = connector_versions[connector]
        latest_v = latest_versions.get(connector)
        rc_v_list = rc_versions.get(connector)
        index = _build_version_index(
            fs,
            store=store,
            connector=connector,
            versions=versions,
            yanked=yanked,
            latest_version=latest_v,
            rc_version=rc_v_list[0] if rc_v_list else None,
            rc_versions_all=rc_v_list,
        )
        index_path = f"{base}/{connector}/versions.json"
        if dry_run:
            _log_progress(
                "  [DRY RUN] Would write %s/versions.json (%d versions)",
                connector,
                len(versions),
            )
        else:
            content = json.dumps(index, indent=2, sort_keys=True) + "\n"
            with fs.open(index_path, "w") as f:
                f.write(content)

    with ThreadPoolExecutor(max_workers=_COMPILE_WRITE_MAX_WORKERS) as pool:
        futures = {
            pool.submit(_write_one_version_index, c): c for c in sorted_connectors
        }
        for i, future in enumerate(as_completed(futures), 1):
            connector = futures[future]
            try:
                future.result()
                result.version_indexes_written += 1
            except Exception as exc:
                error_msg = f"Failed to write versions.json for {connector}: {exc}"
                logger.error(error_msg)
                result.errors.append(error_msg)
            if i % 100 == 0:
                _log_progress(
                    "  Wrote %d / %d version indexes...", i, len(sorted_connectors)
                )

    # --- Step 13: Specs secrets mask (optional) ---
    if with_secrets_mask:
        _log_progress("Step 13: Generating specs secrets mask...")
        # Reuse entries collected during Step 10 to avoid redundant GCS reads.
        secret_names = _extract_secret_property_names(all_registry_entries)
        sorted_names = sorted(secret_names)
        result.specs_secrets_mask_properties = len(sorted_names)
        mask_content = yaml.dump({"properties": sorted_names}, default_flow_style=False)
        mask_path = (
            f"{store.bucket_root}/{_REGISTRIES_PREFIX}/{_SPECS_SECRETS_MASK_FILENAME}"
        )

        _log_progress(
            "  Found %d secret properties: %s",
            len(sorted_names),
            ", ".join(sorted_names),
        )

        if dry_run:
            _log_progress(
                "  [DRY RUN] Would write %s",
                _SPECS_SECRETS_MASK_FILENAME,
            )
        else:
            with fs.open(mask_path, "w") as f:
                f.write(mask_content)
            _log_progress(
                "  Wrote %s",
                _SPECS_SECRETS_MASK_FILENAME,
            )

    _log_progress(result.summary())
    return result
