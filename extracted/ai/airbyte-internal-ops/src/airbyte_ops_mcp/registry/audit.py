# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Audit registry completeness by comparing local metadata against GCS.

This module provides functionality to detect connectors whose local
`dockerImageTag` has not yet been published to the GCS registry.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from airbyte_ops_mcp.registry._constants import (
    METADATA_FILE_NAME,
    METADATA_FOLDER,
)
from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_storage_client

logger = logging.getLogger(__name__)

CONNECTOR_PATH_PREFIX = "airbyte-integrations/connectors"


@dataclass
class UnpublishedConnector:
    """A connector whose current local version is not published on GCS."""

    connector_name: str
    local_version: str


@dataclass
class AuditResult:
    """Result of auditing which connectors have unpublished versions."""

    unpublished: list[UnpublishedConnector] = field(default_factory=list)
    checked_count: int = 0
    skipped_archived: list[str] = field(default_factory=list)
    skipped_rc: list[str] = field(default_factory=list)
    skipped_disabled: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _read_local_metadata(metadata_path: Path) -> dict[str, Any] | None:
    """Read and parse a local metadata.yaml file.

    Returns None if the file doesn't exist or can't be parsed.
    """
    if not metadata_path.exists():
        return None
    try:
        return yaml.safe_load(metadata_path.read_text())
    except Exception:
        return None


def _is_archived(metadata: dict[str, Any]) -> bool:
    """Check if a connector is archived based on its metadata."""
    data = metadata.get("data", {})
    support_level = data.get("supportLevel", "")
    return support_level == "archived"


def _is_rc_version(version: str) -> bool:
    """Check if a version string looks like a release candidate."""
    return "rc" in version.lower()


def _is_disabled_on_all_registries(metadata: dict[str, Any]) -> bool:
    """Check if a connector is disabled on all registries.

    A connector is considered disabled if every entry present in
    `registryOverrides` has `enabled: false`.  Only the entries that
    exist are inspected — if a registry key is omitted entirely it is
    not counted.  Connectors without any `registryOverrides` section
    are assumed enabled (the default) and return `False`.
    """
    data = metadata.get("data", {})
    overrides = data.get("registryOverrides", {})
    if not overrides:
        return False
    return all(entry.get("enabled") is False for entry in overrides.values())


def find_unpublished_connectors(
    repo_path: str | Path,
    bucket_name: str,
    connector_names: list[str] | None = None,
) -> AuditResult:
    """Find connectors whose local version is not published on GCS.

    For each connector in the local checkout, reads `dockerImageTag` from
    `metadata.yaml` and checks whether `metadata/<docker-repo>/<version>/metadata.yaml`
    exists in the GCS bucket.  Connectors that are archived, disabled on all
    registries, or have RC versions are skipped.

    Args:
        repo_path: Path to the Airbyte monorepo checkout.
        bucket_name: GCS bucket name to check against.
        connector_names: Optional list of connector names to check.
            If `None`, discovers all connectors in the repo.

    Returns:
        An `AuditResult` containing unpublished connectors and metadata.
    """
    repo_path = Path(repo_path)
    connectors_dir = repo_path / CONNECTOR_PATH_PREFIX

    if not connectors_dir.exists():
        raise ValueError(f"Connectors directory not found: {connectors_dir}")

    # Discover connector names if not provided
    if connector_names is None:
        connector_names = sorted(
            d.name
            for d in connectors_dir.iterdir()
            if d.is_dir() and (d / METADATA_FILE_NAME).exists()
        )

    result = AuditResult()

    # Collect connectors and their versions first, then batch-check GCS
    to_check: list[tuple[str, str]] = []  # (connector_name, version)

    for name in connector_names:
        metadata_path = connectors_dir / name / METADATA_FILE_NAME
        metadata = _read_local_metadata(metadata_path)
        if metadata is None:
            result.errors.append(f"{name}: metadata.yaml not found or unreadable")
            continue

        if _is_archived(metadata):
            result.skipped_archived.append(name)
            continue

        if _is_disabled_on_all_registries(metadata):
            result.skipped_disabled.append(name)
            continue

        data = metadata.get("data", {})
        version = data.get("dockerImageTag")
        if not version:
            result.errors.append(f"{name}: no dockerImageTag in metadata")
            continue

        if _is_rc_version(version):
            result.skipped_rc.append(name)
            continue

        to_check.append((name, version))

    if not to_check:
        result.checked_count = 0
        return result

    # Check GCS for each connector version
    storage_client = get_gcs_storage_client()
    bucket = storage_client.bucket(bucket_name)

    for name, version in to_check:
        result.checked_count += 1
        blob_path = f"{METADATA_FOLDER}/airbyte/{name}/{version}/{METADATA_FILE_NAME}"
        blob = bucket.blob(blob_path)

        try:
            exists = blob.exists()
        except Exception as e:
            result.errors.append(f"{name}: GCS check failed: {e}")
            continue

        if not exists:
            logger.info(
                "Unpublished: %s version %s (checked %s)",
                name,
                version,
                blob_path,
            )
            result.unpublished.append(
                UnpublishedConnector(connector_name=name, local_version=version)
            )

    logger.info(
        "Audit complete: %d checked, %d unpublished, %d archived-skipped, %d disabled-skipped, %d rc-skipped",
        result.checked_count,
        len(result.unpublished),
        len(result.skipped_archived),
        len(result.skipped_disabled),
        len(result.skipped_rc),
    )

    return result


def generate_connector_list_summary(
    connectors: list[str],
    *,
    assert_none: bool = False,
    unpublished: bool = False,
    audit_result: AuditResult | None = None,
) -> str:
    """Generate a markdown summary for the connector list command."""
    count = len(connectors)

    # 1. Header: label depends on mode, icon depends on assertion result
    label = "unpublished connector version(s)" if unpublished else "connector(s)"
    if assert_none:
        icon = "✅" if count == 0 else "⚠️"
        header = f"## {icon} {count} {label} found"
    else:
        header = f"## {count} {label} found"

    lines: list[str] = [header, ""]

    # 2. Connector list: table (if we have version info) or bullet list
    max_listed = 50
    if count > 0 and audit_result and audit_result.unpublished:
        version_map = {
            e.connector_name: e.local_version for e in audit_result.unpublished
        }
        lines.extend(["| Connector | Local Version |", "|-----------|---------------|"])
        for name in connectors:
            lines.append(f"| `{name}` | `{version_map.get(name, '-')}` |")
    elif count > 0:
        for name in connectors[:max_listed]:
            lines.append(f"- `{name}`")
        if count > max_listed:
            lines.append(f"\n*... and {count - max_listed} more (truncated).*")

    # 3. Audit details (collapsible) when available
    if audit_result:
        lines.extend(
            [
                "",
                "<details>",
                "<summary>Audit Details</summary>",
                "",
                f"- **Checked:** {audit_result.checked_count}",
                f"- **Unpublished:** {len(audit_result.unpublished)}",
                f"- **Archived (skipped):** {len(audit_result.skipped_archived)}",
                f"- **Disabled (skipped):** {len(audit_result.skipped_disabled)}",
                f"- **RC versions (skipped):** {len(audit_result.skipped_rc)}",
            ]
        )
        if audit_result.errors:
            lines.append(f"- **Warnings:** {len(audit_result.errors)}")
            for err in audit_result.errors:
                lines.append(f"  - {err}")
        lines.extend(["", "</details>"])

    return "\n".join(lines)
