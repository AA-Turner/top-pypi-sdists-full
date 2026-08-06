"""Unit tests for connection-level resource requirements."""

from __future__ import annotations

from contextlib import contextmanager
from types import SimpleNamespace
from typing import Iterator
from unittest.mock import patch
from uuid import UUID

import pytest
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.cloud_admin.connection_resources import (
    CpuRung,
    DiskRung,
    MemoryRung,
    _parse_cpu,
    _requirements_from_connection,
    _rung_requirements,
    _validate_requirements,
    get_connection_resource_requirements,
    set_connection_resource_requirements,
)
from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth

CONNECTION_ID = "00000000-0000-0000-0000-000000000001"
WORKSPACE_ID = "00000000-0000-0000-0000-000000000002"
AUTH = ResolvedCloudAuth(bearer_token="token")
ISSUE_URL = "https://github.com/airbytehq/airbyte-ops-mcp/issues/1209"


def _response(payload: dict[str, object]) -> dict[str, object]:
    return payload


def _connection(requirements: dict[str, str] | None = None) -> dict[str, object]:
    return {
        "connectionId": CONNECTION_ID,
        "resourceRequirements": requirements or {},
    }


def _context() -> list[dict[str, object]]:
    return [
        {
            "connection_id": CONNECTION_ID,
            "workspace_id": WORKSPACE_ID,
            "organization_id": "org-1",
        }
    ]


@contextmanager
def _mock_write_dependencies(
    responses: list[dict[str, object]],
    *,
    context: list[dict[str, object]] | None = None,
    tier: str = "TIER_2",
) -> Iterator[object]:
    with patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.validate_admin_and_authorization",
        return_value=("admin@airbyte.io", None),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.query_connection_workspace_details",
        return_value=context or _context(),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.get_org_tier",
        return_value=SimpleNamespace(customer_tier=tier, source_health=None),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.make_config_api_request",
        side_effect=responses,
    ) as request, patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.post_channel_message",
    ):
        yield request


def _set_requirements(**overrides: object) -> object:
    values: dict[str, object] = {
        "auth": AUTH,
        "connection_id": CONNECTION_ID,
        "workspace_id": WORKSPACE_ID,
        "cpu_rung": None,
        "memory_rung": None,
        "disk_rung": None,
        "unset": False,
        "override_reason": "Increase worker resources",
        "issue_url": ISSUE_URL,
        "approval_comment_url": "https://example.slack.com/archives/C1/p1",
        "customer_tier_filter": "TIER_2",
    }
    values.update(overrides)
    return set_connection_resource_requirements(**values)


@pytest.mark.unit
def test_get_defaults_connection() -> None:
    with patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.make_config_api_request",
        return_value=_response(_connection()),
    ) as post:
        result = get_connection_resource_requirements(
            auth=AUTH,
            connection_id=CONNECTION_ID,
        )

    assert result.is_on_defaults is True
    assert result.was_overridden is False
    assert result.memory_rung == "DEFAULT"
    assert result.next_memory_rung == "1Gi"
    assert result.disk_rung == "DEFAULT"
    assert result.next_disk_rung == "2Gi"
    assert post.call_args.kwargs["json"] == {"connectionId": CONNECTION_ID}


@pytest.mark.unit
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("500m", 0.5, id="integer-millicores"),
        pytest.param("2.0", 2.0, id="decimal-cores"),
    ],
)
def test_parse_valid_cpu_quantities(value: str, expected: float) -> None:
    assert _parse_cpu(value) == expected


@pytest.mark.unit
def test_parse_fractional_millicores_rejected() -> None:
    with pytest.raises(PyAirbyteInputError, match="Invalid CPU quantity"):
        _parse_cpu("0.5m")


@pytest.mark.unit
@pytest.mark.parametrize(
    ("rung", "request_key", "limit_key"),
    [
        *(
            pytest.param(
                rung,
                "memory_request",
                "memory_limit",
                id=f"memory-{rung.value}",
            )
            for rung in MemoryRung
            if rung != MemoryRung.DEFAULT
        ),
        *(
            pytest.param(
                rung,
                "ephemeral_storage_request",
                "ephemeral_storage_limit",
                id=f"disk-{rung.value}",
            )
            for rung in DiskRung
            if rung != DiskRung.DEFAULT
        ),
        *(
            pytest.param(
                rung,
                "cpu_request",
                "cpu_limit",
                id=f"cpu-{rung.value}",
            )
            for rung in CpuRung
            if rung != CpuRung.DEFAULT
        ),
    ],
)
def test_rung_sets_equal_request_and_limit(
    rung: MemoryRung | DiskRung | CpuRung,
    request_key: str,
    limit_key: str,
) -> None:
    assert _rung_requirements(
        rung,
        request_key=request_key,
        limit_key=limit_key,
    ) == {request_key: rung.value, limit_key: rung.value}


@pytest.mark.unit
def test_default_rungs_omit_dimension() -> None:
    assert (
        _rung_requirements(
            MemoryRung.DEFAULT,
            request_key="memory_request",
            limit_key="memory_limit",
        )
        == {}
    )
    assert (
        _rung_requirements(
            DiskRung.DEFAULT,
            request_key="ephemeral_storage_request",
            limit_key="ephemeral_storage_limit",
        )
        == {}
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    (
        "requirements",
        "rung_attribute",
        "next_rung_attribute",
        "expected_rung",
        "expected_next",
        "expected_overridden",
    ),
    [
        pytest.param(
            {},
            "memory_rung",
            "next_memory_rung",
            "DEFAULT",
            "1Gi",
            False,
            id="defaults-memory",
        ),
        pytest.param(
            {"memory_request": "6Gi", "memory_limit": "8Gi"},
            "memory_rung",
            "next_memory_rung",
            "8Gi",
            None,
            True,
            id="overridden-memory",
        ),
        pytest.param(
            {"memory_request": "3.5Gi", "memory_limit": "3.5Gi"},
            "memory_rung",
            "next_memory_rung",
            "OFF_LADDER",
            "4Gi",
            True,
            id="parseable-memory-between-rungs",
        ),
        pytest.param(
            {"ephemeral_storage_request": "3Gi", "ephemeral_storage_limit": "3Gi"},
            "disk_rung",
            "next_disk_rung",
            "OFF_LADDER",
            "5Gi",
            True,
            id="parseable-disk-between-rungs",
        ),
        pytest.param(
            {"cpu_request": "not-a-cpu", "cpu_limit": "not-a-cpu"},
            "cpu_rung",
            "next_cpu_rung",
            "OFF_LADDER",
            None,
            True,
            id="unparseable-cpu",
        ),
    ],
)
def test_read_reports_ladder_status(
    requirements: dict[str, str],
    rung_attribute: str,
    next_rung_attribute: str,
    expected_rung: str,
    expected_next: str | None,
    expected_overridden: bool,
) -> None:
    result = _requirements_from_connection(_connection(requirements), CONNECTION_ID)

    assert result.was_overridden is expected_overridden
    assert getattr(result, rung_attribute) == expected_rung
    assert getattr(result, next_rung_attribute) == expected_next


@pytest.mark.unit
def test_set_happy_path() -> None:
    responses = [
        _response(_connection()),
        _response(_connection({"cpu_request": "2", "memory_limit": "6Gi"})),
    ]
    with patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.validate_admin_and_authorization",
        return_value=("admin@airbyte.io", None),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.query_connection_workspace_details",
        return_value=_context(),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.get_org_tier",
        return_value=SimpleNamespace(
            customer_tier="TIER_2",
            source_health=None,
        ),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.make_config_api_request",
        side_effect=responses,
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.post_channel_message",
    ):
        result = set_connection_resource_requirements(
            auth=AUTH,
            connection_id=CONNECTION_ID,
            workspace_id=WORKSPACE_ID,
            cpu_rung=CpuRung.TWO,
            memory_rung=MemoryRung.SIX_GI,
            disk_rung=None,
            unset=False,
            override_reason="Increase worker resources",
            issue_url=ISSUE_URL,
            approval_comment_url="https://example.slack.com/archives/C1/p1",
            customer_tier_filter="TIER_2",
            cpu_impact_acknowledged=True,
        )

    assert result.success is True
    assert result.new_cpu_request == "2"
    assert "apply to the next sync attempt" in result.message


@pytest.mark.unit
@pytest.mark.parametrize(
    ("existing", "cpu_rung", "memory_rung", "disk_rung", "unset", "expected_payload"),
    [
        pytest.param(
            {"cpu_limit": "3", "memory_limit": "8Gi"},
            None,
            MemoryRung.SEVEN_GI,
            None,
            False,
            {
                "cpu_limit": "3",
                "memory_request": "7Gi",
                "memory_limit": "7Gi",
            },
            id="memory-update-preserves-cpu",
        ),
        pytest.param(
            {
                "cpu_limit": "3",
                "memory_request": "6Gi",
                "memory_limit": "6Gi",
            },
            None,
            None,
            DiskRung.FIVE_GI,
            False,
            {
                "cpu_limit": "3",
                "memory_request": "6Gi",
                "memory_limit": "6Gi",
                "ephemeral_storage_request": "5Gi",
                "ephemeral_storage_limit": "5Gi",
            },
            id="disk-update-preserves-cpu-and-memory",
        ),
        pytest.param(
            {
                "memory_request": "6Gi",
                "memory_limit": "6Gi",
                "ephemeral_storage_request": "5Gi",
                "ephemeral_storage_limit": "5Gi",
            },
            None,
            MemoryRung.DEFAULT,
            None,
            False,
            {
                "ephemeral_storage_request": "5Gi",
                "ephemeral_storage_limit": "5Gi",
            },
            id="default-memory-omits-memory",
        ),
        pytest.param(
            {"cpu_request": "2"},
            None,
            None,
            None,
            True,
            {},
            id="unset-sends-empty-requirements",
        ),
    ],
)
def test_write_sends_expected_merged_requirements(
    existing: dict[str, str],
    cpu_rung: CpuRung | None,
    memory_rung: MemoryRung | None,
    disk_rung: DiskRung | None,
    unset: bool,
    expected_payload: dict[str, str],
) -> None:
    with _mock_write_dependencies(
        [_response(_connection(existing)), _response(_connection(expected_payload))]
    ) as request:
        result = _set_requirements(
            cpu_rung=cpu_rung,
            memory_rung=memory_rung,
            disk_rung=disk_rung,
            unset=unset,
            override_reason="Update worker resources",
            cpu_impact_acknowledged=cpu_rung is not None,
        )

    assert result.success is True
    if unset:
        assert result.was_overridden_before is True
    assert (
        request.call_args_list[-1].kwargs["json"]["resourceRequirements"]
        == expected_payload
    )


@pytest.mark.unit
def test_uuid_organization_id_resolves_customer_tier() -> None:
    organization_id = UUID("00000000-0000-0000-0000-000000000003")
    context = _context()
    context[0]["organization_id"] = organization_id
    tier_by_organization = {
        str(organization_id): SimpleNamespace(
            customer_tier="TIER_2",
            source_health=None,
        )
    }

    with patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.validate_admin_and_authorization",
        return_value=("admin@airbyte.io", None),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.query_connection_workspace_details",
        return_value=context,
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.get_org_tier",
        side_effect=lambda organization_id, **_: tier_by_organization[organization_id],
    ) as get_tier, patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.make_config_api_request",
        side_effect=[
            _response(_connection()),
            _response(_connection({"cpu_request": "2"})),
        ],
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.post_channel_message",
    ):
        result = set_connection_resource_requirements(
            auth=AUTH,
            connection_id=CONNECTION_ID,
            workspace_id=WORKSPACE_ID,
            cpu_rung=CpuRung.TWO,
            memory_rung=None,
            disk_rung=None,
            unset=False,
            override_reason="Increase worker resources",
            issue_url=ISSUE_URL,
            approval_comment_url="https://example.slack.com/archives/C1/p1",
            customer_tier_filter="TIER_2",
            cpu_impact_acknowledged=True,
        )

    assert result.success is True
    get_tier.assert_called_once_with(str(organization_id), allow_degraded=True)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("existing", "cpu_rung"),
    [
        pytest.param({"cpu_request": "2"}, CpuRung.THREE, id="request-only"),
        pytest.param(
            {"cpu_request": "2", "cpu_limit": "2"},
            CpuRung.THREE,
            id="request-and-limit",
        ),
    ],
)
def test_cpu_raise_requires_acknowledgement(
    existing: dict[str, str],
    cpu_rung: CpuRung,
) -> None:
    with patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.validate_admin_and_authorization",
        return_value=("admin@airbyte.io", None),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.query_connection_workspace_details",
        return_value=_context(),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.get_org_tier",
        return_value=SimpleNamespace(customer_tier="TIER_2", source_health=None),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.make_config_api_request",
        return_value=_response(_connection(existing)),
    ), pytest.raises(PyAirbyteInputError, match="cpu_impact_acknowledged"):
        _set_requirements(cpu_rung=cpu_rung)


@pytest.mark.unit
def test_missing_approval_rejected() -> None:
    with patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.validate_admin_and_authorization",
        return_value=(None, "Authorization validation failed: approval required"),
    ):
        result = _set_requirements(cpu_rung=CpuRung.TWO)

    assert result.success is False
    assert "approval" in result.message


@pytest.mark.unit
def test_bad_issue_url_rejected() -> None:
    with pytest.raises(PyAirbyteInputError, match="issue_url"):
        _set_requirements(cpu_rung=CpuRung.TWO, issue_url="https://example.com/issue")


@pytest.mark.unit
def test_tier_mismatch_rejected() -> None:
    with patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.validate_admin_and_authorization",
        return_value=("admin@airbyte.io", None),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.query_connection_workspace_details",
        return_value=_context(),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.get_org_tier",
        return_value=SimpleNamespace(customer_tier="TIER_1", source_health=None),
    ):
        result = _set_requirements(cpu_rung=CpuRung.TWO)

    assert result.success is False
    assert "Tier mismatch" in result.message


@pytest.mark.unit
def test_existing_override_is_replaced_and_previous_values_reported() -> None:
    with _mock_write_dependencies(
        [
            _response(_connection({"cpu_request": "2", "cpu_limit": "2"})),
            _response(_connection({"cpu_request": "3", "cpu_limit": "3"})),
        ]
    ) as post:
        result = _set_requirements(
            cpu_rung=CpuRung.THREE,
            cpu_impact_acknowledged=True,
        )

    assert result.success is True
    assert result.was_overridden_before is True
    assert result.is_overridden_after is True
    assert result.previous_cpu_request == "2"
    assert result.previous_cpu_limit == "2"
    assert result.new_cpu_request == "3"
    assert result.new_cpu_limit == "3"
    assert post.call_args_list[-1].kwargs["json"]["resourceRequirements"] == {
        "cpu_request": "3",
        "cpu_limit": "3",
    }


@pytest.mark.unit
@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        pytest.param("cpu_request", "not-cpu", "Invalid CPU", id="malformed-cpu"),
        pytest.param("cpu_request", "5", "maximum", id="over-cap-cpu"),
    ],
)
def test_cpu_validation_backstop(field: str, value: str, message: str) -> None:
    with pytest.raises(PyAirbyteInputError, match=message):
        _validate_requirements(**{field: value})


@pytest.mark.unit
def test_workspace_mismatch_rejected() -> None:
    context = _context()
    context[0]["workspace_id"] = "different-workspace"
    with patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.validate_admin_and_authorization",
        return_value=("admin@airbyte.io", None),
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.query_connection_workspace_details",
        return_value=context,
    ), patch(
        "airbyte_ops_mcp.cloud_admin.connection_resources.get_org_tier",
    ):
        result = _set_requirements(cpu_rung=CpuRung.TWO)

    assert result.success is False
    assert "workspace" in result.message
