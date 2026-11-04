"""After the worker delivered a run's close: wait until the server has STORED the run's queued data
(its applied watermark), then raise for what it refused on this attempt (infra I15d)."""

from __future__ import annotations

import sys
import time
from typing import Any, Callable

#: How often the run is read again while the server reports data accepted but not stored.
POLL_SECONDS = 1.0
PROGRESS_EVERY_SECONDS = 5.0


def wait_for_stored_data(
    read_row: Callable[[], Any],
    row: Any,
    *,
    run_ref: str,
    write_epoch: int | None,
    deadline: float | None = None,
    on_progress: Callable[[str], None] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> Any:
    """``row``: the run as just read (`GET /v1/runs/{id}`), None when that read failed; ``read_row``
    reads it again (None on a failed read, asked again). A server without the ingest queue, or a team
    off it, serves no `ingest`: the row comes back as is. Otherwise waits until the applied watermark
    reaches what was accepted when the wait began (another writer still logging never holds it), a
    line every ~5 s, with no time cap (the user's decision) unless the caller set one: ``deadline``
    (monotonic; `flush_timeout`, a SIGTERM's grace), past which, like Ctrl-C, it returns the last row
    while the server stores on. Raises `DeliveryIncomplete` (`DATA_REFUSED`) for refusals on
    ``write_epoch``."""
    from probe.sdk.delivery.outbox.waiter import DeliveryIncomplete, WaitOutcome, WaitResult

    say = on_progress or _print_progress
    started = said = clock()
    try:
        while not isinstance(row, dict):  # the read failed: the store is unknown, not done
            if deadline is not None and clock() >= deadline:
                return row
            sleep(POLL_SECONDS)
            row = read_row()
        ingest = _get_ingest(row)
        if ingest is None:
            return row
        # A run's messages share one partition, so its offsets compare: this one is the last accepted.
        target = ingest.get("accepted_offset")
        while not _has_reached(ingest, target):
            now = clock()
            if deadline is not None and now >= deadline:
                say(_render_line(run_ref, ingest, now - started, has_stopped=True))
                return row
            if now - said >= PROGRESS_EVERY_SECONDS:
                said = now
                say(_render_line(run_ref, ingest, now - started))
            sleep(POLL_SECONDS)
            fresh = read_row()
            if _get_ingest(fresh) is not None:
                row, ingest = fresh, _get_ingest(fresh)
    except KeyboardInterrupt:
        return row
    refusals = [r for r in ingest.get("refusals") or () if _is_this_attempt(r, write_epoch)]
    if refusals:
        raise DeliveryIncomplete(WaitResult(outcome=WaitOutcome.DATA_REFUSED, run_ref=run_ref, refusals=refusals))
    return row


def _has_reached(ingest: dict, target: Any) -> bool:
    """Is every message accepted up to ``target`` applied (stored or refused)?"""
    if not isinstance(target, int):
        return bool(ingest.get("is_caught_up", True))  # nothing was accepted, or an odd answer
    applied = ingest.get("applied_offset")
    return isinstance(applied, int) and applied >= target


def _get_ingest(row: Any) -> dict | None:
    ingest = row.get("ingest") if isinstance(row, dict) else None
    return ingest if isinstance(ingest, dict) else None


def _is_this_attempt(refusal: Any, write_epoch: int | None) -> bool:
    """A refusal of this attempt's writes: its epoch, or one the batch did not name."""
    if not isinstance(refusal, dict):
        return False
    epoch = refusal.get("write_epoch")
    return write_epoch is None or epoch is None or epoch == write_epoch


def _render_line(run_ref: str, ingest: dict, waited: float, *, has_stopped: bool = False) -> str:
    points = int(ingest.get("pending_points") or 0)
    amount = f"{points:,} point(s)" if points else "its last data"
    if has_stopped:
        return (
            f"probe: run {run_ref}: stopped waiting after {round(waited)} s (the limit you set); the "
            f"server is still storing {amount} and does so without this process"
        )
    return (
        f"probe: run {run_ref}: delivered; the server is still storing {amount} "
        f"({round(waited)} s so far); Ctrl-C to stop waiting"
    )


def _print_progress(line: str) -> None:
    try:
        print(line, file=sys.stderr, flush=True)
    except Exception:  # noqa: BLE001 -- a closed stderr never stops the wait
        pass
