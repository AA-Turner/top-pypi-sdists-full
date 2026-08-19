# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the connector rollout monitoring API-based tool."""

from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from unittest.mock import MagicMock, patch

import pytest
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.cloud_admin.api_client import (
    get_actor_sync_info,
    pause_connector_rollout,
)
from airbyte_ops_mcp.connector_ops.rollouts.state_transitions import (
    pause_rollout,
    unpause_rollout,
)
from airbyte_ops_mcp.mcp.connector_versions import (
    RolloutActorSelectionInfo,
    RolloutActorSyncStats,
    RolloutMonitoringResult,
    query_prod_rollout_monitoring_stats,
)
from airbyte_ops_mcp.mcp.connector_versions import (
    pause_connector_rollout as pause_connector_rollout_tool,
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
def test_pause_connector_rollout_uses_manual_pause_payload() -> None:
    """Pause sends the state and reason fields without a finalize pin flag."""
    with patch(
        "airbyte_ops_mcp.cloud_admin.api_client._get_access_token",
        return_value="test-access-token",
    ), patch("airbyte_ops_mcp.cloud_admin.api_client.requests.post") as mock_post:
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"state": "paused"}
        mock_post.return_value = mock_response

        result = pause_connector_rollout(
            docker_repository="airbyte/source-faker",
            docker_image_tag="7.2.0-rc.1",
            actor_definition_id="actor-definition",
            rollout_id="rollout-id",
            updated_by="user-id",
            paused_reason="Failure threshold exceeded: 2 failures (threshold=1)",
            config_api_root="https://api.test.com",
            bearer_token="test-token",
        )

        assert result == {"state": "paused"}
        assert mock_post.call_args.kwargs["json"] == {
            "docker_repository": "airbyte/source-faker",
            "docker_image_tag": "7.2.0-rc.1",
            "actor_definition_id": "actor-definition",
            "id": "rollout-id",
            "state": "paused",
            "paused_reason": "Failure threshold exceeded: 2 failures (threshold=1)",
            "updated_by": "user-id",
        }


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


_CLOUD_AUTH_PATCHES = (
    (
        "airbyte_ops_mcp.mcp.connector_versions.require_internal_admin_flag_only",
        None,
    ),
    (
        "airbyte_ops_mcp.mcp.connector_versions._resolve_cloud_auth",
        MagicMock(bearer_token="test-token", client_id=None, client_secret=None),
    ),
    (
        "airbyte_ops_mcp.mcp.connector_versions.api_client.get_user_id_by_email",
        "user-uuid",
    ),
)


@contextmanager
def _patched_cloud_auth() -> Iterator[None]:
    """Patch the admin gate, cloud auth, and email lookup the rollout tools share."""
    with ExitStack() as stack:
        for target, return_value in _CLOUD_AUTH_PATCHES:
            stack.enter_context(patch(target, return_value=return_value))
        yield


@pytest.mark.unit
@pytest.mark.parametrize(
    "tool_kwargs,transition,transition_result,expect_call,expected_fragment",
    [
        pytest.param(
            {"paused_reason": "  Sync failures on TIER_2  "},
            "pause_rollout",
            None,
            True,
            "Sync failures on TIER_2",
            id="pause_normalizes_the_reason_and_attributes_the_user",
        ),
        pytest.param(
            {"paused_reason": "   "},
            "pause_rollout",
            None,
            False,
            "paused_reason is required",
            id="pause_rejects_a_blank_reason",
        ),
        pytest.param(
            {"unpause": True},
            "unpause_rollout",
            (20, {}),
            True,
            "resumed rollout",
            id="unpause_needs_no_reason",
        ),
        pytest.param(
            {"unpause": True, "paused_reason": "not applicable"},
            "unpause_rollout",
            None,
            False,
            "does not apply",
            id="unpause_rejects_a_reason_rather_than_dropping_it",
        ),
        pytest.param(
            {"unpause": True},
            "unpause_rollout",
            PyAirbyteInputError(message="rollout is not paused"),
            True,
            "rollout is not paused",
            id="unpause_reports_an_api_failure_as_an_unsuccessful_result",
        ),
    ],
)
def test_pause_connector_rollout_tool_pauses_unpauses_and_guards(
    tool_kwargs: dict[str, object],
    transition: str,
    transition_result: object,
    expect_call: bool,
    expected_fragment: str,
) -> None:
    """One tool covers both transitions, each with its own required inputs."""
    mock_ctx = MagicMock()
    mock_ctx.request_context.lifespan_context = {}
    raises = isinstance(transition_result, Exception)

    with _patched_cloud_auth(), patch(
        f"airbyte_ops_mcp.mcp.connector_versions.{transition}",
        side_effect=transition_result if raises else None,
        return_value=None if raises else transition_result,
    ) as mock_transition:
        result = pause_connector_rollout_tool(
            docker_repository="airbyte/source-faker",
            docker_image_tag="7.2.0-rc.1",
            actor_definition_id="actor-definition",
            rollout_id="rollout-id",
            admin_user_email="ops@airbyte.io",
            ctx=mock_ctx,
            **tool_kwargs,
        )

    assert result.success is (expect_call and not raises)
    assert expected_fragment in (result.message or "") or expected_fragment == (
        result.paused_reason
    )
    assert mock_transition.called is expect_call
    if expect_call and not raises:
        assert mock_transition.call_args.kwargs["updated_by"] == "user-uuid"
        assert "current_target_percentage" not in mock_transition.call_args.kwargs


@pytest.mark.unit
@pytest.mark.parametrize(
    "current_target_percentage,expected_target",
    [
        pytest.param(20, 20, id="resumes_at_current_pct_pinning_nobody_new"),
        pytest.param(0, 1, id="nothing_pinned_yet_resumes_at_one_pct"),
        pytest.param(None, 1, id="missing_pct_resumes_at_one_pct"),
    ],
)
def test_unpause_rollout_resumes_at_the_rollouts_own_percentage(
    current_target_percentage: int | None,
    expected_target: int,
) -> None:
    """Callers never supply a percentage: it is read from the rollout itself."""
    with patch(
        "airbyte_ops_mcp.connector_ops.rollouts.state_transitions.api_client.get_connector_rollout",
        return_value={"current_target_rollout_pct": current_target_percentage},
    ), patch(
        "airbyte_ops_mcp.connector_ops.rollouts.state_transitions.api_client.progress_connector_rollout"
    ) as mock_progress:
        resume_percentage, _ = unpause_rollout(
            docker_repository="airbyte/source-faker",
            docker_image_tag="7.2.0-rc.1",
            actor_definition_id="actor-definition",
            rollout_id="rollout-id",
            updated_by="user-id",
            config_api_root="https://api.test.com",
            bearer_token="test-token",
        )

    assert resume_percentage == expected_target
    assert mock_progress.call_args.kwargs["target_percentage"] == expected_target


@pytest.mark.unit
def test_pause_rollout_requires_a_reason() -> None:
    """The business layer refuses an unexplained hold, whatever the caller."""
    with patch(
        "airbyte_ops_mcp.connector_ops.rollouts.state_transitions.api_client.pause_connector_rollout"
    ) as mock_pause, pytest.raises(PyAirbyteInputError, match="reason is required"):
        pause_rollout(
            docker_repository="airbyte/source-faker",
            docker_image_tag="7.2.0-rc.1",
            actor_definition_id="actor-definition",
            rollout_id="rollout-id",
            updated_by="user-id",
            paused_reason="   ",
            config_api_root="https://api.test.com",
            bearer_token="test-token",
        )

    mock_pause.assert_not_called()
