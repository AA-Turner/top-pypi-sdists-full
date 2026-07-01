"""CVC gateway routes for external channels.

Exposes the full channel stack to the dashboard, the CLI, and any
external HTTP client (curl, n8n, scripts):

    GET    /api/channels/                  — list available + configured channels
    GET    /api/channels/{name}/status     — live status (health, last activity, errors)
    POST   /api/channels/{name}/start      — start an adapter with a config body
    POST   /api/channels/{name}/stop       — stop an adapter
    POST   /api/channels/{name}/send       — send an outbound message (test or scripted use)
    POST   /api/channels/whatsapp/webhook  — Meta WhatsApp Cloud API inbound webhook
    POST   /api/channels/webhook/inbound   — generic webhook receiver
    GET    /api/channels/webhook/health    — liveness probe

All endpoints are public from CVC's perspective (the gateway already
binds to localhost by default). Auth is the gateway's existing auth
middleware, NOT anything channel-specific.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Request

from cvc.integrations.bootstrap import get_registry
from cvc.integrations.channels.base import OutboundMessage


logger = logging.getLogger("cvc.gateway.channels")

router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# CRUD-ish surface
# ─────────────────────────────────────────────────────────────────────────────


@router.get("")
async def list_channels() -> Dict[str, Any]:
    """List every available channel + its current status."""
    reg = get_registry()
    status = reg.status()
    return {
        "channels": [
            {
                "name": s.name,
                "enabled": s.enabled,
                "healthy": s.healthy,
                "capabilities": [c.value for c in s.capabilities],
                "started_at": s.started_at,
                "last_activity_at": s.last_activity_at,
                "last_error": s.last_error,
                "info": s.info,
                "config_keys": s.config_keys,
            }
            for s in status.values()
        ]
    }


@router.get("/{name}/status")
async def channel_status(name: str) -> Dict[str, Any]:
    reg = get_registry()
    adapter = reg.get(name)
    if adapter is None:
        raise HTTPException(status_code=404, detail=f"no such channel: {name}")
    s = adapter.status()
    return {
        "name": s.name,
        "enabled": s.enabled,
        "healthy": s.healthy,
        "capabilities": [c.value for c in s.capabilities],
        "started_at": s.started_at,
        "last_activity_at": s.last_activity_at,
        "last_error": s.last_error,
        "info": s.info,
    }


@router.post("/{name}/start")
async def channel_start(name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    reg = get_registry()
    adapter = reg.get(name)
    if adapter is None:
        raise HTTPException(status_code=404, detail=f"no such channel: {name}")
    cfg = dict(payload or {})
    cfg["enabled"] = True
    try:
        await reg.start(name, cfg)
    except Exception as exc:  # noqa: BLE001
        adapter._last_error = str(exc)  # type: ignore[attr-defined]
        raise HTTPException(status_code=500, detail=f"failed to start {name}: {exc}")
    return {"ok": True, "name": name}


@router.post("/{name}/stop")
async def channel_stop(name: str) -> Dict[str, Any]:
    reg = get_registry()
    if name not in reg.list_names():
        raise HTTPException(status_code=404, detail=f"no such channel: {name}")
    try:
        await reg.stop(name)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"failed to stop {name}: {exc}")
    return {"ok": True, "name": name}


@router.post("/{name}/send")
async def channel_send(name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Send a message through a channel. Useful for testing + scripts.

    Body shape matches :class:`OutboundMessage` minus the dataclass wrapper:
        {"chat_id": "...", "text": "...", "thread_id": "...", "media": [...]}
    """
    reg = get_registry()
    if name not in reg.list_names():
        raise HTTPException(status_code=404, detail=f"no such channel: {name}")
    msg = OutboundMessage(
        chat_id=str(payload.get("chat_id", "")),
        text=str(payload.get("text", "")),
        thread_id=(str(payload.get("thread_id")) if payload.get("thread_id") else None),
        reply_to_message_id=(
            str(payload.get("reply_to_message_id"))
            if payload.get("reply_to_message_id") else None
        ),
        media=list(payload.get("media", []) or []),
        inline_keyboard=payload.get("inline_keyboard"),
        parse_mode=payload.get("parse_mode"),
        edit_message_id=(
            str(payload.get("edit_message_id"))
            if payload.get("edit_message_id") else None
        ),
        silent=bool(payload.get("silent", False)),
    )
    try:
        result = await reg.send(name, msg)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"send failed: {exc}")
    return {"ok": True, "result": result}


# ─────────────────────────────────────────────────────────────────────────────
# Webhook receivers
# ─────────────────────────────────────────────────────────────────────────────


@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request) -> Dict[str, Any]:
    """Meta WhatsApp Cloud API inbound webhook.

    Verifies the ``hub.mode`` / ``hub.verify_token`` handshake on GET and
    processes inbound message payloads on POST.
    """
    reg = get_registry()
    adapter = reg.get("whatsapp")
    if adapter is None or not hasattr(adapter, "handle_inbound_webhook"):
        raise HTTPException(status_code=503, detail="whatsapp adapter not loaded")
    body = await request.json()
    try:
        result = await adapter.handle_inbound_webhook(body)  # type: ignore[attr-defined]
    except Exception as exc:  # noqa: BLE001
        logger.exception("whatsapp webhook handler crashed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
    return result


@router.get("/whatsapp/webhook")
async def whatsapp_webhook_verify(
    request: Request,
    hub_mode: Optional[str] = None,
    hub_verify_token: Optional[str] = None,
    hub_challenge: Optional[str] = None,
) -> Any:
    """Meta Cloud API webhook verification handshake."""
    reg = get_registry()
    adapter = reg.get("whatsapp")
    expected = getattr(adapter, "cfg", lambda k, d=None: d)("verify_token", "")
    if hub_mode == "subscribe" and hub_verify_token == expected:
        # Echo the challenge back as plain text.
        from fastapi import Response
        return Response(content=str(hub_challenge or ""), media_type="text/plain")
    raise HTTPException(status_code=403, detail="verify_token mismatch")


@router.post("/webhook/inbound")
async def generic_webhook_inbound(request: Request) -> Dict[str, Any]:
    """Generic inbound webhook receiver — see :class:`WebhookAdapter`."""
    reg = get_registry()
    adapter = reg.get("webhook")
    if adapter is None or not hasattr(adapter, "handle_inbound"):
        raise HTTPException(status_code=503, detail="webhook adapter not loaded")
    body = await request.body()
    signature = request.headers.get("X-CVC-Signature")
    return await adapter.handle_inbound(body, signature)  # type: ignore[attr-defined]



@router.get("/webhook/health")
async def webhook_health() -> Dict[str, Any]:
    reg = get_registry()
    return {"ok": True, "channels": reg.list_names()}
