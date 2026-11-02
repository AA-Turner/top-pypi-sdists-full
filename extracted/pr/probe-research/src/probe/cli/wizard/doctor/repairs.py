"""probe doctor's outbox repairs: drop dead letters no retry can deliver, rescue stranded writes."""

from __future__ import annotations
import sys


def drop_unrecoverable_dead_letters() -> list[str]:
    """`probe doctor --fix`: dead letters no retry can deliver -- a superseded
    run attempt's, or a run the server says does not exist, asked again with
    the write's own credential -- move to `discarded/` (kept, never sent; #3629,
    T24), and what that did. Every other dead letter stays for `probe outbox
    retry`. Empty when nothing moved."""
    try:
        from probe import analytics as telemetry
        from probe.sdk.delivery.journal.journal import Journal

        counts = Journal().drop_unrecoverable()
        if not counts.writes:
            return []
        telemetry.emit_outbox_discarded(
            counts, reason=telemetry.DiscardReason.UNRECOVERABLE, interactive=sys.stdin.isatty()
        )
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return []
    return [
        f"Set aside {counts.writes} dead-lettered write(s) that can never be delivered "
        "(a newer attempt took their run over, or the run no longer exists); "
        "they are kept in the outbox's discarded/ folder."
    ]


def rescue_outbox() -> dict | None:
    """`probe doctor`'s fix: rescue, now, writes stranded under a dead
    credential of the logged-in account (`journal.rescue_stranded`; any
    `probe` command does it by itself every 10 minutes) and start sending
    them in the background. Under the one rescue lock; None when there is
    nothing to say, or another rescue is running."""
    try:
        from probe.sdk.delivery import outbox as outbox_worker
        from probe.sdk.delivery.journal.journal import Journal
        from probe.sdk.delivery.outbox.drain.credentials import _stored_login_fingerprint
        from probe.sdk.delivery.journal.item_locks import _try_lock
        from probe.sdk.delivery.outbox.drain.adoption import (
            rescue_lock_path,
            rescue_stranded)

        root = Journal()
        if not outbox_worker.rescue_enabled() or root.paused:
            return None
        login = _stored_login_fingerprint(None)
        here = set(outbox_worker.env_fingerprints()) | ({login} if login else set())
        lock = rescue_lock_path()
        lock.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with _try_lock(lock) as mine:
            if not mine:
                return None
            report = rescue_stranded(root, here=here)
        if report.rescued or report.adopted_waiting:
            outbox_worker.spawn_rescuer(root)
        if not (report.rescued or report.refused or report.adopted_waiting):
            return None
        return {
            "rescued": dict(report.rescued),
            "cannot_rescue": {fp: str(why) for fp, why in report.refused.items()},
            "adopted_waiting": report.adopted_waiting,
        }
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None
