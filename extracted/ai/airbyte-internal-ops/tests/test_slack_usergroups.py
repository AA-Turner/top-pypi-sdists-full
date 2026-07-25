# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for Slack usergroup lookup."""

from unittest.mock import MagicMock, patch

import pytest
from slack_sdk.errors import SlackApiError

from airbyte_ops_mcp.mcp.human_in_the_loop import lookup_slack_usergroup
from airbyte_ops_mcp.slack_api import (
    SlackAPIError,
    SlackUsergroup,
    list_slack_usergroups,
)
from airbyte_ops_mcp.slack_api import (
    lookup_slack_usergroup as lookup_slack_usergroups,
)


@pytest.mark.unit
@patch("airbyte_ops_mcp.slack_api.WebClient")
def test_list_slack_usergroups(mock_web_client: MagicMock) -> None:
    mock_web_client.return_value.usergroups_list.return_value = {
        "usergroups": [
            {
                "id": "S123",
                "handle": "oc-apis",
                "name": "API Oncall",
                "description": "API connector oncall",
                "users": ["U1", "U2"],
            }
        ]
    }

    result = list_slack_usergroups(token="xoxb-token")

    assert result == [
        SlackUsergroup(
            id="S123",
            handle="oc-apis",
            name="API Oncall",
            description="API connector oncall",
            user_count=2,
        )
    ]
    mock_web_client.return_value.usergroups_list.assert_called_once_with(
        include_disabled=False, include_users=True
    )


@pytest.mark.unit
@patch("airbyte_ops_mcp.slack_api.list_slack_usergroups")
def test_lookup_slack_usergroup_matches_handle_or_name(
    mock_list_usergroups: MagicMock,
) -> None:
    mock_list_usergroups.return_value = [
        SlackUsergroup("S1", "oc-apis", "APIs Oncall", "", 3),
        SlackUsergroup("S2", "oc-platform", "Platform Oncall", "", 4),
    ]

    result = lookup_slack_usergroup("@API")

    assert result.id_or_handle == "@API"
    assert result.total_matches == 1
    assert result.matches[0].id == "S1"


@pytest.mark.unit
@patch("airbyte_ops_mcp.slack_api.list_slack_usergroups")
def test_lookup_slack_usergroup_matches_exact_id(
    mock_list_usergroups: MagicMock,
) -> None:
    mock_list_usergroups.return_value = [
        SlackUsergroup("S0BKR63VAN5", "oc-internal-ai", "Internal AI", "", 3),
        SlackUsergroup("S0BKLTJNKC6", "oc-db-dw", "DB/DW", "", 4),
    ]

    result = lookup_slack_usergroups("S0BKR63VAN5")

    assert result == [
        SlackUsergroup("S0BKR63VAN5", "oc-internal-ai", "Internal AI", "", 3)
    ]


@pytest.mark.unit
@patch("airbyte_ops_mcp.slack_api.list_slack_usergroups")
def test_lookup_slack_usergroup_rejects_blank_id_or_handle(
    mock_list_usergroups: MagicMock,
) -> None:
    with pytest.raises(ValueError, match="id_or_handle must be non-empty"):
        lookup_slack_usergroups("  ")

    mock_list_usergroups.assert_not_called()


@pytest.mark.unit
@patch("airbyte_ops_mcp.slack_api.list_slack_usergroups")
def test_mcp_lookup_slack_usergroup_rejects_blank_id_or_handle(
    mock_list_usergroups: MagicMock,
) -> None:
    with pytest.raises(ValueError, match="id_or_handle must be non-empty"):
        lookup_slack_usergroup("")

    mock_list_usergroups.assert_not_called()


@pytest.mark.unit
@patch("airbyte_ops_mcp.slack_api.WebClient")
def test_list_slack_usergroups_missing_scope(mock_web_client: MagicMock) -> None:
    mock_web_client.return_value.usergroups_list.side_effect = SlackApiError(
        message="missing scope",
        response={"ok": False, "error": "missing_scope"},
    )

    with pytest.raises(SlackAPIError, match="usergroups:read"):
        list_slack_usergroups(token="xoxb-token")
