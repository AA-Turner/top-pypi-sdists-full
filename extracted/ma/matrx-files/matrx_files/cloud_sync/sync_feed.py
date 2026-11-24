"""THE device-replica change feed, one implementation for every host that serves it.

``GET /files/sync/changes`` (the standalone service, ``api/router_files.py``) and the
Cloud Computer bridge (aidream ``/cloud-files/sync/changes``) read the same two sources
through this module, so a fix to one is a fix to both:

1. the ``(updated_at, id)`` keyset over ``files.files`` — rows that share an
   ``updated_at`` are never skipped at a page boundary;
2. the relocation ledger (``files.file_pathway_move``) — the placement mover keeps
   ``updated_at``, so source 1 never re-sends a moved row; the ledger re-sends it at its
   new path (a device renames by ``file_id``) or as a tombstone when it left the
   visible set.

The two sources are served as ONE causal stream: a page is the merge of both by time
(a keyset row at its ``updated_at``, a ledger mark at its ``feed_at``), and each cursor
half advances only past what the page emitted. Serving every relocation first (the
first version) applied a move onto a path BEFORE the tombstone of the file that left
that path, so a device turned the departed file into a conflict copy and then deleted
the moved file by path (review 2026-11-02, defect 1).

Protocol: the first call with neither ``since`` nor ``cursor`` is the bootstrap (alive
rows only, from the beginning); every page returns ``next_cursor`` — opaque, stored and
passed back forever. Once the bootstrap drains the cursor flips tombstone-aware, so
deletions ride the same feed. ``since`` (ISO-8601) is the entry point for a client that
kept a raw ``updated_at`` watermark; it is tombstone-aware from the start.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any


def encode_sync_cursor(
    ts: datetime,
    row_id: str,
    include_deleted: bool,
    moves: tuple[datetime, str] | None = None,
) -> str:
    """``moves`` is the relocation-ledger position (``files.file_pathway_move`` feed_at, id) — the
    feed's second source (placement registry § 7). Absent = no ledger mark consumed yet."""
    body: dict[str, Any] = {"v": 1, "ts": ts.isoformat(), "id": row_id, "d": bool(include_deleted)}
    if moves is not None:
        body["m"] = [moves[0].isoformat(), moves[1]]
    payload = json.dumps(body, separators=(",", ":"))
    return base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")


def decode_sync_cursor_moves(cursor: str) -> tuple[datetime, str] | None:
    """The relocation-ledger position a cursor carries, or ``None`` (a cursor minted before the
    ledger joined the feed replays the owner's ledger once — every mark is idempotent)."""
    padded = cursor + "=" * (-len(cursor) % 4)
    data = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())
    m = data.get("m") if isinstance(data, dict) else None
    if not m:
        return None
    return datetime.fromisoformat(m[0]), str(m[1])


def decode_sync_cursor(cursor: str) -> tuple[datetime, str, bool]:
    """Decode an opaque sync cursor. Raises ValueError (→ 400) on garbage."""
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        data = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())
        if not isinstance(data, dict):
            raise ValueError("cursor payload is not an object")
        if data.get("v") != 1:
            raise ValueError(f"unknown cursor version {data.get('v')!r}")
        return (
            datetime.fromisoformat(data["ts"]),
            str(data["id"]),
            bool(data.get("d")),
        )
    except (ValueError, KeyError, TypeError, AttributeError, json.JSONDecodeError) as e:
        raise ValueError(f"malformed sync cursor: {e}") from e


@dataclass
class SyncChangesPage:
    """One page: relocations and keyset rows in one causal order (raw ``_SYNC_CHANGE_FIELDS`` dicts)."""

    rows: list[dict[str, Any]]
    next_cursor: str
    has_more: bool


def _as_datetime(value: Any) -> datetime:
    return value if isinstance(value, datetime) else datetime.fromisoformat(str(value))


async def read_sync_changes_page(
    engine: Any,
    *,
    user_id: str,
    cursor: str | None = None,
    since: str | None = None,
    limit: int = 500,
    include_system: bool = False,
) -> SyncChangesPage:
    """Read one page of the device feed through ``engine`` (a ``SyncEngine``).

    Raises ``ValueError`` for a malformed ``cursor``/``since`` (the caller answers 400)."""
    if cursor:
        cursor_ts, cursor_id, include_deleted = decode_sync_cursor(cursor)
        moves_pos = decode_sync_cursor_moves(cursor)
    elif since:
        cursor_ts = datetime.fromisoformat(since.replace("Z", "+00:00"))
        cursor_id, include_deleted = "", True
        # A raw watermark: relocations after it are what this client has not seen.
        moves_pos = (cursor_ts, "")
    else:
        cursor_ts, cursor_id, include_deleted = None, "", False
        # Bootstrap reads current state, so earlier moves are already in it; moves that
        # happen while it pages arrive once it flips tombstone-aware.
        moves_pos = (datetime.now(UTC) - timedelta(seconds=10), "")

    # Both sources, each up to ``limit`` past its own position; the page is the first
    # ``limit`` of their merge by time. Any unread item of a source that filled its read sorts
    # after all ``limit`` items it returned, so it can never belong in this page.
    moved: list[dict[str, Any]] = []
    last_move: tuple[Any, str] | None = None
    if include_deleted:
        moved, last_move = await engine.list_sync_relocations_async(
            after_ts=moves_pos[0] if moves_pos else None,
            after_id=(moves_pos[1] or None) if moves_pos else None,
            include_system=include_system,
            limit=limit,
            user_id=user_id,
        )
    rows = await engine.list_sync_changes_async(
        cursor_ts=cursor_ts,
        cursor_id=cursor_id or None,
        include_deleted=include_deleted,
        include_system=include_system,
        limit=limit,
        user_id=user_id,
    )
    moves_full = last_move is not None and len(moved) >= limit
    main_full = len(rows) >= limit

    def move_key(entry: dict[str, Any]) -> tuple[datetime, int, str]:
        pos = entry.get("_move_pos") or last_move
        return (_as_datetime(pos[0]), 1, str(pos[1]))

    merged = sorted(
        [(move_key(m), "m", m) for m in moved]
        + [((_as_datetime(r["updated_at"]), 0, str(r["id"])), "k", r) for r in rows],
        key=lambda item: item[0],
    )
    page = merged[:limit]
    emitted_moves = [item for item in page if item[1] == "m"]
    emitted_rows = [item[2] for item in page if item[1] == "k"]
    if emitted_moves:
        # Every mark read was emitted: the reader's own last position (it also covers marks it
        # skipped as repeats). Otherwise the last emitted mark's own position.
        if len(emitted_moves) == len(moved) and last_move is not None:
            moves_pos = (_as_datetime(last_move[0]), str(last_move[1]))
        elif emitted_moves[-1][2].get("_move_pos"):
            pos = emitted_moves[-1][2]["_move_pos"]
            moves_pos = (_as_datetime(pos[0]), str(pos[1]))
        # else: a reader that does not say each mark's position — keep the old one; the emitted
        # marks come again next page (every mark is idempotent), none is ever skipped.
    elif last_move is not None and not moved:
        moves_pos = (_as_datetime(last_move[0]), str(last_move[1]))
    rows_left = len(rows) - len(emitted_rows)
    has_more = len(merged) > limit or moves_full or main_full
    if emitted_rows:
        last = emitted_rows[-1]
        # Once a feed position exists, future polls must see tombstones —
        # the bootstrap-only alive filter applies just until it drains.
        next_d = include_deleted or not (main_full or rows_left > 0)
        next_cursor = encode_sync_cursor(_as_datetime(last["updated_at"]), str(last["id"]), next_d, moves_pos)
    elif cursor_ts is not None:
        # No keyset row emitted at a known position: tombstone-aware from here once the
        # keyset is drained (a bootstrap ending on an empty page flips too).
        next_cursor = encode_sync_cursor(cursor_ts, cursor_id, include_deleted or not rows, moves_pos)
    else:
        # Empty bootstrap (no files yet): anchor at epoch, tombstone-aware.
        next_cursor = encode_sync_cursor(datetime(1970, 1, 1, tzinfo=UTC), "", True, moves_pos)
    out = [{k: v for k, v in item[2].items() if k != "_move_pos"} for item in page]
    return SyncChangesPage(rows=out, next_cursor=next_cursor, has_more=has_more)


__all__ = [
    "SyncChangesPage",
    "decode_sync_cursor",
    "decode_sync_cursor_moves",
    "encode_sync_cursor",
    "read_sync_changes_page",
]
