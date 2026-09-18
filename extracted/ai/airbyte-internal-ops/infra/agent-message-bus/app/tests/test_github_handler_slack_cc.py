# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for `slack_users_cc` handling in GitHub webhook notifications."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from agent_message_bus.devin_client import INJECT_OK
from agent_message_bus.github_handler import handle_github_webhook
from agent_message_bus.models import Subscription, WatchEvent

SESSION_URL = "https://app.devin.ai/sessions/abc123"
ISSUE_URL = "https://github.com/airbytehq/airbyte-ops-mcp/issues/1357"


def _subscription(slack_users_cc: str | None) -> Subscription:
    now = datetime.now(tz=timezone.utc)
    return Subscription(
        id="sub-1",
        github_url=ISSUE_URL,
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        number=1357,
        session_url=SESSION_URL,
        session_id="abc123",
        type="issue",
        watch_events=[WatchEvent.COMMENT],
        created_at=now,
        expires_at=now + timedelta(hours=1),
        slack_users_cc=slack_users_cc,
    )


def _comment_payload() -> dict[str, Any]:
    return {
        "action": "created",
        "sender": {"login": "octocat", "type": "User"},
        "repository": {"owner": {"login": "airbytehq"}, "name": "airbyte-ops-mcp"},
        "issue": {"number": 1357},
        "comment": {"id": 42, "body": "hello"},
    }


@pytest.mark.parametrize(
    "slack_users_cc,expected_suffix",
    [
        pytest.param("<@U123>, <@U456>", "\n\nCC: <@U123>, <@U456>", id="cc_set"),
        pytest.param(None, None, id="cc_unset"),
        pytest.param("", None, id="cc_empty"),
    ],
)
def test_notification_includes_slack_cc(
    slack_users_cc: str | None, expected_suffix: str | None
) -> None:
    store = MagicMock()
    store.find_by_issue.return_value = [_subscription(slack_users_cc)]
    with patch("agent_message_bus.github_handler.inject_message", return_value=INJECT_OK) as inject:
        result = handle_github_webhook("issue_comment", _comment_payload(), store)

    assert result["notified"] == 1
    message = inject.call_args.args[1]
    if expected_suffix is None:
        assert "CC:" not in message
    else:
        assert message.endswith(expected_suffix)
