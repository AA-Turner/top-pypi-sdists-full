# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for progressive rollout status helpers."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import call, patch

import pytest

from airbyte_ops_mcp.registry.progressive_rollout_status import (
    get_connector_definition_id,
    get_connector_rollout_status,
)


@pytest.mark.unit
def test_get_connector_rollout_status_uses_active_query_result() -> None:
    rollout_rows = [
        {
            "rollout_id": "rollout-active",
            "actor_definition_id": "definition-id",
            "state": "in_progress",
            "has_breaking_changes": False,
            "updated_by_user_id": "8d6f338f-0a67-4d75-9da4-30b80d6003e3",
            "updated_by_user_name": "Test User",
            "updated_by_user_email": "test-user@airbyte.io",
            "rc_docker_image_tag": "1.2.3-rc.1",
            "rc_docker_repository": "airbyte/source-test",
            "filters": '{"customerTierFilters":[{"name":"TIER","value":["TIER_2"]}]}',
        },
        {
            "rollout_id": "rollout-terminal",
            "actor_definition_id": "definition-id",
            "state": "succeeded",
            "has_breaking_changes": False,
            "filters": None,
        },
    ]

    with patch(
        "airbyte_ops_mcp.registry.progressive_rollout_status.get_connector_definition_id",
        return_value="definition-id",
    ), patch(
        "airbyte_ops_mcp.registry.progressive_rollout_status.query_connector_rollouts_for_connector",
        side_effect=[rollout_rows, [rollout_rows[0]]],
    ) as query_rollouts:
        status = get_connector_rollout_status(
            repo_path=Path("/repo"),
            connector_name="source-test",
            active_only=False,
            limit=100,
        )

    assert query_rollouts.call_args_list == [
        call(
            actor_definition_id="definition-id",
            active_only=False,
            limit=100,
        ),
        call(
            actor_definition_id="definition-id",
            active_only=True,
            limit=1,
        ),
    ]
    assert status.has_active_rollout is True
    assert status.rollout_count == 2
    assert status.rollouts[0].customer_tier == "TIER_2"
    assert status.rollouts[0].filters == {
        "customerTierFilters": [{"name": "TIER", "value": ["TIER_2"]}]
    }
    assert status.rollouts[0].rollout_docker_image_tag == "1.2.3-rc.1"
    assert status.rollouts[0].rollout_docker_repository == "airbyte/source-test"
    assert (
        status.rollouts[0].updated_by_user_id == "8d6f338f-0a67-4d75-9da4-30b80d6003e3"
    )
    assert status.rollouts[0].updated_by_user_name == "Test User"
    assert status.rollouts[0].updated_by_user_email == "test-user@airbyte.io"


@pytest.mark.unit
def test_get_connector_rollout_status_reports_no_active_rollouts_for_terminal_rows() -> (
    None
):
    rollout_rows = [
        {
            "rollout_id": "rollout-terminal",
            "actor_definition_id": "definition-id",
            "state": "succeeded",
            "has_breaking_changes": False,
            "filters": {"tierFilter": {"tier": "TIER_1"}},
        },
    ]

    with patch(
        "airbyte_ops_mcp.registry.progressive_rollout_status.get_connector_definition_id",
        return_value="definition-id",
    ), patch(
        "airbyte_ops_mcp.registry.progressive_rollout_status.query_connector_rollouts_for_connector",
        side_effect=[rollout_rows, []],
    ):
        status = get_connector_rollout_status(
            repo_path=Path("/repo"),
            connector_name="source-test",
            active_only=False,
            limit=100,
        )

    assert status.has_active_rollout is False
    assert status.rollouts[0].customer_tier == "TIER_1"


@pytest.mark.unit
def test_get_connector_definition_id_reads_local_metadata() -> None:
    metadata = {"data": {"definitionId": "definition-id"}}

    with patch(
        "airbyte_ops_mcp.registry.progressive_rollout_status.load_raw_connector_metadata_from_local",
        return_value=metadata,
    ) as load_metadata:
        definition_id = get_connector_definition_id(Path("/repo"), "source-test")

    load_metadata.assert_called_once_with(Path("/repo"), "source-test")
    assert definition_id == "definition-id"
