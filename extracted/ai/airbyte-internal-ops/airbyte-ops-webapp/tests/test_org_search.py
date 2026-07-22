"""Tests for the shared organization/workspace search component.

Covers the `organization_label` field that lets a caller (e.g. the Organization
Pins tab) show the resolved parent-organization label for a workspace hit
instead of the workspace's own label.
"""

from __future__ import annotations

import pytest

from airbyte_ops_webapp import state as state_module
from airbyte_ops_webapp.pages.shared_components.org_search import (
    search_organizations_and_workspaces,
)


@pytest.fixture(autouse=True)
def _mock_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force mock mode so the search uses the curated fixtures."""
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")


def test_org_hit_resolves_organization_label() -> None:
    """An organization hit carries its own name as the resolved org label."""
    rows = search_organizations_and_workspaces("Acme Corp").results
    org_rows = [r for r in rows if r.entity_type == "organization"]
    assert org_rows, "expected an organization hit for 'Acme Corp'"
    row = org_rows[0]
    assert row.organization_id == row.entity_id
    assert row.organization_label == "[Org] Acme Corp"


def test_workspace_hit_resolves_parent_organization_label() -> None:
    """A workspace hit resolves `organization_label` to the parent org, not the workspace."""
    rows = search_organizations_and_workspaces("Acme Production").results
    ws_rows = [r for r in rows if r.entity_type == "workspace"]
    assert ws_rows, "expected a workspace hit for 'Acme Production'"
    row = ws_rows[0]
    # The clicked entity + its display label are the workspace...
    assert row.workspace_id == row.entity_id
    assert "Acme Production" in row.display_label
    # ...but the resolved org label points at the parent organization.
    assert row.organization_id == "00000000-0000-0000-0000-000000000001"
    assert row.organization_label == "[Org] Acme Corp"
