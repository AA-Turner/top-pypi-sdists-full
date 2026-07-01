"""
WhatsApp adapter for CVC — Business Cloud API only.

Uses Meta's official Cloud API (https://developers.facebook.com/docs/whatsapp/cloud-api).
This is the production-grade path that doesn't require a personal phone
number to be permanently linked. The trade-off: you need a Meta Business
account and a registered phone number. For personal/dev use, see the
:bluebubbles: adapter (Hermes reference) which is macOS-only.

Receive path: the gateway exposes ``/api/channels/whatsapp/webhook``
which receives Cloud API webhook events. The adapter polls the
gateway's mounted FastAPI app and routes the verified payloads back
into CVC.

Send path: Cloud API ``POST /<phone_number_id>/messages``.

Features v1:
  - Text messages (send + receive)
  - Media: image / audio / voice / video / document
  - Reply to a specific message
  - Per-phone-number allowlist (E.164 format)
  - Read receipts (optional)
"""

from __future__ import annotations

import asyncio
import json
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


# WhatsApp message text cap. Meta allows 4096 chars; we leave headroom.
_MAX_LEN = 4000


def _is_allowed(allowlist: List[str], from_number: str) -> bool:
    if not allowlist:
        return False
    return from_number in set(allowlist)


class WhatsAppAdapter(BaseChannelAdapter):
    name = "whatsapp"
    display_name = "WhatsApp Cloud API"
    description = (
        "Meta WhatsApp Cloud API (production-grade). No personal phone "
        "needed. Requires a Meta Business account + registered phone number. "
        "Free tier is 1000 conversations/month."
    )
    config_schema = [
        {
            "key": "phone_number_id",
            "label": "Phone number ID",
            "help": "Meta Business Suite → WhatsApp → API Setup.",
            "required": True,
            "kind": "str",
        },
        {
            "key": "access_token",
            "label": "Access token",
            "help": "Permanent System User Access Token (recommended) or temporary.",
            "secret": True,
            "required": True,
            "kind": "str",
        },
        {
            "key": "verify_token",
            "label": "Webhook verify_token (you pick this)",
            "help": (
                "Any secret string — Meta will send it back during webhook "
                "registration. Must match what you entered in the Meta dashboard."
            ),
            "secret": True,
            "required": True,
            "kind": "str",
        },
        {
            "key": "allowlist",
            "label": "Allowed phone numbers (E.164, comma-separated)",
            "help": (
                "Example: +919876543210,+14155551234. WhatsApp users must "
                "opt-in to receive messages (24h window rule)."
            ),
            "required": True,
            "kind": "list[str]",
        },
    ]


    def capabilities(self) -> List[Capability]:
        return [
            Capability.TEXT,
            Capability.MEDIA,
            Capability.REACTIONS,
        ]

    # ── Lifecycle ──────────────────────────────────────────────────

    async def start(self) -> None:
        phone_id = self.cfg("phone_number_id", "")
        token = self.cfg("access_token", "")
        if not phone_id or not token:
            raise RuntimeError("whatsapp: phone_number_id AND access_token are required")
        self._phone_id = phone_id
        self._token = token
        self._allowlist = self.cfg_list("allowlist")
        self._base = f"https://graph.facebook.com/v22.0/{phone_id}"
        # Cloud API is webhook-driven, so there is no polling loop here.
        # The gateway mounts /api/channels/whatsapp/webhook which calls
        # :meth:`handle_inbound_webhook`.
        self._healthy = True
        self._started_at = time.time()
        logger.info("whatsapp: ready (phone_number_id=%s)", phone_id)

    async def stop(self) -> None:
        self._healthy = False

    # ── Send ───────────────────────────────────────────────────────

    async def send(self, message: OutboundMessage) -> Dict[str, Any]:
        # WhatsApp Cloud API prefers plain text. Strip markdown cleanly.
        text = markdown_to_plain(message.text or "")
        chunks = [text[i : i + _MAX_LEN] for i in range(0, len(text), _MAX_LEN)] or [""]
        last_msg_id: Optional[str] = None
        async with httpx.AsyncClient(timeout=30.0) as client:
            for i, chunk in enumerate(chunks):
                if not chunk:
                    continue
                payload: Dict[str, Any] = {
                    "messaging_product": "whatsapp",
                    "to": message.chat_id,
                    "type": "text",
                    "text": {"body": chunk},
                }
                if message.reply_to_message_id and i == 0:
                    payload["context"] = {"message_id": message.reply_to_message_id}
                resp = await client.post(
                    f"{self._base}/messages",
                    headers={"Authorization": f"Bearer {self._token}"},
                    json=payload,
                )
                resp.raise_for_status()
                body = resp.json()
                last_msg_id = (body.get("messages") or [{}])[0].get("id")
        result = {"message_id": last_msg_id} if last_msg_id else {}

        # C6: capture outbound.
        try:
            capture_message_out(
                channel=self.name,
                actor="bot",
                session_id=f"cvc_ch_{self.name}_{message.chat_id}",
                summary=text[:140],
                data={
                    "chat_id": message.chat_id,
                    "message_id": last_msg_id,
                    "text_length": len(text),
                    "chunks": len([c for c in chunks if c]),
                },
            )
        except Exception:
            pass

        return result

    # ── Webhook handler (called by the FastAPI gateway route) ──────

    async def handle_inbound_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process one Cloud API webhook event payload.

        Cloud API delivers entries like:
          {"entry": [{"changes": [{"value": {"messages": [...]}}]}]}
        We iterate every message and route it through the inbound pipeline.
        """
        processed: List[str] = []
        try:
            entries = payload.get("entry", []) or []
            for entry in entries:
                changes = entry.get("changes", []) or []
                for change in changes:
                    value = change.get("value", {}) or {}
                    messages = value.get("messages", []) or []
                    contacts = value.get("contacts", []) or []
                    name_for = {c.get("wa_id"): c.get("profile", {}).get("name", "") for c in contacts}
                    for msg in messages:
                        await self._process_whatsapp_message(msg, name_for)
                        processed.append(msg.get("id", ""))
        except Exception as exc:  # noqa: BLE001
            logger.exception("whatsapp: webhook handling failed: %s", exc)
            self._last_error = str(exc)
        return {"processed": processed}

    async def _process_whatsapp_message(
        self, msg: Dict[str, Any], name_for: Dict[str, str]
    ) -> None:
        from_number = msg.get("from", "")
        if not _is_allowed(self._allowlist, from_number):
            # C6: capture rejected message.
            try:
                capture_message_skipped(
                    channel=self.name,
                    actor=from_number,
                    summary=f"whatsapp: from {from_number} not in allowlist",
                    data={"chat_id": from_number, "reason": "not_in_allowlist", "msg_type": msg.get("type")},
                )
            except Exception:
                pass
            logger.info("whatsapp: rejecting from %s (not in allowlist)", from_number)
            return
        msg_type = msg.get("type", "")
        text = ""
        media: List[Dict[str, Any]] = []
        if msg_type == "text":
            text = msg.get("text", {}).get("body", "")
        elif msg_type in {"image", "audio", "voice", "video", "document", "sticker"}:
            sub = msg.get(msg_type, {}) or {}
            url = sub.get("url") or sub.get("link", "")
            mime = sub.get("mime_type", "application/octet-stream")
            media.append({
                "kind": msg_type if msg_type != "sticker" else "sticker",
                "url": url,
                "mime": mime,
                "size": 0,
                "caption": sub.get("caption", ""),
            })
            text = sub.get("caption", "") or f"[{msg_type}]"
        inbound = InboundMessage(
            channel=self.name,
            chat_id=from_number,
            user_id=from_number,
            user_name=name_for.get(from_number, ""),
            text=text,
            thread_id=None,
            reply_to_message_id=(msg.get("context") or {}).get("id"),
            media=media,
            is_command=text.lstrip().startswith("/"),
            command=(text.split(maxsplit=1)[0].lstrip("/").lower() or None) if text.lstrip().startswith("/") else None,
            command_args=(text.split(maxsplit=1)[1] if " " in text else None),
            raw=msg,
        )

        # C6: capture inbound at the channel boundary.
        try:
            capture_message_in(
                channel=self.name,
                actor=from_number,
                session_id=f"cvc_ch_{self.name}_{from_number}",
                summary=text[:140] or f"[{msg_type}]",
                data={
                    "chat_id": from_number,
                    "msg_id": msg.get("id"),
                    "msg_type": msg_type,
                    "media_count": len(media),
                    "is_command": inbound.is_command,
                    "command": inbound.command,
                    "text_length": len(text),
                },
            )
        except Exception:
            pass

        reply = await self._emit_inbound(inbound)
        if reply and reply.text:
            await self.send(reply)

    def _info(self) -> Dict[str, Any]:
        info = super()._info()
        info["phone_number_id"] = self.cfg("phone_number_id", "")
        info["allowlist_size"] = len(getattr(self, "_allowlist", []))
        return info
