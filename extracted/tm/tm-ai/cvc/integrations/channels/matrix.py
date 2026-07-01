"""
Matrix adapter for CVC — Application Service style.

Uses Matrix's Client-Server HTTP API (no external SDK required). The
adapter logs in as a bot user via ``/login`` → access_token, then
long-polls ``/sync`` for new messages.

Features v1:
  - Receive text + media messages in any room the bot is in
  - Send text + media replies
  - Threads: Matrix threads are just rooms; we treat them as separate
    ``chat_id`` values
  - Per-user + per-room allowlist

Deliberately deferred to v1.1+:
  - Encrypted rooms (E2EE) — requires olm / vodozemac
  - State events (display name, avatar) — not core UX
  - Appservice-style ghost users — overkill for CVC
"""

from __future__ import annotations

import asyncio
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


from ..formatting.markdown import markdown_to_plain  # noqa: E402


_MAX_LEN = 4000


def _is_allowed(allowlist: List[str], sender: str, room: str) -> bool:
    if not allowlist:
        return False
    return any(t in {sender, room} for t in allowlist)


class MatrixAdapter(BaseChannelAdapter):
    name = "matrix"
    display_name = "Matrix"
    description = (
        "Connect to any Matrix homeserver (matrix.org, element.io, or self-hosted). "
        "Long-polls /sync. E2EE rooms are not supported in v1."
    )
    config_schema = [
        {
            "key": "homeserver_url",
            "label": "Homeserver URL",
            "help": "Example: https://matrix.org",
            "default": "https://matrix.org",
            "required": True,
            "kind": "str",
        },
        {
            "key": "user_id",
            "label": "Bot user ID",
            "help": "Example: @cvc:matrix.org",
            "required": True,
            "kind": "str",
        },
        {
            "key": "password",
            "label": "Bot password",
            "secret": True,
            "required": True,
            "kind": "str",
        },
        {
            "key": "allowlist",
            "label": "Allowed user IDs / room IDs (comma-separated)",
            "help": "Examples: @you:matrix.org, !someroom:matrix.org",
            "required": True,
            "kind": "list[str]",
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
        homeserver = self.cfg("homeserver_url", "").rstrip("/")
        user = self.cfg("user_id", "")  # e.g. "@cvc:matrix.org"
        password = self.cfg("password", "")
        if not (homeserver and user and password):
            raise RuntimeError(
                "matrix: homeserver_url, user_id, AND password are required"
            )
        self._homeserver = homeserver
        self._user = user
        self._allowlist = self.cfg_list("allowlist")
        # Login.
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{homeserver}/_matrix/client/v3/login",
                json={
                    "type": "m.login.password",
                    "identifier": {"type": "m.id.user", "user": user},
                    "password": password,
                },
            )
            resp.raise_for_status()
            self._token = resp.json()["access_token"]
        # Sync loop.
        self._sync_task = asyncio.create_task(self._sync_loop())
        self._healthy = True
        self._started_at = time.time()
        logger.info("matrix: connected to %s as %s", homeserver, user)

    async def stop(self) -> None:
        task: Optional[asyncio.Task] = getattr(self, "_sync_task", None)
        if task is not None:
            task.cancel()
        self._healthy = False

    async def _sync_loop(self) -> None:
        """Long-poll ``/sync`` and route every new m.room.message event
        through the inbound pipeline."""
        since: Optional[str] = None
        url = f"{self._homeserver}/_matrix/client/v3/sync"
        headers = {"Authorization": f"Bearer {self._token}"}
        async with httpx.AsyncClient(timeout=60.0) as client:
            while True:
                try:
                    params: Dict[str, Any] = {"timeout": 30000}
                    if since:
                        params["since"] = since
                    resp = await client.get(url, params=params, headers=headers)
                    if resp.status_code != 200:
                        logger.warning("matrix: sync HTTP %s", resp.status_code)
                        await asyncio.sleep(2.0)
                        continue
                    data = resp.json()
                    since = data.get("next_batch", since)
                    for room_id, room in (data.get("rooms", {}) or {}).get("join", {}).items():
                        await self._process_room_events(room_id, room)
                except asyncio.CancelledError:
                    raise
                except Exception as exc:  # noqa: BLE001
                    logger.exception("matrix: sync error: %s", exc)
                    await asyncio.sleep(2.0)

    async def _process_room_events(self, room_id: str, room: Dict[str, Any]) -> None:
        timeline = room.get("timeline", {}) or {}
        events = timeline.get("events", []) or []
        for ev in events:
            if ev.get("type") != "m.room.message":
                continue
            sender = ev.get("sender", "")
            content = ev.get("content", {}) or {}
            msgtype = content.get("msgtype", "")
            text = ""
            media: List[Dict[str, Any]] = []
            if msgtype == "m.text":
                text = content.get("body", "")
            elif msgtype.startswith("m.image") or msgtype.startswith("m.audio") or msgtype.startswith("m.video") or msgtype == "m.file":
                kind = {
                    "m.image": "photo",
                    "m.audio": "audio",
                    "m.video": "video",
                    "m.file": "document",
                }.get(msgtype, "document")
                text = content.get("body", "") or f"[{kind}]"
                url = content.get("url", "")
                if url.startswith("mxc://"):
                    # Translate mxc:// to the authenticated download URL.
                    media.append({"kind": kind, "url": f"{self._homeserver}/_matrix/media/v3/download/{url.removeprefix('mxc://')}", "mime": content.get("info", {}).get("mimetype", "application/octet-stream"), "size": content.get("info", {}).get("size", 0)})
            if not _is_allowed(self._allowlist, sender, room_id):
                continue
            inbound = InboundMessage(
                channel=self.name,
                chat_id=room_id,
                user_id=sender,
                user_name=sender,
                text=text,
                thread_id=None,
                reply_to_message_id=None,
                media=media,
                is_command=text.lstrip().startswith("!"),
                command=(text.split(maxsplit=1)[0].lstrip("!").lower() or None) if text.lstrip().startswith("!") else None,
                command_args=(text.split(maxsplit=1)[1] if " " in text else None),
                raw=ev,
            )
            reply = await self._emit_inbound(inbound)
            if reply and reply.text:
                await self.send(reply)

    async def send(self, message: OutboundMessage) -> Dict[str, Any]:
        text = markdown_to_plain(message.text or "")
        chunks = [text[i : i + _MAX_LEN] for i in range(0, len(text), _MAX_LEN)] or [""]
        txn = int(time.time() * 1000)
        url = f"{self._homeserver}/_matrix/client/v3/rooms/{message.chat_id}/send/m.room.message/{txn}"
        headers = {"Authorization": f"Bearer {self._token}"}
        last_event_id: Optional[str] = None
        async with httpx.AsyncClient(timeout=30.0) as client:
            for chunk in chunks:
                if not chunk:
                    continue
                body: Dict[str, Any] = {"msgtype": "m.text", "body": chunk}
                if message.reply_to_message_id:
                    body["m.relates_to"] = {"m.in_reply_to": {"event_id": message.reply_to_message_id}}
                resp = await client.put(url, headers=headers, json=body)
                resp.raise_for_status()
                last_event_id = resp.json().get("event_id")
                txn += 1
        return {"event_id": last_event_id} if last_event_id else {}

    def _info(self) -> Dict[str, Any]:
        info = super()._info()
        info["homeserver"] = self.cfg("homeserver_url", "")
        info["user_id"] = self.cfg("user_id", "")
        info["allowlist_size"] = len(getattr(self, "_allowlist", []))
        return info
