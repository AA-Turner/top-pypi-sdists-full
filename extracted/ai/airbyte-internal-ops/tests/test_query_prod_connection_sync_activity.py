# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for `query_prod_connection_sync_activity`."""

from __future__ import annotations

from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.mcp.prod_db_ops import (
    StatusFilter,
    _validate_sync_activity_scope,
    _validate_sync_activity_window,
    query_prod_connection_sync_activity,
)

UTC = timezone.utc


@pytest.mark.unit
@pytest.mark.parametrize(
    "organization_id,workspace_id,connection_ids,raises",
    [
        pytest.param("org-id", None, None, False, id="organization_scope"),
        pytest.param(None, "workspace-id", None, False, id="workspace_scope"),
        pytest.param(None, None, ["connection-id"], False, id="connection_scope"),
        pytest.param("org-id", "workspace-id", None, False, id="org_plus_workspace"),
        pytest.param(None, None, None, True, id="missing_scope"),
        pytest.param(None, None, [], True, id="empty_connection_scope"),
    ],
)
def test_validate_sync_activity_scope(
    organization_id: str | None,
    workspace_id: str | None,
    connection_ids: list[str] | None,
    raises: bool,
) -> None:
    if raises:
        with pytest.raises(PyAirbyteInputError):
            _validate_sync_activity_scope(
                organization_id=organization_id,
                workspace_id=workspace_id,
                connection_ids=connection_ids,
            )
        return
    _validate_sync_activity_scope(
        organization_id=organization_id,
        workspace_id=workspace_id,
        connection_ids=connection_ids,
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "start_offset_hours,end_offset_hours,naive_start,naive_end,raises",
    [
        pytest.param(-24, -1, False, False, False, id="recent_window"),
        pytest.param(-1000, 0, False, False, False, id="old_window_allowed"),
        pytest.param(-1, 1, False, False, False, id="future_end_allowed"),
        pytest.param(-1, -2, False, False, True, id="start_after_end"),
        pytest.param(-24, -24, False, False, True, id="zero_length_window"),
        pytest.param(-24, -1, True, False, True, id="naive_start_rejected"),
        pytest.param(-24, -1, False, True, True, id="naive_end_rejected"),
    ],
)
def test_validate_sync_activity_window(
    start_offset_hours: int,
    end_offset_hours: int,
    naive_start: bool,
    naive_end: bool,
    raises: bool,
) -> None:
    now = datetime(2026, 5, 29, 12, 0, tzinfo=UTC)
    start_at = now + timedelta(hours=start_offset_hours)
    end_at = now + timedelta(hours=end_offset_hours)
    if naive_start:
        start_at = start_at.replace(tzinfo=None)
    if naive_end:
        end_at = end_at.replace(tzinfo=None)

    if raises:
        with pytest.raises(PyAirbyteInputError):
            _validate_sync_activity_window(start_at=start_at, end_at=end_at)
        return

    normalized_start, normalized_end = _validate_sync_activity_window(
        start_at=start_at,
        end_at=end_at,
    )
    assert normalized_start.tzinfo is UTC
    assert normalized_end.tzinfo is UTC


@pytest.mark.unit
def test_validate_sync_activity_window_normalizes_offset_to_utc() -> None:
    now = datetime(2026, 5, 29, 12, 0, tzinfo=UTC)
    tz_plus_one = timezone(timedelta(hours=1))
    start_at = (now - timedelta(hours=2)).astimezone(tz_plus_one)
    end_at = (now - timedelta(hours=1)).astimezone(tz_plus_one)

    normalized_start, normalized_end = _validate_sync_activity_window(
        start_at=start_at,
        end_at=end_at,
    )

    assert normalized_start == now - timedelta(hours=2)
    assert normalized_end == now - timedelta(hours=1)


@pytest.mark.unit
def test_query_prod_connection_sync_activity_delegates_to_prod_db() -> None:
    """End-to-end: scope is validated, alias resolved, tier enrichment applied."""
    now = datetime.now(UTC)
    start_at = now - timedelta(hours=1)
    end_at = now
    raw_rows = [
        {
            "organization_id": "org-id",
            "connection_id": "conn-id",
            "dataplane_name": "US",
        },
    ]

    with ExitStack() as stack:
        prod_query = stack.enter_context(
            patch(
                "airbyte_ops_mcp.mcp.prod_db_ops"
                ".query_connection_sync_activity_from_prod",
                return_value=raw_rows,
            )
        )
        enrich = stack.enter_context(
            patch(
                "airbyte_ops_mcp.mcp.prod_db_ops.enrich_rows_by_org",
                side_effect=lambda rows: [
                    {**r, "customer_tier": "TIER_2"} for r in rows
                ],
            )
        )

        result = query_prod_connection_sync_activity(
            start_at=start_at,
            end_at=end_at,
            organization_id="org-id",
            status_filter=StatusFilter.FAILED,
        )

    prod_query.assert_called_once()
    call_kwargs = prod_query.call_args.kwargs
    assert call_kwargs["organization_id"] == "org-id"
    assert call_kwargs["status_filter"] == "failed"
    enrich.assert_called_once()
    assert result == [
        {
            "organization_id": "org-id",
            "connection_id": "conn-id",
            "dataplane_name": "US",
            "customer_tier": "TIER_2",
        },
    ]
