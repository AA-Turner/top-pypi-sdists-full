"""Shared organization/workspace search tool for the Ops Webapp.

Provides a single search implementation that both the Connector Version Manager
and Customer Billing pages can register on their respective FastMCPApp instances.
"""

from __future__ import annotations

import logging

from airbyte_ops_mcp.prod_db_access.queries import (
    search_organizations,
    search_workspaces,
)
from pydantic import BaseModel, Field

from airbyte_ops_webapp.state import mock_only_enabled

logger = logging.getLogger(__name__)


class OrgSearchRow(BaseModel):
    """A single DataTable-bound org/workspace search result row."""

    entity_type: str
    entity_id: str
    entity_name: str
    entity_email: str
    organization_id: str
    workspace_id: str
    display_label: str


class OrgSearchResult(BaseModel):
    """Typed result of an org/workspace search.

    `results` is the DataTable-bound row list (one row per matched org or
    workspace).
    """

    results: list[OrgSearchRow] = Field(default_factory=list)
    error: str = ""


_MOCK_ORGANIZATIONS: list[dict[str, str]] = [
    {
        "organization_id": "00000000-0000-0000-0000-000000000001",
        "organization_name": "Acme Corp",
        "email": "admin@acme.io",
    },
    {
        "organization_id": "00000000-0000-0000-0000-000000000002",
        "organization_name": "MotherDuck",
        "email": "ops@motherduck.com",
    },
    {
        "organization_id": "00000000-0000-0000-0000-000000000003",
        "organization_name": "Airbyte",
        "email": "admin@airbyte.io",
    },
    {
        "organization_id": "00000000-0000-0000-0000-000000000004",
        "organization_name": "Dataflow Labs",
        "email": "team@dataflowlabs.dev",
    },
]

_MOCK_WORKSPACES: list[dict[str, str]] = [
    {
        "organization_id": "00000000-0000-0000-0000-000000000001",
        "workspace_id": "aaaaaaaa-0000-0000-0000-000000000001",
        "workspace_name": "Acme Production",
        "email": "eng@acme.io",
    },
    {
        "organization_id": "00000000-0000-0000-0000-000000000001",
        "workspace_id": "aaaaaaaa-0000-0000-0000-000000000002",
        "workspace_name": "Acme Staging",
        "email": "staging@acme.io",
    },
    {
        "organization_id": "00000000-0000-0000-0000-000000000002",
        "workspace_id": "bbbbbbbb-0000-0000-0000-000000000001",
        "workspace_name": "MotherDuck Analytics",
        "email": "analytics@motherduck.com",
    },
    {
        "organization_id": "00000000-0000-0000-0000-000000000003",
        "workspace_id": "cccccccc-0000-0000-0000-000000000001",
        "workspace_name": "Airbyte Cloud Dogfood",
        "email": "dogfood@airbyte.io",
    },
    {
        "organization_id": "00000000-0000-0000-0000-000000000004",
        "workspace_id": "dddddddd-0000-0000-0000-000000000001",
        "workspace_name": "Dataflow Labs Dev",
        "email": "dev@dataflowlabs.dev",
    },
]

# A large demo customer with many workspaces. Enough rows that a search for
# "motherduck" overflows the results view, exercising the scroll + sticky-header
# behavior of the org lookup modal (and any other table) in mock mode.
_MOCK_WORKSPACES += [
    {
        "organization_id": "00000000-0000-0000-0000-000000000002",
        "workspace_id": f"eeeeeeee-0000-0000-0000-{i:012d}",
        "workspace_name": f"MotherDuck Team {i:02d}",
        "email": f"team{i:02d}@motherduck.com",
    }
    for i in range(1, 31)
]


def _mock_search(query: str) -> OrgSearchResult:
    """Return mock results for org/workspace search in mock mode."""
    q = query.strip().lower()
    results: list[OrgSearchRow] = []
    for org in _MOCK_ORGANIZATIONS:
        name = org.get("organization_name", "")
        email = org.get("email", "")
        if q in name.lower() or q in email.lower():
            org_id = org["organization_id"]
            label_parts = ["[Org]", name]
            if email:
                label_parts.append(f"({email})")
            results.append(
                OrgSearchRow(
                    entity_type="organization",
                    entity_id=org_id,
                    entity_name=name,
                    entity_email=email,
                    organization_id=org_id,
                    workspace_id="",
                    display_label=" ".join(label_parts),
                )
            )
    for ws in _MOCK_WORKSPACES:
        name = ws.get("workspace_name", "")
        email = ws.get("email", "")
        if q in name.lower() or q in email.lower():
            ws_id = ws["workspace_id"]
            label_parts = ["[WS]", name]
            if email:
                label_parts.append(f"({email})")
            results.append(
                OrgSearchRow(
                    entity_type="workspace",
                    entity_id=ws_id,
                    entity_name=name,
                    entity_email=email,
                    organization_id=ws["organization_id"],
                    workspace_id=ws_id,
                    display_label=" ".join(label_parts),
                )
            )
    return OrgSearchResult(results=results)


def search_organizations_and_workspaces(
    query: str,
    limit: int = 20,
) -> OrgSearchResult:
    """Search organizations and workspaces by name (case-insensitive substring match).

    Searches across organization name/email and workspace name/slug.
    Returns a list of matching results with entity type, ID, name, and org ID.
    """
    if not query.strip():
        return OrgSearchResult(error="Please enter a search term.")

    if mock_only_enabled():
        return _mock_search(query)

    try:
        org_rows = search_organizations(name_contains=query, limit=limit)
        ws_rows = search_workspaces(name_contains=query, limit=limit)
    except Exception:
        logger.exception("Organization/workspace search failed for query: %s", query)
        return OrgSearchResult(error="Search failed. Prod DB may be unavailable.")

    results: list[OrgSearchRow] = []
    for row in org_rows:
        org_id = str(row["organization_id"])
        name = row.get("organization_name") or ""
        email = row.get("email") or ""
        label_parts = ["[Org]", name]
        if email:
            label_parts.append(f"({email})")
        results.append(
            OrgSearchRow(
                entity_type="organization",
                entity_id=org_id,
                entity_name=name,
                entity_email=email,
                organization_id=org_id,
                workspace_id="",
                display_label=" ".join(label_parts),
            )
        )
    for row in ws_rows:
        ws_id = str(row["workspace_id"])
        name = row.get("workspace_name") or ""
        email = row.get("email") or ""
        label_parts = ["[WS]", name]
        if email:
            label_parts.append(f"({email})")
        results.append(
            OrgSearchRow(
                entity_type="workspace",
                entity_id=ws_id,
                entity_name=name,
                entity_email=email,
                organization_id=str(row["organization_id"])
                if row.get("organization_id")
                else "",
                workspace_id=ws_id,
                display_label=" ".join(label_parts),
            )
        )

    return OrgSearchResult(results=results)
