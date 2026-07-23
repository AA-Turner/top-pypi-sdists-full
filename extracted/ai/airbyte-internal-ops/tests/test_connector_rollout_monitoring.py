# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the connector rollout monitoring API-based tool."""

from unittest.mock import MagicMock, patch

import pytest
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.cloud_admin.api_client import get_actor_sync_info
from airbyte_ops_mcp.mcp.connector_versions import (
    RolloutActorSelectionInfo,
    RolloutActorSyncStats,
    RolloutMonitoringResult,
    query_prod_rollout_monitoring_stats,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "api_response,expected_selection_info,expected_sync_stats",
    [
        pytest.param(
            {
                "data": {
                    "actor_selection_info": {
                        "num_actors": 100,
                        "num_pinned_to_connector_rollout": 10,
                        "num_actors_eligible_or_already_pinned": 50,
                    },
                    "syncs": {
                        "actor-1": {
                            "num_connections": 5,
                            "num_succeeded": 10,
                            "num_failed": 2,
                        },
                        "actor-2": {
                            "num_connections": 3,
                            "num_succeeded": 8,
                            "num_failed": 0,
                        },
                    },
                }
            },
            RolloutActorSelectionInfo(
                num_actors=100,
                num_pinned_to_connector_rollout=10,
                num_actors_eligible_or_already_pinned=50,
            ),
            [
                RolloutActorSyncStats(
                    actor_id="actor-1",
                    num_connections=5,
                    num_succeeded=10,
                    num_failed=2,
                ),
                RolloutActorSyncStats(
                    actor_id="actor-2", num_connections=3, num_succeeded=8, num_failed=0
                ),
            ],
            id="typical_response_with_multiple_actors",
        ),
        pytest.param(
            {
                "data": {
                    "actor_selection_info": {
                        "num_actors": 0,
                        "num_pinned_to_connector_rollout": 0,
                        "num_actors_eligible_or_already_pinned": 0,
                    },
                    "syncs": {},
                }
            },
            RolloutActorSelectionInfo(
                num_actors=0,
                num_pinned_to_connector_rollout=0,
                num_actors_eligible_or_already_pinned=0,
            ),
            [],
            id="empty_rollout_no_actors",
        ),
        pytest.param(
            {"data": {"actor_selection_info": {}, "syncs": {}}},
            RolloutActorSelectionInfo(
                num_actors=0,
                num_pinned_to_connector_rollout=0,
                num_actors_eligible_or_already_pinned=0,
            ),
            [],
            id="missing_fields_defaults_to_zero",
        ),
    ],
)
def test_query_prod_rollout_monitoring_stats(
    api_response: dict,
    expected_selection_info: RolloutActorSelectionInfo,
    expected_sync_stats: list[RolloutActorSyncStats],
) -> None:
    """Test query_prod_rollout_monitoring_stats transforms API response correctly."""
    mock_ctx = MagicMock()
    mock_ctx.request_context.lifespan_context = {}

    with patch(
        "airbyte_ops_mcp.mcp.connector_versions._resolve_cloud_auth"
    ) as mock_resolve_auth, patch(
        "airbyte_ops_mcp.mcp.connector_versions.api_client.get_actor_sync_info"
    ) as mock_get_sync_info:
        mock_resolve_auth.return_value = MagicMock(
            bearer_token="test-token", client_id=None, client_secret=None
        )
        mock_get_sync_info.return_value = api_response

        result = query_prod_rollout_monitoring_stats(
            rollout_id="test-rollout-id", ctx=mock_ctx
        )

        assert isinstance(result, RolloutMonitoringResult)
        assert result.rollout_id == "test-rollout-id"
        assert result.actor_selection_info == expected_selection_info

        assert len(result.actor_sync_stats) == len(expected_sync_stats)
        for actual, expected in zip(
            sorted(result.actor_sync_stats, key=lambda x: x.actor_id),
            sorted(expected_sync_stats, key=lambda x: x.actor_id),
        ):
            assert actual == expected


@pytest.mark.unit
def test_get_actor_sync_info_api_call() -> None:
    """Test get_actor_sync_info makes correct API call."""
    with patch(
        "airbyte_ops_mcp.cloud_admin.api_client._get_access_token"
    ) as mock_get_token, patch(
        "airbyte_ops_mcp.cloud_admin.api_client.requests.post"
    ) as mock_post:
        mock_get_token.return_value = "test-access-token"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"actor_selection_info": {}, "syncs": {}}
        }
        mock_post.return_value = mock_response

        result = get_actor_sync_info(
            rollout_id="test-rollout-id",
            config_api_root="https://api.test.com",
            bearer_token="test-token",
        )

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert (
            call_args[0][0]
            == "https://api.test.com/connector_rollout/get_actor_sync_info"
        )
        assert call_args[1]["json"] == {"id": "test-rollout-id"}
        assert "Authorization" in call_args[1]["headers"]
        assert result == {"data": {"actor_selection_info": {}, "syncs": {}}}


@pytest.mark.unit
def test_get_actor_sync_info_non_json_body() -> None:
    """A 200 with a non-JSON body raises the documented `PyAirbyteInputError`.

    `requests`' `response.json()` raises on an unparseable body; this must be
    normalized to `PyAirbyteInputError` so the eligibility guards that catch it
    (both the fall-through pre-checks and the error-recording handlers) behave
    as documented rather than leaking a raw decode error.
    """
    with patch(
        "airbyte_ops_mcp.cloud_admin.api_client._get_access_token"
    ) as mock_get_token, patch(
        "airbyte_ops_mcp.cloud_admin.api_client.requests.post"
    ) as mock_post:
        mock_get_token.return_value = "test-access-token"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>gateway error</html>"
        mock_response.json.side_effect = ValueError("Expecting value")
        mock_post.return_value = mock_response

        with pytest.raises(PyAirbyteInputError, match="not valid JSON"):
            get_actor_sync_info(
                rollout_id="test-rollout-id",
                config_api_root="https://api.test.com",
                bearer_token="test-token",
            )


@pytest.mark.unit
def test_get_actor_sync_info_not_found() -> None:
    """Test get_actor_sync_info raises error when rollout not found."""
    with patch(
        "airbyte_ops_mcp.cloud_admin.api_client._get_access_token"
    ) as mock_get_token, patch(
        "airbyte_ops_mcp.cloud_admin.api_client.requests.post"
    ) as mock_post:
        mock_get_token.return_value = "test-access-token"
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_post.return_value = mock_response

        with pytest.raises(PyAirbyteInputError, match="Rollout not found"):
            get_actor_sync_info(
                rollout_id="nonexistent-rollout",
                config_api_root="https://api.test.com",
                bearer_token="test-token",
            )
