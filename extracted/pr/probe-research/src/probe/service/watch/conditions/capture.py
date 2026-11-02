"""family capture_stalled: a live session's transcript waiting past its last receipt."""

from __future__ import annotations
from collections.abc import Mapping
from probe.service.watch.settings import CAPTURE_STALL_S


def capture_conditions(receipts: Mapping, now: float, still: dict | None = None) -> dict[str, dict]:
    """`{sid: facts}` for each session whose transcript has waited
    CAPTURE_STALL_S, not finalized: complete lines (or, not yet counted, bytes)
    or a staged batch waiting. Its age is from when `still` (the caller's, kept
    across calls: sid -> (`received_bytes`, since when, last seen offline))
    first saw it waiting with its cursor where it is now (never before its last
    receipt, `received_at`). A receipt says when the last batch landed, not
    when what waits now was written: aged from it, a session idle 11 h and then
    used again read as stalled 11 h minutes after its next prompt (10-28, New
    Workspace), as did one resumed after hours closed. So a stall already
    running when this watch first sees it (a service just started) is reported
    an hour after that sighting. A session whose last upload had no network
    (`offline`) is not stalled, and once back is aged from the last time it
    was offline. A trailing line with no newline yet is not waiting."""
    still = {} if still is None else still
    found = {}
    for sid in [s for s in still if s not in receipts]:
        del still[sid]
    for sid, receipt in receipts.items():
        if not isinstance(receipt, Mapping) or receipt.get("finalized"):
            still.pop(sid, None)
            continue
        lines = receipt.get("pending_lines")
        waiting = (lines > 0 if isinstance(lines, int) else int(receipt.get("pending_bytes") or 0) > 0) \
            or bool(receipt.get("pending_batch"))
        if not waiting:
            still.pop(sid, None)
            continue
        cursor = receipt.get("received_bytes")
        seen = still.get(sid)
        if seen is None or seen[0] != cursor:
            seen = (cursor, now, None)
        if receipt.get("offline"):
            # No network at all: the laptop's, not a stall. Once it is back, the
            # wait counts from the last time it was offline, not its last receipt.
            still[sid] = (seen[0], seen[1], now)
            continue
        still[sid] = seen
        received_at = receipt.get("received_at")
        stamped = isinstance(received_at, (int, float))
        since = max(received_at, seen[1]) if stamped else seen[1]
        offline_at = seen[2] if len(seen) > 2 else None
        if offline_at is not None:
            since = max(since, offline_at)
        if now - since < CAPTURE_STALL_S:
            continue
        # `received_h`: since its last receipt (the oldest first in the report);
        # `waiting_h`: how long what waits has been seen waiting.
        found[sid] = {"received_h": round((now - (received_at if stamped else seen[1])) / 3600.0, 1),
                      "waiting_h": round((now - since) / 3600.0, 1),
                      "receipt": "received_at" if stamped else "unmoved",
                      "pending_bytes": receipt.get("pending_bytes"), "pending_lines": lines,
                      "pending_batch": bool(receipt.get("pending_batch")), "retrying": bool(receipt.get("retrying"))}
    return found


async def _no_receipts() -> dict:
    return {}
