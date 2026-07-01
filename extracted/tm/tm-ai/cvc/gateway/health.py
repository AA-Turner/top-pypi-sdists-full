"""
Health router — /health, /api/health
"""

from __future__ import annotations

import logging
import time

from fastapi import APIRouter

from cvc import __version__

logger = logging.getLogger("cvc.gateway.health")

router = APIRouter()

_START = time.time()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "cvc-gateway",
        "version": __version__,
        "uptime_seconds": round(time.time() - _START, 2),
    }


@router.get("/api/health")
async def api_health():
    return await health()
