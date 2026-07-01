"""
cvc.gateway.swarm — /api/swarm/* routes

Exposes the swarm primitives to the dashboard:
  GET   /api/swarm/identity        — this owner's peer identity
  POST  /api/swarm/rename          — change display name
  GET   /api/swarm/policy          — current share policy
  POST  /api/swarm/policy          — update share policy
  GET   /api/swarm/peers           — known peers
  POST  /api/swarm/peers           — add a peer manually
  DELETE /api/swarm/peers/{id}     — forget a peer
  POST  /api/swarm/broadcast       — send an insight to the swarm
  GET   /api/swarm/inbox           — recent incoming broadcasts
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

logger = logging.getLogger("cvc.gateway.swarm")

router = APIRouter()


def _swarm_dir() -> Path:
    candidates = [Path.cwd() / ".cvc" / "vault" / "swarm", Path.home() / ".cvc" / "vault" / "swarm"]
    for p in candidates:
        if p.exists():
            return p
    p = candidates[-1]
    p.mkdir(parents=True, exist_ok=True)
    return p


def _node():
    from cvc.swarm import SwarmNode

    return SwarmNode(_swarm_dir())


# ── identity ─────────────────────────────────────────────────────────


@router.get("/swarm/identity")
async def swarm_identity() -> dict[str, Any]:
    try:
        node = _node()
        return node.identity().to_dict()
    except Exception as exc:
        logger.exception("swarm/identity failed")
        raise HTTPException(500, str(exc))


@router.post("/swarm/rename")
async def swarm_rename(req: dict[str, Any]) -> dict[str, Any]:
    name = (req.get("display_name") or "").strip()
    if not name:
        raise HTTPException(400, "display_name required")
    try:
        return _node().rename(name).to_dict()
    except ValueError as exc:
        raise HTTPException(400, str(exc))


# ── share policy ─────────────────────────────────────────────────────


@router.get("/swarm/policy")
async def swarm_policy() -> dict[str, Any]:
    return _node().policy().to_dict()


@router.post("/swarm/policy")
async def swarm_policy_update(req: dict[str, Any]) -> dict[str, Any]:
    from cvc.swarm import SharePolicy

    fields = {k: v for k, v in req.items() if k in SharePolicy.__dataclass_fields__}
    if not fields:
        raise HTTPException(400, "no valid policy fields supplied")
    try:
        _node().set_policy(SharePolicy(**fields))
        return _node().policy().to_dict()
    except Exception as exc:
        logger.exception("policy update failed")
        raise HTTPException(500, str(exc))


# ── peers ────────────────────────────────────────────────────────────


@router.get("/swarm/peers")
async def swarm_peers() -> dict[str, Any]:
    peers = _node().known_peers()
    return {"peers": [p.to_dict() for p in peers], "count": len(peers)}


@router.post("/swarm/peers")
async def swarm_peers_add(req: dict[str, Any]) -> dict[str, Any]:
    from cvc.swarm import Peer

    try:
        peer = Peer(
            **{
                k: v
                for k, v in req.items()
                if k in Peer.__dataclass_fields__
            }
        )
    except Exception as exc:
        raise HTTPException(400, f"invalid peer payload: {exc}")
    if not peer.peer_id or not peer.address:
        raise HTTPException(400, "peer_id and address required")
    _node().add_peer(peer)
    return peer.to_dict()


@router.delete("/swarm/peers/{peer_id}")
async def swarm_peers_remove(peer_id: str) -> dict[str, Any]:
    _node().remove_peer(peer_id)
    return {"ok": True, "removed": peer_id}


# ── broadcasts ───────────────────────────────────────────────────────


@router.post("/swarm/broadcast")
async def swarm_broadcast(req: dict[str, Any]) -> dict[str, Any]:
    topic = (req.get("topic") or "").strip()
    payload = req.get("payload") or {}
    if not topic:
        raise HTTPException(400, "topic required")
    if not isinstance(payload, dict):
        raise HTTPException(400, "payload must be an object")
    bc = _node().broadcast(topic=topic, payload=payload)
    return bc.to_dict()


@router.get("/swarm/inbox")
async def swarm_inbox(limit: int = 50) -> dict[str, Any]:
    items = _node().inbox(limit=limit)
    return {"broadcasts": [b.to_dict() for b in items], "count": len(items)}