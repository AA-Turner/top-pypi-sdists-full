"""Telegram + Discord message bridges.

Mirrors sage's existing iMessage bridge (sms_manager.py) for two more
platforms. The agent-call layer is identical — what differs is only the
inbound parsing + outbound chunking. Each bridge is intentionally thin:
parse → authorize → call agent → split & send.

Security default: BOTH bridges require an explicit allow-list of chat or
channel IDs at construction time. Empty allow-list = bridge rejects
everything. Sage will never auto-respond to a stranger who finds the bot's
username.

This file contains *only* the message-routing layer. Long-poll loop
(Telegram) and Gateway websocket (Discord) live in their own runner
modules so we can unit-test the routing without standing up real network
clients.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable

logger = logging.getLogger("sage.messaging_bridges")


# Platform message-length limits. Replies longer than these get split.
_TELEGRAM_MAX_CHARS = 4096
_DISCORD_MAX_CHARS = 2000


# ── Shared message type ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class BridgeMessage:
    """Normalised inbound message — what the agent sees regardless of source."""
    platform: str  # "telegram" | "discord" | "imessage"
    chat_id: str
    sender_id: str
    sender_name: str
    text: str


# Type aliases for clarity.
# Agent fn: (BridgeMessage) -> reply-text (sync, returns full response).
AgentFn = Callable[[BridgeMessage], str]


# ── Telegram ─────────────────────────────────────────────────────────────────


class TelegramBridge:
    """Routes Telegram messages to the sage agent and sends replies back.

    Wire it up with the python-telegram-bot library (or the raw Bot API);
    the parsing in ``handle_inbound`` matches Telegram's update schema.
    """

    def __init__(
        self,
        *,
        agent: AgentFn,
        send_message: Callable[..., None],
        allowed_chat_ids: frozenset[str],
    ):
        # ``send_message(chat_id, text)`` — caller provides the actual
        # network call. Lets us swap a real client for a dummy/fake in tests.
        self._agent = agent
        self._send = send_message
        self._allowed = {str(x) for x in allowed_chat_ids}

    def handle_inbound(self, update: dict) -> None:
        """Process one Telegram update. Idempotent — call repeatedly with
        the same payload safely (no side-effects beyond the agent + send)."""
        message = update.get("message") or {}
        chat = message.get("chat") or {}
        sender = message.get("from") or {}
        text = message.get("text")

        if not text:
            return  # Stickers, photos, etc. — ignore for now

        chat_id = str(chat.get("id", ""))
        if chat_id not in self._allowed:
            logger.info("Telegram: ignoring message from unauthorized chat %s", chat_id)
            return

        bridge_msg = BridgeMessage(
            platform="telegram",
            chat_id=chat_id,
            sender_id=str(sender.get("id", "")),
            sender_name=sender.get("first_name", "user"),
            text=text,
        )
        reply = self._agent(bridge_msg)
        if not reply:
            return

        # Telegram caps individual messages at 4096 chars. Split + send
        # in order. The recipient sees a sequence of messages rather than
        # one giant truncated blob.
        for chunk in _chunk_text(reply, _TELEGRAM_MAX_CHARS):
            self._send(chat_id=int(chat_id), text=chunk)


# ── Discord ──────────────────────────────────────────────────────────────────


class DiscordBridge:
    """Routes Discord messages to the sage agent and sends replies back.

    Designed to be invoked from a discord.py / disnake / Gateway-WS event
    handler. ``handle_inbound`` takes the raw event payload; the caller
    is responsible for the websocket loop.
    """

    def __init__(
        self,
        *,
        agent: AgentFn,
        send_message: Callable[..., None],
        allowed_channel_ids: frozenset[str],
        bot_user_id: str | None = None,
    ):
        self._agent = agent
        self._send = send_message
        self._allowed = {str(x) for x in allowed_channel_ids}
        # If set, messages authored by this user ID are skipped — prevents
        # infinite loops where the bot replies to its own posts.
        self._bot_user_id = bot_user_id

    def handle_inbound(self, event: dict) -> None:
        author = event.get("author") or {}
        author_id = str(author.get("id", ""))
        channel_id = str(event.get("channel_id", ""))
        text = event.get("content")

        if not text:
            return

        # Skip self-messages to avoid bot-loops
        if self._bot_user_id and author_id == self._bot_user_id:
            return

        if channel_id not in self._allowed:
            logger.info("Discord: ignoring message in unauthorized channel %s", channel_id)
            return

        bridge_msg = BridgeMessage(
            platform="discord",
            chat_id=channel_id,
            sender_id=author_id,
            sender_name=author.get("username", "user"),
            text=text,
        )
        reply = self._agent(bridge_msg)
        if not reply:
            return

        # Discord caps individual messages at 2000 chars.
        for chunk in _chunk_text(reply, _DISCORD_MAX_CHARS):
            self._send(channel_id=channel_id, text=chunk)


# ── Shared helper ────────────────────────────────────────────────────────────


def _chunk_text(text: str, max_chars: int) -> list[str]:
    """Split ``text`` into runs of at most ``max_chars`` characters.

    Splits on natural boundaries (paragraph/line/word) when possible so
    code blocks and prose don't get cut mid-word. Falls back to a hard
    character split if a single line exceeds the limit (rare).
    """
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    remaining = text
    while len(remaining) > max_chars:
        # Look for the latest paragraph break before the limit
        split_at = remaining.rfind("\n\n", 0, max_chars)
        if split_at < max_chars // 2:
            # Try single newline
            split_at = remaining.rfind("\n", 0, max_chars)
        if split_at < max_chars // 2:
            # Try word boundary
            split_at = remaining.rfind(" ", 0, max_chars)
        if split_at < max_chars // 2:
            # Last resort — hard split on character count
            split_at = max_chars
        chunks.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


__all__ = [
    "BridgeMessage",
    "TelegramBridge",
    "DiscordBridge",
]
