"""Tests for the organization-scoped connector pin MCP tools."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.mcp import prod_db_ops
from airbyte_ops_mcp.mcp.prod_db_ops import (
    PinOriginFilter,
    _normalize_optional_version_id,
    _pin_category,
    _require_organization_id,
    _resolve_connector_filter_id,
    query_prod_pin_stats_for_organization,
    query_prod_pins_for_organization,
)

_ORG_ID = "11111111-1111-1111-1111-111111111111"
_VERSION_ID = "22222222-2222-2222-2222-222222222222"


@pytest.mark.unit
@pytest.mark.parametrize(
    "origin_type,expected",
    [
        pytest.param("connector_rollout", "rollout", id="rollout"),
        pytest.param("breaking_change", "breaking_change", id="breaking_change"),
        pytest.param(None, "manual", id="none_is_manual"),
        pytest.param("user", "manual", id="other_is_manual"),
    ],
)
def test_pin_category(origin_type: str | None, expected: str) -> None:
    assert _pin_category(origin_type) == expected


@pytest.mark.unit
def test_resolve_connector_filter_id_rejects_both() -> None:
    with pytest.raises(PyAirbyteInputError):
        _resolve_connector_filter_id(
            connector_definition_id="def-id",
            connector_canonical_name="source-postgres",
        )


@pytest.mark.unit
def test_resolve_connector_filter_id_passthrough_definition_id() -> None:
    assert (
        _resolve_connector_filter_id(
            connector_definition_id="def-id",
            connector_canonical_name=None,
        )
        == "def-id"
    )


@pytest.mark.unit
def test_resolve_connector_filter_id_blank_inputs_are_none() -> None:
    """Blank or whitespace-only inputs resolve to `None`, not a zero-match filter."""
    assert (
        _resolve_connector_filter_id(
            connector_definition_id="",
            connector_canonical_name="   ",
        )
        is None
    )


@pytest.mark.unit
@pytest.mark.parametrize("blank", ["", "   ", None])
def test_require_organization_id_rejects_blank(blank: str | None) -> None:
    with pytest.raises(PyAirbyteInputError):
        _require_organization_id(blank)  # type: ignore[arg-type]


@pytest.mark.unit
def test_require_organization_id_passthrough_uuid() -> None:
    assert _require_organization_id(_ORG_ID) == _ORG_ID


@pytest.mark.unit
def test_require_organization_id_canonicalizes_uppercase_uuid() -> None:
    assert _require_organization_id(_ORG_ID.upper()) == _ORG_ID


@pytest.mark.unit
def test_require_organization_id_rejects_malformed_uuid() -> None:
    with pytest.raises(PyAirbyteInputError):
        _require_organization_id("not-a-uuid")


@pytest.mark.unit
@pytest.mark.parametrize("blank", ["", "   ", None])
def test_normalize_optional_version_id_blank_is_none(blank: str | None) -> None:
    assert _normalize_optional_version_id(blank) is None


@pytest.mark.unit
def test_normalize_optional_version_id_rejects_invalid_uuid() -> None:
    with pytest.raises(PyAirbyteInputError):
        _normalize_optional_version_id("not-a-uuid")


@pytest.mark.unit
def test_normalize_optional_version_id_passthrough_uuid() -> None:
    assert _normalize_optional_version_id(f"  {_VERSION_ID}  ") == _VERSION_ID


@pytest.mark.unit
def test_resolve_connector_filter_id_resolves_canonical_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        prod_db_ops,
        "resolve_canonical_name_to_definition_id",
        lambda canonical_name: f"resolved-{canonical_name}",
    )
    assert (
        _resolve_connector_filter_id(
            connector_definition_id=None,
            connector_canonical_name="source-postgres",
        )
        == "resolved-source-postgres"
    )


@pytest.mark.unit
def test_query_prod_pin_stats_for_organization_maps_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_query_org_pin_stats(
        organization_id: str,
        *,
        connector_definition_id: str | None = None,
        limit: int = 1000,
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured["organization_id"] = organization_id
        captured["connector_definition_id"] = connector_definition_id
        captured["limit"] = limit
        return [
            {
                "version_id": "v-1",
                "connector_definition_id": "def-1",
                "connector_name": "Postgres",
                "docker_repository": "airbyte/source-postgres",
                "docker_image_tag": "3.6.1",
                "last_published": datetime(2026, 1, 2, tzinfo=timezone.utc),
                "pin_count": 5,
                "manual_pins": 2,
                "rollout_pins": 2,
                "breaking_change_pins": 1,
                "actor_pins": 3,
                "workspace_pins": 1,
                "org_pins": 1,
                "has_active_rollout": True,
            }
        ]

    monkeypatch.setattr(prod_db_ops, "query_org_pin_stats", fake_query_org_pin_stats)

    result = query_prod_pin_stats_for_organization(organization_id=_ORG_ID)

    assert captured["organization_id"] == _ORG_ID
    assert len(result) == 1
    row = result[0]
    assert row.version_id == "v-1"
    assert row.pin_count == 5
    assert row.has_active_rollout is True
    assert row.last_published == "2026-01-02T00:00:00+00:00"


@pytest.mark.unit
def test_query_prod_pins_for_organization_maps_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_query_org_connector_pins(
        organization_id: str,
        *,
        connector_definition_id: str | None = None,
        pinned_version_id: str | None = None,
        limit: int = 1000,
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured["organization_id"] = organization_id
        captured["pinned_version_id"] = pinned_version_id
        return [
            {
                "connector_definition_id": "def-1",
                "connector_name": "Postgres",
                "docker_repository": "airbyte/source-postgres",
                "pinned_version_id": "v-1",
                "pinned_version_tag": "3.6.1",
                "pin_scope_type": "actor",
                "scope_id": "actor-1",
                "scope_name": "My Actor",
                "origin_type": "connector_rollout",
                "pinned_by_user_email": None,
                "pinned_by_user_name": None,
                "rollout_id": "rollout-1",
                "rollout_state": "in_progress",
                "description": "rollout pin",
                "reference_url": None,
                "created_at": datetime(2026, 1, 2, tzinfo=timezone.utc),
                "expires_at": None,
            },
            {
                "connector_definition_id": "def-1",
                "connector_name": "Postgres",
                "docker_repository": "airbyte/source-postgres",
                "pinned_version_id": "v-1",
                "pinned_version_tag": "3.6.1",
                "pin_scope_type": "organization",
                "scope_id": _ORG_ID,
                "scope_name": "Acme",
                "origin_type": None,
                "pinned_by_user_email": "ops@example.com",
                "pinned_by_user_name": "Ops",
                "rollout_id": None,
                "rollout_state": None,
                "description": "manual pin",
                "reference_url": "https://example.com",
                "created_at": datetime(2026, 1, 3, tzinfo=timezone.utc),
                "expires_at": datetime(2026, 2, 3, tzinfo=timezone.utc),
            },
        ]

    monkeypatch.setattr(
        prod_db_ops,
        "query_org_connector_pins",
        fake_query_org_connector_pins,
    )

    result = query_prod_pins_for_organization(
        organization_id=_ORG_ID,
        pinned_version_id=_VERSION_ID,
        origin_filter=PinOriginFilter.ALL,
    )

    assert captured["pinned_version_id"] == _VERSION_ID
    assert "origin_filter" not in captured
    assert len(result) == 2

    rollout_pin, manual_pin = result
    assert rollout_pin.pin_category == "rollout"
    assert rollout_pin.rollout_id == "rollout-1"
    assert rollout_pin.is_active_rollout is True
    assert rollout_pin.set_by is None
    assert rollout_pin.created_at == "2026-01-02T00:00:00+00:00"

    assert manual_pin.pin_category == "manual"
    assert manual_pin.is_active_rollout is False
    assert manual_pin.set_by == "ops@example.com"
    assert manual_pin.expires_at == "2026-02-03T00:00:00+00:00"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("origin_filter", "expected_categories"),
    [
        pytest.param(PinOriginFilter.ALL, ["rollout", "manual"], id="all"),
        pytest.param(PinOriginFilter.CONNECTOR_ROLLOUT, ["rollout"], id="rollout"),
        pytest.param(PinOriginFilter.MANUAL, ["manual"], id="manual"),
        pytest.param(PinOriginFilter.BREAKING_CHANGE, [], id="breaking_change"),
    ],
)
def test_query_prod_pins_for_organization_filters_origin_in_memory(
    monkeypatch: pytest.MonkeyPatch,
    origin_filter: PinOriginFilter,
    expected_categories: list[str],
) -> None:
    def fake_query_org_connector_pins(
        organization_id: str,
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        return [
            {
                "connector_definition_id": "def-1",
                "connector_name": "Postgres",
                "docker_repository": "airbyte/source-postgres",
                "pinned_version_id": "v-1",
                "pinned_version_tag": "3.6.1",
                "pin_scope_type": "actor",
                "scope_id": "actor-1",
                "scope_name": "My Actor",
                "origin_type": "connector_rollout",
                "pinned_by_user_email": None,
                "pinned_by_user_name": None,
                "rollout_id": "rollout-1",
                "rollout_state": "in_progress",
                "description": None,
                "reference_url": None,
                "created_at": datetime(2026, 1, 2, tzinfo=timezone.utc),
                "expires_at": None,
            },
            {
                "connector_definition_id": "def-1",
                "connector_name": "Postgres",
                "docker_repository": "airbyte/source-postgres",
                "pinned_version_id": "v-1",
                "pinned_version_tag": "3.6.1",
                "pin_scope_type": "organization",
                "scope_id": _ORG_ID,
                "scope_name": "Acme",
                "origin_type": "user",
                "pinned_by_user_email": "ops@example.com",
                "pinned_by_user_name": "Ops",
                "rollout_id": None,
                "rollout_state": None,
                "description": None,
                "reference_url": None,
                "created_at": datetime(2026, 1, 3, tzinfo=timezone.utc),
                "expires_at": None,
            },
        ]

    monkeypatch.setattr(
        prod_db_ops,
        "query_org_connector_pins",
        fake_query_org_connector_pins,
    )

    result = query_prod_pins_for_organization(
        organization_id=_ORG_ID,
        origin_filter=origin_filter,
    )

    assert [pin.pin_category for pin in result] == expected_categories
