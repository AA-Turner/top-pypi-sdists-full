"""Tests for the Telegram and Discord message bridges.

Sage already has an iMessage bridge (sms_manager.py). These two bridges
expand the same surface area to Telegram and Discord — common platforms
for AI assistants and the ones OpenClaw highlights.

Design: each bridge is a thin adapter that translates inbound platform
messages into a sage prompt, runs them through the existing chat handler,
and sends the reply back. The agent loop is identical across bridges —
only the I/O layer differs.

TDD: tests describe the inbound-message → agent-call → outbound-reply
contract. Network plumbing (long-poll for Telegram, websocket for
Discord) is exercised separately via integration tests once we have
keys/tokens.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from sage.core.messaging_bridges import (
    BridgeMessage,
    DiscordBridge,
    TelegramBridge,
)


# ── Shared message type ──────────────────────────────────────────────────────


class TestBridgeMessage:
    def test_message_has_core_fields(self):
        m = BridgeMessage(
            platform="telegram",
            chat_id="123",
            sender_id="user-456",
            sender_name="Layne",
            text="hi sage",
        )
        assert m.platform == "telegram"
        assert m.text == "hi sage"
        assert m.sender_name == "Layne"


# ── TelegramBridge ──────────────────────────────────────────────────────────


class TestTelegramBridge:
    def _bridge(self, *, agent=None, sender=None):
        return TelegramBridge(
            agent=agent or MagicMock(return_value="default agent reply"),
            send_message=sender or MagicMock(),
            allowed_chat_ids=frozenset({"123"}),
        )

    def test_inbound_message_routed_to_agent(self):
        agent = MagicMock(return_value="sage answer")
        sender = MagicMock()
        bridge = self._bridge(agent=agent, sender=sender)
        bridge.handle_inbound({
            "message": {
                "chat": {"id": 123, "type": "private"},
                "from": {"id": 456, "first_name": "Layne"},
                "text": "what is 2+2?",
            },
        })
        agent.assert_called_once()
        # Reply goes back to the originating chat
        sender.assert_called_once_with(chat_id=123, text="sage answer")

    def test_unauthorized_chat_id_silently_ignored(self):
        agent = MagicMock(return_value="should not be called")
        sender = MagicMock()
        bridge = TelegramBridge(
            agent=agent, send_message=sender,
            allowed_chat_ids=frozenset({"123"}),
        )
        bridge.handle_inbound({
            "message": {
                "chat": {"id": 999, "type": "private"},
                "from": {"id": 1, "first_name": "Spammer"},
                "text": "let me in",
            },
        })
        agent.assert_not_called()
        sender.assert_not_called()

    def test_missing_text_message_ignored(self):
        agent = MagicMock()
        bridge = self._bridge(agent=agent)
        # Sticker / photo / etc. — no `text` field
        bridge.handle_inbound({
            "message": {
                "chat": {"id": 123, "type": "private"},
                "from": {"id": 1, "first_name": "L"},
                "sticker": {"file_id": "x"},
            },
        })
        agent.assert_not_called()

    def test_bridge_replies_carry_long_responses_intact(self):
        """Telegram's 4096-char limit per message means long agent replies
        get split into multiple sends. The bridge handles this."""
        long_text = "x" * 5000
        agent = MagicMock(return_value=long_text)
        sender = MagicMock()
        bridge = self._bridge(agent=agent, sender=sender)
        bridge.handle_inbound({
            "message": {
                "chat": {"id": 123, "type": "private"},
                "from": {"id": 1, "first_name": "L"},
                "text": "give me a long answer",
            },
        })
        # Should have called send_message at least twice (5000 > 4096)
        assert sender.call_count >= 2


# ── DiscordBridge ───────────────────────────────────────────────────────────


class TestDiscordBridge:
    def _bridge(self, *, agent=None, sender=None):
        return DiscordBridge(
            agent=agent or MagicMock(return_value="reply"),
            send_message=sender or MagicMock(),
            allowed_channel_ids=frozenset({"chan-123"}),
        )

    def test_dm_message_routed_to_agent(self):
        agent = MagicMock(return_value="answer")
        sender = MagicMock()
        bridge = self._bridge(agent=agent, sender=sender)
        bridge.handle_inbound({
            "channel_id": "chan-123",
            "author": {"id": "user-1", "username": "layne"},
            "content": "hey sage",
        })
        agent.assert_called_once()
        sender.assert_called_once_with(channel_id="chan-123", text="answer")

    def test_message_from_bot_self_ignored(self):
        """Don't reply to our own messages (would cause infinite loop)."""
        agent = MagicMock()
        bridge = DiscordBridge(
            agent=agent,
            send_message=MagicMock(),
            allowed_channel_ids=frozenset({"chan-123"}),
            bot_user_id="bot-self",
        )
        bridge.handle_inbound({
            "channel_id": "chan-123",
            "author": {"id": "bot-self", "username": "sage-bot"},
            "content": "from myself",
        })
        agent.assert_not_called()

    def test_message_in_unauthorized_channel_ignored(self):
        agent = MagicMock()
        bridge = self._bridge(agent=agent)
        bridge.handle_inbound({
            "channel_id": "wrong-channel",
            "author": {"id": "u-1", "username": "x"},
            "content": "hey",
        })
        agent.assert_not_called()

    def test_long_replies_split_to_discord_2000_char_limit(self):
        """Discord caps individual messages at 2000 chars."""
        long_text = "x" * 5500
        agent = MagicMock(return_value=long_text)
        sender = MagicMock()
        bridge = self._bridge(agent=agent, sender=sender)
        bridge.handle_inbound({
            "channel_id": "chan-123",
            "author": {"id": "u-1", "username": "x"},
            "content": "long please",
        })
        # 5500 chars / 2000 per send → 3 messages
        assert sender.call_count >= 3


# ── Allow-list behavior (shared concern) ─────────────────────────────────────


class TestAllowlistEnforcement:
    """Both bridges must hard-default to an empty allow-list. Sage shouldn't
    answer random strangers messaging it — bridge is opt-in per chat."""

    def test_telegram_empty_allowlist_rejects_everything(self):
        agent = MagicMock()
        bridge = TelegramBridge(
            agent=agent, send_message=MagicMock(),
            allowed_chat_ids=frozenset(),
        )
        bridge.handle_inbound({
            "message": {
                "chat": {"id": 1, "type": "private"},
                "from": {"id": 1, "first_name": "X"},
                "text": "hi",
            },
        })
        agent.assert_not_called()

    def test_discord_empty_allowlist_rejects_everything(self):
        agent = MagicMock()
        bridge = DiscordBridge(
            agent=agent, send_message=MagicMock(),
            allowed_channel_ids=frozenset(),
        )
        bridge.handle_inbound({
            "channel_id": "any",
            "author": {"id": "u", "username": "x"},
            "content": "hey",
        })
        agent.assert_not_called()
