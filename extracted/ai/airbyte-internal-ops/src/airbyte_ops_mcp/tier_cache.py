# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Disk-cached customer tier resolution for Airbyte Cloud organizations and workspaces.

This module provides a two-layer disk cache for resolving customer tiers:

1. **Org tier cache** (`tier_cache.json`): Maps `organization_id` to `customer_tier`.
   Bulk-loaded from the platform's GCS export of `sales_customer_attributes`
   (the newest `.jsonl` under `gs://airbyte_warehouse_exports/data/sales_customer_attributes/`,
   the same dump the platform backend reads). Contains only Tier 0 and Tier 1 orgs
   (approximately 288 rows). Any org not in the cache defaults to `TIER_2`.
   Refreshed every 24 hours.

2. **Workspace-org cache** (`workspace_org_cache.json`): Maps `workspace_id` to
   `{organization_id, dataplane_name}`. Lazy-populated on first lookup miss from the
   Prod DB Replica, then served from disk. Same 24-hour TTL.

Public API:
- `get_org_tier()` / `get_org_tiers()` — resolve org(s) to tier
- `resolve_workspace()` / `resolve_workspaces()` — resolve workspace(s) to org + tier
- `enrich_rows_by_org()` — add `customer_tier` and `is_eu` to result rows
- `filter_rows_by_tier()` — client-side tier filtering
- `refresh_tier_cache()` — force-refresh the tier cache from the GCS export
- `get_cache_stats()` — cache freshness and size info
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, cast

import google.auth.credentials
from google.api_core.exceptions import GoogleAPICallError
from google.auth.exceptions import GoogleAuthError
from google.cloud import storage
from pydantic import BaseModel, Field

from airbyte_ops_mcp.gcp_auth import (
    _get_identity_from_credentials,
    get_gcp_credentials_for_tier_gcs_ro,
)
from airbyte_ops_mcp.prod_db_access.queries import query_workspace_info

logger = logging.getLogger(__name__)

# Type aliases for cache data structures
TierData = dict[str, dict[str, str]]
WorkspaceData = dict[str, dict[str, str]]


# Type alias for customer tier values
CustomerTier = Literal["TIER_0", "TIER_1", "TIER_2"]

# Type alias for tier filter values (includes ALL for no filtering)
TierFilter = Literal["TIER_0", "TIER_1", "TIER_2", "ALL"]

# Cache configuration
CACHE_DIR = Path(
    os.environ.get("AIRBYTE_OPS_CACHE_DIR", "~/.cache/airbyte-ops-mcp")
).expanduser()
TIER_CACHE_FILE = CACHE_DIR / "tier_cache.json"
WORKSPACE_CACHE_FILE = CACHE_DIR / "workspace_org_cache.json"
CACHE_TTL_SECONDS = 24 * 60 * 60  # 24 hours

# GCS source for tier data — the platform's `sales_customer_attributes` export.
# Defaults match the prod backend config; env vars mirror the platform's
# `GCS_AIRBYTE_WAREHOUSE_EXPORTS_*` / `GCS_DATA_SALES_CUSTOMER_ATTRIBUTES_*` names.
TIER_EXPORT_PROJECT = os.environ.get(
    "GCS_AIRBYTE_WAREHOUSE_EXPORTS_PROJECT_ID", "prod-ab-cloud-proj"
)
TIER_EXPORT_BUCKET = os.environ.get(
    "GCS_AIRBYTE_WAREHOUSE_EXPORTS_BUCKET_NAME", "airbyte_warehouse_exports"
)
TIER_EXPORT_PREFIX = os.environ.get(
    "GCS_DATA_SALES_CUSTOMER_ATTRIBUTES_OBJECT_PREFIX", "data/sales_customer_attributes"
)

# Sentinel values the export uses for rows with no resolved org/tier.
_NO_ORGANIZATION_ID = "No Organization Id"
_NO_CUSTOMER_TIER = "No Customer Tier"

# Only Tier 0 and Tier 1 orgs are cached (Tier 2 is the default for cache misses).
_CACHED_TIER_VALUES = frozenset({"tier 0", "tier 1"})

# Mapping from raw tier strings to rollout tier values (lowercase keys for case-insensitive lookup)
_TIER_VALUE_TO_ROLLOUT_TIER: dict[str, CustomerTier] = {
    "tier 0": "TIER_0",
    "tier 1": "TIER_1",
    "tier 2": "TIER_2",
}

# Default tier for orgs not in the cache
DEFAULT_TIER: CustomerTier = "TIER_2"


def _resolve_tier_value(tier_value: str) -> CustomerTier:
    """Resolve a raw customer-tier string to a normalized CustomerTier value.

    Case-insensitive lookup. Logs a warning and defaults to TIER_2 for unknown values.
    """
    resolved = _TIER_VALUE_TO_ROLLOUT_TIER.get(tier_value.lower().strip())
    if resolved is not None:
        return resolved
    logger.warning(
        "Unknown tier value '%s' from tier export — defaulting to %s",
        tier_value,
        DEFAULT_TIER,
    )
    return DEFAULT_TIER


# =============================================================================
# Pydantic Models
# =============================================================================


class OrgTierEntry(BaseModel):
    """Cached entry for an organization's customer tier."""

    customer_tier: str = Field(
        description="Customer tier value (e.g., 'Tier 0', 'Tier 1')"
    )


class WorkspaceOrgEntry(BaseModel):
    """Cached entry mapping a workspace to its organization and region."""

    organization_id: str = Field(description="The organization UUID")
    dataplane_name: str = Field(
        default="US",
        description="Dataplane region name (e.g., 'US', 'EU', 'US-Central')",
    )


class OrgTierResult(BaseModel):
    """Result of resolving an organization's customer tier."""

    organization_id: str = Field(description="The organization UUID")
    customer_tier: CustomerTier = Field(
        description="Resolved tier: TIER_0, TIER_1, or TIER_2"
    )
    is_in_cache: bool = Field(
        description="Whether this org was found in the tier cache (False means defaulted to TIER_2)"
    )


class WorkspaceResolution(BaseModel):
    """Result of resolving a workspace to its organization, tier, and region."""

    workspace_id: str = Field(description="The workspace UUID")
    organization_id: str | None = Field(
        default=None,
        description="The resolved organization UUID (None if workspace not found)",
    )
    customer_tier: CustomerTier = Field(
        default="TIER_2", description="Resolved tier: TIER_0, TIER_1, or TIER_2"
    )
    dataplane_name: str | None = Field(
        default=None, description="Dataplane region name (e.g., 'US', 'EU')"
    )
    is_eu: bool = Field(
        default=False, description="Whether the workspace is in the EU region"
    )
    resolved: bool = Field(
        default=False, description="Whether the workspace was successfully resolved"
    )


class TierCacheStats(BaseModel):
    """Statistics about the tier cache state."""

    tier_cache_size: int = Field(description="Number of orgs in the tier cache")
    workspace_cache_size: int = Field(
        description="Number of workspaces in the workspace cache"
    )
    tier_cache_age_seconds: float | None = Field(
        default=None,
        description="Age of the tier cache in seconds (None if not cached)",
    )
    workspace_cache_age_seconds: float | None = Field(
        default=None,
        description="Age of the workspace cache in seconds (None if not cached)",
    )
    tier_cache_path: str = Field(description="Path to the tier cache file")
    workspace_cache_path: str = Field(description="Path to the workspace cache file")


class TierSummary(BaseModel):
    """Summary of tier distribution across a set of results."""

    tier_0_count: int = Field(default=0, description="Number of TIER_0 entries")
    tier_1_count: int = Field(default=0, description="Number of TIER_1 entries")
    tier_2_count: int = Field(default=0, description="Number of TIER_2 entries")
    total: int = Field(default=0, description="Total number of entries")

    def __str__(self) -> str:
        """Return a human-readable summary string."""
        return (
            f"{self.tier_0_count} TIER_0, {self.tier_1_count} TIER_1, "
            f"{self.tier_2_count} TIER_2 (total: {self.total})"
        )


# =============================================================================
# Cache I/O Helpers
# =============================================================================


def _ensure_cache_dir() -> None:
    """Create the cache directory if it does not exist."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _read_cache_file(path: Path) -> tuple[dict[str, Any] | None, float | None]:
    """Read a cache file and return (data, fetched_at_timestamp).

    Returns `(None, None)` if the file does not exist, is unreadable, or is malformed.
    """
    if not path.exists():
        return None, None
    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        logger.warning("Cache file %s is corrupt or unreadable, ignoring", path.name)
        return None, None
    fetched_at = raw.get("fetched_at")
    data = raw.get("data")
    if not isinstance(data, dict) or not isinstance(fetched_at, (int, float)):
        return None, None
    return data, float(fetched_at)


def _write_cache_file(path: Path, data: dict[str, Any]) -> None:
    """Write data to a cache file with a `fetched_at` timestamp."""
    _ensure_cache_dir()
    payload = {
        "fetched_at": datetime.now(timezone.utc).timestamp(),
        "data": data,
    }
    path.write_text(json.dumps(payload, indent=2, default=str))
    logger.info("Wrote cache file %s (%d entries)", path.name, len(data))


def _is_cache_fresh(fetched_at: float | None) -> bool:
    """Return True if the cache was fetched within the TTL window."""
    if fetched_at is None:
        return False
    age = datetime.now(timezone.utc).timestamp() - fetched_at
    return age < CACHE_TTL_SECONDS


# =============================================================================
# Tier Cache (GCS export -> disk)
# =============================================================================


def _extract_export_timestamp(blob_name: str) -> int:
    """Extract the export timestamp embedded in a tier-export `.jsonl` file name.

    Mirrors the platform backend's selection logic
    (`OrganizationCustomerAttributesServiceDataImpl.extractTimestamp`): split the
    *full* object name on `_` and take index `5` (0-based). The
    `data/sales_customer_attributes/` prefix contributes two underscores, and
    the export basename is `YYYY_MM_DD_<epoch_ms>_<part>.jsonl`, so for
    `data/sales_customer_attributes/2024_11_24_1732490206044_0.jsonl` the parts
    are `[data/sales, customer, attributes/2024, 11, 24, 1732490206044, 0.jsonl]`
    and index `5` (`1732490206044`) is the epoch-ms timestamp. Returns `0` when
    that field is missing or non-numeric, so unparseable names sort oldest.
    """
    timestamp_part = blob_name.split("_")
    if len(timestamp_part) <= 5:
        return 0
    try:
        return int(timestamp_part[5])
    except ValueError:
        logger.warning(
            "Failed to extract timestamp from tier-export name: %s", blob_name
        )
        return 0


def _parse_tier_export_line(line: str) -> tuple[str, str] | None:
    """Parse one `.jsonl` line into `(organization_id, customer_tier)`.

    Reads the `_airbyte_data.organization_id` / `_airbyte_data.customer_tier`
    fields the export writes. Returns `None` for blank lines, rows missing
    either field, or the export's sentinel (`No Organization Id` /
    `No Customer Tier`) rows.

    Raises `json.JSONDecodeError` on a malformed line. The caller treats that
    as a hard failure rather than silently skipping the row: a dropped line
    could omit a Tier 0/1 org, silently degrading it to the `TIER_2` default
    and bypassing tier protection.
    """
    if not line.strip():
        return None
    record = json.loads(line)
    airbyte_data = record.get("_airbyte_data")
    if not isinstance(airbyte_data, dict):
        return None
    org_id = airbyte_data.get("organization_id")
    tier = airbyte_data.get("customer_tier")
    if not org_id or not tier:
        return None
    if org_id == _NO_ORGANIZATION_ID or tier == _NO_CUSTOMER_TIER:
        return None
    return str(org_id), str(tier)


def _fetch_tier_data_from_gcs(
    credentials: google.auth.credentials.Credentials | None = None,
) -> dict[str, dict[str, str]]:
    """Fetch org -> tier mappings from the platform's GCS export.

    Reads the newest `.jsonl` under
    `gs://{TIER_EXPORT_BUCKET}/{TIER_EXPORT_PREFIX}/` (selected by the timestamp
    embedded in the file name, mirroring the platform backend), and returns a
    dict of `{org_id: {"customer_tier": "Tier 0"}}`. Only Tier 0 and Tier 1
    orgs are kept (Tier 2 is the default for cache misses).

    Returns an empty dict when the export prefix contains no `.jsonl` file (the
    caller hard-fails on an empty result). Raises `RuntimeError` on a malformed
    line rather than serving a partial tier map.
    """
    if credentials is None:
        credentials = get_gcp_credentials_for_tier_gcs_ro()
    client = storage.Client(project=TIER_EXPORT_PROJECT, credentials=credentials)
    blobs = [
        blob
        for blob in client.list_blobs(TIER_EXPORT_BUCKET, prefix=TIER_EXPORT_PREFIX)
        if blob.name.endswith(".jsonl")
    ]
    if not blobs:
        logger.warning(
            "No .jsonl tier export found in gs://%s/%s",
            TIER_EXPORT_BUCKET,
            TIER_EXPORT_PREFIX,
        )
        return {}

    most_recent = max(blobs, key=lambda blob: _extract_export_timestamp(blob.name))
    logger.info("Reading tier export gs://%s/%s", TIER_EXPORT_BUCKET, most_recent.name)

    tier_data: dict[str, dict[str, str]] = {}
    content = most_recent.download_as_text()
    for line_number, line in enumerate(content.splitlines(), start=1):
        try:
            parsed = _parse_tier_export_line(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Malformed JSON on line {line_number} of tier export "
                f"gs://{TIER_EXPORT_BUCKET}/{most_recent.name}: {exc}. "
                f"Refusing to serve a partial tier map (would bypass tier protection)."
            ) from exc
        if parsed is None:
            continue
        org_id, tier = parsed
        if tier.lower().strip() in _CACHED_TIER_VALUES:
            tier_data[org_id] = {"customer_tier": tier}

    logger.info("Loaded %d tier entries from GCS export", len(tier_data))
    return tier_data


def _load_tier_cache(
    *,
    force_refresh: bool = False,
    credentials: google.auth.credentials.Credentials | None = None,
) -> dict[str, dict[str, str]]:
    """Load the org tier cache, refreshing from the GCS export if stale or missing.

    `force_refresh` bypasses the TTL check and reloads from GCS. `credentials`
    are optional GCP credentials for the export bucket; falls back to the
    default identity. Returns a dict mapping org_id to `{"customer_tier": "Tier 0"}`.

    A failed GCS refresh — auth failure, listing/download error, an empty
    export, or a malformed line — is a **hard failure** and raises
    `RuntimeError`. It deliberately does *not* fall back to a stale cache:
    masking a broken tier source would let a Tier 0/1 org silently degrade to
    the `TIER_2` default (bypassing tier protection) and would hide a
    service-account access regression indefinitely.
    """
    if not force_refresh:
        data, fetched_at = _read_cache_file(TIER_CACHE_FILE)
        if data is not None and _is_cache_fresh(fetched_at):
            logger.debug("Tier cache is fresh (%d entries)", len(data))
            return cast(TierData, data)

    effective_credentials = credentials or get_gcp_credentials_for_tier_gcs_ro()
    identity = (
        _get_identity_from_credentials(effective_credentials) or "application_default"
    )
    try:
        tier_data = _fetch_tier_data_from_gcs(credentials=effective_credentials)
    except (GoogleAPICallError, GoogleAuthError) as exc:
        raise RuntimeError(
            f"GCS tier refresh failed. Cannot proceed without tier data "
            f"(would bypass tier protection). Identity attempted: {identity}. "
            f"Original error: {exc}"
        ) from exc
    if not tier_data:
        raise RuntimeError(
            f"GCS tier export returned no rows. Cannot proceed without tier data "
            f"(would bypass tier protection). Identity attempted: {identity}. "
            f"Check GCS access and gs://{TIER_EXPORT_BUCKET}/{TIER_EXPORT_PREFIX}."
        )
    _write_cache_file(TIER_CACHE_FILE, tier_data)
    return tier_data


# =============================================================================
# Workspace Cache (Prod DB -> disk, lazy)
# =============================================================================


def _load_workspace_cache() -> dict[str, dict[str, str]]:
    """Load the workspace-org cache from disk.

    Returns:
        Dict mapping workspace_id to `{"organization_id": "...", "dataplane_name": "..."}`.
    """
    data, fetched_at = _read_cache_file(WORKSPACE_CACHE_FILE)
    if data is not None and _is_cache_fresh(fetched_at):
        return cast(WorkspaceData, data)
    # Stale or missing — return empty; entries will be lazy-populated
    return {}


def _save_workspace_cache(cache: dict[str, dict[str, str]]) -> None:
    """Persist the workspace-org cache to disk."""
    _write_cache_file(WORKSPACE_CACHE_FILE, cache)


def _resolve_workspace_from_db(workspace_id: str) -> WorkspaceOrgEntry | None:
    """Resolve a workspace to its org and dataplane via the Prod DB Replica.

    Returns None if the workspace is not found.
    """
    info = query_workspace_info(workspace_id)
    if info is None:
        return None
    return WorkspaceOrgEntry(
        organization_id=str(info["organization_id"]),
        dataplane_name=info.get("dataplane_name") or "US",
    )


# =============================================================================
# Public API: Org Tier Resolution
# =============================================================================


def get_org_tier(
    organization_id: str,
    *,
    credentials: google.auth.credentials.Credentials | None = None,
) -> OrgTierResult:
    """Resolve a single organization's customer tier.

    Loads the tier cache (refreshing from the GCS export if stale), looks up the
    org, and returns the tier. Orgs not in the cache default to TIER_2.

    Args:
        organization_id: The organization ID to look up.
        credentials: Optional GCP credentials for the tier-export refresh. Falls back to default.
    """
    tier_cache = _load_tier_cache(credentials=credentials)
    entry = tier_cache.get(organization_id)
    if entry is not None:
        tier_value = entry.get("customer_tier", "")
        return OrgTierResult(
            organization_id=organization_id,
            customer_tier=_resolve_tier_value(tier_value),
            is_in_cache=True,
        )
    return OrgTierResult(
        organization_id=organization_id,
        customer_tier=DEFAULT_TIER,
        is_in_cache=False,
    )


def get_org_tiers(organization_ids: list[str]) -> list[OrgTierResult]:
    """Resolve customer tiers for multiple organizations in a single cache load."""
    tier_cache = _load_tier_cache()
    results: list[OrgTierResult] = []
    for org_id in organization_ids:
        entry = tier_cache.get(org_id)
        if entry is not None:
            tier_value = entry.get("customer_tier", "")
            results.append(
                OrgTierResult(
                    organization_id=org_id,
                    customer_tier=_resolve_tier_value(tier_value),
                    is_in_cache=True,
                )
            )
        else:
            results.append(
                OrgTierResult(
                    organization_id=org_id,
                    customer_tier=DEFAULT_TIER,
                    is_in_cache=False,
                )
            )
    return results


# =============================================================================
# Public API: Workspace Resolution
# =============================================================================


def resolve_workspace(
    workspace_id: str,
    *,
    credentials: google.auth.credentials.Credentials | None = None,
) -> WorkspaceResolution:
    """Resolve a workspace to its organization, tier, and region.

    Uses the workspace cache (lazy-populated from Prod DB) and tier cache.
    """
    ws_cache = _load_workspace_cache()
    tier_cache = _load_tier_cache(credentials=credentials)

    ws_entry = ws_cache.get(workspace_id)
    if ws_entry is None:
        # Cache miss — resolve from Prod DB
        db_result = _resolve_workspace_from_db(workspace_id)
        if db_result is None:
            return WorkspaceResolution(workspace_id=workspace_id, resolved=False)

        # Populate cache
        ws_entry = {
            "organization_id": db_result.organization_id,
            "dataplane_name": db_result.dataplane_name,
        }
        ws_cache[workspace_id] = ws_entry
        _save_workspace_cache(ws_cache)

    org_id = ws_entry["organization_id"]
    dataplane_name = ws_entry.get("dataplane_name", "US")

    # Resolve tier
    tier_entry = tier_cache.get(org_id)
    if tier_entry is not None:
        tier_value = tier_entry.get("customer_tier", "")
        customer_tier = _resolve_tier_value(tier_value)
    else:
        customer_tier = DEFAULT_TIER

    return WorkspaceResolution(
        workspace_id=workspace_id,
        organization_id=org_id,
        customer_tier=customer_tier,
        dataplane_name=dataplane_name,
        is_eu=dataplane_name == "EU",
        resolved=True,
    )


def resolve_workspaces(workspace_ids: list[str]) -> list[WorkspaceResolution]:
    """Resolve multiple workspaces to their organizations, tiers, and regions.

    Batches cache reads to minimize I/O.
    """
    ws_cache = _load_workspace_cache()
    tier_cache = _load_tier_cache()
    cache_updated = False

    results: list[WorkspaceResolution] = []
    for ws_id in workspace_ids:
        ws_entry = ws_cache.get(ws_id)
        if ws_entry is None:
            # Cache miss — resolve from Prod DB
            db_result = _resolve_workspace_from_db(ws_id)
            if db_result is None:
                results.append(WorkspaceResolution(workspace_id=ws_id, resolved=False))
                continue

            ws_entry = {
                "organization_id": db_result.organization_id,
                "dataplane_name": db_result.dataplane_name,
            }
            ws_cache[ws_id] = ws_entry
            cache_updated = True

        org_id = ws_entry["organization_id"]
        dataplane_name = ws_entry.get("dataplane_name", "US")

        tier_entry = tier_cache.get(org_id)
        if tier_entry is not None:
            tier_value = tier_entry.get("customer_tier", "")
            customer_tier = _resolve_tier_value(tier_value)
        else:
            customer_tier = DEFAULT_TIER

        results.append(
            WorkspaceResolution(
                workspace_id=ws_id,
                organization_id=org_id,
                customer_tier=customer_tier,
                dataplane_name=dataplane_name,
                is_eu=dataplane_name == "EU",
                resolved=True,
            )
        )

    if cache_updated:
        _save_workspace_cache(ws_cache)

    return results


# =============================================================================
# Public API: Row Enrichment and Filtering
# =============================================================================


def enrich_rows_by_org(
    rows: list[dict[str, Any]],
    org_id_key: str = "organization_id",
    dataplane_name_key: str = "dataplane_name",
    *,
    credentials: google.auth.credentials.Credentials | None = None,
) -> list[dict[str, Any]]:
    """Add `customer_tier` and `is_eu` fields to each row based on organization_id.

    Uses the org tier cache to resolve tiers. Each row must have an `organization_id`
    field (or the field specified by `org_id_key`). If the row already has a
    `dataplane_name` field, `is_eu` is derived from it; otherwise defaults to False.

    `credentials` are optional GCP credentials used to refresh the tier cache from
    the GCS export; falls back to the default identity.

    This mutates and returns the same list (no copy).
    """
    tier_cache = _load_tier_cache(credentials=credentials)

    for row in rows:
        org_id = str(row.get(org_id_key, ""))
        tier_entry = tier_cache.get(org_id)
        if tier_entry is not None:
            tier_value = tier_entry.get("customer_tier", "")
            row["customer_tier"] = _resolve_tier_value(tier_value)
        else:
            row["customer_tier"] = DEFAULT_TIER

        dataplane_name = row.get(dataplane_name_key, "")
        row["is_eu"] = dataplane_name == "EU"

    return rows


def filter_rows_by_tier(
    rows: list[dict[str, Any]],
    tier_filter: TierFilter,
) -> list[dict[str, Any]]:
    """Filter rows by customer tier.

    Rows must already have a `customer_tier` field (from `enrich_rows_by_org`).
    If `tier_filter` is `"ALL"`, no filtering is applied.
    """
    if tier_filter == "ALL":
        return rows
    return [r for r in rows if r.get("customer_tier") == tier_filter]


def build_tier_summary(rows: list[dict[str, Any]]) -> TierSummary:
    """Build a tier distribution summary from enriched rows."""
    tier_0 = sum(1 for r in rows if r.get("customer_tier") == "TIER_0")
    tier_1 = sum(1 for r in rows if r.get("customer_tier") == "TIER_1")
    tier_2 = sum(1 for r in rows if r.get("customer_tier") == "TIER_2")
    return TierSummary(
        tier_0_count=tier_0,
        tier_1_count=tier_1,
        tier_2_count=tier_2,
        total=len(rows),
    )


def build_weighted_tier_summary(
    rows: list[dict[str, Any]],
    count_key: str,
) -> TierSummary:
    """Build a tier distribution summary weighting each row by `count_key`.

    Unlike `build_tier_summary` (which counts one per row), this sums the
    integer value at `count_key` into each tier bucket. Use it for rows that
    are already aggregated (e.g. per-organization counts) where each row
    represents more than one underlying entity. Rows must already carry a
    `customer_tier` field (from `enrich_rows_by_org`).
    """
    tier_0 = sum(
        int(r.get(count_key, 0)) for r in rows if r.get("customer_tier") == "TIER_0"
    )
    tier_1 = sum(
        int(r.get(count_key, 0)) for r in rows if r.get("customer_tier") == "TIER_1"
    )
    tier_2 = sum(
        int(r.get(count_key, 0)) for r in rows if r.get("customer_tier") == "TIER_2"
    )
    return TierSummary(
        tier_0_count=tier_0,
        tier_1_count=tier_1,
        tier_2_count=tier_2,
        total=tier_0 + tier_1 + tier_2,
    )


# =============================================================================
# Public API: Cache Management
# =============================================================================


def refresh_tier_cache() -> TierCacheStats:
    """Force-refresh the tier cache from the GCS export and return stats."""
    _load_tier_cache(force_refresh=True)
    return get_cache_stats()


def get_cache_stats() -> TierCacheStats:
    """Return current cache statistics."""
    tier_data, tier_ts = _read_cache_file(TIER_CACHE_FILE)
    ws_data, ws_ts = _read_cache_file(WORKSPACE_CACHE_FILE)

    now = datetime.now(timezone.utc).timestamp()

    return TierCacheStats(
        tier_cache_size=len(tier_data) if tier_data else 0,
        workspace_cache_size=len(ws_data) if ws_data else 0,
        tier_cache_age_seconds=(now - tier_ts) if tier_ts else None,
        workspace_cache_age_seconds=(now - ws_ts) if ws_ts else None,
        tier_cache_path=str(TIER_CACHE_FILE),
        workspace_cache_path=str(WORKSPACE_CACHE_FILE),
    )
