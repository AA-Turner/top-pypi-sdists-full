"""
Discord adapter for CVC.

Uses the official ``discord.py`` library (already a CVC core dep).

Features v1:
  - Receive DMs and server messages
  - Slash commands via bot menu
  - Send text + embeds
  - Reply to a specific message
  - Per-server + per-user allowlist
  - Channel threads (mapped to Discord threads via message.channel.parent)

Channels we deliberately defer to v1.1+:
  - Voice channel activity (no business value for CVC)
  - Components v2 (buttons + select menus) — v1.5
  - Reactions → cognitive commits (already supported structurally; needs polish)
"""

from __future__ import annotations

import asyncio
import io
import logging
import time
from typing import Any, Dict, List, Optional

import httpx

from .base import (
    BaseChannelAdapter,
    Capability,
    InboundMessage,
    OutboundMessage,
)


logger = logging.getLogger(__name__)


try:
    import discord
    from discord import Intents, Message, Embed
    _DISCORD_AVAILABLE = True
except Exception as _exc:  # noqa: BLE001
    _DISCORD_AVAILABLE = False
    _exc_discord = _exc
    discord = None  # type: ignore
    Intents = None  # type: ignore
    Message = None  # type: ignore
    Embed = None  # type: ignore


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


_MAX_LEN = 1900  # Discord cap is 2000; leave headroom.


def _is_allowed(allowlist: List[str], user_id: int, guild_id: Optional[int], channel_id: int) -> bool:
    if not allowlist:
        return False
    targets = {str(user_id), str(channel_id)}
    if guild_id is not None:
        targets.add(str(guild_id))
    return bool(targets & set(allowlist))


class DiscordAdapter(BaseChannelAdapter):
    name = "discord"
    display_name = "Discord Bot"
    description = (
        "Discord bot via discord.py. Talk to CVC from any server channel "
        "or DM. Requires the bot to have the Message Content Intent enabled "
        "in the Discord developer portal (Privileged Gateway Intents)."
    )
    config_schema = [
        {
            "key": "bot_token",
            "label": "Bot token",
            "help": "From the Discord developer portal → Bot → Reset Token.",
            "secret": True,
            "required": True,
            "kind": "str",
        },
        {
            "key": "allowlist",
            "label": "Allowed user IDs / channel IDs (comma-separated)",
            "help": (
                "Discord user IDs are 17-19 digit snowflakes. "
                "Add channel IDs to scope specific channels."
            ),
            "required": True,
            "kind": "list[str]",
        },
        {
            "key": "stream_edits",
            "label": "Stream edits",
            "help": "Edit one message in-place as the agent thinks.",
            "default": True,
            "kind": "bool",
        },
    ]


    def capabilities(self) -> List[Capability]:
        return [
            Capability.TEXT,
            Capability.MEDIA,
            Capability.INLINE_KEYBOARD,
            Capability.THREADS,
            Capability.EDIT,
            Capability.REACTIONS,
            Capability.STREAMING,
        ]

    async def start(self) -> None:
        if not _DISCORD_AVAILABLE:
            raise RuntimeError(
                "discord.py is not installed. Run `pip install 'discord.py[voice]>=2.4'`."
            ) from _exc_discord
        token = self.cfg("bot_token", "")
        if not token:
            raise RuntimeError("discord: bot_token is required in config")
        self._allowlist = self.cfg_list("allowlist")
        intents = Intents.default()
        intents.message_content = True
        self._client = discord.Client(intents=intents)  # type: ignore[arg-type]
        self._client.event(self._on_ready)
        self._client.event(self._on_message)
        self._stream_edits = self.cfg_bool("stream_edits", True)
        # Spawn the discord.py client as a background task.
        self._tasks.append(asyncio.create_task(self._client.start(token)))
        self._healthy = True
        self._started_at = time.time()
        logger.info("discord: client started")

    async def stop(self) -> None:
        client = getattr(self, "_client", None)
        if client is not None:
            try:
                await client.close()
            except Exception:
                pass
        for t in self._tasks:
            t.cancel()
        self._tasks.clear()
        self._healthy = False

    async def send(self, message: OutboundMessage) -> Dict[str, Any]:
        client = self._client
        channel_id = int(message.chat_id)
        channel = client.get_channel(channel_id) or await client.fetch_channel(channel_id)

        text = message.text or ""
        last_msg_id: Optional[str] = None
        if text:
            # Discord supports a small markdown subset natively; tables are
            # rewritten to row groups so users on mobile don't see raw pipes.
            rewritten = wrap_markdown_tables(text)
            # Discord has a 2000-char cap; split if needed.
            chunks = [rewritten[i : i + _MAX_LEN] for i in range(0, len(rewritten), _MAX_LEN)] or [""]
            for i, chunk in enumerate(chunks):
                kwargs: Dict[str, Any] = {"content": chunk}
                if message.reply_to_message_id and i == 0:
                    kwargs["reference"] = discord.MessageReference(  # type: ignore[attr-defined]
                        message_id=int(message.reply_to_message_id),
                        channel_id=channel_id,
                        fail_if_not_exists=False,
                    )
                sent = await channel.send(**kwargs)
                last_msg_id = str(sent.id)

        # C6: capture outbound.
        try:
            capture_message_out(
                channel=self.name,
                actor="bot",
                session_id=f"cvc_ch_{self.name}_{channel_id}_{message.thread_id or ''}".rstrip("_"),
                summary=text[:140] or "<empty>",
                data={
                    "chat_id": str(channel_id),
                    "thread_id": message.thread_id,
                    "message_id": last_msg_id,
                    "text_length": len(text),
                },
            )
        except Exception:
            pass

        return {"message_id": last_msg_id} if last_msg_id else {}

    # ── Inbound ────────────────────────────────────────────────────

    async def _on_ready(self) -> None:
        logger.info("discord: connected as %s", self._client.user)

    async def _on_message(self, message: Message) -> None:
        if message.author.bot:
            return
        if not _is_allowed(self._allowlist, message.author.id, message.guild.id if message.guild else None, message.channel.id):
            # C6: capture rejected message.
            try:
                capture_message_skipped(
                    channel=self.name,
                    actor=str(message.author.id),
                    summary=f"discord: user {message.author.id} not in allowlist",
                    data={"chat_id": str(message.channel.id), "reason": "not_in_allowlist"},
                )
            except Exception:
                pass
            return
        # Threads: capture the parent channel id as thread_id so the
        # registry / agent can see context.
        thread_id = None
        if hasattr(message.channel, "parent") and message.channel.parent is not None:
            thread_id = str(message.channel.parent.id)
        inbound = InboundMessage(
            channel=self.name,
            chat_id=str(message.channel.id),
            user_id=str(message.author.id),
            user_name=message.author.display_name or message.author.name,
            text=message.content or "",
            thread_id=thread_id,
            reply_to_message_id=str(message.reference.message_id) if message.reference else None,
            media=await self._extract_media(message),
            is_command=message.content.startswith("!") or message.content.startswith("/"),
            command=None,
            command_args=None,
            raw=message,
        )
        try:
            async with message.channel.typing():
                reply = await self._emit_inbound(inbound)
        except Exception:
            reply = await self._emit_inbound(inbound)

        # C6: capture inbound at the channel boundary.
        try:
            capture_message_in(
                channel=self.name,
                actor=str(message.author.id),
                session_id=f"cvc_ch_{self.name}_{message.channel.id}_{thread_id or ''}".rstrip("_"),
                summary=(message.content or "")[:140] or "<empty>",
                data={
                    "chat_id": str(message.channel.id),
                    "thread_id": thread_id,
                    "guild_id": str(message.guild.id) if message.guild else None,
                    "user_name": message.author.display_name or message.author.name,
                    "is_command": message.content.startswith("!") or message.content.startswith("/"),
                    "text_length": len(message.content or ""),
                    "media_count": len(message.attachments),
                },
            )
        except Exception:
            pass

        if reply and reply.text:
            await self.send(reply)

    async def _extract_media(self, message: Message) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for att in message.attachments:
            try:
                data = await att.read()
            except Exception:
                continue
            kind = "photo" if (att.content_type or "").startswith("image/") else "document"
            out.append({
                "kind": kind,
                "data": data,
                "mime": att.content_type or "application/octet-stream",
                "size": att.size,
                "filename": att.filename,
            })
        return out

    def _info(self) -> Dict[str, Any]:
        info = super()._info()
        info["allowlist_size"] = len(getattr(self, "_allowlist", []))
        return info
