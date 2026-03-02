"""Shared orchestration loop for bidirectional channel communication.

Extracts the poll -> route -> SSE stream -> format -> deliver pattern that
both the Telegram bridge and CLI interactive implement independently.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from .base import Channel, ChannelEvent, ChannelMessage

# Telegram's typing indicator expires after ~5s; refresh before that.
_TYPING_REFRESH_INTERVAL = 4.0


async def channel_loop(
    channel: Channel,
    client: Any,
    server_url: str,
    agent_options: dict | None = None,
) -> None:
    """Universal bidirectional channel loop.

    Any :class:`Channel` plus an HTTP client that can stream from
    ``/api/agent/chat`` yields a fully working chat integration.

    Args:
        channel: The channel to poll and deliver through.
        client: An HTTP client (e.g. ``httpx.AsyncClient``) with a
            ``.stream("POST", url, ...)`` async context manager.
        server_url: Base URL of the emdash-core server
            (e.g. ``"http://127.0.0.1:8765"``).
        agent_options: Extra options forwarded to the chat endpoint
            (``max_iterations``, ``mode``, etc.).
    """
    await channel.start()
    try:
        async for message in channel.poll_messages():
            if not await channel.check_authorization(message.sender_id):
                await channel.send_event(
                    message.sender_id,
                    ChannelEvent("error", "Not authorized"),
                )
                continue

            if await channel.route_message(message):
                continue

            session_id = channel.get_session_id(message.sender_id)
            await _process_agent_stream(
                channel, client, server_url, message, session_id, agent_options
            )
    finally:
        await channel.stop()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_INTERACTIVE_EVENTS = frozenset({
    "clarification",
    "plan_submitted",
    "plan_mode_requested",
})


async def _typing_indicator_loop(channel: Channel, sender_id: str) -> None:
    """Continuously refresh the typing indicator until cancelled.

    Keeps the indicator active for the entire duration of agent processing
    so users always see that the bot is working.
    """
    try:
        while True:
            await asyncio.sleep(_TYPING_REFRESH_INTERVAL)
            await channel.notify_activity(sender_id)
    except asyncio.CancelledError:
        pass


async def _process_agent_stream(
    channel: Channel,
    client: Any,
    server_url: str,
    message: ChannelMessage,
    session_id: str | None,
    agent_options: dict | None,
) -> None:
    """POST to /api/agent/chat, parse the SSE stream, and deliver events."""
    # Track this sender so automation/background tasks can deliver back
    from .router import get_channel_router
    router = get_channel_router()
    if router:
        router.track_sender(channel.name, message.sender_id)

    payload: dict[str, Any] = {
        "message": message.content,
        "options": agent_options or {},
    }
    if message.images:
        payload["images"] = [
            {"data": img.data, "format": img.format} for img in message.images
        ]
    if session_id:
        payload["session_id"] = session_id

    url = f"{server_url}/api/agent/chat"
    last_message_id = ""

    await channel.notify_activity(message.sender_id)
    typing_task = asyncio.create_task(
        _typing_indicator_loop(channel, message.sender_id)
    )

    try:
        async for event_type, data in _iter_sse(client, "POST", url, json_body=payload):
            last_message_id = await _handle_sse_event(
                channel, client, server_url, message.sender_id,
                event_type, data, last_message_id,
            )
    except Exception as exc:
        await channel.send_event(
            message.sender_id,
            ChannelEvent("error", f"Stream error: {exc}"),
        )
    finally:
        typing_task.cancel()


async def _handle_sse_event(
    channel: Channel,
    client: Any,
    server_url: str,
    sender_id: str,
    event_type: str,
    data: dict,
    last_message_id: str,
) -> str:
    """Process a single SSE event; return the latest message_id."""
    # Session tracking (always runs, then falls through to formatting)
    if event_type == "session_start":
        sid = data.get("session_id")
        if sid:
            channel.set_session_id(sender_id, sid)
        # Fall through — let the formatter handle display (e.g. live panel)

    # Interactive events — delegate to the channel, then stream the
    # continuation endpoint response.
    if event_type in _INTERACTIVE_EVENTS:
        response_text = await channel.handle_pending_interaction(
            sender_id, event_type, data,
        )
        session_id = channel.get_session_id(sender_id)
        if session_id and response_text is not None:
            continuation_url = _continuation_url(
                server_url, session_id, event_type, response_text,
            )
            if continuation_url:
                url, params = continuation_url
                await _stream_continuation(
                    channel, client, server_url, sender_id, url, params,
                )
        return last_message_id

    # Normal events — format and deliver
    event = channel.format_sse_event(event_type, data)
    if event is None:
        await channel.notify_activity(sender_id)
        return last_message_id

    if event.is_update and last_message_id:
        result = await channel.update_event(sender_id, last_message_id, event)
    else:
        result = await channel.send_event(sender_id, event)

    return result.message_id or last_message_id


def _continuation_url(
    server_url: str,
    session_id: str,
    event_type: str,
    response_text: str,
) -> tuple[str, dict | None] | None:
    """Return (url, params) for the continuation endpoint, or None."""
    base = f"{server_url}/api/agent/chat/{session_id}"
    lower = response_text.strip().lower()

    if event_type == "clarification":
        return f"{base}/clarification/answer", {"answer": response_text}

    if event_type == "plan_submitted":
        if lower in ("approve", "yes", "y", "ok", "proceed"):
            return f"{base}/plan/approve", None
        feedback = "" if lower in ("reject", "no", "n", "cancel") else response_text
        return f"{base}/plan/reject", {"feedback": feedback}

    if event_type == "plan_mode_requested":
        if lower in ("approve", "yes", "y", "ok"):
            return f"{base}/planmode/approve", None
        feedback = "" if lower in ("reject", "no", "n") else response_text
        return f"{base}/planmode/reject", {"feedback": feedback}

    return None


async def _stream_continuation(
    channel: Channel,
    client: Any,
    server_url: str,
    sender_id: str,
    url: str,
    params: dict | None,
) -> None:
    """Stream a continuation endpoint and deliver its events."""
    last_message_id = ""
    await channel.notify_activity(sender_id)
    typing_task = asyncio.create_task(
        _typing_indicator_loop(channel, sender_id)
    )

    try:
        async for event_type, data in _iter_sse(client, "POST", url, params=params):
            last_message_id = await _handle_sse_event(
                channel, client, server_url, sender_id,
                event_type, data, last_message_id,
            )
    except Exception as exc:
        await channel.send_event(
            sender_id,
            ChannelEvent("error", f"Continuation error: {exc}"),
        )
    finally:
        typing_task.cancel()


async def _iter_sse(
    client: Any,
    method: str,
    url: str,
    *,
    json_body: dict | None = None,
    params: dict | None = None,
):
    """Iterate SSE lines from an HTTP streaming response.

    Yields ``(event_type, data_dict)`` tuples.
    """
    kwargs: dict[str, Any] = {}
    if json_body is not None:
        kwargs["json"] = json_body
    if params is not None:
        kwargs["params"] = params

    async with client.stream(method, url, **kwargs) as response:
        response.raise_for_status()
        current_event: str | None = None

        async for line in response.aiter_lines():
            line = line.strip()
            if line.startswith("event: "):
                current_event = line[7:]
            elif line.startswith("data: ") and current_event:
                try:
                    data = json.loads(line[6:])
                    if data is None:
                        data = {}
                    yield current_event, data
                except json.JSONDecodeError:
                    pass
            elif line == ": ping":
                pass  # keep-alive
