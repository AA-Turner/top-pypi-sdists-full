# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Local generation of connector version artifacts.

This module provides functions to generate the complete set of artifacts for a
connector version, including registry entries (`cloud.json` / `oss.json`)
produced by running `docker run ... spec` against the connector image.

The generated artifacts are written to a local output directory and are **not**
uploaded to GCS.  Use the `artifacts publish` CLI command for uploading.

Artifacts produced
------------------
* `metadata.yaml` -- enriched copy with git info, components SHA, and SBOM URL.
* `icon.svg`      -- copied from the connector code directory.
* `cloud.json`    -- registry entry for the *cloud* registry.
* `oss.json`      -- registry entry for the *oss* registry.
* `spdx.json`     -- SPDX SBOM generated from the connector Docker image.

* `doc.md`                    -- connector documentation (from repo docs tree).
* `manifest.yaml`             -- manifest-only connector manifest (if present).
* `components.zip`             -- zipped Python components for manifest connectors.
* `components.zip.sha256`       -- SHA-256 of `components.zip`.
"""

from __future__ import annotations

import base64
import copy
import datetime as dt
import hashlib
import json
import logging
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import git as gitpython
import requests
import yaml

from airbyte_ops_mcp.registry._constants import (
    COMPONENTS_PY_FILE_NAME,
    COMPONENTS_ZIP_FILE_NAME,
    COMPONENTS_ZIP_SHA256_FILE_NAME,
    CONNECTOR_DEPENDENCY_FILE_NAME,
    DOC_FILE_NAME,
    MANIFEST_FILE_NAME,
    SBOM_FILE_NAME,
    VALID_REGISTRIES,
)
from airbyte_ops_mcp.registry._gcs_helpers import (
    get_gcs_storage_client,
    safe_read_gcs_file,
)
from airbyte_ops_mcp.registry._python_deps_analysis import (
    _is_python_connector,
    extract_cdk_version_from_dependencies,
    generate_python_dependencies_file,
)
from airbyte_ops_mcp.registry._resolve_gcs_paths import (
    dependencies_blob_path,
    prod_icon_cdn_url,
    prod_sbom_cdn_url,
    versioned_file_blob_path,
)
from airbyte_ops_mcp.registry._sbom_generation import generate_sbom
from airbyte_ops_mcp.registry.store import RegistryStore
from airbyte_ops_mcp.registry.validate import (
    ValidateOptions,
    validate_metadata,
)

logger = logging.getLogger(__name__)


def _json_serial(obj: object) -> str:
    """JSON serializer for objects not serializable by default json code.

    YAML parsers auto-convert bare date-like values (e.g. `releaseDate: 2021-07-08`)
    into `datetime.date` or `datetime.datetime` objects.  The stdlib `json.dumps`
    cannot handle these, so we convert them to ISO-format strings here.
    """
    if isinstance(obj, (dt.datetime, dt.date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _get_registry_override(
    metadata_data: dict[str, Any],
    registry_type: str,
) -> dict[str, Any]:
    """Return registry overrides, or an empty dictionary when none exist."""
    registry_overrides = metadata_data.get("registryOverrides", {})
    if not isinstance(registry_overrides, dict):
        return {}

    override = registry_overrides.get(registry_type, {})
    if not isinstance(override, dict):
        return {}
    return override


def is_registry_enabled(
    metadata_data: dict[str, Any],
    registry_type: str,
) -> bool:
    """Return whether a connector should be present in a registry.

    Missing `registryOverrides` means enabled by default. A connector is
    excluded only when the matching registry explicitly sets `enabled: false`.
    """
    override: dict[str, Any] = _get_registry_override(metadata_data, registry_type)
    return override.get("enabled", True) is not False


# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------


@dataclass
class GenerateResult:
    """Result of a local artifact generation run."""

    connector_name: str
    version: str
    docker_image: str
    output_dir: str
    artifacts_written: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    validation_errors: list[str] = field(default_factory=list)
    dry_run: bool = False

    @property
    def success(self) -> bool:
        return len(self.errors) == 0 and len(self.validation_errors) == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "connector_name": self.connector_name,
            "version": self.version,
            "docker_image": self.docker_image,
            "output_dir": self.output_dir,
            "artifacts_written": self.artifacts_written,
            "errors": self.errors,
            "validation_errors": self.validation_errors,
            "dry_run": self.dry_run,
            "success": self.success,
        }


# ---------------------------------------------------------------------------
# Docker spec helpers
# ---------------------------------------------------------------------------


def _run_docker_spec(docker_image: str, deployment_mode: str) -> dict[str, Any]:
    """Run `docker run --rm -e DEPLOYMENT_MODE=<mode> <image> spec`.

    Args:
        docker_image: Fully qualified image (e.g. `airbyte/source-faker:1.2.3`).
        deployment_mode: `"cloud"` or `"oss"`.

    Returns:
        The parsed spec JSON object.

    Raises:
        RuntimeError: If the docker command fails or the output cannot be parsed.
    """
    cmd = [
        "docker",
        "run",
        "--rm",
        "-e",
        f"DEPLOYMENT_MODE={deployment_mode}",
        docker_image,
        "spec",
    ]
    logger.info("Running: %s", " ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"docker spec ({deployment_mode}) failed with exit code {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    # The connector outputs one JSON object per line (Airbyte protocol messages).
    # The spec message has type == "SPEC".
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        if isinstance(msg, dict) and msg.get("type") == "SPEC":
            spec_data = msg.get("spec")
            if spec_data is not None:
                return spec_data

    raise RuntimeError(
        f"No SPEC message found in docker output for {docker_image} "
        f"(mode={deployment_mode}).  stdout={result.stdout[:500]}"
    )


# ---------------------------------------------------------------------------
# Registry entry transformation  (ported from legacy registry_entry.py)
# ---------------------------------------------------------------------------


def _apply_overrides_from_registry(
    metadata_data: dict[str, Any],
    registry_type: str,
    *,
    skip_docker_image_tag: bool = True,
) -> dict[str, Any]:
    """Apply registryOverrides for *registry_type* and return a new dict.

    This mirrors the legacy `_apply_overrides_from_registry` function.

    Args:
        metadata_data: The raw `metadata.data` dict.
        registry_type: `"cloud"` or `"oss"`.
        skip_docker_image_tag: If *True* (default), skip applying a
            `dockerImageTag` override.  This should be *True* for versioned
            entries (the version being published) and *False* for `latest/`
            entries which should reflect the overridden/pinned version.
    """
    data = copy.deepcopy(metadata_data)
    overrides = _get_registry_override(data, registry_type)

    # Remove the "enabled" key -- it's a control flag, not a data field.
    overrides.pop("enabled", None)

    # Remove None values.
    overrides = {k: v for k, v in overrides.items() if v is not None}

    # For versioned entries, do NOT apply dockerImageTag overrides -- the
    # version being published should keep its own tag.
    if skip_docker_image_tag:
        overrides.pop("dockerImageTag", None)

    data.update(overrides)
    return data


def _apply_package_info_fields(
    metadata_data: dict[str, Any],
    store: RegistryStore,
    local_dependencies: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Look up CDK dependency info and return a `packageInfo` dict.

    When `local_dependencies` is provided (i.e. we just generated
    `dependencies.json` locally), the CDK version is extracted from it
    directly — avoiding a GCS round-trip.  Otherwise falls back to reading
    the per-version `dependencies.json` blob from GCS (legacy behaviour).

    Args:
        metadata_data: The `metadata.data` dict (needs `dockerRepository`
            and `dockerImageTag`).
        store: Parsed store target used for GCS dependency blob lookups.
        local_dependencies: Optional locally-generated dependencies dict
            (as returned by `generate_python_dependencies_file`).

    Returns:
        A dict suitable for the `packageInfo` field in the registry entry,
        or an empty dict if the dependency blob is not found.
    """
    package_info: dict[str, Any] = dict(metadata_data.get("packageInfo") or {})

    # --- Fast path: use locally-generated dependencies ---
    if local_dependencies is not None:
        cdk_version = extract_cdk_version_from_dependencies(local_dependencies)
        package_info["cdk_version"] = cdk_version
        if cdk_version is not None:
            logger.info("Found CDK version from local dependencies: %s", cdk_version)
        return package_info

    # --- Slow path: look up from GCS ---
    docker_repo = metadata_data.get("dockerRepository", "")
    connector_name = docker_repo.replace("airbyte/", "")
    connector_version = metadata_data.get("dockerImageTag", "")

    if not connector_name or not connector_version:
        return {}

    dependencies_path = dependencies_blob_path(
        connector_name=connector_name, version=connector_version, store=store
    )

    logger.info(
        "Looking up dependencies blob for %s %s at %s",
        connector_name,
        connector_version,
        dependencies_path,
    )

    try:
        storage_client = get_gcs_storage_client()
    except (ValueError, Exception) as exc:
        logger.info("GCS credentials unavailable, skipping packageInfo lookup: %s", exc)
        return package_info

    bucket = storage_client.bucket(store.bucket)
    blob = bucket.blob(dependencies_path)
    blob_contents = safe_read_gcs_file(blob)

    if blob_contents is not None:
        dependencies_json = json.loads(blob_contents)
        cdk_version = extract_cdk_version_from_dependencies(dependencies_json)
        package_info["cdk_version"] = cdk_version
        logger.info("Found CDK version: %s", cdk_version)
    else:
        logger.info("No dependencies blob found at %s", dependencies_path)

    return package_info


def _build_registry_entry(
    metadata_data: dict[str, Any],
    registry_type: str,
    spec: dict[str, Any],
    *,
    store: RegistryStore | None = None,
    local_dependencies: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Transform raw `metadata.data` into a registry entry (`cloud.json` / `oss.json`).

    This is a port of the legacy `_apply_metadata_overrides` pipeline in
    `registry_entry.py`, including generated-field population and package-info
    enrichment.

    Args:
        metadata_data: The raw `metadata.data` dict.
        registry_type: `"cloud"` or `"oss"`.
        spec: The parsed connector spec dict.
        store: Parsed store target for dependency lookups (defaults to prod).
    """
    if store is None:
        store = RegistryStore.parse("coral:prod")
    entry = _apply_overrides_from_registry(metadata_data, registry_type)

    # --- Remove fields not needed in the registry entry ---
    entry.pop("registryOverrides", None)
    connector_type: str = entry.pop("connectorType", "source")

    # --- Rename connectorSubtype -> sourceType ---
    connector_subtype = entry.pop("connectorSubtype", None)
    if connector_subtype:
        entry["sourceType"] = connector_subtype

    # --- Rename definitionId -> sourceDefinitionId / destinationDefinitionId ---
    definition_id = entry.pop("definitionId", None)
    if definition_id:
        id_field = (
            "sourceDefinitionId"
            if connector_type == "source"
            else "destinationDefinitionId"
        )
        entry[id_field] = definition_id

    # --- Standard boilerplate fields ---
    entry["tombstone"] = False
    entry["custom"] = False
    # `public` may have been supplied by `registryOverrides.<registry>.public`.
    # Connectors are public unless the metadata explicitly opts out.
    entry.setdefault("public", True)

    # --- Capability flags (match legacy Pydantic model defaults) ---
    entry.setdefault("supportsDataActivation", False)
    if connector_type == "source":
        entry.setdefault("supportsFileTransfer", False)

    # --- Generated fields (full population matching legacy pipeline) ---
    docker_repo = metadata_data.get("dockerRepository", "")
    docker_tag = metadata_data.get("dockerImageTag", "")
    connector_name = docker_repo.replace("airbyte/", "")
    metadata_file_path = (
        versioned_file_blob_path(connector_name=connector_name, version=docker_tag)
        if connector_name and docker_tag
        else ""
    )

    # The legacy pipeline populated `metadata_last_modified` from the GCS blob's
    # `updated` timestamp. For simplicity (and to avoid coupling generation to GCS
    # availability), we use the current generation timestamp instead. Downstream
    # consumers don't rely on the exact timestamp source.
    now_ts = datetime.now(tz=timezone.utc).isoformat()

    generated = entry.get("generated") or {}
    generated["source_file_info"] = {
        "metadata_file_path": metadata_file_path,
        "metadata_bucket_name": store.bucket,
        "metadata_last_modified": now_ts,
        "registry_entry_generated_at": now_ts,
    }
    entry["generated"] = generated

    # --- iconUrl (deterministic CDN path) ---
    entry["iconUrl"] = prod_icon_cdn_url(connector_name=connector_name)

    # --- packageInfo (use local dependencies if available, else GCS) ---
    entry["packageInfo"] = _apply_package_info_fields(
        metadata_data, store, local_dependencies=local_dependencies
    )

    # --- Language field ---
    if not entry.get("language"):
        tags = entry.get("tags", [])
        languages = [
            tag.replace("language:", "") for tag in tags if tag.startswith("language:")
        ]
        entry["language"] = languages[0] if languages else None

    # --- ab_internal defaults (match legacy Pydantic model defaults) ---
    default_ab_internal: dict[str, Any] = {
        "sl": 100,
        "ql": 100,
        "isEnterprise": False,
        "requireVersionIncrementsInPullRequests": True,
    }
    existing_ab_internal = entry.get("ab_internal") or {}
    entry["ab_internal"] = {**default_ab_internal, **existing_ab_internal}

    # --- supportLevel default ---
    if not entry.get("supportLevel"):
        entry["supportLevel"] = "community"

    # --- Releases / breaking changes ---
    entry["releases"] = _build_releases(entry)

    # --- Inject the spec ---
    entry["spec"] = spec

    return entry


def _build_releases(metadata: dict[str, Any]) -> dict[str, Any]:
    """Build the `releases` field for the registry entry.

    Ported from legacy `_apply_connector_releases`.
    """
    documentation_url = metadata.get("documentationUrl", "")
    releases_input = metadata.get("releases")
    result: dict[str, Any] = {}

    if releases_input is None:
        return result

    breaking_changes = releases_input.get("breakingChanges")
    if breaking_changes:
        base_url = f"{documentation_url}-migrations"
        result["migrationDocumentationUrl"] = releases_input.get(
            "migrationDocumentationUrl", base_url
        )
        for version, bc in breaking_changes.items():
            if "migrationDocumentationUrl" not in bc:
                bc["migrationDocumentationUrl"] = f"{base_url}#{version}"
        result["breakingChanges"] = breaking_changes

    rollout_config = releases_input.get("rolloutConfiguration")
    if rollout_config:
        # Apply defaults matching the legacy pipeline's Pydantic model
        default_rollout: dict[str, Any] = {
            "enableProgressiveRollout": False,
            "advanceDelayMinutes": 10,
            "initialPercentage": 0,
            "maxPercentage": 50,
        }
        result["rolloutConfiguration"] = {**default_rollout, **rollout_config}

    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def _resolve_doc_path(
    metadata_data: dict[str, Any],
    repo_root: Path,
) -> Path | None:
    """Derive the local `doc.md` path from the `documentationUrl` in metadata.

    The convention (matching the legacy pipeline) is:

        documentationUrl = "https://docs.airbyte.com/integrations/sources/faker"
        -> repo_root / "docs/integrations/sources/faker.md"
    """
    documentation_url: str = metadata_data.get("documentationUrl", "")
    if not documentation_url:
        return None

    base = "https://docs.airbyte.com/"
    if base not in documentation_url:
        return None

    relative = documentation_url.replace(base, "").strip("/")
    return repo_root / "docs" / f"{relative}.md"


def _create_components_zip(
    manifest_path: Path,
    components_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    """Create `components.zip` containing *manifest.yaml* and *components.py*.

    Returns:
        Tuple of (zip_path, sha256_path).
    """
    zip_path = output_dir / COMPONENTS_ZIP_FILE_NAME
    sha256_path = output_dir / COMPONENTS_ZIP_SHA256_FILE_NAME

    with zipfile.ZipFile(zip_path, "w") as zf:
        for file_path in (components_path, manifest_path):
            if file_path.exists():
                zf.write(filename=file_path, arcname=file_path.name)

    # Compute SHA-256
    sha256_hash = hashlib.sha256()
    with zip_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    sha256_b64 = base64.b64encode(sha256_hash.digest()).decode("utf8")
    sha256_path.write_text(sha256_b64)

    return zip_path, sha256_path


# ---------------------------------------------------------------------------
# Metadata enrichment helpers
# ---------------------------------------------------------------------------


def _get_git_info_for_file(file_path: Path) -> dict[str, str] | None:
    """Return git commit metadata for the last commit that touched *file_path*.

    Returns a dict with keys `commit_sha`, `commit_timestamp`,
    `commit_author`, `commit_author_email`, or *None* on failure.
    """
    try:
        repo = gitpython.Repo(file_path.parent, search_parent_directories=True)
        sha = repo.git.log("-1", "--format=%H", str(file_path))
        if not sha:
            logger.warning(
                "No git history for %s (file may be uncommitted).", file_path
            )
            return None
        commit = repo.commit(sha)
        return {
            "commit_sha": commit.hexsha,
            "commit_timestamp": commit.authored_datetime.isoformat(),
            "commit_author": commit.author.name,
            "commit_author_email": commit.author.email,
        }
    except (gitpython.exc.InvalidGitRepositoryError, gitpython.exc.GitCommandError):
        logger.warning("Could not retrieve git info for %s.", file_path)
        return None


def _enrich_metadata_git_info(
    metadata: dict[str, Any],
    metadata_file: Path,
) -> dict[str, Any]:
    """Inject `data.generated.git` into the metadata dict."""
    git_info = _get_git_info_for_file(metadata_file)
    if git_info:
        generated = metadata.setdefault("data", {}).setdefault("generated", {})
        generated["git"] = git_info
        logger.info("Enriched metadata with git info: %s", git_info["commit_sha"][:8])
    return metadata


def _enrich_metadata_components_sha(
    metadata: dict[str, Any],
    components_sha256: str | None,
) -> dict[str, Any]:
    """Inject `data.generated.pythonComponents` into the metadata dict."""
    if components_sha256:
        generated = metadata.setdefault("data", {}).setdefault("generated", {})
        generated["pythonComponents"] = {
            "required": True,
            "sha256": components_sha256,
        }
        logger.info("Enriched metadata with components SHA256.")
    return metadata


def _enrich_metadata_sbom_url(
    metadata: dict[str, Any],
    sbom_generated: bool = False,
) -> dict[str, Any]:
    """Inject `data.generated.sbomUrl` into the metadata dict.

    When `sbom_generated` is `True` the SBOM was generated locally and will
    be uploaded alongside the other artifacts, so we can set the URL
    unconditionally.  Otherwise we fall back to an HTTP HEAD check against the
    CDN (legacy behaviour).
    """
    data = metadata.get("data", {})
    docker_repo = data.get("dockerRepository", "")
    docker_tag = data.get("dockerImageTag", "")
    if not docker_repo or not docker_tag:
        return metadata

    connector_name = docker_repo.replace("airbyte/", "")
    sbom_url = prod_sbom_cdn_url(connector_name=connector_name, version=docker_tag)

    if sbom_generated:
        generated = metadata.setdefault("data", {}).setdefault("generated", {})
        generated["sbomUrl"] = sbom_url
        logger.info("Enriched metadata with SBOM URL.")
        return metadata

    # Fallback: check whether the SBOM already exists on the CDN.
    try:
        response = requests.head(sbom_url, timeout=10)
        if response.ok:
            generated = metadata.setdefault("data", {}).setdefault("generated", {})
            generated["sbomUrl"] = sbom_url
            logger.info("Enriched metadata with SBOM URL.")
    except requests.RequestException:
        logger.warning("Could not check SBOM URL: %s", sbom_url)
    return metadata


def generate_version_artifacts(
    metadata_file: Path,
    docker_image: str,
    output_dir: Path | None = None,
    repo_root: Path | None = None,
    dry_run: bool = False,
    with_validate: bool = True,
    with_dependency_dump: bool = True,
    with_sbom: bool = True,
) -> GenerateResult:
    """Generate all version artifacts for a connector release.

    Artifacts are enriched with git commit info, SBOM URL, and (when applicable)
    components SHA before writing.  Validation is run after generation by default.

    Args:
        metadata_file: Path to the connector's `metadata.yaml`.
        docker_image: Docker image to run spec against (e.g. `airbyte/source-faker:6.2.38`).
        output_dir: Directory to write artifacts to.  If `None`, a temp directory is created.
        repo_root: Root of the Airbyte repo checkout (for resolving `doc.md`).
            If `None`, inferred by walking up from `metadata_file`.
        dry_run: If `True`, report what would be generated without writing or running docker.
        with_validate: If `True` (default), run metadata validators after generation.
            Pass `False` (`--no-validate`) to skip.
        with_dependency_dump: If `True` (default), generate `dependencies.json`
            for Python connectors.  Pass `False` (`--no-dependency-dump`) to skip.
        with_sbom: If `True` (default), generate `spdx.json` (SBOM) for
            connectors.  Pass `False` (`--no-sbom`) to skip.

    Returns:
        A `GenerateResult` describing what was produced.
    """
    # --- Load metadata ---
    if not metadata_file.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")

    raw_metadata: dict[str, Any] = yaml.safe_load(metadata_file.read_text())
    metadata_data: dict[str, Any] = raw_metadata.get("data", {})

    connector_name = metadata_data.get("dockerRepository", "unknown").replace(
        "airbyte/", ""
    )
    version = metadata_data.get("dockerImageTag", "unknown")

    # --- Resolve output directory ---
    if output_dir is None:
        output_dir = Path(
            tempfile.mkdtemp(prefix=f"connector-artifacts-{connector_name}-{version}-")
        )
    output_dir.mkdir(parents=True, exist_ok=True)

    result = GenerateResult(
        connector_name=connector_name,
        version=version,
        docker_image=docker_image,
        output_dir=str(output_dir),
        dry_run=dry_run,
    )

    if dry_run:
        logger.info("[DRY RUN] Would generate artifacts to %s", output_dir)
        result.artifacts_written = [
            "metadata.yaml",
            "icon.svg",
            "doc.md",
            "cloud.json",
            "oss.json",
            "manifest.yaml (if present)",
            "components.zip (if components.py present)",
            "components.zip.sha256 (if components.py present)",
            f"version={version}",
        ]
        if with_sbom:
            result.artifacts_written.append(SBOM_FILE_NAME)
        if with_dependency_dump:
            result.artifacts_written.append("dependencies.json (if Python connector)")
        return result

    # --- Prepare metadata output ---
    metadata_out = output_dir / "metadata.yaml"
    result.artifacts_written.append("metadata.yaml")

    # --- Enrich metadata with git info *before* building registry entries so
    #     that `generated.git` propagates into `cloud.json` / `oss.json`. ---
    raw_metadata = _enrich_metadata_git_info(raw_metadata, metadata_file)

    # --- Generate SBOM from the connector Docker image ---
    sbom_generated = False
    if not with_sbom:
        logger.info("SBOM generation disabled via --no-sbom.")
    else:
        try:
            sbom_path = generate_sbom(docker_image, output_dir)
        except RuntimeError as exc:
            logger.warning("SBOM generation failed (non-fatal): %s", exc)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("Docker not available or SBOM generation timed out.")
        else:
            result.artifacts_written.append(SBOM_FILE_NAME)
            sbom_generated = True
            logger.info("Generated SBOM: %s", sbom_path)

    # --- Enrich metadata with SBOM URL ---
    raw_metadata = _enrich_metadata_sbom_url(
        raw_metadata, sbom_generated=sbom_generated
    )

    # --- Run docker spec for cloud and oss ---
    specs: dict[str, dict[str, Any]] = {}
    for mode in VALID_REGISTRIES:
        try:
            specs[mode] = _run_docker_spec(docker_image, mode)
            logger.info("Got %s spec from docker image %s", mode, docker_image)
        except RuntimeError as exc:
            error_msg = f"Failed to get {mode} spec: {exc}"
            logger.error(error_msg)
            result.errors.append(error_msg)

    # --- Generate dependencies.json for Python connectors ---
    # This must happen *before* building registry entries so that the
    # local dependencies data can be used for packageInfo without a GCS
    # round-trip.
    local_dependencies: dict[str, Any] | None = None
    if not with_dependency_dump:
        logger.info("Dependency generation disabled via --no-dependency-dump.")
    elif _is_python_connector(metadata_data):
        logger.info("Python connector detected — generating dependencies.json")
        local_dependencies = generate_python_dependencies_file(
            metadata_data=metadata_data,
            docker_image=docker_image,
            output_dir=output_dir,
        )
        if local_dependencies is not None:
            result.artifacts_written.append(CONNECTOR_DEPENDENCY_FILE_NAME)
    else:
        logger.info(
            "Non-Python connector (%s) — skipping dependencies.json generation.",
            connector_name,
        )

    # --- Generate registry entries (cloud.json, oss.json) ---
    for registry_type in VALID_REGISTRIES:
        if not is_registry_enabled(metadata_data, registry_type):
            logger.info(
                "Registry type %s is not enabled for %s, skipping %s.json generation.",
                registry_type,
                connector_name,
                registry_type,
            )
            continue

        spec = specs.get(registry_type)
        if spec is None:
            error_msg = (
                f"Cannot generate {registry_type}.json: no spec available "
                f"(docker spec for {registry_type} failed or was not run)."
            )
            result.errors.append(error_msg)
            continue

        registry_entry = _build_registry_entry(
            metadata_data,
            registry_type,
            spec,
            local_dependencies=local_dependencies,
        )

        out_path = output_dir / f"{registry_type}.json"
        out_path.write_text(
            json.dumps(registry_entry, indent=2, sort_keys=True, default=_json_serial)
            + "\n"
        )
        result.artifacts_written.append(f"{registry_type}.json")
        logger.info("Wrote %s", out_path)

    # --- Copy icon.svg (sibling of metadata.yaml in the connector directory) ---
    icon_source = metadata_file.parent / "icon.svg"
    if icon_source.is_file():
        icon_out = output_dir / "icon.svg"
        shutil.copy2(icon_source, icon_out)
        result.artifacts_written.append("icon.svg")
        logger.info("Wrote %s", icon_out)
    else:
        logger.warning("No icon.svg found at %s.", icon_source)
        result.errors.append("Icon file is missing.")

    # --- Copy doc.md (derived from documentationUrl in metadata) ---
    if repo_root is None:
        # Infer repo root by walking up from metadata_file looking for .git
        # Note: .git can be a directory (normal clone) or a file (git worktree)
        # Resolve to absolute path first so the walk-up works with relative paths.
        candidate = metadata_file.resolve().parent
        while candidate != candidate.parent:
            git_indicator = candidate / ".git"
            if git_indicator.is_dir() or git_indicator.is_file():
                repo_root = candidate
                break
            candidate = candidate.parent

    if repo_root is not None:
        doc_source = _resolve_doc_path(metadata_data, repo_root)
        if doc_source is not None and doc_source.is_file():
            doc_out = output_dir / DOC_FILE_NAME
            shutil.copy2(doc_source, doc_out)
            result.artifacts_written.append(DOC_FILE_NAME)
            logger.info("Wrote %s (from %s)", doc_out, doc_source)
        else:
            error_msg = (
                f"Documentation file not found: {doc_source}. "
                f"Derived from documentationUrl in metadata."
            )
            logger.error(error_msg)
            result.errors.append(error_msg)
    else:
        error_msg = "Cannot resolve doc.md: repo root not found."
        logger.error(error_msg)
        result.errors.append(error_msg)

    # --- Copy manifest.yaml (from connector root, if present) ---
    connector_dir = metadata_file.parent
    manifest_source = connector_dir / MANIFEST_FILE_NAME
    components_sha256: str | None = None
    if manifest_source.is_file():
        manifest_out = output_dir / MANIFEST_FILE_NAME
        shutil.copy2(manifest_source, manifest_out)
        result.artifacts_written.append(MANIFEST_FILE_NAME)
        logger.info("Wrote %s", manifest_out)

        # --- Generate components.zip if components.py exists ---
        components_source = connector_dir / COMPONENTS_PY_FILE_NAME
        if components_source.is_file():
            zip_path, sha256_path = _create_components_zip(
                manifest_path=manifest_source,
                components_path=components_source,
                output_dir=output_dir,
            )
            result.artifacts_written.append(COMPONENTS_ZIP_FILE_NAME)
            result.artifacts_written.append(COMPONENTS_ZIP_SHA256_FILE_NAME)
            logger.info("Wrote %s and %s", zip_path, sha256_path)
            # Read back the SHA256 for metadata enrichment
            components_sha256 = sha256_path.read_text().strip()
    else:
        logger.info(
            "No manifest.yaml at %s — skipping manifest artifacts.", manifest_source
        )

    # --- Enrich metadata with components SHA (after zip creation) ---
    raw_metadata = _enrich_metadata_components_sha(raw_metadata, components_sha256)

    # --- Write final enriched metadata.yaml ---
    # Use sort_keys=True to match the legacy pipeline's alphabetical key ordering.
    # After Registry 2.0 launches we are free to change the key ordering.
    metadata_out.write_text(
        yaml.dump(raw_metadata, default_flow_style=False, sort_keys=True)
    )
    logger.info("Wrote enriched %s", metadata_out)

    # --- Write version marker file (version=<semver>) ---
    # This zero-byte file is used by the compile step as a fast-check marker.
    # Including it in the generated artifacts means `latest/` gets the marker
    # for free via a recursive copy, removing the need for a separate write.
    marker_file = output_dir / f"version={version}"
    marker_file.write_bytes(b"")
    result.artifacts_written.append(f"version={version}")
    logger.info("Wrote version marker %s", marker_file)

    # --- Validate metadata (after generation) ---
    if with_validate:
        logger.info("Running post-generation validation...")
        doc_path: str | None = None
        if repo_root is not None:
            resolved = _resolve_doc_path(metadata_data, repo_root)
            doc_path = str(resolved) if resolved else None
        validation = validate_metadata(
            metadata_data=metadata_data,
            opts=ValidateOptions(docs_path=doc_path),
        )
        if not validation.passed:
            for err in validation.errors:
                logger.error("Validation error: %s", err)
            result.validation_errors = validation.errors
        else:
            logger.info("Validation passed (%d validators).", validation.validators_run)

    return result
