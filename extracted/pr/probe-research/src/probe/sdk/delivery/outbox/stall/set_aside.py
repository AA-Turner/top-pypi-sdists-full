"""What the worker does about a stalled run between passes: set its stuck write aside (R9, R12),
and tell the server once per run and cause, retrying a report it did not take (D5)."""

from __future__ import annotations

import json
from typing import Any

from probe.sdk.delivery.outbox.held import HeldCause, hold_lane, hold_op, is_set_aside_alone
from probe.sdk.delivery.outbox.stall import stall as _stall
from probe.sdk.delivery.outbox.stall.stall import DeliveryStallCause, StallReport

#: The longest the worker waits for another drain's lock before it sets anything aside (then:
#: after the next pass).
_LOCK_WAIT_SECONDS = 2.0


def set_aside_stalled(journal: Any, tracker: Any, lanes: Any) -> int:
    """Set each due stuck write (`ProgressTracker.due_stalls`) aside, under the drain lock so no
    other pass is between two ops. A metric, step or upload moves to held/ alone, and only with
    its run's lock (another drain may be sending it, its drain lock let go: #3618); anything
    else holds its whole run lane in place. Returns how many were set aside."""
    from probe.foundation.os_backend import os_backend as oscompat

    due = tracker.due_stalls()
    if not due:
        return 0
    try:
        handle = journal.drain_lock.open("a+")
    except OSError:
        return 0
    moved: list = []
    try:
        if not _take_drain_lock(handle, wait_for_lock=True, timeout=_LOCK_WAIT_SECONDS):
            return 0
        try:
            moved = [head for head in due if _set_aside(journal, head)]
        finally:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
    finally:
        handle.close()
    for head in moved:
        tracker.note_set_aside(head)
        # Tried next pass with its ladder kept (I14): in a 503 storm the next write fails too
        # and must not restart at 2 s every stall window.
        lanes.retry_now(head.lane)
        tracker.queue_report(head.run_ref, DeliveryStallCause.STALLED, head.error)
    if moved:
        send_due_reports(tracker)
    return len(moved)


def _set_aside(journal: Any, head: Any) -> bool:
    try:
        op = json.loads(head.path.read_text())
    except (OSError, ValueError):
        return False  # gone: delivered meanwhile
    if not isinstance(op, dict):
        return False
    if not is_set_aside_alone(op):
        if not isinstance(head.lane, str):
            return False
        return hold_lane(journal.dir, head.lane, head.path, run_ref=head.run_ref, error=head.error)
    with holding_run_lock(journal, head.lane) as locked:
        if not locked:
            return False  # another drain is sending it: after the next pass
        return hold_op(head.path, op, cause=HeldCause.STALLED) is not None


def report_new_stalls(tracker: Any, report: Any) -> None:
    """After a pass: owe a report for each run with a write refused for good, or whose
    credential was refused; then send what is due."""
    for record in report.dead_letter_records:
        ref = record.get("run_ref")
        if isinstance(ref, str):
            tracker.queue_report(ref, DeliveryStallCause.REFUSED, record.get("error"))
    lane_refs = getattr(report, "lane_refs", {})
    for lane, stall in report.stalled_runs.items():
        ref = lane_refs.get(lane, lane)
        if isinstance(ref, str) and stall.status in (401, 403) and not stall.held:
            tracker.queue_report(ref, DeliveryStallCause.LOGIN_REFUSED, stall.error)
    send_due_reports(tracker)


def send_due_reports(tracker: Any) -> None:
    """Send each owed report whose time has come, with the counts the record last published."""
    due = tracker.due_reports()
    if not due:
        return
    tracker.publish(force=True)
    for ref, cause, error in due:
        run = tracker.runs.get(ref)
        body = StallReport(
            cause=str(cause),
            held=int(getattr(run, "held", 0) or 0),
            failed=int(getattr(run, "failed", 0) or 0),
            op_count=int(getattr(run, "pending", 0) or 0),
            first_error=error,
        )
        taken = _stall.send_stall_report(ref, body, tracker.context_of(ref))
        # A refused credential refuses its own report too: one try, then the server's beats
        # and its silence path carry it.
        tracker.note_report_result(ref, cause, taken=taken, final=cause == DeliveryStallCause.LOGIN_REFUSED)
from probe.sdk.delivery.outbox.drain.lock import _take_drain_lock, holding_run_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
