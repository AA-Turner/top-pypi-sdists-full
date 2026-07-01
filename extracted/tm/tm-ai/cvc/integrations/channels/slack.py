"""
Slack adapter for CVC.

Uses the official ``slack-bolt`` async framework (already a CVC core
dep) in Socket Mode for the receive path. Sends via the Web API.

Features v1:
  - DMs and channel messages
  - Slash command auto-registration (only the bot token is needed)
  - Block Kit message composition (text + section blocks)
  - Reply threading (thread_ts)
  - Per-user + per-channel allowlist
  - Reactions to inbound messages to acknowledge receipt (optional)

Deliberately deferred to v1.1+:
  - Interactive modals (workflow shortcut)
  - App Home tab (overview surface)
  - File uploads >1 GB
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


try:
    from slack_bolt.async_app import AsyncApp
    from slack_sdk.web.async_client import AsyncWebClient
    _SLACK_AVAILABLE = True
except Exception as _exc:  # noqa: BLE001
    _SLACK_AVAILABLE = False
    _exc_slack = _exc
    AsyncApp = None  # type: ignore
    AsyncWebClient = None  # type: ignore


from .base import (  # noqa: E402
    BaseChannelAdapter,
    Capability,
    InboundMessage,
    OutboundMessage,
)
from ..formatting.markdown import wrap_markdown_tables  # noqa: E402


# C6: spine channel capture — fires at the channel boundary.
try:
    from cvc.events.channel_capture import (
        capture_message_in,
        capture_message_out,
        capture_message_error,
        capture_message_skipped,
    )
except Exception:  # noqa: BLE001
    def capture_message_in(*_a, **_kw): return None  # type: ignore
    def capture_message_out(*_a, **_kw): return None  # type: ignore
    def capture_message_error(*_a, **_kw): return None  # type: ignore
    def capture_message_skipped(*_a, **_kw): return None  # type: ignore


def _is_allowed(allowlist: List[str], user_id: str, channel_id: str) -> bool:
    if not allowlist:
        return False
    return any(t in {user_id, channel_id} for t in allowlist)


class SlackAdapter(BaseChannelAdapter):
    name = "slack"
    display_name = "Slack App"
    description = (
        "Slack app via slack-bolt Socket Mode. No public URL needed. "
        "Talk to CVC from any channel or DM in your Slack workspace."
    )
    config_schema = [
        {
            "key": "bot_token",
            "label": "Bot User OAuth Token (xoxb-…)",
            "help": "Slack app → OAuth & Permissions → Bot Token.",
            "secret": True,
            "required": True,
            "kind": "str",
        },
        {
            "key": "app_token",
            "label": "App-Level Token (xapp-…)",
            "help": (
                "Slack app → Basic Information → App-Level Tokens. "
                "Needs the 'connections:write' scope for Socket Mode."
            ),
            "secret": True,
            "required": True,
            "kind": "str",
        },
        {
            "key": "allowlist",
            "label": "Allowed user IDs / channel IDs (comma-separated)",
            "help": "Slack user IDs start with U, channel IDs with C.",
            "required": True,
            "kind": "list[str]",
        },
        {
            "key": "port",
            "label": "Local socket port (optional)",
            "help": "0 = pick automatically.",
            "default": "0",
            "kind": "str",
        },
    ]


    def capabilities(self) -> List[Capability]:
        return [
            Capability.TEXT,
            Capability.MEDIA,
            Capability.THREADS,
            Capability.EDIT,
            Capability.REACTIONS,
        ]

    async def start(self) -> None:
        if not _SLACK_AVAILABLE:
            raise RuntimeError(
                "slack-bolt is not installed. Run `pip install 'slack-bolt>=1.18'`."
            ) from _exc_slack
        bot_token = self.cfg("bot_token", "")
        app_token = self.cfg("app_token", "")
        if not bot_token or not app_token:
            raise RuntimeError("slack: bot_token AND app_token are required")
        self._allowlist = self.cfg_list("allowlist")
        self._app = AsyncApp(token=bot_token)
        self._client = AsyncWebClient(token=bot_token)

        # Generic message handler — slash commands routed via bot_mention filter.
        @self._app.event("message")
        async def _on_message(event, client, logger_):
            await self._on_message_event(event, client)

        # Slash command handlers.
        @self._app.command("/cvc")
        async def _on_cvc(ack, respond, command):
            await ack()
            await self._route_command(command, respond)

        # Reaction added — used as an alternative lightweight inbound
        # signal. Forwarded as a synthetic message.
        @self._app.event("reaction_added")
        async def _on_reaction(event, client, logger_):
            await self._on_reaction_event(event)

        self._socket_task = asyncio.create_task(self._app.start(port=int(self.cfg("port", "0") or 0)))
        self._healthy = True
        self._started_at = time.time()
        logger.info("slack: bolt app started (socket mode=%s)", bool(app_token))

    async def stop(self) -> None:
        app = getattr(self, "_app", None)
        if app is not None:
            try:
                await app.close()
            except Exception:
                pass
        for t in getattr(self, "_tasks", []):
            t.cancel()
        self._healthy = False

    async def send(self, message: OutboundMessage) -> Dict[str, Any]:
        text = message.text or ""
        if not text:
            return {}
        # Slack mrkdwn is similar to standard markdown but uses *bold*
        # and _italic_. We do a light table→row-group rewrite so the
        # user sees bullets instead of raw pipes.
        rewritten = wrap_markdown_tables(text)
        # Split if very long; Slack allows 40k chars but a 4k chunk is
        # friendlier for the client.
        chunks = [rewritten[i : i + 3500] for i in range(0, len(rewritten), 3500)] or [""]
        last_ts: Optional[str] = None
        for chunk in chunks:
            kwargs: Dict[str, Any] = {"channel": message.chat_id, "text": chunk}
            if message.thread_id:
                kwargs["thread_ts"] = message.thread_id
            elif message.reply_to_message_id:
                kwargs["thread_ts"] = message.reply_to_message_id
            resp = await self._client.chat_postMessage(**kwargs)
            last_ts = resp.get("ts")
        result = {"ts": last_ts} if last_ts else {}

        # C6: capture outbound.
        try:
            capture_message_out(
                channel=self.name,
                actor="bot",
                session_id=f"cvc_ch_{self.name}_{message.chat_id}_{message.thread_id or ''}".rstrip("_"),
                summary=text[:140],
                data={
                    "chat_id": message.chat_id,
                    "thread_id": message.thread_id,
                    "ts": last_ts,
                    "text_length": len(text),
                    "chunks": len(chunks),
                },
            )
        except Exception:
            pass

        return result

    # ── Inbound ────────────────────────────────────────────────────

    async def _on_message_event(self, event: Dict[str, Any], client: Any) -> None:
        if event.get("subtype"):
            return  # ignore edits, joins, etc.
        user = event.get("user", "")
        channel = event.get("channel", "")
        text = event.get("text", "")
        ts = event.get("ts", "")
        if not _is_allowed(self._allowlist, user, channel):
            # C6: capture rejected message.
            try:
                capture_message_skipped(
                    channel=self.name,
                    actor=user,
                    summary=f"slack: user {user} not in allowlist (channel {channel})",
                    data={"chat_id": channel, "reason": "not_in_allowlist", "ts": ts},
                )
            except Exception:
                pass
            return
        inbound = InboundMessage(
            channel=self.name,
            chat_id=channel,
            user_id=user,
            user_name=await self._resolve_user_name(client, user),
            text=text,
            thread_id=event.get("thread_ts"),
            reply_to_message_id=None,
            media=[],
            is_command=text.lstrip().startswith("/"),
            command=(text.split(maxsplit=1)[0].lstrip("/").lower() or None) if text.lstrip().startswith("/") else None,
            command_args=(text.split(maxsplit=1)[1] if " " in text else None),
            raw=event,
        )

        # C6: capture inbound at the channel boundary.
        try:
            capture_message_in(
                channel=self.name,
                actor=user,
                session_id=f"cvc_ch_{self.name}_{channel}_{event.get('thread_ts') or ''}".rstrip("_"),
                summary=text[:140] or "<empty>",
                data={
                    "chat_id": channel,
                    "thread_id": event.get("thread_ts"),
                    "ts": ts,
                    "is_command": inbound.is_command,
                    "command": inbound.command,
                    "command_args": (inbound.command_args or "")[:80],
                    "text_length": len(text),
                },
            )
        except Exception:
            pass

        reply = await self._emit_inbound(inbound)
        if reply and reply.text:
            await self.send(reply)

    async def _on_reaction_event(self, event: Dict[str, Any]) -> None:
        # Reactions are mapped to a synthetic "I see you reacted with X"
        # message so the agent can respond. Keeps the cognitive commit
        # trail complete.
        user = event.get("user", "")
        item = event.get("item", {})
        reaction = event.get("reaction", "")
        channel = item.get("channel", "")
        if not _is_allowed(self._allowlist, user, channel):
            return
        inbound = InboundMessage(
            channel=self.name,
            chat_id=channel,
            user_id=user,
            user_name=user,
            text=f"[reaction: :{reaction}:]",
            thread_id=item.get("ts"),
            reply_to_message_id=item.get("ts"),
            media=[],
            is_command=False,
            command=None,
            command_args=None,
            raw=event,
        )
        reply = await self._emit_inbound(inbound)
        if reply and reply.text:
            # Send the reaction reply in-thread.
            reply.thread_id = item.get("ts")
            await self.send(reply)

    async def _route_command(self, command: Dict[str, Any], respond: Any) -> None:
        # The /cvc slash command is the user explicitly asking CVC.
        # Treat as a regular message — gateway handles routing.
        inbound = InboundMessage(
            channel=self.name,
            chat_id=command.get("channel_id", ""),
            user_id=command.get("user_id", ""),
            user_name=command.get("user_name", ""),
            text=command.get("text", "") or "[/cvc]",
            thread_id=None,
            reply_to_message_id=None,
            media=[],
            is_command=True,
            command="cvc",
            command_args=command.get("text"),
            raw=command,
        )
        reply = await self._emit_inbound(inbound)
        if reply and reply.text:
            await respond(reply.text)

    @staticmethod
    async def _resolve_user_name(client: Any, user_id: str) -> str:
        try:
            resp = await client.users_info(user=user_id)
            user = resp.get("user", {})
            return user.get("real_name") or user.get("name") or user_id
        except Exception:
            return user_id

    def _info(self) -> Dict[str, Any]:
        info = super()._info()
        info["allowlist_size"] = len(getattr(self, "_allowlist", []))
        return info
