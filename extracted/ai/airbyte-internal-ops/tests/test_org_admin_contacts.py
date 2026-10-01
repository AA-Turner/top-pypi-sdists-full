# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for organization administrator contact lookup."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.connector_ops.rollouts.constants import CustomerTier
from airbyte_ops_mcp.mcp import prod_db_ops
from airbyte_ops_mcp.tier_cache import OrgTierResult, TierSourceHealth

_ORG_ID = "11111111-1111-1111-1111-111111111111"
_WORKSPACE_A = "22222222-2222-2222-2222-222222222222"
_WORKSPACE_B = "33333333-3333-3333-3333-333333333333"
_USER_A = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
_USER_B = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
_USER_C = "cccccccc-cccc-cccc-cccc-cccccccccccc"


@pytest.fixture(autouse=True)
def mock_org_tiers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        prod_db_ops,
        "get_org_tiers",
        lambda organization_ids, *, allow_degraded=False: [
            OrgTierResult(
                organization_id=organization_id,
                customer_tier=CustomerTier.TIER_2,
                is_in_cache=True,
            )
            for organization_id in organization_ids
        ],
    )


@pytest.mark.unit
def test_query_prod_org_admin_contacts_aggregates_admin_roles_and_activity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    activity_at = datetime(2026, 1, 2, tzinfo=timezone.utc)
    captured: dict[str, object] = {}

    def fake_tier_query(
        *, organization_ids: list[str], allow_degraded: bool
    ) -> list[OrgTierResult]:
        captured["tier_organization_ids"] = organization_ids
        captured["allow_degraded"] = allow_degraded
        return [
            OrgTierResult(
                organization_id=_ORG_ID,
                customer_tier=CustomerTier.TIER_1,
                is_in_cache=True,
                source_health=TierSourceHealth(
                    degraded=True,
                    reason="Tier export unavailable.",
                    export_age_seconds=7200,
                    export_row_count=1,
                ),
            )
        ]

    monkeypatch.setattr(prod_db_ops, "get_org_tiers", fake_tier_query)

    def fake_admin_query(
        organization_id: str, workspace_ids: list[str]
    ) -> list[dict[str, object]]:
        captured["organization_id"] = organization_id
        captured["workspace_ids"] = workspace_ids
        return [
            {
                "user_id": _USER_B,
                "user_name": "Workspace Admin",
                "user_email": "workspace@example.com",
                "user_status": "active",
                "user_created_at": activity_at,
                "user_updated_at": activity_at,
                "admin_role": "workspace_admin",
                "workspace_id": _WORKSPACE_B,
            },
            {
                "user_id": _USER_C,
                "user_name": None,
                "user_email": None,
                "user_status": "active",
                "user_created_at": activity_at,
                "user_updated_at": activity_at,
                "admin_role": "workspace_admin",
                "workspace_id": _WORKSPACE_A,
            },
            {
                "user_id": _USER_A,
                "user_name": "All Scope Admin",
                "user_email": "all@example.com",
                "user_status": "active",
                "user_created_at": activity_at,
                "user_updated_at": activity_at,
                "admin_role": "organization_admin",
                "workspace_id": None,
            },
            {
                "user_id": _USER_A,
                "user_name": "All Scope Admin",
                "user_email": "all@example.com",
                "user_status": "active",
                "user_created_at": activity_at,
                "user_updated_at": activity_at,
                "admin_role": "workspace_admin",
                "workspace_id": _WORKSPACE_B,
            },
            {
                "user_id": _USER_A,
                "user_name": "All Scope Admin",
                "user_email": "all@example.com",
                "user_status": "active",
                "user_created_at": activity_at,
                "user_updated_at": activity_at,
                "admin_role": "workspace_admin",
                "workspace_id": _WORKSPACE_A,
            },
        ]

    def fake_activity_query(
        organization_id: str, user_ids: list[str], cutoff_date: datetime
    ) -> list[dict[str, object]]:
        captured["activity_organization_id"] = organization_id
        captured["user_ids"] = user_ids
        captured["cutoff_date"] = cutoff_date
        return [
            {"user_id": _USER_A, "last_connection_event_at": activity_at},
        ]

    monkeypatch.setattr(prod_db_ops, "query_org_admin_contacts", fake_admin_query)
    monkeypatch.setattr(
        prod_db_ops,
        "query_org_user_last_connection_events",
        fake_activity_query,
    )

    result = prod_db_ops.query_prod_org_admin_contacts(
        organization_id=_ORG_ID,
        workspace_ids=[_WORKSPACE_A, _WORKSPACE_B],
        activity_lookback_days=90,
    )

    assert captured["organization_id"] == _ORG_ID
    assert captured["workspace_ids"] == [_WORKSPACE_A, _WORKSPACE_B]
    assert captured["tier_organization_ids"] == [_ORG_ID]
    assert captured["allow_degraded"] is True
    assert captured["activity_organization_id"] == _ORG_ID
    assert captured["user_ids"] == [_USER_A, _USER_B, _USER_C]
    cutoff_date = captured["cutoff_date"]
    assert isinstance(cutoff_date, datetime)
    assert cutoff_date.tzinfo == timezone.utc
    assert result.organization_id == _ORG_ID
    assert result.customer_tier == "TIER_1"
    assert result.tier_warnings == [
        "Customer tier is indeterminable: Tier export unavailable; "
        "export age: 2h old; 1 organization row. "
        "Tier classifications are not authoritative."
    ]
    assert [admin.user_id for admin in result.admins] == [_USER_A, _USER_B, _USER_C]
    assert result.admins[0].is_org_admin is True
    assert result.admins[0].admin_workspace_ids == sorted([_WORKSPACE_A, _WORKSPACE_B])
    assert result.admins[0].user_created_at == activity_at
    assert result.admins[0].user_updated_at == activity_at
    assert result.admins[0].last_connection_event_at == activity_at
    assert result.admins[1].is_org_admin is False
    assert result.admins[1].admin_workspace_ids == [_WORKSPACE_B]
    assert result.admins[1].last_connection_event_at is None
    assert result.admins[2].name is None
    assert result.admins[2].email is None
    assert result.admins[2].admin_workspace_ids == [_WORKSPACE_A]


@pytest.mark.unit
def test_query_prod_org_admin_contacts_skips_activity_without_admins(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(prod_db_ops, "query_org_admin_contacts", lambda *_args: [])

    def unexpected_activity_query(*_args: object) -> list[dict[str, object]]:
        pytest.fail("activity query should be skipped when there are no admins")

    monkeypatch.setattr(
        prod_db_ops,
        "query_org_user_last_connection_events",
        unexpected_activity_query,
    )

    result = prod_db_ops.query_prod_org_admin_contacts(organization_id=_ORG_ID)

    assert result.admins == []
    assert result.customer_tier == "TIER_2"
    assert result.tier_warnings == []


@pytest.mark.unit
def test_query_prod_org_admin_contacts_rejects_invalid_organization_uuid() -> None:
    with pytest.raises(PyAirbyteInputError, match="valid organization UUID"):
        prod_db_ops.query_prod_org_admin_contacts(organization_id="not-a-uuid")


@pytest.mark.unit
def test_query_prod_org_admin_contacts_accepts_empty_workspace_ids(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_admin_query(
        organization_id: str, workspace_ids: list[str]
    ) -> list[dict[str, object]]:
        captured["organization_id"] = organization_id
        captured["workspace_ids"] = workspace_ids
        return []

    monkeypatch.setattr(prod_db_ops, "query_org_admin_contacts", fake_admin_query)
    monkeypatch.setattr(
        prod_db_ops,
        "query_org_user_last_connection_events",
        lambda *_args: [],
    )

    result = prod_db_ops.query_prod_org_admin_contacts(
        organization_id=_ORG_ID,
        workspace_ids=[],
    )

    assert captured == {"organization_id": _ORG_ID, "workspace_ids": []}
    assert result.admins == []


@pytest.mark.unit
def test_query_prod_org_admin_contacts_rejects_invalid_workspace_uuid() -> None:
    with pytest.raises(PyAirbyteInputError, match="invalid workspace UUID"):
        prod_db_ops.query_prod_org_admin_contacts(
            organization_id=_ORG_ID,
            workspace_ids=["not-a-uuid"],
        )
