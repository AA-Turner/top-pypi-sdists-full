# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for `plain_text_input` forwarding in Slack interactions."""

from __future__ import annotations

import json
from typing import Any

from agent_message_bus import slack_handler
from agent_message_bus.devin_client import INJECT_OK
from agent_message_bus.slack_handler import (
    _extract_typed_text,
    _format_slack_notification,
    handle_slack_interaction,
)

SESSION_URL = "https://app.devin.ai/sessions/abc"


def _action() -> dict[str, Any]:
    return {
        "action_id": "defer_reason",
        "type": "button",
        "text": {"type": "plain_text", "text": "Needs canary"},
        "value": json.dumps({"session_url": SESSION_URL}),
    }


def _user() -> dict[str, Any]:
    return {"id": "U123", "name": "octocat"}


def test_format_notification_without_typed_text_is_unchanged() -> None:
    notification = _format_slack_notification(_action(), _user(), "pick a reason")

    assert notification == (
        "Slack action received: @octocat clicked 'Needs canary'"
        "\n\nOriginal message context: pick a reason"
    )


def test_format_notification_with_typed_text() -> None:
    notification = _format_slack_notification(
        _action(), _user(), "pick a reason", typed_text=[("note", "needs canary")]
    )

    assert notification == (
        "Slack action received: @octocat clicked 'Needs canary'"
        "\n\nText entered in the message (note): needs canary"
        "\n\nOriginal message context: pick a reason"
    )


def test_format_notification_labels_each_input() -> None:
    notification = _format_slack_notification(
        _action(),
        _user(),
        typed_text=[("note", "first"), ("reason_detail", "second")],
    )

    assert notification == (
        "Slack action received: @octocat clicked 'Needs canary'"
        "\n\nText entered in the message (note): first"
        "\n\nText entered in the message (reason_detail): second"
    )


def test_extract_typed_text_missing_state() -> None:
    assert _extract_typed_text({}) == []
    assert _extract_typed_text({"state": None}) == []
    assert _extract_typed_text({"state": {"values": "nope"}}) == []


def test_extract_typed_text_skips_non_inputs_and_blank_values() -> None:
    payload = {
        "state": {
            "values": {
                "block-1": {
                    "note": {"type": "plain_text_input", "value": "   "},
                    "other": {"type": "plain_text_input", "value": None},
                    "btn": {"type": "button", "value": "clicked"},
                }
            }
        }
    }
    assert _extract_typed_text(payload) == []


def test_extract_typed_text_returns_values_in_order() -> None:
    payload = {
        "state": {
            "values": {
                "block-1": {"a": {"type": "plain_text_input", "value": " first "}},
                "block-2": {"b": {"type": "plain_text_input", "value": "second"}},
            }
        }
    }
    assert _extract_typed_text(payload) == [("a", "first"), ("b", "second")]


def test_handle_slack_interaction_forwards_typed_text(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def fake_inject(session_url: str, message: str) -> str:
        captured["session_url"] = session_url
        captured["message"] = message
        return INJECT_OK

    monkeypatch.setattr(slack_handler, "inject_message", fake_inject)
    monkeypatch.setattr(slack_handler, "_update_message_after_action", lambda **kwargs: None)

    payload = {
        "type": "block_actions",
        "user": _user(),
        "actions": [_action()],
        "message": {"text": "pick a reason", "ts": "1234.5678"},
        "channel": {"id": "C123"},
        "response_url": "https://hooks.slack.com/actions/xxx",
        "state": {
            "values": {
                "note-block": {"note": {"type": "plain_text_input", "value": "needs canary"}}
            }
        },
    }

    result = handle_slack_interaction(payload)

    assert result["notified"] == 1
    assert captured["session_url"] == SESSION_URL
    assert "Text entered in the message (note): needs canary" in captured["message"]
