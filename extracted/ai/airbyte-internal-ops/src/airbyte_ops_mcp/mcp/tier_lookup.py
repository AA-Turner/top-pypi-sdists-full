# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for customer tier lookup and cache management.

Provides tools to resolve customer tiers for organizations, workspaces, and connections,
and to manage the tier cache.

## MCP reference

.. include:: ../../../docs/mcp-generated/tier_lookup.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.prod_db_access.queries import query_connection_workspace_details
from airbyte_ops_mcp.tier_cache import (
    CustomerTier,
    TierCacheStats,
    TierSummary,
    build_tier_summary,
    get_cache_stats,
    get_org_tier,
    get_org_tiers,
    refresh_tier_cache,
    resolve_workspaces,
)

# =============================================================================
# Pydantic Models for MCP Tool Responses
# =============================================================================


class TierLookupEntry(BaseModel):
    """A single resolved tier entry for an org, workspace, or connection."""

    input_id: str = Field(description="The original ID that was looked up")
    input_type: str = Field(
        description="Type of the input ID: 'organization', 'workspace', or 'connection'"
    )
    organization_id: str | None = Field(
        default=None, description="Resolved organization UUID"
    )
    workspace_id: str | None = Field(
        default=None,
        description="Workspace UUID (if input was workspace or connection)",
    )
    connection_id: str | None = Field(
        default=None, description="Connection UUID (if input was connection)"
    )
    customer_tier: CustomerTier = Field(
        description="Resolved tier: TIER_0, TIER_1, or TIER_2"
    )
    dataplane_name: str | None = Field(
        default=None, description="Dataplane region name (e.g., 'US', 'EU')"
    )
    is_eu: bool = Field(
        default=False, description="Whether the entity is in the EU region"
    )
    resolved: bool = Field(
        default=True, description="Whether the ID was successfully resolved"
    )


class TierLookupResult(BaseModel):
    """Result of a customer tier lookup across multiple IDs."""

    entries: list[TierLookupEntry] = Field(
        description="Individual tier lookup results for each input ID"
    )
    summary: TierSummary = Field(
        description="Tier distribution summary across all resolved entries"
    )
    summary_text: str = Field(description="Human-readable tier distribution summary")


class TierCacheRefreshResult(BaseModel):
    """Result of refreshing the tier cache."""

    stats: TierCacheStats = Field(description="Cache statistics after refresh")
    message: str = Field(description="Human-readable result message")


# =============================================================================
# MCP Tools
# =============================================================================


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def lookup_customer_tiers(
    organization_ids: Annotated[
        list[str] | None,
        Field(
            description=(
                "List of organization UUIDs to look up tiers for. "
                "Example: ['664c690e-5263-49ba-b01f-4a6759b3330a']"
            ),
            default=None,
        ),
    ] = None,
    workspace_ids: Annotated[
        list[str] | None,
        Field(
            description=(
                "List of workspace UUIDs to look up tiers for. "
                "Each workspace will be resolved to its organization and tier. "
                "Example: ['266ebdfe-0d7b-4540-9817-de7e4505ba61']"
            ),
            default=None,
        ),
    ] = None,
    connection_ids: Annotated[
        list[str] | None,
        Field(
            description=(
                "List of connection UUIDs to look up tiers for. "
                "Each connection will be resolved to its workspace, organization, and tier."
            ),
            default=None,
        ),
    ] = None,
) -> TierLookupResult:
    """Look up customer tier classification for organizations, workspaces, and/or connections.

    Accepts mixed lists of organization IDs, workspace IDs, and connection IDs.
    Resolves each to its organization and maps to a customer tier (TIER_0, TIER_1, or TIER_2).

    Tier 0 and Tier 1 orgs are explicitly tracked in Salesforce and cached from BigQuery.
    Any org not in the cache defaults to TIER_2.

    Returns enriched entries with tier, region (EU/US), and a summary of the distribution.
    """
    entries: list[TierLookupEntry] = []

    # Resolve organization IDs directly
    org_ids = organization_ids or []
    if org_ids:
        org_results = get_org_tiers(org_ids)
        for result in org_results:
            entries.append(
                TierLookupEntry(
                    input_id=result.organization_id,
                    input_type="organization",
                    organization_id=result.organization_id,
                    customer_tier=result.customer_tier,
                    resolved=True,
                )
            )

    # Resolve workspace IDs -> org -> tier
    ws_ids = workspace_ids or []
    if ws_ids:
        ws_results = resolve_workspaces(ws_ids)
        for result in ws_results:
            entries.append(
                TierLookupEntry(
                    input_id=result.workspace_id,
                    input_type="workspace",
                    organization_id=result.organization_id,
                    workspace_id=result.workspace_id,
                    customer_tier=result.customer_tier,
                    dataplane_name=result.dataplane_name,
                    is_eu=result.is_eu,
                    resolved=result.resolved,
                )
            )

    # Resolve connection IDs -> workspace -> org -> tier
    conn_ids = connection_ids or []
    if conn_ids:
        conn_details = query_connection_workspace_details(conn_ids)
        conn_map: dict[str, dict[str, Any]] = {
            str(row["connection_id"]): row for row in conn_details
        }

        for conn_id in conn_ids:
            row = conn_map.get(conn_id)
            if row is None:
                entries.append(
                    TierLookupEntry(
                        input_id=conn_id,
                        input_type="connection",
                        connection_id=conn_id,
                        customer_tier="TIER_2",
                        resolved=False,
                    )
                )
                continue

            org_id = str(row["organization_id"])
            dataplane_name = row.get("dataplane_name") or "US"
            org_result = get_org_tier(org_id)

            entries.append(
                TierLookupEntry(
                    input_id=conn_id,
                    input_type="connection",
                    organization_id=org_id,
                    workspace_id=str(row["workspace_id"]),
                    connection_id=conn_id,
                    customer_tier=org_result.customer_tier,
                    dataplane_name=dataplane_name,
                    is_eu=dataplane_name == "EU",
                    resolved=True,
                )
            )

    # Build summary from enriched entries
    summary_rows = [{"customer_tier": e.customer_tier} for e in entries if e.resolved]
    summary = build_tier_summary(summary_rows)

    return TierLookupResult(
        entries=entries,
        summary=summary,
        summary_text=str(summary),
    )


@mcp_tool(
    read_only=False,
    idempotent=True,
)
def refresh_customer_tier_cache() -> TierCacheRefreshResult:
    """Force-refresh the customer tier cache from BigQuery.

    The tier cache is automatically refreshed every 24 hours. Use this tool to
    manually trigger a refresh if you need the latest tier data immediately
    (e.g., after a Salesforce update).

    Returns cache statistics after the refresh.
    """
    stats = refresh_tier_cache()
    return TierCacheRefreshResult(
        stats=stats,
        message=(
            f"Tier cache refreshed: {stats.tier_cache_size} orgs cached, "
            f"{stats.workspace_cache_size} workspaces cached."
        ),
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def get_customer_tier_cache_stats() -> TierCacheStats:
    """Get current statistics about the customer tier cache.

    Returns cache size, age, and file paths for both the tier cache
    (org -> tier) and workspace cache (workspace -> org + region).

    Useful for checking cache freshness and diagnosing issues.
    """
    return get_cache_stats()


def register_tier_lookup_tools(app: FastMCP) -> None:
    """Register tier lookup tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
