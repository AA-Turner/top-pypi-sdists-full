# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the GitHub webhook handler."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from unittest.mock import MagicMock, patch

from agent_message_bus.devin_client import INJECT_OK
from agent_message_bus.github_handler import handle_github_webhook
from agent_message_bus.models import Subscription, WatchEvent

SESSION_URL = "https://app.devin.ai/sessions/abc123"
ISSUE_URL = "https://github.com/airbytehq/airbyte-ops-mcp/issues/1357"


def _subscription(**overrides: Any) -> Subscription:
    now = datetime.now(tz=timezone.utc)
    data: dict[str, Any] = {
        "id": "sub-1",
        "github_url": ISSUE_URL,
        "owner": "airbytehq",
        "repo": "airbyte-ops-mcp",
        "number": 1357,
        "session_url": SESSION_URL,
        "session_id": "abc123",
        "type": "issue",
        "watch_events": [WatchEvent.COMMENT],
        "created_at": now,
        "expires_at": now + timedelta(hours=1),
    }
    data.update(overrides)
    return Subscription(**data)


def _comment_payload(sender_type: str) -> dict[str, Any]:
    return {
        "action": "created",
        "sender": {"login": "devin-ai-integration[bot]", "type": sender_type},
        "repository": {"owner": {"login": "airbytehq"}, "name": "airbyte-ops-mcp"},
        "issue": {"number": 1357},
        "comment": {"id": 42, "body": "hello"},
    }


def _store_with(*subs: Subscription) -> MagicMock:
    store = MagicMock()
    store.find_by_issue.return_value = list(subs)
    return store


def test_bot_sender_is_notified() -> None:
    store = _store_with(_subscription())
    with patch("agent_message_bus.github_handler.inject_message", return_value=INJECT_OK) as inject:
        result = handle_github_webhook("issue_comment", _comment_payload("Bot"), store)

    assert result["status"] == "processed"
    assert result["notified"] == 1
    inject.assert_called_once()
    assert inject.call_args.args[0] == SESSION_URL
    assert "@devin-ai-integration[bot]" in inject.call_args.args[1]


def test_user_sender_is_notified() -> None:
    store = _store_with(_subscription())
    with patch("agent_message_bus.github_handler.inject_message", return_value=INJECT_OK):
        result = handle_github_webhook("issue_comment", _comment_payload("User"), store)

    assert result["status"] == "processed"
    assert result["notified"] == 1
