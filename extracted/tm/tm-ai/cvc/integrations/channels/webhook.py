"""
Generic Webhook adapter for CVC — bidirectional.

The receive side is just a route on the gateway:
  POST /api/channels/webhook/inbound
  Body: ``{"chat_id": "...", "user_id": "...", "user_name": "...", "text": "..."}``

The send side exposes ``POST /api/channels/webhook/outbound/<name>`` so
external systems can push CVC replies into any HTTP receiver (Slack
Incoming Webhook clone, n8n workflow, custom script, etc.).

This is the lowest-friction channel — it doesn't need any SDK or
platform account. Every user gets a working integration the moment
they run CVC.

Features v1:
  - Inbound: ``POST /api/channels/webhook/inbound`` with HMAC verification
  - Outbound: per-channel ``POST /api/channels/webhook/outbound/<name>``
  - Optional shared-secret auth on both paths
  - Configurable receivers in the channel config
"""

from __future__ import annotations

import hashlib
import hmac
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


def _check_signature(secret: str, body: bytes, provided: Optional[str]) -> bool:
    if not secret:
        return True
    if not provided:
        return False
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, provided)


class WebhookAdapter(BaseChannelAdapter):
    name = "webhook"
    display_name = "Webhook (generic)"
    description = (
        "Generic bidirectional HTTP webhook with optional HMAC-SHA256 "
        "signing. The lowest-friction channel — works on a fresh install "
        "with zero tokens. Pipe CVC replies into n8n, Zapier, Slack "
        "Incoming Webhook, or your own scripts."
    )
    config_schema = [
        {
            "key": "shared_secret",
            "label": "Shared secret (optional)",
            "help": (
                "If set, inbound webhooks must include X-CVC-Signature: "
                "<hex sha256 hmac>. Outbound calls will also sign requests."
            ),
            "secret": True,
            "required": False,
            "kind": "str",
        },
        {
            "key": "receivers",
            "label": "Receivers (JSON, optional)",
            "help": (
                'Example: {"n8n": {"url": "https://n8n.example.com/webhook", '
                '"headers": {"Authorization": "Bearer ..."}}}. '
                "Leave empty to skip outbound HTTP entirely."
            ),
            "required": False,
            "kind": "json",
            "default": {},
        },
    ]


    def capabilities(self) -> List[Capability]:
        return [Capability.TEXT, Capability.MEDIA]  # pyright: ignore[reportReturnType] 

    async def start(self) -> None:
        self._secret = self.cfg("shared_secret", "")
        self._receivers = self.cfg_dict("receivers")  # name -> {url, headers}
        # No background tasks — the gateway routes expose the inbound +
        # outbound HTTP endpoints and call into us.
        self._healthy = True
        self._started_at = time.time()
        logger.info(
            "webhook: ready (receivers=%d, hmac=%s)",
            len(self._receivers), bool(self._secret),
        )

    async def stop(self) -> None:
        self._healthy = False

    async def handle_inbound(
        self, body: bytes, signature: Optional[str] = None
    ) -> Dict[str, Any]:
        """Called by the gateway when ``/api/channels/webhook/inbound`` is hit."""
        if not _check_signature(self._secret, body, signature):
            return {"ok": False, "error": "invalid signature"}
        import json as _json
        try:
            payload = _json.loads(body)
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": f"invalid JSON: {exc}"}
        inbound = InboundMessage(
            channel=self.name,
            chat_id=str(payload.get("chat_id", "default")),
            user_id=str(payload.get("user_id", "anon")),
            user_name=str(payload.get("user_name", "")),
            text=str(payload.get("text", "")),
            thread_id=(str(payload.get("thread_id")) if payload.get("thread_id") else None),
            reply_to_message_id=(str(payload.get("reply_to_message_id")) if payload.get("reply_to_message_id") else None),
            media=list(payload.get("media", []) or []),
            is_command=bool(payload.get("is_command", False)),
            command=payload.get("command"),
            command_args=payload.get("command_args"),
            raw=payload,
        )
        reply = await self._emit_inbound(inbound)
        return {
            "ok": True,
            "reply": (reply.text if reply else None),
            "media": (reply.media if reply else []),
        }

    async def send(self, message: OutboundMessage) -> Dict[str, Any]:
        # Send to every configured receiver that matches chat_id (or all if no filter).
        receivers = self._receivers
        text = markdown_to_plain(message.text or "")
        async with httpx.AsyncClient(timeout=30.0) as client:
            for name, recv in receivers.items():
                url = recv.get("url", "")
                if not url:
                    continue
                headers = dict(recv.get("headers", {}) or {})
                payload = {
                    "chat_id": message.chat_id,
                    "text": text,
                    "thread_id": message.thread_id,
                    "reply_to_message_id": message.reply_to_message_id,
                    "media": message.media,
                    "channel": self.name,
                }
                if self._secret:
                    body = (payload.__class__.__name__ and "") or ""  # placeholder
                    import json as _json
                    body = _json.dumps(payload, ensure_ascii=False).encode("utf-8")
                    headers["X-CVC-Signature"] = hmac.new(
                        self._secret.encode("utf-8"), body, hashlib.sha256
                    ).hexdigest()
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
        return {"ok": True}

    def _info(self) -> Dict[str, Any]:
        info = super()._info()
        info["receivers"] = list(self._receivers.keys()) if hasattr(self, "_receivers") else []
        info["hmac_enabled"] = bool(self.cfg("shared_secret", ""))
        return info
