# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for Zendesk spam alerts."""

from __future__ import annotations

import pytest
import requests

from airbyte_ops_mcp import slack_posting
from airbyte_ops_mcp.mcp import zendesk_ops
from airbyte_ops_mcp.slack_api import SlackAPIError
from airbyte_ops_mcp.slack_posting import SlackPostResult, post_channel_message


@pytest.mark.unit
def test_notify_zendesk_spam_ticket_posts_alert(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    posted: list[tuple[str, str]] = []

    def _post(channel: str, text: str) -> SlackPostResult:
        posted.append((channel, text))
        return SlackPostResult(channel_id="C123", ts="123.456")

    monkeypatch.setattr(zendesk_ops, "post_channel_message", _post)
    monkeypatch.setenv("ZENDESK_SUBDOMAIN", "airbyte1416")

    result = zendesk_ops.notify_zendesk_spam_ticket(
        ticket_id=42,
        reason="Repeated unsolicited advertising.",
        subject="Product offer",
        agent_session_url="https://app.devin.ai/sessions/abc",
    )

    assert result.success is True
    assert result.ticket_id == 42
    assert result.slack_permalink == (
        "https://airbytehq-team.slack.com/archives/C123/p123456"
    )
    assert len(posted) == 1
    channel, text = posted[0]
    assert channel == "C02U1H7M71A"
    assert ":spam:" in text
    assert "https://airbyte1416.zendesk.com/agent/tickets/42|#42" in text
    for user_id in zendesk_ops._SPAM_ALERT_MENTION_IDS:
        assert f"<@{user_id}>" in text
    assert "*Reason:* Repeated unsolicited advertising." in text
    assert "<https://app.devin.ai/sessions/abc|Devin session>" in text


@pytest.mark.unit
def test_notify_zendesk_spam_ticket_escapes_subject_and_reason(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    posted: list[str] = []
    monkeypatch.setattr(
        zendesk_ops,
        "post_channel_message",
        lambda channel, text: (
            posted.append(text) or SlackPostResult(channel_id="C123", ts="123.456")
        ),
    )

    result = zendesk_ops.notify_zendesk_spam_ticket(
        ticket_id=42,
        reason="<script>&",
        subject="<script>&",
    )

    assert result.success is True
    assert ": &lt;script&gt;&amp; as spam." in posted[0]
    assert "*Reason:* &lt;script&gt;&amp;" in posted[0]


@pytest.mark.unit
def test_notify_zendesk_spam_ticket_omits_session_line_without_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    posted: list[str] = []
    monkeypatch.setattr(
        zendesk_ops,
        "post_channel_message",
        lambda channel, text: (
            posted.append(text) or SlackPostResult(channel_id="C123", ts="123.456")
        ),
    )

    zendesk_ops.notify_zendesk_spam_ticket(ticket_id=42, reason="Spam.")

    assert "Devin session" not in posted[0]


@pytest.mark.unit
def test_notify_zendesk_spam_ticket_omits_unsafe_session_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    posted: list[str] = []
    monkeypatch.setattr(
        zendesk_ops,
        "post_channel_message",
        lambda channel, text: (
            posted.append(text) or SlackPostResult(channel_id="C123", ts="123.456")
        ),
    )

    result = zendesk_ops.notify_zendesk_spam_ticket(
        ticket_id=42,
        reason="Spam.",
        agent_session_url=(
            "https://app.devin.ai/sessions/abc> <!channel> <https://example.com"
        ),
    )

    assert result.success is True
    assert len(posted) == 1
    assert "<!channel>" not in posted[0]
    assert "Devin session" not in posted[0]


@pytest.mark.unit
def test_notify_zendesk_spam_ticket_escapes_session_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    posted: list[str] = []
    monkeypatch.setattr(
        zendesk_ops,
        "post_channel_message",
        lambda channel, text: (
            posted.append(text) or SlackPostResult(channel_id="C123", ts="123.456")
        ),
    )

    result = zendesk_ops.notify_zendesk_spam_ticket(
        ticket_id=42,
        reason="Spam.",
        agent_session_url="https://app.devin.ai/sessions/abc?x=1&y=2",
    )

    assert result.success is True
    assert "<https://app.devin.ai/sessions/abc?x=1&amp;y=2|Devin session>" in posted[0]


@pytest.mark.unit
def test_notify_zendesk_spam_ticket_uses_plain_id_without_subdomain(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    posted: list[str] = []
    monkeypatch.delenv("ZENDESK_SUBDOMAIN", raising=False)
    monkeypatch.setattr(
        zendesk_ops,
        "post_channel_message",
        lambda channel, text: (
            posted.append(text) or SlackPostResult(channel_id="C123", ts="123.456")
        ),
    )

    zendesk_ops.notify_zendesk_spam_ticket(ticket_id=42, reason="Spam.")

    assert "ticket #42 as spam." in posted[0]
    assert "zendesk.com" not in posted[0]


@pytest.mark.unit
def test_notify_zendesk_spam_ticket_returns_slack_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(channel: str, text: str) -> SlackPostResult:
        raise SlackAPIError("Slack unavailable")

    monkeypatch.setattr(zendesk_ops, "post_channel_message", _raise)

    result = zendesk_ops.notify_zendesk_spam_ticket(ticket_id=42, reason="Spam.")

    assert result.success is False
    assert result.message == "Slack unavailable"
    assert result.slack_permalink is None


@pytest.mark.unit
def test_notify_zendesk_spam_ticket_returns_transport_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(channel: str, text: str) -> SlackPostResult:
        raise requests.ConnectionError("boom")

    monkeypatch.setattr(zendesk_ops, "post_channel_message", _raise)

    result = zendesk_ops.notify_zendesk_spam_ticket(ticket_id=42, reason="Spam.")

    assert result.success is False
    assert "boom" in result.message


@pytest.mark.unit
def test_notify_zendesk_spam_ticket_returns_missing_token_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)
    monkeypatch.delenv("SLACK_BOT_TOKEN_HITL", raising=False)
    monkeypatch.setattr(
        slack_posting,
        "_post_message",
        lambda *args, **kwargs: slack_posting._resolve_slack_bot_token(),
    )
    monkeypatch.setattr(zendesk_ops, "post_channel_message", post_channel_message)

    result = zendesk_ops.notify_zendesk_spam_ticket(ticket_id=42, reason="Spam.")

    assert result.success is False
    assert "No Slack bot token found." in result.message
