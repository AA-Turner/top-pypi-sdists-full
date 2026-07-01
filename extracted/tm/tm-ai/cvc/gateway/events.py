"""
Event Spine HTTP read API.

Exposes the append-only event ledger at ~/.cvc/events/ over HTTP so
the dashboard can query, filter, and visualize the full timeline.

Endpoints
=========

  GET /api/events
    Query parameters:
      workspace       filter by workspace path (or substring match)
      channel         filter by single channel or comma-separated list
      kind            filter by single kind or comma-separated list
      actor           filter by exact actor
      session_id      filter by session id
      since           unix seconds — only events with ts >= since
      until           unix seconds — only events with ts <= until
      tags            comma-separated tags (any-match)
      search          case-insensitive substring match in summary+kind
      limit           max events (default 200, max 5000)
      offset          pagination offset
      reverse         if "true" (default), newest first

    Response:
      {
        "events": [...],
        "total": N,
        "limit": 200,
        "offset": 0,
        "has_more": true|false
      }

  GET /api/events/stats
    Aggregate counts:
      ?workspace, ?since, ?until
    Response:
      {
        "total": N,
        "by_kind": {"chat.user_message": 5, ...},
        "by_channel": {"web": 8, ...},
        "by_day": [{"day": "2026-06-30", "count": 3}, ...]
      }

  GET /api/events/info
    Diagnostic info about the spine (file count, total events, etc.)

Singularity
===========

Like the soul, the event spine is workspace-agnostic — but each
event has a `workspace` field. Queries default to ALL workspaces
(unless ?workspace= is given). This matches the singularity
principle: one body, every channel, every workspace.
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Query

logger = logging.getLogger("cvc.gateway.events")

router = APIRouter()


@router.get("/events")
async def list_events(
    workspace: str | None = Query(default=None, description="Filter by workspace path"),
    channel: str | None = Query(default=None, description="channel or comma-separated list"),
    kind: str | None = Query(default=None, description="kind or comma-separated list"),
    actor: str | None = Query(default=None),
    session_id: str | None = Query(default=None),
    since: float | None = Query(default=None, description="unix seconds"),
    until: float | None = Query(default=None, description="unix seconds"),
    tags: str | None = Query(default=None, description="comma-separated tags"),
    search: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=5000),
    offset: int = Query(default=0, ge=0),
    reverse: bool = Query(default=True),
) -> dict[str, Any]:
    """Query the event spine with filters and pagination."""
    try:
        from cvc.events.spine import query as spine_query, count as spine_count

        channel_list = _split_csv(channel)
        kind_list = _split_csv(kind)
        tags_list = _split_csv(tags)

        events = spine_query(
            workspace=workspace,
            channel=channel_list,
            kind=kind_list,
            actor=actor,
            session_id=session_id,
            since=since,
            until=until,
            tags=tags_list,
            search=search,
            limit=offset + limit + 1,  # +1 to know if there's more
            reverse=reverse,
        )

        # Apply offset
        page = events[offset : offset + limit]
        has_more = len(events) > offset + limit

        # Total = full count with filters (no pagination), but cap at 50000
        total = spine_count(
            workspace=workspace,
            channel=channel_list,
            kind=kind_list,
            actor=actor,
            since=since,
            until=until,
        )

        return {
            "events": page,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": has_more,
        }
    except Exception as exc:  # noqa: BLE001 — never break the dashboard
        logger.exception("list_events failed")
        return {"events": [], "total": 0, "limit": limit, "offset": offset,
                "has_more": False, "error": str(exc)}


@router.get("/events/stats")
async def events_stats(
    workspace: str | None = Query(default=None),
    since: float | None = Query(default=None),
    days: int = Query(default=30, ge=1, le=365, description="for daily buckets"),
) -> dict[str, Any]:
    """Aggregate counts for the dashboard."""
    try:
        from cvc.events.spine import (
            count as spine_count,
            stats_by_kind,
            stats_by_channel,
            stats_by_day,
        )
        return {
            "total": spine_count(workspace=workspace, since=since),
            "by_kind": stats_by_kind(workspace=workspace, since=since),
            "by_channel": stats_by_channel(workspace=workspace, since=since),
            "by_day": stats_by_day(workspace=workspace, days=days),
        }
    except Exception as exc:
        logger.exception("events_stats failed")
        return {"total": 0, "by_kind": {}, "by_channel": {},
                "by_day": [], "error": str(exc)}


@router.get("/events/info")
async def events_info() -> dict[str, Any]:
    """Diagnostic info about the spine."""
    try:
        from cvc.events.spine import spine_info
        return spine_info()
    except Exception as exc:
        return {"error": str(exc)}


@router.get("/events/{event_id}")
async def get_event(event_id: str) -> dict[str, Any]:
    """Fetch one event by ULID."""
    try:
        from cvc.events.spine import query as spine_query
        # Read all matching files. The spine doesn't index by id
        # for performance reasons, but events are small enough that
        # a full scan is OK. With 1000 events × 200 bytes = 200KB.
        # If this becomes slow we'll add an id→offset index in C7.
        for evt in spine_query(limit=10000, reverse=False):
            if evt.get("id") == event_id:
                return {"event": evt}
        return {"error": f"event {event_id} not found"}
    except Exception as exc:
        return {"error": str(exc)}


def _split_csv(s: str | None) -> list[str] | None:
    """Split a comma-separated string into a list, or None if empty."""
    if not s:
        return None
    out = [x.strip() for x in s.split(",") if x.strip()]
    return out or None


@router.get("/events/config")
async def events_config() -> dict[str, Any]:
    """Return current retention config + last-run stats (for dashboard admin)."""
    try:
        from cvc.events.retention import get_config
        return get_config()
    except Exception as exc:
        return {"error": str(exc)}


@router.post("/events/rotate")
async def events_rotate_now() -> dict[str, Any]:
    """Manually trigger one rotation pass (admin action).

    Useful when the dashboard wants to force a rollover — e.g. before
    running a big import, or when verifying the rotation policy works.
    """
    try:
        from cvc.events.retention import run_once
        stats = run_once()
        return {"ok": True, **stats}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@router.post("/events/purge")
async def events_purge_now(days: int | None = Query(default=None, ge=1, le=3650)) -> dict[str, Any]:
    """Manually purge events older than ``days`` (admin action).

    If ``days`` is omitted, uses the configured retention. Useful for
    one-off cleanup or testing.
    """
    try:
        from cvc.events.retention import run_once
        stats = run_once(retention_days=days)
        return {"ok": True, **stats}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}