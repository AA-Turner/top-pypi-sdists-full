# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for organization `is_agentic` flag MCP tools."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.cloud_admin.models import OrganizationInfo
from airbyte_ops_mcp.cloud_admin.organization_agentic_flag import (
    set_organization_agentic_status,
)
from airbyte_ops_mcp.mcp import organization_admin
from airbyte_ops_mcp.tier_cache import OrgTierResult


def _tier_result(customer_tier: str) -> OrgTierResult:
    return OrgTierResult(
        organization_id="org-1",
        customer_tier=customer_tier,
        is_in_cache=True,
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "organization_ids,expected_ids",
    [
        pytest.param("org-1", ["org-1"], id="single_string"),
        pytest.param(["org-1", " org-2 ", "org-1"], ["org-1", "org-2"], id="list"),
        pytest.param(["", " ", "org-1"], ["org-1"], id="drops_blank_values"),
    ],
)
def test_normalize_organization_ids(
    organization_ids: str | list[str],
    expected_ids: list[str],
) -> None:
    """`_normalize_organization_ids` trims, dedupes, and accepts single/list input."""
    assert (
        organization_admin._normalize_organization_ids(organization_ids) == expected_ids
    )


@pytest.mark.unit
def test_get_organization_agentic_flag_reads_multiple_orgs_from_db(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`get_organization_agentic_flag` returns DB rows and missing IDs for a list."""
    monkeypatch.setattr(
        organization_admin,
        "query_organization_agentic_flags",
        lambda organization_ids: [
            {
                "organization_id": "org-1",
                "organization_name": "Org One",
                "email": "admin@one.example",
                "tombstone": False,
                "is_agentic": True,
            },
            {
                "organization_id": "org-2",
                "organization_name": "Org Two",
                "email": "admin@two.example",
                "tombstone": False,
                "is_agentic": False,
            },
        ],
    )
    monkeypatch.setattr(
        organization_admin,
        "get_org_tier",
        lambda organization_id, **_: _tier_result(
            "TIER_1" if organization_id == "org-1" else "TIER_2"
        ),
    )

    result = organization_admin.get_organization_agentic_flag(
        ["org-1", "org-2", "missing-org"],
        ctx=MagicMock(),
    )

    assert [org.organization_id for org in result.organizations] == ["org-1", "org-2"]
    assert [org.is_agentic for org in result.organizations] == [True, False]
    assert result.organizations[0].customer_tier == "TIER_1"
    assert result.organizations[0].tier_warning is not None
    assert result.missing_organization_ids == ["missing-org"]


@pytest.mark.unit
def test_get_organization_agentic_flag_uses_config_api_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`get_organization_agentic_flag` uses Config API when an override is passed."""
    get_org_info = MagicMock(
        return_value=OrganizationInfo.model_validate(
            {
                "organizationId": "org-1",
                "organizationName": "Org One",
                "email": "admin@one.example",
                "isAgentic": True,
            }
        )
    )
    monkeypatch.setattr(organization_admin, "_get_organization_info", get_org_info)
    monkeypatch.setattr(
        organization_admin,
        "_resolve_cloud_auth",
        lambda ctx: ("token", None, None),
    )
    monkeypatch.setattr(
        organization_admin,
        "get_org_tier",
        lambda organization_id, **_: _tier_result("TIER_2"),
    )

    result = organization_admin.get_organization_agentic_flag(
        "org-1",
        config_api_root="https://config-api.test",
        ctx=MagicMock(),
    )

    assert result.organizations[0].organization_id == "org-1"
    assert result.organizations[0].is_agentic is True
    get_org_info.assert_called_once_with(
        organization_id="org-1",
        config_api_root="https://config-api.test",
        client_id=None,
        client_secret=None,
        bearer_token="token",
    )


@pytest.mark.unit
def test_set_organization_agentic_status_posts_to_config_api() -> None:
    """`set_organization_agentic_status` posts to the platform admin endpoint."""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "organizationId": "org-1",
        "organizationName": "Org One",
        "email": "admin@one.example",
        "isAgentic": True,
    }

    with patch(
        "airbyte_ops_mcp.cloud_admin.organization_agentic_flag.requests.post"
    ) as post:
        post.return_value = response
        result = set_organization_agentic_status(
            organization_id="org-1",
            is_agentic=True,
            config_api_root="https://config-api.example/api/v1",
            bearer_token="token",
        )

    assert result.organization_id == "org-1"
    assert result.is_agentic is True
    post.assert_called_once_with(
        "https://config-api.example/api/v1/organizations/agentic_status",
        json={"organizationId": "org-1", "isAgentic": True},
        headers={
            "Authorization": "Bearer token",
            "User-Agent": "Airbyte-Internal-Ops Python client",
            "Content-Type": "application/json",
        },
        timeout=30,
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "organization_names,expected_success,expected_messages",
    [
        pytest.param(
            {"org-1": "Org One", "org-2": "Org Two"},
            [True, True],
            [
                "updated managed agentic org status to True",
                "already has managed agentic org status True",
            ],
            id="multi_org_success_and_noop",
        ),
        pytest.param(
            {"org-1": "wrong", "org-2": "Org Two"},
            [False, True],
            [
                "Organization name mismatch",
                "already has managed agentic org status True",
            ],
            id="per_org_identity_validation",
        ),
    ],
)
def test_update_organization_agentic_flag_validates_and_updates_list(
    monkeypatch: pytest.MonkeyPatch,
    organization_names: dict[str, str],
    expected_success: list[bool],
    expected_messages: list[str],
) -> None:
    """`update_organization_agentic_flag` validates approval, identity, and list behavior."""
    rows_by_org_id = {
        "org-1": {
            "organization_id": "org-1",
            "organization_name": "Org One",
            "email": "admin@one.example",
            "tombstone": False,
            "is_agentic": False,
        },
        "org-2": {
            "organization_id": "org-2",
            "organization_name": "Org Two",
            "email": "admin@two.example",
            "tombstone": False,
            "is_agentic": True,
        },
    }
    updated_orgs = []

    def fake_query(organization_ids: list[str]) -> list[dict[str, object]]:
        return [rows_by_org_id[organization_id] for organization_id in organization_ids]

    def fake_update(
        organization_id: str,
        is_agentic: bool,
        config_api_root: str,
        client_id: str | None,
        client_secret: str | None,
        bearer_token: str | None,
    ) -> OrganizationInfo:
        updated_orgs.append(organization_id)
        return OrganizationInfo.model_validate(
            {
                "organizationId": organization_id,
                "organizationName": rows_by_org_id[organization_id][
                    "organization_name"
                ],
                "email": rows_by_org_id[organization_id]["email"],
                "isAgentic": is_agentic,
            }
        )

    monkeypatch.setattr(
        organization_admin, "require_internal_admin_flag_only", lambda: None
    )
    monkeypatch.setattr(
        organization_admin,
        "resolve_admin_email_from_approval",
        lambda approval_comment_url: "approver@airbyte.io",
    )
    monkeypatch.setattr(
        organization_admin, "query_organization_agentic_flags", fake_query
    )
    monkeypatch.setattr(
        organization_admin, "_set_organization_agentic_status", fake_update
    )
    monkeypatch.setattr(
        organization_admin,
        "_resolve_cloud_auth",
        lambda ctx: ("token", None, None),
    )
    monkeypatch.setattr(
        organization_admin,
        "get_org_tier",
        lambda organization_id, **_: _tier_result("TIER_2"),
    )

    result = organization_admin.update_organization_agentic_flag(
        ["org-1", "org-2"],
        True,
        approval_comment_url="https://slack.example/approval",
        organization_names=organization_names,
        ctx=MagicMock(),
    )

    assert [item.success for item in result.results] == expected_success
    for update_result, expected_message in zip(result.results, expected_messages):
        assert expected_message in update_result.message
    assert len(updated_orgs) == (1 if expected_success[0] else 0)


@pytest.mark.unit
def test_update_organization_agentic_flag_rejects_tier_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`update_organization_agentic_flag` defaults to `TIER_2` and rejects TIER_1."""
    monkeypatch.setattr(
        organization_admin, "require_internal_admin_flag_only", lambda: None
    )
    monkeypatch.setattr(
        organization_admin,
        "resolve_admin_email_from_approval",
        lambda approval_comment_url: "approver@airbyte.io",
    )
    monkeypatch.setattr(
        organization_admin,
        "query_organization_agentic_flags",
        lambda organization_ids: [
            {
                "organization_id": "org-1",
                "organization_name": "Org One",
                "email": "admin@one.example",
                "tombstone": False,
                "is_agentic": False,
            }
        ],
    )
    monkeypatch.setattr(
        organization_admin,
        "get_org_tier",
        lambda organization_id, **_: _tier_result("TIER_1"),
    )
    update = MagicMock()
    monkeypatch.setattr(organization_admin, "_set_organization_agentic_status", update)

    result = organization_admin.update_organization_agentic_flag(
        "org-1",
        True,
        approval_comment_url="https://slack.example/approval",
        organization_name="Org One",
        ctx=MagicMock(),
    )

    assert result.success is False
    assert "Tier mismatch" in result.results[0].message
    assert result.results[0].customer_tier == "TIER_1"
    assert result.results[0].tier_warning is not None
    update.assert_not_called()


@pytest.mark.unit
def test_update_organization_agentic_flag_requires_approval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`update_organization_agentic_flag` rejects updates without valid HITL approval."""
    monkeypatch.setattr(
        organization_admin, "require_internal_admin_flag_only", lambda: None
    )

    def reject_approval(approval_comment_url: str) -> str:
        raise organization_admin.ApprovalResolutionError("approval required")

    monkeypatch.setattr(
        organization_admin,
        "resolve_admin_email_from_approval",
        reject_approval,
    )

    result = organization_admin.update_organization_agentic_flag(
        ["org-1", "org-2"],
        True,
        approval_comment_url="invalid-approval",
        organization_names={"org-1": "Org One", "org-2": "Org Two"},
        ctx=MagicMock(),
    )

    assert result.success is False
    assert result.message == "approval required"
    assert [item.organization_id for item in result.results] == ["org-1", "org-2"]
    assert all(item.message == "approval required" for item in result.results)


@pytest.mark.unit
def test_update_organization_agentic_flag_uses_production_config_api_root(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`update_organization_agentic_flag` uses the trusted Config API root."""
    monkeypatch.setattr(
        organization_admin, "require_internal_admin_flag_only", lambda: None
    )
    monkeypatch.setattr(
        organization_admin,
        "resolve_admin_email_from_approval",
        lambda approval_comment_url: "approver@airbyte.io",
    )
    monkeypatch.setattr(
        organization_admin,
        "query_organization_agentic_flags",
        lambda organization_ids: [
            {
                "organization_id": "org-1",
                "organization_name": "Org One",
                "email": "admin@one.example",
                "tombstone": False,
                "is_agentic": False,
            }
        ],
    )
    monkeypatch.setattr(
        organization_admin,
        "get_org_tier",
        lambda organization_id, **_: _tier_result("TIER_2"),
    )
    monkeypatch.setattr(
        organization_admin,
        "_resolve_cloud_auth",
        lambda ctx: ("token", None, None),
    )
    set_status = MagicMock(
        return_value=OrganizationInfo.model_validate(
            {
                "organizationId": "org-1",
                "organizationName": "Org One",
                "email": "admin@one.example",
                "isAgentic": True,
            }
        )
    )
    monkeypatch.setattr(
        organization_admin, "_set_organization_agentic_status", set_status
    )

    result = organization_admin.update_organization_agentic_flag(
        "org-1",
        True,
        approval_comment_url="https://slack.example/approval",
        organization_name="Org One",
        ctx=MagicMock(),
    )

    assert result.success is True
    assert result.results[0].organization_id == "org-1"
    set_status.assert_called_once_with(
        organization_id="org-1",
        is_agentic=True,
        config_api_root=organization_admin.constants.CLOUD_CONFIG_API_ROOT,
        client_id=None,
        client_secret=None,
        bearer_token="token",
    )
