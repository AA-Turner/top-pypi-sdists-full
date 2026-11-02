"""family outbox_stuck: writes nothing here will send without a person, the oldest past OUTBOX_STUCK_S."""

from __future__ import annotations

import asyncio
from pathlib import Path
from probe.service.watch.loop import _UNREAD, _on_daemon_thread
from probe.service.watch.settings import OUTBOX_STUCK_S, OUTBOX_TIMEOUT_S


# -- what the slower checks read --------------------------------------------------


def _age_s(stamp: object, now: float) -> float | None:
    """Seconds since an ISO stamp (a journal's `oldest_pending`), or None."""
    if not isinstance(stamp, str) or not stamp:
        return None
    try:
        from datetime import datetime, timezone

        parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return max(0.0, now - parsed.timestamp())


def outbox_condition(now: float, root: Path | None = None) -> tuple[str, dict] | None:
    """The machine's outbox (`journal.default_root`, its delivery and
    credential queues folded in) as `(reason, facts)` when one queue holds
    writes nothing here will send without a person, that queue's oldest
    OUTBOX_STUCK_S old (`blocked_oldest_pending`, judged per queue: another
    queue's old backlog never makes this one's fresh hold read as stuck):
    `auth_blocked` (an older client's queue-wide block), `credential_refused`
    (a credential the API refused, #2041) or `held` (writes set aside for a
    credential nothing here holds; a run close waiting on its data is not).
    A paused outbox is someone's switch. Counts only, never a fingerprint.
    Blocking (status files and one listing, never the op files): a thread."""
    try:
        from probe.sdk.delivery.journal.journal import Journal
        from probe.sdk.delivery.journal.paths import default_root

        status = Journal.read_status(default_root() if root is None else root)
    except Exception:  # noqa: BLE001 -- no outbox, or one this release cannot read: nothing to say
        return None
    if not isinstance(status, dict) or status.get("paused"):
        return None
    reason = status.get("blocked_reason")
    oldest = _age_s(status.get("blocked_oldest_pending"), now)
    if not isinstance(reason, str) or oldest is None or oldest < OUTBOX_STUCK_S:
        return None
    refused = status.get("refused_fingerprints")
    return reason, {"pending": _count(status.get("pending")), "oldest_pending_h": round(oldest / 3600.0, 1),
                    "held": _count(status.get("held")),
                    "refused_credentials": len(refused) if isinstance(refused, dict) else 0,
                    "dead_lettered": _count(status.get("failed"))}


def _count(value: object) -> int:
    """A status file's count, or 0 for one that is not a number."""
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError, OverflowError):
        return 0


class OutboxReadMixin:
    """Part of Watch: its methods run with `self` the Watch; compose() folds them into Watch."""

    async def _read_outbox(self, now: float) -> object:
        """`outbox_condition` on a thread of its own, given up past
        OUTBOX_TIMEOUT_S (a hung home mount), then `_UNREAD`; none started
        while the last one is still stuck there."""
        if self._outbox_busy:
            return _UNREAD
        self._outbox_busy = True

        def read() -> tuple | None:
            try:
                return self.outbox(now)
            finally:
                self._outbox_busy = False

        try:
            return await _on_daemon_thread(read, OUTBOX_TIMEOUT_S)
        except asyncio.TimeoutError:
            self.log("watch: reading the outbox did not finish in time")
            return _UNREAD
