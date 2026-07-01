"""
cvc.gateway.adapters — /api/adapters/* routes

Exposes the universal adapter registry to the dashboard:
  GET  /api/adapters             — full snapshot (every adapter, capabilities, health)
  GET  /api/adapters/{id}        — single adapter detail
  GET  /api/adapters/healthy      — only healthy adapters (for selection)
  POST /api/adapters/negotiate    — given a capability set, return the best match
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException

logger = logging.getLogger("cvc.gateway.adapters")

router = APIRouter()


def _caps_from_list(names: list[str]) -> set:
    from cvc.adapters.capabilities import Capability

    out: set[Capability] = set()
    for name in names:
        try:
            out.add(Capability(name))
        except ValueError:
            continue
    return out


@router.get("/adapters")
async def list_adapters() -> dict[str, Any]:
    """Full snapshot of every discovered adapter + capability matrix."""
    try:
        from cvc.adapters.registry import get_registry
        reg = get_registry()
        return reg.snapshot()
    except Exception as exc:
        logger.exception("list_adapters failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/adapters/healthy")
async def list_healthy_adapters() -> dict[str, Any]:
    """Only adapters currently flagged healthy — used for brain selection."""
    from cvc.adapters.registry import get_registry

    reg = get_registry()
    snap = reg.snapshot()
    return {
        "adapters": [a for a in snap["adapters"] if a["healthy"]],
        "count": sum(1 for a in snap["adapters"] if a["healthy"]),
    }


@router.get("/adapters/{adapter_id}")
async def get_adapter(adapter_id: str) -> dict[str, Any]:
    """Single adapter detail by id."""
    from cvc.adapters.registry import get_registry

    reg = get_registry()
    report = reg.get_report(adapter_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Unknown adapter: {adapter_id}")
    return report.to_dict()


@router.post("/adapters/negotiate")
async def negotiate(req: dict[str, Any]) -> dict[str, Any]:
    """
    Given a set of required capability strings, return the best-match
    healthy adapter (or null).

    Body: { "capabilities": ["streaming", "function_calling", ...] }
    """
    from cvc.adapters.registry import get_registry

    cap_names = req.get("capabilities") or []
    if not isinstance(cap_names, list):
        raise HTTPException(status_code=400, detail="capabilities must be a list")

    required = _caps_from_list(cap_names)
    if not required:
        raise HTTPException(status_code=400, detail="no valid capabilities supplied")

    reg = get_registry()
    pick = reg.negotiate(required)
    return {
        "required": sorted(c.value for c in required),
        "matched": pick.to_dict() if pick else None,
        "total_healthy": sum(1 for r in reg.list_reports() if r.healthy),
    }