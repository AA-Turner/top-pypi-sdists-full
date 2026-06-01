# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Registry store comparison operations.

This module compares two registry stores (e.g. a candidate dev store against
the prod reference) and reports differences at both the index and per-connector
artifact level.

Usage:

    from airbyte_ops_mcp.registry.compare import compare_stores

    result = compare_stores(
        store_bucket="dev-airbyte-cloud-connector-metadata-service-2",
        store_prefix="dev/20260306-mirror-compile/",
        reference_bucket="prod-airbyte-cloud-connector-metadata-service",
        reference_prefix="",
        connector_name=["source-faker"],
    )

High-level algorithm
--------------------
1. Discover connectors in both stores by scanning versioned directories
   (`metadata/airbyte/<connector>/<version>/metadata.yaml`).  Falls back to
   `latest/` discovery when no versioned paths are found.
2. For connectors present in both, resolve the comparison version (highest GA
   semver in the store, matched against the reference).
3. Compare per-connector artifacts:
   `metadata.yaml`, `cloud.json`, `oss.json`, `spec.json`.
4. Compare global registry indexes:
   `registries/v0/cloud_registry.json`, `registries/v0/oss_registry.json`.
5. Return a structured result with per-connector and index-level diffs.

Tolerated paths
---------------
Certain JSON fields are expected to differ between stores (e.g. generation
timestamps).  The `tolerated_paths` parameter accepts dpath glob expressions
that identify fields where **presence and type** are validated but **value
differences** are suppressed.
"""

from __future__ import annotations

import contextlib
import copy
import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any

import dpath
import gcsfs
from packaging.version import InvalidVersion, Version

from airbyte_ops_mcp.registry._constants import METADATA_FOLDER
from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_credentials_token

logger = logging.getLogger(__name__)

# Artifact files to compare per connector version
_ARTIFACT_FILES = ("metadata.yaml", "cloud.json", "oss.json", "spec.json")

# Global index files to compare
_INDEX_FILES = (
    "registries/v0/cloud_registry.json",
    "registries/v0/oss_registry.json",
)

# Default tolerated dpath expressions -- presence and type are still validated,
# but differing values are not reported as differences.
DEFAULT_TOLERATED_PATHS: tuple[str, ...] = (
    "generated/source_file_info/metadata_last_modified",
    "generated/source_file_info/registry_entry_generated_at",
)

# Degree of parallelism for per-connector artifact comparison.
# Each thread performs ~10 GCS RPCs per connector; 20 threads keeps
# total in-flight requests manageable while cutting wall-clock time ~20x.
_COMPARE_ARTIFACT_MAX_WORKERS = 20


# ---------------------------------------------------------------------------
# Result models
# ---------------------------------------------------------------------------


@dataclass
class ArtifactDiff:
    """Difference found in a single artifact file."""

    connector: str
    file: str
    status: str  # "only_in_store", "only_in_reference", "content_differs", "match"
    details: str = ""
    tolerated_diffs: list[str] = field(default_factory=list)


@dataclass
class ConnectorDiff:
    """Summary of differences for a single connector."""

    connector: str
    status: str  # "only_in_store", "only_in_reference", "artifacts_differ", "match"
    artifact_diffs: list[ArtifactDiff] = field(default_factory=list)
    store_version: str = ""
    reference_version: str = ""


@dataclass
class IndexDiff:
    """Difference found in a global index file."""

    file: str
    status: str  # "only_in_store", "only_in_reference", "content_differs", "match"
    entry_count_store: int = 0
    entry_count_reference: int = 0
    details: str = ""


@dataclass
class CompareResult:
    """Full result of a store comparison."""

    store: str
    reference_store: str
    connectors_in_store: int = 0
    connectors_in_reference: int = 0
    connectors_only_in_store: list[str] = field(default_factory=list)
    connectors_only_in_reference: list[str] = field(default_factory=list)
    connectors_matching: int = 0
    connectors_differing: int = 0
    connector_diffs: list[ConnectorDiff] = field(default_factory=list)
    index_diffs: list[IndexDiff] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.errors:
            return "completed-with-errors"
        if (
            self.connectors_only_in_store
            or self.connectors_only_in_reference
            or self.connectors_differing
            or any(d.status != "match" for d in self.index_diffs)
        ):
            return "differences-found"
        return "match"

    def summary(self) -> str:
        return (
            f"[{self.status}] "
            f"Store: {self.connectors_in_store} connectors, "
            f"Reference: {self.connectors_in_reference} connectors. "
            f"Only in store: {len(self.connectors_only_in_store)}, "
            f"only in reference: {len(self.connectors_only_in_reference)}. "
            f"Matching: {self.connectors_matching}, "
            f"differing: {self.connectors_differing}. "
            f"Errors: {len(self.errors)}."
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-friendly dict."""
        return {
            "status": self.status,
            "store": self.store,
            "reference_store": self.reference_store,
            "connectors_in_store": self.connectors_in_store,
            "connectors_in_reference": self.connectors_in_reference,
            "connectors_only_in_store": self.connectors_only_in_store,
            "connectors_only_in_reference": self.connectors_only_in_reference,
            "connectors_matching": self.connectors_matching,
            "connectors_differing": self.connectors_differing,
            "connector_diffs": [
                {
                    "connector": d.connector,
                    "status": d.status,
                    "store_version": d.store_version,
                    "reference_version": d.reference_version,
                    "artifact_diffs": [
                        {
                            "file": a.file,
                            "status": a.status,
                            "details": a.details,
                            **(
                                {"tolerated_diffs": a.tolerated_diffs}
                                if a.tolerated_diffs
                                else {}
                            ),
                        }
                        for a in d.artifact_diffs
                    ],
                }
                for d in self.connector_diffs
            ],
            "index_diffs": [
                {
                    "file": d.file,
                    "status": d.status,
                    "entry_count_store": d.entry_count_store,
                    "entry_count_reference": d.entry_count_reference,
                    "details": d.details,
                }
                for d in self.index_diffs
            ],
            "errors": self.errors,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _log_progress(msg: str, *args: object) -> None:
    """Log a progress message to both the logger and stderr."""
    logger.info(msg, *args)
    formatted = msg % args if args else msg
    print(formatted, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Version-aware connector discovery
# ---------------------------------------------------------------------------


def _is_ga_version(version_str: str) -> bool:
    """Return True if the version string is a GA (non-prerelease) semver."""
    try:
        v = Version(version_str)
    except InvalidVersion:
        return False
    return not v.is_prerelease and not v.is_devrelease


def _parse_version(version_str: str) -> Version | None:
    """Parse a version string, returning None if invalid."""
    try:
        return Version(version_str)
    except InvalidVersion:
        return None


def _extract_connector_version(
    path: str, bucket: str, prefix: str = ""
) -> tuple[str, str] | None:
    """Extract (connector_name, version) from a GCS metadata path.

    Expected path format:
        `<bucket>/[<prefix>/]metadata/airbyte/<connector>/<version>/metadata.yaml`

    Returns None if the path does not match or the directory is `latest`
    or `release_candidate`.
    """
    expected_prefix = f"{bucket}/{prefix}{METADATA_FOLDER}/airbyte/"
    if not path.startswith(expected_prefix):
        return None
    remainder = path[len(expected_prefix) :]
    parts = remainder.split("/")
    if len(parts) < 2:
        return None
    connector = parts[0]
    version = parts[1]
    if version in ("latest", "release_candidate"):
        return None
    return connector, version


def _discover_connectors_with_versions(
    fs: gcsfs.GCSFileSystem,
    bucket: str,
    prefix: str,
    connector_name: list[str] | None = None,
) -> dict[str, list[str]]:
    """Discover connectors and their available versions by scanning versioned paths.

    Scans `metadata/airbyte/<connector>/<version>/metadata.yaml` to find all
    (connector, version) pairs.  Falls back to `latest/` discovery if no
    versioned paths are found.

    Returns:
        dict mapping connector_name -> list of version strings.
    """
    base = f"{bucket}/{prefix}{METADATA_FOLDER}/airbyte"

    # Primary: scan versioned directories
    if connector_name:
        metadata_paths: list[str] = []
        for name in connector_name:
            pattern = f"{base}/{name}/*/metadata.yaml"
            metadata_paths.extend(fs.glob(pattern))
    else:
        pattern = f"{base}/*/*/metadata.yaml"
        metadata_paths = fs.glob(pattern)

    connector_versions: dict[str, list[str]] = {}
    for path in metadata_paths:
        parsed = _extract_connector_version(path, bucket, prefix)
        if parsed is None:
            continue
        connector, version = parsed
        connector_versions.setdefault(connector, []).append(version)

    # Also scan latest/ directories to find connectors that only have latest/
    # (e.g. compiled stores or mixed stores with some versioned + some latest-only).
    if connector_name:
        latest_paths: list[str] = []
        for name in connector_name:
            latest_pattern = f"{base}/{name}/latest/metadata.yaml"
            latest_paths.extend(fs.glob(latest_pattern))
    else:
        latest_pattern = f"{base}/*/latest/metadata.yaml"
        latest_paths = fs.glob(latest_pattern)

    for path in latest_paths:
        parts = path.split("/")
        try:
            # Use tail of path to avoid mis-parsing if prefix contains "latest"
            # Expected: .../<connector>/latest/metadata.yaml
            if len(parts) >= 3 and parts[-2] == "latest":
                connector = parts[-3]
            else:
                continue
            if connector in connector_versions:
                # Already discovered via versioned paths -- skip
                continue
            connector_versions.setdefault(connector, []).append("latest")
        except (ValueError, IndexError):
            logger.warning("Could not parse connector from path: %s", path)

    return connector_versions


def _resolve_best_version(versions: list[str]) -> str:
    """Pick the best version to use for comparison.

    Prefers the highest GA semver.  Falls back to the highest pre-release,
    then `"latest"` if only that pseudo-version is available.
    """
    if versions == ["latest"]:
        return "latest"

    ga_candidates: list[tuple[Version, str]] = []
    all_candidates: list[tuple[Version, str]] = []
    for v_str in versions:
        if v_str == "latest":
            continue
        parsed = _parse_version(v_str)
        if parsed is None:
            continue
        all_candidates.append((parsed, v_str))
        if _is_ga_version(v_str):
            ga_candidates.append((parsed, v_str))

    if ga_candidates:
        ga_candidates.sort(reverse=True)
        return ga_candidates[0][1]

    if all_candidates:
        all_candidates.sort(reverse=True)
        return all_candidates[0][1]

    return "latest"


def _resolve_reference_version(
    fs: gcsfs.GCSFileSystem,
    ref_base: str,
    connector: str,
    store_version: str,
) -> str:
    """Resolve the version to compare against in the reference store.

    Tries the exact store version first.  Falls back to `latest/`.
    """
    if store_version == "latest":
        return "latest"

    # Try exact version match in reference
    ref_path = f"{ref_base}/{connector}/{store_version}/metadata.yaml"
    if fs.exists(ref_path):
        return store_version

    # Fall back to latest/
    ref_latest = f"{ref_base}/{connector}/latest/metadata.yaml"
    if fs.exists(ref_latest):
        return "latest"

    return store_version


def _read_json_blob(
    fs: gcsfs.GCSFileSystem,
    path: str,
) -> dict[str, Any] | None:
    """Read and parse a JSON blob, returning None if it doesn't exist."""
    if not fs.exists(path):
        return None
    with fs.open(path, "r") as f:
        return json.load(f)


def _read_text_blob(
    fs: gcsfs.GCSFileSystem,
    path: str,
) -> str | None:
    """Read a text blob, returning None if it doesn't exist."""
    if not fs.exists(path):
        return None
    with fs.open(path, "r") as f:
        return f.read()


def _normalize_json(data: Any) -> str:
    """Serialize JSON with sorted keys for stable comparison."""
    return json.dumps(data, sort_keys=True, indent=2)


# ---------------------------------------------------------------------------
# Tolerated-path helpers
# ---------------------------------------------------------------------------


def _get_value_type_name(value: Any) -> str:
    """Return a simple type name suitable for comparison."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    return type(value).__name__


def _apply_tolerations(
    store_data: dict[str, Any],
    ref_data: dict[str, Any],
    tolerated_paths: tuple[str, ...] | list[str],
) -> tuple[dict[str, Any], dict[str, Any], list[str], list[str]]:
    """Strip tolerated paths from copies of both dicts after validating presence and type.

    Only suppresses a tolerated path when presence and type match **and** at
    least one matched value actually differs between store and reference.
    Identical values are left in place so they do not appear in the tolerated
    list.  Deep copies are deferred until the first path that needs deletion.

    Returns:
        Tuple of (store_copy, ref_copy, tolerated_list, violation_messages).
        `tolerated_list` contains the dpath expressions whose values differed
        but were suppressed.  `violation_messages` contains descriptions of
        paths that failed presence or type validation despite being tolerated.
    """
    store_copy: dict[str, Any] | None = None
    ref_copy: dict[str, Any] | None = None
    tolerated: list[str] = []
    violations: list[str] = []

    for dpath_expr in tolerated_paths:
        store_matches = dict(dpath.search(store_data, dpath_expr, yielded=True))
        ref_matches = dict(dpath.search(ref_data, dpath_expr, yielded=True))

        store_paths = set(store_matches.keys())
        ref_paths = set(ref_matches.keys())

        # Presence validation -- both the existence and the matched path sets
        # must align.  A count mismatch indicates a structural difference.
        if store_paths != ref_paths:
            if not store_paths and not ref_paths:
                # Neither side has this path -- nothing to tolerate
                continue
            if store_paths and not ref_paths:
                violations.append(
                    f"tolerated path '{dpath_expr}' present in store but missing in reference"
                )
            elif ref_paths and not store_paths:
                violations.append(
                    f"tolerated path '{dpath_expr}' present in reference but missing in store"
                )
            else:
                violations.append(
                    f"tolerated path '{dpath_expr}' matched different paths: "
                    f"store={sorted(store_paths)}, reference={sorted(ref_paths)}"
                )
            continue

        # Type validation for each matched path (keyed by path for safety)
        type_ok = True
        for m_path in sorted(store_paths):
            s_type = _get_value_type_name(store_matches[m_path])
            r_type = _get_value_type_name(ref_matches[m_path])
            if s_type != r_type:
                violations.append(
                    f"tolerated path '{dpath_expr}' has type mismatch at '{m_path}': "
                    f"store={s_type}, reference={r_type}"
                )
                type_ok = False
                break

        if not type_ok:
            continue

        # Check whether at least one matched value actually differs
        has_diff = any(
            _normalize_json(store_matches[p]) != _normalize_json(ref_matches[p])
            for p in store_paths
        )
        if not has_diff:
            # Values are identical -- no need to suppress anything
            continue

        # Values differ but presence and type match -- suppress by removing
        # from copies so they don't appear in the downstream comparison.
        if store_copy is None:
            store_copy = copy.deepcopy(store_data)
            ref_copy = copy.deepcopy(ref_data)

        for m_path in store_paths:
            with contextlib.suppress(KeyError, dpath.PathNotFound):
                dpath.delete(store_copy, m_path)
            with contextlib.suppress(KeyError, dpath.PathNotFound):
                assert ref_copy is not None  # for type checker
                dpath.delete(ref_copy, m_path)

        tolerated.append(dpath_expr)

    return (
        store_copy if store_copy is not None else store_data,
        ref_copy if ref_copy is not None else ref_data,
        tolerated,
        violations,
    )


# ---------------------------------------------------------------------------
# JSON content comparison
# ---------------------------------------------------------------------------


def _compare_json_content(
    store_data: dict[str, Any],
    ref_data: dict[str, Any],
    tolerated_paths: tuple[str, ...] | list[str] = (),
) -> tuple[str, list[str]]:
    """Compare two JSON dicts and return a human-readable diff summary.

    Args:
        store_data: JSON dict from the store being evaluated.
        ref_data: JSON dict from the reference store.
        tolerated_paths: dpath expressions for fields where value differences
            are suppressed (presence and type are still validated).

    Returns:
        Tuple of (details_string, tolerated_list).
        `details_string` is empty if the dicts match (after toleration).
        `tolerated_list` names the paths whose values differed but were
        suppressed.
    """
    all_tolerated: list[str] = []
    effective_store = store_data
    effective_ref = ref_data

    if tolerated_paths:
        effective_store, effective_ref, tolerated, violations = _apply_tolerations(
            store_data, ref_data, tolerated_paths
        )
        all_tolerated = tolerated
        if violations:
            logger.warning("Toleration violations: %s", "; ".join(violations))

    store_normalized = _normalize_json(effective_store)
    ref_normalized = _normalize_json(effective_ref)

    if store_normalized == ref_normalized:
        return "", all_tolerated

    # Find top-level key differences
    store_keys = set(effective_store.keys())
    ref_keys = set(effective_ref.keys())

    diffs: list[str] = []
    only_in_store = store_keys - ref_keys
    only_in_ref = ref_keys - store_keys
    if only_in_store:
        diffs.append(f"keys only in store: {sorted(only_in_store)}")
    if only_in_ref:
        diffs.append(f"keys only in reference: {sorted(only_in_ref)}")

    # Check value differences for shared keys
    changed_keys: list[str] = []
    for key in sorted(store_keys & ref_keys):
        if _normalize_json(effective_store[key]) != _normalize_json(effective_ref[key]):
            changed_keys.append(key)
    if changed_keys:
        diffs.append(f"values differ for keys: {changed_keys}")

    details = "; ".join(diffs) if diffs else "content differs (nested)"
    return details, all_tolerated


# ---------------------------------------------------------------------------
# Per-connector comparison
# ---------------------------------------------------------------------------


def _compare_connector_artifacts(
    fs: gcsfs.GCSFileSystem,
    connector: str,
    store_base: str,
    ref_base: str,
    store_version: str,
    ref_version: str,
    tolerated_paths: tuple[str, ...] | list[str] = (),
) -> ConnectorDiff:
    """Compare artifacts for a single connector between store and reference.

    Uses the resolved `store_version` and `ref_version` to build
    artifact paths instead of always looking at `latest/`.
    """
    artifact_diffs: list[ArtifactDiff] = []

    for filename in _ARTIFACT_FILES:
        store_path = f"{store_base}/{connector}/{store_version}/{filename}"
        ref_path = f"{ref_base}/{connector}/{ref_version}/{filename}"

        store_exists = fs.exists(store_path)
        ref_exists = fs.exists(ref_path)

        if not store_exists and not ref_exists:
            continue
        if store_exists and not ref_exists:
            artifact_diffs.append(
                ArtifactDiff(
                    connector=connector,
                    file=filename,
                    status="only_in_store",
                )
            )
            continue
        if not store_exists and ref_exists:
            artifact_diffs.append(
                ArtifactDiff(
                    connector=connector,
                    file=filename,
                    status="only_in_reference",
                )
            )
            continue

        # Both exist -- compare contents
        if filename.endswith(".json"):
            store_data = _read_json_blob(fs, store_path)
            ref_data = _read_json_blob(fs, ref_path)
            if store_data is not None and ref_data is not None:
                details, tolerated = _compare_json_content(
                    store_data, ref_data, tolerated_paths
                )
                if details:
                    artifact_diffs.append(
                        ArtifactDiff(
                            connector=connector,
                            file=filename,
                            status="content_differs",
                            details=details,
                            tolerated_diffs=tolerated,
                        )
                    )
                elif tolerated:
                    # All diffs were tolerated -- still record for visibility
                    artifact_diffs.append(
                        ArtifactDiff(
                            connector=connector,
                            file=filename,
                            status="match",
                            details="",
                            tolerated_diffs=tolerated,
                        )
                    )
        else:
            # YAML or other text -- byte comparison
            store_text = _read_text_blob(fs, store_path)
            ref_text = _read_text_blob(fs, ref_path)
            if store_text != ref_text:
                artifact_diffs.append(
                    ArtifactDiff(
                        connector=connector,
                        file=filename,
                        status="content_differs",
                        details="text content differs",
                    )
                )

    # Only real diffs (not tolerated-only matches) count as differing
    real_diffs = [d for d in artifact_diffs if d.status != "match"]
    status = "match" if not real_diffs else "artifacts_differ"
    return ConnectorDiff(
        connector=connector,
        status=status,
        artifact_diffs=artifact_diffs,
        store_version=store_version,
        reference_version=ref_version,
    )


# ---------------------------------------------------------------------------
# Index comparison
# ---------------------------------------------------------------------------


def _compare_index_file(
    fs: gcsfs.GCSFileSystem,
    filename: str,
    store_bucket_root: str,
    ref_bucket_root: str,
    tolerated_paths: tuple[str, ...] | list[str] = (),
) -> IndexDiff:
    """Compare a global registry index file between store and reference."""
    store_path = f"{store_bucket_root}/{filename}"
    ref_path = f"{ref_bucket_root}/{filename}"

    store_data = _read_json_blob(fs, store_path)
    ref_data = _read_json_blob(fs, ref_path)

    if store_data is None and ref_data is None:
        return IndexDiff(file=filename, status="match")
    if store_data is not None and ref_data is None:
        return IndexDiff(file=filename, status="only_in_store")
    if store_data is None and ref_data is not None:
        return IndexDiff(file=filename, status="only_in_reference")

    # Both exist
    assert store_data is not None
    assert ref_data is not None

    store_sources = len(store_data.get("sources", []))
    store_dests = len(store_data.get("destinations", []))
    ref_sources = len(ref_data.get("sources", []))
    ref_dests = len(ref_data.get("destinations", []))

    store_count = store_sources + store_dests
    ref_count = ref_sources + ref_dests

    details, _tolerated = _compare_json_content(store_data, ref_data, tolerated_paths)
    status = "match" if not details else "content_differs"

    return IndexDiff(
        file=filename,
        status=status,
        entry_count_store=store_count,
        entry_count_reference=ref_count,
        details=details,
    )


def _compare_index_file_from_data(
    filename: str,
    store_data: dict[str, Any] | None,
    ref_data: dict[str, Any] | None,
    tolerated_paths: tuple[str, ...] | list[str] = (),
) -> IndexDiff:
    """Build an `IndexDiff` from already-loaded index JSON data.

    This is the same logic as :func:`_compare_index_file` but avoids a
    redundant GCS read when the caller has already fetched the data (e.g.
    in the fast index-only code path).
    """
    if store_data is None and ref_data is None:
        return IndexDiff(file=filename, status="match")
    if store_data is not None and ref_data is None:
        return IndexDiff(file=filename, status="only_in_store")
    if store_data is None and ref_data is not None:
        return IndexDiff(file=filename, status="only_in_reference")

    # Both exist
    assert store_data is not None
    assert ref_data is not None

    store_sources = len(store_data.get("sources", []))
    store_dests = len(store_data.get("destinations", []))
    ref_sources = len(ref_data.get("sources", []))
    ref_dests = len(ref_data.get("destinations", []))

    store_count = store_sources + store_dests
    ref_count = ref_sources + ref_dests

    details, _tolerated = _compare_json_content(store_data, ref_data, tolerated_paths)
    status = "match" if not details else "content_differs"

    return IndexDiff(
        file=filename,
        status=status,
        entry_count_store=store_count,
        entry_count_reference=ref_count,
        details=details,
    )


def _extract_connectors_from_index(
    index_data: dict[str, Any],
) -> set[str]:
    """Extract connector docker-repository names from a registry index JSON.

    Parses the `sources` and `destinations` arrays and returns the set of
    unique `dockerRepository` values.  This provides a lightweight way to
    determine which connectors are present without scanning the GCS bucket
    structure.
    """
    repos: set[str] = set()
    for section in ("sources", "destinations"):
        for entry in index_data.get(section, []):
            docker_repo = entry.get("dockerRepository", "")
            if docker_repo:
                # Strip the registry prefix (e.g. "airbyte/source-faker"
                # -> "source-faker") to match the connector names used
                # by the discovery-based code path.
                name = (
                    docker_repo.split("/", 1)[-1] if "/" in docker_repo else docker_repo
                )
                repos.add(name)
    return repos


# ---------------------------------------------------------------------------
# Main compare function
# ---------------------------------------------------------------------------


def compare_stores(
    store_bucket: str,
    store_prefix: str,
    reference_bucket: str,
    reference_prefix: str,
    connector_name: list[str] | None = None,
    *,
    with_artifacts: bool = True,
    with_indexes: bool = True,
    tolerated_paths: tuple[str, ...] | list[str] = DEFAULT_TOLERATED_PATHS,
) -> CompareResult:
    """Compare two registry stores and return structured differences.

    Args:
        store_bucket: Bucket name for the store being evaluated.
        store_prefix: Path prefix within the store bucket (e.g. `"dev/20260306/"`).
            Must include trailing `/` if non-empty.
        reference_bucket: Bucket name for the known-good reference store.
        reference_prefix: Path prefix within the reference bucket.
            Must include trailing `/` if non-empty.
        connector_name: If provided, only compare these connector names.
        with_artifacts: If *True* (default), compare per-connector artifact
            files (`metadata.yaml`, `cloud.json`, `oss.json`, `spec.json`).
        with_indexes: If *True* (default), compare global registry index
            files (`cloud_registry.json`, `oss_registry.json`).
        tolerated_paths: dpath expressions for JSON fields where value
            differences are suppressed (presence and type are still validated).
            Pass an empty tuple to disable.

    Returns:
        A `CompareResult` with all differences found.
    """
    store_label = f"{store_bucket}/{store_prefix}" if store_prefix else store_bucket
    ref_label = (
        f"{reference_bucket}/{reference_prefix}"
        if reference_prefix
        else reference_bucket
    )

    result = CompareResult(store=store_label, reference_store=ref_label)

    token = get_gcs_credentials_token()
    fs = gcsfs.GCSFileSystem(token=token)

    # ------------------------------------------------------------------
    # Fast path: index-only mode (no artifact comparison requested)
    # ------------------------------------------------------------------
    # When only comparing indexes, we skip the expensive GCS glob-based
    # connector discovery entirely.  Instead, connector-level counts and
    # only-in-store / only-in-reference lists are derived from the index
    # JSON files themselves.
    # ------------------------------------------------------------------
    if not with_artifacts:
        _log_progress("Skipping per-connector artifact comparison (--no-artifacts).")

        if with_indexes:
            store_root = (
                f"{store_bucket}/{store_prefix.rstrip('/')}"
                if store_prefix
                else store_bucket
            )
            ref_root = (
                f"{reference_bucket}/{reference_prefix.rstrip('/')}"
                if reference_prefix
                else reference_bucket
            )

            _log_progress("Comparing global index files...")

            # Accumulate connector names across all index files so that
            # the result reports meaningful connector-level counts even
            # without a full bucket scan.
            all_store_connectors: set[str] = set()
            all_ref_connectors: set[str] = set()

            for index_file in _INDEX_FILES:
                try:
                    store_path = f"{store_root}/{index_file}"
                    ref_path = f"{ref_root}/{index_file}"

                    store_data = _read_json_blob(fs, store_path)
                    ref_data = _read_json_blob(fs, ref_path)

                    # Accumulate connector names from the index contents
                    if store_data is not None:
                        all_store_connectors |= _extract_connectors_from_index(
                            store_data
                        )
                    if ref_data is not None:
                        all_ref_connectors |= _extract_connectors_from_index(ref_data)

                    # Build the IndexDiff from the already-loaded data
                    index_diff = _compare_index_file_from_data(
                        index_file,
                        store_data,
                        ref_data,
                        tolerated_paths,
                    )
                    result.index_diffs.append(index_diff)
                except Exception as exc:
                    result.errors.append(f"Error comparing index {index_file}: {exc}")

            # Apply optional connector name filter
            if connector_name:
                filter_set = set(connector_name)
                all_store_connectors &= filter_set
                all_ref_connectors &= filter_set

            result.connectors_in_store = len(all_store_connectors)
            result.connectors_in_reference = len(all_ref_connectors)
            result.connectors_only_in_store = sorted(
                all_store_connectors - all_ref_connectors
            )
            result.connectors_only_in_reference = sorted(
                all_ref_connectors - all_store_connectors
            )
            result.connectors_matching = len(all_store_connectors & all_ref_connectors)
        else:
            _log_progress("Skipping global index comparison (--no-indexes).")

        _log_progress(result.summary())
        return result

    # ------------------------------------------------------------------
    # Standard path: artifact comparison (discovery required)
    # ------------------------------------------------------------------

    # Step 1: Discover connectors and versions in both stores (parallel)
    _log_progress("Discovering connectors in store and reference in parallel...")

    with ThreadPoolExecutor(max_workers=2) as pool:
        store_future = pool.submit(
            _discover_connectors_with_versions,
            gcsfs.GCSFileSystem(token=token),
            store_bucket,
            store_prefix,
            connector_name,
        )
        ref_future = pool.submit(
            _discover_connectors_with_versions,
            gcsfs.GCSFileSystem(token=token),
            reference_bucket,
            reference_prefix,
            connector_name,
        )
        store_cv = store_future.result()
        ref_cv = ref_future.result()

    store_connectors = set(store_cv.keys())
    _log_progress(
        "Found %d connectors in store (%d total versions)",
        len(store_connectors),
        sum(len(v) for v in store_cv.values()),
    )

    ref_connectors = set(ref_cv.keys())
    _log_progress(
        "Found %d connectors in reference (%d total versions)",
        len(ref_connectors),
        sum(len(v) for v in ref_cv.values()),
    )

    # Apply connector name filter (already partially applied during discovery,
    # but re-apply here for safety with the intersection logic)
    if connector_name:
        filter_set = set(connector_name)
        store_connectors = store_connectors & filter_set
        ref_connectors = ref_connectors & filter_set

    result.connectors_in_store = len(store_connectors)
    result.connectors_in_reference = len(ref_connectors)

    # Connectors only in one store
    result.connectors_only_in_store = sorted(store_connectors - ref_connectors)
    result.connectors_only_in_reference = sorted(ref_connectors - store_connectors)

    for c in result.connectors_only_in_store:
        result.connector_diffs.append(
            ConnectorDiff(connector=c, status="only_in_store")
        )
    for c in result.connectors_only_in_reference:
        result.connector_diffs.append(
            ConnectorDiff(connector=c, status="only_in_reference")
        )

    # Step 2: Compare per-connector artifacts
    common = sorted(store_connectors & ref_connectors)

    _log_progress(
        "Comparing artifacts for %d connectors present in both stores"
        " (max_workers=%d)...",
        len(common),
        _COMPARE_ARTIFACT_MAX_WORKERS,
    )

    store_base = f"{store_bucket}/{store_prefix}{METADATA_FOLDER}/airbyte"
    ref_base = f"{reference_bucket}/{reference_prefix}{METADATA_FOLDER}/airbyte"

    def _compare_one(connector: str) -> ConnectorDiff | str:
        """Compare a single connector in a worker thread.

        Returns a `ConnectorDiff` on success or an error string on
        failure.  Each thread creates its own `gcsfs` client because
        `GCSFileSystem` is not thread-safe.
        """
        try:
            thread_fs = gcsfs.GCSFileSystem(token=token)
            store_version = _resolve_best_version(store_cv.get(connector, ["latest"]))
            ref_version = _resolve_reference_version(
                thread_fs, ref_base, connector, store_version
            )
            return _compare_connector_artifacts(
                thread_fs,
                connector,
                store_base,
                ref_base,
                store_version=store_version,
                ref_version=ref_version,
                tolerated_paths=tolerated_paths,
            )
        except Exception as exc:
            return f"Error comparing {connector}: {exc}"

    with ThreadPoolExecutor(max_workers=_COMPARE_ARTIFACT_MAX_WORKERS) as pool:
        # pool.map preserves input order (deterministic output)
        outcomes = list(pool.map(_compare_one, common))

    for outcome in outcomes:
        if isinstance(outcome, str):
            result.errors.append(outcome)
            continue

        diff = outcome
        if diff.status == "match":
            result.connectors_matching += 1
        else:
            result.connectors_differing += 1

        # Include diffs that have artifact_diffs (even matches with
        # tolerated info), but skip completely clean matches.
        if diff.artifact_diffs:
            result.connector_diffs.append(diff)

    _log_progress("Connector artifact comparison complete.")

    # Step 3: Compare global index files (if requested)
    if with_indexes:
        store_root = (
            f"{store_bucket}/{store_prefix.rstrip('/')}"
            if store_prefix
            else store_bucket
        )
        ref_root = (
            f"{reference_bucket}/{reference_prefix.rstrip('/')}"
            if reference_prefix
            else reference_bucket
        )

        _log_progress("Comparing global index files...")
        for index_file in _INDEX_FILES:
            try:
                index_diff = _compare_index_file(
                    fs, index_file, store_root, ref_root, tolerated_paths
                )
                result.index_diffs.append(index_diff)
            except Exception as exc:
                result.errors.append(f"Error comparing index {index_file}: {exc}")
    else:
        _log_progress("Skipping global index comparison (--no-indexes).")

    _log_progress(result.summary())
    return result
