# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Disk-cached customer tier resolution for Airbyte Cloud organizations and workspaces.

This module provides a two-layer disk cache for resolving customer tiers:

1. **Org tier cache** (`tier_cache.json`): Maps `organization_id` to `customer_tier`.
   Bulk-fetched from BigQuery (`airbyte_warehouse_reporting.sales_customer_attributes`).
   Contains only Tier 0 and Tier 1 orgs (approximately 288 rows). Any org not in the cache
   defaults to `TIER_2`. Refreshed every 24 hours.

2. **Workspace-org cache** (`workspace_org_cache.json`): Maps `workspace_id` to
   `{organization_id, dataplane_name}`. Lazy-populated on first lookup miss from the
   Prod DB Replica, then served from disk. Same 24-hour TTL.

Public API:
- `get_org_tier()` / `get_org_tiers()` — resolve org(s) to tier
- `resolve_workspace()` / `resolve_workspaces()` — resolve workspace(s) to org + tier
- `enrich_rows_by_org()` — add `customer_tier` and `is_eu` to result rows
- `filter_rows_by_tier()` — client-side tier filtering
- `refresh_tier_cache()` — force-refresh the BigQuery tier cache
- `get_cache_stats()` — cache freshness and size info
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import google.auth.credentials
from google.cloud import bigquery
from pydantic import BaseModel, Field

from airbyte_ops_mcp.gcp_auth import get_gcp_credentials_for_bigquery_ro
from airbyte_ops_mcp.prod_db_access.queries import query_workspace_info

logger = logging.getLogger(__name__)


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

# BigQuery source for tier data
BIGQUERY_PROJECT = "airbyte-data-prod"
BIGQUERY_TIER_QUERY = """
SELECT
    organization_id,
    customer_tier
FROM `airbyte-data-prod.airbyte_warehouse_reporting.sales_customer_attributes`
WHERE organization_id IS NOT NULL
  AND organization_id != 'No Organization Id'
  AND customer_tier IN ('Tier 0', 'Tier 1')
"""

# Mapping from BigQuery tier values to rollout tier values (lowercase keys for case-insensitive lookup)
_BQ_TIER_TO_ROLLOUT_TIER: dict[str, CustomerTier] = {
    "tier 0": "TIER_0",
    "tier 1": "TIER_1",
    "tier 2": "TIER_2",
}

# Default tier for orgs not in the cache
DEFAULT_TIER: CustomerTier = "TIER_2"


def _resolve_bq_tier(bq_tier_value: str) -> CustomerTier:
    """Resolve a BigQuery tier string to a normalized CustomerTier value.

    Case-insensitive lookup. Logs a warning and defaults to TIER_2 for unknown values.
    """
    resolved = _BQ_TIER_TO_ROLLOUT_TIER.get(bq_tier_value.lower().strip())
    if resolved is not None:
        return resolved
    logger.warning(
        "Unknown tier value '%s' from BigQuery — defaulting to %s",
        bq_tier_value,
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
# Tier Cache (BigQuery -> disk)
# =============================================================================


def _fetch_tier_data_from_bigquery(
    credentials: google.auth.credentials.Credentials | None = None,
) -> dict[str, dict[str, str]]:
    """Fetch org -> tier mappings from BigQuery.

    Returns a dict of `{org_id: {"customer_tier": "Tier 0"}}`.
    Only includes Tier 0 and Tier 1 orgs (Tier 2 is the default).
    """
    if credentials is None:
        credentials = get_gcp_credentials_for_bigquery_ro()
    client = bigquery.Client(project=BIGQUERY_PROJECT, credentials=credentials)
    query_job = client.query(BIGQUERY_TIER_QUERY)
    results = query_job.result()

    tier_data: dict[str, dict[str, str]] = {}
    for row in results:
        org_id = row.organization_id
        tier = row.customer_tier
        if org_id and tier:
            tier_data[str(org_id)] = {"customer_tier": str(tier)}

    logger.info("Fetched %d tier entries from BigQuery", len(tier_data))
    return tier_data


def _load_tier_cache(
    *,
    force_refresh: bool = False,
    credentials: google.auth.credentials.Credentials | None = None,
) -> dict[str, dict[str, str]]:
    """Load the org tier cache, refreshing from BigQuery if stale or missing.

    Args:
        force_refresh: If True, bypass TTL check and refresh from BigQuery.
        credentials: Optional GCP credentials for BigQuery. Falls back to default.

    Returns:
        Dict mapping org_id to `{"customer_tier": "Tier 0"}`.
    """
    if not force_refresh:
        data, fetched_at = _read_cache_file(TIER_CACHE_FILE)
        if data is not None and _is_cache_fresh(fetched_at):
            logger.debug("Tier cache is fresh (%d entries)", len(data))
            return data  # type: ignore[return-value]

    # Fetch fresh data from BigQuery — hard-fail if unavailable
    tier_data = _fetch_tier_data_from_bigquery(credentials=credentials)
    if not tier_data:
        raise RuntimeError(
            "BigQuery tier query returned no rows. Cannot proceed without tier data. "
            "Check BigQuery access and the sales_customer_attributes table."
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
        return data  # type: ignore[return-value]
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

    Loads the tier cache (refreshing from BigQuery if stale), looks up the org,
    and returns the tier. Orgs not in the cache default to TIER_2.

    Args:
        organization_id: The organization ID to look up.
        credentials: Optional GCP credentials for BigQuery refresh. Falls back to default.
    """
    tier_cache = _load_tier_cache(credentials=credentials)
    entry = tier_cache.get(organization_id)
    if entry is not None:
        bq_tier = entry.get("customer_tier", "")
        return OrgTierResult(
            organization_id=organization_id,
            customer_tier=_resolve_bq_tier(bq_tier),
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
            bq_tier = entry.get("customer_tier", "")
            results.append(
                OrgTierResult(
                    organization_id=org_id,
                    customer_tier=_resolve_bq_tier(bq_tier),
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


def resolve_workspace(workspace_id: str) -> WorkspaceResolution:
    """Resolve a workspace to its organization, tier, and region.

    Uses the workspace cache (lazy-populated from Prod DB) and tier cache.
    """
    ws_cache = _load_workspace_cache()
    tier_cache = _load_tier_cache()

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
        bq_tier = tier_entry.get("customer_tier", "")
        customer_tier = _resolve_bq_tier(bq_tier)
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
            bq_tier = tier_entry.get("customer_tier", "")
            customer_tier = _resolve_bq_tier(bq_tier)
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
) -> list[dict[str, Any]]:
    """Add `customer_tier` and `is_eu` fields to each row based on organization_id.

    Uses the org tier cache to resolve tiers. Each row must have an `organization_id`
    field (or the field specified by `org_id_key`). If the row already has a
    `dataplane_name` field, `is_eu` is derived from it; otherwise defaults to False.

    This mutates and returns the same list (no copy).
    """
    tier_cache = _load_tier_cache()

    for row in rows:
        org_id = str(row.get(org_id_key, ""))
        tier_entry = tier_cache.get(org_id)
        if tier_entry is not None:
            bq_tier = tier_entry.get("customer_tier", "")
            row["customer_tier"] = _resolve_bq_tier(bq_tier)
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


# =============================================================================
# Public API: Cache Management
# =============================================================================


def refresh_tier_cache() -> TierCacheStats:
    """Force-refresh the tier cache from BigQuery and return stats."""
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
