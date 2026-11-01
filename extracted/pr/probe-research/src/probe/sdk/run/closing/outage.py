"""reopen a run the reaper ended while this process could not be heard."""

from __future__ import annotations
import weakref
from typing import TYPE_CHECKING, Any
from uuid import uuid4

if TYPE_CHECKING:  # Run only in annotations: importing it here would loop back into run.py
    from ..run import Run

    from ...client.client import Client


def _recover_after_outage(
    client: "Client",
    run_id: str,
    *,
    role: str,
    write_epoch: int | None,
    handle_ref: "weakref.ref[Run] | None" = None,
    system_verdict_only: bool = False,
) -> Any:
    """Reopen a run the reaper ended while this process could not be heard.

    Returns the epoch the run was reopened under, None when there was nothing
    to do (or nothing this process may do), or ``_RECOVERY_RETRY``.

    Deliberately narrow. Only an OWNER recovers -- an observer never staked its
    lifetime on the run and has no standing to resurrect it. Only 'crashed' is
    recovered: that is the verdict meaning "an owner was beating and stopped",
    which is exactly what an outage manufactures. And only when the row's epoch
    still matches ours, so a newer attempt that legitimately took the run over
    is never clobbered by the old process waking up. A handle that does not
    know its epoch cannot prove that, so it does not recover.

    The reopen KEEPS the epoch (SDK reliability 1.1). It used to bump it, and
    every op this process had already queued still carried the old one: the
    server fenced each with 409 and the drain dead-lettered it (live: a
    20-minute outage lost 2,478 of 2,659 steps), and every OTHER rank of the
    same job, still on the old epoch, was fenced for the rest of the run. The
    server honours `keep_epoch` only for a `crashed` row still on
    `expected_write_epoch`, so a writer a newer attempt superseded cannot use
    it to take the run back.

    An older server drops `keep_epoch` and would bump anyway, so there the
    reopen is SKIPPED (G1: `supports_feature` plus a fallback, not
    `_require_feature`, whose raise this thread would swallow). Nothing is lost
    by skipping: a crashed row still takes data (the fence refuses only an
    epoch OLDER than the row's), and `finish()` still writes the real verdict.

    Every failure here is swallowed: this is best-effort repair on a background
    thread, and it must never take down the work it is reporting on. A failure
    that may pass (a transport error, a 5xx) returns ``_RECOVERY_RETRY`` so the
    beat loop tries again; anything else (a 409: a sibling rank recovered it
    first, or a newer attempt owns it) ends the attempt.

    ``system_verdict_only`` (2.2) is for a beat that LANDED on a crashed row,
    with no failed beat to explain it: only a verdict the system made -- the
    reaper's (``reason: stale``) or a writer-gone report's -- is repaired. A
    person or an agent that set ``crashed`` on purpose (``probe run end
    --status crashed`` on a hung job whose beat thread still runs) meant it.
    """
    if role != "owner" or write_epoch is None:
        return None
    try:
        # Feature first: it is cached per client, so on an older server a beat
        # that keeps landing on the crashed row costs no request at all.
        if not client.supports_feature("run_reopen_keep_epoch"):
            return None
        row = client.get_run(run_id)
        if row.get("status") != "crashed":
            return None
        if row.get("write_epoch") != write_epoch:
            return None
        if system_verdict_only and not _crashed_by_the_system(client, run_id):
            return None
        # 2.8: a leased writer recovers under its OWN lease, so a GONE a wrong
        # writer-gone report left on it is undone (the server revives it), and
        # its later release does not close the run `crashed`.
        handle = handle_ref() if handle_ref is not None else None
        lease = getattr(handle, "_lease", None) if handle is not None else None
        receipt = client.reopen_run(
            run_id,
            session_id=lease["session_id"] if lease else str(uuid4()),
            keep_epoch=True,
            expected_write_epoch=write_epoch,
            writer=lease,
        )
    except Exception as exc:  # noqa: BLE001 -- see docstring
        from ...delivery.ops.classify import classify

        try:
            transient = classify(exc) == "transient"
        except Exception:  # noqa: BLE001
            transient = False
        return _RECOVERY_RETRY if transient else None
    new_epoch = receipt.get("write_epoch") if isinstance(receipt, dict) else None
    if new_epoch is None:
        return None
    new_epoch = int(new_epoch)
    # The handle is held WEAKLY so the beat thread still does not pin it: an
    # abandoned Run must stay collectable, and its collection is what ends the
    # beat. If it is already gone there is nothing left to write anyway.
    handle = handle_ref() if handle_ref is not None else None
    if handle is not None:
        handle.write_epoch = new_epoch
    return new_epoch


#: The `reason` a system-made `crashed` carries on its status event: the
#: reaper's stale sweep, and a writer-gone report (2.2). A status PATCH -- a
#: person, an agent, a launcher -- carries none.
_SYSTEM_CRASH_REASONS = frozenset({"stale", "writer_gone"})


def _crashed_by_the_system(client: "Client", run_id: str) -> bool:
    """Whether the run's latest status change is a system-made `crashed`.

    One read, and only when a beat lands on a crashed row (the loop then
    leaves that row alone until it changes). Raises on a failed read, which
    the caller classifies like any other recovery failure."""
    events = client.events.for_run(run_id)
    for event in events if isinstance(events, list) else []:
        if not isinstance(event, dict) or event.get("event_type") != "run.status_changed":
            continue
        payload = event.get("payload") or {}
        return payload.get("status") == "crashed" and payload.get("reason") in _SYSTEM_CRASH_REASONS
    return False
from probe.sdk.run.closing.heartbeat import _RECOVERY_RETRY  # noqa: E402 -- pieces need each other; the front door loads this one first
