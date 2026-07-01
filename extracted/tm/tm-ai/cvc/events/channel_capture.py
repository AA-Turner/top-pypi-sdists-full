"""
Channel capture — emit channel.message_in / channel.message_out / channel.error.

This complements :mod:`cvc.events.chat_capture` which captures turn-level events
inside the agent loop. Channel-level events fire at the *channel boundary*
(webhook / bot receive, bot reply, channel error) so the timeline shows the
exact moment a message arrives at CVC from outside and the exact moment a
reply is sent back — even if the user message is empty (slash commands,
status pings), or if the agent crashes before any chat event fires.

All captures are best-effort — they never raise to the caller. Capture
errors are logged at DEBUG level and dropped.

Usage
-----

    from cvc.events.channel_capture import capture_message_in, capture_message_out

    # At the webhook / bot boundary, when a message arrives:
    capture_message_in(
        channel="telegram",
        actor="123456789",                  # user id (string)
        session_id="cvc_ch_telegram_98765", # (channel, chat_id, thread_id)
        summary=text[:140],
        data={
            "chat_id": chat_id,
            "thread_id": thread_id,
            "media_count": len(media),
            "is_command": inbound.is_command,
            "command": inbound.command,
            "reply_to": inbound.reply_to_message_id,
        },
    )

    # When the bot replies (or streaming finishes, or webhook returns):
    capture_message_out(
        channel="telegram",
        session_id="...",
        actor="bot",
        summary=reply_text[:140],
        data={
            "chat_id": chat_id,
            "message_id": sent_message_id,
            "length": len(reply_text),
            "streaming": True,
        },
    )

    # On any channel error (rate limit, auth fail, network):
    capture_message_error(
        channel="telegram",
        session_id="...",
        summary="telegram: 429 Too Many Requests",
        data={
            "chat_id": chat_id,
            "error_type": "rate_limit",
            "retry_after": retry_after,
        },
    )

Kind taxonomy (locked in spine)
-------------------------------
    channel.message_in      user → CVC (inbound from the outside world)
    channel.message_out     CVC → user (outbound reply from CVC)
    channel.error           channel-level failure (rate limit, auth, network, parse)

These are kept separate from chat.* events because:
  - Channel events fire at the boundary (before/after the agent loop)
  - Chat events fire inside the agent loop (per turn)
  - A single chat turn can produce multiple channel.message_out events
    (streaming drafts + final formatted reply) but exactly one chat.assistant_message
"""
from __future__ import annotations

import logging
import time
import uuid
from typing import Any, Optional

logger = logging.getLogger("cvc.events.channel_capture")


def _capture(
    *,
    kind: str,
    channel: str,
    actor: Optional[str],
    session_id: Optional[str],
    summary: Optional[str],
    data: Optional[dict[str, Any]] = None,
    workspace: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> Optional[str]:
    """Internal helper — call spine.capture with safe defaults."""
    try:
        from cvc.events.spine import capture

        # Spine requires str summary; build a sensible default if caller passed None.
        if not summary:
            data_kind = (data or {}).get("kind") or (data or {}).get("error_type") or ""
            if kind == "channel.error":
                summary = f"{channel}: error{data_kind and f' ({data_kind})'}"
            elif kind == "channel.message_in":
                summary = f"{channel}: inbound from {actor or 'unknown'}"
            elif kind == "channel.message_out":
                summary = f"{channel}: outbound to {actor or 'user'}"
            else:
                summary = f"{channel}: {kind}"

        return capture(
            kind=kind,
            channel=channel,
            actor=actor,
            session_id=session_id,
            summary=summary,
            data=data or {},
            workspace=workspace,
            tags=tags or [],
        )
    except Exception as exc:  # noqa: BLE001 — capture is best-effort
        logger.debug("channel_capture: %s capture failed: %s", kind, exc)
        return None


def capture_message_in(
    *,
    channel: str,
    actor: Optional[str] = None,
    session_id: Optional[str] = None,
    summary: Optional[str] = None,
    data: Optional[dict[str, Any]] = None,
    workspace: Optional[str] = None,
) -> Optional[str]:
    """Emit a ``channel.message_in`` event when a user message arrives at CVC.

    Fires at the channel boundary (webhook handler, bot _on_message, email
    poller, etc.) — BEFORE the agent starts thinking. This is the first
    spine event for any interaction coming from outside the dashboard.

    Args:
        channel: "telegram" | "slack" | "discord" | "whatsapp" | "email" | "matrix" | etc.
        actor: User identifier at the channel (e.g. Telegram user_id, email from-addr).
        session_id: Stable per (channel, chat_id[, thread_id]). Same value the
            chat_capture uses, so a single user message produces
            channel.message_in AND chat.session_start with the same session_id.
        summary: Short human-readable preview of the message (truncated to ~140 chars).
        data: Channel-specific metadata (chat_id, thread_id, media_count, etc.).
        workspace: Active workspace at the time of receipt. Optional —
            channel adapters may not know the workspace yet.

    Returns:
        The new event ULID, or None on capture failure.
    """
    return _capture(
        kind="channel.message_in",
        channel=channel,
        actor=actor,
        session_id=session_id,
        summary=summary,
        data=data,
        workspace=workspace,
        tags=["channel-inbound"],
    )


def capture_message_out(
    *,
    channel: str,
    actor: Optional[str] = "bot",
    session_id: Optional[str] = None,
    summary: Optional[str] = None,
    data: Optional[dict[str, Any]] = None,
    workspace: Optional[str] = None,
) -> Optional[str]:
    """Emit a ``channel.message_out`` event when CVC replies to the user.

    Fires at the channel boundary (after ``send()`` returns, after streaming
    finishes, after the webhook response is built). Multiple channel.message_out
    events may fire per user turn (streaming drafts + final formatted reply).

    Args:
        channel: Same channel name as the inbound.
        actor: Defaults to "bot". Set to a human id only if CVC forwards
            a human reply via relay (rare).
        session_id: Same session_id as the inbound.
        summary: Short preview of the reply (truncated to ~140 chars).
        data: Channel-specific metadata (chat_id, message_id, length, streaming).
        workspace: Active workspace at the time of send.

    Returns:
        The new event ULID, or None on capture failure.
    """
    return _capture(
        kind="channel.message_out",
        channel=channel,
        actor=actor,
        session_id=session_id,
        summary=summary,
        data=data,
        workspace=workspace,
        tags=["channel-outbound"],
    )


def capture_message_error(
    *,
    channel: str,
    actor: Optional[str] = None,
    session_id: Optional[str] = None,
    summary: Optional[str] = None,
    data: Optional[dict[str, Any]] = None,
    workspace: Optional[str] = None,
) -> Optional[str]:
    """Emit a ``channel.error`` event on channel-level failures.

    Examples:
      - Telegram 429 rate limit
      - Slack invalid_auth on reconnect
      - WhatsApp webhook signature verify failed
      - Email IMAP login failure
      - Network timeout reaching the channel API

    Does NOT fire for agent-level errors — those are chat.error from chat_capture.
    Only channel-stack errors: things that prevent CVC from talking to the
    channel itself.

    Args:
        channel: Channel where the error happened.
        actor: User identifier if the error is tied to a specific user,
            None if it's a connection/auth error not tied to a user.
        session_id: Same session_id as the inbound if known.
        summary: Short human-readable description (e.g. "telegram: 429 Too Many Requests").
        data: Structured error info (error_type, retry_after, http_status, exception class).
        workspace: Active workspace at the time of error.

    Returns:
        The new event ULID, or None on capture failure.
    """
    return _capture(
        kind="channel.error",
        channel=channel,
        actor=actor,
        session_id=session_id,
        summary=summary,
        data=data,
        workspace=workspace,
        tags=["channel-error"],
    )


def capture_message_skipped(
    *,
    channel: str,
    actor: Optional[str] = None,
    session_id: Optional[str] = None,
    summary: Optional[str],
    data: Optional[dict[str, Any]] = None,
    workspace: Optional[str] = None,
) -> Optional[str]:
    """Emit a ``channel.message_skipped`` event when a message is rejected.

    Examples:
      - Telegram user not in allowlist
      - WhatsApp webhook from unverified number
      - Email from blocked sender

    Args:
        channel: Channel where the skip happened.
        actor: User identifier of the rejected sender.
        session_id: None usually (no session opened for skipped messages).
        summary: Why the message was skipped (e.g. "user 12345 not in allowlist").
        data: Structured skip reason.
        workspace: Active workspace at the time of skip.

    Returns:
        The new event ULID, or None on capture failure.
    """
    return _capture(
        kind="channel.message_skipped",
        channel=channel,
        actor=actor,
        session_id=session_id,
        summary=summary,
        data=data,
        workspace=workspace,
        tags=["channel-skipped"],
    )