from __future__ import annotations

import asyncio
import time
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from matrx_utils import vcprint

from matrx_ai.db._registry import get_model

_CACHE_TTL_SECONDS = 60.0

_cached_classes: dict[str, dict[str, Any]] = {}
_cache_timestamp: float = 0.0
_cache_lock = asyncio.Lock()


def _is_cache_fresh() -> bool:
    return bool(_cached_classes) and (time.monotonic() - _cache_timestamp) < _CACHE_TTL_SECONDS


async def _refresh_cache() -> None:
    global _cached_classes, _cache_timestamp

    try:
        OpsIssueClass = get_model("OpsIssueClass")
        rows = await OpsIssueClass.filter().order_by("key").all()
        new_cache: dict[str, dict[str, Any]] = {}
        for inst in rows:
            new_cache[inst.key] = inst.to_dict()

        _cached_classes = new_cache
        _cache_timestamp = time.monotonic()

    except Exception as exc:
        vcprint(
            f"[OpsIssueRegistry] Failed to refresh issue class cache: {exc}",
            color="yellow",
        )


async def get_issue_class(key: str) -> dict[str, Any] | None:
    if not _is_cache_fresh():
        async with _cache_lock:
            if not _is_cache_fresh():
                await _refresh_cache()

    return _cached_classes.get(key)


async def get_all_classes() -> dict[str, dict[str, Any]]:
    if not _is_cache_fresh():
        async with _cache_lock:
            if not _is_cache_fresh():
                await _refresh_cache()

    return dict(_cached_classes)


async def auto_register_class(
    key: str,
    *,
    name: str | None = None,
    category: str = "unknown",
    provider: str | None = None,
    severity: str = "medium",
) -> dict[str, Any] | None:
    try:
        OpsIssueClass = get_model("OpsIssueClass")
        now = datetime.now(timezone.utc)

        inst = await OpsIssueClass.create(
            id=str(uuid4()),
            key=key,
            name=name or key.replace(".", " ").replace("_", " ").title(),
            category=category,
            provider=provider,
            severity=severity,
            disposition="monitor",
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        new_row = inst.to_dict()
        _cached_classes[key] = new_row

        vcprint(
            f"[OpsIssueRegistry] Auto-registered new issue class: {key}",
            color="yellow",
        )
        return new_row

    except Exception as exc:
        vcprint(
            f"[OpsIssueRegistry] Failed to auto-register issue class '{key}': {exc}",
            color="yellow",
        )
        return None
