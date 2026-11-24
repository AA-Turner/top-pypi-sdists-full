from __future__ import annotations

import asyncio
import time
from datetime import UTC, datetime, timezone
from typing import Any
from uuid import uuid4

from matrx_utils import vcprint
from matrx_utils.text_case import humanize_identifier

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
            name=name or humanize_identifier(key),
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


def is_settled(issue_class: dict[str, Any]) -> bool:
    """Settled = a person verified the class resolved (``is_active=false`` / ``disposition='suppress'``)."""
    return (not issue_class.get("is_active", True)) or issue_class.get("disposition") == "suppress"


async def reopen_settled_class(
    issue_class: dict[str, Any], *, message: str, disposition: str = "monitor"
) -> bool:
    """A recurrence reopens a settled class, through the package's own ``OpsIssueClass`` model.

    The event is recorded either way (a settled class must never hide its recurrences); this makes the
    triage surfaces read the class as open again. The previous resolution note is kept under the new one.
    Returns True when it reopened; never raises (a failed reopen is announced, the event still lands)."""
    if not is_settled(issue_class):
        return False
    try:
        OpsIssueClass = get_model("OpsIssueClass")
        now = datetime.now(UTC)
        previous = str(issue_class.get("resolution_notes") or "").strip()
        note = f"REOPENED {now.isoformat()}: recurred after being settled - {message[:300]}"
        await OpsIssueClass.filter(id=issue_class["id"]).update(
            disposition=disposition,
            is_active=True,
            resolution_notes=f"{note}\n\nPrevious: {previous}" if previous else note,
            updated_at=now,
        )
        issue_class["is_active"] = True
        issue_class["disposition"] = disposition
        cached = _cached_classes.get(str(issue_class.get("key")))
        if cached is not None:
            cached.update(is_active=True, disposition=disposition)
        vcprint(
            f"[OpsIssueRegistry] Reopened settled issue class: {issue_class.get('key')}",
            color="yellow",
        )
        return True
    except Exception as exc:  # noqa: BLE001 - announced, and the event is still recorded
        vcprint(
            f"[OpsIssueRegistry] Failed to reopen settled class '{issue_class.get('key')}': {exc}",
            color="red",
        )
        return False
